#!/usr/bin/env python3
"""Verify and replay the two frozen exact-control suites. No network access."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

manifest_path = ROOT / 'BUNDLE_MANIFEST.json'
manifest = json.loads(manifest_path.read_text())

def verify_bundle():
    for rel, row in manifest['files'].items():
        path = ROOT / rel
        check(path.is_file(), 'Missing payload: ' + rel)
        check(path.stat().st_size == row['bytes'], 'Length mismatch: ' + rel)
        check(sha(path) == row['sha256'], 'Hash mismatch: ' + rel)

verify_bundle()
author_root = ROOT / 'channel-natural-repair-20261009'
review_root = ROOT / 'channel-natural-repair-review-20261009'
author_manifest = json.loads((author_root / 'MANIFEST.json').read_text())
for rel, row in author_manifest['files'].items():
    path = author_root / rel
    check(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'Author manifest mismatch: ' + rel)
seal = json.loads((review_root / 'REVIEW_SEAL.json').read_text())
for section in ['author_artifacts', 'unchanged_predecessor_inputs', 'review_artifacts']:
    for rel, digest in seal[section].items():
        check(sha(ROOT / rel) == digest, 'Review seal mismatch: ' + rel)
provenance = json.loads((ROOT / 'INPUT_PROVENANCE.json').read_text())
for rel, digest in provenance['originals'].items():
    check(sha(ROOT / rel) == digest, 'Original-byte mismatch: ' + rel)

import sympy
suites = [
    ('author', author_root / 'verify.py', author_root / 'CHECK_RESULTS.json', 61),
    ('independent', review_root / 'independent_controls.py', review_root / 'INDEPENDENT_CONTROLS.json', 43),
]
results = []
for name, script, output, expected in suites:
    before = sha(output)
    run = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True)
    check(run.returncode == 0, name + ' failed: ' + run.stdout + run.stderr)
    data = json.loads(output.read_text())
    check(data['status'] == 'PASS' and data['check_count'] == expected, name + ' unexpected result')
    check(sha(output) == before, name + ' result is not byte-identical')
    results.append({'suite': name, 'passed': True, 'checks': expected, 'result_byte_identical': True, 'stdout': json.loads(run.stdout)})
verify_bundle()
print(json.dumps({
    'replay_verified': True,
    'payload_files_verified': len(manifest['files']),
    'bundle_manifest_sha256': sha(manifest_path),
    'author_result_sha256': sha(author_root / 'RESULT.md'),
    'review_seal_sha256': sha(review_root / 'REVIEW_SEAL.json'),
    'python_version': platform.python_version(),
    'sympy_version': sympy.__version__,
    'all_payload_bytes_unchanged': True,
    'suites': results,
}, indent=2))
