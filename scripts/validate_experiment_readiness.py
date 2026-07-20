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

# current v2 packet file contracts (R7): harness + hidden-key split + complete analysis
FCSP2_REQUIRED = ["README.md", "STATUS.yaml", "PROTOCOL.md", "DESIGN.yaml", "ENDPOINTS.yaml",
                  "DECISION-RULES.yaml", "RUN-MANIFEST.schema.json", "OUTPUT.schema.json",
                  "DEVIATION-LEDGER.md", "FREEZE-HASH.txt", "items/PUBLIC-ITEMS.json",
                  "items/KEYS.json", "baselines/BASELINE-ARM.md", "treatments/TREATMENT-ARM.md",
                  "harness/run_fcsp.py", "analysis/analyze_fcsp2.py",
                  "simulation/design_sensitivity.py", "scripts/generate_items.py",
                  "tests/test_smoke.py"]
ER2_REQUIRED = ["README.md", "STATUS.yaml", "PROTOCOL.md", "E1-E5-SPEC.yaml",
                "BASELINE-TREATMENT-CONTRACT.md", "RUN-MANIFEST.schema.json",
                "OUTPUT.schema.json", "SCORING-RUBRIC.md", "DECISION-RULES.yaml",
                "DEVIATION-LEDGER.md", "FREEZE-HASH.txt", "fixtures/KEYS.json",
                "harness/run_er.py", "analysis/analyze_er2.py",
                "scripts/generate_cases.py", "tests/test_smoke.py"]

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
    # collect files first, then filter — sorted(os.walk(...)) exhausts the
    # generator before any dirs[:] pruning could take effect, so a stray
    # __pycache__/.pyc must be excluded by PATH, not by live pruning.
    rows = []
    for base, _dirs, fns in os.walk(pkt_dir):
        if "__pycache__" in base.replace("\\", "/").split("/"):
            continue
        for fn in fns:
            if fn == "FREEZE-HASH.txt" or fn.endswith((".pyc", ".pyo")):
                continue
            rel = os.path.relpath(os.path.join(base, fn), pkt_dir).replace("\\", "/")
            rows.append((rel, os.path.join(base, fn)))
    h = hashlib.sha256()
    for rel, full in sorted(rows):
        h.update(rel.encode() + b"\x00")
        h.update(io.open(full, "rb").read() + b"\x00")
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

    # per-packet file contracts + freeze + STATUS agreement.
    # Current v2 packets: full contract + index<->STATUS agreement.
    # Historical R6 packets (Decision 0020): freeze preserved + recomputes, a
    # correction note is present, and they are NOT current (READY_TO_RUN is
    # only allowed on a CURRENT packet); their byte-frozen in-packet STATUS is
    # historical and is therefore NOT required to agree with the index.
    def freeze_checks(pid, p):
        pdir = os.path.join(ROOT, p["path"])
        recorded = ""
        for ln in read(p["path"] + "FREEZE-HASH.txt").splitlines():
            ln = ln.strip()
            if len(ln) == 64 and all(c in "0123456789abcdef" for c in ln):
                recorded = ln
        check("%s freeze hash recomputes" % pid, recorded == packet_freeze(pdir),
              "recorded=%s computed=%s" % (recorded[:12], packet_freeze(pdir)[:12]))
        check("%s index freeze hash matches the packet file" % pid,
              p.get("freeze_hash") == recorded)

    for pid, required in (("FCSP-2", FCSP2_REQUIRED), ("ER-2", ER2_REQUIRED)):
        p = packets.get(pid)
        check("%s present in the index" % pid, p is not None)
        if not p:
            continue
        pdir = os.path.join(ROOT, p["path"])
        missing = [f for f in required if not os.path.exists(os.path.join(pdir, f))]
        check("%s carries its full required file set" % pid, not missing, str(missing))
        freeze_checks(pid, p)
        st = yaml.safe_load(read(p["path"] + "STATUS.yaml"))
        check("%s STATUS.yaml agrees with the index (readiness+registration)" % pid,
              st["readiness_state"] == p["readiness_state"]
              and st["registration_state"] == p["registration_state"])
        check("%s deviation ledger has no entries before a run" % pid,
              "No entries" in read(p["path"] + "DEVIATION-LEDGER.md"))

    for pid in ("FCSP-1", "ER-1"):
        p = packets.get(pid)
        check("%s present in the index" % pid, p is not None)
        if not p:
            continue
        check("%s is marked historical (Decision 0020)" % pid, p.get("historical") is True)
        check("%s carries a superseded_by pointer" % pid, bool(p.get("superseded_by")))
        check("%s carries a correction note" % pid, bool(p.get("correction_note")))
        check("%s (historical) is not classified READY_TO_RUN" % pid,
              p["readiness_state"] != "READY_TO_RUN", p["readiness_state"])
        freeze_checks(pid, p)  # byte-frozen preservation still verified

    # only CURRENT (non-historical) packets may hold READY_TO_RUN
    bad_ready = [pid for pid, p in packets.items()
                 if p.get("readiness_state") == "READY_TO_RUN" and p.get("historical")]
    check("no historical packet holds READY_TO_RUN", not bad_ready, str(bad_ready))

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
