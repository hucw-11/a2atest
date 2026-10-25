import hashlib
from pathlib import Path

import numpy as np

from a2afm.data import windows
from a2afm.system import SIGNAL_FAMILIES, random_signals
from closed_loop.core import DT, run


def make_specs(seed,widths=(1,4,10),per_cell=50,smooth_count=60):
    """Independent trajectories, two amplitude regimes, random times/sign ordering."""
    strata=[('background',0)]*smooth_count
    for regime in ('impulse','amplitude'):
        for width in widths: strata.extend([(regime,width)]*per_cell)
    t=np.arange(601)*DT; specs=[]; counters={}
    for j,(regime,width) in enumerate(strata):
        rng=np.random.default_rng(np.random.SeedSequence([seed,j]))
        family=SIGNAL_FAMILIES[j%7]; _,signal=random_signals(rng,family)
        bg=np.array([signal(ti,0,0) for ti in t])
        params=np.array([rng.uniform(.8,1.2),rng.uniform(.3,1.),rng.uniform(1.,3.)])
        initial=rng.normal(0,.2,2); eps=rng.normal(0,.5,len(t)); d=bg.copy(); events=[]
        if width:
            while True:
                starts=np.sort(rng.integers(75,491,size=2))
                if starts[1]-starts[0]>=100: break
            signs=rng.permutation([1,-1])
            for start,sign in zip(starts,signs):
                amplitude=float(sign*(rng.uniform(.15,.35)/(width*DT) if regime=='impulse' else rng.uniform(.5,3.)))
                d[start:start+width]+=amplitude
                events.append(dict(start=int(start),end=int(start+width),amplitude=amplitude,
                                   area=amplitude*width*DT,width_s=width*DT))
        stratum=f'{regime}_{width}'
        ordinal=counters.get(stratum,0); counters[stratum]=ordinal+1
        specs.append(dict(t=t.copy(),d=d,background=bg,params=params,initial=initial,eps=eps,
                          dt=DT,sigma_a=.5,events=events,kind=family,regime=regime,width=width,
                          stratum=stratum,collector='none' if ordinal%2==0 else 'dob',
                          trajectory_id=f'{seed}:{j}'))
    return specs


def manifest(specs):
    return [dict(id=s['trajectory_id'],family=s['kind'],regime=s['regime'],width=s['width'],
                 collector=s['collector'],params=s['params'].tolist(),initial=s['initial'].tolist(),
                 events=s['events']) for s in specs]


def collect(specs):
    traces={}
    for policy in ('none','dob'):
        group=[s for s in specs if s['collector']==policy]
        if group:
            for tr in run(group,policy,bandwidth=24.): traces[tr['trajectory_id']]=tr
    return [traces[s['trajectory_id']] for s in specs]


def dataset(traces):
    # Vectorized construction has exactly the original windows() ordering.
    data={key:[] for key in ('source','target','condition','trajectory','index')}
    for j,tr in enumerate(traces):
        index=np.arange(23,len(tr['t'])-23)
        history=index[:,None]+np.arange(-23,1)
        data['source'].append(tr['dhat'][history])
        data['target'].append(tr['d'][index[:,None]+np.arange(24)])
        data['condition'].append(np.concatenate([tr[k][history] for k in ('x','v','u')]+[
            np.broadcast_to(tr['params'],(len(index),3))],axis=1))
        data['trajectory'].append(np.full(len(index),j)); data['index'].append(index)
    data={k:np.concatenate(v).astype(np.float32 if k in ('source','target','condition') else np.int64)
          for k,v in data.items()}
    if len(data['source'])!=555*len(traces): raise AssertionError('Stride-one window coverage changed')
    return data


def file_hash(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def array_hash(*arrays):
    h=hashlib.sha256()
    for arr in arrays:
        arr=np.ascontiguousarray(arr)
        h.update(str((arr.shape,str(arr.dtype))).encode()); h.update(arr.tobytes())
    return h.hexdigest()
