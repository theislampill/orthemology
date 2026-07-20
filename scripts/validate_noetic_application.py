#!/usr/bin/env python3
"""Noetic-application fixtures + example validator (Decision 0021 §7).

Deterministic, offline. Asserts that the ten adversarial fixtures preserve the
required Orthemology distinctions and the NO-SOUL-ACCESS invariant, and that
the example episode keeps occurrence/observation/inferred-profile/interior
distinct and makes only creed-internal, non-empirical, non-soul-state claims.
Establishes internal discipline of this project's application — never an
empirical or theological truth.
"""
import io
import json
import os
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
WANT = {"N%d" % i for i in range(1, 11)}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def main():
    doc = yaml.safe_load(read("tests/noetic-application-fixtures.yaml"))
    fx = {f["id"]: f for f in doc["fixtures"]}
    check("all ten fixtures N1..N10 present", set(fx) == WANT, str(sorted(set(fx) ^ WANT)))
    check("the no-soul-access invariant is declared", "no_soul_access_invariant" in doc)

    for fid, f in sorted(fx.items()):
        for key in ("observation", "candidate_profiles", "inferred_profile",
                    "correct_action", "forbidden_placements", "distinction_tested"):
            check("%s has %s" % (fid, key), key in f)
        forb = " ".join(f.get("forbidden_placements", [])).lower()
        check("%s forbids asserting motive/culpability/soul-state" % fid,
              "motive" in forb or "soul" in forb or "culpability" in forb, forb[:60])
        # the correct action never rests on an interior/motive assertion
        ca = f["correct_action"].lower()
        check("%s correct action is not a moralized interior verdict" % fid,
              "motive" not in ca and "soul" not in ca and "culpable" not in ca)

    # specific distinctions the audit demanded
    check("N1 holds under underdetermination (no moralized placement)",
          fx["N1"]["inferred_profile"] == "underdetermined"
          and "hold" in fx["N1"]["correct_action"].lower())
    check("N3 separates sound metaortheme from defective metaorthemma",
          "binding" in fx["N3"]["inferred_profile"] and "stays sound" in fx["N3"]["correct_action"])
    check("N5 applies evaluator symmetry without proving non-circularity",
          "symmetry" in fx["N5"]["correct_action"].lower())
    check("N6 distinguishes independence from count",
          "independence" in fx["N6"]["correct_action"].lower()
          or "dependence" in fx["N6"]["correct_action"].lower())
    check("N7 separates diagnosis from route",
          "route" in fx["N7"]["distinction_tested"].lower())
    check("N8 blocks closure by whole-state reread",
          "reread" in fx["N8"]["correct_action"].lower())
    check("N9 claims runtime closure only",
          "runtime closure only" in fx["N9"]["correct_action"].lower())
    check("N10 negative control refuses to invent a deformation",
          fx["N10"]["inferred_profile"] == "no-deformation")

    ex = json.loads(read("examples/noetic-analysis-episode.json"))
    check("example keeps occurrence/observation/inferred/interior distinct",
          "occurrence" in ex and "observation" in ex and "inferred_profile" in ex
          and "not_available" in ex["observation"])
    check("example inferred profile is NOT ground truth / NOT soul access",
          "NOT ground truth" in ex["inferred_profile"]["is_not"]
          and "NOT soul access" in ex["inferred_profile"]["is_not"])
    check("example declares an explicitly creed-internal analysis",
          "creed-internal" in ex["declared_noetic_analysis"]["school_boundary"])
    ncl = " ".join(ex["explicit_non_claims"]).lower()
    for tok in ("motive", "culpability", "soul-state", "restored", "empirical"):
        check("example non-claims include %r" % tok, tok in ncl)
    check("example runtime closure is not restoration",
          ex["post_render_reread"]["closure_legitimate"] is False)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
