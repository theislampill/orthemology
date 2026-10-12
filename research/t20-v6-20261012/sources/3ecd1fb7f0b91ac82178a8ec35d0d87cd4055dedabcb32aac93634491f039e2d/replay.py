#!/usr/bin/env python3
"""Fresh trust-zero replay of new closure files and their new operational dependency."""
from pathlib import Path
import hashlib, json, os, re, subprocess, tempfile
ROOT = Path(__file__).resolve().parent
W = ROOT.parent
LEAN = W / '.toolchains/lean-4.19.0-linux/bin/lean'
OPER = W / 'homogeneous-per-model-20261010/operational/CaseOperational.lean'
OUT = Path(tempfile.mkdtemp(prefix='replay-', dir=ROOT / 'validation'))
modules = [('CaseOperational', OPER)] + [(n, ROOT / (n + '.lean')) for n in
    ['HomogeneousPER', 'ConcreteUniverse', 'GuardControls']]
log = [subprocess.check_output([str(LEAN), '--version'], text=True)]
records = []
for name, src in modules:
    source = src.read_text()
    clean = re.sub(r'/\-.*?\-/', '', source, flags=re.S)
    clean = re.sub(r'--[^\n]*', '', clean)
    forbidden = re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', clean)
    assert not forbidden, (name, forbidden)
    cmd = [str(LEAN), '--trust=0', '-o', str(OUT / (name + '.olean')), str(src)]
    p = subprocess.run(cmd, env={**os.environ, 'LEAN_PATH': str(OUT)}, capture_output=True, text=True)
    output = p.stdout + p.stderr
    log.append('$ ' + ' '.join(cmd) + '\n' + output)
    (ROOT / 'validation/REPLAY.log').write_text('\n'.join(log))
    assert p.returncode == 0, (name, output)
    assert not any(x in output for x in ['sorryAx', 'warning:', 'error:']), (name, output)
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output, flags=re.S):
        actual = set(re.sub(r'\s+', '', match).split(','))
        assert actual <= {'propext', 'Classical.choice', 'Quot.sound', ''}, actual
    records.append({'module': name, 'source': str(src.relative_to(W)),
        'sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'exit_code': p.returncode,
        'trust_zero': True, 'olean_sha256': hashlib.sha256((OUT / (name + '.olean')).read_bytes()).hexdigest()})
    print(name + ' PASS', flush=True)
receipt = {'status': 'PASS', 'fresh_output': str(OUT.relative_to(ROOT)),
    'scope': 'New operational dependency and homogeneous closure only; no source-theory baseline rebuild.',
    'modules': records, 'axioms_allowed': ['propext', 'Classical.choice', 'Quot.sound']}
(ROOT / 'validation/REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
