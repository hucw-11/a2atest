"""Aggregate paired repeats, trajectory bootstrap, audits, plots and report tables."""
import argparse
import csv
import json
import os
from pathlib import Path

import numpy as np
import torch
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parent/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from experiment import save_json
from shock_validation.data import make_specs,file_hash


def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def arrays(out,method,key,stage='shadow'):
    output=[]
    for rep in range(3):
        values=[]
        for seed in (11,22,33):
            payload=read(out/f'data{rep}/{method}_seed{seed}_{stage}.json')
            rows=payload['trajectories'] if stage=='shadow' else payload
            values.append([np.nan if row[key] is None else row[key] for row in rows])
        output.append(values)
    return np.array(output)


def paired_bootstrap(b,a,strata,count=5000,alpha=.025,root=True):
    """Shared test trajectories across all runs; paired training resampling too.

    Strata have fixed equal composition. b/a shape: data, weight_seed, trajectory.
    Filtering removes background trajectories for event-only endpoints.
    """
    mask=np.isfinite(a[0,0]) & np.isfinite(b[0,0]); a=a[:,:,mask]; b=b[:,:,mask]; strata=np.array(strata)[mask]
    groups=[np.flatnonzero(strata==s) for s in sorted(set(strata))]
    rng=np.random.default_rng(7142026)
    def statistic(values):
        per_run=np.mean(values,axis=-1)
        return np.mean(np.sqrt(per_run) if root else per_run)
    observed=100*(1-statistic(b)/statistic(a)); conditional=[]; hierarchical=[]
    for _ in range(count):
        index=np.concatenate([rng.choice(group,len(group),replace=True) for group in groups])
        aa=a[:,:,index]; bb=b[:,:,index]
        conditional.append(100*(1-statistic(bb)/statistic(aa)))
        datasets=rng.integers(0,3,3); weights=rng.integers(0,3,(3,3))
        aa=aa[datasets[:,None],weights]; bb=bb[datasets[:,None],weights]
        hierarchical.append(100*(1-statistic(bb)/statistic(aa)))
    interval=lambda v: [float(x) for x in np.quantile(v,[alpha/2,1-alpha/2])]
    return dict(improvement_percent=float(observed),conditional_interval=interval(conditional),
                exploratory_hierarchical_interval=interval(hierarchical),confidence=1-alpha,
                paired_trajectory_count=int(mask.sum()),bootstrap_replicates=count)


def aggregate_shadow(out):
    rows=read(out/'shadow_summary.json'); grouped={}
    for method in dict.fromkeys(r['method'] for r in rows):
        entries=[r for r in rows if r['method']==method]
        grouped[method]={k:float(np.mean([r[k] for r in entries])) for k in entries[0] if k not in ('method','seed','data_rep')}
        grouped[method]['repeats']=len(entries)
    return grouped


def aggregate_control(out,stage='closed'):
    grouped={}; individual=[]
    for folder in sorted(out.glob('data[0-2]')):
        for path in sorted(folder.glob(f'*_{stage}.json')):
            method,seed=path.name.rsplit('_seed',1); seed=int(seed.split('_')[0]); rows=read(path)
            result=dict(data_rep=int(folder.name[-1]),method=method,seed=seed)
            result['tracking_rmse']=float(np.sqrt(np.mean([r['tracking_rmse']**2 for r in rows])))
            for key in ('event_tracking_energy','event_tracking_peak','u_rms','du_rms','saturation_fraction'):
                valid=[r[key] for r in rows if r[key] is not None]
                result[key]=float(np.sqrt(np.mean(np.square(valid))) if key in ('u_rms','du_rms') else np.mean(valid))
            individual.append(result)
    for method in dict.fromkeys(r['method'] for r in individual):
        entries=[r for r in individual if r['method']==method]
        grouped[method]={k:float(np.mean([r[k] for r in entries])) for k in entries[0] if k not in ('method','seed','data_rep')}
    return grouped,individual


