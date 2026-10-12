#!/usr/bin/env python3
"""Read-only integrity checks. Hash matches are not mathematical certification."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def check_file(path, item):
    assert path.is_file() and not path.is_symlink(), str(path)
    raw = path.read_bytes()
    assert len(raw) == item['bytes'], ('size', str(path))
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], ('sha256', str(path))

def main():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    expected = {item['path'] for item in manifest['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == expected | {'MANIFEST.json'}, ('inventory', actual ^ (expected | {'MANIFEST.json'}))
    for item in manifest['files']:
        check_file(ROOT/item['path'], item)
    sources = json.loads((ROOT/'SOURCE_ROOT_HASHES.json').read_text())['files']
    for item in sources:
        check_file(ROOT/item['archive_path'], item)
    bindings = json.loads((ROOT/'INPUT_RESOLUTION.json').read_text())['bindings']
    for item in bindings:
        check_file(ROOT/item['archive_path'], item)
    ws = ROOT/'workspace'
    manifests = [
        'bayes-feasibility-compatibility-20261010/MANIFEST.json',
        'measure-bayes-face-transport-20261010/MANIFEST.json',
        'constrained-learning-possibility-20261010/MANIFEST.json',
        'bayes-feasibility-review-20261010/MANIFEST.json',
        'bayes-feasibility-review-20261010/FINAL_ADDENDUM_MANIFEST.json',
        'measure-bayes-face-review-20261010/MANIFEST.json',
        'constrained-learning-review-20261010/MANIFEST.json',
        'constrained-learning-review-20261010/REVIEWED_EXACTFILES.json',
    ]
    checked = 0
    for name in manifests:
        path = ws/name
        for item in json.loads(path.read_text())['files']:
            check_file(path.parent/item['path'], item)
            checked += 1
    finite = ws/'bayes-feasibility-compatibility-20261010'
    old = finite/'RESULT.pre-convexity-qualification.md'
    current = finite/'RESULT.md'
    change = json.loads((finite/'CORRECTION_RECORD.json').read_text())
    assert hashlib.sha256(old.read_bytes()).hexdigest() == change['old_result_sha256']
    assert hashlib.sha256(current.read_bytes()).hexdigest() == change['new_result_sha256']
    before, after = change['before'].encode(), change['after'].encode()
    assert old.read_bytes().count(before) == 1
    assert old.read_bytes().replace(before, after) == current.read_bytes()
    review = ws/'bayes-feasibility-review-20261010'
    assert old.read_bytes() == (review/'reviewed_target/RESULT.md').read_bytes()
    assert current.read_bytes() == (review/'final_target/RESULT.md').read_bytes()
    assert (finite/'MANIFEST.pre-convexity-qualification.json').read_bytes() == (review/'reviewed_target/MANIFEST.json').read_bytes()
    for item in json.loads((finite/'MANIFEST.pre-convexity-qualification.json').read_text())['files']:
        target = old if item['path'] == 'RESULT.md' else finite/item['path']
        check_file(target, item)
    # Independently recompute retained Git blob identifiers for the two direct
    # finite-packet source texts. This is content identity, not remote auth.
    blob_checks = 0
    for item in json.loads((finite/'INPUT_BINDINGS.json').read_text())['local_inputs']:
        if 'git_blob_sha' in item:
            raw = (ws/item['path']).read_bytes()
            observed = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            assert observed == item['git_blob_sha']
            blob_checks += 1
    print(json.dumps({'status':'PASS','archive_files_checked':len(expected),
                      'root_source_files_checked':len(sources),
                      'direct_input_bindings_checked':len(bindings),
                      'original_manifest_entries_checked':checked,
                      'git_blob_ids_checked':blob_checks,
                      'correction_exact_single_replacement':True,
                      'scope':'Integrity and version identity only; not theorem certification.'}, sort_keys=True))

if __name__ == '__main__':
    main()
