from pathlib import Path
import os,subprocess,json,hashlib
A=Path(__file__).resolve().parent;B=A.parents[2];L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
mutations=[
('shift_position_clock','PhysicalCostConservation','prefixLength blocks ni.1 + ni.2.val','prefixLength blocks (ni.1 + 1) + ni.2.val'),
('drop_first_record_in_exact_cost','RecursivePhysicalBudget',"∑' n, (plannedBadCount (good θ) (recursiveExecuted P good menu (x (n+1))) : ℝ≥0∞)","∑' n, (plannedBadCount (good θ) (recursiveExecuted P good menu (x (n+2))) : ℝ≥0∞)"),
('invert_good_charge','RecursivePhysicalBudget','if a ∈ G then 0 else 1','if a ∈ G then 1 else 0'),
('remove_rank_budget_factor','RecursivePhysicalBudget','((phaseRank P good menu p : ℝ) + 1) *','((phaseRank P good menu p : ℝ)) *'),
('decoder_next_action','dependencies.MeasurablePhysicalFlattening','(prefixActions blocks (t+1)).getD t d','(prefixActions blocks (t+1)).getD (t+1) d')]
records=[]
for name,mod,old,new in mutations:
 rel=Path(mod.replace('.','/')+'.lean');s=(A/'snapshot'/rel).read_text();assert old in s
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);p=d/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.replace(old,new,1))
 r=subprocess.run([str(L),'-j1','--root='+str(d),str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=d/'compile.log';log.write_text(r.stdout)
 errors=[l for l in r.stdout.splitlines() if 'error:' in l]
 assert r.returncode!=0 and errors,(name,r.stdout)
 records.append({'name':name,'module':mod,'source_sha256':sha(p),'exit':r.returncode,'errors':errors[:5],'log_sha256':sha(log),'status':'REJECTED'})
 print(name,r.returncode,flush=True)
(A/'MUTATION_RESULT.json').write_text(json.dumps({'status':'PASS','mutations':records},indent=2)+'\n')
