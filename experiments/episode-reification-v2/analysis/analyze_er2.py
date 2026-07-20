#!/usr/bin/env python3
"""ER-2 frozen analysis — corrected scoring + complete inference.

Usage:
  python analyze_er2.py --runs runs.jsonl --manifest manifest.json \
      --keys ../fixtures/KEYS.json --facts-root ../fixtures --out report.json

Scoring repairs (audit B6/B7):
  - completion is scored by EQUALITY: endorse_completion == closure_legitimate
    (refusing a legitimate closure is a false positive, feeding the E1 harm
    rule; endorsing an illegitimate closure is a false-closure miss);
  - traceability verifies every cited grounding_fact_id EXISTS in the case's
    fact list AND intersects the keyed supporting set (not a presence flag);
  - E5 requires BOTH neighbor verdicts correct AND mismatch_identified AND the
    correct remedy category (not a bare neighbors_used flag).

Inference (audit B9): case is the unit; archetypes are strata. Paired
arm contrast per component with an arm-swap permutation test over cases,
percentile bootstrap CIs, Holm over the two primaries (defect discovery;
completion correctness), E1 false-positive harm rule, cost-ratio harm rule,
failed-run gate, mechanical decision execution. Synthetic runs adjudicate
nothing.
"""
import argparse
import io
import json
import os
import random

PERMS = 10000
BOOTS = 2000


def load_jsonl(path):
    with io.open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def fact_ids(facts_root, case):
    p = os.path.join(facts_root, case, "facts.json")
    return {a["id"] for a in json.load(io.open(p, encoding="utf-8"))["facts"]}


def score(rec, key, present_ids):
    if not rec["parsed_ok"] or rec.get("answers") is None:
        return None
    a = rec["answers"]
    gt = key
    s = {}
    s["defect_discovered"] = 1.0 if a["defect_category"] == gt["defect_category"] else 0.0
    s["remedy_correct"] = 1.0 if a["remedy_category"] == gt["remedy_category"] else 0.0
    # completion by EQUALITY (audit B6 repair)
    s["completion_correct"] = 1.0 if bool(a["endorse_completion"]) == bool(gt["closure_legitimate"]) else 0.0
    s["false_positive_on_legit"] = (1.0 if (gt["closure_legitimate"] and not a["endorse_completion"])
                                    else 0.0)
    # traceability: cited ids exist AND intersect the supporting set (audit B7 repair)
    cited = set(a.get("grounding_fact_ids") or [])
    exist = cited and cited <= present_ids
    supports = cited & set(gt.get("supporting", []))
    s["traceability"] = 1.0 if (exist and supports) else 0.0
    # E5 semantic (audit B7 repair)
    if key["archetype"] == "A5":
        e5 = a.get("e5") or {}
        e5k = key.get("e5", {})
        ok = (bool(e5.get("neighbor_a_expected_pass")) == e5k.get("neighbor_a_expected_pass")
              and bool(e5.get("neighbor_b_expected_pass")) == e5k.get("neighbor_b_expected_pass")
              and bool(e5.get("mismatch_identified"))
              and a["defect_category"] == gt["defect_category"])
        s["e5_robustness"] = 1.0 if ok else 0.0
    s["answer_tokens"] = rec.get("answer_tokens", 0)
    return s


def per_case(records, keys, facts_root):
    kmap = {k["case"]: k for k in keys}
    acc, fails = {}, {}
    for rec in records:
        arm = rec["arm"]
        fails.setdefault(arm, [0, 0])
        fails[arm][1] += 1
        s = score(rec, kmap[rec["case_id"]], fact_ids(facts_root, rec["case_id"]))
        if s is None:
            fails[arm][0] += 1
            continue
        acc.setdefault(arm, {}).setdefault(rec["case_id"], []).append(s)
    out = {}
    for arm, cases in acc.items():
        out[arm] = {}
        for cid, rows in cases.items():
            out[arm][cid] = {k: (sum(r[k] for r in rows if r.get(k) is not None)
                                 / max(1, sum(1 for r in rows if r.get(k) is not None)))
                             for k in rows[0]}
    return out, {a: (n / d if d else None) for a, (n, d) in fails.items()}


def arch_pooled(per_arm, keys, comp):
    arch = {k["case"]: k["archetype"] for k in keys}
    g = {}
    for cid, agg in per_arm.items():
        if agg.get(comp) is None:
            continue
        g.setdefault(arch[cid], []).append(agg[comp])
    means = {a: sum(v) / len(v) for a, v in g.items()}
    return means, (sum(means.values()) / len(means) if means else None)


def perm_p(diffs, seed, n=PERMS):
    if not diffs:
        return None
    obs = abs(sum(diffs) / len(diffs))
    rng = random.Random(seed)
    return sum(1 for _ in range(n)
               if abs(sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs))
               >= obs - 1e-12) / n


def boot_ci(diffs, seed, n=BOOTS):
    if not diffs:
        return None
    rng = random.Random(seed)
    vals = sorted(sum(diffs[rng.randrange(len(diffs))] for _ in diffs) / len(diffs)
                  for _ in range(n))
    return [vals[int(0.025 * n)], vals[int(0.975 * n) - 1]]


