from collections import Counter

import numpy as np

from closed_loop.core import DT


def validation_weights(traces,data):
    """Equal shock strata/events and equal background trajectories, not point counts."""
    count=len(traces); shock=np.zeros((count,601)); background=np.zeros_like(shock)
    strata=Counter(tr['stratum'] for tr in traces if tr['events'])
    for j,tr in enumerate(traces):
        valid=np.zeros(601,dtype=bool); valid[50:578]=True
        bg=valid.copy()
        for event in tr['events']:
            a,b=event['start'],event['end']
            if not valid[a:b].all(): raise AssertionError('An event is outside the evaluation window')
            shock[j,a:b]=1/(len(strata)*strata[tr['stratum']]*len(tr['events'])*(b-a))
            bg[a:min(601,b+25)]=False
        background[j,bg]=1/(count*int(bg.sum()))
    ids,indices=data['trajectory'],data['index']
    a,b=shock[ids,indices],background[ids,indices]
    np.testing.assert_allclose([a.sum(),b.sum()],[1.,1.],atol=1e-12)
    return a,b


def validation_score(pred,target,weights):
    error=(np.asarray(pred,dtype=float)-target[:,0])**2
    shock=float(error@weights[0]); background=float(error@weights[1])
    return dict(score=.5*(shock+background),shock_rmse=float(np.sqrt(shock)),
                background_rmse=float(np.sqrt(background)))


def expand(pred,data,count):
    full=np.full((count,601),np.nan)
    full[data['trajectory'],data['index']]=pred
    return full


def event_metrics(tr,pred):
    pred=np.asarray(pred); truth=tr['d']; bg=tr['background']; records=[]
    valid=np.zeros(len(pred),dtype=bool); valid[50:578]=True
    background=valid.copy()
    for eid,event in enumerate(tr['events']):
        a,b=event['start'],event['end']; extended=b+25
        if not np.isfinite(pred[a:extended]).all(): raise AssertionError('Missing event or recovery predictions')
        err=pred[a:b]-truth[a:b]; amplitude=event['amplitude']; sign=np.sign(amplitude)
        pulse_est=pred[a:extended]-bg[a:extended]
        peak=int(np.argmax(sign*pulse_est)); peak_value=sign*pulse_est[peak]
        peak_time_distance=max(0,peak-(b-a-1))*DT
        record=dict(event=eid,start=a,end=b,amplitude=amplitude,area=event['area'],
             mse=float(np.mean(err**2)),onset_mse=float(err[0]**2),
             relative_mse=float(np.mean(err**2)/(amplitude**2)),
             peak_absolute_error=float(abs(peak_value-abs(amplitude))),
             peak_time_distance_s=float(peak_time_distance),
             area_absolute_error=float(abs(np.sum(err)*DT)),
             extended_area_absolute_error=float(abs(np.sum(pred[a:extended]-truth[a:extended])*DT)),
             post_mse=float(np.mean((pred[b:extended]-truth[b:extended])**2)))
        records.append(record); background[a:extended]=False
    result=dict(trajectory=tr['trajectory_id'],stratum=tr['stratum'],regime=tr['regime'],width=tr['width'],
                total_mse=float(np.mean((pred[valid]-truth[valid])**2)),
                background_mse=float(np.mean((pred[background]-truth[background])**2)),
                event_mse=float(np.mean([r['mse'] for r in records])) if records else None)
    for key in ('onset_mse','relative_mse','peak_absolute_error','peak_time_distance_s',
                'area_absolute_error','extended_area_absolute_error','post_mse'):
        result[key]=float(np.mean([r[key] for r in records])) if records else None
    return result,records


def summarize(rows):
    shock=[r for r in rows if r['event_mse'] is not None]
    strata=sorted({r['stratum'] for r in shock})
    shock_mse=float(np.mean([np.mean([r['event_mse'] for r in shock if r['stratum']==s]) for s in strata]))
    result=dict(shock_rmse=float(np.sqrt(shock_mse)),
                background_rmse=float(np.sqrt(np.mean([r['background_mse'] for r in rows]))),
                total_rmse=float(np.sqrt(np.mean([r['total_mse'] for r in rows]))))
    for key in ('onset_mse','relative_mse','post_mse'):
        value=np.mean([r[key] for r in shock]); result[key.replace('_mse','_rmse')]=float(np.sqrt(value))
    for key in ('peak_absolute_error','peak_time_distance_s','area_absolute_error','extended_area_absolute_error'):
        result[key]=float(np.mean([r[key] for r in shock]))
    return result
