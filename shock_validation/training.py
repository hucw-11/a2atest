"""Paired CPU training, independent random streams, resumable complete state."""
import copy
import hashlib
import time
from pathlib import Path

import numpy as np
import torch

from a2afm.models import WindowNet, predict_window
from experiment import save_checkpoint, save_json
from shock_validation.metrics import validation_score


def state_hash(state):
    h=hashlib.sha256()
    for key,value in state.items(): h.update(key.encode()); h.update(value.detach().numpy().tobytes())
    return h.hexdigest()


def streams(seed):
    return {key:torch.Generator().manual_seed(seed+offset) for key,offset in
            [('batch',10000),('augmentation',20000),('tau',30000)]}


def sample_batch(tensors,generators,batch=128,noise=.01):
    source,target,condition=tensors
    idx=torch.randint(len(source),(batch,),generator=generators['batch'])
    s=source[idx]+noise*torch.randn((batch,24),generator=generators['augmentation'])
    tau=torch.rand((batch,1),generator=generators['tau'])
    return s,target[idx],condition[idx],tau,idx


def objective(model,s,y,c,tau,method):
    predictor='midpoint' if method=='midpoint' else 'single_step'
    pred=predict_window(model,s,c,4,predictor)
    result=(pred-y).square().mean()+4*(pred[:,0]-y[:,0]).square().mean()
    aux=result.new_zeros(())
    if method in ('B','midpoint'):
        aux=(model(s,c,(1-tau)*s+tau*y,tau)-(y-s)).square().mean()
    elif method=='C':
        aux=(model(s,c,s,torch.zeros_like(tau))-(y-s)).square().mean()
    elif method=='D':
        aux=(model(s,c,s,tau)-(y-s)).square().mean()
    return result+aux,result,aux


def predict_current(model,tensors,norm,method,batch=4096):
    source,_,condition=tensors; output=[]; model.eval()
    with torch.inference_mode():
        for i in range(0,len(source),batch):
            output.append(predict_window(model,source[i:i+batch],condition[i:i+batch],4,
                          'midpoint' if method=='midpoint' else 'single_step')[:,0].numpy())
    return norm.invert(np.concatenate(output))


