#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "results" / "all_checks_results.json"
CHECKS = [
    ("SPA-R1", "check_r1_common_factor_registry.py", "r1_common_factor_registry_results.json"),
    ("SPA-R2", "check_r2_deletion_criterion.py", "r2_deletion_criterion_results.json"),
    ("SPA-R3", "check_r3_resource_quotient.py", "r3_resource_quotient_results.json"),
    ("SPA-R4", "check_r4_observation_cobuchi.py", "r4_observation_cobuchi_results.json"),
    ("SPA-R5", "check_r5_common_knowledge_radius.py", "r5_common_knowledge_radius_results.json"),
    ("SPA-R6", "check_r6_provenance_roots.py", "r6_provenance_root_results.json"),
    ("SPA-R7", "check_r7_representation_defect.py", "r7_representation_defect_results.json"),
    ("SPA-R8", "check_r8_collision_gain.py", "r8_collision_gain_results.json"),
    ("SPA-R9", "check_r9_common_decoder.py", "r9_common_decoder_results.json"),
    ("SPA-R10", "check_r10_minimum_collision_cover.py", "r10_minimum_collision_cover_results.json"),
    ("SPA-R11", "check_r11_history_state_twin.py", "r11_history_state_twin_results.json"),
    ("SPA-R12", "check_r12_predictive_quotient.py", "r12_predictive_quotient_results.json"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    entries: list[dict[str, object]] = []
    errors: list[str] = []
    mutant_killed = 0
    mutant_total = 0

    for result_id, script_name, result_name in CHECKS:
        script = BASE / "checks" / script_name
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=BASE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        result_path = BASE / "results" / result_name
        parsed: dict[str, object] = {}
        parse_error = None
        if result_path.exists():
            try:
                parsed = json.loads(result_path.read_text(encoding="utf-8"))
            except Exception as exc:  # audit output, not library API
                parse_error = f"{type(exc).__name__}: {exc}"
        else:
            parse_error = "result file absent"

        killed = int(parsed.get("mutants_killed", 0) or 0)
        total = int(parsed.get("mutants_total", 0) or 0)
        mutant_killed += killed
        mutant_total += total
        status = parsed.get("status")
        entry_ok = proc.returncode == 0 and status == "PASS" and killed == total and total > 0 and parse_error is None
        if not entry_ok:
            errors.append(result_id)
        entries.append(
            {
                "result_id": result_id,
                "script": f"checks/{script_name}",
                "script_sha256": sha256_bytes(script.read_bytes()),
                "returncode": proc.returncode,
                "stdout_sha256": sha256_bytes(proc.stdout),
                "stderr_sha256": sha256_bytes(proc.stderr),
                "reported_status": status,
                "mutants_killed": killed,
                "mutants_total": total,
                "result_file": f"results/{result_name}",
                "result_file_sha256": sha256_bytes(result_path.read_bytes()) if result_path.exists() else None,
                "parse_error": parse_error,
                "entry_pass": entry_ok,
            }
        )

    payload = {
        "schema": "spa-all-checks-results-v1",
        "status": "PASS" if not errors else "FAIL",
        "execution_mode": "fresh_subprocess_per_checker_no_imported_prefilled_counts",
        "python_executable": sys.executable,
        "rounds_executed": len(entries),
        "rounds_passed": sum(bool(e["entry_pass"]) for e in entries),
        "mutants_killed": mutant_killed,
        "mutants_total": mutant_total,
        "failed_result_ids": errors,
        "entries": entries,
        "claim_ceiling": "bounded constructed executable evidence only; no architecture implementation, Lean checking, adoption, novelty, or metaphysical conclusion",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("status", "rounds_passed", "rounds_executed", "mutants_killed", "mutants_total")}, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
