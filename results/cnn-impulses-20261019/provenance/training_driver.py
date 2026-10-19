"""Four architecture/objective controls with pulse-inclusive evaluation."""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib
import json
import multiprocessing
from pathlib import Path
import platform
import subprocess
import time
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from a2afm.data import windows,Normalizer
from a2afm.models import integrate,flow_loss
from a2afm.baselines import estimate
from multichannel.core import reference_scales,augmented_kalman
from multichannel.experiment import select_filters,csv_save
from cnn_experiment.models import METHODS,make_model,Estimator
from cnn_experiment.data import (TRAIN_FAMILIES,TEST_FAMILIES,CONDITIONS,
    trajectories,observations,trajectory_metrics)

ROOT=Path(__file__).resolve().parents[1]
BASELINES=['raw','ema','augmented_kalman']


def save(path,obj):
    path=Path(path); tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    tmp.replace(path)


def predict(model,tensors,steps=4):
    source,_,condition=tensors; result=[]; model.eval()
    with torch.inference_mode():
        for i in range(0,len(source),512):
            s=source[i:i+512]; c=condition[i:i+512]
            result.append((integrate(model,s,c,steps) if model.flow else model(s,c)).numpy())
    return np.concatenate(result)


def train_seed(seed,td,vd,norm_state,config,out_string):
    """Independent worker. Each method gets identical minibatches for this seed."""
    torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
    out=Path(out_string); norm=Normalizer(state=norm_state)
    source,target,condition=norm.tensors(td); val=norm.tensors(vd)
    def log(message):
        line=f'[{datetime.now(timezone.utc).isoformat()}] seed={seed} {message}'
        print(line,flush=True)
        with (out/f'train_seed{seed}.log').open('a',encoding='utf-8') as f:f.write(line+'\n')
    results=[]
    for method in METHODS:
        torch.manual_seed(seed); model=make_model(method)
        opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.0001)
        batches=torch.Generator().manual_seed(seed+1000)
        torch.manual_seed(seed+2000)  # same flow-time samples across architectures
        path=out/'models'/f'{method}_seed{seed}.pt'; last=path.with_stem(path.stem+'_last')
        history=[]; start=0; best=float('inf'); previous_seconds=0.
        if config['resume'] and last.exists():
            ck=torch.load(last,map_location='cpu',weights_only=False)
            model.load_state_dict(ck['model']); opt.load_state_dict(ck['optimizer'])
            batches.set_state(ck['batch_rng']); torch.set_rng_state(ck['rng'])
            start=ck['step']; best=ck['best']; history=ck['history']; previous_seconds=ck['training_seconds']
        begin=time.perf_counter()
        for step in range(start+1,config['steps']+1):
            model.train(); idx=torch.randint(len(source),(128,),generator=batches)
            s,y,c=source[idx],target[idx],condition[idx]; opt.zero_grad(set_to_none=True)
            if model.flow: loss,fm,endpoint=flow_loss(model,s,y,c,steps=4)
            else:
                p=model(s,c); endpoint=((p-y)**2).mean()+4*((p[:,0]-y[:,0])**2).mean()
                loss=endpoint; fm=loss.new_zeros(())
            if not torch.isfinite(loss): raise RuntimeError(f'Nonfinite loss: {method} seed={seed}')
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),5.); opt.step()
            if step%500==0 or step==config['steps']:
                pred=norm.invert(predict(model,val))[:,0]
                mse=float(np.mean((pred-vd['target'][:,0])**2))
                history.append(dict(step=step,loss=float(loss.detach()),fm_loss=float(fm.detach()),
                    endpoint_loss=float(endpoint.detach()),val_mse=mse))
                ck=dict(method=method,seed=seed,step=step,model=model.state_dict(),normalizer=norm_state,
                    config=config,val_mse=mse,parameters=sum(p.numel() for p in model.parameters()))
                if mse<best:best=mse;torch.save(ck,path)
                torch.save(dict(ck,optimizer=opt.state_dict(),rng=torch.get_rng_state(),batch_rng=batches.get_state(),
                    best=best,history=history,training_seconds=previous_seconds+time.perf_counter()-begin),last)
                save(path.with_name(path.stem+'_history.json'),history)
                log(f'{method} {step}/{config["steps"]} validation_RMSE={np.sqrt(mse):.5f}')
        ck=torch.load(path,map_location='cpu',weights_only=False)
        results.append(dict(method=method,seed=seed,best_step=ck['step'],validation_rmse=float(np.sqrt(best)),
            parameters=ck['parameters'],training_seconds=previous_seconds+time.perf_counter()-begin,
            scope='one training thread; up to three concurrent seed workers; includes validation/checkpoint IO'))
    return results


