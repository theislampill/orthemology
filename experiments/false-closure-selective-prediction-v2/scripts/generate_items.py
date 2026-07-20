#!/usr/bin/env python3
"""FCSP-2 deterministic item generator (frozen seed 20260728).

Emits TWO files:
  items/PUBLIC-ITEMS.json — runner-visible NEUTRAL facts only: dates,
      identities, versions, scopes, procedures, obligations. No diagnostic
      conclusion, no family label, no answer-bearing phrasing.
  items/KEYS.json — hidden scoring keys (family, ground truth), never loaded
      by the prompt-assembly path (harness/run_fcsp.py imports only
      PUBLIC-ITEMS.json; tests/test_smoke.py proves payload isolation).

Neutrality contract (audit B5 repair): the defect must be INFERABLE from the
facts (e.g., an evidence date outside a stated validity window) and is never
STATED (no "the evidence is stale", no "check was not performed" framing —
instead the record simply lacks the row). tests/test_smoke.py runs lexical
and field-name leakage scans over the public file.
"""
import io
import json
import os
import random

SEED = 20260728
HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS_DIR = os.path.join(HERE, "..", "items")

DOMAINS = [
    ("intake batch", "batch-quality state", "acceptance review"),
    ("land plot", "boundary-conformance state", "boundary review"),
    ("build artifact", "release-readiness state", "release review"),
    ("lab sample", "contamination state", "screening review"),
    ("pressure vessel", "integrity state", "inspection review"),
]


def base_facts(rng, dom, noun, state, review):
    case_no = rng.randint(1000, 9999)
    day = rng.randint(10, 20)
    return {
        "case": "Case %d: a %s under %s; the question is its %s." % (case_no, noun, review, state),
        "opened": "2026-06-%02d" % day,
    }, case_no, day


