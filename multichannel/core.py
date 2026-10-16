"""Causal sensor corruption and a physics-based multisensor observer."""
import numpy as np
from scipy.linalg import expm


SCENARIOS = {
    'clean': (0., 0.),
    'x_1pct': (.01, 0.), 'v_1pct': (0., .01), 'xv_1pct': (.01, .01),
    'x_5pct': (.05, 0.), 'v_5pct': (0., .05), 'xv_5pct': (.05, .05),
}


def reference_scales(training):
    """One fixed population scale per channel, fitted only on clean training data."""
    return {k: float(np.std(np.concatenate([t[k] for t in training]))) for k in ('x', 'v')}


def measure(trajectory, scales, fractions, seed):
    """Corrupt observations, never the physical states or ground-truth labels.

    All scenarios share standardized sensor draws for a given trajectory seed.
    The SAME measured x/v enter both the residual and the network conditions.
    """
    fx, fv = fractions
    if min(fx, fv) < 0:
        raise ValueError('Noise fractions must be nonnegative')
    out = dict(trajectory)
    rng = np.random.default_rng(seed)
    ex, ev = rng.normal(size=(2, len(trajectory['t'])))
    sx, sv = fx * scales['x'], fv * scales['v']
    out['x_true'], out['v_true'] = trajectory['x'], trajectory['v']
    out['x'] = trajectory['x'] + sx * ex
    out['v'] = trajectory['v'] + sv * ev
    m, c, k = trajectory['params']
    out['dhat'] = m*out['a_measured'] + c*out['v'] + k*out['x'] - out['u']
    out['sigma_x'], out['sigma_v'] = sx, sv
    out['residual_variance'] = float((m*out['sigma_a'])**2 + (c*sv)**2 + (k*sx)**2)
    return out


def augmented_kalman(tr, q):
    """State [x,v,d,d_dot], measurements [x_m,v_m,a_m], known applied u.

    Continuous prior: x'=v, v'=(-kx-cv+d+u)/m, d'=d_dot,
    d_dot'=white noise of spectral density q. Exact matrix-exponential
    discretization; u is held at its previous sample during prediction.
    Sensor noise covariance is diagonal; residual and x/v are not treated as
    independent measurements. No true x/v/d is accessed.
    """
    if q <= 0:
        raise ValueError('q must be positive')
    m, c, k = tr['params']; dt = tr['dt']
    a = np.array([[0, 1, 0, 0], [-k/m, -c/m, 1/m, 0],
                  [0, 0, 0, 1], [0, 0, 0, 0]], dtype=float)
    ab = np.zeros((5, 5)); ab[:4, :4] = a; ab[1, 4] = 1/m
    discrete = expm(ab*dt); f, b = discrete[:4, :4], discrete[:4, 4]
    density = np.zeros((4, 4)); density[3, 3] = q
    van_loan = expm(np.block([[a, density], [np.zeros((4, 4)), -a.T]])*dt)
    process = van_loan[:4, 4:] @ f.T
    process = (process + process.T)/2
    h = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [-k/m, -c/m, 1/m, 0]])
    r = np.diag([tr['sigma_x']**2, tr['sigma_v']**2, tr['sigma_a']**2])
    state = np.zeros(4); p = np.eye(4)*10; result = np.empty(len(tr['t']))
    for i in range(len(result)):
        if i:
            state = f @ state + b*tr['u'][i-1]
            p = f @ p @ f.T + process
        y = np.array([tr['x'][i], tr['v'][i], tr['a_measured'][i]-tr['u'][i]/m])
        ph = p @ h.T
        gain = np.linalg.solve(h @ ph + r, ph.T).T
        state += gain @ (y-h @ state)
        update = np.eye(4)-gain @ h
        p = update @ p @ update.T + gain @ r @ gain.T
        p = (p+p.T)/2
        result[i] = state[2]
    return result
