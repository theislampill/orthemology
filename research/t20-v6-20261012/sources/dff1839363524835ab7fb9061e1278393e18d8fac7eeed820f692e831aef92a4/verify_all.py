#!/usr/bin/env python3
"""Portable, isolated replay of the declared mathematical packet.

Requires Python standard library and the official Lean 4.19.0 compiler. No
network, remote mutation, inherited Seventh script, or optional solver is used.
Results are written outside the frozen source payload in the chosen output dir.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
INPUTS = ["dynamic_interlock.py", "verify_dynamic.py", "verify_covering.py",
          "DynamicInterlock.lean", "CoveringCore.lean", "COVERING_WITNESSES.json"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", help="Path to the official Lean 4.19.0 executable")
    ap.add_argument("--output-dir", default=str(ROOT / "verification-replay"))
    args = ap.parse_args()
    lean = args.lean or shutil.which("lean")
    if not lean:
        recorded = json.loads((ROOT / "LEAN_TOOLCHAIN_RECEIPT.json").read_text())["lean_executable"]
        if Path(recorded).is_file():
            lean = recorded
    if not lean:
        raise SystemExit("Lean unavailable. Supply --lean with official Lean 4.19.0; no kernel pass is inferred.")
    lean = str(Path(lean).resolve())
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    if "version 4.19.0," not in version:
        raise SystemExit(f"Wrong pinned compiler: {version}")
    out = Path(args.output_dir).resolve()
    if out == ROOT:
        raise SystemExit("Choose an output directory separate from the source packet.")
    out.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / "SOURCE_BINDING.json").read_text())
    for source in sources["sources"]:
        assert sha(ROOT / source["packet_copy"]) == source["sha256"]
    steps = []
    with tempfile.TemporaryDirectory(prefix="dynamic-interlock-replay-") as raw:
        work = Path(raw)
        for name in INPUTS:
            shutil.copyfile(ROOT / name, work / name)
        (work / "build").mkdir()
        commands = [
            ("finite", [os.sys.executable, "verify_dynamic.py"], {}),
            ("covering", [os.sys.executable, "verify_covering.py"], {}),
            ("lean_interlock", [lean, "-o", "build/DynamicInterlock.olean", "DynamicInterlock.lean"], {}),
            ("lean_covering", [lean, "CoveringCore.lean"], {"LEAN_PATH": str(work / "build")}),
        ]
        for name, command, extra_env in commands:
            result = subprocess.run(command, cwd=work, env={**os.environ, **extra_env},
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log = out / f"{name}.log"
            log.write_text(result.stdout)
            if result.returncode or "sorryAx" in result.stdout:
                raise SystemExit(f"Failed {name}: exit {result.returncode}; inspect {log}")
            steps.append({"step": name, "exit_code": result.returncode,
                          "log": log.name, "log_sha256": sha(log)})
        results = {}
        for name in ["FINITE_CHECK_RESULTS.json", "COVERING_CHECK_RESULTS.json", "DELETION_TRACES.json"]:
            shutil.copyfile(work / name, out / name)
            if name != "DELETION_TRACES.json":
                results[name] = json.loads((work / name).read_text())
    receipt = {
        "status": "PASS_AUTHOR_ISOLATED_REPLAY",
        "independent_review": "PENDING_V2_REVIEW",
        "lean_version": version,
        "source_sha256": {name: sha(ROOT / name) for name in INPUTS},
        "bound_sixth_source_copies_verified": len(sources["sources"]),
        "steps": steps,
        "results": results,
        "formal_scope": ["root counting and honest overlap", "live revocation exclusion",
                         "charged cancellation exclusion and availability",
                         "joint local binding / revocation / institution composition",
                         "threshold arithmetic and minimum roots",
                         "unique maximal good path and abstract untested candidate",
                         "idempotent repair persistence", "covering-to-portfolio equivalence",
                         "singleton incidence bound", "four-edge finite graph lemma"],
        "ordinary_only_scope": ["full execution-history/world applicability argument",
                                "general covering-number optimality reduction and binomial enumeration",
                                "nine-point seven-block contradiction before its graph lemma"],
        "not_claimed": ["physical implementation certification", "kernel formalization of every ordinary proof",
                        "unrestricted mobile faults", "currentness oracle", "new quorum or covering mathematics",
                        "fixed R5 resource enlargement or defeat"]
    }
    (out / "REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
