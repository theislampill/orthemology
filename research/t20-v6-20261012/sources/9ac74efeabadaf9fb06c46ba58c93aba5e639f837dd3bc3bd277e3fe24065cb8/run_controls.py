from pathlib import Path
import json,subprocess,os,hashlib,datetime,re
R=Path(__file__).resolve().parent;W=R.parent;O=R/'fresh-output';e=json.loads((R/'environment.json').read_text());env=dict(os.environ,LEAN_PATH=e['LEAN_PATH']);records=[]
for name,expected in [('IndependentControls',None),('FalseOrderInsensitive',"tactic 'decide' proved that the proposition"),('FalseUnusedImageAccepted',"tactic 'decide' proved that the proposition"),('FalseMalformedTotal','tactic \'assumption\' failed'),('FalseTypeProjection','type mismatch')]:
 cmd=[e['lean'],'--trust=0','-s','65536']
 if expected is None:cmd+=['-o',str(O/(name+'.olean'))]
 cmd+=[str(R/(name+'.lean'))]
 p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=O/(name+'.log');log.write_text(p.stdout)
 if expected is None:
  assert p.returncode==0 and not any(x in p.stdout for x in ['sorryAx','error:','warning:']),(name,p.stdout)
  assert len(re.findall(r'^PASS independent control',p.stdout,re.M))==22
  assert re.findall(r'^(true|false)$',p.stdout,re.M)==['true','false']
 else:assert p.returncode!=0 and expected in p.stdout,(name,p.stdout)
 print(('PASS ' if expected is None else 'REJECTED ')+name,flush=True)
 records.append({'name':name,'expected_rejection':expected,'exit_code':p.returncode,'log':str(log.relative_to(W)),'source_sha256':hashlib.sha256((R/(name+'.lean')).read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
(R/'INDEPENDENT_CONTROLS.json').write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records},indent=2)+'\n')
# Reproduce the seven frozen endpoint negative controls in the independent fresh environment.
original=[]
for name in ['AcceptMissing','AcceptExtra','AcceptDistinctSwap','AcceptFalseConversion','AcceptMalformedClaim','DropUnusedImage','MakeInvalidSearchTotal']:
 src=W/'hase-actual-source-enumerability-20261010/diagnostics'/(name+'.lean')
 p=subprocess.run([e['lean'],'--trust=0','-s','65536',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=O/('Candidate_'+name+'.log');log.write_text(p.stdout)
 expected='unsolved goals' if name=='MakeInvalidSearchTotal' else "tactic 'decide' proved that the proposition"
 assert p.returncode!=0 and expected in p.stdout,(name,p.stdout)
 original.append({'name':name,'exit_code':p.returncode,'expected_rejection':expected,'source':str(src.relative_to(W)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'log':str(log.relative_to(W)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
 print('REJECTED candidate '+name,flush=True)
(R/'CANDIDATE_NEGATIVES_REPLAY.json').write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':original},indent=2)+'\n')
