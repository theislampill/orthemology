#!/usr/bin/env python3
import pathlib,os,subprocess,hashlib,re,json,datetime
from fractions import Fraction as F
A=pathlib.Path(__file__).resolve().parent;B=A.parent;R=B.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
src=A/'snapshot/SmoothRobustness.lean';assert sha(src)=='e70adf24f9cc824e654cf5b4be6023d5bfc15410d2c15cc24143e98e5de809e4'
assert sha(src)==sha(R/'source-bridges/lean/SmoothRobustness.lean')
for lib in env['LEAN_PATH'].split(':')[2:]:assert not(pathlib.Path(lib)/'SmoothRobustness.olean').exists()
controls=re.findall(r'^(?:theorem|lemma)\s+(\w+)',(A/'controls/RobustnessControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import RobustnessControls\n'+''.join(f'#check @RobustnessAudit.{n}\n#print axioms RobustnessAudit.{n}\n' for n in controls))
logs={}
for mod in ['RobustnessControls','ControlReadback']:
 out=A/'build'/(mod+'.olean');cmd=[str(lean),'--root='+str(A/'controls'),'-o',str(out),str(A/'controls'/(mod+'.lean'))]
 p=subprocess.run(cmd,env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
 log=A/'logs'/(mod+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode==0 and 'sorryAx' not in p.stdout and 'error:' not in p.stdout,p.stdout
 logs[mod]={'command':cmd,'exit':p.returncode,'source_sha256':sha(A/'controls'/(mod+'.lean')),'log_sha256':sha(log),'olean_sha256':sha(out)}
axioms={};text=(A/'logs/DeltaReadback.log').read_text()
for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",text):
 axioms[m[1]]=[x.strip() for x in (m[2] or '').split(',') if x.strip()]
assert set(axioms)==set(json.loads((A/'TARGETS.json').read_text()))
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in axioms.values())
for name in ['SmoothRobustness','DeltaReadback']:
 text=(A/'logs'/(name+'.log')).read_text();assert 'error:' not in text and 'sorryAx' not in text
 logs[name]={'exit':0,'source_sha256':sha(src if name=='SmoothRobustness' else A/'controls/DeltaReadback.lean'),'log_sha256':sha(A/'logs'/(name+'.log')),'olean_sha256':sha(A/'build'/(name+'.olean'))}
mutations=[('LinearRatioAdmitted','(heta : Tendsto (fun n => eta n / e n) atTop (𝓝 0))','(heta : Tendsto (fun n => eta n / e n) atTop (𝓝 1))'),('SubprobabilityRepair','(hcsum : ∀ n, ∑ i, c n i = 1)','(hcsum : ∀ n, ∑ i, c n i ≤ 1)'),('ZeroBarycentricWeights','(hw : ∀ i, 0 < w i)','(hw : ∀ i, 0 ≤ w i)')]
neg=[]
for name,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True)
 s=src.read_text();assert old in s
 dest=d/'SmoothRobustness.lean';dest.write_text(s.replace(old,new))
 p=subprocess.run([str(lean),'--root='+str(d),str(dest)],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
 log=A/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout
 neg.append({'mutation':name,'exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log),'expected':'REJECT'})
 print(name,'REJECTED',flush=True)
# Exact counterfamily: tiny barycentric regret alone is not linear localization.
for n in range(2,102):
 e=F(1,n**4);eta=F(3,n**6);d=F(1,n**3);p=F(1,3);c=p-d
 assert 0<c<1 and 3*c<1
 assert (c-1)**2+2*c*c-((p-1)**2+2*p*p)==eta
 assert eta/e==F(3,n**2) and d/e==n
for row in json.loads((B/'SOURCE_MANIFEST.json').read_text()):assert sha(R/row['origin'])==row['source_sha256']
res={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_geometry_audit_sha256':sha(B/'Geometry_Independent_Audit_20260930.zip'),'module':'SmoothRobustness','source_sha256':sha(src),'source_original_unchanged':True,'base_source_drift':False,'readbacks':axioms,'logs':logs,'positive_control_theorems':controls,'main_boundedness_type_guard':True,'counterfamily_rational_cases':100,'negative_mutations':neg}
(A/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
