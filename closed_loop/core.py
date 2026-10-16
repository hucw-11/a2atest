import numpy as np
import torch
from scipy.linalg import expm
from a2afm.models import integrate

DT=.02
LENGTH=24

def reference(t):
    w=2*np.pi*.15
    return .4*np.sin(w*t),.4*w*np.cos(w*t),-.4*w*w*np.sin(w*t)

def scenarios(n,seed,kind='mixed',duration=12.,sigma=.5):
    rng=np.random.default_rng(seed); t=np.arange(round(duration/DT)+1)*DT
    result=[]
    for j in range(n):
        params=np.array([rng.uniform(.8,1.2),rng.uniform(.3,1.),rng.uniform(1.,3.)])
        family=kind if kind!='mixed' else ['smooth','pulse_1','pulse_4','pulse_10'][j%4]
        d=.3*np.sin(2*np.pi*rng.uniform(.2,.8)*t+rng.uniform(-np.pi,np.pi))
        events=[]
        if family!='smooth':
            width={'pulse_1':1,'pulse_4':4,'pulse_10':10}[family]
            for at,sign in [(rng.uniform(2.5,3.5),1),(rng.uniform(6.5,7.5),-1)]:
                start=int(round(at/DT)); area=float(rng.uniform(.15,.35))
                amplitude=sign*area/(width*DT)
                d[start:start+width]+=amplitude
                events.append(dict(start=start,end=start+width,amplitude=amplitude,area=sign*area,width_s=width*DT))
        result.append(dict(t=t,d=d,params=params,eps=rng.normal(0,sigma,len(t)),sigma_a=sigma,
                           dt=DT,kind=family,events=events,trajectory_id=f'{seed}:{j}',initial=np.zeros(2)))
    return result

def matrices(params):
    result=[]
    for m,c,k in params:
        aug=np.array([[0,1,0],[-k/m,-c/m,1/m],[0,0,0.]])
        e=expm(aug*DT); result.append(e)
    e=np.array(result)
    return e[:,:2,:2],e[:,:2,2]

def neural_prediction(estimator,history,params):
    # Each channel is oldest to newest. Stored u is the input at acceleration sampling.
    x,v,u,a=history.transpose(2,0,1)
    m,c,k=params.T
    source=m[:,None]*a+c[:,None]*v+k[:,None]*x-u
    condition=np.concatenate([x,v,u,params],axis=1)
    norm=estimator.norm.state
    s=torch.as_tensor((source-norm['d_mean'])/norm['d_std'],dtype=torch.float32)
    cond=torch.as_tensor((condition-norm['c_mean'])/norm['c_std'],dtype=torch.float32)
    with torch.inference_mode():
        model=estimator.model
        y=integrate(model,s,cond,estimator.steps) if model.flow else model(s,cond)
    return estimator.norm.invert(y.numpy())[:,0]

