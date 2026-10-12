#!/usr/bin/env python3
"""Replay six added model/application/control files; reuse 89 bound objects."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from verify_v3 import sha, verify_v3

parser = argparse.ArgumentParser(description=__doc__)
for name in ['lean', 'packages', 'prerequisite-objects', 'out']:
    parser.add_argument('--' + name, type=Path, required=True)
args = parser.parse_args()
for name in vars(args): setattr(args, name, getattr(args, name).resolve())
root = Path(__file__).resolve().parent
new = root / 'hase-full-per-extension-20261010'
imported = root / 'hase-imported-compiler-transport-20261010'
review = new / 'validation/independent-review'
assert not args.out.exists() and not args.out.is_relative_to(root)
before = verify_v3(root)
receipt_bytes = (review / 'PREREQUISITE_REBUILD.json').read_bytes()
prior = json.loads(receipt_bytes)
assert sha(receipt_bytes) == '7960ee87b94726090cd2c9f2ddd5abe7c99b9fb29b72abea7302847cdf4e52d1'
assert prior['status'] == 'PASS' and len(prior['build_records']) == 89
assert sha(args.lean.read_bytes()) == prior['lean_binary_sha256']
version = subprocess.check_output([str(args.lean), '--version'], text=True).strip()
assert version == prior['lean_version']
packages = json.loads((imported / 'EXTERNAL_PACKAGE_MANIFEST.json').read_text())['packages']
pins = []
for item in packages:
    observed = subprocess.check_output(['git', '-C', str(args.packages / item['name']), 'rev-parse', 'HEAD'], text=True).strip()
    assert observed == item['rev']
    pins.append({'name': item['name'], 'rev': observed})
acq = json.loads((imported / 'ACQUISITION.json').read_text())
sources = {r['module']: r for r in acq['sources']}
assert len(sources) == 83 and acq['pin'] == prior['pin']
proof_names = {'OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface', 'ImportedCompilerTransport'}
objects = []
for item in prior['build_records']:
    name = item['module']
    assert item['trust_zero'] and item['exit_code'] == 0
    relative = Path(*name.split('.'))
    obj = args.prerequisite_objects / relative.with_suffix('.olean')
    assert sha(obj.read_bytes()) == item['object_sha256'], name
    if name in sources:
        data = (imported / 'sources' / (name + '.lean')).read_bytes()
        assert sha(data) == sources[name]['sha256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == sources[name]['git_blob']
    elif name in proof_names:
        data = (imported / 'proofs' / (name + '.lean')).read_bytes()
    else:
        assert name in {'Mathlib.Algebra.MvPolynomial.Polynomial', 'Mathlib.Algebra.MvPolynomial.Funext'}
        src = args.packages / 'mathlib' / relative.with_suffix('.lean')
        data = src.read_bytes()
        assert data == subprocess.check_output(['git', '-C', str(args.packages / 'mathlib'), 'show', 'HEAD:' + relative.with_suffix('.lean').as_posix()])
    assert sha(data) == item['source_sha256'], name
    objects.append({'module': name, 'source_sha256': sha(data), 'object_sha256': item['object_sha256']})
scalar = json.loads((new / 'SCALAR_ACQUISITION.json').read_text())
data = (new / 'ScalarFusionCore.lean').read_bytes()
assert scalar['source_bytes'].encode() == data
assert scalar['sha256'] == sha(data)
assert scalar['response']['sha'] == hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
assert scalar['request']['ref'] == prior['pin']

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
paths = [args.out, args.prerequisite_objects] + [args.packages / p['name'] / '.lake/build/lib/lean' for p in packages]
env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, paths))}
steps = [('FullPER', new / 'FullPER.lean', 'FullPER.olean', False),
         ('ScalarFusionCore', new / 'ScalarFusionCore.lean', 'ScalarFusionCore.olean', False),
         ('Application', new / 'Application.lean', 'Application.olean', False),
         ('AuthorDependencyAudit', new / 'DependencyAudit.lean', 'author-audit/DependencyAudit.olean', True),
         ('IndependentControls', review / 'IndependentControls.lean', 'IndependentControls.olean', False),
         ('ReviewerDependencyAudit', review / 'DependencyAudit.lean', 'reviewer-audit/DependencyAudit.olean', True)]
records = []
log_path = args.out / 'FULL_PER_REPLAY.log'
with log_path.open('w') as log:
    log.write(version + '\nLEAN_PATH=' + env['LEAN_PATH'] + '\n')
    for name, source, object_name, audit in steps:
        if not audit:
            assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', decomment(source.read_text())), name
        dest = args.out / object_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        command = [str(args.lean), '--trust=0', '-o', str(dest), str(source)]
        start = time.monotonic()
        result = subprocess.run(command, cwd=source.parent, env=env, capture_output=True, text=True)
        output = result.stdout + result.stderr
        log.write('$ ' + ' '.join(command) + '\n' + output); log.flush()
        assert result.returncode == 0, output
        assert 'sorryAx' not in output and 'warning:' not in output and 'error:' not in output, output
        for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output, re.S):
            assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Classical.choice', 'Quot.sound', ''}
        if name == 'ReviewerDependencyAudit': assert output.count('PASS: ') == 6, output
        records.append({'module_or_check': name, 'source': str(source.relative_to(root)),
                        'source_sha256': sha(source.read_bytes()), 'output_sha256': sha(dest.read_bytes()),
                        'exit_code': result.returncode, 'trust_zero': True,
                        'seconds': round(time.monotonic()-start, 3), 'command': command})
        print(name, 'PASS', flush=True)
after = verify_v3(root)
assert before == after
for item in objects:
    obj = args.prerequisite_objects / Path(*item['module'].split('.')).with_suffix('.olean')
    assert sha(obj.read_bytes()) == item['object_sha256']
receipt = {'status': 'PASS_BOUNDED_MODEL_REPLAY',
           'scope': 'Concrete whole-HasE full-PER model, exact semantic W/c3 application, and independent controls. Literal HasE target and negation remain OPEN.',
           'lean_version': version, 'lean_binary_sha256': prior['lean_binary_sha256'],
           'all_frozen_payloads_and_v2_files_preserved': True, 'frozen_payload_files': before['frozen_payload_files'],
           'frozen_manifests': before['packages'], 'new_trust_zero_compilations': 6,
           'original_project_modules_rebuilt': 0, 'prerequisite_objects_verified_and_reused': 89,
           'prerequisite_breakdown': {'original_modules': 83, 'prior_proof_modules': 4, 'mathlib_prerequisites': 2},
           'prerequisite_receipt_sha256': sha(receipt_bytes), 'reused_objects': objects,
           'prerequisite_object_root': str(args.prerequisite_objects), 'pinned_packages_verified': pins,
           'scalar_acquisition_binding_verified': True, 'build_records': records,
           'independent_dependency_audit_targets_passed': 6, 'lean_path': env['LEAN_PATH'],
           'log_sha256': sha(log_path.read_bytes()), 'lean_bootstrap_verified': False}
(args.out / 'FULL_PER_REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS: six trust-zero compilations; 89 prerequisites rehashed and reused; no 83-module rebuild; all frozen bytes preserved.')
