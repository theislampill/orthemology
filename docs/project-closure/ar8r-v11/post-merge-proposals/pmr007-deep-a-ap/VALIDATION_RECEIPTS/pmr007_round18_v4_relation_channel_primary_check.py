from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import math
import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "PMR007_ROUND18_CERTIFICATE_OBJECT_REFINEMENT_V4.yaml"
OUT = Path(__file__).with_name("pmr007_round18_v4_relation_channel_primary_check_results.json")


def rho_cover(good: list[set[int]], m: int) -> float | int:
    if any(not s for s in good):
        return math.inf
    for k in range(1, m + 1):
        for chosen in combinations(range(m), k):
            if all(s.intersection(chosen) for s in good):
                return k
    return math.inf


def brute_exact_state_alphabet(good: list[set[int]]) -> float | int:
    if any(not s for s in good):
        return math.inf
    best = math.inf
    for outputs in product(*[tuple(sorted(s)) for s in good]):
        best = min(best, len(set(outputs)))
    return best


def canonical_partitions(n: int):
    """Restricted-growth strings enumerating all set partitions of range(n)."""
    if n == 0:
        yield ()
        return
    a = [0] * n

    def rec(i: int, max_seen: int):
        if i == n:
            yield tuple(a)
            return
        for v in range(max_seen + 2):
            a[i] = v
            yield from rec(i + 1, max(max_seen, v))

    a[0] = 0
    yield from rec(1, 0)


def compatible_for_assignment(
    good: list[set[int]], obs: tuple[int, ...], enc: tuple[int, ...], msg_by_enc: tuple[int, ...]
) -> bool:
    buckets: dict[tuple[int, int], list[int]] = {}
    for q in range(len(good)):
        buckets.setdefault((obs[q], msg_by_enc[enc[q]]), []).append(q)
    for states in buckets.values():
        inter = set(good[states[0]])
        for q in states[1:]:
            inter &= good[q]
        if not inter:
            return False
    return True


def min_compatible_messages(good: list[set[int]], obs: tuple[int, ...], enc: tuple[int, ...]) -> float | int:
    if any(not s for s in good):
        return math.inf
    r = max(enc) + 1
    for k in range(1, r + 1):
        for msg_by_enc in product(range(k), repeat=r):
            if compatible_for_assignment(good, obs, enc, msg_by_enc):
                return len(set(msg_by_enc))
    return math.inf


def direct_protocol_exists(
    good: list[set[int]], obs: tuple[int, ...], enc: tuple[int, ...], k: int, m_objects: int
) -> bool:
    """Directly enumerate encoder maps and decoder maps, independent of intersection shortcut."""
    r = max(enc) + 1
    obs_vals = sorted(set(obs))
    decoder_slots = [(o, msg) for o in obs_vals for msg in range(k)]
    for msg_by_enc in product(range(k), repeat=r):
        for decoder_values in product(range(m_objects), repeat=len(decoder_slots)):
            dec = dict(zip(decoder_slots, decoder_values))
            if all(dec[(obs[q], msg_by_enc[enc[q]])] in good[q] for q in range(len(good))):
                return True
    return False


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def relation_intersection_condition(code: list[str], good: list[set[int]], radius: int) -> bool:
    n = len(code[0])
    for y in map("".join, product("01", repeat=n)):
        ambiguity = [q for q, cw in enumerate(code) if hamming(cw, y) <= radius]
        if not ambiguity:
            continue
        inter = set(good[ambiguity[0]])
        for q in ambiguity[1:]:
            inter &= good[q]
        if not inter:
            return False
    return True


def direct_relation_decoder_exists(code: list[str], good: list[set[int]], radius: int, m_objects: int) -> bool:
    n = len(code[0])
    received = list(map("".join, product("01", repeat=n)))
    for outputs in product(range(m_objects), repeat=len(received)):
        dec = dict(zip(received, outputs))
        ok = True
        for q, cw in enumerate(code):
            for y in received:
                if hamming(cw, y) <= radius and dec[y] not in good[q]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return True
    return False


def max_binary_code_size(length: int, distance: int) -> int:
    words = list(map("".join, product("01", repeat=length)))
    compat = [[hamming(words[i], words[j]) >= distance for j in range(len(words))] for i in range(len(words))]
    best = 0

    def search(candidates: list[int], chosen: int):
        nonlocal best
        if chosen + len(candidates) <= best:
            return
        if not candidates:
            best = max(best, chosen)
            return
        v = candidates[0]
        with_v = [u for u in candidates[1:] if compat[v][u]]
        search(with_v, chosen + 1)
        search(candidates[1:], chosen)

    search(list(range(len(words))), 0)
    return best


