#!/usr/bin/env python3
"""Read-only replay of 70 byte bindings and 12 occurrence assertions.

Original verification code for the Fourteenth occurrence-correspondence result.
Accepts separately obtained source files; does not import or execute their code.
Uses only the Python standard library. No network or source writes.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


class VerificationError(Exception):
    """A bounded verification failure, reported without local absolute paths."""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def ph(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':')).encode())


def verify(source):
    if not source.is_dir():
        raise VerificationError('source directory is missing or is not a directory')
    lock_path = Path(__file__).resolve().with_name('source-lock.json')
    try:
        custody = json.loads(lock_path.read_text(encoding='utf-8'))['files']
    except (OSError, ValueError, KeyError, TypeError):
        raise VerificationError('source-lock.json is missing or malformed') from None
    if not isinstance(custody, list) or len(custody) != 70:
        raise VerificationError('source-lock.json must contain the exact 70-file closure')
    checks = []
    blobs = {}

    def check(name, ok):
        checks.append({'check': name, 'pass': bool(ok)})
        if not ok:
            raise VerificationError(name)

    for r in custody:
        relative = PurePosixPath(r['path'])
        if (relative.is_absolute() or '..' in relative.parts or
                relative.as_posix() != r['path'] or r['path'] in blobs):
            raise VerificationError('source-lock.json has an invalid relative path')
        try:
            b = source.joinpath(*relative.parts).read_bytes()
        except OSError:
            raise VerificationError('missing or unreadable locked file: ' + r['path']) from None
        check('custody:' + r['path'], sha(b) == r['sha256'] and
              len(b) == r['bytes'] and
              hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == r['blob_sha1'])
        blobs[r['path']] = b

    # Parse only the exact bytes already checked above, never a second disk read.
    def rows(path):
        return [json.loads(s) for s in blobs[path.as_posix()].decode('utf-8').splitlines() if s.strip()]

    p = Path('qamus/examples/p007-li-pilot')
    loc = 'quran:61:5:4'
    projection = next(r for r in rows(p / 'projections.jsonl') if r['projection']['occurrence_id'] == loc)
    edges = [r for r in rows(p / 'transclusion-edges.jsonl') if r['details']['occurrence_id'] == loc]
    facts = [r for r in rows(p / 'typed-facts.jsonl') if any(s.get('quran_loc') == loc for s in r.get('surface_spans', [])) or r['fact_type'] == 'particle_rootlessness']
    lattice = next(r for r in rows(p / 'candidate-lattice.jsonl') if r['occurrence_id'] == loc)
    check('exact projection hash', ph(projection['projection']) == projection['projection_hash'])
    check('four appearances same hash', len(projection['appearances']) == 4 and all(r['projection_hash'] == projection['projection_hash'] for r in projection['appearances']))
    check('certified entry versus candidate sense', any(r['edge_type'] == 'particle_entry_certified_edge' and r['status'] == 'certified' for r in edges) and any(r['edge_type'] == 'particle_sense_candidate_edge' and r['status'] == 'candidate' and not r['details'].get('evidence_bundle_ref') for r in edges) and not any(r['edge_type'] == 'particle_sense_certified_edge' for r in edges))
    check('governor relation withheld', projection['projection']['certification_plane']['governor_relation'] == 'unresolved' and 'relation' not in projection['projection']['hover_cards'][0]['governor'])
    check('both unresolved dependencies preserved', set(projection['projection']['unresolved_dependencies']) == {'occurrence_to_sense_certification', 'governor_relation_governed_key'})
    check('alternative discovery retained', len(lattice['segmentation_candidates']) == 2 and len(lattice['function_candidates']) == 4)
    mut = copy.deepcopy(projection['projection'])
    mut['certification_plane']['sense'] = 'certified'
    check('sense status enters hash', ph(mut) != projection['projection_hash'])
    state = {}
    for e in rows(p / 'certification/events.jsonl'):
        state[e['fact_id']] = e['to_status']
    check('five relevant facts currently certified', len(facts) == 5 and all(state[f['fact_id']] == 'certified' for f in facts))
    check('legacy replaced not erased', all(state['fact:p00slice:61_5_4:' + k] == 'review_required' and state['fact:p00slice:61_5_4:' + k + ':v2'] == 'certified' for k in ['func', 'gov', 'case']))
    can = json.loads(blobs['qamus/examples/website-payloads/multi_entry_liqawmihi_61_5_4.payload.json'])
    check('canary is separate candidate provenance', can['artifact_id'] == 'artifact:vncanary:61:5:4' and can['projection']['certification']['status'] == 'candidate' and can['provenance']['provenance_class'] == 'illustrative-from-live')
    check('canary relation kinds remain distinct', [l['relation_kind'] for l in can['projection']['entry_links']] == ['clitic_component_of_entry', 'candidate_entry', 'root_family_of_entry'])
    check('canary is not byte-identical pilot projection', can['projection_hash'] != projection['projection_hash'] and can['projection']['surface'] != projection['projection']['surface'])
    return {
        'status': 'PASS',
        'scope': 'held-byte data assertions only; no linguistic or global regression certification',
        'custody_files_checked': len(custody),
        'checks': checks,
        'query': {
            'occurrence': loc,
            'morpheme': 'mocc:p007:61:5:4',
            'projection_hash': projection['projection_hash'],
            'appearances': [r['appearance_id'] for r in projection['appearances']],
            'fact_ids': [r['fact_id'] for r in facts],
            'certification_plane': projection['projection']['certification_plane'],
            'canary_artifact': can['artifact_id'],
            'canary_hash': can['projection_hash'],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir', type=Path,
                        help='root of the separately obtained pinned source directory')
    args = parser.parse_args()
    try:
        result = verify(args.source_dir)
    except VerificationError as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}, sort_keys=True))
        return 1
    except (KeyError, TypeError, ValueError, StopIteration):
        print(json.dumps({'status': 'FAIL', 'reason': 'malformed lock or unexpected pinned data shape'}, sort_keys=True))
        return 1
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
