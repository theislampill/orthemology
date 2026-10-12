"""Bounded replay of pinned DAEE witness typing and its recognition guard.

This imports unchanged source copies. It does not run the full repo suite, infer
human states, or classify a successful correction as recovered knowledge.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
SOURCES = BASE / "sources"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCES / "tools"))
import check_ir_instance_integrity as ir
from jsonschema import Draft202012Validator


def main() -> None:
    binding = json.loads((BASE / "SOURCE_BINDINGS.json").read_text())
    for item in binding["files"]:
        b = (SOURCES / item["path"]).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert actual == item["git_blob_sha"], item["path"]

    witness = copy.deepcopy(ir.POSITIVE_SAMPLE["field_witness"])
    baseline_errors = ir.field_witness_errors(witness)
    assert not baseline_errors, baseline_errors
    checks = [{"case": "unaltered embedded field witness", "errors": baseline_errors}]
    edits = [
        ("closure moved to interlocutor field", "closure", "operator", "𝒞(Ψᴵ)", "closure.operator"),
        ("transfer made guaranteed", "transfer_boundary", "mode", "guaranteed-update", "transfer_boundary.mode"),
        ("runtime source moved to interlocutor", "transfer_boundary", "from", "Ψᴵ", "transfer_boundary.from"),
    ]
    for title, section, key, value, marker in edits:
        candidate = copy.deepcopy(witness)
        candidate[section][key] = value
        errors = ir.field_witness_errors(candidate)
        assert any(marker in e for e in errors), (title, errors)
        checks.append({"case": title, "errors": errors})

    # Test the exact published guard as a guard, rather than pretending that
    # this projection is a full IR or a complete behavioral execution.
    schema = json.loads((SOURCES / "atomics/skill/references/diagnostics/diagnostic-ir.schema.json").read_text())
    guard = next(rule for rule in schema["allOf"]
                 if rule.get("if", {}).get("properties", {}).get("alignment_state", {}).get("const") == "alignment-advanced")
    guard_results = []
    for strength in ("none", "weak", "medium", "strong"):
        projection = {"alignment_state": "alignment-advanced", "recognition_strength": strength}
        declared_errors = [e.message for e in Draft202012Validator(guard).iter_errors(projection)]
        candidate = copy.deepcopy(ir.POSITIVE_SAMPLE)
        candidate.update(projection)
        custom_errors = ir.schema_errors(candidate, schema)
        assert not custom_errors, custom_errors
        assert bool(declared_errors) == (strength != "strong")
        guard_results.append({"recognition_strength": strength,
                              "published_guard_errors": declared_errors,
                              "custom_schema_errors": custom_errors})

    result = {
        "frozen_commit": binding["frozen_commit"],
        "scope": "Exact copied field_witness_errors and schema_errors plus the published alignment guard only; no full pipeline or live-model replay.",
        "verified_source_files": len(binding["files"]),
        "witness_boundary_checks": checks,
        "alignment_guard_checks": guard_results,
        "conclusions": [
            "Actual witness typing separates runtime closure from interlocutor update.",
            "The published advanced-alignment recognition-strength guard is not enforced by custom schema_errors.",
            "Neither result establishes actual knowledge, willingness, prior acquisition, restoration, or warrant."
        ]
    }
    (BASE / "CHECK_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
