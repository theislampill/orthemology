#!/usr/bin/env python3
"""FCSP-1 deterministic smoke tests. NOT an experiment; produces no result.

1. committed items equal the seeded regeneration (byte-for-byte);
2. items/manifest/output schemas compile and validate mock records;
3. mock (synthetic_smoke) runs traverse the frozen analysis end-to-end;
4. the report of a synthetic traversal carries no outcome adjudication.
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


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    items_path = os.path.join(PKT, "items", "ITEMS.json")
    committed = io.open(items_path, encoding="utf-8").read()
    subprocess.check_call([sys.executable, os.path.join(PKT, "scripts", "generate_items.py")],
                          stdout=subprocess.DEVNULL)
    regenerated = io.open(items_path, encoding="utf-8").read()
    check("committed items equal seeded regeneration", committed == regenerated)
    if committed != regenerated:  # restore, never leave drift behind
        io.open(items_path, "w", encoding="utf-8", newline="").write(committed)

    items = json.loads(committed)["items"]
    check("40 items, 8 negative controls",
          len(items) == 40 and sum(1 for i in items if not i["substantive"]) == 8)

    from jsonschema import Draft202012Validator
    out_schema = json.load(io.open(os.path.join(PKT, "OUTPUT.schema.json"), encoding="utf-8"))
    man_schema = json.load(io.open(os.path.join(PKT, "RUN-MANIFEST.schema.json"), encoding="utf-8"))
    Draft202012Validator.check_schema(out_schema)
    Draft202012Validator.check_schema(man_schema)
    vout = Draft202012Validator(out_schema)

    # mock records: baseline closes over everything; treatment ledgers burdens
    records = []
    for it in items:
        for arm in ("baseline", "treatment"):
            truth = it["ground_truth"]
            rec = {
                "item_id": it["item_id"], "arm": arm, "repeat": 1, "seed": 20260721,
                "parsed_ok": True, "synthetic_smoke": True,
                "record": {
                    "placement": ("abstain-escalate"
                                  if arm == "treatment" and truth["abstention_appropriate"]
                                  else ("no-defect" if not it["substantive"]
                                        else "defect-confirmed")),
                    "confidence": 0.9 if not it["substantive"] else 0.6,
                    "closure_claimed": (arm == "baseline") or truth["closure_legitimate"],
                    "residual_burdens": ([] if arm == "baseline" else
                                         [{"burden": b["burden"],
                                           "disposition": b["correct_disposition"]}
                                          for b in truth["residual_burdens"]]),
                    "record_tokens": 120 if arm == "baseline" else 180,
                },
            }
            errs = list(vout.iter_errors(rec))
            if errs:
                check("mock record validates (%s/%s)" % (it["item_id"], arm), False,
                      errs[0].message[:80])
            records.append(rec)
    check("every mock record schema-validates", not FAILS)

    manifest = {
        "packet_id": "FCSP-1",
        "packet_freeze_hash": "0" * 64,
        "run_id": "smoke-traversal",
        "run_authorized_by": "NONE — synthetic smoke, not a run",
        "started_at": "2026-07-20T00:00:00Z",
        "executor": {"model_id": "mock", "model_version_or_hash": "mock", "provider": "mock"},
        "sampling": {"temperature": 0.0, "top_p": 1.0, "max_output_tokens": 2048},
        "repeats": 1, "seeds": [20260721],
        "registration_state": "NOT_REGISTERED",
        "synthetic_smoke": True,
    }
    errs = list(Draft202012Validator(man_schema).iter_errors(manifest))
    check("mock manifest schema-validates", not errs, errs[0].message[:80] if errs else "")

    with tempfile.TemporaryDirectory() as td:
        runs = os.path.join(td, "runs.jsonl")
        io.open(runs, "w", encoding="utf-8", newline="\n").write(
            "\n".join(json.dumps(r) for r in records) + "\n")
        man = os.path.join(td, "manifest.json")
        io.open(man, "w", encoding="utf-8", newline="\n").write(json.dumps(manifest))
        rep = os.path.join(td, "report.json")
        subprocess.check_call([sys.executable, os.path.join(PKT, "analysis", "analyze_fcsp.py"),
                               "--runs", runs, "--manifest", man,
                               "--items", items_path, "--out", rep],
                              stdout=subprocess.DEVNULL)
        report = json.load(io.open(rep, encoding="utf-8"))
    check("analysis traverses mock data end-to-end", report["n_records"] == len(records))
    check("synthetic traversal is stamped synthetic", report["synthetic_smoke"] is True)
    check("synthetic traversal adjudicates NO outcome",
          "no scientific result" in report["outcome"])
    check("endpoints computed (false-closure + AURC present)",
          report["endpoints"]["false_closure_rate"]["baseline"]["pooled"] is not None
          and report["endpoints"]["aurc"]["treatment"] is not None)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
