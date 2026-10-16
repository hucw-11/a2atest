import unittest
import numpy as np
import torch
from a2afm.system import Plant,simulate
from a2afm.data import windows
from a2afm.models import WindowNet,flow_loss,integrate

class CoreTests(unittest.TestCase):
    def test_noiseless_residual(self):
        tr=simulate(Plant(1.2,.5,2.3),lambda t,x,v:np.sin(t),lambda t,x,v:np.cos(2*t),duration=1,sigma_a=0)
        np.testing.assert_allclose(tr['dhat'],tr['d'],atol=1e-12)

    def test_noise_amplification(self):
        p=Plant(1.3,.5,2.)
        tr=simulate(p,lambda t,x,v:0,lambda t,x,v:0,duration=1,sigma_a=.7)
        np.testing.assert_allclose(tr['dhat']-tr['d'],p.m*(tr['a_measured']-tr['a']),atol=1e-12)

    def test_window_alignment_and_causality(self):
        tr=simulate(Plant(),lambda t,x,v:t,lambda t,x,v:2*t,duration=1)
        a=windows([tr],8,1); t=a['index'][0]
        np.testing.assert_equal(a['source'][0],tr['dhat'][t-7:t+1].astype(np.float32))
        np.testing.assert_equal(a['target'][0],tr['d'][t:t+8].astype(np.float32))
        for key in ['x','v','u','dhat','d']:
            tr[key][t+1:]+=100
        b=windows([tr],8,1)
        np.testing.assert_equal(a['source'][0],b['source'][0])
        np.testing.assert_equal(a['condition'][0],b['condition'][0])
        self.assertEqual(a['target'][0,0],b['target'][0,0])
        self.assertNotEqual(a['target'][0,1],b['target'][0,1])

    def test_endpoint_gradients(self):
        net=WindowNet(8,32); s=torch.randn(4,8); c=torch.randn(4,27); y=torch.randn(4,8)
        loss,fm,end=flow_loss(net,s,y,c,steps=2)
        end.backward()
        self.assertTrue(any(p.grad is not None and p.grad.abs().sum()>0 for p in net.parameters()))
        self.assertTrue(torch.isfinite(loss))
        self.assertEqual(integrate(net,s,c,2).shape,y.shape)

    def test_simulation_analytic(self):
        # m=1,c=2,k=1, x(0)=1,v(0)=0 -> x=(1+t)*exp(-t).
        tr=simulate(Plant(1,2,1),lambda t,x,v:0,lambda t,x,v:0,duration=2,initial=(1,0),sigma_a=0)
        np.testing.assert_allclose(tr['x'],(1+tr['t'])*np.exp(-tr['t']),atol=1e-9)

if __name__=='__main__': unittest.main()
