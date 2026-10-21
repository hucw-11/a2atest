"""Reproducible train/evaluate pipeline; run with --help for configuration."""
import argparse
import csv
import json
import hashlib
import os
from pathlib import Path
import time
import uuid
from datetime import datetime,timezone,timedelta
import numpy as np
import torch
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parent/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from a2afm.system import make_trajectories
from a2afm.data import windows,Normalizer
from a2afm.models import WindowNet,integrate,flow_loss,predict_window
from a2afm.baselines import estimate,tune

ROOT=Path(__file__).resolve().parent

def log(message):
    stamp=datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S UTC+8')
    line=f'[{stamp}] {message}'
    print(line,flush=True)
    with (ROOT/'WORK_LOG.md').open('a',encoding='utf-8') as f: f.write('\n- '+line+'\n')

def save_json(path,obj):
    path=Path(path); tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(path)

def save_checkpoint(path,payload):
    """Atomic checkpoint replacement; tolerate short Windows scanner file locks."""
    path=Path(path)
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        # A Python file handle avoids the native torch path opener on Windows.
        with tmp.open('wb') as stream:
            torch.save(payload,stream)
        for attempt in range(20):
            try:
                tmp.replace(path)
                return
            except PermissionError:
                if attempt==19: raise
                time.sleep(.1)
    finally:
        if tmp.exists(): tmp.unlink()


def predict(model,tensors,steps=4,batch=512,predictor='midpoint'):
    src,_,cond=tensors; output=[]
    model.eval()
    with torch.no_grad():
        for i in range(0,len(src),batch):
            s=src[i:i+batch]; c=cond[i:i+batch]
            output.append(predict_window(model,s,c,steps,predictor).cpu().numpy())
    return np.concatenate(output)

def train(args,kind,seed,train_data,val_data,norm,device,out):
    torch.manual_seed(seed); np.random.seed(seed)
    model=WindowNet(args.length,args.width,kind not in ['regression','residual'],residual=kind=='residual').to(device)
    predictor=getattr(args,'predictor','midpoint')
    source_noise_std=getattr(args,'source_noise_std',0.)
    optimizer=torch.optim.AdamW(model.parameters(),lr=args.lr,weight_decay=1e-4)
    tensors=norm.tensors(train_data,device); validation=norm.tensors(val_data,device)
    source,target,condition=tensors
    path=out/f'{kind}_seed{seed}.pt'; last=out/f'{kind}_seed{seed}_last.pt'
    history=[]; best=float('inf'); start=0
    if args.resume and last.exists():
        ck=torch.load(last,map_location=device,weights_only=False)
        if ck['config']!=vars(args):
            # Output directory and resume flag can change without invalidating parameters.
            for key in ['length','width','lr','batch','flow_steps','steps','train_trajectories']:
                if ck['config'][key]!=vars(args)[key]: raise ValueError(f'Resume config mismatch: {key}')
            for key,default in [('predictor','midpoint'),('source_noise_std',0.)]:
                if ck['config'].get(key,default)!=vars(args).get(key,default):
                    raise ValueError(f'Resume config mismatch: {key}')
        if ck['normalizer'].keys()!=norm.state.keys() or any(
                not np.array_equal(ck['normalizer'][key],value) for key,value in norm.state.items()):
            raise ValueError('Resume normalizer mismatch; use the original training data')
        model.load_state_dict(ck['model']); optimizer.load_state_dict(ck['optimizer'])
        start=ck['step']; best=ck['best']; history=ck['history']
        torch.set_rng_state(ck['rng'].cpu())
        if device=='cuda' and ck.get('cuda_rng') is not None: torch.cuda.set_rng_state_all(ck['cuda_rng'])
        log(f'恢复 {kind} seed={seed}，训练步数 {start}')
    begin=time.perf_counter()
    for step in range(start+1,args.steps+1):
        model.train()
        idx=torch.randint(len(source),(args.batch,),device=device)
        s,y,c=source[idx],target[idx],condition[idx]
        # Independent white noise in normalized source units, fresh for every batch.
        # The same perturbed source is used by FM interpolation and endpoint prediction.
        if source_noise_std:
            s=s+source_noise_std*torch.randn_like(s)
        optimizer.zero_grad(set_to_none=True)
        if kind in ['regression','residual']:
            p=model(s,c)
            result=(p-y).square().mean()+4*(p[:,0]-y[:,0]).square().mean()
            fm=result.new_zeros(()); loss=result
        else:
            loss,fm,result=flow_loss(model,s,y,c,0. if kind=='fm_only' else 1.,args.flow_steps,predictor)
        if not torch.isfinite(loss): raise RuntimeError(f'Non-finite loss at step {step}')
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.); optimizer.step()
        if step%100==0 or step==args.steps:
            pred=norm.invert(predict(model,validation,args.flow_steps,predictor=predictor))
            rmse=float(np.sqrt(np.mean((pred[:,0]-val_data['target'][:,0])**2)))
            row={'step':step,'loss':float(loss.detach()),'fm_loss':float(fm.detach()),
                 'result_loss':float(result.detach()),'val_rmse':rmse}
            history.append(row)
            ck={'model':model.state_dict(),'normalizer':norm.state,'config':vars(args),
                'kind':kind,'seed':seed,'step':step,'val_rmse':rmse}
            if rmse<best:
                best=rmse; save_checkpoint(path,ck)
            save_checkpoint(last,{**ck,'optimizer':optimizer.state_dict(),'best':best,'history':history,
                        'rng':torch.get_rng_state(),
                        'cuda_rng':torch.cuda.get_rng_state_all() if device=='cuda' else None})
            save_json(out/f'{kind}_seed{seed}_history.json',history)
            log(f'{kind} seed={seed} step={step}/{args.steps} val_RMSE={rmse:.5f} best={best:.5f}')
    ck=torch.load(path,map_location=device,weights_only=False); model.load_state_dict(ck['model'])
    log(f'完成 {kind} seed={seed}，本轮耗时 {time.perf_counter()-begin:.1f} s，选择验证最优 step={ck["step"]}')
    return model,history

