from pathlib import Path
import os,hashlib,json,subprocess,re
from datetime import datetime,timezone
here=Path(__file__).resolve().parent; root=here.parents[1]
lean=root/'toolchain/lean-4.19.0-linux/bin/lean'; mathlib=root/'toolchain/mathlib4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='3111f8189b6bc36447c9da68da38775f828ce660ed19f5725cd7f240ee451d63'
origin=root/'root-research/lean/PhysicalFlattening.lean';snapshot=here/'snapshot/PhysicalFlattening.lean'
assert sha(origin)==sha(snapshot)==expected
assert sha(lean)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
libs=[mathlib/'.lake/build/lib/lean']+sorted(mathlib.glob('.lake/packages/*/.lake/build/lib/lean'))
checks=[]
for p in json.loads((root/'toolchain/ACQUISITION.json').read_text())['packages']:
 d=mathlib if p['name']=='mathlib' else mathlib/'.lake/packages'/p['name']
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
 dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip()
 assert rev==p['revision'] and not dirty
 checks.append({'name':p['name'],'revision':rev,'tracked_clean':not dirty})
for lib in libs:
 assert not (lib/'PhysicalFlattening.olean').exists()
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[here/'build']+libs)))
env.pop('LEAN_SRC_PATH',None)
(here/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
r={'status':'RUNNING','started_utc':datetime.now(timezone.utc).isoformat(),'original_sha256':expected,'lean_sha256':sha(lean),'dependencies':checks,'modules':[]}
for m in ['PhysicalFlattening','BoundaryControls']:
 p=here/'snapshot'/(m+'.lean');obj=here/'build'/(m+'.olean')
 assert not obj.exists(),m
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',re.sub(r'/\*[\s\S]*?\*/|--[^\n]*','',p.read_text()))
 cmd=[str(lean),'-j1','--root='+str(here/'snapshot'),'-o',str(obj),str(p)]
 x=subprocess.run(cmd,cwd=mathlib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=here/'logs'/(m+'.log');log.write_text(x.stdout)
 ax=set(a.strip() for z in re.findall(r'depends on axioms: \[([^\]]*)\]',x.stdout) for a in z.split(',') if a.strip())
 row={'module':m,'source_sha256':sha(p),'command':cmd,'exit':x.returncode,'log_sha256':sha(log),'axioms':sorted(ax),'olean_sha256':sha(obj) if obj.exists() else None};r['modules'].append(row)
 (here/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(m,x.returncode,x.stdout,flush=True)
 if x.returncode or 'sorryAx' in x.stdout or not ax<={'propext','Classical.choice','Quot.sound'}:raise SystemExit('FAILED '+m)
assert sha(origin)==expected
r['status']='PASS';r['finished_utc']=datetime.now(timezone.utc).isoformat();(here/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
