#!/usr/bin/env python3
"""Verify this closed public projection. No external source file is required."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MAIN = 'PARTICULAR_POWERS_AND_MODAL_WARRANT.md'
NOTES = 'LOCUS_AND_INCREMENT_NOTES.md'
ORIGINAL_MAIN = '8dc3412ffe2d46a708b722ce1a1b8d22057c44493339a3a499417327753a327c'
PUBLIC_MAIN = '6506838ecede1e4c967a75f855ad7121c722bcfcf3b6e1404a7b81062100ac41'
ORIGINAL_NOTES = '3bad70233e2a5feaf6ee5edc2aaff68b6641873e0593de00a0f0733fa49fa604'
PUBLIC_NOTES = 'ff44cc66086a65c65ddf3dd36c1fd4e21c238ed0987ab83b9a7fe47457521c08'
BASELINE = dict(zip(('M01','M02','M03','M04','M05','M06','M07','M08','M09','M10'),
                    (188,156,105,89,176,176,92,151,30,29)))
REPORT_DELTA = dict(zip(BASELINE, (3,28,0,0,17,17,0,28,0,0)))
EXPECTED = {MAIN, NOTES, 'README.md', 'SOURCE_LEDGER.json', 'INPUT_BINDING.json',
            'PRESERVATION_MAP.json', 'ORIGINAL_TO_PUBLIC.json',
            'SOURCE_REUSE_ACCOUNTING.json', 'verify_public.py', 'MANIFEST.json',
            'review/PUBLIC_PRESERVATION_REVIEW.md',
            'review/PUBLIC_PRESERVATION_REFERENCE.json',
            'review/PUBLIC_SCIENTIFIC_PRESERVATION.md',
            'review/PUBLIC_SCIENTIFIC_REFERENCE.json'}
WORD = re.compile(r"\b[\w]+(?:[’'-][\w]+)*\b")


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def get(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def check_record(name, record):
    require(name in EXPECTED, 'Unknown bound file: ' + name)
    data = (ROOT / name).read_bytes()
    require(record['bytes'] == len(data), 'Size mismatch: ' + name)
    require(record['sha256'] == digest(data), 'Hash mismatch: ' + name)


def check_review(reference_path, summary_path, schema, verdict):
    reference = get(reference_path)
    require(reference['schema'] == schema, 'Wrong review schema')
    require(reference['verdict'] == verdict, 'Review verdict does not accept this scope')
    require(reference['mandatory_corrections'] == [], 'Review has unresolved corrections')
    required = {MAIN, NOTES}
    require(required <= set(reference['reviewed_files']), 'Review lacks primary targets')
    for name, record in reference['reviewed_files'].items():
        check_record(name, record)
    check_record(summary_path, reference['public_summary'])


def main():
    files, dirs = set(), set()
    for p in ROOT.rglob('*'):
        name = p.relative_to(ROOT).as_posix()
        require(not p.is_symlink(), 'Symlink forbidden: ' + name)
        if p.is_file():
            files.add(name)
        elif p.is_dir():
            dirs.add(name)
        else:
            raise ValueError('Unsupported filesystem entry: ' + name)
    require(files == EXPECTED, 'Closed file inventory mismatch: missing=' +
            str(sorted(EXPECTED-files)) + '; extra=' + str(sorted(files-EXPECTED)))
    require(dirs == {'review'}, 'Closed directory inventory mismatch')
    manifest = get('MANIFEST.json')
    require(manifest['schema'] == 'modal-source-portable-public-manifest-v2', 'Wrong manifest schema')
    require(set(manifest['files']) == EXPECTED-{'MANIFEST.json'}, 'Manifest inventory mismatch')
    require(manifest['directories'] == ['review'], 'Manifest directory mismatch')
    for name, record in manifest['files'].items():
        check_record(name, record)
    require(digest((ROOT/MAIN).read_bytes()) == PUBLIC_MAIN, 'Public paper changed')
    require(digest((ROOT/NOTES).read_bytes()) == PUBLIC_NOTES, 'Public locus notes changed')
    mapping = get('PRESERVATION_MAP.json')
    require(mapping['schema'] == 'modal-source-complete-byte-range-map-v2', 'Wrong mapping schema')
    require(len(mapping['documents']) == 2, 'Text mapping incomplete')
    bound = {MAIN:(ORIGINAL_MAIN,PUBLIC_MAIN,34811), NOTES:(ORIGINAL_NOTES,PUBLIC_NOTES,10019)}
    seen = set()
    changes = {}
    for doc in mapping['documents']:
        name = doc['public']['path']
        require(name in bound and name not in seen, 'Unknown or duplicate mapped document')
        seen.add(name)
        original, public, original_size = bound[name]
        require(doc['original']['sha256'] == original, 'Wrong original text identity')
        require(doc['original']['bytes'] == original_size, 'Wrong original text size')
        check_record(name, doc['public'])
        require(doc['public']['sha256'] == public, 'Wrong public text identity')
        data = (ROOT/name).read_bytes()
        original_end = public_end = 0
        changed = []
        for lineno, segment in enumerate(doc['segments'], 1):
            require(segment['original_line'] == lineno, 'Nonsequential line mapping')
            require(segment['original_start'] == original_end, 'Original byte gap/overlap')
            require(segment['public_start'] == public_end, 'Public byte gap/overlap')
            oe, pe = segment['original_end'], segment['public_end']
            require(isinstance(oe,int) and original_end < oe <= original_size, 'Invalid original range')
            require(isinstance(pe,int) and public_end <= pe <= len(data), 'Invalid public range')
            part = data[public_end:pe]
            require(digest(part) == segment['public_sha256'], 'Wrong mapped public slice')
            if segment['unchanged']:
                require(segment['original_sha256'] == segment['public_sha256'], 'Unchanged slice hash mismatch')
                require(oe-original_end == pe-public_end, 'Unchanged slice size mismatch')
            else:
                changed.append(lineno)
                require(bool(segment.get('change_reason')), 'Missing editorial reason')
            original_end, public_end = oe, pe
        require(original_end == original_size and public_end == len(data), 'Incomplete byte coverage')
        changes[name] = changed
    require(seen == set(bound), 'Missing mapped document')
    require(changes == {MAIN:[112,114,116,140,142,150,160,171], NOTES:[55,64]}, 'Unexpected textual change')
    origin = get('ORIGINAL_TO_PUBLIC.json')
    require(origin['originals_unchanged'] is True, 'Original preservation not declared')
    require(origin['projection_has_prose_edits'] is True, 'Projection edits not declared')
    require(origin['preserved_prior_archive']['sha256'] == '190ff2991fd020eb3bd64ea37db46ca681f3246bc9db7b60b2225520a7e00c19', 'Wrong prior archive')
    require(len(origin['mappings']) == 4, 'Missing original-to-public record')
    for record in origin['mappings']:
        name = record['public']['path']
        check_record(name,record['public'])
        if record['transformation'] == 'byte-identical':
            require(record['original']['sha256'] == record['public']['sha256'], 'Identity record differs')
    ledger = get('SOURCE_LEDGER.json')
    require(len(ledger['sources']) == 8, 'Source register incomplete')
    require([s['id'] for s in ledger['sources']] == ['P01','P02','P03','P04','P05','P06','P05-supplied','P07'], 'Source identities changed')
    require(len(get('INPUT_BINDING.json')['inputs']) == 10, 'Predecessor binding incomplete')
    reuse = get('SOURCE_REUSE_ACCOUNTING.json')
    require(reuse['schema'] == 'modal-source-cumulative-reuse-accounting-v2', 'Wrong accounting schema')
    require(reuse['article_body_verbatim_words_added'] == 0, 'Unreviewed article quotation')
    blocks = reuse['charged_modal_blocks']
    require(len(blocks) == 2 and all(b['source'] == 'M01' for b in blocks), 'Unexpected modal charged blocks')
    count = 0
    for b, expected_count in zip(blocks, (4,3)):
        require(b['file'] == MAIN, 'Wrong charged file')
        chunk = (ROOT/MAIN).read_bytes()[b['start_byte']:b['end_byte']]
        require(digest(chunk) == b['text_sha256'], 'Wrong charged span digest')
        local_count = len(WORD.findall(chunk.decode('utf-8')))
        require(local_count == b['words'] == expected_count, 'Wrong pointer word count')
        count += local_count
    require(set(reuse['aggregate']) == set(BASELINE), 'Accounting source set changed')
    totals = {}
    for key, base in BASELINE.items():
        row = reuse['aggregate'][key]
        modal = count if key == 'M01' else 0
        total = base + modal + REPORT_DELTA[key]
        require(row['necessary_source_projection'] == base, 'Baseline charge changed')
        require(row['modal_public_v2'] == modal, 'Modal delta mismatch')
        require(row['report_v3'] == REPORT_DELTA[key], 'Report charge mismatch')
        require(row['combined_total'] == total, 'Aggregate mismatch')
        require(row['limit'] == 200 and total <= 200, 'Source allowance exceeded')
        require(row['remaining'] == 200-total, 'Headroom mismatch')
        totals[key] = total
    check_review('review/PUBLIC_PRESERVATION_REFERENCE.json',
                 'review/PUBLIC_PRESERVATION_REVIEW.md',
                 'modal-source-public-preservation-review-v2',
                 'PASS_BOUNDED_PRESERVATION_AND_DISTRIBUTION_REVIEW')
    check_review('review/PUBLIC_SCIENTIFIC_REFERENCE.json',
                 'review/PUBLIC_SCIENTIFIC_PRESERVATION.md',
                 'modal-source-public-scientific-preservation-v2',
                 'PASS_BOUNDED_SCIENTIFIC_PRESERVATION')
    print(json.dumps({'status':'PASS','payload_files':len(files),'payload_directories':len(dirs),
                      'original_main_sha256':ORIGINAL_MAIN,'public_main_sha256':PUBLIC_MAIN,
                      'combined_declared_source_totals':totals,'external_files_required':0,
                      'scope':'Portable integrity and declared accounting only; independent review records bind human preservation and attribution judgments.'},indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
