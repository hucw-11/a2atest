"""Sampled sensing, delayed control completion, and exact piecewise ZOH dynamics."""
import numpy as np
from scipy.linalg import expm

from closed_loop.core import DT, LENGTH, measures, neural_prediction, reference


def run_delayed(specs,method='none',estimator=None,delay_s=0.,kp=16.,kd=8.,
                limit=12.,comp_limit=12.,delay_start=LENGTH-1):
    """One nonpreemptive worker; busy samples are collected but no jobs are queued.

    Delays describe sensor-to-actuator completion, not a sleep in the simulator.
    Measurements use held control just before events at a sampling boundary.
    Completions exactly on that boundary apply after measurement, before a new job.
    A subperiod completion splits the plant transition into old/new-control pieces.
    Plants are independent; batching only accelerates simulated arithmetic.
    """
    if method not in ('none','a2afm','regression'): raise ValueError('Unsupported delayed observer')
    n=len(specs); count=len(specs[0]['t'])
    delay=np.broadcast_to(np.asarray(delay_s,dtype=float),(count,)).copy()
    if not np.isfinite(delay).all() or (delay<0).any(): raise ValueError('Delay must be finite and nonnegative')
    if any(len(s['t'])!=count or not np.allclose(np.diff(s['t']),DT) for s in specs):
        raise ValueError('All specifications must use the same 20ms sample grid')
    params=np.array([s['params'] for s in specs]); m,c,k=params.T
    state=np.array([s['initial'] for s in specs]); held=np.zeros(n)
    history=np.zeros((n,LENGTH,4)); available_estimate=np.zeros(n)
    pending=None; transition_cache={}; traces=np.zeros((n,count,9))
    issued=np.zeros(count,dtype=bool); skipped=np.zeros(count,dtype=bool)
    energy=np.zeros((n,count)); saturation=np.zeros((n,count)); peaks=np.zeros((n,count))
    def advance(duration,truth):
        nonlocal state
        if duration<=1e-13: return
        duration=round(float(duration),12)
        if duration not in transition_cache:
            transitions=[]
            for mass,damping,stiffness in params:
                aug=np.array([[0,1,0],[-stiffness/mass,-damping/mass,1/mass],[0,0,0.]])
                transitions.append(expm(aug*duration))
            matrices=np.array(transitions)
            transition_cache[duration]=(matrices[:,:2,:2],matrices[:,:2,2])
        ad,bd=transition_cache[duration]
        state=np.einsum('nij,nj->ni',ad,state)+bd*(held+truth)[:,None]
    for i,t in enumerate(specs[0]['t']):
        truth=np.array([s['d'][i] for s in specs]); eps=np.array([s['eps'][i] for s in specs])
        x,v=state.T.copy(); measured_held=held.copy()
        a=(measured_held+truth-c*v-k*x)/m+eps
        residual=m*a+c*v+k*x-measured_held
        history=np.roll(history,-1,axis=1); history[:,-1]=np.stack((x,v,measured_held,a),axis=1)
        if pending is not None and pending[0]<=t+1e-12:
            _,held,available_estimate=pending; pending=None
        if pending is None:
            issued[i]=True
            estimate=neural_prediction(estimator,history,params) if method!='none' and i>=LENGTH-1 else np.zeros(n)
            compensation=np.clip(estimate,-comp_limit,comp_limit) if i>=LENGTH-1 else np.zeros(n)
            r,rv,ra=reference(t)
            nominal=c*v+k*x+m*(ra+kd*(rv-v)+kp*(r-x))
            cmd=np.clip(nominal-compensation,-limit,limit)
            latency=delay[i] if i>=delay_start else 0.
            pending=(t+latency,cmd,estimate)
            if latency<=1e-12:
                _,held,available_estimate=pending; pending=None
        else:
            skipped[i]=True
        r,_,_=reference(t)
        traces[:,i]=np.stack((x,v,measured_held,a,residual,available_estimate,held,x-r,
                              np.clip(available_estimate,-comp_limit,comp_limit)),axis=1)
        old=held.copy()
        split=pending is not None and pending[0]<t+DT-1e-12
        h1=float(pending[0]-t) if split else DT
        advance(h1,truth)
        if split:
            _,held,available_estimate=pending; pending=None
            advance(DT-h1,truth)
        h2=DT-h1
        energy[:,i]=(old*old*h1+held*held*h2)/DT
        saturation[:,i]=((abs(old)>=limit-1e-8)*h1+(abs(held)>=limit-1e-8)*h2)/DT
        peaks[:,i]=np.maximum(abs(old),abs(held))
    output=[]
    for j,s in enumerate(specs):
        tr=dict(s)
        for col,name in enumerate(('x','v','u','a_measured','dhat','estimate','command','error','compensation')):
            tr[name]=traces[j,:,col]
        tr.update(delay_s=delay.copy(),issued=issued.copy(),skipped=skipped.copy(),
                  interval_u_squared=energy[j],interval_saturation=saturation[j],interval_u_peak=peaks[j])
        output.append(tr)
    return output


def delayed_measures(tr):
    result=measures(tr)
    valid=(tr['t']>=1.) & (np.arange(len(tr['t']))<len(tr['t'])-1)
    result.update(u_rms=float(np.sqrt(np.mean(tr['interval_u_squared'][valid]))),
                  u_peak=float(np.max(tr['interval_u_peak'][valid])),
                  saturation_fraction=float(np.mean(tr['interval_saturation'][valid])),
                  skipped_fraction=float(np.mean(tr['skipped'][valid])))
    return result
