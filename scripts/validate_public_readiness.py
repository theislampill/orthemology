#!/usr/bin/env python3
"""Public experiment-readiness conformance validator (R7D, Decision 0029, audit B3/B4).

Deterministic, offline. Derives the allowed public readiness statements from the
canonical packet index (experiments/experiment-status.yaml) and fails when a public
surface (README, STATUS, CONTRIBUTING) contradicts it:

  1. when the packet readiness_states are not all identical, NO surface may carry a
     scalar "every designed study / all packets are READY TO RUN" claim (audit B3);
  2. the exact current packet states must be recoverable from the packet index and
     the public prose must not name a superseded packet (FCSP-1/ER-1) as the ready
     one when its successor (FCSP-2/ER-2) is the READY_TO_RUN packet;
  3. no current surface describes the deterministic checks as "check/checks/showing
     consistency" — the project uses bounded conformance language (audit B4).

Establishes no empirical claim; a public-honesty gate only.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
SURFACES = ["README.md", "STATUS.md", "CONTRIBUTING.md"]

# scalar over-claim patterns banned when packet states differ
SCALAR = [
    re.compile(r"every designed study is ready to run", re.I),
    re.compile(r"all (packets|studies)[^.]*ready to run", re.I),
    re.compile(r"the terminology packets are ready to run", re.I),
]
# bounded-conformance discipline (audit B4)
CONSISTENCY = re.compile(r"check(s|ing)? consistency|consistency only|show(s|ing)? consistency", re.I)


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    idx = yaml.safe_load(read("experiments/experiment-status.yaml"))
    packets = idx["packets"]
    states = {p["packet_id"]: p["readiness_state"] for p in packets}
    distinct = set(states.values())
    check("packet index has more than one distinct readiness state (scalar 'all "
          "ready' is therefore false)", len(distinct) > 1, str(sorted(distinct)))

    # 1. no scalar over-claim on any surface
    for rel in SURFACES:
        text = read(rel)
        for pat in SCALAR:
            m = pat.search(text)
            check("%s carries no scalar 'all packets READY TO RUN' claim" % rel,
                  m is None, "matched %r" % (m.group(0) if m else ""))

    # 2. exact current packet states present in the index (poka-yoke on the source)
    for pid, want in [("FCSP-2", "READY_TO_RUN"), ("ER-2", "READY_TO_RUN"),
                      ("FCSP-1", "DETERMINISTICALLY_VALIDATED"),
                      ("ER-1", "DETERMINISTICALLY_VALIDATED"),
                      ("TERM-P0-V2", "READY_FOR_HUMAN_MATCHING_REVIEW"),
                      ("TERM-P1-TEMPLATE", "DRAFT"),
                      ("TERM-CONFIRMATORY-TEMPLATE", "DRAFT")]:
        check("packet %s state is %s in the index" % (pid, want), states.get(pid) == want,
              repr(states.get(pid)))

    # 2b. public prose must not name a superseded packet as the ready one
    for rel in SURFACES:
        text = read(rel)
        if re.search(r"FCSP-1[^.\n]*READY_TO_RUN|ER-1[^.\n]*READY_TO_RUN", text):
            check("%s does not call a superseded packet (FCSP-1/ER-1) READY_TO_RUN" % rel, False)
        else:
            check("%s does not call a superseded packet (FCSP-1/ER-1) READY_TO_RUN" % rel, True)

    # 3. bounded-conformance language (no "check consistency")
    for rel in SURFACES:
        text = read(rel)
        m = CONSISTENCY.search(text)
        check("%s uses bounded conformance language (no 'check consistency')" % rel,
              m is None, "matched %r" % (m.group(0) if m else ""))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
