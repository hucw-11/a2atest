"""Learning-curve summaries with paired training/test hierarchical bootstrap."""
import argparse
import json
from pathlib import Path
import numpy as np
from experiment import save_json
import matplotlib.pyplot as plt

METHODS = ['A','B','C','direct']
BUDGETS = [100,250,500,1000,2000,4000,8000]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def average_curve(values, coordinates):
    return np.trapezoid(values,x=np.log(coordinates),axis=-1)/np.log(coordinates[-1]/coordinates[0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',default='results/learning_speed')
    args = parser.parse_args()
    out = Path(args.out)
    entries = []
    for path in sorted(out.glob('data*/*_gaussian_*.json')) + sorted(out.glob('data*/*_student.json')):
        entries.append(read(path))
    lookup = {(r['scenario'],r['replica'],r['seed'],r['method'],r['budget']):r for r in entries}
    if len(lookup)!=468:
        raise ValueError(f'Expected 468 evaluations, found {len(lookup)}')
    summaries = []
    for scenario in ('gaussian_mid','gaussian_low','gaussian_high','student'):
        budgets = BUDGETS if scenario=='gaussian_mid' else [1000,8000]
        for budget in budgets:
            for method in METHODS:
                group = [r for r in entries if (r['scenario'],r['budget'],r['method'])==(scenario,budget,method)]
                summaries.append(dict(scenario=scenario,budget=budget,method=method,
                    **{key:float(np.mean([r['summary'][key] for r in group])) for key in group[0]['summary']}))
    save_json(out/'summary.json',summaries)
    # Main endpoint uses all predeclared early budgets, avoiding best-budget selection.
    sample = lookup['gaussian_mid',0,11,'A',100]['trajectories']
    shock_indices = np.array([i for i,r in enumerate(sample) if r['event_mse'] is not None])
    strata = sorted({sample[i]['stratum'] for i in shock_indices})
    groups = [np.array([i for i in shock_indices if sample[i]['stratum']==s]) for s in strata]
    arrays = {}
    for method in METHODS:
        arrays[method] = np.array([[[[r['event_mse'] or 0.,r['background_mse']] for r in
            lookup['gaussian_mid',replica,seed,method,budget]['trajectories']]
            for budget in BUDGETS[:5]] for replica in range(3) for seed in (11,22,33)])
    def endpoint(values,indices,channel):
        curve = np.sqrt(np.mean(values[:,:,indices,channel],axis=-1))
        return float(np.mean(average_curve(curve,BUDGETS[:5])))
    comparisons = []
    for reference in ('A','C','direct'):
        rng = np.random.default_rng(20261108)
        effects = []
        background = []
        for _ in range(5000):
            datasets = rng.integers(0,3,3)
            seeds = rng.integers(0,3,(3,3))
            model_indices = (datasets[:,None]*3+seeds).ravel()
            indices = np.concatenate([rng.choice(group,len(group),replace=True) for group in groups])
            bg_indices = rng.integers(0,720,720)
            b = arrays['B'][model_indices]
            a = arrays[reference][model_indices]
            effects.append(100*(1-endpoint(b,indices,0)/endpoint(a,indices,0)))
            background.append(100*(endpoint(b,bg_indices,1)/endpoint(a,bg_indices,1)-1))
        alpha = .025 if reference in ('A','C') else .05
        effect = 100*(1-endpoint(arrays['B'],shock_indices,0)/endpoint(arrays[reference],shock_indices,0))
        comparisons.append(dict(reference=reference,early_shock_improvement_percent=effect,
            interval=np.quantile(effects,[alpha/2,1-alpha/2]).tolist(),confidence=1-alpha,
            background_degradation_percent=100*(endpoint(arrays['B'],np.arange(720),1)/endpoint(arrays[reference],np.arange(720),1)-1),
            background_interval95=np.quantile(background,[.025,.975]).tolist()))
    save_json(out/'early_comparisons.json',comparisons)
    # Pair each run using optimizer time at the exact stored budgets.
    times = {}
    for replica in range(3):
        for seed in (11,22,33):
            history = read(out/f'data{replica}/seed{seed}_history.json')
            for method in METHODS:
                times[replica,seed,method] = [next(r['optimizer_seconds'] for r in history if r['method']==method and r['step']==budget) for budget in BUDGETS]
    time_rows = []
    for replica in range(3):
        for seed in (11,22,33):
            low = max(times[replica,seed,m][0] for m in METHODS)
            high = min(times[replica,seed,m][4] for m in METHODS)
            grid = np.linspace(np.log(low),np.log(high),100)
            for method in METHODS:
                curve = [lookup['gaussian_mid',replica,seed,method,b]['summary']['shock_rmse'] for b in BUDGETS]
                interpolated = np.interp(grid,np.log(times[replica,seed,method]),curve)
                time_rows.append(dict(replica=replica,seed=seed,method=method,start_seconds=low,end_seconds=high,
                    early_time_area=float(np.trapezoid(interpolated,x=grid)/(grid[-1]-grid[0]))))
    save_json(out/'time_comparison.json',time_rows)
    subgroups = []
    for entry in entries:
        if entry['scenario']!='gaussian_mid':
            continue
        for field in ('family','stratum'):
            for value in sorted({r[field] for r in entry['trajectories']}):
                rows = [r for r in entry['trajectories'] if r[field]==value]
                shock = [r['event_mse'] for r in rows if r['event_mse'] is not None]
                subgroups.append(dict(replica=entry['replica'],seed=entry['seed'],method=entry['method'],budget=entry['budget'],
                    field=field,value=value,shock_rmse=float(np.sqrt(np.mean(shock))) if shock else None,
                    background_rmse=float(np.sqrt(np.mean([r['background_mse'] for r in rows]))),
                    total_rmse=float(np.sqrt(np.mean([r['total_mse'] for r in rows])))))
    save_json(out/'subgroups.json',subgroups)
    fig,axes = plt.subplots(1,3,figsize=(15,4.5),layout='constrained')
    for method in METHODS:
        group = [r for r in summaries if r['method']==method and r['scenario']=='gaussian_mid']
        for ax,key,title in zip(axes,['shock_rmse','background_rmse','onset_rmse'],['Event-balanced shock','Background','Shock onset']):
            ax.plot(BUDGETS,[r[key] for r in group],marker='o',label=method)
            ax.set_xscale('log'); ax.set_yscale('log'); ax.set_title(title+' RMSE')
            ax.set_xlabel('Optimizer updates'); ax.grid(alpha=.2)
    axes[0].legend(); fig.savefig(out/'learning_curves.png',dpi=160); plt.close(fig)
    fig,axes = plt.subplots(2,4,figsize=(16,8),layout='constrained')
    families = sorted({r['value'] for r in subgroups if r['field']=='family'})
    for ax,family in zip(axes.ravel(),families):
        for method in METHODS:
            curve = [np.mean([r['total_rmse'] for r in subgroups if r['field']=='family' and r['value']==family and r['method']==method and r['budget']==b]) for b in BUDGETS]
            ax.plot(BUDGETS,curve,marker='.',label=method)
        ax.set_xscale('log'); ax.set_yscale('log'); ax.set_title(family); ax.grid(alpha=.2)
    axes.ravel()[-1].axis('off'); axes[0,0].legend()
    fig.suptitle('Whole-trajectory RMSE by background family; pulse and non-pulse trajectories included')
    fig.savefig(out/'families.png',dpi=150); plt.close(fig)
    lines = ['# 训练速度实验数值表','', '3 套独立训练数据，每套 3 个配对种子。各预算使用准确更新步的权重，无测试选模。','',
             '| 更新数 | A 冲击 | B 冲击 | C 冲击 | 直接回归冲击 | B 相对 A 改善 |','|---|---:|---:|---:|---:|---:|']
    for budget in BUDGETS:
        values = {r['method']:r['shock_rmse'] for r in summaries if r['scenario']=='gaussian_mid' and r['budget']==budget}
        lines.append(f'| {budget} | '+ ' | '.join(f'{values[m]:.5f}' for m in METHODS)+f' | {100*(1-values["B"]/values["A"]):.2f}% |')
    lines += ['', '## 预先指定的早期曲线比较','', '预算 100–2000，沿 log(更新数) 对冲击 RMSE 曲线积分并归一化。改善为正表示 B 更好。',
              '层级 bootstrap 同时配对重采样训练数据、权重种子与测试轨迹。外层仅 3 套数据，区间精度有限。','',
              '| B 对照 | 冲击曲线改善 | 区间 | 背景曲线恶化 |','|---|---:|---|---:|']
    for row in comparisons:
        lines.append(f'| {row["reference"]} | {row["early_shock_improvement_percent"]:.2f}% | {row["interval"]} | {row["background_degradation_percent"]:.2f}% |')
    lines += ['', '## 插值后的相近优化耗时比较','', '每个配对运行取四种方法共有的早期耗时区间，在 log 时间上插值。排除采样、验证和磁盘保存耗时，属于探索性比较。','', '| 方法 | 平均冲击曲线面积 |','|---|---:|']
    for method in METHODS:
        lines.append(f'| {method} | {np.mean([r["early_time_area"] for r in time_rows if r["method"]==method]):.5f} |')
    lines += ['', '## 其他噪声条件','', '| 场景 | 更新数 | A 冲击 | B 冲击 | C 冲击 | 直接回归冲击 |','|---|---:|---:|---:|---:|---:|']
    for scenario in ('gaussian_low','gaussian_high','student'):
        for budget in (1000,8000):
            group = {r['method']:r['shock_rmse'] for r in summaries if r['scenario']==scenario and r['budget']==budget}
            lines.append(f'| {scenario} | {budget} | '+' | '.join(f'{group[m]:.5f}' for m in METHODS)+' |')
    lines += ['', '## 1000 更新时，各背景信号族的背景 RMSE','',
              '剔除新增矩形脉冲及随后0.5秒，保留信号族本身的阶跃变化。','',
              '| 信号族 | A | B | C | 直接回归 |','|---|---:|---:|---:|---:|']
    for family in families:
        values = [np.mean([r['background_rmse'] for r in subgroups if r['field']=='family' and r['value']==family and r['method']==m and r['budget']==1000]) for m in METHODS]
        lines.append(f'| {family} | '+' | '.join(f'{v:.5f}' for v in values)+' |')
    lines += ['', '## 1000 更新时，各冲击制度与宽度的 RMSE','',
              'impulse表示固定冲量范围，amplitude表示幅值与宽度独立。尾部编号乘20即毫秒宽度。','',
              '| 分层 | A | B | C | 直接回归 |','|---|---:|---:|---:|---:|']
    for stratum in strata:
        values = [np.mean([r['shock_rmse'] for r in subgroups if r['field']=='stratum' and r['value']==stratum and r['method']==m and r['budget']==1000]) for m in METHODS]
        lines.append(f'| {stratum} | '+' | '.join(f'{v:.5f}' for v in values)+' |')
    (out/'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(comparisons,indent=2))


if __name__=='__main__':
    main()
