#!/usr/bin/env python3
"""Pilot 0 v2 analysis — deterministic, feasibility-only (v2.1, Decision 0018).

Derived from the v1 skeleton (terminology/pilot0/analysis/analyze_pilot0.py,
immutable history) with the v2 additions the v2.0 spec described but never
shipped: flag-aware eligibility filtering for the C-vs-C' contrast and
descriptive E1-E4 summaries. PRODUCES NO ADOPTION/RETIREMENT VERDICT BY
CONSTRUCTION: Pilot 0 is feasibility/instrumentation only. The only outcome
this script emits is one of the four feasibility outcomes of
EXECUTION-SPEC.md section 4, derived mechanically from the numeric gates
stated there.

Usage:
  python analyze_pilot0_v2.py run.json --items ../items/ITEMS.json --out report.json
  python analyze_pilot0_v2.py --selftest          (synthetic mock traversal)
"""
import argparse
import io
import itertools
import json
import statistics
import sys

ARMS = ["A", "B", "C", "Cprime"]

GATES = {  # numeric feasibility gates (EXECUTION-SPEC.md section 4a)
    "min_pairwise_rater_agreement": 0.70,
    "sham_comprehension_gap_pp_max": 10.0,
    "item_pass_rate_floor": 0.10,
    "item_pass_rate_ceiling": 0.90,
    "min_items_within_band": 5,
    "negative_control_overhead_tokens_max": 30.0,
}


def load(path):
    return json.load(io.open(path, encoding="utf-8"))


def pass_rate(rows, item=None, arm=None, eligible_ids=None):
    vals = []
    for r in rows:
        if item and r["item"] != item:
            continue
        if arm and r["arm"] != arm:
            continue
        if eligible_ids is not None and r["item"] not in eligible_ids:
            continue
        scores = [v for rr in r.get("rater_scores", {}).values() for v in rr.values()]
        vals.extend(scores)
    return (sum(vals) / len(vals)) if vals else None


def agreement(rows):
    out = {}
    for r in rows:
        raters = r.get("rater_scores", {})
        pairs = list(itertools.combinations(sorted(raters), 2))
        agree = total = 0
        for a, b in pairs:
            for probe in raters[a]:
                if probe in raters[b]:
                    total += 1
                    agree += int(raters[a][probe] == raters[b][probe])
        if total:
            out.setdefault((r["item"], r["arm"]), []).append(agree / total)
    return {k: statistics.mean(v) for k, v in out.items()}


def overhead(rows):
    nc = [r for r in rows if r["item"].startswith(("P0-NC", "P0v2-NC"))]
    by_arm = {arm: [r["response_tokens"] for r in nc if r["arm"] == arm] for arm in ARMS}
    base = statistics.mean(by_arm["A"]) if by_arm["A"] else float("nan")
    return {arm: (statistics.mean(v) - base if v else None) for arm, v in by_arm.items()}


def comprehension_gap(rows):
    c = [r["comprehension_accuracy"] for r in rows
         if r["arm"] == "C" and r.get("comprehension_accuracy") is not None]
    cp = [r["comprehension_accuracy"] for r in rows
          if r["arm"] == "Cprime" and r.get("comprehension_accuracy") is not None]
    if not c or not cp:
        return None
    return 100 * (statistics.mean(c) - statistics.mean(cp))


