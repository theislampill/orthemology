#!/usr/bin/env python3
"""Hash-check retained inputs, freshly compile only this four-module extension."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, tempfile

R = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--workspace', type=Path, default=R.parent)
p.add_argument('--output', type=Path)
a = p.parse_args()
W = a.workspace.resolve()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((R / 'MANIFEST.json').read_text())
bind = json.loads((R / 'INPUTS.json').read_text())

def verify():
    for row in manifest['files']:
        assert sha(R / row['path']) == row['sha256'], row['path']
    for row in [bind['receipt']] + bind['read_only_prior_controls']:
        assert sha(W / row['path']) == row['sha256'], row['path']
    for row in bind['source_objects'] + bind['external_source_objects']:
        for k in ['source', 'object']:
            assert sha(W / row[k + '_path']) == row[k + '_sha256'], row[k + '_path']
    assert sha(W / '.toolchains/lean-4.19.0-linux/bin/lean') == bind['lean_binary_sha256']

verify()
if a.output:
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
else:
    (R / 'validation').mkdir(exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='fresh-', dir=R / 'validation'))
lean = W / '.toolchains/lean-4.19.0-linux/bin/lean'
libs = [W / 'hase-full-per-review-20261010/fresh-lib'] + sorted(
    (W / 'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, [out] + libs))}
records, logs = [], []
for m in ['FiniteK', 'SourceRaw', 'RawImages', 'DependencyAudit']:
    src = R / (m + '.lean')
    content = re.sub(r'/\-.*?\-/', '', src.read_text(), flags=re.S)
    content = re.sub(r'--[^\n]*', '', content)
    content = re.sub(r'"(?:\\.|[^"\\])*"', '""', content)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b', content), m
    cmd = [str(lean), '--trust=0', '-o', str(out / (m + '.olean')), str(src)]
    run = subprocess.run(cmd, env=env, text=True, capture_output=True)
    log = run.stdout + run.stderr
    logs.append('$ ' + ' '.join(cmd) + '\n' + log)
    (out / (m + '.log')).write_text(log)
    assert run.returncode == 0, (m, log)
    assert not any(x in log for x in ['warning:', 'error:', 'sorryAx']), (m, log)
    axioms = set()
    for found in re.findall(r'(?:depends on axioms:|axioms)\s*\[([^\]]*)\]', log, re.S):
        axioms.update(re.sub(r'\s+', '', found).split(','))
    assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (m, axioms)
    records.append({'module': m, 'source_sha256': sha(src),
        'object_sha256': sha(out / (m + '.olean')), 'exit_code': run.returncode,
        'trust_zero': True, 'axioms': sorted(axioms)})
    print(m, 'PASS', flush=True)
verify()
(out / 'REPLAY.log').write_text('\n'.join(logs))
receipt = {'status': 'PASS', 'manifest_sha256': sha(R / 'MANIFEST.json'),
    'output': str(out), 'modules': records,
    'bound_originals_unchanged_before_and_after': True,
    'baseline_rebuilt': False,
    'scope': 'Finite equality-valued total Raw/application carrier and full applicative congruence quotient collapse only; no whole-HasE model, universal W decision, field novelty, or audit closure.'}
(out / 'REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('Receipt:', out / 'REPLAY.json')
