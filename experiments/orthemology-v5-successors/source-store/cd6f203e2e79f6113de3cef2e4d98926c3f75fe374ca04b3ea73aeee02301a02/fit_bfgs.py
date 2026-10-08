"""Independent implementation A: equal-level probit with multistart BFGS."""
import numpy as np
from scipy.special import log_ndtr
from scipy.optimize import minimize


def fit(contrast, response, weighting='equal_bin'):
    x, y = np.asarray(contrast, float), np.asarray(response, float)
    if x.ndim != 1 or x.shape != y.shape or not np.isfinite(x).all():
        raise ValueError('Invalid contrast/response vectors')
    if weighting not in ('equal_bin', 'trial_count'):
        raise ValueError('Unknown weighting')
    if not np.isfinite(y).all() or np.any((y < 0) | (y > 1)):
        raise ValueError('Responses must be finite values in [0, 1]')
    xs = np.unique(x)
    if len(xs) != 8:
        raise ValueError('Exactly eight populated contrast levels required')
    ys = np.array([y[x == level].mean() for level in xs])
    counts = np.array([np.count_nonzero(x == level) for level in xs])
    D = np.column_stack([np.ones(len(xs)), xs*10])
    w = np.ones(len(xs)) if weighting == 'equal_bin' else counts

    def fg(beta):
        eta = D@beta
        lp, lq = log_ndtr(eta), log_ndtr(-eta)
        phi = -.5*eta**2-.5*np.log(2*np.pi)
        rp, rq = np.exp(phi-lp), np.exp(phi-lq)
        value = -np.sum(w*(ys*lp+(1-ys)*lq))
        grad = -D.T@(w*(ys*rp-(1-ys)*rq))
        return value, grad

    fits = [minimize(fg, np.array(start), jac=True, method='BFGS',
                    options={'gtol':1e-11, 'maxiter':2000})
            for start in ([0.,1.], [0.,0.], [0.,-1.])]
    chosen = min(fits, key=lambda result: result.fun)
    score = float(np.max(np.abs(fg(chosen.x)[1])))
    if not np.isfinite(chosen.x).all() or score > 2e-7:
        raise ValueError('BFGS fit failed stationarity check')
    return {'sensitivity':float(chosen.x[1]*10/np.sqrt(2*np.pi)),
            'intercept':float(chosen.x[0]), 'beta1_contrast':float(chosen.x[1]*10),
            'negative_log_likelihood':float(chosen.fun), 'bin_counts':counts.tolist()}
