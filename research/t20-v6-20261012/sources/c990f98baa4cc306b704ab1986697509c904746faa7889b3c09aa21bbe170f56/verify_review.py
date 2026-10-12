"""Check the exact independent-review bindings and retained replay agreement."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((root / 'MANIFEST.json').read_text())
for item in manifest['files']:
    path = root / item['path']
    assert path.stat().st_size == item['bytes'], item['path']
    assert sha(path) == item['sha256'], item['path']

receipt = json.loads((root / 'RECEIPT.json').read_text())
checked_external = 0
for item in receipt['reviewed_input_bindings']:
    path = root.parent / item['path']
    if item.get('required_in_replay', False):
        assert path.exists(), item['path']
    if path.exists():
        assert path.stat().st_size == item['bytes'], item['path']
        assert sha(path) == item['sha256'], item['path']
        checked_external += 1

author = root.parent / 'exponential-tail-effectivity-20261010'
for original, replay in [
    ('CONTROLS.json', 'author_rerun.json'),
    ('RECURSIVE_ORACLE_CONTROLS.json', 'author_recursive_rerun.json'),
]:
    if (author / original).exists():
        assert json.loads((author / original).read_text()) == json.loads((root / replay).read_text())
assert json.loads((root / 'verification.txt').read_text())['status'] == 'PASS'
assert json.loads((root / 'author_manifest_rerun.json').read_text())['status'] == 'PASS'
print(json.dumps({'status':'PASS','review_files_bound':len(manifest['files']),
                  'available_reviewed_inputs_bound':checked_external,
                  'scope':'Identity and retained finite-control agreement only; ordinary proof verdict is in REVIEW.md.'},indent=2))
