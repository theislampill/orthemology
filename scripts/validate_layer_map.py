#!/usr/bin/env python3
"""Layer-map validator (R7B, Phase H). Deterministic, offline.

Asserts the six-layer map is complete and firewall-consistent: every layer has a
claim type and evidence status drawn from the closed vocabularies and non-claims;
the empirical layer carries no result; the theological layer is creed-internal
and school-labeled; and the firewall note is present. Establishes no empirical or
theological claim."""
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


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    m = yaml.safe_load(io.open(os.path.join(ROOT, "docs/architecture/ORTHEMOLOGY-LAYER-MAP.yaml"),
                               encoding="utf-8").read())
    ctypes = set(m["claim_types"])
    estatuses = set(m["evidence_statuses"])
    layers = {l["id"]: l for l in m["layers"]}
    check("six layers L1..L6 present", set(layers) == {"L%d" % i for i in range(1, 7)},
          str(sorted(layers)))
    for lid, l in sorted(layers.items()):
        for field in ("name", "depends_on", "objects", "claim_type", "evidence_status", "non_claims", "document"):
            check("%s has %s" % (lid, field), field in l)
        check("%s claim_type in vocabulary" % lid, l.get("claim_type") in ctypes, l.get("claim_type"))
        check("%s evidence_status in vocabulary" % lid, l.get("evidence_status") in estatuses, l.get("evidence_status"))
        check("%s has non_claims" % lid, bool(l.get("non_claims")))

    # firewall specifics
    l6 = layers.get("L6", {})
    check("empirical layer L6 has no result", l6.get("evidence_status") == "not-run-no-empirical-result")
    check("L6 non-claims say no study run",
          any("no study" in nc.lower() or "no result" in nc.lower() for nc in l6.get("non_claims", [])))
    l5 = layers.get("L5", {})
    check("theological layer L5 is creed-internal", l5.get("evidence_status") == "creed-internal")
    check("L5 is school-labeled Athari",
          any("athari" in nc.lower() for nc in l5.get("non_claims", [])))
    l3 = layers.get("L3", {})
    check("noetic layer L3 asserts no soul access",
          any("soul access" in nc.lower() for nc in l3.get("non_claims", [])))
    l2 = layers.get("L2", {})
    check("dynamic layer L2 says OSM not validation",
          any("not validation" in nc.lower() for nc in l2.get("non_claims", [])))
    check("firewall note present and says warrant does not flow upward",
          "not flow upward" in str(m.get("firewall_note", "")).lower())

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
