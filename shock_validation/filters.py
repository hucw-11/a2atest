"""Causal reference observers, with parameters selected only on validation data."""
import numpy as np
from closed_loop.core import DT, matrices


class AugmentedKalman:
    """State [x,v,d], random-walk disturbance; measures x,v and acceleration.

    Exact x/v are represented by variance 1e-12. R_a is the known sensor variance.
    The held input at sample k was applied over interval [k-1,k).
    """
    def __init__(self,params,sigma,q):
        self.params=np.asarray(params); n=len(params); ad,bd=matrices(self.params)
        self.F=np.tile(np.eye(3),(n,1,1)); self.F[:,:2,:2]=ad; self.F[:,:2,2]=bd
        self.B=np.zeros((n,3)); self.B[:,:2]=bd
        m,c,k=self.params.T
        self.H=np.tile(np.eye(3),(n,1,1)); self.H[:,2]=np.stack((-k/m,-c/m,1/m),axis=1)
        self.R=np.tile(np.diag([1e-12,1e-12,1.]),(n,1,1)); self.R[:,2,2]=np.asarray(sigma)**2
        self.Q=np.zeros((n,3,3)); self.Q[:,2,2]=q
        self.P=np.tile(np.eye(3)*10,(n,1,1)); self.state=np.zeros((n,3)); self.started=False

    def update(self,x,v,u,a):
        if self.started:
            self.state=np.einsum('nij,nj->ni',self.F,self.state)+self.B*np.asarray(u)[:,None]
            self.P=self.F@self.P@self.F.transpose(0,2,1)+self.Q
        self.started=True
        y=np.stack((x,v,np.asarray(a)-np.asarray(u)/self.params[:,0]),axis=1)
        hp=self.H@self.P; innovation=hp@self.H.transpose(0,2,1)+self.R
        gain=np.linalg.solve(innovation,hp).transpose(0,2,1)
        self.state+=np.einsum('nij,nj->ni',gain,y-np.einsum('nij,nj->ni',self.H,self.state))
        M=np.eye(3)-gain@self.H
        self.P=M@self.P@M.transpose(0,2,1)+gain@self.R@gain.transpose(0,2,1)
        return self.state[:,2].copy()


def filter_predictions(traces,method,param=None):
    raw=np.array([tr['dhat'] for tr in traces])
    if method=='raw': return raw
    output=np.empty_like(raw)
    if method=='ema':
        state=raw[:,0].copy()
        for i in range(raw.shape[1]):
            state=(1-param)*state+param*raw[:,i]; output[:,i]=state
    elif method=='aug_kalman':
        observer=AugmentedKalman([tr['params'] for tr in traces],[tr['sigma_a'] for tr in traces],param)
        channels={k:np.array([tr[k] for tr in traces]) for k in ('x','v','u','a_measured')}
        for i in range(raw.shape[1]): output[:,i]=observer.update(*(channels[k][:,i] for k in channels))
    else: raise ValueError(method)
    return output
