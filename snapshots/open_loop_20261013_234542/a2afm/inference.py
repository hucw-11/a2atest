"""Load only your own trusted checkpoint files."""
import numpy as np
import torch
from .models import WindowNet,integrate
from .data import Normalizer


class DisturbanceEstimator:
    def __init__(self,checkpoint,device='cpu',steps=None):
        ck=torch.load(checkpoint,map_location=device,weights_only=False)
        cfg=ck['config']; self.length=cfg['length']; self.device=device
        self.steps=cfg['flow_steps'] if steps is None else steps
        self.norm=Normalizer(state=ck['normalizer'])
        self.model=WindowNet(self.length,cfg['width'],ck['kind']!='regression').to(device)
        self.model.load_state_dict(ck['model']); self.model.eval()

    def estimate(self,x,v,u,a_measured,params):
        """Pass exactly L historical samples, oldest -> current. Returns d_t, future vector."""
        arrays=[np.asarray(a,dtype=np.float32) for a in [x,v,u,a_measured]]
        if any(a.shape!=(self.length,) for a in arrays):
            raise ValueError(f'Each history must have shape ({self.length},)')
        if any(not np.isfinite(a).all() for a in arrays): raise ValueError('Nonfinite input')
        x,v,u,a=arrays; params=np.asarray(params,dtype=np.float32)
        if params.shape!=(3,) or not np.isfinite(params).all() or params[0]<=0:
            raise ValueError('params must be [m,c,kappa], with m>0')
        m,c,k=params; dhat=m*a+c*v+k*x-u
        data={'source':dhat[None], 'target':np.zeros((1,self.length),np.float32),
              'condition':np.r_[x,v,u,params][None]}
        source,_,condition=self.norm.tensors(data,self.device)
        with torch.no_grad():
            output=integrate(self.model,source,condition,self.steps) if self.model.flow else self.model(source,condition)
        future=self.norm.invert(output.cpu().numpy())[0]
        return float(future[0]),future
