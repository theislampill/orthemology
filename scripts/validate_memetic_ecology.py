#!/usr/bin/env python3
"""Represented-standard + memetic-ecology validator (R7C, Decision 0028).

Deterministic, offline. Turns the R7B vocabulary sketch into a governed model:

  1. REPRESENTED-STANDARD.example.json validates against its schema; it is
     many-to-many on metaortheme types (RepMeta), carries an explicit carrier
     stance from the 8-mode enum, a fidelity_status, provenance, validity, and
     lineage, and denies being the type / metaorthemma / execution / soul (B11);
  2. MEMETIC-ECOLOGY.example.json validates against its schema; every node and
     edge is identified/versioned/provenanced/status'd; every edge's source and
     target resolve to nodes; every mutation edge declares a mutation_identity
     (ablation-based, not wording similarity) (B12);
  3. false tawatur: every tawatur analysis, and fixtures TW1..TW6, follow the
     rule — any common_source OR copying_dependence forbids
     `tawatur-like-independence`; a warrant conclusion never rests on count or
     graph degree (B13).

Establishes no epistemic warrant from number/popularity; no interior/soul claim.
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


def tawatur_conclusion(common_source, copying, independent_routes):
    """The warrant rule: count never suffices; any dependence forbids independence.
    The false-tawatur SUBTYPE (copying vs common-source) is informational; the
    load-bearing point is that dependence => not tawatur-like-independence."""
    if common_source or copying:
        return "false-tawatur-copying" if copying else "false-tawatur-common-source"
    if independent_routes >= 2:
        return "tawatur-like-independence"
    return "underdetermined-needs-more-origin-analysis"


def main():
    rs_schema = json.loads(read(APP + "/REPRESENTED-STANDARD.schema.json"))
    rs = json.loads(read(APP + "/REPRESENTED-STANDARD.example.json"))
    eco_schema = json.loads(read(APP + "/MEMETIC-ECOLOGY.schema.json"))
    eco = json.loads(read(APP + "/MEMETIC-ECOLOGY.example.json"))

    # 1. represented standard
    try:
        jsonschema.validate(rs, rs_schema)
        check("represented-standard example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("represented-standard example validates against schema", False, e.message)
    check("RepMeta is many-to-many (>=1 metaortheme type; example uses 2)",
          len(rs.get("represented_metaortheme_types", [])) >= 2)
    check("represented standard carries an explicit carrier stance",
          rs.get("stance") in {"expresses", "quotes", "endorses", "embodies", "applies", "opposes", "distorts", "transmits"})
    check("represented standard has a fidelity_status", bool(rs.get("fidelity_status")))
    ncl = " ".join(rs.get("non_claims", [])).lower()
    check("represented standard denies being type/metaorthemma/execution/soul",
          "not the normative metaortheme type" in ncl and "metaorthemma" in ncl and "soul" in ncl)

    # 2. ecology graph
    try:
        jsonschema.validate(eco, eco_schema)
        check("memetic-ecology example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("memetic-ecology example validates against schema", False, e.message)
    node_ids = {n["id"] for n in eco["nodes"]}
    for e in eco["edges"]:
        check("edge %s endpoints resolve to nodes" % e["id"],
              e["source"] in node_ids and e["target"] in node_ids,
              "%s -> %s" % (e["source"], e["target"]))
        if e["edge_type"] == "mutation":
            check("mutation edge %s declares a mutation_identity" % e["id"],
                  "mutation_identity" in e)
    check("ecology declares no-warrant-from-degree and no-interior non-claims",
          any("warrant" in nc.lower() for nc in eco.get("non_claims", []))
          and any("interior" in nc.lower() or "soul" in nc.lower() for nc in eco.get("non_claims", [])))

    # 3. false tawatur — example analyses obey the rule
    for a in eco["tawatur_analyses"]:
        oa = a["origin_analysis"]
        expected = tawatur_conclusion(oa["common_source"], oa["copying_dependence"], oa["independent_routes"])
        check("tawatur analysis %s conclusion is warrant-rule-consistent" % a["claim_id"],
              a["warrant_conclusion"] == expected or
              (a["warrant_conclusion"].startswith("false-tawatur") and expected.startswith("false-tawatur")),
              "declared %s vs rule %s" % (a["warrant_conclusion"], expected))
        check("tawatur analysis %s denies count-as-warrant" % a["claim_id"],
              any("count" in nc.lower() or "degree" in nc.lower() or "popularity" in nc.lower()
                  for nc in a.get("non_claims", [])))

    # fixtures
    fx = yaml.safe_load(read(APP + "/FALSE-TAWATUR-FIXTURES.yaml"))["fixtures"]
    for f in fx:
        got = tawatur_conclusion(f["common_source"], f["copying_dependence"], f["independent_routes"])
        expected = f["expected"]
        ok = got == expected or (got.startswith("false-tawatur") and expected.startswith("false-tawatur"))
        check("fixture %s (%s) -> %s" % (f["id"], f["distinction"][:30], expected), ok,
              "rule gave %s" % got)
    # the rule NEVER returns tawatur-like when dependence exists
    for f in fx:
        if f["common_source"] or f["copying_dependence"]:
            check("fixture %s with dependence is not tawatur-like" % f["id"],
                  f["expected"] != "tawatur-like-independence")

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
