#!/usr/bin/env python3
"""Exact checks of the v2 bridge and the normalisation-bearing linear-record form.

General results rest on the manuscript's proofs. Finite checks are not a proof
assistant, independent peer review, historical-priority search or physical test.
Python 3.10+, SymPy. No network access or input-file writes.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import sympy as sp


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def partitions(n: int):
    """Canonical labels for all partitions of n states."""
    def visit(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for x in range(max(prefix, default=-1) + 2):
                yield from visit(prefix + [x])
    yield from visit([])


def congruence_checks():
    checked = positive = 0
    by_size = []
    for n in range(1, 5):
        local = 0
        for ell in partitions(n):
            zcount = max(ell) + 1
            L = sp.Matrix([[int(ell[w] == z) for w in range(n)] for z in range(zcount)])
            basis = L.nullspace()
            for a in it.product(range(n), repeat=n):
                direct = all(ell[i] != ell[j] or ell[a[i]] == ell[a[j]]
                             for i in range(n) for j in range(n))
                quotient = {}
                factorable = True
                for w in range(n):
                    z, out = ell[w], ell[a[w]]
                    if z in quotient and quotient[z] != out:
                        factorable = False
                    quotient[z] = out
                La = sp.Matrix([[int(ell[a[w]] == z) for w in range(n)] for z in range(zcount)])
                linear = all(La * d == sp.zeros(zcount, 1) for d in basis)
                require(direct == factorable == linear, 'Congruence/factorisation/kernel mismatch')
                if direct:
                    Q = sp.Matrix([[int(quotient[z] == zz) for z in range(zcount)]
                                   for zz in range(zcount)])
                    require(Q * L == La, 'Quotient action does not reproduce observed action')
                checked += 1
                local += 1
                positive += int(direct)
        by_size.append({'states': n, 'action_partition_cases': local})
    return {'status': 'PASS', 'cases': checked, 'congruent_cases': positive,
            'domains': by_size, 'arithmetic': 'exact integers and rational nullspaces'}


def vertices(A, m):
    """Enumerate nonnegative vertices via linearly independent support columns.

