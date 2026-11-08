"""Paired learning curves for the FM auxiliary loss, on fresh physical data."""
import argparse
import copy
import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import torch

from a2afm.data import Normalizer
from a2afm.inference import DisturbanceEstimator
from a2afm.models import WindowNet
from experiment import save_checkpoint, save_json
from shock_validation.data import make_specs, collect, dataset, manifest, array_hash, file_hash
from shock_validation.metrics import validation_weights, validation_score, expand, event_metrics, summarize
from shock_validation.training import streams, sample_batch, objective, predict_current, state_hash

CONFIG = dict(budgets=[100,250,500,1000,2000,4000,8000], seeds=[11,22,33],
              replicas=[0,1,2], methods=['A','B','C','direct'], train_seed=310000,
              validation_seed=320000, test_seed=330000, batch=128, lr=.001,
              source_noise=.01, primary_early_budgets=[100,250,500,1000,2000],
              noise_budgets=[1000,8000], checkpoint_rule='exact update, no selection',
              primary='log-update averaged shock RMSE, B versus A and C; background guardrail',
              time_comparison='log-time area over common measured optimizer-time range; interpolation exploratory')


def train_replica(out_string, replica, config):
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    folder = Path(out_string) / f'data{replica}'
    folder.mkdir(parents=True, exist_ok=True)
    train_specs = make_specs(config['train_seed'] + replica*1000)
    val_specs = make_specs(config['validation_seed'] + replica*1000, per_cell=20, smooth_count=24)
    data = dataset(collect(train_specs))
    val_traces = collect(val_specs)
    val_data = dataset(val_traces)
    normalizer = Normalizer(data)
    tensors = normalizer.tensors(data)
    validation = normalizer.tensors(val_data)
    weights = validation_weights(val_traces, val_data)
    save_json(folder/'manifest.json', dict(train=manifest(train_specs), validation=manifest(val_specs),
        training_hash=array_hash(data['source'],data['target'],data['condition']),
        train_windows=len(data['source']), validation_windows=len(val_data['source'])))
    for seed in config['seeds']:
        history_path = folder/f'seed{seed}_history.json'
        if history_path.exists() and json.loads(history_path.read_text())[-1]['step']==max(config['budgets']):
            continue
        torch.manual_seed(seed)
        initial = WindowNet()
        models = {}
        optimizers = {}
        seconds = {method:0. for method in config['methods']}
        hashes = {}
        for method in config['methods']:
            if method=='direct':
                torch.manual_seed(seed)
                model = WindowNet(flow=False)
            else:
                model = copy.deepcopy(initial)
            models[method] = model
            hashes[method] = state_hash(model.state_dict())
            optimizers[method] = torch.optim.AdamW(model.parameters(),lr=config['lr'],weight_decay=1e-4)
        generators = streams(seed)
        history = []
        start = 0
        resume = folder/f'seed{seed}_resume.pt'
        if resume.exists():
            saved = torch.load(resume,weights_only=False)
            for method in models:
                models[method].load_state_dict(saved['models'][method])
                optimizers[method].load_state_dict(saved['optimizers'][method])
            for key,generator in generators.items():
                generator.set_state(saved['rng'][key])
            start,seconds,history = saved['step'],saved['seconds'],saved['history']
        for step in range(start+1,max(config['budgets'])+1):
            source,target,condition,tau,_ = sample_batch(tensors,generators,config['batch'],config['source_noise'])
            # Rotate execution order to reduce systematic first-model timing bias.
            order = config['methods'][step%4:] + config['methods'][:step%4]
            for method in order:
                model = models[method]
                model.train()
                optimizer = optimizers[method]
                begin = time.perf_counter()
                optimizer.zero_grad(set_to_none=True)
                loss,_,_ = objective(model,source,target,condition,tau,method)
                if not torch.isfinite(loss):
                    raise ValueError('Nonfinite training loss')
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                optimizer.step()
                seconds[method] += time.perf_counter()-begin
            if step in config['budgets']:
                for method,model in models.items():
                    score = validation_score(predict_current(model,validation,normalizer,method),val_data['target'],weights)
                    metadata = dict(step=step,method=method,seed=seed,replica=replica,
                                    optimizer_seconds=seconds[method],initial_hash=hashes[method],
                                    parameters=sum(p.numel() for p in model.parameters()),**score)
                    history.append(metadata)
                    save_checkpoint(folder/f'{method}_seed{seed}_step{step}.pt',dict(
                        model=model.state_dict(),normalizer=normalizer.state,
                        config=dict(length=24,width=128,flow_steps=4,predictor='single_step'),
                        kind='regression' if method=='direct' else 'a2afm',**metadata))
                save_checkpoint(resume,dict(step=step,seconds=seconds,history=history,
                    models={m:v.state_dict() for m,v in models.items()},
                    optimizers={m:v.state_dict() for m,v in optimizers.items()},
                    rng={k:g.get_state() for k,g in generators.items()}))
                save_json(history_path,history)
                print(f'data{replica} seed{seed} updates={step} complete',flush=True)


