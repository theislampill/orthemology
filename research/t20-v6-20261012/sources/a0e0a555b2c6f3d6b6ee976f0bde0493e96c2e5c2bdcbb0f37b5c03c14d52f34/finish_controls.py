from pathlib import Path
import os,json,subprocess,hashlib,re
from datetime import datetime,timezone
here=Path(__file__).resolve().parent;root=here.parents[1];lean=root/'toolchain/lean-4.19.0-linux/bin/lean';mathlib=root/'toolchain/mathlib4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((here/'REPLAY_RESULT.json').read_text());r['development_attempts']=[r['modules'].pop()]
assert r['modules'][0]['exit']==0
assert sha(here/'build/PhysicalFlattening.olean')==r['modules'][0]['olean_sha256']
assert sha(root/'root-research/lean/PhysicalFlattening.lean')==r['original_sha256']
env=dict(os.environ,LEAN_PATH=(here/'LEAN_PATH.txt').read_text().strip());env.pop('LEAN_SRC_PATH',None)
for m in ['BoundaryControls','TargetReadback']:
 p=here/'snapshot'/(m+'.lean');obj=here/'build'/(m+'.olean');log=here/'logs'/(m+'.log')
 cmd=[str(lean),'-j1','--root='+str(here/'snapshot'),'-o',str(obj),str(p)]
 x=subprocess.run(cmd,cwd=mathlib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log.write_text(x.stdout)
 ax=set(a.strip() for z in re.findall(r'depends on axioms: \[([^\]]*)\]',x.stdout) for a in z.split(',') if a.strip())
 r['modules'].append({'module':m,'source_sha256':sha(p),'command':cmd,'exit':x.returncode,'log_sha256':sha(log),'axioms':sorted(ax),'olean_sha256':sha(obj) if obj.exists() else None})
 r['status']='PASS' if x.returncode==0 else 'FAIL';(here/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(m,x.returncode,x.stdout,flush=True)
 assert x.returncode==0 and 'sorryAx' not in x.stdout and ax<={'propext','Classical.choice','Quot.sound'}
assert sha(root/'root-research/lean/PhysicalFlattening.lean')==r['original_sha256']
r['finished_utc']=datetime.now(timezone.utc).isoformat();(here/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
