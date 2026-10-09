#!/usr/bin/env python3
"""Verify bound inputs and replay only review-local copies of exact controls."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt = json.loads((ROOT / 'REVIEW_RECEIPT.json').read_text())

def verify_bound():
    for record in receipt['bound_files']:
        path = ROOT / record['path']
        assert path.is_file(), f"Missing bound file: {record['path']}"
        assert sha(path) == record['sha256'], f"Changed bound file: {record['path']}"

verify_bound()
results = {}
for label, source, output, expected in [
    ('independent', ROOT / 'independent_controls.py', 'INDEPENDENT_CONTROLS.json', ROOT / 'INDEPENDENT_CONTROLS.json'),
    ('author', ROOT / 'author_replay' / 'exact_controls.py', 'results/exact_controls.json', ROOT / 'author_replay' / 'results' / 'exact_controls.json'),
]:
    directory = ROOT / 'verification_replay' / label
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'results').mkdir(exist_ok=True)
    script = directory / source.name
    shutil.copyfile(source, script)
    proc = subprocess.run([sys.executable, str(script)], cwd=directory, check=True,
                          text=True, capture_output=True, timeout=90)
    (directory / 'replay.log').write_text(proc.stdout)
    actual = directory / output
    assert actual.read_bytes() == expected.read_bytes(), f'{label} replay mismatch'
    results[label] = json.loads(actual.read_text())
verify_bound()

out = {
    'status': 'PASS',
    'receipt_sha256': sha(ROOT / 'REVIEW_RECEIPT.json'),
    'bound_file_count': len(receipt['bound_files']),
    'independent_assertions': results['independent']['total_assertions'],
    'author_assertions': results['author']['assertions'],
    'replays_byte_identical': True,
    'sources_unchanged_before_and_after_replay': True,
    'scope': 'Scoped mathematical review verification only; no integration, release, physical validation or T20 closure.'
}
(ROOT / 'VERIFICATION.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, indent=2, sort_keys=True))
