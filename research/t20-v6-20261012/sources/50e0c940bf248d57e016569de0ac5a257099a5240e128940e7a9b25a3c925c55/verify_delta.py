#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import re,json,hashlib,os,subprocess,datetime
A=Path(__file__).resolve().parent;B=A.parent;R=B.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'NudgeRigidity':'50968a1703261df4e2794636cbdddca8e0e1a5867854a27e543bc83b0a9afc46','CoherentNudgeRigidity':'229b7273ce75c5e119f18593fe95901e5b4f049ccd99fef9303bda3278080917'}
for mod,h in expected.items():assert sha(A/'snapshot'/(mod+'.lean'))==sha(R/'source-bridges/lean'/(mod+'.lean'))==h
for row in json.loads((B/'SOURCE_MANIFEST.json').read_text()):assert sha(R/row['origin'])==row['source_sha256']
robust=json.loads((B/'robustness-delta/RESULT.json').read_text());assert sha(R/'source-bridges/lean/SmoothRobustness.lean')==robust['source_sha256']
assert sha(B/'robustness-delta/build/SmoothRobustness.olean')==robust['logs']['SmoothRobustness']['olean_sha256']
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
for lib in env['LEAN_PATH'].split(':')[3:]:
 for mod in expected:assert not(Path(lib)/(mod+'.olean')).exists()
log=(A/'logs/DeltaReadback.log').read_text();assert 'error:' not in log and 'sorryAx' not in log
axioms={}
for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",log):
 axioms[m[1]]=[x.strip() for x in (m[2] or '').split(',') if x.strip()]
assert set(axioms)==set(json.loads((A/'TARGETS.json').read_text()))
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in axioms.values())
controls=re.findall(r'^lemma\s+(\w+)',(A/'controls/NudgeControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import NudgeControls\n'+''.join(f'#check @NudgeAudit.{n}\n#print axioms NudgeAudit.{n}\n' for n in controls))
p=subprocess.run([str(lean),'--root='+str(A/'controls'),'-o',str(A/'build/ControlReadback.olean'),str(A/'controls/ControlReadback.lean')],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
(A/'logs/ControlReadback.log').write_text(p.stdout+p.stderr)
assert p.returncode==0 and 'sorryAx' not in p.stdout,p.stdout
logs={}
for mod in list(expected)+['NudgeControls','DeltaReadback','ControlReadback']:
 text=(A/'logs'/(mod+'.log')).read_text();assert 'error:' not in text and 'sorryAx' not in text
 src=A/('snapshot' if mod in expected else 'controls')/(mod+'.lean')
 logs[mod]={'exit':0,'source_sha256':sha(src),'log_sha256':sha(A/'logs'/(mod+'.log')),'olean_sha256':sha(A/'build'/(mod+'.olean'))}
mutations=[('NonStrictNudges','NudgeRigidity','< 0','≤ 0'),('UnnormalisedCoherentEndpoint','CoherentNudgeRigidity','base n i - e n * A n i / S n','base n i - e n * A n i')]
negative=[]
for name,mod,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True)
 src=(A/'snapshot'/(mod+'.lean')).read_text();assert old in src
 dest=d/(mod+'.lean');dest.write_text(src.replace(old,new))
 p=subprocess.run([str(lean),'--root='+str(d),str(dest)],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
 log=A/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout
 negative.append({'mutation':name,'exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log),'expected':'REJECT'})
 print(name,'REJECTED',flush=True)
b=[F(1,2),F(7,20),F(7,20)];d=[F(-13,10),F(-1),F(-1)];c=[F(139,330),F(191,660),F(191,660)]
derivatives=[]
for w in [[1,1,1],[1,2,2]]:
 vals=[sum(2*w[i]*(b[i]-(i==j))*d[i] for i in range(3)) for j in range(3)]
 assert all(x<0 for x in vals);derivatives.append(list(map(str,vals)))
assert sum(c)==1 and all(0<x<1 for x in c)
assert all(c[i]-b[i]==F(2,33)*d[i] for i in range(3))
res={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_geometry_audit_sha256':sha(B/'Geometry_Independent_Audit_20260930.zip'),'base_robustness_audit_sha256':sha(B/'robustness-delta/Smooth_Robustness_Independent_Audit_20260930.zip'),'new_sources':expected,'original_sources_unchanged':True,'readbacks':axioms,'logs':logs,'positive_control_theorems':controls,'universal_type_guards':2,'pointwise_separator':{'b':list(map(str,b)),'direction':list(map(str,d)),'coherent_target':list(map(str,c)),'actual_derivatives':derivatives,'kernel_theorems':['NudgeAudit.pointwise_strict_common_nudge','NudgeAudit.no_pointwise_common_coherent_endpoint','NudgeAudit.pointwise_coherent_directed_nudge']},'negative_mutations':negative}
(A/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
