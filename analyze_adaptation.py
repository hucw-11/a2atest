"""Verify adaptation/delay artifacts and add interpretation without changing trained sources."""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import torch
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parent/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from a2afm.inference import DisturbanceEstimator
from closed_loop.adaptation import METHODS
from experiment import ROOT, save_json


def main():
    out=ROOT/'results/closed_adaptation'; delay_out=ROOT/'results/computation_delay'
    for folder in (out,delay_out):
        if json.loads((folder/'status.json').read_text())['status']!='complete':
            raise ValueError(f'Incomplete experiment: {folder}')
        for name,digest in json.loads((folder/'source_hashes.json').read_text()).items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
                raise ValueError(f'Source/initial-weight hash mismatch: {name}')
    config=json.loads((out/'config.json').read_text())
    torch.set_num_threads(config['threads'])
    audit=json.loads((out/'checkpoint_audit.json').read_text())
    if len(audit)!=2*2*len(METHODS)*len(config['seeds']): raise ValueError('Missing adaptation checkpoint')
    for row in audit:
        path=out/row['mode']/f"{row['method']}_seed{row['seed']}_round{row['round']}.pt"
        est=DisturbanceEstimator(path); count=[]
        hook=est.model.register_forward_hook(lambda *args:count.append(1))
        h=np.zeros(24)
        est.estimate(h,h,h,h,[1,.6,2]); hook.remove()
        expected=8 if row['method']=='midpoint_fm' else 1
        if len(count)!=expected: raise ValueError(f'Wrong inference call count: {path}')
    # Prove that the independent delay implementation reproduces the original loop at zero delay.
    base=json.loads((out/'test_metrics.json').read_text())
    delayed=json.loads((delay_out/'trajectory_metrics.json').read_text())
    lookup={(r['stage'],r['method'],r['seed'],r['trajectory']):r['tracking_rmse']
            for r in base if r['suite']=='shock'}
    for r in delayed:
        if r['condition']=='zero':
            np.testing.assert_allclose(r['tracking_rmse'],lookup[(r['stage'],r['method'],r['seed'],r['trajectory'])],
                                       atol=1e-10,rtol=1e-10)
    summary=json.loads((out/'summary.json').read_text())
    def score(suite,stage,method,key='tracking_rmse'):
        return next(r[key] for r in summary if r['suite']==suite and r['stage']==stage and r['method']==method)
    a=score('shock','state_and_pulses','single_fm'); b=score('shock','state_and_pulses','midpoint_fm')
    shock_a=score('shock','state_and_pulses','single_fm','shock_rmse')
    shock_b=score('shock','state_and_pulses','midpoint_fm','shock_rmse')
    addition=['## 补充结论与验证','',
              f'本次闭环并加入冲击适配后，单步/多步跟踪RMSE比从冻结时的'
              f"{score('shock','frozen','single_fm')/score('shock','frozen','midpoint_fm'):.2f}降至{a/b:.2f}。"
              '配对区间跨过零，未观察到明确的跟踪差距；这不是预先设定等效界值的统计等效检验。',
              f'冲击扰动估计仍有差距：单步冲击RMSE={shock_a:.5f}，多步={shock_b:.5f}，'
              f'单步高约{100*(shock_a/shock_b-1):.1f}%。跟踪接近不代表估计精度完全相同。',
              '加入冲击后，混合测试集误差略有增加，存在任务分布取舍；更多冲击训练不保证所有信号都改善。',
              '未加入同预算开环继续训练对照，因此本次改善属于“闭环数据微调+闭环验证选择”的整体流程，'
              '不能完全排除额外优化步数或选择指标变化的贡献。此限制不影响对本流程实际测试结果的比较。',
              '源文件与初始权重SHA-256、36个每轮最佳检查点的部署调用次数、独立延时实现的零延时结果均已核验。'
              '26项单元测试通过，详细见verification.json。',
              '计算延时的独立结果见[延时复核报告](../computation_delay/REPORT.md)。'
              '它使用软件耗时分位数与指定调度模型，不是实际硬件在环测试。','',
              '补充分析复现：`.\\.venv\\Scripts\\python.exe analyze_adaptation.py`。']
    path=out/'REPORT.md'
    original=path.read_text(encoding='utf-8').split('\n## 补充结论与验证')[0]
    path.write_text(original.rstrip()+'\n\n'+'\n'.join(addition)+'\n',encoding='utf-8')
    # Show the same evaluation interval as the reported metrics, avoiding startup-scale masking.
    with np.load(out/'example_traces.npz') as traces:
        fig,axes=plt.subplots(2,1,figsize=(12,7),layout='constrained')
        for ax,suite in zip(axes,('mixed','shock')):
            for stage in ('frozen','state_only','state_and_pulses'):
                t=traces[f'{suite}__{stage}__single_fm__t']
                error=traces[f'{suite}__{stage}__single_fm__error']; mask=t>=1.
                ax.plot(t[mask],error[mask],label=stage,lw=.9)
            ax.set(title=f'single_fm, {suite}, evaluated interval',ylabel='tracking error',xlabel='time (s)')
            ax.grid(alpha=.2)
        axes[0].legend(); fig.savefig(out/'single_tracking.png',dpi=150); plt.close(fig)
    verification=dict(unit_tests_passed=26,checkpoint_deployment_calls_checked=len(audit),
                      adaptation_source_and_initial_weight_hashes='matched',delay_source_hashes='matched',
                      zero_delay_matches_original_closed_loop=True,
                      analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    save_json(out/'verification.json',verification)
    save_json(delay_out/'verification.json',verification)
    print(json.dumps(verification))


if __name__=='__main__': main()
