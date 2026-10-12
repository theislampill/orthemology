#!/usr/bin/env python3
"""Fresh local-dependency rebuild and exact target audit; no parent oleans imported."""
from pathlib import Path
import sys,os,re,json,hashlib,datetime,zipfile,subprocess
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'handoff'))
from qualify_lean419 import guard_version,verify_dependencies,validate_inventory,source_lint
from canonical_gate import run_bounded,parse_audit,APPROVED_AXIOMS
H=lambda b:hashlib.sha256(b).hexdigest()
P=Path(os.environ.get('P01_PARENT_PROJECT','private-locator:f27ed1fe8acaf6f42e17')).resolve()
PACKET=Path(os.environ.get('P01_PARENT_PACKET','private-locator:5c3e9e56216cbd1fa602')).resolve()
SUCCESSOR=Path(os.environ.get('P01_SUCCESSOR','private-locator:a441cffeddaa6ab1c3f8')).resolve()
L=Path(os.environ.get('P01_LEAN','private-locator:4211d241978f643cb623')).resolve()
CANON=Path(os.environ.get('P01_CANONICAL','private-locator:36fb2027a2cd56fb6b89')).resolve()
main=['P01CanonicalCarrierProjection']
contracts=['ProjectionContract']
W=R/(sys.argv[1] if len(sys.argv)>1 else 'qualification-final')
W.mkdir();(W/'sources').mkdir();(W/'artifacts').mkdir();(W/'evidence').mkdir()
receipt={'schema':'p01-canonical-carrier-projection-v1','status':'NOT_QUALIFIED','kernel_credit':False,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main_modules':main,'source_scope':'Exact unary canonical Code-carrier squares for raw-index Pi/Id and represented Sigma; one-way generic arrow/identity inclusions and strict countermodels; no full recursive canonical equality or adoption'}
def git(*args):
 p=subprocess.run(['git','-C',str(CANON),*args],check=True,capture_output=True,text=True);return p.stdout.strip()
try:
 receipt['driver_sha256']=H(Path(__file__).read_bytes());receipt['compiler_binary_sha256']=H(L.read_bytes())
 receipt['helper_sha256']={p.name:H(p.read_bytes()) for p in (R/'handoff').glob('*.py')}
 receipt['compiler_path']=str(L)
 version=run_bounded([str(L),'--version'],W);assert version['ok'];guard_version(version['stdout']);receipt['compiler']=version['stdout'].strip()
 parent=Path(os.environ.get('P01_PARENT_RECEIPT','private-locator:0af38908eca905bd4934'))
 pj=json.loads(parent.read_text());assert pj['kernel_credit'] and pj['target_count']==382
 inv=validate_inventory(PACKET);assert H((PACKET/'formal/SOURCE_INVENTORY.json').read_bytes())==pj['source_inventory_sha256']
 receipt['parent_receipt_sha256']=H(parent.read_bytes());receipt['parent_source_inventory_sha256']=pj['source_inventory_sha256']
 receipt['dependencies']=verify_dependencies(P,json.loads((P/'lake-manifest.json').read_text()))
 receipt['canonical_commit']=git('rev-parse','HEAD');assert receipt['canonical_commit']=='03e2604dfcef278b01c60d19b05370fcec4194b6'
 receipt['canonical_status_before']=git('status','--porcelain=v1');assert not receipt['canonical_status_before']
 zip_path=SUCCESSOR/'P01_Recursive_Curry_Effect_Successor_2026-09-30.zip'
 receipt['successor_archive_sha256']=H(zip_path.read_bytes());assert receipt['successor_archive_sha256']=='e4698d9acf9f2b3ab637c0b35bbfb361b8c31a58368bef4ddbace53693867f24'
 origins={}
 for row in inv['files']:
  src=PACKET/row['path']
  if src.suffix=='.lean' and src.stem!='lakefile':
   assert src.stem not in origins
   origins[src.stem]=src
   assert H((P/src.name).read_bytes())==H(src.read_bytes())
 with zipfile.ZipFile(zip_path) as z:
  for name in ['P01RecursiveModel','P01CurryParametricity','P01ModelWitnesses']:
   src=SUCCESSOR/'sources'/(name+'.lean');assert src.read_bytes()==z.read('sources/'+src.name);origins[name]=src
 DEP=Path(os.environ.get('P01_DEPENDENT','private-locator:4895465318e5977e697d')).resolve()
 dep_zip=DEP/'P01_Raw_Index_Dependent_Successor_2026-09-30.zip'
 receipt['dependent_archive_sha256']=H(dep_zip.read_bytes());assert receipt['dependent_archive_sha256']=='dec5951de21c2ef0918f9eb6da130907e4dba4df213dd84ef04209aa251840cc'
 with zipfile.ZipFile(dep_zip) as z:
  for name in ['P01DependentModel','P01DependentSubstitution','P01DependentFundamental','P01DependentControls','P01DependentRepresentation']:
   src=DEP/'sources'/(name+'.lean');assert src.read_bytes()==z.read('sources/'+src.name);origins[name]=src
 receipt['canonical_constructor_sources']={}
 for name in ['InternalPolymorphism','EffectsAndDependence']:
  src=CANON/'experiments/orthemology-v5/source/lean'/(name+'.lean')
  assert src.read_bytes()==origins[name].read_bytes()
  receipt['canonical_constructor_sources'][name]={'canonical_path':str(src.relative_to(CANON)),'sha256':H(src.read_bytes()),'matches_compiled_predecessor':True}
 for name in main+contracts:origins[name]=R/'sources'/(name+'.lean')
 order=[];active=set();visited=set()
 def visit(name):
  if name in visited:return
  assert name not in active;active.add(name)
  for line in origins[name].read_text().splitlines():
   m=re.match(r'^import\s+([A-Za-z][A-Za-z0-9_.]*)\s*$',line)
   if m and m[1] in origins:visit(m[1])
  active.remove(name);visited.add(name);order.append(name)
 for name in main+contracts+['AuditSupport']:visit(name)
 receipt['module_order']=order;receipt['source_bindings']={};names=[];theorem_count=0
 for name in order:
  src=origins[name];txt=src.read_text();dst=W/'sources'/src.name;dst.write_bytes(src.read_bytes())
  receipt['source_bindings'][name]={'origin':str(src),'sha256':H(src.read_bytes()),'bytes':src.stat().st_size,'role':'new' if name in main else 'contract' if name in contracts else 'predecessor'}
  if name not in main:continue
  source_lint(txt);ns=[]
  for line in txt.splitlines():
   m=re.fullmatch(r'namespace ([A-Za-z][A-Za-z0-9_.]*)',line)
   if m:ns.append(m[1]);continue
   if re.fullmatch(r'end [A-Za-z][A-Za-z0-9_.]*',line):ns.pop();continue
   m=re.match(r'^(?:@\[[^]]+\] )?(?:(?:noncomputable|private) )?(def|abbrev|theorem|lemma|structure|inductive|instance) ([A-Za-z][A-Za-z0-9_.]*)',line)
   if m:names.append('.'.join(ns+[m[2]]));theorem_count+=m[1] in ['theorem','lemma']
 assert names and len(names)==len(set(names))
 audit=['import '+n for n in main]+['import AuditSupport','set_option pp.universes true','set_option format.width 120']
 for n in names:audit += [f'#eval IO.println "AUDIT_BEGIN {n}"',f'#check {n}',f'#ortho_audit {n}',f'#print axioms {n}',f'#eval IO.println "AUDIT_END {n}"']
 (W/'sources/DependentAudit.lean').write_text('\n'.join(audit)+'\n')
 paths=[W/'artifacts']+[d/'.lake/build/lib/lean' for d in (P/'.lake/packages').iterdir()]
 env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,paths));receipt['lean_path']=env['LEAN_PATH']
 receipt['artifacts']=[]
 for name in order+['DependentAudit']:
  target=W/'artifacts'/(name+'.olean');assert not target.exists()
  q=run_bounded([str(L),'-j1','-o',str(target),name+'.lean'],W/'sources',env=env,timeout=900,output_limit=32*1024*1024)
  for stream in ['stdout','stderr']:(W/'evidence'/(name+'.'+stream)).write_text(q[stream])
  (W/'evidence'/(name+'.json')).write_text(json.dumps({k:v for k,v in q.items() if k not in ['stdout','stderr']},indent=2)+'\n')
  assert q['ok'],f'compiler failure {name}'
  assert not re.search(r'\bsorry\b|sorryAx|declaration uses|error:',q['stdout']+q['stderr']),f'bad diagnostics {name}'
  if name in main:assert not q['stdout'].strip() and not q['stderr'].strip(),f'nonempty source diagnostics {name}'
  receipt['artifacts'].append({'module':name,'path':str(target.relative_to(W)),'sha256':H(target.read_bytes()),'bytes':target.stat().st_size})
  print(name,'PASS',flush=True)
 receipt['declarations']=parse_audit(q['stdout'],names)
 receipt['axiom_union']=sorted({a for d in receipt['declarations'].values() for a in d['axioms']});assert set(receipt['axiom_union'])<=APPROVED_AXIOMS
 for name,row in receipt['source_bindings'].items():assert H(origins[name].read_bytes())==row['sha256']==H((W/'sources'/(name+'.lean')).read_bytes())
 assert H(Path(__file__).read_bytes())==receipt['driver_sha256']
 assert {p.name:H(p.read_bytes()) for p in (R/'handoff').glob('*.py')}==receipt['helper_sha256']
 assert H(zip_path.read_bytes())==receipt['successor_archive_sha256']
 assert H(dep_zip.read_bytes())==receipt['dependent_archive_sha256']
 receipt['canonical_status_after']=git('status','--porcelain=v1');assert receipt['canonical_status_after']==receipt['canonical_status_before']
 assert git('rev-parse','HEAD')==receipt['canonical_commit']
 receipt.update(status='KERNEL_VERIFIED_CANONICAL_CARRIER_PROJECTION',kernel_credit=True,target_count=len(names),theorem_declaration_count=theorem_count,fresh_module_count=len(order),main_module_count=len(main),canonical_adoption=False)
except Exception as e:
 receipt.update(status='QUALIFICATION_FAILED',reason=repr(e))
receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(W/'QUALIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k in ['status','reason','target_count','theorem_declaration_count','fresh_module_count','axiom_union']},indent=2))
sys.exit(0 if receipt['kernel_credit'] else 1)
