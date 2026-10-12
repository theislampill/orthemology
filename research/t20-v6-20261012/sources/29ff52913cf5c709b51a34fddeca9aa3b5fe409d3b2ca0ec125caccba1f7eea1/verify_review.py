"""Read-only verification of source/coverage receipts and preservation boundaries."""
from pathlib import Path
from collections import Counter
import hashlib
import json

O = Path(__file__).resolve().parent
W = O.parents[1]
P = W / 't20-consolidation-20261011/projection/package-v4'
L = O.parent / 'later_scopes'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text())

def require(value, label):
    if not value:
        raise RuntimeError(label)

a = load(L / 'RESULT_AUDIT_262.json')
d = load(P / 'coverage/CUMULATIVE_PROGRAMME_CROSSWALK.json')
original = {r['id']: r for r in d['inherited_result_bindings']}
require(len(a) == len({r['id'] for r in a}) == len(original) == 262,
        '262 unique results')
require(set(original) == {r['id'] for r in a}, 'same result population')
require(all(r['original_statement'] == original[r['id']]['inherited_statement']
            for r in a), 'preserved inherited statements')
require(all(r['historical_selected_source_read_ids'] ==
            original[r['id']]['selected_source_read_ids'] for r in a),
        'preserved historical associations')
require(sum(bool(r['historical_selected_source_read_ids']) for r in a) == 77,
        '77 associated results')
counts = Counter(r['audit_classification'] for r in a)
require(dict(counts) == load(L / 'COUNTS_AND_CHECKS.json')['classifications'],
        'first audit class counts')
require(counts['indexed_preserved_reference'] == 169 and
        counts['later_scope_reference_only'] == 1, '170 reference-only rows')

source = load(O / 'SUPPLEMENTAL_READ_T12_TOTAL_INTEGER.json')
f = O / 'INTEGER_TOTAL_REPORT_PROTOCOL_v3.md'
require(sha(f) == source['observed_sha256'] == source['expected_public_sha256'],
        'integer source hash binding')
require(len(f.read_text().splitlines()) == 117, 'integer source 117-line body')
source_binding = next(r for r in d['inherited_source_bindings']
                      if r['id'] == source['source_id'])
require(sha(f) == source_binding['public_sha256'], 'inherited source binding')
require(source['source_id'] in original[source['result_id']]['inherited_statement']['source_ids'],
        'exact source belongs to exact result row')
require(source_binding['public_url'] == source['public_url'], 'exact pinned URL')
require(source['baseline_commit'] in source['public_url'], 'fixed commit pin')

input_checks = [{'path': x['path'], 'hash_matches': sha(W / x['path']) == x['sha256']}
                for x in load(O / 'INPUT_BINDINGS.json')]
require(all(x['hash_matches'] for x in input_checks),
        'review inputs, including first audit, unchanged')
fresh_checks = [{'path': x['file'], 'hash_matches': sha(W / x['file']) == x['sha256']}
                for x in load(L / 'FRESH_READ_BINDINGS.json')]
require(all(x['hash_matches'] for x in fresh_checks), 'first audit fresh source bindings')
initial = load(O / 'V4_PRE_REVIEW_HASHES.json')
current = {str(p.relative_to(P)): sha(p) for p in P.rglob('*') if p.is_file()}
require(current == initial, 'immutable v4 unchanged, including file population')

result = {
    'status': 'PASS',
    'v4_files': len(current),
    'v4_unchanged': current == initial,
    'inherited_rows': 262,
    'historical_associated': 77,
    'historical_unassociated': 185,
    'first_audit_classifications': dict(counts),
    'first_audit_bounded_later_or_fresh_examination': 15,
    'supplemental_exact_source_rows': [source['result_id']],
    'after_this_review_only_bounded_later_or_fresh_examination': 16,
    'after_this_review_only_reference_credit': 169,
    'original_audit_counts_mutated': False,
    'input_checks': input_checks,
    'first_audit_fresh_source_checks': fresh_checks,
    'supplement_source_sha256': sha(f),
    'supplement_source_lines': 117,
    'evidence_ceiling': 'Source and receipt checks only; no whole-programme proof verification or closure authority.'
}
(O / 'VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items()
                  if k not in ['input_checks', 'first_audit_fresh_source_checks']}, indent=2))
