#!/usr/bin/env python3
"""Exact finite controls for RESULT.md; mathematical models, not metaphysical evidence."""
from itertools import product
from fractions import Fraction
from pathlib import Path
import hashlib
import importlib.util
import importlib.machinery
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CAT = ROOT / 't20-consolidation-20261011/catalogue/objects'
ENGINE_HASH = '6b06c7cec417a961052971d605b54570c34e44d3e0f0ddfc1a2021e384038268'


def subsets(seq):
    return [frozenset(x for i, x in enumerate(seq) if mask >> i & 1)
            for mask in range(1 << len(seq))]


def exact(L, R):
    return frozenset((x,y) for x,m in L for n,y in R if m == n)


def summary(L, R, q):
    return frozenset((x,y) for x,m in L for n,y in R if q[m] == q[n])


def lifts(L, R, q):
    return all(any((x,k) in L and (k,y) in R for _,k in L)
               for x,m in L for n,y in R if q[m] == q[n])


def profile(R, m):
    return frozenset(y for n,y in R if n == m)


def profile_constant(R, M, q):
    return all(q[m] != q[n] or profile(R,m) == profile(R,n)
               for m in M for n in M)


def rank(matrix):
    a = [list(map(Fraction,row)) for row in matrix]
    piv = 0
    for col in range(len(a[0])):
        selected = next((i for i in range(piv,len(a)) if a[i][col]),None)
        if selected is None:
            continue
        a[piv],a[selected] = a[selected],a[piv]
        denominator = a[piv][col]
        a[piv] = [v/denominator for v in a[piv]]
        for i in range(len(a)):
            if i != piv:
                factor = a[i][col]
                a[i] = [v-factor*w for v,w in zip(a[i],a[piv])]
        piv += 1
        if piv == len(a):
            break
    return piv


def engine_control():
    path = CAT / ENGINE_HASH[:2] / ENGINE_HASH
    assert hashlib.sha256(path.read_bytes()).hexdigest() == ENGINE_HASH
    name = 'grounding_provenance_inherited_engine'
    loader = importlib.machinery.SourceFileLoader(name,str(path))
    spec = importlib.util.spec_from_loader(name,loader)
    engine = importlib.util.module_from_spec(spec)
    sys.modules[name] = engine
    loader.exec_module(engine)
    ms = [engine.Event(f'm{i}','actual-intermediary') for i in range(2)]
    es = [engine.Event(f'e{i}','actual-product') for i in range(2)]
    rules = tuple(engine.rule(f'A-m{i}','A',output=ms[i]) for i in range(2)) + tuple(
        engine.rule(f'm{i}-e{i}',(),inputs=[ms[i].key],output=es[i]) for i in range(2))
    run = engine.run(rules,'A')
    byname = {r.name:r for r in rules}
    L = frozenset((p.rule,m.key) for m in ms for p in run.proofs[m.key])
    R = frozenset((m,e.key) for e in es for p in run.proofs[e.key]
                  for m in byname[p.rule].event_inputs)
    q = {m.key:run.productive_roots(m.key) for m in ms}
    assert all(v == frozenset('A') for v in q.values())
    c,cq = exact(L,R),summary(L,R,q)
    assert c == frozenset([('A-m0','e0'),('A-m1','e1')])
    assert cq-c == frozenset([('A-m0','e1'),('A-m1','e0')])
    return {'source_sha256':ENGINE_HASH,'actual_events':sorted(run.events),
            'issued_bearers':[a.bearer for a in run.issued],
            'original_root_answers':{k:sorted(run.productive_roots(k)) for k in sorted(run.events)},
            'actual_upstream_fragments':sorted(L),'actual_downstream_uses':sorted(R),
            'genuine_endpoint_composition':sorted(c),'spurious_after_provider_summary':sorted(cq-c),
            'engine_modified':False,
            'scope':'New finite two-channel interpretation in unchanged engine; not a metaphysical premise proof.'}


