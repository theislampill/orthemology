#!/usr/bin/env python3
"""Current-DAEE runtime crosswalk validator (R7D, Phase G, audit B24/B25).

Deterministic, offline. Guards the read-only adjudication of the CURRENT daee-epistemics
runtime objects:

  1. the dual pin coincides (historical R7B pin == current-reviewed pin == c86b3c66) and
     is recorded, so no session chases a nonexistent published delta;
  2. every mandatory DAEE object is present in the correspondence table, each mapped as
     an application-extension (never a core primitive) with per-row non-claims;
  3. the boundary firewall (no import as core primitive; co-development != validation) is
     declared.

Reads only committed repo files; performs no network call.
"""
import io
import os
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
PIN = "c86b3c6673147b8802fe222373a165a37d4d24a8"
FAILS = []
MANDATORY = {"Diagnostic IR", "burden nodes + dependency graph", "owner activation plan",
             "route pressure (nabla)", "Delta", "field_witness", "normalized activation record (NAR)",
             "Mid-Reread Pressure (MRP)", "R(H, Delta)", "Psi-N", "Psi-I", "T_lang",
             "hard registers / live lenses"}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def main():
    cw = yaml.safe_load(read(APP + "/CURRENT-RUNTIME-CROSSWALK.yaml"))

    dp = cw.get("dual_pin", {})
    check("dual pin: historical R7B pin == current live main == c86b3c66",
          dp.get("historical_r7b_pin") == PIN and dp.get("current_live_main") == PIN and dp.get("coincide") is True)
    check("dual pin records the read-only grounding", bool(dp.get("verified_read_only")))

    objs = {r["daee_object"] for r in cw.get("correspondence", [])}
    missing = MANDATORY - objs
    check("every mandatory DAEE object is adjudicated", not missing, "missing=%s" % sorted(missing))
    for r in cw.get("correspondence", []):
        check("correspondence %s is an application-extension (not core primitive)" % r["daee_object"],
              r.get("mapping_type") == "application-extension")
        check("correspondence %s carries non-claims" % r["daee_object"], bool(r.get("non_claims")))

    # the load-bearing non-conflations are present somewhere in the table
    blob = yaml.safe_dump(cw).lower()
    for phrase in ["not ground truth", "not a differential gradient", "not result correctness",
                   "not the full world", "runtime closure is not human restoration",
                   "not school-neutral core primitives"]:
        check("crosswalk asserts boundary: %r" % phrase, phrase in blob)

    top = " ".join(cw.get("non_claims", [])).lower()
    check("firewall: co-development is not validation (shared lineage)",
          "not validation" in top and "lineage" in top)
    check("firewall: no DAEE object imported as a core primitive",
          "core primitive" in top)

    # file-by-file adjudication uses only the closed disposition vocabulary
    DISPO = {"keep-old-reading", "revise-crosswalk", "new-application-extension", "defer", "reject"}
    for fa in cw.get("file_adjudication", []):
        check("file adjudication %s uses a valid disposition" % fa.get("file"),
              fa.get("disposition") in DISPO, repr(fa.get("disposition")))

    # the boundary + adjudication docs exist
    for rel in [APP + "/CURRENT-RUNTIME-BOUNDARY.md", "docs/project-closure/r7d/DAEE-CURRENT-DELTA-ADJUDICATION.md"]:
        check("%s exists" % rel, os.path.exists(os.path.join(ROOT, rel)))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
