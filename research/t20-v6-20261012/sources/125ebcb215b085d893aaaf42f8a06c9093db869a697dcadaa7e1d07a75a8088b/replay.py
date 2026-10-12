#!/usr/bin/env python3
"""Replay only the three frozen typed-observer core modules, retaining old objects."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=json.loads((R/'INPUTS.json').read_text())
def check():
 for row in bind['bound_inputs']:
  assert sha(W/row['path'])==row['sha256'],row['path']
 old=json.loads((W/'hase-type-indexed-henkin-obstruction-20261010/INPUTS.json').read_text())
 for row in [old['receipt']]+old['bound_inputs']+old['reused_objects']:
  assert sha(W/row['path'])==row['sha256'],row['path']
 assert sha(W/'.toolchains/lean-4.19.0-linux/bin/lean')==old['lean_binary_sha256']
check()
out=Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
paths=[out,W/'hase-type-indexed-henkin-obstruction-20261010/validation',
 W/'hase-internal-graph-review-20261010/fresh-lib',W/'hase-full-per-review-20261010/fresh-lib']
paths+=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,paths))}
records=[];logs=[]
for m in ['TypedObserver','TypedObservations','TypedFamilyContract']:
 p=R/(m+'.lean');src=re.sub(r'/\-.*?\-/','',p.read_text(),flags=re.S);src=re.sub(r'--[^\n]*','',src)
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',src),m
 cmd=[str(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'--trust=0','-o',str(out/(m+'.olean')),str(p)]
 r=subprocess.run(cmd,env=env,text=True,capture_output=True);log=r.stdout+r.stderr
 logs.append('$ '+' '.join(cmd)+'\n'+log)
 assert r.returncode==0,(m,log)
 assert not any(x in log for x in ['warning:','error:','sorryAx']),(m,log)
 ax=set()
 for a in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
  ax.update(re.sub(r'\s+','',a).split(','))
 assert ax <= {'propext','Classical.choice','Quot.sound'}
 records.append({'module':m,'source_sha256':sha(p),'object_sha256':sha(out/(m+'.olean')),'exit_code':r.returncode,'trust_zero':True,'axioms':sorted(ax)})
 print(m,'PASS')
check()
(R/'validation/REPLAY.log').write_text('\n'.join(logs))
(R/'validation/REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(out.relative_to(R)),'scope':'Generic original-Has typed observer, HasE identities, conditional fixed-body-family coherence. No cross-typing module, baseline rebuild, universal W or noninhabitation.','modules':records},indent=2)+'\n')
