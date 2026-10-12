#!/usr/bin/env python3
"""Read-only bounded custody replay. External raw-source checks are opt-in."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re

A = 'scoped-original-authority-20261010'
R = 'source-conditional-right-review-20261010'
O = 'original-normative-authority-20261009'
MARKER = re.compile(r'\((\d+)/(\d+)\)')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe_file(root, relative):
    p = Path(relative)
    need(not p.is_absolute() and '..' not in p.parts, 'Unsafe path: ' + relative)
    out = root / p
    need(not any(x.is_symlink() for x in [out, *out.parents]), 'Symlink: ' + relative)
    need(out.is_file(), 'Missing file: ' + relative)
    return out


def check_record(root, record):
    data = safe_file(root, record['path']).read_bytes()
    need(digest(data) == record['sha256'], 'SHA-256 mismatch: ' + record['path'])
    if 'bytes' in record:
        need(len(data) == record['bytes'], 'Byte-count mismatch: ' + record['path'])


def normalize(text):
    return re.sub(r'[\x00-\x1f\x7f]', '\n', text).strip()


def split_pages(text):
    pages = {}
    previous = 0
    markers = list(MARKER.finditer(text))
    for match in markers:
        key = tuple(map(int, match.groups()))
        need(key not in pages, 'Duplicate page marker: ' + str(key))
        pages[key] = normalize(text[previous:match.start()])
        previous = match.end()
    return pages, text[previous:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--external-source-root', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    need(root not in output.parents and output != root, 'Output must be outside the packet')
    need(not output.exists(), 'Refusing to overwrite output')
    manifest_data = safe_file(root, 'MANIFEST.json').read_bytes()
    manifest_hash = digest(manifest_data)
    if args.expected_manifest_sha256:
        need(manifest_hash == args.expected_manifest_sha256, 'External manifest pin mismatch')
    manifest = json.loads(manifest_data)
    listed = [r['path'] for r in manifest['files']]
    need(len(listed) == len(set(listed)), 'Duplicate inventory entry')
    actual = set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'Symlink in packet')
        if p.is_file():
            actual.add(p.relative_to(root).as_posix())
    need(actual == set(listed) | {'MANIFEST.json'}, 'Packet inventory mismatch')
    for record in manifest['files']:
        check_record(root, record)

    source = load(root / A / 'SOURCE_READS.json')
    review = load(root / R / 'INPUT_RECEIPT.json')
    external = load(root / 'EXTERNAL_SOURCES.json')
    omitted = {r['path']: r for r in external['nonvendored_full_source']}
    need(set(omitted) == {source['source']['word']['path'], source['source']['inherited_body']['path']},
         'Unexpected full-source exclusion set')
    for p in omitted:
        need(not (root / p).exists(), 'Full source unexpectedly included')
    need(review['reviewed_report']['sha256'] ==
         'ea7f8680df2137e56f5a37ff6c286978d41cf063631d8995828ee9315808f7a8',
         'Frozen author target changed')
    check_record(root, review['reviewed_report'])
    check_record(root, review['review_report'])
    groups = {
        'author_manifest': load(root / A / 'MANIFEST.json')['files'],
        'author_inputs': load(root / A / 'INPUT_BINDINGS.json')['records'],
        'inherited_check': load(root / A / 'INHERITED_BINDING_CHECK.json')['checks'],
        'controlling_inputs': load(root / O / 'INPUT_BINDINGS.json')['records'],
        'review_received_files': review['exact_received_files'],
        'review_binding_files': [r['binding_file'] for r in review['verification_summary']],
        'current_source_records': [source['source']['word'], source['source']['inherited_body'],
                                   *source['local_selected_files'], source['reused_primary_extract']],
        'copied_originals': load(root / 'EXACT_INHERITANCE.json')['copied_files'],
    }
    binding_results = {}
    for name, records in groups.items():
        included = skipped = 0
        for record in records:
            if record['path'] in omitted:
                counterpart = omitted[record['path']]
                need(all(record[k] == counterpart[k] for k in ('bytes', 'sha256')),
                     'External source binding mismatch')
                skipped += 1
            else:
                check_record(root, record)
                included += 1
        binding_results[name] = {'checked_included': included,
                                 'identified_external_not_checked': skipped}

    excerpts = [*source['local_selected_files'], source['reused_primary_extract']]
    received_excerpts = {r['path']: r for r in review['extract_check']['records']}
    shared = {}
    page_occurrences = 0
    for record in excerpts:
        text = (root / record['path']).read_bytes().decode('utf-8')
        pages, tail = split_pages(text)
        need(not tail.strip(), 'Unmarked text after final excerpt page')
        keys = list(pages)
        need(bool(keys) and keys == [(keys[0][0], p) for p in range(keys[0][1], keys[-1][1] + 1)],
             'Excerpt page markers are not continuous')
        need(len(keys) == received_excerpts[record['path']]['page_occurrences'],
             'Review page count mismatch')
        for key, body in pages.items():
            if key in shared:
                need(shared[key] == body, 'Overlapping excerpt page mismatch')
            shared[key] = body
        page_occurrences += len(keys)
    need(page_occurrences == review['extract_check']['checked_page_occurrences'],
         'Total page occurrence mismatch')
    need(len(shared) == review['extract_check']['checked_distinct_pages'],
         'Distinct page count mismatch')

    raw_result = {'performed': False, 'status': 'Not requested; full Word and decode are not vendored.'}
    if args.external_source_root:
        raw_root = args.external_source_root.resolve()
        for record in omitted.values():
            check_record(raw_root, record)
        word = (raw_root / source['source']['word']['path']).read_bytes()
        saved_decode = (raw_root / source['source']['inherited_body']['path']).read_bytes()
        decoded = re.sub(r'[\u064b-\u065f\u0670]', '', word.decode('utf-16le', errors='ignore'))
        need(decoded.encode('utf-8') == saved_decode, 'Exact raw decode reproduction mismatch')
        raw_pages, _ = split_pages(decoded)
        need(len(raw_pages) == review['extract_check']['unique_body_markers'],
             'Raw body marker count mismatch')
        for key, body in shared.items():
            need(key in raw_pages and body == raw_pages[key], 'External raw page mismatch: ' + str(key))
        raw_result = {
            'performed': True, 'status': 'Passed using separately supplied exact local raw files',
            'external_source_root': str(raw_root), 'nonvendored_source_identities': list(omitted.values()),
            'exact_decode_bytes_match': True, 'unique_received_body_markers': len(raw_pages),
            'checked_page_occurrences': page_occurrences, 'checked_distinct_pages': len(shared),
            'all_selected_pages_match': True,
            'limit': 'Exact received-witness identity and normalized selected spans only; not a full Word parser, rendered-page collation, new witness, or fresh scholarly reading.'}

    result = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'PASS', 'classification': 'Administrative custody verification; excluded from research time',
        'packet_root': str(root), 'manifest_sha256': manifest_hash,
        'external_manifest_pin_checked': bool(args.expected_manifest_sha256),
        'executed_script_sha256': digest(Path(__file__).read_bytes()),
        'payload_files_checked': len(listed), 'exact_inventory_and_hashes_match': True,
        'binding_checks': binding_results,
        'portable_excerpt_check': {'files': len(excerpts), 'continuous_page_occurrences': page_occurrences,
                                   'distinct_pages': len(shared), 'overlaps_match': True,
                                   'limit': 'Internal excerpt continuity and equality; raw-source derivation is not replayed by the portable check.'},
        'external_raw_check': raw_result,
        'scholarly_limit': 'No proof of interpretation, acceptance, integration, readiness, or T20 closure.'}
    with output.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('PASS:', len(listed), 'payload files;', page_occurrences,
          'page occurrences;', len(shared), 'distinct pages; raw check:', raw_result['performed'])


if __name__ == '__main__':
    main()
