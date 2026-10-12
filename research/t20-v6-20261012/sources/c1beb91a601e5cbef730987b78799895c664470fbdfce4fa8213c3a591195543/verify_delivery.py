#!/usr/bin/env python3
"""Check delivery bytes and declared omissions; this is not mathematical verification."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = json.loads((ROOT / 'DELIVERY_MANIFEST.json').read_text())
    expected = {row['path']: row for row in manifest['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    if actual != set(expected) | {'DELIVERY_MANIFEST.json'}:
        raise RuntimeError('Delivery inventory mismatch: missing=' + str(sorted(set(expected)-actual)) + ' extra=' + str(sorted(actual-set(expected)-{'DELIVERY_MANIFEST.json'})))
    for rel, row in expected.items():
        p = ROOT / rel
        if p.is_symlink() or p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
            raise RuntimeError('Delivery byte mismatch: ' + rel)
    origin = json.loads((ROOT / 'ORIGIN_SNAPSHOT.json').read_text())
    omitted = {row['path']: row for row in json.loads((ROOT / 'OMISSIONS.json').read_text())['files']}
    included = 0
    for row in origin['files']:
        rel = row['path']
        if rel in omitted:
            if (ROOT / rel).exists() or row['sha256'] != omitted[rel]['sha256'] or row['bytes'] != omitted[rel]['bytes']:
                raise RuntimeError('Omission mismatch: ' + rel)
        else:
            if rel not in expected or any(row[k] != expected[rel][k] for k in ['bytes','sha256']):
                raise RuntimeError('Original-byte mismatch: ' + rel)
            included += 1
    if set(omitted) - {row['path'] for row in origin['files']}:
        raise RuntimeError('Omission not bound to origin snapshot')
    author = ROOT/'fibrewise-split-correction-20261011'
    review = ROOT/'fibrewise-split-independent-review-20261011'
    bound = json.loads((review/'BINDINGS.json').read_text())
    if digest(author/'AUTHOR_FREEZE.json') != bound['author_freeze_sha256']:
        raise RuntimeError('Reviewer-to-author freeze binding mismatch')
    present_binding_checks = 1
    declared_omitted_bindings = 0
    for row in json.loads((author/'AUTHOR_FREEZE.json').read_text())['files']:
        rel = str((author/row['path']).relative_to(ROOT))
        if rel in omitted:
            if any(omitted[rel][k] != row[k] for k in ['sha256','bytes']):
                raise RuntimeError('Author manifest omission binding mismatch: '+rel)
            declared_omitted_bindings += 1
        else:
            if any(expected[rel][k] != row[k] for k in ['sha256','bytes']):
                raise RuntimeError('Author manifest present binding mismatch: '+rel)
            present_binding_checks += 1
    for row in json.loads((author/'INPUT_BINDINGS.json').read_text()):
        if digest(author/row['snapshot']) != row['sha256']:
            raise RuntimeError('Predecessor snapshot binding mismatch')
        present_binding_checks += 1
    for filename,key in [('RESULT.md','author_result_sha256'),('gaussian_step.py','implementation_sha256')]:
        if digest(author/filename) != bound[key]:
            raise RuntimeError('Reviewed key identity mismatch: '+filename)
        present_binding_checks += 1
    for row in json.loads((review/'FREEZE.json').read_text())['files']:
        rel = str((review/row['path']).relative_to(ROOT))
        if any(expected[rel][k] != row[k] for k in ['sha256','bytes']):
            raise RuntimeError('Reviewer manifest binding mismatch: '+rel)
    return {'present_reviewer_binding_checks':present_binding_checks, 'declared_but_absent_source_bindings':declared_omitted_bindings, 'status':'PASS', 'classification':'byte integrity only', 'delivery_files':len(expected), 'preserved_original_files':included, 'omitted_source_body_files':len(omitted), 'manifest_sha256':digest(ROOT/'DELIVERY_MANIFEST.json')}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
