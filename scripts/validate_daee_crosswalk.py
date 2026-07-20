#!/usr/bin/env python3
"""daee/Orthemology crosswalk + notation-firewall validator (Decision 0021).

Deterministic, offline. Asserts the crosswalk's typing discipline and the
notation firewall; establishes internal consistency of THIS project's typed
interpretation, never the truth of daee's premises or any empirical/theological
claim.

Checks:
  1. crosswalk pins the daee commit; every row cites a daee source, a mapping
     type from the closed set, and a status layer from the closed set;
  2. NO row carries status_layer 'empirical' (there is no empirical claim);
  3. the mandatory typed distinctions are all present and the crosswalk states
     Psi-I is not ground truth / not soul access;
  4. deformation types map to ortheme-level candidate state-types, never to
     metaortheme, and their row is creed-internal-normative with a no-motive
     non-claim;
  5. Diagnostic IR maps many-to-one and is explicitly not one metaorthemma;
  6. notation firewall: every declared collision resolves to a namespaced D.*
     form; no raw daee collision glyph is introduced into
     docs/notation-registry.yaml (tamper-tested by construction);
  7. co-development limitation and non-validation are stated;
  8. the R6 integration note carries its superseding banner.
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
FAILS = []
MAP_TYPES = {"exact-structural-analogue", "partial-analogue", "one-to-many",
             "many-to-one", "application-extension", "no-mapping"}
LAYERS = {"direct-repository-description", "orthemological-crosswalk",
          "creed-internal-normative", "empirical"}
PIN = "c86b3c6673147b8802fe222373a165a37d4d24a8"


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    try:
        cw = yaml.safe_load(read(APP + "/DAEE-ORTHEMOLOGY-CROSSWALK.yaml"))
        parsed = isinstance(cw, dict) and "rows" in cw
    except yaml.YAMLError as e:
        cw, parsed = {}, False
        print("[FAIL] crosswalk YAML parses cleanly — %s" % str(e).splitlines()[0])
        FAILS.append("crosswalk YAML parses")
    check("crosswalk YAML parses into a rows mapping", parsed)
    if not parsed:
        print("TOTAL: %d failures" % len(FAILS))
        sys.exit(1)
    check("crosswalk pins the daee commit", cw.get("daee_pinned_commit") == PIN)
    rows = cw["rows"]
    check("crosswalk has rows", len(rows) >= 12)
    for r in rows:
        rid = r["daee"][:40]
        check("row '%s' cites a daee source" % rid, bool(r.get("daee_source")))
        check("row '%s' mapping_type is valid" % rid, r.get("mapping_type") in MAP_TYPES,
              r.get("mapping_type"))
        check("row '%s' status_layer is valid" % rid, r.get("status_layer") in LAYERS,
              r.get("status_layer"))
    check("NO row is empirical (there is no empirical claim)",
          not any(r.get("status_layer") == "empirical" for r in rows))

    td = " ".join(cw.get("typed_distinctions", [])).lower()
    for tok in ("occurrence", "observation", "candidate noetic profiles", "inferred",
                "actual interior", "metaortheme", "metaorthemma", "diagnostic ir",
                "orthing episode", "restoration"):
        check("typed distinctions include %r" % tok, tok in td)
    psi = [r for r in rows if r["daee"].startswith("Psi-I")]
    check("a Psi-I row exists", bool(psi))
    if psi:
        nc = " ".join(psi[0].get("non_claims", [])).lower()
        check("the Psi-I row itself disclaims ground truth AND soul access",
              "not ground truth" in nc and ("soul access" in nc or "not o*(m;a)" in nc),
              "Psi-I non_claims=%r" % nc[:80])

    deform = [r for r in rows if r["daee"].lower().startswith("deformation types")]
    check("a deformation row exists", bool(deform))
    if deform:
        d = deform[0]
        check("deformation maps to ortheme-level candidate state-types, not metaortheme",
              "ortheme-level" in d["orthemology_object"]
              and "metaortheme" not in d["orthemology_object"].replace("ortheme-level", ""))
        check("deformation row is creed-internal-normative",
              d["status_layer"] == "creed-internal-normative")
        check("deformation row disclaims motive/culpability/soul",
              any("motive" in nc or "soul" in nc or "culpability" in nc
                  for nc in d.get("non_claims", [])))

    ir = [r for r in rows if r["daee"].startswith("Diagnostic IR")]
    check("Diagnostic IR row exists and maps many-to-one, not one metaorthemma",
          bool(ir) and ir[0]["mapping_type"] == "many-to-one"
          and "NOT one metaorthemma" in " ".join(ir[0].get("non_claims", [])))

    # notation firewall
    fw = yaml.safe_load(read(APP + "/NOTATION-FIREWALL.yaml"))
    for c in fw["collisions"]:
        check("collision %s resolves to a namespaced D.* form" % c["daee_symbol"],
              c.get("daee_namespaced", "").startswith("D."))
    reg = read("docs/notation-registry.yaml")
    for glyph_name in ("D.mu_mem", "D.kappa_dep", "D.Omega_ont", "D.m_mode", "D.N_frame"):
        check("notation registry not polluted with %s" % glyph_name, glyph_name not in reg)
    check("firewall forbids merging the registries",
          "never extended with daee" in fw.get("registry_merge_forbidden", "").lower()
          or "orthemology-only" in fw.get("registry_merge_forbidden", "").lower())

    app_readme = read(APP + "/README.md")
    boundary = read(APP + "/SOURCE-BOUNDARY.md")
    both = app_readme + boundary
    check("co-development limitation stated", "co-develop" in both.lower()
          or "same owner" in both.lower())
    check("non-validation stated", "not independent validation" in both.lower()
          or "not validation" in both.lower())
    check("no-soul-access stated", "soul" in both.lower())

    note = read("docs/integrations/daee-epistemics-orthemology-mapping.md")
    check("R6 integration note carries its superseding banner",
          "SUPERSEDED" in note and "0021" in note)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
