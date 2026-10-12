"""Run isolated semantic probes only after the one owned cold replay qualifies.
Does not compile any imported custom module or mutate the frozen packet.
"""
from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime
BASE=Path('private-locator:8f24556a330b05a11a95')
ROOT=Path(__file__).resolve().parent
COLD=BASE/'tranche5/global-parity-iff-independent-review/cold-v1'
MANIFEST='384f5a5feddbad0c1588fb9b482d587592b85f134370b86d97d090b8a0da31a9'
ENVROOT=BASE/'recovery-20261001/environment'
LEAN=ENVROOT/'toolchain/lean-4.19.0-linux/bin/lean'
MATHLIB=ENVROOT/'mathlib4'
BUILD=COLD/'global_parity_controller/build'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((COLD/'REPLAY_RESULT.json').read_text())
assert r['status']=='PASS', 'Qualified full replay is required; currently '+r['status']
assert r['input_manifest_sha256']==MANIFEST
suite=r['suites'][0]
assert suite['status']=='PASS' and len(suite['modules'])==89
assert suite['readback']['target_count']==888
assert sha(LEAN)==r['lean_sha256']
for m in suite['modules']:
    p=BUILD/(m['module'].replace('.','/')+'.olean')
    assert sha(p)==m['olean_sha256'], 'Changed qualified object '+m['module']
libs=[BUILD,MATHLIB/'.lake/build/lib/lean']
libs += sorted(p for p in (MATHLIB/'.lake/packages').glob('*/.lake/build/lib/lean') if p.is_dir())
env=dict(os.environ)
env.pop('LEAN_SRC_PATH',None)
env['LEAN_PATH']=':'.join(map(str,libs))
env['PATH']=str(LEAN.parent)+os.pathsep+env.get('PATH','')
files=sys.argv[1:] or ['SemanticBoundaryProbes.lean','SingletonOracleProbes.lean']
result={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'packet_manifest_sha256':MANIFEST,'qualified_replay_receipt_sha256':sha(COLD/'REPLAY_RESULT.json'),
        'lean_sha256':sha(LEAN),'probe_runner_sha256':sha(Path(__file__)),'lean_path':[str(p) for p in libs],
        'imported_object_count':len(suite['modules']),'probes':[]}
OUT=ROOT/'runs'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
OUT.mkdir(parents=True)
save=lambda:(OUT/'PROBE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
save()
for name in files:
    source=ROOT/name
    cmd=[str(LEAN),'-j1','--root='+str(ROOT),'-o',str(OUT/source.with_suffix('.olean').name),str(source)]
    run=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=OUT/source.with_suffix('.log').name;log.write_text(run.stdout)
    rr={'source':str(source),'sha256':sha(source),'exit':run.returncode,'command':cmd,'log':str(log),'log_sha256':sha(log)}
    result['probes'].append(rr);save();print(name,run.returncode,flush=True);print(run.stdout[:3000] if run.returncode else 'clean output; axiom readbacks='+str(run.stdout.count('depends on axioms:')),flush=True)
    if run.returncode:result['status']='PROBE_FAILURE';break
else:result['status']='PASS'
for m in suite['modules']:
    assert sha(BUILD/(m['module'].replace('.','/')+'.olean'))==m['olean_sha256']
result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
print('RESULT',OUT/'PROBE_RESULT.json',flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
