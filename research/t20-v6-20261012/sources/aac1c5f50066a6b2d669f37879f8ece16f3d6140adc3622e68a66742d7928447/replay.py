#!/usr/bin/env python3
import os, pathlib, subprocess, json, hashlib, datetime, re, argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(); parser.add_argument('--work-dir', type=pathlib.Path)
args=parser.parse_args()
AUDIT=(args.work_dir or pathlib.Path(__file__).resolve().parent).resolve()
for name in ['snapshot','build','logs']: (AUDIT/name).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
mods=['RepairObstruction','StatisticalRepair','CountableIdentification','RepairTestingBridge','RestorationCountability','BinaryConstructiveRepair','FiniteQueryLocality','FiniteQueryMeasure','CorrelatedOracleMeasure','EventualCausalRestoration']
lean=ROOT/'toolchain/lean-4.19.0-linux/bin/lean'; mathlib=ROOT/'toolchain/mathlib4'
libs=[mathlib/'.lake/build/lib/lean']+sorted(mathlib.glob('.lake/packages/*/.lake/build/lib/lean'))
checks={'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),'lean_sha256':sha(lean),'dependencies':[],'custom_shadows':[]}
assert checks['lean_sha256']=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
acq=json.loads((ROOT/'toolchain/ACQUISITION.json').read_text())
for p in acq['packages']:
 d=mathlib if p['name']=='mathlib' else mathlib/'.lake/packages'/p['name']
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
 dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip()
 assert rev==p['revision'] and not dirty,(p['name'],rev,dirty)
 checks['dependencies'].append({'name':p['name'],'revision':rev,'tracked_clean':not dirty})
for lib in libs+[lean.parents[1]/'lib/lean']:
 for m in mods:
  if (lib/(m+'.olean')).exists(): checks['custom_shadows'].append(str(lib/(m+'.olean')))
assert not checks['custom_shadows']
rows=[]
for m in mods:
 src=ROOT/('source-bridges/lean' if m=='RepairObstruction' else 'root-research/lean')/(m+'.lean')
 dest=AUDIT/'snapshot'/(m+'.lean')
 assert not (AUDIT/'build'/(m+'.olean')).exists(),m
 dest.write_bytes(src.read_bytes())
 assert not re.search(r'\b(sorry|axiom|admit)\b',re.sub(r'/\*[\s\S]*?\*/|--[^\n]*','',dest.read_text()))
 rows.append({'module':m,'origin':str(src.relative_to(ROOT)),'source_sha256':sha(src)})
(AUDIT/'SOURCE_MANIFEST.json').write_text(json.dumps(rows,indent=2)+'\n')
(AUDIT/'TOOLCHAIN_CHECK.json').write_text(json.dumps(checks,indent=2)+'\n')
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[AUDIT/'build']+libs)))
env.pop('LEAN_SRC_PATH',None)
(AUDIT/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'modules':[]}
for row in rows:
 m=row['module']; out=AUDIT/'build'/(m+'.olean'); log=AUDIT/'logs'/(m+'.log')
 cmd=[str(lean),'--root='+str(AUDIT/'snapshot'),'-o',str(out),str(AUDIT/'snapshot'/(m+'.lean'))]
 p=subprocess.run(cmd,cwd=mathlib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log.write_text(p.stdout)
 r={**row,'command':cmd,'exit':p.returncode,'log_sha256':sha(log),'olean_sha256':sha(out) if out.exists() else None}
 receipt['modules'].append(r)
 (AUDIT/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(m,p.returncode,flush=True)
 assert p.returncode==0 and 'sorryAx' not in p.stdout and 'error:' not in p.stdout,p.stdout
for row in rows:
 assert sha(ROOT/row['origin'])==row['source_sha256']
receipt['status']='PASS'; receipt['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(AUDIT/'REPLAY_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
