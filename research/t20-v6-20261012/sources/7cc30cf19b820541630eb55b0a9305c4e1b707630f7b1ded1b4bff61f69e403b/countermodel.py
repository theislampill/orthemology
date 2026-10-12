#!/usr/bin/env python3
"""Exact rational Schur-completion variant of a classical nonmoment example.

This program computes arbitrary finite prefixes. Universal totality and strict
square positivity are proved in PROOF.md, not inferred from finite tests.
Only Python's standard library is required. No floating-point arithmetic occurs.
"""
from fractions import Fraction as Q
from math import isqrt

FIRST_TEN = ((0, 0), (2, 1), (1, 2), (1, 1), (1, 0),
             (0, 1), (2, 0), (0, 2), (3, 0), (0, 3))
SMALL_INDEX = {p: i for i, p in enumerate(FIRST_TEN, 1)}


def monomial_index(a, b):
    """One-based bijection N^2 -> positive integers."""
    if not (isinstance(a, int) and isinstance(b, int) and a >= 0 and b >= 0):
        raise ValueError("Exponents must be nonnegative integers")
    d = a + b
    return SMALL_INDEX[(a, b)] if d < 4 else b + 1 + d * (d + 1) // 2


def exponent_at(n):
    """Inverse of monomial_index, evaluated with integer arithmetic only."""
    if not isinstance(n, int) or n < 1:
        raise ValueError("Indices start at one")
    if n <= 10:
        return FIRST_TEN[n - 1]
    d = (isqrt(8 * (n - 1) + 1) - 1) // 2
    b = n - 1 - d * (d + 1) // 2
    return (d - b, b)


def midpoint_index(p, q):
    """None means an odd exponent; otherwise index of the integral midpoint."""
    a, b = p[0] + q[0], p[1] + q[1]
    return None if a % 2 or b % 2 else monomial_index(a // 2, b // 2)


def dot(v, w):
    return sum((a * b for a, b in zip(v, w)), Q(0))


class SchurMoment:
    """Lazy exact computation of the single infinitely specified sequence.

    At every stage B is the exact inverse of the previously constructed Gram
    matrix. Extending a prefix does not change any previously assigned moment.
    """
    def __init__(self):
        self.j = [Q(1), Q(1), Q(1), Q(4)]
        self.B = [[Q(1, 4) if i == j == 3 else Q(int(i == j))
                   for j in range(4)] for i in range(4)]

    def extend(self, n):
        if not isinstance(n, int) or n < 1:
            raise ValueError("Indices start at one")
        while len(self.j) < n:
            k = len(self.j) + 1
            p = exponent_at(k)
            v = []
            for i in range(1, k):
                h = midpoint_index(exponent_at(i), p)
                if h is not None and not h < k:
                    raise AssertionError("Midpoint precedence was violated")
                v.append(Q(0) if h is None else self.j[h - 1])
            w = [dot(row, v) for row in self.B]
            diagonal = Q(1) + dot(v, w)
            new_B = [[self.B[i][j] + w[i] * w[j] for j in range(k - 1)]
                     + [-w[i]] for i in range(k - 1)]
            new_B.append([-a for a in w] + [Q(1)])
            self.j.append(diagonal)
            self.B = new_B
        return self

    def moment(self, a, b):
        if not (isinstance(a, int) and isinstance(b, int) and a >= 0 and b >= 0):
            raise ValueError("Exponents must be nonnegative integers")
        if a % 2 or b % 2:
            return Q(0)
        h = monomial_index(a // 2, b // 2)
        self.extend(h)
        return self.j[h - 1]

    def gram(self, n):
        self.extend(n)
        P = [exponent_at(i) for i in range(1, n + 1)]
        return [[self.moment(a + c, b + d) for c, d in P] for a, b in P]

    def apply(self, polynomial):
        """Apply Lambda to a finitely supported dict {(a,b): rational coefficient}."""
        return sum((Q(c) * self.moment(a, b) for (a, b), c in polynomial.items()), Q(0))


def multiply(p, q):
    result = {}
    for (a, b), c in p.items():
        for (d, e), f in q.items():
            h = (a + d, b + e)
            result[h] = result.get(h, Q(0)) + Q(c) * Q(f)
    return {e: c for e, c in result.items() if c}


WITNESS = {(0, 0): Q(1), (4, 2): Q(1), (2, 4): Q(1), (2, 2): Q(-1)}


if __name__ == "__main__":
    import argparse, json, sys
    # Generated exact integers may exceed Python's default decimal-print limit.
    # This process prints its own arithmetic output; it parses no huge integers.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=int, default=15)
    args = parser.parse_args()
    model = SchurMoment().extend(args.prefix)
    print(json.dumps({"prefix": args.prefix,
                      "moments": [{"index": i, "exponent": exponent_at(i), "value": str(j)}
                                  for i, j in enumerate(model.j[:args.prefix], 1)],
                      "Lambda_F": str(model.apply(WITNESS))}, indent=2))
