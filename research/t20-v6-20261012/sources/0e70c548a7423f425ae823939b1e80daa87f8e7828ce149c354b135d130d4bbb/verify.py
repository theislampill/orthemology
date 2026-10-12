#!/usr/bin/env python3
"""Narrow pinned fresh-output replay. Does not build retained dependencies."""
import datetime
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
WORK = ROOT.parent
MODULES = ['FiniteCorrectionTable', 'SourceSidecarController', 'SourceObservableMinimum',
           'SourceCorrectionHistories', 'FiniteSidecarControls', 'FiniteSidecarAudit']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = ROOT / 'SOURCE_BOUNDARY.json'
    data = json.loads(manifest.read_text())
    def verify_pins():
        for row in data['retained'] + data['additive']:
            path = WORK / row['path']
            if not path.is_file() or sha(path) != row['sha256']:
                raise RuntimeError('Input changed or missing: ' + row['path'])
        frozen = json.loads((ROOT / 'CANDIDATE_FREEZE.json').read_text())
        for row in frozen['files']:
            if sha(ROOT / row['name']) != row['sha256']:
                raise RuntimeError('Frozen candidate changed: ' + row['name'])
    verify_pins()
    path_result = subprocess.run(['bash', '-c',
        'source "$1"; printf "ACTUAL_LEAN_PATH=%s\\n" "$LEAN_PATH"',
        'bash', str(ROOT / 'env.sh')], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=True)
    path_lines = [line[len('ACTUAL_LEAN_PATH='):] for line in path_result.stdout.splitlines()
                  if line.startswith('ACTUAL_LEAN_PATH=')]
    if path_lines != [data['lean_path']]:
        raise RuntimeError('Retained import search path differs from the pinned environment')
    for binding in data['actual_imports']:
        relative = pathlib.Path(*binding['module'].split('.')).with_suffix('.olean')
        candidates = [pathlib.Path(directory) / relative for directory in data['lean_path'].split(':')]
        candidates.append(WORK / '.toolchains/lean-4.19.0-linux/lib/lean' / relative)
        resolved = next((path for path in candidates if path.is_file()), None)
        if resolved is None or resolved.resolve() != (WORK / binding['object']).resolve():
            raise RuntimeError('Changed object resolution for module: ' + binding['module'])
    proc = subprocess.run(['bash', str(ROOT / 'check.sh')], stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)
    (ROOT / 'validation/pinned-replay.log').write_text(proc.stdout)
    if proc.returncode:
        raise RuntimeError(proc.stdout)
    imported = sorted({line[len('IMPORTED '):].strip() for line in proc.stdout.splitlines()
                       if line.startswith('IMPORTED ') and line[len('IMPORTED '):].strip() not in MODULES})
    expected = sorted(row['module'] for row in data['actual_imports'])
    if imported != expected:
        raise RuntimeError('Actual retained import closure differs from pinned closure')
    verify_pins()
    receipt = {
        'status': 'PASS', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'method': 'six additive modules fresh --trust=0 compilation; inherited objects reused, not rebuilt',
        'manifest_sha256': sha(manifest),
        'candidate_freeze_sha256': sha(ROOT / 'CANDIDATE_FREEZE.json'),
        'retained_pin_count': len(data['retained']), 'additive_pin_count': len(data['additive']),
        'retained_import_count': len(imported),
        'actual_output': proc.stdout.splitlines()[-1],
        'log_sha256': sha(ROOT / 'validation/pinned-replay.log'),
    }
    (ROOT / 'validation/AUTHOR_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
