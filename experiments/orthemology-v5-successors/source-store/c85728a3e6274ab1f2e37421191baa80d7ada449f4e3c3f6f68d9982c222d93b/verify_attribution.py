#!/usr/bin/env python3
"""Finite verification of the one-unknown-class robust lifting.

Uses explicit actual-root images, not a silent independent-label fault model.
Only Python's standard library is required. Generality is supplied by the
ordinary proof and the separately scoped Lean counting lemmas.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sets_of_size(m, size):
    return [sum(1 << i for i in xs) for xs in combinations(range(m), size)]


def image(mask, alias):
    representative = alias & -alias
    return (mask & ~alias) | (representative if mask & alias else 0)


def all_root_faults(m, alias, b):
    roots = image((1 << m) - 1, alias)
    active = [i for i in range(m) if roots >> i & 1]
    for bad in combinations(active, b):
        yield sum(1 << i for i in bad)


def bad_labels(m, alias, bad_roots):
    return sum(1 << i for i in range(m) if image(1 << i, alias) & bad_roots)


def choose_alias_for_small_intersection(m, c, intersection):
    inside = [i for i in range(m) if intersection >> i & 1]
    outside = [i for i in range(m) if not (intersection >> i & 1)]
    selected = inside[:c]
    selected += outside[:c-len(selected)]
    return sum(1 << i for i in selected)


def actor_transcript(path, tainted_labels, nonce):
    # All roots, including compromised ones, use the same per-label messages
    # and timings. The only observable variation is the actual effect bit.
    labels = [i for i in range(path.bit_length()) if path >> i & 1]
    return {"nonce": nonce, "path": labels,
            "prepare": [(i, "BOUND", 1) for i in labels],
            "effect": "NO_EFFECT" if path & tainted_labels else "REPAIRED",
            "cancel": [(i, "CLOSED_THIS_NONCE", 3) for i in labels]}


def check_overlap_and_realizability():
    image_pair_cases = 0
    robust_cases = 0
    realized_worlds = 0
    parameter_cases = 0
    bridging_cases = 0
    for m in range(3, 8):
        masks = range(1 << m)
        weights = [x.bit_count() for x in masks]
        universe = (1 << m)-1
        for c in range(1, m):
            aliases = sets_of_size(m, c)
            minima = [m] * (1 << (2*m))
            for alias in aliases:
                images = [image(x, alias) for x in masks]
                for left in masks:
                    offset = left << m
                    li = images[left]
                    for right in masks:
                        idx = offset | right
                        value = (li & images[right]).bit_count()
                        minima[idx] = min(minima[idx], value)
                        image_pair_cases += 1
            for left in masks:
                for right in masks:
                    intersection = (left & right).bit_count()
                    if intersection:
                        predicted = max(1, intersection-c+1)
                    else:
                        predicted = int(c > m-min(weights[left], weights[right]))
                        bridging_cases += predicted
                    actual = minima[(left << m) | right]
                    assert actual == predicted
                    for b in range(1, m-c+1):
                        k = b+c-1
                        assert (actual > b) == (intersection >= k+1)
                        robust_cases += 1
            for b in range(1, m-c+1):
                k = b+c-1
                realized_max = set()
                for alias in aliases:
                    for actual_bad in all_root_faults(m, alias, b):
                        labels = bad_labels(m, alias, actual_bad)
                        assert labels.bit_count() <= k
                        if labels.bit_count() == k:
                            realized_max.add(labels)
                        realized_worlds += 1
                assert realized_max == set(sets_of_size(m, k))
                feasible = []
                for q in range(1, m+1):
                    for r in range(1, m+1):
                        if q+r > m+k and q <= m-k and r <= m-k:
                            feasible.append((q,r))
                assert bool(feasible) == (m >= 3*k+1)
                if m == 3*k+1:
                    assert feasible == [(2*k+1,2*k+1)]
                if m <= 3*k:
                    # Availability-forced maximal sets witness failure for any
                    # subpaths they contain, not merely for threshold families.
                    first_bad = (1 << k)-1
                    second_bad = ((1 << k)-1) << (m-k)
                    left, right = universe ^ first_bad, universe ^ second_bad
                    assert (left & right).bit_count() <= k
                    alias = choose_alias_for_small_intersection(m,c,left & right)
                    assert (image(left,alias) & image(right,alias)).bit_count() <= b
                parameter_cases += 1
    return {"actual_image_pair_cases_m_le_7": image_pair_cases,
            "robust_equivalence_cases": robust_cases,
            "fixed_map_actual_root_fault_worlds": realized_worlds,
            "parameter_feasibility_and_nonuniform_obstructions": parameter_cases,
            "forced_bridge_zero_label_intersection_cases": bridging_cases}


def check_minimum_constructions():
    worlds = 0
    path_cases = 0
    cancellation_sets = 0
    common_transcript_pairs = 0
    rows = []
    for b,c in [(1,1),(1,2),(2,1),(1,3),(2,2),(3,1)]:
        k=b+c-1; m=3*k+1; q=2*k+1
        all_labels=(1 << m)-1
        paths=sets_of_size(m,q)
        aliases=sets_of_size(m,c)
        for alias in aliases:
            for cancellation in sets_of_size(m,k+1):
                assert image(cancellation,alias).bit_count() >= b+1
                cancellation_sets += 1
            for actual_bad in all_root_faults(m,alias,b):
                fault_labels=bad_labels(m,alias,actual_bad)
                assert fault_labels.bit_count() <= k
                assert any(not (image(p,alias) & actual_bad) for p in paths)
                for p in paths:
                    assert (p & ~fault_labels).bit_count() >= k+1
                    path_cases += 1
                worlds += 1
        assert len(paths) == comb(m,k)
        # Each maximal fault-label set is realized by one canonical fixed map.
        for tainted in sets_of_size(m,k):
            alias=choose_alias_for_small_intersection(m,c,tainted)
            bad_roots=(tainted & ~alias) | (alias & -alias)
            assert bad_roots.bit_count()==b
            assert bad_labels(m,alias,bad_roots)==tainted
            good=[p for p in paths if not (image(p,alias) & bad_roots)]
            assert good == [all_labels ^ tainted]
        # Compare full allowed observations for all still-uncovered worlds.
        # Preparation and newly added cancellation replies do not reveal maps.
        for index,path in enumerate(paths):
            transcripts=[actor_transcript(path,t,index) for t in sets_of_size(m,k) if path&t]
            assert all(x==transcripts[0] for x in transcripts)
            common_transcript_pairs += len(transcripts)
        rows.append({"B_actual_roots":b,"class_size_c":c,"k_bad_labels":k,
                     "labels_m":m,"actual_roots":m-c+1,"q":q,"r":q,
                     "cancel_labels":k+1,"macro_attempts":len(paths),
                     "additional_actual_roots_vs_known_map":2*(c-1),
                     "prebuilt_gate_occurrences":q*len(paths)})
    return {"minimum_construction_actual_worlds":worlds,
            "selected_path_availability_checks":path_cases,
            "actual_image_cancellation_checks":cancellation_sets,
            "common_failed_transcript_comparisons":common_transcript_pairs},rows


def check_named_counterexamples():
    traces={}
    # Four-label paths cannot avoid the bad two-label root.
    m=5;alias=(1<<0)|(1<<1);bad=image(alias,alias)
    assert all(image(p,alias)&bad for p in sets_of_size(m,4))
    traces["five_labels_four_gate_liveness_failure"]={
        "labels":m,"alias_class":[0,1],"faulty_actual_root":0,
        "failed_paths":[[i for i in range(m) if p>>i&1] for p in sets_of_size(m,4)]}
    # Three-label path/quorum stale landing with exactly one actual fault.
    left=sum(1<<i for i in [0,1,2]);right=sum(1<<i for i in [2,3,4]);bad=1<<2
    shared=image(left,alias)&image(right,alias)
    assert shared==bad
    intact_revokers=image(right,alias)&~bad
    assert not (image(left,alias)&intact_revokers)
    traces["five_labels_stale_landing"]={"alias_class":[0,1],"path":[0,1,2],
        "revocation_labels":[2,3,4],"faulty_actual_root":2,
        "actual_path_roots":[0,2],"actual_revocation_roots":[2,3,4],
        "old_path_can_land_after_effective_revoke":True}
    # Two cancellation labels may both be one faulty actual root.
    alias=sum(1<<i for i in [0,1]);bad=1<<0
    assert image(alias,alias)==bad
    traces["two_cancel_labels_not_two_roots"]={"alias_class":[0,1],
        "cancellation_labels":[0,1],"actual_acknowledging_roots":[0],
        "budget_actual_roots":1,"closure_not_warranted":True}
    # Corner case retained: a large class forces a shared root even when the
    # paths have no common label. That one shared root is still corruptible.
    m=5;c=4;left=0b00011;right=0b11100
    values=[(image(left,a)&image(right,a)).bit_count() for a in sets_of_size(m,c)]
    assert set(values)=={1}
    traces["forced_alias_bridge"]={"m":m,"c":c,"left_labels":[0,1],
        "right_labels":[2,3,4],"label_intersection":0,
        "shared_actual_roots_under_every_map":1,
        "not_safe_against_B1":True}
    return traces


def main():
    counts=check_overlap_and_realizability()
    extra,rows=check_minimum_constructions();counts.update(extra)
    traces=check_named_counterexamples()
    result={"status":"PASS_FINITE_FIXED_MAP_CONTROLS","counts":counts,
            "minimum_constructions":rows,
            "scope":"Fixed observation-compatible families; no arbitrary map-learning protocol claim.",
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'ATTRIBUTION_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'ATTRIBUTION_COUNTEREXAMPLES.json').write_text(json.dumps(traces,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
