"""Shared closed-loop data collection and validation-selected offline adaptation."""
from pathlib import Path
import time

import numpy as np
import torch

from a2afm.data import windows
from a2afm.inference import DisturbanceEstimator
from a2afm.models import flow_loss
from a2afm.system import SIGNAL_FAMILIES, random_signals
from closed_loop.core import DT, measures, run
from experiment import log, save_checkpoint, save_json

METHODS=('single_fm','midpoint_fm','regression')


def mixed_specs(n,seed,sigma=None,duration=12.,pulse_half=False):
    """Paired base specifications; optional pulses do not alter parameters/noise."""
    rng=np.random.default_rng(seed); pulse_rng=np.random.default_rng(seed+10000000)
    t=np.arange(round(duration/DT)+1)*DT; specs=[]
    for j in range(n):
        family=SIGNAL_FAMILIES[j%len(SIGNAL_FAMILIES)]
        _,signal=random_signals(rng,family)
        params=np.array([rng.uniform(.8,1.2),rng.uniform(.3,1.),rng.uniform(1.,3.)])
        initial=rng.normal(0,.2,2)
        scale=float(rng.uniform(.2,.9)) if sigma is None else sigma
        eps=rng.normal(0,scale,len(t))
        d=np.array([signal(ti,0,0) for ti in t]); events=[]
        if pulse_half and j>=n//2:
            width=(1,4,10)[(j-n//2)%3]
            for at,sign in ((pulse_rng.uniform(2.5,3.5),1),(pulse_rng.uniform(6.5,7.5),-1)):
                start=round(at/DT); area=float(sign*pulse_rng.uniform(.15,.35))
                amplitude=area/(width*DT); d[start:start+width]+=amplitude
                events.append(dict(start=start,end=start+width,amplitude=amplitude,
                                   area=area,width_s=width*DT))
        specs.append(dict(t=t.copy(),d=d,params=params,initial=initial,eps=eps,
                          sigma_a=scale,dt=DT,events=events,kind=family,
                          trajectory_id=f'{seed}:{j}'))
    return specs


def collect_shared(specs,collectors,seed,bandwidth=24.):
    """Every competing learner receives exactly the same five-policy replay set."""
    rng=np.random.default_rng(seed); groups=np.array_split(rng.permutation(len(specs)),5)
    trajectories=[]; manifest=[]
    for policy,indices in zip(('none','dob',*METHODS),groups):
        subset=[specs[int(i)] for i in indices]
        if not subset: continue
        traces=run(subset,policy if policy in ('none','dob') else 'a2afm',
                   collectors.get(policy),bandwidth=bandwidth)
        trajectories.extend(traces)
        for spec in subset:
            manifest.append(dict(id=spec['trajectory_id'],family=spec['kind'],collector=policy,
                                 has_pulse=bool(spec['events']),events=spec['events']))
    return windows(trajectories,24,2),manifest


def closed_score(estimator,specs):
    traces=run(specs,'a2afm',estimator)
    rows=[measures(tr) for tr in traces]
    return dict(tracking_rmse=float(np.sqrt(np.mean([r['tracking_rmse']**2 for r in rows]))),
                d_rmse=float(np.sqrt(np.mean([r['d_rmse']**2 for r in rows]))))


def fine_tune(parent,data,validation,args,folder,method,seed,round_number):
    """Warm-start; select by held-out closed-loop tracking, including step 0."""
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    best_path=folder/f'{method}_seed{seed}_round{round_number}.pt'
    last_path=folder/f'{method}_seed{seed}_round{round_number}_last.pt'
    if args.resume and last_path.exists():
        finished=torch.load(last_path,map_location='cpu',weights_only=False)
        if finished['adaptation_step']==args.round_steps:
            save_json(folder/f'{method}_seed{seed}_round{round_number}_history.json',finished['adaptation_history'])
            return DisturbanceEstimator(best_path),finished['adaptation_history']
    estimator=DisturbanceEstimator(parent)
    model=estimator.model
    base=torch.load(parent,map_location='cpu',weights_only=False)
    source,target,condition=estimator.norm.tensors(data,'cpu')
    optimizer=torch.optim.AdamW(model.parameters(),lr=args.lr,weight_decay=1e-4)
    torch.manual_seed(seed+round_number*100000)
    cfg=dict(base['config']); cfg.update(adaptation_lr=args.lr,adaptation_round=round_number,
                                      source_noise_std=args.source_noise_std)
    initial=closed_score(estimator,validation)
    history=[dict(step=0,**initial)]; best=initial['tracking_rmse']; start=0
    def checkpoint(step,score):
        return dict(model=model.state_dict(),normalizer=base['normalizer'],config=cfg,
                    kind=base['kind'],seed=seed,step=step,val_rmse=score['d_rmse'],
                    tracking_score=score['tracking_rmse'],parent=str(parent),
                    adaptation_step=step,adaptation_round=round_number)
    if args.resume and last_path.exists():
        ck=torch.load(last_path,map_location='cpu',weights_only=False)
        model.load_state_dict(ck['model']); optimizer.load_state_dict(ck['optimizer'])
        torch.set_rng_state(ck['rng']); start=ck['adaptation_step']
        history=ck['adaptation_history']; best=ck['best_tracking_score']
    else:
        save_checkpoint(best_path,checkpoint(0,initial))
    begin=time.perf_counter()
    for step in range(start+1,args.round_steps+1):
        model.train(); idx=torch.randint(len(source),(args.batch,))
        s=source[idx]; y=target[idx]; c=condition[idx]
        if args.source_noise_std: s=s+args.source_noise_std*torch.randn_like(s)
        optimizer.zero_grad(set_to_none=True)
        if model.flow:
            loss,fm,end=flow_loss(model,s,y,c,predictor=estimator.predictor)
        else:
            pred=model(s,c); fm=pred.new_zeros(())
            end=(pred-y).square().mean()+4*(pred[:,0]-y[:,0]).square().mean(); loss=end
        if not torch.isfinite(loss): raise RuntimeError('Nonfinite adaptation loss')
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.); optimizer.step()
        if step%args.validation_every==0 or step==args.round_steps:
            model.eval(); score=closed_score(estimator,validation)
            history.append(dict(step=step,loss=float(loss.detach()),fm_loss=float(fm.detach()),
                                result_loss=float(end.detach()),**score))
            ck=checkpoint(step,score)
            if score['tracking_rmse']<best:
                best=score['tracking_rmse']; save_checkpoint(best_path,ck)
            save_checkpoint(last_path,{**ck,'optimizer':optimizer.state_dict(),'rng':torch.get_rng_state(),
                             'best_tracking_score':best,'adaptation_history':history})
            save_json(folder/f'{method}_seed{seed}_round{round_number}_history.json',history)
            log(f'adapt {folder.name} {method}/{seed} round={round_number} step={step} '
                f'val_tracking={score["tracking_rmse"]:.6f} best={best:.6f}')
    log(f'adapt completed {folder.name} {method}/{seed} round={round_number}, '
        f'seconds={time.perf_counter()-begin:.1f}')
    return DisturbanceEstimator(best_path),history
