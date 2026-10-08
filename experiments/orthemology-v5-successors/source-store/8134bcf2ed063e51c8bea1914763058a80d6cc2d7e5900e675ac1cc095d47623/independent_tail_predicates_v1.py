"""Independent exact A/B evaluator. Pure functions: no files, network, or CLI.

This package checks only supplied aggregate certificates or synthetic inputs.
A successful predicate result depends on the externally sourced Berry--Esseen
theorem described in ../FINITE_MATH_SCOPE.md; this program does not prove it.
"""
from fractions import Fraction
import re


def parse_rational(value):
    """Accept exact integer or integer/positive-integer strings, never floats."""
    if type(value) is not str or re.fullmatch(r'[+-]?[0-9]+(?:/[0-9]+)?', value) is None:
        raise ValueError('An exact rational string is required.')
    parts = value.split('/')
    numerator = int(parts[0])
    denominator = int(parts[1]) if len(parts) == 2 else 1
    if denominator <= 0:
        raise ValueError('The denominator must be positive.')
    return Fraction(numerator, denominator)


def evaluate(t_text, v_text, k, r):
    """Evaluate only the two accepted inequalities, after validating inputs."""
    if type(k) is not int or type(r) is not int or k <= 0 or r <= 0:
        raise ValueError('K and R must be positive integers, excluding booleans.')
    t, variance = parse_rational(t_text), parse_rational(v_text)
    if t < 0 or variance < 0:
        raise ValueError('Threshold and variance must be nonnegative.')
    result = {'t': str(t), 'V': str(variance), 'K': k, 'R': r}
    if t == 0:
        return dict(result, status='zero_threshold_exact_tail_one', exact_tail='1')
    if variance == 0:
        raise ValueError('A positive observed threshold with zero variance is inconsistent.')

    # Independent cross-products; no square roots, probabilities, or floating point.
    tn, td = t.numerator, t.denominator
    vn, vd = variance.numerator, variance.denominator
    kr = k * r
    a_numerator = 121 * vn * td * td - 100 * tn * tn * vd
    b_numerator = 3721 * vn * kr * kr - 1000000 * vd
    a_pass, b_pass = a_numerator > 0, b_numerator > 0
    result.update({
        'M': str(Fraction(1, kr)),
        'A_lhs': str(Fraction(100 * tn * tn, td * td)),
        'A_rhs': str(Fraction(121 * vn, vd)),
        'A_margin': str(Fraction(a_numerator, vd * td * td)),
        'A': a_pass,
        'B_lhs': str(Fraction(1000000, kr * kr)),
        'B_rhs': str(Fraction(3721 * vn, vd)),
        'B_margin': str(Fraction(b_numerator, vd * kr * kr)),
        'B': b_pass,
        'status': 'certificate_conditions_hold' if a_pass and b_pass else 'certificate_unavailable',
    })
    if a_pass and b_pass:
        result['strict_lower_bound'] = '167/1500'
    return result
