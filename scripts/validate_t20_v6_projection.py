#!/usr/bin/env python3
"""Validate the new public object, independently of the private package PASS.

All registered bodies are checked regardless of suffix. This is source integrity,
publication boundary and current-record binding, not mathematical acceptance.
"""
from __future__ import annotations
import collections
import hashlib
import json
import pathlib
import re
import sys
import subprocess
from functools import lru_cache

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'research/t20-v6-20261012'
MANIFEST = PREFIX + '/PUBLIC_PROJECTION_MANIFEST.json'
BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
SHA = re.compile(r'[0-9a-f]{64}\Z')
# Actual locators have a concrete component, unlike regex-only detection fixtures.
PRIVATE = re.compile(r'(?<![A-Za-z0-9:/])/(?:workspace|mnt/(?:data|c)|home|tmp|Users|root|opt|usr/local)/[A-Za-z0-9_.-][^\s`"\'<>\[\]{}\\|]*|(?<![A-Za-z0-9])[A-Za-z]:\\(?:\\)?(?:Users|workspace)\\')
UUID = re.compile(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b', re.I)
PUBLIC_CITATION_UUIDS = {
    'fa8a2dceb11330669cf39dbb5dd02ca0b58b949d699b61bfd5eb3d53eefe9da8': 'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8',
    '7f12edad1756dcfb5c29fd6c0c8ee2c1df9120bf2306028ba1cd2bb7f9a4309c': '480c45bd6774594309f907a1287f794299e81dcb4ed43827c253cd5d7704eca4',
    'd2afbb10e8c04806bc0e1244210c3c685c573ceaba06a4d17ab6c1eb3bdcb75b': 'bb074141092db975476a224663d6878c678a0de5a01a680030f98956bf7d54b2',
}
SYNTHETIC_FIXTURES = {
    '7230eb7f76593b74ed7872862c0ec7405c16389ebc1307b7260ece6992d11d37': {'/'+'tmp/no-source', '/'+'tmp/A.lean'},
    '9ecf81f0c65bcbc0f7eb2412810e6482f8dda2e0c21771ba96b7e7f7b8c2a5dc': {'/'+'home/private-owner/source.json', '/'+'home/private', '/'+'home/private/approval', '/'+'home/private/source'},
    'a7334c42d58f90331ef8de0e975763ae46bae46356e5503a89ea2f9d0980e1db': {'/'+'tmp/outside'},
    'd72dea559413e805a4e8ca87c5e9c081f853b5d81d348f568667c30b0f52ace0': {'/'+'tmp/a'},
}

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('invalid repository path')
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or any(p in ('..', '.') for p in value.split('/')) or '' in value.split('/'):
        raise ValueError('unsafe repository path')
    return path

def private_locators(text):
    return {m.group().rstrip('.,;:)') for m in PRIVATE.finditer(text)}

def private_uuid(text, body_sha256):
    allowed = PUBLIC_CITATION_UUIDS.get(body_sha256)
    if allowed:
        # Remove only the exact reviewed public citation span. A repeated UUID
        # elsewhere in the prose or a changed source receives no exception.
        for match in re.finditer(r'https?://[^\s<>`"\']+', text):
            url = match.group().rstrip(').,;]')
            if sha256(url.encode()) == allowed:
                text = text[:match.start()] + (' ' * len(url)) + text[match.start()+len(url):]
    return bool(UUID.search(text))

@lru_cache(maxsize=8)
def _origin_records(root):
    document = json.loads((pathlib.Path(root) / PREFIX / 'ORIGIN_REFERENCES.json').read_bytes())
    if document.get('schema') != 't20-v6-exact-origin-references-v1':
        return {}
    return {row['repository_path']: row for row in document['records']}

def origin_reference_text(src, text, root):
    """Occurrence-local scan copy; original coordinates are not local promises.

    Full body identity and all occurrence counts are required. New prose,
    mutated sources and other documents receive no exemption.
    """
    if not src.startswith(PREFIX + '/'):
        return text
    try:
        row = _origin_records(str(root)).get(src)
        if not row or row.get('origin_context') != 'preserved_source_document' or sha256(text.encode('utf-8')) != row['public_sha256']:
            return text
        replacements = []
        for reference in row['references']:
            target = '/'.join(reference['components'])
            safe_path(target)
            if not reference['occurrences'] or text.count(target) != reference['occurrences']:
                return text
            replacements.append(target)
        for target in replacements:
            text = text.replace(target, 'original-reference:' + sha256(target.encode()))
        return text
    except (OSError, KeyError, ValueError, TypeError):
        return text

def check_object(root, row):
    errors = []
    identity = row.get('source_sha256', '')
    if not SHA.fullmatch(identity):
        errors.append('invalid source identity')
    disposition = row.get('disposition')
    if disposition in ('IDENTITY_ONLY', 'NOT_PUBLISHED'):
        if any(key in row for key in ('repository_path', 'public_sha256', 'public_bytes')):
            errors.append('nonpublished source has a public body')
        return errors
    if disposition not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
        return errors + ['unknown disposition']
    try:
        relative = safe_path(row['repository_path'])
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('source symlink or escaped root')
        if row.get('repository_revision') is not None:
            if disposition != 'REUSE' or row['repository_revision'] != BASE:
                raise ValueError('invalid pinned historical reuse')
            body = subprocess.check_output(['git', 'show', BASE + ':' + relative.as_posix()], cwd=root)
        else:
            body = path.read_bytes()
    except (KeyError, OSError, ValueError, subprocess.CalledProcessError):
        return errors + ['missing or unsafe public source']
    if sha256(body) != row.get('public_sha256') or len(body) != row.get('public_bytes'):
        errors.append('public body differs')
    if disposition in ('REUSE', 'ADD_EXACT') and (sha256(body) != identity or len(body) != row.get('source_bytes')):
        errors.append('false byte identity')
    if disposition == 'PROJECT' and sha256(body) == identity:
        errors.append('projection does not change identity')
    # Existing public objects retain their current bytes and existing repository gates.
    if disposition != 'REUSE':
        try:
            text = body.decode('utf-8')
            allowed = SYNTHETIC_FIXTURES.get(identity, set()) if sha256(body) == identity else set()
            if private_locators(text) - allowed:
                errors.append('private machine locator')
            if re.search(r'(?:library-file:|project-file:|sandbox:/|libfile_[A-Za-z0-9]{12,}|file-[A-Za-z0-9]{16,})', text):
                errors.append('private platform linkage requires qualification')
            if private_uuid(text, sha256(body)):
                errors.append('nonpublic UUID linkage requires qualification')
        except UnicodeDecodeError:
            errors.append('unqualified binary source')
    return errors

def validate(root=ROOT):
    manifest = json.loads((root / MANIFEST).read_bytes())
    errors = []
    if manifest.get('schema') != 'orthemology-t20-v6-public-projection-v1' or manifest.get('base_commit') != BASE:
        errors.append('wrong public object or baseline')
    if manifest.get('scientific_acceptance') is not False or manifest.get('t21_started') is not False:
        errors.append('unauthorized scientific state')
    rows = manifest['objects']
    by_hash = {r['source_sha256']: r for r in rows}
    if len(rows) != 28478 or len(by_hash) != len(rows):
        errors.append('source universe missing or duplicated')
    counts = dict(collections.Counter(r['disposition'] for r in rows))
    if counts != manifest['counts'] or counts.get('REUSE') != 5625:
        errors.append('selection count or saved reuse differs')
    baseline_paths = set(subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASE], cwd=root, text=True).splitlines())
    protected = ['experiments/orthemology-v5', 'experiments/orthemology-v5-continuations',
                 'experiments/orthemology-v5-successors', 'docs/provenance/v5-consolidation',
                 'docs/provenance/v5-research-continuations', 'docs/provenance/v5-successors',
                 'research/t20-live-20261009']
    if subprocess.check_output(['git', 'diff', '--name-only', BASE, '--'] + protected, cwd=root):
        errors.append('preserved v5 or prior T20 baseline changed')
    for path, binding in _origin_records(str(root)).items():
        owner = by_hash.get(binding['source_sha256'], {})
        if owner.get('repository_path') != path or owner.get('public_sha256') != binding['public_sha256']:
            errors.append('original reference owner differs')
            continue
        text = (root / path).read_text(encoding='utf-8')
        if origin_reference_text(path, text, root) == text:
            errors.append('original reference occurrences differ')
    for row in rows:
        errors.extend(row['source_sha256'] + ': ' + error for error in check_object(root, row))
        if row['disposition'] == 'REUSE' and row['repository_path'] not in baseline_paths:
            errors.append('reused path absent from pinned baseline')
        if row['disposition'] in ('ADD_EXACT', 'PROJECT') and (row['repository_path'] in baseline_paths or not row['repository_path'].startswith(PREFIX + '/')):
            errors.append('new object is not additive in the public projection')
        for dependency in row.get('required_dependencies', []):
            if dependency not in by_hash:
                errors.append('undeclared dependency identity: ' + row['source_sha256'])
            elif row['disposition'] in ('REUSE', 'ADD_EXACT', 'PROJECT') and by_hash[dependency]['disposition'] not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
                errors.append('declared publication dependency is not available: ' + row['source_sha256'])
    # Manifest inventory is explicit; generated controls and navigation are separate.
    declared = {r['repository_path'] for r in rows if r['disposition'] in ('ADD_EXACT', 'PROJECT')}
    controls = json.loads((root / PREFIX / 'PUBLIC_CONTROLS.json').read_bytes())
    for relative, digest in controls['files'].items():
        safe_path(relative)
        body = (root / relative).read_bytes()
        if sha256(body) != digest:
            errors.append('public control differs: ' + relative)
        text = body.decode('utf-8')
        if private_locators(text) or private_uuid(text, sha256(body)) or re.search(r'(?:library-file:|project-file:|sandbox:/|libfile_[A-Za-z0-9]{12,}|file-[A-Za-z0-9]{16,})', text):
            errors.append('private identifier in public control: ' + relative)
    expected = declared | set(controls['files']) | {MANIFEST, PREFIX + '/PUBLIC_CONTROLS.json'}
    actual = {p.relative_to(root).as_posix() for p in (root / PREFIX).rglob('*') if p.is_file()}
    if actual != expected:
        errors.append('public inventory differs: ' + str(sorted(actual ^ expected)[:10]))
    register = json.loads((root / PREFIX / 'research-v6/synthesis/CROSS_CONTRIBUTIONS.json').read_bytes())
    if len(register['records']) != 15:
        errors.append('contribution cardinality differs')
    for contribution in register['records']:
        row = by_hash.get(contribution['sha256'], {})
        if row.get('disposition') not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
            errors.append('current contribution absent: ' + contribution['id'])
        review = root / PREFIX / 'research-v6' / contribution['independent_review']
        if not review.is_file():
            errors.append('current review absent: ' + contribution['id'])
    return errors, counts

def main():
    errors, counts = validate()
    for error in errors:
        print('[FAIL]', error)
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'scope': 'PUBLIC_SOURCE_INTEGRITY_AND_DECLARED_BOUNDARIES_ONLY', 'counts': counts, 'scientific_acceptance': False}, sort_keys=True))
    return int(bool(errors))

if __name__ == '__main__':
    sys.exit(main())
