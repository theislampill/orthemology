#!/usr/bin/env python3
import pathlib,os,subprocess,hashlib,re,json,datetime
A=pathlib.Path(__file__).resolve().parent;R=A.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for dirname,module,ctrl in [('approximate-delta','ApproximateRepairIdentification','ApproximateControls'),('blind-delta','BlindGuessSharpness','BlindControls')]:
 d=A/dirname;src=d/'snapshot'/(module+'.lean');orig=R/'root-research/lean'/(module+'.lean')
 assert sha(src)==sha(orig)
 record={'module':module,'source_sha256':sha(src),'original':str(orig.relative_to(R)),'readbacks':{},'logs':{}}
 for name in [module,ctrl,'DeltaReadback']:
  log=d/'logs'/(name+'.log');s=log.read_text()
  assert 'error:' not in s and 'sorryAx' not in s,(name,s)
  out=d/'build'/(name+'.olean');assert out.exists()
  record['logs'][name]={'source_sha256':sha(src if name==module else d/'controls'/(name+'.lean')),'exit':0,'log_sha256':sha(log),'olean_sha256':sha(out)}
 text=(d/'logs/DeltaReadback.log').read_text()
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",text):
  deps=[x.strip() for x in (m[2] or '').split(',') if x.strip()]
  assert set(deps)<={'propext','Classical.choice','Quot.sound'}
  record['readbacks'][m[1]]=deps
 assert len(record['readbacks'])==6
 results.append(record)
mutations=[('approximate-delta','ApproximateRepairIdentification','LinearRatioWronglyAllowed','(hratio : Tendsto (fun n => eta n / e n) atTop (𝓝 0))','(hratio : Tendsto (fun n => eta n / e n) atTop (𝓝 1))'),('blind-delta','BlindGuessSharpness','ChangingBlindSeed','def blindNext (guess : ℝ) (_ : Bool) : ℝ := guess','def blindNext (guess : ℝ) (_ : Bool) : ℝ := guess+1')]
neg=[]
for dirname,module,name,old,new in mutations:
 d=A/dirname;md=d/'mutations'/name;md.mkdir(parents=True,exist_ok=True)
 s=(d/'snapshot'/(module+'.lean')).read_text();assert s.count(old)==1
 dest=md/(module+'.lean');dest.write_text(s.replace(old,new))
 env=dict(os.environ,LEAN_PATH=(d/'LEAN_PATH.txt').read_text().strip())
 p=subprocess.run([str(R/'toolchain/lean-4.19.0-linux/bin/lean'),'--root='+str(md),str(dest)],env=env,cwd=R/'toolchain/mathlib4',text=True,capture_output=True)
 log=d/'logs'/(name+'.log');log.write_text(p.stdout+p.stderr)
 assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout
 neg.append({'mutation':name,'exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log),'expected':'REJECT'})
 print(name,'REJECTED',flush=True)
for row in json.loads((A/'SOURCE_MANIFEST.json').read_text()):assert sha(R/row['origin'])==row['source_sha256']
(A/'DELTAS_RESULT.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_audit_zip_sha256':sha(A/'Causal_Query_Independent_Audit_20260930.zip'),'new_modules':results,'positive_control_theorems':6,'explicit_approximate_main_type_guard':True,'negative_mutations':neg,'base_source_drift':False},indent=2)+'\n')