def metrics(y,p):
    error=p-y
    return {'rmse':float(np.sqrt(np.mean(error**2))),'mae':float(np.mean(abs(error))),
            'snr_db':float(10*np.log10(max(np.mean(y*y),1e-15)/max(np.mean(error*error),1e-15)))}

def evaluate(args,models,norm,device,out,filter_params):
    rows=[]; individual=[]
    scenarios=[('gaussian_low',.2,'gaussian'),('gaussian_mid',.5,'gaussian'),
               ('gaussian_high',.9,'gaussian'),('student_ood',.5,'student')]
    for scenario,sigma,noise in scenarios:
        # Same trajectories and underlying standardized noise for Gaussian noise sweep.
        trajectories=make_trajectories(args.test_trajectories,args.test_seed,sigma,noise)
        data=windows(trajectories,args.length,2); tensors=norm.tensors(data,device)
        predictions={}
        for method in ['raw','ema','local_poly','kalman','physics_backward']:
            seqs=[estimate(tr,method,filter_params.get(method)) for tr in trajectories]
            predictions[(method,-1)]=np.array([seqs[j][i] for j,i in zip(data['trajectory'],data['index'])])
        for (kind,seed),model in models.items():
            predictions[(kind,seed)]=norm.invert(predict(model,tensors,args.flow_steps))[:,0]
        y=data['target'][:,0]
        for (method,seed),pred in predictions.items():
            for family in ['all','multisine','chirp','steps']:
                mask=np.ones(len(y),bool) if family=='all' else np.array([trajectories[i]['kind']==family for i in data['trajectory']])
                rows.append({'scenario':scenario,'family':family,'method':method,'seed':seed,**metrics(y[mask],pred[mask])})
            for tid,tr in enumerate(trajectories):
                mask=data['trajectory']==tid
                individual.append({'scenario':scenario,'trajectory':tid,'family':tr['kind'],
                                   'method':method,'seed':seed,**metrics(y[mask],pred[mask])})
        np.savez_compressed(out/f'predictions_{scenario}.npz',target=y,trajectory=data['trajectory'],index=data['index'],
                            **{f'{m}_seed{s}':p for (m,s),p in predictions.items()})
        if scenario=='gaussian_mid':
            fig,axes=plt.subplots(3,1,figsize=(12,9),layout='constrained')
            for tid,ax in enumerate(axes):
                mask=(data['trajectory']==tid); ts=trajectories[tid]['t'][data['index'][mask]]
                ax.plot(ts,y[mask],color='black',lw=1.8,label='True d')
                for method,seed,color in [('raw',-1,'0.7'),('kalman',-1,'tab:green'),
                                           ('regression',args.seeds[0],'tab:orange'),('a2afm',args.seeds[0],'tab:blue')]:
                    ax.plot(ts,predictions[(method,seed)][mask],lw=.8,alpha=.8,label=method,color=color)
                ax.set_title(trajectories[tid]['kind']); ax.set_ylabel('Disturbance'); ax.set_xlim(2,10); ax.grid(alpha=.2)
            axes[0].legend(ncol=5); axes[-1].set_xlabel('Time (s)')
            fig.savefig(out/'denoising.png',dpi=160); plt.close(fig)
    for name,records in [('metrics.csv',rows),('trajectory_metrics.csv',individual)]:
        with (out/name).open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
    save_json(out/'metrics.json',rows)
    # Separate FM integration-discretization check, without model reselection.
    integration=[]
    tr=make_trajectories(6,40000,.5); data=windows(tr,args.length,4); ts=norm.tensors(data,device)
    for (kind,seed),model in models.items():
        if kind!='a2afm': continue
        for steps in [1,2,4,8,16]:
            p=norm.invert(predict(model,ts,steps))[:,0]
            integration.append({'seed':seed,'integration_steps':steps,**metrics(data['target'][:,0],p)})
    save_json(out/'integration_check.json',integration)
    return rows

