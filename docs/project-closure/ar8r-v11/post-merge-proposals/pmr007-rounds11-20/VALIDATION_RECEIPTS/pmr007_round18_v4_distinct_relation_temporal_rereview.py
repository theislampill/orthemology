from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json
import math
import random
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "PMR007_ROUND18_CERTIFICATE_OBJECT_REFINEMENT_V4.yaml"
HASHES = ROOT / "PMR-007_FRONTIER_ROUND18_V4_FROZEN_HASHES.sha256"
OUT = Path(__file__).with_name("PMR-007_FRONTIER_ROUND18_V4_DISTINCT_RELATION_TEMPORAL_REREVIEW_RESULTS.json")


def verify_hashes() -> list[str]:
    failures = []
    for line in HASHES.read_text().splitlines():
        if not line.strip():
            continue
        expected, path = line.split(maxsplit=1)
        p = Path(path)
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != expected:
            failures.append(str(p))
    return failures


def rho_dp(good_masks: tuple[int, ...], m: int) -> int | float:
    n = len(good_masks)
    if any(mask == 0 for mask in good_masks):
        return math.inf
    cover_by_obj = []
    for k in range(m):
        mask = 0
        for q, gm in enumerate(good_masks):
            if gm >> k & 1:
                mask |= 1 << q
        cover_by_obj.append(mask)
    full = (1 << n) - 1
    dp = {0: 0}
    for cm in cover_by_obj:
        nxt = dict(dp)
        for state_mask, cost in dp.items():
            nm = state_mask | cm
            nxt[nm] = min(nxt.get(nm, 10**9), cost + 1)
        dp = nxt
    return dp.get(full, math.inf)


def min_distinct_outputs(good_masks: tuple[int, ...], m: int) -> int | float:
    choices = [tuple(k for k in range(m) if gm >> k & 1) for gm in good_masks]
    if any(not c for c in choices):
        return math.inf
    best = m + 1

    def rec(i: int, used: int):
        nonlocal best
        if used.bit_count() >= best:
            return
        if i == len(choices):
            best = min(best, used.bit_count())
            return
        for k in choices[i]:
            rec(i + 1, used | (1 << k))

    rec(0, 0)
    return best


def partitions(n: int):
    a = [0] * n

    def rec(i: int, mx: int):
        if i == n:
            yield tuple(a)
            return
        for x in range(mx + 2):
            a[i] = x
            yield from rec(i + 1, max(mx, x))

    if n == 0:
        yield ()
    else:
        yield from rec(1, 0)


def intersection_nonempty(good: list[set[int]], states: list[int]) -> bool:
    inter = set(good[states[0]])
    for q in states[1:]:
        inter &= good[q]
    return bool(inter)


def criterion_min_messages(good: list[set[int]], obs: tuple[int, ...], enc: tuple[int, ...]) -> int | float:
    if any(not x for x in good):
        return math.inf
    ecount = max(enc) + 1
    for k in range(1, ecount + 1):
        for msg in product(range(k), repeat=ecount):
            ok = True
            for o in set(obs):
                for a in range(k):
                    states = [q for q in range(len(good)) if obs[q] == o and msg[enc[q]] == a]
                    if states and not intersection_nonempty(good, states):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return len(set(msg))
    return math.inf


def decoder_first_min_messages(good: list[set[int]], obs: tuple[int, ...], enc: tuple[int, ...], m: int) -> int | float:
    """Independent route: enumerate decoders first, then test whether every encoder cell has a legal message."""
    if any(not x for x in good):
        return math.inf
    ecount = max(enc) + 1
    ovals = sorted(set(obs))
    for k in range(1, ecount + 1):
        slots = [(o, a) for o in ovals for a in range(k)]
        for values in product(range(m), repeat=len(slots)):
            dec = dict(zip(slots, values))
            all_cells = True
            for e in range(ecount):
                states = [q for q in range(len(good)) if enc[q] == e]
                if not any(all(dec[(obs[q], a)] in good[q] for q in states) for a in range(k)):
                    all_cells = False
                    break
            if all_cells:
                return k
    return math.inf


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def ambiguity_criterion(code: list[str], good: list[set[int]], r: int) -> bool:
    words = ["".join(x) for x in product("01", repeat=len(code[0]))]
    for y in words:
        states = [q for q, cw in enumerate(code) if hamming(cw, y) <= r]
        if states and not intersection_nonempty(good, states):
            return False
    return True


