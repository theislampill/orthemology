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

    ver_first = (read("VERSION").split("\n") or [""])[0].strip()
    check("VERSION first line is exactly the authored revision label",
          ver_first.rstrip(".") == a["revision_label"],
          "VERSION=%r authored=%r" % (ver_first, a["revision_label"]))

    for key, rel in a["primary_documents"].items():
        head = "\n".join(read(rel).split("\n")[:16])
        check("header of %s names %s" % (rel, rev), rev in head,
              "header still names an older revision")

    def marker(text, name):
        m = re.search(r"<!--\s*state:%s\s*-->(.*?)<!--\s*/state:%s\s*-->" % (name, name),
                      text, re.S)
        return m.group(1).strip() if m else None

    readme = read("README.md")
    ids = [str(i).zfill(4) for i in d["decision_ids"]]
    lo, hi = min(ids), max(ids)
    got_range = marker(readme, "decision-range")
    check("README decision-range marker is exactly %s–%s" % (lo, hi),
          got_range == "%s–%s" % (lo, hi),
          "marker content is %r" % got_range)
    n_ex = d["example_json_count"]
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    got_ex = marker(readme, "example-json-count")
    stated = int(got_ex) if (got_ex or "").isdigit() else words.get(got_ex)
    check("README example-json-count marker matches the tree (%d)" % n_ex, stated == n_ex,
          "marker content is %r, tree has %d" % (got_ex, n_ex))

    # OPEN-DECISIONS: exact owner-burden ID set — no extras, omissions, duplicates,
    # or stale titles. Burden IDs are stable (Decision 0014 amendment).
    od = read("OPEN-DECISIONS.md")
    marker_lines = {}
    dupes = []
    for line in od.split("\n"):
        for mid in re.findall(r"<!--\s*owner-burden:([A-Z0-9-]+)\s*-->", line):
            if mid in marker_lines:
                dupes.append(mid)
            else:
                marker_lines[mid] = line
    authored_ids = [b["id"] for b in a["owner_only_burdens"]]
    check("OPEN-DECISIONS has no duplicate owner-burden ID", not dupes,
          "duplicated: %s" % sorted(set(dupes)))
    check("OPEN-DECISIONS covers every authored owner burden",
          set(authored_ids) <= set(marker_lines),
          "missing: %s" % sorted(set(authored_ids) - set(marker_lines)))
    check("OPEN-DECISIONS lists no extra owner burden",
          set(marker_lines) <= set(authored_ids),
          "extra: %s" % sorted(set(marker_lines) - set(authored_ids)))
    check("no authored owner-burden ID is duplicated in the state file",
          len(authored_ids) == len(set(authored_ids)))
    for b in a["owner_only_burdens"]:
        line = marker_lines.get(b["id"], "")
        check("OPEN-DECISIONS %s line carries the authored title verbatim" % b["id"],
              b["text"].lower() in line.lower(),
              "authored title %r not on the marker line" % b["text"])
    for banned in ["classical-edition verification", "schema repair", "source verification is owner"]:
        check("OPEN-DECISIONS free of ordinary-research burden %r" % banned,
              banned.lower() not in od.lower())

    status = read("STATUS.md")
    check("STATUS carries the terminology status", "NOT RUN" in status.upper())
    check("STATUS carries the empirical status",
          "no designed study" in status.lower() or "not run" in status.lower())
    check("STATUS records the open license decision", "license" in status.lower())

    # STATUS claim-status-by-lane block: exact equality with the authored wording.
    lane_block = marker(status, "claim-status-by-lane")
    check("STATUS has the claim-status-by-lane marker block", lane_block is not None)
    if lane_block is not None:
        got = {}
        bad_lines = []
        for line in lane_block.split("\n"):
            line = line.strip()
            if not line:
                continue
            m = re.match(r"-\s*([a-z_]+):\s*(.*)$", line)
            if m:
                got[m.group(1)] = m.group(2).strip()
            else:
                bad_lines.append(line)
        check("claim-status block has only well-formed '- lane: wording' lines",
              not bad_lines, "unparsed: %r" % bad_lines[:2])
        want = {k: " ".join(str(v).split()) for k, v in a["claim_status_wording"].items()}
        got = {k: " ".join(v.split()) for k, v in got.items()}
        check("claim-status block lane set is exactly the authored set",
              set(got) == set(want),
              "missing=%s extra=%s" % (sorted(set(want) - set(got)),
                                       sorted(set(got) - set(want))))
        for k in sorted(set(got) & set(want)):
            check("claim-status wording for lane %r is verbatim" % k, got[k] == want[k],
                  "surface=%r authored=%r" % (got[k], want[k]))

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
