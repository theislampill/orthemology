#!/usr/bin/env python3
"""ER-1 frozen analysis script.

Usage:
  python analyze_er.py --runs runs.jsonl --manifest manifest.json \
      --spec ../E1-E5-SPEC.yaml --out report.json

Scores answer records (OUTPUT.schema.json) against the frozen keys in
E1-E5-SPEC.yaml and SCORING-RUBRIC.md, per arm, and reports the endpoint set.
When every record is synthetic_smoke, the report is stamped synthetic and
adjudicates no outcome (Decision 0018 no-run guard).
"""
import argparse
import io
import json

import yaml


def load_jsonl(path):
    with io.open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def score(rec, case):
    gt = case["ground_truth"]
    ans = rec["answers"]
    s = {}
    s["defect_discovered"] = (ans["defect_identified"] == gt["pathway_defect"])
    s["remedy_correct"] = (ans["remedy"] == gt["correct_remedy"])
    s["false_closure_prevented"] = (ans["endorse_completion"] is False) or gt["closure_legitimate"]
    s["traceability"] = bool(ans.get("grounding_element"))
    if case["id"] == "E5":
        s["robustness_diagnosis"] = bool(ans.get("neighbors_used"))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    records = load_jsonl(a.runs)
    manifest = json.load(io.open(a.manifest, encoding="utf-8"))
    spec = yaml.safe_load(io.open(a.spec, encoding="utf-8"))
    cases = {c["id"]: c for c in spec["cases"]}

    synthetic = all(r.get("synthetic_smoke") for r in records) and bool(records)
    per_arm = {}
    for r in records:
        sc = score(r, cases[r["case_id"]])
        cost = {"answer_tokens": r.get("answer_tokens"), "seconds": r.get("seconds")}
        per_arm.setdefault(r["arm"], []).append({"case": r["case_id"], **sc, **cost})

    endpoints = {}
    for arm, rows in per_arm.items():
        n = len(rows)
        endpoints[arm] = {
            "defect_discovery_rate": sum(x["defect_discovered"] for x in rows) / n,
            "remedy_accuracy": sum(x["remedy_correct"] for x in rows) / n,
            "false_closure_prevention": sum(x["false_closure_prevented"] for x in rows) / n,
            "traceability_rate": sum(x["traceability"] for x in rows) / n,
            "robustness_diagnosis_rate": (
                (lambda e5: sum(x.get("robustness_diagnosis", False) for x in e5) / len(e5)
                 if e5 else None)([x for x in rows if x["case"] == "E5"])),
            "mean_answer_tokens": (
                (lambda t: sum(t) / len(t) if t else None)(
                    [x["answer_tokens"] for x in rows if x.get("answer_tokens") is not None])),
            "n": n,
        }

    report = {"schema": "orthemology-er-report-v1", "packet_id": "ER-1",
              "synthetic_smoke": synthetic, "run_id": manifest.get("run_id"),
              "n_records": len(records), "endpoints": endpoints}
    report["outcome"] = (
        "SYNTHETIC SMOKE TRAVERSAL — no scientific result; decision rules NOT applied"
        if synthetic else
        "endpoints computed; adjudication per DECISION-RULES.yaml by the authorized run")
    io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(report, indent=2) + "\n")
    print("report written:", a.out, "| synthetic_smoke:", synthetic)


if __name__ == "__main__":
    main()
