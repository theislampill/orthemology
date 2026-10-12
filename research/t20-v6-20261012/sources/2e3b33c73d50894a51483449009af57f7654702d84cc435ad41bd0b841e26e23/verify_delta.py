#!/usr/bin/env python3
from pathlib import Path
import re,json,hashlib,subprocess,os,datetime
A=Path(__file__).resolve().parent;B=A.parent;R=B.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'FiniteHullApproximateIff':'4404099e3cff80cde3c34a81bb6d4af0c2015d053ef26a78378e351e806b8c91','IntrinsicBarycentric':'4792328206bd362737bf4db247b62abab5c31d81583b9ecec8de43f759f1ab78'}
for mod,h in expected.items():assert sha(A/'snapshot'/(mod+'.lean'))==sha(R/'source-bridges/lean'/(mod+'.lean'))==h
for row in json.loads((B/'SOURCE_MANIFEST.json').read_text()):assert sha(R/row['origin'])==row['source_sha256']
for folder,mod in [('robustness-delta','SmoothRobustness'),('finite-hull-delta','FiniteHullSmoothRigidity')]:
 r=json.loads((B/folder/'RESULT.json').read_text());assert sha(R/'source-bridges/lean'/(mod+'.lean'))==r['source_sha256'];assert sha(B/folder/'build'/(mod+'.olean'))==r['logs'][mod]['olean_sha256']
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
for lib in env['LEAN_PATH'].split(':')[4:]:
 for mod in expected:assert not(Path(lib)/(mod+'.olean')).exists()
def parse(t):
 assert 'error:' not in t and 'sorryAx' not in t
 ax={}
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",t):
  assert m[1] not in ax
  ax[m[1]]=[x.strip() for x in (m[2] or '').split(',') if x.strip()]
 assert all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in ax.values())
 return ax
ax=parse((A/'logs/DeltaReadback.log').read_text());assert set(ax)==set(json.loads((A/'TARGETS.json').read_text()))
controls=re.findall(r'^lemma\s+(\w+)',(A/'controls/InterfaceControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import InterfaceControls\n'+''.join(f'#check @HullInterfaceAudit.{n}\n#print axioms HullInterfaceAudit.{n}\n' for n in controls))
p=subprocess.run([str(lean),'--root='+str(A/'controls'),'-o',str(A/'build/ControlReadback.olean'),str(A/'controls/ControlReadback.lean')],cwd=R/'toolchain/mathlib4',env=env,text=True,capture_output=True)
(A/'logs/ControlReadback.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout
cax=parse(p.stdout);assert set(cax)=={'HullInterfaceAudit.'+x for x in controls}
logs={}
for mod in list(expected)+['InterfaceControls','DeltaReadback','ControlReadback']:
 t=(A/'logs'/(mod+'.log')).read_text();assert 'error:' not in t and 'sorryAx' not in t
 src=A/('snapshot' if mod in expected else 'controls')/(mod+'.lean')
 logs[mod]={'exit':0,'source_sha256':sha(src),'log_sha256':sha(A/'logs'/(mod+'.log')),'olean_sha256':sha(A/'build'/(mod+'.olean'))}
mutations=[('BoundaryInsteadOfRelativeInterior','IntrinsicBarycentric','(hp : p ∈ intrinsicInterior ℝ (convexHull ℝ (Set.range v)))','(hp : p ∈ convexHull ℝ (Set.range v))'),('ForceZeroTolerance','FiniteHullApproximateIff','let eta : ℕ → ℝ := fun n => ∑ k, ∑ j, |D n k j|','let eta : ℕ → ℝ := fun _ => 0')]
negative=[]
for name,mod,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);s=(A/'snapshot'/(mod+'.lean')).read_text();assert old in s
 dest=d/(mod+'.lean');dest.write_text(s.replace(old,new))
 p=subprocess.run([str(lean),'--root='+str(d),str(dest)],cwd=R/'toolchain/mathlib4',env=env,text=True,capture_output=True)
 log=A/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout
 negative.append({'mutation':name,'exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log),'expected':'REJECT'});print(name,'REJECTED',flush=True)
r={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_finite_hull_audit_sha256':sha(B/'finite-hull-delta/Finite_Hull_Independent_Audit_20260930.zip'),'new_sources':expected,'original_sources_unchanged':True,'source_readbacks':ax,'logs':logs,'positive_control_theorems':controls,'control_readbacks':cax,'intrinsic_approximate_iff_type_guard':True,'finite_controls_sha256':sha(A/'FINITE_CONTROLS.json'),'negative_mutations':negative}
(A/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
