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
import ast
import glob
import hashlib
import io
import os
from pathlib import Path
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

IMPORT_TO_DIST = {"yaml": "PyYAML", "jsonschema": "jsonschema", "typst": "typst",
                  "markdown_it": "markdown-it-py", "pypdf": "pypdf",
                  "referencing": "referencing", "attrs": "attrs", "attr": "attrs",
                  "rpds": "rpds-py", "mdurl": "mdurl",
                  "jsonschema_specifications": "jsonschema-specifications"}
POPPLER_LOCK_RELATIVE = "publication/poppler-linux-64.explicit.txt"
MICROMAMBA_URL = (
    "https://github.com/mamba-org/micromamba-releases/releases/"
    "download/2.8.1-0/micromamba-linux-64"
)
MICROMAMBA_SHA256 = (
    "9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82"
)
POPPLER_URL = (
    "https://conda.anaconda.org/conda-forge/linux-64/"
    "poppler-25.07.0-h13eef12_1.conda"
)
POPPLER_SHA256 = (
    "a45c9c35808c44d817209af859d2e9d90b89c72f8cd8fcea20163ee774583ed8"
)

# These exact research payloads use their own Python 3.12 environments. They
# are inspected source, not imports of the Python 3.11 repository CI runtime.
# New bytes or an unrelated import cannot borrow this separate lock scope.
RESEARCH_SOURCE_LOCKS = {
    '41b4c6a14166306b9f593728df115892a3f0a64aa4c153741b9579c14b74270d': {
        'fit_bfgs.py': 'cd6f203e2e79f6113de3cef2e4d98926c3f75fe374ca04b3ea73aeee02301a02',
        'fit_checked.py': 'ebefc609d09bf68296e5a1c5392064effaf4c4d462b82cbb451b1e93340ec376',
        'reanalyse.py': '20110e73fd822e21651064578946cdf910edc493c973953b2c7d1bb74481dd94',
        'test_package.py': 'afb1ba14ecbbf193f07ac81f985be30535abf9771387813e9dbd0bbbfc72fb50',
        'validate.py': '7d9a4c8d071e2591c8d4568c88c277ab61834e52df21500a1367efb2ac7e060a',
    },
    '65b97f7db87e4cdcb0f4157240cfece5b48363b3e6a18fdccf72d6528ebcbf85': {
        'analysis_core.py': '84d819256b564b4acc8def4602d6882cebfd15417f44e8f9c3b5005d459f8875',
        'run_reanalysis.py': '86bc29fab24a54e5a09efce1a7696b9491f28b95cd23ed4ecee89e076e524baf',
        'estimate_contrasts.py': 'f9b3153dcad9a21842796a09df7966b26c1348f0785f3863e09177b28f6a3aa3',
        'batch_sensitivity.py': '0e17bc10f0e52c199fece92cd649c6006e7e7b5b9c94dce834b6410d288ab8d0',
        'manipulation_checks.py': 'a67a96c885051d5639869b7fe01d5f07a00a8269f50ee9f48f9ec06e8b55a288',
        'test_analysis_core.py': 'a1be6c6b5a84eeb7d3417fdc8713fcd0d7982d7358ddf0cc78079b2f0ba60a6a',
    },
}


def separately_pinned_research(root):
    store = Path(root) / 'experiments/orthemology-v5-successors/source-store'
    owned = {}
    for lock_hash, sources in RESEARCH_SOURCE_LOCKS.items():
        lock = store / lock_hash / 'requirements.txt'
        paths = {store / digest / name: digest for name, digest in sources.items()}
        if not lock.exists() and not any(path.exists() for path in paths):
            continue
        try:
            data = lock.read_bytes()
            if hashlib.sha256(data).hexdigest() != lock_hash:
                raise ValueError('Changed separate research dependency lock')
            pins = set()
            for line in data.decode('utf-8').splitlines():
                match = re.fullmatch(r'([A-Za-z0-9_]+)==([0-9][A-Za-z0-9.]+)', line)
                if not match:
                    raise ValueError('Research dependency is not exactly pinned')
                pins.add(match[1])
            for path, digest in paths.items():
                if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    raise ValueError('Changed separately pinned research source')
                owned[os.path.normpath(str(path))] = pins
        except OSError as error:
            raise ValueError('Missing separately pinned research source or lock') from error
    return owned


