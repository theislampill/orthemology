#!/usr/bin/env python3
"""Compile only new source/controls against hash-verified v3 prerequisite objects."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from verify_continuation import sha, verify

parser = argparse.ArgumentParser(description=__doc__)
for name in ['v3', 'lean', 'packages', 'prerequisite-objects', 'out']:
    parser.add_argument('--' + name, type=Path, required=True)
args = parser.parse_args()
for name in vars(args): setattr(args, name, getattr(args, name).resolve())
root = Path(__file__).resolve().parent
assert not args.out.exists() and not args.out.is_relative_to(root) and not args.out.is_relative_to(args.v3)
before = verify(root, args.v3)
contract = json.loads((root / 'V3_REUSE_CONTRACT.json').read_text())
prior_bytes = (args.v3 / contract['v3_prerequisite_receipt']).read_bytes()
prior = json.loads(prior_bytes)
assert prior['status'] == 'PASS' and len(prior['build_records']) == 89
assert sha(args.lean.read_bytes()) == prior['lean_binary_sha256']
version = subprocess.check_output([str(args.lean), '--version'], text=True).strip()
assert version == prior['lean_version']
imported = args.v3 / 'hase-imported-compiler-transport-20261010'
acq = json.loads((imported / 'ACQUISITION.json').read_text())
sources = {r['module']: r for r in acq['sources']}
assert len(sources) == 83 and acq['pin'] == prior['pin']
packages = json.loads((imported / 'EXTERNAL_PACKAGE_MANIFEST.json').read_text())['packages']
pins = []
for item in packages:
    observed = subprocess.check_output(['git', '-C', str(args.packages / item['name']), 'rev-parse', 'HEAD'], text=True).strip()
    assert observed == item['rev']
    pins.append({'name': item['name'], 'rev': observed})
objects = []
for r in prior['build_records']:
    name = r['module']; rel = Path(*name.split('.'))
    assert r['trust_zero'] and r['exit_code'] == 0
    obj = args.prerequisite_objects / rel.with_suffix('.olean')
    assert sha(obj.read_bytes()) == r['object_sha256'], name
    if name in sources:
        data = (imported / 'sources' / (name + '.lean')).read_bytes()
        assert sha(data) == sources[name]['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == sources[name]['git_blob']
    elif name in {'OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface', 'ImportedCompilerTransport'}:
        data = (imported / 'proofs' / (name + '.lean')).read_bytes()
    else:
        assert name in {'Mathlib.Algebra.MvPolynomial.Polynomial', 'Mathlib.Algebra.MvPolynomial.Funext'}
        data = (args.packages / 'mathlib' / rel.with_suffix('.lean')).read_bytes()
        assert data == subprocess.check_output(['git', '-C', str(args.packages / 'mathlib'), 'show', 'HEAD:' + rel.with_suffix('.lean').as_posix()])
    assert sha(data) == r['source_sha256']
    objects.append({'module': name, 'source_sha256': sha(data), 'object_sha256': r['object_sha256']})
graph_reuse = json.loads((root / contract['additional_scalar_dependency']['path']).read_text())
scalar = graph_reuse['ScalarFusionCore']
scalar_source = args.v3 / scalar['source']['path']
scalar_object = args.prerequisite_objects / 'ScalarFusionCore.olean'
assert sha(scalar_source.read_bytes()) == scalar['source']['sha256']
assert sha(scalar_object.read_bytes()) == scalar['object']['sha256']
objects.append({'module': 'ScalarFusionCore', 'source_sha256': scalar['source']['sha256'], 'object_sha256': scalar['object']['sha256']})
model_receipt = json.loads((args.v3 / 'hase-full-per-extension-20261010/validation/independent-review/REVIEW_RECEIPT.json').read_text())
for item in model_receipt['new_replays']:
    if item['module'] == 'ScalarFusionCore': continue
    assert item['module'] in {'FullPER', 'Application'} and item['trust_zero'] and item['exit_code'] == 0
    assert sha((args.v3 / item['source']['path']).read_bytes()) == item['source']['sha256']
    assert sha((args.prerequisite_objects / (item['module'] + '.olean')).read_bytes()) == item['object']['sha256']
    objects.append({'module': item['module'], 'source_sha256': item['source']['sha256'], 'object_sha256': item['object']['sha256']})
closed = root / 'hase-closed-scalar-instances-20261010'
closed_inputs = json.loads((closed / 'INPUTS.json').read_text())
assert closed_inputs['lean_binary_sha256'] == prior['lean_binary_sha256']
for item in closed_inputs['receipts_and_manifests']:
    name = item['path']
    if name.startswith('hase-full-per-review-20261010/'):
        name = 'hase-full-per-extension-20261010/validation/independent-review/' + name.split('/', 1)[1]
    assert sha((args.v3 / name).read_bytes()) == item['sha256']
for item in closed_inputs['frozen_source_files']:
    source = args.v3 / item['path']
    if not source.is_file(): source = root / item['path']
    assert sha(source.read_bytes()) == item['sha256']
for item in closed_inputs['reused_objects']:
    obj = args.prerequisite_objects / Path(*item['module'].split('.')).with_suffix('.olean')
    assert sha(obj.read_bytes()) == item['sha256']
assert len(closed_inputs['reused_objects']) == len(objects) == 92
for item in closed_inputs['fresh_acquisitions']:
    acquisition = json.loads((closed / item['acquisition']).read_text())
    data = (closed / item['path']).read_bytes()
    assert acquisition['content'].encode() == data and sha(data) == item['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == acquisition['sha']
    assert item['ref'] == prior['pin']

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

plan = json.loads((root / 'REPLAY_PLAN.json').read_text())
args.out.mkdir(parents=True)
paths = [args.out, args.prerequisite_objects] + [args.packages / p['name'] / '.lake/build/lib/lean' for p in packages]
env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, paths))}
log_path = args.out / 'SOURCE_CONTINUATION_REPLAY.log'
records = []
with log_path.open('w') as log:
    log.write(version + '\nLEAN_PATH=' + env['LEAN_PATH'] + '\n')
    for step in plan['steps']:
        source = root / step['source']
        clean = re.sub(r'"(?:[^"\\]|\\.)*"', '""', decomment(source.read_text()))
        assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', clean), step['name']
        dest = args.out / step['output']
        assert not dest.exists()
        dest.parent.mkdir(parents=True, exist_ok=True)
        command = [str(args.lean), '--trust=0', '-o', str(dest), str(source)]
        start = time.monotonic()
        run = subprocess.run(command, cwd=source.parent, env=env, capture_output=True, text=True)
        text = run.stdout + run.stderr
        log.write('$ ' + ' '.join(command) + '\n' + text); log.flush()
        assert run.returncode == 0, text
        assert 'sorryAx' not in text and 'warning:' not in text and 'error:' not in text, text
        for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', text, re.S):
            assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Classical.choice', 'Quot.sound', ''}
        for marker, count in step.get('expected_markers', {}).items(): assert text.count(marker) == count, (marker, text)
        records.append({'name': step['name'], 'source': step['source'], 'source_sha256': sha(source.read_bytes()),
                        'output_sha256': sha(dest.read_bytes()), 'trust_zero': True, 'exit_code': run.returncode,
                        'seconds': round(time.monotonic()-start, 3), 'command': command})
        print(step['name'], 'PASS', flush=True)
assert verify(root, args.v3) == before
for r in objects:
    obj = args.prerequisite_objects / Path(*r['module'].split('.')).with_suffix('.olean')
    assert sha(obj.read_bytes()) == r['object_sha256']
receipt = {'status': 'PASS_BOUNDED_SOURCE_CONTINUATION_REPLAY', 'scope': plan['scope'],
           'lean_version': version, 'lean_binary_sha256': prior['lean_binary_sha256'],
           'continuation_and_v3_hashes_preserved': True, 'prior_89_objects_verified_and_reused': 89,
           'additional_model_objects_verified_and_reused': ['ScalarFusionCore', 'FullPER', 'Application'],
           'total_reused_object_count': 92, 'original_83_modules_rebuilt': 0,
           'new_trust_zero_compilations': len(records), 'records': records, 'reused_objects': objects,
           'pinned_packages_verified': pins, 'v3_index_sha256': contract['v3_index_sha256'],
           'prerequisite_receipt_sha256': sha(prior_bytes), 'lean_path': env['LEAN_PATH'],
           'log_sha256': sha(log_path.read_bytes()), 'limitations': plan['limitations']}
(args.out / 'SOURCE_CONTINUATION_REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS: all new trust-zero steps; verified prior objects reused; no 83-module rebuild; source bytes unchanged.')