def evaluate(out, config):
    torch.set_num_threads(1)
    scenarios = [('gaussian_mid',.5),('gaussian_low',.2),('gaussian_high',.9),('student',.5)]
    for scenario,sigma in scenarios:
        specs = make_specs(config['test_seed'],widths=(1,2,4,6,10),per_cell=60,smooth_count=120)
        for index,spec in enumerate(specs):
            spec['sigma_a'] = sigma
            if scenario=='student':
                rng = np.random.default_rng(np.random.SeedSequence([340000,index]))
                spec['eps'] = rng.standard_t(3,len(spec['t']))*sigma/np.sqrt(3)
            else:
                spec['eps'] *= sigma/.5
        traces = collect(specs)
        data = dataset(traces)
        save_json(out/f'{scenario}_manifest.json',dict(trajectories=manifest(specs),
            observation_hash=array_hash(data['source'],data['condition']),target_hash=array_hash(data['target'])))
        budgets = config['budgets'] if scenario=='gaussian_mid' else config['noise_budgets']
        for replica in config['replicas']:
            folder = out/f'data{replica}'
            for seed in config['seeds']:
                for method in config['methods']:
                    for budget in budgets:
                        name = f'{method}_seed{seed}_step{budget}'
                        result_path = folder/f'{name}_{scenario}.json'
                        if result_path.exists():
                            continue
                        estimator = DisturbanceEstimator(folder/f'{name}.pt')
                        prediction = predict_current(estimator.model,estimator.norm.tensors(data),estimator.norm,method)
                        full = expand(prediction,data,len(traces))
                        rows = []
                        for trace,pred in zip(traces,full):
                            row,_ = event_metrics(trace,pred)
                            row['family'] = trace['kind']
                            rows.append(row)
                        save_json(result_path,dict(replica=replica,seed=seed,method=method,budget=budget,
                            scenario=scenario,summary=summarize(rows),trajectories=rows))
                print(f'evaluated {scenario} data{replica} seed{seed}',flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',default='results/learning_speed')
    parser.add_argument('--stage',choices=['all','train','evaluate'],default='all')
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    sources = [Path(__file__), *Path('shock_validation').glob('*.py'),
               *Path('a2afm').glob('*.py'),Path('closed_loop/core.py'),Path('experiment.py')]
    provenance = dict(config=CONFIG,hashes={str(p):file_hash(p) for p in sources},
                      torch=torch.__version__,numpy=np.__version__)
    frozen = out/'frozen.json'
    if frozen.exists():
        if json.loads(frozen.read_text())!=provenance:
            raise ValueError('Configuration or source changed')
    else:
        save_json(frozen,provenance)
    if args.stage in ('all','train'):
        with ProcessPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(train_replica,str(out),replica,CONFIG) for replica in CONFIG['replicas']]
            for future in futures:
                future.result()
    if args.stage in ('all','evaluate'):
        evaluate(out,CONFIG)
    print('COMPLETE',flush=True)


if __name__=='__main__':
    main()
