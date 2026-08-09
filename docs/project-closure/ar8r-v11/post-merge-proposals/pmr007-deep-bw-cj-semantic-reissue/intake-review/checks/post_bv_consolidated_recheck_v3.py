#!/usr/bin/env python3
"""Recheck BW-CJ while replacing the rejected V2 CI/CJ repetition.

V3 preserves BW-CH's bounded V2 results, but it does not count repeated
randomly constructed CI/CJ twins as independent evidence.  CI and CJ are
checked exhaustively over their declared finite signatures.  The checker also
runs explicit predicate mutants so a tautological OR, an ignored target, or an
identity-only comparison cannot pass as the intended fibre criterion.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROUNDS_BEFORE_CI = ["BW", "BX", "BY", "BZ", "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH"]


def run_v2_prefix() -> dict:
    here = Path(__file__).resolve().parent
    source = here / "post_bv_consolidated_recheck_v2.py"
    with tempfile.TemporaryDirectory() as temporary:
        temporary = Path(temporary)
        copied = temporary / source.name
        shutil.copy2(source, copied)
        completed = subprocess.run(
            [sys.executable, str(copied)],
            cwd=temporary,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        result = temporary / "post_bv_consolidated_recheck_v2_results.json"
        if completed.returncode != 0 or not result.is_file():
            raise RuntimeError("bounded V2 prefix failed to reproduce")
        document = json.loads(result.read_text(encoding="utf-8"))
    return {round_id: document["results"][round_id] for round_id in ROUNDS_BEFORE_CI}


def complete_profile(world: dict) -> tuple:
    return tuple(world["output_laws"])


def target_leaking_profile(world: dict) -> tuple:
    return complete_profile(world) + (world["target"],)


def fibre_collision(left: dict, right: dict, projection=complete_profile) -> bool:
    return projection(left) == projection(right) and left["target"] != right["target"]


def mutant_or(left: dict, right: dict, projection=complete_profile) -> bool:
    return projection(left) == projection(right) or left["target"] != right["target"]


def mutant_ignore_target(left: dict, right: dict, projection=complete_profile) -> bool:
    return projection(left) == projection(right)


def mutant_identity_only(left: dict, right: dict, projection=complete_profile) -> bool:
    return left is right and projection(left) == projection(right) and left["target"] != right["target"]


def predicate_mutation_receipt(positive: tuple[dict, dict], changed_profile: tuple[dict, dict], same_target: tuple[dict, dict]) -> dict:
    cases = {
        "positive": positive,
        "changed_profile": changed_profile,
        "same_target": same_target,
    }
    expected = {"positive": True, "changed_profile": False, "same_target": False}
    predicates = {
        "correct": fibre_collision,
        "or_mutant": mutant_or,
        "ignore_target_mutant": mutant_ignore_target,
        "identity_only_mutant": mutant_identity_only,
    }
    outcomes = {
        name: {case: predicate(*pair) for case, pair in cases.items()}
        for name, predicate in predicates.items()
    }
    killed = {
        name: any(outcomes[name][case] != expected[case] for case in cases)
        for name in predicates
        if name != "correct"
    }
    return {
        "expected": expected,
        "outcomes": outcomes,
        "mutants_killed": killed,
        "correct_matches_expected": outcomes["correct"] == expected,
        "all_declared_mutants_killed": all(killed.values()),
    }


def recheck_ci() -> dict:
    row = {
        "declared_profiles": 0,
        "content_sensitive": 0,
        "content_insensitive": 0,
        "exhaustive_target_fibre_witnesses": 0,
        "witness_failures": 0,
        "target_leak_controls": 0,
        "target_leak_false_positives": 0,
        "profile_change_controls": 0,
        "profile_change_false_positives": 0,
        "same_target_controls": 0,
        "same_target_false_positives": 0,
    }
    first_cases = None
    for profile in itertools.product(range(5), repeat=6):
        row["declared_profiles"] += 1
        sensitive = any(len({profile[2 * content + guard] for content in range(3)}) > 1 for guard in range(2))
        row["content_sensitive"] += int(sensitive)
        row["content_insensitive"] += int(not sensitive)

        impersonal = {"output_laws": profile, "target": 0}
        intentional = {"output_laws": profile, "target": 1}
        changed = list(profile)
        changed[0] = (changed[0] + 1) % 5
        changed_profile = {"output_laws": tuple(changed), "target": 1}
        same_target = {"output_laws": profile, "target": 0}

        row["exhaustive_target_fibre_witnesses"] += 1
        row["witness_failures"] += int(not fibre_collision(impersonal, intentional))
        row["target_leak_controls"] += 1
        row["target_leak_false_positives"] += int(fibre_collision(impersonal, intentional, target_leaking_profile))
        row["profile_change_controls"] += 1
        row["profile_change_false_positives"] += int(fibre_collision(impersonal, changed_profile))
        row["same_target_controls"] += 1
        row["same_target_false_positives"] += int(fibre_collision(impersonal, same_target))
        if first_cases is None:
            first_cases = ((impersonal, intentional), (impersonal, changed_profile), (impersonal, same_target))

    row["predicate_mutation_receipt"] = predicate_mutation_receipt(*first_cases)
    row["authority"] = "EXHAUSTIVE_DECLARED_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION"
    row["pass"] = (
        row["declared_profiles"] == 15625
        and row["exhaustive_target_fibre_witnesses"] == 15625
        and row["witness_failures"] == 0
        and row["target_leak_false_positives"] == 0
        and row["profile_change_false_positives"] == 0
        and row["same_target_false_positives"] == 0
        and row["content_insensitive"] == 25
        and row["predicate_mutation_receipt"]["correct_matches_expected"]
        and row["predicate_mutation_receipt"]["all_declared_mutants_killed"]
    )
    return row


def fittingness_sensitive(profile: tuple[int, ...]) -> bool:
    return any(
        profile[(content * 2 + 0) * 2 + payoff] != profile[(content * 2 + 1) * 2 + payoff]
        for content in range(2)
        for payoff in range(2)
    )


def registered_payoff_independent(profile: tuple[int, ...]) -> bool:
    return all(
        profile[(content * 2 + fittingness) * 2 + 0] == profile[(content * 2 + fittingness) * 2 + 1]
        for content in range(2)
        for fittingness in range(2)
    )


def recheck_cj() -> dict:
    row = {
        "declared_profiles": 0,
        "fittingness_sensitive": 0,
        "registered_payoff_independent": 0,
        "eligible_profiles": 0,
        "exhaustive_personal_impersonal_witnesses": 0,
        "eligibility_recheck_failures": 0,
        "witness_failures": 0,
        "target_leak_controls": 0,
        "target_leak_false_positives": 0,
        "profile_change_controls": 0,
        "profile_change_false_positives": 0,
        "same_target_controls": 0,
        "same_target_false_positives": 0,
        "ineligible_profiles_rejected": 0,
    }
    first_cases = None
    for profile in itertools.product(range(3), repeat=8):
        row["declared_profiles"] += 1
        sensitive = fittingness_sensitive(profile)
        payoff_independent = registered_payoff_independent(profile)
        row["fittingness_sensitive"] += int(sensitive)
        row["registered_payoff_independent"] += int(payoff_independent)
        if not (sensitive and payoff_independent):
            row["ineligible_profiles_rejected"] += 1
            continue

        row["eligible_profiles"] += 1
        impersonal = {"output_laws": profile, "target": ("impersonal", False)}
        personal = {"output_laws": profile, "target": ("personal", True)}
        changed = list(profile)
        changed[0] = (changed[0] + 1) % 3
        changed_profile = {"output_laws": tuple(changed), "target": ("personal", True)}
        same_target = {"output_laws": profile, "target": ("impersonal", False)}

        row["exhaustive_personal_impersonal_witnesses"] += 1
        row["eligibility_recheck_failures"] += int(not (fittingness_sensitive(impersonal["output_laws"]) and registered_payoff_independent(impersonal["output_laws"])))
        row["eligibility_recheck_failures"] += int(not (fittingness_sensitive(personal["output_laws"]) and registered_payoff_independent(personal["output_laws"])))
        row["witness_failures"] += int(not fibre_collision(impersonal, personal))
        row["target_leak_controls"] += 1
        row["target_leak_false_positives"] += int(fibre_collision(impersonal, personal, target_leaking_profile))
        row["profile_change_controls"] += 1
        row["profile_change_false_positives"] += int(fibre_collision(impersonal, changed_profile))
        row["same_target_controls"] += 1
        row["same_target_false_positives"] += int(fibre_collision(impersonal, same_target))
        if first_cases is None:
            first_cases = ((impersonal, personal), (impersonal, changed_profile), (impersonal, same_target))

    row["predicate_mutation_receipt"] = predicate_mutation_receipt(*first_cases)
    row["authority"] = "EXHAUSTIVE_ELIGIBLE_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION"
    row["pass"] = (
        row["declared_profiles"] == 6561
        and row["eligible_profiles"] > 0
        and row["ineligible_profiles_rejected"] > 0
        and row["exhaustive_personal_impersonal_witnesses"] == row["eligible_profiles"]
        and row["eligibility_recheck_failures"] == 0
        and row["witness_failures"] == 0
        and row["target_leak_false_positives"] == 0
        and row["profile_change_false_positives"] == 0
        and row["same_target_false_positives"] == 0
        and row["predicate_mutation_receipt"]["correct_matches_expected"]
        and row["predicate_mutation_receipt"]["all_declared_mutants_killed"]
    )
    return row


def main() -> int:
    output = {
        "schema": "pmr007-post-bv-consolidated-recheck-v3",
        "seed": 20260805,
        "v2_ci_cj_disposition": "REJECTED_TAUTOLOGICAL_REPETITION_NOT_INDEPENDENT_EVIDENCE",
        "authority": "BOUNDED_FINITE_SIGNATURE_WITNESSES_ONLY",
        "results": run_v2_prefix(),
    }
    output["results"]["CI"] = recheck_ci()
    output["results"]["CJ"] = recheck_cj()
    output["overall_pass"] = all(row.get("pass") is True for row in output["results"].values())
    target = Path(__file__).with_name("post_bv_consolidated_recheck_v3_results.json")
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
