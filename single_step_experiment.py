"""CPU experiment: enlarged mixed signals, source jitter, and one-call FM.

Run with the project Python. Existing results/main checkpoints are never changed.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
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

from a2afm.baselines import estimate, tune
from a2afm.data import Normalizer, windows
from a2afm.inference import DisturbanceEstimator
from a2afm.models import predict_window
from a2afm.system import SIGNAL_FAMILIES, make_trajectories
from closed_loop.core import measures, run, scenarios
from experiment import ROOT, log, metrics, predict, save_json, train

METHODS=('single_fm','midpoint_fm','regression','residual')
SCENARIOS=(('gaussian_low',.2,'gaussian'),('gaussian_mid',.5,'gaussian'),
           ('gaussian_high',.9,'gaussian'),('student_ood',.5,'student'))


def method_config(args,method):
    cfg=argparse.Namespace(**vars(args))
    cfg.predictor='single_step' if method=='single_fm' else 'midpoint'
    cfg.flow_steps=4
    return cfg


def kind_for(method):
    return method if method in ('regression','residual') else 'a2afm'


def summarize(values):
    values=np.asarray(values,dtype=float)
    return {'mean':float(values.mean()),'std':float(values.std(ddof=1)) if len(values)>1 else 0.}


def timing(models,norm,out):
    s=torch.zeros(1,24); c=torch.zeros(1,75); result=[]
    for (method,seed),model in models.items():
        if seed!=min(seed for _,seed in models): continue
        predictor='single_step' if method=='single_fm' else 'midpoint'
        counter=[0]
        def hook(*unused): counter[0]+=1
        handle=model.register_forward_hook(hook)
        with torch.inference_mode(): predict_window(model,s,c,4,predictor)
        handle.remove()
        samples=[]
        with torch.inference_mode():
            for _ in range(30): predict_window(model,s,c,4,predictor)
            for _ in range(300):
                start=time.perf_counter_ns()
                predict_window(model,s,c,4,predictor)
                samples.append((time.perf_counter_ns()-start)/1e6)
        result.append(dict(method=method,parameters=sum(p.numel() for p in model.parameters()),
                           forward_calls=counter[0],latency_median_ms=float(np.median(samples)),
                           latency_p95_ms=float(np.percentile(samples,95))))
    save_json(out/'latency.json',result)
    return result


def evaluate_open(args,models,norm,filter_params,out):
    records=[]; trajectories=[]; example=None
    for scenario,sigma,noise in SCENARIOS:
        log(f'单步实验评估 {scenario}')
        trs=make_trajectories(args.test_trajectories,50000,sigma,noise,families=SIGNAL_FAMILIES)
        data=windows(trs,args.length,2); tensors=norm.tensors(data,'cpu')
        predictions={}
        for method in ('raw','ema','local_poly','kalman','physics_backward'):
            seq=[estimate(tr,method,filter_params.get(method)) for tr in trs]
            predictions[(method,-1)]=np.array([seq[j][i] for j,i in zip(data['trajectory'],data['index'])])
        for (method,seed),model in models.items():
            pred=norm.invert(predict(model,tensors,4,predictor='single_step' if method=='single_fm' else 'midpoint'))
            predictions[(method,seed)]=pred[:,0]
            records.append(dict(scenario=scenario,family='all_horizon',method=method,seed=seed,
                                **metrics(data['target'],pred)))
        target=data['target'][:,0]
        for (method,seed),pred in predictions.items():
            for family in ('all',*SIGNAL_FAMILIES):
                mask=np.ones(len(target),bool) if family=='all' else np.array([trs[j]['kind']==family for j in data['trajectory']])
                if mask.any():
                    records.append(dict(scenario=scenario,family=family,method=method,seed=seed,
                                        **metrics(target[mask],pred[mask])))
            for tid,tr in enumerate(trs):
                mask=data['trajectory']==tid
                trajectories.append(dict(scenario=scenario,trajectory=tid,family=tr['kind'],
                                         method=method,seed=seed,**metrics(target[mask],pred[mask])))
        if scenario=='gaussian_mid': example=(trs,data,predictions)
        # All current-d predictions retained for paired trajectory-level analysis.
        np.savez_compressed(out/f'predictions_{scenario}.npz',target=target,
                            trajectory=data['trajectory'],index=data['index'],
                            **{f'{m}_seed{s}':p for (m,s),p in predictions.items()})
    save_json(out/'metrics.json',records); save_json(out/'trajectory_metrics.json',trajectories)
    trs,data,preds=example
    fig,axes=plt.subplots(3,1,figsize=(12,9),layout='constrained')
    for ax,family in zip(axes,('multisine+chirp','multisine+steps','multisine+chirp+steps')):
        tid=next(i for i,tr in enumerate(trs) if tr['kind']==family)
        mask=data['trajectory']==tid; ts=trs[tid]['t'][data['index'][mask]]
        ax.plot(ts,data['target'][mask,0],color='black',label='truth')
        for method in METHODS:
            ax.plot(ts,preds[(method,args.seeds[0])][mask],lw=.8,label=method)
        ax.set(title=family,xlim=(2,10),ylabel='disturbance'); ax.grid(alpha=.2)
    axes[0].legend(ncol=5); axes[-1].set_xlabel('time (s)')
    fig.savefig(out/'mixed_predictions.png',dpi=150); plt.close(fig)
    return records


def evaluate_closed(args,out):
    # Stress test only: weights frozen, no closed-loop or pulse-specific fine-tuning.
    validation=scenarios(12,82000); specs=scenarios(24,83000)
    from closed_loop.experiment import tune_filters
    params,grid=tune_filters(validation)
    save_json(out/'closed_filter_tuning.json',dict(selected=params,grid=grid))
    rows=[]
    methods=('none','dob','kalman',*METHODS)
    for method in methods:
        for seed in args.seeds if method in METHODS else [-1]:
            estimator=None
            if method in METHODS:
                estimator=DisturbanceEstimator(out/method/f'{kind_for(method)}_seed{seed}.pt')
            traces=run(specs,'a2afm' if method in METHODS else method,estimator,
                       bandwidth=params['dob'],kalman_q=params['kalman'])
            for tid,tr in enumerate(traces):
                rows.append(dict(method=method,seed=seed,trajectory=tid,family=tr['kind'],**measures(tr)))
        log(f'冻结权重闭环冲击测试完成 {method}')
    save_json(out/'closed_metrics.json',rows)
    return rows


def report(args,records,closed,times,training_stats,split_stats,out):
    def cell(method,scenario,family='all'):
        r=summarize([r['rmse'] for r in records if r['method']==method and r['scenario']==scenario and r['family']==family])
        return f"{r['mean']:.5f} ± {r['std']:.5f}" if method in METHODS else f"{r['mean']:.5f}"
    lines=['# 单次调用 FM、微小源噪声与五倍混合轨迹实验报告','',
           f"生成时间：{datetime.now(timezone(timedelta(hours=8))).isoformat()}",'',
           '## 实现与损失','',
           '单步预测：`prediction = source + v_theta(source, condition, source, tau=0)`。'
           '网络输出仍是速度，积分跨度为1；不把tau=1当成已知终点。训练结果分支与部署调用同一实现。',
           '速度监督保持原方案：每个batch样本独立随机抽tau，'
           '`z=(1-tau)*s_aug+tau*y`，目标速度`y-s_aug`。',
           '每个训练batch在归一化source上重新加入独立零均值高斯白噪声；'
           'FM插值、目标速度与结果分支共同使用同一份扰动后的source。'
           'x/v/u、标签和归一化统计不加这项噪声，验证、测试和部署也不加。',
           f"白噪声标准差为归一化单位 {args.source_noise_std}，对应物理扰动单位 {training_stats['source_jitter_physical_std']:.6f}。",
           '结果损失：`mean((prediction-y)^2) + 4*mean((prediction[:,0]-y[:,0])^2)`；'
           'FM总损失为速度损失加结果损失，权重均为1。',
           '条件为过去至当前24点x、v、u和3个已知参数；source为过去24点扰动残差；'
           '目标为当前至未来24点真实扰动。仅第一项用于当前扰动估计，未来项为辅助监督。','',
           '## 数据与训练配置','',
           f"训练轨迹 {args.train_trajectories} 条（原72条的 {args.train_trajectories/72:.1f} 倍），"
           f"验证 {args.validation_trajectories} 条，每个测试噪声场景 {args.test_trajectories} 条。",
           '轨迹包含多正弦、chirp、阶跃加小正弦，以及三种两两叠加和三者同时叠加。'
           '混合分量权重从[0.5,1]随机抽取后按L2范数归一化；混合分量在同一轨迹中同时存在。',
           f"每条16秒，dt=0.02秒。训练窗口 {split_stats['train_windows']}，验证窗口 {split_stats['validation_windows']}。",
           f"训练family计数：`{json.dumps(split_stats['train_families'],ensure_ascii=False)}`。",
           '训练/验证/测试按整条轨迹隔离，随机种子分别为10000/20000/50000；'
           '各测试噪声场景共享相同底层轨迹和系统参数。归一化只拟合训练集。',
           f"CPU训练，线程 {args.threads}，随机种子 {args.seeds}；每模型 {args.steps} 次更新，"
           f"batch={args.batch}，宽度={args.width}，AdamW学习率={args.lr}，weight_decay=1e-4，梯度裁剪5。",
           '默认15000次更新是原3000次的5倍，以维持训练数据扩大5倍后的大致采样覆盖率。'
           '每100次更新验证，按当前扰动验证RMSE选择最佳检查点；报告使用最佳检查点。',
           '四个模型共享数据、噪声增强尺度、更新次数和验证选择规则；'
           '不同模型的随机数消耗不同，因此不声称每步抽到完全相同的样本或白噪声。','',
           '## 模型容量、调用次数与耗时','',
           '| 方法 | 参数量 | 单次预测网络调用 | batch=1中位耗时(ms) | P95(ms) | 训练秒数 |',
           '|---|---:|---:|---:|---:|---:|']
    for row in times:
        dur=summarize([r['seconds'] for r in training_stats['runs'] if r['method']==row['method']])
        lines.append(f"| {row['method']} | {row['parameters']} | {row['forward_calls']} | {row['latency_median_ms']:.4f} | {row['latency_p95_ms']:.4f} | {dur['mean']:.1f} ± {dur['std']:.1f} |")
    lines+=['','single_fm与midpoint_fm采用同一网络结构，后者中点积分4步；'
            'regression直接输出目标，residual输出source加修正量。'
            '延迟取第一个训练种子的模型，预热30次、逐次测量300次，包含张量预测路径，'
            '不含传感器采集、NumPy归一化和控制器。调用次数由forward hook实测。'
            '参数量相近，但多步FM的训练及推理计算量明显更大，不属于等算力比较。','',
            '## 当前扰动测试RMSE','',
            '| 方法 | Gaussian 0.2 | Gaussian 0.5 | Gaussian 0.9 | Student-t(3) 0.5 |',
            '|---|---:|---:|---:|---:|']
    for method in (*METHODS,'raw','ema','local_poly','kalman','physics_backward'):
        lines.append('| '+method+' | '+' | '.join(cell(method,s) for s,_,_ in SCENARIOS)+' |')
    lines+=['','±为共享数据下不同训练种子的样本标准差，不是置信区间或独立数据集重复。'
            '滤波参数只用验证集选择。Student-t噪声未参与训练；混合信号族在训练中出现，不属于信号族OOD。','',
            '## 中等高斯噪声下各信号族RMSE','',
            '| 信号族 | single_fm | midpoint_fm | regression | residual |',
            '|---|---:|---:|---:|---:|']
    for family in SIGNAL_FAMILIES:
        if any(r['family']==family for r in records):
            lines.append('| '+family+' | '+' | '.join(cell(m,'gaussian_mid',family) for m in METHODS)+' |')
    lines+=['','## 冻结权重的闭环冲击压力测试','',
            '所有网络沿用上述开环混合数据训练的权重，未做闭环适配或脉冲微调。'
            '24条独立12秒轨迹，含平滑扰动和宽0.02/0.08/0.20秒矩形冲击。'
            '沿用原控制器及饱和限制；各方法相同历史热身，仿真未加入实测计算延迟。'
            '这是控制分布变化和短脉冲的压力测试，不能与旧closed_adapted实验直接归因比较。',
            '| 方法 | 扰动RMSE | 冲击RMSE | 跟踪RMSE | 饱和比例 |',
            '|---|---:|---:|---:|---:|']
    for method in ('none','dob','kalman',*METHODS):
        rows=[r for r in closed if r['method']==method]
        def pooled(key):
            vals=[r[key] for r in rows if r[key] is not None]
            return float(np.sqrt(np.mean(np.square(vals)))) if vals else float('nan')
        lines.append(f"| {method} | {pooled('d_rmse'):.5f} | {pooled('shock_rmse'):.5f} | {pooled('tracking_rmse'):.5f} | {np.mean([r['saturation_fraction'] for r in rows]):.4f} |")
    lines+=['','RMSE按种子及等长轨迹的MSE平均后开方；冲击RMSE仅统计有冲击轨迹。','',
            '## 结果解释与限制','']
    means={m:np.mean([r['rmse'] for r in records if r['method']==m and r['family']=='all' and r['scenario']=='gaussian_mid']) for m in METHODS}
    best=min(means,key=means.get)
    lines.append(f"本次中等高斯噪声下最佳神经网络为 **{best}**（RMSE={means[best]:.5f}）。"
                 f"single_fm相对midpoint_fm的RMSE变化为 {(means['single_fm']/means['midpoint_fm']-1)*100:+.2f}%，"
                 f"相对residual为 {(means['single_fm']/means['residual']-1)*100:+.2f}%。正值表示误差增大。")
    latency={r['method']:r['latency_median_ms'] for r in times}
    lines.append(f"实测预测路径中位耗时，single_fm相对midpoint_fm加速 {latency['midpoint_fm']/latency['single_fm']:.2f} 倍。"
                 '是否采用单步方案，应同时考虑表中各噪声条件、信号族和闭环指标，不能仅凭调用次数判断精度。')
    lines+=['','单步预测在使用时等价于条件残差回归；保留的FM损失是辅助约束，'
            '它是否带来收益由与residual的实际结果判断，不宣称自动继承生成分布或不确定性建模能力。',
            '相较旧main，同时改变了训练数据规模、信号族、训练更新数、源噪声和预测方式；'
            '本报告不能把与旧结果的差异单独归因于某一项。未做无源噪声消融，无法独立判断1%白噪声是否改善泛化。',
            '准确x/v和已知模型参数的假设有利于physics_backward；真实传感器、模型失配、'
            '闭环计算延迟和硬件部署尚未验证。各方法虽共享信息，但历史长度和计算预算不同。','',
            '## 复现与文件','',
            '```powershell',
            '.\\.venv\\Scripts\\python.exe -m unittest test_core test_single_step closed_loop.test_core -v',
            '.\\.venv\\Scripts\\python.exe single_step_experiment.py',
            '# 中断后使用相同参数并加 --resume；仅重新生成报告用 --evaluate-only',
            '```','',
            '实际配置见config.json，环境见environment.json，源文件哈希见source_hashes.json；'
            'split_manifest.json记录独立轨迹ID、families和窗口数。'
            '每个方法目录包含最佳/末次权重及训练历史；metrics.json、trajectory_metrics.json、'
            'closed_metrics.json与predictions_*.npz保留完整分析数据。','',
            '![训练曲线](training.png)','', '![混合轨迹预测](mixed_predictions.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='results/single_step_mixed')
    p.add_argument('--steps',type=int,default=15000)
    p.add_argument('--seeds',type=int,nargs='+',default=[11,22,33])
    p.add_argument('--train-trajectories',type=int,default=360)
    p.add_argument('--validation-trajectories',type=int,default=90)
    p.add_argument('--test-trajectories',type=int,default=56)
    p.add_argument('--length',type=int,default=24)
    p.add_argument('--width',type=int,default=128)
    p.add_argument('--batch',type=int,default=128)
    p.add_argument('--lr',type=float,default=.001)
    p.add_argument('--source-noise-std',type=float,default=.01)
    p.add_argument('--threads',type=int,default=4)
    p.add_argument('--resume',action='store_true')
    p.add_argument('--evaluate-only',action='store_true')
    args=p.parse_args()
    if args.source_noise_std<0 or min(args.train_trajectories,args.validation_trajectories,args.test_trajectories)<7:
        p.error('noise std must be nonnegative and each split needs at least seven trajectories')
    if args.length!=24: p.error('closed-loop benchmark currently requires length=24')
    torch.set_num_threads(args.threads); torch.use_deterministic_algorithms(True)
    out=ROOT/args.out; out.mkdir(parents=True,exist_ok=True)
    config=vars(args)
    if (out/'config.json').exists():
        previous=json.loads((out/'config.json').read_text(encoding='utf-8'))
        ignored={'resume','evaluate_only','out'}
        if any(previous.get(k)!=v for k,v in config.items() if k not in ignored):
            raise ValueError('Output directory already contains a different experiment configuration')
        if not (args.resume or args.evaluate_only):
            raise ValueError('Output exists; use --resume, --evaluate-only, or a new --out')
    else: save_json(out/'config.json',config)
    files=[ROOT/'single_step_experiment.py',ROOT/'experiment.py',ROOT/'closed_loop/core.py',*sorted((ROOT/'a2afm').glob('*.py'))]
    hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    if args.resume or args.evaluate_only:
        if (out/'source_hashes.json').exists() and json.loads((out/'source_hashes.json').read_text())!=hashes:
            raise ValueError('Experiment sources changed since this run; use a new output directory')
    else: save_json(out/'source_hashes.json',hashes)
    save_json(out/'environment.json',dict(torch=torch.__version__,numpy=np.__version__,device='cpu',
                                        platform=platform.platform(),processor=platform.processor(),
                                        cpu_count=os.cpu_count(),torch_threads=args.threads))
    save_json(out/'status.json',dict(status='preparing'))
    log(f'单步混合实验开始：CPU，训练轨迹={args.train_trajectories}，每模型更新={args.steps}')
    tr=make_trajectories(args.train_trajectories,10000,families=SIGNAL_FAMILIES)
    val=make_trajectories(args.validation_trajectories,20000,families=SIGNAL_FAMILIES)
    td=windows(tr,args.length,2); vd=windows(val,args.length,4); norm=Normalizer(td)
    split_stats=dict(train_windows=len(td['source']),validation_windows=len(vd['source']),
                     train_families=dict(Counter(t['kind'] for t in tr)),
                     validation_families=dict(Counter(t['kind'] for t in val)),
                     train=[dict(id=t['trajectory_id'],family=t['kind']) for t in tr],
                     validation=[dict(id=t['trajectory_id'],family=t['kind']) for t in val],
                     test=[dict(id=f'50000:{i}',family=SIGNAL_FAMILIES[i%7]) for i in range(args.test_trajectories)])
    save_json(out/'split_manifest.json',split_stats)
    params=tune(val,vd); save_json(out/'filter_params.json',params)
    log(f"混合数据完成：训练窗口={len(td['source'])}，验证窗口={len(vd['source'])}")
    stats_path=out/'training_stats.json'
    stats=json.loads(stats_path.read_text()) if stats_path.exists() else dict(runs=[])
    stats['source_jitter_physical_std']=args.source_noise_std*norm.state['d_std']
    models={}; histories={}
    for method in METHODS:
        cfg=method_config(args,method); folder=out/method; folder.mkdir(exist_ok=True)
        for seed in args.seeds:
            kind=kind_for(method); last=folder/f'{kind}_seed{seed}_last.pt'
            complete=last.exists() and torch.load(last,map_location='cpu',weights_only=False)['step']==args.steps
            if args.evaluate_only or (args.resume and complete):
                est=DisturbanceEstimator(folder/f'{kind}_seed{seed}.pt'); model=est.model
                history=json.loads((folder/f'{kind}_seed{seed}_history.json').read_text())
            else:
                save_json(out/'status.json',dict(status='training',method=method,seed=seed))
                start=time.perf_counter()
                model,history=train(cfg,kind,seed,td,vd,norm,'cpu',folder)
                elapsed=time.perf_counter()-start
                prior=next((r for r in stats['runs'] if r['method']==method and r['seed']==seed),None)
                if prior: prior['seconds']+=elapsed
                else: stats['runs'].append(dict(method=method,seed=seed,seconds=elapsed))
                save_json(stats_path,stats)
            models[(method,seed)]=model; histories[(method,seed)]=history
    fig,ax=plt.subplots(figsize=(12,5),layout='constrained')
    for (method,seed),h in histories.items():
        ax.plot([r['step'] for r in h],[r['val_rmse'] for r in h],label=f'{method}/{seed}',alpha=.7)
    ax.set(xlabel='update',ylabel='validation current-d RMSE'); ax.grid(alpha=.2); ax.legend(ncol=4,fontsize=8)
    fig.savefig(out/'training.png',dpi=150); plt.close(fig)
    save_json(out/'status.json',dict(status='evaluating'))
    records=evaluate_open(args,models,norm,params,out)
    closed=evaluate_closed(args,out); times=timing(models,norm,out)
    report(args,records,closed,times,stats,split_stats,out)
    save_json(out/'status.json',dict(status='complete',finished=datetime.now(timezone.utc).isoformat()))
    log(f'单步混合实验完成：{out / "REPORT.md"}')


if __name__=='__main__': main()
