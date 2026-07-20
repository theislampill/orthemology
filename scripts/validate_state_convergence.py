#!/usr/bin/env python3
"""Prove the generated-state contract converges across a commit boundary
(Decision 0014, R4 independent-review amendment).

The pre-amendment contract stored `source_commit_at_generation = git rev-parse HEAD`
inside the tracked state file, so committing a regeneration always produced a new
HEAD and the check could never pass on the commit that contained it. This script
is the standing regression against that class of defect. In a throwaway git
repository built from the current tree it verifies:

  1. regenerate -> commit the state file -> `--check` PASSES on the very commit
     that contains the regenerated file (commit-boundary convergence);
  2. a second `--check` with no changes still passes (idempotence);
  3. tamper control: mutating one declared source input makes `--check` FAIL
     (the digest is not vacuous);
  4. mutating an excluded generated artifact does NOT trip the digest
     (exclusion policy honored; such files carry their own checks).

Offline; uses only the local git binary and the tree itself.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name,
                         (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def run(args, cwd, expect=None):
    r = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    if expect is not None and r.returncode != expect:
        return False, r.stdout.decode(errors="replace")[-400:]
    return True, r.stdout.decode(errors="replace")[-400:]


def main():
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode().splitlines()
    tmp = tempfile.mkdtemp(prefix="orthemology-convergence-")
    try:
        for rel in files:
            src = os.path.join(ROOT, rel)
            if not os.path.isfile(src):
                continue
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

        env_git = ["git", "-c", "user.name=convergence-test",
                   "-c", "user.email=convergence-test@localhost"]
        for args in (["git", "init", "-q"],
                     ["git", "add", "-A"],
                     env_git + ["commit", "-q", "-m", "base"]):
            ok, out = run(args, tmp, expect=0)
            if not ok:
                check("throwaway repo setup", False, out)
                print("TOTAL: %d failures" % len(FAILS))
                sys.exit(1)

        gen = [sys.executable, os.path.join(tmp, "scripts", "generate_current_state.py")]

        ok, out = run(gen, tmp, expect=0)
        check("regeneration succeeds in the throwaway repo", ok, out)
        run(["git", "add", "-A"], tmp)
        run(env_git + ["commit", "-q", "-m", "regenerated state", "--allow-empty"], tmp)

        ok, out = run(gen + ["--check"], tmp, expect=0)
        check("--check PASSES on the commit containing the regenerated state "
              "(commit-boundary convergence)", ok, out)

        ok, out = run(gen + ["--check"], tmp, expect=0)
        check("--check remains green with no further changes (idempotence)", ok, out)

        # tamper control: a declared source input
        probe = os.path.join(tmp, "docs", "glossary.md")
        with io.open(probe, "a", encoding="utf-8") as f:
            f.write("\nconvergence-tamper-probe\n")
        ok, out = run(gen + ["--check"], tmp, expect=1)
        check("--check FAILS after tampering with a declared source input", ok, out)
        run(["git", "checkout", "--", "docs/glossary.md"], tmp)
        ok, _ = run(gen + ["--check"], tmp, expect=0)
        check("--check recovers after the tamper is reverted", ok)

        # excluded-path control: an artifact mutation must not trip the digest
        excluded_probe = os.path.join(tmp, "docs", "provenance", "RELEASE-MANIFEST.sha256")
        if os.path.exists(excluded_probe):
            with io.open(excluded_probe, "a", encoding="utf-8") as f:
                f.write("# excluded-path probe\n")
            ok, out = run(gen + ["--check"], tmp, expect=0)
            check("--check ignores mutations of digest-excluded generated files "
                  "(they carry their own checks)", ok, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
