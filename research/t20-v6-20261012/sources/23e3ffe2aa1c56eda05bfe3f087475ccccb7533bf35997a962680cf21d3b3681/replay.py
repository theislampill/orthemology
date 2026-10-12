from pathlib import Path
import subprocess,os,json,hashlib,shutil,datetime,tempfile
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-rational-kernel-transport-20261011'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=C/'CANDIDATE_FREEZE.json';freeze=json.loads(f.read_text());fh=H(f)
entries=freeze['files']
def check():
 for e in entries:
  p=C/e.get('name',e.get('path',''))
  assert H(p)==e['sha256'],str(p)
check()
sourcepins=json.loads((W/'hase-finite-sidecar-independent-review-20261011/INHERITED_SOURCES_BEFORE.json').read_text())['files']
def checksources():
 for e in sourcepins:
  p=Path(e['path']);p=p if p.is_absolute() else W/p
  assert H(p)==e['sha256'],str(p)
checksources()
d=R/'candidate';d.mkdir(exist_ok=True)
for e in entries:
 p=C/e.get('name',e.get('path',''));q=d/p.relative_to(C);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.copy2(f,R/'CANDIDATE_FREEZE.json')
env=os.environ.copy();base=subprocess.check_output(['bash','-c',f'source {C}/env.sh; printf "ACTUAL_LEAN_PATH=%s\\n" "$LEAN_PATH"'],text=True)
base=next(s.removeprefix('ACTUAL_LEAN_PATH=') for s in base.splitlines() if s.startswith('ACTUAL_LEAN_PATH='))
assert str(C/'validation') not in base
pins={}
for root in base.split(':'):
 for p in Path(root).rglob('*.olean'):
  n=str(p.relative_to(root))
  if n not in pins:pins[n]={'path':str(p),'sha256':H(p)}
(R/'INHERITED_OBJECTS.json').write_text(json.dumps(pins,indent=2))
lib=Path(tempfile.mkdtemp(prefix='fresh-replay-',dir=R));env['LEAN_PATH']=str(lib)+':'+base
(R/'LEAN_PATH.txt').write_text(env['LEAN_PATH'])
mods=['SeededSourceLookup','SeededSourceHistories','SeededSourceControls','SeededSourceAudit','IndependentBoundaries','IndependentAudit'];results=[]
for m in mods:
 p=(R if m.startswith('Independent') else d)/(m+'.lean')
 if not p.exists():continue
 cmd=[str(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'--trust=0','-o',str(lib/(m+'.olean')),str(p)]
 t=subprocess.run(cmd,env=env,cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(m+'.log')).write_text(t.stdout);print(m,t.returncode,flush=True)
 assert t.returncode==0 and all(x not in t.stdout for x in ['sorryAx',': error:',': warning:']),t.stdout
 results.append({'module':m,'source_sha256':H(p),'object_sha256':H(lib/(m+'.olean')),'exit':t.returncode})
check();checksources();assert H(f)==fh
for e in pins.values():assert H(Path(e['path']))==e['sha256'],e['path']
(R/'REPLAY.json').write_text(json.dumps({'status':'PASS','freeze_sha256':fh,'trust':0,'results':results,'inherited_object_count':len(pins),'candidate_and_inherited_objects_unchanged':True,'candidate_import_path_excluded':True,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))

for name in ['rational_kernel.py','test_transport.py','FIXTURE.json']:
 shutil.copy2(d/name,R/name)
t=subprocess.run(['python3',str(R/'test_transport.py')],cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(R/'AUTHOR_PYTHON_REPLAY.json').write_text(t.stdout)
assert t.returncode==0,t.stdout
assert H(R/'FIXTURE.json')==H(d/'FIXTURE.json'),'Fixture regenerated differently'
print('PASS Python replay and identical fixture',flush=True)
