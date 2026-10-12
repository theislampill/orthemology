from pathlib import Path
import os,subprocess,json,hashlib
A=Path(__file__).resolve().parent;B=A.parents[2];L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
mutations=[
('omit_current_action_cost','CausalActionTree','| .node a k => cost a + ∑ y, P a y * treeValue P cost F (k y)','| .node a k => 0 + ∑ y, P a y * treeValue P cost F (k y)'),
('restart_instead_of_residual','CausalActionTree','| .node a k => (a,k)','| .node a k => s'),
('omit_action_compatibility','CanonicalHistoryPMF','if n = h.length ∧ ActionCompatible (fun (_ : Unit) h => π h) () h then','if n = h.length then'),
('drop_history_head_charge','CanonicalHistoryBudget','(h.map (fun ay => c ay.1)).sum','(h.tail.map (fun ay => c ay.1)).sum'),
('allow_zero_likelihood_normalization','NormalizedResetPotential','(hm : 0 < dHistoryMass (continuingKernel K stay p) θ h)','(hm : 0 ≤ dHistoryMass (continuingKernel K stay p) θ h)'),
('ignore_observed_support_change','RecursiveHistorySafety','| (a,y)::h => supportUpdate P (historySupport B₀ h) a y','| (a,y)::h => historySupport B₀ h')]
records=[]
for name,mod,old,new in mutations:
 s=(A/'snapshot'/(mod+'.lean')).read_text();assert old in s
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);p=d/(mod+'.lean');p.write_text(s.replace(old,new,1))
 r=subprocess.run([str(L),'-j1','--root='+str(d),str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=d/'compile.log';log.write_text(r.stdout)
 errors=[l for l in r.stdout.splitlines() if 'error:' in l];assert r.returncode!=0 and errors,(name,r.stdout)
 records.append({'name':name,'module':mod,'source_sha256':sha(p),'exit':r.returncode,'errors':errors[:5],'log_sha256':sha(log),'status':'REJECTED'});print(name,r.returncode,flush=True)
(A/'MUTATION_RESULT.json').write_text(json.dumps({'status':'PASS','mutations':records},indent=2)+'\n')
