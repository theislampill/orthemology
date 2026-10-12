from pathlib import Path
import re,json,hashlib
W=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parent
x=json.loads((R/'frozen/INPUTS.json').read_text()); existing={r['module']:r for r in x['external_source_objects']}
pkgs=sorted((W/'separating-projection-lean-20261009/.lake/packages').iterdir())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def initial_imports(s):
 i=0;found=[]
 while i<len(s):
  if s[i].isspace():i+=1;continue
  if s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j;continue
  if s[i:i+2]=='/-':
   depth=1;i+=2
   while depth:
    assert i<len(s)
    if s[i:i+2]=='/-':depth+=1;i+=2
    elif s[i:i+2]=='-/':depth-=1;i+=2
    else:i+=1
   continue
  m=re.match(r'(prelude|import)\b',s[i:])
  if not m:return found
  token=m.group();i+=len(token)
  if token=='prelude':continue
  j=s.find('\n',i);j=len(s) if j<0 else j
  raw=s[i:j].split('--')[0].strip()
  for name in raw.split():
   assert re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*',name),(name,raw)
   found.append(name)
  i=j
 return found
def closure():
 todo=['Mathlib.Data.Fintype.EquivFin'];seen=set();extra=[]
 while todo:
  m=todo.pop()
  if m in seen:continue
  seen.add(m)
  if m.split('.')[0] in ['Init','Lean','Std','Lake']:continue
  rel=Path(*m.split('.'))
  candidates=[(p/(str(rel)+'.lean'),p/'.lake/build/lib/lean'/(str(rel)+'.olean')) for p in pkgs if (p/(str(rel)+'.lean')).is_file()]
  assert len(candidates)==1,(m,candidates)
  s,o=candidates[0];assert o.is_file(),str(o)
  if m not in existing:
   extra.append({'module':m,'source_path':str(s.relative_to(W)),'source_sha256':sha(s),'object_path':str(o.relative_to(W)),'object_sha256':sha(o),'scope':'Existing external object, hash-bound and reused, not rebuilt.'})
  else:
   assert sha(s)==existing[m]['source_sha256'];assert sha(o)==existing[m]['object_sha256']
  todo.extend(initial_imports(s.read_text()))
 return seen,extra
if __name__=='__main__':
 seen,extra=closure()
 (R/'REVIEW_DEPENDENCIES.json').write_text(json.dumps({'scope':'Extra external import closure for independent finite-reachable-image control; baseline author inputs remain unchanged.','extra_external_source_objects':sorted(extra,key=lambda r:r['module']),'inspected_external_modules':len(seen)},indent=2)+'\n')
 print('Extra external dependencies',len(extra),'total traversed',len(seen))
 y=json.loads((W/x['receipt']['path']).read_text());source={r['module']:r for r in y['source_checks']};objects={r['module']:r for r in y['build_records']}
 assert y['status']=='PASS'
 for r in x['source_objects']:
  assert source[r['module']]['sha256']==r['source_sha256']
  assert objects[r['module']]['source_sha256']==r['source_sha256']
  assert objects[r['module']]['object_sha256']==r['object_sha256']
  assert objects[r['module']]['trust_zero'] and objects[r['module']]['exit_code']==0
 print('All 30 retained source/object pairs independently matched to prerequisite trust-zero receipt.')
