"""Aggregate by trajectory; training seeds do not create independent test trials."""
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'results/closed_loop'
    lines=['# 闭环分组比较与配对统计','',
           '以下位置误差以系统位置单位计，控制输入以系统力单位计。每个冲击宽度只有6条独立测试轨迹。',
           '', '| 阶段 | 脉冲宽度/信号 | 方法 | 扰动RMSE | 冲击RMSE | 跟踪RMSE | 平均轨迹峰值误差 | 平均恢复秒 | 未恢复比例 |',
           '|---|---|---|---:|---:|---:|---:|---:|---:|']
    tables=[]
    for stage in ['open_frozen','closed_frozen','closed_adapted']:
        rows=json.loads((out/f'{stage}_metrics.json').read_text())
        for family in ['smooth','pulse_1','pulse_4','pulse_10']:
            for method in ['none','dob','kalman','regression','a2afm']:
                rr=[r for r in rows if r['family']==family and r['method']==method]
                values=[]; rec=dict(stage=stage,family=family,method=method)
                for key in ['d_rmse','shock_rmse','tracking_rmse','peak_error','recovery_s','recovery_fail_fraction']:
                    v=[r[key] for r in rr if r[key] is not None]
                    number=float(np.sqrt(np.mean(np.square(v)))) if v and key.endswith('rmse') else float(np.mean(v)) if v else None
                    rec[key]=number; values.append(f'{number:.5f}' if number is not None else '—')
                tables.append(rec)
                lines.append('| '+stage+' | '+family+' | '+method+' | '+' | '.join(values)+' |')
    lines+=['','## 新闭环模型：配对轨迹Bootstrap','',
            '对每条轨迹先平均三个训练种子的平方误差，再对24条轨迹配对重采样5000次。正值表示A2AFM误差更小；不使用窗口独立重采样。',
            '', '| 对照 | 指标 | 对照RMSE − A2AFM RMSE | 95%区间 |','|---|---|---:|---:|']
    rows=json.loads((out/'closed_adapted_metrics.json').read_text())
    rng=np.random.default_rng(91001); comparisons=[]
    for key in ['tracking_rmse','d_rmse']:
        def arr(method):
            return np.array([np.mean([r[key]**2 for r in rows if r['method']==method and r['trajectory']==i]) for i in range(24)])
        fm=arr('a2afm'); idx=rng.integers(24,size=(5000,24))
        for method in ['none','dob','kalman','regression']:
            base=arr(method); samples=np.sqrt(base[idx].mean(1))-np.sqrt(fm[idx].mean(1))
            lo,hi=np.quantile(samples,[.025,.975]); delta=np.sqrt(base.mean())-np.sqrt(fm.mean())
            comparisons.append(dict(method=method,metric=key,delta=float(delta),ci=[float(lo),float(hi)]))
            lines.append(f'| {method} | {key} | {delta:.6f} | [{lo:.6f}, {hi:.6f}] |')
    # The measurement residual noise is the same across methods in an exactly known plant.
    z=np.load(out/'open_frozen_none_-1.npz'); mse=[]; pulse=[]
    manifest=json.loads((out/'test_manifest.json').read_text())
    for i in range(24):
        err=z[f'dhat_{i}']-z[f'd_{i}']; mse.append(np.mean(err[z[f't_{i}']>=1]**2))
        parts=[err[event['start']:event['end']]**2 for event in manifest[i]['events']]
        if parts: pulse.append(float(np.mean(np.concatenate(parts))))
    raw=dict(d_rmse=float(np.sqrt(np.mean(mse))),shock_rmse=float(np.sqrt(np.mean(pulse))))
    lines+=['','## 原始加速度残差参照','',
            f'原始d_hat全时段RMSE={raw["d_rmse"]:.5f}；冲击采样区间RMSE={raw["shock_rmse"]:.5f}。',
            '两项都先按轨迹取MSE再跨轨迹开方，与主表加权一致；短脉冲不会因样本更少而失去权重。',
            '残差噪声等于m*epsilon，与控制命令无关。原模型冲击表现应与该参照一起看，不能只比较全时段RMSE。']
    (out/'ANALYSIS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (out/'analysis.json').write_text(json.dumps(dict(grouped=tables,bootstrap=comparisons,raw=raw),indent=2),encoding='utf-8')
    print(json.dumps(dict(bootstrap=comparisons,raw=raw),indent=2))

if __name__=='__main__': main()
