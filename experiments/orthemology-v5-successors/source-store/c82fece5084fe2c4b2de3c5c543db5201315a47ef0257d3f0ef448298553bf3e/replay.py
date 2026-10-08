#!/usr/bin/env python3
"""Portable, fixed-scope replay of the T20 exact scalar-fusion reduction.

Supply the unchanged T16 source package, official Lean 4.19.0 executable,
prepared exact pinned dependencies, and a new output directory. No installation,
network access, inherited controls, or broader scientific replay is performed.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess

if not __debug__:
    raise SystemExit("OPTIMIZED_PYTHON_UNSUPPORTED")
HERE = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda name: json.loads((HERE / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["predecessor", "lean", "dependencies", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    predecessor, lean, dependencies, output = [getattr(args, n).resolve()
        for n in ["predecessor", "lean", "dependencies", "output"]]
    if output.exists():
        raise SystemExit("FRESH_OUTPUT_REQUIRED")
    for protected in [predecessor, dependencies, HERE]:
        if output == protected or protected in output.parents or output in protected.parents:
            raise SystemExit("OUTPUT_OVERLAPS_INPUT_REFUSED")
    for row in read("FILE_MANIFEST.json")["files"]:
        assert sha(HERE / row["path"]) == row["sha256"], row["path"]
    scope, closure = read("PROOF_SCOPE.json"), read("PREDECESSOR_CLOSURE.json")
    assert sha(lean) == scope["lean_binary_sha256"]
    version = subprocess.check_output([str(lean), "--version"], text=True).strip()
    assert "version 4.19.0," in version and "6caaee842e94" in version
    assert sha(predecessor / "MATHEMATICAL_SOURCE_LOCK.json") == closure["source_lock_sha256"]
    for row in closure["records"]:
        assert sha(predecessor / row["path"]) == row["sha256"], row["module"]
    pins = read("lake-manifest.json")["packages"]
    for pin in pins:
        repo = dependencies / pin["name"]
        assert subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip() == pin["rev"]
        assert not subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"], text=True).strip()
    for row in read("DEPENDENCY_OBJECTS.json")["records"]:
        assert sha(dependencies / row["path"]) == row["sha256"], row["path"]
    output.mkdir(parents=True)
    objects, logs = output / "objects", output / "logs"
    objects.mkdir(); logs.mkdir()
    paths = [objects, *[dependencies / pin["name"] / ".lake/build/lib/lean" for pin in pins]]
    env = dict(os.environ, LEAN_NUM_THREADS="1", LEAN_PATH=":".join(map(str, paths)))
    records = []

    def run(name, command, expected=0, diagnostic=None):
        result = subprocess.run(command, cwd=output, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
        log = logs / (name + ".log"); log.write_text(result.stdout)
        records.append({"name": name, "exit": result.returncode, "expected_exit": expected, "log_sha256": sha(log)})
        (output / "PROGRESS.json").write_text(json.dumps(records, indent=2) + "\n")
        assert result.returncode == expected, name
        if diagnostic: assert diagnostic in result.stdout, name
        if expected == 0: assert "sorryAx" not in result.stdout and "error:" not in result.stdout, name
        print(name + " PASS", flush=True)
        return result.stdout

    for row in closure["records"]:
        obj = objects / (row["module"].replace(".", "/") + ".olean")
        obj.parent.mkdir(parents=True, exist_ok=True)
        run("inherited-" + row["module"], [str(lean), "--trust=0", "--root=" + str(predecessor / "lean"), "-o", str(obj), str(predecessor / row["path"])])
    for name in ["ScalarFusionCore", "ScalarFusionReverse", "ClosedProofCanonicalisation", "LiteralScalarFusion"]:
        module = HERE / ("src/" + name + ".lean")
        assert sha(module) == scope["source_sha256"][name]
        run(name, [str(lean), "--trust=0", "--root=" + str(HERE / "src"), "-o", str(objects / (name + ".olean")), str(module)])
    for name in scope["success_tests"]:
        text = run(name, [str(lean), "--trust=0", str(HERE / ("tests/" + name + ".lean"))])
        if name == "AllDeclarationAxioms":
            names = re.findall(r"'([^']+)' (?:depends on axioms:|does not depend on any axioms)", text)
            assert names == scope["new_declaration_names"]
            for group in re.findall(r"depends on axioms:\s*\[([^]]*)\]", text, re.S):
                assert {x.strip() for x in group.split(",") if x.strip()} <= set(scope["expected_new_axioms_subset"])
    for name, diagnostic in scope["rejection_tests"].items():
        run(name, [str(lean), "--trust=0", str(HERE / ("tests/" + name + ".lean"))], 1, diagnostic)
    for row in closure["records"]:
        assert sha(predecessor / row["path"]) == row["sha256"], row["module"]
    receipt = {"status": "PASS", "scope": scope["scope"], "new_source_sha256": scope["source_sha256"],
        "literal_x_xpluszero_HasE": "OPEN", "old_T16_registry_status": "NOT_RUN",
        "fresh_predecessor_modules_as_dependencies": len(closure["records"]),
        "all_new_declarations_checked": len(scope["new_declaration_names"]), "records": records}
    (output / "SCOPED_REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("T20_EXACT_SCALAR_FUSION_REPLAY_PASS", flush=True)


if __name__ == "__main__":
    main()
