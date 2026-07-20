#!/usr/bin/env python3
"""Experiment-packet readiness validator (Decision 0018, R6).

Deterministic, offline. Enforces the canonical index
experiments/experiment-status.yaml: closed vocabularies, per-packet file
contracts, freeze-hash agreement, transition prerequisites, honest
registration language, and the no-run guard. Establishes packet state and
internal agreement — never an empirical result.
"""
import hashlib
import io
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

FCSP_REQUIRED = ["README.md", "STATUS.yaml", "PROTOCOL.md", "DESIGN.yaml", "ENDPOINTS.yaml",
                 "DECISION-RULES.yaml", "RUN-MANIFEST.schema.json", "OUTPUT.schema.json",
                 "DEVIATION-LEDGER.md", "FREEZE-HASH.txt", "items/ITEMS.json",
                 "baselines/BASELINE-ARM.md", "treatments/TREATMENT-ARM.md",
                 "analysis/analyze_fcsp.py", "simulation/power_sim.py",
                 "scripts" + "/" + "generate_items.py", "tests" + "/" + "test_smoke.py"]
ER_REQUIRED = ["README.md", "STATUS.yaml", "PROTOCOL.md", "E1-E5-SPEC.yaml",
               "BASELINE-TREATMENT-CONTRACT.md", "RUN-MANIFEST.schema.json",
               "OUTPUT.schema.json", "SCORING-RUBRIC.md", "DECISION-RULES.yaml",
               "DEVIATION-LEDGER.md", "FREEZE-HASH.txt",
               "analysis/analyze_er.py", "scripts" + "/" + "generate_fixtures.py", "tests" + "/" + "test_smoke.py"]

PREREG_ALLOW = ("not externally", "none is externally", "externally registered",
                "external registry", "owner/external act", "externally preregistered before", "registry record",
                "EXTERNALLY_PREREGISTERED", "is not, by itself, a public preregistration",
                "preregistration")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def packet_freeze(pkt_dir):
    h = hashlib.sha256()
    for base, dirs, fns in sorted(os.walk(pkt_dir)):
        dirs.sort()
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in sorted(fns):
            if fn == "FREEZE-HASH.txt":
                continue
            rel = os.path.relpath(os.path.join(base, fn), pkt_dir).replace("\\", "/")
            h.update(rel.encode() + b"\x00")
            h.update(io.open(os.path.join(base, fn), "rb").read() + b"\x00")
    return h.hexdigest()


