#!/usr/bin/env python3
"""Check explicitly inventoried continuation files and the exact v3 dependency."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

sha = lambda b: hashlib.sha256(b).hexdigest()

def checked(root, name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    dest = root / p
    assert dest.resolve().is_relative_to(root.resolve()) and not dest.is_symlink()
    return dest

def verify_index(root, expected_sha=None):
    raw = (root / 'ARCHIVE_CONTENTS.json').read_bytes()
    if expected_sha: assert sha(raw) == expected_sha
    records = json.loads(raw)['files']
    assert len({r['path'] for r in records}) == len(records)
    for r in records:
        data = checked(root, r['path']).read_bytes()
        assert len(data) == r['bytes'] and sha(data) == r['sha256'], r['path']
    return len(records)

def verify(root, v3):
    count = verify_index(root)
    contract = json.loads((root / 'V3_REUSE_CONTRACT.json').read_text())
    prior_count = verify_index(v3, contract['v3_index_sha256'])
    prior_receipt = v3 / contract['v3_prerequisite_receipt']
    assert sha(prior_receipt.read_bytes()) == contract['v3_prerequisite_receipt_sha256']
    inventory = json.loads((root / 'PRESERVED_SOURCES.json').read_text())
    for r in inventory['files']:
        data = checked(root, r['path']).read_bytes()
        assert len(data) == r['bytes'] and sha(data) == r['sha256']
    plan = json.loads((root / 'REPLAY_PLAN.json').read_text())
    assert plan['all_component_reviews_final'] is True
    for r in plan['final_bindings']:
        assert sha(checked(root, r['path']).read_bytes()) == r['sha256']
    return {'status': 'PASS', 'archive_indexed_files': count, 'preserved_source_files': len(inventory['files']),
            'v3_indexed_files_verified': prior_count, 'all_component_reviews_final_bound': True}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--v3', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(Path(__file__).resolve().parent, args.v3.resolve()), indent=2))
