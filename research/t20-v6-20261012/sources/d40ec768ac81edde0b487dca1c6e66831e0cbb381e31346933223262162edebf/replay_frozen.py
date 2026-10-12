#!/usr/bin/env python3
"""Replay unmodified frozen sources without writing in the author's directory."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, time
R = Path(__file__).resolve().parent
W = R.parent
F = R / 'frozen-target'
ORIGINAL = W / 'full-polynomial-moment-countermodel-20261010'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((F / 'FROZEN_MANIFEST.json').read_text())
expected_manifest = '94de1970b395a0f96c94fbfeb3eb7b621432959a6843cbc7024ffc8faaaa3561'
assert sha(F / 'FROZEN_MANIFEST.json') == expected_manifest
for row in manifest['files']:
    for base in (ORIGINAL, F):
        p = base / row['path']
        assert p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], str(p)
records = []
A = R / 'author-replay'
A.mkdir(exist_ok=True)
for name in ('countermodel.py', 'check_exact.py'):
    shutil.copyfile(F / name, A / name)
start = time.monotonic()
p = subprocess.run(['python3', 'check_exact.py'], cwd=A, text=True, capture_output=True, timeout=120)
(A / 'REPLAY.log').write_text(p.stdout + p.stderr)
assert p.returncode == 0, p.stdout + p.stderr
ar = json.loads((A / 'EXACT_CHECK_RECEIPT.json').read_text())
assert ar['checks_passed'] == 37588
assert sha(A / 'PREFIX_25.json') == sha(F / 'PREFIX_25.json')
records.append({'name':'author_exact_replay','status':'PASS','checks':ar['checks_passed'],
                'prefix_matches_frozen':True,'log':'author-replay/REPLAY.log',
                'elapsed_seconds':round(time.monotonic()-start,3)})
L = R / 'lean-replay'
L.mkdir(exist_ok=True)
lean = W / '.toolchains/lean-4.19.0-linux/bin/lean'
retained = W / 'lean-truncated-moment-obstruction-20261010/lean_path.txt'
paths = [str(L)] + [p for p in retained.read_text().strip().split(':') if p != str(retained.parent)]
env = dict(os.environ, LEAN_PATH=':'.join(paths))
for name in ('ScalarSupport.lean','RetainedMatrixProbe.lean','wrong_seed_value.lean','wrong_origin_value.lean'):
    shutil.copyfile(F / 'lean-support' / name, L / name)
source = (L / 'ScalarSupport.lean').read_text()
assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by)\b', source)
for name, success in [('ScalarSupport',True),('RetainedMatrixProbe',True),('wrong_seed_value',False),('wrong_origin_value',False)]:
    cmd = [str(lean),'--trust=0']
    if name == 'ScalarSupport': cmd += ['-o',str(L / 'ScalarSupport.olean')]
    cmd += [str(L / (name+'.lean'))]
    start = time.monotonic()
    p = subprocess.run(cmd,cwd=W,env=env,text=True,capture_output=True,timeout=120)
    output = p.stdout + p.stderr
    logfile = L / (name+'.log')
    logfile.write_text(output)
    assert (p.returncode == 0) == success, (name, p.returncode, output)
    if not success:
        assert 'error:' in output and ('unsolved goals' in output or 'tactic' in output)
        assert 'does not exist' not in output and 'unknown module' not in output
    if name == 'ScalarSupport':
        axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)
        assert len(axioms) == 4
        for theorem, names in axioms:
            assert {x.strip() for x in names.split(',')} <= {'propext','Classical.choice','Quot.sound'}
    records.append({'name':name,'status':'PASS' if success else 'EXPECTED_REJECTION',
                    'exit_status':p.returncode,'trust':0,'log':str(logfile.relative_to(R)),
                    'log_sha256':sha(logfile),'elapsed_seconds':round(time.monotonic()-start,3)})
# All original frozen files must remain identical after replays.
for row in manifest['files']:
    assert sha(ORIGINAL / row['path']) == row['sha256'], row['path']
receipt = {'status':'PASS_FROZEN_REPLAYS','frozen_manifest_sha256':expected_manifest,
           'all_frozen_files_verified':len(manifest['files']),
           'author_original_unchanged':True,'records':records,
           'lean_scope':'Universal scalar F>=3/4 and F>0; seed arithmetic only. No Lean formalization of the functional or universal square positivity.',
           'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),
           'lean_executable_sha256':sha(lean),'replay_driver_sha256':sha(Path(__file__))}
(R / 'FROZEN_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
