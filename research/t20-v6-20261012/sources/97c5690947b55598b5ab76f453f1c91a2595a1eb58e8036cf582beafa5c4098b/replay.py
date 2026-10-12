#!/usr/bin/env python3
"""Fresh trust-zero replay of this addition, reusing hash-bound predecessors."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
W = ROOT.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inputs = json.loads((ROOT / 'INPUTS.json').read_text())
manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
for row in manifest['files']:
    assert sha(ROOT / row['path']) == row['sha256'], row['path']
for row in inputs['source_and_receipt_bindings']:
    assert sha(W / row['path']) == row['sha256'], row['path']
for row in inputs['reused_objects']:
    assert sha(W / row['path']) == row['sha256'], row['path']
LEAN = W / inputs['lean_binary_path']
assert sha(LEAN) == inputs['lean_binary_sha256'], 'Lean compiler'
STAGE = Path(tempfile.mkdtemp(prefix='replay-', dir=ROOT / 'validation'))
LIB = STAGE / 'lib'
LIB.mkdir()
(STAGE / 'validation').mkdir()
for path in ROOT.iterdir():
    if path.is_file() and (path.suffix in {'.lean', '.py'} or path.name == 'source_ast.json'):
        shutil.copy2(path, STAGE / path.name)
libs = list((W / 'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, [LIB,
    W / 'hase-closed-scalar-instances-20261010/validation',
    W / 'hase-full-per-review-20261010/fresh-lib'] + libs)), 'PYTHONDONTWRITEBYTECODE': '1'}
logs = []
records = []

def run(args, label, timeout=900):
    started = time.monotonic()
    proc = subprocess.run(list(map(str, args)), cwd=STAGE, env=env,
                          capture_output=True, text=True, timeout=timeout)
    output = proc.stdout + proc.stderr
    logs.append('$ ' + ' '.join(map(str, args)) + '\n' + output)
    (STAGE / 'validation' / (label + '.log')).write_text(output)
    assert proc.returncode == 0, (label, proc.returncode, output)
    records.append({'label': label, 'exit_code': 0, 'seconds': round(time.monotonic()-started, 3)})
    print(label, 'PASS', flush=True)
    return proc.stdout

run([LEAN, '--version'], 'compiler')
modules = ['OpenDevelopments', 'DomainControls', 'ScalarCertificates', 'LiteralSourceQ', 'SourceExport', 'NonstandardRejection', 'NegativeCertificateControls', 'OpenCertificateControl']
for module in modules:
    src = STAGE / (module + '.lean')
    code = re.sub(r'/\-.*?\-/', '', src.read_text(), flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', code), module
    out = run([LEAN, '--trust=0', '-o', LIB / (module + '.olean'), src], module)
    assert not any(x in out for x in ['error:', 'warning:', 'sorryAx']), module
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', out, re.S):
        assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Quot.sound', 'Classical.choice', ''}
exported = run([LEAN, '--trust=0', '--run', STAGE / 'SourceExport.lean'], 'literal_source_export')
assert json.loads(exported) == json.loads((ROOT / 'source_ast.json').read_text()), 'literal source JSON differs'
run(['python3', '-m', 'unittest', '-v', 'test_diagnostic.py'], 'adversarial_python_tests')
run(['python3', STAGE / 'generate_controls.py'], 'regenerate_concrete_certificates')
assert sha(STAGE / 'ConcreteScalarCertificates.lean') == sha(ROOT / 'ConcreteScalarCertificates.lean'), 'generated Lean differs'
for src in (STAGE / 'validation').glob('*.json'):
    recorded = ROOT / 'validation' / src.name
    assert recorded.exists() and json.loads(src.read_text()) == json.loads(recorded.read_text()), src.name
for module in ['ConcreteScalarCertificates', 'DependencyAudit']:
    src = STAGE / (module + '.lean')
    code = re.sub(r'/\-.*?\-/', '', src.read_text(), flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', code), module
    out = run([LEAN, '--trust=0', '-o', LIB / (module + '.olean'), src], module)
    assert not any(x in out for x in ['error:', 'warning:', 'sorryAx']), module
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', out, re.S):
        assert set(re.sub(r'\s+', '', match).split(',')) <= {'propext', 'Quot.sound', 'Classical.choice', ''}
# Recheck all bound predecessors, not just the inputs used last.
for row in inputs['source_and_receipt_bindings'] + inputs['reused_objects']:
    assert sha(W / row['path']) == row['sha256'], ('changed predecessor', row['path'])
summary = {'status': 'PASS', 'strategy': 'complete developments, not normal order',
           'verified_reused_objects': len(inputs['reused_objects']),
           'fresh_stage': str(STAGE.relative_to(ROOT)), 'steps': records,
           'source_export_rebound': True,
           'concrete_cases': json.loads((STAGE / 'validation/CONCRETE_SUMMARY.json').read_text()),
           'scope': 'Computable closed-HasE generic count extraction; bounded diagnostic and exact finite source certificates; no universal W judgment.'}
(ROOT / 'validation/FINAL_REPLAY.log').write_text('\n'.join(logs))
(ROOT / 'validation/FINAL_REPLAY.json').write_text(json.dumps(summary, indent=2) + '\n')
print('FINAL PASS', flush=True)
