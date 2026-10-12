from pathlib import Path
import json,hashlib,subprocess,os,re,datetime
A=Path(__file__).resolve().parent;B=A.parents[2];OLD=A.parent/'canonical-sufficiency';auth=B/'tranche3/control/evidence/canonical-sufficiency-qualification-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(auth/'SOURCE_MANIFEST.json')=='6774f8d2437528d3a02965ab0ea7a0d805cdc7c661ddb117834e88ef6ad835f2'
prior=json.loads((OLD/'REPLAY_RESULT.json').read_text());assert prior['status']=='PASS';oldrows={r['module']:r for r in prior['modules']};rows=json.loads((auth/'SOURCE_MANIFEST.json').read_text());assert len(rows)==len(oldrows)==72
for n in ['snapshot','build','logs']:(A/n).mkdir(exist_ok=True)
r={'status':'RUNNING','retained_reviewer_receipt_sha256':sha(OLD/'REPLAY_RESULT.json'),'author_manifest_sha256':sha(auth/'SOURCE_MANIFEST.json'),'module_count':72,'fresh_module_count':9,'retained_module_count':63,'modules':[],'difference_scope':'Exactly nine insertions of set_option linter.unusedSectionVars false; no proof or theorem edits.'}
for row in rows:
 m=row['module'];rel=Path(m.replace('.','/'));src=auth/'source'/rel.with_suffix('.lean');dst=A/'snapshot'/rel.with_suffix('.lean');dst.parent.mkdir(parents=True,exist_ok=True)
 assert sha(src)==sha(B/row['source'])==row['sha256'];dst.write_bytes(src.read_bytes());before=OLD/'snapshot'/rel.with_suffix('.lean');changed=sha(before)!=sha(dst)
 if changed:assert dst.read_text().replace('set_option linter.unusedSectionVars false\n','')==before.read_text()
 oldobj=OLD/'build'/rel.with_suffix('.olean');assert sha(oldobj)==oldrows[m]['olean_sha256']
 row['changed']=changed
 if not changed:
  obj=A/'build'/rel.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True);assert not obj.exists();obj.write_bytes(oldobj.read_bytes())
assert sum(x['changed'] for x in rows)==9
libs=(OLD/'LEAN_PATH.txt').read_text().strip().split(':')[1:]
env=dict(os.environ,LEAN_PATH=':'.join([str(A/'build')]+libs));env.pop('LEAN_SRC_PATH',None);(A/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';assert sha(L)==prior['lean_sha256']
for row in rows:
 m=row['module'];rel=Path(m.replace('.','/'));src=A/'snapshot'/rel.with_suffix('.lean');obj=A/'build'/rel.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
 if row['changed']:
  assert not obj.exists();p=subprocess.run([str(L),'-j1','--root='+str(A/'snapshot'),'-o',str(obj),str(src)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs'/(m+'.log');log.write_text(p.stdout)
  assert p.returncode==0 and not re.search(r'\berror:|\bwarning:|sorryAx',p.stdout),p.stdout
  d={'exit':p.returncode,'log_sha256':sha(log),'status':'FRESH_CURRENT_SOURCE'};print(m,p.returncode,flush=True)
 else:d={'status':'RETAINED_FROM_FRESH_REVIEWER_REPLAY','retained_source_sha256':oldrows[m]['source_sha256'],'retained_olean_sha256':oldrows[m]['olean_sha256']}
 r['modules'].append({'module':m,'origin':row['source'],'source_sha256':sha(src),'olean_sha256':sha(obj),**d});(A/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
for row in rows:assert sha(B/row['source'])==row['sha256']
r['status']='PASS';r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(A/'REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
(A/'AUTHOR_MANIFEST.json').write_bytes((auth/'SOURCE_MANIFEST.json').read_bytes());(A/'PRIOR_REVIEWER_REPLAY.json').write_bytes((OLD/'REPLAY_RESULT.json').read_bytes());(A/'OFFICIAL_IMPORTS.json').write_bytes((OLD/'OFFICIAL_IMPORTS.json').read_bytes())
