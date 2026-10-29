#!/usr/bin/env python3
"""ER-2 deterministic smoke + isolation tests. NOT an experiment.

1. public renderings are deterministic; the separate scoring key still equals
   seeded regeneration in the full (non-public-only) smoke;
2. fact-atom parity: both arm renderings carry exactly the same fact IDs
   (information match, audit H2);
3. label-free payloads: harness payloads contain no KEYS token, archetype
   label, defect flag, or diagnostic conclusion (audit B8/H1);
4. corrected scoring is exercised: the E1 EQUALITY fix (refusing legitimate
   closure scores wrong), semantic traceability, semantic E5;
5. full mock end-to-end with no adjudicated outcome.
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
FIX = os.path.join(PKT, "fixtures")
FAILS = []

LABEL_TOKENS = ["KEYS", "stopped-clock", "justified rare miss", "defective binding",
                "metamorphic", "binding_defect", "reliability_note", "archetype",
                "closure_legitimate", "defect_category", "A1", "A2", "A3", "A4", "A5",
                "out-of-date", "wrong-edition", "resolution-limit"]


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--public-only", action="store_true",
                    help="check public rendering/payloads without keys, scorer or adapters")
    args = ap.parse_args()
    sys.path.insert(0, os.path.join(PKT, "scripts"))
    from generate_cases import public_cases, public_files, scoring_keys
    canonical = public_cases()
    rendered = public_files()
    check("seeded public rendering is deterministic", rendered == public_files())
    check("complete 20-case public population", sorted(canonical) == ["C%02d" % n for n in range(1, 21)]
          and len(rendered) == 60)
    check("no scoring key is returned as public material", "KEYS.json" not in rendered)
    for cid, facts in canonical.items():
        log = rendered[cid + "/baseline-record.md"]
        treatment = json.loads(rendered[cid + "/treatment-record.json"])
        carried = {a["fact_id"]: a["text"] for section in treatment["sections"].values() for a in section}
        check("%s: both arms carry every fact atom" % cid,
              carried == {a["id"]: a["text"] for a in facts}
              and all("[" + a["id"] + "] " + a["text"] in log for a in facts))

    bad = []
    for cid in canonical:
        for arm_file in ("baseline-record.md", "treatment-record.json"):
            txt = rendered[cid + "/" + arm_file]
            for tok in LABEL_TOKENS:
                if tok in txt:
                    bad.append("%s/%s: %s" % (cid, arm_file, tok))
    check("runner-visible renderings are label-free", not bad, str(bad[:4]))
    sys.path.insert(0, os.path.join(PKT, "harness"))
    from run_er import cases, payload
    check("harness uses the complete seeded public population", cases() == sorted(canonical))
    pbad = []
    for cid in canonical:
        for arm in ("baseline", "treatment"):
            material = payload(cid, arm).split("Answer about the case record above", 1)[0]
            pbad.extend("%s/%s: %s" % (cid, arm, tok) for tok in LABEL_TOKENS if tok in material)
    check("no KEYS/label token in assembled case material", not pbad, str(pbad[:3]))
    if args.public_only:
        print("TOTAL: %d failures; public rendering only, no experiment" % len(FAILS))
        sys.exit(1 if FAILS else 0)

    key_text = io.open(os.path.join(FIX, "KEYS.json"), encoding="utf-8").read()
    check("separate scoring key equals seeded regeneration", key_text == scoring_keys())
    keys = json.loads(key_text)["keys"]
    check("20 cases, 5 archetypes x 4 variants",
          len(keys) == 20 and len({k["archetype"] for k in keys}) == 5)
    check("scoring and public cases have identical identities",
          {k["case"] for k in keys} == set(canonical))

    # corrected scoring: E1 equality + semantic traceability + semantic E5
    sys.path.insert(0, os.path.join(PKT, "analysis"))
    from analyze_er2 import score
    a1 = next(k for k in keys if k["archetype"] == "A1")
    facts_a1 = {a["id"] for a in canonical[a1["case"]]}
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
    facts_a5 = {a["id"] for a in canonical[a5["case"]]}
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
                               "--out", rep], stdout=subprocess.DEVNULL)
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
