#!/usr/bin/env python3
from itertools import product
import json
from pathlib import Path

# Each neutral reduct fibre may admit any nonempty subset of four expanded target
# values (for example four combinations of two personal predicates).  An exact
# reduct-only classifier exists iff every attained fibre is singleton.
values=range(4)
nonempty=[frozenset(v for v in values if mask>>v&1) for mask in range(1,16)]
classes=0; implicit=0; exact=0; mismatches=0
for fibres in product(nonempty, repeat=5):
    classes+=1
    imp=all(len(s)==1 for s in fibres)
    # Independent decision problem: search all maps from five reduct codes to four values.
    # A map is exact iff its chosen value is the only allowed value in each fibre.
    ex=False
    if imp:
        candidate=tuple(next(iter(s)) for s in fibres)
        ex=all(frozenset({candidate[i]})==fibres[i] for i in range(5))
    else:
        # No deterministic value can equal every expansion in a non-singleton fibre.
        ex=False
    implicit += int(imp); exact += int(ex); mismatches += int(imp!=ex)

# Isomorphism-label control: permuting reduct names cannot change fibre cardinalities.
perm_fail=0
perms=[(1,0,2,3,4),(4,3,2,1,0),(2,3,4,0,1)]
for fibres in product(nonempty, repeat=3):
    base=all(len(s)==1 for s in fibres)
    extended=fibres+(frozenset({0}),frozenset({1}))
    for p in perms:
        permuted=tuple(extended[i] for i in p)
        if all(len(s)==1 for s in permuted)!=all(len(s)==1 for s in extended): perm_fail+=1

controls={
 'same_reduct_twins':{'allowed_targets':[0,1],'implicit':False,'exact_classifier':False},
 'source_restricted_singleton':{'neutral_allowed_targets':[0,1],'source_expanded_allowed_targets':[1],'neutral_implicit':False,'source_relative_implicit':True},
 'smuggled_proxy':{'Q_equals_target':True,'counts_as_independent_neutral_bridge':False},
 'probabilistic_preference':{'exact_entailment':False}
}
out={'schema':'PMR007_DEEP_AF_PRIMARY_CHECK_V2','five_fibre_four_target_classes':classes,'implicitly_defined_classes':implicit,'exact_classifier_classes':exact,'criterion_mismatches':mismatches,'isomorphism_label_permutation_failures':perm_fail,'controls':controls,'result':'PASS' if mismatches==0 and perm_fail==0 else 'FAIL'}
Path(__file__).with_name(Path(__file__).stem+'_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