def main():
    X,Y,M = range(2),range(2),range(3)
    ls,rs = subsets(list(product(X,M))),subsets(list(product(M,Y)))
    qs = [dict(zip(M,z)) for z in product(range(3),repeat=3)]
    counts = {'fixed_composition_cases':0,'universal_upstream_cases':0,
              'witness_pair_cases':0,'constant_summary_cases':0}
    for R in rs:
        for q in qs:
            all_exact = True
            for L in ls:
                c,cq = exact(L,R),summary(L,R,q)
                assert c <= cq
                assert (c == cq) == lifts(L,R,q)
                all_exact &= c == cq
                counts['fixed_composition_cases'] += 1
                active_left = {m for _,m in L}
                active_right = {n for n,_ in R}
                key_sound = all(q[m] != q[n] or m == n
                                for m in active_left for n in active_right)
                actual_witness_pairs = {(x,m,n,y) for x,m in L for n,y in R if m == n}
                quotient_witness_pairs = {(x,m,n,y) for x,m in L for n,y in R if q[m] == q[n]}
                assert key_sound == (actual_witness_pairs == quotient_witness_pairs)
                counts['witness_pair_cases'] += 1
                if len(set(q.values())) == 1:
                    assert cq == frozenset(product({x for x,_ in L},{y for _,y in R}))
                    counts['constant_summary_cases'] += 1
            assert all_exact == profile_constant(R,M,q)
            counts['universal_upstream_cases'] += 1

    # The weakest fixed-L,R endpoint condition need not preserve specific witnesses.
    L = frozenset([('x',0)])
    R = frozenset([(0,'y'),(1,'y')])
    q = {0:'g',1:'g'}
    assert exact(L,R) == summary(L,R,q)
    assert 0 != 1 and q[0] == q[1]
    endpoint_vs_witness = {'endpoint_composition_exact':True,
        'specific_left_middle':0,'specific_right_middle':1,
        'same_provider':True,'specific_witnesses_compose':False}

    # Fixed-case exactness does not require neighbourhood constancy.
    L = frozenset([('x',0),('x',1)])
    R = frozenset([(0,'y')])
    assert exact(L,R) == summary(L,R,q)
    assert not profile_constant(R,[0,1],q)

    # Fixed family of continuations: combined profile is the coarsest safe refinement.
    sidecars=[]
    for R in rs:
        profiles = {m:profile(R,m) for m in M}
        distinct = set(profiles.values())
        assert profile_constant(R,M,profiles)
        for q0 in qs:
            if profile_constant(R,M,q0):
                assert len(set(q0.values())) >= len(distinct)
        sidecars.append(len(distinct))

    rank_rows=[]
    for n in range(1,21):
        ident = [[int(i == j) for j in range(n)] for i in range(n)]
        ones = [[1]*n for _ in range(n)]
        assert rank(ident) == n and rank(ones) == 1
        rank_rows.append({'intermediaries':n,'original_provider_count':1,
                          'exact_linear_rank':n,'collapsed_linear_rank':1,
                          'distinct_continuation_profiles':n,'spurious_routes':n*(n-1)})
    # Exhaustively confirm diagonal rectangles contain at most one diagonal point.
    rectangle_cases = 0
    for n in range(1,7):
        for A in subsets(list(range(n))):
            for B in subsets(list(range(n))):
                rectangle = set(product(A,B))
                if all(i == j for i,j in rectangle):
                    assert len(rectangle) <= 1
                rectangle_cases += 1

    out = {'status':'PASS','enumeration_dimensions':{'X':2,'M':3,'Y':2,'summary_labels':3},
           'counts':counts,'endpoint_vs_witness_control':endpoint_vs_witness,
           'fixed_case_weaker_than_uniform_control':True,
           'minimal_profile_sidecar_cases':len(sidecars),'rank_controls':rank_rows,
           'diagonal_rectangle_checks':rectangle_cases,'inherited_engine_control':engine_control(),
           'verification_scope':'Exact finite Python controls; written general proofs; no fresh Lean run or independent review.'}
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'counts':counts,'rank_cases':len(rank_rows),
                      'rectangle_cases':rectangle_cases,'engine_control':'PASS'},indent=2))


if __name__ == '__main__':
    main()
