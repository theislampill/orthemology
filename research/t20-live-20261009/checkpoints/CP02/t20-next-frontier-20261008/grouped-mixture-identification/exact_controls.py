"""Finite rational controls for the written proofs; no empirical simulation.

No generic polynomial root finder or full histogram decoder is implemented here.
The reconstruction control compares its recovered polynomial with an independently
multiplied polynomial on the hidden test nodes, then verifies exact weights.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, prod


def q(histogram):
    return prod((1 - F(1, 4**e))**n for e, n in histogram.items())


def moments(nodes, weights, order):
    return [sum(w * z**r for z, w in zip(nodes, weights))
            for r in range(order + 1)]


def signed_pair(nodes):
    c = [1 / prod(z - t for j, t in enumerate(nodes) if j != i)
         for i, z in enumerate(nodes)]
    C = sum(t for t in c if t > 0)
    assert C > 0 and sum(c) == 0
    A = [(z, t / C) for z, t in zip(nodes, c) if t > 0]
    B = [(z, -t / C) for z, t in zip(nodes, c) if t < 0]
    assert all(w > 0 for _, w in A + B)
    assert sum(w for _, w in A) == sum(w for _, w in B) == 1
    return A, B, 1 / C


def pair_moments(pair, order):
    return moments(*zip(*pair), order)


def rank(A):
    A = [list(map(F, row)) for row in A]
    r = 0
    for j in range(len(A[0])):
        pivot = next((i for i in range(r, len(A)) if A[i][j]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        a = A[r][j]
        A[r] = [v / a for v in A[r]]
        for i in range(len(A)):
            if i != r:
                a = A[i][j]
                A[i] = [x - a*y for x, y in zip(A[i], A[r])]
        r += 1
        if r == len(A):
            break
    return r


def solve(A, b):
    n = len(A)
    A = [list(map(F, row)) + [F(v)] for row, v in zip(A, b)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if A[i][j])
        A[j], A[pivot] = A[pivot], A[j]
        p = A[j][j]
        A[j] = [v / p for v in A[j]]
        for i in range(n):
            if i != j:
                a = A[i][j]
                A[i] = [x - a*y for x, y in zip(A[i], A[j])]
    return [row[-1] for row in A]


def polynomial_from_roots(nodes):
    p = [F(1)]
    for z in nodes:
        out = [F(0)] * (len(p) + 1)
        for i, a in enumerate(p):
            out[i] -= z * a
            out[i + 1] += a
        p = out
    return p


def positive_compositions(total, count):
    if count == 1:
        yield (total,)
    else:
        for first in range(1, total - count + 2):
            for tail in positive_compositions(total - first, count - 1):
                yield (first,) + tail


def run():
    # Sharpness, eligibility, strict positivity, and the next exact gap.
    for k in range(1, 9):
        nodes = [F(3, 4)**j for j in range(2*k)]
        assert nodes == [q({1: j}) for j in range(2*k)]
        A, B, gap = signed_pair(nodes)
        assert len(A) == len(B) == k
        am, bm = pair_moments(A, 2*k - 1), pair_moments(B, 2*k - 1)
        assert am[:-1] == bm[:-1] and am[-1] - bm[-1] == gap > 0
        shifted_A = [(F(3, 4)*z, w) for z, w in A]
        shifted_B = [(F(3, 4)*z, w) for z, w in B]
        assert all(z < 1 for z, _ in shifted_A + shifted_B)
        assert pair_moments(shifted_A, 2*k-2) == pair_moments(shifted_B, 2*k-2)
    print('PASS sharpness for k=1..8, positive rational weights, actual codes, nonempty shift')

    A, B, gap = signed_pair([F(3, 4)**j for j in range(4)])
    assert A == [(F(1), F(27, 175)), (F(9, 16), F(148, 175))]
    assert B == [(F(3, 4), F(111, 175)), (F(27, 64), F(64, 175))]
    assert pair_moments(A, 3) == [F(1), F(63, 100), F(27, 64), F(7803, 25600)]
    assert pair_moments(B, 3)[-1] == F(30213, 102400)
    assert gap == F(999, 102400)
    print('PASS explicit k=2 witness: shared moments 1, 63/100, 27/64; third gap 999/102400')

    for k in range(1, 9):
        A, B, gap = signed_pair([F(3, 4)**j for j in range(2*k+1)])
        assert (len(A), len(B)) == (k+1, k)
        am, bm = pair_moments(A, 2*k), pair_moments(B, 2*k)
        assert am[:-1] == bm[:-1] and am[-1] - bm[-1] == gap > 0
    print('PASS bounded-order versus unrestricted-order obstruction for k=1..8')

    nodes = [q({1: 1}), q({2: 1}), q({1: 2, 3: 1})]
    weights = [F(2, 9), F(1, 3), F(4, 9)]
    m = moments(nodes, weights, 10)
    G = [[m[i+j] for j in range(5)] for i in range(5)]
    s = rank(G)
    assert s == 3
    p = solve([[m[i+j] for j in range(s)] for i in range(s)], [-m[i+s] for i in range(s)]) + [F(1)]
    assert p == polynomial_from_roots(nodes)
    recovered_weights = solve([[z**i for z in nodes] for i in range(s)], m[:s])
    assert recovered_weights == weights
    assert moments(nodes, recovered_weights, 10) == m
    singular_at = next(r for r in range(6)
                       if rank([[m[i+j] for j in range(r+1)] for i in range(r+1)]) < r+1)
    assert singular_at == s
    squared_expectation = sum(p[i]*p[j]*m[i+j] for i in range(s+1) for j in range(s+1))
    assert squared_expectation == 0
    print('PASS unknown rank, Prony polynomial, exact weights, first singular Hankel at s=3, zero square certificate')
    print('  nodes:', ', '.join(map(str, nodes)))
    print('  annihilator ascending coefficients:', ', '.join(map(str, p)))

    # All <=3-node mixtures on six actual codes with weights in positive fifths.
    grid = [F(3, 4)**j for j in range(6)]
    seen = {}
    for size in range(1, 4):
        for support in combinations(range(6), size):
            for numerators in positive_compositions(5, size):
                w = [F(n, 5) for n in numerators]
                signature = tuple(moments([grid[j] for j in support], w, 5))
                key = (support, numerators)
                assert signature not in seen or seen[signature] == key
                seen[signature] = key
    assert len(seen) == 186
    print('PASS 186 finite <=3-component fifth-weight controls have distinct moment panels through order 5')

    # Full grouped law <-> moments <-> count law, and continuation span rank.
    R = 5
    count_law = []
    for t in range(R+1):
        direct = sum(w*z**t*(1-z)**(R-t) for z, w in zip(nodes, weights))
        expanded = sum((-1)**j * comb(R-t, j)*m[t+j] for j in range(R-t+1))
        assert direct == expanded
        count_law.append(comb(R, t)*direct)
    assert sum(count_law) == 1
    for r in range(R+1):
        factorial_moment = sum(F(prod(range(t-r+1, t+1)), prod(range(R-r+1, R+1)))*prob
                               for t, prob in enumerate(count_law) if t >= r)
        assert factorial_moment == m[r]
    for h in range(9):
        assert rank([[z**r for z in grid] for r in range(h+1)]) == min(h+1, len(grid))
    print('PASS grouped word probabilities, count factorial moments, continuation Vandermonde ranks')

    x, y = F(1, 4), F(1, 16)
    left, right = [1-x, 1-y], [(1-x)*(1-y), 1-x*y]
    ml, mr = moments(left, [F(1, 2)]*2, 2), moments(right, [F(1, 2)]*2, 2)
    assert ml[1] == mr[1] == F(27, 32)
    assert ml[2] == F(369, 512) and mr[2] == F(2997, 4096)
    assert mr[2]-ml[2] == x*y*(1-x)*(1-y) == F(45, 4096)
    assert ml[1]**2 == mr[1]**2 and ml[1]**2 != ml[2]
    assert F(3, 7)*1 + F(4, 7)*F(9, 16) == F(3, 4)
    print('PASS preceding all-profile mixture pair at actual base4 rates; fresh-resampling loss; dependent-repeat loss')

    a, b = F(3, 4), F(9, 16)
    m2 = (a*a+b*b)/2
    joint = [F(n, 512) for n in (225, 159, 63, 65)]
    assert sum(joint) == 1 and min(joint) >= 0
    assert joint[0]+joint[1] == a and joint[0]+joint[2] == b
    assert a+b-1 <= joint[0] <= min(a, b)
    averaged = [joint[0], (joint[1]+joint[2])/2, (joint[1]+joint[2])/2, joint[3]]
    mean = (a+b)/2
    assert averaged == [m2, mean-m2, mean-m2, 1-2*mean+m2]
    assert averaged == [F(n, 512) for n in (225, 111, 111, 65)]
    deficit = m2-a*b
    assert deficit == F(9, 512) and 2*deficit/(a-b)**2 == 1
    print('PASS stationary swap: independent bound is exact; dependent endpoints counterfeit whole persistent pair law')

    cycle = [F(1), F(3, 4), F(9, 16)]
    cycle_m2 = sum(z*z for z in cycle)/3
    cycle_c = sum(cycle[i]*cycle[(i+1)%3] for i in range(3))/3
    cycle_square = sum((cycle[i]-cycle[(i+1)%3])**2 for i in range(3))/3
    assert (cycle_m2, cycle_c, cycle_square) == (F(481, 768), F(37, 64), F(37, 384))
    assert cycle_square == 2*(cycle_m2-cycle_c)
    initial_m2 = F(27, 91) + F(64, 91)*b*b
    cross = (F(27, 91)+F(64, 91)*b)*a
    assert initial_m2 == cross == F(27, 52) and a*a != initial_m2
    print('PASS nonreversible directed cycle; failure without equal second marginals')

    for i in range(1, 8):
        E = 2**i
        near = a*(1-F(1, 4**E))
        delta = a-near
        d = (a*a+near*near)/2-a*near
        assert d == delta*delta/2 and 2*d/delta**2 == 1
        for r in (0, 1, 2, 5, 17):
            assert 0 <= a**r-near**r <= r*F(1, 4**E)
    print('PASS near-code swaps and moment-perturbation bounds (finite controls only)')
    print('ALL 10 CONTROL FAMILIES PASSED. These tests do not prove the arbitrary-k or oracle theorems.')


if __name__ == '__main__':
    run()
