"""Audit saved runs and add paired trajectory bootstrap comparisons to the report."""
import argparse
import hashlib
import json

import numpy as np
import torch

from a2afm.inference import DisturbanceEstimator
from a2afm.system import make_trajectories
from experiment import ROOT, save_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default='results/single_step_mixed')
    args=parser.parse_args(); out=ROOT/args.out
    config=json.loads((out/'config.json').read_text(encoding='utf-8'))
    status=json.loads((out/'status.json').read_text(encoding='utf-8'))
    if status['status']!='complete': raise ValueError('Training and evaluation are not complete')
    hashes=json.loads((out/'source_hashes.json').read_text(encoding='utf-8'))
    for name,expected in hashes.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Experiment source changed: {name}')
    torch.set_num_threads(config['threads'])
    audit=[]
    for method in ('single_fm','midpoint_fm','regression','residual'):
        kind=method if method in ('regression','residual') else 'a2afm'
        for seed in config['seeds']:
            path=out/method/f'{kind}_seed{seed}.pt'
            ck=torch.load(path,map_location='cpu',weights_only=False)
            last=torch.load(out/method/f'{kind}_seed{seed}_last.pt',map_location='cpu',weights_only=False)
            if last['step']!=config['steps']: raise ValueError(f'Incomplete checkpoint: {path}')
            history=last['history']
            if history[-1]['step']!=config['steps'] or len({r['step'] for r in history})!=len(history):
                raise ValueError(f'Incomplete or duplicate validation history: {path}')
            if ck['val_rmse']!=min(r['val_rmse'] for r in history):
                raise ValueError(f'Checkpoint was not selected by best validation RMSE: {path}')
            est=DisturbanceEstimator(path)
            calls=[]
            hook=est.model.register_forward_hook(lambda *unused: calls.append(1))
            zeros=np.zeros(config['length'])
            first=est.estimate(zeros,zeros,zeros,zeros,[1,.6,2])[1]
            expected=8 if method=='midpoint_fm' else 1
            if len(calls)!=expected: raise ValueError(f'Wrong deployed forward count: {path}')
            second=est.estimate(zeros,zeros,zeros,zeros,[1,.6,2])[1]
            hook.remove()
            np.testing.assert_array_equal(first,second)
            audit.append(dict(method=method,seed=seed,best_step=ck['step'],
                              validation_rmse=ck['val_rmse'],last_step=last['step'],
                              deployed_calls=expected,noise_free_deployment=True))
    save_json(out/'checkpoint_audit.json',audit)

    rows=json.loads((out/'trajectory_metrics.json').read_text(encoding='utf-8'))
    rng=np.random.default_rng(20261021); comparisons=[]
    for scenario in ('gaussian_low','gaussian_mid','gaussian_high','student_ood'):
        tids=sorted({r['trajectory'] for r in rows if r['scenario']==scenario})
        mse={}
        for method in ('single_fm','midpoint_fm','regression','residual'):
            mse[method]=np.array([np.mean([r['rmse']**2 for r in rows if r['scenario']==scenario
                                          and r['method']==method and r['trajectory']==tid]) for tid in tids])
        indices=rng.integers(len(tids),size=(5000,len(tids)))
        for reference in ('midpoint_fm','regression','residual'):
            delta=np.sqrt(mse['single_fm'][indices].mean(1))-np.sqrt(mse[reference][indices].mean(1))
            comparisons.append(dict(scenario=scenario,reference=reference,
                                     pooled_single_rmse=float(np.sqrt(mse['single_fm'].mean())),
                                     pooled_reference_rmse=float(np.sqrt(mse[reference].mean())),
                                     delta_rmse=float(np.sqrt(mse['single_fm'].mean())-np.sqrt(mse[reference].mean())),
                                     ci95_low=float(np.percentile(delta,2.5)),
                                     ci95_high=float(np.percentile(delta,97.5)),trajectories=len(tids)))
    save_json(out/'paired_bootstrap.json',dict(repetitions=5000,seed=20261021,unit='trajectory',comparisons=comparisons))

    # Exercise the public estimator API with actual rolling x/v/u/a histories.
    tr=make_trajectories(1,91000,sigma=.5,families=('multisine+chirp+steps',))[0]
    est=DisturbanceEstimator(out/'single_fm'/f"a2afm_seed{config['seeds'][0]}.pt")
    predicted=np.full(len(tr['t']),np.nan); calls=[]
    hook=est.model.register_forward_hook(lambda *unused: calls.append(1))
    for i in range(est.length-1,len(predicted)):
        h=slice(i-est.length+1,i+1)
        predicted[i],_=est.estimate(tr['x'][h],tr['v'][h],tr['u'][h],tr['a_measured'][h],tr['params'])
    hook.remove(); valid=np.isfinite(predicted)
    if len(calls)!=int(valid.sum()): raise ValueError('Online estimator performed more than one call per estimate')
    online=dict(trajectory_id=tr['trajectory_id'],family=tr['kind'],windows=int(valid.sum()),
                forward_calls=len(calls),rmse=float(np.sqrt(np.mean((predicted[valid]-tr['d'][valid])**2))))
    save_json(out/'online_api_check.json',online)
    np.savez_compressed(out/'online_api_check.npz',t=tr['t'],truth=tr['d'],estimate=predicted)

    appendix=['## 检查点审计与配对分析','',
              f'全部{len(audit)}个检查点核对实际完成的更新数、部署调用次数和重复输入的确定性；'
              '并核对训练代码的SHA-256与实验记录一致。详情见checkpoint_audit.json。','',
              '| 方法 | 种子 | 最佳更新 | 验证RMSE | 部署调用次数 |',
              '|---|---:|---:|---:|---:|']
    for row in audit:
        appendix.append(f"| {row['method']} | {row['seed']} | {row['best_step']} | {row['validation_rmse']:.5f} | {row['deployed_calls']} |")
    all_metrics=json.loads((out/'metrics.json').read_text(encoding='utf-8'))
    appendix+=['','整段24点辅助预测RMSE（含当前及未来，不等同于当前扰动估计误差）：','',
               '| 方法 | Gaussian 0.2 | Gaussian 0.5 | Gaussian 0.9 | Student-t 0.5 |',
               '|---|---:|---:|---:|---:|']
    for method in ('single_fm','midpoint_fm','regression','residual'):
        cells=[]
        for scenario in ('gaussian_low','gaussian_mid','gaussian_high','student_ood'):
            values=[r['rmse'] for r in all_metrics if r['method']==method and r['scenario']==scenario and r['family']=='all_horizon']
            cells.append(f"{np.mean(values):.5f}")
        appendix.append('| '+method+' | '+' | '.join(cells)+' |')
    appendix+=['','以下先对同一轨迹的不同种子MSE求平均，再对轨迹平均后开方。'
               '使用相同轨迹索引配对bootstrap，整条轨迹为重采样单位，5000次。'
               '差值=single_fm RMSE减去对照RMSE，负值有利于single_fm。'
               '区间仅描述固定训练集及这组模型下测试轨迹抽样的不确定性，不包含训练集变动，'
               '也未做多重比较校正。','',
               '| 场景 | 对照 | RMSE差值 | 配对bootstrap 95%区间 |',
               '|---|---|---:|---:|']
    for row in comparisons:
        appendix.append(f"| {row['scenario']} | {row['reference']} | {row['delta_rmse']:+.5f} | [{row['ci95_low']:+.5f}, {row['ci95_high']:+.5f}] |")
    appendix+=['',f"独立三分量混合轨迹 {online['trajectory_id']} 通过公开DisturbanceEstimator API逐点运行："
               f"{online['windows']}次估计共调用网络{online['forward_calls']}次，当前扰动RMSE={online['rmse']:.5f}。"
               '这验证了真实历史输入的部署路径，但单条轨迹不作为整体泛化结论。','',
               '补充分析复现：`.\\.venv\\Scripts\\python.exe analyze_single_step.py`。']
    path=out/'REPORT.md'
    original=path.read_text(encoding='utf-8').split('\n## 检查点审计与配对分析')[0]
    if '闭环结论补充：' not in original:
        closed=json.loads((out/'closed_metrics.json').read_text(encoding='utf-8'))
        def tracking(method):
            return float(np.sqrt(np.mean([r['tracking_rmse']**2 for r in closed if r['method']==method])))
        extra=(f"闭环结论补充：单步FM的跟踪RMSE为{tracking('single_fm'):.5f}，"
               f"多步FM为{tracking('midpoint_fm'):.5f}，前者约为后者的"
               f"{tracking('single_fm')/tracking('midpoint_fm'):.2f}倍。"
               '因此，本次单步模型的开环精度接近，并不代表闭环冲击表现也接近。'
               '这些权重没有经过闭环或脉冲适配，结果不足以支持直接替换现有闭环模型。\n\n'
               '对照结论补充：直接回归在四档噪声下的当前扰动RMSE均值均低于单步FM，'
               '预测路径耗时也更低；本次配置没有显示单步FM优于直接回归的优势。'
               '这不排除其他训练配置的可能性，但不能将本次单次调用的速度收益表述为对回归网络的优势。\n')
        original=original.replace('\n## 复现与文件','\n'+extra+'\n## 复现与文件')
    notes=out/'execution_notes.json'
    if notes.exists():
        if '| 已记录训练秒数† |' not in original:
            original=original.replace('| 训练秒数 |','| 已记录训练秒数† |')
            original=original.replace('single_fm与midpoint_fm采用同一网络结构，',
                                      '†single_fm种子33和residual种子22经历保存中断，表中这两种方法的训练耗时'
                                      '未包含中断前的部分，属于下界；不用于训练加速比结论。详情见文末执行记录。\n\n'
                                      'single_fm与midpoint_fm采用同一网络结构，')
        appendix+=['','执行记录：'+json.loads(notes.read_text(encoding='utf-8'))['note']]
    path.write_text(original.rstrip()+'\n\n'+'\n'.join(appendix)+'\n',encoding='utf-8')
    print(json.dumps(dict(checkpoints=len(audit),online_api_check=online),ensure_ascii=False))


if __name__=='__main__': main()
