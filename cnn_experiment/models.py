"""Matched-size temporal CNN and existing dense network factories."""
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from a2afm.models import WindowNet, integrate
from a2afm.data import Normalizer


class CausalConv(nn.Conv1d):
    def forward(self, x):
        return super().forward(F.pad(x, (self.dilation[0]*(self.kernel_size[0]-1), 0)))


class ChannelNorm(nn.Module):
    def __init__(self, channels):
        super().__init__(); self.norm=nn.LayerNorm(channels)

    def forward(self, x):
        return self.norm(x.transpose(1,2)).transpose(1,2)


class TemporalBlock(nn.Module):
    def __init__(self, channels, dilation):
        super().__init__()
        self.net=nn.Sequential(ChannelNorm(channels),
            CausalConv(channels,channels,3,dilation=dilation),nn.SiLU(),
            CausalConv(channels,channels,3,dilation=dilation))

    def forward(self,x):
        return x+.5*self.net(x)


class TemporalCNN(nn.Module):
    """Causal temporal features, flattened dense readout to future coordinates.

    A future output index is NOT a historical input index. Therefore retain
    ordered features and use a shared 80-wide readout, rather than interpreting
    each convolution position as the same-time target. The three residual
    blocks have dilations 1/2/4 and receptive field 29, covering all 24 inputs.
    The CNN backbone has 32 channels; the readout is dense (not a fully
    convolutional architecture). Same bounded final LayerNorm as the dense
    baseline; no change to the FM bridge or integration scheme.
    """
    def __init__(self,length=24,flow=True,channels=32,head_width=80):
        super().__init__(); self.length=length; self.flow=flow
        self.register_buffer('position',torch.linspace(-1,1,length).view(1,1,length))
        self.features=nn.Sequential(nn.Conv1d(13 if flow else 8,channels,1),nn.SiLU(),
            TemporalBlock(channels,1),TemporalBlock(channels,2),TemporalBlock(channels,4))
        self.readout=nn.Sequential(nn.Flatten(),nn.Linear(channels*length,head_width),
            nn.SiLU(),nn.LayerNorm(head_width),nn.Linear(head_width,length))

    def forward(self,source,condition,z=None,tau=None):
        n=len(source); length=self.length
        history=condition[:,:3*length].reshape(n,3,length)
        params=condition[:,3*length:,None].expand(-1,-1,length)
        pieces=[source[:,None,:],history,params,self.position.expand(n,-1,-1)]
        if self.flow:
            times=torch.cat([tau,torch.sin(torch.pi*tau),torch.cos(torch.pi*tau),tau*tau],dim=1)
            pieces.extend([z[:,None,:],times[:,:,None].expand(-1,-1,length)])
        return self.readout(self.features(torch.cat(pieces,dim=1)))


METHODS=['mlp_a2afm','mlp_regression','cnn_a2afm','cnn_regression']


def make_model(method):
    if method not in METHODS: raise ValueError(method)
    flow=method.endswith('a2afm')
    return TemporalCNN(flow=flow) if method.startswith('cnn') else WindowNet(24,128,flow)


class Estimator:
    def __init__(self,path):
        ck=torch.load(path,map_location='cpu',weights_only=False)
        self.model=make_model(ck['method']); self.model.load_state_dict(ck['model']); self.model.eval()
        self.norm=Normalizer(state=ck['normalizer']); self.steps=4

    def estimate(self,x,v,u,a,params):
        x,v,u,a=[np.asarray(t,dtype=np.float32) for t in [x,v,u,a]]
        params=np.asarray(params,dtype=np.float32)
        if any(t.shape!=(24,) or not np.isfinite(t).all() for t in [x,v,u,a]):
            raise ValueError('Expected four finite histories of length 24')
        if params.shape!=(3,) or not np.isfinite(params).all() or params[0]<=0:
            raise ValueError('Invalid plant parameters')
        m,c,k=params
        source=m*a+c*v+k*x-u
        data={'source':source[None], 'target':np.zeros((1,24),np.float32),
              'condition':np.r_[x,v,u,params][None]}
        s,_,cond=self.norm.tensors(data)
        with torch.inference_mode():
            y=integrate(self.model,s,cond,self.steps) if self.model.flow else self.model(s,cond)
        result=self.norm.invert(y.numpy())[0]
        return float(result[0]),result
