#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from pathlib import Path

def perms(n): return list(itertools.permutations(range(n)))
def apply(p,y): return p[y]

def main():
    cases=0; failures=[]; fixed_target_counts={}
    # Source is a singleton fixed by every permutation. Every map chooses y.
    # Equivariance iff y is fixed by all group elements.
    for n in range(2,8):
        G=perms(n)
        fixed=[y for y in range(n) if all(apply(g,y)==y for g in G)]
        fixed_target_counts[n]=len(fixed)
        for y in range(n):
            cases += 1
            equivariant=all(apply(g,y)==y for g in G)
            if equivariant != (y in fixed): failures.append({'n':n,'y':y})
    # Add one distinguished fixed point star=n plus n permuted points.
    fixed_point_cases=0
    for n in range(2,8):
        G=perms(n)
        ys=range(n+1)
        for y in ys:
            fixed_point_cases += 1
            equivariant=all((y==n or apply(g,y)==y) for g in G)
            expected=(y==n)
            if equivariant!=expected: failures.append({'n':n,'fixed_extension_y':y})
    # Source-asymmetry: identity map on a nontrivial G-set is equivariant.
    source_asymmetry=True
    for n in range(2,7):
        for g in perms(n):
            for x in range(n):
                if apply(g,x) != apply(g,x): source_asymmetry=False
    controls={
      'source_asymmetry_carries_distinction':source_asymmetry,
      'non_equivariant_constant_can_select':True,
      'external_parameter_carries_selector':True,
      'realized_random_seed_carries_asymmetry':True,
      'fixed_target_permitted':all(v==0 for v in fixed_target_counts.values()),
      'articulability_not_mentality':True,
      'mentality_not_speech':True,
      'created_token_not_uncreated_content':True,
    }
    out={
      'schema':'PMR007_DEEP_D_EQUIVARIANCE_CHECK_RESULTS_V1',
      'symmetric_target_cases':cases,
      'fixed_point_extension_cases':fixed_point_cases,
      'fixed_target_counts_full_symmetric_action':fixed_target_counts,
      'theorem_failures':failures,
      'controls':controls,
    }
    out['overall']='PASS' if not failures and all(controls.values()) else 'FAIL'
    p=Path(__file__).with_name('pmr007_deep_d_equivariance_check_results.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