def scan_repository_imports(root):
    """Return top-level imports from the repository trees governed by the lock."""
    used = set()
    research = separately_pinned_research(root)
    for tree in ("scripts", "experiments", "terminology"):
        for base, dirs, fns in os.walk(os.path.join(root, tree)):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fn in fns:
                if not fn.endswith(".py"):
                    continue
                with io.open(os.path.join(base, fn), encoding="utf-8") as stream:
                    src = stream.read()
                # Generated foreign-language source inside strings is not a
                # Python dependency. Parse errors must remain failures.
                file_imports = set()
                for node in ast.walk(ast.parse(src, filename=os.path.join(base, fn))):
                    if isinstance(node, ast.Import):
                        file_imports.update(alias.name.split(".")[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                        file_imports.add(node.module.split(".")[0])
                used.update(file_imports - research.get(os.path.normpath(os.path.join(base, fn)), set()))
    return used


def find_local_modules(root):
    """Return repository-local modules and top-level namespace packages."""
    paths = glob.glob(os.path.join(str(root), "**", "*.py"), recursive=True)
    modules = {os.path.splitext(os.path.basename(path))[0] for path in paths}
    for path in paths:
        relative_parts = os.path.relpath(path, root).split(os.sep)
        if len(relative_parts) > 1 and relative_parts[0].isidentifier():
            modules.add(relative_parts[0])
    return modules


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


def parse_explicit_package_lock(text):
    """Parse a single-platform conda explicit lock with SHA-256 URL fragments."""
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines or lines[0] != "@EXPLICIT":
        raise ValueError("explicit package lock must begin with @EXPLICIT")
    entries = []
    seen_urls = set()
    seen_filenames = set()
    pattern = re.compile(
        r"^(https://conda\.anaconda\.org/conda-forge/"
        r"(?:linux-64|noarch)/([^#]+))#([0-9a-f]{64})$"
    )
    for line in lines[1:]:
        match = pattern.fullmatch(line)
        if not match:
            raise ValueError("malformed or non-SHA256 explicit package row: %s" % line)
        url, filename, sha256 = match.groups()
        if url in seen_urls or filename in seen_filenames:
            raise ValueError("duplicate explicit package row: %s" % filename)
        seen_urls.add(url)
        seen_filenames.add(filename)
        entries.append(
            {"filename": filename, "sha256": sha256, "url": url}
        )
    if not entries:
        raise ValueError("explicit package lock contains no packages")
    return entries


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
    provisioner = io.open(
        os.path.join(ROOT, "scripts", "provision_ci_infrastructure.py"),
        encoding="utf-8",
    ).read()
    check("workflow installs from the lock",
          "pip install --quiet -r requirements-ci.lock.txt" in wf)
    others = [ln.strip() for ln in wf.splitlines()
              if "pip install" in ln and "requirements-ci.lock.txt" not in ln]
    check("no duplicate unpinned install path in the workflow", not others, str(others))

    package_lock_path = os.path.join(ROOT, *POPPLER_LOCK_RELATIVE.split("/"))
    package_lock_entries = []
    package_lock_error = ""
    try:
        package_lock_entries = parse_explicit_package_lock(
            io.open(package_lock_path, encoding="utf-8").read()
        )
    except (OSError, ValueError) as error:
        package_lock_error = str(error)
    check(
        "CI Poppler lock is a complete SHA256 explicit environment",
        not package_lock_error and len(package_lock_entries) == 61,
        package_lock_error or ("rows=%d" % len(package_lock_entries)),
    )
    expected_poppler = {
        "filename": os.path.basename(POPPLER_URL),
        "sha256": POPPLER_SHA256,
        "url": POPPLER_URL,
    }
    check(
        "CI Poppler lock contains the exact 25.07.0 linux-64 build",
        [entry for entry in package_lock_entries
         if entry["filename"].startswith("poppler-25.07.0-")] == [expected_poppler],
    )
    workflow_literals = (
        'python-version: "3.11.9"',
        MICROMAMBA_URL,
        MICROMAMBA_SHA256,
        "bc1b26e6a386d853fd6e07225bb3b0b7a17a2a19b2ed51b5aaacedb3597ec6c3",
        "poppler-linux-64.explicit.txt",
        '"create"',
        '"--no-rc"',
        (
            "texlive/texlive@sha256:"
            "ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51"
        ),
        (
            "sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1"
        ),
        "linux/amd64",
        '("pdfinfo", "pdftoppm", "pdffonts")',
        '[executable, "-v"]',
    )
    missing_workflow_literals = [
        literal for literal in workflow_literals
        if literal not in (wf + "\n" + provisioner)
    ]
    check(
        "workflow provisions and probes exact PDF infrastructure",
        "run: python scripts/provision_ci_infrastructure.py" in wf
        and not missing_workflow_literals,
        str(missing_workflow_literals),
    )
    check(
        "CI verifies infrastructure SHA256 values before executing micromamba",
        provisioner.index("observed = sha256_file(download)")
        < provisioner.index("str(micromamba),")
        and provisioner.index("observed_lock = sha256_file(POPPLER_LOCK)")
        < provisioner.index("str(micromamba),"),
    )
    check(
        "workflow does not install an unpinned system Poppler or solve packages",
        "apt-get install" not in wf
        and "conda install" not in wf
        and "create-args:" not in wf,
    )

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
