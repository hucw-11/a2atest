import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np
import torch

from a2afm.inference import DisturbanceEstimator
from a2afm.models import WindowNet, flow_loss, predict_window, single_step
from a2afm.system import SIGNAL_FAMILIES, make_trajectories, random_signals
from experiment import save_checkpoint, save_json


class SingleStepTests(unittest.TestCase):
    def test_json_retries_transient_destination_lock(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'history.json'
            real_replace=Path.replace
            attempts=[]
            def locked_once(src,dst):
                attempts.append(1)
                if len(attempts)==1: raise PermissionError('simulated scanner lock')
                return real_replace(src,dst)
            with patch.object(Path,'replace',locked_once),patch('experiment.time.sleep'):
                save_json(path,{'step':1})
            self.assertEqual(len(attempts),2)
            self.assertIn('"step": 1',path.read_text())
            self.assertEqual(list(Path(folder).iterdir()),[path])

    def test_atomic_checkpoint_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'checkpoint.pt'
            for step in range(3):
                save_checkpoint(path,dict(step=step,tensor=torch.arange(5)))
                ck=torch.load(path,weights_only=True)
                self.assertEqual(ck['step'],step)
                torch.testing.assert_close(ck['tensor'],torch.arange(5))
            self.assertEqual(list(Path(folder).iterdir()),[path])

    def test_one_call_at_initial_state_and_zero_time(self):
        model=WindowNet(8,32); s=torch.randn(4,8); c=torch.randn(4,27)
        inputs=[]
        handle=model.register_forward_pre_hook(lambda module,args: inputs.append(args))
        result=single_step(model,s,c)
        handle.remove()
        self.assertEqual(len(inputs),1)
        torch.testing.assert_close(inputs[0][2],s)
        torch.testing.assert_close(inputs[0][3],torch.zeros(4,1))
        torch.testing.assert_close(result,s+model(s,c,s,torch.zeros(4,1)))

    def test_endpoint_loss_has_two_total_calls_and_gradients(self):
        model=WindowNet(8,32); s=torch.randn(4,8); c=torch.randn(4,27); y=torch.randn_like(s)
        calls=[]
        handle=model.register_forward_hook(lambda *args: calls.append(1))
        loss,fm,end=flow_loss(model,s,y,c,predictor='single_step')
        handle.remove()
        self.assertEqual(len(calls),2)
        prediction=single_step(model,s,c)
        expected=(prediction-y).square().mean()+4*(prediction[:,0]-y[:,0]).square().mean()
        torch.testing.assert_close(end,expected)
        end.backward()
        self.assertTrue(any(p.grad is not None and p.grad.abs().sum()>0 for p in model.parameters()))

    def test_same_prediction_with_different_targets(self):
        model=WindowNet(8,32); s=torch.randn(4,8); c=torch.randn(4,27)
        outputs=[]
        handle=model.register_forward_hook(lambda module,args,out: outputs.append(out.detach().clone()))
        flow_loss(model,s,torch.zeros_like(s),c,predictor='single_step')
        flow_loss(model,s,torch.full_like(s,100),c,predictor='single_step')
        handle.remove()
        torch.testing.assert_close(outputs[1],outputs[3])

    def test_residual_regression_identity(self):
        model=WindowNet(8,32,flow=False,residual=True)
        for p in model.parameters(): torch.nn.init.zeros_(p)
        s=torch.randn(4,8); c=torch.randn(4,27)
        torch.testing.assert_close(predict_window(model,s,c),s)

    def test_mixed_signals_are_weighted_component_sum(self):
        rng=np.random.default_rng(123)
        parts=[random_signals(rng,name) for name in ('multisine','chirp','steps')]
        weights=rng.uniform(.5,1.,3); weights/=np.linalg.norm(weights)
        _,mixed=random_signals(np.random.default_rng(123),'multisine+chirp+steps')
        for t in (0.,.21,1.8,4.2):
            self.assertAlmostEqual(mixed(t,0,0),sum(w*p[1](t,0,0) for w,p in zip(weights,parts)))
        trs=make_trajectories(7,32,duration=.1,families=SIGNAL_FAMILIES)
        self.assertEqual(tuple(t['kind'] for t in trs),SIGNAL_FAMILIES)

    def test_checkpoint_deployment_uses_one_call_without_jitter(self):
        model=WindowNet(8,32)
        normalizer=dict(d_mean=0.,d_std=1.,c_mean=np.zeros(27),c_std=np.ones(27))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'model.pt'
            torch.save(dict(model=model.state_dict(),kind='a2afm',normalizer=normalizer,
                            config=dict(length=8,width=32,flow_steps=4,predictor='single_step',source_noise_std=.01)),path)
            est=DisturbanceEstimator(path); calls=[]
            hook=est.model.register_forward_hook(lambda *args: calls.append(1))
            history=np.zeros(8)
            a=est.estimate(history,history,history,history,[1,.6,2])
            self.assertEqual(len(calls),1)
            b=est.estimate(history,history,history,history,[1,.6,2])
            hook.remove()
            np.testing.assert_array_equal(a[1],b[1])


if __name__=='__main__': unittest.main()
