#!/usr/bin/env python3
"""Replay the bounded T20 model proof in an empty output directory.

Only the supplied official Lean toolchain, Init and these three modules are used.
The target directory must not exist, so replay never overwrites frozen evidence.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from datetime import datetime, timezone

lane = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', type=Path, required=True, help='Official Lean 4.19.0 executable')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
lean = args.lean.resolve()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=False)
(out / 'inputs').mkdir()
(out / 'objects').mkdir()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

env = dict(os.environ)
env['LEAN_PATH'] = str(out / 'objects')
env.pop('LEAN_SRC_PATH', None)
names = ['GroundExtension', 'GroundExtensionControls', 'ModalCapacityControl']
all_modules = names + ['AxiomAudit']
record = {
    'schema': 't20-existential-ground-replay-v1',
    'started_utc': datetime.now(timezone.utc).isoformat(),
    'lean_binary': str(lean), 'lean_binary_sha256': sha(lean),
    'output_directory': str(out), 'lean_path': env['LEAN_PATH'],
    'dependencies': 'Official Lean 4.19.0 Init closure and three local modules only',
    'module_results': [],
}
version = subprocess.run([str(lean), '--version'], env=env, cwd=out,
                         text=True, capture_output=True)
record['version'] = version.stdout.strip()
if version.returncode or 'version 4.19.0,' not in record['version']:
    raise SystemExit('Expected working official Lean 4.19.0')

declared = []
for name in names:
    source = lane / 'lean' / (name + '.lean')
    text = source.read_text()
    namespace = re.search(r'^namespace (.+)$', text, re.M).group(1)
    declared.extend(namespace + '.' + x for x in
                    re.findall(r'^theorem ([A-Za-z0-9_]+)', text, re.M))
    # This conservative textual check complements the transitive kernel audit.
    forbidden = re.findall(r'\b(?:sorry|admit|axiom|unsafe|partial|implemented_by|native_decide)\b', text)
    if forbidden:
        raise SystemExit(f'Forbidden trust escape in {source}: {forbidden}')

audit_names = re.findall(r'^#print axioms (.+)$',
                        (lane / 'lean/AxiomAudit.lean').read_text(), re.M)
if declared != audit_names:
    raise SystemExit('Theorem audit does not exactly cover the source declarations')
record['theorem_count'] = len(declared)
record['forbidden_token_scan'] = 'passed'
record['audit_inventory_exact'] = True

for name in all_modules:
    source = lane / 'lean' / (name + '.lean')
    copied = out / 'inputs' / source.name
    shutil.copyfile(source, copied)
    command = [str(lean), '-o', str(out / 'objects' / (name + '.olean')), str(copied)]
    result = subprocess.run(command, env=env, cwd=out, text=True, capture_output=True)
    stdout = out / (name + '.stdout.log')
    stderr = out / (name + '.stderr.log')
    stdout.write_text(result.stdout)
    stderr.write_text(result.stderr)
    record['module_results'].append({
        'module': name, 'source_sha256': sha(source), 'command': command,
        'exit_code': result.returncode,
        'stdout_file': stdout.name, 'stdout_sha256': sha(stdout),
        'stderr_file': stderr.name, 'stderr_sha256': sha(stderr),
    })
    if result.returncode:
        (out / 'REPLAY_RECEIPT.json').write_text(json.dumps(record, indent=2) + '\n')
        raise SystemExit(f'Failed module {name}; inspect retained logs')

audit = (out / 'AxiomAudit.stdout.log').read_text()
reported = re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)", audit)
if reported != declared:
    raise SystemExit('Kernel audit output does not exactly match theorem inventory')
axioms = sorted(set(x.strip() for block in re.findall(r'depends on axioms:\s*\[([^]]*)\]', audit)
                    for x in block.split(',') if x.strip()))
record['transitive_axioms_union'] = axioms
if not set(axioms).issubset({'propext', 'Classical.choice', 'Quot.sound'}):
    raise SystemExit(f'Unexpected axiom: {axioms}')
record['completed_utc'] = datetime.now(timezone.utc).isoformat()
record['result'] = 'all_modules_compiled_and_every_theorem_axiom_audited'
(out / 'REPLAY_RECEIPT.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'result': record['result'], 'theorems': len(declared),
                  'transitive_axioms_union': axioms,
                  'receipt': str(out / 'REPLAY_RECEIPT.json')}, indent=2))
