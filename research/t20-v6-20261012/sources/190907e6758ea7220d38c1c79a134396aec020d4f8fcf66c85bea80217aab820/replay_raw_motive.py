#!/usr/bin/env python3
"""Replay only the RawMotive addition against verified v1-built source objects."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time
from verify import sha, verify

parser = argparse.ArgumentParser(description=__doc__)
for name in ['lean', 'packages', 'dependency-objects', 'project-objects', 'out']:
    parser.add_argument('--' + name, required=True, type=Path)
args = parser.parse_args()
for name in vars(args): setattr(args, name, getattr(args, name).resolve())
root = Path(__file__).resolve().parent
raw = root / 'hase-raw-motive-boundary-20261010'
imported = root / 'hase-imported-compiler-transport-20261010'
assert not args.out.exists() and not args.out.is_relative_to(root)
before = verify(root)
version = subprocess.check_output([str(args.lean), '--version'], text=True).strip()
assert 'version 4.19.0' in version and '6caaee842e94' in version
prior_path = root / 'preservation/FRESH_EXTRACT_83_REPLAY.json'
prior_bytes = prior_path.read_bytes()
prior = json.loads(prior_bytes)
assert prior['status'] == 'PASS' and prior['original_project_modules_rebuilt'] == 83
built = {r['module']: r for r in prior['build_records'] if not r['trust_zero']}
acq = json.loads((imported / 'ACQUISITION.json').read_text())
sources = {r['module']: r for r in acq['sources']}
assert set(built) == set(sources) and len(built) == 83
objects = []
for name, record in built.items():
    data = (imported / 'sources' / (name + '.lean')).read_bytes()
    obj = args.project_objects / (name + '.olean')
    assert sha(data) == record['source_sha256'] == sources[name]['sha256'], name
    assert sha(obj.read_bytes()) == record['output_sha256'], name
    objects.append({'module': name, 'source_sha256': sha(data), 'object_sha256': record['output_sha256']})
packages = json.loads((imported / 'EXTERNAL_PACKAGE_MANIFEST.json').read_text())['packages']
pins = []
for item in packages:
    observed = subprocess.check_output(['git', '-C', str(args.packages / item['name']), 'rev-parse', 'HEAD'], text=True).strip()
    assert observed == item['rev']
    pins.append({'name': item['name'], 'rev': observed})
external = []
for item in prior['external_objects_reused']:
    relative = Path(*item['module'].split('.'))
    obj = args.dependency_objects / relative.with_suffix('.olean')
    source = args.packages / 'mathlib' / relative.with_suffix('.lean')
    tracked = subprocess.check_output(['git', '-C', str(args.packages / 'mathlib'), 'show', 'HEAD:' + relative.with_suffix('.lean').as_posix()])
    assert sha(obj.read_bytes()) == item['object_sha256']
    assert source.read_bytes() == tracked and sha(tracked) == item['source_sha256']
    external.append(item)

def decomment(text):
    out = []; depth = 0; i = 0
    while i < len(text):
        if text[i:i+2] == '/-': depth += 1; i += 2
        elif depth and text[i:i+2] == '-/': depth -= 1; i += 2
        elif not depth and text[i:i+2] == '--':
            end = text.find('\n', i); i = len(text) if end < 0 else end
        else:
            if not depth or text[i] == '\n': out.append(text[i])
            i += 1
    assert depth == 0
    return ''.join(out)

args.out.mkdir(parents=True)
paths = [args.out, args.project_objects, args.dependency_objects] + [args.packages / p['name'] / '.lake/build/lib/lean' for p in packages]
env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, paths))}
records = []
log_path = args.out / 'RAW_MOTIVE_REPLAY.log'
with log_path.open('w') as log:
    log.write(version + '\nLEAN_PATH=' + env['LEAN_PATH'] + '\n')
    for name, source in [('RawMotiveBoundary', raw / 'RawMotiveBoundary.lean'),
                         ('IndependentBoundaryChecks', raw / 'validation/IndependentBoundaryChecks.lean')]:
        assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', decomment(source.read_text()))
        dest = args.out / (name + '.olean')
        command = [str(args.lean), '--trust=0', '-o', str(dest), str(source)]
        start = time.monotonic()
        result = subprocess.run(command, cwd=source.parent, env=env, capture_output=True, text=True)
        output = result.stdout + result.stderr
        log.write('$ ' + ' '.join(command) + '\n' + output); log.flush()
        assert result.returncode == 0, output
        assert 'sorryAx' not in output and 'warning:' not in output and 'error:' not in output, output
        for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output, re.S):
            assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Classical.choice', 'Quot.sound', ''}
        records.append({'module': name, 'source': str(source.relative_to(root)),
                        'source_sha256': sha(source.read_bytes()), 'output_sha256': sha(dest.read_bytes()),
                        'exit_code': result.returncode, 'trust_zero': True,
                        'seconds': round(time.monotonic()-start, 3), 'command': command})
        print(name, 'PASS', flush=True)
after = verify(root)
assert before == after
receipt = {'status': 'PASS', 'scope': 'RawMotiveBoundary and independent controls only; inherited F/G soundness, not new full-PER soundness. Literal HasE [] c3 (W q) remains OPEN.',
           'lean_version': version, 'all_frozen_bytes_preserved': True,
           'verified_frozen_payload_files': before['frozen_payload_files'],
           'verified_frozen_manifests': before['packages'],
           'new_compilations': 2, 'all_new_compilations_trust_zero': True,
           'original_project_modules_rebuilt': 0, 'original_project_objects_verified_and_reused': 83,
           'prior_build_receipt_sha256': sha(prior_bytes), 'project_objects': objects,
           'project_object_root': str(args.project_objects), 'external_objects_verified_and_reused': external,
           'pinned_packages_verified': pins, 'build_records': records,
           'lean_path': env['LEAN_PATH'], 'log_sha256': sha(log_path.read_bytes())}
(args.out / 'RAW_MOTIVE_REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS: two trust-zero compilations; 83 prior source objects hash-verified and reused; all frozen bytes unchanged.')
