#!/usr/bin/env python3
from pathlib import Path
import os,subprocess,re,json,hashlib,datetime
A=Path(__file__).resolve().parent;B=A.parent;R=B.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=A/'snapshot/FiniteHullSmoothRigidity.lean';expected='fbb94e84a7a0a02c42e6da70a04ff7e4db1a12cef2aa6608745d953216760523'
assert sha(source)==sha(R/'source-bridges/lean/FiniteHullSmoothRigidity.lean')==expected
for row in json.loads((B/'SOURCE_MANIFEST.json').read_text()):assert sha(R/row['origin'])==row['source_sha256']
robust=json.loads((B/'robustness-delta/RESULT.json').read_text());assert sha(R/'source-bridges/lean/SmoothRobustness.lean')==robust['source_sha256']
assert sha(B/'robustness-delta/build/SmoothRobustness.olean')==robust['logs']['SmoothRobustness']['olean_sha256']
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
for lib in env['LEAN_PATH'].split(':')[3:]:assert not(Path(lib)/'FiniteHullSmoothRigidity.olean').exists()
def parse(text):
 d={}
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",text):
  assert m[1] not in d
  d[m[1]]=[x.strip() for x in (m[2] or '').split(',') if x.strip()]
 assert all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in d.values())
 assert 'error:' not in text and 'sorryAx' not in text
 return d
axioms=parse((A/'logs/DeltaReadback.log').read_text());assert set(axioms)==set(json.loads((A/'TARGETS.json').read_text()))
controls=re.findall(r'^lemma\s+(\w+)',(A/'controls/HullControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import HullControls\n'+''.join(f'#check @HullAudit.{n}\n#print axioms HullAudit.{n}\n' for n in controls))
p=subprocess.run([str(lean),'--root='+str(A/'controls'),'-o',str(A/'build/ControlReadback.olean'),str(A/'controls/ControlReadback.lean')],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
(A/'logs/ControlReadback.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout
control_ax=parse(p.stdout);assert set(control_ax)=={'HullAudit.'+x for x in controls}
logs={}
for mod in ['FiniteHullSmoothRigidity','HullControls','DeltaReadback','ControlReadback']:
 text=(A/'logs'/(mod+'.log')).read_text();assert 'error:' not in text and 'sorryAx' not in text
 src=A/('snapshot' if mod=='FiniteHullSmoothRigidity' else 'controls')/(mod+'.lean')
 logs[mod]={'exit':0,'source_sha256':sha(src),'log_sha256':sha(A/'logs'/(mod+'.log')),'olean_sha256':sha(A/'build'/(mod+'.olean'))}
mutations=[('ConfuseTruthAndCoordinateCount','let N : ℝ := Fintype.card J','let N : ℝ := Fintype.card ι'),('ZeroBarycentricWeights','(hw : ∀ j, 0 < w j)','(hw : ∀ j, 0 ≤ w j)')]
negative=[]
for name,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True)
 src=source.read_text();assert old in src
 dest=d/'FiniteHullSmoothRigidity.lean';dest.write_text(src.replace(old,new))
 p=subprocess.run([str(lean),'--root='+str(d),str(dest)],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
 log=A/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout
 negative.append({'mutation':name,'exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log),'expected':'REJECT'})
 print(name,'REJECTED',flush=True)
res={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_geometry_audit_sha256':sha(B/'Geometry_Independent_Audit_20260930.zip'),'base_robustness_audit_sha256':sha(B/'robustness-delta/Smooth_Robustness_Independent_Audit_20260930.zip'),'source_sha256':sha(source),'source_original_unchanged':True,'source_readbacks':axioms,'logs':logs,'positive_control_theorems':controls,'control_readbacks':control_ax,'general_hull_type_guard':True,'negative_mutations':negative}
(A/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
