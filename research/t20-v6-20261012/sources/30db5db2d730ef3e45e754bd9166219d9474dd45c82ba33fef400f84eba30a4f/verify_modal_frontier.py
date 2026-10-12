#!/usr/bin/env python3
"""Finite tests for the modal/metaphysical supplement.

Exhaustive finite model checks are not proofs about all metaphysically possible
worlds. Infinite and topological results have separate manuscript proofs.
"""
from __future__ import annotations
import json, itertools, time, platform
from pathlib import Path
from modal_support import *

HERE = Path(__file__).resolve().parent
OUT = HERE / 'finite_results.json'


def antichains(n):
    masks = range(1 << n)
    out = []
    for fam_bits in range(1 << (1 << n)):
        fam = tuple(a for a in masks if fam_bits >> a & 1)
        if all((a & b) != a and (a & b) != b
               for a, b in itertools.combinations(fam, 2)):
            out.append(fam)
    return out


def is_dag(edges, n):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for i, j in edges:
        reach[i][j] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] |= reach[i][k] and reach[k][j]
    cycle = any(reach[i][j] and reach[j][i] for i in range(n) for j in range(i+1,n))
    return not cycle, reach


def verify():
    results = []
    t0 = time.monotonic()

    count = 0
    horn_count = 0
    # All subsets of the nine proper, nonempty positive rules on three atoms.
    n = 3
    options = [(a, j) for j in range(n) for a in range(1, 1 << n)
               if not a >> j & 1]
    assert len(options) == 9
    for rmask in range(1 << len(options)):
        rules = tuple(options[i] for i in range(len(options)) if rmask >> i & 1)
        for seed_domain in range(1 << n):
            supp = minimal_supports(n, [i for i in range(n) if seed_domain >> i & 1], rules)
            for seed in subsets(seed_domain):
                got = closure(n, seed, rules)
                for j in range(n):
                    assert bool(got >> j & 1) == supported(supp[j], seed)
                    count += 1
            horn_count += 1
        assert closure(n, 0, rules) == 0
    results.append(dict(group='Horn support compiler', systems=horn_count,
                        pointwise_checks=count, status='PASS'))

    # Blocker equivalence and involution, including empty support conventions.
    duals = 0
    valuations = 0
    all_data = {}
    for n in range(5):
        acs = antichains(n)
        all_data[n] = acs
        for s in acs:
            b = blockers(s, n)
            assert blockers(b, n) == s
            duals += 1
            for a in range(1 << n):
                absent = ((1 << n)-1) ^ a
                assert supported(s, a) == (not any(c & absent == c for c in b))
                valuations += 1
    results.append(dict(group='Support/blocker duality', antichains=duals,
                        valuation_checks=valuations, status='PASS'))

    # Exact completion audit: direct enumeration of all compatible downsets.
    audit_count = 0
    necessity_checks = 0
    orders_checked = 0
    witness_checks = 0
    query_witness_checks = 0
    for n, acs in all_data.items():
        complexes = sorted({frozenset(b for a in family for b in subsets(a))
                            for family in acs if family}, key=lambda c: (len(c), sorted(c)))
        by_k = {}
        for k in range(n+1):
            by_skel = {}
            for c in complexes:
                sk = frozenset(a for a in c if a.bit_count() <= k)
                by_skel.setdefault(sk, []).append(c)
            by_k[k] = by_skel
        for s in acs:
            b = blockers(s, n)
            order = max((a.bit_count() for a in b), default=0)
            for c in complexes:
                max_faces = tuple(a for a in c if not any(a != d and a & d == a for d in c))
                worlds = tuple(((1 << n)-1) ^ a for a in max_faces)
                necessary = all(supported(s, a) for a in worlds)
                assert necessary == (not any(a in c for a in b))
                necessity_checks += 1
            for k, by_skel in by_k.items():
                for sk, cs in by_skel.items():
                    truthvals = {not any(a in c for a in b) for c in cs}
                    expect = ('NECESSARY_FOR_ALL_COMPLETIONS' if truthvals == {True}
                              else 'NOT_NECESSARY_FOR_ALL_COMPLETIONS' if truthvals == {False}
                              else 'UNDETERMINED')
                    assert audit(s, sk, n, k) == expect
                    lo, hi = skeleton_bounds(sk, n, k)
                    assert lo in cs and hi in cs
                    if k >= order:
                        assert expect != 'UNDETERMINED'
                    audit_count += 1
            # Sharp lower-order indistinguishable completions for every long cut.
            for h in b:
                if h == 0:
                    continue
                good = frozenset(a for a in subsets(h) if a != h)
                bad = frozenset(subsets(h))
                assert necessary_from_complex(s, good, n)
                assert not necessary_from_complex(s, bad, n)
                for k in range(h.bit_count()):
                    assert frozenset(a for a in good if a.bit_count() <= k) == frozenset(a for a in bad if a.bit_count() <= k)
                    witness_checks += 1
            orders_checked += 1
            # Membership-query lower bound. Skip constant false/true degeneracies.
            if s and 0 not in s:
                good = frozenset(a for a in range(1 << n) if not any(h & a == h for h in b))
                for h in b:
                    bad = good | {h}
                    assert all(t in bad for a in bad for t in subsets(a))
                    assert good ^ bad == {h}
                    assert necessary_from_complex(s, good, n)
                    assert not necessary_from_complex(s, bad, n)
                    query_witness_checks += 1
    results.append(dict(group='Exact modal completion audit', audits=audit_count,
                        necessity_equivalences=necessity_checks, status='PASS'))
    results.append(dict(group='Sharp modal arity/query lower bounds', support_families=orders_checked,
                        lower_arity_witnesses=witness_checks,
                        indispensable_query_witnesses=query_witness_checks, status='PASS'))

    recombination_checks = 0
    distinct_complexes = 0
    for n, acs in all_data.items():
        complexes = {frozenset(b for a in fam for b in subsets(a)) for fam in acs if fam}
        for c in complexes:
            union = 0
            for a in c:
                union |= a
            assert union_closed(c) == (c == frozenset(subsets(union)))
            distinct_complexes += 1
            if not union_closed(c):
                continue
            necessary = ((1 << n)-1) ^ union
            for s in acs:
                if necessary_from_complex(s, c, n):
                    assert supported(s, necessary)
                recombination_checks += 1
    results.append(dict(group='Finite recombination and necessary support',
                        complexes=distinct_complexes, implication_checks=recombination_checks,
                        status='PASS'))

    # Every proper collection of absences can coexist; all together cannot.
    local_count = 0
    for n in range(2, 11):
        full = (1 << n)-1
        worlds = tuple(range(1, full+1))
        c = absence_complex(worlds, n)
        assert c == frozenset(range(full))
        assert necessary_active(worlds, n) == 0
        assert all(supported(tuple(1 << i for i in range(n)), a) for a in worlds)
        local_count += len(c)
    results.append(dict(group='Arbitrary finite coabsence obstruction family', arities=list(range(2,11)),
                        faces_checked=local_count, status='PASS'))

    root_models = 0
    cone_assertions = 0
    distributions = {}
    for n in range(1,6):
        opts = [(i,j) for i in range(n) for j in range(n)
                if i != j and (n < 5 or i < j)]
        dags = 0
        for emask in range(1 << len(opts)):
            edges = [e for i,e in enumerate(opts) if emask >> i & 1]
            dag, reach = is_dag(edges, n)
            if not dag:
                continue
            dags += 1
            has_parent = {j for _,j in edges}
            for necessary in range(1 << n):
                # All n nodes are concrete and actual. World 1 retains exactly this mask.
                contingent = [i for i in range(n) if not necessary >> i & 1]
                if not all(i in has_parent for i in contingent):
                    continue
                roots = [i for i in range(n) if i not in has_parent]
                assert roots and all(necessary >> i & 1 for i in roots)
                for target in range(n):
                    assert any(reach[r][target] for r in roots if necessary >> r & 1)
                    cone_assertions += 1
                root_models += 1
        distributions[n] = dags
    results.append(dict(group='Positive actual-ancestry theorem finite instances',
                        satisfying_models=root_models, target_cone_checks=cone_assertions,
                        dags_by_order=distributions,
                        scope='all labelled digraphs through n=4; all fixed-topological-order DAGs n=5', status='PASS'))

    # Direct semantic matrices for de-dicto/de-re and essential ownership.
    modal_mats = 0
    quantifier_failures = 0
    identity_checks = 0
    for nw in range(1,4):
        for nd in range(1,5):
            for code in range(1 << (nw*nd)):
                rows = tuple((code >> (w*nd)) & ((1 << nd)-1) for w in range(nw))
                box_exists = all(rows)
                fixed = necessary_active(rows, nd)
                if box_exists and fixed == 0:
                    quantifier_failures += 1
                for g in range(nd):
                    qvals = tuple(bool(row >> g & 1) for row in rows)
                    assert (all(qvals) == bool(fixed >> g & 1))
                    identity_checks += 1
                modal_mats += 1
    results.append(dict(group='Modal quantifier and rigid-witness matrices', matrices=modal_mats,
                        countermodels_box_exists_without_exists_box=quantifier_failures,
                        rigid_witness_checks=identity_checks, status='PASS'))

    # All-proper-subset cohosting has no one global common bearer.
    cohost_count = 0
    for n in range(2,13):
        roles = set(range(n))
        holders = [roles - {i} for i in range(n)]
        assert not any(roles <= b for b in holders)
        for mask in range((1 << n)-1):
            need = {j for j in roles if mask >> j & 1}
            assert any(need <= b for b in holders)
            cohost_count += 1
    results.append(dict(group='Common-bearer high-order obstruction', arities=list(range(2,13)),
                        proper_role_sets=cohost_count, status='PASS'))

    # Omniscience can be a stable factive *relation* with contingent contents.
    truths = ((True, False), (False, True))
    knowledge = truths
    assert all((not knowledge[w][p]) or truths[w][p] for w in range(2) for p in range(2))
    assert all((not truths[w][p]) or knowledge[w][p] for w in range(2) for p in range(2))
    assert not all(knowledge[w][0] for w in range(2))
    collapse_checks = 0
    for e in itertools.product((False,True), repeat=2):
        for p in itertools.product((False,True), repeat=2):
            if all(e) and all(not e[w] or p[w] for w in range(2)):
                assert all(p)
            collapse_checks += 1
    results.append(dict(group='Modal collapse and noncollapse controls',
                        valuation_checks=collapse_checks, contingent_omniscience_model=True, status='PASS'))

    # Simultaneously certain fulfilment of all choices iff compatible profiles are diagonal.
    joint_checks = 0
    for n in range(2,5):
        for m in range(2,5):
            for profile in itertools.product(range(m), repeat=n):
                possible = any(all(y == a for a in profile) for y in range(m))
                assert possible == (len(set(profile)) == 1)
                joint_checks += 1
    results.append(dict(group='Joint unrestricted-will compatibility', profiles=joint_checks, status='PASS'))

    # Formal model of all-world local predicates with rotating concrete carriers.
    local_pred_checks = 0
    for nw in range(2,6):
        for nx in range(1,6):
            domain = tuple((w,x) for w in range(nw) for x in range(nx))
            exists = lambda w,d: d[0] == w
            assert all(any(exists(w,d) for d in domain) for w in range(nw))
            assert not any(all(exists(w,d) for w in range(nw)) for d in domain)
            for w in range(nw):
                actual = [d for d in domain if exists(w,d)]
                assert [d[1] for d in actual] == list(range(nx))
                local_pred_checks += 1
    results.append(dict(group='Worldwise conservative-lift instances', local_isomorphism_checks=local_pred_checks,
                        scope='finite illustrations of the separately proved general construction', status='PASS'))

    # Threshold family demonstrates independent arity and query count.
    from math import comb
    threshold_rows = []
    for n in range(1,9):
        for r in range(1,n+1):
            supports = tuple(a for a in range(1 << n) if a.bit_count() == r)
            b = blockers(supports,n)
            assert len(b) == comb(n,n-r+1)
            assert all(a.bit_count() == n-r+1 for a in b)
            threshold_rows.append(dict(n=n, required_active=r,
                                       cut_arity=n-r+1, oracle_queries=len(b)))
    results.append(dict(group='Threshold support arity and query formulas', cases=len(threshold_rows), status='PASS'))

    data = dict(status='PASS', groups=results, python=platform.python_version(),
                elapsed_seconds=round(time.monotonic()-t0,3),
                limits=['Finite exact checks, not a proof of metaphysical premises.',
                        'No independent audit or Lean kernel verification.',
                        'Infinite descent, compactness, and general lifting use paper proofs.'])
    OUT.write_text(json.dumps(data,indent=2)+'\n')
    (HERE/'threshold_profiles.json').write_text(json.dumps(threshold_rows,indent=2)+'\n')
    print(json.dumps(data, indent=2))

if __name__ == '__main__':
    verify()