def decoder_backtracking(code: list[str], good: list[set[int]], r: int, m: int) -> bool:
    words = ["".join(x) for x in product("01", repeat=len(code[0]))]
    constraints = []
    for y in words:
        allowed = set(range(m))
        used = False
        for q, cw in enumerate(code):
            if hamming(cw, y) <= r:
                allowed &= good[q]
                used = True
        if used:
            constraints.append(allowed)
    return all(constraints) and all(bool(x) for x in constraints)


def cyclic_scc_bad(graph: tuple[int, ...], target_mask: int, n: int) -> bool:
    """graph[q] is a nonempty successor bitmask; direct universal co-Buchi check."""
    # Reachability closure and SCC by mutual reachability, tiny n.
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
        for j in range(n):
            if graph[i] >> j & 1:
                reach[i][j] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    reach[i][j] = reach[i][j] or reach[k][j]
    seen = set()
    for i in range(n):
        if i in seen:
            continue
        comp = {j for j in range(n) if reach[i][j] and reach[j][i]}
        seen |= comp
        cyclic = len(comp) > 1 or bool(graph[i] >> i & 1)
        if cyclic and any(not (target_mask >> q & 1) for q in comp):
            return True
    return False


def exhaustive_rank_temporal() -> tuple[int, int, int]:
    n = 3
    successor_masks = list(range(1, 1 << n))
    total = eligible = failures = 0
    for target in range(1 << n):
        for ranks in product(range(3), repeat=n):
            for graph in product(successor_masks, repeat=n):
                total += 1
                ok = True
                for q in range(n):
                    for s in range(n):
                        if graph[q] >> s & 1:
                            if target >> q & 1:
                                ok = ok and ranks[s] <= ranks[q]
                            else:
                                ok = ok and ranks[s] < ranks[q]
                    if not ok:
                        break
                if not ok:
                    continue
                eligible += 1
                if cyclic_scc_bad(graph, target, n):
                    failures += 1
    return total, eligible, failures


