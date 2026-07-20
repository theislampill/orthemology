#!/usr/bin/env python3
"""Decision-status / supersession validator (R4 independent review).

Guards against the Decision 0009 / 0011 defect class: two decisions both
"adopted" while defining one normative symbol incompatibly, with no
supersession notice at the superseded site. Checks, deterministically:

  1. every docs/decisions/NNNN-*.md file has a row in docs/decision-status.yaml
     and vice versa; statuses come from a closed vocabulary;
  2. for every registered normative symbol: the CURRENT formula appears in the
     current defining decision;
  3. every registered SUPERSEDED definition site still contains its historical
     formula (history preserved, not rewritten) AND carries a dated
     "SUPERSESSION NOTICE" that names the superseding decision;
  4. no OTHER decision file states a superseded formula (the superseding
     decision itself may quote it, e.g. in its Problem section);
  5. no CURRENT normative surface (theory/, manuscript/, companion/, docs/
     outside decisions, generated, and project-closure trees) states a
     superseded formula — historical archives are exempt.

Deterministic; offline."""
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
VALID_STATUSES = {"adopted", "adopted-with-superseded-clause", "superseded"}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    reg = yaml.safe_load(read("docs/decision-status.yaml"))
    rows = reg["decisions"]

    ddir = os.path.join(ROOT, "docs", "decisions")
    files = {f[:4]: f for f in sorted(os.listdir(ddir)) if re.match(r"^\d{4}-.*\.md$", f)}

    check("every decision file has a registry row", set(files) <= set(rows),
          "unregistered: %s" % sorted(set(files) - set(rows)))
    check("every registry row has a decision file", set(rows) <= set(files),
          "ghost rows: %s" % sorted(set(rows) - set(files)))
    for did, row in sorted(rows.items()):
        check("decision %s status is in the closed vocabulary" % did,
              row.get("status") in VALID_STATUSES, repr(row.get("status")))
    for did, row in sorted(rows.items()):
        if "superseded_by" in row:
            check("decision %s superseded_by %s resolves" % (did, row["superseded_by"]),
                  row["superseded_by"] in files)

    texts = {did: read(os.path.join("docs", "decisions", fn)) for did, fn in files.items()}

    for sym, spec in sorted(reg.get("normative_symbols", {}).items()):
        cur = spec["current"]
        cur_text = texts.get(cur["decision"], "")
        check("%s: current formula present in decision %s" % (sym, cur["decision"]),
              cur["formula"] in cur_text)

        superseding = {cur["decision"]}
        superseded_sites = set()
        for old in spec.get("superseded", []):
            did = old["decision"]
            superseded_sites.add(did)
            t = texts.get(did, "")
            check("%s: superseded formula preserved (not rewritten) in decision %s"
                  % (sym, did), old["formula"] in t)
            has_notice = re.search(r"SUPERSESSION NOTICE.*%s" % old["notice_must_reference"],
                                   t, re.S) is not None
            check("%s: decision %s carries a supersession notice naming %s"
                  % (sym, did, old["notice_must_reference"]), has_notice)
            # the registered supersession target must match the current definer
            check("%s: supersession notice target %s IS the current definer"
                  % (sym, old["notice_must_reference"]),
                  old["notice_must_reference"] == cur["decision"])

            # 4. no other decision restates the superseded formula
            offenders = [d for d, t2 in sorted(texts.items())
                         if old["formula"] in t2 and d not in superseded_sites | superseding]
            check("%s: no other decision restates the superseded formula" % sym,
                  not offenders, "restated in: %s" % offenders)

            # 5. current normative surfaces are free of the superseded formula.
            # Scans .md AND .yaml/.yml (a YAML gloss is as normative as prose), and
            # matches an ASCII-normalized form (∧ -> AND, := -> =, whitespace
            # collapsed) so a paraphrase cannot evade the exact-string scan — the
            # defect class the R4 fresh review found in docs/semantic-roles.yaml.
            def norm(s):
                return re.sub(r"\s+", " ", s.replace("∧", "AND").replace(":=", "="))

            offenders = []
            for base, _dirs, fns in os.walk(ROOT):
                rel_base = os.path.relpath(base, ROOT).replace("\\", "/")
                if rel_base.startswith((".git", "archive", "docs/decisions",
                                        "docs/project-closure", "docs/generated",
                                        "artifacts", "terminology")):
                    continue
                for fn in fns:
                    if not fn.endswith((".md", ".yaml", ".yml")):
                        continue
                    rel = (rel_base + "/" + fn).lstrip("./")
                    if rel == "docs/decision-status.yaml":
                        continue  # the supersession registry records the formula by design
                    if norm(old["formula"]) in norm(read(rel)):
                        offenders.append(rel)
            check("%s: no current normative surface states the superseded formula "
                  "(md+yaml, ASCII-normalized)" % sym,
                  not offenders, str(offenders))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
