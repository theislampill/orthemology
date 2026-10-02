"""Exact conditional confidence-budget witnesses for the coBuchi cost theorem.

This validates arithmetic parameters and witness inequalities only. It does not
check a winning region, controller implementation, or applicability to the world.
No floating-point logarithm or exponential is used.
"""
from fractions import Fraction as F


class BudgetResourceLimit(ValueError):
    """The requested exact integer computation exceeds the declared work guard."""


def _positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f'{name} must be a positive integer')
    return value


def _fraction(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError(f'{name} must be an exact Fraction or integer, not a float')
    return F(value)


def ceil_log2_fraction(value):
    """Least nonnegative k with 2**k >= a positive exact rational value."""
    x = _fraction(value, 'log argument')
    if x <= 0:
        raise ValueError('log argument must be positive')
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if (1 << k) * x.denominator < x.numerator:
        k += 1
    if k and (1 << (k - 1)) * x.denominator >= x.numerator:
        k -= 1
    return k


def _ceil(value):
    return -((-value.numerator) // value.denominator)


def budget_certificate(*, states, actions, models, p_min, margin,
                       failure_probability, max_power_bits=1_000_000):
    """Produce an integer T whose conditional theorem guarantees P(C>T)<=delta.

    p_min must lower-bound every positive actual row entry; margin must be a
    genuine empirical separating margin. Those semantic conditions are supplied,
    not inferred by this arithmetic evaluator.
    """
    s = _positive_int(states, 'states')
    a = _positive_int(actions, 'actions')
    m = _positive_int(models, 'models')
    limit = _positive_int(max_power_bits, 'max_power_bits')
    p = _fraction(p_min, 'p_min')
    eta = _fraction(margin, 'margin')
    delta = _fraction(failure_probability, 'failure_probability')
    if not 0 < p <= 1:
        raise ValueError('p_min must lie in (0,1]')
    if eta <= 0:
        raise ValueError('margin must be positive')
    if not 0 < delta < 1:
        raise ValueError('failure_probability must lie in (0,1)')
    if s * max(1, a.bit_length()) > limit:
        raise BudgetResourceLimit('rotor-size integer exceeds the work guard')
    D = s * a**s
    if p != 1 and D * max(p.numerator.bit_length(), p.denominator.bit_length()) > limit:
        raise BudgetResourceLimit('exact path-probability power exceeds the work guard')
    r = F(1) if p == 1 else p**D
    q = s * a
    capped = min(eta, F(1))
    c = capped**2 / 2
    A = F(2 * q * s) * (1 + c) / c
    k = ceil_log2_fraction(2 * A / delta)
    n = _ceil(F(k) / c)
    j = q * (n + m - 1) + 2 * m * (n + m + 1)
    ell = ceil_log2_fraction(2 / delta)
    T = _ceil(F(2 * D) * (j + ell) / r)
    return {
        'claim': 'CONDITIONAL_PARAMETER_BOUND_ONLY',
        'states': s, 'actions': a, 'models': m,
        'p_min': p, 'margin': eta, 'failure_probability': delta,
        'rotor_size_bound': D, 'block_success_lower': r,
        'tail_rate': c, 'tail_coefficient_upper': A,
        'cutoff_log_witness': k, 'cutoff': n,
        'charged_interval_bound': j, 'residual_log_witness': ell,
        'bad_count_budget': T,
        'unverified_semantic_preconditions': [
            'initial state belongs to the specified computed winning region',
            'actual policy is the admitted generated coBuchi controller',
            'hard-menu, common-policy and row-law contracts hold',
            'p_min and margin are valid for the actual finite input',
        ],
    }


def verify_certificate(cert, *, max_power_bits=1_000_000):
    """Recompute numeric data and check the exact dyadic witness inequalities."""
    try:
        # Numeric equality alone accepts 72.0 == 72 and 0.5 == Fraction(1,2).
        # A certificate is a canonical exact-data record, not merely an equal value.
        if type(cert) is not dict:
            return False
        integer_fields = ('states','actions','models','rotor_size_bound',
            'cutoff_log_witness','cutoff','charged_interval_bound',
            'residual_log_witness','bad_count_budget')
        rational_fields = ('p_min','margin','failure_probability',
            'block_success_lower','tail_rate','tail_coefficient_upper')
        if any(type(cert[k]) is not int for k in integer_fields):
            return False
        if any(type(cert[k]) is not F for k in rational_fields):
            return False
        if type(cert['claim']) is not str:
            return False
        premises = cert['unverified_semantic_preconditions']
        if type(premises) is not list or any(type(v) is not str for v in premises):
            return False
        keys = ('states','actions','models','p_min','margin','failure_probability')
        expected = budget_certificate(**{k:cert[k] for k in keys},
                                      max_power_bits=max_power_bits)
        if cert != expected:
            return False
        n = cert['cutoff']; k = cert['cutoff_log_witness']
        c = cert['tail_rate']; A = cert['tail_coefficient_upper']
        delta = cert['failure_probability']; ell = cert['residual_log_witness']
        return (n >= 1 and c*n >= k and F(2)**k >= 2*A/delta
                and F(2)**ell >= 2/delta
                and cert['block_success_lower']*cert['bad_count_budget']
                    >= 2*cert['rotor_size_bound']*(cert['charged_interval_bound']+ell))
    except (KeyError, TypeError, ValueError, OverflowError):
        return False
