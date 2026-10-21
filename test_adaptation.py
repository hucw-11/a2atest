import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import torch

from a2afm.inference import DisturbanceEstimator
from a2afm.models import WindowNet
from closed_loop.adaptation import collect_shared, fine_tune, mixed_specs
from experiment import save_checkpoint


class AdaptationTests(unittest.TestCase):
    def test_pulse_ablation_is_paired_and_does_not_mutate_other_inputs(self):
        base=mixed_specs(10,44); pulsed=mixed_specs(10,44,pulse_half=True)
        for j,(a,b) in enumerate(zip(base,pulsed)):
            for key in ('t','params','initial','eps'):
                np.testing.assert_array_equal(a[key],b[key])
            if j<5: np.testing.assert_array_equal(a['d'],b['d'])
            else:
                self.assertEqual(len(b['events']),2)
                difference=b['d']-a['d']
                expected=np.zeros_like(difference)
                for event in b['events']:
                    expected[event['start']:event['end']]+=event['amplitude']
                    self.assertAlmostEqual(event['amplitude']*event['width_s'],event['area'])
                np.testing.assert_allclose(difference,expected,atol=1e-12)

    def test_shared_collection_has_disjoint_policy_assignments(self):
        # Mock neural collection with a causal zero-compensation controller.
        from closed_loop.core import run
        specs=mixed_specs(10,55,duration=1.)
        with patch('closed_loop.adaptation.run',side_effect=lambda subset,*a,**k:run(subset,'none')):
            data,manifest=collect_shared(specs,{},123)
        self.assertEqual(len({r['id'] for r in manifest}),10)
        self.assertEqual(set(r['collector'] for r in manifest),{'none','dob','single_fm','midpoint_fm','regression'})
        self.assertEqual(data['source'].shape[1],24)
        self.assertEqual(data['condition'].shape[1],75)

    def test_fine_tuning_retains_parent_when_tracking_does_not_improve(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory); parent=folder/'parent.pt'
            model=WindowNet(24,32,flow=False)
            save_checkpoint(parent,dict(model=model.state_dict(),normalizer=dict(d_mean=0.,d_std=1.,
                c_mean=np.zeros(75),c_std=np.ones(75)),config=dict(length=24,width=32,flow_steps=4),kind='regression'))
            rng=np.random.default_rng(99)
            data=dict(source=rng.normal(size=(8,24)).astype(np.float32),
                      target=rng.normal(size=(8,24)).astype(np.float32),
                      condition=rng.normal(size=(8,75)).astype(np.float32))
            args=argparse.Namespace(resume=False,lr=.0002,source_noise_std=.01,
                                    round_steps=2,batch=4,validation_every=1)
            with patch('closed_loop.adaptation.closed_score',return_value=dict(tracking_rmse=1.,d_rmse=1.)),patch('closed_loop.adaptation.log'):
                est,history=fine_tune(parent,data,[],args,folder/'adapted','regression',11,1)
            self.assertEqual(len(history),3)
            for key,value in model.state_dict().items(): torch.testing.assert_close(value,est.model.state_dict()[key])
            last=torch.load(folder/'adapted/regression_seed11_round1_last.pt',weights_only=False)
            self.assertEqual(last['adaptation_step'],2)
            args.resume=True
            restored,_=fine_tune(parent,data,[],args,folder/'adapted','regression',11,1)
            self.assertIsInstance(restored,DisturbanceEstimator)


if __name__=='__main__': unittest.main()
