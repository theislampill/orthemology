"""Exact CLI replay, with two source-derived compile-map dependency entries.

The fixture is synthetic structural test data, not a diagnosis. This is not a
full repository build, CI run, release test, or live-model behavior test.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import subprocess
import sys
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parent
ROOT = BASE / "sources"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import check_ir_instance_integrity as ir
import compiled_runtime_lib as compile_lib


def main() -> None:
    # Exact compiler metadata formula, restricted to the two owners that the
    # stock sample and its checker self-tests resolve. No fabricated IDs or paths.
    mapping = {}
    for bundle, paths in compile_lib.BUNDLE_SOURCES.items():
        for path in paths:
            if Path(path).stem not in {"M1-self-refutation", "M8-reductio"}:
                continue
            doc = compile_lib.load_source_doc(ROOT, path)
            mapping[doc.module_id] = {
                "module_id": doc.module_id, "module_class": doc.module_class,
                "canonical_path": doc.canonical_path, "source": doc.source_rel_path,
                "source_sha256": doc.sha256, "bundle_path": bundle,
            }
    out = ROOT / "skill"
    out.mkdir(exist_ok=True)
    (out / "compiled-module-map.json").write_text(json.dumps({
        "replay_scope": "two-owner dependency projection, not a whole compiled runtime",
        "compiler_version": compile_lib.COMPILER_VERSION,
        "bundle_mapping_version": compile_lib.BUNDLE_MAPPING_VERSION,
        "modules": mapping,
    }, indent=2) + "\n")
    assert set(mapping) == {"M1-self-refutation", "M8-reductio"}

    schema = json.loads((ROOT / "atomics/skill/references/diagnostics/diagnostic-ir.schema.json").read_text())
    validator = Draft202012Validator(schema)
    original = copy.deepcopy(ir.POSITIVE_SAMPLE)
    original_schema_errors = [(list(e.absolute_path), e.message) for e in validator.iter_errors(original)]
    # Original has the inherited, independent reason_category=3/open-gate issue.
    # Set category 1 in BOTH control and experimental records to isolate this
    # specific recognition guard. This is test-fixture surgery only.
    control = copy.deepcopy(original)
    control["reason_category"] = 1
    control["alignment_state"] = "alignment-advanced"
    control["recognition_strength"] = "strong"
    assert not list(validator.iter_errors(control))
    fixture_dir = ROOT / "replay-fixtures"
    fixture_dir.mkdir(exist_ok=True)
    log_dir = BASE / "replay-logs"
    log_dir.mkdir(exist_ok=True)
    results = []
    for strength in ("strong", "medium", "weak", "none"):
        sample = copy.deepcopy(control)
        sample["recognition_strength"] = strength
        fixture = fixture_dir / f"alignment-advanced-{strength}.json"
        fixture.write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n")
        schema_errors = [{"path": list(e.absolute_path), "message": e.message}
                         for e in validator.iter_errors(sample)]
        command = [sys.executable, "-B", str(ROOT / "tools/check_ir_instance_integrity.py"), "--file", str(fixture)]
        run = subprocess.run(command, text=True, capture_output=True)
        (log_dir / f"custom-cli-{strength}.txt").write_text(run.stdout + run.stderr)
        (log_dir / f"jsonschema-{strength}.json").write_text(json.dumps(schema_errors, indent=2) + "\n")
        assert run.returncode == 0, (strength, run.stdout, run.stderr)
        assert bool(schema_errors) == (strength != "strong"), (strength, schema_errors)
        results.append({"strength": strength, "cli_command": command,
                        "custom_cli_exit": run.returncode, "full_schema_errors": schema_errors})
    results_path = BASE / "FULL_PATH_RESULTS.json"
    results_path.write_text(json.dumps({
        "frozen_commit": "c86b3c6673147b8802fe222373a165a37d4d24a8",
        "source_dependency_method": "Exact pinned helpers plus the two required module-map entries derived using load_source_doc and BUNDLE_SOURCES; full runtime was not rebuilt.",
        "original_embedded_sample_schema_errors": original_schema_errors,
        "control_changes": {"reason_category": 1, "alignment_state": "alignment-advanced", "recognition_strength": "strong"},
        "only_experimental_change": "recognition_strength",
        "same_records_both_validators": True,
        "results": results,
        "scope_limit": "Official custom CLI acceptance demonstrated with stated dependency projection. No claim about every downstream production checker, full CI, live model, or empirical recognition."
    }, ensure_ascii=False, indent=2) + "\n")
    print(results_path.read_text())


if __name__ == "__main__":
    main()
