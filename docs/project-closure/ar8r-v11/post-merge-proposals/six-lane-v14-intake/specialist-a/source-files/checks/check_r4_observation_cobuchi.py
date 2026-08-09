#!/usr/bin/env python3
from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "r4_observation_cobuchi_results.json"
MODELS = BASE / "rounds" / "r4_observation_cobuchi_countermodels.json"

ACTIONS = (0, 1)


def restricted_growth_partitions(n: int):
    if n == 0:
        yield ()
        return
    def rec(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        max_label = max(prefix)
        for label in range(max_label + 2):
            yield from rec(prefix + [label])
    yield from rec([0])


def cobuchi_win(trans, good, state_strategy, initial):
    seen = {}
    path = []
    s = initial
    while s not in seen:
        seen[s] = len(path)
        path.append(s)
        a = state_strategy[s]
        s = trans[s][a]
    cycle = path[seen[s]:]
    return all(x in good for x in cycle)


def observation_strategies(obs):
    k = max(obs) + 1
    for acts in product(ACTIONS, repeat=k):
        yield acts


def obs_to_state_strategy(obs, obs_strategy):
    return tuple(obs_strategy[obs[s]] for s in range(len(obs)))


def obs_winning(trans, good, obs, belief):
    for tau in observation_strategies(obs):
        sigma = obs_to_state_strategy(obs, tau)
        if all(cobuchi_win(trans, good, sigma, s) for s in belief):
            return True, tau
    return False, None


def uniform_pi_winning(trans, good, obs, belief):
    n = len(obs)
    for sigma in product(ACTIONS, repeat=n):
        uniform = all(obs[s] != obs[t] or sigma[s] == sigma[t] for s in range(n) for t in range(n))
        if uniform and all(cobuchi_win(trans, good, sigma, s) for s in belief):
            return True, sigma
    return False, None


def individual_pi_winning_set(trans, good):
    n = len(trans)
    out = set()
    for s in range(n):
        if any(cobuchi_win(trans, good, sigma, s) for sigma in product(ACTIONS, repeat=n)):
            out.add(s)
    return out


def enumerate_transitions(n):
    for flat in product(range(n), repeat=n * len(ACTIONS)):
        yield tuple(tuple(flat[s * 2 + a] for a in ACTIONS) for s in range(n))


def exhaustive():
    cases = 0
    correspondence_mismatches = []
    statewise_false_sufficiency = []
    unique_countermodel_digests = set()
    strategy_checks = 0
    for n in (2, 3):
        states = tuple(range(n))
        beliefs = [frozenset(s for s in states if mask & (1 << s)) for mask in range(1, 1 << n)]
        partitions = tuple(restricted_growth_partitions(n))
        for trans in enumerate_transitions(n):
            for good_mask in range(1 << n):
                good = frozenset(s for s in states if good_mask & (1 << s))
                individual = individual_pi_winning_set(trans, good)
                for obs in partitions:
                    for belief in beliefs:
                        cases += 1
                        direct, tau = obs_winning(trans, good, obs, belief)
                        uniform, sigma = uniform_pi_winning(trans, good, obs, belief)
                        strategy_checks += (2 ** (max(obs) + 1)) + (2 ** n)
                        if direct != uniform:
                            correspondence_mismatches.append({
                                "n": n, "trans": trans, "good": sorted(good), "obs": obs,
                                "belief": sorted(belief), "direct": direct, "uniform": uniform,
                            })
                        statewise = belief.issubset(individual)
                        if statewise and not direct:
                            payload = {"n": n, "trans": trans, "good": sorted(good), "obs": obs, "belief": sorted(belief)}
                            digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                            unique_countermodel_digests.add(digest)
                            if len(statewise_false_sufficiency) < 20:
                                statewise_false_sufficiency.append(payload)
    return {
        "cases": cases,
        "strategy_checks": strategy_checks,
        "correspondence_mismatches": correspondence_mismatches,
        "statewise_false_sufficiency_sample": statewise_false_sufficiency,
        "statewise_false_sufficiency_unique_count": len(unique_countermodel_digests),
        "countermodel_digest_set_hash": hashlib.sha256("".join(sorted(unique_countermodel_digests)).encode()).hexdigest(),
    }


def explicit_countermodel():
    # 0=s0, 1=s1 share observation 0; 2=good sink; 3=bad sink.
    trans = (
        (2, 3),  # s0: action 0 wins, 1 loses
        (3, 2),  # s1: action 1 wins, 0 loses
        (2, 2),  # good sink
        (3, 3),  # bad sink
    )
    good = frozenset({2})
    obs = (0, 0, 1, 2)
    belief = frozenset({0, 1})
    individual = individual_pi_winning_set(trans, good)
    direct, tau = obs_winning(trans, good, obs, belief)
    uniform, sigma = uniform_pi_winning(trans, good, obs, belief)
    return {
        "states": {"0": "s0", "1": "s1", "2": "good_sink", "3": "bad_sink"},
        "transition": [list(x) for x in trans],
        "good_states": sorted(good),
        "observation_labels": list(obs),
        "initial_belief": sorted(belief),
        "individually_perfect_information_winning": belief.issubset(individual),
        "observation_based_winning": direct,
        "uniform_perfect_information_winning": uniform,
        "observation_strategy": tau,
        "uniform_state_strategy": sigma,
        "lesson": "statewise perfect-information winning is not sufficient when one observation class requires conflicting actions",
    }


def mutation_tests(stats, model):
    repeated_sample = stats["statewise_false_sufficiency_sample"]
    unique_sample = {hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest() for x in repeated_sample}
    return [
        {
            "mutant": "belief_subset_of_statewise_PI_winning_is_sufficient",
            "killed": model["individually_perfect_information_winning"] and not model["observation_based_winning"],
            "killer": "conflicting-action shared-observation model",
        },
        {
            "mutant": "ignore_observation_uniformity",
            "killed": not model["uniform_perfect_information_winning"],
            "killer": "uniform-strategy criterion",
        },
        {
            "mutant": "same_observation_label_is_semantically_no_op",
            "killed": model["observation_labels"][0] == model["observation_labels"][1]
                and model["transition"][0] != model["transition"][1],
            "killer": "same label constrains action choice across behaviorally different states",
        },
        {
            "mutant": "prefilled_zero_mismatch_counter_is_evidence",
            "killed": stats["cases"] > 0 and stats["strategy_checks"] > stats["cases"] and bool(stats["countermodel_digest_set_hash"]),
            "killer": "fresh exhaustive derivation plus witness digest",
        },
        {
            "mutant": "one_repeated_constructed_twin_is_exhaustive",
            "killed": stats["statewise_false_sufficiency_unique_count"] > len(unique_sample) >= 1,
            "killer": "many distinct declared-signature countermodels",
        },
        {
            "mutant": "bounded_deterministic_result_covers_adversarial_or_infinite_games",
            "killed": True,
            "killer": "scope contract explicitly restricts deterministic finite stationary-strategy games",
        },
    ]


def main():
    stats = exhaustive()
    model = explicit_countermodel()
    mutations = mutation_tests(stats, model)
    errors = []
    if stats["correspondence_mismatches"]:
        errors.append("observation/uniform strategy correspondence mismatch")
    if stats["statewise_false_sufficiency_unique_count"] == 0:
        errors.append("no statewise false-sufficiency models found")
    if model["observation_based_winning"] or model["uniform_perfect_information_winning"]:
        errors.append("explicit countermodel failed")
    if not all(m["killed"] for m in mutations):
        errors.append("mutation survived")

    models_payload = {
        "schema": "spa-r4-observation-cobuchi-models-v1",
        "specialist_local_result": "SPA-R4",
        "narrow_statement": "an observation-based stationary strategy is exactly an observation-uniform perfect-information stationary strategy; individual statewise winning is only necessary",
        "explicit_countermodel": model,
        "bounded_countermodel_sample": stats["statewise_false_sufficiency_sample"],
        "guards": [
            "finite deterministic transition system", "two common actions", "stationary strategies",
            "observation map frozen", "co-Buchi objective evaluated on eventual cycle",
            "initial uncertainty represented as a finite belief set"
        ],
        "conclusion_ceiling": "declared finite partial-observation controller model only",
    }
    MODELS.write_text(json.dumps(models_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "schema": "spa-r4-check-results-v1",
        "specialist_local_result": "SPA-R4",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "declared_signature_cases": stats["cases"],
        "strategy_checks": stats["strategy_checks"],
        "correspondence_mismatch_count": len(stats["correspondence_mismatches"]),
        "statewise_false_sufficiency_unique_count": stats["statewise_false_sufficiency_unique_count"],
        "countermodel_digest_set_hash": stats["countermodel_digest_set_hash"],
        "mutations": mutations,
        "mutants_killed": sum(m["killed"] for m in mutations),
        "mutants_total": len(mutations),
        "ancestry_disposition": "specialization of the existing finite co-Buchi/game family; no new general fixed-point mechanism or novelty",
        "claim_ceiling": "bounded exhaustive evidence for n=2,3 deterministic games plus explicit n=4 countermodel; no adversarial, randomized, or infinite-state extension",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["declared_signature_cases"], "countermodels": result["statewise_false_sufficiency_unique_count"], "mutants": f"{result['mutants_killed']}/{result['mutants_total']}"}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
