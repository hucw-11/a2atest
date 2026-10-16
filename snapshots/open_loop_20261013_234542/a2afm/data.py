import numpy as np
import torch


def windows(trajectories, length=24, stride=2):
    sources=[]; targets=[]; conditions=[]; ids=[]; times=[]
    for tid,tr in enumerate(trajectories):
        for t in range(length-1,len(tr['t'])-length+1,stride):
            h=slice(t-length+1,t+1)
            sources.append(tr['dhat'][h])
            targets.append(tr['d'][t:t+length])
            # Raw measured history and known equation coefficients; no future conditions.
            conditions.append(np.r_[tr['x'][h],tr['v'][h],tr['u'][h],tr['params']])
            ids.append(tid); times.append(t)
    return {'source':np.asarray(sources,dtype=np.float32),
            'target':np.asarray(targets,dtype=np.float32),
            'condition':np.asarray(conditions,dtype=np.float32),
            'trajectory':np.array(ids),'index':np.array(times)}


class Normalizer:
    def __init__(self, data=None, state=None):
        if state is None:
            self.state={'d_mean':float(data['target'].mean()),
                        'd_std':float(max(data['target'].std(),1e-6)),
                        'c_mean':data['condition'].mean(0),
                        'c_std':np.maximum(data['condition'].std(0),1e-5)}
        else:
            self.state=state

    def tensors(self,data,device='cpu'):
        s=self.state
        return tuple(torch.as_tensor(a,dtype=torch.float32,device=device) for a in (
            (data['source']-s['d_mean'])/s['d_std'],
            (data['target']-s['d_mean'])/s['d_std'],
            (data['condition']-s['c_mean'])/s['c_std']))

    def invert(self,y):
        return y*self.state['d_std']+self.state['d_mean']
