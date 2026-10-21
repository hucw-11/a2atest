"""Second-order plant. Signals are callables f(time, position, velocity)."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Plant:
    m: float = 1.0
    c: float = 0.6
    kappa: float = 2.0

    def __post_init__(self):
        if self.m <= 0 or self.c < 0 or self.kappa < 0:
            raise ValueError('Require m>0, c>=0, kappa>=0')

    @property
    def A(self):
        return np.array([[0., 1.], [-self.kappa/self.m, -self.c/self.m]])

    def acceleration(self, t, state, u, d):
        x, v = state
        return (u(t, x, v)+d(t, x, v)-self.c*v-self.kappa*x)/self.m


def simulate(plant, u, d, duration=20., dt=.02, initial=(0., 0.), sigma_a=.5,
             seed=0, noise='gaussian'):
    """RK4 substepping; acceleration sensor noise never drives the true plant."""
    if dt <= 0 or duration <= 0 or sigma_a < 0:
        raise ValueError('Invalid duration, dt or noise scale')
    t = np.arange(int(round(duration/dt))+1)*dt
    states = np.zeros((len(t), 2), dtype=np.float64)
    states[0] = initial
    def rhs(time, y):
        return np.array([y[1], plant.acceleration(time, y, u, d)])
    for i in range(len(t)-1):
        y = states[i].copy()
        h = dt/4
        for j in range(4):
            time = t[i]+j*h
            a = rhs(time,y); b = rhs(time+h/2,y+h*a/2)
            c = rhs(time+h/2,y+h*b/2); e = rhs(time+h,y+h*c)
            y += h*(a+2*b+2*c+e)/6
        states[i+1] = y
    x,v = states.T
    controls = np.array([u(ti,xi,vi) for ti,xi,vi in zip(t,x,v)])
    disturbances = np.array([d(ti,xi,vi) for ti,xi,vi in zip(t,x,v)])
    acc = (controls+disturbances-plant.c*v-plant.kappa*x)/plant.m
    rng = np.random.default_rng(seed)
    if noise == 'gaussian':
        eps = rng.normal(0,sigma_a,len(t))
    elif noise == 'student':
        eps = rng.standard_t(3,len(t))*sigma_a/np.sqrt(3)
    else:
        raise ValueError(noise)
    measured = acc+eps
    dhat = plant.m*measured+plant.c*v+plant.kappa*x-controls
    return dict(t=t,x=x,v=v,u=controls,d=disturbances,a=acc,a_measured=measured,
                dhat=dhat,params=np.array([plant.m,plant.c,plant.kappa]),
                sigma_a=float(sigma_a),noise=noise,dt=dt)


def random_signals(rng, kind='multisine'):
    if '+' in kind:
        names=kind.split('+')
        components=[random_signals(rng,name) for name in names]
        weights=rng.uniform(.5,1.,len(names))
        weights=weights/np.linalg.norm(weights)
        def mixed(t,x,v):
            return float(sum(w*pair[1](t,x,v) for w,pair in zip(weights,components)))
        return components[0][0],mixed
    amplitudes=rng.uniform(.15,.8,3); frequencies=rng.uniform(.12,1.3,3)
    phases=rng.uniform(-np.pi,np.pi,3)
    fu,pu=rng.uniform(.1,.8),rng.uniform(-np.pi,np.pi)
    def u(t,x,v):
        return .8*np.sin(2*np.pi*fu*t+pu)+.25*np.cos(2*np.pi*.17*t)
    if kind == 'multisine':
        def d(t,x,v):
            return float(np.sum(amplitudes*np.sin(2*np.pi*frequencies*t+phases)))
    elif kind == 'chirp':
        f0,rate=rng.uniform(.1,.4),rng.uniform(.02,.09)
        def d(t,x,v):
            return float(amplitudes.sum()*.65*np.sin(2*np.pi*(f0*t+rate*t*t/2)+phases[0]))
    elif kind == 'steps':
        levels=rng.uniform(-1.2,1.2,16); interval=rng.uniform(1.,2.)
        def d(t,x,v):
            return float(levels[min(int(t/interval),len(levels)-1)]+.15*np.sin(2*np.pi*.4*t))
    else:
        raise ValueError(kind)
    return u,d


SIGNAL_FAMILIES=('multisine','chirp','steps','multisine+chirp','multisine+steps',
                 'chirp+steps','multisine+chirp+steps')


def make_trajectories(n, seed, sigma=None, noise='gaussian', duration=16.,families=None):
    rng=np.random.default_rng(seed)
    result=[]
    for i in range(n):
        family_names=('multisine','chirp','steps') if families is None else tuple(families)
        if not family_names: raise ValueError('At least one signal family is required')
        kind=family_names[i%len(family_names)]
        u,d=random_signals(rng,kind)
        p=Plant(rng.uniform(.8,1.2),rng.uniform(.3,1.),rng.uniform(1.,3.))
        tr=simulate(p,u,d,duration=duration,initial=rng.normal(0,.2,2),
                    sigma_a=float(rng.uniform(.2,.9) if sigma is None else sigma),
                    seed=int(rng.integers(2**31)),noise=noise)
        tr['kind']=kind; tr['trajectory_id']=f'{seed}:{i}'
        result.append(tr)
    return result
