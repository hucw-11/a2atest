import unittest
import numpy as np
from a2afm.system import Plant, simulate
from a2afm.data import windows
from multichannel.core import measure, reference_scales, augmented_kalman


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.tr = simulate(Plant(), lambda t,x,v: np.sin(t),
                           lambda t,x,v: np.cos(t), duration=2., seed=83)
        self.scales = reference_scales([self.tr])

    def test_residual_uses_same_measurements_and_preserves_truth(self):
        before = {k:self.tr[k].copy() for k in ['x','v','d','a_measured','dhat']}
        noisy = measure(self.tr, self.scales, (.05,.05), 31)
        m,c,k = self.tr['params']
        np.testing.assert_allclose(noisy['dhat']-self.tr['dhat'],
            c*(noisy['v']-self.tr['v'])+k*(noisy['x']-self.tr['x']), atol=1e-14)
        for key,value in before.items(): np.testing.assert_array_equal(self.tr[key],value)
        np.testing.assert_array_equal(noisy['d'],self.tr['d'])
        w = windows([noisy]); i=w['index'][0]; hist=slice(i-23,i+1)
        np.testing.assert_allclose(w['source'][0],noisy['dhat'][hist],rtol=1e-6)
        np.testing.assert_allclose(w['condition'][0,:24],noisy['x'][hist],rtol=1e-6)

    def test_paired_channel_noise_and_clean_identity(self):
        clean = measure(self.tr,self.scales,(0,0),31)
        one = measure(self.tr,self.scales,(.01,0),31)
        both = measure(self.tr,self.scales,(.05,.05),31)
        np.testing.assert_array_equal(clean['dhat'],self.tr['dhat'])
        np.testing.assert_array_equal(one['v'],self.tr['v'])
        np.testing.assert_allclose(both['x']-self.tr['x'],5*(one['x']-self.tr['x']),atol=1e-15)

    def test_kalman_causal_and_truth_independent(self):
        noisy = measure(self.tr,self.scales,(.05,.05),31)
        original = augmented_kalman(noisy,100)
        changed = dict(noisy)
        changed['d']=noisy['d']+100
        changed['x_true']=noisy['x_true']+100
        changed['v_true']=noisy['v_true']+100
        np.testing.assert_array_equal(augmented_kalman(changed,100),original)
        for key in ['x','v','a_measured','u']:
            changed[key]=noisy[key].copy(); changed[key][60:]+=100
        np.testing.assert_array_equal(augmented_kalman(changed,100)[:60],original[:60])
        self.assertTrue(np.isfinite(original).all())

    def test_kalman_constant_disturbance_recovery(self):
        tr = simulate(Plant(),lambda t,x,v:0,lambda t,x,v:.7,duration=3,sigma_a=.01)
        measured = measure(tr,{'x':1.,'v':1.},(.001,.001),7)
        result=augmented_kalman(measured,.01)
        self.assertLess(np.sqrt(np.mean((result[50:]-.7)**2)),.03)


if __name__ == '__main__': unittest.main()
