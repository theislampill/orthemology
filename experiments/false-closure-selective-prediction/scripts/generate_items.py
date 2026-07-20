#!/usr/bin/env python3
"""Deterministic item generator for FCSP-1 (frozen seed 20260720).

Generates items/ITEMS.json: 9 scenario families x 4 substantive items + 8
negative controls = 44 items, every scenario synthetic and public. The
committed file must equal the regenerated output byte-for-byte
(tests/test_smoke.py enforces this). Changing this generator or the seed is a
new packet version.
"""
import hashlib
import io
import json
import os
import random

SEED = 20260720
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "items", "ITEMS.json")

DOMAINS = [
    ("inventory-batch", "a warehouse intake batch", "batch-quality state"),
    ("survey-plot", "a surveyed land plot", "boundary-conformance state"),
    ("build-artifact", "a software build artifact", "release-readiness state"),
    ("lab-sample", "a laboratory sample", "contamination state"),
]

FAMILIES = {
    "F1-observational-aliasing": (
        "Two distinct underlying states of {noun} produce the same immediate observation; "
        "only a declared discriminating check separates them. The record shows the observation "
        "and one discriminating check that was AVAILABLE but not yet performed."),
    "F2-identity-version": (
        "{noun} was replaced/renumbered mid-process; an earlier finding attaches to the "
        "predecessor version while the current handling concerns the successor."),
    "F3-mis-scoped-green": (
        "A verification step for {noun} reports PASS, but its declared scope covers a "
        "different property than the one the completion claim needs."),
    "F4-stale-evidence": (
        "The key evidence about {noun} carried an explicit validity window that has lapsed, "
        "and a superseding measurement is known to exist but was not retrieved."),
    "F5-co-holding-defects": (
        "{noun} simultaneously exhibits two independent defects; confirming either one does "
        "not settle the other, and the handling record so far mentions only one."),
    "F6-route-sufficient": (
        "The safe interim route for {noun} is already determined by what IS known, even though "
        "the finer identity of the underlying state remains open."),
    "F7-false-closure-burdens": (
        "Handling of {noun} reaches its end state while one obligation was deferred to a named "
        "owner and another was accepted as residual risk; the draft completion statement calls "
        "everything resolved."),
    "F8-hard-constraint-route": (
        "The otherwise-preferred handling route for {noun} violates a hard constraint that is "
        "explicitly recorded; an admissible but slower route exists."),
    "F9-negative-control": (
        "A routine, single-defect, fresh-evidence case about {noun} with no aliasing, no version "
        "change, correctly scoped checks, and no open obligations."),
}


def make_item(rng, fam_key, template, idx):
    dom_key, noun, state = DOMAINS[idx % len(DOMAINS)]
    case_no = rng.randint(100, 999)
    scenario = ("Case %d concerns %s; the question is its %s. " % (case_no, noun, state)
                + template.format(noun=noun))
    substantive = fam_key != "F9-negative-control"
    truth = {
        "correct_placement": "defect-confirmed" if fam_key in (
            "F5-co-holding-defects", "F7-false-closure-burdens") else (
            "no-defect" if fam_key == "F9-negative-control" else "underdetermined"),
        "live_alternatives_required": fam_key in (
            "F1-observational-aliasing", "F2-identity-version", "F6-route-sufficient"),
        "evidence_validity_issue": fam_key in ("F2-identity-version", "F4-stale-evidence"),
        "scope_issue": fam_key == "F3-mis-scoped-green",
        "closure_legitimate": fam_key == "F9-negative-control",
        "residual_burdens": (
            [{"burden": "deferred-to-owner", "correct_disposition": "deferred"},
             {"burden": "risk-accepted-residual", "correct_disposition": "risk-accepted"}]
            if fam_key == "F7-false-closure-burdens" else
            ([] if fam_key == "F9-negative-control" else
             [{"burden": "open-discriminating-check", "correct_disposition": "open"}])),
        "admissible_routes": (["slow-admissible"] if fam_key == "F8-hard-constraint-route"
                              else ["standard"]),
        "abstention_appropriate": truth_abstention(fam_key),
    }
    return {
        "item_id": "%s-%02d" % (fam_key, idx + 1),
        "family": fam_key,
        "domain": dom_key,
        "substantive": substantive,
        "scenario": scenario,
        "ground_truth": truth,
    }


def truth_abstention(fam_key):
    return fam_key in ("F1-observational-aliasing", "F2-identity-version",
                       "F4-stale-evidence")


def main():
    rng = random.Random(SEED)
    items = []
    for fam_key, template in FAMILIES.items():
        n = 8 if fam_key == "F9-negative-control" else 4
        for i in range(n):
            items.append(make_item(rng, fam_key, template, i))
    doc = {
        "schema": "orthemology-fcsp-items-v1",
        "generator_seed": SEED,
        "item_count": len(items),
        "items": items,
    }
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print("wrote %d items, sha256 %s" % (
        len(items), hashlib.sha256(text.encode()).hexdigest()[:16]))


if __name__ == "__main__":
    main()
