#!/usr/bin/env python3
"""Independent finite calculations; no imports from author implementation."""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check():
    points = list(itertools.product(range(3), repeat=2))
    add = lambda x, y: tuple(a + b for a, b in zip(x, y))
    q = (2, 2)
    fixed = [(a, b) for a in points for b in points if add(a, b) == q]
    indispensable = [(a, b) for a, b in fixed if a != q and b != q]
    both_solo = [(a, b) for a, b in fixed if a == q and b == q]
    assert (len(fixed), len(indispensable), len(both_solo)) == (9, 7, 0)
    assert add((1, 1), (1, 1)) == q and add((1, 1), (0, 0)) != q
    # Reveals why ordinary profile union is not joint productive concentration.
    joint_range = {add(a, b) for a in points for b in points}
    assert len(joint_range) == 25 and (4, 4) not in points
    assert set(points) | set(points) == set(points)
    assert all(add(t, (0, 0)) == t for t in joint_range)

    productive = []
    jointly_relevant = []
    fixed_solo_and_indispensable = []
    both_control_all = []
    for mask in range(16):
        f = lambda a, b: (mask >> (2*a+b)) & 1
        vals = [f(0,0),f(0,1),f(1,0),f(1,1)]
        mono = all(f(a,b) <= f(c,d) for a,b,c,d in itertools.product((0,1), repeat=4) if a <= c and b <= d)
        prod = mono and f(0,0) == 0 and f(1,1) == 1
        ra = any(f(0,b) != f(1,b) for b in (0,1))
        rb = any(f(a,0) != f(a,1) for a in (0,1))
        if prod: productive.append(vals)
        if prod and ra and rb: jointly_relevant.append(vals)
        if f(1,1) and f(1,0) and f(0,1) and not f(1,0) and not f(0,1):
            fixed_solo_and_indispensable.append(vals)
        ca = all(any(all(f(a,b) == out for b in (0,1)) for a in (0,1)) for out in (0,1))
        cb = all(any(all(f(a,b) == out for a in (0,1)) for b in (0,1)) for out in (0,1))
        if ca and cb: both_control_all.append(vals)
    assert len(productive) == 4
    assert sorted(jointly_relevant) == [[0,0,0,1],[0,1,1,1]]
    assert not fixed_solo_and_indispensable and not both_control_all

    # Independent actual controls distinguish causes that are relevant somewhere
    # from contributions indispensable in the actual saturated configuration.
    OR = lambda a,b: max(a,b)
    AND = lambda a,b: min(a,b)
    assert AND(1,1) == 1 and AND(1,0) == AND(0,1) == 0
    assert OR(1,1) == OR(1,0) == OR(0,1) == 1
    assert OR(0,0) == 0 and OR(1,0) != OR(0,0)
    assert all(OR(t,t) == t for t in (0,1))
    assert not any(all(OR(a,b) == 0 for b in (0,1)) for a in (0,1))

    bool_vectors = list(itertools.product((0,1), repeat=2))
    def determine(preferred):
        scores = {v: -sum(abs(x-y) for x,y in zip(v,preferred)) for v in bool_vectors}
        maximizers = [v for v, score in scores.items() if score == max(scores.values())]
        assert len(maximizers) == 1
        return maximizers[0]
    concord_rows = [(p,determine(p),determine(p)) for p in bool_vectors]
    assert all(p == a == b for p,a,b in concord_rows)
    mismatch = (determine((0,0)), determine((1,1)))
    assert mismatch[0] != mismatch[1]
    assert tuple(map(max, zip(*mismatch))) != mismatch[0]

    cnd = lambda relation: all(not ((0,c) in relation and (1,c) in relation) for c in range(4))
    entire = lambda g, relation: all((g,c) in relation for c in range(4))
    refs = list(itertools.product((0,1), range(4)))
    accepted = covered = rejected = 0
    for mask in range(256):
        r = {entry for i,entry in enumerate(refs) if (mask >> i) & 1}
        accepted += cnd(r)
        rejected += not cnd(r)
        covered += cnd(r) and all((0,c) in r or (1,c) in r for c in range(4))
        assert not (cnd(r) and entire(0,r) and entire(1,r))
    assert (accepted, covered, rejected) == (81,16,175)
    one_owner = {(0,c) for c in range(4)}
    split = {(0,0),(0,1),(1,2),(1,3)}
    duplicate = split | {(1,0)}
    assert cnd(one_owner) and entire(0,one_owner) and not entire(1,one_owner)
    assert cnd(split) and not entire(0,split) and not entire(1,split)
    assert not cnd(duplicate)
    return {
      'status':'PASS', 'scope':'Independent finite arithmetic, truth tables, ownership relations, and adverse controls. No full metaphysical model claim.',
      'additive':{'joint_profiles':81,'fixed_target_profiles':9,'both_indispensable':7,'both_solo':0},
      'B5_union_control':{'single_command_range':9,'joint_sum_range':25,'union_is_joint_range':False,'explicit_missing_bounded_solo_target':[4,4],'unbounded_solo_command_for_any_sum':'the sum itself'},
      'boolean':{'tables':16,'monotone_nonspontaneous_actual':4,'both_relevant_productive':jointly_relevant,'both_rectangular_full_control':0},
      'ownership':{'relations':256,'cnd':accepted,'cnd_and_covered':covered,'rejected':rejected,'nonvacuous_entire_positive':True,'duplicate_negative':True},
      'controls':{'changed_effort_changes_act':True,'AND_indispensable':True,'OR_redundant_actual_but_relevant':True,'concord_all_targets_without_rectangular_control':True},
      'intrinsic_policy':{'unique_maximizers_for_four_targets':True,'different_intrinsic_preferences_break_concord':True,'independently_warranted_shared_preferences':False,'epistemic_or_foreknowledge_semantics':'NOT_REPRESENTED'}
    }

if __name__ == '__main__':
    result = check()
    (ROOT / 'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
