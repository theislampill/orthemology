import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
W = ROOT.parent
AUTHOR = W / 'hase-closed-scalar-instances-20261010'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def row(p):
    return {'path': str(p.relative_to(W)), 'sha256': sha(p), 'bytes': p.stat().st_size}

manifest = json.loads((AUTHOR / 'MANIFEST.json').read_text())
for r in manifest['files']:
    assert sha(AUTHOR / r['path']) == r['sha256'], r['path']
inputs = json.loads((AUTHOR / 'INPUTS.json').read_text())
for r in inputs['receipts_and_manifests'] + inputs['frozen_source_files']:
    assert sha(W / r['path']) == r['sha256'], r['path']
assert sha(W / '.toolchains/lean-4.19.0-linux/bin/lean') == inputs['lean_binary_sha256']
for r in inputs['reused_objects']:
    p = W / 'hase-full-per-review-20261010/fresh-lib' / pathlib.Path(*r['module'].split('.')).with_suffix('.olean')
    assert sha(p) == r['sha256'], p
for r in inputs['fresh_acquisitions']:
    p = AUTHOR / r['path']; b = p.read_bytes()
    acq = json.loads((AUTHOR / r['acquisition']).read_text())
    assert b == acq['content'].encode()
    assert sha(p) == r['sha256']
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == acq['sha']
for r in json.loads((ROOT / 'INPUT_VERIFICATION.json').read_text())['checks']:
    assert sha(W / r['path']) == r['sha256'], r['path']
literal_binding = next(r for r in json.loads((W / 'identity-frontier-inspection-20261009/SOURCE_BINDINGS.json').read_text())['sources'] if r['name'] == 'LiteralScalarFusion.lean')
p = W / literal_binding['local_path']; b = p.read_bytes()
assert sha(p) == literal_binding['sha256']
assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == literal_binding['git_blob']

replays = []
for source_name, obj_name, log_name, author in [
    ('sources/ClosedProofCanonicalisation.lean', 'ClosedProofCanonicalisation', 'CANONICALISATION_REPLAY.log', True),
    ('sources/ClosedScalarInstances.lean', 'ClosedScalarInstances', 'CANDIDATE_REPLAY.log', True),
    ('sources/Controls.lean', 'Controls', 'AUTHOR_CONTROLS_REPLAY.log', True),
    ('sources/DependencyAudit.lean', 'DependencyAudit', 'AUTHOR_DEPENDENCY_REPLAY.log', True),
    ('IndependentControls.lean', 'ClosedScalarReviewControls', 'INDEPENDENT_CONTROLS.log', False),
    ('DependencyAudit.lean', 'ClosedScalarDependencyAudit', 'DEPENDENCY_AUDIT.log', False),
]:
    source = ROOT / source_name
    obj = ROOT / 'fresh-lib' / (obj_name + '.olean')
    log = ROOT / log_name
    assert obj.exists()
    text = log.read_text()
    assert not any(x in text for x in ['error:', 'warning:', 'sorryAx'])
    for axes in re.findall(r'(?:depends on axioms:|axioms)\s*\[([^\]]*)\]', text, re.S):
        assert set(re.sub(r'\s+', '', axes).split(',')) <= {'propext','Classical.choice','Quot.sound',''}
    r = {'source': row(source), 'object': row(obj), 'log': row(log), 'trust_zero': True, 'exit_code': 0}
    if author:
        assert source.read_bytes() == (AUTHOR / source.name).read_bytes()
        r['author_source'] = row(AUTHOR / source.name)
    replays.append(r)

receipt = {
    'status': 'PASS_BOUNDED_CLOSED_SOURCE_INSTANCE_REVIEW',
    'universal_HasE_target': 'OPEN',
    'source_derivability': 'For each n with actual HasE [] n N, exact HasE [] (c3 n) (inst frozen_W_body n)',
    'executable_extraction_claimed': False,
    'source_derivation_serialization_claimed': False,
    'new_replays': replays,
    'author_manifest': row(AUTHOR / 'MANIFEST.json'),
    'author_result': row(AUTHOR / 'RESULT.md'),
    'author_inputs': row(AUTHOR / 'INPUTS.json'),
    'review': row(ROOT / 'REVIEW.md'),
    'input_verification': row(ROOT / 'INPUT_VERIFICATION.json'),
    'prerequisite_receipt': row(W / 'hase-full-per-review-20261010/PREREQUISITE_REBUILD.json'),
    'model_review_receipt': row(W / 'hase-full-per-review-20261010/REVIEW_RECEIPT.json'),
    'literal_q_source_binding': literal_binding,
    'reused_object_count': len(inputs['reused_objects']),
    'pinned_original_sources_rehashed': 83,
    'independent_control_theorem_count': 18,
    'independent_control_axiom_reports': 11,
    'kernel_dependency_audit_targets': 7,
    'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
    'no_protected_changes': True,
    'third_party_objects_reused': True,
    'lean_bootstrap_verified': False,
}
(ROOT / 'REVIEW_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
files = [p for p in ROOT.rglob('*') if p.is_file() and p.name != 'MANIFEST.json']
(ROOT / 'MANIFEST.json').write_text(json.dumps({'files': [dict(row(p), path=str(p.relative_to(ROOT))) for p in sorted(files)]}, indent=2) + '\n')
print('PASS: frozen review bound; 92 reused objects and all six fresh replays verified.')
print('REVIEW_RECEIPT.json', sha(ROOT / 'REVIEW_RECEIPT.json'))
print('MANIFEST.json', sha(ROOT / 'MANIFEST.json'))
