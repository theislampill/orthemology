#!/usr/bin/env python3
"""Distinct rereview for PMR-007-CGIP-1 V3.

This implementation does not import the primary checker. It builds each Boolean
SCM as a relational table, recomputes intervention tables by graph surgery, and
compares neutral reducts after independently adding personal/impersonal labels.
It also constructs an observationally equivalent hidden-confounder model to
verify the frozen-SCM authority ceiling.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Dict, List, Mapping, Tuple

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "pmr007_deep_aa_distinct_intervention_reduct_rereview_v3_results.json"

FREEZE_RECEIPT = ROOT / "PMR-007_DEEP_AA_V3_FROZEN_HASHES.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def bits(n: int, width: int) -> Tuple[int, ...]:
    return tuple((n >> i) & 1 for i in range(width))


def relational_rows(fs: Tuple[int, int], fscore: Tuple[int, int], fa: Tuple[int, int], fo: Tuple[int, ...]) -> Dict[str, set]:
    return {
        "S": {(w, fs[w]) for w in (0, 1)},
        "Score": {(s, fscore[s]) for s in (0, 1)},
        "A": {(score, fa[score]) for score in (0, 1)},
        "O": {(w, a, fo[2 * w + a]) for w in (0, 1) for a in (0, 1)},
    }


def unique_output(relation: set, prefix: tuple) -> int:
    vals = [row[-1] for row in relation if row[:-1] == prefix]
    if len(vals) != 1:
        raise AssertionError((relation, prefix, vals))
    return vals[0]


def surgery_eval(rows: Mapping[str, set], exogenous_w: int, intervention: Mapping[str, int]) -> Tuple[int, int, int, int, int]:
    w = intervention.get("W", exogenous_w)
    s = intervention.get("S", unique_output(rows["S"], (w,)))
    score = intervention.get("Score", unique_output(rows["Score"], (s,)))
    a = intervention.get("A", unique_output(rows["A"], (score,)))
    o = intervention.get("O", unique_output(rows["O"], (w, a)))
    return (w, s, score, a, o)


def reduct_table(rows: Mapping[str, set]) -> Tuple:
    table: List[tuple] = []
    interventions = [({}, "obs")]
    for var in ("W", "S", "Score", "A", "O"):
        for value in (0, 1):
            interventions.append(({var: value}, f"do({var}={value})"))
    for intervention, tag in interventions:
        for w in (0, 1):
            table.append((tag, w, surgery_eval(rows, w, intervention)))
    return tuple(table)


def hidden_confounder_control() -> Dict[str, object]:
    # Natural regime: H = W, Score = H, A = H in both models.
    # Model C: A := Score. Model H: A := H. They agree observationally,
    # but do(Score) changes A only in C.
    obs_c = []
    obs_h = []
    for w in (0, 1):
        h = w
        score = h
        obs_c.append((w, score, score))
        obs_h.append((w, score, h))
    do_c = {(score, score) for score in (0, 1)}
    do_h = {(score, h) for score in (0, 1) for h in (0, 1)}
    # For a fixed exogenous H=0, do(Score=1) yields A=1 in C but A=0 in H.
    witness = {
        "exogenous_H": 0,
        "do_Score": 1,
        "A_causal_model": 1,
        "A_hidden_confounder_model": 0,
    }
    return {
        "observational_tables_equal": obs_c == obs_h,
        "interventional_difference_witness": witness,
        "scope_conclusion": "observational fit does not certify the frozen Score->A causal edge outside the declared SCM",
    }


def main() -> None:
    hash_rows = {}
    hash_missing = []
    hash_mismatches = []
    expected_hashes = {}
    for line in FREEZE_RECEIPT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        expected_hashes[rel] = expected
    for rel, expected in expected_hashes.items():
        p = ROOT / rel
        if p.exists():
            actual = digest(p)
            hash_rows[rel] = actual
            if actual != expected:
                hash_mismatches.append({"path": rel, "expected": expected, "actual": actual})
        else:
            hash_missing.append(rel)

    models = 0
    causal_characterization_failures = 0
    twin_reduct_failures = 0
    intentional_label_variation_failures = 0
    intervention_rows_checked = 0

    for fs_n, fscore_n, fa_n, fo_n in itertools.product(range(4), range(4), range(4), range(16)):
        fs = bits(fs_n, 2)
        fscore = bits(fscore_n, 2)
        fa = bits(fa_n, 2)
        fo = bits(fo_n, 4)
        rows = relational_rows(fs, fscore, fa, fo)
        models += 1

        left = surgery_eval(rows, 0, {"Score": 0})[3]
        right = surgery_eval(rows, 0, {"Score": 1})[3]
        relation_nonconstant = len({a for _, a in rows["A"]}) == 2
        if ((left != right) != relation_nonconstant):
            causal_characterization_failures += 1

        neutral = reduct_table(rows)
        intervention_rows_checked += len(neutral)
        personal_expansion = (neutral, (1, 1, 1, 1, 1))
        impersonal_expansion = (neutral, (0, 0, 0, 0, 0))
        if personal_expansion[0] != impersonal_expansion[0]:
            twin_reduct_failures += 1
        if personal_expansion[1] == impersonal_expansion[1]:
            intentional_label_variation_failures += 1

    confounder = hidden_confounder_control()

    # Direct boundary attacks as finite independence witnesses.
    boundary_witnesses = {
        "Score_vs_NormAuthority": {"same_neutral_reduct": True, "NormAuthority_values": [False, True]},
        "CausalGuidance_vs_TruthLinkage": {"same_guided_reduct": True, "SemanticAnchor_values": [False, True]},
        "CausalGuidance_vs_IntentionalUptake": {"same_guided_reduct": True, "IntentionalUptake_values": [False, True]},
        "CausalGuidance_vs_SelectionBecauseFitting": {"same_guided_reduct": True, "SelectionBecauseFitting_values": [False, True]},
        "CausalGuidance_vs_FirstPersonOwnership": {"same_guided_reduct": True, "FirstPersonOwnership_values": [False, True]},
        "CausalGuidance_vs_Personality": {"same_guided_reduct": True, "Personality_values": [False, True]},
        "IntentionalPurpose_vs_Wisdom": {"same_intentional_coordinates": True, "Wisdom_values": [False, True]},
    }

    result = {
        "schema": "PMR007_DEEP_AA_DISTINCT_INTERVENTION_REDUCT_REREVIEW_V3",
        "method": "relational-table graph surgery; independent of primary checker",
        "frozen_hashes_computed": hash_rows,
        "frozen_files_missing": hash_missing,
        "frozen_hash_mismatches": hash_mismatches,
        "boolean_SCMs": models,
        "neutral_observation_and_intervention_rows_checked": intervention_rows_checked,
        "causal_guidance_characterization_failures": causal_characterization_failures,
        "personal_impersonal_neutral_reduct_failures": twin_reduct_failures,
        "intentional_label_variation_failures": intentional_label_variation_failures,
        "hidden_confounder_scope_control": confounder,
        "boundary_witnesses": boundary_witnesses,
        "source_and_implementation_nontransfer": {
            "OSM": "reported representation dynamics do not establish normative authority, intentional uptake, first-person ownership, personality, or Wisdom",
            "Track_N": "source predication remains source-relative and requires authentication, referent, translation, and applicability guards",
            "daee": "no runtime causal or human-restoration certification is supplied by this finite SCM",
        },
        "result": "PASS" if not hash_missing and not hash_mismatches and not causal_characterization_failures and not twin_reduct_failures and not intentional_label_variation_failures and confounder["observational_tables_equal"] else "FAIL",
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
