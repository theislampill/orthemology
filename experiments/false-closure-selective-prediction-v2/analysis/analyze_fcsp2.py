#!/usr/bin/env python3
"""FCSP-2 frozen analysis — implements EVERY endpoint declared in
ENDPOINTS.yaml and executes DECISION-RULES.yaml mechanically.

Usage:
  python analyze_fcsp2.py --runs runs.jsonl --manifest manifest.json \
      --keys ../items/KEYS.json --out report.json

Estimand and units (DESIGN.yaml): the inferential unit is the ITEM, paired
across arms. Repeats are within-item technical replicates averaged into the
item aggregate BEFORE any inference; a temperature-0 rerun adds no
independent information and is never counted as if it did.

Inference: paired arm-swap permutation tests over items (10,000 resamples,
seeded) for both primaries; percentile bootstrap CIs over items (2,000
resamples); Holm adjustment over the two primaries. No observed-power rescue
exists: the sensitivity plan is fixed pre-run (simulation/design_sensitivity)
and the inconclusive gates are exactly the named ones.

Synthetic (mock) inputs traverse everything and yield NO adjudicated outcome.
"""
import argparse
import io
import json
import random

PERMS = 10000
BOOTS = 2000
PSEED = 20260730
BSEED = 20260731


def load_jsonl(path):
    with io.open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


# ---------------- per-record scoring against the hidden keys ----------------

def score_record(rec, key):
    """Returns per-record endpoint components (None = not applicable)."""
    gt = key["ground_truth"]
    if not rec["parsed_ok"] or rec.get("record") is None:
        return None  # failed run — handled by failure accounting
    r = rec["record"]
    placed = r["placement"] not in ("abstain-escalate",)
    s = {}
    s["false_closure"] = 1.0 if (r["closure_claimed"] and not gt["closure_legitimate"]) else 0.0
    # missed residual: every ground-truth burden must be covered by a record
    # burden with the correct disposition (disposition-multiset matching —
    # name-independent, deterministic)
    want = sorted(b["correct_disposition"] for b in gt["residual_burdens"])
    got = sorted(b.get("disposition") for b in (r.get("residual_burdens") or []))
    tmp = list(got)
    missed = 0
    for w in want:
        if w in tmp:
            tmp.remove(w)
        else:
            missed += 1
    s["missed_residual"] = 1.0 if missed else 0.0
    s["burden_disposition_acc"] = (1.0 - missed / len(want)) if want else None
    s["abstained"] = 0.0 if placed else 1.0
    s["abstention_appropriate_hit"] = (
        (1.0 if not placed else 0.0) if gt["abstention_appropriate"] else None)
    s["route_ok"] = 1.0 if r.get("route_selected") in gt["admissible_routes"] else 0.0
    s["result_correct"] = ((1.0 if r["placement"] == gt["correct_placement"] else 0.0)
                           if placed else None)
    s["confidence"] = float(r["confidence"])
    s["placement_error"] = ((0.0 if r["placement"] == gt["correct_placement"] else 1.0)
                            if placed else None)
    s["record_size"] = len(json.dumps(r))
    return s


def item_level(records, keys):
    """arm -> item_id -> mean-over-repeats component dict."""
    kmap = {k["item_id"]: k for k in keys}
    acc = {}
    fails = {}
    for rec in records:
        arm = rec["arm"]
        fails.setdefault(arm, [0, 0])
        fails[arm][1] += 1
        s = score_record(rec, kmap[rec["item_id"]])
        if s is None:
            fails[arm][0] += 1
            continue
        acc.setdefault(arm, {}).setdefault(rec["item_id"], []).append(s)
    out = {}
    for arm, items in acc.items():
        out[arm] = {}
        for iid, rows in items.items():
            agg = {}
            for k in rows[0]:
                vals = [r[k] for r in rows if r[k] is not None]
                agg[k] = (sum(vals) / len(vals)) if vals else None
            out[arm][iid] = agg
    fail_rates = {arm: (n / d if d else None) for arm, (n, d) in fails.items()}
    return out, fail_rates


