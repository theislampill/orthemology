from pathlib import Path
import json,subprocess,os,hashlib,datetime
R=Path(__file__).resolve().parent; base=json.loads((R/'RESULT.json').read_text());env=dict(os.environ);env['LEAN_PATH']=base['lean_path']
mutations=[
 ('omit_index_lift','P01DependentSubstitution','fun n => substIndex (fun k => .var (k+1)) (σ n)','fun n => σ n'),
 ('omit_type_lift','P01DependentSubstitution','| n+1 => renameType Nat.succ (σ n)','| n+1 => σ n'),
 ('omit_j_proof_coordinate','P01DependentFundamental','(index_cons (index_cons (index_refl η) heq.1) heq.2.1.symm)','(index_cons (index_cons (index_refl η) heq.1) (Conv.refl .i))')]
records=[]
for label,module,old,new in mutations:
 w=R/'mutations'/label;w.mkdir(parents=True,exist_ok=True)
 orig=(R/'sources'/(module+'.lean')).read_text();assert orig.count(old)==1
 s=w/(module+'.lean');s.write_text(orig.replace(old,new));cmd=[base['compiler_path'],'-j1','-o',str(w/(module+'.olean')),s.name]
 p=subprocess.run(cmd,cwd=w,env=env,capture_output=True,timeout=300);(w/'stdout').write_bytes(p.stdout);(w/'stderr').write_bytes(p.stderr)
 records.append({'mutation':label,'module':module,'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'exit_code':p.returncode,'expected_failure_observed':p.returncode!=0,'command':cmd,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()})
 print(label,p.returncode,p.stdout.decode()[:2000]);assert p.returncode!=0
(R/'MUTATION_CONTROLS.json').write_text(json.dumps(records,indent=2)+'\n')
