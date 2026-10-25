"""Classical controls and fixed one-second event metrics."""
import numpy as np
from closed_loop.core import DT, LENGTH, matrices, reference, measures
from shock_validation.filters import AugmentedKalman


def run_reference(specs,method,param=None):
    params=np.array([s['params'] for s in specs]); m,c,k=params.T; ad,bd=matrices(params)
    n=len(specs); state=np.array([s['initial'] for s in specs]); held=np.zeros(n)
    filtered=None; out=np.zeros((n,len(specs[0]['t']),8))
    observer=AugmentedKalman(params,[s['sigma_a'] for s in specs],param) if method=='aug_kalman' else None
    for i,t in enumerate(specs[0]['t']):
        truth=np.array([s['d'][i] for s in specs]); eps=np.array([s['eps'][i] for s in specs])
        x,v=state.T; a=(held+truth-c*v-k*x)/m+eps; raw=m*a+c*v+k*x-held
        if method=='none': est=np.zeros(n)
        elif method in ('raw','raw_clipped'): est=raw.copy()
        elif method=='ema':
            filtered=raw.copy() if filtered is None else (1-param)*filtered+param*raw
            est=filtered.copy()
        elif method=='aug_kalman': est=observer.update(x,v,held,a)
        else: raise ValueError(method)
        cap=3. if method=='raw_clipped' else (np.inf if method=='raw' else 12.)
        comp=np.clip(est,-cap,cap) if i>=LENGTH-1 else np.zeros(n)
        r,rv,ra=reference(t); nominal=c*v+k*x+m*(ra+8*(rv-v)+16*(r-x))
        command=np.clip(nominal-comp,-12,12)
        out[:,i]=np.stack((x,v,held,a,raw,est,command,x-r),axis=1)
        state=np.einsum('nij,nj->ni',ad,state)+bd*(command+truth)[:,None]; held=command
    result=[]
    for j,s in enumerate(specs):
        tr=dict(s)
        for column,key in enumerate(('x','v','u','a_measured','dhat','estimate','command','error')): tr[key]=out[j,:,column]
        result.append(tr)
    return result


def control_metrics(tr):
    row=measures(tr)
    energies=[]; peaks=[]
    for event in tr['events']:
        error=tr['error'][event['start']:event['start']+50]
        energies.append(float(np.sum(error**2)*DT)); peaks.append(float(np.max(abs(error))))
    row.update(trajectory=tr['trajectory_id'],stratum=tr['stratum'],regime=tr['regime'],width=tr['width'],
               event_tracking_energy=float(np.mean(energies)) if energies else None,
               event_tracking_peak=float(np.mean(peaks)) if peaks else None)
    # Raw primary data stays finite JSON (old recovery statistic can be NaN).
    return {k:(None if isinstance(v,float) and not np.isfinite(v) else v) for k,v in row.items()}
