#!/usr/bin/env python3
"""Meta-noetic memetics + sound-corrective-dynamics validator (R7B, Decision 0025).

Deterministic, offline. Enforces the memetics extension's discipline:

  DYNAMIC-CROSSWALK.yaml
    - the four distinct bearers are present (mu / mu-tilde / mu-bar / execution)
      and declared distinct;
    - carrier roles (>=6), the three distinct histories, the ecology nodes/edges,
      and the memetic modes (>=7, incl. false-tawatur and restoration) are present;
    - every bearer and the top level carry non-claims (no motive/soul assertion).

  NOETIC-FIELD-DYNAMICS.yaml
    - the adopted descent model is G1 (order-theoretic/route-ranked), G2 is
      conditional/future with its requirements listed, and daee's own bound
      ("not literal physical gradient") is cited [direct];
    - the burden functional is anti-gaming: raw count is not a potential and the
      lexicographic order leads with truthful disclosure;
    - the five/six state spaces stay separate (incl. the social-metaorthemic
      field and actual-uptake), non-monotonicity includes no-guaranteed-
      convergence, and fitrah is bounded (creed-internal; not a coordinate).

Both files pin the reviewed daee commit. Establishes no empirical or theological
claim; asserts no soul access.
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

# SEMANTIC guard (R7C, audit B19-3): the four bearers stay DISTINCT. A bearer
# gloss must not equate it to another bearer. This catches the tamper probe
# "mu-tilde gloss = the same object as a case-bound metaorthemma".
CONFLATE = re.compile(r"\b(same\s+(object\s+)?as|identical\s+to|equal\s+to|is\s+the\s+same\s+(object\s+)?as)\b", re.I)
OTHER_BEARERS = ["metaorthemma", "mu-bar", "mu-tilde", "execution", "metaortheme type"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
PIN = "c86b3c6673147b8802fe222373a165a37d4d24a8"
FAILS = []
FITRAH_PROPERTIES = {"qualitative", "defeasible", "multidimensional"}
FITRAH_POSITIVE = {"normative-disposition", "proper-function-orientation"}
FITRAH_PROHIBITED = {
    "measurable-scalar", "field-coordinate", "metaortheme", "algorithm",
    "discourse-readable-soul-state", "guaranteed-attractor",
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def load(rel):
    return yaml.safe_load(io.open(os.path.join(ROOT, rel), encoding="utf-8").read())


def validate_fitrah_boundary(boundary):
    """Validate the school-internal fiṭrah model without reading subject interiors."""
    if not isinstance(boundary, dict):
        return ["fitrah-boundary-not-object"]
    issues = []
    if boundary.get("status") != "creed-internal":
        issues.append("fitrah-not-creed-internal")
    properties = boundary.get("model_properties")
    property_set = {item for item in properties if isinstance(item, str)} if isinstance(properties, list) else set()
    if not isinstance(properties, list) or not FITRAH_PROPERTIES.issubset(property_set):
        issues.append("fitrah-properties-incomplete")
    if isinstance(properties, list) and any(not isinstance(item, str) for item in properties):
        issues.append("fitrah-properties-malformed")
    if isinstance(properties, list) and property_set - FITRAH_PROPERTIES:
        issues.append("fitrah-properties-forbidden")
    positive = boundary.get("is")
    positive_set = {item for item in positive if isinstance(item, str)} if isinstance(positive, list) else set()
    if not isinstance(positive, list) or not FITRAH_POSITIVE.issubset(positive_set):
        issues.append("fitrah-positive-model-incomplete")
    if isinstance(positive, list) and any(not isinstance(item, str) for item in positive):
        issues.append("fitrah-positive-model-malformed")
    if isinstance(positive, list) and positive_set - FITRAH_POSITIVE:
        issues.append("fitrah-positive-model-forbidden")
    prohibited = boundary.get("is_not")
    prohibited_set = {item for item in prohibited if isinstance(item, str)} if isinstance(prohibited, list) else set()
    if not isinstance(prohibited, list) or not FITRAH_PROHIBITED.issubset(prohibited_set):
        issues.append("fitrah-prohibitions-incomplete")
    if isinstance(prohibited, list) and any(not isinstance(item, str) for item in prohibited):
        issues.append("fitrah-prohibitions-malformed")
    if positive_set & prohibited_set:
        issues.append("fitrah-positive-negative-conflict")
    corruption = boundary.get("corruption_assessment")
    if not isinstance(corruption, dict):
        issues.append("fitrah-corruption-boundary-missing")
    else:
        if corruption.get("dissent_alone_sufficient") is not False:
            issues.append("dissent-alone-circular")
        if corruption.get("requires_independent_evidence") is not True:
            issues.append("corruption-without-independent-evidence")
        if corruption.get("interior_status") != "held-or-underdetermined":
            issues.append("interior-status-overclaimed")
    return issues


def main():
    cw = load(APP + "/DYNAMIC-CROSSWALK.yaml")
    fd = load(APP + "/NOETIC-FIELD-DYNAMICS.yaml")

    # --- DYNAMIC-CROSSWALK ---
    check("crosswalk pins the daee commit", cw.get("daee_pinned_commit") == PIN)
    bearer_names = " ".join(b.get("name", "") for b in cw.get("bearers", []))
    for tok in ("mu", "mu-tilde", "mu-bar", "execution"):
        check("bearer present: %s" % tok, tok in bearer_names)
    check("bearers declared distinct (!=)", "!=" in str(cw.get("distinctness", "")))
    for b in cw.get("bearers", []):
        nm = b.get("name", "?")
        check("bearer %s has non_claims" % nm[:16], bool(b.get("non_claims")))
        # SEMANTIC: a bearer gloss must not equate it to another bearer (B19-3)
        gloss = str(b.get("gloss", ""))
        m = CONFLATE.search(gloss)
        conflated = m and any(o in gloss.lower() for o in OTHER_BEARERS)
        check("bearer %s gloss does not equate it to another bearer" % nm[:16],
              not conflated, "found %r in gloss" % (m.group(0) if m else ""))
    # the represented-standard bearer must stay distinct from the metaorthemma
    mut = next((b for b in cw.get("bearers", []) if "mu-tilde" in b.get("name", "")), {})
    mtext = (str(mut.get("gloss", "")) + " " + " ".join(mut.get("non_claims", []))).lower()
    check("mu-tilde is not equated with a metaorthemma/mu-bar",
          not (("same" in mtext or "identical" in mtext) and ("metaorthemma" in mtext or "mu-bar" in mtext)))
    roles = cw.get("carrier_roles", {}).get("roles", [])
    check("carrier roles >= 6 (one artifact, several roles)", len(roles) >= 6, "%d" % len(roles))
    hist = cw.get("three_histories", {}).get("histories", [])
    check("exactly three distinct histories", len(hist) == 3, str(hist))
    eco = cw.get("ecology", {})
    check("ecology nodes include represented-standards",
          any("represented" in n for n in eco.get("nodes", [])))
    for edge in ("transmission", "mutation", "reinforcement", "replacement"):
        check("ecology edge present: %s" % edge, edge in eco.get("edges", []))
    modes = cw.get("memetic_modes", {}).get("modes", [])
    check("memetic modes >= 7", len(modes) >= 7, "%d" % len(modes))
    mode_names = " ".join(m.get("name", "").lower() for m in modes)
    check("memetic modes include false tawatur", "tawatur" in mode_names)
    check("memetic modes include restoration of a misrepresented standard",
          "restoration" in mode_names)
    top_nc = " ".join(cw.get("non_claims", [])).lower()
    check("crosswalk non-claims forbid motive/soul assertion",
          "motive" in top_nc and "soul" in top_nc)

    # --- NOETIC-FIELD-DYNAMICS ---
    check("field-dynamics pins the daee commit", fd.get("daee_pinned_commit") == PIN)
    ga = fd.get("gradient_adjudication", {})
    # R7D (Decision 0033, B26): G1 is a CANDIDATE, not adopted, inside an unmerged PR
    check("descent model G1 is proposed-candidate (not adopted; R7D B26)",
          ga.get("proposed_candidate") == "G1" and ga.get("G1", {}).get("status") == "proposed-candidate")
    g1_reading = str(ga.get("G1", {}).get("reading", "")).lower()
    check("G1 uses admissible/pathway-adequate vocabulary, not 'strictly sound' (B27)",
          "AdmissibleCorrectiveTransition" in ga.get("predicate_vocabulary", [])
          and "strict soundness is reserved" in str(ga.get("strict_soundness_reserved", "")).lower()
          and "admissible" in g1_reading and "never 'strictly sound'" in g1_reading)
    check("G2 is conditional/future", ga.get("G2", {}).get("status") == "conditional-future")
    check("G2 lists its requirements", len(ga.get("G2", {}).get("requirements", [])) >= 6)
    dob = ga.get("daee_own_bound", {})
    check("daee's own bound is cited as [direct]", dob.get("status") == "direct"
          and "not literal" in str(dob.get("statement", "")).lower())
    check("preferred phrasing is descent-like, not literal gradient",
          "descent-like" in str(ga.get("preferred_phrasing", "")).lower())
    bf = fd.get("burden_functional", {})
    check("raw burden count is NOT a potential", bf.get("raw_count_is_not_a_potential") is True)
    # R7C (B14/B15): feasibility-first constrained order, two timescales
    cd = fd.get("corrective_dynamics", {})
    ff = cd.get("feasibility_first", {})
    check("hard constraints are feasibility-first (filtered before ranking)",
          bool(ff.get("predicate")) and ("before" in str(ff.get("rule", "")).lower()
                                          and "inadmissible" in str(ff.get("rule", "")).lower()))
    check("ordering is a partial/declared order, NOT one universal total lexicographic",
          cd.get("ordering", {}).get("universal_total_lexicographic") is False)
    check("mandatory invariants lead with truthful disclosure",
          "truthful-disclosure" in cd.get("mandatory_invariants", []))
    tt = cd.get("two_timescales", {})
    check("two timescales (fast episode vs slow meta) are separated",
          bool(tt.get("fast_episode")) and bool(tt.get("slow_meta")) and bool(tt.get("coupling")))
    check("no runtime improvement entails result truth or restoration",
          "restoration" in str(cd.get("no_result_or_restoration_entailment", "")).lower())
    check("non-monotonicity includes no-guaranteed-convergence",
          "no-guaranteed-convergence" in fd.get("non_monotonicity", []))
    spaces = fd.get("state_spaces", {}).get("spaces", [])
    check("state spaces >= 6 (separate)", len(spaces) >= 6, "%d" % len(spaces))
    joined = " ".join(spaces)
    check("state spaces include the social-metaorthemic field", "metaorthemic" in joined)
    check("state spaces include actual-uptake", "uptake" in joined)
    fb = fd.get("fitrah_boundary", {})
    fb_issues = validate_fitrah_boundary(fb)
    check("fitrah boundary is qualitative, defeasible, multidimensional, and anti-reifying",
          not fb_issues, "; ".join(fb_issues))
    fd_nc = " ".join(fd.get("non_claims", [])).lower()
    check("field-dynamics non-claims forbid motive/soul assertion",
          "soul" in fd_nc and ("motive" in fd_nc or "interior" in fd_nc))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
