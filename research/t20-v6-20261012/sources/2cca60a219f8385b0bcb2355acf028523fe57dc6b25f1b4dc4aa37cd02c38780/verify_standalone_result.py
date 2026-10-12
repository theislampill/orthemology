"""Read-only, independent binding checks for the recorded portable replay.

This does not run Lean or manufacture a replay result. It validates the completed
source and reviewer receipts against their actual archives, inputs, logs and
fresh objects, then writes a separate mechanical evidence record.
"""
from pathlib import Path
import datetime
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'standalone-companion-v2'
OUT = RUN / 'independent fresh output'
INPUT = RUN / 'companion inputs with spaces'
SOURCE = OUT / 'extracted source/Eighth_Actual_Batch_Controller_Source'
ZIP_HASH = '19f90a7bfd9bd2840c71c972029447533e9f5985281c275c5c0979ff8597f906'
MANIFEST_HASH = 'f084853b8aafc5497567695e1b5e565af7f68baeaa4c85faefa31798922c193e'
PUBLIC_HASH = '6acd4dc584cb37c7c9e168dd71f912f96cd31fedc9f408fdb8742450462dc9fa'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text())


def record(p):
    return {'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}


def files(base):
    assert all(not p.is_symlink() for p in base.rglob('*'))
    return {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}


def inventory(base, manifest_name, identity):
    assert sha(base / manifest_name) == identity
    rows = load(base / manifest_name)['files']
    names = [r['path'] for r in rows]
    assert len(names) == len(set(names))
    assert files(base) == set(names) | {manifest_name}
    for row in rows:
        p = base / row['path']
        assert p.stat().st_size == row.get('bytes', row.get('size'))
        assert sha(p) == row['sha256']


def axioms(log, expected, receipt):
    text = log.read_text()
    observed = {}
    pattern = r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^]]*)\])"
    matches = list(re.finditer(pattern, text))
    for match in matches:
        name, raw = match.groups()
        assert name not in observed
        vals = sorted(x.strip() for x in (raw or '').split(',') if x.strip())
        assert set(vals) <= {'propext', 'Classical.choice', 'Quot.sound'}
        observed[name] = vals
    assert re.sub(pattern, '', text).strip() == ''
    assert set(observed) == set(expected) and len(observed) == len(expected)
    assert observed == receipt


def stages(base, rows, build, expected_modules):
    assert [r['module'] for r in rows] == expected_modules
    object_names = set()
    for row in rows:
        assert row['exit_code'] == 0 and row['timed_out'] is False
        log = base / 'logs' / ('version.log' if row['module'] == 'compiler_version' else row['module'] + '.log')
        assert sha(log) == row['log_sha256']
        assert not re.search(r'error|warning|sorryax|out of memory|stack overflow|replay_timeout', log.read_text(), re.I)
        if 'source_sha256' in row:
            assert sha(row['command'][-1]) == row['source_sha256']
            obj = build / (row['module'] + '.olean')
            assert sha(obj) == row['object_sha256']
            assert Path(row['command'][row['command'].index('-o') + 1]) == obj
            object_names.add(obj.name)
        assert Path(row['command'][0]).name == 'lean'
    assert files(build) == object_names


