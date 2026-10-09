#!/usr/bin/env python3
"""Independent exact controls for the interaction-calibration-anchor candidate.

Uses only Python standard-library integer and Fraction arithmetic. These finite
controls test consequences and countermodels; the general theorem is reviewed
by proof, not inferred from the grid. Writes only an optional explicitly named
JSON output inside this review directory.
"""
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
checks = {}


def rate_product(rates, mask):
    return prod((v for i, v in enumerate(rates) if mask >> i & 1), start=F(1))


def q(counts, rates, active):
    result = F(1)
    for support, count in enumerate(counts, start=1):
        if count and support & active == support:
            result *= (1 - rate_product(rates, support)) ** count
    return result


def isolated_factor(table, support):
    result = F(1)
    sub = support
    while True:
        sign = 1 if (support.bit_count() - sub.bit_count()) % 2 == 0 else -1
        assert table[sub] > 0, 'Interior mask logs require strictly positive Q.'
        result *= table[sub] ** sign
        if sub == 0:
            return result
        sub = (sub - 1) & support


def kink(x):
    # Continuous and strictly increasing, not differentiable at x=1/3.
    return 2*x if x <= F(1, 3) else (x + 1)/2


def verify_isolation(counts, rates):
    table = [q(counts, rates, mask) for mask in range(1 << len(rates))]
    nchecks = 0
    for support, count in enumerate(counts, start=1):
        got = isolated_factor(table, support)
        expected = (1 - rate_product(rates, support)) ** count
        assert got == expected
        assert (got == 1) == (count == 0)
        assert (got < 1) == (count > 0)
        nchecks += 1
    return nchecks


def masks():
    num = 0
    worlds = 0
    for roots in (1, 2, 3):
        rates = [F(1, 2), F(2, 5), F(3, 7)][:roots]
        for counts in product(range(3), repeat=(1 << roots)-1):
            num += verify_isolation(counts, rates)
            worlds += 1
    # Deterministic dense/holey higher-root inventories; unrelated maps may kink.
    for roots in (4, 5):
        rates = [kink(F(i+1, roots+2)) for i in range(roots)]
        for seed in range(32):
            counts = tuple(((support * 17 + seed * 13) ^ (support >> 1)) % 4
                           for support in range(1, 1 << roots))
            num += verify_isolation(counts, rates)
            worlds += 1
    checks['exact_mask_isolation'] = {'worlds': worlds, 'support_checks': num}


def unary_fibres_and_interaction_rejection():
    unary = 0
    interaction = 0
    grid = [F(0), F(1, 7), F(1, 2), F(5, 6), F(1)]
    for n in range(1, 7):
        for m in range(1, 7):
            # For u=1-x: r=1-u^m, r'=1-u^n. Both are homeomorphisms.
            for x in grid:
                u = 1-x
                old, new = 1-u**m, 1-u**n
                assert (1-old)**n == (1-new)**m
                unary += 1
            if n != m:
                u, v = F(1, 2), F(1, 3)
                old = (1-(1-u**m)*(1-v**m))**n
                new = (1-(1-u**n)*(1-v**n))**m
                assert old != new
                interaction += 1
    checks['unary_equivalence'] = unary
    checks['boundary_matched_interaction_rejections'] = interaction
    a, b = F(1, 2), F(1, 3)
    hp = 1-(1-a)**2
    old = (1-a)**2 * (1-a*b)
    new = (1-hp) * (1-hp*b)
    assert (1-a)**2 == 1-hp and old != new
    checks['anchored_unary_count_change_detected'] = {'old': str(old), 'new': str(new)}


def harmless_unused_coordinate():
    counts = (2, 0, 1, 0, 0, 0, 0)  # A unary and AB, C unused.
    outcomes = [q(counts, [F(1,2), F(1,3), c], 7)
                for c in (F(0), F(1,9), F(8,9), F(1))]
    assert len(set(outcomes)) == 1
    assert all(q((0,)*7, rates, 7) == 1
               for rates in product((F(0), F(1,2), F(1)), repeat=3))
    checks['unused_and_empty_inventory'] = True


def endpoint_control():
    # A unary forces Q=0 at a=1; AB is still a finite isolated contrast if b<1.
    counts = (1, 0, 2)
    b = F(2, 5)
    assert q(counts, [F(1), b], 3) == 0
    assert q(counts, [F(1), b], 1) == 0
    expected_boundary = (1-b)**2
    assert expected_boundary > 0
    for k in range(2, 12):
        a = 1-F(1, 2**k)
        table = [q(counts, [a, b], mask) for mask in range(4)]
        isolated = isolated_factor(table, 3)
        assert isolated == (1-a*b)**2
        assert isolated > expected_boundary
    checks['raw_zero_is_not_a_log_mask_input'] = {'isolated_boundary': str(expected_boundary)}


