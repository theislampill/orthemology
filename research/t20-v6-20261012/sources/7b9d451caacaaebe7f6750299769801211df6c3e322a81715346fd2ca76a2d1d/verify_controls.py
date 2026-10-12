#!/usr/bin/env python3
import pathlib,subprocess,os,json,re,hashlib,datetime
A=pathlib.Path(__file__).resolve().parent;R=A.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
targets=json.loads((A/'TARGETS.json').read_text());log=(A/'logs/TargetReadback.log').read_text()
axioms={}
for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",log):
 name=m[1];assert name not in axioms
 axioms[name]=sorted(x.strip() for x in (m[2] or '').split(',') if x.strip())
assert set(axioms)==set(targets),(set(targets)-set(axioms),set(axioms)-set(targets))
assert all(set(a)<=set(['propext','Classical.choice','Quot.sound']) for a in axioms.values())
assert 'error:' not in log and 'sorryAx' not in log
(A/'AXIOM_READBACK.json').write_text(json.dumps({'status':'PASS','target_count':len(targets),'source_manifest_sha256':sha(A/'SOURCE_MANIFEST.json'),'readback_sha256':sha(A/'logs/TargetReadback.log'),'targets':axioms},indent=2)+'\n')
controls=re.findall(r'^(?:theorem|lemma)\s+(\w+)',(A/'controls/GeometryControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import GeometryControls\n'+''.join(f'#check @GeometryAudit.{n}\n#print axioms GeometryAudit.{n}\n' for n in controls))
p=subprocess.run([str(lean),'--root='+str(A/'controls'),str(A/'controls/ControlReadback.lean')],cwd=R/'toolchain/mathlib4',env=env,text=True,capture_output=True)
(A/'logs/ControlReadback.log').write_text(p.stdout+p.stderr)
assert p.returncode==0 and 'sorryAx' not in p.stdout,p.stdout
mutations=[('OnlyTwoOutcomes','BregmanProjection','(hcard : 3 ≤ Fintype.card ι)','(hcard : 2 ≤ Fintype.card ι)'),('ZeroPerturbation','BregmanProjection','(p + e n • vertex i0)','(p + e n • (0 : Vec ι))'),('ReverseBregman','SmoothRigidity','F v - F b - G b (v - b)','F b - F v - G v (b - v)'),('ZeroCurvatureAllowed','SmoothScalar','positive : ∀ x ∈ Ioo 0 1, 0 < ddf x','positive : ∀ x ∈ Ioo 0 1, 0 ≤ ddf x')]
results=[]
for name,module,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True)
 src=(A/'snapshot'/(module+'.lean')).read_text();assert old in src
 dest=d/(module+'.lean');dest.write_text(src.replace(old,new))
 p=subprocess.run([str(lean),'--root='+str(d),str(dest)],cwd=R/'toolchain/mathlib4',env=env,text=True,capture_output=True)
 log=A/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout,(name,p.stdout)
 results.append({'name':name,'module':module,'old':old,'new':new,'expected':'REJECT','exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log)})
 print(name,'REJECTED',flush=True)
(A/'CONTROL_RESULT.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'positive_theorems':controls,'positive_count':len(controls),'main_type_guard':True,'mutations':results},indent=2)+'\n')
