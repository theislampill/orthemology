#!/usr/bin/env python3
"""Pilot 0 analysis skeleton — deterministic parsing, rubric bookkeeping, and
variance-component summaries. PRODUCES NO EFFICACY VERDICTS BY CONSTRUCTION:
Pilot 0 is feasibility/instrumentation only (see PILOT0-PROTOCOL.md §1, §5).

Input format (one JSON per run):
{
  "manifest": {...conforming to RUN-MANIFEST.schema.json...},
  "responses": [
    {"item": "P0-ID-1", "arm": "A", "executor": "model-x", "repeat": 1,
     "rater_scores": {"rater1": {"probe_idx": 0/1, ...}, ...},
     "response_tokens": 123,
     "comprehension_accuracy": null | 0.0-1.0}
  ]
}

Smoke test: python analyze_pilot0.py --selftest   (runs on synthetic data)
"""
import argparse
import itertools
import json
import statistics
import sys

ARMS = ["A", "B", "C", "Cprime"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def agreement(rows):
    """Simple pairwise percent agreement per item-arm cell (Krippendorff alpha
    belongs to Pilot 1's mixed-model spec; Pilot 0 needs only feasibility)."""
    out = {}
    for r in rows:
        key = (r["item"], r["arm"])
        raters = r.get("rater_scores", {})
        codes = sorted(raters)
        pairs = list(itertools.combinations(codes, 2))
        if not pairs:
            continue
        agree = total = 0
        for a, b in pairs:
            for probe in raters[a]:
                if probe in raters[b]:
                    total += 1
                    agree += int(raters[a][probe] == raters[b][probe])
        if total:
            out.setdefault(key, []).append(agree / total)
    return {k: statistics.mean(v) for k, v in out.items()}


def overhead_guard(rows):
    """Negative-control token overhead per arm vs Arm A."""
    nc = [r for r in rows if r["item"].startswith("P0-NC")]
    by_arm = {arm: [r["response_tokens"] for r in nc if r["arm"] == arm] for arm in ARMS}
    base = statistics.mean(by_arm["A"]) if by_arm["A"] else float("nan")
    return {arm: (statistics.mean(v) - base if v else None) for arm, v in by_arm.items()}


def variance_components(rows):
    """Crude per-factor score-variance summary feeding Pilot 1's simulation-based
    power (NOT a mixed model; the model spec lives in pilot1/)."""
    def mean_scores(group_key):
        groups = {}
        for r in rows:
            scores = [v for rr in r.get("rater_scores", {}).values() for v in rr.values()]
            if scores:
                groups.setdefault(r[group_key], []).extend(scores)
        return {k: statistics.mean(v) for k, v in groups.items()}
    comp = {}
    for factor in ("item", "arm", "executor"):
        means = mean_scores(factor)
        comp[factor] = (statistics.pvariance(list(means.values())) if len(means) > 1 else 0.0)
    return comp


def comprehension_gate(rows):
    c = [r["comprehension_accuracy"] for r in rows if r["arm"] == "C" and r.get("comprehension_accuracy") is not None]
    cp = [r["comprehension_accuracy"] for r in rows if r["arm"] == "Cprime" and r.get("comprehension_accuracy") is not None]
    if not c or not cp:
        return {"status": "insufficient data"}
    gap = statistics.mean(c) - statistics.mean(cp)
    return {"C_mean": statistics.mean(c), "Cprime_mean": statistics.mean(cp),
            "gap_pp": 100 * gap, "gate_within_10pp": abs(gap) <= 0.10}


def synthetic():
    import random
    rng = random.Random(0)
    rows = []
    items = ["P0-ID-1", "P0-PW-1", "P0-MB-1", "P0-NC-1"]
    for item, arm, rep in itertools.product(items, ARMS, (1, 2)):
        rows.append({
            "item": item, "arm": arm, "executor": "synthetic-model", "repeat": rep,
            "rater_scores": {"r1": {"0": rng.randint(0, 1), "1": rng.randint(0, 1)},
                             "r2": {"0": rng.randint(0, 1), "1": rng.randint(0, 1)}},
            "response_tokens": 80 + rng.randint(0, 40),
            "comprehension_accuracy": (0.9 if arm in ("C", "Cprime") else None),
        })
    return {"manifest": {"run_id": "SELFTEST", "synthetic": True}, "responses": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_json", nargs="?", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    data = synthetic() if args.selftest else load(args.run_json)
    rows = data["responses"]
    report = {
        "run_id": data["manifest"].get("run_id"),
        "n_responses": len(rows),
        "pairwise_rater_agreement": {f"{i}|{a}": v for (i, a), v in agreement(rows).items()},
        "negative_control_overhead_tokens_vs_A": overhead_guard(rows),
        "variance_components_crude": variance_components(rows),
        "sham_comprehension_gate": comprehension_gate(rows),
        "NOTE": "Feasibility summaries only. NO efficacy verdict is computed, by design.",
    }
    json.dump(report, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
