from pathlib import Path
import os,subprocess,json,hashlib
A=Path(__file__).resolve().parent;B=A.parents[2];L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
mutations=[
('use_post_action_support','ObservedHistoryLicensing','historyAction d H n ∈ menu (historySupport P B (H n))','historyAction d H n ∈ menu (historySupport P B (H (n+1)))'),
('erase_action_consistency_for_positive_cylinder','ObservedHistoryLicensing','(hc : ActionCompatible π r h)','(hc : True)'),
('erase_live_model_for_positive_cylinder','ObservedHistoryLicensing','(ht : θ ∈ historySupport P B h)','(ht : θ ∈ B)'),
('discard_history_safety_during_seed_selection','AELicensedEquivalence','(hga.and hsa)','(hga.and hga)'),
('read_action_before_it_is_recorded','ObservedHistoryLicensing','(H (n+1),H n)','(H n,H n)')]

records=[]
for name,mod,old,new in mutations:
 s=(A/'snapshot'/(mod+'.lean')).read_text();assert old in s
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);p=d/(mod+'.lean');p.write_text(s.replace(old,new,1))
 r=subprocess.run([str(L),'-j1','--root='+str(d),str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=d/'compile.log';log.write_text(r.stdout)
 errors=[l for l in r.stdout.splitlines() if 'error:' in l];assert r.returncode!=0 and errors,(name,r.stdout)
 records.append({'name':name,'module':mod,'source_sha256':sha(p),'exit':r.returncode,'errors':errors[:5],'log_sha256':sha(log),'status':'REJECTED'});print(name,r.returncode,flush=True)
(A/'MUTATION_RESULT.json').write_text(json.dumps({'status':'PASS','mutations':records},indent=2)+'\n')