def main():
    archive = RUN / 'source input archive.zip'
    assert sha(archive) == ZIP_HASH and archive.stat().st_size == 2438940
    public_archive = ROOT.parents[1] / 'research/batch-refinement/delivery/Eighth_Actual_Batch_Controller_Source_v5.zip'
    assert sha(public_archive) == ZIP_HASH
    inventory(INPUT, 'ACCEPTANCE_MANIFEST.json', MANIFEST_HASH)
    inventory(SOURCE, 'PUBLIC_MANIFEST.json', PUBLIC_HASH)
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == 109
        assert {str(Path(n).relative_to('Eighth_Actual_Batch_Controller_Source')) for n in names} == files(SOURCE)
        for name in names:
            assert z.read(name) == (SOURCE / Path(name).relative_to('Eighth_Actual_Batch_Controller_Source')).read_bytes()
    launch = load(RUN / 'LAUNCH_BINDING.json')
    assert sha(RUN / 'launch_independent.py') == launch['launch_script_sha256']
    assert sha(INPUT / 'replay_review.py') == launch['tested_entrypoint_sha256']
    for name, digest in launch['nonexecuting_shadow_objects'].items():
        assert sha(RUN / 'unrelated caller cwd' / name) == digest
    assert list(RUN.glob('unexpected-*')) == []
    assert not list(OUT.rglob('REPLAY_FAILURE.json'))
    science = load(OUT / 'fresh science/RECEIPT.json')
    review = load(OUT / 'RECEIPT.json')
    assert science['status'] == review['status'] == 'PASS'
    assert review['source_replay_receipt_sha256'] == sha(OUT / 'fresh science/RECEIPT.json')
    assert review['source_zip_sha256'] == ZIP_HASH
    assert review['companion_manifest_sha256'] == MANIFEST_HASH
    assert science['public_manifest_sha256'] == review['source_public_manifest_sha256'] == PUBLIC_HASH
    assert science['prior_custom_objects_reused'] == review['prior_scientific_objects_reused'] == 0
    assert science['dependencies_checked_before_after'] and not science['dependencies_mutated'] and not review['dependencies_mutated']
    assert len(science['metadata_relocations_used']) == 5
    assert all(not r['actual_file_mutated'] and r['replacement_count'] == 1 for r in science['metadata_relocations_used'])
    index = load(SOURCE / 'SOURCE_INDEX.json')
    order = load(INPUT / 'records/REVIEW_SOURCE_ORDER_V4.json')
    snames = [d['name'] for m in index['modules'] for d in m['declarations']]
    rnames = [d['name'] for m in order['modules'] for d in m['named_explicit_declarations']]
    assert len(index['modules']) == 61 and len(order['modules']) == 9
    assert len(snames) == len(set(snames)) == 902
    assert len(rnames) == len(set(rnames)) == 78
    assert sum(d['kind'] == 'theorem' for m in index['modules'] if m['author_science'] for d in m['declarations']) == 476
    assert sum(d['kind'] == 'theorem' for m in order['modules'] for d in m['named_explicit_declarations']) == 47
    stages(OUT / 'fresh science', science['stages'], OUT / 'fresh science/build',
           ['compiler_version'] + [m['module'] for m in index['modules']] + ['AllNamedDeclarations'])
    stages(OUT, review['stages'], OUT / 'fresh review',
           [m['module'] for m in order['modules']] + ['ReviewerNamedDeclarations'])
    axioms(OUT / 'fresh science/logs/AllNamedDeclarations.log', snames, science['declaration_axioms'])
    axioms(OUT / 'logs/ReviewerNamedDeclarations.log', rnames, review['reviewer_axioms'])
    result = {'status': 'PASS_INDEPENDENT_POST_REPLAY_BINDINGS',
        'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'fresh_source_modules': 61, 'fresh_review_modules': 9,
        'fresh_named_declaration_audit_modules': 2, 'compiler_version_checks': 1,
        'scientific_named_declarations': 902, 'reviewer_named_declarations': 78,
        'author_theorems': 476, 'reviewer_theorems': 47,
        'fresh_objects_bound': 72, 'compiler_logs_bound': 73,
        'combined_compiler_seconds': round(sum(r['seconds'] for r in science['stages'] + review['stages']), 3),
        'source_archive_entries_exactly_equal_extraction': 109,
        'hostile_environment_sentinels_created': [], 'nonexecuting_poison_objects_unchanged': True,
        'input_manifest_and_source_archive_unchanged': True,
        'source_and_review_axiom_log_records_exact': True,
        'artifacts': [record(p) for p in [Path(__file__), RUN / 'LAUNCH_BINDING.json', RUN / 'launch_independent.py',
            RUN / 'console.log', OUT / 'RECEIPT.json', OUT / 'fresh science/RECEIPT.json']]}
    (ROOT / 'STANDALONE_POST_REPLAY_BINDINGS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'artifacts'}, indent=2))


if __name__ == '__main__':
    main()
