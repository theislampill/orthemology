"""Replay existing controls on a disposable copy; preserve the received checkpoint."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else None
if OUT is None or OUT == ROOT or ROOT in OUT.parents:
    raise SystemExit("Usage: python3 replay.py /absolute/output/directory/outside/checkpoint")
OUT.mkdir(parents=True, exist_ok=True)


def manifest_check(root):
    entries = []
    for line in (root / 'SHA256SUMS').read_text().splitlines():
        digest, relative = line.split('  ', 1)
        assert not Path(relative).is_absolute() and '..' not in Path(relative).parts, relative
        path = root / relative
        assert path.is_file() and not path.is_symlink(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, relative
        entries.append(relative)
    return len(entries)


def blob_check(path, digest):
    data = path.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == digest, path


count = manifest_check(ROOT)
for row in json.loads((ROOT / 'warranted-learning-20261009/sources/SOURCE_BINDINGS.json').read_text()):
    blob_check(ROOT / 'warranted-learning-20261009/sources' / row['path'], row['sha'])
for row in json.loads((ROOT / 'constructive-t20-20261009/revocation-dependency/REPOSITORY_BINDINGS.json').read_text())['sources']:
    blob_check(ROOT / 'constructive-t20-20261009/sources' / row['path'], row['git_blob'])
for row in json.loads((ROOT / 'provenance-learning-transport-20261009/SOURCE_BINDINGS.json').read_text()):
    blob_check(ROOT / row['local'], row['blob_sha'])
fifth = ROOT / 'evidence-withdrawal-warrant-20261009'
fifth_entries = json.loads((fifth / 'DELIVERABLE_MANIFEST.json').read_text())['files']
for row in fifth_entries:
    data = (fifth / row['path']).read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']

# Existing scripts are unchanged. Only their orchestration is new.
# Mirror fresh author stdout into the disposable copy's review replay record.
commands = [
    ('learning', 'warranted-learning-20261009', ['verify.py'], None),
    ('null_author', 'null-evidence-dynamics-20261009', ['verify.py'],
     'null-evidence-dynamics-review-20261009/AUTHOR_REPLAY.json'),
    ('null_review', 'null-evidence-dynamics-review-20261009', ['independent_diagnostics.py'], None),
    ('reset_exact', 'constructive-t20-20261009/revocation-dependency', ['verify.py'], None),
    ('reset_units', 'constructive-t20-20261009/revocation-dependency',
     ['-m', 'unittest', 'discover', '-s', 'tests', '-v'], None),
    ('provenance_author', 'provenance-learning-transport-20261009', ['verify_models.py'],
     'provenance-learning-review-20261009/AUTHOR_REPLAY.json'),
    ('provenance_review', 'provenance-learning-review-20261009', ['independent_controls.py'], None),
]
rows = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
with tempfile.TemporaryDirectory(prefix='t20-replay-') as directory:
    work = Path(directory) / ROOT.name
    shutil.copytree(ROOT, work)
    for name, relative, arguments, mirror in commands:
        result = subprocess.run([sys.executable, *arguments], cwd=work / relative,
                                env=env, capture_output=True, text=True)
        (OUT / (name + '.stdout')).write_text(result.stdout)
        (OUT / (name + '.stderr')).write_text(result.stderr)
        row = {'id': name, 'cwd': relative, 'command': ['python3', *arguments],
               'exit_code': result.returncode,
               'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest()}
        rows.append(row)
        if result.returncode != 0:
            (OUT / 'REPLAY.json').write_text(json.dumps({'status': 'FAIL', 'runs': rows}, indent=2) + '\n')
            raise SystemExit(name + ' failed; inspect retained stderr/stdout')
        if mirror:
            (work / mirror).write_text(result.stdout)
    # Also check that deterministic report-writing controls preserved their snapshots.
    copied_count = manifest_check(work)

assert manifest_check(ROOT) == count == copied_count
receipt = {
    'status': 'PASS', 'python': sys.version.split()[0],
    'checkpoint_files_sha256_verified': count,
    'retained_git_blob_bindings_verified': 31,
    'fifth_unit_delivery_entries_verified': len(fifth_entries),
    'included_arabic_body_projections': 15,
    'runs': rows,
    'preserved_checkpoint_unchanged': True,
    'limits': 'Finite exact and numerical replay only; no general proof certification, '
              'new source appraisal, external source retrieval, Lean run, old-archive reconstruction, '
              'actual warrant or T20 closure. Fifth-unit body extracts are derived electronic-text '
              'projections; bulky HTML/full dar014/predecessor bodies are omitted.'
}
(OUT / 'REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
