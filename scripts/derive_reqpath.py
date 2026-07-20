#!/usr/bin/env python3
"""ReqPath derivation with trace (R3).

Derives ReqPath(e) = CorePath ∩ RequiredBy(...) from the machine-readable
governance rule table (docs/governance-requirements.yaml), emitting a
per-verdict derivation trace (required / not-required, with the governing rule
and rationale). `--check` recomputes every fixture in tests/reqpath-fixtures.json
and verifies: (a) derived sets match expectations in CorePath conceptual order;
(b) the omission attack (a declared path missing a derivable requirement) is
detected as a mismatch, never silently tolerated.

Honest status (also stated in the YAML): the shipped table is *one* complete,
deterministic governance instance; RequiredBy in general remains a
governance-supplied parameterized interface, not a universal closed calculus.
"""
import argparse
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


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def load():
    gov = yaml.safe_load(open(os.path.join(ROOT, "docs", "governance-requirements.yaml"), encoding="utf-8"))
    reg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    return gov, reg


def derive(shape, gov, reg):
    core = list(reg["core_path"])  # conceptual order from the registry
    rules = gov["rules"]
    req, trace = [], []
    for v in core:
        rule = rules.get(v)
        if rule is None:
            trace.append((v, "NOT-REQUIRED", "no governance rule names this core verdict"))
            continue
        cond = rule["when"]
        required = (cond == "always") or bool(shape.get(cond, False))
        trace.append((v, "REQUIRED" if required else "NOT-REQUIRED",
                      "when=%s; %s" % (cond, rule["rationale"])))
        if required:
            req.append(v)
    return req, trace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--shape", help="JSON file with an episode shape; prints the trace")
    args = ap.parse_args()
    gov, reg = load()

    if args.shape:
        shape = json.load(open(args.shape, encoding="utf-8"))
        req, trace = derive(shape, gov, reg)
        for v, status, why in trace:
            print("%-20s %-13s %s" % (v, status, why))
        print("ReqPath:", req)
        return

    # rule sanity: every rule names a registry core verdict; every core verdict has a rule
    core = set(reg["core_path"])
    rules = set(gov["rules"])
    check("every governance rule targets a CorePath verdict", rules <= core, str(sorted(rules - core)))
    check("every CorePath verdict has exactly one rule", core <= rules, str(sorted(core - rules)))

    fx = json.load(open(os.path.join(ROOT, "tests", "reqpath-fixtures.json"), encoding="utf-8"))
    for f in fx["fixtures"]:
        req, trace = derive(f["shape"], gov, reg)
        if "expected_reqpath" in f:
            check("%s derived ReqPath matches expectation" % f["id"], req == f["expected_reqpath"],
                  "derived=%s" % req)
        if f.get("expected_mismatch"):
            declared = f["declared_reqpath_missing_token_verdict"]
            check("%s omission attack detected (declared != derived)" % f["id"],
                  declared != req, "omission tolerated")
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
