#!/usr/bin/env python3
"""Check complete archive inventory and replay unmodified retained controls."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT / 'fixed-marginal-correction-20261011'
REVIEW = ROOT / 'fixed-marginal-correction-independent-review-20261011'
PARTICIPATING = ROOT / 'marginal-constraint-root-check-20261011'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + str(key))
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=no_duplicate_keys)


def verify_inventory():
    manifest = read_json(ROOT / 'MANIFEST.json')
    require(manifest.get('format') == 'sha256-complete-files-v1', 'manifest format')
    entries = manifest['files']
    paths = [row['path'] for row in entries]
    require(len(paths) == len(set(paths)), 'duplicate manifest path')
    for rel in paths:
        p = PurePosixPath(rel)
        require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == rel,
                'unsafe or noncanonical manifest path: ' + rel)
    all_paths = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in all_paths), 'symlinks are not permitted')
    require(all(p.is_file() or p.is_dir() for p in all_paths), 'nonregular archive member')
    actual = {p.relative_to(ROOT).as_posix() for p in all_paths if p.is_file()}
    expected = set(paths) | {'MANIFEST.json'}
    require(actual == expected,
            'inventory mismatch; missing=' + repr(sorted(expected - actual)) +
            '; extra=' + repr(sorted(actual - expected)))
    for row in entries:
        p = ROOT / row['path']
        require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                'manifest byte/hash mismatch: ' + row['path'])
    return len(entries)


def verify_retained_pins():
    scope = read_json(ROOT / 'PRESERVATION_SCOPE.json')
    af = read_json(AUTHOR / 'AUTHOR_FREEZE.json')
    vf = read_json(REVIEW / 'REVIEW_FREEZE.json')
    vb = read_json(REVIEW / 'REVIEW_BINDINGS.json')
    require(digest(AUTHOR / 'RESULT.md') == scope['author_result_sha256'] ==
            af['result_sha256'] == vf['author_result_sha256'] == vb['reviewed_result_sha256'],
            'author result pin')
    require(digest(AUTHOR / 'MANIFEST.json') == scope['author_manifest_sha256'] ==
            af['manifest_sha256'] == vb['reviewed_manifest_sha256'], 'author manifest pin')
    require(digest(REVIEW / 'REVIEW.md') == scope['review_sha256'] == vf['review_sha256'],
            'review result pin')
    require(digest(REVIEW / 'MANIFEST.json') == scope['review_manifest_sha256'] ==
            vf['manifest_sha256'], 'review manifest pin')
    for folder in (AUTHOR, REVIEW):
        for row in read_json(folder / 'MANIFEST.json')['files']:
            p = folder / row['path']
            require(digest(p) == row['sha256'] and p.stat().st_size == row['bytes'],
                    'retained manifest entry: ' + str(p.relative_to(ROOT)))
    for rel, wanted in vb['author_files_before_and_after'].items():
        require(digest(AUTHOR / rel) == wanted == digest(REVIEW / 'author-snapshot' / rel),
                'author/reviewer snapshot pin: ' + rel)
    for row in read_json(AUTHOR / 'INPUT_BINDINGS.json'):
        require(digest(AUTHOR / row['snapshot']) == row['sha256'],
                'retained input snapshot: ' + row['snapshot'])
    for name in ('check.py', 'CHECKS.json'):
        require((PARTICIPATING / name).read_bytes() ==
                (AUTHOR / 'inputs/participating-root-check' / name).read_bytes(),
                'participating root custody: ' + name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--inventory-only', action='store_true')
    args = parser.parse_args()
    inventory_count = verify_inventory()
    verify_retained_pins()
    if args.inventory_only:
        print(json.dumps({'status': 'PASS_INVENTORY_AND_PINS',
                          'manifest_entries': inventory_count}))
        return
    require(args.output_dir is not None, '--output-dir is required for replays')
    out = args.output_dir.resolve()
    require(out != ROOT and ROOT not in out.parents,
            'output directory must be outside the evidence tree')
    out.mkdir(parents=True, exist_ok=False)
    # Preserve optimization mode in child interpreters. No assertion gates are
    # used by this wrapper; root-check JSON is checked even when -O disables
    # the unmodified root script\'s historical assert statement.
    python = [sys.executable] + (['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else [])
    records = []

    def run(label, script, arguments):
        command = python + [str(script)] + arguments
        result = subprocess.run(command, cwd=str(out), capture_output=True, text=True)
        (out / (label + '.stdout.log')).write_text(result.stdout)
        (out / (label + '.stderr.log')).write_text(result.stderr)
        records.append({'label': label, 'script': script.relative_to(ROOT).as_posix(),
                        'returncode': result.returncode})
        require(result.returncode == 0, label + ' exited ' + str(result.returncode))
        return result.stdout

    for label, folder in [('author', AUTHOR), ('review-author-snapshot', REVIEW / 'author-snapshot')]:
        run(label, folder / 'verify.py', ['--output-dir', str(out / label)])
        got = read_json(out / label / 'CHECKS.json')
        expected = read_json(REVIEW / 'portable-author-replay/CHECKS.json')
        require(got['status'] == 'PASS' and got['check_count'] == 43 and
                len(got['checks']) == 43 and all(x['pass'] is True for x in got['checks']),
                label + ' portable 43-control contract')
        require({k:v for k,v in got.items() if k not in ('python','sympy')} ==
                {k:v for k,v in expected.items() if k not in ('python','sympy')},
                label + ' control record mismatch')
        records[-1].update({'controls': 43, 'all_passed': True,
                           'record_byte_identical': (out / label / 'CHECKS.json').read_bytes() ==
                           (REVIEW / 'portable-author-replay/CHECKS.json').read_bytes(),
                           'python': got['python'], 'sympy': got['sympy']})

    run('review-final', REVIEW / 'check_independent.py', ['--output-dir', str(out / 'review-final')])
    got = read_json(out / 'review-final/INDEPENDENT_CHECKS.json')
    expected = read_json(REVIEW / 'independent-replay/INDEPENDENT_CHECKS.json')
    require(got['passed'] is True and got['check_count'] == 50 and len(got['checks']) == 50
            and all(x['passed'] is True for x in got['checks']), 'review 50-control contract')
    require({k:v for k,v in got.items() if k != 'sympy_version'} ==
            {k:v for k,v in expected.items() if k != 'sympy_version'}, 'review control record mismatch')
    records[-1].update({'controls': 50, 'all_passed': True,
                       'record_byte_identical': (out / 'review-final/INDEPENDENT_CHECKS.json').read_bytes() ==
                       (REVIEW / 'independent-replay/INDEPENDENT_CHECKS.json').read_bytes(),
                       'scope': 'Separate reviewer controls include reviewer-participating extensions.'})

    raw = run('root-participating', PARTICIPATING / 'check.py', [])
    got = json.loads(raw)
    (out / 'ROOT_PARTICIPATING_CHECKS.json').write_text(raw)
    require(got == read_json(PARTICIPATING / 'CHECKS.json') and got['passed'] == got['total'] == 8
            and len(got['checks']) == 8 and all(x is True for x in got['checks'].values()),
            'participating root 8-control contract')
    records[-1].update({'controls': 8, 'all_passed': True,
                       'record_byte_identical': raw.encode() == (PARTICIPATING / 'CHECKS.json').read_bytes(),
                       'scope': 'Participating algebra; no independent certification.'})
    require(verify_inventory() == inventory_count, 'post-replay inventory changed')
    receipt = {'status': 'PASS_PORTABLE_EXACT_CONTROLS',
               'optimization_level': sys.flags.optimize,
               'manifest_entries': inventory_count,
               'records': records,
               'historical_author_original_inclusive_controls': 49,
               'original_location_bindings_not_replayed': 6,
               'initial_reviewer_39_control_snapshot': 'Preserved unchanged; historical, not final acceptance.',
               'participating_extension': 'Dc >= 6 E is reviewer-supplied, not independently certified by its originator.',
               'source_bodies_included': False, 'source_reading_renewed': False,
               'protected_state_changed': False, 'integration_or_closure': False}
    (out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
