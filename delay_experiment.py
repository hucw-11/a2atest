"""Independent compute-delay check for frozen and closed-loop-adapted weights."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time

import numpy as np
import torch
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parent/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from a2afm.inference import DisturbanceEstimator
from closed_loop.adaptation import METHODS
from closed_loop.core import LENGTH, reference, scenarios
from closed_loop.delayed import delayed_measures, run_delayed
from experiment import ROOT, log, save_json


def latency_profile(estimator,repeats=300):
    """Public estimator API plus nominal controller arithmetic; batch size one."""
    h=np.zeros(LENGTH,dtype=np.float32); params=np.array([1.,.6,2.],dtype=np.float32)
    samples=[]
    for i in range(repeats+30):
        start=time.perf_counter_ns()
        estimate,_=estimator.estimate(h,h,h,h,params)
        r,rv,ra=reference(2.)
        nominal=params[1]*0.+params[2]*0.+params[0]*(ra+8*rv+16*r)
        command=np.clip(nominal-np.clip(estimate,-12,12),-12,12)
        elapsed=(time.perf_counter_ns()-start)/1e9
        if i>=30: samples.append(elapsed)
    return dict(p50_s=float(np.median(samples)),p95_s=float(np.percentile(samples,95)),
                max_s=float(np.max(samples)),samples_s=samples)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='results/computation_delay')
    p.add_argument('--adaptation',default='results/closed_adaptation')
    p.add_argument('--initial',default='results/single_step_mixed')
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--seeds',type=int,nargs='+',default=[11,22,33])
    p.add_argument('--test-trajectories',type=int,default=24)
    args=p.parse_args(); torch.set_num_threads(args.threads)
    torch.use_deterministic_algorithms(True)
    out=ROOT/args.out; out.mkdir(parents=True,exist_ok=True)
    if json.loads((ROOT/args.adaptation/'status.json').read_text())['status']!='complete':
        raise ValueError('Complete adaptation training before measuring uncontended CPU latency')
    save_json(out/'config.json',vars(args))
    save_json(out/'source_hashes.json',{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
              for name in ('delay_experiment.py','closed_loop/delayed.py','closed_loop/core.py','a2afm/inference.py')})
    profiles=[]; rows=[]; names=('zero','measured_p50','measured_p95','fixed_5ms','fixed_20ms','fixed_40ms')
    specs=scenarios(args.test_trajectories,150000)
    for stage in ('frozen','state_and_pulses'):
        for method in METHODS:
            for seed in args.seeds:
                if stage=='frozen':
                    kind='regression' if method=='regression' else 'a2afm'
                    path=ROOT/args.initial/method/f'{kind}_seed{seed}.pt'
                else:
                    path=ROOT/args.adaptation/stage/f'{method}_seed{seed}_round2.pt'
                estimator=DisturbanceEstimator(path); profile=latency_profile(estimator)
                profiles.append(dict(stage=stage,method=method,seed=seed,checkpoint=str(path),
                                     checkpoint_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**profile))
                for condition,delay in zip(names,(0.,profile['p50_s'],profile['p95_s'],.005,.020,.040)):
                    traces=run_delayed(specs,'a2afm',estimator,delay_s=delay)
                    for tid,tr in enumerate(traces):
                        rows.append(dict(stage=stage,method=method,seed=seed,condition=condition,
                                         delay_s=delay,trajectory=tid,**delayed_measures(tr)))
                log(f'delay check {stage}/{method}/{seed}, software p50={profile["p50_s"]*1000:.4f}ms')
    save_json(out/'latency_profiles.json',profiles); save_json(out/'trajectory_metrics.json',rows)
    summary=[]
    for stage in ('frozen','state_and_pulses'):
        for method in METHODS:
            for condition in names:
                group=[r for r in rows if r['stage']==stage and r['method']==method and r['condition']==condition]
                summary.append(dict(stage=stage,method=method,condition=condition,
                     tracking_rmse=float(np.sqrt(np.mean([r['tracking_rmse']**2 for r in group]))),
                     delay_ms=float(np.mean([r['delay_s'] for r in group]))*1000,
                     skipped_fraction=float(np.mean([r['skipped_fraction'] for r in group])),
                     saturation_fraction=float(np.mean([r['saturation_fraction'] for r in group]))))
    save_json(out/'summary.json',summary)
    lines=['# 计算延时下的闭环复核','',
           '本实验与适配主实验分离，使用冻结权重与加入冲击适配后的权重，不在有延时仿真中再次训练或选模型。',
           '## 延时如何进入动力学','',
           '在t_k采集观测并开始计算，t_k+δ才施加新控制。期间旧控制量继续驱动系统。'
           'δ小于20ms时，将同一采样区间分成两段，分别使用旧/新控制量进行精确ZOH推进。'
           'δ等于或超过周期时，单个计算工作线程在忙碌采样点跳过新任务，持续采集历史；'
           '不排队、不抢占，完成后在下一采样点启动新任务。',
           '采样边界恰好完成的任务在本次采样后生效，再允许启动新计算；'
           '这与原零延时实现的“先测量、再施加控制”顺序一致。前23个点为共同理想PD热身，之后开始施加延时。',
           '## 软件耗时测量','',
           '本地CPU、batch=1、30次预热后测300次，测量公开estimate API和PD控制算术，'
           '包含输入检查、归一化、网络推理、反归一化与控制限幅；不包含传感器/执行器I/O、通信、'
           '操作系统调度或真实硬件抖动。各模型和种子单独测量。',
           'measured_p50/measured_p95使用对应分位数作为恒定软件计算延时；P95不是硬件最坏执行时间保证。'
           '另外统一施加5/20/40ms延时做敏感性测试。仿真批计算只为加速独立轨迹计算，'
           '不把24个系统的批吞吐冒充单系统延时。',
           f'与适配主实验使用同一独立冲击测试规格seed150000、{args.test_trajectories}条轨迹。'
           '所有测量在适配训练结束后进行。','',
           '| 权重 | 方法 | 延时条件 | 平均延时(ms) | 跟踪RMSE | 跳过任务比例 | 饱和时间比例 |',
           '|---|---|---|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f"| {r['stage']} | {r['method']} | {r['condition']} | {r['delay_ms']:.4f} | {r['tracking_rmse']:.5f} | {r['skipped_fraction']:.3f} | {r['saturation_fraction']:.4f} |")
    lines+=['','RMSE先平均种子及轨迹的MSE再开方。控制RMS/饱和时间在旧/新控制的分段区间上积分，'
            '不将尚未完成计算的新控制提前作用于植物。',
            '## 解释范围','',
            '实测软件延时若远小于20ms，单步计算更快不一定转化为显著跟踪优势。'
            '固定延时敏感性只说明当前控制器在指定调度策略下的表现，不能替代真实硬件实时性测量。'
            '尚未模拟网络传输、随机调度抖动、并行控制任务或延时补偿控制器。','',
            '```powershell','.\\.venv\\Scripts\\python.exe -m unittest test_delayed -v',
            '.\\.venv\\Scripts\\python.exe delay_experiment.py','```','',
            '![计算延时与跟踪误差](delay_comparison.png)']
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,stage in zip(axes,('frozen','state_and_pulses')):
        for method in METHODS:
            values=[next(r['tracking_rmse'] for r in summary if r['stage']==stage and r['method']==method and r['condition']==name)
                    for name in ('zero','fixed_5ms','fixed_20ms','fixed_40ms')]
            ax.plot([0,5,20,40],values,'o-',label=method)
        ax.set(title=stage,xlabel='fixed computation delay (ms)',ylabel='tracking RMSE'); ax.grid(alpha=.2)
    axes[0].legend(); fig.savefig(out/'delay_comparison.png',dpi=150); plt.close(fig)
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save_json(out/'status.json',dict(status='complete'))
    log(f'computation delay check complete: {out / "REPORT.md"}')


if __name__=='__main__': main()
