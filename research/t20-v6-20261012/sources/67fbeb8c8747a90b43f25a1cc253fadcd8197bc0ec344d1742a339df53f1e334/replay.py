#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,hashlib,os,datetime,re,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--work-dir',type=Path);args=parser.parse_args();A=(args.work_dir or Path(__file__).resolve().parent).resolve()
for n in ['snapshot','build','logs']:(A/n).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
seal=R/'crosswalk/evidence/generated-qualification-20260930T214115Z';auth=json.loads((seal/'RESULT.json').read_text());assert auth['status']=='PASS'
modules=[x['module'] for x in auth['modules']];retained=set(modules[:8]);M=R/'toolchain/mathlib4';L=R/'toolchain/lean-4.19.0-linux/bin/lean'
assert sha(L)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
pins=json.loads((R/'toolchain/ACQUISITION.json').read_text());checks=[]
for row in pins['packages']:
 d=M if row['name']=='mathlib' else M/'.lake/packages'/row['name']
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip();dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip()
 assert rev==row['revision'] and not dirty
 checks.append({'name':row['name'],'revision':rev,'tracked_clean':True})
libs=[M/'.lake/build/lib/lean']+sorted(M.glob('.lake/packages/*/.lake/build/lib/lean'))
for lib in libs+[L.parents[1]/'lib/lean']:
 for mod in modules:assert not (lib/(mod.replace('.','/')+'.olean')).exists()
base=R/'integration-proof-audit';baserec=json.loads((base/'REPLAY_RESULT.json').read_text());baserows={r['module']:r for r in baserec['modules']}
rows=[]
for row in auth['modules']:
 mod=row['module'];rel=Path(mod.replace('.','/')+'.lean');sealed=seal/'source'/rel;orig=R/'crosswalk'/('lean' if mod in retained else 'lean-quant')/rel
 assert sha(sealed)==row['source_sha256']==sha(orig)
 dest=A/'snapshot'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(sealed.read_bytes())
 code=re.sub(r'/-[\s\S]*?-/|--[^\n]*','',dest.read_text());assert not re.search(r'\b(sorry|admit|axiom)\b',code)
 imports=re.findall(r'^import\s+(\S+)',code,re.M)
 assert all(x.startswith(('Mathlib','Batteries','Lean','Std')) or x in modules for x in imports),(mod,imports)
 r={'module':mod,'origin':str(orig.relative_to(R)),'sealed_source_sha256':sha(sealed),'source_sha256':sha(dest),'imports':imports,'fresh_this_pass':mod not in retained}
 if mod in retained:
  assert baserows[mod]['source_sha256']==row['source_sha256']
  obj=base/'build'/Path(mod+'.olean');assert sha(obj)==baserows[mod]['olean_sha256']
  r['retained_olean_sha256']=sha(obj)
 else:assert not(A/'build'/Path(mod.replace('.','/')+'.olean')).exists()
 rows.append(r)
(A/'SOURCE_MANIFEST.json').write_text(json.dumps(rows,indent=2)+'\n')
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[A/'build',base/'build']+libs)));env.pop('LEAN_SRC_PATH',None)
(A/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_sha256':sha(L),'lean_version':subprocess.check_output([str(L),'--version'],text=True).strip(),'pins':checks,'author_receipt_sha256':sha(seal/'RESULT.json'),'retained_baseline_receipt_sha256':sha(base/'REPLAY_RESULT.json'),'fresh_module_count':len(modules)-len(retained),'retained_module_count':len(retained),'modules':[]}
for row in rows:
 mod=row['module']
 if mod in retained:receipt['modules'].append({**row,'status':'RETAINED_VERIFIED_FRESH_PRIOR_REPLAY'});continue
 rel=Path(mod.replace('.','/'));obj=A/'build'/rel.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
 src=A/'snapshot'/rel.with_suffix('.lean');log=A/'logs'/(mod+'.log');cmd=[str(L),'--root='+str(A/'snapshot'),'-o',str(obj),str(src)]
 p=subprocess.run(cmd,env=env,cwd=M,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log.write_text(p.stdout)
 receipt['modules'].append({**row,'command':cmd,'exit':p.returncode,'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None})
 (A/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(mod,p.returncode,flush=True)
 assert p.returncode==0 and 'error:' not in p.stdout and 'sorryAx' not in p.stdout,p.stdout
for row in rows:assert sha(R/row['origin'])==row['source_sha256']
receipt['status']='PASS';receipt['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(A/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
