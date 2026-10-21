import unittest
from types import SimpleNamespace
import numpy as np
from scipy.linalg import expm
from a2afm.data import Normalizer
from a2afm.models import WindowNet

from closed_loop.core import DT, run, scenarios
from closed_loop.delayed import run_delayed


class DelayedTests(unittest.TestCase):
    def test_zero_delay_matches_neural_feedback_path(self):
        estimator=SimpleNamespace(model=WindowNet(24,32),steps=4,predictor='single_step',
             norm=Normalizer(state=dict(d_mean=0.,d_std=1.,c_mean=np.zeros(75),c_std=np.ones(75))))
        specs=scenarios(2,74,duration=1.)
        a=run(specs,'a2afm',estimator); b=run_delayed(specs,'a2afm',estimator,delay_s=0.)
        for old,new in zip(a,b):
            for key in ('x','v','estimate','command'):
                np.testing.assert_allclose(old[key],new[key],atol=1e-11,rtol=1e-11)

    def test_zero_delay_matches_original_control_and_plant(self):
        specs=scenarios(3,73,duration=1.)
        a=run(specs,'none'); b=run_delayed(specs,'none',delay_s=0.)
        for old,new in zip(a,b):
            for key in ('x','v','u','command','error','dhat'):
                np.testing.assert_allclose(old[key],new[key],atol=1e-11,rtol=1e-11)

    def test_subperiod_delay_splits_exact_plant_transition(self):
        spec=scenarios(1,79,duration=DT)[0]
        spec.update(params=np.array([1.,.6,2.]),initial=np.array([1.,.2]),d=np.zeros(2),eps=np.zeros(2))
        tr=run_delayed([spec],delay_s=.005,kp=0.,kd=0.,delay_start=0)[0]
        aug=np.array([[0,1,0],[-2,-.6,1],[0,0,0.]])
        first=expm(aug*.005); second=expm(aug*.015)
        state=first[:2,:2]@spec['initial']
        state=second[:2,:2]@state+second[:2,2]*2.12
        np.testing.assert_allclose([tr['x'][1],tr['v'][1]],state,atol=1e-12)
        self.assertEqual(tr['u'][0],0.)
        self.assertAlmostEqual(tr['u'][1],2.12)

    def test_overrun_skips_new_jobs_instead_of_future_control(self):
        specs=scenarios(1,81,duration=.2)
        tr=run_delayed(specs,delay_s=2*DT,delay_start=0)[0]
        np.testing.assert_array_equal(tr['issued'],np.arange(len(tr['t']))%2==0)
        np.testing.assert_array_equal(tr['skipped'],~tr['issued'])
        self.assertEqual(tr['command'][0],0.)
        self.assertEqual(tr['command'][1],0.)

    def test_delay_simulator_has_no_future_truth_leak(self):
        specs=scenarios(1,88,duration=1.)
        a=run_delayed(specs,delay_s=.007)[0]
        specs[0]['d'][30:]+=20.
        b=run_delayed(specs,delay_s=.007)[0]
        np.testing.assert_array_equal(a['command'][:30],b['command'][:30])

    def test_invalid_delay_is_rejected(self):
        for value in (-.01,float('nan'),float('inf')):
            with self.assertRaises(ValueError): run_delayed(scenarios(1,5,duration=.1),delay_s=value)


if __name__=='__main__': unittest.main()