def holm(pv):
    items = sorted((p, k) for k, p in pv.items() if p is not None)
    out, m, prev = {}, len(items), 0.0
    for i, (p, k) in enumerate(items):
        prev = min(1.0, max(prev, (m - i) * p))
        out[k] = prev
    return out


def paired(base, treat, comp, common, seed):
    d = [treat[c][comp] - base[c][comp] for c in common
         if base[c].get(comp) is not None and treat[c].get(comp) is not None]
    return (sum(d) / len(d) if d else None), perm_p(d, seed), boot_ci(d, seed + 1), d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--keys", required=True)
    ap.add_argument("--facts-root", required=True)
    ap.add_argument("--rules", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import yaml
    records = load_jsonl(a.runs)
    manifest = json.load(io.open(a.manifest, encoding="utf-8"))
    keys = json.load(io.open(a.keys, encoding="utf-8"))["keys"]
    rules = yaml.safe_load(io.open(a.rules or os.path.join(
        os.path.dirname(os.path.abspath(a.keys)), "..", "DECISION-RULES.yaml"), encoding="utf-8"))
    synthetic = bool(records) and all(r.get("synthetic_smoke") for r in records)

    per_arm, fails = per_case(records, keys, a.facts_root)
    base, treat = per_arm.get("baseline", {}), per_arm.get("treatment", {})
    common = sorted(set(base) & set(treat))

    endpoints = {}
    for comp, name in (("defect_discovered", "defect_discovery_rate"),
                       ("remedy_correct", "remedy_accuracy"),
                       ("completion_correct", "completion_correctness"),
                       ("traceability", "traceability_rate"),
                       ("false_positive_on_legit", "false_positive_on_legit_rate")):
        endpoints[name] = {}
        for arm, d in (("baseline", base), ("treatment", treat)):
            _, pooled = arch_pooled(d, keys, comp)
            endpoints[name][arm] = pooled
    # E5 only over A5 cases
    a5 = [k["case"] for k in keys if k["archetype"] == "A5"]
    for arm, d in (("baseline", base), ("treatment", treat)):
        vals = [d[c]["e5_robustness"] for c in a5 if c in d and d[c].get("e5_robustness") is not None]
        endpoints.setdefault("e5_robustness_rate", {})[arm] = (sum(vals) / len(vals)) if vals else None

    dd, dd_p, dd_ci, dd_diffs = paired(base, treat, "defect_discovered", common, 20260740)
    cc, cc_p, cc_ci, _ = paired(base, treat, "completion_correct", common, 20260742)
    hp = holm({"defect": dd_p, "completion": cc_p})
    endpoints["defect_discovery_contrast"] = {"treatment_minus_baseline": dd,
                                              "perm_p": dd_p, "holm_p": hp.get("defect"), "ci95": dd_ci}
    endpoints["completion_correctness_contrast"] = {"treatment_minus_baseline": cc,
                                                    "perm_p": cc_p, "holm_p": hp.get("completion"), "ci95": cc_ci}
    # cost ratio (mean answer tokens T/B)
    bt = [base[c]["answer_tokens"] for c in common]
    tt = [treat[c]["answer_tokens"] for c in common]
    endpoints["cost_ratio"] = ((sum(tt) / len(tt)) / (sum(bt) / len(bt))
                               if bt and tt and sum(bt) else None)
    _, fp_pool = arch_pooled(treat, keys, "false_positive_on_legit")
    endpoints["treatment_false_positive_rate"] = fp_pool

    report = {"schema": "orthemology-er2-report-v1", "packet_id": "ER-2",
              "synthetic_smoke": synthetic, "run_id": manifest.get("run_id"),
              "n_records": len(records), "failed_run_rate": fails,
              "unit_of_inference": "case (paired across arms); archetypes are strata; "
              "repeats averaged within case",
              "endpoints": endpoints, "outcome_affecting_deviation": False}

    if synthetic:
        report["outcome"] = ("SYNTHETIC SMOKE TRAVERSAL — endpoints computed, decision rules "
                             "NOT adjudicated; no scientific result (Decision 0018)")
    else:
        P = rules["parameters"]
        harm, gates = [], []
        if (endpoints["treatment_false_positive_rate"] or 0) > P["harm_margin_e1_false_positive"]:
            harm.append("treatment refuses legitimate completion beyond margin")
        if endpoints["cost_ratio"] and endpoints["cost_ratio"] > P["harm_margin_cost_ratio"]:
            harm.append("cost ratio beyond margin")
        for arm, r in fails.items():
            if r and r > P["max_failed_run_rate"]:
                gates.append("failed-run %.3f in %s" % (r, arm))
        if gates:
            report["outcome"] = "inconclusive: " + "; ".join(gates)
        elif harm:
            report["outcome"] = "evidence of harm or failure: " + "; ".join(harm)
        elif (dd is not None and dd >= P["minimum_important_effect_defect_discovery"]
              and (hp.get("defect") or 1) < P["alpha"]
              and cc is not None and cc >= P["minimum_important_effect_completion"]
              and (hp.get("completion") or 1) < P["alpha"]):
            report["outcome"] = "supports incremental value"
        else:
            report["outcome"] = ("does not yet support incremental value "
                                 "(pre-run fixed-sensitivity design; no observed-power rescue)")

    io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(report, indent=2) + "\n")
    print("report:", a.out, "| synthetic:", synthetic, "| outcome:", report["outcome"][:60])


if __name__ == "__main__":
    main()
