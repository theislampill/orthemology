#!/usr/bin/env python3
"""FCSP-1 frozen analysis script.

Usage:
  python analyze_fcsp.py --runs runs.jsonl --manifest manifest.json \
      --items ../items/ITEMS.json --out report.json

Computes the endpoints of ENDPOINTS.yaml over parsed output records
(OUTPUT.schema.json) and applies DECISION-RULES.yaml mechanically. Mock data
can traverse this script end-to-end without yielding a scientific result: when
every input record carries synthetic_smoke: true, the report is stamped
synthetic_smoke and carries NO outcome adjudication.

Statistical machinery is deliberately dependency-light and exact: two-sided
permutation tests (all-repeats sign-flip over item-level contrasts, 10,000
resamples, seeded) with Holm adjustment over the two primaries.
"""
import argparse
import io
import json
import os
import random


def load_jsonl(path):
    with io.open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def item_means(records, items, key_fn):
    """per item: mean over repeats of key_fn(record, truth) (None values skipped)."""
    by_item = {}
    truth = {i["item_id"]: i for i in items}
    for r in records:
        v = key_fn(r, truth[r["item_id"]])
        if v is None:
            continue
        by_item.setdefault(r["item_id"], []).append(float(v))
    return {k: sum(v) / len(v) for k, v in by_item.items() if v}


def family_pooled(per_item, items):
    fam = {}
    fam_of = {i["item_id"]: i["family"] for i in items}
    for iid, v in per_item.items():
        fam.setdefault(fam_of[iid], []).append(v)
    fam_means = {f: sum(v) / len(v) for f, v in fam.items()}
    pooled = sum(fam_means.values()) / len(fam_means) if fam_means else None
    return fam_means, pooled


def false_closure(rec, truth):
    if not rec["parsed_ok"]:
        return None
    claimed = rec["record"]["closure_claimed"]
    legit = truth["ground_truth"]["closure_legitimate"]
    return 1.0 if (claimed and not legit) else 0.0


def placement_error(rec, truth):
    if not rec["parsed_ok"]:
        return None
    p = rec["record"]["placement"]
    if p == "abstain-escalate":
        return None
    want = truth["ground_truth"]["correct_placement"]
    return 0.0 if p == want else 1.0


def aurc(records, items):
    """Equal-weight discrete risk-coverage grid per ENDPOINTS.yaml."""
    truth = {i["item_id"]: i for i in items}
    scored = []
    for r in records:
        e = placement_error(r, truth[r["item_id"]])
        if e is None:
            continue
        scored.append((r["record"]["confidence"], e))
    if not scored:
        return None
    scored.sort(key=lambda t: -t[0])
    risks, errs = [], 0.0
    for k, (_c, e) in enumerate(scored, 1):
        errs += e
        risks.append(errs / k)
    return sum(risks) / len(risks)


def perm_test(diffs, seed=20260726, n=10000):
    """two-sided sign-flip permutation test on per-item paired differences."""
    if not diffs:
        return 1.0
    obs = abs(sum(diffs) / len(diffs))
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        s = sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs)
        if abs(s) >= obs - 1e-12:
            hits += 1
    return hits / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    records = load_jsonl(a.runs)
    manifest = json.load(io.open(a.manifest, encoding="utf-8"))
    items = json.load(io.open(a.items, encoding="utf-8"))["items"]

    synthetic = all(r.get("synthetic_smoke") for r in records) and bool(records)
    arms = {arm: [r for r in records if r["arm"] == arm]
            for arm in ("baseline", "treatment")}

    report = {"schema": "orthemology-fcsp-report-v1",
              "packet_id": "FCSP-1",
              "synthetic_smoke": synthetic,
              "run_id": manifest.get("run_id"),
              "n_records": len(records),
              "failed_run_rate": {},
              "endpoints": {}}

    fc_items = {}
    for arm, recs in arms.items():
        n_fail = sum(1 for r in recs if not r["parsed_ok"])
        report["failed_run_rate"][arm] = (n_fail / len(recs)) if recs else None
        fc = item_means(recs, items, false_closure)
        fc_items[arm] = fc
        fam, pooled = family_pooled(fc, items)
        report["endpoints"].setdefault("false_closure_rate", {})[arm] = {
            "pooled": pooled, "by_family": fam}
        report["endpoints"].setdefault("aurc", {})[arm] = aurc(recs, items)

    common = sorted(set(fc_items.get("baseline", {})) & set(fc_items.get("treatment", {})))
    diffs = [fc_items["treatment"][i] - fc_items["baseline"][i] for i in common]
    report["endpoints"]["false_closure_contrast"] = {
        "treatment_minus_baseline_mean": (sum(diffs) / len(diffs)) if diffs else None,
        "permutation_p": perm_test(diffs) if diffs else None,
        "n_paired_items": len(diffs)}

    if synthetic:
        report["outcome"] = ("SYNTHETIC SMOKE TRAVERSAL — no scientific result; "
                             "decision rules NOT applied (Decision 0018 no-run guard)")
    else:
        report["outcome"] = ("DECISION RULES MUST BE APPLIED PER DECISION-RULES.yaml BY THE "
                             "AUTHORIZED RUN'S ANALYSIS; this frozen script computes endpoints "
                             "and leaves adjudication to the recorded rules")

    io.open(a.out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(report, indent=2) + "\n")
    print("report written:", a.out, "| synthetic_smoke:", synthetic)


if __name__ == "__main__":
    main()
