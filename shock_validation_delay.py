"""Post-training measured-latency supplement; does not select or alter weights."""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from a2afm.inference import DisturbanceEstimator
from closed_loop.delayed import run_delayed, delayed_measures
from experiment import save_json
from shock_validation.control import control_metrics
from shock_validation.data import make_specs


def main():
    p=argparse.ArgumentParser(); p.add_argument('--out',default='results/shock_validation'); args=p.parse_args()
    out=Path(args.out); cfg=json.loads((out/'frozen_config.json').read_text()); torch.set_num_threads(1)
    specs=make_specs(cfg['test_seed'],widths=cfg['test_widths'],per_cell=60,smooth_count=120)
    summary=[]
    for rep in cfg['data_replicates']:
        folder=out/f'data{rep}'
        for seed in cfg['seeds']:
            for method in cfg['primary_methods']:
                path=folder/f'{method}_seed{seed}_delay.json'
                shadow=json.loads((folder/f'{method}_seed{seed}_shadow.json').read_text())
                latency=shadow['latency']['p50_ms']/1000
                if path.exists(): rows=json.loads(path.read_text())
                else:
                    estimator=DisturbanceEstimator(folder/f'{method}_seed{seed}.pt')
                    traces=run_delayed(specs,'a2afm',estimator,delay_s=latency)
                    rows=[]
                    for tr in traces:
                        row=control_metrics(tr); measured=delayed_measures(tr)
                        for key in ('u_rms','u_peak','saturation_fraction','skipped_fraction'): row[key]=measured[key]
                        rows.append(row)
                    save_json(path,rows)
                summary.append(dict(data_rep=rep,seed=seed,method=method,delay_ms=latency*1000,
                    tracking_rmse=float(np.sqrt(np.mean([r['tracking_rmse']**2 for r in rows])))))
                print(f'delayed data{rep}/{method}/{seed}: {summary[-1]["tracking_rmse"]:.6f}',flush=True)
    save_json(out/'delay_summary.json',summary)


if __name__=='__main__': main()
