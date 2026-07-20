#!/usr/bin/env python3
"""Generate docs/current-state.yaml — the single canonical project-state source
(Decision 0014; daee-epistemics import: canonical source -> generated surfaces).

The file has two blocks:
  authored:  human/agent-maintained facts (revision label, owner burdens,
             research residuals, open parameters, claim-status wording).
             The generator PRESERVES this block verbatim.
  derived:   everything countable or hashable from the tree (decision IDs,
             schema/example/fixture/validator counts, PDF paths+hashes+pages,
             terminology freeze hashes, source-status summary, and the
             convergent source_tree_digest drift key over the declared
             source-input set in docs/project-state-inputs.yaml).
             The generator RECOMPUTES this block. No commit hash appears in
             the derived block: exact equality with a value derived from HEAD
             inside a tracked file cannot converge (Decision 0014 amendment).

`--check` recomputes and fails on any drift instead of writing.
"""
import argparse
import hashlib
import io
import json
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
STATE = os.path.join(ROOT, "docs", "current-state.yaml")
INPUT_POLICY = os.path.join(ROOT, "docs", "project-state-inputs.yaml")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def source_tree_digest():
    """Convergent drift key (Decision 0014 amendment): SHA-256 over sorted
    "relpath NUL file-sha256 LF" records for every git-tracked file not excluded
    by docs/project-state-inputs.yaml. Contains no commit hash, so committing the
    regenerated state file cannot invalidate it."""
    policy = yaml.safe_load(open(INPUT_POLICY, encoding="utf-8"))
    excl = policy.get("exclude", [])

    def excluded(rel):
        return any(rel.startswith(e) if e.endswith("/") else rel == e for e in excl)

    rows = []
    for rel in sorted(f for f in git("ls-files").splitlines() if f):
        p = os.path.join(ROOT, rel)
        if excluded(rel) or not os.path.isfile(p):
            continue
        rows.append(rel + "\x00" + sha256(p) + "\n")
    return hashlib.sha256("".join(rows).encode("utf-8")).hexdigest()


def git(*args, default="UNKNOWN"):
    try:
        return subprocess.check_output(["git"] + list(args), cwd=ROOT).decode().strip()
    except Exception:
        return default


def count_files(rel, pattern):
    d = os.path.join(ROOT, rel)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if re.search(pattern, f))


def derive():
    decisions = count_files("docs/decisions", r"^\d{4}-.*\.md$")
    decision_ids = [d[:4] for d in decisions]
    schemas = count_files("schemas", r"\.schema\.json$")
    examples_json = count_files("examples", r"\.json$")
    examples_md = count_files("examples", r"\.md$")
    validators = sorted(f for f in os.listdir(os.path.join(ROOT, "scripts"))
                        if f.startswith(("validate_", "audit_", "derive_")) and f.endswith(".py"))

    pdfs = {}
    art = os.path.join(ROOT, "artifacts")
    if os.path.isdir(art):
        for fn in sorted(f for f in os.listdir(art) if f.endswith(".pdf")):
            side_path = os.path.join(art, fn.replace(".pdf", ".sources.json"))
            side = json.load(open(side_path, encoding="utf-8")) if os.path.exists(side_path) else {}
            pdfs[fn] = {"sha256": sha256(os.path.join(art, fn)),
                        "pages": side.get("page_count"),
                        "source_commit": side.get("source_commit")}

    def freeze(rel):
        p = os.path.join(ROOT, rel, "FREEZE-HASH.txt")
        if not os.path.exists(p):
            return None
        for line in io.open(p, encoding="utf-8"):
            line = line.strip()
            if len(line) == 64 and all(c in "0123456789abcdef" for c in line):
                return line
        return None

    src_status = {}
    ssp = os.path.join(ROOT, "references", "source-status.yaml")
    if os.path.exists(ssp):
        reg = yaml.safe_load(open(ssp, encoding="utf-8")) or {}
        for row in reg.get("claims", []):
            src_status[row["status"]] = src_status.get(row["status"], 0) + 1

    fixtures = {}
    for rel, key in (("tests/verdict-fixtures.json", "verdict"),
                     ("tests/reason-fixtures.json", "reason"),
                     ("tests/claim-reasoning-fixtures.json", "claim_reasoning"),
                     ("tests/reqpath-fixtures.json", "reqpath"),
                     ("tests/latent-state-fixtures.json", "latent_state")):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            doc = json.load(open(p, encoding="utf-8"))
            items = doc.get("fixtures") or doc.get("cases") or []
            if isinstance(doc, dict) and not items:
                items = [k for k in doc if k.startswith(("F", "CR", "RP", "LS"))]
            fixtures[key] = len(items)
    neg = os.path.join(ROOT, "tests", "schema-negative", "NEGATIVE-FIXTURES.json")
    if os.path.exists(neg):
        fixtures["negative"] = len(json.load(open(neg, encoding="utf-8"))["fixtures"])
    inv = os.path.join(ROOT, "tests", "invalid")
    if os.path.isdir(inv):
        fixtures["invalid_records"] = len([f for f in os.listdir(inv) if f.endswith(".json")])

    return {
        "source_tree_digest": source_tree_digest(),
        "source_tree_digest_policy": "docs/project-state-inputs.yaml",
        "tracked_files": len(git("ls-files").splitlines()),
        "decision_ids": decision_ids,
        "decision_count": len(decision_ids),
        "schemas": schemas,
        "schema_count": len(schemas),
        "example_json_count": len(examples_json),
        "example_markdown_count": len(examples_md),
        "validator_scripts": validators,
        "validator_count": len(validators),
        "fixture_counts": fixtures,
        "pdfs": pdfs,
        "terminology_freeze_hashes": {"pilot0_v1": freeze("terminology/pilot0"),
                                      "pilot0_v2": freeze("terminology/pilot0-v2")},
        "source_status_summary": src_status,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    doc = yaml.safe_load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    authored = doc.get("authored", {})
    new = {"schema": "orthemology-current-state-v1",
           "note": ("GENERATED derived block — edit only the authored block, then run "
                    "scripts/generate_current_state.py. CI checks for drift."),
           "authored": authored,
           "derived": derive()}
    text = yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=100)

    if args.check:
        current = open(STATE, encoding="utf-8").read() if os.path.exists(STATE) else ""
        ok = current == text
        print("[%s] docs/current-state.yaml derived block is current" % ("PASS" if ok else "FAIL"))
        print("TOTAL: %d failures" % (0 if ok else 1))
        sys.exit(0 if ok else 1)

    io.open(STATE, "w", encoding="utf-8", newline="\n").write(text)
    print("wrote docs/current-state.yaml (%d decisions, %d schemas, %d validators)"
          % (new["derived"]["decision_count"], new["derived"]["schema_count"],
             new["derived"]["validator_count"]))


if __name__ == "__main__":
    main()
