"""Rebuild only the unchanged prerequisite closure for literal shift proofs."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, os, re, subprocess

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'baseline'; OUT=ROOT/'build'; LOG=ROOT/'logs'
OUT.mkdir(exist_ok=True);LOG.mkdir(exist_ok=True)
LEAN=Path(os.environ.get('LEAN_HOME',str(ROOT.parent/'.toolchains/lean-4.19.0-linux')))/'bin/lean'
env=dict(os.environ,LEAN_PATH=str(OUT)+':'+os.environ['LEAN_PATH'])
(ROOT/'build_lean_path.txt').write_text(env['LEAN_PATH']+'\n')
mods={p.relative_to(SRC).with_suffix('').as_posix().replace('/','.'):p for p in SRC.rglob('*.lean')}
deps={k:{t for l in p.read_text().splitlines() if l.startswith('import ') for t in l.split()[1:] if t in mods} for k,p in mods.items()}
pins={r['module']:r['source_sha256'] for r in json.loads((ROOT/'inputs/BASELINE_REBUILD.json').read_text())['modules']}
needed=set()
def visit(k):
    if k in needed:return
    needed.add(k)
    for d in deps[k]:visit(d)
for k in ['LoopRenaming','CodecStmt','Q8Compiler']:visit(k)
for k in needed:
    if hashlib.sha256(mods[k].read_bytes()).hexdigest()!=pins[k]:raise RuntimeError('Source pin mismatch: '+k)
records=[];done=set()
def build(k):
    source=mods[k];output=OUT/(k.replace('.','/')+'.olean');output.parent.mkdir(parents=True,exist_ok=True)
    start=datetime.datetime.now(datetime.timezone.utc)
    result=subprocess.run([str(LEAN),'--trust=0','--root='+str(SRC),'-o',str(output),str(source)],env=env,cwd=ROOT,capture_output=True,text=True)
    (LOG/('baseline-'+k+'.log')).write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError(k+' failed\n'+result.stdout+result.stderr)
    print('PASS '+k,flush=True)
    return {'module':k,'source_sha256':pins[k],'object_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'started_utc':start.isoformat(),'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    while done!=needed:
        ready=sorted(k for k in needed-done if deps[k]<=done)
        if not ready:raise RuntimeError('Dependency cycle')
        records.extend(pool.map(build,ready));done.update(ready)
receipt={'scope':'Fresh trust=0 compilation of nine unchanged prerequisite modules, not all77 baseline modules.','trust':0,'modules':records}
(ROOT/'PREREQUISITE_REBUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