def summarize(rows,seeds):
    result=[]
    for condition in CONDITIONS:
        for family in ['all',*TEST_FAMILIES]:
            for method in [*BASELINES,*METHODS]:
                selected=[r for r in rows if r['condition']==condition and r['method']==method
                          and (family=='all' or r['family']==family)]
                row=dict(condition=condition,family=family,method=method)
                for key in ['mse','shock_mse','recovery_mse','background_mse','onset_mse']:
                    values=[r[key] for r in selected if r[key] is not None]
                    row[key.replace('mse','rmse')]=float(np.sqrt(np.mean(values))) if values else None
                for key in ['mae','shock_area_abs','shock_peak_ratio']:
                    values=[r[key] for r in selected if r[key] is not None]
                    row[key]=float(np.mean(values)) if values else None
                result.append(row)
    return result


def compare(rows,n):
    rng=np.random.default_rng(20261019); results=[]
    # Stratify paired resampling by waveform family; keep family proportions fixed.
    for condition in CONDITIONS:
        for metric in ['mse','shock_mse']:
            families=TEST_FAMILIES if metric=='mse' else TEST_FAMILIES[1:]
            groups=[np.arange(i,n,len(TEST_FAMILIES)) for i,f in enumerate(TEST_FAMILIES) if f in families]
            indices=np.concatenate([rng.choice(g,size=(5000,len(g)),replace=True) for g in groups],axis=1)
            def values(method):
                return np.array([np.mean([r[metric] for r in rows if r['condition']==condition
                    and r['method']==method and r['trajectory']==i and r[metric] is not None])
                    if any(r['condition']==condition and r['method']==method and r['trajectory']==i
                           and r[metric] is not None for r in rows) else np.nan for i in range(n)])
            cnn=values('cnn_a2afm')
            for baseline in ['mlp_a2afm','mlp_regression','cnn_regression','raw','augmented_kalman']:
                other=values(baseline); diff=np.sqrt(other[indices].mean(1))-np.sqrt(cnn[indices].mean(1))
                ids=np.concatenate(groups)
                results.append(dict(condition=condition,metric=metric.replace('mse','rmse'),baseline=baseline,
                    baseline_minus_cnn_a2afm=float(np.sqrt(other[ids].mean())-np.sqrt(cnn[ids].mean())),
                    stratified_paired_trajectory_95=np.quantile(diff,[.025,.975]).tolist()))
    return results


def latency(out,test,seeds):
    results=[]; torch.set_num_threads(2)
    for method in METHODS:
        est=Estimator(out/'models'/f'{method}_seed{seeds[0]}.pt')
        calls=0
        for _ in range(30): est.estimate(*[test[0][k][:24] for k in ['x','v','u','a_measured']],test[0]['params'])
        samples=[]
        # Two complete representative streams include positive and negative pulses.
        for tr in [test[1],test[-1]]:
            history=np.column_stack([tr[k][:24] for k in ['x','v','u','a_measured']])
            for i in range(24,len(tr['t'])):
                sample=np.array([tr[k][i] for k in ['x','v','u','a_measured']])
                begin=time.perf_counter_ns()
                history=np.roll(history,-1,axis=0);history[-1]=sample
                est.estimate(history[:,0],history[:,1],history[:,2],history[:,3],tr['params'])
                samples.append((time.perf_counter_ns()-begin)/1e6);calls+=1
        results.append(dict(method=method,seed=seeds[0],calls=calls,threads=2,batch_size=1,
            parameters=sum(p.numel() for p in est.model.parameters()),
            network_evaluations_per_estimate=8 if est.model.flow else 1,
            median_ms=float(np.median(samples)),p95_ms=float(np.quantile(samples,.95)),
            p99_ms=float(np.quantile(samples,.99)),max_ms=float(max(samples)),
            fraction_over_20ms=float(np.mean(np.array(samples)>20)),
            scope='history update, residual, normalization, network/integration, output; excludes sensor/actuator IO and model load'))
    return results


