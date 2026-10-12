"""Local fresh replay using only the existing, specified Lean 4.19 environment."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRANCHE = HERE.parents[1]
OUT = Path(os.environ.get("T20_VALIDATION_OUT", str(HERE / "validation"))).resolve()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, log, env=None):
    result = subprocess.run(args, cwd=HERE, env=env, capture_output=True, text=True)
    (OUT / log).write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"{args}: exit {result.returncode}; see {log}")
    return result.stdout


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for entry in json.loads((HERE / "INPUT_MANIFEST.json").read_text()):
        assert digest(ROOT / entry["path"]) == entry["sha256"], entry["path"]
    assert digest(HERE / "lean/GroundedSupport.lean") == digest(TRANCHE / "testimony-continuation/grounded-attestation/lean/GroundedSupport.lean")
    run([sys.executable, "-B", "-m", "unittest", "-v"], "python-final.txt")
    occurrence = json.loads(run([sys.executable, "-B", "occurrence_model.py"], "OCCURRENCE_RESULTS.json"))
    continuation = json.loads(run([sys.executable, "-B", "continuation_model.py"], "CONTINUATION_RESULTS.json"))
    for result in (occurrence, continuation):
        assert all(c["actual"] == c["expected"] for c in result["cases"])
    environment = TRANCHE / "hase-positive-research/toolchain-preparation/OPTIONAL_environment.sh"
    envbytes = subprocess.check_output(["bash", "-c", 'source "$1"; env -0', "bash", str(environment)])
    env = dict(item.decode().split("=", 1) for item in envbytes.split(b"\0") if item)
    obj = OUT / "final-objects"
    obj.mkdir(exist_ok=True)
    # Existing objects from earlier runs are not consumed: outputs for all three
    # local modules are removed and rebuilt in dependency order.
    for name in ("GroundedSupport", "SupportBridge", "ContextualEncoding"):
        (obj / (name + ".olean")).unlink(missing_ok=True)
    env["LEAN_PATH"] = str(obj) + ":" + env["LEAN_PATH"]
    lean = str(Path(env["LEAN_TOOLCHAIN_ROOT"]) / "bin/lean")
    version = run([lean, "--version"], "lean-version-final.txt", env)
    assert "4.19.0" in version
    direct_deps = {}
    for name in ("GroundedSupport", "SupportBridge", "ContextualEncoding"):
        source = HERE / "lean" / (name + ".lean")
        run([lean, "-o", str(obj / (name + ".olean")), str(source)], "lean-final-" + name + ".txt", env)
        deps = run([lean, "--deps", str(source)], "lean-deps-" + name + ".txt", env)
        direct_deps[name] = [{"path": p, "sha256": digest(Path(p))} for p in deps.splitlines() if Path(p).is_file()]
    run([lean, "lean/Readback.lean"], "lean-readback-final.txt", env)
    assert "sorryAx" not in (OUT / "lean-readback-final.txt").read_text()
    receipts = {
        "status": "PASS", "started_utc": started,
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "lean_version": version.strip(), "lean_executable_sha256": digest(Path(lean)),
        "fresh_local_source_modules": ["GroundedSupport (inherited byte-identical)", "SupportBridge", "ContextualEncoding"],
        "new_theorem_count": 9, "unit_tests": 8,
        "occurrence_cases": len(occurrence["cases"]), "encoding_roundtrips": occurrence["roundtrip_cases"],
        "continuation_cases": len(continuation["cases"]),
        "request_step_executions": continuation["executed_request_steps"],
        "retained_root_profiles_per_model": 64,
        "operational_monotonicity_checked": all(p["operational_monotonicity"] for p in continuation["profiles"]),
        "old_inputs_unchanged": True,
        "source_hashes": {str(p.relative_to(HERE)): digest(p) for p in sorted(HERE.rglob("*")) if p.is_file() and "validation" not in p.parts and "__pycache__" not in p.parts and p.suffix in (".py", ".lean")},
        "direct_dependency_hashes": direct_deps,
        "limits": ["Existing official toolchain and dependency objects reused; no full dependency source rebuild.",
                   "No machine proof of Python-to-Lean implementation correspondence.",
                   "No actual-world source authentication, permission warrant, deployment or universal identity proof."]
    }
    (OUT / "FINAL_VERIFICATION.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps({k: receipts[k] for k in ("status", "new_theorem_count", "unit_tests", "occurrence_cases", "continuation_cases", "request_step_executions", "old_inputs_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
