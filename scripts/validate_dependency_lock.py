#!/usr/bin/env python3
"""Dependency-lock validator (R6, audit finding B6).

Checks, deterministically and offline:
  1. requirements-ci.lock.txt exists and every non-comment line is an EXACT
     `name==version` pin (no ranges, no unpinned names);
  2. every third-party package imported by scripts/, experiments/, and
     terminology packet code is represented in the lock (by import->distribution
     mapping);
  3. the workflow installs from the lock and has no other pip install path;
  4. the lock's honesty note states it is a version lock (not hash-locked) and
     claims reproducibility only under the recorded toolchain;
  5. the effective installed versions of the locked packages are importable and
     recorded to stdout (the build report surface).
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

IMPORT_TO_DIST = {"yaml": "PyYAML", "jsonschema": "jsonschema", "typst": "typst",
                  "markdown_it": "markdown-it-py", "pypdf": "pypdf",
                  "referencing": "referencing", "attrs": "attrs", "attr": "attrs",
                  "rpds": "rpds-py", "mdurl": "mdurl",
                  "jsonschema_specifications": "jsonschema-specifications"}


def scan_repository_imports(root):
    """Return top-level imports from the repository trees governed by the lock."""
    used = set()
    for tree in ("scripts", "experiments", "terminology"):
        for base, dirs, fns in os.walk(os.path.join(root, tree)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in fns:
                if not fn.endswith(".py"):
                    continue
                with io.open(os.path.join(base, fn), encoding="utf-8") as stream:
                    src = stream.read()
                for match in re.finditer(
                        r"^\s*(?:import\s+([A-Za-z_][A-Za-z0-9_]*)"
                        r"|from\s+([A-Za-z_][A-Za-z0-9_]*)\s+import\s)", src, re.M):
                    used.add(match.group(1) or match.group(2))
    return used


def find_local_modules(root):
    """Return repository-local Python module basenames excluded from lock ownership."""
    return {os.path.splitext(os.path.basename(path))[0]
            for path in glob.glob(os.path.join(str(root), "**", "*.py"), recursive=True)}


def classify_imports(used, local_modules, import_to_dist=None, stdlib_modules=None):
    """Partition imported names by authoritative Python/distribution ownership."""
    import_to_dist = IMPORT_TO_DIST if import_to_dist is None else import_to_dist
    stdlib_modules = sys.stdlib_module_names if stdlib_modules is None else stdlib_modules
    result = {name: set() for name in ("stdlib", "third_party", "local", "unmapped")}
    for module in used:
        if module in stdlib_modules:
            result["stdlib"].add(module)
        elif module in import_to_dist:
            result["third_party"].add(module)
        elif module in local_modules:
            result["local"].add(module)
        else:
            result["unmapped"].add(module)
    return result


def find_missing_distributions(third_party, pins, import_to_dist=None):
    """Return mapped distributions used by code but absent from exact pins."""
    import_to_dist = IMPORT_TO_DIST if import_to_dist is None else import_to_dist
    return sorted({import_to_dist[module] for module in third_party
                   if import_to_dist[module] not in pins})


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    lock_path = os.path.join(ROOT, "requirements-ci.lock.txt")
    check("lock file exists", os.path.exists(lock_path))
    text = io.open(lock_path, encoding="utf-8").read()
    pins = {}
    bad = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)==([A-Za-z0-9_.\-]+)$", ln)
        if m:
            pins[m.group(1)] = m.group(2)
        else:
            bad.append(ln)
    check("every lock line is an exact name==version pin", not bad, str(bad[:3]))

    # imports actually used by repository code
    used = scan_repository_imports(ROOT)
    classified = classify_imports(used, find_local_modules(ROOT))
    third_party = classified["third_party"]
    unmapped = sorted(classified["unmapped"])
    check("no unmapped third-party import (extend IMPORT_TO_DIST when adding deps)",
          not unmapped, str(unmapped[:5]))
    missing = find_missing_distributions(third_party, pins)
    check("every imported third-party package is represented in the lock",
          not missing, str(missing))

    wf = io.open(os.path.join(ROOT, ".github", "workflows", "validate.yml"),
                 encoding="utf-8").read()
    check("workflow installs from the lock",
          "pip install --quiet -r requirements-ci.lock.txt" in wf)
    others = [ln.strip() for ln in wf.splitlines()
              if "pip install" in ln and "requirements-ci.lock.txt" not in ln]
    check("no duplicate unpinned install path in the workflow", not others, str(others))

    folded = re.sub(r"\s+", " ", text.replace("#", " "))
    check("lock states its honesty note (version lock; recorded toolchain only)",
          "hash lock" in folded and "recorded toolchain" in folded)

    import importlib
    effective = {}
    for mod, dist in sorted(IMPORT_TO_DIST.items()):
        if dist not in pins or mod in ("attr", "rpds", "mdurl", "jsonschema_specifications"):
            continue
        try:
            m = importlib.import_module(mod)
            effective[dist] = getattr(m, "__version__", "(no __version__)")
        except ImportError as e:
            check("locked package %s importable" % dist, False, str(e))
    print("effective versions (build report): %s" % effective)
    print("python: %s" % sys.version.split()[0])

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
