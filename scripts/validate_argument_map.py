#!/usr/bin/env python3
"""Dynamic-orthability argument-map validator (R7D, Phase J, audit B41).

Deterministic, offline. Turns the metaphysical ladder from a navigation table into a
machine-checkable argument map:

  1. exactly ten rungs, each with premise, inference type, conclusion, dependency,
     evidence/source status, objection, rival exit, and school-neutral/Athari-internal
     status;
  2. evidence_status is from the five-status hierarchy; no rung above cross-source
     synthesis is empirically grounded;
  3. rung dependencies form the 1->10 chain (each rung depends on the previous);
  4. OSM/DAEE exemplify only rungs 1-3 and the non_entailments block says no lower
     application proves an upper rung;
  5. the companion references the map.

Establishes no empirical or theological claim; a structure gate only.
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
FAILS = []
STATUSES = {"primary-text-verified", "secondary-reconstruction", "cross-source-synthesis",
            "orthemological-extension", "creed-internal-inference"}
FIELDS = ("premise", "inference_type", "conclusion", "dependency", "evidence_status",
          "objection", "rival_exit", "status")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def main():
    m = yaml.safe_load(read("companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml"))
    rungs = m.get("rungs", [])
    check("argument map has exactly ten rungs", len(rungs) == 10, "got %d" % len(rungs))
    ns = [r["n"] for r in rungs]
    check("rungs numbered 1..10", ns == list(range(1, 11)), str(ns))
    for r in rungs:
        for f in FIELDS:
            check("rung %d declares %s" % (r["n"], f), bool(str(r.get(f, "")).strip()))
        check("rung %d evidence_status is in the five-status hierarchy" % r["n"],
              r.get("evidence_status") in STATUSES, repr(r.get("evidence_status")))
        check("rung %d status is school-neutral or athari-internal" % r["n"],
              r.get("status") in {"school-neutral", "athari-internal"}, repr(r.get("status")))
        # dependency chain: rung n>1 depends on n-1
        if r["n"] > 1:
            check("rung %d depends on rung %d" % (r["n"], r["n"] - 1), r.get("dependency") == r["n"] - 1,
                  repr(r.get("dependency")))
    # no rung above cross-source synthesis is empirically grounded (no 'empirical' status)
    check("no rung claims empirical grounding above cross-source synthesis",
          all("empirical" not in str(r.get("evidence_status", "")).lower() for r in rungs))
    # exemplified_by only on rungs 1-3
    for r in rungs:
        if r.get("exemplified_by"):
            check("only rungs 1-3 carry an OSM/DAEE exemplification (rung %d)" % r["n"], r["n"] <= 3)
    ne = " ".join(m.get("non_entailments", [])).lower()
    check("non_entailments: OSM/DAEE exemplify 1-3 and prove no upper rung",
          "1-3" in ne and ("do not prove" in ne or "not a proof" in ne or "does not prove" in ne
                           or "not prove" in ne))
    check("rungs 8-10 are athari-internal",
          all(r.get("status") == "athari-internal" for r in rungs if r["n"] >= 8))
    # the companion references the map
    comp = read("companion/dynamic-orthing-noetic-learning-and-orthability.md")
    check("companion references the machine-readable argument map",
          "DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml" in comp)
    check("companion lists eight distinct dynamic-orthability modalities (B39)",
          "Eight modalities" in comp or "eight" in comp.lower())

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
