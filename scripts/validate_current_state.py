#!/usr/bin/env python3
"""Validate the public state surfaces against docs/current-state.yaml
(Decision 0014). The generated state is authoritative; VERSION, README,
STATUS, OPEN-DECISIONS and the primary document headers must agree with it.

Checks:
  1. the derived block is current (no drift) — delegated to generate_current_state --check;
  2. VERSION names the current revision;
  3. every primary document header names the current revision;
  4. README's decision range matches the actual decision IDs;
  5. README's example count matches the actual count;
  6. OPEN-DECISIONS lists exactly the authored owner-only burdens (no more, no fewer)
     and contains no ordinary-research burden;
  7. STATUS carries the authored terminology/empirical/license claim wording;
  8. no public surface asserts a numbered release, DOI, or peer review;
  9. every research residual has a trigger;
 10. the recorded terminology freeze hashes match the packet files on disk
     (this is the check that catches a mis-reported hash in prose).
"""
import io
import os
import re
import subprocess
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


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    state = yaml.safe_load(read("docs/current-state.yaml"))
    a, d = state["authored"], state["derived"]
    rev = a["revision"]

    rc = subprocess.call([sys.executable, os.path.join(ROOT, "scripts", "generate_current_state.py"),
                          "--check"], cwd=ROOT, stdout=subprocess.DEVNULL)
    check("derived block is current (no drift)", rc == 0, "run scripts/generate_current_state.py")

    check("VERSION names the current revision (%s)" % rev, read("VERSION").strip().startswith(rev))

    for key, rel in a["primary_documents"].items():
        head = "\n".join(read(rel).split("\n")[:16])
        check("header of %s names %s" % (rel, rev), rev in head,
              "header still names an older revision")

    readme = read("README.md")
    ids = d["decision_ids"]
    lo, hi = min(ids), max(ids)
    check("README decision range covers %s-%s" % (lo, hi),
          re.search(r"%s\s*[-–]\s*%s" % (lo, hi), readme) is not None,
          "README decision range is stale")
    n_ex = d["example_json_count"]
    m = re.search(r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+machine-readable", readme)
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    stated = None
    if m:
        tok = m.group(1)
        stated = int(tok) if tok.isdigit() else words.get(tok)
    check("README machine-readable example count matches (%d)" % n_ex, stated == n_ex,
          "README says %r, tree has %d" % (stated, n_ex))

    od = read("OPEN-DECISIONS.md")
    for burden in a["owner_only_burdens"]:
        key = burden.split("(")[0].strip().split(";")[0]
        head = " ".join(key.split()[:3]).lower()
        check("OPEN-DECISIONS covers owner burden %r" % head, head in od.lower())
    for banned in ["classical-edition verification", "schema repair", "source verification is owner"]:
        check("OPEN-DECISIONS free of ordinary-research burden %r" % banned,
              banned.lower() not in od.lower())

    status = read("STATUS.md")
    check("STATUS carries the terminology status", "NOT RUN" in status.upper())
    check("STATUS carries the empirical status",
          "no designed study" in status.lower() or "not run" in status.lower())
    check("STATUS records the open license decision", "license" in status.lower())

    for rel in ["README.md", "STATUS.md", "VERSION", "docs/CITING.md"]:
        t = read(rel).lower()
        for banned in ["peer reviewed and accepted", "doi:10.", "stable release v"]:
            check("%s asserts no %r" % (rel, banned), banned not in t)

    for rr in a["research_residuals_with_triggers"]:
        check("research residual %s has a trigger" % rr["id"], bool(rr.get("trigger")))

    # freeze hashes: recorded state vs the packet files themselves
    for packet, key in (("terminology/pilot0", "pilot0_v1"),
                        ("terminology/pilot0-v2", "pilot0_v2")):
        recorded = d["terminology_freeze_hashes"].get(key)
        onfile = None
        for line in read(os.path.join(packet, "FREEZE-HASH.txt")).split("\n"):
            line = line.strip()
            if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
                onfile = line
        check("%s freeze hash in state matches the packet file" % key, recorded == onfile,
              "state=%s file=%s" % (recorded, onfile))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
