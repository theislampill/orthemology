#!/usr/bin/env python3
"""Offline bounded custody checks. No predecessor execution or scholarly validation."""
import argparse, difflib, hashlib, json, re
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def verify(root, payload_only=False):
    root = root.resolve()
    checks = []
    def checked(name, condition, detail=None):
        if not condition:
            raise ValueError(name + ': FAILED' + (': ' + str(detail) if detail else ''))
        checks.append({'check': name, 'status': 'PASS', **({'detail': detail} if detail is not None else {})})
    def file(relative):
        p = root / relative
        checked('safe regular path: ' + relative, p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root))
        return p
    def read(relative):
        return file(relative).read_bytes()
    def j(relative):
        return json.loads(read(relative))
    def bound(relative, entry):
        d = read(relative)
        checked('byte/hash binding: ' + relative, len(d) == entry['bytes'] and digest(d) == entry['sha256'])
        return d
    def manifest(directory, historical=False):
        entries = j(directory + '/MANIFEST.json')['files']
        for e in entries:
            rel = e['path']
            target = directory + '/' + rel
            if historical:
                target = A + '/pre-clarification/REPORT.md' if rel == 'REPORT.md' else A + '/' + rel
            bound(target, e)
        return len(entries)

    A = 'intrinsic-succession-origin-20261010'
    R = 'intrinsic-succession-review-20261010'
    pm_data = read('PAYLOAD_MANIFEST.json')
    pm = json.loads(pm_data)
    expected = {e['path'] for e in pm['files']}
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    excluded = {'PAYLOAD_MANIFEST.json', 'PACKET_RECEIPT.json'}
    checked('exact payload inventory', actual - excluded == expected)
    checked('no symbolic links', not any(p.is_symlink() for p in root.rglob('*')))
    for e in pm['files']:
        bound(e['path'], e)
    checked('payload entry paths unique', len(expected) == len(pm['files']))
    if not payload_only:
        seal = j('PACKET_RECEIPT.json')
        checked('receipt binds payload manifest', seal['payload_manifest_sha256'] == digest(pm_data))
        checked('sealed inventory complete', actual == expected | excluded)

    freeze = j('REVIEW_FREEZE.json')
    for e in freeze['bound_files']:
        bound(e['path'], e)
    author_entries = manifest(A)
    review_entries = manifest(R)
    historical_entries = manifest(A + '/pre-clarification', historical=True)

    inheritance = j(A + '/INPUT_BINDINGS.json')
    for e in inheritance['inputs']:
        bound(e['path'], e)
    inheritance_index = j('EXACT_INHERITANCE.json')
    for e in inheritance_index['copied_files']:
        bound(e['path'], e)

    review_initial = j(R + '/INPUT_BINDINGS.json')['inputs']
    expected_changed = {A + '/REPORT.md', A + '/MANIFEST.json'}
    actual_changed = set()
    for e in review_initial:
        frozen = bound(R + '/' + e['snapshot_path'], e)
        source = read(e['source_path'])
        if source != frozen:
            actual_changed.add(e['source_path'])
            historical = A + '/pre-clarification/' + Path(e['source_path']).name
            checked('old version retained: ' + e['source_path'], read(historical) == frozen)
    checked('review transition exactly author report and manifest', actual_changed == expected_changed)
    for e in j(R + '/FINAL_INPUT_BINDINGS.json')['inputs']:
        frozen = bound(R + '/' + e['snapshot_path'], e)
        checked('final frozen/current identity: ' + e['source_path'], read(e['source_path']) == frozen)

    change = j(A + '/CHANGE_RECORD.json')
    before = bound(A + '/' + change['before']['path'], change['before'])
    after = bound(A + '/' + change['after']['path'], change['after'])
    oldtext, newtext = before.decode('utf-8'), after.decode('utf-8')
    ops = [list(o) for o in difflib.SequenceMatcher(None, oldtext, newtext, autojunk=False).get_opcodes() if o[0] != 'equal']
    checked('exactly one insertion and no removal/replacement', len(ops) == 1 and ops[0][0] == 'insert')
    checked('one-insertion coordinates match final review', ops == j(R + '/VERIFICATION.json')['final_diff_operations'])
    delta = ''.join(difflib.unified_diff(oldtext.splitlines(keepends=True), newtext.splitlines(keepends=True), fromfile='old', tofile='new'))
    recorded = read(R + '/FINAL_REPORT_DIFF.txt').decode('utf-8')
    checked('recorded final diff body reproduces', delta.split('\n', 2)[2] == recorded.split('\n', 2)[2])

    for name, start, end in [('DAR016_WEB49_103.txt', 49, 103), ('DAR016_WEB104_160.txt', 104, 160)]:
        lines = read(A + '/sources/' + name).decode('utf-8').splitlines()
        # A retained terminal blank line is formatting, not a missing coordinate.
        while lines and lines[-1] == '':
            lines.pop()
        matches = [re.match(r'^L(\d+):', line) for line in lines]
        checked('Dar declared complete retained coordinates: ' + name, all(matches) and [int(m.group(1)) for m in matches] == list(range(start, end + 1)))
    for name in ['MAJMU16_297_309.txt', 'MAJMU16_310_312.txt']:
        checked('Majmu retained-copy identity: ' + name, read(A + '/sources/' + name) == read('intrinsic-representation-dependency-20261010/' + name))
    checked('Shifa selected bytes occur in retained wider input', read(A + '/sources/SHIFA_e174_e175.txt') in read('wise-reason-asymmetry-20261010/sources/SHIFA_e173_e180.txt'))
    for e in j(A + '/SOURCE_READS.json')['source_returns']:
        checked('retained source locator resolves: ' + e['path'], (root / A / e['path']).is_file())

    cp20 = 'constructive-foundation-selection-20261009/inputs/CP20/wise-particular-determination-return-20261009/REPORT.md'
    cp23 = 'constructive-foundation-selection-20261009/inputs/CP23/affirmative-wise-determination-20261009/REPORT.md'
    checked('CP20 report equals recorded git blob', git_blob(read(cp20)) == inheritance['cp20_report_blob'])
    checked('CP20 reading record equals recorded git blob', git_blob(read(A + '/CP20_READING_RECORD.json')) == inheritance['cp20_reading_record_blob'])
    cp23_bytes = read(cp23)
    checked('CP23 preserved one-extra-terminal-LF exception', cp23_bytes.endswith(b'\n') and git_blob(cp23_bytes[:-1]) == inheritance['cp23_report_blob'] and git_blob(cp23_bytes) != inheritance['cp23_report_blob'])
    for e in j('constructive-foundation-selection-20261009/WISE_FRONTIER_CHECK.json')['inputs']:
        d = read(e['path'])
        checked('wise-frontier inherited local hash: ' + e['path'], len(d) == e['bytes'] and digest(d) == e['local_sha256'])
        if e['exact_blob_match']:
            checked('wise-frontier recorded git blob: ' + e['path'], git_blob(d) == e['git_blob_sha1'])

    return {'status': 'PASS', 'scope': 'Administrative custody and source-binding checks only; no semantic validation, fresh primary-reading claim, predecessor rerun, mathematical model validation, or T20 closure.', 'payload_manifest_sha256': digest(pm_data), 'payload_files': len(pm['files']), 'author_manifest_entries': author_entries, 'review_manifest_entries': review_entries, 'historical_author_manifest_entries': historical_entries, 'author_bound_inputs': len(inheritance['inputs']), 'review_initial_bindings': len(review_initial), 'checks_passed': len(checks), 'checks': checks}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path, required=True, help='New JSON file outside packet root; existing paths are refused')
    ap.add_argument('--payload-only', action='store_true', help='Initial administrative pre-seal check only; not a sealed replay')
    args = ap.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    if out.is_relative_to(root) or out.exists():
        ap.error('Output must be a new path outside the packet root')
    result = verify(root, args.payload_only)
    with out.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2); f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'checks'}, ensure_ascii=False))
