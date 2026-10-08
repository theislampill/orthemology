"""Synthetic successor records; no fixture carries research acceptance credit."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

AREA = 'experiments/orthemology-v5-successors'
PROV = 'docs/provenance/v5-successors'
OLD = 'experiments/orthemology-v5-continuations'
OLDPROV = 'docs/provenance/v5-research-continuations'
BASE = '1' * 40
TREE = '2' * 40


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def raw_hash(raw):
    return hashlib.sha256(raw).hexdigest()


def put_bytes(root, path, raw):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return raw_hash(raw)


def put(root, path, value):
    return put_bytes(root, path, (json.dumps(value, indent=2, ensure_ascii=False,
                                            allow_nan=False) + '\n').encode())


def source(root, sid, raw, name):
    checksum = raw_hash(raw)
    path = f'{AREA}/source-store/{checksum}/{name}'
    put_bytes(root, path, raw)
    return {'id': sid, 'origin_input_id': 'T07-FIXTURE', 'origin_input_sha256': 'a' * 64,
            'origin_archive_sha256': 'b' * 64, 'member_chain': [name],
            'original_sha256': checksum, 'original_bytes': len(raw),
            'public_path': path, 'public_sha256': checksum, 'public_bytes': len(raw),
            'projection': 'EXACT', 'projection_basis': 'Synthetic exact source.',
            'review_scope': 'Synthetic declared statement only.', 'derivation': None}


def documents(bundle):
    return {'BASELINE_BINDING': bundle['baseline_binding'],
            'PRESERVATION': bundle['preservation'],
            'SOURCE_MAP': {'sources': bundle['sources'], 'reviews': bundle['reviews']},
            'RESULT_STATUS': {'results': bundle['results'], 'statuses': bundle['statuses']},
            'EVIDENCE_BINDINGS': {'bindings': bundle['bindings'], 'receipts': bundle['receipts']},
            'SUPERSESSION': {'edges': bundle['supersession'], 'selectors': bundle['selectors'],
                            'legacy_endpoints': bundle['legacy_endpoints']},
            'OBLIGATION_CROSSWALK': {'obligations': bundle['obligations']},
            'TWELVE_AVENUES': {'avenues': bundle['avenues']},
            'CALCULUS_MAP': {'results': bundle['calculus']},
            'EMPIRICAL_SCOPE': {'results': bundle['empirical']},
            'PUBLIC_PROJECTION': {'reviews': bundle['projection_reviews'], 'allowlist': bundle['public_allowlist']},
            **bundle['supplementary']}


def save_bundle(root, bundle):
    records = {}
    for name, value in documents(bundle).items():
        path = f'{PROV}/{name}.json'
        records[name] = {'path': path, 'sha256': put(root, path, value)}
    for suite in bundle['suites']:
        path = f"{AREA}/suites/{suite['id']}.json"
        records['suite:' + suite['id']] = {'path': path, 'sha256': put(root, path, suite)}
    bundle['registry']['records'] = records
    put(root, f'{AREA}/registry.json', bundle['registry'])


def rebind(bundle):
    sources = {s['id']: s for s in bundle['sources']}
    reviews = {r['id']: r for r in bundle['reviews']}
    suites = {s['id']: s for s in bundle['suites']}
    statuses = {s['id']: s for s in bundle['statuses']}
    bundle['bindings'] = []
    for row in bundle['results']:
        suite_targets = []
        for sid in row['suite_ids']:
            suite_targets.append({'suite_id': sid, 'target_ids': [t['id'] for t in suites[sid]['targets']
                                  if t['source_id'] in row['source_ids']]})
        bundle['bindings'].append({'id': row['id'], 'statement_sha256': digest(row),
            'sources': {sid: {**{k: sources[sid][k] for k in ['original_sha256', 'public_sha256']},
                              'projection_review_sha256': next((digest(p) for p in bundle['projection_reviews']
                                  if sources[sid]['derivation'] and p['id'] == sources[sid]['derivation']['review_id']), None)}
                        for sid in row['source_ids']},
            'reviews': {rid: reviews[rid]['review_sha256'] for rid in row['review_ids']},
            'suite_targets': suite_targets, 'receipt_ids': list(statuses[row['id']]['receipt_ids']),
            'receipts': {rec['id']: digest(rec) for rec in bundle['receipts']
                         if rec['id'] in statuses[row['id']]['receipt_ids']}})
    bundle['registry']['result_ids'] = [r['id'] for r in bundle['results']]
    bundle['registry']['suite_ids'] = [s['id'] for s in bundle['suites']]
    for selector in bundle['selectors']:
        result = next(r for r in bundle['results'] if r['id'] == selector['result_id'])
        selector['statement_sha256'] = digest(result)


def make_bundle(root):
    files = []
    for path, raw in [(OLD + '/registry.json', b'{"fixture":"legacy"}\n'),
                      (OLDPROV + '/SIXTH_FINAL_OVERLAY.json', b'{"fixture":"overlay"}\n')]:
        checksum = put_bytes(root, path, raw)
        git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        files.append({'path': path, 'bytes': len(raw), 'sha256': checksum, 'git_blob_sha1': git_blob})
    files.sort(key=lambda f: f['path'])
    preservation = {'schema': 'orthemology-v5-preservation-v1', 'base_commit': BASE,
                    'base_tree': TREE, 'roots': [OLD, OLDPROV], 'files': files}
    preservation_sha = put(root, PROV + '/PRESERVATION.json', preservation)
    binding = {'schema': 'orthemology-v5-baseline-binding-v1', 'base_commit': BASE,
               'base_tree': TREE, 'preservation_sha256': preservation_sha,
               'legacy_registry': {'path': OLD + '/registry.json', 'sha256': raw_hash((root / OLD / 'registry.json').read_bytes())},
               'legacy_overlay': {'path': OLDPROV + '/SIXTH_FINAL_OVERLAY.json', 'sha256': raw_hash((root / OLDPROV / 'SIXTH_FINAL_OVERLAY.json').read_bytes())}}
    src = source(root, 'source-proof', b'namespace Demo\ntheorem ok : True := True.intro\nend Demo\n', 'Proof.lean')
    rev = source(root, 'source-review', b'Review: the declared True statement is checked at its scope.\n', 'Review.md')
    result = {'id': 'T07-FIXTURE', 'title': 'Synthetic scoped theorem', 'tranche': 7,
              'family': 'fixture-family', 'original_avenues': [1], 'evidence_keys': ['fixture-key'],
              'target': 'theorem ok : True := True.intro', 'input_contract': 'No runtime inputs.',
              'assumptions': [], 'conclusion': 'True in the declared logical model.',
              'limitations': ['No empirical, operational or adoption claim.'], 'calculus': 'NONE',
              'operational_model': 'Lean logical proposition.', 'math_form': 'FORMAL',
              'claim_scope': 'DECLARED_SUITE', 'domain': 'SOURCE_TEXT',
              'source_ids': ['source-proof'], 'review_ids': ['review-a'], 'suite_ids': [],
              'origin_status': 'Synthetic fixture only.', 'obligation_ids': [],
              'residual_scope': 'No general research claim.'}
    review = {'id': 'review-a', 'source_id': 'source-review', 'reviewed_source_ids': ['source-proof'],
              'target': result['target'], 'scope': 'Synthetic declared theorem only.',
              'outcome': 'REVIEWED_AT_SCOPE', 'review_sha256': rev['public_sha256']}
    status = {'id': result['id'], 'custody': 'EXACT', 'inherited_evidence': 'WRITTEN_MATHEMATICS',
              'fresh_evidence': 'NOT_RUN', 'research_disposition': 'CANDIDATE',
              'implementation_reach': 'NONE', 'external_warrants': {k: 'NOT_ESTABLISHED' for k in
              ['actual_world', 'normative', 'empirical_replication', 'specialist_review', 'novelty', 'terminology_adoption']},
              'receipt_ids': [], 'independent_evidence_count': 1}
    bundle = {'registry': {'schema': 'orthemology-v5-successors-v1', 'programme': 'Orthemology v5',
                           'cutoff': 'fifteenth-final', 'baseline_commit': BASE, 'baseline_tree': TREE,
                           'records': {}, 'suite_ids': [], 'result_ids': [result['id']]},
              'baseline_binding': binding, 'preservation': preservation,
              'sources': [src, rev], 'reviews': [review], 'results': [result], 'statuses': [status],
              'bindings': [], 'suites': [], 'receipts': [], 'supersession': [], 'legacy_endpoints': [],
              'selectors': [{'family': result['family'], 'result_id': result['id'], 'statement_sha256': digest(result)}],
              'obligations': [], 'avenues': [{'number': n, 'result_ids': [result['id']] if n == 1 else [],
                  'disposition': 'SCOPED_SUCCESSORS' if n == 1 else 'NO_NEW_RESULT',
                  'scope': 'Synthetic fixture scope.'} for n in range(1, 13)],
              'calculus': [{'id': result['id'], 'calculus': 'NONE', 'operational_model': result['operational_model'],
                           'canonical_adoption': 'NOT_ADOPTED'}],
              'empirical': [], 'supplementary': {}, 'projection_reviews': [],
              'public_allowlist': [{'path': s['public_path'], 'sha256': s['public_sha256'], 'bytes': s['public_bytes'],
                                    'kind': 'SOURCE', 'source_ids': [s['id']]} for s in [src, rev]]}
    rebind(bundle)
    save_bundle(root, bundle)
    anchor = {k: deepcopy(v) for k, v in binding.items() if k != 'schema'}
    anchor['git_required'] = False
    return bundle, anchor


def add_suite(root, bundle):
    row = bundle['results'][0]
    source_row = bundle['sources'][0]
    target = {'id': 'target-ok', 'source_id': source_row['id'], 'declaration': row['target'],
              'target_sha256': raw_hash(row['target'].encode()), 'domain': row['domain'], 'calculus': row['calculus']}
    controls = [{'id': cid, 'source_id': source_row['id'], 'target_id': target['id'],
                 'role': 'POSITIVE' if outcome == 'ACCEPT' else 'MUTATION_REJECTION',
                 'expected_outcome': outcome, 'expected_outcome_sha256': raw_hash(outcome.encode())}
                for cid, outcome in [('positive', 'ACCEPT'), ('negative', 'REJECT')]]
    toolchain = {'kind': 'LEAN', 'version': '4.19.0', 'platform': 'linux-x86_64',
                 'executable_sha256': '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
                 'packages': []}
    suite = {'id': 'fixture-suite', 'family': row['family'], 'result_families': [row['family']], 'origin_archive_sha256': 'b' * 64,
             'source_ids': [source_row['id']], 'review_ids': ['review-a'], 'targets': [target],
             'controls': controls, 'toolchain': toolchain, 'replay': {'schema': 'synthetic-unit-fixture-v1'}}
    receipt = {'id': 'receipt-a', 'suite_id': suite['id'], 'family': suite['family'],
               'suite_sha256': digest(suite), 'source_hashes': {source_row['id']: source_row['public_sha256']},
               'review_hashes': {'review-a': bundle['reviews'][0]['review_sha256']},
               'toolchain_sha256': digest(toolchain), 'outcome': 'QUALIFIED_DECLARED_SUITE',
               'target_readbacks': [{'target_id': target['id'], 'source_id': target['source_id'],
                                     'target_sha256': target['target_sha256'], 'outcome': 'CHECKED'}],
               'controls': [{'id': c['id'], 'source_id': c['source_id'], 'target_id': c['target_id'], 'role': c['role'],
                              'expected_outcome_sha256': c['expected_outcome_sha256'],
                              'actual_outcome': c['expected_outcome'], 'actual_outcome_sha256': c['expected_outcome_sha256'],
                              'terminal': 'COMPLETED', 'exit_code': 0 if c['expected_outcome'] == 'ACCEPT' else 1,
                              'log_sha256': 'c' * 64} for c in controls],
               'stages': [{'id': 'compile', 'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': 'd' * 64}],
               'invocation': ['lean', 'Proof.lean'], 'started_at': '2026-10-05T00:00:00Z',
               'ended_at': '2026-10-05T00:00:01Z', 'exit_code': 0, 'log_sha256': 'e' * 64,
               'axioms': [], 'proof_scope': 'DECLARED_SUITE',
               'replay_evidence': {'schema': 'synthetic-unit-receipt-v1'}}
    bundle['suites'] = [suite]
    bundle['receipts'] = [receipt]
    row['suite_ids'] = [suite['id']]
    bundle['statuses'][0].update(fresh_evidence='QUALIFIED_DECLARED_SUITE',
                                  implementation_reach='DECLARED_FORMAL_SUITE', receipt_ids=[receipt['id']])
    rebind(bundle)
    save_bundle(root, bundle)
    return suite, receipt


def fixture_suite_validator(suite, sources, root):
    if suite['replay'] != {'schema': 'synthetic-unit-fixture-v1'}:
        raise ValueError('Unknown synthetic fixture replay contract')


def fixture_receipt_validator(receipt, suite, sources, root):
    if receipt['replay_evidence'] != {'schema': 'synthetic-unit-receipt-v1'}:
        raise ValueError('Unknown synthetic fixture receipt contract')
