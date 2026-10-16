"""Run from the repository root: python -m multichannel.experiment."""
import argparse
import csv
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import subprocess

import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import experiment as training
from a2afm.system import make_trajectories
from a2afm.data import windows, Normalizer
from a2afm.baselines import estimate
from a2afm.inference import DisturbanceEstimator
from multichannel.core import SCENARIOS, measure, reference_scales, augmented_kalman

ROOT = Path(__file__).resolve().parents[1]
METHODS = ['raw','ema','physics_backward','augmented_kalman',
           'frozen_regression','frozen_a2afm','mixed_regression','mixed_a2afm']


def save(path, obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def csv_save(path, rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def sensors(traces, scales, scenario, seed):
    return [measure(tr,scales,SCENARIOS[scenario],seed+i) for i,tr in enumerate(traces)]


def select_filters(traces, data):
    records=[]; chosen={}
    for method,values in [('ema',[.05,.1,.2,.35,.5,.7,.9]),
                          ('augmented_kalman',[.01,1.,100.,10000.])]:
        for value in values:
            seq=[augmented_kalman(t,value) if method=='augmented_kalman'
                 else estimate(t,method,value) for t in traces]
            pred=np.array([seq[j][i] for j,i in zip(data['trajectory'],data['index'])])
            records.append(dict(method=method,value=value,mse=float(np.mean((pred-data['target'][:,0])**2))))
        chosen[method]=min((r for r in records if r['method']==method),key=lambda r:r['mse'])['value']
    return chosen,records


def score(pred,target):
    e=np.asarray(pred,dtype=np.float64)-target
    return dict(mse=float(np.mean(e**2)),rmse=float(np.sqrt(np.mean(e**2))),
                mae=float(np.mean(abs(e))),abs_p95=float(np.quantile(abs(e),.95)),
                abs_p99=float(np.quantile(abs(e),.99)),max_abs=float(np.max(abs(e))))


def write_report(out, rows, individual, scales, args):
    summary=[]; comparisons=[]
    rng=np.random.default_rng(20261016)
    indices=rng.integers(args.test_trajectories,size=(5000,args.test_trajectories))
    def trajectory_mse(scenario,method):
        return np.array([np.mean([r['mse'] for r in individual if r['scenario']==scenario
                                 and r['method']==method and r['trajectory']==i])
                         for i in range(args.test_trajectories)])
    for scenario in SCENARIOS:
        for method in METHODS:
            selected=[r for r in rows if r['scenario']==scenario and r['method']==method]
            summary.append(dict(scenario=scenario,method=method,
                rmse=float(np.sqrt(np.mean([r['mse'] for r in selected]))),
                mae=float(np.mean([r['mae'] for r in selected])),
                rmse_seed_std=float(np.std([r['rmse'] for r in selected],ddof=1)) if len(selected)>1 else None,
                abs_p99_seed_mean=float(np.mean([r['abs_p99'] for r in selected]))))
        for prefix in ['frozen','mixed']:
            fm=trajectory_mse(scenario,prefix+'_a2afm'); reg=trajectory_mse(scenario,prefix+'_regression')
            diff=np.sqrt(reg[indices].mean(1))-np.sqrt(fm[indices].mean(1))
            comparisons.append(dict(scenario=scenario,training=prefix,
                regression_minus_a2afm=float(np.sqrt(reg.mean())-np.sqrt(fm.mean())),
                paired_trajectory_bootstrap_95=np.quantile(diff,[.025,.975]).tolist()))
    save(out/'summary.json',summary); save(out/'comparisons.json',comparisons)
    lookup={(r['scenario'],r['method']):r['rmse'] for r in summary}
    lines=['# 多通道测量噪声实验','',f'完成时间（UTC）：{datetime.now(timezone.utc).isoformat()}',
        '',f'Python {platform.python_version()}，PyTorch {torch.__version__}，CPU；每个新模型训练 {args.steps} 步，训练种子 {args.seeds}。',
        f'原始独立轨迹：训练 {args.train_trajectories}、验证 {args.val_trajectories}、测试 {args.test_trajectories}。',
        '训练/验证加速度噪声沿用原实验的 Gaussian σ∈[0.2,0.9]；测试固定 Gaussian σ=0.5。',
        f'仅从干净训练轨迹计算固定尺度：std(x)={scales["x"]:.8f}，std(v)={scales["v"]:.8f}。',
        '百分比乘以上述固定尺度得到传感器噪声的绝对标准差，不按测试轨迹重新缩放。',
        '', '## 协议', '',
        '- 原模型 frozen：加载 results/main 中已有 3000 步训练检查点，保持冻结。',
        '- 新模型 mixed：每条训练轨迹生成以下七种观测版本；统一训练一个多噪声模型，而不是每个场景单独调模型。',
        '- 七种版本共享物理轨迹与加速度测量；同一轨迹的位置/速度噪声标准正态抽样跨场景配对。',
        '- 共 7 倍观测版本，不是 7 倍独立轨迹；固定噪声实现，不是每个 epoch 在线重新采样。',
        '- 新模型仍是同一 A2AFM/回归结构、损失和超参数；验证按七种场景的混合当前扰动 MSE 选择检查点。',
        '- 训练窗口 stride=2，验证 stride=8，测试 stride=2；每窗 24 点。所有测试方法使用相同有效时刻。',
        '- 同一份带噪 x/v 同时用于条件与物理残差，真值和真实动力学不受噪声污染。',
        '- 这是开环估计实验；控制输入维持原脚本定义，没有测试带噪状态反馈控制、延迟或重尾传感器噪声。',
        '- augmented_kalman 使用 [x,v,d,d_dot] 状态和 [x_m,v_m,a_m] 测量，已知真实模型及传感器噪声方差。',
        '- EMA 与增广 Kalman 为每个场景分别按独立验证集调参；新神经模型在场景间共享权重。',
        '- Kalman 扰动采用局部线性变化先验；实际阶跃/多正弦不严格满足它，预测按上一采样输入作零阶保持近似。',
        '- physics_backward 对带噪速度直接后向差分，是噪声敏感性参照，不代表最优物理估计器。',
        '', '## 传感器噪声标准差','', '| 场景 | σx | σv |','|---|---:|---:|']
    for name,(fx,fv) in SCENARIOS.items(): lines.append(f'| {name} | {fx*scales["x"]:.8f} | {fv*scales["v"]:.8f} |')
    lines += ['', '## 当前扰动 RMSE', '',
        '先平均各训练种子的 MSE 再开方；不是各 RMSE 的简单均值。精确数值、种子标准差和 MAE 见 summary.json。',
        '', '| 场景 | 原始残差 | EMA | 速度差分 | 增广Kalman | 冻结回归 | 冻结A2AFM | 新回归 | 新A2AFM |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for name in SCENARIOS:
        lines.append('| '+name+' | '+' | '.join(f'{lookup[name,m]:.5f}' for m in METHODS)+' |')
    lines += ['', '## 回归减 A2AFM 的配对轨迹 Bootstrap', '',
        '先对同一轨迹的训练种子 MSE 平均，再对独立轨迹配对重采样 5000 次。正值代表 A2AFM 更好。',
        '区间未作多重比较校正，仅描述这组固定数据与训练种子；不覆盖独立数据集重复的不确定性。',
        '', '| 场景 | 模型 | RMSE差 | 95%区间 |','|---|---|---:|---|']
    for r in comparisons:
        lo,hi=r['paired_trajectory_bootstrap_95']
        lines.append(f'| {r["scenario"]} | {r["training"]} | {r["regression_minus_a2afm"]:.6f} | [{lo:.6f}, {hi:.6f}] |')
    lines += ['', '## 曲线', '', '![噪声敏感性](noise_sweep.png)', '', '![联合5%噪声时序](xv_5pct.png)',
        '', '## 文件与复现', '',
        '- 运行方式见 ../../multichannel/README.md；config.json 保存完整实验配置。',
        '- predictions_*.npz 保存所有方法/种子的预测、真值、轨迹索引与时刻；measurements_*.npz 保存测试观测。',
        '- metrics.csv 为逐种子/方法指标，trajectory_metrics.csv 为逐轨迹指标。',
        '- models/ 保存新模型最佳检查点、末次可恢复检查点和训练历史；原模型保持原样。',
        '- filter_tuning.json 保存验证搜索的所有候选分数；data_manifest.json 标识划分。',
        '- source_hashes.json 和 frozen_checkpoint_hashes.json 记录源码与原权重摘要。',
        '- 没有依据测试结果选择参数；本轮没有测试高于5%的噪声或新的噪声分布。']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    fig,axes=plt.subplots(1,3,figsize=(15,4),layout='constrained')
    for channel,ax in zip(['x','v','xv'],axes):
        for method in ['frozen_a2afm','frozen_regression','mixed_a2afm','mixed_regression','augmented_kalman','ema']:
            ax.plot([0,1,5],[lookup[s,method] for s in ['clean',channel+'_1pct',channel+'_5pct']],marker='o',label=method)
        ax.set(title=channel+' sensor noise',xlabel='Noise / training std (%)',ylabel='Disturbance RMSE')
        ax.grid(alpha=.25)
    axes[0].legend(fontsize=7); fig.savefig(out/'noise_sweep.png',dpi=160); plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='results/multichannel-20261016')
    p.add_argument('--steps',type=int,default=3000)
    p.add_argument('--seeds',type=int,nargs='+',default=[11,22,33])
    p.add_argument('--train-trajectories',type=int,default=72)
    p.add_argument('--val-trajectories',type=int,default=18)
    p.add_argument('--test-trajectories',type=int,default=24)
    p.add_argument('--threads',type=int,default=2)
    p.add_argument('--resume',action='store_true')
    args=p.parse_args(); out=(ROOT/args.out).resolve()
    if min(args.steps,args.train_trajectories,args.val_trajectories,args.test_trajectories,args.threads)<1:
        p.error('Counts and threads must be positive')
    if out.exists() and any(out.iterdir()) and not args.resume:
        p.error('Output is not empty; use a new directory or --resume')
    out.mkdir(parents=True,exist_ok=True); modeldir=out/'models'; modeldir.mkdir(exist_ok=True)
    def log(message):
        line=f'[{datetime.now(timezone.utc).isoformat()}] {message}'
        print(line,flush=True)
        with (out/'run.log').open('a',encoding='utf-8') as f: f.write(line+'\n')
    training.log=log  # Route reused trainer logging into this experiment only.
    torch.set_num_threads(args.threads); torch.use_deterministic_algorithms(True)
    cfg=vars(args).copy(); cfg.pop('resume')
    if args.resume and (out/'config.json').exists() and json.loads((out/'config.json').read_text())!=cfg:
        raise ValueError('Resume configuration differs from saved experiment')
    save(out/'config.json',cfg); save(out/'status.json',{'status':'running'})
    files=[ROOT/'experiment.py',ROOT/'requirements-lock.txt',*sorted((ROOT/'a2afm').glob('*.py')),
           *sorted((ROOT/'multichannel').glob('*.py'))]
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    if args.resume and (out/'source_hashes.json').exists() and json.loads((out/'source_hashes.json').read_text())!=hashes:
        raise ValueError('Source changed since the saved run; start a new output directory')
    save(out/'source_hashes.json',hashes)
    save(out/'environment.json',{'python':platform.python_version(),'torch':torch.__version__,
         'numpy':np.__version__,'platform':platform.platform(),'device':'cpu','threads':args.threads,
         'base_git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
    old={(kind,seed):DisturbanceEstimator(ROOT/f'results/main/{kind}_seed{seed}.pt')
         for kind in ['a2afm','regression'] for seed in args.seeds}
    save(out/'frozen_checkpoint_hashes.json',{f'{kind}_seed{seed}.pt':
         hashlib.sha256((ROOT/f'results/main/{kind}_seed{seed}.pt').read_bytes()).hexdigest() for kind,seed in old})
    log('Generating independent clean train/validation/test trajectories')
    train_base=make_trajectories(args.train_trajectories,10000)
    val_base=make_trajectories(args.val_trajectories,20000)
    test_base=make_trajectories(args.test_trajectories,50000,.5)
    scales=reference_scales(train_base); save(out/'reference_scales.json',scales)
    save(out/'data_manifest.json',{'train':[t['trajectory_id'] for t in train_base],
         'validation':[t['trajectory_id'] for t in val_base],'test':[t['trajectory_id'] for t in test_base],
         'sensor_seed_bases':{'train':81000,'validation':82000,'test':85000},'scenarios':SCENARIOS})
    train_tr=[t for scenario in SCENARIOS for t in sensors(train_base,scales,scenario,81000)]
    val_tr=[t for scenario in SCENARIOS for t in sensors(val_base,scales,scenario,82000)]
    td=windows(train_tr,24,2); vd=windows(val_tr,24,8); norm=Normalizer(td)
    log(f'Training windows={len(td["source"])}; validation windows={len(vd["source"])}; scales={scales}')
    train_args=argparse.Namespace(out=str(modeldir),steps=args.steps,seeds=args.seeds,length=24,width=128,
        batch=128,lr=.001,flow_steps=4,train_trajectories=args.train_trajectories,
        test_trajectories=args.test_trajectories,threads=args.threads,resume=args.resume,ablation=False)
    models={}
    for seed in args.seeds:
        for kind in ['a2afm','regression']:
            training.train(train_args,kind,seed,td,vd,norm,'cpu',modeldir)
            models[kind,seed]=DisturbanceEstimator(modeldir/f'{kind}_seed{seed}.pt')
    rows=[]; individual=[]; tuning={}
    for scenario in SCENARIOS:
        log('Tuning and evaluating '+scenario)
        val=sensors(val_base,scales,scenario,82000); val_data=windows(val,24,8)
        params,grid=select_filters(val,val_data); tuning[scenario]={'selected':params,'grid':grid}
        save(out/'filter_tuning.json',tuning)
        test=sensors(test_base,scales,scenario,85000); data=windows(test,24,2); target=data['target'][:,0]
        predictions={}
        for method in METHODS[:4]:
            seq=[augmented_kalman(t,params[method]) if method=='augmented_kalman'
                 else estimate(t,method,params.get(method)) for t in test]
            predictions[method,-1]=np.array([seq[j][i] for j,i in zip(data['trajectory'],data['index'])])
        for label,estimators in [('frozen',old),('mixed',models)]:
            for (kind,seed),est in estimators.items():
                pred=training.predict(est.model,est.norm.tensors(data),est.steps)
                predictions[label+'_'+kind,seed]=est.norm.invert(pred)[:,0]
        for (method,seed),pred in predictions.items():
            if not np.isfinite(pred).all(): raise RuntimeError(f'Nonfinite output: {scenario} {method} {seed}')
            rows.append(dict(scenario=scenario,method=method,seed=seed,**score(pred,target)))
            for j,tr in enumerate(test):
                mask=data['trajectory']==j
                individual.append(dict(scenario=scenario,method=method,seed=seed,trajectory=j,
                    family=tr['kind'],**score(pred[mask],target[mask])))
        np.savez_compressed(out/f'predictions_{scenario}.npz',target=target,trajectory=data['trajectory'],index=data['index'],
                            **{f'{m}_seed{s}':v for (m,s),v in predictions.items()})
        np.savez_compressed(out/f'measurements_{scenario}.npz',
            **{f'{key}_{i}':tr[key] for i,tr in enumerate(test) for key in
               ['t','x','v','x_true','v_true','u','d','a_measured','dhat','params','sigma_x','sigma_v','sigma_a']})
        if scenario=='xv_5pct':
            fig,axes=plt.subplots(3,1,figsize=(12,9),layout='constrained')
            for j,ax in enumerate(axes):
                if j>=len(test): break
                mask=data['trajectory']==j; ts=test[j]['t'][data['index'][mask]]
                ax.plot(ts,target[mask],color='black',label='truth')
                for key in [('augmented_kalman',-1),('frozen_a2afm',args.seeds[0]),
                            ('mixed_a2afm',args.seeds[0]),('mixed_regression',args.seeds[0])]:
                    ax.plot(ts,predictions[key][mask],label=key[0],alpha=.8,lw=.8)
                ax.set(xlim=(2,10),title=test[j]['kind'],ylabel='Disturbance'); ax.grid(alpha=.25)
            axes[0].legend(); axes[-1].set_xlabel('Time (s)'); fig.savefig(out/'xv_5pct.png',dpi=160); plt.close(fig)
        csv_save(out/'metrics.csv',rows); csv_save(out/'trajectory_metrics.csv',individual)
    write_report(out,rows,individual,scales,args)
    save(out/'status.json',{'status':'complete','finished_utc':datetime.now(timezone.utc).isoformat(),
        'scenarios':len(SCENARIOS),'trained_models':len(models),'metric_rows':len(rows)})
    log('Complete: '+str(out/'REPORT.md'))


if __name__=='__main__': main()