def train_group(folder,tensors,validation,val_data,weights,norm,seed,cfg,methods):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    done=folder/f'seed{seed}_training.json'; resume=folder/f'seed{seed}_resume.pt'
    if done.exists(): return
    torch.manual_seed(seed); initial=WindowNet(); initial_state=copy.deepcopy(initial.state_dict())
    models={}; optimizers={}; histories={}; best={}; seconds={}; initial_hashes={}
    for method in methods:
        if method=='direct':
            torch.manual_seed(seed); model=WindowNet(flow=False)
        else:
            model=WindowNet(); model.load_state_dict(initial_state)
        models[method]=model; optimizers[method]=torch.optim.AdamW(model.parameters(),lr=cfg['lr'],weight_decay=1e-4)
        histories[method]=[]; best[method]=float('inf'); seconds[method]=0.
        initial_hashes[method]=state_hash(model.state_dict())
    generators=streams(seed); start=0
    if resume.exists():
        ck=torch.load(resume,weights_only=False)
        if ck['cfg']!=cfg or ck['methods']!=methods: raise ValueError('Resume configuration changed')
        for method in methods:
            models[method].load_state_dict(ck['models'][method]); optimizers[method].load_state_dict(ck['optimizers'][method])
        for key,g in generators.items(): g.set_state(ck['rng'][key])
        histories,best,seconds,start=ck['histories'],ck['best'],ck['seconds'],ck['step']
    def checkpoint(method,step,score):
        return dict(model=models[method].state_dict(),normalizer=norm.state,
                    config=dict(length=24,width=128,flow_steps=4,predictor='midpoint' if method=='midpoint' else 'single_step'),
                    kind='regression' if method=='direct' else 'a2afm',seed=seed,step=step,
                    method=method,validation=score,initial_hash=initial_hashes[method])
    for step in range(start+1,cfg['updates']+1):
        s,y,c,tau,idx=sample_batch(tensors,generators,cfg['batch'],cfg['source_noise'])
        for method in methods:
            model=models[method]; model.train(); optimizer=optimizers[method]
            begin=time.perf_counter(); optimizer.zero_grad(set_to_none=True)
            loss,result,aux=objective(model,s,y,c,tau,method)
            if not torch.isfinite(loss): raise RuntimeError('Nonfinite loss')
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.); optimizer.step()
            seconds[method]+=time.perf_counter()-begin
        if step%cfg['validation_every']==0 or step==cfg['updates']:
            for method in methods:
                pred=predict_current(models[method],validation,norm,method)
                score=validation_score(pred,val_data['target'],weights)
                histories[method].append(dict(step=step,training_seconds=seconds[method],**score))
                if score['score']<best[method]:
                    best[method]=score['score']; save_checkpoint(folder/f'{method}_seed{seed}.pt',checkpoint(method,step,score))
            save_checkpoint(resume,dict(cfg=cfg,methods=methods,step=step,models={m:v.state_dict() for m,v in models.items()},
                optimizers={m:v.state_dict() for m,v in optimizers.items()},histories=histories,best=best,seconds=seconds,
                rng={k:g.get_state() for k,g in generators.items()}))
            save_json(folder/f'seed{seed}_history.json',histories)
            print(f'{folder.name} seed={seed} step={step} '+ ' '.join(f'{m}={best[m]:.5f}' for m in methods),flush=True)
    # Equal measured optimizer time control: same A trajectory through primary horizon,
    # then continue A until its accumulated optimizer time reaches B's budget.
    if 'A' in models and 'B' in models:
        method='A'; step=cfg['updates']; target_seconds=seconds['B']
        best_ck=torch.load(folder/f'A_seed{seed}.pt',weights_only=False); best_ck['method']='A_time'
        save_checkpoint(folder/f'A_time_seed{seed}.pt',best_ck)
        timed_history=copy.deepcopy(histories['A']); timed_seconds=seconds['A']; timed_best=best['A']
        # Preserve the primary A timing and history; this budget is supplementary.
        while timed_seconds<target_seconds:
            s,y,c,tau,idx=sample_batch(tensors,generators,cfg['batch'],cfg['source_noise'])
            model=models['A']; model.train(); optimizer=optimizers['A']; begin=time.perf_counter()
            optimizer.zero_grad(set_to_none=True); loss,_,_=objective(model,s,y,c,tau,'A')
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.); optimizer.step()
            timed_seconds+=time.perf_counter()-begin; step+=1
            if step%cfg['validation_every']==0 or timed_seconds>=target_seconds:
                score=validation_score(predict_current(model,validation,norm,'A'),val_data['target'],weights)
                timed_history.append(dict(step=step,training_seconds=timed_seconds,**score))
                if score['score']<timed_best:
                    timed_best=score['score']; ck=checkpoint('A',step,score); ck['method']='A_time'
                    save_checkpoint(folder/f'A_time_seed{seed}.pt',ck)
        histories['A_time']=timed_history; seconds['A_time']=timed_seconds
    summary={m:dict(steps=histories[m][-1]['step'],training_seconds=seconds[m],
        initial_hash=initial_hashes.get(m,initial_hashes.get('A')),parameters=sum(p.numel() for p in models.get(m,models.get('A')).parameters()),
        train_forward_calls_per_update={'A':1,'B':2,'C':2,'D':2,'direct':1,'midpoint':9,'A_time':1}[m],
        selected_step=torch.load(folder/f'{m}_seed{seed}.pt',weights_only=False)['step']) for m in histories}
    save_json(folder/f'seed{seed}_history.json',histories); save_json(done,summary)
    print(f'{folder.name} seed={seed} TRAINING COMPLETE',flush=True)
