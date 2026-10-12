"""Build/test an unapplied one-guard candidate in a separate research copy."""
from __future__ import annotations
import copy
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "sources"
CANDIDATE = BASE / "candidate-copy"
REL = Path("tools/check_ir_instance_integrity.py")
EXPECTED_BLOB = "469a1d4e60520671171caf4989353460eada7a8b"


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    before = (SOURCE / REL).read_bytes()
    assert git_blob(before) == EXPECTED_BLOB
    # Whole research source copy only. The actual repository is not a target.
    shutil.copytree(SOURCE, CANDIDATE, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    old = before.decode("utf-8")
    anchor = '    if "reason_category" in instance and instance.get("reason_category") not in REASON_CATEGORY_VALUES:\n'
    assert old.count(anchor) == 1
    insert = '''    if (
        instance.get("alignment_state") == "alignment-advanced"
        and "recognition_strength" in instance
        and instance["recognition_strength"] != "strong"
    ):
        errors.append("schema: alignment-advanced requires recognition_strength strong when supplied")

'''
    new = old.replace(anchor, insert + anchor)
    (CANDIDATE / REL).write_bytes(new.encode("utf-8"))
    patch = "".join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                       fromfile="a/" + REL.as_posix(), tofile="b/" + REL.as_posix()))
    (BASE / "UNAPPLIED_RECOGNITION_GUARD.patch").write_text(patch)

    schema = json.loads((SOURCE / "atomics/skill/references/diagnostics/diagnostic-ir.schema.json").read_text())
    validator = Draft202012Validator(schema)
    strong = json.loads((SOURCE / "replay-fixtures/alignment-advanced-strong.json").read_text())
    candidates = [(s, json.loads((SOURCE / f"replay-fixtures/alignment-advanced-{s}.json").read_text()))
                  for s in ("strong", "medium", "weak", "none")]
    omitted = copy.deepcopy(strong)
    del omitted["recognition_strength"]
    candidates.append(("omitted", omitted))
    nonadvanced = copy.deepcopy(strong)
    nonadvanced.update({"alignment_state": "tribunal-loosened", "recognition_strength": "none"})
    candidates.append(("nonadvanced-none", nonadvanced))
    logs = BASE / "candidate-logs"
    logs.mkdir(exist_ok=True)
    results = []
    for name, record in candidates:
        target = CANDIDATE / "replay-fixtures" / f"candidate-{name}.json"
        target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        errors = [{"path": list(e.absolute_path), "message": e.message}
                  for e in validator.iter_errors(record)]
        command = [sys.executable, "-B", str(CANDIDATE / REL), "--file", str(target)]
        run = subprocess.run(command, capture_output=True, text=True)
        (logs / (name + ".txt")).write_text(run.stdout + run.stderr)
        should_reject = name in {"medium", "weak", "none", "omitted"}
        assert bool(errors) == should_reject, (name, errors)
        assert (run.returncode != 0) == should_reject, (name, run.returncode, run.stdout, run.stderr)
        if name in {"medium", "weak", "none"}:
            assert "alignment-advanced requires recognition_strength strong" in run.stdout
        if name == "omitted":
            assert "missing required field: recognition_strength" in run.stdout
        results.append({"case": name, "expected_exit": 1 if should_reject else 0,
                        "actual_exit": run.returncode, "schema_errors": errors,
                        "command": command})
    assert (SOURCE / REL).read_bytes() == before
    result = {
        "unapplied": True,
        "repository_changed": False,
        "frozen_commit": "c86b3c6673147b8802fe222373a165a37d4d24a8",
        "target": REL.as_posix(),
        "preimage_git_blob_sha": git_blob(before),
        "preimage_sha256": hashlib.sha256(before).hexdigest(),
        "candidate_git_blob_sha": git_blob(new.encode()),
        "candidate_sha256": hashlib.sha256(new.encode()).hexdigest(),
        "patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
        "dependency_scope": "Unchanged two-owner compiler-derived map projection from full-path replay; no complete runtime rebuild or full CI.",
        "guard_scope": "Mirrors only the existing advanced-alignment implication for an included recognition_strength; preserves current missing-field behavior.",
        "results": results,
    }
    (BASE / "CANDIDATE_REPAIR_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
