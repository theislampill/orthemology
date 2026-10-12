"""Verify final archive equivalence without claiming to replay its own ZIP."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import importlib.util
import json
import stat
import subprocess
import sys
import zipfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parents[1] / 'research/batch-refinement/delivery/Eighth_Actual_Batch_Controller_Acceptance_v1.zip'
DEST = ROOT / 'final-companion-archive-v1'
ZIP_SHA = '48394ad696250f13be38c3b71074c3f4411090886d7861f12231ff370b4714e5'
FINAL_MANIFEST = '1e7388da4c230cdeeb338b249ccef37e4b7138849faf7a01fddc75d2fedb174f'
TESTED_MANIFEST = 'f084853b8aafc5497567695e1b5e565af7f68baeaa4c85faefa31798922c193e'
FOLDER = 'Eighth_Actual_Batch_Controller_Acceptance'


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def bind(p): return {'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}


def verify_record(base, row):
    p = base / row['path']
    assert p.is_file() and not p.is_symlink()
    assert p.stat().st_size == row.get('bytes', row.get('size')) and sha(p) == row['sha256']


def main():
    assert not DEST.exists()
    assert ARCHIVE.stat().st_size == 419952 and sha(ARCHIVE) == ZIP_SHA
    with zipfile.ZipFile(ARCHIVE) as z:
        rows = z.infolist(); names = [r.filename for r in rows]
        assert len(names) == len(set(names)) == 292
        assert sum(r.file_size for r in rows) == 1950258
        for r in rows:
            p = PurePosixPath(r.filename)
            assert str(p) == r.filename and not p.is_absolute()
            assert p.parts[0] == FOLDER and len(p.parts) > 1
            assert not any(x in ('', '.', '..') for x in p.parts) and '\\' not in r.filename
            assert not r.is_dir() and stat.S_IFMT(r.external_attr >> 16) in (0, stat.S_IFREG)
            assert not r.flag_bits & 1
        DEST.mkdir()
        for r in rows:
            p = DEST / r.filename; p.parent.mkdir(exist_ok=True, parents=True); p.write_bytes(z.read(r))
    base = DEST / FOLDER
    assert sha(base / 'ACCEPTANCE_MANIFEST.json') == FINAL_MANIFEST
    final = load(base / 'ACCEPTANCE_MANIFEST.json')
    paths = [r['path'] for r in final['files']]
    assert len(paths) == len(set(paths)) == 291
    assert {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()} == set(paths) | {'ACCEPTANCE_MANIFEST.json'}
    for row in final['files']: verify_record(base, row)
    oldpath = ROOT / 'STANDALONE_TESTED_COMPANION_MANIFEST.json'
    assert sha(oldpath) == TESTED_MANIFEST
    old = load(oldpath)
    for row in old['files']: verify_record(base, row)
    assert len(old['files']) == 121
    assert (base / 'tested-inputs/ACCEPTANCE_MANIFEST.json').read_bytes() == oldpath.read_bytes()
    assert (base / 'records/STANDALONE_TESTED_COMPANION_MANIFEST.json').read_bytes() == oldpath.read_bytes()
    equivalent = load(base / 'TESTED_INPUT_EQUIVALENCE.json')
    assert equivalent['unchanged_input_files'] == old['files']
    assert equivalent['tested_companion_manifest_sha256'] == TESTED_MANIFEST
    standalone = load(base / 'records/ACTUAL_BATCH_STANDALONE_RECEIPT.json')
    assert sha(base / 'records/ACTUAL_BATCH_STANDALONE_RECEIPT.json') == '5dc4120ff184b3833bb1acf4c6ea02f1cec88f916584f3bb7dda61a03f502793'
    for row in standalone['bound_review_artifacts']: verify_record(base / 'records', row)
    assert len(standalone['bound_review_artifacts']) == 87
    run = ROOT / 'standalone-companion-v2/independent fresh output'
    assert (base / 'independent-replay/RECEIPT.json').read_bytes() == (run / 'RECEIPT.json').read_bytes()
    assert (base / 'independent-replay/source-RECEIPT.json').read_bytes() == (run / 'fresh science/RECEIPT.json').read_bytes()
    for p in (run / 'logs').glob('*.log'):
        assert p.read_bytes() == (base / 'independent-replay/logs' / p.name).read_bytes()
    for p in (run / 'fresh science/logs').glob('*.log'):
        assert p.read_bytes() == (base / 'independent-replay/source-logs' / p.name).read_bytes()
    assert not any(p.suffix in {'.olean', '.ilean', '.so', '.dll', '.dylib', '.pyc'} for p in base.rglob('*'))
    spec = importlib.util.spec_from_file_location('accepted_companion_archive', base / 'replay_review.py')
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    assert helper.verify_companion()[0] == FINAL_MANIFEST
    command = [sys.executable, '-B', str(base / 'test_companion.py')]
    test = subprocess.run(command, cwd='/tmp', text=True, capture_output=True, timeout=30)
    log = DEST / 'contract-tests.log'; log.write_text(test.stdout + test.stderr)
    assert test.returncode == 0 and 'Ran 5 tests' in log.read_text() and 'OK' in log.read_text()
    assert helper.verify_companion()[0] == FINAL_MANIFEST
    source_archive = ARCHIVE.parent / 'Eighth_Actual_Batch_Controller_Source_v5.zip'
    assert sha(source_archive) == standalone['source_zip_sha256']
    result = {'status': 'PASS_FINAL_COMPANION_ARCHIVE_EQUIVALENCE',
        'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'companion_zip_name': ARCHIVE.name, 'companion_zip_bytes': 419952,
        'companion_zip_sha256': ZIP_SHA, 'companion_manifest_sha256': FINAL_MANIFEST,
        'source_zip_sha256': standalone['source_zip_sha256'],
        'tested_execution_manifest_sha256': TESTED_MANIFEST,
        'standalone_acceptance_receipt_sha256': sha(base / 'records/ACTUAL_BATCH_STANDALONE_RECEIPT.json'),
        'regular_zip_members': 292, 'manifest_bound_files': 291,
        'tested_input_files_preserved_exactly': 121, 'appended_packaging_evidence_files': 170,
        'sealed_standalone_bound_artifacts_preserved': 87,
        'safe_archive_extraction': True, 'all_manifest_files_verified': True,
        'all_historical_sealed_bindings_verified': True,
        'independent_replay_aliases_identical': True, 'custom_binary_objects_in_archive': 0,
        'extracted_companion_contract_tests': 5, 'contract_test_cwd': '/tmp',
        'additional_lean_replay_claimed': False,
        'scope': 'Final ZIP byte/inventory equivalence to the independently cold-replayed execution inputs, with declared acceptance evidence appended. This is external to the ZIP; no self-certification or broader scientific closure.',
        'bound_artifacts': [bind(Path(__file__)), bind(log), bind(base / 'ACCEPTANCE_MANIFEST.json'), bind(base / 'TESTED_INPUT_EQUIVALENCE.json')]}
    output = ROOT / 'ACTUAL_BATCH_FINAL_ARCHIVE_RECEIPT.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'bound_artifacts'}, indent=2))
    print('receipt_sha256', sha(output))


if __name__ == '__main__': main()
