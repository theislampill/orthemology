#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,hashlib,os,datetime,re,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--work-dir',type=Path);args=parser.parse_args();A=(args.work_dir or Path(__file__).resolve().parent).resolve()
for n in ['snapshot','build','logs']:(A/n).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();M=R/'toolchain/mathlib4';L=R/'toolchain/lean-4.19.0-linux/bin/lean'
assert sha(L)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
pins=json.loads((R/'toolchain/ACQUISITION.json').read_text());checks=[]
for row in pins['packages']:
 d=M if row['name']=='mathlib' else M/'.lake/packages'/row['name'];rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip();dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip();assert rev==row['revision'] and not dirty;checks.append({'name':row['name'],'revision':rev,'tracked_clean':True})
libs=[M/'.lake/build/lib/lean']+sorted(M.glob('.lake/packages/*/.lake/build/lib/lean'))
for lib in libs+[L.parents[1]/'lib/lean']:assert not(lib/'RecurrentSupport.olean').exists()
orig=R/'necessity-bridge-review/lean/RecurrentSupport.lean';assert sha(orig)=='ee53d2fceb24d3552b0cf0798fb8c10b22717f66e80546db2e26d48c36d19899';auth=R/'necessity-bridge-review/recurrence-formal';assert sha(auth/'MANIFEST.json')=='6ee0ff22552034b7621de594c2282018f84ff94e7925b960892bf0c9198765a8'
for row in json.loads((auth/'MANIFEST.json').read_text())['files']:assert sha(auth/row['path'])==row['sha256']
src=A/'snapshot/RecurrentSupport.lean';src.write_bytes(orig.read_bytes());assert not(A/'build/RecurrentSupport.olean').exists();env=dict(os.environ,LEAN_PATH=':'.join(map(str,[A/'build']+libs)));env.pop('LEAN_SRC_PATH',None);(A/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':sha(src),'author_manifest_sha256':sha(auth/'MANIFEST.json'),'lean_sha256':sha(L),'lean_version':subprocess.check_output([str(L),'--version'],text=True).strip(),'pins':checks,'modules':[]}
cmd=[str(L),'--root='+str(A/'snapshot'),'-o',str(A/'build/RecurrentSupport.olean'),str(src)];p=subprocess.run(cmd,env=env,cwd=M,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs/RecurrentSupport.log';log.write_text(p.stdout);receipt['modules'].append({'module':'RecurrentSupport','source_sha256':sha(src),'exit':p.returncode,'command':cmd,'log_sha256':sha(log),'olean_sha256':sha(A/'build/RecurrentSupport.olean') if(A/'build/RecurrentSupport.olean').exists() else None});(A/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');assert p.returncode==0 and 'sorryAx' not in p.stdout and 'error:' not in p.stdout,p.stdout;assert sha(orig)==sha(src);receipt['status']='PASS';receipt['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(A/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('RecurrentSupport PASS',flush=True)
