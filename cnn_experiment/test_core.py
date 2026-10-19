import unittest
import numpy as np
import torch
from a2afm.data import windows
from a2afm.models import flow_loss,integrate
from cnn_experiment.models import CausalConv,make_model,METHODS
from cnn_experiment.data import trajectories,TRAIN_FAMILIES,TEST_FAMILIES,trajectory_metrics
from multichannel.core import reference_scales
from cnn_experiment.data import observations


class CNNTests(unittest.TestCase):
    def test_causal_convolution_prefix(self):
        conv=CausalConv(2,3,3,dilation=4); x=torch.randn(2,2,24)
        before=conv(x); changed=x.clone(); changed[:,:,13:]+=100
        torch.testing.assert_close(conv(changed)[:,:,:13],before[:,:,:13],rtol=0,atol=0)

    def test_model_shapes_and_endpoint_gradients(self):
        s=torch.randn(3,24); c=torch.randn(3,75); target=torch.randn(3,24)
        for name in METHODS:
            model=make_model(name)
            if model.flow:
                loss,_,end=flow_loss(model,s,target,c,steps=4)
                end.backward(); self.assertTrue(torch.isfinite(loss))
                y=integrate(model,s,c,4)
            else:
                y=model(s,c); ((y-target)**2).mean().backward()
            self.assertEqual(y.shape,(3,24))
            self.assertTrue(any(p.grad is not None and p.grad.abs().sum()>0 for p in model.parameters()))

    def test_midpoint_network_evaluation_count(self):
        model=make_model('cnn_a2afm'); count=[]
        hook=model.register_forward_hook(lambda *args:count.append(1))
        integrate(model,torch.zeros(1,24),torch.zeros(1,75),4)
        hook.remove(); self.assertEqual(len(count),8)

    def test_measurement_consistency_and_no_future_inputs(self):
        base=trajectories(4,100,TRAIN_FAMILIES); scale=reference_scales(base)
        tr=observations(base,scale,'xv_5pct',500)[1]
        m,c,k=tr['params']
        np.testing.assert_allclose(tr['dhat']-tr['d'],m*(tr['a_measured']-tr['a'])+
            c*(tr['v']-tr['v_true'])+k*(tr['x']-tr['x_true']),atol=1e-13)
        before=windows([tr],24,1); cutoff=100
        changed=dict(tr)
        for key in ['x','v','u','dhat','d']:
            changed[key]=tr[key].copy(); changed[key][cutoff+1:]+=100
        after=windows([changed],24,1); mask=before['index']<=cutoff
        np.testing.assert_array_equal(before['source'][mask],after['source'][mask])
        np.testing.assert_array_equal(before['condition'][mask],after['condition'][mask])

    def test_all_pulse_samples_scored_and_unseen_widths(self):
        data=trajectories(6,200,TEST_FAMILIES)
        self.assertNotIn('pulse_2',TRAIN_FAMILIES); self.assertNotIn('pulse_6',TRAIN_FAMILIES)
        for tr in data:
            w=windows([tr],24,1); idx=w['index']
            perfect=trajectory_metrics(tr,idx,tr['d'][idx])
            self.assertEqual(perfect['mse'],0.)
            if tr['events']:
                self.assertEqual(perfect['shock_mse'],0.)
                for ev in tr['events']:
                    self.assertAlmostEqual(np.sum(tr['d'][ev['start']:ev['end']]-
                        tr['background'][ev['start']:ev['end']])*.02,ev['area'])


if __name__=='__main__': unittest.main()
