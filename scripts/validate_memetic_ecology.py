#!/usr/bin/env python3
"""Represented-standard + governed memetic-ecology validator
(R7C Decision 0028; R7D Decisions 0031 & 0032; audit B13-B23, probes P4/P5/P6/P8).

Deterministic, offline. R7C gave the ecology a vocabulary; R7D gives it graph
semantics, relation-level fidelity/stance, and a defensible source-dependence model:

  D (Decision 0031): every represented metaortheme TYPE resolves to a metaortheme-type
     node (no ghost type); no self-lineage; fidelity/stance are RELATION-level
     (REP-META-ASSESSMENT, one row per (standard,type)); carrier stance is a typed
     CARRIER-RELATION (quotation != endorsement).
  E (Decision 0032): unique node/edge ids; typed endpoints per edge_type; a
     transmission names the transmitted standard; a mutation declares an ablation
     witness; social stabilization never constitutes warrant (machine firewall).
  F (Decision 0032): the MACHINE independence conclusion is source-safe and NEVER
     concludes tawatur warrant — two independent routes yield
     `source-independence-supported`, not `tawatur-like-independence`; creed-internal
     tawatur WARRANT is a separate, school-labeled assessment.

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

# typed endpoints per edge relation: edge_type -> (allowed source types, allowed target types)
ENDPOINT_RULES = {
    "endorsement": ({"institution", "actor", "artifact", "interpretive-community"}, {"represented-standard"}),
    "transmission": ({"institution", "actor", "artifact"}, {"institution", "actor", "artifact"}),
    "application": ({"represented-standard"}, {"episode"}),
    "copying-dependence": ({"artifact"}, {"artifact"}),
    "mutation": ({"artifact", "represented-standard"}, {"artifact", "represented-standard"}),
}
STANCES = {"expresses", "quotes", "endorses", "embodies", "applies", "opposes", "distorts", "transmits"}
PROHIBITED_WARRANT_KEYS = {
    "witness_count", "minimum_count", "popularity", "graph_degree",
    "institutional_persistence", "numeric_threshold",
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def independence_conclusion(common_source, copying, independent_routes):
    """MACHINE-safe (audit B21/B23): never concludes tawatur WARRANT. Dependence
    forbids an independence claim; >=2 independent routes support SOURCE independence
    only; unknown origin is underdetermined. Tawatur warrant is a separate,
    creed-internal, school-labeled judgement — not derivable here."""
    if common_source or copying:
        return "dependence-detected"
    if independent_routes >= 2:
        return "source-independence-supported"
    return "origin-analysis-underdetermined"


def _schema_issues(document, schema):
    """Return bounded structural diagnostics instead of raising on malformed input."""
    try:
        validator = jsonschema.Draft7Validator(schema)
        return ["schema:%s" % e.message for e in sorted(validator.iter_errors(document), key=lambda e: list(e.path))]
    except (TypeError, ValueError, jsonschema.SchemaError) as exc:
        return ["schema:%s" % str(exc)]


def validate_tawatur_document(document, source_status_ids=None, schema=None):
    """Validate the closed warrant contract and its cross-field invariants."""
    if schema is None:
        try:
            schema = json.loads(read(APP + "/TAWATUR-WARRANT.schema.json"))
        except (OSError, ValueError) as exc:
            return ["schema-load:%s" % exc]
    issues = _schema_issues(document, schema)
    if not isinstance(document, dict):
        return issues or ["document-not-object"]
    assessments = document.get("assessments")
    if not isinstance(assessments, list):
        return issues or ["assessments-not-array"]
    for assessment in assessments:
        if not isinstance(assessment, dict):
            continue
        if PROHIBITED_WARRANT_KEYS.intersection(assessment):
            issues.append("numeric-or-prevalence-warrant-field")
        refs = assessment.get("source_status_refs", [])
        if source_status_ids is not None and isinstance(refs, list):
            if any(ref not in source_status_ids for ref in refs):
                issues.append("unresolved-source-status-ref")
        units = assessment.get("source_units")
        if isinstance(units, list):
            unit_ids = [u.get("unit_id") for u in units if isinstance(u, dict)]
            if len(unit_ids) != len(set(unit_ids)):
                issues.append("duplicate-source-unit")
            unit_set = set(unit_ids)
        else:
            unit_set = set()
        origin = assessment.get("origin_analysis")
        if isinstance(origin, dict):
            if (origin.get("common_cause_status") == "detected"
                    and origin.get("path_independence") == "supported"):
                issues.append("common-cause-conflicts-with-independence")
            if (origin.get("copying_status") == "detected"
                    and origin.get("path_independence") == "supported"):
                issues.append("copying-conflicts-with-independence")
        qualities = assessment.get("transmitter_quality")
        if isinstance(qualities, list):
            quality_ids = [q.get("source_unit_id") for q in qualities if isinstance(q, dict)]
            if unit_set and set(quality_ids) != unit_set:
                issues.append("transmitter-quality-coverage-mismatch")
        routes = assessment.get("acquisition_routes")
        if isinstance(routes, list):
            route_ids = [r.get("route_id") for r in routes if isinstance(r, dict)]
            route_set = set(route_ids)
            if len(route_ids) != len(route_set):
                issues.append("duplicate-acquisition-route")
            for route in routes:
                if isinstance(route, dict) and any(
                        unit not in unit_set for unit in route.get("source_unit_ids", [])):
                    issues.append("acquisition-route-unresolved-source-unit")
        else:
            route_set = set()
        subjects = assessment.get("subject_assessments")
        if isinstance(subjects, list):
            subject_ids = [s.get("subject_id") for s in subjects if isinstance(s, dict)]
            if len(subject_ids) != len(set(subject_ids)):
                issues.append("duplicate-subject-assessment")
            for subject in subjects:
                if isinstance(subject, dict) and any(
                        route not in route_set for route in subject.get("route_refs", [])):
                    issues.append("subject-route-unresolved")
    return list(dict.fromkeys(issues))


def main():
    rs_schema = json.loads(read(APP + "/REPRESENTED-STANDARD.schema.json"))
    rs = json.loads(read(APP + "/REPRESENTED-STANDARD.example.json"))
    eco_schema = json.loads(read(APP + "/MEMETIC-ECOLOGY.schema.json"))
    eco = json.loads(read(APP + "/MEMETIC-ECOLOGY.example.json"))
    rma_schema = json.loads(read(APP + "/REP-META-ASSESSMENT.schema.json"))
    rma = json.loads(read(APP + "/REP-META-ASSESSMENT.example.json"))
    car_schema = json.loads(read(APP + "/CARRIER-RELATION.schema.json"))
    car = json.loads(read(APP + "/CARRIER-RELATION.example.json"))

    # node registries (E: uniqueness by list, not set)
    node_ids_list = [n["id"] for n in eco["nodes"]]
    node_ids = set(node_ids_list)
    ntype = {n["id"]: n["node_type"] for n in eco["nodes"]}
    metatype_ids = {n["id"] for n in eco["nodes"] if n["node_type"] == "metaortheme-type"}
    repstd_ids = {n["id"] for n in eco["nodes"] if n["node_type"] == "represented-standard"}

    # ---- D: represented standard ----
    try:
        jsonschema.validate(rs, rs_schema)
        check("represented-standard example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("represented-standard example validates against schema", False, e.message)
    check("RepMeta is many-to-many (>=1 metaortheme type; example uses 2)",
          len(rs.get("represented_metaortheme_types", [])) >= 2)
    # D1: every represented type resolves to a metaortheme-type node (no ghost type)
    ghosts = [t for t in rs.get("represented_metaortheme_types", []) if t not in metatype_ids]
    check("every represented metaortheme type resolves to a metaortheme-type node (no ghost, B13)",
          not ghosts, "ghosts=%s" % ghosts)
    # D1: no self-lineage
    check("represented standard is not in its own lineage (no self-lineage, B14)",
          rs["id"] not in rs.get("lineage", []))
    check("represented standard carries an explicit carrier stance", rs.get("stance") in STANCES)
    ncl = " ".join(rs.get("non_claims", [])).lower()
    check("represented standard denies being type/metaorthemma/execution/soul",
          "not the normative metaortheme type" in ncl and "metaorthemma" in ncl and "soul" in ncl)

    # ---- D2: relation-level fidelity/stance ----
    try:
        jsonschema.validate(rma, rma_schema)
        check("rep-meta-assessment example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("rep-meta-assessment example validates against schema", False, e.message)
    assessed = {}
    for a in rma["assessments"]:
        check("assessment std %s resolves to a represented-standard node" % a["represented_standard_id"],
              a["represented_standard_id"] in repstd_ids)
        check("assessment type %s resolves to a metaortheme-type node" % a["metaortheme_type_id"],
              a["metaortheme_type_id"] in metatype_ids)
        assessed.setdefault(a["represented_standard_id"], {})[a["metaortheme_type_id"]] = a["fidelity"]
    # coverage: each represented standard's types each have an assessment row
    for t in rs.get("represented_metaortheme_types", []):
        check("represented standard %s has a per-type assessment for %s (B15)" % (rs["id"], t),
              t in assessed.get(rs["id"], {}))
    # B15: when per-type fidelities differ, the global rollup is 'partial'
    fids = set(assessed.get(rs["id"], {}).values())
    if len(fids) > 1:
        check("mixed per-type fidelity rolls up to global 'partial' (not one uniform field, B15)",
              rs.get("fidelity_status") == "partial", repr(rs.get("fidelity_status")))

    # ---- D3: carrier relation ----
    try:
        jsonschema.validate(car, car_schema)
        check("carrier-relation example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("carrier-relation example validates against schema", False, e.message)
    for r in car["relations"]:
        check("carrier relation %s->%s resolves both endpoints" % (r["carrier_id"], r["represented_standard_id"]),
              r["carrier_id"] in node_ids and r["represented_standard_id"] in repstd_ids)
    check("carrier relations distinguish modes (quotation is present and distinct from endorsement, B16)",
          {r["mode"] for r in car["relations"]} >= {"quotes"} and
          "endorses" in {r["mode"] for r in car["relations"]})

    # ---- E: ecology graph semantics ----
    try:
        jsonschema.validate(eco, eco_schema)
        check("memetic-ecology example validates against schema", True)
    except jsonschema.ValidationError as e:
        check("memetic-ecology example validates against schema", False, e.message)
    # E1: unique node ids + unique edge ids
    check("node ids are unique (no duplicate nodes, B17/P5)",
          len(node_ids_list) == len(node_ids),
          "dups=%s" % [x for x in node_ids_list if node_ids_list.count(x) > 1])
    edge_ids_list = [e["id"] for e in eco["edges"]]
    check("edge ids are unique", len(edge_ids_list) == len(set(edge_ids_list)))
    for e in eco["edges"]:
        et = e["edge_type"]
        # endpoints resolve
        ok_ep = e["source"] in node_ids and e["target"] in node_ids
        check("edge %s endpoints resolve to nodes" % e["id"], ok_ep, "%s -> %s" % (e["source"], e["target"]))
        # E1: typed endpoints per relation (B17/P8 illegal endpoint)
        if et in ENDPOINT_RULES and ok_ep:
            src_ok = ntype[e["source"]] in ENDPOINT_RULES[et][0]
            tgt_ok = ntype[e["target"]] in ENDPOINT_RULES[et][1]
            check("edge %s (%s) has type-valid endpoints" % (e["id"], et), src_ok and tgt_ok,
                  "%s(%s) -> %s(%s)" % (e["source"], ntype[e["source"]], e["target"], ntype[e["target"]]))
        # E2: transmission names the transmitted standard, resolving to a node (B18/P8)
        if et == "transmission":
            ts = e.get("transmitted_standard")
            check("transmission edge %s names a resolvable transmitted standard (B18)" % e["id"],
                  bool(ts) and ts in repstd_ids, repr(ts))
        # E3: mutation declares a structured ablation witness (B19)
        if et == "mutation":
            mi = e.get("mutation_identity")
            ok_mi = isinstance(mi, dict) and all(k in mi for k in
                    ("classification", "compared_versions", "preserved_invariants", "changed_fields", "witness", "evidence", "assessor"))
            check("mutation edge %s declares a structured ablation witness (B19)" % e["id"], ok_mi,
                  "keys=%s" % (sorted(mi) if isinstance(mi, dict) else type(mi).__name__))
    # E4: truth firewall — no edge/node asserts warrant from propagation/degree (B20)
    firewall_ok = not any(e.get("establishes_warrant") or e.get("warranted_by_degree") for e in eco["edges"]) \
        and not any(n.get("warranted") for n in eco["nodes"])
    check("no edge/node asserts warrant from propagation/degree (machine firewall, B20)", firewall_ok)
    check("ecology declares no-warrant-from-degree and no-interior non-claims",
          any("warrant" in nc.lower() for nc in eco.get("non_claims", []))
          and any("interior" in nc.lower() or "soul" in nc.lower() for nc in eco.get("non_claims", [])))

    # ---- F: independence conclusion (machine-safe) + tawatur warrant separation ----
    for a in eco["tawatur_analyses"]:
        oa = a["origin_analysis"]
        expected = independence_conclusion(oa["common_source"], oa["copying_dependence"], oa["independent_routes"])
        check("ecology analysis %s independence conclusion is machine-rule-consistent" % a["claim_id"],
              a["warrant_conclusion"] == expected
              or (a["warrant_conclusion"].startswith("false-tawatur") and expected == "dependence-detected"),
              "declared %s vs rule %s" % (a["warrant_conclusion"], expected))
        check("ecology analysis %s denies count-as-warrant" % a["claim_id"],
              any("count" in nc.lower() or "degree" in nc.lower() or "popularity" in nc.lower()
                  for nc in a.get("non_claims", [])))

    fx_doc = yaml.safe_load(read(APP + "/FALSE-TAWATUR-FIXTURES.yaml"))
    check("false-tawatur fixtures point to the current warrant contract",
          fx_doc.get("warrant_contract") == "orthemology-tawatur-warrant-v2")
    check("false-tawatur fixtures enumerate the Task 7 warrant regression surface",
          len(fx_doc.get("warrant_regression_surface", [])) == 7)
    fx = fx_doc["fixtures"]
    for f in fx:
        # B22: impossible origin counts rejected (independent routes cannot exceed witnesses)
        check("fixture %s: independent_routes <= apparent_witnesses (B22)" % f["id"],
              f["independent_routes"] <= f["apparent_witnesses"],
              "%d > %d" % (f["independent_routes"], f["apparent_witnesses"]))
        got = independence_conclusion(f["common_source"], f["copying_dependence"], f["independent_routes"])
        check("fixture %s (%s) -> %s" % (f["id"], f["distinction"][:28], f["expected"]),
              got == f["expected"], "rule gave %s" % got)
    # the machine rule NEVER returns tawatur-like-independence (that is warrant, not machine)
    for f in fx:
        got = independence_conclusion(f["common_source"], f["copying_dependence"], f["independent_routes"])
        check("fixture %s machine conclusion is not a tawatur WARRANT claim (B23)" % f["id"],
              got != "tawatur-like-independence")

    # Creed-internal tawatur warrant is a separate, closed, school-labeled record.
    tw = yaml.safe_load(read(APP + "/TAWATUR-WARRANT.example.yaml"))
    source_registry = yaml.safe_load(read("references/source-status.yaml"))
    source_ids = {row["id"] for row in source_registry.get("claims", [])}
    tw_issues = validate_tawatur_document(tw, source_ids)
    check("tawatur-warrant example validates structurally and semantically", not tw_issues,
          "; ".join(tw_issues[:8]))
    for w in tw.get("assessments", []):
        check("tawatur-warrant %s is school-labeled" % w.get("id", "?"),
              bool(str(w.get("school", "")).strip()))
        check("tawatur-warrant %s keeps objective truth outside subject assessments" % w.get("id", "?"),
              all("objective_truth_status" not in s for s in w.get("subject_assessments", [])))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
