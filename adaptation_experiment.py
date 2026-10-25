"""Two-round closed-loop adaptation, with state-shift and pulse-exposure controls."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import time

import numpy as np
import torch
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parent/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from a2afm.inference import DisturbanceEstimator
from closed_loop.adaptation import METHODS, closed_score, collect_shared, fine_tune, mixed_specs
from closed_loop.core import measures, run, scenarios
from experiment import ROOT, log, save_json

MODES=('state_only','state_and_pulses')


def original_path(args,method,seed):
    kind='regression' if method=='regression' else 'a2afm'
    return ROOT/args.initial/method/f'{kind}_seed{seed}.pt'


def round_path(out,mode,method,seed,round_number):
    return out/mode/f'{method}_seed{seed}_round{round_number}.pt'


def pool(args,out,mode,round_number,collectors):
    cache=out/'cache'/f'{mode}_round{round_number}.npz'
    if args.resume and cache.exists():
        with np.load(cache) as data: return {name:data[name] for name in data.files}
    # Both modes start from identical base specifications. Pulses are the only added factor.
    seed=110000+round_number*1000
    specs=mixed_specs(args.train_trajectories,seed,pulse_half=mode=='state_and_pulses')
    data,manifest=collect_shared(specs,collectors,seed+500)
    cache.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(cache,**data)
    save_json(out/f'{mode}_round{round_number}_manifest.json',dict(seed=seed,
              trajectories=len(specs),windows=len(data['source']),
              collector_seed=args.seeds[0],collector_counts=dict(Counter(r['collector'] for r in manifest)),
              pulse_trajectories=sum(r['has_pulse'] for r in manifest),trajectories_manifest=manifest,
              cache_sha256=hashlib.sha256(cache.read_bytes()).hexdigest()))
    log(f'adapt shared pool {mode} round={round_number}: {len(specs)} trajectories, {len(data["source"])} windows')
    return data


def evaluate(args,out,estimators):
    suites=dict(mixed=mixed_specs(args.test_mixed,140000,sigma=.5),
                shock=scenarios(args.test_shock,150000))
    rows=[]; examples={}
    for suite,specs in suites.items():
        for stage in ('frozen',*MODES):
            for method in METHODS:
                for seed in args.seeds:
                    est=estimators[(stage,method,seed)]
                    traces=run(specs,'a2afm',est)
                    for tid,tr in enumerate(traces):
                        rows.append(dict(suite=suite,stage=stage,method=method,seed=seed,
                                         trajectory=tid,family=tr['kind'],**measures(tr)))
                    if seed==args.seeds[0]:
                        tid=1 if suite=='shock' else min(6,len(specs)-1)
                        examples[(suite,stage,method)]=traces[tid]
        for method in ('none','dob','kalman'):
            traces=run(specs,method,bandwidth=24.,kalman_q=1e5)
            for tid,tr in enumerate(traces):
                rows.append(dict(suite=suite,stage='classical',method=method,seed=-1,
                                 trajectory=tid,family=tr['kind'],**measures(tr)))
        log(f'adaptation held-out test completed: {suite}')
    save_json(out/'test_metrics.json',rows)
    np.savez_compressed(out/'example_traces.npz',**{
        f'{suite}__{stage}__{method}__{name}':tr[name]
        for (suite,stage,method),tr in examples.items()
        for name in ('t','d','estimate','x','v','u','command','error')})
    return rows,examples


def pooled(rows,key):
    values=[r[key] for r in rows if r[key] is not None]
    return float(np.sqrt(np.mean(np.square(values)))) if values else None


def bootstrap(rows,out):
    rng=np.random.default_rng(20261022); records=[]
    for suite in ('mixed','shock'):
        tids=sorted({r['trajectory'] for r in rows if r['suite']==suite})
        indices=rng.integers(len(tids),size=(5000,len(tids)))
        def mse(stage,method):
            return np.array([np.mean([r['tracking_rmse']**2 for r in rows
                       if r['suite']==suite and r['stage']==stage and r['method']==method
                       and r['trajectory']==tid]) for tid in tids])
        for stage in ('frozen',*MODES):
            a=mse(stage,'single_fm'); b=mse(stage,'midpoint_fm')
            delta=np.sqrt(a[indices].mean(1))-np.sqrt(b[indices].mean(1))
            records.append(dict(suite=suite,comparison='single_minus_midpoint',stage=stage,
                                delta=float(np.sqrt(a.mean())-np.sqrt(b.mean())),
                                low=float(np.percentile(delta,2.5)),high=float(np.percentile(delta,97.5))))
        for mode in MODES:
            a=mse(mode,'single_fm'); b=mse('frozen','single_fm')
            delta=np.sqrt(a[indices].mean(1))-np.sqrt(b[indices].mean(1))
            records.append(dict(suite=suite,comparison='adapted_minus_frozen_single',stage=mode,
                                delta=float(np.sqrt(a.mean())-np.sqrt(b.mean())),
                                low=float(np.percentile(delta,2.5)),high=float(np.percentile(delta,97.5))))
    save_json(out/'paired_bootstrap.json',dict(seed=20261022,repetitions=5000,unit='trajectory',comparisons=records))
    return records


def report(args,out,rows,examples,histories,comparisons):
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,suite in zip(axes,('mixed','shock')):
        stages=('frozen',*MODES); positions=np.arange(len(stages))
        for offset,method in enumerate(METHODS):
            values=[pooled([r for r in rows if r['suite']==suite and r['stage']==s and r['method']==method],
                           'tracking_rmse') for s in stages]
            ax.bar(positions+(offset-1)*.24,values,width=.24,label=method)
        ax.set(xticks=positions,xticklabels=stages,title=suite,ylabel='tracking RMSE'); ax.grid(axis='y',alpha=.2)
    axes[0].legend(); fig.savefig(out/'tracking_comparison.png',dpi=150); plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(12,7),layout='constrained')
    for ax,suite in zip(axes,('mixed','shock')):
        for stage in ('frozen',*MODES):
            tr=examples[(suite,stage,'single_fm')]
            ax.plot(tr['t'],tr['error'],label=stage,lw=.9)
        ax.set(title=f'single_fm, {suite}',ylabel='tracking error',xlabel='time (s)'); ax.grid(alpha=.2)
    axes[0].legend(); fig.savefig(out/'single_tracking.png',dpi=150); plt.close(fig)
    summary=[]
    for suite in ('mixed','shock'):
        for stage in ('frozen',*MODES):
            for method in METHODS:
                group=[r for r in rows if r['suite']==suite and r['stage']==stage and r['method']==method]
                summary.append(dict(suite=suite,stage=stage,method=method,
                                    **{key:pooled(group,key) for key in ('tracking_rmse','d_rmse','shock_rmse')},
                                    saturation_fraction=float(np.mean([r['saturation_fraction'] for r in group]))))
    save_json(out/'summary.json',summary)
    lines=['# 单步与多步 FM 的闭环适配实验','',
           '## 要回答的问题','',
           '检验单步FM在冻结权重闭环测试中的劣势，能否通过闭环数据适配改善；'
           '将闭环状态分布变化与冲击信号暴露分成两个适配组，避免把两者的作用混为一谈。','',
           '## 实验设计','',
           '| 组别 | 训练数据 | 作用 |','|---|---|---|',
           '| frozen | 上一实验开环权重直接使用 | 固定基线 |',
           '| state_only | 闭环下的七类平滑/阶跃混合轨迹，不添加矩形冲击 | 适应闭环状态分布 |',
           '| state_and_pulses | 相同底层轨迹，其中后一半加入矩形冲击 | 再检验冲击暴露的作用 |','',
           f'模型：single_fm、midpoint_fm、regression；种子{args.seeds}，全部本地CPU。'
           '各模型从上一实验对应种子的最佳开环权重开始，保持原网络结构、归一化统计、'
           '速度/结果损失和归一化标准差0.01的训练源噪声。',
           f'每组做两轮闭环收集，每轮{args.train_trajectories}条12秒轨迹。'
           '用无补偿、DOB、单步FM、多步FM、回归五种策略等分收集；'
           f'神经策略使用种子{args.seeds[0]}，第二轮使用第一轮验证选择的权重。'
           '同一适配组内所有学习器共享完全相同的数据；第二轮混合第一轮数据回放。',
           '两种适配组的底层扰动、系统参数、初始状态、加速度噪声完全配对；'
           '加冲击使用独立随机数流。冲击幅值由J/width定义，|J|∈[0.15,0.35]，宽度0.02/0.08/0.20秒。',
           f'每轮{args.round_steps}次更新，合计{2*args.round_steps}次，batch={args.batch}，'
           f'AdamW学习率{args.lr}、weight_decay=1e-4、梯度裁剪5；每轮重建优化器。'
           '第二轮从第一轮验证选择的最佳模型开始，不从末次权重开始。',
           f'每{args.validation_every}次更新用独立的12条混合+12条冲击闭环验证轨迹评估，'
           '按跨轨迹跟踪MSE平均后开方选择检查点，包含更新0的父模型作为候选。'
           '两种适配组共享验证集，验证信号含冲击；state_only仅训练数据不含额外冲击。',
           '收集数据只使用训练规格，训练标签使用仿真扰动真值；部署输入仍仅含过去观测。'
           '验证/测试轨迹不加入训练池；控制器、饱和、20ms周期和历史热身规则固定。',
           f'独立测试：{args.test_mixed}条混合轨迹（seed140000）、{args.test_shock}条冲击轨迹（seed150000）；'
           '测试种子与上一次报告不同，因此通过本实验重跑的frozen基线比较，不能直接拼接旧表数值。',
           '本主实验使用同步、无额外计算延迟的控制，用于隔离适配作用；计算延迟作为独立因素另行复核。','',
           '## 独立测试结果','',
           '| 测试集 | 适配组 | 方法 | 跟踪RMSE | 扰动RMSE | 冲击RMSE | 饱和比例 |',
           '|---|---|---|---:|---:|---:|---:|']
    for r in summary:
        shock='—' if r['shock_rmse'] is None else f"{r['shock_rmse']:.5f}"
        lines.append(f"| {r['suite']} | {r['stage']} | {r['method']} | {r['tracking_rmse']:.5f} | {r['d_rmse']:.5f} | {shock} | {r['saturation_fraction']:.4f} |")
    lines+=['','RMSE先平均种子和轨迹的MSE再开方；冲击RMSE仅统计有冲击轨迹。'
            '训练种子共享数据，不视为独立数据集重复。','',
            '经典控制参照（沿用上一实验验证选择的DOB=24 rad/s、Kalman q=1e5，未用本次测试集调参）：','',
            '| 测试集 | 方法 | 跟踪RMSE | 扰动RMSE |', '|---|---|---:|---:|']
    for suite in ('mixed','shock'):
        for method in ('none','dob','kalman'):
            group=[r for r in rows if r['suite']==suite and r['stage']=='classical' and r['method']==method]
            lines.append(f"| {suite} | {method} | {pooled(group,'tracking_rmse'):.5f} | {pooled(group,'d_rmse'):.5f} |")
    lines+=['','## 单步与多步的差距','']
    for suite in ('mixed','shock'):
        group=[r for r in summary if r['suite']==suite]
        def score(stage,method): return next(r['tracking_rmse'] for r in group if r['stage']==stage and r['method']==method)
        frozen=score('frozen','single_fm')
        for mode in MODES:
            a=score(mode,'single_fm'); b=score(mode,'midpoint_fm')
            lines.append(f"- {suite}/{mode}：单步跟踪RMSE相对冻结模型变化{100*(a/frozen-1):+.2f}%；"
                         f"单步/多步跟踪误差比为{a/b:.2f}。负的变化表示适配改善。")
    lines+=['','## 配对轨迹bootstrap','',
            '5000次配对重采样，单位为整条测试轨迹，先对同轨迹不同种子的MSE求平均。'
            '区间仅反映固定训练数据与模型条件下测试轨迹抽样的不确定性，不包含训练集变化，未校正多重比较。','',
            '| 测试集 | 对比 | 适配组 | 跟踪RMSE差 | 95%区间 |','|---|---|---|---:|---|']
    for r in comparisons:
        lines.append(f"| {r['suite']} | {r['comparison']} | {r['stage']} | {r['delta']:+.6f} | [{r['low']:+.6f}, {r['high']:+.6f}] |")
    audit=[]
    for mode in MODES:
        for method in METHODS:
            for seed in args.seeds:
                for rnd in (1,2):
                    path=round_path(out,mode,method,seed,rnd)
                    best=torch.load(path,map_location='cpu',weights_only=False)
                    last=torch.load(path.with_name(path.stem+'_last.pt'),map_location='cpu',weights_only=False)
                    if last['adaptation_step']!=args.round_steps or best['tracking_score']!=min(r['tracking_rmse'] for r in last['adaptation_history']):
                        raise ValueError(f'Invalid adaptation checkpoint selection: {path}')
                    audit.append(dict(mode=mode,method=method,seed=seed,round=rnd,
                                      selected_step=best['adaptation_step'],tracking_score=best['tracking_score'],
                                      completed_step=last['adaptation_step']))
    save_json(out/'checkpoint_audit.json',audit)
    lines+=['','## 验证选择审计','',
            '更新0表示保留父模型。全部末次检查点核对已完成规定更新数，最佳检查点核对为验证跟踪误差最低者。','',
            '| 组别 | 方法 | 种子 | 第一轮选择更新 | 第二轮选择更新 |','|---|---|---:|---:|---:|']
    for mode in MODES:
        for method in METHODS:
            for seed in args.seeds:
                steps=[next(r['selected_step'] for r in audit if r['mode']==mode and r['method']==method and r['seed']==seed and r['round']==rnd) for rnd in (1,2)]
                lines.append(f'| {mode} | {method} | {seed} | {steps[0]} | {steps[1]} |')
    lines+=['','## 边界与解释','',
            '这是仿真中的监督离线适配，不是部署时使用真值的在线学习，也不是对跟踪损失直接反向传播。'
            '训练仍优化扰动监督损失，跟踪误差仅用于独立验证模型选择。',
            '第二轮共同数据池依赖第一轮种子11的适配控制器，因此不同种子并非独立收集数据重复。'
            '每轮验证包括父模型；若没有改进，可以保留父模型，需同时查看选择步骤。',
            '额外冲击适配组同时改变信号暴露和由此产生的闭环状态，不能声称完全分离二者的因果贡献。'
            'state_only也包含原先的阶跃信号，仅不包含新增的窄矩形冲击。',
            '真实传感器、系统参数失配、模型结构/超参数独立调优尚未覆盖。'
            '比较的是相同更新次数，单步/多步训练计算量不同。','',
            '## 复现与产物','',
            '```powershell','.\\.venv\\Scripts\\python.exe -m unittest test_adaptation test_single_step test_core closed_loop.test_core -v',
            '.\\.venv\\Scripts\\python.exe adaptation_experiment.py',
            '# 中断后使用相同参数加 --resume','```','',
            'config.json、source_hashes.json、split_manifest.json记录配置与隔离；各组目录含每轮最佳、'
            '末次权重和验证历史。训练窗口缓存cache/留在本地且不提交，可由收集规格与检查点重建；'
            '每轮manifest记录缓存SHA-256和收集策略。test_metrics.json保留逐轨迹指标。','',
            '![跟踪误差汇总](tracking_comparison.png)','', '![单步FM闭环跟踪曲线](single_tracking.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='results/closed_adaptation')
    p.add_argument('--initial',default='results/single_step_mixed')
    p.add_argument('--train-trajectories',type=int,default=360)
    p.add_argument('--round-steps',type=int,default=2500)
    p.add_argument('--validation-every',type=int,default=500)
    p.add_argument('--test-mixed',type=int,default=56)
    p.add_argument('--test-shock',type=int,default=24)
    p.add_argument('--batch',type=int,default=128)
    p.add_argument('--lr',type=float,default=.0002)
    p.add_argument('--source-noise-std',type=float,default=.01)
    p.add_argument('--seeds',type=int,nargs='+',default=[11,22,33])
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--resume',action='store_true')
    args=p.parse_args()
    if min(args.train_trajectories,args.round_steps,args.validation_every,args.test_mixed,args.test_shock)<1:
        p.error('counts must be positive')
    torch.set_num_threads(args.threads); torch.use_deterministic_algorithms(True)
    out=ROOT/args.out; out.mkdir(parents=True,exist_ok=True)
    files=[ROOT/'adaptation_experiment.py',ROOT/'closed_loop/adaptation.py',ROOT/'closed_loop/core.py',
           ROOT/'experiment.py',*sorted((ROOT/'a2afm').glob('*.py'))]
    files += [original_path(args,m,s) for m in METHODS for s in args.seeds]
    hashes={f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    if (out/'config.json').exists():
        previous=json.loads((out/'config.json').read_text(encoding='utf-8'))
        if not args.resume or any(previous[k]!=v for k,v in vars(args).items() if k!='resume'):
            raise ValueError('Use a new output directory or --resume with identical configuration')
        if json.loads((out/'source_hashes.json').read_text())!=hashes: raise ValueError('Source hash mismatch')
    else:
        save_json(out/'config.json',vars(args)); save_json(out/'source_hashes.json',hashes)
    save_json(out/'environment.json',dict(device='cpu',torch=torch.__version__,numpy=np.__version__,
                                          platform=platform.platform(),threads=args.threads))
    val=mixed_specs(12,120000,sigma=.5)+scenarios(12,130000)
    save_json(out/'split_manifest.json',dict(train_seeds=[111000,112000],validation_seeds=[120000,130000],
              test_seeds=[140000,150000],validation_ids=[s['trajectory_id'] for s in val],
              test_mixed_ids=[f'140000:{i}' for i in range(args.test_mixed)],
              test_shock_ids=[f'150000:{i}' for i in range(args.test_shock)]))
    estimators={('frozen',m,s):DisturbanceEstimator(original_path(args,m,s)) for m in METHODS for s in args.seeds}
    histories={}
    for mode in MODES:
        replay=[]
        for round_number in (1,2):
            save_json(out/'status.json',dict(status='collecting',mode=mode,round=round_number))
            collector_paths={m:original_path(args,m,args.seeds[0]) if round_number==1 else
                             round_path(out,mode,m,args.seeds[0],1) for m in METHODS}
            collectors={m:DisturbanceEstimator(path) for m,path in collector_paths.items()}
            data=pool(args,out,mode,round_number,collectors); replay.append(data)
            merged={k:np.concatenate([d[k] for d in replay]) for k in ('source','target','condition')}
            for method in METHODS:
                for seed in args.seeds:
                    save_json(out/'status.json',dict(status='training',mode=mode,round=round_number,method=method,seed=seed))
                    parent=original_path(args,method,seed) if round_number==1 else round_path(out,mode,method,seed,1)
                    est,history=fine_tune(parent,merged,val,args,out/mode,method,seed,round_number)
                    histories[(mode,method,seed,round_number)]=history
                    if round_number==2: estimators[(mode,method,seed)]=est
    save_json(out/'status.json',dict(status='testing'))
    rows,examples=evaluate(args,out,estimators)
    comparisons=bootstrap(rows,out); report(args,out,rows,examples,histories,comparisons)
    save_json(out/'status.json',dict(status='complete'))
    log(f'adaptation experiment complete: {out / "REPORT.md"}')


if __name__=='__main__': main()
