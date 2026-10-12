from pathlib import Path
import os,subprocess,json,hashlib
A=Path(__file__).resolve().parent;B=A.parents[2];L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
mutations=[
('allow_zero_mass_branch','DeterministicContinuation','(hy : 0 < P (π r []) y)','(hy : 0 ≤ P (π r []) y)'),
('reverse_acquired_history_order','DeterministicContinuation','π r (future ++ h)','π r (h ++ future)'),
('erase_finite_query_event_guard','RelativeTailTransfer','(hE : E ⊆ finiteQueryTrace)','(hE : True)'),
('retain_unsafe_source_rows','SafeSetTailTransfer','let F := fun a => if a ∈ D then P a else Q a','let F := fun a => if a ∈ D then P a else P a'),
('erase_all_time_safe_event_guard','SafeSetTailTransfer','(hstay : C ⊆ alwaysIn D)','(hstay : True)'),
('erase_pointwise_safety','WinningContinuation','(∀ h, ActionCompatible π r h → (historySupport P B h).Nonempty →\n    π r h ∈ menu (historySupport P B h))','True')]

records=[]
for name,mod,old,new in mutations:
 s=(A/'snapshot'/(mod+'.lean')).read_text();assert old in s
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);p=d/(mod+'.lean');p.write_text(s.replace(old,new,1))
 r=subprocess.run([str(L),'-j1','--root='+str(d),str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=d/'compile.log';log.write_text(r.stdout)
 errors=[l for l in r.stdout.splitlines() if 'error:' in l];assert r.returncode!=0 and errors,(name,r.stdout)
 records.append({'name':name,'module':mod,'source_sha256':sha(p),'exit':r.returncode,'errors':errors[:5],'log_sha256':sha(log),'status':'REJECTED'});print(name,r.returncode,flush=True)
(A/'MUTATION_RESULT.json').write_text(json.dumps({'status':'PASS','mutations':records},indent=2)+'\n')
