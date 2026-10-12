#!/usr/bin/env python3
"""Verify explicit inventory paths only, without traversing source trees."""
import hashlib
import json
from pathlib import Path, PurePosixPath

sha = lambda b: hashlib.sha256(b).hexdigest()

def safe_path(root, name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    out = root / p
    assert out.resolve().is_relative_to(root.resolve()) and not out.is_symlink(), name
    return out

def verify(root):
    index = json.loads((root / 'ARCHIVE_CONTENTS.json').read_text())
    names = [r['path'] for r in index['files']]
    assert len(names) == len(set(names))
    for record in index['files']:
        data = safe_path(root, record['path']).read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], record['path']
    sources = json.loads((root / 'PRESERVED_SOURCES.json').read_text())
    for record in sources['files']:
        data = safe_path(root, record['path']).read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], record['path']
    plan = json.loads((root / 'REPLAY_PLAN.json').read_text())
    for review in plan['reviews']:
        assert sha((root / review['directory'] / 'REVIEW.md').read_bytes()) == review['review_sha256']
        assert sha((root / review['directory'] / 'MANIFEST.json').read_bytes()) == review['manifest_sha256']
        assert sha((root / review['accepted_report']).read_bytes()) == review['accepted_report_sha256']
        bindings = json.loads((root / review['directory'] / 'SNAPSHOT_BINDINGS.json').read_text())
        for name, record in bindings['files'].items():
            data = safe_path(root, name).read_bytes()
            assert len(data) == record['bytes'] and sha(data) == record['sha256'], name
    return {'status': 'PASS', 'indexed_files': len(names), 'preserved_original_files': len(sources['files']),
            'final_independent_reviews_bound': len(plan['reviews']), 'scope': plan['scope']}

if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2))
