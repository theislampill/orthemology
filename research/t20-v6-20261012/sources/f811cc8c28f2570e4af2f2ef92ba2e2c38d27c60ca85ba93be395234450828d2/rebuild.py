from pathlib import Path
import json,re,os,subprocess,shutil,hashlib,time
W=Path.cwd();R=W/'hase-joint-proof-uniqueness-independent-review-20261010';C=W/'hase-joint-proof-uniqueness-20261010'
b=json.load(open(C/'SOURCE_BOUNDARY.json')); paths=b['lean_path'].split(':'); mapping={}
bindings=json.load(open(W/'joint-computation-preservation-20261010/Joint_Induction_Computation_Intermediate_Evidence_20261010/prerequisites/IMPORT_BINDINGS.json'))
for x in bindings:
 if x.get('source',{}).get('root')=='retained':mapping[x['module']]=W/x['source']['path']
# Respect current path precedence for newly added sources; prior explicit source bindings win when directory has no adjacent source.
for p in reversed(paths):
 p=Path(p)
 if '.lake' in p.parts:continue
 for d in [p.parent,p]:
  if d.exists():
   for s in d.glob('*.lean'):mapping[s.stem]=s
for s in C.glob('*.lean'):mapping[s.stem]=s
roots=['JointProofUniqueness','OriginalProofUniqueness','ProofUniquenessControls','ProofUniquenessAudit'];order=[];seen=set()
def visit(m):
 if m in seen:return
 seen.add(m)
 if m not in mapping:
  if m.startswith(('Mathlib.','Batteries.','Aesop.','Qq.','ImportGraph.','LeanSearchClient.','Plausible.','ProofWidgets.')):return
  assert any((Path(p)/(m.replace('.','/')+'.olean')).exists() for p in paths if '.lake' in Path(p).parts) or m=='Lean' or m.startswith(('Lean.','Init','Std')),m
  return
 s=mapping[m]
 for line in s.read_text().splitlines():
  if line.startswith('import '):
   for dep in line.split()[1:]:
    if dep.startswith('--'):break
    visit(dep)
 order.append(m)
for m in roots:visit(m)
lib=R/'fresh-lib';lib.mkdir(exist_ok=True);src=R/'sources';src.mkdir(exist_ok=True)
rows=[]
for p in paths:
 if '.lake' in Path(p).parts:
  for obj in Path(p).rglob('*.olean'):
   q=lib/obj.relative_to(p);q.parent.mkdir(parents=True,exist_ok=True)
   if not q.exists():q.symlink_to(obj)
for x in bindings:
 if x.get('source',{}).get('root')=='packages' and x.get('object',{}).get('root')=='retained':
  p=W/x['object']['path'];q=lib/(x['module'].replace('.','/')+'.olean');q.parent.mkdir(parents=True,exist_ok=True)
  if q.exists():
   assert hashlib.sha256(q.read_bytes()).digest()==hashlib.sha256(p.read_bytes()).digest()
  else:shutil.copy2(p,q)
for m in order:
 s=mapping[m];q=src/(m.replace('.','/')+'.lean');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,q)
 rows.append({'module':m,'original':str(s.relative_to(W)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
(R/'SOURCE_INPUTS.json').write_text(json.dumps(rows,indent=2))
env=os.environ.copy();env['LEAN_PATH']=':'.join([str(lib)]+[p for p in paths if '.lake' in Path(p).parts]);(R/'LEAN_PATH.txt').write_text(env['LEAN_PATH'])
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean';print('BUILD',len(order),'project source modules',flush=True)
for n,m in enumerate(order):
 q=src/(m.replace('.','/')+'.lean');o=lib/(m.replace('.','/')+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run([str(lean),'--trust=0','-o',str(o),str(q)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(m.replace('.','_')+'.log')).write_text(r.stdout);print(n+1,m,r.returncode,flush=True)
 if r.returncode: print(r.stdout,flush=True);raise SystemExit(r.returncode)
 assert 'declaration uses \'sorry\'' not in r.stdout
(R/'REBUILD_PASS.json').write_text(json.dumps({'status':'PASS','module_count':len(order),'lean_path':env['LEAN_PATH'],'trust':0},indent=2))
