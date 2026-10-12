#!/usr/bin/env python3
"""Replay the two predecessor packages from extracted sources; every output goes to a new, separate directory.

No installs, network access, dependency writes, or recursive overlay traversal.
The dependency object root must already provide the two Mathlib objects listed
in the retained EXTERNAL_BUILD_PLAN.json. Other pinned package objects are reused.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from verify import PACKAGES, sha, verify

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', required=True, type=Path)
parser.add_argument('--packages', required=True, type=Path)
parser.add_argument('--dependency-objects', required=True, type=Path)
parser.add_argument('--out', required=True, type=Path)
parser.add_argument('--project-objects', type=Path, help='Reuse exact already-built 83-module objects; omit for a fresh source rebuild.')
args = parser.parse_args()
root = Path(__file__).resolve().parent
isolated = root / 'hase-open-term-standardness-20261010'
imported = root / 'hase-imported-compiler-transport-20261010'
args.lean = args.lean.resolve()
args.packages = args.packages.resolve()
args.dependency_objects = args.dependency_objects.resolve()
args.out = args.out.resolve()
assert not args.out.is_relative_to(root), 'Outputs must be outside the evidence directory.'
assert not args.out.exists(), 'Choose a new output directory.'
before = verify(root)
args.out.mkdir(parents=True)
isolated_out = args.out / 'isolated'
project_out = args.out / 'project'
isolated_out.mkdir()
project_out.mkdir()
version = subprocess.check_output([str(args.lean), '--version'], text=True).strip()
assert 'version 4.19.0' in version and '6caaee842e94' in version, version
packages = json.loads((imported / 'EXTERNAL_PACKAGE_MANIFEST.json').read_text())['packages']
pins = []
for item in packages:
    path = args.packages / item['name']
    observed = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
    assert observed == item['rev'], (item['name'], observed, item['rev'])
    pins.append({'name': item['name'], 'rev': observed})
libs = [args.packages / p['name'] / '.lake/build/lib/lean' for p in packages]
external_objects = []
for item in json.loads((imported / 'EXTERNAL_BUILD_PLAN.json').read_text()):
    relative = Path(*item['module'].split('.')).with_suffix('.lean')
    source = args.packages / 'mathlib' / relative
    tracked = subprocess.check_output(['git', '-C', str(args.packages / 'mathlib'), 'show', 'HEAD:' + relative.as_posix()])
    assert source.read_bytes() == tracked
    obj = args.dependency_objects / relative.with_suffix('.olean')
    external_objects.append({'module': item['module'], 'source_sha256': sha(tracked),
                             'object_sha256': sha(obj.read_bytes()), 'reused': True})
acq = json.loads((imported / 'ACQUISITION.json').read_text())
items = {r['module']: r for r in acq['sources']}
assert len(items) == len(acq['sources']) == 83 and not acq['missing']

def decomment(text):
    result = []; depth = 0; i = 0
    while i < len(text):
        if text[i:i+2] == '/-': depth += 1; i += 2
        elif depth and text[i:i+2] == '-/': depth -= 1; i += 2
        elif not depth and text[i:i+2] == '--':
            end = text.find('\n', i); i = len(text) if end < 0 else end
        else:
            if not depth or text[i] == '\n': result.append(text[i])
            i += 1
    assert depth == 0
    return ''.join(result)

for name, item in items.items():
    data = (imported / 'sources' / (name + '.lean')).read_bytes()
    assert sha(data) == item['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == item['git_blob']
    imports = [word for line in decomment(data.decode()).splitlines()
               if re.match(r'^\s*import\s', line) for word in line.split()[1:]]
    assert imports == item['imports'], name
for name in ['OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface']:
    assert (isolated / (name + '.lean')).read_bytes() == (imported / 'proofs' / (name + '.lean')).read_bytes()

log = (args.out / 'REPLAY.log').open('w')
log.write(version + '\n')
records = []
def build(name, source, out, paths, strict=False):
    dest = out / Path(*name.split('.')).with_suffix('.olean')
    assert not dest.exists(), str(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    command = [str(args.lean)] + (['--trust=0'] if strict else []) + ['-o', str(dest), str(source)]
    env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, paths))}
    if strict:
        assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', decomment(source.read_text())), source
    start = time.monotonic()
    result = subprocess.run(command, cwd=source.parent, env=env, text=True, capture_output=True)
    output = result.stdout + result.stderr
    log.write('LEAN_PATH=' + env['LEAN_PATH'] + '\n$ ' + ' '.join(command) + '\n' + output)
    log.flush()
    assert result.returncode == 0, output
    if strict:
        assert 'sorryAx' not in output and 'warning:' not in output and 'error:' not in output, output
        for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output, re.S):
            assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Classical.choice', 'Quot.sound', ''}, match
    records.append({'module': name, 'source': str(source.relative_to(root)), 'source_sha256': sha(source.read_bytes()),
                    'exit_code': result.returncode, 'trust_zero': strict, 'seconds': round(time.monotonic()-start, 3),
                    'output_sha256': sha(dest.read_bytes()), 'command': command, 'lean_path': env['LEAN_PATH']})
    print(name, 'PASS', flush=True)

for name in ['OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface']:
    build(name, isolated / (name + '.lean'), isolated_out, [isolated_out], strict=True)
build('ReviewerChecks', isolated / 'validation/ReviewerChecks.lean', isolated_out, [isolated_out], strict=True)

reused_projects = []
if args.project_objects:
    args.project_objects = args.project_objects.resolve()
    for name in items:
        obj = args.project_objects / (name + '.olean')
        reused_projects.append({'module': name, 'source_sha256': items[name]['sha256'], 'object_sha256': sha(obj.read_bytes())})
    paths = [project_out, args.project_objects, args.dependency_objects] + libs
else:
    paths = [project_out, args.dependency_objects] + libs
    active = set(); seen = set()
    def visit(name):
        if name not in items or name in seen: return
        assert name not in active, name
        active.add(name)
        for dep in items[name]['imports']: visit(dep)
        build(name, imported / 'sources' / (name + '.lean'), project_out, paths)
        active.remove(name); seen.add(name)
    visit(acq['root'])
    assert seen == set(items)
for name in ['OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface', 'ImportedCompilerTransport']:
    build(name, imported / 'proofs' / (name + '.lean'), project_out, paths, strict=True)
build('IndependentTransportChecks', imported / 'validation/IndependentTransportChecks.lean', project_out, paths, strict=True)
after = verify(root)
assert before == after
log.close()
receipt = {'status': 'PASS', 'scope': 'Artifact-source replay only; literal HasE [] c3 (W q) remains OPEN.',
           'lean_version': version, 'verified_frozen_payload_files': before['frozen_payload_files'], 'verified_frozen_manifests': PACKAGES,
           'frozen_bytes_preserved': True, 'isolated_modules_rebuilt': 3, 'isolated_reviewer_checks_rebuilt': 1,
           'original_project_modules_rebuilt': 0 if args.project_objects else 83,
           'original_project_modules_reused': 83 if args.project_objects else 0,
           'imported_proof_modules_rebuilt': 4, 'imported_reviewer_checks_rebuilt': 1,
           'all_nine_proof_and_review_compilations_trust_zero': True,
           'external_objects_reused': external_objects, 'pinned_packages': pins,
           'project_object_root': str(args.project_objects or project_out),
           'reused_project_objects': reused_projects, 'build_records': records,
           'log_sha256': sha((args.out / 'REPLAY.log').read_bytes()),
           'not_claimed': ['New mathematical novelty', 'Whole-HasE soundness for the new interpretation',
                           'Literal-target derivation or nonderivability', 'Fresh rebuild of external dependency packages']}
(args.out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS:', len(records), 'compilations;', receipt['original_project_modules_rebuilt'], 'original modules rebuilt;',
      receipt['original_project_modules_reused'], 'reused; all frozen hashes preserved.', flush=True)