def synthetic():
    import random
    rng = random.Random(0)
    rows = []
    items = ["P0v2-ID-1", "P0v2-PW-1", "P0v2-MB-1", "P0v2-NC-1"]
    for item, arm, rep in itertools.product(items, ARMS, (1, 2)):
        rows.append({"item": item, "arm": arm, "executor": "synthetic-model", "repeat": rep,
                     "rater_scores": {"r1": {"0": rng.randint(0, 1), "1": rng.randint(0, 1)},
                                      "r2": {"0": rng.randint(0, 1), "1": rng.randint(0, 1)}},
                     "response_tokens": 80 + rng.randint(0, 40),
                     "comprehension_accuracy": (0.9 if arm in ("C", "Cprime") else None)})
    return {"manifest": {"run_id": "SELFTEST", "synthetic": True}, "responses": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_json", nargs="?", default=None)
    ap.add_argument("--items", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    data = synthetic() if args.selftest else load(args.run_json)
    rows = data["responses"]
    synthetic_run = bool(data["manifest"].get("synthetic"))

    eligible = None
    substantive = None
    if args.items:
        items_doc = load(args.items)
        eligible = {i["id"] for i in items_doc["items"] if i.get("eligible_for_c_vs_cprime")}
        substantive = {i["id"] for i in items_doc["items"] if i.get("substantive", True)}

    agr = agreement(rows)
    gap = comprehension_gap(rows)
    ovh = overhead(rows)
    report = {
        "schema": "orthemology-pilot0-v2-report-v1",
        "run_id": data["manifest"].get("run_id"),
        "synthetic": synthetic_run,
        "n_responses": len(rows),
        "feasibility": {
            "pairwise_rater_agreement": {"%s|%s" % k: v for k, v in agr.items()},
            "sham_comprehension_gap_pp": gap,
            "negative_control_overhead_tokens_vs_A": ovh,
        },
        "descriptive_estimands_no_verdict": {
            "E1_C_minus_B": _diff(rows, "C", "B", substantive),
            "E2_C_minus_Cprime_eligible": _diff(rows, "C", "Cprime", eligible),
            "E3_B_minus_A": _diff(rows, "B", "A", substantive),
            "E4_overhead": ovh,
            "NOTE": "descriptive only; efficacy margins are NOT applied in Pilot 0",
        },
    }

    if synthetic_run:
        report["outcome"] = ("SYNTHETIC SELFTEST — no feasibility outcome; "
                             "no adoption/retirement outcome exists at any Pilot 0 stage")
    else:
        report["outcome"] = feasibility_outcome(agr, gap, ovh, rows)
    report["gates"] = GATES

    text = json.dumps(report, indent=2) + "\n"
    if args.out:
        io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    else:
        sys.stdout.write(text)


def _diff(rows, arm_hi, arm_lo, id_filter):
    hi = pass_rate(rows, arm=arm_hi, eligible_ids=id_filter)
    lo = pass_rate(rows, arm=arm_lo, eligible_ids=id_filter)
    return None if hi is None or lo is None else hi - lo


def feasibility_outcome(agr, gap, ovh, rows):
    """Mechanical mapping to the four feasibility outcomes. Never adopt/retire."""
    problems = []
    low_agr = [k for k, v in agr.items() if v < GATES["min_pairwise_rater_agreement"]]
    if low_agr:
        problems.append("rater agreement below gate in %d cells" % len(low_agr))
    if gap is None:
        problems.append("sham comprehension gate unmeasurable")
    elif abs(gap) > GATES["sham_comprehension_gap_pp_max"]:
        problems.append("sham comprehension gap %.1fpp exceeds gate" % gap)
    heavy = [a for a, v in ovh.items()
             if v is not None and v > GATES["negative_control_overhead_tokens_max"]]
    if heavy:
        problems.append("negative-control overhead exceeds gate in arms %s" % heavy)
    items = sorted({r["item"] for r in rows if not r["item"].startswith(("P0-NC", "P0v2-NC"))})
    in_band = 0
    for it in items:
        pr = pass_rate(rows, item=it)
        if pr is not None and GATES["item_pass_rate_floor"] <= pr <= GATES["item_pass_rate_ceiling"]:
            in_band += 1
    if in_band < min(GATES["min_items_within_band"], len(items)):
        problems.append("only %d/%d items inside the pass-rate band" % (in_band, len(items)))

    if not problems:
        return "ADVANCE_TO_PILOT1"
    if len(problems) <= 2 and "unmeasurable" not in " ".join(problems):
        return "REVISE_AND_RETEST_INSTRUMENT: " + "; ".join(problems)
    if any("unmeasurable" in p for p in problems):
        return "INCONCLUSIVE: " + "; ".join(problems)
    return "DO_NOT_ADVANCE_THIS_ITEM_VERSION: " + "; ".join(problems)


if __name__ == "__main__":
    main()
