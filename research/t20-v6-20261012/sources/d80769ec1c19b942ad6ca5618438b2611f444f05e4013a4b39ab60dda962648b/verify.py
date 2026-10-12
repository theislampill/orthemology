#!/usr/bin/env python3
"""Verify pinned inputs, then fresh additive Lean and exact Python replay."""
import datetime, hashlib, json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
WORK=ROOT.parent
MODULES=['SeededSourceLookup','SeededSourceHistories','SeededSourceControls','SeededSourceAudit']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=json.loads((ROOT/'SOURCE_BOUNDARY.json').read_text())
    freeze=json.loads((ROOT/'CANDIDATE_FREEZE.json').read_text())
    def pins():
        for r in data['retained']:
            if sha(WORK/r['path'])!=r['sha256']: raise RuntimeError('Retained input changed: '+r['path'])
        for r in freeze['files']:
            if sha(ROOT/r['name'])!=r['sha256']: raise RuntimeError('Frozen candidate changed: '+r['name'])
    pins()
    run=subprocess.run(['bash','-c','source "$1"; printf "ACTUAL_LEAN_PATH=%s\\n" "$LEAN_PATH"','bash',str(ROOT/'env.sh')],capture_output=True,text=True,check=True)
    paths=[s.removeprefix('ACTUAL_LEAN_PATH=') for s in run.stdout.splitlines() if s.startswith('ACTUAL_LEAN_PATH=')]
    if paths!=[data['lean_path']]: raise RuntimeError('Retained import path changed')
    for r in data['actual_imports']:
        rel=pathlib.Path(*r['module'].split('.')).with_suffix('.olean')
        options=[pathlib.Path(p)/rel for p in data['lean_path'].split(':')]+[WORK/'.toolchains/lean-4.19.0-linux/lib/lean'/rel]
        resolved=next((p for p in options if p.is_file()),None)
        if resolved is None or resolved.resolve()!=(WORK/r['object']).resolve(): raise RuntimeError('Import resolution changed: '+r['module'])
    proc=subprocess.run(['bash',str(ROOT/'check.sh')],capture_output=True,text=True)
    output=proc.stdout+proc.stderr
    (ROOT/'validation/pinned-replay.log').write_text(output)
    if proc.returncode: raise RuntimeError(output)
    imports=sorted({s.removeprefix('IMPORTED ') for s in output.splitlines() if s.startswith('IMPORTED ')}-set(MODULES))
    if imports!=sorted(r['module'] for r in data['actual_imports']): raise RuntimeError('Import closure changed')
    for flag,name in [([], 'normal'),(['-O'],'optimized')]:
        p=subprocess.run(['python3',*flag,str(ROOT/'test_transport.py')],capture_output=True,text=True,check=True)
        (ROOT/f'validation/python-{name}.json').write_text(p.stdout)
    if (ROOT/'validation/python-normal.json').read_bytes()!=(ROOT/'validation/python-optimized.json').read_bytes(): raise RuntimeError('Python modes disagree')
    tests=json.loads((ROOT/'validation/python-normal.json').read_text())
    fixture=json.loads((ROOT/'FIXTURE.json').read_text())
    def li(x): return '['+', '.join(li(a) if isinstance(a,list) else str(a) for a in x)+']'
    expected='def fixture : Cubes := ⟨'+', '.join(map(li,fixture['cubes']))+'⟩'
    if expected not in (ROOT/'SeededSourceControls.lean').read_text(): raise RuntimeError('Source fixture differs from rational constructor fixture')
    pins()
    receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'method':'four additive modules freshly kernel-checked --trust=0; retained dependencies reused, not rebuilt',
      'freeze_sha256':sha(ROOT/'CANDIDATE_FREEZE.json'),'source_boundary_sha256':sha(ROOT/'SOURCE_BOUNDARY.json'),
      'retained_pins':len(data['retained']),'retained_imports':len(imports),
      'python_checks':tests['count'],'python_exhaustive_rows':tests['exhaustive_rows'],
      'fixture_identity':True,'source_log_sha256':sha(ROOT/'validation/pinned-replay.log'),
      'python_log_sha256':sha(ROOT/'validation/python-normal.json'),
      'fresh_output':[s for s in output.splitlines() if s.startswith('Fresh output: ')][-1]}
    (ROOT/'validation/AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
