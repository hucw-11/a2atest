"""Post-hoc descriptive statistics and runtime, without selecting models on test data."""
import argparse
import csv
import json
from pathlib import Path
import time
import numpy as np
import torch
from a2afm.inference import DisturbanceEstimator
from a2afm.models import integrate

def main():
    p=argparse.ArgumentParser(); p.add_argument('--out',default='results/main'); args=p.parse_args()
    root=Path(args.out); config=json.loads((root/'config.json').read_text())
    torch.set_num_threads(config['threads'])
    with (root/'trajectory_metrics.csv').open(encoding='utf-8') as f: rows=list(csv.DictReader(f))
    selected=[r for r in rows if r['scenario']=='gaussian_mid']
    def mses(method):
        return np.array([np.mean([float(r['rmse'])**2 for r in selected if r['method']==method and int(r['trajectory'])==i])
                         for i in range(config['test_trajectories'])])
    fm=mses('a2afm'); rng=np.random.default_rng(20261013)
    indices=rng.integers(len(fm),size=(5000,len(fm)))
    comparisons=[]
    for method in ['raw','ema','local_poly','kalman','physics_backward','regression','fm_only']:
        if not any(r['method']==method for r in selected): continue
        baseline=mses(method)
        differences=np.sqrt(baseline[indices].mean(1))-np.sqrt(fm[indices].mean(1))
        comparisons.append({'baseline':method,'rmse_baseline_minus_a2afm':float(np.sqrt(baseline.mean())-np.sqrt(fm.mean())),
                            'paired_trajectory_bootstrap_95':np.quantile(differences,[.025,.975]).tolist()})
    timings=[]
    for method in ['a2afm','regression','fm_only']:
        path=root/f'{method}_seed{config["seeds"][0]}.pt'
        if not path.exists(): continue
        est=DisturbanceEstimator(path); model=est.model
        src=torch.zeros(1,est.length); cond=torch.zeros(1,3*est.length+3)
        def run():
            return integrate(model,src,cond,est.steps) if model.flow else model(src,cond)
        with torch.inference_mode():
            for _ in range(10): run()
            samples=[]
            for _ in range(100):
                start=time.perf_counter(); run(); samples.append((time.perf_counter()-start)*1000)
        timings.append({'method':method,'parameters':sum(p.numel() for p in model.parameters()),
                        'median_ms_batch1':float(np.median(samples)),'p95_ms_batch1':float(np.quantile(samples,.95)),
                        'scope':'CPU network plus flow integration only; excludes preprocessing and sensor IO'})
    results={'bootstrap':comparisons,'latency':timings}
    (root/'additional_analysis.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    lines=['# 补充分析','','## 配对轨迹 Bootstrap（中等高斯噪声）','',
           '先对每条测试轨迹的各训练种子 MSE 取均值，再以轨迹为单位配对重采样 5000 次；不是对高度重叠的窗口独立重采样。',
           '正差值表示 A2AFM 的 RMSE 更低。这些区间仅描述当前仿真测试分布与训练种子集合，不覆盖真实系统迁移不确定性。',
           '', '| 对照 | RMSE(对照) − RMSE(A2AFM) | 95% 区间 |','|---|---:|---:|']
    for r in comparisons:
        lo,hi=r['paired_trajectory_bootstrap_95']
        lines.append(f'| {r["baseline"]} | {r["rmse_baseline_minus_a2afm"]:.5f} | [{lo:.5f}, {hi:.5f}] |')
    lines+=['','## CPU 推理耗时','','单样本，10 次预热、100 次测量；只包含网络和流积分，不含预处理/传感器 I/O。',
            '', '| 方法 | 参数量 | 中位数 ms | P95 ms |','|---|---:|---:|---:|']
    for r in timings: lines.append(f'| {r["method"]} | {r["parameters"]} | {r["median_ms_batch1"]:.3f} | {r["p95_ms_batch1"]:.3f} |')
    (root/'ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
