import copy
import unittest
import numpy as np
import torch
from a2afm.data import windows
from a2afm.models import WindowNet,single_step
from closed_loop.core import run
from shock_validation.data import make_specs,collect,dataset
from shock_validation.metrics import validation_weights,event_metrics,summarize
from shock_validation.training import streams,sample_batch,objective,state_hash
from shock_validation.filters import filter_predictions
from shock_validation.control import run_reference


class ShockValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        cls.specs=make_specs(999,per_cell=1,smooth_count=2)
        cls.traces=collect(cls.specs); cls.data=dataset(cls.traces)

    def test_vectorization_matches_original_and_event_points_are_present(self):
        original=windows(self.traces,24,1)
        for k in original: np.testing.assert_array_equal(original[k],self.data[k])
        for j,tr in enumerate(self.traces):
            present=set(self.data['index'][self.data['trajectory']==j])
            for e in tr['events']: self.assertTrue(set(range(e['start'],e['end'])).issubset(present))

    def test_weighting_is_event_and_stratum_balanced(self):
        a,b=validation_weights(self.traces,self.data)
        self.assertAlmostEqual(a.sum(),1); self.assertAlmostEqual(b.sum(),1)
        for j,tr in enumerate(self.traces):
            self.assertAlmostEqual(b[self.data['trajectory']==j].sum(),1/len(self.traces))
            if tr['events']: self.assertAlmostEqual(a[self.data['trajectory']==j].sum(),1/6)

    def test_endpoint_auxiliary_is_whole_result_mse_and_gradient(self):
        torch.manual_seed(7); model=WindowNet(); s=torch.randn(4,24); y=torch.randn(4,24); c=torch.randn(4,75); tau=torch.rand(4,1)
        _,_,aux=objective(model,s,y,c,tau,'C'); expected=(single_step(model,s,c)-y).square().mean()
        torch.testing.assert_close(aux,expected)
        g1=torch.autograd.grad(aux,tuple(model.parameters())); g2=torch.autograd.grad(expected,tuple(model.parameters()))
        for a,b in zip(g1,g2): torch.testing.assert_close(a,b)

    def test_rng_streams_and_resume_preserve_pairing(self):
        tensors=(torch.arange(2400).reshape(100,24).float(),torch.randn(100,24),torch.randn(100,75))
        a=streams(11); b=streams(11)
        sample_batch(tensors,a); sample_batch(tensors,b)
        torch.rand((500,1),generator=b['tau'])
        saved={k:g.get_state() for k,g in a.items()}; x=sample_batch(tensors,a); z=sample_batch(tensors,b)
        for index in (0,1,2,4): torch.testing.assert_close(x[index],z[index])
        for k,g in a.items(): g.set_state(saved[k])
        replay=sample_batch(tensors,a)
        for p,q in zip(x,replay): torch.testing.assert_close(p,q)

    def test_perfect_metrics_and_single_point_shock(self):
        rows=[]
        for tr in self.traces:
            row,events=event_metrics(tr,tr['d']); rows.append(row)
            for e in events:
                for key in ('mse','area_absolute_error','extended_area_absolute_error','peak_absolute_error','peak_time_distance_s'):
                    self.assertAlmostEqual(e[key],0)
        self.assertAlmostEqual(summarize(rows)['shock_rmse'],0)

    def test_causality_filter_and_control_measurement_timing(self):
        original=run(self.specs,'none'); ours=run_reference(self.specs,'none')
        for a,b in zip(original,ours):
            for k in ('x','v','u','a_measured','dhat','command','error'): np.testing.assert_allclose(a[k],b[k],atol=1e-12)
        changed=copy.deepcopy(self.traces)
        for tr in changed:
            for k in ('x','v','u','a_measured','dhat'): tr[k][300:]+=20
        for method,p in [('ema',.5),('aug_kalman',1.)]:
            a=filter_predictions(self.traces,method,p); b=filter_predictions(changed,method,p)
            np.testing.assert_array_equal(a[:,:300],b[:,:300]); self.assertTrue(np.isfinite(a).all())

    def test_distinct_splits_and_same_model_initialization(self):
        other=make_specs(1000,per_cell=1,smooth_count=2)
        self.assertFalse({s['trajectory_id'] for s in other}&{s['trajectory_id'] for s in self.specs})
        self.assertFalse(np.array_equal(other[0]['d'],self.specs[0]['d']))
        model=WindowNet(); cloned=WindowNet(); cloned.load_state_dict(model.state_dict())
        self.assertEqual(state_hash(model.state_dict()),state_hash(cloned.state_dict()))
        self.assertEqual(sum(p.numel() for p in model.parameters()),86296)

    def test_training_forward_counts_are_matched_as_claimed(self):
        model=WindowNet(); s=torch.randn(3,24); y=torch.randn(3,24); c=torch.randn(3,75); tau=torch.rand(3,1)
        calls=[]; handle=model.register_forward_hook(lambda *args:calls.append(1))
        try:
            for method,count in [('A',1),('B',2),('C',2),('midpoint',9)]:
                calls.clear(); objective(model,s,y,c,tau,method)
                self.assertEqual(len(calls),count)
        finally: handle.remove()

    def test_bootstrap_known_effect_and_no_pseudoreplication(self):
        from analyze_shock_validation import paired_bootstrap
        a=np.ones((3,3,20)); b=.81*a
        result=paired_bootstrap(b,a,['a']*10+['b']*10,count=50)
        self.assertEqual(result['paired_trajectory_count'],20)
        self.assertAlmostEqual(result['improvement_percent'],10.)
        np.testing.assert_allclose(result['conditional_interval'],[10,10])
        np.testing.assert_allclose(result['exploratory_hierarchical_interval'],[10,10])

    def test_raw_compensation_is_causal_and_distinct_from_clipped(self):
        raw=run_reference(self.specs,'raw'); clipped=run_reference(self.specs,'raw_clipped')
        for tr in raw: np.testing.assert_allclose(tr['estimate'],tr['dhat'],atol=1e-12)
        self.assertTrue(any(not np.array_equal(a['command'],b['command']) for a,b in zip(raw,clipped)))


if __name__=='__main__': unittest.main()
