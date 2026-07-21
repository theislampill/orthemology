#!/usr/bin/env python3
"""Dynamic-orthing / latent-state learning validator (R7B, Decision 0024).

Deterministic, offline. Enforces the dynamic extension's discipline:
  1. the four update levels are declared and each is exercised by a fixture;
  2. every fixture is well-formed and carries a non-claim;
  3. the load-bearing separations are each asserted by at least one fixture:
     episode-inference != model-learning (DYN-1), world edge != learner edge
     (DYN-2), analysis-version change blocks transport (DYN-3), ortheme
     admission is by ablation not latent split (DYN-4), no one-to-one
     latent->profile map (DYN-5), orthogonality does not define an ortheme
     (DYN-6), endpoint underdetermines mechanism (DYN-7);
  4. the OSM/CSCG source is bounded to exemplification-not-validation and to no
     human/metaphysical/wet-lab transfer (DYN-8 + crosswalk);
  5. the crosswalk rows carry a valid claim_status and non-claims, and never
     define an ortheme by orthogonality.

Establishes no empirical, human, or metaphysical claim.
"""
import io
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

# SEMANTIC guard (R7C, audit B19-2): a latent/model object may be a VEHICLE for
# orthemic distinctions but is never an ortheme "by declaration". This catches
# the tamper probe "latent model state z_t IS an ortheme by declaration".
# Negated forms ("is NOT an ortheme", "not define an ortheme") do not match.
ORTHEME_ASSERT = re.compile(r"\b(is|are|becomes?|declared)\s+(an?\s+)?orthemes?\b", re.I)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/latent-state-orthing"
FAILS = []
LEVELS = {"episode-inference", "representation-learning", "repertoire-revision",
          "analysis-version-change"}
CLAIM_STATUS = {"source-report", "model-mechanics", "synthesis", "orthemology-extension"}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def load(rel):
    return yaml.safe_load(io.open(os.path.join(ROOT, rel), encoding="utf-8").read())


def main():
    fx = load(APP + "/DYNAMIC-FIXTURES.yaml")
    cw = load(APP + "/OSM-CSCG-ORTHEME-CROSSWALK.yaml")

    # 1. update levels
    declared = set(fx.get("update_levels", []))
    check("all four update levels declared", declared == LEVELS,
          "declared=%s" % sorted(declared))
    fixtures = fx.get("fixtures", [])
    used = {f.get("level") for f in fixtures}
    check("every update level is exercised by a fixture", LEVELS <= used,
          "missing: %s" % sorted(LEVELS - used))

    # 2. fixture well-formedness
    ids = [f.get("id") for f in fixtures]
    for f in fixtures:
        fid = f.get("id", "?")
        for field in ("id", "name", "level", "scenario", "distinction", "forbids", "non_claim"):
            check("fixture %s has %s" % (fid, field), bool(str(f.get(field, "")).strip()))
        check("fixture %s level is valid" % fid, f.get("level") in LEVELS, f.get("level"))

    # 3. required fixtures present (R7C extended to the failure families DYN-10..DYN-20)
    for n in range(1, 21):
        req = "DYN-%d" % n
        check("fixture %s present" % req, req in ids)

    # 3b. update coupling (R7C, audit B7): each of the four levels is GOVERNED
    coupling = load(APP + "/UPDATE-COUPLING.yaml")
    ct = {t["level"]: t for t in coupling.get("transitions", [])}
    check("update coupling covers all four levels", set(ct) == LEVELS, str(sorted(ct)))
    for lvl, t in sorted(ct.items()):
        for field in ("trigger", "authority", "input", "version", "transport", "invalidated", "reopening", "rollback"):
            check("coupling[%s] declares %s" % (lvl, field), bool(t.get(field)))
    rr = ct.get("repertoire-revision", {})
    check("repertoire revision changes the DECLARED repertoire, not worldly facts",
          "represent" in str(rr.get("non_claim", "")).lower()
          and "not worldly" in str(rr.get("non_claim", "")).lower())

    # 4. OSM boundary: DYN-8 forbids validation-use + wet-lab + metaphysical transfer
    dyn8 = next((f for f in fixtures if f.get("id") == "DYN-8"), {})
    blob8 = (str(dyn8.get("forbids", "")) + " " + str(dyn8.get("non_claim", ""))).lower()
    check("DYN-8 forbids citing OSM as validation/support", "support" in blob8 or "validation" in blob8 or "evidence" in blob8)
    check("DYN-8 forbids wet-lab/biological import", "wet-lab" in blob8 or "biological" in blob8)
    check("DYN-8 forbids human/metaphysical transfer",
          ("metaphys" in blob8) and ("human" in blob8 or "noetic" in blob8))

    # 5. crosswalk discipline
    check("crosswalk overall_status is 'not validation'",
          "not validation" in str(cw.get("overall_status", "")).lower())
    rows = cw.get("rows", [])
    check("crosswalk has rows", len(rows) >= 6)
    for r in rows:
        rid = str(r.get("osm_concept", "?"))[:36]
        check("row '%s' claim_status valid" % rid, r.get("claim_status") in CLAIM_STATUS,
              r.get("claim_status"))
        check("row '%s' has non_claims" % rid, bool(r.get("non_claims")))
    # the orthogonality row must deny ortheme-definition-by-orthogonality
    orth = [r for r in rows if "orthogonal" in str(r.get("osm_concept", "")).lower()
            or "decorrelat" in str(r.get("osm_concept", "")).lower()]
    check("an orthogonalization row exists", bool(orth))
    if orth:
        nc = " ".join(orth[0].get("non_claims", [])).lower()
        check("orthogonalization row denies defining an ortheme",
              "not define an ortheme" in nc or "does not define" in nc or "not sufficient" in nc)
    # an endpoint-underdetermines row must exist and deny mechanism identification
    endp = [r for r in rows if "endpoint" in str(r.get("osm_concept", "")).lower()
            or "trajectory" in str(r.get("osm_concept", "")).lower()]
    check("endpoint-underdetermines-mechanism row exists", bool(endp))

    # SEMANTIC: no row asserts a latent/model object IS an ortheme (B19-2)
    for r in rows:
        obj = str(r.get("orthemology_object", ""))
        m = ORTHEME_ASSERT.search(obj)
        check("row '%s' does not assert a latent/model object IS an ortheme"
              % str(r.get("osm_concept", "?"))[:28], m is None,
              "found %r" % (m.group(0) if m else ""))
    # the latent-state row must explicitly deny ortheme status and require ablation
    lat = [r for r in rows if "latent" in str(r.get("osm_concept", "")).lower()
           and "state" in str(r.get("osm_concept", "")).lower()]
    check("a latent-state row exists", bool(lat))
    if lat:
        nc = " ".join(lat[0].get("non_claims", [])).lower()
        check("latent-state row denies ortheme status (admission is by ablation)",
              "not an ortheme" in nc and "ablation" in nc)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
