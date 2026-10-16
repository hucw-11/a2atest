"""Run: python -m closed_loop.experiment. Original models/results are read-only."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import torch
from a2afm.data import windows,Normalizer
from a2afm.inference import DisturbanceEstimator
from experiment import train,log,save_json
from closed_loop.core import scenarios,run,measures,DT
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def tune_filters(specs):
    # Tune closed-loop tracking objective, with identical fixed controller and saturation.
    result={}; records=[]
    for method,values in [('dob',[3.,6.,12.,24.,48.,96.]),('kalman',[1e2,1e3,1e4,1e5,1e6])]:
        best=(float('inf'),None)
        for value in values:
            traces=run(specs,method,**({'bandwidth':value} if method=='dob' else {'kalman_q':value}))
            metric=[measures(t) for t in traces]
            # Physical units explicit: tracking squared error + 1e-5 * control increment squared.
            score=np.mean([r['tracking_rmse']**2+1e-5*r['du_rms']**2 for r in metric])
            records.append(dict(method=method,value=value,score=float(score)))
            if score<best[0]: best=(score,value)
        result[method]=best[1]
    return result,records

def evaluate(stage,models,specs,params,out,closed=True):
    rows=[]; examples={}
    for method in ['none','dob','kalman','regression','a2afm']:
        seeds=[11,22,33] if method in ['a2afm','regression'] else [-1]
        for seed in seeds:
            traces=run(specs,method,models.get((method,seed)),bandwidth=params['dob'],kalman_q=params['kalman'],closed=closed)
            for i,tr in enumerate(traces):
                rows.append(dict(stage=stage,method=method,seed=seed,trajectory=i,family=tr['kind'],**measures(tr)))
            if seed in [-1,11]: examples[method]=traces
            np.savez_compressed(out/f'{stage}_{method}_{seed}.npz',
                **{f'{name}_{i}':tr[name] for i,tr in enumerate(traces) for name in
                   ['t','d','estimate','x','v','u','command','error','dhat','a_measured','params']})
            log(f'闭环扩展 {stage} {method} seed={seed} 完成')
    with (out/f'{stage}_metrics.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    save_json(out/f'{stage}_metrics.json',rows)
    plot_examples(stage,examples,out,closed)
    return rows

def plot_examples(stage,examples,out,closed):
    fig,axes=plt.subplots(3,3,figsize=(15,10),layout='constrained')
    colors={'none':'0.5','dob':'tab:blue','kalman':'tab:orange','regression':'tab:green','a2afm':'tab:red'}
    for column,tid in enumerate([1,2,3]):
        tr=examples['none'][tid]; event=tr['events'][0]; start=tr['t'][event['start']]
        axes[0,column].plot(tr['t'],tr['d'],'k',label='True disturbance',lw=2)
        for method in ['none','dob','kalman','regression','a2afm']:
            q=examples[method][tid]
            if method!='none': axes[0,column].plot(q['t'],q['estimate'],label=method,lw=1,color=colors[method])
            axes[1,column].plot(q['t'],q['error'],label=method,lw=1,color=colors[method])
            axes[2,column].plot(q['t'],q['command'],label=method,lw=1,color=colors[method])
        for row in range(3):
            axes[row,column].set_xlim(start-.2,start+1.5); axes[row,column].grid(alpha=.2)
            key=['estimate','error','command'][row]; mask=(tr['t']>=start-.2)&(tr['t']<=start+1.5)
            values=np.concatenate([examples[m][tid][key][mask] for m in examples])
            if row==0: values=np.r_[values,tr['d'][mask]]
            lo,hi=values.min(),values.max(); pad=max((hi-lo)*.1,.001)
            axes[row,column].set_ylim(lo-pad,hi+pad)
        axes[0,column].set_title(f'{tr["kind"]}: width={event["width_s"]:.2f}s')
        axes[2,column].set_xlabel('Time (s)')
    for ax,label in zip(axes[:,0],['Disturbance estimate','Tracking error','Control input']): ax.set_ylabel(label)
    axes[0,0].legend(fontsize=8); axes[1,0].legend(fontsize=8)
    fig.suptitle(f'{stage} | '+('closed loop' if closed else 'open loop shock test'))
    fig.savefig(out/f'{stage}.png',dpi=150); plt.close(fig)

def report(stages,params,out):
    lines=['# 冲击扰动与闭环控制实验','',
           '原系统保持原样；副本位于 snapshots/open_loop_20261013_234542。闭环代码位于 closed_loop/。',
           '', '## 控制器与观测器','',
           '`u_nom=c*v+kappa*x+m*(r_ddot+8*(r_dot-v)+16*(r-x))`，`u=clip(u_nom-clip(d_est,-12,12),-12,12)`。',
           '参考为 `r=0.4*sin(2*pi*0.15*t)`。dt=0.02s，精确 ZOH 离散植物，控制及扰动在采样区间内保持常值。',
           '采样顺序：读取旧控制 u[k-1] 下的加速度 -> 计算扰动残差 -> 更新观测器 -> 计算新控制 u[k] -> 推进植物。不存在控制/加速度的代数循环。',
           '所有方法在第24个采样点开始补偿；此前保持相同PD控制。无额外模拟计算延迟，属于同步采样控制仿真。',
           '',f'DOB：`d_est[k]=(1-alpha)*d_est[k-1]+alpha*d_hat[k]`，`alpha=1-exp(-omega*dt)`，验证选择 omega={params["dob"]} rad/s。这是有加速度传感器的残差 Q 滤波 DOB，不对噪声位置作两次数值微分。',
           f'Kalman：增广扰动状态 `[d,d_dot]`，常速度转移；测量 d_hat；验证选择过程驱动方差 q={params["kalman"]}，R=(m*sigma_a)^2。',
           '神经网络：保留原过去→未来FM和直接回归结构，只用首项扰动估计。经典方法使用d_hat；网络也使用x/v/u/系统参数。',
           '参数只按12条验证轨迹的 `tracking_RMSE²+1e-5*Δu_RMS²` 选择，未用测试集调参。',
           '', '## 冲击定义与数据','',
           '测试包含平滑扰动及 0.02/0.08/0.20 秒矩形脉冲，每条冲击轨迹包含一正一负冲击，出现时间随机。',
           '每次冲量绝对值 J∈[0.15,0.35]，幅值为 J/width，叠加小幅正弦背景。宽度相同的试验在各方法间共享参数、参考与噪声序列。',
           '这是有限宽度脉冲；单周期脉冲也不是数学 Dirac δ。采样区间内定义为常值，所以窄脉冲不会被积分器遗漏。',
           '每个阶段24条测试轨迹（每类6条），高斯加速度噪声σ=0.5。原权重冻结迁移与闭环新权重分别报告。',
           '', '## 汇总指标','',
           '下表先按训练种子平均每条轨迹的MSE，再跨轨迹开方；不是把三个种子当成72条独立测试轨迹。none为无补偿参照，不算四种观测器之一。',
           '冲击RMSE只统计脉冲持续区间，避免短冲击被长时间背景掩盖。',
           '', '| 阶段 | 方法 | 扰动RMSE | 冲击区间RMSE | 跟踪RMSE | 控制RMS | Δu RMS |',
           '|---|---|---:|---:|---:|---:|---:|']
    summaries=[]
    for stage,rows in stages.items():
        for method in ['none','dob','kalman','regression','a2afm']:
            rr=[r for r in rows if r['method']==method]
            def rms(key):
                vals=[r[key] for r in rr if r[key] is not None]
                return float(np.sqrt(np.mean(np.square(vals))))
            summary=dict(stage=stage,method=method,**{k:rms(k) for k in ['d_rmse','shock_rmse','tracking_rmse','u_rms','du_rms']})
            summaries.append(summary)
            lines.append('| '+stage+' | '+method+' | '+' | '.join(f'{summary[k]:.5f}' for k in ['d_rmse','shock_rmse','tracking_rmse','u_rms','du_rms'])+' |')
    lines+=['','## 指标解释与适用范围','',
            '- open_frozen阶段控制不使用估计，所以跟踪/控制指标在方法间相同，只比较去噪；closed_frozen比较旧权重迁移；closed_adapted比较新闭环数据训练权重。',
            '- 原权重未见过冲击及反馈控制输入。不能把旧模型的迁移失败直接归结为FM方法本身；也不能用新模型成绩宣称旧模型无需训练即可泛化。',
            '- 新模型训练使用72条独立轨迹，含平滑和三种宽度冲击，混合无补偿PD与DOB采集；验证/测试轨迹独立。',
            '- 恢复时间从脉冲结束起计算，在2秒观察窗口内寻找位置误差连续0.5秒保持在±0.02内的起点；未恢复比例单列在CSV。未恢复不会被写成0秒。',
            '- 脉冲起点对齐采样网格，不包含异步或亚采样宽度冲击；这不是对真实Dirac冲量的测试。',
            '- CSV同时给出峰值误差、饱和比例、冲击峰值估计比和脉冲区间积分误差。峰值比包含正弦背景，不是严格的纯脉冲增益。',
            '- 控制输入和补偿统一限幅12；估计器原始输出不截断后再评分，避免隐藏不良估计。',
            '- 当前已知精确x/v和系统参数；数值试验不能证明神经网络闭环全局稳定性，也未覆盖参数失配和传感器延时。',
            '- 无补偿线性离散闭环的标称极点已检查在单位圆内；完整含非线性限幅与神经观测器系统只报告实际仿真表现。',
            '', '参考：[DOB综述](https://doi.org/10.1109/TIE.2015.2478397)；本实验采用可测加速度的残差Q滤波形式。']
    for stage in stages: lines+=['',f'## {stage} 示例',f'![{stage}]({stage}.png)']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save_json(out/'summary.json',summaries)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--steps',type=int,default=3000)
    parser.add_argument('--resume',action='store_true'); args=parser.parse_args()
    torch.set_num_threads(4); torch.use_deterministic_algorithms(True)
    out=ROOT/'results/closed_loop'; out.mkdir(parents=True,exist_ok=True)
    log('计划：先冻结原权重测试冲击，再建立并训练闭环版本，比较四种观测器及无补偿参照')
    validation=scenarios(12,72000); params,grid=tune_filters(validation)
    save_json(out/'filter_tuning.json',dict(selected=params,grid=grid))
    test=scenarios(24,73000); save_json(out/'test_manifest.json',[{k:t[k] for k in ['trajectory_id','kind','events']} for t in test])
    old={(kind,seed):DisturbanceEstimator(ROOT/f'results/main/{kind}_seed{seed}.pt')
         for kind in ['a2afm','regression'] for seed in [11,22,33]}
    stages={}
    stages['open_frozen']=evaluate('open_frozen',old,test,params,out,closed=False)
    stages['closed_frozen']=evaluate('closed_frozen',old,test,params,out)
    cfg=argparse.Namespace(out=str(out/'models'),steps=args.steps,seeds=[11,22,33],length=24,width=128,
                           batch=128,lr=.001,flow_steps=4,train_trajectories=72,test_trajectories=24,
                           threads=4,resume=args.resume,ablation=False)
    modeldir=out/'models'; modeldir.mkdir(exist_ok=True)
    train_specs=scenarios(72,71000)
    training=run(train_specs[:36],'none')+run(train_specs[36:],'dob',bandwidth=params['dob'])
    val_tr=run(validation,'none')
    td=windows(training,24,2); vd=windows(val_tr,24,2)
    norm=Normalizer(td); models={}
    save_json(out/'config.json',dict(train=vars(cfg),dt=DT,kp=16,kd=8,limit=12,sigma_a=.5,
                                    train_seed=71000,validation_seed=72000,test_seed=73000))
    for seed in [11,22,33]:
        for kind in ['a2afm','regression']:
            train(cfg,kind,seed,td,vd,norm,'cpu',modeldir)
            models[(kind,seed)]=DisturbanceEstimator(modeldir/f'{kind}_seed{seed}.pt')
    stages['closed_adapted']=evaluate('closed_adapted',models,test,params,out)
    report(stages,params,out)
    save_json(out/'status.json',dict(status='complete'))
    log(f'冲击及闭环实验完成：{out / "REPORT.md"}')

if __name__=='__main__': main()
