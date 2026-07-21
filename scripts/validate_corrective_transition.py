#!/usr/bin/env python3
"""Governed corrective-transition validator (R7D, Decision 0033, audit B28/B29).

Deterministic, offline. R7C summarized route pressure, selection, binding, execution,
delta, diagnostics, and reread under "descent". This gate keeps the stages separate
and enforces the load-bearing non-conflations (phase-H6 probes):

  * a route is selected only from the hard-constraint-ADMISSIBLE set (feasibility
    filtered first) and only with a ranking witness (no differential gradient);
  * `delta` is a runtime control-state change — NEVER result correctness, and an
    admissible transition is NEVER `strictly_sound` (that is a factive claim-relative
    predicate, Decision 0011);
  * a CLOSURE posture requires a performed whole-state reread;
  * runtime closure is never asserted as human restoration;
  * no burden is deleted/concealed to simulate progress;
  * one episode never silently revises the global standard (slow-timescale revision
    needs explicit authorization).

Establishes no empirical or theological claim; asserts no soul access.
"""
import io
import json
import os
import sys

try:
    import yaml
    import jsonschema
except ImportError as e:
    print("FATAL: requires pyyaml + jsonschema:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def transition_ok(t):
    """Return (ok, rule_violated) under the H6 discipline."""
    if t.get("selected_route") not in (t.get("eligible_routes") or []):
        return False, "route-not-admissible"
    if not str(t.get("ranking_witness", "")).strip():
        return False, "no-ranking-witness"
    if t.get("verdicts", {}).get("strictly_sound") is True:
        return False, "delta-as-soundness"
    reread = t.get("reread", {})
    if t.get("terminal_posture") == "CLOSURE" and not reread.get("performed"):
        return False, "reread-omitted"
    ncl = " ".join(t.get("non_claims", [])).lower()
    if t.get("verdicts", {}).get("runtime_closure") and "restoration" not in ncl:
        return False, "closure-as-restoration"
    delta = str(t.get("delta", "")).lower()
    if ("delet" in delta or "conceal" in delta) and t.get("terminal_posture") in ("CLOSURE", "STOP"):
        return False, "burden-deletion"
    if ("global" in delta and ("revis" in delta or "chang" in delta)) and "authoriz" not in delta:
        return False, "unauthorized-global-revision"
    return True, None


def main():
    schema = json.loads(read(APP + "/CORRECTIVE-TRANSITION.schema.json"))
    ex = json.loads(read(APP + "/CORRECTIVE-TRANSITION.example.json"))
    try:
        jsonschema.validate(ex, schema)
        check("corrective-transition example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("corrective-transition example validates against schema", False, e.message)

    # every example transition is a valid governed corrective transition
    for t in ex["transitions"]:
        ok, rule = transition_ok(t)
        check("example transition %s is a valid governed corrective transition" % t["transition_id"],
              ok, "violates %s" % rule)
        # explicit non-conflation assertions present
        v = t["verdicts"]
        check("example transition %s keeps delta != soundness (strictly_sound not-claimed)" % t["transition_id"],
              v["strictly_sound"] in ("not-claimed", False))

    # fixtures
    fx = yaml.safe_load(read(APP + "/CORRECTIVE-TRANSITION-FIXTURES.yaml"))["fixtures"]
    ids = {f["id"] for f in fx}
    check("all eight corrective-transition fixtures present", ids == {"CT%d" % i for i in range(1, 9)}, str(sorted(ids)))
    for f in fx:
        ok, rule = transition_ok(f["transition"])
        exp = f["expected_valid"]
        check("fixture %s (%s) validity == %s" % (f["id"], f["distinction"][:32], exp),
              ok == exp, "got valid=%s (rule %s)" % (ok, rule))
        if not exp and "violates" in f:
            check("fixture %s violates declared rule %s" % (f["id"], f["violates"]),
                  rule == f["violates"], "got %s" % rule)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