def report(out,summary,comparisons,timing,config):
    lines=['# CNN 与全连接 A2AFM：冲击扰动估计','',
        f'训练：{config["train_trajectories"]}条独立轨迹 × 2种测量条件；验证{config["val_trajectories"]}条；测试{config["test_trajectories"]}条。',
        f'四组模型均从头训练，种子{config["seeds"]}，每模型{config["steps"]}次更新；保持原FM桥接和4步中点积分。',
        '训练/验证：平滑、20/80/200ms脉冲；测试另含未参与训练的40/120ms宽度。',
        '两种测量条件：x/v准确和x/v联合5%高斯噪声；加速度噪声始终σ=0.5。',
        '百分比相对于干净训练集固定通道标准差；同一真轨迹及测量噪声在各方法间共享。',
        '训练、验证、测试均stride=1，包含所有单采样冲击；物理采样20ms，脉冲对齐采样网格。',
        '独立数据种子为91000/92000/93000；每条冲击轨迹含正负各一次脉冲，冲量绝对值0.15–0.35。',
        'CNN使用32通道、3个扩张因果卷积残差块（dilation=1/2/4），展平后80宽全连接读出；不是纯全卷积解码器。',
        '卷积提取历史特征，读出层映射至未来坐标；窗口内没有未来实测信息。',
        '同一种子共享训练批次顺序，两个FM模型还共享流时间抽样；每500步按两条件混合验证当前MSE选择最佳权重。',
        '训练1线程/worker，最多3个独立种子同时执行；相同步数和近似参数量，不是等FLOPs或等墙钟时间。',
        '', '## 汇总', '',
        '先平均模型种子和轨迹的MSE再开方；冲击RMSE仅脉冲持续点，按轨迹等权，不让长脉冲主导。',
        '背景排除脉冲及其后0.5秒；恢复区间误差统计这0.5秒。此处没有闭环控制。',
        '', '| 测量条件 | 方法 | 全时段RMSE | 冲击RMSE | 背景RMSE | 冲击后RMSE |',
        '|---|---|---:|---:|---:|---:|']
    for r in summary:
        if r['family']=='all':lines.append(f'| {r["condition"]} | {r["method"]} | {r["rmse"]:.5f} | {r["shock_rmse"]:.5f} | {r["background_rmse"]:.5f} | {r["recovery_rmse"]:.5f} |')
    lines+=['','## 按冲击宽度分组','','| 条件 | 宽度 | 方法 | 冲击RMSE | 起点RMSE | 平均绝对积分误差 |','|---|---|---|---:|---:|---:|']
    for r in summary:
        if r['family'] not in ['all','smooth']:
            width=int(r['family'].split('_')[1])*20
            lines.append(f'| {r["condition"]} | {width}ms | {r["method"]} | {r["shock_rmse"]:.5f} | {r["onset_rmse"]:.5f} | {r["shock_area_abs"]:.5f} |')
    lines+=['','## 配对统计','','对各训练种子MSE平均，再在每种波形内按轨迹配对重采样5000次。正差值代表CNN A2AFM更好；未作多重比较校正。',
        '', '| 条件 | 指标 | 对照 | 对照减CNN A2AFM | 95%区间 |','|---|---|---|---:|---|']
    for r in comparisons:
        lo,hi=r['stratified_paired_trajectory_95']
        lines.append(f'| {r["condition"]} | {r["metric"]} | {r["baseline"]} | {r["baseline_minus_cnn_a2afm"]:.5f} | [{lo:.5f}, {hi:.5f}] |')
    lines+=['','## 在线计算延迟','','训练worker退出后测量，2线程、batch=1、30次预热、两条完整测试流。包括历史更新/残差/归一化/模型/输出，不含传感器和执行器。',
        '', '| 方法 | 参数量 | 中位ms | P95ms | P99ms | 最大ms | 超20ms比例 |','|---|---:|---:|---:|---:|---:|---:|']
    for r in timing:lines.append(f'| {r["method"]} | {r["parameters"]} | {r["median_ms"]:.3f} | {r["p95_ms"]:.3f} | {r["p99_ms"]:.3f} | {r["max_ms"]:.3f} | {r["fraction_over_20ms"]:.4f} |')
    lines+=['','## 曲线','','![宽度比较](shock_widths.png)','','![冲击时序](pulse_examples.png)',
        '', '## 限制与复现','',
        '- 训练见过冲击，40/120ms是未见宽度的插值测试，不是完全零样本冲击泛化。',
        '- 仍为已知准确系统参数、有限宽脉冲、同步采样和开环估计，不是Dirac冲量或闭环性能证明。',
        '- 主评分因未来标签长度而省略末23个点，冲击全部位于有效区间；背景样本不包含启动窗口。',
        '- 传统方法EMA/增广Kalman每个测量条件独立验证调参，知道传感器噪声方差；神经模型共享两条件权重。',
        '- CNN增加了卷积计算；参数相近不代表计算量相近。测得延迟不构成实时截止时间保证。',
        '- 初始流仍为原始历史残差，未修改此前讨论的重尾起点问题；本轮没有重尾噪声。',
        '- 复现命令见 ../../cnn_experiment/README.md；配置、划分、权重、观测、预测和源码摘要均归档。']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    lookup={(r['condition'],r['family'],r['method']):r for r in summary}
    fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
    for condition,ax in zip(CONDITIONS,axes):
        for method in [*METHODS,'raw','augmented_kalman']:
            ax.plot([20,40,80,120,200],[lookup[condition,f,method]['shock_rmse'] for f in TEST_FAMILIES[1:]],marker='o',label=method)
        ax.set(xlabel='Pulse width (ms)',ylabel='Pulse-interval RMSE',title=condition);ax.grid(alpha=.25)
    axes[0].legend(fontsize=7);fig.savefig(out/'shock_widths.png',dpi=160);plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='results/cnn-impulses-20261019')
    p.add_argument('--steps',type=int,default=3000);p.add_argument('--seeds',nargs='+',type=int,default=[11,22,33])
    p.add_argument('--train-trajectories',type=int,default=96)
    p.add_argument('--val-trajectories',type=int,default=24)
    p.add_argument('--test-trajectories',type=int,default=72)
    p.add_argument('--workers',type=int,default=3);p.add_argument('--resume',action='store_true')
    args=p.parse_args();out=(ROOT/args.out).resolve(); config=vars(args).copy(); comparable=dict(config);comparable.pop('resume')
    if min(args.steps,args.workers,args.train_trajectories,args.val_trajectories,args.test_trajectories)<1:p.error('Positive counts required')
    if out.exists() and any(out.iterdir()) and not args.resume:p.error('Use a fresh output directory or --resume')
    out.mkdir(parents=True,exist_ok=True);(out/'models').mkdir(exist_ok=True)
    if args.resume and (out/'config.json').exists() and json.loads((out/'config.json').read_text())!=comparable:raise ValueError('Resume config changed')
    files=[*sorted((ROOT/'cnn_experiment').glob('*.py')),*sorted((ROOT/'a2afm').glob('*.py')),
           *sorted((ROOT/'multichannel').glob('*.py')),ROOT/'experiment.py',ROOT/'requirements-lock.txt']
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    if args.resume and (out/'source_hashes.json').exists() and json.loads((out/'source_hashes.json').read_text())!=hashes:raise ValueError('Resume source changed')
    save(out/'config.json',comparable);save(out/'source_hashes.json',hashes);save(out/'status.json',{'status':'running'})
    save(out/'environment.json',dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__,
        platform=platform.platform(),device='cpu',training_threads_per_worker=1,evaluation_threads=2,
        parent_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()))
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    train=trajectories(args.train_trajectories,91000,TRAIN_FAMILIES)
    val=trajectories(args.val_trajectories,92000,TRAIN_FAMILIES)
    test=trajectories(args.test_trajectories,93000,TEST_FAMILIES)
    scales=reference_scales(train);save(out/'reference_scales.json',scales)
    manifest={label:[{k:t[k] for k in ['trajectory_id','kind','events']} for t in traces]
              for label,traces in [('train',train),('validation',val),('test',test)]}
    manifest['sensor_seed_bases']={'train':101000,'validation':102000,'test':103000};save(out/'data_manifest.json',manifest)
    td=windows([t for condition in CONDITIONS for t in observations(train,scales,condition,101000)],24,1)
    vd=windows([t for condition in CONDITIONS for t in observations(val,scales,condition,102000)],24,1)
    norm=Normalizer(td);print(f'Train windows={len(td["source"])}, validation={len(vd["source"])}, scales={scales}',flush=True)
    training=[]
    with ProcessPoolExecutor(max_workers=min(args.workers,len(args.seeds)),mp_context=multiprocessing.get_context('spawn')) as pool:
        jobs=[pool.submit(train_seed,s,td,vd,norm.state,config,str(out)) for s in args.seeds]
        for job in as_completed(jobs):training.extend(job.result());save(out/'training_summary.json',training)
    models={(method,seed):Estimator(out/'models'/f'{method}_seed{seed}.pt') for method in METHODS for seed in args.seeds}
    rows=[];tuning={}; noisy_test=None
    for condition in CONDITIONS:
        print('Evaluating '+condition,flush=True)
        validation=observations(val,scales,condition,102000)
        params,grid=select_filters(validation,windows(validation,24,1));tuning[condition]=dict(selected=params,grid=grid)
        save(out/'filter_tuning.json',tuning)
        measured=observations(test,scales,condition,103000);data=windows(measured,24,1);predictions={}
        for method in BASELINES:
            seq=[augmented_kalman(t,params[method]) if method=='augmented_kalman'
                 else estimate(t,method,params.get(method)) for t in measured]
            predictions[method,-1]=np.array([seq[j][i] for j,i in zip(data['trajectory'],data['index'])])
        for (method,seed),est in models.items():
            predictions[method,seed]=est.norm.invert(predict(est.model,est.norm.tensors(data)))[:,0]
        for (method,seed),pred in predictions.items():
            if not np.isfinite(pred).all():raise RuntimeError(f'Nonfinite predictions {method}/{seed}')
            for j,tr in enumerate(measured):
                mask=data['trajectory']==j
                rows.append(dict(condition=condition,method=method,seed=seed,trajectory=j,family=tr['kind'],
                    **trajectory_metrics(tr,data['index'][mask],pred[mask])))
        np.savez_compressed(out/f'predictions_{condition}.npz',target=data['target'][:,0],trajectory=data['trajectory'],index=data['index'],
            **{f'{m}_seed{s}':v for (m,s),v in predictions.items()})
        np.savez_compressed(out/f'observations_{condition}.npz',
            **{f'{k}_{j}':tr[k] for j,tr in enumerate(measured) for k in
               ['t','x','v','x_true','v_true','u','a_measured','d','background','dhat','params','sigma_x','sigma_v','sigma_a']})
        if condition=='xv_5pct':
            noisy_test=measured;fig,axes=plt.subplots(3,1,figsize=(12,9),layout='constrained')
            for j,ax in zip([1,2,5],axes):
                mask=data['trajectory']==j;ts=measured[j]['t'][data['index'][mask]]
                ax.plot(ts,data['target'][mask],color='black',lw=2,label='truth')
                for method in METHODS:ax.plot(ts,predictions[method,args.seeds[0]][mask],label=method,lw=1)
                ax.plot(ts,predictions['raw',-1][mask],label='raw',alpha=.35,lw=.7)
                onset=measured[j]['events'][0]['start']*.02
                ax.set(xlim=(onset-.2,onset+.7),ylabel='Disturbance',title=measured[j]['kind']);ax.grid(alpha=.25)
            axes[0].legend(ncol=3);axes[-1].set_xlabel('Physical time (s)');fig.savefig(out/'pulse_examples.png',dpi=160);plt.close(fig)
    csv_save(out/'trajectory_metrics.csv',rows)
    summary=summarize(rows,args.seeds);comparisons=compare(rows,args.test_trajectories)
    save(out/'summary.json',summary);save(out/'comparisons.json',comparisons)
    print('Measuring sequential batch-1 latency after all training workers exited',flush=True)
    timing=latency(out,noisy_test,args.seeds);save(out/'latency.json',timing)
    report(out,summary,comparisons,timing,comparable)
    save(out/'status.json',dict(status='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        models=len(models),trajectory_metric_rows=len(rows),windows_per_condition=len(data['source'])))
    print('Complete: '+str(out/'REPORT.md'),flush=True)


if __name__=='__main__':main()