def rank_admissible_objects(model: dict) -> dict[str, list[str]]:
    tw = model["temporal_witness"]
    rank = tw["rank"]
    target = set(tw["target"])
    safe = set(tw["safe"])
    out: dict[str, list[str]] = {q: [] for q in tw["states"]}
    for q in tw["states"]:
        for obj, fields in tw["objects"].items():
            action = fields["action"]
            if action not in tw["transitions"].get(q, {}):
                continue
            succ = tw["transitions"][q][action]
            ok = bool(succ) and set(succ) <= safe
            if q in target:
                ok = ok and all(rank[x] <= rank[q] for x in succ)
            else:
                ok = ok and all(rank[x] < rank[q] for x in succ)
            if ok:
                out[q].append(obj)
    return out


def direct_cobuchi(tw: dict, policy: dict[str, str]) -> bool:
    graph: dict[str, list[str]] = {}
    for q, obj in policy.items():
        action = tw["objects"][obj]["action"]
        graph[q] = list(tw["transitions"][q][action])
    target = set(tw["target"])
    # A finite graph satisfies universal co-Buchi from all states iff every cyclic SCC is target-only.
    idx = 0
    stack: list[str] = []
    on: set[str] = set()
    ind: dict[str, int] = {}
    low: dict[str, int] = {}
    comps: list[list[str]] = []

    def dfs(v: str):
        nonlocal idx
        ind[v] = low[v] = idx
        idx += 1
        stack.append(v)
        on.add(v)
        for w in graph[v]:
            if w not in ind:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], ind[w])
        if low[v] == ind[v]:
            comp: list[str] = []
            while True:
                w = stack.pop()
                on.remove(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for q in tw["states"]:
        if q not in ind:
            dfs(q)
    for comp in comps:
        cyclic = len(comp) > 1 or comp[0] in graph[comp[0]]
        if cyclic and not set(comp) <= target:
            return False
    return True


def main() -> None:
    model = yaml.safe_load(MODEL.read_text())
    failures: list[str] = []

    # Exact-state support-cover equality over all 3-object families through 5 states.
    subsets3 = [set(i for i in range(3) if mask >> i & 1) for mask in range(8)]
    exact_cases = 0
    exact_mismatches = 0
    for n in range(1, 6):
        for fam in product(subsets3, repeat=n):
            exact_cases += 1
            if rho_cover(list(fam), 3) != brute_exact_state_alphabet(list(fam)):
                exact_mismatches += 1
    if exact_mismatches:
        failures.append("ORTC-EXACT mismatch")

    # General encoder-information theorem: exhaustive n=3, two objects, all obs/encoder partitions.
    subsets2 = [set(i for i in range(2) if mask >> i & 1) for mask in range(4)]
    partitions3 = list(canonical_partitions(3))
    info_cases = 0
    info_mismatches = 0
    for fam in product(subsets2, repeat=3):
        good = list(fam)
        for obs in partitions3:
            for enc in partitions3:
                info_cases += 1
                predicted = min_compatible_messages(good, obs, enc)
                direct = math.inf
                for k in range(1, max(enc) + 2):
                    if direct_protocol_exists(good, obs, enc, k, 2):
                        direct = k
                        break
                if predicted != direct:
                    info_mismatches += 1
    if info_mismatches:
        failures.append("ORTC-INFO mismatch")

    # Adversarial relation criterion over all 3-state, 2-object families and all binary length-2 encoders.
    relation_cases = 0
    relation_mismatches = 0
    codewords2 = list(map("".join, product("01", repeat=2)))
    for fam in product(subsets2, repeat=3):
        good = list(fam)
        for code in product(codewords2, repeat=3):
            for radius in (0, 1):
                relation_cases += 1
                criterion = relation_intersection_condition(list(code), good, radius)
                direct = direct_relation_decoder_exists(list(code), good, radius, 2)
                if criterion != direct:
                    relation_mismatches += 1
    if relation_mismatches:
        failures.append("ORTC-ERROR-RELATION mismatch")

    # Strict relation-vs-label witness.
    aw = model["adversarial_relation_witness"]
    obj_index = {k: i for i, k in enumerate(aw["objects"])}
    strict_good = [{obj_index[k] for k in aw["admissible"][q]} for q in aw["states"]]
    strict_code = [aw["binary_code"][q] for q in aw["states"]]
    strict_relation = relation_intersection_condition(strict_code, strict_good, aw["adversarial_hamming_radius"])
    capacities = {str(n): max_binary_code_size(n, 3) for n in range(1, 6)}
    exact_binary_label_min = next(n for n in range(1, 6) if capacities[str(n)] >= 2)
    exact_four_label_min = next(n for n in range(1, 6) if capacities[str(n)] >= 4)
    if not strict_relation or exact_binary_label_min != 3 or exact_four_label_min != 5:
        failures.append("strict relation/label witness")

    # Model examples, projection and completion intersection.
    example_results = []
    for ex in model["examples"]:
        objects = ex["objects"]
        index = {k: i for i, k in enumerate(objects)}
        good = [{index[k] for k in ex["admissible"][q]} for q in ex["states"]]
        rr = rho_cover(good, len(objects))
        row = {"id": ex["id"], "object_rho": "infinity" if rr == math.inf else rr}
        if "action_projection" in ex:
            actions = sorted(set(ex["action_projection"].values()))
            ai = {a: i for i, a in enumerate(actions)}
            agood = [{ai[ex["action_projection"][k]] for k in ex["admissible"][q]} for q in ex["states"]]
            ar = rho_cover(agood, len(actions))
            row["action_rho"] = "infinity" if ar == math.inf else ar
        example_results.append(row)
    projection_pass = next(x for x in example_results if x["id"] == "R18-CM-OBJECT-PROJECTION") == {
        "id": "R18-CM-OBJECT-PROJECTION",
        "object_rho": 2,
        "action_rho": 1,
    }
    rc = model["robust_completion_witness"]
    completion_sets = [set(v) for v in rc["completion_admissible"].values()]
    completion_union = set().union(*completion_sets)
    completion_intersection = set.intersection(*completion_sets)
    completion_pass = sorted(completion_union) == rc["expected_union"] and sorted(completion_intersection) == rc["expected_intersection"]
    if not projection_pass or not completion_pass:
        failures.append("projection/completion witness")

    # Named temporal rank witness and direct semantics.
    admissible = rank_admissible_objects(model)
    tw = model["temporal_witness"]
    temporal_expected = tw["expected_admissible"]
    temporal_match = admissible == temporal_expected
    policy_count = 0
    temporal_failures = 0
    for choices in product(*[admissible[q] for q in tw["states"]]):
        policy_count += 1
        policy = dict(zip(tw["states"], choices))
        if not direct_cobuchi(tw, policy):
            temporal_failures += 1
    hw = model["history_witness"]
    history_current_rho = rho_cover([{0}, {0}], 1)
    history_future_rho = rho_cover([{0}, {1}], 2)
    history_pass = history_current_rho == hw["expected_current_rho"] and history_future_rho == hw["expected_future_rho"]
    if not temporal_match or temporal_failures or not history_pass:
        failures.append("temporal/history witness")

    result = {
        "schema": "PMR007_ROUND18_V4_PRIMARY_CHECK",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "exact_state_relations_checked": exact_cases,
        "exact_state_relation_mismatches": exact_mismatches,
        "general_encoder_information_cases": info_cases,
        "general_encoder_information_mismatches": info_mismatches,
        "adversarial_relation_channel_cases": relation_cases,
        "adversarial_relation_channel_mismatches": relation_mismatches,
        "binary_code_capacity_min_distance_3": capacities,
        "strict_relation_selector_possible_with_2_bits": strict_relation,
        "exact_nonconstant_binary_label_minimum_bits_under_one_flip": exact_binary_label_min,
        "exact_four_state_label_minimum_bits_under_one_flip": exact_four_label_min,
        "examples": example_results,
        "projection_strict_witness_pass": projection_pass,
        "robust_completion_intersection_pass": completion_pass,
        "temporal_rank_admissible": admissible,
        "temporal_rank_match": temporal_match,
        "rank_admissible_policies_checked": policy_count,
        "direct_temporal_failures": temporal_failures,
        "history_current_rho": history_current_rho,
        "history_future_rho": history_future_rho,
        "history_witness_pass": history_pass,
        "scope": [
            "finite complete certificate-object relations",
            "finite deterministic encoder and decoder information",
            "pointwise zero-error relation selection",
            "fixed binary adversarial Hamming channel",
            "fixed finite perfect-information rank certificate",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
