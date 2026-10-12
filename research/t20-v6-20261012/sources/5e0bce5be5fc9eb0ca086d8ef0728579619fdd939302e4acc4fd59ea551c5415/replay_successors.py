from pathlib import Path
import hashlib,json,os,subprocess,re,datetime
A=Path(__file__).resolve().parent;B=A.parents[2];auth=B/'tranche3/control/evidence/physical-budget-qualification-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(auth/'SOURCE_MANIFEST.json')=='6047b716ef273acdbe961e10032b738aab08308a496d96b0a8e5647e77584d54'
rows={x['module']:x for x in json.loads((auth/'SOURCE_MANIFEST.json').read_text())}
baseline=json.loads((A/'REPLAY_RESULT.json').read_text());assert baseline['status']=='PASS'
for r in baseline['modules']:
 assert rows[r['module']]['sha256']==r['source_sha256']
 assert sha(A/'snapshot'/Path(r['module'].replace('.','/')+'.lean'))==r['source_sha256']
 assert sha(A/'build'/Path(r['module'].replace('.','/')+'.olean'))==r['olean_sha256']
r={'status':'RUNNING','baseline_receipt_sha256':sha(A/'REPLAY_RESULT.json'),'author_manifest_sha256':sha(auth/'SOURCE_MANIFEST.json'),'modules':[]}
L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';assert sha(L)==baseline['lean_sha256']
env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip());env.pop('LEAN_SRC_PATH',None)
for mod in ['PhysicalCostConservation','RecursivePhysicalBudget']:
 orig=B/rows[mod]['source'];src=A/'snapshot'/(mod+'.lean');sealed=auth/'source'/(mod+'.lean')
 assert sha(orig)==sha(sealed)==rows[mod]['sha256']
 src.write_bytes(sealed.read_bytes());obj=A/'build'/(mod+'.olean');assert not obj.exists()
 code=re.sub(r'/-[\s\S]*?-/|--[^\n]*','',src.read_text());assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b|debug\.skipKernelTC',code)
 imports=re.findall(r'^import\s+(\S+)',code,re.M)
 assert all((A/'build'/(i.replace('.','/')+'.olean')).exists() for i in imports)
 cmd=[str(L),'-j1','--root='+str(A/'snapshot'),'-o',str(obj),str(src)]
 p=subprocess.run(cmd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs'/(mod+'.log');log.write_text(p.stdout)
 r['modules'].append({'module':mod,'origin':str(orig.relative_to(B)),'source_sha256':sha(src),'imports':imports,'command':cmd,'exit':p.returncode,'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None})
 (A/'SUCCESSOR_REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(mod,p.returncode,flush=True)
 assert p.returncode==0 and not re.search(r'\berror:|sorryAx|declaration uses .sorry.',p.stdout),p.stdout
 assert sha(orig)==sha(sealed)==sha(src)
r['status']='PASS';r['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(A/'SUCCESSOR_REPLAY_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