def limit_envelope():
    # Proof in REVIEW explains b(1-p) <= log(1-p*b)/log(1-p) <= b.
    # Exact envelopes shrink also for a calibration with no finite derivative at 0:
    # r(u)=sqrt(u), u_k=4^-k, p_k=2^-k.
    rows = []
    b = F(3, 7)
    last_width = F(1)
    for k in range(1, 21):
        u, p = F(1, 4**k), F(1, 2**k)
        assert p*p == u
        lo, hi = b*(1-p), b
        width = hi-lo
        assert 0 <= lo <= hi <= 1 and width < last_width
        last_width = width
        rows.append({'k': k, 'u': str(u), 'p': str(p), 'lo': str(lo), 'hi': str(hi)})
    checks['nondifferentiable_at_zero_limit_envelope'] = {'steps': len(rows), 'last': rows[-1]}


def shared_gate_absorption():
    a, b = F(2, 5), F(3, 7)
    def no_hit(supports):
        total = F(0)
        for alive in range(4):
            weight = (a if alive & 1 else 1-a)*(b if alive & 2 else 1-b)
            if not any(s & alive == s for s in supports):
                total += weight
        return total
    one = no_hit([1])
    duplicated_and_absorbed = no_hit([1, 1, 3])
    assert one == duplicated_and_absorbed == 1-a
    independent = (1-a)**2*(1-a*b)
    assert independent != one
    checks['shared_root_gate_failure'] = {'shared': str(one), 'independent': str(independent)}


def mixture_countercontrol():
    # Half the trials have one A route; half have one B route. No AB route exists.
    a = b = F(1, 2)
    q_ab = ((1-a)+(1-b))/2
    q_a, q_b = 1-a/2, 1-b/2
    isolated = q_ab/(q_a*q_b)
    assert isolated == F(8, 9) and isolated != 1
    checks['fresh_inventory_mixture_fake_interaction'] = str(isolated)


def support_specific_map_countercontrol():
    # World 1 uses shared A calibration H_2(a), one A and one AB route.
    # World 2 keeps AB's calibrations but uses identity for two A-only routes.
    # Equality would violate anchored-unary identification if map sharing were dropped.
    tests = 0
    for a, b in product([F(0), F(1, 5), F(1, 2), F(4, 5), F(1)], repeat=2):
        common_a = 1-(1-a)**2
        left = (1-common_a)*(1-common_a*b)
        right = (1-a)**2*(1-common_a*b)
        assert left == right
        tests += 1
    checks['support_specific_calibration_failure'] = tests


def crosstalk_countercontrol():
    tests = 0
    grid = [F(i, 8) for i in range(9)]
    for a, b in product(grid, repeat=2):
        ap = a*(2-a*b)/(2-b)
        bp = b*(2-b)
        assert 0 <= ap <= 1 and 0 <= bp <= 1
        assert ap*bp == a*b*(2-a*b)
        assert 1-ap*bp == (1-a*b)**2
        tests += 1
    for b in grid:
        values = [a*(2-a*b)/(2-b) for a in grid]
        assert values[0] == 0 and values[-1] == 1
        assert all(x<y for x, y in zip(values, values[1:]))
    bvalues = [b*(2-b) for b in grid]
    assert bvalues[0] == 0 and bvalues[-1] == 1
    assert all(x<y for x,y in zip(bvalues,bvalues[1:]))
    checks['coordinate_crosstalk_count_failure'] = tests


def discontinuous_endpoint_countercontrol():
    # Binary endpoint maps preserve endpoints and are nondecreasing, but are not
    # continuous or strictly increasing. A support and an absorbed superset collide.
    grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    for x, y in product(grid, repeat=2):
        a, b = F(x >= F(1, 2)), F(y >= F(1, 2))
        assert 1-a == (1-a)**5*(1-a*b)**3
    checks['binary_nondecreasing_map_failure'] = 25


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    for fn in (masks, unary_fibres_and_interaction_rejection, harmless_unused_coordinate,
               endpoint_control, limit_envelope, shared_gate_absorption,
               mixture_countercontrol, support_specific_map_countercontrol,
               crosstalk_countercontrol, discontinuous_endpoint_countercontrol):
        fn()
    result = {'status': 'PASS', 'arithmetic': 'exact integer/Fraction only',
              'independent_of_author_code': True, 'checks': checks}
    rendered = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        destination = args.output.resolve()
        if destination.parent != HERE:
            raise ValueError('Output must stay directly inside the assigned review directory.')
        destination.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
