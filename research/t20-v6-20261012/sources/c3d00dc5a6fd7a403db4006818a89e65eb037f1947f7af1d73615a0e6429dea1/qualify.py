#!/usr/bin/env python3
"""Fresh exact-pin qualification of NEW recursive model targets, with fixed parent imports."""
from pathlib import Path
import json,re,hashlib,datetime,sys,os
R=Path(__file__).resolve().parent
sys.path.insert(0,'private-locator:9065824700fca3542e8d')
from qualify_lean419 import guard_version,verify_dependencies,source_lint
from canonical_gate import run_bounded,parse_audit,APPROVED_AXIOMS
P=Path(os.environ.get('P01_PARENT_PROJECT','private-locator:f27ed1fe8acaf6f42e17')).resolve()
L=Path(os.environ.get('P01_LEAN','private-locator:4211d241978f643cb623')).resolve()
W=R/sys.argv[1];W.mkdir();(W/'artifacts').mkdir();(W/'evidence').mkdir()
H=lambda b:hashlib.sha256(b).hexdigest()
receipt={'status':'NOT_QUALIFIED','kernel_credit':False,'scope':'new recursive finite PER interpretation, contextual Curry parametricity, finite shared-seed coupling and exact mass laws; no full dependent model or predecessor adoption','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 parent=Path(os.environ.get('P01_PARENT_RECEIPT','private-locator:0af38908eca905bd4934')).resolve()
 parentj=json.loads(parent.read_text());assert parentj['kernel_credit'] and parentj['target_count']==382
 for a in parentj['compiled_artifacts']:
  rel=Path(a['path']);assert not rel.is_absolute() and '..' not in rel.parts and rel.parts[0]=='project'
  f=P/rel.relative_to('project');assert H(f.read_bytes())==a['sha256']
 receipt['qualification_driver_sha256']=H(Path(__file__).read_bytes())
 receipt['compiler_binary_sha256']=H(L.read_bytes())
 receipt['compiler_binary_path']=str(L)
 receipt['parent_project_path']=str(P)
 receipt['parent_receipt_sha256']=H(parent.read_bytes())
 receipt['parent_source_inventory_sha256']=parentj['source_inventory_sha256']
 receipt['dependencies']=verify_dependencies(P,json.loads((P/'lake-manifest.json').read_text()))
 v=run_bounded([str(L),'--version'],W);assert v['ok'];guard_version(v['stdout']);receipt['compiler']=v['stdout'].strip()
 modules=sys.argv[2:] or ['P01RecursiveModel','P01RecursiveAssertions']
 names=[];receipt['sources']={}
 for m in modules:
  src=R/'sources'/(m+'.lean');text=src.read_text();source_lint(text);(W/src.name).write_text(text)
  receipt['sources'][src.name]={'sha256':H(src.read_bytes()),'bytes':src.stat().st_size}
  namespace=[]
  for line in text.splitlines():
   a=re.fullmatch(r'namespace ([A-Za-z][A-Za-z0-9_.]*)',line)
   if a:namespace.append(a[1]);continue
   if re.fullmatch(r'end [A-Za-z][A-Za-z0-9_.]*',line):namespace.pop();continue
   a=re.match(r'^(?:@\[[^]]+\] )?(?:(?:noncomputable|private) )?(?:def|abbrev|theorem|lemma|structure|inductive|instance) ([A-Za-z][A-Za-z0-9_.]*)',line)
   if a:names.append('.'.join(namespace+[a[1]]))
 assert len(names)==len(set(names)) and names
 audit=['import '+m for m in modules]+['import AuditSupport','set_option pp.universes true','set_option format.width 120']
 for n in names:audit += [f'#eval IO.println "AUDIT_BEGIN {n}"',f'#check {n}',f'#ortho_audit {n}',f'#print axioms {n}',f'#eval IO.println "AUDIT_END {n}"']
 (W/'FrontierAudit.lean').write_text('\n'.join(audit)+'\n')
 paths=[W/'artifacts',P/'.lake/build/lib/lean']+[d/'.lake/build/lib/lean' for d in (P/'.lake/packages').iterdir()]
 env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,paths))
 receipt['lean_path']=env['LEAN_PATH']
 receipt['artifacts']=[]
 for m in modules+['FrontierAudit']:
  target=W/'artifacts'/(m+'.olean');assert not target.exists()
  q=run_bounded([str(L),'-j1','-o',str(target),m+'.lean'],W,env=env,timeout=900,output_limit=32*1024*1024)
  for stream in ['stdout','stderr']:(W/'evidence'/(m+'.'+stream)).write_text(q[stream])
  (W/'evidence'/(m+'.json')).write_text(json.dumps({k:v for k,v in q.items() if k not in ['stdout','stderr']},indent=2)+'\n')
  assert q['ok'],f'compiler failure {m}'
  assert not re.search(r'\bsorry\b|sorryAx|declaration uses|error:',q['stdout']+q['stderr']),f'invalid compiler diagnostics {m}'
  assert target.stat().st_size>0
  receipt['artifacts'].append({'path':str(target.relative_to(W)),'bytes':target.stat().st_size,'sha256':H(target.read_bytes())})
 receipt['declarations']=parse_audit(q['stdout'],names)
 receipt['axiom_union']=sorted({a for d in receipt['declarations'].values() for a in d['axioms']})
 assert set(receipt['axiom_union'])<=APPROVED_AXIOMS and not q['stderr'].strip()
 for name,binding in receipt['sources'].items():assert H((W/name).read_bytes())==binding['sha256']==H((R/'sources'/name).read_bytes())
 assert H(Path(__file__).read_bytes())==receipt['qualification_driver_sha256']
 receipt.update(status='KERNEL_VERIFIED_SCOPED_P01_SUCCESSOR',kernel_credit=True,target_count=len(names))
except Exception as e:receipt.update(status='QUALIFICATION_FAILED',reason=repr(e))
receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(W/'QUALIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['declarations','dependencies','artifacts','sources']},indent=2))
sys.exit(0 if receipt['kernel_credit'] else 1)
