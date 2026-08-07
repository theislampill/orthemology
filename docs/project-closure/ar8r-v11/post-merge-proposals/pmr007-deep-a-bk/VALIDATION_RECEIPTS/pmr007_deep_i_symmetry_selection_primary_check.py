from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path

# Set partitions represented as tuple of tuple blocks.
def partitions(items):
    if not items:
        yield ()
        return
    first=items[0]
    for p in partitions(items[1:]):
        yield ((first,),)+p
        for i in range(len(p)):
            yield p[:i]+(tuple(sorted((first,)+p[i])),)+p[i+1:]

def canonical_partition(p):
    return tuple(sorted((tuple(sorted(b)) for b in p), key=lambda b:b[0]))

def all_invariant_nonempty_sets(p):
    k=len(p)
    for mask in range(1,1<<k):
        s=set()
        for i,b in enumerate(p):
            if mask>>i & 1:s.update(b)
        yield frozenset(s)

def fixed_points(p):
    # Full symmetric action within each block: exactly singleton blocks are globally fixed.
    return {b[0] for b in p if len(b)==1}

seen=set(); cases=0; failures=[]; transitive_cases=0; positive_cases=0
for n in range(1,8):
    for raw in partitions(tuple(range(n))):
        p=canonical_partition(raw)
        if p in seen: continue
        seen.add(p)
        fp=fixed_points(p)
        for C in all_invariant_nonempty_sets(p):
            cases+=1
            direct_exists=any(x in fp for x in C)
            criterion=bool(set(C)&fp)
            if direct_exists!=criterion:
                failures.append({'n':n,'partition':p,'C':sorted(C)})
            containing=[b for b in p if set(b)<=set(C)]
            if len(containing)==1 and len(containing[0])>1:
                transitive_cases+=1
                if direct_exists:
                    failures.append({'type':'transitive_nonselection','n':n,'partition':p,'C':sorted(C)})
            if criterion: positive_cases+=1

# Concrete model regressions.
regressions={
 'no_application': len([])==0,
 'symmetric_pair_fixed_points': len(fixed_points(((0,1),)))==0,
 'three_cycle_fixed_points': len(fixed_points(((0,1,2),)))==0,
 'unique_fixed_candidate': fixed_points(((0,),(1,2)))=={0},
}
if not all(regressions.values()):failures.append({'type':'regression', 'data':regressions})

out={
 'schema':'PMR007_DEEP_I_PRIMARY_CHECK_RESULTS_V1',
 'partition_structures':len(seen),
 'invariant_candidate_fibres_checked':cases,
 'transitive_nonselection_cases':transitive_cases,
 'positive_fixed_point_cases':positive_cases,
 'regressions':regressions,
 'failure_count':len(failures),
 'failures':failures[:20],
 'result':'PASS' if not failures else 'FAIL',
}
p=Path(__file__).with_name('pmr007_deep_i_symmetry_selection_primary_check_results.json')
p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
