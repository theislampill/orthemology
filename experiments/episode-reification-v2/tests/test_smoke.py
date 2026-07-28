#!/usr/bin/env python3
"""ER-2 deterministic smoke + isolation tests. NOT an experiment.

1. committed fixtures+keys equal seeded regeneration;
2. fact-atom parity: both arm renderings carry exactly the same fact IDs
   (information match, audit H2);
3. label-free payloads: harness payloads contain no KEYS token, archetype
   label, defect flag, or diagnostic conclusion (audit B8/H1);
4. corrected scoring is exercised: the E1 EQUALITY fix (refusing legitimate
   closure scores wrong), semantic traceability, semantic E5;
5. full mock end-to-end with no adjudicated outcome.
"""
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(HERE)
FIX = os.path.join(PKT, "fixtures")
FAILS = []

LABEL_TOKENS = ["stopped-clock", "justified rare miss", "defective binding",
                "metamorphic", "binding_defect", "reliability_note", "archetype",
                "closure_legitimate", "defect_category", "A1", "A2", "A3", "A4", "A5",
                "out-of-date", "wrong-edition", "resolution-limit"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def snapshot():
    out = {}
    for base, _d, fns in os.walk(FIX):
        for fn in fns:
            p = os.path.join(base, fn)
            out[os.path.relpath(p, FIX)] = io.open(p, encoding="utf-8").read()
    return out


def main():
    before = snapshot()
    subprocess.check_call([sys.executable, os.path.join(PKT, "scripts", "generate_cases.py")],
                          stdout=subprocess.DEVNULL)
    after = snapshot()
    check("committed fixtures+keys equal seeded regeneration", before == after)
    if before != after:
        for rel, c in before.items():
            io.open(os.path.join(FIX, rel), "w", encoding="utf-8", newline="").write(c)

    keys = json.load(io.open(os.path.join(FIX, "KEYS.json"), encoding="utf-8"))["keys"]
    check("20 cases, 5 archetypes x 4 variants",
          len(keys) == 20 and len({k["archetype"] for k in keys}) == 5)

    # fact-atom parity: both renderings mention every fact id
    for k in keys:
        cid = k["case"]
        facts = json.load(io.open(os.path.join(FIX, cid, "facts.json"), encoding="utf-8"))["facts"]
        ids = [a["id"] for a in facts]
        log = io.open(os.path.join(FIX, cid, "baseline-record.md"), encoding="utf-8").read()
        treat = json.dumps(json.load(io.open(os.path.join(FIX, cid, "treatment-record.json"),
                                             encoding="utf-8")))
        log_ok = all(fid in log for fid in ids)
        treat_ok = all(fid in treat for fid in ids)
        check("%s: both arms carry every fact atom" % cid, log_ok and treat_ok,
              "log=%s treat=%s" % (log_ok, treat_ok))

    # label-free renderings
    bad = []
    for k in keys:
        cid = k["case"]
        for arm_file in ("baseline-record.md", "treatment-record.json"):
            txt = io.open(os.path.join(FIX, cid, arm_file), encoding="utf-8").read()
            for tok in LABEL_TOKENS:
                if tok in txt:
                    bad.append("%s/%s: %s" % (cid, arm_file, tok))
    check("runner-visible renderings are label-free", not bad, str(bad[:4]))

    # corrected scoring: E1 equality + semantic traceability + semantic E5
    sys.path.insert(0, os.path.join(PKT, "analysis"))
    from analyze_er2 import score
    a1 = next(k for k in keys if k["archetype"] == "A1")
    facts_a1 = {a["id"] for a in json.load(io.open(os.path.join(FIX, a1["case"], "facts.json"),
                                                   encoding="utf-8"))["facts"]}
    endorse = {"case_id": a1["case"], "arm": "treatment", "parsed_ok": True,
               "answers": {"defect_category": "none", "grounding_fact_ids": list(a1["supporting"]),
                           "remedy_category": "none", "endorse_completion": True}}
    refuse = dict(endorse)
    refuse["answers"] = dict(endorse["answers"], endorse_completion=False)
    s_e = score(endorse, a1, facts_a1)
    s_r = score(refuse, a1, facts_a1)
    check("A1 endorsing legitimate completion scores correct",
          s_e["completion_correct"] == 1.0 and s_e["false_positive_on_legit"] == 0.0)
    check("A1 refusing legitimate completion scores WRONG + false-positive (E1 bug fixed)",
          s_r["completion_correct"] == 0.0 and s_r["false_positive_on_legit"] == 1.0)
    # traceability: invented id fails
    inv = dict(endorse); inv["answers"] = dict(endorse["answers"], grounding_fact_ids=["F99"])
    check("traceability rejects a non-existent grounding id", score(inv, a1, facts_a1)["traceability"] == 0.0)
    # E5 semantic
    a5 = next(k for k in keys if k["archetype"] == "A5")
    facts_a5 = {a["id"] for a in json.load(io.open(os.path.join(FIX, a5["case"], "facts.json"),
                                                   encoding="utf-8"))["facts"]}
    good_e5 = {"case_id": a5["case"], "arm": "treatment", "parsed_ok": True,
               "answers": {"defect_category": a5["defect_category"],
                           "grounding_fact_ids": list(a5["supporting"]),
                           "remedy_category": a5["remedy_category"], "endorse_completion": False,
                           "e5": {"neighbor_a_expected_pass": a5["e5"]["neighbor_a_expected_pass"],
                                  "neighbor_b_expected_pass": a5["e5"]["neighbor_b_expected_pass"],
                                  "mismatch_identified": True}}}
    flag_only = dict(good_e5)
    flag_only["answers"] = dict(good_e5["answers"],
                                e5={"neighbor_a_expected_pass": True, "neighbor_b_expected_pass": True,
                                    "mismatch_identified": True})
    check("E5 passes on both-neighbors-correct + mismatch + remedy",
          score(good_e5, a5, facts_a5)["e5_robustness"] == 1.0)
    check("E5 fails on a bare/incorrect neighbor flag",
          score(flag_only, a5, facts_a5)["e5_robustness"] == 0.0)

    # end-to-end
    with tempfile.TemporaryDirectory() as td:
        man = os.path.join(td, "m.json"); runs = os.path.join(td, "r.jsonl")
        pays = os.path.join(td, "p.jsonl"); rep = os.path.join(td, "rep.json")
        subprocess.check_call([sys.executable, os.path.join(PKT, "harness", "run_er.py"),
                               "--adapter", "mock", "--manifest", man, "--out", runs,
                               "--dump-payloads", pays], stdout=subprocess.DEVNULL)
        payloads = [json.loads(ln) for ln in io.open(pays, encoding="utf-8")]
        # scan the CASE MATERIAL only: both arms receive an identical answer-schema
        # probe (the shared closed response vocabulary), which is not a between-arm
        # confound; strip it before scanning so we test the case rendering, not the
        # shared response format.
        pbad = []
        for p in payloads:
            material = p["payload"].split("Answer about the case record above", 1)[0]
            for tok in LABEL_TOKENS:
                if tok in material:
                    pbad.append("%s/%s: %s" % (p["case"], p["arm"], tok))
        check("no KEYS/label token in any exact payload's case material", not pbad, str(pbad[:3]))
        subprocess.check_call([sys.executable, os.path.join(PKT, "analysis", "analyze_er2.py"),
                               "--runs", runs, "--manifest", man,
                               "--keys", os.path.join(FIX, "KEYS.json"),
                               "--facts-root", FIX, "--out", rep], stdout=subprocess.DEVNULL)
        report = json.load(io.open(rep, encoding="utf-8"))
    check("mock end-to-end traverses harness->parser->analysis", report["n_records"] == 40)
    check("synthetic traversal stamped + unadjudicated",
          report["synthetic_smoke"] is True and "no scientific result" in report["outcome"])
    for e in ("defect_discovery_contrast", "completion_correctness_contrast",
              "traceability_rate", "e5_robustness_rate", "cost_ratio",
              "treatment_false_positive_rate"):
        check("endpoint %s present" % e, e in report["endpoints"])
    check("Holm-adjusted primaries present",
          report["endpoints"]["defect_discovery_contrast"]["holm_p"] is not None
          and report["endpoints"]["completion_correctness_contrast"]["holm_p"] is not None)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
