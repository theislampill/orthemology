from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,shutil,datetime
D=Path(__file__).resolve().parent;P=D.parents[1]/'t20-consolidation-20261011/projection/package-v4';rows=[]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(q,p):return json.loads((q/p).read_text())
def put(q,p,x):(q/p).write_text(json.dumps(x))
def case(name,edit):
 with tempfile.TemporaryDirectory(prefix='t20-depth-negative-') as t:
  q=Path(t)/'package';shutil.copytree(P,q);edit(q)
  r=subprocess.run([sys.executable,'-B','validate_depth.py'],cwd=q,capture_output=True,text=True,timeout=30)
  rows.append({'case':name,'exit_code':r.returncode,'rejected':r.returncode!=0,'stdout':r.stdout,'stderr':r.stderr})
def stale(q):
 c=read(q,'depth/REVIEW_CURRENTNESS.json');r=c['reviews'][0];w=r['binding_witnesses'][0];v=read(q,w['path']);node=v
 for k in w['selector'][:-1]:node=node[k]
 node[w['selector'][-1]]='0'*64;put(q,w['path'],v)
 for b in r['current_binding_documents']:
  if b['path']==w['path']:b['public_sha256']=h(q/w['path'])
 put(q,'depth/REVIEW_CURRENTNESS.json',c)
case('stale structured review witness despite refreshed binding-document digest',stale)
def source(q):
 put(q,'depth/ADVERSARIAL_SOURCE.json',{'public_source':'depth/joint_correction/RESULT.md','public_sha256':h(q/'depth/joint_correction/RESULT.md'),'sha256':'0'*64,'public_projection':'EXACT'})
case('false exact original/public identity',source)
def closure(q):
 c=read(q,'DEPTH_REPLAY_VERIFICATION.json');c['runs'][0]['suite_sources'][0]['sha256']='0'*64;put(q,'DEPTH_REPLAY_VERIFICATION.json',c)
case('stale fresh replay closure',closure)
def predecessor(q):
 c=read(q,'depth/V3_PRESERVATION.json');c['files'][0]['v3_sha256']='0'*64;put(q,'depth/V3_PRESERVATION.json',c)
case('false predecessor preservation digest',predecessor)
def method(q):
 c=read(q,'coverage/SELECTED_SOURCE_READS.json')
 for r in c:
  if r['id']=='S25':r['public_sha256']='0'*64
 put(q,'coverage/SELECTED_SOURCE_READS.json',c)
case('stale methodology route digest',method)
ok=all(r['rejected'] for r in rows);res={'status':'PASS' if ok else 'FAIL','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'cases':rows};(D/'ADVERSARIAL_DEPTH.json').write_text(json.dumps(res,indent=2)+'\n');print(res['status'],len(rows));sys.exit(not ok)