def run(specs,method='none',estimator=None,bandwidth=12.,kalman_q=1e4,
        kp=16.,kd=8.,limit=12.,comp_limit=12.,closed=True):
    """Measure using held u(k-1), update observer, then apply u(k) over next interval.

    Disturbance is defined piecewise constant on intervals; exact ZOH transition.
    No observer has access to true d. Truth is used only by the simulated plant.
    """
    n=len(specs); steps=len(specs[0]['t']); params=np.array([s['params'] for s in specs])
    m,c,k=params.T; ad,bd=matrices(params)
    state=np.array([s['initial'] for s in specs]); held=np.zeros(n)
    history=np.zeros((n,LENGTH,4)); dob=np.zeros(n)
    kstate=np.zeros((n,2)); covariance=np.tile(np.eye(2)*10,(n,1,1))
    F=np.array([[1,DT],[0,1.]])
    G=np.array([DT*DT/2,DT]); Q=kalman_q*np.outer(G,G)
    R=np.array([(s['params'][0]*s['sigma_a'])**2 for s in specs])
    traces=np.zeros((n,steps,10))
    alpha=1-np.exp(-bandwidth*DT)
    for i,t in enumerate(specs[0]['t']):
        truth=np.array([s['d'][i] for s in specs]); eps=np.array([s['eps'][i] for s in specs])
        x,v=state.T
        a=(held+truth-c*v-k*x)/m+eps
        residual=m*a+c*v+k*x-held
        history=np.roll(history,-1,axis=1); history[:,-1]=np.stack([x,v,held,a],axis=1)
        if method=='dob':
            dob=(1-alpha)*dob+alpha*residual; estimate=dob.copy()
        elif method=='kalman':
            kstate=kstate@F.T; covariance=F@covariance@F.T+Q
            gain=covariance[:,:,0]/(covariance[:,0,0]+R)[:,None]
            kstate+=gain*(residual-kstate[:,0])[:,None]
            # Joseph covariance update keeps symmetry and positivity.
            M=np.tile(np.eye(2),(n,1,1)); M[:,:,0]-=gain
            covariance=M@covariance@M.transpose(0,2,1)+R[:,None,None]*gain[:,:,None]*gain[:,None,:]
            estimate=kstate[:,0].copy()
        elif method in ['a2afm','regression']:
            estimate=neural_prediction(estimator,history,params) if i>=LENGTH-1 else np.zeros(n)
        elif method=='none': estimate=np.zeros(n)
        else: raise ValueError(method)
        # All methods activate compensation after identical history warmup.
        compensation=np.clip(estimate,-comp_limit,comp_limit) if i>=LENGTH-1 else np.zeros(n)
        r,rv,ra=reference(t)
        nominal=c*v+k*x+m*(ra+kd*(rv-v)+kp*(r-x))
        cmd=np.clip(nominal-compensation,-limit,limit) if closed else np.full(n,.7*np.sin(2*np.pi*.3*t))
        traces[:,i]=np.stack([x,v,held,a,residual,estimate,cmd,x-r,compensation,nominal-compensation],axis=1)
        state=np.einsum('nij,nj->ni',ad,state)+bd*(cmd+truth)[:,None]
        held=cmd
    output=[]
    for j,s in enumerate(specs):
        tr=dict(s)
        for col,name in enumerate(['x','v','u','a_measured','dhat','estimate','command','error','compensation','unsaturated_command']):
            tr[name]=traces[j,:,col]
        output.append(tr)
    return output

def measures(tr):
    valid=tr['t']>=1.; e=tr['error'][valid]; u=tr['command'][valid]
    out=dict(d_rmse=float(np.sqrt(np.mean((tr['estimate'][valid]-tr['d'][valid])**2))),
             tracking_rmse=float(np.sqrt(np.mean(e**2))),peak_error=float(np.max(abs(e))),
             u_rms=float(np.sqrt(np.mean(u*u))),u_peak=float(np.max(abs(u))),
             du_rms=float(np.sqrt(np.mean(np.diff(u)**2))),saturation_fraction=float(np.mean(abs(u)>=12.-1e-8)))
    shock_errors=[]; areas=[]; peak_ratios=[]; recoveries=[]
    for event in tr['events']:
        a,b=event['start'],event['end']; stop=min(len(tr['t']),b+100)
        shock_errors.extend((tr['estimate'][a:b]-tr['d'][a:b])**2)
        # Recovery is error within 0.02 for an entire 0.5-second interval, searched up to 2s.
        recovered=np.nan
        for i in range(b,stop-24):
            if np.all(abs(tr['error'][i:i+25])<=.02): recovered=(i-b)*DT; break
        recoveries.append(recovered)
        areas.append(float(np.sum(tr['estimate'][a:b]-tr['d'][a:b])*DT))
        peak_ratios.append(float(np.max(np.sign(event['amplitude'])*tr['estimate'][a:b])/abs(event['amplitude'])))
    out['shock_rmse']=float(np.sqrt(np.mean(shock_errors))) if shock_errors else None
    out['shock_area_abs_error']=float(np.mean(abs(np.array(areas)))) if areas else None
    out['shock_peak_ratio']=float(np.mean(peak_ratios)) if peak_ratios else None
    finite=[r for r in recoveries if np.isfinite(r)]
    out['recovery_s']=float(np.mean(finite)) if finite else None
    out['recovery_fail_fraction']=float(1-len(finite)/len(recoveries)) if recoveries else None
    return out
