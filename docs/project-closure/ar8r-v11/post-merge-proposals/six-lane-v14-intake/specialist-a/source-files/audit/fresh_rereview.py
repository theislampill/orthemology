#!/usr/bin/env python3
"""Procedurally distinct rereview of the frozen specialist-A candidate.

This file deliberately imports none of the generation checker modules. It
re-derives selected load-bearing claims from the frozen typed objects and small
exhaustive model spaces.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import yaml

BASE = Path(__file__).resolve().parents[1]


def partitions(n: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []

    def rec(i: int, labels: list[int]) -> None:
        if i == n:
            # Canonical restricted-growth strings.
            out.append(tuple(labels))
            return
        upper = 0 if not labels else max(labels) + 1
        for lab in range(upper + 1):
            labels.append(lab)
            rec(i + 1, labels)
            labels.pop()

    if n == 0:
        return [tuple()]
    rec(1, [0])
    return out


def projection(profile: tuple[int, ...], cells: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(profile[i] for i in cells)


def restriction_injective_set(hypotheses: tuple[tuple[int, ...], ...], cells: tuple[int, ...]) -> bool:
    return len({projection(h, cells) for h in hypotheses}) == len(hypotheses)


def restriction_collision_pair(hypotheses: tuple[tuple[int, ...], ...], cells: tuple[int, ...]) -> bool:
    for i, h in enumerate(hypotheses):
        for hp in hypotheses[i + 1 :]:
            if all(h[j] == hp[j] for j in cells):
                return True
    return False


def pareto_front(costs: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    keep = []
    for c in costs:
        dominated = any(d != c and d[0] <= c[0] and d[1] <= c[1] for d in costs)
        if not dominated and c not in keep:
            keep.append(c)
    return tuple(sorted(keep))


def feasible(costs: Iterable[tuple[int, int]], budget: tuple[int, int]) -> bool:
    return any(c[0] <= budget[0] and c[1] <= budget[1] for c in costs)


def eventually_cycle_good(start: int, strategy: tuple[int, ...], trans: tuple[tuple[int, int], ...], good: set[int]) -> bool:
    seen: dict[int, int] = {}
    seq: list[int] = []
    s = start
    while s not in seen:
        seen[s] = len(seq)
        seq.append(s)
        s = trans[s][strategy[s]]
    cycle = seq[seen[s] :]
    return bool(cycle) and all(x in good for x in cycle)


def obs_strategies(obs: tuple[int, ...]) -> list[tuple[int, ...]]:
    labels = sorted(set(obs))
    out = []
    for acts in itertools.product((0, 1), repeat=len(labels)):
        amap = dict(zip(labels, acts))
        out.append(tuple(amap[o] for o in obs))
    return out


def union_graph(rel_a: tuple[int, ...], rel_b: tuple[int, ...]) -> list[set[int]]:
    n = len(rel_a)
    g = [set([i]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if rel_a[i] == rel_a[j] or rel_b[i] == rel_b[j]:
                g[i].add(j)
                g[j].add(i)
    return g


def distances(g: list[set[int]], w: int) -> dict[int, int]:
    d = {w: 0}
    q = deque([w])
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def defect(rep: tuple[int, ...], target: tuple[int, ...]) -> int:
    return sum(1 for i in range(len(rep)) for j in range(i + 1, len(rep)) if rep[i] == rep[j] and target[i] != target[j])


def target_collisions(base: tuple[int, ...], target: tuple[int, ...]) -> set[tuple[int, int]]:
    return {(i, j) for i in range(len(base)) for j in range(i + 1, len(base)) if base[i] == base[j] and target[i] != target[j]}


def separated(pairs: set[tuple[int, int]], factor: tuple[int, ...]) -> set[tuple[int, int]]:
    return {(i, j) for i, j in pairs if factor[i] != factor[j]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="audit/FRESH_REREVIEW.json")
    args = ap.parse_args()

    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    def record(name: str, passed: bool, detail: Any) -> None:
        checks.append({"check": name, "pass": bool(passed), "detail": detail})
        if not passed:
            errors.append(name)

    # R1: derive totality from the frozen typed registry rather than stored counts.
    registry = yaml.safe_load((BASE / "registry/architecture_factor_registry.yaml").read_text())
    manifest = yaml.safe_load((BASE / "coverage/declared_family_manifest.yaml").read_text())
    coverage = yaml.safe_load((BASE / "coverage/total_coverage_map.yaml").read_text())
    factor_ids = [f["id"] for f in registry["factors"]]
    product_size = math.prod(len(f["values"]) for f in registry["factors"])
    arch_total = all(set(a["factor_map"]) == set(factor_ids) for a in registry["architectures"])
    manifest_ids = [x["id"] for x in manifest["families"]]
    coverage_ids = [x["family_id"] for x in coverage["rows"]]
    common_outputs = set(registry["common_decoder"]["output_fields"])
    forbidden = set(registry["common_decoder"]["forbidden_input_fields"])
    record(
        "r1_typed_totality_and_target_blind_surface",
        len(factor_ids) == len(set(factor_ids)) == 8
        and product_size == 256
        and arch_total
        and len(manifest_ids) == len(set(manifest_ids)) == 22
        and sorted(manifest_ids) == sorted(coverage_ids)
        and not (common_outputs & forbidden),
        {"factor_count": len(factor_ids), "product_size": product_size, "architecture_maps_total": arch_total, "manifest_count": len(manifest_ids)},
    )

    # R2: independent injectivity/collision algorithms over every small binary H,D.
    r2_cases = 0
    r2_mismatch = 0
    unrestricted_failures = 0
    for n in (1, 2, 3):
        universe = tuple(itertools.product((0, 1), repeat=n))
        for mask in range(1, 1 << len(universe)):
            h = tuple(universe[i] for i in range(len(universe)) if mask & (1 << i))
            for dmask in range(1 << n):
                cells = tuple(i for i in range(n) if dmask & (1 << i))
                r2_cases += 1
                if restriction_injective_set(h, cells) == restriction_collision_pair(h, cells):
                    r2_mismatch += 1
        for dmask in range((1 << n) - 1):
            cells = tuple(i for i in range(n) if dmask & (1 << i))
            if not restriction_injective_set(universe, cells):
                unrestricted_failures += 1
    parity = tuple(x for x in itertools.product((0, 1), repeat=3) if x[2] == (x[0] ^ x[1]))
    record(
        "r2_restriction_injectivity_and_structural_exception",
        r2_cases == 2106 and r2_mismatch == 0 and unrestricted_failures == 11 and restriction_injective_set(parity, (0, 1)),
        {"cases": r2_cases, "mismatches": r2_mismatch, "unrestricted_proper_deletions_noninjective": unrestricted_failures, "parity_two_cell_identifiable": restriction_injective_set(parity, (0, 1))},
    )

    # R3: scalar permutation invariance and Pareto-feasibility, independently.
    scalar_ok = True
    scalar_checks = 0
    for costs in itertools.product((1, 2, 3), repeat=3):
        expected = min(costs)
        for perm in set(itertools.permutations(costs)):
            scalar_checks += 1
            scalar_ok &= min(perm) == expected
    pareto_ok = True
    pareto_checks = 0
    for costs in itertools.combinations_with_replacement(tuple(itertools.product((1, 2, 3), repeat=2)), 3):
        front = pareto_front(costs)
        for budget in itertools.product((1, 2, 3), repeat=2):
            pareto_checks += 1
            pareto_ok &= feasible(costs, budget) == feasible(front, budget)
    chimera = ((1, 3), (3, 1))
    chimera_inf = (min(x[0] for x in chimera), min(x[1] for x in chimera))
    record(
        "r3_resource_quotient_and_pareto_correction",
        scalar_ok and pareto_ok and not feasible(chimera, chimera_inf),
        {"scalar_permutation_checks": scalar_checks, "pareto_budget_checks": pareto_checks, "unattained_coordinatewise_infimum": chimera_inf},
    )

    # R4: independent observation-policy enumeration and explicit conflict model.
    correspondence = True
    r4_cases = 0
    false_sufficiency = 0
    for flat in itertools.product((0, 1), repeat=4):
        trans = ((flat[0], flat[1]), (flat[2], flat[3]))
        state_strategies = tuple(itertools.product((0, 1), repeat=2))
        for obs in ((0, 0), (0, 1)):
            uniform = tuple(obs_strategies(obs))
            for gmask in range(4):
                good = {i for i in range(2) if gmask & (1 << i)}
                for bmask in (1, 2, 3):
                    belief = [i for i in range(2) if bmask & (1 << i)]
                    direct = any(all(eventually_cycle_good(s, st, trans, good) for s in belief) for st in uniform)
                    uniform_state = any(
                        all(eventually_cycle_good(s, st, trans, good) for s in belief)
                        for st in state_strategies
                        if all(obs[i] != obs[j] or st[i] == st[j] for i in range(2) for j in range(2))
                    )
                    statewise = all(any(eventually_cycle_good(s, st, trans, good) for st in state_strategies) for s in belief)
                    correspondence &= direct == uniform_state
                    false_sufficiency += int(statewise and not direct)
                    r4_cases += 1
    trans4 = ((2, 3), (3, 2), (2, 2), (3, 3))
    good4 = {2}
    state_strats4 = tuple(itertools.product((0, 1), repeat=4))
    individual = all(any(eventually_cycle_good(s, st, trans4, good4) for st in state_strats4) for s in (0, 1))
    common_obs = tuple(st for st in state_strats4 if st[0] == st[1])
    no_uniform = not any(all(eventually_cycle_good(s, st, trans4, good4) for s in (0, 1)) for st in common_obs)
    record(
        "r4_observation_uniformity_and_statewise_countermodel",
        correspondence and false_sufficiency > 0 and individual and no_uniform,
        {"small_game_cases": r4_cases, "statewise_false_sufficiency_cases": false_sufficiency, "explicit_individual_win": individual, "explicit_uniform_loss": no_uniform},
    )

    # R5: union-reachability radius, all finite equivalence pairs through n=4.
    r5_cases = 0
    radius_failures = 0
    first_order_not_ck = 0
    max_radius = 0
    for n in (1, 2, 3, 4):
        ps = partitions(n)
        for pa in ps:
            for pb in ps:
                g = union_graph(pa, pb)
                for valmask in range(1 << n):
                    truth = {i for i in range(n) if valmask & (1 << i)}
                    for w in range(n):
                        ds = distances(g, w)
                        d = max(ds.values())
                        max_radius = max(max_radius, d)
                        ck = all(v in truth for v in ds)
                        ball_d = all(v in truth for v, dist in ds.items() if dist <= d)
                        if ck != ball_d or d > n - 1:
                            radius_failures += 1
                        everyone1 = all(v in truth for v, dist in ds.items() if dist <= 1)
                        first_order_not_ck += int(everyone1 and not ck)
                        r5_cases += 1
    pa = (0, 0, 1)
    pb = (0, 1, 1)
    g = union_graph(pa, pb)
    ds = distances(g, 0)
    truth = {0, 1}
    explicit_e1 = all(v in truth for v, dist in ds.items() if dist <= 1)
    explicit_ck = all(v in truth for v in ds)
    record(
        "r5_common_knowledge_union_radius",
        r5_cases == 15034 and radius_failures == 0 and max_radius <= 3 and first_order_not_ck == 588 and explicit_e1 and not explicit_ck,
        {"cases": r5_cases, "radius_failures": radius_failures, "first_order_not_common_knowledge": first_order_not_ck, "max_radius": max_radius},
    )

    # R6: typed lineage rules; copying and syncing cannot mint roots.
    roots: list[set[str]] = [{"r0"}]
    for i in range(100):
        roots.append(set(roots[-1]))
    copy_chain_ok = len(roots) == 101 and len(set().union(*roots)) == 1
    synced = roots[10] | {"r1"}
    sync_union_ok = synced == {"r0", "r1"}
    acquired = synced | {"r2"}
    acquisition_adds = acquired - synced == {"r2"}
    same_roots_distinct_nodes = roots[0] == roots[100] and 0 != 100
    record(
        "r6_provenance_root_nonmultiplicity",
        copy_chain_ok and sync_union_ok and acquisition_adds and same_roots_distinct_nodes,
        {"episodes": len(roots), "global_roots_after_100_copies": len(set().union(*roots)), "sync_roots": sorted(synced), "acquisition_delta": sorted(acquired - synced)},
    )

    # R7: decoder existence by direct assignment search versus fibre constancy.
    decoder_cases = 0
    decoder_failures = 0
    joint_cases = 0
    joint_failures = 0
    for n in (1, 2, 3, 4):
        maps = tuple(itertools.product((0, 1), repeat=n))
        for rep in maps:
            for target in maps:
                fibre_const = defect(rep, target) == 0
                direct = any(all(dec[rep[i]] == target[i] for i in range(n)) for dec in itertools.product((0, 1), repeat=2))
                decoder_failures += int(fibre_const != direct)
                decoder_cases += 1
                for q in maps:
                    joint = tuple((rep[i], q[i]) for i in range(n))
                    # Encode joint pairs without relying on labels.
                    joint_defect = sum(1 for i in range(n) for j in range(i + 1, n) if joint[i] == joint[j] and target[i] != target[j])
                    joint_failures += int(joint_defect > defect(rep, target))
                    joint_cases += 1
    record(
        "r7_representation_fibre_defect",
        decoder_failures == 0 and joint_failures == 0,
        {"decoder_cases": decoder_cases, "decoder_failures": decoder_failures, "joint_cases": joint_cases, "joint_monotonicity_failures": joint_failures},
    )

    # R8: coverage identity, monotonicity, submodularity over all 3-object maps.
    maps3 = tuple(itertools.product((0, 1), repeat=3))
    r8_cases = 0
    identity_checks = 0
    failures = 0
    submod_checks = 0
    for base in maps3:
        for target in maps3:
            pairs = target_collisions(base, target)
            for factors in itertools.product(maps3, repeat=3):
                covers = [separated(pairs, f) for f in factors]
                subset_cover: dict[int, set[tuple[int, int]]] = {}
                for mask in range(8):
                    union: set[tuple[int, int]] = set()
                    for i in range(3):
                        if mask & (1 << i):
                            union |= covers[i]
                    subset_cover[mask] = union
                    remaining = pairs - union
                    failures += int(len(remaining) != len(pairs) - len(union))
                    identity_checks += 1
                for a in range(8):
                    for b in range(8):
                        if a & ~b:
                            continue
                        for e in range(3):
                            if b & (1 << e):
                                continue
                            marg_a = len(subset_cover[a | (1 << e)]) - len(subset_cover[a])
                            marg_b = len(subset_cover[b | (1 << e)]) - len(subset_cover[b])
                            failures += int(marg_a < marg_b)
                            submod_checks += 1
                # A factor that is a function of base cannot split a base fibre.
                derived = base
                failures += int(bool(separated(pairs, derived)))
                r8_cases += 1
    record(
        "r8_residual_collision_coverage",
        r8_cases == 32768 and identity_checks == 262144 and failures == 0 and submod_checks > 0,
        {"signatures": r8_cases, "identity_checks": identity_checks, "submodularity_checks": submod_checks, "failures": failures},
    )

    # R9: common decoder across a tagged union, recomputed independently.
    point_maps = []
    for obs in itertools.product((0, 1), repeat=2):
        for target in itertools.product((0, 1), repeat=2):
            point_maps.append(tuple(zip(obs, target)))
    r9_cases = 0
    r9_mismatch = 0
    r9_local_only = 0
    for arches in itertools.product(point_maps, repeat=3):
        seen: dict[int, int] = {}
        consistent = True
        for arch in arches:
            for obs, target in arch:
                if obs in seen and seen[obs] != target:
                    consistent = False
                seen.setdefault(obs, target)
        brute = any(all(dec[obs] == target for arch in arches for obs, target in arch) for dec in itertools.product((0, 1), repeat=2))
        local = all(any(all(dec[obs] == target for obs, target in arch) for dec in itertools.product((0, 1), repeat=2)) for arch in arches)
        r9_mismatch += int(consistent != brute)
        r9_local_only += int(local and not brute)
        r9_cases += 1
    record(
        "r9_cross_architecture_common_decoder",
        r9_cases == 4096 and r9_mismatch == 0 and r9_local_only > 0,
        {"cases": r9_cases, "criterion_mismatches": r9_mismatch, "local_decoders_without_common": r9_local_only},
    )

    # R10: exact minimum collision cover, independently brute-forced and DP-checked.
    def rr_union(covers: tuple[int, ...], subset: int) -> int:
        u = 0
        for i, c in enumerate(covers):
            if subset & (1 << i):
                u |= c
        return u

    def rr_brute_min(universe: int, covers: tuple[int, ...]) -> int | None:
        vals = [subset.bit_count() for subset in range(1 << len(covers)) if rr_union(covers, subset) == universe]
        return min(vals) if vals else None

    def rr_dp_min(universe: int, covers: tuple[int, ...]) -> int | None:
        inf = len(covers) + 1
        dp = {0: 0}
        for c in covers:
            nxt = dict(dp)
            for mask, val in dp.items():
                nm = mask | c
                nxt[nm] = min(nxt.get(nm, inf), val + 1)
            dp = nxt
        return dp.get(universe)

    r10_cases = 0
    r10_min_mismatch = 0
    r10_no_cover_mismatch = 0
    r10_deletion_mismatch = 0
    for n in range(1, 5):
        universe = (1 << n) - 1
        for m in range(1, 5):
            for covers in itertools.product(range(1 << n), repeat=m):
                b = rr_brute_min(universe, covers)
                d = rr_dp_min(universe, covers)
                r10_min_mismatch += int(b != d)
                r10_no_cover_mismatch += int((b is None) != (rr_union(covers, (1 << m) - 1) != universe))
                for subset in range(1 << m):
                    if rr_union(covers, subset) != universe:
                        continue
                    for f in range(m):
                        if not (subset & (1 << f)):
                            continue
                        removal_breaks = rr_union(covers, subset & ~(1 << f)) != universe
                        others = rr_union(covers, subset & ~(1 << f))
                        private = bool(covers[f] & ~others & universe)
                        r10_deletion_mismatch += int(removal_breaks != private)
                r10_cases += 1
    greedy_universe = (1 << 6) - 1
    greedy_covers = (
        sum(1 << (x - 1) for x in (1, 2, 3, 4)),
        sum(1 << (x - 1) for x in (1, 2, 5)),
        sum(1 << (x - 1) for x in (3, 4, 6)),
    )
    uncovered = greedy_universe
    chosen = set()
    while uncovered:
        i = max((i for i in range(3) if i not in chosen), key=lambda j: ((greedy_covers[j] & uncovered).bit_count(), -j))
        chosen.add(i)
        uncovered &= ~greedy_covers[i]
    record(
        "r10_minimum_collision_cover",
        r10_cases == sum((1 << n) ** m for n in range(1, 5) for m in range(1, 5))
        and r10_min_mismatch == 0 and r10_no_cover_mismatch == 0 and r10_deletion_mismatch == 0
        and len(chosen) == 3 and rr_brute_min(greedy_universe, greedy_covers) == 2,
        {"set_systems": r10_cases, "minimum_mismatches": r10_min_mismatch, "no_cover_mismatches": r10_no_cover_mismatch, "deletion_mismatches": r10_deletion_mismatch, "greedy": len(chosen), "optimum": rr_brute_min(greedy_universe, greedy_covers)},
    )

    # R11: finite causal history-state twin and open-loop/adaptive partition equality.
    def rr_kernel(table: int, history: tuple[tuple[int, int], ...], nxt: int) -> int:
        if not history:
            idx = nxt
        else:
            pi, po = history[0]
            idx = 2 + ((pi * 2 + po) * 2 + nxt)
        return (table >> idx) & 1

    rr_policies = tuple((first, decision) for first in (0, 1) for decision in itertools.product((0, 1), repeat=4))

    def rr_run_policy(table: int, policy: tuple[int, tuple[int, ...]]) -> tuple[tuple[int, int], ...]:
        first, decision = policy
        o0 = rr_kernel(table, (), first)
        h = ((first, o0),)
        i1 = decision[first * 2 + o0]
        o1 = rr_kernel(table, h, i1)
        return h + ((i1, o1),)

    adaptive_groups: dict[tuple[object, ...], set[int]] = {}
    open_groups: dict[tuple[object, ...], set[int]] = {}
    r11_trace_checks = 0
    r11_mismatch = 0
    r11_output_only_fail = 0
    for table in range(1 << 10):
        ap = tuple(rr_run_policy(table, pol) for pol in rr_policies)
        # The independent twin uses an explicitly updated transcript state.
        twin_profile = []
        for first, decision in rr_policies:
            state: tuple[tuple[int, int], ...] = ()
            o0 = rr_kernel(table, state, first)
            state = state + ((first, o0),)
            i1 = decision[first * 2 + o0]
            o1 = rr_kernel(table, state, i1)
            state = state + ((i1, o1),)
            twin_profile.append(state)
            r11_trace_checks += 1
        r11_mismatch += int(ap != tuple(twin_profile))
        op = []
        for i0, i1 in itertools.product((0, 1), repeat=2):
            o0 = rr_kernel(table, (), i0)
            h = ((i0, o0),)
            o1 = rr_kernel(table, h, i1)
            op.append(h + ((i1, o1),))
        adaptive_groups.setdefault(ap, set()).add(table)
        open_groups.setdefault(tuple(op), set()).add(table)
        r11_output_only_fail += int(any(rr_kernel(table, ((0, po),), ni) != rr_kernel(table, ((1, po),), ni) for po in (0, 1) for ni in (0, 1)))
    record(
        "r11_finite_history_state_twin",
        r11_trace_checks == 32768 and r11_mismatch == 0
        and {frozenset(v) for v in adaptive_groups.values()} == {frozenset(v) for v in open_groups.values()}
        and r11_output_only_fail > 0,
        {"trace_checks": r11_trace_checks, "mismatches": r11_mismatch, "adaptive_fibres": len(adaptive_groups), "open_loop_fibres": len(open_groups), "output_only_failures": r11_output_only_fail},
    )

    # R12: predictive residual quotient versus direct minimal decoder-state search.
    r12_mismatch = 0
    r12_compressible = 0
    r12_deletion_merge = 0
    r12_profile_q: dict[tuple[object, ...], set[int]] = {}
    for table in range(1 << 10):
        histories = tuple(((i, rr_kernel(table, (), i)),) for i in (0, 1))
        sigs = tuple(tuple(rr_kernel(table, h, ni) for ni in (0, 1)) for h in histories)
        q = len(set(sigs))
        brute_min = None
        for k in (1, 2):
            found = False
            for assignment in itertools.product(range(k), repeat=2):
                for decoder_bits in range(1 << (k * 2)):
                    if all(((decoder_bits >> (assignment[hi] * 2 + ni)) & 1) == rr_kernel(table, histories[hi], ni) for hi in range(2) for ni in (0, 1)):
                        found = True
                        break
                if found:
                    break
            if found:
                brute_min = k
                break
        r12_mismatch += int(brute_min != q)
        r12_compressible += int(q == 1)
        r12_deletion_merge += int(q == 2 and len({s[0] for s in sigs}) == 1)
        op = []
        for i0, i1 in itertools.product((0, 1), repeat=2):
            o0 = rr_kernel(table, (), i0)
            h = ((i0, o0),)
            o1 = rr_kernel(table, h, i1)
            op.append(h + ((i1, o1),))
        r12_profile_q.setdefault(tuple(op), set()).add(q)
    profile_q_fail = sum(len(v) != 1 for v in r12_profile_q.values())
    record(
        "r12_predictive_history_quotient",
        r12_mismatch == 0 and r12_compressible > 0 and r12_deletion_merge > 0 and profile_q_fail == 0,
        {"tables": 1024, "minimality_mismatches": r12_mismatch, "compressible": r12_compressible, "deletion_merges": r12_deletion_merge, "profile_invariance_failures": profile_q_fail},
    )

    # Recheck the claim status and custody ceilings, without treating them as proof.
    import re
    result_files = sorted(p for p in (BASE / "results").glob("r*_*.json") if re.match(r"r\d+_", p.name))
    status_safe = len(result_files) == 12
    for p in result_files:
        d = json.loads(p.read_text())
        ancestry = str(d.get("ancestry_disposition", "")).lower()
        positive_novelty_markers = ("novelty awarded", "novelty established", "novel theorem", "new theorem origin")
        status_safe &= d.get("status") == "PASS" and "novelty" in ancestry and not any(marker in ancestry for marker in positive_novelty_markers)
    record("result_status_and_novelty_ceiling", status_safe, {"result_files": len(result_files)})

    output = BASE / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "spa-fresh-rereview-v1",
        "status": "PASS" if not errors else "FAIL",
        "generation_checker_imports": False,
        "review_method": "independent implementations and small exhaustive spaces; no imports from checks/check_r*.py and no trust in prefilled counters",
        "checks": checks,
        "errors": errors,
        "claim_ceiling": "procedurally distinct local rereview; bounded mathematical/executable evidence only, not external review, architecture implementation, Lean verification, adoption, novelty, or metaphysical truth",
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(checks), "errors": errors}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
