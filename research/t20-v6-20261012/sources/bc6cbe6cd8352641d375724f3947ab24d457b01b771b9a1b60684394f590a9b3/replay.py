"""Replay compact mathematical controls, without fetching omitted source witnesses."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
ROOT = Path(__file__).resolve().parent

def verify(manifest, base):
    obj = json.loads(manifest.read_text())
    for row in obj['files']:
        data = (base / row['path']).read_bytes()
        assert len(data) == row['bytes'], row['path']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
    return len(obj['files'])

count = verify(ROOT / 'BUNDLE_MANIFEST.json', ROOT)
verify(ROOT / 'source-audit-revision-20261010/MANIFEST.json', ROOT / 'source-audit-revision-20261010')
verify(ROOT / 'audit-aware-revision-review-20261010/MANIFEST.json', ROOT / 'audit-aware-revision-review-20261010')
verify(ROOT / 'audit-occurrence-review-20261010/MANIFEST.json', ROOT / 'audit-occurrence-review-20261010')
jobs = [
    ('.', 'check_occurrence_algebra_only.py', 'OCCURRENCE_ALGEBRA_ONLY_RESULTS.json'),
    ('source-audit-revision-20261010', 'verify.py', 'CONTROL_RESULTS.json'),
    ('source-audit-revision-20261010', 'companions/check_triple_interaction.py', 'TRIPLE_CONTROL_RESULTS.json'),
    ('audit-aware-correction-root-20261010', 'check_zero_audit.py', 'ZERO_AUDIT_CHECKS.json'),
    ('audit-aware-correction-root-20261010', 'check_triple_interaction.py', 'TRIPLE_CHECKS.json'),
    ('audit-aware-revision-review-20261010', 'independent_controls.py', 'INDEPENDENT_RESULTS.json'),
]
rows = []
for directory, script, expected in jobs:
    base = ROOT / directory
    run = subprocess.run([sys.executable, script], cwd=base, text=True, capture_output=True, check=True)
    assert json.loads(run.stdout) == json.loads((base / expected).read_text()), (directory, script)
    rows.append({'directory': directory, 'script': script, 'status': 'PASS', 'recorded_output_equal': True})
assert count == verify(ROOT / 'BUNDLE_MANIFEST.json', ROOT)
print(json.dumps({'status': 'PASS', 'manifest_files': count, 'exact_replays': rows,
                  'preserved_omitted_source_check': 'The original review-time receipts are retained. verify_snapshot.py and the occurrence review combined custody/algebra check are not rerun because their original witnesses are intentionally omitted. The separate occurrence algebra-only replay makes no custody claim.',
                  'scope': 'Compact exact-control replay and byte preservation only. No empirical, psychological, formal-kernel, protected-integration, or T20-closure claim.'}, indent=2))
