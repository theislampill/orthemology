"""Check included bytes and receipt targets; do not pretend excluded sources are present."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(path, digest, size=None):
    p = ROOT / path
    assert p.is_file() and not p.is_symlink(), path
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, path
    assert size is None or len(data) == size, path


sealed = []
for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
    digest, path = line.split('  ', 1)
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    check(path, digest)
    sealed.append(path)
assert len(sealed) == len(set(sealed))
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
assert actual == set(sealed) | {'SHA256SUMS'}
for path in actual:
    assert Path(path).suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.pdf', '.html'}
    assert not any(word in Path(path).name.lower() for word in ('ocr', 'layout', 'apparatus'))

inventory = json.loads((ROOT / 'DELIVERY_MANIFEST.json').read_text())
for row in inventory['files']:
    check(row['path'], row['sha256'], row['bytes'])
assert {r['path'] for r in inventory['files']} | {'DELIVERY_MANIFEST.json'} == set(sealed)

copies = json.loads((ROOT / 'COPY_RECORD.json').read_text())
relocated = {r['source_path']: r['path'] for r in copies['files']}
for row in copies['files']:
    check(row['path'], row['sha256'], row['bytes'])
for row in copies['cross_receipt_targets']:
    check(row['target'], row['sha256'], row['bytes'])

external = {r['path']: r for r in json.loads((ROOT / 'EXTERNAL_WITNESSES.json').read_text())['witnesses']}
included_rows = excluded_rows = 0
review_dir = ROOT / 'affirmative-source-review-20261009'
for name in ('INPUT_BINDINGS.json', 'TOKEN_FORCE_BINDINGS.json'):
    for row in json.loads((review_dir / name).read_text())['entries']:
        source_path = row['path']
        target = relocated.get(source_path, source_path)
        if (ROOT / target).is_file():
            check(target, row['sha256'], row['bytes'])
            included_rows += 1
        else:
            witness = external[source_path]
            assert witness['sha256'] == row['sha256'] and witness['bytes'] == row['bytes']
            excluded_rows += 1
for name in ('SHA256SUMS', 'TOKEN_FORCE_SHA256SUMS'):
    for line in (review_dir / name).read_text().splitlines():
        digest, path = line.split('  ', 1)
        check('affirmative-source-review-20261009/' + path, digest)
for row in json.loads((ROOT / 'PROJECTION_BINDINGS.json').read_text())['projections']:
    check(row['path'], row['sha256'], row['bytes'])
    assert row['source_sha256'] == external[row['source_path']]['sha256']

print(json.dumps({
    'status': 'PASS',
    'sealed_payload_files': len(sealed),
    'all_zip_files': len(actual),
    'byte_exact_copied_records': len(copies['files']),
    'cleaned_public_domain_projections': 2,
    'exact_reviewed_report_targets': len(copies['cross_receipt_targets']),
    'review_binding_rows_with_included_bytes': included_rows,
    'review_binding_rows_with_external_metadata_only': excluded_rows,
    'modern_images_pdfs_html_ocr_apparatus_files_included': 0,
    'limits': 'Integrity and receipt binding only. External metadata is not a replay of excluded '
              'witness bytes, renewed source reading, independent historical authentication, '
              'mathematical certification, repository authority, or T20 closure.'
}, indent=2))
