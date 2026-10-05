"""Independent implementation B: observed-Hessian fitting and Fisher checks."""
import numpy as np
from scipy import optimize, special

SQRT2PI = np.sqrt(2 * np.pi)
LOG2PI = np.log(2 * np.pi)


def objective_parts(b, X, y, weights):
    """Stable probit cross-entropy, observed gradient and observed Hessian."""
    eta = X @ b
    lp, lq = special.log_ndtr(eta), special.log_ndtr(-eta)
    ld = -.5 * eta**2 - .5 * LOG2PI
    rp, rq = np.exp(ld-lp), np.exp(ld-lq)
    f = -np.sum(weights*(y*lp + (1-y)*lq))
    g = X.T @ (weights*(-y*rp + (1-y)*rq))
    curvature = weights*(y*rp*(eta+rp) + (1-y)*rq*(-eta+rq))
    H = X.T @ (curvature[:, None] * X)
    return f, g, H


def fisher_scoring(X, y, weights):
    """Separately iterated expected-information scoring check, with line search."""
    b = np.zeros(2)
    for iteration in range(1000):
        f, g, _ = objective_parts(b, X, y, weights)
        eta = X@b
        logphi = -.5*eta**2-.5*LOG2PI
        w = weights*np.exp(2*logphi-special.log_ndtr(eta)-special.log_ndtr(-eta))
        information = X.T@(w[:, None]*X)
        step = np.linalg.solve(information, g)
        if np.max(np.abs(g)) < 1e-11:
            break
        factor = 1.
        while objective_parts(b-factor*step, X, y, weights)[0] > f + 1e-14:
            factor /= 2
            if factor < 2**-40:
                break
        new = b-factor*step
        if np.max(np.abs(new-b)) < 1e-13:
            b = new
            break
        b = new
    return b, iteration+1, float(np.max(np.abs(objective_parts(b, X, y, weights)[1])))


def fit(x, responses, weighting='equal_bin'):
    """Independent implementation B with analytic Hessian and score checks."""
    x, responses = np.asarray(x, float), np.asarray(responses, float)
    if x.ndim != 1 or x.shape != responses.shape or not np.isfinite(x).all():
        raise ValueError('Invalid contrast/response vectors')
    if weighting not in ('equal_bin', 'trial_count'):
        raise ValueError('Unknown weighting')
    if not np.isfinite(responses).all() or np.any((responses < 0) | (responses > 1)):
        raise ValueError('Responses must be finite values in [0, 1]')
    if len(np.unique(x)) != 8:
        raise ValueError('Exactly eight populated contrast levels required')
    levels = np.unique(x)
    ns, ys = [], []
    for level in levels:
        r = responses[(x==level) & np.isfinite(responses)]
        ns.append(len(r))
        ys.append(np.mean(r) if len(r) else np.nan)
    ns, ys = np.asarray(ns), np.asarray(ys)
    keep = np.isfinite(ys)
    xv, y, n = levels[keep], ys[keep], ns[keep]
    scale = np.max(np.abs(xv))
    X = np.column_stack([np.ones(len(xv)), xv/scale])
    w = np.ones(len(xv)) if weighting == "equal_bin" else n.astype(float)
    candidates = []
    for initial in [np.zeros(2), np.array([.2, 2.]), np.array([-.2, -2.])]:
        opt = optimize.minimize(lambda b: objective_parts(b,X,y,w)[0], initial,
                                jac=lambda b: objective_parts(b,X,y,w)[1],
                                hess=lambda b: objective_parts(b,X,y,w)[2],
                                method="trust-exact", options={"gtol":1e-11, "maxiter":1000})
        # A root solve polishes the actual likelihood score; no clipping/penalty.
        root = optimize.root(lambda b: objective_parts(b,X,y,w)[1], opt.x,
                             jac=lambda b: objective_parts(b,X,y,w)[2], method="hybr",
                             options={"xtol":1e-11})
        b = root.x if np.linalg.norm(objective_parts(root.x,X,y,w)[1]) < np.linalg.norm(objective_parts(opt.x,X,y,w)[1]) else opt.x
        f,g,H = objective_parts(b,X,y,w)
        candidates.append((b,f,g,H,bool(opt.success),str(opt.message),bool(root.success)))
    best = min(candidates, key=lambda row: np.linalg.norm(row[2]))
    b,f,g,H,success,message,rootsuccess = best
    fs, its, fsgrad = fisher_scoring(X,y,w)
    slope = b[1]/scale/SQRT2PI
    startspread = max(np.max(np.abs(row[0]-b)) for row in candidates)
    checkspread = np.max(np.abs(fs-b))
    if not (np.all(np.isfinite(b)) and np.max(np.abs(g)) < 1e-8
            and np.min(np.linalg.eigvalsh(H)) > 0
            and startspread < 1e-6 and checkspread < 1e-6):
        raise ValueError('Checked fit failed numerical convergence criteria')
    return {"sensitivity":float(slope), "intercept":float(b[0]),
            "beta1_contrast":float(b[1]/scale), "negative_log_likelihood":float(f),
            "n_trials":int(n.sum()), "bin_counts":n.tolist(), "n_bins":len(n),
            "empty_bins_removed":int(np.sum(~keep)), "weighting":weighting,
            "max_abs_score_scaled":float(np.max(np.abs(g))),
            "observed_hessian_eigenvalues_scaled":np.linalg.eigvalsh(H).tolist(),
            "max_parameter_difference_three_starts_scaled":float(startspread),
            "fisher_scoring_max_parameter_difference_scaled":float(checkspread),
            "fisher_scoring_iterations":its, "fisher_scoring_max_score":fsgrad,
            "optimizer_success_before_polishing":success,
            "optimizer_message_before_polishing":message,"root_success":rootsuccess}

