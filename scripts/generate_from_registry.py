#!/usr/bin/env python3
"""Generate machine surfaces from the canonical verdict registry (R3 §7.3 /
daee-epistemics import: canonical atomized source -> generated surfaces).

Generates:
  - schemas/verdict-record.schema.json $defs.verdict_id.enum  (semantic IDs,
    registry order);
  - docs/generated/verdict-aliases.md  (prose table: alias, id, name, factive,
    core-path membership) — the prose surface other docs may embed or cite.

Modes: default = write; --check = fail if any generated surface would change
(drift detection for CI).
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


def build():
    reg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    ids = [v["id"] for v in reg["verdicts"]]
    core = set(reg["core_path"])

    spath = os.path.join(ROOT, "schemas", "verdict-record.schema.json")
    sdoc = json.load(open(spath, encoding="utf-8"))
    sdoc["$defs"]["verdict_id"]["enum"] = ids
    schema_text = json.dumps(sdoc, ensure_ascii=False, indent=2) + "\n"

    lines = [
        "# Verdict aliases (GENERATED — do not edit)",
        "",
        "Generated from `docs/verdict-registry.yaml` by `scripts/generate_from_registry.py`.",
        "Semantic IDs are authoritative in machine records; display aliases are prose-only (Decision 0004).",
        "",
        "| Alias | Semantic ID | Name | Factive | CorePath |",
        "|---|---|---|---|---|",
    ]
    for v in reg["verdicts"]:
        lines.append("| %s | `%s` | %s | %s | %s |" % (
            v.get("alias", ""), v["id"], v.get("name", ""),
            "yes" if v.get("factive") else "no",
            "yes" if v["id"] in core else "no"))
    table_text = "\n".join(lines) + "\n"
    return [(spath, schema_text), (os.path.join(ROOT, "docs", "generated", "verdict-aliases.md"), table_text)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    fails = 0
    for path, text in build():
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if args.check:
            ok = current == text
            print("[%s] generated surface current: %s" % ("PASS" if ok else "FAIL",
                                                          os.path.relpath(path, ROOT)))
            fails += 0 if ok else 1
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("wrote", os.path.relpath(path, ROOT))
    if args.check:
        print("TOTAL: %d failures" % fails)
        sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
