#!/usr/bin/env python3
"""Cold, isolated Lean replay. No installations; never overwrites evidence."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
COMPILER_SHA = "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
MODULES = ("VeracityBoundary", "VeracityControls")
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text_digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

def verify_public_package(root):
    manifest = json.loads((root / 'SOURCE_PACKAGE.json').read_text())
    for row in manifest['files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe package member')
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Selected source package identity mismatch: ' + row['path'])
    return {'status': 'PASS', 'selected_files': len(manifest['files']), 'historical_raw_source_binding_replay': 'NOT_RUN; locator-only public source selection'}

def check_sources():
    checked = verify_public_package(ROOT)
    bindings = json.loads((ROOT / 'SOURCE_LOCATORS.json').read_text())
    premise_map = json.loads((ROOT / 'SOURCE_PREMISE_MAP.json').read_text())
    for premise in premise_map['premises']:
        for key in premise['sealed_passage_ids']:
            assert key in bindings['paragraphs'], key
    checked['report_paragraph_locators'] = len(bindings['paragraphs'])
    checked['external_source_locators'] = len(bindings['external_sources'])
    return checked


def main():
    global LEAN
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    LEAN = args.lean.resolve()
    if args.output.is_symlink(): raise SystemExit("Refusing an existing output symlink")
    out = args.output.resolve()
    if out.exists(): raise SystemExit('Refusing to overwrite an existing replay directory')
    if any(out.is_relative_to(p) for p in [ROOT, LEAN.parent.parent]): raise SystemExit('Output must be outside source and compiler trees')
    if not out.parent.is_dir(): raise SystemExit('Output parent must exist')
    out = guarded_output(args.output,[ROOT,args.lean.parent.parent,LEAN.parent.parent])
    if not LEAN.is_file() or digest(LEAN) != COMPILER_SHA:
        raise SystemExit("Expected existing official Lean 4.19.0 executable is absent or has a different digest. No install attempted.")
    out.mkdir()
    env = os.environ.copy()
    env["LEAN_PATH"] = str(out)
    steps = []
    declarations = []
    dependencies = []

    def run(name, args, reject=False):
        result = subprocess.run([str(LEAN), *map(str, args)], cwd=ROOT, env=env,
                                capture_output=True, text=True, timeout=180)
        log = result.stdout + result.stderr
        (out / (name + ".log")).write_text(log)
        steps.append({"name": name, "arguments": list(map(str, args)), "exit_code": result.returncode,
                      "expected": "false-proposition rejection" if reject else "success", "log": name + ".log"})
        if reject:
            assert result.returncode != 0, name + " unexpectedly accepted"
            assert log.count("error:") == 1 and "tactic 'decide' proved that the proposition" in log and "is false" in log, name + " failed for the wrong reason"
            assert "failed to synthesize" not in log and "unknown" not in log, name + " elaboration failure"
        else:
            assert result.returncode == 0 and "error:" not in log and "warning:" not in log, name + " did not cleanly succeed"
        return log

    try:
        source_check = check_sources()
        (out / "SOURCE_BINDING_CHECK.json").write_text(json.dumps(source_check, indent=2) + "\n")
        version = run("toolchain", ["--version"])
        assert "version 4.19.0" in version, "wrong Lean version"
        for module in MODULES:
            source = ROOT / "src" / (module + ".lean")
            content = source.read_text()
            imports = re.findall(r"^import\s+(\S+)", content, re.M)
            assert imports == (["Init"] if module == "VeracityBoundary" else ["VeracityBoundary"]), "unexpected source import"
            assert not re.search(r"\b(sorry|admit|axiom|native_decide|unsafe)\b|Lean\.ofReduceBool", content), "forbidden proof escape"
            run(module, ["-o", out / (module + ".olean"), source])
            dep_log = run(module + "-direct-imports", ["--deps", source])
            for line in dep_log.splitlines():
                dep = Path(line.strip())
                if dep.is_file():
                    dependencies.append({"module": module, "path": str(dep), "sha256": digest(dep), "bytes": dep.stat().st_size})
            namespace = "VeracityBoundary" if module == "VeracityBoundary" else "VeracityBoundary.Controls"
            for name in re.findall(r"^theorem\s+(\w+)", content, re.M):
                declarations.append({"name": namespace + "." + name, "module": module, "source": str(source.relative_to(ROOT)),
                                     "source_line": content[:content.index("theorem " + name)].count("\n") + 1})
        run("api-contract", [ROOT / "tests/APIContract.lean"])
        run("acceptance", [ROOT / "tests/Acceptance.lean"])
        readback = ["import VeracityControls", "set_option pp.universes true", "set_option pp.proofs false", "set_option format.width 140"]
        proof_readback = ["import VeracityBoundary", "set_option pp.proofs true", "set_option format.width 140"]
        for declaration in declarations:
            readback += ["#print " + declaration["name"], "#print axioms " + declaration["name"]]
            if declaration["module"] == "VeracityBoundary":
                proof_readback += ["#print " + declaration["name"]]
        (out / "Readback.lean").write_text("\n".join(readback) + "\n")
        (out / "ProofReadback.lean").write_text("\n".join(proof_readback) + "\n")
        log = run("readback", [out / "Readback.lean"])
        run("proof-readback", [out / "ProofReadback.lean"])
        assert "sorryAx" not in log and "Lean.ofReduceBool" not in log, "unacceptable axiom"
        for declaration in declarations:
            name = re.escape(declaration["name"])
            match = re.search(r"'" + name + r"' depends on axioms: \[([^\]]*)\]", log)
            if match:
                axioms = [x.strip() for x in match.group(1).split(",") if x.strip()]
            else:
                assert re.search(r"'" + name + r"' does not depend on any axioms", log), "missing axiom readback: " + declaration["name"]
                axioms = []
            assert set(axioms) <= ALLOWED_AXIOMS, "nonstandard axiom: " + declaration["name"]
            declaration["axioms"] = axioms
        for source in sorted((ROOT / "tests/rejected").glob("*.lean")):
            run("rejected-" + source.stem, [source], reject=True)
        verify_public_package(ROOT)
        status = "PASS"
        failure = None
    except Exception as exc:
        status = "FAIL"
        failure = str(exc)

    files = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and path.parts[len(ROOT.parts)] not in {"validation", "development", "__pycache__"} and path.name != "SHA256SUMS":
            files.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest = {"schema": "t20-veracity-replay-v1", "status": status, "failure": failure,
                "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "compiler": {"path": str(LEAN), "sha256": digest(LEAN)},
                "scope": "Conditional Init-only mathematics and explicit finite interpretations, not metaphysical warrant or authentication",
                "direct_imports": dependencies, "source_files": files, "steps": steps,
                "declarations": declarations,
                "outputs": [{"path": str(path.relative_to(out)), "sha256": digest(path), "bytes": path.stat().st_size}
                            for path in sorted(out.rglob("*")) if path.is_file()]}
    (out / "VERIFICATION.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": status, "output": str(out), "steps": len(steps), "theorems": len(declarations), "failure": failure}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
