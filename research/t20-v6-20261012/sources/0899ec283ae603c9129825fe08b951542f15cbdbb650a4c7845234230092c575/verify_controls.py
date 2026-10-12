#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,hashlib,os,datetime,sys,re
A=Path(__file__).resolve().parent;R=A.parent;sys.path.insert(0,str(R/'portable-continuation/tooling'));from portable_core import sha,write_json,parse_readback,public_targets,check_diagnostics
lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
def run(src,log,obj=None):
 cmd=[str(lean),'-j1','--root='+str(src.parent)]+(['-o',str(obj)] if obj else [])+[str(src)];p=subprocess.run(cmd,cwd=R/'toolchain/mathlib4',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log.write_text(p.stdout);return p
src=A/'controls/MicroControls.lean';p=run(src,A/'logs/MicroControls.log',A/'build/MicroControls.olean');assert p.returncode==0,p.stdout;check_diagnostics(p.stdout);targets=public_targets(src.read_text());(A/'controls/ControlReadback.lean').write_text('import MicroControls\n'+''.join(f'#check @{x}\n#print axioms {x}\n' for x in targets));p=run(A/'controls/ControlReadback.lean',A/'logs/ControlReadback.log');assert p.returncode==0,p.stdout;axioms=parse_readback(p.stdout,targets)
mutations=[
 ('PrematureReplan','MicroQueue','if rest = [] then plan (choose (z :: h)) else rest','plan (choose (z :: h))'),
 ('ReusedFirstFeedback','MicroReplay','X a (actionCount a prev)','X a 0'),
 ('DropLastAction','MicroReplay','feed X h (plan (choose h))','feed X h ((plan (choose h)).dropLast)'),
 ('CollapseMultiplicity','HistoryLikelihood','actionCount a h + as.count a','actionCount a h + if a ∈ as then 1 else 0'),
 ('ConfuseBlockAndActionClock','MicroPhysical','⟨prefixLength blocks N,fun t ht => ?_⟩','⟨N,fun t ht => ?_⟩'),
 ('IgnoreAcquiredLikelihood','MicroLikelihood','greedyMax (fun σ => historyScore (P σ) h)','greedyMax (fun σ => historyScore (P σ) [])')]

results=[]
for name,module,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);s=(A/'snapshot'/(module+'.lean')).read_text();assert old in s;src=d/(module+'.lean');src.write_text(s.replace(old,new));log=A/'logs'/(name+'.log');p=run(src,log);assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout,(name,p.stdout);results.append({'name':name,'module':module,'old':old,'new':new,'expected':'REJECT','exit':p.returncode,'source_sha256':sha(src),'log_sha256':sha(log)});print(name,'REJECTED',flush=True)
write_json(A/'CONTROL_RESULT.json',{'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'positive_targets':targets,'positive_target_count':len(targets),'control_axioms':axioms,'control_source_sha256':sha(A/'controls/MicroControls.lean'),'control_log_sha256':sha(A/'logs/MicroControls.log'),'control_readback_sha256':sha(A/'logs/ControlReadback.log'),'expected_rejected_mutations':results})
