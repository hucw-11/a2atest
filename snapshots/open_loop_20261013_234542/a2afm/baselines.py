"""All filters are causal. Hyperparameters must be selected on validation only."""
import numpy as np
from scipy.signal import lfilter, savgol_coeffs


def estimate(tr,method,param=None):
    y=tr['dhat']; dt=tr['dt']; m,c,k=tr['params']
    if method=='raw': return y.copy()
    if method=='ema':
        alpha=float(param)
        return lfilter([alpha],[1,-(1-alpha)],y,zi=[(1-alpha)*y[0]])[0]
    if method=='local_poly':
        w=int(param)
        coeff=savgol_coeffs(w,2,pos=w-1,use='dot')
        out=y.copy()
        for t in range(w-1,len(y)): out[t]=coeff@y[t-w+1:t+1]
        return out
    if method=='kalman':
        # State [d, d_dot], constant-velocity prior, acceleration measurement R.
        F=np.array([[1,dt],[0,1.]])
        G=np.array([dt*dt/2,dt]); Q=float(param)*np.outer(G,G)
        R=(m*tr['sigma_a'])**2
        state=np.array([y[0],0.]); P=np.eye(2)*10
        out=np.empty_like(y)
        for t,value in enumerate(y):
            state=F@state; P=F@P@F.T+Q
            gain=P[:,0]/(P[0,0]+R)
            state=state+gain*(value-state[0])
            P=P-np.outer(gain,P[0,:]); out[t]=state[0]
        return out
    if method=='physics_backward':
        # One-sided, second-order derivative. Requires only velocity <= t.
        v=tr['v']; acc=np.zeros_like(v)
        acc[1]=(v[1]-v[0])/dt
        acc[2:]=(3*v[2:]-4*v[1:-1]+v[:-2])/(2*dt)
        return m*acc+c*tr['v']+k*tr['x']-tr['u']
    raise ValueError(method)


def tune(trajectories,data):
    grids={'ema':[.05,.1,.2,.35,.5,.7,.9],
           'local_poly':[5,9,15,23],
           'kalman':[.01,.1,1.,10.,100.,1000.,10000.]}
    chosen={}
    for method,grid in grids.items():
        scores=[]
        for param in grid:
            preds=[estimate(tr,method,param) for tr in trajectories]
            p=np.array([preds[j][i] for j,i in zip(data['trajectory'],data['index'])])
            scores.append(np.mean((p-data['target'][:,0])**2))
        chosen[method]=grid[int(np.argmin(scores))]
    return chosen
