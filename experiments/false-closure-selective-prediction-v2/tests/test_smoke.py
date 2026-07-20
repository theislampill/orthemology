#!/usr/bin/env python3
"""FCSP-2 deterministic smoke + isolation tests. NOT an experiment.

1. committed public items + keys equal seeded regeneration;
2. payload isolation: the harness's exact payloads contain no key material,
   family label, ground-truth token, or answer-bearing diagnostic phrase;
3. lexical + field-name leakage scans over the public file;
4. full mock end-to-end: harness -> parser -> analysis -> report, with all
   declared endpoints present and NO adjudicated outcome;
5. decision rules unit-tested on synthetic endpoint values (never run data).
"""
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(HERE)
FAILS = []

LEAK_TOKENS = ["stale", "not performed", "was not performed", "predecessor",
               "wrong scope", "false closure", "aliasing", "family", "ground_truth",
               "closure_legitimate", "abstention_appropriate", "correct_placement",
               "defect is", "the defect", "leak"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    pub_p = os.path.join(PKT, "items", "PUBLIC-ITEMS.json")
    key_p = os.path.join(PKT, "items", "KEYS.json")
    before = (io.open(pub_p, encoding="utf-8").read(), io.open(key_p, encoding="utf-8").read())
    subprocess.check_call([sys.executable, os.path.join(PKT, "scripts", "generate_items.py")],
                          stdout=subprocess.DEVNULL)
    after = (io.open(pub_p, encoding="utf-8").read(), io.open(key_p, encoding="utf-8").read())
    check("committed items+keys equal seeded regeneration", before == after)
    if before != after:
        io.open(pub_p, "w", encoding="utf-8", newline="").write(before[0])
        io.open(key_p, "w", encoding="utf-8", newline="").write(before[1])

    pub = json.loads(before[0])
    check("50 items (40 substantive + 10 controls)",
          pub["item_count"] == 50
          and sum(1 for k in json.loads(before[1])["keys"] if not k["substantive"]) == 10)

    low = before[0].lower()
    hits = [t for t in LEAK_TOKENS if t in low]
    check("public items pass the lexical/field-name leakage scan", not hits, str(hits))

    with tempfile.TemporaryDirectory() as td:
        man = os.path.join(td, "manifest.json")
        runs = os.path.join(td, "runs.jsonl")
        pays = os.path.join(td, "payloads.jsonl")
        raw = os.path.join(td, "raw.jsonl")
        subprocess.check_call([sys.executable, os.path.join(PKT, "harness", "run_fcsp.py"),
                               "--adapter", "mock", "--manifest", man, "--out", runs,
                               "--raw", raw, "--dump-payloads", pays],
                              stdout=subprocess.DEVNULL)
        payloads = [json.loads(ln) for ln in io.open(pays, encoding="utf-8")]
        check("harness emitted a payload per item-arm", len(payloads) == 100)
        keys_doc = json.loads(before[1])
        bad = []
        truth_tokens = set()
        for k in keys_doc["keys"]:
            truth_tokens.add(k["family"])
            for b in k["ground_truth"]["residual_burdens"]:
                truth_tokens.add(b["correct_disposition"] + '":')
        for p in payloads:
            pl = p["payload"]
            for tok in ("ground_truth", "closure_legitimate", "correct_placement",
                        "abstention_appropriate", "F1-aliasing", "F4-stale", "family"):
                if tok in pl:
                    bad.append("%s/%s: %s" % (p["item_id"], p["arm"], tok))
        check("payload isolation: no key/label/truth token in any exact payload",
              not bad, str(bad[:3]))

        # analysis end-to-end
        rep = os.path.join(td, "report.json")
        subprocess.check_call([sys.executable, os.path.join(PKT, "analysis", "analyze_fcsp2.py"),
                               "--runs", runs, "--manifest", man,
                               "--keys", key_p, "--out", rep],
                              stdout=subprocess.DEVNULL)
        report = json.load(io.open(rep, encoding="utf-8"))
    check("mock end-to-end traverses harness->parser->analysis", report["n_records"] == 100)
    check("synthetic traversal is stamped synthetic and unadjudicated",
          report["synthetic_smoke"] is True and "no scientific result" in report["outcome"])
    declared = ["false_closure_rate", "missed_residual_rate", "appropriate_abstention_rate",
                "route_admissibility_accuracy", "result_accuracy",
                "burden_disposition_accuracy", "aurc", "excess_aurc", "aurc_by_family",
                "aurc_leave_one_family_out", "false_closure_contrast", "aurc_contrast",
                "result_accuracy_contrast", "structure_overhead_ratio_on_controls",
                "false_closure_worst_case_bound"]
    missing = [e for e in declared if e not in report["endpoints"]]
    check("every declared endpoint appears in the report", not missing, str(missing))
    check("Holm-adjusted primaries present",
          report["endpoints"]["false_closure_contrast"]["holm_p"] is not None
          and report["endpoints"]["aurc_contrast"]["holm_p"] is not None)
    check("unit statement present",
          "item" in report["unit_of_inference"])

    # decision rules unit-tested on synthetic endpoint values (not run data)
    sys.path.insert(0, os.path.join(PKT, "analysis"))
    import yaml
    from analyze_fcsp2 import decide
    rules = yaml.safe_load(io.open(os.path.join(PKT, "DECISION-RULES.yaml"), encoding="utf-8"))

    def fake(fc_d, fc_p, au_d, au_p, ra_d=0.0, ra_p=1.0, ov=1.2, fail=0.0):
        return {"failed_run_rate": {"baseline": fail, "treatment": fail},
                "outcome_affecting_deviation": False,
                "endpoints": {
                    "false_closure_contrast": {"treatment_minus_baseline": fc_d, "holm_p": fc_p},
                    "aurc_contrast": {"treatment_minus_baseline": au_d, "holm_p": au_p},
                    "result_accuracy_contrast": {"treatment_minus_baseline": ra_d, "perm_p": ra_p},
                    "structure_overhead_ratio_on_controls": ov}}
    check("decision: supports fires on strong dual win",
          decide(fake(-0.15, 0.01, -0.08, 0.01), rules) == "supports incremental value")
    check("decision: adequately designed null is does-not-yet-support",
          decide(fake(-0.02, 0.60, -0.01, 0.70), rules).startswith("does not yet support"))
    check("decision: harm fires on accuracy degradation",
          decide(fake(-0.15, 0.01, -0.08, 0.01, ra_d=-0.10, ra_p=0.01), rules).startswith("evidence of harm"))
    check("decision: failed-run gate names inconclusive",
          decide(fake(-0.15, 0.01, -0.08, 0.01, fail=0.10), rules).startswith("inconclusive"))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