def main():
    idx = yaml.safe_load(read("experiments/experiment-status.yaml"))
    rvoc = set(idx["readiness_vocabulary"])
    gvoc = set(idx["registration_vocabulary"])
    packets = {p["packet_id"]: p for p in idx["packets"]}

    for pid, p in sorted(packets.items()):
        check("%s readiness in closed vocabulary" % pid,
              p["readiness_state"] in rvoc, p["readiness_state"])
        check("%s registration in closed vocabulary" % pid,
              p["registration_state"] in gvoc, p["registration_state"])
        check("%s path exists" % pid, os.path.isdir(os.path.join(ROOT, p["path"])))
        check("%s records run_exists" % pid, p.get("run_exists") is False,
              "no run may exist in this repository")
        if p["registration_state"] == "EXTERNALLY_PREREGISTERED":
            check("%s EXTERNALLY_PREREGISTERED names a registry record" % pid,
                  bool(p.get("external_registry_record")))
        gates = " ".join(p.get("required_remaining_gates", [])).lower()
        if "matching review" in gates:
            check("%s with a pending matching review is not READY_TO_RUN or beyond" % pid,
                  p["readiness_state"] in ("DRAFT", "SPEC_COMPLETE",
                                           "DETERMINISTICALLY_VALIDATED",
                                           "READY_FOR_HUMAN_MATCHING_REVIEW"),
                  p["readiness_state"])

    # per-packet file contracts + freeze + STATUS agreement for the two new packets
    for pid, required in (("FCSP-1", FCSP_REQUIRED), ("ER-1", ER_REQUIRED)):
        p = packets.get(pid)
        check("%s present in the index" % pid, p is not None)
        if not p:
            continue
        pdir = os.path.join(ROOT, p["path"])
        missing = [f for f in required if not os.path.exists(os.path.join(pdir, f))]
        check("%s carries its full required file set" % pid, not missing, str(missing))
        recorded = ""
        for ln in read(p["path"] + "FREEZE-HASH.txt").splitlines():
            ln = ln.strip()
            if len(ln) == 64 and all(c in "0123456789abcdef" for c in ln):
                recorded = ln
        computed = packet_freeze(pdir)
        check("%s freeze hash recomputes" % pid, recorded == computed,
              "recorded=%s computed=%s" % (recorded[:12], computed[:12]))
        check("%s index freeze hash matches the packet file" % pid,
              p.get("freeze_hash") == recorded)
        st = yaml.safe_load(read(p["path"] + "STATUS.yaml"))
        check("%s STATUS.yaml agrees with the index (readiness+registration)" % pid,
              st["readiness_state"] == p["readiness_state"]
              and st["registration_state"] == p["registration_state"])
        check("%s deviation ledger has no entries before a run" % pid,
              "No entries" in read(p["path"] + "DEVIATION-LEDGER.md"))

    # terminology packet gates
    check("TERM-P0-V2 is READY_FOR_HUMAN_MATCHING_REVIEW (review honestly pending)",
          packets.get("TERM-P0-V2", {}).get("readiness_state")
          == "READY_FOR_HUMAN_MATCHING_REVIEW")
    spec = read("terminology/pilot0-v2/EXECUTION-SPEC.md")
    for outcome in ("ADVANCE_TO_PILOT1", "REVISE_AND_RETEST_INSTRUMENT",
                    "DO_NOT_ADVANCE_THIS_ITEM_VERSION", "INCONCLUSIVE"):
        check("pilot0-v2 spec carries feasibility outcome %s" % outcome, outcome in spec)
    offenders = [ln.strip()[:90] for ln in spec.splitlines()
                 if "adopt-candidate" in ln and "supersede" not in ln]
    check("pilot0-v2 never offers adopt-candidate as a live outcome", not offenders,
          str(offenders))
    check("no Pilot-0 adoption/retirement decision anywhere in the spec",
          "No adoption or retirement conclusion of any kind is available from Pilot 0" in spec)

    # honest preregistration language across current experiment/manuscript surfaces
    offenders = []
    for rel in ("manuscript/orthemma-ortheme-systems-revised-draft.md",
                "STATUS.md", "README.md", "OPEN-DECISIONS.md",
                "experiments/README.md", "experiments/experiment-status.yaml",
                "terminology/pilot0-v2/EXECUTION-SPEC.md"):
        for i, ln in enumerate(read(rel).splitlines(), 1):
            if re.search(r"\bpre-?registered\b", ln, re.I):
                if not any(a.lower() in ln.lower() for a in PREREG_ALLOW):
                    offenders.append("%s:%d %s" % (rel, i, ln.strip()[:80]))
    check("no unqualified 'preregistered' claim on a current surface",
          not offenders, "; ".join(offenders[:3]))

    # no-run guard: no non-synthetic output record, no run-output file shape
    offenders = []
    for tree in ("experiments", "terminology"):
        for base, dirs, fns in os.walk(os.path.join(ROOT, tree)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in fns:
                rel = os.path.relpath(os.path.join(base, fn), ROOT).replace("\\", "/")
                if fn in ("runs.jsonl", "report.json") or fn.endswith(".runs.jsonl"):
                    offenders.append(rel + " (run-output file shape)")
                    continue
                if fn.endswith((".json", ".jsonl")):
                    if '"synthetic_smoke": false' in read(rel):
                        offenders.append(rel + " (non-synthetic record)")
    check("no-run guard: no empirical run output exists in the repository",
          not offenders, str(offenders[:4]))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
