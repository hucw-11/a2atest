"""Frozen, matched single-step FM shock experiment. All computation is local CPU."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import torch

from a2afm.data import Normalizer
from a2afm.inference import DisturbanceEstimator
from closed_loop.core import run
from experiment import save_json
from shock_validation.data import make_specs,manifest,collect,dataset,file_hash,array_hash
from shock_validation.metrics import validation_weights,validation_score,expand,event_metrics,summarize
from shock_validation.training import train_group,predict_current
from shock_validation.filters import filter_predictions
from shock_validation.control import run_reference,control_metrics

ROOT=Path(__file__).resolve().parent
DEFAULT=dict(updates=15000,validation_every=500,batch=128,lr=.001,source_noise=.01,
             seeds=[11,22,33],data_replicates=[0,1,2],train_count=360,val_count=144,test_count=720,
             train_seed_base=210000,val_seed_base=220000,test_seed=230000,
             primary_methods=['A','B','C'],reference_methods=['direct','midpoint'],
             train_widths=[1,4,10],test_widths=[1,2,4,6,10],sigma_a=.5,
             selection='0.5*equal-stratum-event-MSE + 0.5*equal-trajectory-background-MSE',
             shock_improvement_threshold=.10,background_degradation_limit=.05,
             threads_per_worker=1,convergence_rule='fixed 15000 updates; report best-step and validation slope, no test-driven extension',
             reference_scope='direct/midpoint on data replicate 0, three weight seeds',
             time_control='A_time matches B optimizer wall time; validation and data preparation excluded',
             closed_event_window='[onset,onset+1 second)',bootstrap_replicates=5000)


def prepare(out,rep,cfg):
    folder=out/f'data{rep}'; folder.mkdir(parents=True,exist_ok=True)
    train_specs=make_specs(cfg['train_seed_base']+rep*1000)
    val_specs=make_specs(cfg['val_seed_base']+rep*1000,per_cell=20,smooth_count=24)
    tr=collect(train_specs); val=collect(val_specs); train_data=dataset(tr); val_data=dataset(val)
    norm=Normalizer(train_data); tensors=norm.tensors(train_data); validation=norm.tensors(val_data)
    weights=validation_weights(val,val_data)
    save_json(folder/'data_manifest.json',dict(train=manifest(train_specs),validation=manifest(val_specs),
        train_windows=len(train_data['source']),validation_windows=len(val_data['source']),
        training_hash=array_hash(train_data['source'],train_data['target'],train_data['condition']),
        validation_hash=array_hash(val_data['source'],val_data['target'],val_data['condition']),
        normalization={k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in norm.state.items()}))
    return folder,tensors,validation,val_data,weights,norm,val


def worker(out_string,rep,cfg):
    torch.set_num_threads(cfg['threads_per_worker']); torch.set_num_interop_threads(1)
    out=Path(out_string); folder,tensors,validation,val_data,weights,norm,val=prepare(out,rep,cfg)
    methods=cfg['primary_methods']+(cfg['reference_methods'] if rep==0 else [])
    for seed in cfg['seeds']: train_group(folder,tensors,validation,val_data,weights,norm,seed,cfg,methods)
    tuning={}
    for method,grid in [('ema',[.05,.1,.2,.35,.5,.7,.9,1.]),('aug_kalman',[.001,.01,.1,1.,10.,100.])]:
        rows=[]
        for param in grid:
            p=filter_predictions(val,method,param)[val_data['trajectory'],val_data['index']]
            rows.append(dict(param=param,**validation_score(p,val_data['target'],weights)))
        tuning[method]=dict(selected=min(rows,key=lambda r:r['score'])['param'],grid=rows)
    save_json(folder/'filter_tuning.json',tuning)
    print(f'data{rep} ALL TRAINING AND TUNING COMPLETE',flush=True)


def evaluate(out,cfg):
    torch.set_num_threads(1)
    specs=make_specs(cfg['test_seed'],widths=cfg['test_widths'],per_cell=60,smooth_count=120)
    traces=collect(specs); data=dataset(traces)
    save_json(out/'test_manifest.json',dict(trajectories=manifest(specs),windows=len(data['source']),
        observation_hash=array_hash(data['source'],data['condition']),target_hash=array_hash(data['target'])))
    summary=[]
    for rep in cfg['data_replicates']:
        folder=out/f'data{rep}'; tuning=json.loads((folder/'filter_tuning.json').read_text())
        entries=[(m,-1,tuning.get(m,{}).get('selected')) for m in ('raw','ema','aug_kalman')]
        methods=cfg['primary_methods']+['A_time']+(cfg['reference_methods'] if rep==0 else [])
        entries += [(m,seed,None) for seed in cfg['seeds'] for m in methods]
        for method,seed,param in entries:
            name=f'{method}_seed{seed}'; scores_path=folder/f'{name}_shadow.json'
            if scores_path.exists():
                summary.append(json.loads(scores_path.read_text())['summary']); continue
            start=time.perf_counter()
            if seed==-1: full=filter_predictions(traces,method,param); latency=None
            else:
                estimator=DisturbanceEstimator(folder/f'{name}.pt')
                full=expand(predict_current(estimator.model,estimator.norm.tensors(data),estimator.norm,method),data,len(traces))
                tr=traces[0]; h=slice(77,101); timings=[]; calls=[0]
                hook=estimator.model.register_forward_hook(lambda *args:calls.__setitem__(0,calls[0]+1))
                for _ in range(30): estimator.estimate(*(tr[k][h] for k in ('x','v','u','a_measured')),tr['params'])
                calls[0]=0
                for _ in range(300):
                    begin=time.perf_counter(); estimator.estimate(*(tr[k][h] for k in ('x','v','u','a_measured')),tr['params']); timings.append((time.perf_counter()-begin)*1000)
                hook.remove(); latency=dict(p50_ms=float(np.median(timings)),p95_ms=float(np.percentile(timings,95)),
                                           forwards_per_estimate=calls[0]/300)
                expected=8 if method=='midpoint' else 1
                if latency['forwards_per_estimate']!=expected: raise AssertionError('Unexpected inference call count')
                # Public B=1 API agrees with batched shadow predictions.
                current,_=estimator.estimate(*(tr[k][h] for k in ('x','v','u','a_measured')),tr['params'])
                np.testing.assert_allclose(current,full[0,100],atol=2e-5,rtol=2e-5)
            rows=[]; events=[]
            for tr,p in zip(traces,full):
                row,event=event_metrics(tr,p); rows.append(row)
                events.extend([dict(trajectory=tr['trajectory_id'],stratum=tr['stratum'],**r) for r in event])
            agg=dict(data_rep=rep,method=method,seed=seed,**summarize(rows)); summary.append(agg)
            save_json(scores_path,dict(summary=agg,latency=latency,trajectories=rows,events=events))
            # Store current-time predictions only; no duplicate input data.
            np.savez_compressed(folder/f'{name}_predictions.npz',prediction=full.astype(np.float32))
            print(f'shadow data{rep}/{name}: shock={agg["shock_rmse"]:.5f} background={agg["background_rmse"]:.5f} ({time.perf_counter()-start:.1f}s)',flush=True)
    save_json(out/'shadow_summary.json',summary)
    # All main models are tested in feedback even if shadow results are negative.
    for rep in cfg['data_replicates']:
        folder=out/f'data{rep}'; tuning=json.loads((folder/'filter_tuning.json').read_text())
        methods=cfg['primary_methods']+['A_time']+(cfg['reference_methods'] if rep==0 else [])
        entries=[(m,-1) for m in ('none','raw','raw_clipped','ema','aug_kalman')]+[(m,s) for s in cfg['seeds'] for m in methods]
        for method,seed in entries:
            path=folder/f'{method}_seed{seed}_closed.json'
            if path.exists(): continue
            if seed==-1: results=run_reference(specs,method,tuning.get(method,{}).get('selected'))
            else: results=run(specs,'a2afm',DisturbanceEstimator(folder/f'{method}_seed{seed}.pt'))
            rows=[control_metrics(tr) for tr in results]; save_json(path,rows)
            print(f'closed data{rep}/{method}/{seed}: tracking={np.sqrt(np.mean([r["tracking_rmse"]**2 for r in rows])):.6f}',flush=True)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',default='results/shock_validation')
    parser.add_argument('--workers',type=int,default=3); parser.add_argument('--stage',choices=['train','evaluate','all'],default='all')
    args=parser.parse_args(); out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    cfg=DEFAULT.copy(); config_path=out/'frozen_config.json'
    if config_path.exists():
        if json.loads(config_path.read_text())!=cfg: raise ValueError('Frozen configuration mismatch')
    else: save_json(config_path,cfg)
    source_files=['shock_validation_experiment.py',*sorted(str(p.relative_to(ROOT)) for p in (ROOT/'shock_validation').glob('*.py')),
                  'a2afm/models.py','a2afm/data.py','closed_loop/core.py','a2afm/system.py']
    provenance=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__,platform=platform.platform(),
        cpu=platform.processor(),cpu_count=os.cpu_count(),workers=args.workers,
        git_base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        hashes={f:file_hash(ROOT/f) for f in source_files})
    provenance_path=out/'provenance.json'
    if not provenance_path.exists(): save_json(provenance_path,provenance)
    elif json.loads(provenance_path.read_text())['hashes']!=provenance['hashes']:
        raise ValueError('Experiment source changed since frozen provenance; archive and explicitly audit before resuming')
    if args.stage in ('all','train'):
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures=[pool.submit(worker,str(out),rep,cfg) for rep in cfg['data_replicates']]
            for future in futures: future.result()
    if args.stage in ('all','evaluate'): evaluate(out,cfg)
    print('EXPERIMENT COMPLETE',flush=True)


if __name__=='__main__': main()
