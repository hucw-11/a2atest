import unittest
import numpy as np
from closed_loop.core import scenarios,run,matrices,DT

class ClosedTests(unittest.TestCase):
    def test_measurement_control_alignment(self):
        s=scenarios(2,11,'pulse_1'); tr=run(s,'dob')
        for t in tr:
            m,c,k=t['params']
            np.testing.assert_allclose(t['dhat'],t['d']+m*t['eps'],atol=1e-12)
            np.testing.assert_allclose(t['u'][1:],t['command'][:-1],atol=1e-12)

    def test_no_future_truth_leak(self):
        s=scenarios(2,12,'pulse_4'); a=run(s,'kalman')
        for tr in s: tr['d'][200:]+=30
        b=run(s,'kalman')
        for x,y in zip(a,b):
            np.testing.assert_equal(x['command'][:200],y['command'][:200])

    def test_pulse_area(self):
        for kind in ['pulse_1','pulse_4','pulse_10']:
            s=scenarios(1,42,kind)[0]
            for ev in s['events']:
                self.assertAlmostEqual(ev['amplitude']*ev['width_s'],ev['area'])

    def test_discrete_stability(self):
        ad,bd=matrices([[1,.6,2]])
        feedback=np.array([2-16,.6-8])
        poles=np.linalg.eigvals(ad[0]+np.outer(bd[0],feedback))
        self.assertLess(max(abs(poles)),1.)

if __name__=='__main__': unittest.main()