def audit(out):
    cfg=read(out/'frozen_config.json'); provenance=read(out/'provenance.json'); root=Path(__file__).resolve().parent
    checks={name:file_hash(root/name)==value for name,value in provenance['hashes'].items()}
    if not all(checks.values()): raise AssertionError('Experiment source hashes changed')
    histories=[]; training=[]; latency=[]
    test_ids={r['id'] for r in read(out/'test_manifest.json')['trajectories']}; all_train=set(); all_val=set()
    for rep in range(3):
        folder=out/f'data{rep}'; manifest=read(folder/'data_manifest.json')
        train_ids={r['id'] for r in manifest['train']}; val_ids={r['id'] for r in manifest['validation']}
        if train_ids&val_ids or train_ids&test_ids or val_ids&test_ids or train_ids&all_train or val_ids&all_val:
            raise AssertionError('Data split identity overlap')
        all_train|=train_ids; all_val|=val_ids
        if (len(train_ids),len(val_ids),manifest['train_windows'],manifest['validation_windows'])!=(360,144,199800,79920):
            raise AssertionError('Wrong split/window counts')
        for seed in cfg['seeds']:
            record=read(folder/f'seed{seed}_training.json'); history=read(folder/f'seed{seed}_history.json')
            hashes=[record[m]['initial_hash'] for m in ('A','B','C')]
            if len(set(hashes))!=1: raise AssertionError('Unpaired initialization')
            if not all(record[m]['steps']==15000 and record[m]['parameters']==86296 for m in ('A','B','C')):
                raise AssertionError('Wrong budget/capacity')
            for method,info in record.items():
                ck=torch.load(folder/f'{method}_seed{seed}.pt',weights_only=False)
                best=min(history[method],key=lambda r:r['score'])
                if ck['step']!=best['step'] or abs(ck['validation']['score']-best['score'])>1e-12:
                    raise AssertionError('Checkpoint did not follow validation-only selection')
                training.append(dict(data_rep=rep,seed=seed,method=method,**info))
                shadow=read(folder/f'{method}_seed{seed}_shadow.json')
                expected=8 if method=='midpoint' else 1
                if shadow['latency']['forwards_per_estimate']!=expected: raise AssertionError('Call count mismatch')
                latency.append(dict(data_rep=rep,seed=seed,method=method,**shadow['latency']))
                histories.append(dict(data_rep=rep,seed=seed,method=method,selected_step=ck['step'],
                    first_score=history[method][0]['score'],last_score=history[method][-1]['score'],best_score=best['score']))
    result=dict(source_hashes=checks,training_trajectories=len(all_train),validation_trajectories=len(all_val),
        test_trajectories=len(test_ids),audited_checkpoints=len(training),split_disjoint=True,
        identical_core_initialization=True,validation_selection_verified=True,
        inference_calls_verified=True,training=training,latency=latency,validation_histories=histories)
    save_json(out/'audit.json',result); return result


