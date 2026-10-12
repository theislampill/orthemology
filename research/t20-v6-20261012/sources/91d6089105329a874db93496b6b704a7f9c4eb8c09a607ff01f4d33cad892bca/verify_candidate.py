#!/usr/bin/env python3
import hashlib,json,datetime,sys
from pathlib import Path
D=Path(__file__).resolve().parent;W=D.parents[1];V=W/'t20-consolidation-20261011/projection/package-v3';P=V.with_name('package-v4')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate JSON key '+k)
   d[k]=v
  return d
 return json.loads(p.read_text(),object_pairs_hook=pairs)
def tree(p):return {f.relative_to(p).as_posix():{'sha256':h(f),'bytes':f.stat().st_size} for f in p.rglob('*') if f.is_file()}
a=tree(V);b=tree(P);checks=[]
def req(label,ok,detail=None):checks.append({'label':label,'pass':bool(ok),'detail':detail})
req('immutable v3 snapshot',a==read(D/'V3_BASELINE_FILES.json'))
m=read(P/'PACKAGE_CONTENTS.json');exp={x['path']:{'sha256':x['sha256'],'bytes':x['bytes']} for x in m['files']}
req('unique manifest members',len(exp)==len(m['files']));req('manifest exact file set',set(exp)|{'PACKAGE_CONTENTS.json'}==set(b))
for p,v in exp.items():req('manifest '+p,b.get(p)==v)
for f in P.rglob('*'):req('no symlink '+f.relative_to(P).as_posix(),not f.is_symlink())
removed=sorted(set(a)-set(b));added=sorted(set(b)-set(a));changed=sorted(p for p in set(a)&set(b) if a[p]!=b[p]);req('no v3 file removed',not removed)
rows=read(P/'PUBLIC_PROJECTION.json')['files'];old=read(V/'PUBLIC_PROJECTION.json')['files'];ids={r['original_sha256']:r for r in rows};req('unique source identities',len(ids)==len(rows))
for r in rows:
 if r['disposition']=='included':req('source '+r['public_path'],b.get(r['public_path'])=={'sha256':r['public_sha256'],'bytes':r['public_bytes']})
 if r['projection']=='EXACT':req('exact original/public '+r['original_sha256'],r['original_sha256']==r['public_sha256'] and r['original_bytes']==r['public_bytes'])
 else:req('amendment disclosed '+r['original_sha256'],bool(r.get('transformations')))
 for c in r.get('required_replay_copies',[]):req('copy '+c['path'],b.get(c['path'])=={'sha256':c['sha256'],'bytes':c['bytes']})
for r in old:
 c=ids.get(r['original_sha256']);req('old identity '+r['original_sha256'],c is not None)
 if c:
  for k in ['original_sha256','original_bytes','disposition','projection','public_path','public_url','public_sha256','public_bytes']:
   if k in r:req('old field '+r['original_sha256']+' '+k,c.get(k)==r[k])
  for cp in r.get('required_replay_copies',[]):req('old replay copy preserved '+cp['path'],cp in c.get('required_replay_copies',[]))
# Independently check machine-readable public locators without treating old custody-only locators as replay promises.
local_bindings=[]
def walk(x,src):
 if isinstance(x,dict):
  for pk,hk in [('public_source','public_sha256'),('public_target','public_sha256'),('public_path','public_sha256')]:
   p=x.get(pk);digest=x.get(hk)
   if isinstance(p,str) and digest and not p.startswith(('https://','CUSTODY_')):
    req('public locator '+src+' -> '+p,p in b and b[p]['sha256']==digest);local_bindings.append((src,p))
  for v in x.values():walk(v,src)
 elif isinstance(x,list):
  for v in x:walk(v,src)
for f in (P/'depth').rglob('*.json'):walk(read(f),f.relative_to(P).as_posix())
for rel in ['CLAIM_REGISTER.json','DEPENDENCY_INDEX.json','CORRECTION_INDEX.json','CROSS_FRONT_INTERFACES.json']:
 key={'CLAIM_REGISTER.json':'claims','DEPENDENCY_INDEX.json':'edges','CORRECTION_INDEX.json':'corrections','CROSS_FRONT_INTERFACES.json':'interfaces'}[rel]
 req('inherited records '+rel,all(r in read(P/rel)[key] for r in read(V/rel)[key]))
for rel in ['apply_additive.py','validate_package.py','INTEGRATION_PINS.json']:
 req('unchanged safety critical '+rel,a[rel]==b[rel])
errors=[x for x in checks if not x['pass']];result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not errors else 'FAIL','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'files':len(b),'bytes':sum(x['bytes'] for x in b.values()),'unchanged_v3_files':len(a)-len(changed)-len(removed),'added':added,'changed':changed,'removed':removed,'source_identities':len(rows),'inherited_source_identities':len(old),'public_binding_count':len(local_bindings),'checks':len(checks),'errors':errors}
for name,obj in [('CANDIDATE_FILES.json',b),('BINDING_CHECKS.json',checks),('CANDIDATE_CHECK.json',result)]: (D/name).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