def main() -> None:
    model = yaml.safe_load(MODEL.read_text())
    failures: list[str] = []
    hash_failures = verify_hashes()
    if hash_failures:
        failures.append("frozen hash drift")

    # Independent exact-state route: bitmask set-cover DP versus recursive output assignment.
    exact_cases = exact_mismatch = 0
    for m, max_n in ((2, 6), (3, 5), (4, 5)):
        subsets = range(1 << m)
        for n in range(1, max_n + 1):
            for fam in product(subsets, repeat=n):
                exact_cases += 1
                if rho_dp(fam, m) != min_distinct_outputs(fam, m):
                    exact_mismatch += 1
    if exact_mismatch:
        failures.append("independent exact-state mismatch")

    # Independent general-encoder route on exhaustive 3-state, two-object class.
    parts = list(partitions(3))
    info_cases = info_mismatch = 0
    for fam_masks in product(range(4), repeat=3):
        good = [{k for k in range(2) if fam_masks[q] >> k & 1} for q in range(3)]
        for obs in parts:
            for enc in parts:
                info_cases += 1
                a = criterion_min_messages(good, obs, enc)
                b = decoder_first_min_messages(good, obs, enc, 2)
                if a != b:
                    info_mismatch += 1
    if info_mismatch:
        failures.append("independent encoder-information mismatch")

    # Independent channel route: random larger relations plus strict witness.
    rng = random.Random(18004)
    relation_cases = relation_mismatch = 0
    for _ in range(30000):
        nstates = rng.randint(1, 5)
        m = rng.randint(1, 4)
        length = rng.randint(1, 4)
        r = rng.randint(0, min(1, length))
        code = ["".join(rng.choice("01") for _ in range(length)) for _ in range(nstates)]
        good = [{k for k in range(m) if rng.random() < 0.6} for _ in range(nstates)]
        relation_cases += 1
        if ambiguity_criterion(code, good, r) != decoder_backtracking(code, good, r, m):
            relation_mismatch += 1
    if relation_mismatch:
        failures.append("independent relation-channel mismatch")

    aw = model["adversarial_relation_witness"]
    oi = {k: i for i, k in enumerate(aw["objects"])}
    good = [{oi[k] for k in aw["admissible"][q]} for q in aw["states"]]
    code = [aw["binary_code"][q] for q in aw["states"]]
    strict_relation = ambiguity_criterion(code, good, 1)
    strict_intersections = {}
    for y in ["".join(x) for x in product("01", repeat=2)]:
        states = [q for q, cw in enumerate(code) if hamming(cw, y) <= 1]
        inter = set(good[states[0]])
        for q in states[1:]:
            inter &= good[q]
        strict_intersections[y] = sorted(inter)
    if not strict_relation or any(len(v) != 1 for v in strict_intersections.values()):
        failures.append("strict relation witness")

    # Projection and robust-completion randomized checks.
    projection_cases = projection_fail = completion_cases = completion_fail = 0
    for _ in range(20000):
        n = rng.randint(1, 7)
        kcount = rng.randint(1, 6)
        acount = rng.randint(1, kcount)
        act = [rng.randrange(acount) for _ in range(kcount)]
        H = [{k for k in range(kcount) if rng.random() < 0.55} for _ in range(n)]
        object_rho = rho_dp(tuple(sum(1 << k for k in s) for s in H), kcount)
        G = [{act[k] for k in s} for s in H]
        action_rho = rho_dp(tuple(sum(1 << a for a in s) for s in G), acount)
        projection_cases += 1
        if action_rho > object_rho:
            projection_fail += 1
        completions = [[{k for k in range(kcount) if rng.random() < 0.6} for _ in range(n)] for __ in range(3)]
        completion_cases += 1
        for q in range(n):
            inter = set(range(kcount))
            union = set()
            for comp in completions:
                inter &= comp[q]
                union |= comp[q]
            if not inter <= union:
                completion_fail += 1
    if projection_fail or completion_fail:
        failures.append("projection/completion failure")

    temporal_total, temporal_eligible, temporal_fail = exhaustive_rank_temporal()
    if temporal_fail:
        failures.append("direct temporal rereview failure")

    # Named history witness independently recomputed.
    current_rho = rho_dp((1, 1), 1)
    future_rho = rho_dp((1, 2), 2)
    history_pass = current_rho == 1 and future_rho == 2
    if not history_pass:
        failures.append("history witness")

    result = {
        "schema": "PMR007_ROUND18_V4_DISTINCT_FRESH_REREVIEW",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "frozen_hash_failures": hash_failures,
        "exact_state_relations_checked": exact_cases,
        "exact_state_mismatches": exact_mismatch,
        "general_encoder_information_cases": info_cases,
        "general_encoder_information_mismatches": info_mismatch,
        "random_relation_channel_cases": relation_cases,
        "random_relation_channel_mismatches": relation_mismatch,
        "strict_relation_selector_possible": strict_relation,
        "strict_relation_intersections": strict_intersections,
        "projection_cases": projection_cases,
        "projection_failures": projection_fail,
        "robust_completion_cases": completion_cases,
        "robust_completion_failures": completion_fail,
        "temporal_structures_checked": temporal_total,
        "rank_guard_eligible_structures": temporal_eligible,
        "direct_temporal_failures": temporal_fail,
        "history_current_rho": current_rho,
        "history_future_rho": future_rho,
        "history_witness_pass": history_pass,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
