#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,hashlib,os,datetime,sys
R=Path(__file__).resolve().parents[1];A=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'portable-continuation/tooling'));from portable_core import verify_pins,sha,imports,check_source,public_targets,write_json
S=R/'crosswalk/evidence/micro-equivalence-qualification-20260930T233321Z';assert sha(S/'RESULT.json')=='2ffa1ea0c1100de528a1fb49fa64c5371a02283ce86d68d32d868ea8ef4aad65';auth=json.loads((S/'RESULT.json').read_text());assert auth['status']=='PASS';modules=[x['module'] for x in auth['modules']];pins=json.loads((R/'toolchain/ACQUISITION.json').read_text());lean,libs,version,checks=verify_pins(R/'toolchain/lean-4.19.0-linux/bin',R/'toolchain/mathlib4',pins,modules)
prior=[R/'portable-continuation/cold-deltas-v3',R/'portable-continuation/cold-replay-v2'];catalog={};builds=[]
for p in prior:
 d=json.loads((p/'REPLAY_RESULT.json').read_text());assert d['status']=='PASS'
 for s in d['suites']:
  builds.append(p/s['id']/'build')
  for row in s['modules']:
   if row['module'] not in catalog:catalog[row['module']]=(row,p/s['id']/'build'/Path(row['module'].replace('.','/')+'.olean'),p/'REPLAY_RESULT.json')
previous=R/'seeded-necessity-audit';previous_receipt=previous/'REPLAY_RESULT.json';pr=json.loads(previous_receipt.read_text());assert pr['status']=='PASS';builds.insert(0,previous/'build')
for row in pr['modules']:
 if row['fresh']:
  catalog[row['module']]=(row,previous/'build'/(row['module']+'.olean'),previous_receipt)
rows=[];targets=[]
for row in auth['modules']:
 m=row['module'];src=S/'source'/(m+'.lean');assert sha(src)==row['source_sha256'];dest=A/'snapshot'/(m+'.lean');dest.write_bytes(src.read_bytes());check_source(dest.read_text());r={'module':m,'source_sha256':sha(dest),'imports':imports(dest.read_text()),'targets':public_targets(dest.read_text()),'fresh':True}
 orig=R/'crosswalk/lean-micro'/(m+'.lean')
 if not orig.exists():orig=R/'crosswalk/lean-necessity'/(m+'.lean')
 if not orig.exists():orig=R/'crosswalk/lean'/(m+'.lean')
 if not orig.exists():orig=R/'root-research/lean'/(m+'.lean')
 if orig.exists():assert sha(orig)==sha(dest);r['current_owner']=str(orig.relative_to(R))
 if m in catalog and catalog[m][0]['source_sha256']==sha(dest):
  old,obj,rec=catalog[m];assert sha(obj)==old['olean_sha256'];r.update({'fresh':False,'retained_object':str(obj.relative_to(R)),'retained_olean_sha256':sha(obj),'retained_receipt':str(rec.relative_to(R)),'retained_receipt_sha256':sha(rec)})
 else:assert not(A/'build'/(m+'.olean')).exists()
 rows.append(r);targets+=r['targets']
write_json(A/'SOURCE_MANIFEST.json',{'modules':rows});write_json(A/'TARGETS.json',targets);env=dict(os.environ,LEAN_PATH=':'.join(map(str,[A/'build']+builds+libs)));env.pop('LEAN_SRC_PATH',None);(A/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n');receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_sha256':sha(lean),'lean_version':version,'pins':checks,'author_receipt_sha256':sha(S/'RESULT.json'),'fresh_modules':sum(r['fresh'] for r in rows),'retained_modules':sum(not r['fresh'] for r in rows),'modules':[]};write_json(A/'REPLAY_RESULT.json',receipt)
for row in rows:
 m=row['module']
 if not row['fresh']:receipt['modules'].append({**row,'status':'RETAINED_INDEPENDENT_FRESH_OBJECT_VERIFIED'});continue
 src=A/'snapshot'/(m+'.lean');obj=A/'build'/(m+'.olean');cmd=[str(lean),'-j1','--root='+str(A/'snapshot'),'-o',str(obj),str(src)];p=subprocess.run(cmd,cwd=R/'toolchain/mathlib4',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs'/(m+'.log');log.write_text(p.stdout);receipt['modules'].append({**row,'command':cmd,'exit':p.returncode,'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None});write_json(A/'REPLAY_RESULT.json',receipt);print(m,p.returncode,flush=True);assert p.returncode==0 and 'error:' not in p.stdout and 'sorryAx' not in p.stdout,p.stdout
(A/'controls/TargetReadback.lean').write_text('\n'.join('import '+m for m in modules)+'\nset_option pp.universes true\n'+''.join(f'#check @{t}\n#print axioms {t}\n' for t in targets));p=subprocess.run([str(lean),'-j1','--root='+str(A/'controls'),str(A/'controls/TargetReadback.lean')],cwd=R/'toolchain/mathlib4',env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(A/'logs/TargetReadback.log').write_text(p.stdout);assert p.returncode==0,p.stdout
from portable_core import parse_readback
axioms=parse_readback(p.stdout,targets);write_json(A/'AXIOM_READBACK.json',{'status':'PASS','target_count':len(targets),'targets':axioms,'log_sha256':sha(A/'logs/TargetReadback.log')});receipt['status']='PASS';receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt['readback_log_sha256']=sha(A/'logs/TargetReadback.log');write_json(A/'REPLAY_RESULT.json',receipt)
