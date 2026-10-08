"""Pure exact aggregate certificate predicates, extracted from the frozen v2 checker.

No raw-data access or empirical execution entry point is present. The probability
interpretation depends on the external Tyurin theorem stated in ../FINITE_MATH_SCOPE.md.
"""
from fractions import Fraction
import re

def rational(obj):
    if not isinstance(obj, dict) or set(obj) != {"numerator", "denominator"}:
        raise ValueError("Expected exact rational object")
    for value in obj.values():
        if not isinstance(value, str) or not re.fullmatch(r"[+-]?[0-9]+", value):
            raise ValueError("Rational components must be integer strings")
    numerator, denominator = int(obj["numerator"]), int(obj["denominator"])
    if denominator <= 0:
        raise ValueError("Denominator must be positive")
    return Fraction(numerator, denominator)


def encode(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def evaluate(K, R, t, V):
    if type(K) is not int or type(R) is not int or K <= 0 or R <= 0:
        raise ValueError("K and R must be positive integers")
    if not isinstance(t, Fraction) or not isinstance(V, Fraction) or t < 0 or V < 0:
        raise ValueError("t and V must be nonnegative exact rationals")
    if V == 0 and t > 0:
        raise ValueError("Positive observed threshold with zero variance is inconsistent")
    M = Fraction(1, K * R)
    result = {"K": K, "R": R, "t": encode(t), "V": encode(V), "M": encode(M)}
    if t == 0:
        return dict(result, status="ZERO_THRESHOLD_TAIL_ONE", exact_tail=encode(Fraction(1)))
    checks = {}
    for name, left, right in (("A", 100 * t * t, 121 * V),
                              ("B", 1000000 * M * M, 3721 * V)):
        checks[name] = {"left": encode(left), "right": encode(right),
                        "right_minus_left": encode(right - left), "passed": left < right}
    result["checks"] = checks
    if all(item["passed"] for item in checks.values()):
        result.update(status="STRICT_LOWER_CERTIFICATE_PASS",
                      strict_lower_bound=encode(Fraction(167, 1500)),
                      reference_level=encode(Fraction(1, 20)),
                      lower_bound_above_reference_margin=encode(Fraction(23, 375)))
    else:
        result["status"] = "CERTIFICATE_UNAVAILABLE"
    return result


def reconcile(aggregate, replication):
    original = aggregate["exact_description"]
    independent = replication["independent_exact_description"]
    def selected(d):
        if not isinstance(d, dict) or type(d.get("games")) is not int or d["games"] <= 0:
            raise ValueError("Each aggregate games count must be a positive nonboolean integer")
        return d["games"], rational(d["T"]), rational(d["V"])
    first, second = selected(original), selected(independent)
    if first != second:
        raise ValueError("Original and independent K,t,V disagree")
    return first

