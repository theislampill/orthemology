#!/usr/bin/env python3
"""ER-1 deterministic smoke tests. NOT an experiment; produces no result.

1. seeded public rendering is deterministic without committed fixture files;
2. both arm renderings cover every fact key (information-match contract);
3. schemas compile; mock answer records validate;
4. mock (synthetic_smoke) records traverse the frozen analysis end-to-end
   with no outcome adjudication.
"""
import argparse
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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--public-only", action="store_true",
                    help="check public rendering only, without scoring or synthetic runs")
    args = ap.parse_args()
    import yaml
    sys.path.insert(0, os.path.join(PKT, "scripts"))
    from generate_fixtures import CASES, public_files
    rendered = public_files()
    check("public rendering is deterministic", rendered == public_files())
    check("complete five-case public population", sorted(CASES) == ["E1", "E2", "E3", "E4", "E5"]
          and len(rendered) == 15)
    for cid, canonical in CASES.items():
        facts = yaml.safe_load(rendered[cid + "/facts.yaml"])
        log = rendered[cid + "/baseline-log.md"]
        ep = json.loads(rendered[cid + "/treatment-episode.json"])
        n_facts = len(facts["fact_keys"])
        n_log = sum(1 for ln in log.splitlines() if ln[:1].isdigit())
        n_ep = len([k for k in ep if k not in ("schema", "case", "title")])
        check("%s renderings carry every fact atom (%d)" % (cid, n_facts),
              n_log == n_facts and n_ep == n_facts,
              "log=%d episode=%d" % (n_log, n_ep))
        check("%s preserves the actual premises in both arms" % cid,
              all(sentence in log and ep[field] == value
                  for _key, sentence, field, value in canonical["facts"]))
    if args.public_only:
        print("TOTAL: %d failures; public rendering only, no experiment" % len(FAILS))
        sys.exit(1 if FAILS else 0)

    spec = yaml.safe_load(io.open(os.path.join(PKT, "E1-E5-SPEC.yaml"), encoding="utf-8"))
    cases = {c["id"]: c for c in spec["cases"]}
    check("five cases specified", sorted(cases) == ["E1", "E2", "E3", "E4", "E5"])
    check("E5 carries both neighbors",
          [n["id"] for n in cases["E5"].get("neighbors", [])] == ["E5a", "E5b"])

    from jsonschema import Draft202012Validator
    out_schema = json.load(io.open(os.path.join(PKT, "OUTPUT.schema.json"), encoding="utf-8"))
    man_schema = json.load(io.open(os.path.join(PKT, "RUN-MANIFEST.schema.json"), encoding="utf-8"))
    Draft202012Validator.check_schema(out_schema)
    Draft202012Validator.check_schema(man_schema)
    vout = Draft202012Validator(out_schema)

    records = []
    for cid, case in cases.items():
        gt = case["ground_truth"]
        for arm in ("baseline", "treatment"):
            rec = {"case_id": cid, "arm": arm, "repeat": 1, "synthetic_smoke": True,
                   "answer_tokens": 90 if arm == "baseline" else 120,
                   "answers": {
                       "defect_identified": gt["pathway_defect"] if arm == "treatment" else "none",
                       "grounding_element": "record field" if arm == "treatment" else None,
                       "remedy": gt["correct_remedy"] if arm == "treatment" else "none",
                       "endorse_completion": (arm == "baseline") or bool(gt["closure_legitimate"]),
                       "neighbors_used": arm == "treatment" and cid == "E5"}}
            errs = list(vout.iter_errors(rec))
            if errs:
                check("mock record validates (%s/%s)" % (cid, arm), False, errs[0].message[:80])
            records.append(rec)
    check("every mock answer record schema-validates", not FAILS)

    manifest = {"packet_id": "ER-1", "packet_freeze_hash": "0" * 64,
                "run_id": "smoke-traversal",
                "run_authorized_by": "NONE — synthetic smoke, not a run",
                "started_at": "2026-07-20T00:00:00Z",
                "executor": {"model_id": "mock", "model_version_or_hash": "mock", "provider": "mock"},
                "sampling": {"temperature": 0.0, "top_p": 1.0, "max_output_tokens": 2048},
                "repeats": 1, "seeds": [20260731],
                "registration_state": "NOT_REGISTERED", "synthetic_smoke": True}
    errs = list(Draft202012Validator(man_schema).iter_errors(manifest))
    check("mock manifest schema-validates", not errs, errs[0].message[:80] if errs else "")

    with tempfile.TemporaryDirectory() as td:
        runs = os.path.join(td, "runs.jsonl")
        io.open(runs, "w", encoding="utf-8", newline="\n").write(
            "\n".join(json.dumps(r) for r in records) + "\n")
        man = os.path.join(td, "manifest.json")
        io.open(man, "w", encoding="utf-8", newline="\n").write(json.dumps(manifest))
        rep = os.path.join(td, "report.json")
        subprocess.check_call([sys.executable, os.path.join(PKT, "analysis", "analyze_er.py"),
                               "--runs", runs, "--manifest", man,
                               "--spec", os.path.join(PKT, "E1-E5-SPEC.yaml"), "--out", rep],
                              stdout=subprocess.DEVNULL)
        report = json.load(io.open(rep, encoding="utf-8"))
    check("analysis traverses mock data end-to-end", report["n_records"] == len(records))
    check("synthetic traversal is stamped synthetic", report["synthetic_smoke"] is True)
    check("synthetic traversal adjudicates NO outcome",
          "no scientific result" in report["outcome"])

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
