"""Sample-aligned finite pulses and an exactly discretized open-loop plant."""
import numpy as np
from scipy.linalg import expm
from multichannel.core import measure

DT=.02
TRAIN_FAMILIES=['smooth','pulse_1','pulse_4','pulse_10']
TEST_FAMILIES=['smooth','pulse_1','pulse_2','pulse_4','pulse_6','pulse_10']
CONDITIONS={'clean':(0.,0.),'xv_5pct':(.05,.05)}


def trajectories(n,seed,families,sigma_a=.5):
    if n%len(families): raise ValueError('Use a multiple of the family count for balanced data')
    rng=np.random.default_rng(seed); t=np.arange(601)*DT; result=[]
    for j in range(n):
        family=families[j%len(families)]
        m,c,k=rng.uniform(.8,1.2),rng.uniform(.3,1.),rng.uniform(1.,3.)
        background=.3*np.sin(2*np.pi*rng.uniform(.2,.8)*t+rng.uniform(-np.pi,np.pi))
        d=background.copy(); events=[]
        if family!='smooth':
            width=int(family.split('_')[1])
            for at,sign in [(rng.uniform(2.5,3.5),1),(rng.uniform(6.5,7.5),-1)]:
                start=int(round(at/DT)); area=sign*rng.uniform(.15,.35); amp=area/(width*DT)
                d[start:start+width]+=amp
                events.append(dict(start=start,end=start+width,amplitude=float(amp),area=float(area),width_s=width*DT))
        u=.7*np.sin(2*np.pi*rng.uniform(.2,.5)*t+rng.uniform(-np.pi,np.pi))
        mat=np.array([[0,1,0],[-k/m,-c/m,1/m],[0,0,0.]])
        e=expm(mat*DT); a,b=e[:2,:2],e[:2,2]
        state=np.empty((len(t),2)); state[0]=rng.normal(0,.1,2)
        for i in range(len(t)-1): state[i+1]=a@state[i]+b*(u[i]+d[i])
        x,v=state.T; accel=(u+d-c*v-k*x)/m
        measured=accel+rng.normal(0,sigma_a,len(t))
        result.append(dict(t=t.copy(),x=x,v=v,u=u,d=d,background=background,a=accel,
            a_measured=measured,dhat=m*measured+c*v+k*x-u,params=np.array([m,c,k]),
            sigma_a=sigma_a,dt=DT,kind=family,events=events,trajectory_id=f'{seed}:{j}'))
    return result


def observations(base,scales,condition,seed):
    return [measure(tr,scales,CONDITIONS[condition],seed+i) for i,tr in enumerate(base)]


def metric_masks(tr,index):
    pulse=np.zeros(len(index),dtype=bool); recovery=pulse.copy()
    for event in tr['events']:
        pulse |= (index>=event['start']) & (index<event['end'])
        recovery |= (index>=event['end']) & (index<event['end']+25)
    return pulse,recovery,~(pulse|recovery)


def trajectory_metrics(tr,index,prediction):
    error=prediction-tr['d'][index]; pulse,recovery,background=metric_masks(tr,index)
    def mse(mask): return float(np.mean(error[mask]**2)) if mask.any() else None
    result=dict(mse=float(np.mean(error**2)),mae=float(np.mean(abs(error))),
        p99_abs=float(np.quantile(abs(error),.99)),shock_mse=mse(pulse),
        recovery_mse=mse(recovery),background_mse=mse(background))
    areas=[]; peaks=[]; onset_errors=[]
    for event in tr['events']:
        mask=(index>=event['start'])&(index<event['end'])
        assert mask.sum()==event['end']-event['start'], 'Pulse samples missing from evaluation'
        areas.append(abs(float(np.sum(error[mask])*DT)))
        # Includes the small sinusoidal background; descriptive, not pure impulse gain.
        peaks.append(float(np.max(np.sign(event['amplitude'])*prediction[mask])/abs(event['amplitude'])))
        onset_errors.append(float(error[index==event['start']][0]**2))
    result.update(shock_area_abs=float(np.mean(areas)) if areas else None,
                  shock_peak_ratio=float(np.mean(peaks)) if peaks else None,
                  onset_mse=float(np.mean(onset_errors)) if onset_errors else None)
    return result
