#!/usr/bin/env python3
"""Recheck pinned reuse, then compile only the three new discriminating controls."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
bind=json.loads((R/'INPUTS.json').read_text())
def checks():
 for row in [bind['receipt']]+bind['bound_inputs']+bind['reused_objects']:
  assert sha(W/row['path'])==row['sha256'], row['path']
 assert sha(W/'.toolchains/lean-4.19.0-linux/bin/lean')==bind['lean_binary_sha256']
checks()
out=Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
libs=[W/'hase-full-per-review-20261010/fresh-lib']+list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[out]+libs))}
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'; records=[]; logs=[]
for m in ['SourceControls','FamilyObstructions','StructuredObserver']:
 p=R/(m+'.lean'); s=re.sub(r'/\-.*?\-/','',p.read_text(),flags=re.S);s=re.sub(r'--[^\n]*','',s)
 assert not re.findall(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',s),m
 cmd=[str(lean),'--trust=0','-o',str(out/(m+'.olean')),str(p)]
 r=subprocess.run(cmd,env=env,text=True,capture_output=True);log=r.stdout+r.stderr
 logs.append('$ '+' '.join(cmd)+'\n'+log)
 assert r.returncode==0,(m,log)
 assert not any(t in log for t in ['warning:','error:','sorryAx']),(m,log)
 ax=set()
 for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
  ax.update(re.sub(r'\s+','',match).split(','))
 assert ax <= {'propext','Classical.choice','Quot.sound'}
 records.append({'module':m,'source_sha256':sha(p),'object_sha256':sha(out/(m+'.olean')),'trust_zero':True,'axioms':sorted(ax),'exit_code':r.returncode})
 print(m,'PASS')
checks()
(R/'validation/REPLAY.log').write_text('\n'.join(logs))
(R/'validation/REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(out.relative_to(R)),'scope':'Only exact-source family-coherence controls and explicitly conditional set-family obstructions; no whole-source model, universal target, source noninhabitation, or baseline rebuild.','modules':records},indent=2)+'\n')