def report(args,rows,histories,out,device):
    allrows=[r for r in rows if r['family']=='all']
    methods=list(dict.fromkeys(r['method'] for r in allrows))
    lines=['# 实验结果','',f'生成时间：{datetime.now(timezone(timedelta(hours=8))).isoformat()}',
           '',f'设备：{device}；训练轨迹 {args.train_trajectories}；验证轨迹 18；每场景测试轨迹 {args.test_trajectories}；随机种子 {args.seeds}。',
           f'窗口 L={args.length}，dt=0.02 s；训练 {args.steps} steps/model；中点积分 {args.flow_steps} 步。',
           '', '## 当前扰动 d(t) 的测试 RMSE', '', '| 方法 | Gaussian 0.2 | Gaussian 0.5 | Gaussian 0.9 | Student-t OOD 0.5 |',
           '|---|---:|---:|---:|---:|']
    summary={}
    for m in methods:
        cells=[]
        for scenario in ['gaussian_low','gaussian_mid','gaussian_high','student_ood']:
            vals=[r['rmse'] for r in allrows if r['method']==m and r['scenario']==scenario]
            cells.append(f'{np.mean(vals):.5f}'+(f' ± {np.std(vals,ddof=1):.5f}' if len(vals)>1 else ''))
            summary[(m,scenario)]=float(np.mean(vals))
        lines.append('| '+m+' | '+' | '.join(cells)+' |')
    gain=100*(1-summary[('a2afm','gaussian_mid')]/summary[('raw','gaussian_mid')])
    lines += ['',f'中等高斯噪声下，A2AFM 相对原始估计的 RMSE 降低 {gain:.2f}%。',
              '', '表中 ± 为训练随机种子间样本标准差，不是置信区间；各方法共享测试轨迹。',
              '滤波方法按验证集调参；神经网络按验证当前时刻 RMSE 选择检查点。完整分信号指标见 metrics.csv，逐轨迹指标见 trajectory_metrics.csv。',
              '', '## 必须保留的解释',
              '- 这是 A2A 思想的信号空间改编，不是原机器人任务的复现；不存在隐空间编码/解码。',
              '- 网络仅使用截至 t 的观测，未来 d 只作训练标签。测试时返回整段预测，但应用只取首项。',
              '- 精确 x/v 的假设使 physics_backward 基线特别强；它使用相同可用信息。不能据此宣称 FM 优于物理方法。',
              '- EMA、局部多项式、Kalman 只使用 d_hat；神经网络额外使用 x/v/u/A，须区分信息量差异。',
              '- Student-t 为未训练噪声分布；阶跃属于训练中出现的信号族，不能称为信号族 OOD。',
              '- 仿真真值来自已知方程；尚无真实传感器数据，未测试系统模型失配或 x/v 含噪。',
              '', '![去噪曲线](denoising.png)', '', '![训练曲线](training.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
    for (kind,seed),h in histories.items(): ax.plot([r['step'] for r in h],[r['val_rmse'] for r in h],label=f'{kind}/{seed}')
    ax.set(xlabel='Training step',ylabel='Validation current-d RMSE'); ax.legend(ncol=3); ax.grid(alpha=.2)
    fig.savefig(out/'training.png',dpi=150); plt.close(fig)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='results/main'); parser.add_argument('--steps',type=int,default=1500)
    parser.add_argument('--seeds',type=int,nargs='+',default=[11,22,33]); parser.add_argument('--length',type=int,default=24)
    parser.add_argument('--width',type=int,default=128); parser.add_argument('--batch',type=int,default=128)
    parser.add_argument('--lr',type=float,default=.001); parser.add_argument('--flow-steps',type=int,default=4)
    parser.add_argument('--train-trajectories',type=int,default=72); parser.add_argument('--test-trajectories',type=int,default=24)
    parser.add_argument('--test-seed',type=int,default=50000)
    parser.add_argument('--threads',type=int,default=4); parser.add_argument('--resume',action='store_true')
    parser.add_argument('--ablation',action='store_true')
    args=parser.parse_args(); torch.set_num_threads(args.threads)
    torch.use_deterministic_algorithms(True)
    device='cuda' if torch.cuda.is_available() else 'cpu'
    out=ROOT/args.out; out.mkdir(parents=True,exist_ok=True)
    save_json(out/'config.json',vars(args))
    save_json(out/'source_hashes.json',{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in [ROOT/'experiment.py',*sorted((ROOT/'a2afm').glob('*.py'))]})
    save_json(out/'environment.json',{'torch':torch.__version__,'numpy':np.__version__,'device':device,
                                    'cpu_count':os.cpu_count(),'torch_threads':args.threads})
    log(f'开始实验 {args.out}；设备 {device}；计划训练 A2AFM/直接回归，评估滤波和物理基线')
    train_tr=make_trajectories(args.train_trajectories,10000)
    val_tr=make_trajectories(18,20000)
    train_data=windows(train_tr,args.length,2); val_data=windows(val_tr,args.length,4)
    norm=Normalizer(train_data)
    filter_params=tune(val_tr,val_data); save_json(out/'filter_params.json',filter_params)
    save_json(out/'split_manifest.json',{'train':[t['trajectory_id'] for t in train_tr],
                                        'validation':[t['trajectory_id'] for t in val_tr],
                                        'test':[f'{args.test_seed}:{i}' for i in range(args.test_trajectories)]})
    log(f'数据完成：训练窗口 {len(train_data["source"])}，验证窗口 {len(val_data["source"])}；滤波参数 {filter_params}')
    models={}; histories={}
    for seed in args.seeds:
        for kind in ['a2afm','regression']+(['fm_only'] if args.ablation else []):
            models[(kind,seed)],histories[(kind,seed)]=train(args,kind,seed,train_data,val_data,norm,device,out)
    log('训练完成，开始冻结测试集评估与积分步数检查')
    rows=evaluate(args,models,norm,device,out,filter_params)
    report(args,rows,histories,out,device)
    save_json(out/'status.json',{'status':'complete','finished':datetime.now(timezone.utc).isoformat()})
    log(f'实验完成：{out / "REPORT.md"}')

if __name__=='__main__': main()
