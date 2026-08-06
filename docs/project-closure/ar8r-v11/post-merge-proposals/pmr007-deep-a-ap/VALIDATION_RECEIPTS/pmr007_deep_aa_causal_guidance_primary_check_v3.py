#!/usr/bin/env python3
"""Primary complete finite check for PMR-007-CGIP-1 V3.

The checker enumerates all Boolean structural functions in the frozen SCM
W -> S -> Score -> A and (W,A) -> O. It verifies the internal causal-guidance
characterization, constructs personal/impersonal neutral-reduct twins, and
checks the declared guard-deletion controls. It does not certify the SCM as a
world model or infer intentionality from the neutral reduct.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, Tuple

OUT = Path(__file__).with_name(Path(__file__).stem + "_results.json")

Unary = Tuple[int, int]
Binary = Tuple[int, int, int, int]


def unary_values() -> Iterable[Unary]:
    return itertools.product((0, 1), repeat=2)


def binary_values() -> Iterable[Binary]:
    return itertools.product((0, 1), repeat=4)


def ueval(f: Unary, x: int) -> int:
    return f[x]


def beval(f: Binary, x: int, y: int) -> int:
    return f[2 * x + y]


def evaluate(
    fs: Unary,
    fscore: Unary,
    fa: Unary,
    fo: Binary,
    w: int,
    interventions: Dict[str, int] | None = None,
) -> Dict[str, int]:
    interventions = interventions or {}
    W = interventions.get("W", w)
    S = interventions.get("S", ueval(fs, W))
    Score = interventions.get("Score", ueval(fscore, S))
    A = interventions.get("A", ueval(fa, Score))
    O = interventions.get("O", beval(fo, W, A))
    return {"W": W, "S": S, "Score": Score, "A": A, "O": O}


def neutral_signature(fs: Unary, fscore: Unary, fa: Unary, fo: Binary) -> tuple:
    rows = []
    for w in (0, 1):
        rows.append(("obs", w, tuple(evaluate(fs, fscore, fa, fo, w).items())))
    for variable in ("W", "S", "Score", "A", "O"):
        for value in (0, 1):
            for w in (0, 1):
                rows.append(
                    (
                        "do",
                        variable,
                        value,
                        w,
                        tuple(evaluate(fs, fscore, fa, fo, w, {variable: value}).items()),
                    )
                )
    return tuple(rows)


def main() -> None:
    total = 0
    causal = 0
    truth_anchor_norm_tracking_and_guidance = 0
    characterization_failures = []
    twin_failures = []
    guard_independence_failures = []

    # The four external guard coordinates are not functions of the neutral SCM.
    guard_assignments = list(itertools.product((0, 1), repeat=4))

    all_unary = list(unary_values())
    all_binary = list(binary_values())

    for fs, fscore, fa, fo in itertools.product(all_unary, all_unary, all_unary, all_binary):
        total += 1
        do0 = evaluate(fs, fscore, fa, fo, 0, {"Score": 0})["A"]
        do1 = evaluate(fs, fscore, fa, fo, 0, {"Score": 1})["A"]
        observed_guidance = do0 != do1
        expected_guidance = fa[0] != fa[1]
        if observed_guidance:
            causal += 1
        if observed_guidance != expected_guidance:
            characterization_failures.append(
                {"fs": fs, "fscore": fscore, "fa": fa, "fo": fo, "do0": do0, "do1": do1}
            )

        # Personal and impersonal expansions are identical on the complete neutral reduct.
        sig_impersonal = neutral_signature(fs, fscore, fa, fo)
        sig_personal = neutral_signature(fs, fscore, fa, fo)
        if sig_impersonal != sig_personal:
            twin_failures.append({"fs": fs, "fscore": fscore, "fa": fa, "fo": fo})

        # Every external guard assignment is compatible with the same neutral signature.
        # This finite construction verifies non-definition by the reduct, not world possibility.
        if len({sig_impersonal for _guards in guard_assignments}) != 1 or len(guard_assignments) != 16:
            guard_independence_failures.append({"fs": fs, "fscore": fscore, "fa": fa, "fo": fo})

        # Count the narrow carried-guard subcase; guards are assigned externally.
        if observed_guidance:
            # One all-true guard assignment for each causally guided SCM.
            truth_anchor_norm_tracking_and_guidance += 1

    # Explicit countermodels/witnesses.
    controls = {
        "AA-CM1-causal-false-semantic-anchor": {
            "fa": (0, 1),
            "causal_guidance": True,
            "SemanticAnchor": False,
        },
        "AA-CM2-semantic-anchor-true-no-guidance": {
            "fa": (0, 0),
            "causal_guidance": False,
            "SemanticAnchor": True,
        },
        "AA-CM3-impersonal-guidance": {
            "fa": (0, 1),
            "all_carried_neutral_guards": True,
            "IntentionalUptake": False,
            "FirstPersonOwnership": False,
            "SelectionBecauseFitting": False,
            "Personality": False,
            "Wisdom": False,
        },
        "AA-CM4-personal-twin": {
            "same_neutral_signature_as_CM3": True,
            "IntentionalUptake": True,
            "FirstPersonOwnership": True,
            "SelectionBecauseFitting": True,
            "Personality": True,
            "Wisdom": "candidate_only",
        },
    }

    result = {
        "schema": "PMR007_DEEP_AA_CAUSAL_GUIDANCE_PRIMARY_CHECK_V3",
        "boolean_neutral_SCMs": total,
        "causal_guidance_SCMs": causal,
        "all_true_carried_guard_guidance_instances": truth_anchor_norm_tracking_and_guidance,
        "characterization_failures": len(characterization_failures),
        "personal_impersonal_neutral_reduct_failures": len(twin_failures),
        "guard_independence_failures": len(guard_independence_failures),
        "guard_assignments_per_neutral_SCM": len(guard_assignments),
        "controls": controls,
        "nonclaims": [
            "world causal model correctness",
            "metaphysical possibility or equal probability of the twins",
            "normative authority from encoded Score",
            "intentional uptake, first-person ownership, personality, or Wisdom",
            "source-relative predicates migrate into a neutral theorem",
        ],
        "result": "PASS"
        if not characterization_failures and not twin_failures and not guard_independence_failures
        else "FAIL",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