def fam_pooled(per_item, keys, comp):
    fam_of = {k["item_id"]: k["family"] for k in keys}
    fams = {}
    for iid, agg in per_item.items():
        if agg.get(comp) is None:
            continue
        fams.setdefault(fam_of[iid], []).append(agg[comp])
    fam_means = {f: sum(v) / len(v) for f, v in fams.items()}
    pooled = (sum(fam_means.values()) / len(fam_means)) if fam_means else None
    return fam_means, pooled


# ------------------------------- AURC family --------------------------------

def aurc_from_items(per_item, item_ids):
    """PRIMARY AURC estimand (ENDPOINTS.yaml v2): one point per ITEM —
    item confidence = mean over repeats, item error = mean placement error
    over placed repeats; items with no placed repeat are excluded and counted
    by the abstention endpoints. Equal-weight discrete grid over items."""
    pts = []
    for iid in item_ids:
        agg = per_item.get(iid)
        if not agg or agg.get("placement_error") is None:
            continue
        pts.append((agg["confidence"], agg["placement_error"]))
    if not pts:
        return None
    pts.sort(key=lambda t: -t[0])
    risks, errs = [], 0.0
    for k, (_c, e) in enumerate(pts, 1):
        errs += e
        risks.append(errs / k)
    return sum(risks) / len(risks)


def optimal_aurc(per_item, item_ids):
    """optimal AURC at the same base error mass: errors ordered last."""
    errs = [per_item[i]["placement_error"] for i in item_ids
            if per_item.get(i, {}).get("placement_error") is not None]
    if not errs:
        return None
    errs.sort()  # ascending: zero-error items first = best ordering
    risks, run = [], 0.0
    for k, e in enumerate(errs, 1):
        run += e
        risks.append(run / k)
    return sum(risks) / len(risks)


# ---------------------------- paired inference ------------------------------

def perm_p_mean(diffs, seed=PSEED, n=PERMS):
    if not diffs:
        return None
    obs = abs(sum(diffs) / len(diffs))
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        s = sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs)
        if abs(s) >= obs - 1e-12:
            hits += 1
    return hits / n


def perm_p_aurc(base_items, treat_items, common, seed=PSEED, n=PERMS):
    obs = abs((aurc_from_items(treat_items, common) or 0)
              - (aurc_from_items(base_items, common) or 0))
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        b, t = {}, {}
        for iid in common:
            if rng.random() < 0.5:
                b[iid], t[iid] = treat_items[iid], base_items[iid]
            else:
                b[iid], t[iid] = base_items[iid], treat_items[iid]
        d = abs((aurc_from_items(t, common) or 0) - (aurc_from_items(b, common) or 0))
        if d >= obs - 1e-12:
            hits += 1
    return hits / n


def boot_ci(fn, common, seed=BSEED, n=BOOTS):
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        sample = [common[rng.randrange(len(common))] for _ in common]
        v = fn(sample)
        if v is not None:
            vals.append(v)
    if not vals:
        return None
    vals.sort()
    return [vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]]


def holm(pvals):
    """dict name->p  ->  dict name->holm-adjusted p."""
    items = sorted((p, k) for k, p in pvals.items() if p is not None)
    out, m = {}, len(items)
    prev = 0.0
    for i, (p, k) in enumerate(items):
        adj = min(1.0, max(prev, (m - i) * p))
        prev = adj
        out[k] = adj
    return out


# --------------------------- decision execution -----------------------------