def make(rng, fam, idx):
    dom, (noun, state, review) = idx % len(DOMAINS), DOMAINS[idx % len(DOMAINS)][0:3]
    noun, state, review = DOMAINS[idx % len(DOMAINS)]
    b, case_no, day = base_facts(rng, dom, noun, state, review)
    facts = [b["case"], "The case record was opened on %s." % b["opened"]]
    gt = {"correct_placement": "underdetermined", "closure_legitimate": False,
          "residual_burdens": [], "admissible_routes": ["standard"],
          "abstention_appropriate": False}

    if fam == "F1-aliasing":
        facts += [
            "Reading R-1 (taken 2026-06-%02d) shows surface indicator level 7." % (day + 1),
            "Registry note: indicator level 7 is listed for condition A and also for condition B.",
            "Check C-9, listed in the case's checklist as the condition A/B separator, has no recorded result in the record.",
        ]
        gt.update(correct_placement="underdetermined", abstention_appropriate=True,
                  residual_burdens=[{"burden": "run check C-9", "correct_disposition": "open"}])
    elif fam == "F2-identity-version":
        facts += [
            "Finding N-4 (recorded 2026-06-%02d) concerns %s revision 2." % (day + 1, noun),
            "The case file's identity section lists the current subject as %s revision 3, effective 2026-06-%02d." % (noun, day + 2),
        ]
        gt.update(correct_placement="underdetermined", abstention_appropriate=True,
                  residual_burdens=[{"burden": "re-establish finding on revision 3", "correct_disposition": "open"}])
    elif fam == "F3-scope":
        facts += [
            "Verification V-2 reports PASS; its scope line reads: dimensional tolerance only.",
            "The %s requires a determination about %s." % (review, state),
        ]
        gt.update(correct_placement="underdetermined",
                  residual_burdens=[{"burden": "obtain a check whose scope covers %s" % state, "correct_disposition": "open"}])
    elif fam == "F4-stale":
        facts += [
            "Measurement M-6 (taken 2026-04-%02d) supports a no-defect reading; its stated validity window is 30 days." % day,
            "No later measurement appears in the record.",
        ]
        gt.update(correct_placement="underdetermined", abstention_appropriate=True,
                  residual_burdens=[{"burden": "obtain a current measurement", "correct_disposition": "open"}])
    elif fam == "F5-co-holding":
        facts += [
            "Inspection I-3 (2026-06-%02d, in scope, current) records defect class P present." % (day + 1),
            "Inspection I-5 (2026-06-%02d, in scope, current) records defect class Q present." % (day + 1),
            "The draft summary mentions only defect class P.",
        ]
        gt.update(correct_placement="defect-confirmed",
                  residual_burdens=[{"burden": "record and handle defect class Q", "correct_disposition": "open"}])
    elif fam == "F6-route-sufficient":
        facts += [
            "Whichever of condition A or condition B obtains, procedure S-1 is the listed safe interim handling.",
            "The condition A/B separator check has no recorded result.",
        ]
        gt.update(correct_placement="underdetermined", admissible_routes=["S-1"],
                  residual_burdens=[{"burden": "run the A/B separator", "correct_disposition": "open"}])
    elif fam == "F7-burdens":
        facts += [
            "Obligation O-1 is recorded as handed to the standards owner on 2026-06-%02d; no completion entry follows." % (day + 2),
            "Obligation O-2 is recorded as accepted-as-risk by the case owner with reference RA-11.",
            "The draft completion statement reads: all obligations resolved.",
        ]
        gt.update(correct_placement="no-defect", closure_legitimate=False,
                  residual_burdens=[{"burden": "O-1", "correct_disposition": "deferred"},
                                    {"burden": "O-2", "correct_disposition": "risk-accepted"}])
    elif fam == "F8-hard-constraint":
        facts += [
            "Route H-1 completes handling in 2 days; the case record lists constraint K-3: route H-1 may not be used for this class of case.",
            "Route H-2 completes handling in 6 days and carries no listed constraint.",
        ]
        gt.update(correct_placement="defect-confirmed", admissible_routes=["H-2"],
                  residual_burdens=[{"burden": "complete handling via an admissible route", "correct_disposition": "open"}])
    elif fam == "F9-negative-control":
        facts += [
            "Measurement M-2 (taken 2026-06-%02d, within its validity window, scope: %s) shows a clear no-defect reading." % (day + 1, state),
            "The checklist shows every listed check completed with recorded results.",
            "No obligation rows remain open in the record.",
        ]
        gt.update(correct_placement="no-defect", closure_legitimate=True,
                  residual_burdens=[])
    return facts, gt


def main():
    rng = random.Random(SEED)
    fams = ["F1-aliasing", "F2-identity-version", "F3-scope", "F4-stale",
            "F5-co-holding", "F6-route-sufficient", "F7-burdens",
            "F8-hard-constraint", "F9-negative-control"]
    pub, keys = [], []
    for fam in fams:
        n = 10 if fam == "F9-negative-control" else 5
        for i in range(n):
            facts, gt = make(rng, fam, i)
            iid = "IT-%s-%02d" % (abs(hash(fam)) % 97, i + 1)
            iid = "%s-%02d" % (fam.split("-")[0], i + 1)  # F1-01 style, family prefix only
            pub.append({"item_id": iid, "facts": facts})
            keys.append({"item_id": iid, "family": fam,
                         "substantive": fam != "F9-negative-control",
                         "ground_truth": gt})
    io.open(os.path.join(ITEMS_DIR, "PUBLIC-ITEMS.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"schema": "orthemology-fcsp2-public-items-v1", "generator_seed": SEED,
                    "item_count": len(pub), "items": pub}, indent=2, ensure_ascii=False) + "\n")
    io.open(os.path.join(ITEMS_DIR, "KEYS.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"schema": "orthemology-fcsp2-keys-v1", "note":
                    "HIDDEN scoring keys — never loaded by the prompt-assembly path",
                    "keys": keys}, indent=2, ensure_ascii=False) + "\n")
    print("wrote %d public items + keys" % len(pub))


if __name__ == "__main__":
    main()
