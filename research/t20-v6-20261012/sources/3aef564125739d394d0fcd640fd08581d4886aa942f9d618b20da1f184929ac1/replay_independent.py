#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, re, os, subprocess, tempfile
R=Path(__file__).resolve().parent; W=R.parent
A=W/'hase-type-indexed-henkin-obstruction-20261010'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A/'MANIFEST.json')=='b18b9bb4dc32125bc163c8185e71841fae3a6882669ec612245b6b66121b3412'
manifest=json.loads((A/'MANIFEST.json').read_text())
bind=json.loads((A/'INPUTS.json').read_text())
before={}
def check():
 for x in manifest['files']:
  p=A/x['path']; assert sha(p)==x['sha256'],str(p)
 for x in [bind['receipt']]+bind['bound_inputs']+bind['reused_objects']:
  p=W/x['path']; assert sha(p)==x['sha256'],str(p)
 assert sha(W/'.toolchains/lean-4.19.0-linux/bin/lean')==bind['lean_binary_sha256']
check()
pre=json.loads((W/bind['receipt']['path']).read_text())
assert pre['pin']==bind['source_pin'] and pre['mathlib_revision']==bind['mathlib_revision']
source_map={x['module']:x for x in pre['source_checks']}
for x in bind['bound_inputs']:
 if x.get('verified_against')=='PREREQUISITE_REBUILD.json/source_checks':
  v=source_map[Path(x['path']).stem]
  assert v['sha256']==x['sha256'] and v['git_blob']==x['git_blob']
object_map={x['module']:x for x in pre['build_records']}
for x in bind['reused_objects']:
 if x['path'].startswith('hase-full-per-review-20261010/fresh-lib/'):
  v=object_map[x['path'].split('/fresh-lib/')[1][:-6].replace('/','.')]
  assert v['object_sha256']==x['sha256']
# Hash the unchanged 83 source closure as an independent provenance check, no compile.
source_checks=[]
for m,v in source_map.items():
 p=W/'hase-imported-compiler-transport-20261010/sources'/f'{m}.lean'
 assert sha(p)==v['sha256'],str(p)
 source_checks.append({'module':m,'sha256':sha(p)})
libs=[W/'hase-full-per-review-20261010/fresh-lib']+sorted((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
out=Path(tempfile.mkdtemp(prefix='independent-',dir=R/'validation'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[out]+libs))}
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
modules=[(A,x) for x in ['SourceControls','FamilyObstructions','StructuredObserver']]+[(R,'IndependentControls')]
if (R/'Dependencies.lean').exists(): modules.append((R,'Dependencies'))
records=[]; logs=[]
for base,m in modules:
 p=base/(m+'.lean'); text=p.read_text(); clean=re.sub(r'/\-.*?\-/','',text,flags=re.S); clean=re.sub(r'--[^\n]*','',clean)
 assert not re.findall(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',clean)
 before[str(p)]=sha(p)
 cmd=[str(lean),'--trust=0','-o',str(out/(m+'.olean')),str(p)]
 r=subprocess.run(cmd,env=env,text=True,capture_output=True); log=r.stdout+r.stderr
 logs.append('$ '+' '.join(cmd)+'\n'+log)
 (R/'validation'/f'{m}.log').write_text(log)
 assert r.returncode==0,(m,log)
 assert not any(z in log for z in ['warning:','error:','sorryAx']),(m,log)
 axioms=set()
 for value in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
  axioms.update(filter(None,re.sub(r'\s+','',value).split(',')))
 assert axioms <= {'propext','Quot.sound','Classical.choice'},(m,axioms)
 records.append({'module':m,'source_sha256':sha(p),'object_sha256':sha(out/(m+'.olean')),'trust_zero':True,'exit_code':r.returncode,'reported_axioms':sorted(axioms)})
 print(m,'PASS',flush=True)
check()
assert all(sha(Path(p))==v for p,v in before.items())
(R/'validation/REPLAY.log').write_text('\n'.join(logs))
(R/'validation/RECEIPT.json').write_text(json.dumps({'status':'PASS','scope':'Independent frozen-delta replay and reviewer-only controls. Reused inherited objects. No 83-module rebuild, whole-model claim, source-target proof, integration, or formal audit-service status.','author_manifest_sha256':sha(A/'MANIFEST.json'),'author_result_sha256':sha(A/'RESULT.md'),'lean_binary_sha256':sha(lean),'source_pin':pre['pin'],'mathlib_revision':pre['mathlib_revision'],'source_closure_hash_checks':source_checks,'reused_object_count':len(bind['reused_objects']),'fresh_output':str(out.relative_to(R)),'modules':records},indent=2)+'\n')