def decide(report, rules):
    P = rules["parameters"]
    e = report["endpoints"]
    fc_d = e["false_closure_contrast"]["treatment_minus_baseline"]
    au_d = e["aurc_contrast"]["treatment_minus_baseline"]
    fc_p = e["false_closure_contrast"]["holm_p"]
    au_p = e["aurc_contrast"]["holm_p"]
    harm = []
    ra = e["result_accuracy_contrast"]
    if ra["treatment_minus_baseline"] is not None and \
       ra["treatment_minus_baseline"] < -P["harm_margin_result_accuracy"] and \
       (ra["perm_p"] or 1) < P["alpha"]:
        harm.append("result-accuracy degradation")
    ov = e["structure_overhead_ratio_on_controls"]
    if ov is not None and ov > P["harm_margin_structure_overhead"]:
        harm.append("structure overhead on negative controls")
    if fc_d is not None and fc_d > 0 and (fc_p or 1) < P["alpha"]:
        harm.append("false-closure increase")
    gates = []
    for arm, r in report["failed_run_rate"].items():
        if r is not None and r > P["max_failed_run_rate"]:
            gates.append("failed-run rate %.3f in %s exceeds %.2f" % (r, arm, P["max_failed_run_rate"]))
    if report.get("outcome_affecting_deviation"):
        gates.append("outcome-affecting recorded deviation")
    if gates:
        return "inconclusive: " + "; ".join(gates)
    if harm:
        return "evidence of harm or failure: " + "; ".join(harm)
    supports = (fc_d is not None and fc_d <= -P["minimum_important_effect_false_closure"]
                and (fc_p or 1) < P["alpha"]
                and au_d is not None and au_d <= -P["minimum_important_effect_aurc"]
                and (au_p or 1) < P["alpha"])
    if supports:
        return "supports incremental value"
    return ("does not yet support incremental value (pre-run fixed-sensitivity design; "
            "no observed-power rescue exists)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--keys", required=True)
    ap.add_argument("--rules", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    import os
    import yaml
    records = load_jsonl(a.runs)
    manifest = json.load(io.open(a.manifest, encoding="utf-8"))
    keys = json.load(io.open(a.keys, encoding="utf-8"))["keys"]
    rules_path = a.rules or os.path.join(os.path.dirname(os.path.abspath(a.keys)),
                                         "..", "DECISION-RULES.yaml")
    rules = yaml.safe_load(io.open(rules_path, encoding="utf-8"))

    synthetic = bool(records) and all(r.get("synthetic_smoke") for r in records)
    per_item, fail_rates = item_level(records, keys)
    base = per_item.get("baseline", {})
    treat = per_item.get("treatment", {})
    common = sorted(set(base) & set(treat))
    sub = [k["item_id"] for k in keys if k["substantive"]]
    ctrl = [k["item_id"] for k in keys if not k["substantive"]]
    common_sub = [i for i in common if i in sub]

    endpoints = {}
    for comp, name in (("false_closure", "false_closure_rate"),
                       ("missed_residual", "missed_residual_rate"),
                       ("abstention_appropriate_hit", "appropriate_abstention_rate"),
                       ("route_ok", "route_admissibility_accuracy"),
                       ("result_correct", "result_accuracy"),
                       ("burden_disposition_acc", "burden_disposition_accuracy")):
        endpoints[name] = {}
        for arm, items in (("baseline", base), ("treatment", treat)):
            fam, pooled = fam_pooled(items, keys, comp)
            endpoints[name][arm] = {"pooled_equal_family": pooled, "by_family": fam}

    endpoints["aurc"] = {arm: aurc_from_items(items, common)
                         for arm, items in (("baseline", base), ("treatment", treat))}
    endpoints["excess_aurc"] = {
        arm: (None if endpoints["aurc"][arm] is None else
              endpoints["aurc"][arm] - (optimal_aurc(items, common) or 0))
        for arm, items in (("baseline", base), ("treatment", treat))}
    endpoints["aurc_by_family"] = {}
    fam_of = {k["item_id"]: k["family"] for k in keys}
    for fam in sorted(set(fam_of.values())):
        ids = [i for i in common if fam_of[i] == fam]
        endpoints["aurc_by_family"][fam] = {
            "baseline": aurc_from_items(base, ids), "treatment": aurc_from_items(treat, ids)}
    endpoints["aurc_leave_one_family_out"] = {}
    for fam in sorted(set(fam_of.values())):
        ids = [i for i in common if fam_of[i] != fam]
        endpoints["aurc_leave_one_family_out"][fam] = {
            "baseline": aurc_from_items(base, ids), "treatment": aurc_from_items(treat, ids)}

    fc_diffs = [treat[i]["false_closure"] - base[i]["false_closure"]
                for i in common_sub
                if base[i]["false_closure"] is not None and treat[i]["false_closure"] is not None]
    fc_mean = (sum(fc_diffs) / len(fc_diffs)) if fc_diffs else None
    fc_p = perm_p_mean(fc_diffs)
    au_b, au_t = endpoints["aurc"]["baseline"], endpoints["aurc"]["treatment"]
    au_diff = None if au_b is None or au_t is None else au_t - au_b
    au_p = perm_p_aurc(base, treat, common) if common else None
    hp = holm({"false_closure": fc_p, "aurc": au_p})
    endpoints["false_closure_contrast"] = {
        "treatment_minus_baseline": fc_mean, "perm_p": fc_p,
        "holm_p": hp.get("false_closure"),
        "bootstrap_ci95": boot_ci(
            lambda s: (sum(treat[i]["false_closure"] - base[i]["false_closure"] for i in s) / len(s))
            if s else None, common_sub),
        "n_paired_items": len(fc_diffs)}
    endpoints["aurc_contrast"] = {
        "treatment_minus_baseline": au_diff, "perm_p": au_p, "holm_p": hp.get("aurc"),
        "bootstrap_ci95": boot_ci(
            lambda s: ((aurc_from_items(treat, s) or 0) - (aurc_from_items(base, s) or 0))
            if s else None, common)}
    ra_diffs = [treat[i]["result_correct"] - base[i]["result_correct"] for i in common_sub
                if base[i].get("result_correct") is not None
                and treat[i].get("result_correct") is not None]
    endpoints["result_accuracy_contrast"] = {
        "treatment_minus_baseline": (sum(ra_diffs) / len(ra_diffs)) if ra_diffs else None,
        "perm_p": perm_p_mean(ra_diffs)}
    ctrl_b = [base[i]["record_size"] for i in ctrl if i in base]
    ctrl_t = [treat[i]["record_size"] for i in ctrl if i in treat]
    endpoints["structure_overhead_ratio_on_controls"] = (
        (sum(ctrl_t) / len(ctrl_t)) / (sum(ctrl_b) / len(ctrl_b))
        if ctrl_b and ctrl_t else None)

    # failed-run worst-case bound: failures scored against their own arm
    wc = {}
    for arm in ("baseline", "treatment"):
        r = fail_rates.get(arm)
        pooled = endpoints["false_closure_rate"][arm]["pooled_equal_family"]
        wc[arm] = None if pooled is None or r is None else min(1.0, pooled + r)
    endpoints["false_closure_worst_case_bound"] = wc

    report = {"schema": "orthemology-fcsp2-report-v1", "packet_id": "FCSP-2",
              "synthetic_smoke": synthetic, "run_id": manifest.get("run_id"),
              "n_records": len(records), "failed_run_rate": fail_rates,
              "unit_of_inference": "item (paired across arms); repeats averaged within item",
              "endpoints": endpoints,
              "outcome_affecting_deviation": False}
    if synthetic:
        report["outcome"] = ("SYNTHETIC SMOKE TRAVERSAL — endpoints computed, decision rules "
                             "NOT adjudicated; no scientific result exists (Decision 0018)")
    else:
        report["outcome"] = decide(report, rules)

    io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(report, indent=2) + "\n")
    print("report:", a.out, "| synthetic:", synthetic, "| outcome:", report["outcome"][:70])


if __name__ == "__main__":
    main()
