"""Exact finite application probes, not a canonical Orthemology module."""
from fractions import Fraction as F


def target_decoder(profiles, score, target):
    """An attained-image decoder iff the target is constant on score fibres."""
    decoder = {}
    for profile in profiles:
        key, value = score(profile), target(profile)
        if key in decoder and decoder[key] != value:
            return None
        decoder[key] = value
    return decoder


def weight_witness_2d(gains, strict_positive=True):
    """Exact rational supporting weights for a finite set of 2-D gains.

    We normalize to weights (t,1-t). This checks all convex combinations by
    linearity; it does not declare the resulting weights normatively correct.
    """
    lower, upper = F(0), F(1)
    for first, second in gains:
        first, second = F(first), F(second)
        coefficient = first - second
        if coefficient == 0:
            if second > 0:
                return None
        elif coefficient > 0:
            upper = min(upper, -second / coefficient)
        else:
            lower = max(lower, -second / coefficient)
    if lower > upper:
        return None
    t = (lower + upper) / 2
    if strict_positive and not 0 < t < 1:
        return None
    if not 0 <= t <= 1:
        return None
    result = (t, 1-t)
    assert all(result[0]*F(d[0]) + result[1]*F(d[1]) <= 0 for d in gains)
    return result


def is_nash_2x2(a, b, p, q):
    """Exact mixed Nash check: p is row-0, q column-0 probability."""
    p, q = F(p), F(q)
    if not 0 <= p <= 1 or not 0 <= q <= 1:
        raise ValueError('Mixed probabilities must lie in [0,1]')
    row_payoffs = [q*F(a[i][0]) + (1-q)*F(a[i][1]) for i in range(2)]
    col_payoffs = [p*F(b[0][j]) + (1-p)*F(b[1][j]) for j in range(2)]
    row_value = p*row_payoffs[0] + (1-p)*row_payoffs[1]
    col_value = q*col_payoffs[0] + (1-q)*col_payoffs[1]
    return row_value >= max(row_payoffs) and col_value >= max(col_payoffs)


def local_factorization(states, observe, desired):
    """Return a local policy on attained observations, or None if impossible."""
    policy = {}
    for state in states:
        observation = observe(state)
        action = desired(state)
        if observation in policy and policy[observation] != action:
            return None
        policy[observation] = action
    return policy