This does not use the feasible-support kernel formula being tested.
"""
    n = A.cols
    found = set()
    for k in range(1, min(n, A.rank()) + 1):
        for support in it.combinations(range(n), k):
            C = A[:, list(support)]
            if C.rank() != k:
                continue
            try:
                sol, params = C.gauss_jordan_solve(m)
            except ValueError:
                continue
            if params.rows or any(x < 0 for x in sol):
                continue
            mu = [sp.Rational(0)] * n
            for j, x in zip(support, sol):
                mu[j] = x
            if sum(mu) == 1:
                found.add(tuple(mu))
    return [sp.Matrix(x) for x in sorted(found)]


def linear_records():
    F = sp.Rational
    cases = [
        ('weighted_mean_interior', [[1,1,1,1],[0,1,2,3]], [1,F(3,2)]),
        ('weighted_mean_face', [[1,1,1,1],[0,1,2,3]], [1,0]),
        ('weighted_mean_one', [[1,1,1,1],[0,1,2,3]], [1,1]),
        ('three_point_mean', [[1,1,1],[0,1,2]], [1,1]),
        ('observation_two_fibres', [[1,1,0,0],[0,0,1,1]], [F(1,2),F(1,2)]),
        ('observation_boundary', [[1,1,0,0],[0,0,1,1]], [1,0]),
        ('binary_marginals', [[1,1,1,1],[1,1,0,0],[0,1,0,1]], [1,F(1,2),F(1,2)]),
        ('exact_distribution', sp.eye(3).tolist(), [F(1,3)]*3),
        ('mass_in_row_span', [[2,2,0],[0,0,2]], [1,1]),
        ('mass_only', [[2,2,2]], [2]),
    ]
    details = []
    comparisons = 0
    for name, aa, mm in cases:
        A, m = sp.Matrix(aa), sp.Matrix(mm)
        n = A.cols
        require(all(sum(d) == 0 for d in A.nullspace()), 'Missing normalisation premise')
        vs = vertices(A, m)
        require(bool(vs), 'Unexpected empty polytope')
        support = [j for j in range(n) if any(v[j] > 0 for v in vs)]
        differences = sp.Matrix.hstack(*(v-vs[0] for v in vs[1:])) if len(vs)>1 else sp.zeros(n,0)
        active = A[:, support].nullspace()
        lifted = []
        for d in active:
            z = sp.zeros(n,1)
            for j, value in zip(support,d):
                z[j] = value
            lifted.append(z)
        predicted = sp.Matrix.hstack(*lifted) if lifted else sp.zeros(n,0)
        require(differences.rank() == predicted.rank() == differences.row_join(predicted).rank(),
                'Feasible-difference span differs from restricted kernel')
        count = 0
        for outputs in it.product((0,1), repeat=n):
            T = sp.Matrix([[int(outputs[j] == y) for j in range(n)] for y in (0,1)])
            equal_outputs = all(T*v == T*vs[0] for v in vs)
            annihilates = T*predicted == sp.zeros(2,predicted.cols)
            require(equal_outputs == annihilates, 'Output constancy criterion fails')
            count += 1
        comparisons += count
        details.append({'name':name,'vertices':len(vs),'feasible_support':support,
                        'difference_dimension':differences.rank(),'binary_channels':count})
    # Dropping the mass premise makes the unrestricted-kernel shortcut wrong.
    A0 = sp.zeros(1,2)
    reset = sp.Matrix([[1,1]])
    require(reset*sp.Matrix([1,-1]) == sp.zeros(1,1), 'Reset must erase feasible differences')
    require(reset*sp.Matrix([1,0]) != sp.zeros(1,1), 'Missing-premise counterexample vanished')
    require(A0*sp.Matrix([1,0]) == sp.zeros(1,1), 'Counterexample not in raw kernel')
    return {'status':'PASS','families':details,'channel_comparisons':comparisons,
            'negative_control':'Omitting the zero-total-mass kernel premise admits a spurious direction',
            'arithmetic':'exact rational vertex enumeration, rank and matrix equality'}


def composition_reconnection():
    joint_cases = 0
    for n in range(2,9):
        xs = list(it.product((0,1),repeat=n))
        Ks = [set(x for x in xs if sum(x)%2 == b) for b in (0,1)]
        for size in range(1,n):
            for scope in it.combinations(range(n),size):
                records = [{tuple(x[i] for i in scope) for x in K} for K in Ks]
                require(records[0] == records[1] == set(it.product((0,1),repeat=size)),
                        'Local records do not agree for the two composition hypotheses')
        for b in (0,1):
            for x in Ks[b]:
                require(sum(x)%2 == b, 'Connected global observation is not deterministic on K_b')
                joint_cases += 1
    ell = lambda w:(w[0],w[0]*w[1])
    reconnect = lambda w:(1,w[1])
    require(ell((0,0)) == ell((0,1)), 'Initial observations differ')
    require(ell(reconnect((0,0))) != ell(reconnect((0,1))), 'Reconnection fails to separate')
    require({ell(reconnect((0,b)))[1] for b in (0,1)} == {0,1}, 'Rank-one decision unavailable')
    # A sample is not a guarantee when the two-hypothesis restriction is removed.
    K0 = {(0,0,0),(0,1,1),(1,0,1),(1,1,0)}
    allx = set(it.product((0,1),repeat=3))
    require((0,0,0) in K0 & allx and K0 <= K0 and not allx <= K0,
            'Unrestricted-relation counterexample missing')
    # Original labels must survive merging of current states.
    actions = [(3,4,4,3,4),(4,3,4,3,4)]
    labels = {0:0,1:0,2:1}
    obs = ('?','?','?',1,0)
    for i,j in it.combinations(range(3),2):
        require(any(obs[a[i]]!=obs[a[j]] for a in actions), 'A pair is not distinguishable')
    for a in actions:
        merged = {(a[w],labels[w]) for w in range(3) if obs[a[w]]==0}
        require(merged=={(4,0),(4,1)}, 'Initial opposite labels not retained')
        require(all(act[4]==4 for act in actions), 'Merge not irreversible')
    return {'status':'PASS','parity_dimensions':list(range(2,9)),
            'joint_configurations_checked':joint_cases,'reconnection_rank':1,
            'counterexamples':['One joint sample does not establish an unrestricted invariant',
                               'Five states, three initial: either first action destroys a needed distinction'],
            'limit':'Conditional finite model; not verification of real sensors or exhaustive external hypotheses'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result={'schema':'information-composition-self-revision-v2-checks','status':'PASS',
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'quotient_bridge':congruence_checks(),
            'general_linear_record':linear_records(),
            'common_composition_instance':composition_reconnection(),
            'scope':'Declared exact finite cases only; written general proofs remain authoritative.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],
                      'quotient_cases':result['quotient_bridge']['cases'],
                      'record_families':len(result['general_linear_record']['families']),
                      'channel_comparisons':result['general_linear_record']['channel_comparisons'],
                      'output':str(args.output)},indent=2))

if __name__=='__main__':
    main()
