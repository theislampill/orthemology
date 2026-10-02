#!/usr/bin/env python3
"""Finite controls of stated repair algebra and its limits, not norm validation."""
from itertools import product, permutations, combinations
import json


def compose(a,b):
    """a after b"""
    return tuple(a[b[x]] for x in range(len(a)))

def fixed(a):
    return {x for x,v in enumerate(a) if x == v}

def run():
    out = {}
    # All idempotent maps of a three-element domain, repeated maps allowed.
    n = 3
    ident = tuple(range(n))
    maps = list(product(range(n), repeat=n))
    idempotents = [f for f in maps if compose(f,f)==f]
    checked = 0
    for fs in product(idempotents, repeat=3):
        if not all(compose(f,g)==compose(g,f) for f,g in combinations(fs,2)):
            continue
        results=[]
        for perm in permutations(fs):
            c=ident
            for f in perm: c=compose(f,c)
            results.append(c)
            assert all(all(y in fixed(f) for y in c) for f in fs)
        assert len(set(results))==1
        checked+=1
    out['commuting_retractions']={
        'domain_size':n, 'idempotent_maps':len(idempotents),
        'ordered_triples_checked':checked,
        'all_orderings_fix_each_repair':True,
        'semantic_claim':'Only conditional on Fix(r_i) tracking actual satisfaction and lawful realizability.'}

    # Shared endpoint exists, idempotence holds, one-pass order still matters.
    r=(0,0,2); s=(2,1,2)
    assert compose(r,r)==r and compose(s,s)==s
    assert fixed(r)&fixed(s)=={2}
    assert compose(r,s)!=compose(s,r)
    assert compose(r,s)[1]==0 and 0 not in fixed(s)
    assert compose(s,r)[1]==2
    out['idempotence_without_commutation']={
        'r':r,'s':s,'common_fixed_points':sorted(fixed(r)&fixed(s)),
        'initial':1,'r_after_s':0,'s_after_r':2,
        'claim':'Individual retractions and a common feasible endpoint do not certify arbitrary one-pass composition.'}

    # Single bearer conflict vs faithful typed accommodation.
    original=17; wrong=71
    scalar_domain={17,71}
    original_requirement={17}; erroneous_keep_requirement={71}
    assert not original_requirement & erroneous_keep_requirement
    # Two correct standards: retain original bytes, correct derived assertion.
    states=list(product((original,wrong), repeat=3))
    # q=(immutable source, transcription, claim); operations consult source.
    rt=lambda q:(q[0],q[0],q[2])
    rc=lambda q:(q[0],q[1],q[0])
    for q in states:
        assert rt(rt(q))==rt(q) and rc(rc(q))==rc(q)
        assert rt(rc(q))==rc(rt(q))
        z=rt(rc(q))
        assert z[0]==q[0] and z[1]==z[0] and z[2]==z[0]
    # Bad claim repair copying current transcription instead of source.
    rc_copy=lambda q:(q[0],q[1],q[1])
    q=(original,wrong,wrong)
    assert rt(rc_copy(q))!=(rc_copy(rt(q)))
    out['source_custody_case']={
        'initial':q, 'source_based_result':rt(rc(q)),
        'claim_first_copies_old_error':rt(rc_copy(q)),
        'transcription_first_then_copy':rc_copy(rt(q)),
        'claim':'Bearer typing and dependency matter; original bytes never change.'}

    # Numeric agreement is not equivalence of units.
    from fractions import Fraction as F
    c=F(20); ft=lambda c:F(9,5)*c+32
    c_bad=c+1; f_bad=ft(c_bad)
    assert ft(c)==68 and f_bad-F(1)!=68
    out['unit_case']={'target_C':str(c),'target_F':str(ft(c)),
        'bad_C':str(c_bad),'bad_F':str(f_bad),
        'subtract_one_from_each_F':str(f_bad-1),
        'correct_F_adjustment':str(F(9,5)),
        'claim':'Conversion-preserving physical correction differs from numeric consensus.'}

    # Pairwise overlap is insufficient for joint satisfaction.
    family=[{'a','b'},{'b','c'},{'a','c'}]
    assert all(a&b for a,b in combinations(family,2))
    assert not set.intersection(*family)
    out['pairwise_not_joint']={'sets':[sorted(s) for s in family],
        'pairwise_nonempty':True,'joint_empty':True}

    # An observation-uniform action cannot make opposite calibration changes.
    cases={'positive_bias':{'minus'},'negative_bias':{'plus'}}
    assert all(cases.values())
    assert not set.intersection(*cases.values())
    out['retained_indistinguishability_application']={
        'cases':{k:sorted(v) for k,v in cases.items()},
        'observation':'same unresolved calibration evidence',
        'individual_repair_exists':True,'uniform_repair_exists':False,
        'ancestry':'Application of retained FRLA/local-factorization obstruction; no new theorem claim.'}

    # Coverage variant: some local operations are identity, not individually repairs.
    coverage_count=0
    for f in range(0,5):
        n=2*f+1
        for bad_count in range(f+1):
            for bad in combinations(range(n), bad_count):
                bad=set(bad)
                for chosen in combinations(range(n),f+1):
                    x=0
                    for root in chosen:
                        if root not in bad: x=1
                    assert x==1
                    coverage_count+=1
    out['fail_silent_coverage']={
        'max_fault_budget':4,'scenarios_and_choices_checked':coverage_count,
        'result':'f+1 distinct Id/R roots include R and their composition is R.',
        'semantic_assumptions':['at most f inert roots','all active roots realize the same correct R',
          'corruption cannot undo repair','R idempotent','every attempt lawful'],
        'credit':'Concrete construction supplied by restoration-crosswalk lane; basic counting identity is not novel.'}
    out['scope']='Executable finite controls only; no validation of world semantics, source authority, proper function, categorical obligation, R5 defeat or metaphysical possibility.'
    return out

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