def tables(out,shadow,closed,delay,statistics,audited):
    labels={'A':'A：同构残差','B':'B：单步 FM','C':'C：端点加权','A_time':'A_time：等优化耗时','direct':'普通直接回归*',
            'midpoint':'中点 FM（8 次）*','raw':'原始残差','ema':'EMA','aug_kalman':'增广 Kalman','none':'无补偿','raw_clipped':'原始残差限幅 ±3'}
    order=['A','B','C','A_time','direct','midpoint','raw','ema','aug_kalman']
    lines=['# 单步 FM 冲击优势：正式实验数值表','',
           '主实验 3 套训练数据 × 3 个配对权重种子；同一 720 条固定测试轨迹。所有数值为各模型独立计算指标后取均值，未使用网络集成。',
           '带 * 的工程参照只在数据重复 0 上训练 3 个种子；应结合下文同数据参照表比较。滤波器的三条记录对应三套验证集选参，不是三次独立学习。','',
           '## 同一观测流：估计能力','',
           '| 方法 | 冲击 RMSE | 背景 RMSE | 全时段 RMSE | 起点 RMSE | 后 0.5s RMSE |',
           '|---|---:|---:|---:|---:|---:|']
    for m in order:
        r=shadow[m]; lines.append(f'| {labels[m]} | '+ ' | '.join(f'{r[k]:.6f}' for k in ('shock_rmse','background_rmse','total_rmse','onset_rmse','post_rmse'))+' |')
    lines+=['','## 逐事件辅助指标','', '| 方法 | 相对幅值 RMSE | 峰值绝对偏差 | 峰值偏离平台时间/s | 脉冲面积绝对误差 | 延长 0.5s 面积绝对误差 |','|---|---:|---:|---:|---:|---:|']
    for m in order:
        r=shadow[m]; lines.append(f'| {labels[m]} | '+' | '.join(f'{r[k]:.6f}' for k in ('relative_rmse','peak_absolute_error','peak_time_distance_s','area_absolute_error','extended_area_absolute_error'))+' |')
    lines+=['','峰值时间偏差计算至真实矩形平台最近时刻的距离；峰值在平台内不罚，因为平台没有唯一峰值时刻。峰值搜索包含事件后 0.5 秒。','',
            '## 配对不确定性','',
            '改善为正代表 B 更好；负代表 B 更差。背景改善为负即背景恶化。冲击两项比较采用各 97.5% 区间；背景、闭环是 95% 区间。层级区间仅探索性。','',
            '| 比较 | 改善/% | 固定训练模型、配对轨迹区间 | 层级重采样区间 |','|---|---:|---|---|']
    for name,r in statistics.items():
        interval=lambda v:f'[{v[0]:.2f}, {v[1]:.2f}]'
        lines.append(f'| {name} | {r["improvement_percent"]:.2f} | {interval(r["conditional_interval"])} | {interval(r["exploratory_hierarchical_interval"])} |')
    lines+=['','## 固定权重闭环，零额外延时','',
            '| 方法 | tracking RMSE | 事件后 1s 误差能量 | 事件后 1s 峰值 | 控制 RMS | Δu RMS | 饱和比例 |',
            '|---|---:|---:|---:|---:|---:|---:|']
    for m in ['none',*order,'raw_clipped']:
        r=closed[m]; lines.append(f'| {labels[m]} | '+' | '.join(f'{r[k]:.7f}' for k in ('tracking_rmse','event_tracking_energy','event_tracking_peak','u_rms','du_rms','saturation_fraction'))+' |')
    lines+=['','## 实际调用数与 CPU 软件耗时','',
            '| 方法 | 参数量 | 训练前向/更新 | 推理前向/次 | 优化耗时/秒 | B=1 API P50/ms | 自身 P50 延时后的 tracking RMSE |',
            '|---|---:|---:|---:|---:|---:|---:|']
    for m in order[:6]:
        training=[r for r in audited['training'] if r['method']==m]; timing=[r for r in audited['latency'] if r['method']==m]
        delay_text=f'{delay[m]["tracking_rmse"]:.7f}' if m in delay else '未加测'
        lines.append(f'| {labels[m]} | {training[0]["parameters"]} | {training[0]["train_forward_calls_per_update"]} | {timing[0]["forwards_per_estimate"]:.0f} | {np.mean([r["training_seconds"] for r in training]):.2f} | {np.mean([r["p50_ms"] for r in timing]):.4f} | {delay_text} |')
    lines+=['','优化耗时仅计更新计算，三套数据并行时可能存在调度/缓存差异。软件推理耗时在所有训练结束后单线程测量，含公开 API 归一化及输入检查，不含传感器/通信/执行器。','',
            '## 同数据工程参照（仅 data0）','', '| 方法 | 冲击 RMSE | 背景 RMSE |','|---|---:|---:|']
    raw=read(out/'shadow_summary.json')
    for m in order:
        values=[r for r in raw if r['data_rep']==0 and r['method']==m]
        lines.append(f'| {labels[m]} | {np.mean([r["shock_rmse"] for r in values]):.6f} | {np.mean([r["background_rmse"] for r in values]):.6f} |')
    lines+=['','## 各独立数据重复','', '| 数据 | 方法 | 冲击 RMSE | 背景 RMSE |','|---|---|---:|---:|']
    for rep in range(3):
        for m in ('A','B','C','A_time'):
            values=[r for r in raw if r['data_rep']==rep and r['method']==m]
            lines.append(f'| {rep} | {m} | {np.mean([r["shock_rmse"] for r in values]):.6f} | {np.mean([r["background_rmse"] for r in values]):.6f} |')
    (out/'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def plots(out,shadow,closed):
    methods=['A','B','C','A_time','direct','midpoint','raw','ema','aug_kalman']
    fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained')
    for ax,key,title in zip(axs,['shock_rmse','background_rmse','tracking_rmse'],['Event-balanced shock RMSE','Background RMSE','Closed-loop tracking RMSE']):
        source=closed if key=='tracking_rmse' else shadow
        labels=[m+'*' if m in ('direct','midpoint') else m for m in methods]
        ax.bar(labels,[source[m][key] for m in methods],color=['#777','#2276c9','#df9838','#aaa','#9675b4','#30a080','#c95050','#555','#558899'])
        ax.tick_params(axis='x',rotation=55); ax.set_title(title); ax.grid(axis='y',alpha=.2)
    fig.suptitle('A/B/C/A_time: 3 datasets x 3 seeds; * direct/midpoint: dataset 0 x 3 seeds',fontsize=11)
    fig.savefig(out/'comparison.png',dpi=160); plt.close(fig)
    fig,axs=plt.subplots(3,3,figsize=(13,10),layout='constrained')
    for rep in range(3):
        for column,seed in enumerate((11,22,33)):
            ax=axs[rep,column]; history=read(out/f'data{rep}/seed{seed}_history.json')
            for method in ('A','B','C'):
                ax.plot([r['step'] for r in history[method]],[r['score'] for r in history[method]],label=method,lw=1)
            ax.set_yscale('log'); ax.set_title(f'Data {rep}, paired seed {seed}'); ax.grid(alpha=.2)
    axs[0,0].legend(); fig.supxlabel('Optimizer updates'); fig.supylabel('Validation selection score (log scale)')
    fig.savefig(out/'validation.png',dpi=150); plt.close(fig)
    specs=make_specs(230000,widths=(1,2,4,6,10),per_cell=60,smooth_count=120)
    preds={m:np.load(out/f'data0/{m}_seed11_predictions.npz')['prediction'] for m in ('A','B','C')}
    raw=np.load(out/'data0/raw_seed-1_predictions.npz')['prediction']
    fig,axs=plt.subplots(2,5,figsize=(17,7),layout='constrained')
    for row,regime in enumerate(('impulse','amplitude')):
        for col,width in enumerate((1,2,4,6,10)):
            j=next(i for i,s in enumerate(specs) if s['regime']==regime and s['width']==width)
            s=specs[j]; start=s['events'][0]['start']; sl=slice(start-10,start+36); time=s['t'][sl]-s['t'][start]
            ax=axs[row,col]; ax.plot(time,raw[j,sl],color='.75',lw=.8,label='Raw')
            ax.plot(time,s['d'][sl],color='black',lw=1.6,label='Truth')
            for m in preds: ax.plot(time,preds[m][j,sl],lw=1,label=m)
            ax.set_title(f'{regime}, {width*20} ms'); ax.grid(alpha=.2); ax.set_xlabel('Time from onset (s)')
    axs[0,0].legend(ncol=3,fontsize=8); fig.savefig(out/'events.png',dpi=150); plt.close(fig)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--out',default='results/shock_validation'); args=p.parse_args(); out=Path(args.out)
    audited=audit(out); shadow=aggregate_shadow(out); closed,closed_rows=aggregate_control(out)
    delay,delay_rows=aggregate_control(out,'delay')
    strata=[r['stratum'] for r in read(out/'data0/A_seed11_shadow.json')['trajectories']]
    stats={}
    for ref in ('A','C'):
        for key,label,alpha in [('event_mse','shock',.025),('background_mse','background',.05)]:
            stats[f'B vs {ref}: {label}']=paired_bootstrap(arrays(out,'B',key),arrays(out,ref,key),strata,alpha=alpha)
        stats[f'B vs {ref}: closed event energy']=paired_bootstrap(arrays(out,'B','event_tracking_energy','closed'),
                arrays(out,ref,'event_tracking_energy','closed'),strata,alpha=.05,root=False)
    save_json(out/'statistics.json',stats); save_json(out/'aggregate.json',dict(shadow=shadow,closed=closed,delay=delay))
    save_json(out/'closed_summary.json',closed_rows)
    # All subgroup rows stay visible; no width selected for favorable reporting.
    subgroup=[]
    for method in ('A','B','C','A_time','raw','ema','aug_kalman','direct','midpoint'):
        replicates=range(1) if method in ('direct','midpoint') else range(3)
        for rep in replicates:
            seeds=(-1,) if method in ('raw','ema','aug_kalman') else (11,22,33)
            for seed in seeds:
                rows=read(out/f'data{rep}/{method}_seed{seed}_shadow.json')['trajectories']
                for stratum in sorted({r['stratum'] for r in rows if r['event_mse'] is not None}):
                    group=[r for r in rows if r['stratum']==stratum]
                    subgroup.append(dict(data_rep=rep,seed=seed,method=method,stratum=stratum,
                        shock_rmse=float(np.sqrt(np.mean([r['event_mse'] for r in group]))),
                        onset_rmse=float(np.sqrt(np.mean([r['onset_mse'] for r in group]))),
                        background_rmse=float(np.sqrt(np.mean([r['background_mse'] for r in group])))))
    with (out/'subgroups.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(subgroup[0])); writer.writeheader(); writer.writerows(subgroup)
    tables(out,shadow,closed,delay,stats,audited); plots(out,shadow,closed)
    print(json.dumps(dict(shadow=shadow,statistics=stats,closed=closed),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
