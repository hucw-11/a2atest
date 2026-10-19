from pathlib import Path
import csv
import hashlib
import json
import sys
import numpy as np
import torch

root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from cnn_experiment.models import METHODS,Estimator
from cnn_experiment.data import trajectory_metrics,TEST_FAMILIES

torch.set_num_threads(2)
p=root/'results/cnn-impulses-20261019'
status=json.loads((p/'status.json').read_text())
assert status['status']=='complete' and status['models']==12
test_log=(p/'tests.log').read_text()
assert 'Ran 18 tests' in test_log and test_log.rstrip().endswith('OK')
assert status['trajectory_metric_rows']==2160 and status['windows_per_condition']==39960
for name,h in json.loads((p/'source_hashes.json').read_text()).items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,name
manifest=json.loads((p/'data_manifest.json').read_text())
assert len(manifest['train'])==96 and len(manifest['validation'])==24 and len(manifest['test'])==72
assert set(t['kind'] for t in manifest['train'])=={'smooth','pulse_1','pulse_4','pulse_10'}
assert set(t['kind'] for t in manifest['test'])==set(TEST_FAMILIES)
for seed in [11,22,33]:
    checkpoints={}
    for method in METHODS:
        ck=torch.load(p/f'models/{method}_seed{seed}_last.pt',map_location='cpu',weights_only=False)
        assert ck['step']==3000
        best=torch.load(p/f'models/{method}_seed{seed}.pt',map_location='cpu',weights_only=False)
        assert best['val_mse']==min(row['val_mse'] for row in ck['history'])
        checkpoints[method]=ck
    for method in METHODS:
        assert torch.equal(checkpoints[method]['batch_rng'],checkpoints['mlp_a2afm']['batch_rng'])
    assert torch.equal(checkpoints['mlp_a2afm']['rng'],checkpoints['cnn_a2afm']['rng'])

rows=list(csv.DictReader((p/'trajectory_metrics.csv').open())); assert len(rows)==2160
checked=0;online=0;pulse_count=0
for condition in ['clean','xv_5pct']:
    with np.load(p/f'predictions_{condition}.npz') as z,np.load(p/f'observations_{condition}.npz') as obs:
        assert len(z['target'])==39960
        for j in range(72):
            mass,c,k=obs[f'params_{j}'];idx=z['index'][z['trajectory']==j]
            np.testing.assert_array_equal(idx,np.arange(23,578))
            np.testing.assert_allclose(obs[f'dhat_{j}'],mass*obs[f'a_measured_{j}']+
                c*obs[f'v_{j}']+k*obs[f'x_{j}']-obs[f'u_{j}'],atol=1e-13)
            np.testing.assert_array_equal(z['target'][z['trajectory']==j],obs[f'd_{j}'][idx].astype(np.float32))
            for ev in manifest['test'][j]['events']:
                assert ((idx>=ev['start'])&(idx<ev['end'])).sum()==ev['end']-ev['start']
                pulse_count+=1
        for row in (r for r in rows if r['condition']==condition):
            j=int(row['trajectory']);mask=z['trajectory']==j
            tr={'d':obs[f'd_{j}'],'events':manifest['test'][j]['events']}
            pred=z[f'{row["method"]}_seed{row["seed"]}'][mask]
            assert np.isfinite(pred).all()
            actual=trajectory_metrics(tr,z['index'][mask],pred)
            for key,value in actual.items():
                if value is None:assert row[key]==''
                else:np.testing.assert_allclose(value,float(row[key]),rtol=1e-12,atol=1e-12)
            checked+=1
        for method in METHODS:
            for seed in [11,22,33]:
                est=Estimator(p/f'models/{method}_seed{seed}.pt')
                for j in [1,2,5]:
                    i=manifest['test'][j]['events'][0]['start'];sl=slice(i-23,i+1)
                    pred,_=est.estimate(*[obs[f'{key}_{j}'][sl] for key in ['x','v','u','a_measured']],obs[f'params_{j}'])
                    selected=(z['trajectory']==j)&(z['index']==i)
                    np.testing.assert_allclose(pred,z[f'{method}_seed{seed}'][selected][0],rtol=0,atol=3e-5)
                    online+=1
timing=json.loads((p/'latency.json').read_text());assert len(timing)==4
for r in timing:
    assert r['calls']==1154 and r['batch_size']==1
    assert r['median_ms']<=r['p95_ms']<=r['p99_ms']<=r['max_ms']
summary=json.loads((p/'summary.json').read_text())
for r in summary:
    selected=[row for row in rows if row['condition']==r['condition'] and row['method']==r['method']
              and (r['family']=='all' or r['family']==row['family'])]
    np.testing.assert_allclose(r['rmse'],np.sqrt(np.mean([float(row['mse']) for row in selected])),rtol=1e-12)

report=dict(status='passed',unit_tests=18,trained_models=12,steps_per_model=3000,
    trajectory_metric_rows_independently_recomputed=checked,summary_rows_checked=len(summary),
    complete_pulse_events_checked=pulse_count,online_vs_batch_at_impulse_onsets=online,
    online_tolerance=3e-5,identical_minibatch_generator_states=True,
    identical_flow_time_generator_states=True,source_hashes='all_match',
    smoke_resume='all four models, both measurement conditions: identical prediction arrays',
    latency_observations_per_model=1154)
(p/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
