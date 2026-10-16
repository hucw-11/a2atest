"""Apply a trained estimator to a fresh custom second-order system."""
import argparse
from pathlib import Path
import numpy as np
from a2afm.system import Plant,simulate
from a2afm.inference import DisturbanceEstimator

def main():
    p=argparse.ArgumentParser(); p.add_argument('--checkpoint',default='results/main/a2afm_seed11.pt')
    p.add_argument('--out',default='results/application.npz'); args=p.parse_args()
    u=lambda t,x,v: .7*np.sin(2*np.pi*.3*t)
    d=lambda t,x,v: .8*np.sin(2*np.pi*.6*t)+.3*np.cos(2*np.pi*1.1*t)
    tr=simulate(Plant(),u,d,duration=10,sigma_a=.5,seed=91234)
    estimator=DisturbanceEstimator(args.checkpoint); length=estimator.length
    predicted=np.full(len(tr['t']),np.nan)
    for i in range(length-1,len(predicted)):
        s=slice(i-length+1,i+1)
        predicted[i],_=estimator.estimate(tr['x'][s],tr['v'][s],tr['u'][s],tr['a_measured'][s],tr['params'])
    valid=np.isfinite(predicted)
    rmse=float(np.sqrt(np.mean((predicted[valid]-tr['d'][valid])**2)))
    path=Path(args.out); path.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(path,t=tr['t'],truth=tr['d'],raw=tr['dhat'],estimate=predicted)
    print(f'Online causal application RMSE={rmse:.6f}; saved {path.resolve()}')

if __name__=='__main__': main()
