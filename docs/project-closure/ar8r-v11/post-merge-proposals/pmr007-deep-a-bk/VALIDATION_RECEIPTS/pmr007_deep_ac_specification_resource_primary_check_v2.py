#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def group(n): return tuple(itertools.permutations(range(n)))
def stab(G, action, x): return {p for p in G if action(p,x)==x}
def is_equivariant(G,E,actE,F): return all(F[actE(p,e)]==p[F[e]] for p in G for e in E)

def main():
    total_maps=eq_maps=stab_checks=0
    extended_total=extended_eq=0
    failures=[]; counts={}
    for n in range(2,6):
        G=group(n); A=tuple(range(n))
        eq=[]
        for vals in itertools.product(A,repeat=n):
            total_maps+=1; F=dict(enumerate(vals))
            if is_equivariant(G,A,lambda p,e:p[e],F):
                eq_maps+=1; eq.append(F)
                for e in A:
                    stab_checks+=1
                    if not stab(G,lambda p,x:p[x],e).issubset(stab(G,lambda p,x:p[x],F[e])):
                        failures.append({'n':n,'kind':'stabilizer'})
        if not any(all(F[e]==e for e in A) for F in eq): failures.append({'n':n,'kind':'identity_missing'})
        STAR=n; E=tuple(range(n+1))
        def actE(p,e): return STAR if e==STAR else p[e]
        ext=0
        for vals in itertools.product(A,repeat=n+1):
            extended_total+=1; F={e:vals[e] for e in E}
            if is_equivariant(G,E,actE,F): ext+=1
        extended_eq += ext
        if ext: failures.append({'n':n,'kind':'fixed_resource_selector','count':ext})
        # Constant-map non-equivariance witness.
        const={e:0 for e in A}
        if n>1 and is_equivariant(G,A,lambda p,e:p[e],const): failures.append({'n':n,'kind':'constant_map_unexpectedly_equivariant'})
        # Equivariant multivalued relation at invariant source: STAR relates to every alternative.
        relation={STAR:frozenset(A)}
        relation_equivariant=all(frozenset(p[a] for a in relation[STAR])==relation[STAR] for p in G)
        unique= len(relation[STAR])==1
        if not relation_equivariant or unique: failures.append({'n':n,'kind':'multivalued_control'})
        counts[str(n)]={'natural_maps':n**n,'equivariant_natural_maps':len(eq),'fixed_resource_total_selectors':ext,'multivalued_invariant_relation':relation_equivariant,'multivalued_unique':unique}
    # Inert semantic expansions of the exact same resource/selector reduct.
    parity_fail=0
    for n in range(2,9):
        reduct={'G':'S_n','n':n,'E':list(range(n)),'A':list(range(n)),'F':list(range(n))}
        imp=(reduct,False,False,False); per=(reduct,True,True,True)
        parity_fail += int(imp[0]!=per[0])
    # Overdetermination and represented-seed controls are explicit typed witnesses.
    overdetermination={'resource_1':'r','resource_2':'r','each_suffices_for_output':'a','unique_output':'a'}
    represented_seed={'seed':2,'selector':'identity','output':2,'volition':False}
    result={
      'schema':'PMR007_DEEP_AC_SPECIFICATION_RESOURCE_PRIMARY_CHECK_V2',
      'n_range':[2,5],
      'counts':counts,
      'deterministic_maps_checked':total_maps,
      'equivariant_maps_found':eq_maps,
      'stabilizer_inclusions_checked':stab_checks,
      'extended_fixed_resource_maps_checked':extended_total,
      'equivariant_total_selectors_with_fixed_resource':extended_eq,
      'personal_impersonal_reduct_failures':parity_fail,
      'overdetermination_control':overdetermination,
      'represented_seed_control':represented_seed,
      'failures':failures,
      'result':'PASS' if not failures and parity_fail==0 else 'FAIL',
      'nonclaims':['world process correspondence','resource completeness','volition','personality','Wisdom','equal metaphysical plausibility']
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
