"""Rebuild figures from saved trajectories without retraining or simulation."""
from pathlib import Path
import numpy as np
from closed_loop.core import scenarios
from closed_loop.experiment import plot_examples

def main():
    out=Path(__file__).resolve().parents[1]/'results/closed_loop'
    specs=scenarios(24,73000)
    for stage in ['open_frozen','closed_frozen','closed_adapted']:
        examples={}
        for method in ['none','dob','kalman','regression','a2afm']:
            seed=11 if method in ['regression','a2afm'] else -1
            z=np.load(out/f'{stage}_{method}_{seed}.npz')
            examples[method]=[{**s,**{name:z[f'{name}_{i}'] for name in ['t','d','estimate','x','v','u','command','error','dhat']}} for i,s in enumerate(specs)]
        plot_examples(stage,examples,out,stage!='open_frozen')

if __name__=='__main__': main()
