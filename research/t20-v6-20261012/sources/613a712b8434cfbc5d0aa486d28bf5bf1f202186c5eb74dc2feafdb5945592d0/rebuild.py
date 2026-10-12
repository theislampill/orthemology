#!/usr/bin/env python3
"""Independent sealed-input verifier and fresh local-module rebuild.
No author helper or prior local P01 artifact is imported. External package caches
and the selected Lean distribution are trusted compiled dependencies.
"""
from pathlib import Path, PurePosixPath
import hashlib,json,zipfile,re,subprocess,os,datetime,sys,time
ROOT=Path(__file__).resolve().parent
AUTHOR=Path('private-locator:afd0ca9a59c89e12a91c')
CANON=Path('private-locator:36fb2027a2cd56fb6b89')
ENV=Path('private-locator:4b06887cf6b87610e5b8')
LEAN=ENV/'lean-4.19.0-linux/bin/lean'
ARCHIVE=AUTHOR/'P01_Canonical_Carrier_Projection_2026-09-30.zip'
PIN='4b5590eaa1667a1fb86fd55714412311dba9f14d6f294c830c36766db5252756'
COMMIT='03e2604dfcef278b01c60d19b05370fcec4194b6'
H=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True).strip()
def snapshot(root):return {str(p.relative_to(root)):H(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
receipt={'schema':'independent-canonical-carrier-audit-v1','started_utc':now(),'status':'RUNNING','canonical_adoption':False,'governor_lifecycle_or_closure_authority':False}
try:
 before=snapshot(AUTHOR)
 assert H(ARCHIVE.read_bytes())==PIN
 receipt['archive']={'path':str(ARCHIVE),'sha256':PIN,'bytes':ARCHIVE.stat().st_size}
 assert git(CANON,'rev-parse','HEAD')==COMMIT and not git(CANON,'status','--porcelain=v1')
 receipt['canonical_before']={'commit':COMMIT,'status':''}
 with zipfile.ZipFile(ARCHIVE) as z:
  assert z.testzip() is None
  members=z.namelist();assert len(members)==len(set(members))
  assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in members)
  manifest=json.loads(z.read('RESULT_MANIFEST.json'))
  rows=manifest['files'];assert len(rows)==len({r['path'] for r in rows})
  assert set(members)=={r['path'] for r in rows}|{'RESULT_MANIFEST.json'}
  for r in rows:
   b=z.read(r['path']);assert len(b)==r['bytes'] and H(b)==r['sha256'];assert (AUTHOR/r['path']).read_bytes()==b
  assert (AUTHOR/'RESULT_MANIFEST.json').read_bytes()==z.read('RESULT_MANIFEST.json')
  q=json.loads(z.read('qualification-final/QUALIFICATION.json'))
  assert H(z.read('qualification-final/QUALIFICATION.json'))==manifest['authoritative_receipt_sha256']
  receipt['sealed_manifest']={'sha256':H(z.read('RESULT_MANIFEST.json')),'files':len(rows),'archive_members':len(members),'exact_coverage':True}
  receipt['author_receipt']={'sha256':manifest['authoritative_receipt_sha256'],'reported_targets':q['target_count'],'reported_theorems':q['theorem_declaration_count']}
  src=ROOT/'sources';obj=ROOT/'artifacts';ev=ROOT/'evidence'
  for p in [src,obj,ev]:p.mkdir(exist_ok=False)
  sources={}
  for name,row in q['source_bindings'].items():
   b=z.read('qualification-final/sources/'+name+'.lean');assert H(b)==row['sha256']
   assert Path(row['origin']).read_bytes()==b
   if row['role'] in ['new','contract']:assert b==z.read('sources/'+name+'.lean')
   sources[name]=b.decode();(src/(name+'.lean')).write_bytes(b)
  receipt['source_bindings']={n:{'sha256':H(s.encode()),'bytes':len(s.encode())} for n,s in sources.items()}
  receipt['canonical_constructor_owners']={}
  for name,row in q['canonical_constructor_sources'].items():
   canonical=CANON/row['canonical_path'];b=canonical.read_bytes()
   historical=subprocess.check_output(['git','-C',str(CANON),'show',COMMIT+':'+row['canonical_path']])
   assert b==historical==sources[name].encode();assert H(b)==row['sha256']
   receipt['canonical_constructor_owners'][name]={'path':row['canonical_path'],'sha256':H(b),'working_tree_equals_git_blob_equals_compiled_source':True}
 receipt['predecessor_archive_pins']=[]
 for p,expected in [(Path('private-locator:e7502100ab2e2b274ef0'),'dec5951de21c2ef0918f9eb6da130907e4dba4df213dd84ef04209aa251840cc'),(Path('private-locator:3537146eb78a87f8f527'),'e4698d9acf9f2b3ab637c0b35bbfb361b8c31a58368bef4ddbace53693867f24')]:
  assert H(p.read_bytes())==expected;receipt['predecessor_archive_pins'].append({'path':str(p),'sha256':expected})
 version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
 assert version=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
 assert H(LEAN.read_bytes())==q['compiler_binary_sha256']
 receipt['compiler']={'path':str(LEAN),'version':version,'sha256':H(LEAN.read_bytes())}
 paths=[obj];deps=[]
 for row in q['dependencies']:
  p=ENV/'mathlib4' if row['name']=='mathlib' else ENV/'mathlib4/.lake/packages'/row['name']
  assert git(p,'rev-parse','HEAD')==row['revision'];assert not git(p,'status','--porcelain=v1','--untracked-files=no')
  cache=p/'.lake/build/lib/lean';assert cache.is_dir() or row['name']=='Cli'
  paths.append(cache);deps.append({'name':row['name'],'path':str(p),'revision':row['revision'],'tracked_clean':True,'cache_path':str(cache)})
 receipt['dependencies']=deps
 env=dict(os.environ,LEAN_PATH=':'.join(map(str,paths)))
 receipt['lean_path']=env['LEAN_PATH'];receipt['trusted_external_caches_only']=True
 order=[];active=set();seen=set()
 def visit(n):
  if n in seen:return
  assert n not in active;active.add(n)
  for match in re.finditer(r'^import\s+([^\n]+)',sources[n],re.M):
   for dep in match[1].split():
    if dep in sources:visit(dep)
    else:assert dep in ['Init','Lean'] or dep.startswith('Mathlib.') or dep.startswith('Lean.')
  active.remove(n);seen.add(n);order.append(n)
 for n in ['P01CanonicalCarrierProjection','ProjectionContract','AuditSupport']:visit(n)
 assert set(order)==set(q['module_order']) and len(order)==30
 receipt['independently_resolved_module_order']=order
 main=sources['P01CanonicalCarrierProjection']
 declarations=re.findall(r'^(def|theorem) ([A-Za-z0-9_]+)',main,re.M)
 assert len(declarations)==19 and sum(k=='theorem' for k,n in declarations)==16
 receipt['targets']=[{'name':'P01DF.'+n,'kind':k} for k,n in declarations]
 assert set('P01DF.'+n for k,n in declarations)==set(q['declarations'])
 assert not re.search(r'\b(sorry|axiom|unsafe|admit)\b',main)
 receipt['runs']=[]
 def compile(n):
  target=obj/(n+'.olean');assert not target.exists()
  cmd=[str(LEAN),'-j1','-o',str(target),n+'.lean'];t=time.monotonic()
  p=subprocess.run(cmd,cwd=src,env=env,capture_output=True,text=True,timeout=900)
  (ev/(n+'.stdout')).write_text(p.stdout);(ev/(n+'.stderr')).write_text(p.stderr)
  r={'module':n,'command':cmd,'cwd':str(src),'started_utc':now(),'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode,'stdout_sha256':H(p.stdout.encode()),'stderr_sha256':H(p.stderr.encode())}
  if target.exists():r.update(artifact_sha256=H(target.read_bytes()),artifact_bytes=target.stat().st_size)
  save(ev/(n+'.json'),r);receipt['runs'].append(r)
  assert p.returncode==0 and not re.search(r'\bsorry\b|sorryAx|error:',p.stdout+p.stderr),n+' failed: '+p.stdout+p.stderr
  if n=='P01CanonicalCarrierProjection':assert not p.stdout.strip() and not p.stderr.strip()
  print(n,'PASS',flush=True);return p.stdout
 save(ROOT/'INPUTS_VERIFIED.json',receipt)
 for n in order:compile(n)
 audit=['import P01CanonicalCarrierProjection','import Lean','open Lean Elab Command','set_option pp.universes true','set_option format.width 120',
 '''elab "#independent_kind " n:ident : command => do
  let env ← getEnv
  let some c := env.checked.get.find? n.getId | throwError "unchecked target"
  let kind := match c with
    | .thmInfo _ => "theorem"
    | .defnInfo _ => "def"
    | _ => "other"
  logInfo m!"KIND {n.getId} {kind}"
  let axioms ← Lean.collectAxioms n.getId
  for a in axioms do
    unless a == `propext || a == `Classical.choice || a == `Quot.sound do
      throwError "unexpected axiom: {a}"
''']
 for k,n in declarations:
  n='P01DF.'+n
  audit.extend([f'#eval IO.println "TARGET_BEGIN {n}"',f'#independent_kind {n}',f'#check {n}',f'#print axioms {n}',f'#eval IO.println "TARGET_END {n}"'])
 (src/'IndependentReadback.lean').write_text('\n'.join(audit)+'\n')
 out=compile('IndependentReadback');readback={};axioms=set()
 for kind,n in declarations:
  n='P01DF.'+n
  matches=re.findall(r'^TARGET_BEGIN '+re.escape(n)+r'\n(.*?)^TARGET_END '+re.escape(n)+r'\s*$',out,re.M|re.S);assert len(matches)==1
  block=matches[0];assert 'KIND '+n+' '+kind in block
  original=q['declarations'][n]['type_and_axiom_text'];assert original in block
  used=re.findall(r"'"+re.escape(n)+r"' depends on axioms: \[([^\]]*)\]",block)
  ax={x.strip() for x in used[0].split(',')} if used else set();assert ax==set(q['declarations'][n]['axioms']);axioms.update(ax)
  readback[n]={'kind':kind,'axioms':sorted(ax),'type_and_axiom_text':original}
 receipt.update(target_count=len(readback),theorem_count=sum(d['kind']=='theorem' for d in readback.values()),declarations=readback,axiom_union=sorted(axioms),fresh_local_modules_before_readback=len(order))
 assert before==snapshot(AUTHOR),'author tree changed during verification'
 assert git(CANON,'rev-parse','HEAD')==COMMIT and not git(CANON,'status','--porcelain=v1')
 receipt['preservation']={'author_tree_before_after_equal':True,'author_tree_files':len(before),'author_tree_snapshot_sha256':H(json.dumps(before,sort_keys=True).encode()),'canonical_commit':COMMIT,'canonical_status_after':''}
 save(ROOT/'AUTHOR_TREE_SNAPSHOT.json',before)
 receipt['status']='FRESH_BUILD_AND_EXACT_READBACK_PASS'
except Exception as e:
 receipt.update(status='FAILED',failure=repr(e));raise
finally:
 receipt['finished_utc']=now();receipt['driver_sha256']=H(Path(__file__).read_bytes());save(ROOT/'RECEIPT.json',receipt)
