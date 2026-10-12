#!/usr/bin/env python3
"""Check recorded byte identities and custody links without rerunning science.

This is consistency checking, not authentication. Compare the separately
provided archive/acceptance hash to detect coordinated package replacement.
No research helper, compiler, network request or environment script is run.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

MANIFEST = 'MANIFEST.json'
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_ARCHIVE_BYTES = 256 * 1024 * 1024

class Invalid(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise Invalid(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def read_json(data):
    def bad_constant(value):
        raise Invalid('nonfinite JSON value')
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=bad_constant)

def safe(name):
    require(isinstance(name, str) and bool(name), 'empty or nonstring path')
    require(not any(ord(c) < 32 or ord(c) == 127 for c in name), 'control character in path')
    require('\\' not in name and ':' not in name, 'nonportable path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and str(path) == name, 'unsafe or noncanonical path')
    require(all(part not in ('', '.', '..') for part in name.split('/')), 'path traversal')
    return name

def valid_identity(row):
    require(isinstance(row, dict), 'identity must be an object')
    require(type(row.get('bytes')) is int and 0 <= row['bytes'] <= MAX_FILE_BYTES, 'invalid byte count')
    require(isinstance(row.get('sha256'), str) and re.fullmatch('[0-9a-f]{64}', row['sha256']) is not None, 'invalid SHA256')

def match(data, row, label):
    valid_identity(row)
    require(len(data) == row['bytes'], 'size mismatch: ' + label)
    require(sha(data) == row['sha256'], 'SHA256 mismatch: ' + label)

def table(rows, crc=False):
    require(isinstance(rows, list) and bool(rows), 'empty or invalid identity table')
    result = {}
    for row in rows:
        valid_identity(row)
        name = safe(row.get('path'))
        require(name not in result, 'duplicate identity path: ' + name)
        if crc:
            require(type(row.get('crc32')) is int and 0 <= row['crc32'] <= 0xffffffff, 'invalid CRC32')
        result[name] = row
    return result

def regular_bytes(path, label):
    require(not path.is_symlink() and stat.S_ISREG(path.stat().st_mode), 'not a regular nonsymlink file: ' + label)
    require(path.stat().st_size <= MAX_FILE_BYTES, 'file exceeds size limit: ' + label)
    return path.read_bytes()

def directory_bytes(directory):
    require(not directory.is_symlink() and directory.is_dir(), 'bundle must be a nonsymlink directory')
    result = {}
    def walk_error(error):
        raise Invalid('directory traversal failed')
    for current, directories, files in os.walk(directory, followlinks=False, onerror=walk_error):
        for name in directories:
            p = Path(current) / name
            require(not p.is_symlink(), 'symlink directory')
            safe(p.relative_to(directory).as_posix())
        for name in files:
            p = Path(current) / name
            relative = safe(p.relative_to(directory).as_posix())
            result[relative] = regular_bytes(p, relative)
    return result

def archive_bytes(data, wanted=None):
    require(len(data) <= MAX_FILE_BYTES, 'archive exceeds compressed size limit')
    result = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        require(bool(infos) and len(infos) <= 20000, 'invalid archive member count')
        require(sum(i.file_size for i in infos) <= MAX_ARCHIVE_BYTES, 'archive exceeds expanded size limit')
        for info in infos:
            require(info.orig_filename == info.filename, 'ZIP filename truncation or translation')
            name = safe(info.filename)
            require(name not in result, 'duplicate ZIP member: ' + name)
            require(not info.is_dir(), 'directory ZIP entries are outside this package contract')
            mode = info.external_attr >> 16
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'nonregular ZIP entry: ' + name)
            require(not info.flag_bits & 1, 'encrypted ZIP entry')
            require(info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'unsupported ZIP compression')
            require(info.file_size <= MAX_FILE_BYTES, 'ZIP member exceeds size limit')
            if wanted is not None:
                require(name in wanted, 'unlisted ZIP member: ' + name)
                require(info.file_size == wanted[name]['bytes'], 'ZIP declared size mismatch: ' + name)
                require(info.CRC == wanted[name]['crc32'], 'ZIP recorded CRC mismatch: ' + name)
            content = archive.read(info)  # zipfile checks actual CRC while reading every member.
            if wanted is not None:
                match(content, wanted[name], name)
            result[name] = content
        if wanted is not None:
            require(set(result) == set(wanted), 'ZIP membership mismatch')
    return result

def pointer(document, path):
    require(isinstance(path, str) and path.startswith('/'), 'invalid JSON pointer')
    value = document
    for encoded in path[1:].split('/'):
        require(re.search(r'~(?![01])', encoded) is None, 'invalid JSON pointer escape')
        key = encoded.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            require(re.fullmatch('0|[1-9][0-9]*', key) is not None, 'invalid JSON array pointer')
            value = value[int(key)]
        else:
            require(isinstance(value, dict), 'JSON pointer crosses scalar')
            value = value[key]
    return value

def verify(directory, allow_staging=False, report=None, outer_archive=None, expected_manifest=None):
    files = directory_bytes(directory)
    require(MANIFEST in files, 'missing manifest')
    raw = files[MANIFEST]
    if expected_manifest is not None:
        require(re.fullmatch('[0-9a-f]{64}', expected_manifest) is not None, 'invalid expected manifest hash')
        require(sha(raw) == expected_manifest, 'manifest pin mismatch')
    document = read_json(raw)
    require(isinstance(document, dict) and document.get('schema') == 'eleventh-public-evidence-v1', 'unsupported manifest schema')
    status = document.get('status')
    require(status in ('STAGING', 'FINAL_REVIEW_CANDIDATE'), 'unsupported package status')
    require(status != 'STAGING' or allow_staging, 'staging requires explicit --allow-staging')
    wanted = table(document.get('files'))
    require(MANIFEST not in wanted, 'manifest self-entry forbidden')
    require(set(files) == set(wanted) | {MANIFEST}, 'outer file membership mismatch')
    for name, row in wanted.items():
        match(files[name], row, name)
    nested = {}
    descriptions = document.get('archives')
    require(isinstance(descriptions, list), 'archives must be a list')
    for description in descriptions:
        name = safe(description['path'])
        require(name in wanted and name.endswith('.zip') and name not in nested, 'invalid or duplicate archive descriptor')
        nested[name] = archive_bytes(files[name], table(description['members'], crc=True))
    require({name for name in wanted if name.endswith('.zip')} == set(nested), 'uninspected payload ZIP')
    def locate(locator):
        require(isinstance(locator, dict) and set(locator) in ({'path'}, {'path', 'member'}), 'invalid evidence locator')
        path = safe(locator['path'])
        require(path in wanted, 'unselected evidence target: ' + path)
        if 'member' in locator:
            member = safe(locator['member'])
            require(path in nested and member in nested[path], 'missing nested evidence target')
            return nested[path][member]
        return files[path]
    edges = document.get('identity_edges')
    require(isinstance(edges, list), 'identity edges must be a list')
    for edge in edges:
        record = read_json(locate(edge['record']))
        target = locate(edge['target'])
        digest = pointer(record, edge['sha256_pointer'])
        require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None, 'invalid receipt digest')
        require(sha(target) == digest, 'stale receipt SHA256 binding')
        if edge.get('bytes_pointer') is not None:
            size = pointer(record, edge['bytes_pointer'])
            require(type(size) is int and len(target) == size, 'stale receipt size binding')
    if status == 'FINAL_REVIEW_CANDIDATE':
        require(document.get('claim_crosswalk') is not None, 'final mode requires selected claim crosswalk')
    crosswalk_counts = None
    crosswalk = None
    if document.get('claim_crosswalk') is not None:
        crosswalk = read_json(locate({'path':safe(document['claim_crosswalk'])}))
        keys = crosswalk.get('evidence_keys')
        claims = crosswalk.get('report_claim_bindings')
        require(isinstance(keys, dict) and bool(keys), 'crosswalk lacks evidence keys')
        require(isinstance(claims, list) and bool(claims), 'crosswalk lacks report claim bindings')
        selected_count = historical_count = 0
        for key, entry in keys.items():
            require(isinstance(key, str) and bool(key) and isinstance(entry, dict), 'invalid evidence key')
            artifacts = entry.get('artifacts', [])
            identities = entry.get('identity_references', [])
            require(isinstance(artifacts, list) and isinstance(identities, list) and bool(artifacts or identities), 'unsupported crosswalk evidence key')
            for artifact in artifacts:
                valid_identity(artifact)
                if 'archive' in artifact:
                    locator = {'path':artifact['archive'], 'member':artifact['archive_member']}
                else:
                    locator = {'path':artifact['path']}
                match(locate(locator), artifact, 'crosswalk artifact')
                selected_count += 1
            for historical in identities:
                valid_identity(historical)
                require(historical.get('distribution') == 'identity_only_not_redistributed', 'historical identity must explicitly remain unselected')
                require(isinstance(historical.get('title'), str) and bool(historical['title']), 'historical identity lacks title')
                require(isinstance(historical.get('scope'), str) and bool(historical['scope']), 'historical identity lacks bounded scope')
                historical_count += 1
        claim_ids = set()
        for claim in claims:
            claim_id = claim.get('claim_id')
            require(isinstance(claim_id, str) and bool(claim_id) and claim_id not in claim_ids, 'duplicate or invalid report claim ID')
            claim_ids.add(claim_id)
            references = claim.get('evidence_keys')
            require(isinstance(references, list) and bool(references), 'claim lacks evidence references')
            require(all(isinstance(key, str) and key in keys for key in references), 'claim names unknown evidence key')
        crosswalk_counts = {'claims':len(claim_ids), 'selected_artifact_links':selected_count, 'historical_identity_only_references':historical_count}
    binding = document.get('report_binding')
    if status == 'FINAL_REVIEW_CANDIDATE':
        require(isinstance(binding, dict) and report is not None, 'final mode requires report binding and --report')
    if binding is not None:
        require(isinstance(binding, dict), 'invalid report binding')
        report_name = safe(binding['path'])
        require('/' not in report_name and report_name.endswith('.docx'), 'report binding must name a native DOCX companion')
        require(report_name not in files, 'report body must remain an external companion')
        require(report is not None, 'bound report requires --report')
        require(report.name == report_name, 'external report basename mismatch')
        report_data = regular_bytes(report, 'external report')
        match(report_data, binding, 'external report')
        if crosswalk is not None:
            declared_report = crosswalk.get('external_report')
            require(isinstance(declared_report, dict), 'claim crosswalk lacks external report identity')
            match(report_data, declared_report, 'claim crosswalk external report')
            require(declared_report.get('name') == report_name, 'claim crosswalk external report filename mismatch')
        report_edges = document.get('report_identity_edges')
        require(isinstance(report_edges, list) and bool(report_edges), 'bound report requires selected receipt identity edges')
        for report_edge in report_edges:
            receipt = read_json(locate(report_edge['record']))
            require(pointer(receipt, report_edge['sha256_pointer']) == binding['sha256'], 'stale report receipt SHA256')
            recorded_size = pointer(receipt, report_edge['bytes_pointer'])
            require(type(recorded_size) is int and recorded_size == binding['bytes'], 'stale report receipt size')
            recorded_name = pointer(receipt, report_edge['name_pointer'])
            name_is_path = report_edge.get('name_is_path', False)
            require(type(name_is_path) is bool, 'invalid report receipt path flag')
            if name_is_path:
                recorded_name = PurePosixPath(safe(recorded_name)).name
            require(recorded_name == report_name, 'stale report receipt filename')
        members = archive_bytes(report_data)
        require('[Content_Types].xml' in members and 'word/document.xml' in members, 'report lacks native Word parts')
    elif report is not None:
        raise Invalid('external report supplied without manifest binding')
    if outer_archive is not None:
        outer = archive_bytes(regular_bytes(outer_archive, 'outer archive'))
        require(set(outer) == set(files), 'outer archive membership mismatch')
        for name in files:
            require(outer[name] == files[name], 'outer archive content mismatch: ' + name)
    return {'status':'PASS', 'scope':'Byte identity, exact archive membership/CRC and selected custody links only; no scientific replay or authentication.',
            'package_status':status, 'manifest_sha256':sha(raw), 'files_checked':len(wanted),
            'nested_archives_checked':len(nested), 'nested_members_checked':sum(len(x) for x in nested.values()),
            'identity_edges_checked':len(edges), 'external_report_checked':binding is not None,
            'outer_archive_checked':outer_archive is not None, 'claim_crosswalk_checked':crosswalk_counts}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--allow-staging', action='store_true')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--expected-manifest-sha256')
    args = parser.parse_args()
    try:
        result = verify(args.directory, args.allow_staging, args.report, args.archive, args.expected_manifest_sha256)
    except (Invalid, ValueError, TypeError, KeyError, IndexError, OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as error:
        # Only deliberate validation messages are exposed; system exceptions can contain local paths.
        result = {'status':'FAIL', 'error':str(error) if isinstance(error, Invalid) else type(error).__name__}
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
