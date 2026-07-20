#!/usr/bin/env python3
"""ER-1 deterministic smoke tests. NOT an experiment; produces no result.

1. committed fixtures equal regeneration;
2. both arm renderings cover every fact key (information-match contract);
3. schemas compile; mock answer records validate;
4. mock (synthetic_smoke) records traverse the frozen analysis end-to-end
   with no outcome adjudication.
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


def snapshot():
    out = {}
    fx = os.path.join(PKT, "fixtures")
    for base, _d, fns in os.walk(fx):
        for fn in fns:
            p = os.path.join(base, fn)
            out[os.path.relpath(p, fx)] = io.open(p, encoding="utf-8").read()
    return out


def main():
    import yaml
    before = snapshot()
    subprocess.check_call([sys.executable, os.path.join(PKT, "scripts", "generate_fixtures.py")],
                          stdout=subprocess.DEVNULL)
    after = snapshot()
    check("committed fixtures equal regeneration", before == after)
    if before != after:
        for rel, content in before.items():
            io.open(os.path.join(PKT, "fixtures", rel), "w",
                    encoding="utf-8", newline="").write(content)

    spec = yaml.safe_load(io.open(os.path.join(PKT, "E1-E5-SPEC.yaml"), encoding="utf-8"))
    cases = {c["id"]: c for c in spec["cases"]}
    check("five cases specified", sorted(cases) == ["E1", "E2", "E3", "E4", "E5"])
    check("E5 carries both neighbors",
          [n["id"] for n in cases["E5"].get("neighbors", [])] == ["E5a", "E5b"])

    # information-match: every fact key appears in both renderings
    for cid in cases:
        d = os.path.join(PKT, "fixtures", cid)
        facts = yaml.safe_load(io.open(os.path.join(d, "facts.yaml"), encoding="utf-8"))
        log = io.open(os.path.join(d, "baseline-log.md"), encoding="utf-8").read()
        ep = json.load(io.open(os.path.join(d, "treatment-episode.json"), encoding="utf-8"))
        n_facts = len(facts["fact_keys"])
        n_log = sum(1 for ln in log.splitlines() if ln[:1].isdigit())
        n_ep = len([k for k in ep if k not in ("schema", "case", "title")])
        check("%s renderings carry every fact atom (%d)" % (cid, n_facts),
              n_log == n_facts and n_ep == n_facts,
              "log=%d episode=%d" % (n_log, n_ep))

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
