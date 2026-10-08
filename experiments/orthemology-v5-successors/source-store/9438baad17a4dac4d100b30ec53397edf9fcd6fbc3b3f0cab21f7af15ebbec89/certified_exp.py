"""Version 1: exact rational Taylor brackets and outward dyadic intervals.

No floating-point arithmetic is used. This module is intentionally small enough
for independent inspection. See ../FINITE_MATH_SCOPE.md for the enclosure proof.
"""
from fractions import Fraction

VERSION = 'rational-alternating-dyadic-v1'
GAMMAS = tuple(map(Fraction, ('1', '11/10', '5/4', '3/2', '2', '3', '5', '10')))
ALPHA = Fraction(1, 20)
WIDTH_TARGET = Fraction(1, 10**12)


def exp_neg_interval(x: Fraction, bits: int = 256):
    """Enclose exp(-x), x>=0, with exact endpoints on a 2**(-bits) grid.

    At every operation lower endpoints round down and upper endpoints round up.
    If true values are below the fixed-point grid, the upper endpoint remains
    strictly positive. bits is an absolute fixed-point precision, not a claim of
    relative accuracy for underflow-scale results.
    """
    x = Fraction(x)
    if x < 0 or type(bits) is not int or bits < 256:
        raise ValueError('nonnegative rational and at least 256 bits required')
    if x == 0:
        return Fraction(1), Fraction(1)
    scale = 1 << bits
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length() + 4)
    y = x / (1 << k)
    while y > Fraction(1, 8):
        y /= 2
        k += 1
    # The decreasing alternating series has odd partial sums below exp(-y)
    # and even partial sums above it. Bounds themselves are exact rationals.
    term, partial, lower, upper = Fraction(1), Fraction(1), Fraction(0), Fraction(1)
    n = 0
    while upper - lower > Fraction(1, 1 << (bits + 8)):
        n += 1
        term *= -y / n
        partial += term
        if n % 2:
            lower = partial
        else:
            upper = partial
    lo = (lower.numerator * scale) // lower.denominator
    hi = -((-upper.numerator * scale) // upper.denominator)
    for _ in range(k):
        lo = (lo * lo) // scale
        hi = -((-hi * hi) // scale)
    return Fraction(lo, scale), Fraction(hi, scale)


def closed_bound(t, total_abs, variance, gamma, bits=256):
    """Frozen closed-form upper bound, not a robust-tail optimizer."""
    t, total_abs, variance, gamma = map(Fraction, (t, total_abs, variance, gamma))
    if min(t, total_abs, variance) < 0 or gamma < 1:
        raise ValueError('invalid closed-bound argument')
    rho = (gamma - 1) / (gamma + 1)
    drift = rho * total_abs
    exponent = Fraction(0) if variance == 0 else -(max(Fraction(0), t - drift)**2) / (2 * variance)
    if t == 0 or variance == 0:
        lo, hi = Fraction(1), Fraction(1)
    else:
        lo, hi = exp_neg_interval(-exponent, bits)
        lo, hi = min(Fraction(1), 2 * lo), min(Fraction(1), 2 * hi)
    # Same frozen calculation may refine numerical precision only.
    while hi - lo > WIDTH_TARGET and bits < 4096:
        bits *= 2
        lo, hi = exp_neg_interval(-exponent, bits)
        lo, hi = min(Fraction(1), 2 * lo), min(Fraction(1), 2 * hi)
    return {'Gamma': gamma, 'rho': rho, 'D': drift, 'exponent': exponent,
            'interval': (lo, hi), 'precision_bits': bits,
            'width_requirement_pass': hi - lo <= WIDTH_TARGET,
            'reference_comparison': alpha_relation(lo, hi)}


def alpha_relation(lower, upper):
    if lower < 0 or upper < lower or upper > 1:
        raise ValueError('invalid probability interval')
    if upper <= ALPHA:
        return 'upper_bound_at_or_below_reference'
    if lower > ALPHA:
        return 'bound_above_reference_not_lower_bound_on_p_star'
    return 'unresolved_enclosure'


def upward_decimal(value, places=12):
    """Fixed decimal upper display; never a nearest-rounded certificate."""
    value = Fraction(value)
    if value < 0 or type(places) is not int or places < 0:
        raise ValueError('nonnegative display required')
    scale = 10**places
    integer = -((-value.numerator * scale) // value.denominator)
    if places == 0:
        return str(integer)
    whole, part = divmod(integer, scale)
    return str(whole) + '.' + str(part).zfill(places)
