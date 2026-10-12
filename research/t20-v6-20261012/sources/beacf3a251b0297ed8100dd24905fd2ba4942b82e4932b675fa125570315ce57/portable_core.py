#!/usr/bin/env python3
"""Offline integrity, safe extraction and pinned Lean source-closure helpers."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,re,stat,subprocess,zipfile
OFFICIAL={'Mathlib','Batteries','Lean','Std','Init','Aesop','Qq','ProofWidgets','Plausible','ImportGraph','LeanSearchClient','Cli'}
AXIOMS={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_json(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def safe_path(root,name):
 if not isinstance(name,str) or not name or '\\' in name or '\x00' in name:raise ValueError('Unsafe path')
 p=PurePosixPath(name)
 if p.is_absolute() or any(x in ('','..','.') for x in name.split('/')) or ':' in name:raise ValueError('Unsafe path '+name)
 out=Path(root).joinpath(*p.parts)
 if not out.resolve().is_relative_to(Path(root).resolve()):raise ValueError('Escaping path '+name)
 return out
def check_zip(p,context_root=None,seen=None):
 seen=set() if seen is None else set(seen);identity=str(Path(p).resolve())
 if identity in seen:raise ValueError('Archive provenance cycle')
 seen.add(identity)
 with zipfile.ZipFile(p) as z:
  names=set()
  for f in z.infolist():
   name=f.filename.rstrip('/');safe_path(Path('/not-extracted'),name)
   if name in names:raise ValueError('Duplicate member '+name)
   names.add(name)
   if stat.S_ISLNK(f.external_attr>>16):raise ValueError('ZIP symlink forbidden')
  if z.testzip() is not None:raise ValueError('ZIP CRC failure')
  for member in names:
   if not member.endswith('MANIFEST.json'):continue
   # Only an archive-root manifest declares this archive's local file table.
   # Nested lane/historical manifests retain their original bases and are
   # authenticated as files, with current replay records checked separately.
   if PurePosixPath(member).parent!=PurePosixPath('.'):continue
   # Historical input manifests describe an earlier package, not this directory.
   # Their exact identity and relevant source records are checked by the replay binder.
   if PurePosixPath(member).name=='INPUT_MASTER_MANIFEST.json':continue
   try:manifest=json.loads(z.read(member))
   except (ValueError,KeyError):continue
   rows=manifest.get('files',[]) if isinstance(manifest,dict) else []
   if not isinstance(rows,list):continue
   for row in rows:
    if not isinstance(row,dict) or not {'path','sha256'}<=set(row):continue
    safe_path(Path('/not-extracted'),row['path'])
    target=str(PurePosixPath(member).parent/row['path'])
    if target not in names and row['path'] in names:target=row['path']
    if target not in names:
     # A copied peer manifest can explicitly retain its original companion context.
     provpath=str(PurePosixPath(member).parent/'PROVENANCE.json')
     if context_root is None or provpath not in names:raise ValueError('Archive manifest member missing '+target)
     prov=json.loads(z.read(provpath))
     if 'archive' not in prov or 'sha256' not in prov:raise ValueError('Unbound peer manifest context')
     peer=safe_path(context_root,prov['archive'])
     if sha(peer)!=prov['sha256']:raise ValueError('Peer archive provenance hash')
     check_zip(peer,context_root,seen)
     with zipfile.ZipFile(peer) as original:
      candidates=[n for n in original.namelist() if PurePosixPath(n).name==PurePosixPath(member).name and original.read(n)==z.read(member)]
      if len(candidates)!=1:raise ValueError('Copied manifest not identical to bound companion')
      peerpath=str(PurePosixPath(candidates[0]).parent/row['path'])
      if peerpath not in original.namelist():raise ValueError('Bound peer manifest member missing')
      data=original.read(peerpath)
    else:data=z.read(target)
    if hashlib.sha256(data).hexdigest()!=row['sha256'] or ('bytes' in row and len(data)!=row['bytes']):raise ValueError('Archive manifest identity mismatch '+target)
 return len(names)
def extract_zip(p,out):
 out=Path(out)
 if out.exists():raise ValueError('Extraction destination must be absent')
 check_zip(p)
 with zipfile.ZipFile(p) as z:out.mkdir(parents=True);z.extractall(out)
 return out

def strip_comments(text):
 # Lean block comments nest. Preserve newlines and quoted string contents.
 out=[];i=0;depth=0;quote=False
 while i<len(text):
  if depth:
   if text.startswith('/-',i):depth+=1;i+=2
   elif text.startswith('-/',i):depth-=1;i+=2
   else:
    if text[i]=='\n':out.append('\n')
    i+=1
  elif quote:
   out.append(text[i])
   if text[i]=='\\' and i+1<len(text):i+=1;out.append(text[i])
   elif text[i]=='"':quote=False
   i+=1
  elif text.startswith('/-',i):depth=1;i+=2
  elif text.startswith('--',i):
   j=text.find('\n',i);i=len(text) if j<0 else j
  else:
   if text[i]=='"':quote=True
   out.append(text[i]);i+=1
 if depth:raise ValueError('Unclosed block comment')
 return ''.join(out)
def imports(text):
 result=[]
 for row in re.findall(r'^\s*import\s+([^\n]+)',strip_comments(text),re.M):result.extend(row.split())
 return result
def validate_suite_id(name):
 if not isinstance(name,str) or not re.fullmatch(r'[a-z][a-z0-9_]*',name):raise ValueError('Unsafe suite ID')
 return name
def validate_module(name):
 if not isinstance(name,str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*",name):raise ValueError('Unsafe module name')
 return name
def check_source(text):
 code=strip_comments(text)
 if re.search(r'\b(sorry|admit|sorryAx|native_decide|axiom|constant|unsafe)\b|debug\.skipKernelTC',code):raise ValueError('Unapproved proof-hole/axiom/unsafe token')
 return code
def check_diagnostics(text):
 if re.search(r"\berror:|\bsorryAx\b|declaration uses[^\n]*sorry",text):raise ValueError('Invalid compiler diagnostic')

def public_targets(text):
 stack=[];targets=[]
 for line in strip_comments(text).splitlines():
  line=line.lstrip()
  if not line:continue
  m=re.match(r'(namespace|section|mutual)(?:\s+(\S+))?',line)
  if m:stack.append((m[1],m[2] or ''));continue
  if re.match(r'end(?:\s|$)',line):
   if stack:stack.pop()
   continue
  # Strip declaration attributes, then common harmless modifiers.
  s=re.sub(r'^(?:@\[[^]]*\]\s*)+','',line)
  m=re.match(r'(?:(?:noncomputable|protected)\s+)?(?:def|abbrev|theorem|lemma|inductive|structure|class)\s+([^\s(:{]+)',s)
  if m:
   ns='.'.join(n for kind,n in stack if kind=='namespace');name=m[1];targets.append((ns+'.' if ns else '')+name)
 if len(targets)!=len(set(targets)):raise ValueError('Duplicate target names')
 return targets
def order_modules(rows):
 for x in rows:validate_module(x['module'])
 by={x['module']:x for x in rows}
 if len(by)!=len(rows):raise ValueError('Duplicate module owner')
 seen=set();active=set();order=[]
 def walk(m):
  if m in seen:return
  if m in active:raise ValueError('Import cycle '+m)
  if m not in by:
   if m.split('.')[0] in OFFICIAL:return
   raise ValueError('Missing custom source '+m)
  active.add(m)
  for dep in by[m]['imports']:walk(dep)
  active.remove(m);seen.add(m);order.append(m)
 for m in by:walk(m)
 return order

def parse_readback(text,targets):
 if re.search(r'\bsorryAx\b|\berror:|declaration uses .sorry.',text):raise ValueError('Invalid proof/readback diagnostic')
 seen={}
 for name,body in re.findall(r"^'(.+)' (does not depend on any axioms|depends on axioms:\s*\[[^\]]*\])",text,re.M):
  if name in seen:raise ValueError('Duplicate axiom target '+name)
  vals=[] if body.startswith('does not') else [v.strip() for v in body.split('[',1)[1][:-1].split(',') if v.strip()]
  if not set(vals)<=AXIOMS:raise ValueError('Unexpected axiom '+name)
  seen[name]=sorted(vals)
 if set(seen)!=set(targets):raise ValueError('Exact target-set mismatch '+repr(set(seen)^set(targets)))
 for name in targets:
  if not re.search(r'(?m)^@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',text):raise ValueError('Missing exact declaration type '+name)
 return seen

def verify_pins(lean_bin,mathlib,pins,modules):
 lean_bin=Path(lean_bin).resolve();mathlib=Path(mathlib).resolve();lean=lean_bin/'lean'
 if sha(lean)!=pins['lean_binary_sha256']:raise ValueError('Lean binary SHA256 differs from pinned Linux x86_64 release')
 version=subprocess.check_output([str(lean),'--version'],text=True).strip()
 if '4.19.0' not in version or '6caaee842e94' not in version:raise ValueError('Wrong Lean version/commit')
 libraries=[];checks=[]
 for row in pins['packages']:
  d=mathlib if row['name']=='mathlib' else mathlib/'.lake/packages'/row['name']
  rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip();dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip()
  if rev!=row['revision'] or dirty:raise ValueError('Wrong or dirty dependency '+row['name'])
  lib=d/'.lake/build/lib/lean'
  if row['name']=='mathlib' and not lib.is_dir():raise ValueError('Missing official Mathlib build cache '+str(lib))
  if lib.is_dir():libraries.append(lib)
  checks.append({'name':row['name'],'revision':rev,'tracked_clean':True,'build_cache_present':lib.is_dir()})
 for lib in libraries+[lean_bin.parent/'lib/lean']:
  for m in modules:
   if (lib/Path(m.replace('.','/')+'.olean')).exists():raise ValueError('Custom module shadows official cache '+m)
 return lean,libraries,version,checks

def official_import_rows(root):
 root=Path(root);rows=json.loads((root/'replay/OFFICIAL_IMPORTS.json').read_text())['imports'];seen=set()
 for row in rows:
  m=validate_module(row['module'])
  if m in seen or not m.startswith('Mathlib.') and m!='Mathlib':raise ValueError('Unknown/duplicate upstream import owner')
  seen.add(m)
  if row['repository']!='mathlib' or row['source']!=m.replace('.','/')+'.lean' or not re.fullmatch('[a-f0-9]{40}',row['git_blob']):raise ValueError('Invalid upstream import record')
 suites=json.loads((root/'replay/SUITES.json').read_text())['suites'];needed=set()
 for suite in suites:
  custom={x['module'] for x in suite['modules']}
  needed.update(i for row in suite['modules'] for i in row['imports'] if i not in custom)
 if needed!=seen:raise ValueError('Official import ownership census mismatch')
 return rows

def verify_official_ownership(root,mathlib):
 mathlib=Path(mathlib).resolve();rows=official_import_rows(root)
 for row in rows:
  # git show pins ownership/content at the already revision-checked commit.
  raw=subprocess.check_output(['git','show','HEAD:'+row['source']],cwd=mathlib)
  blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  if blob!=row['git_blob'] or safe_path(mathlib,row['source']).read_bytes()!=raw:raise ValueError('Untracked/wrong official import '+row['module'])
 return rows

def verify_canonical_subset(root):
 root=Path(root);d=json.loads((root/'provenance/canonical/IDENTITY.json').read_text());raw=(root/'provenance/canonical/COMMIT_OBJECT.raw').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=d['commit_object_sha256']:raise ValueError('Commit object SHA256')
 if hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=d['commit']:raise ValueError('Git commit identity')
 if raw.splitlines()[0]!=b'tree '+d['tree'].encode():raise ValueError('Commit tree link')
 tree={};by={}
 for e in d['git_entries']:
  if e['type']!='blob':raise ValueError('Unsupported Git entry')
  safe_path(root,e['path']);node=tree;parts=e['path'].split('/')
  for p in parts[:-1]:node=node.setdefault(p,{})
  if parts[-1] in node:raise ValueError('Duplicate Git path')
  node[parts[-1]]=(e['mode'],bytes.fromhex(e['git_blob']));by[e['path']]=e
 def digest(node):
  rows=[]
  for name,val in node.items():
   isdir=isinstance(val,dict);mode,h=('40000',digest(val)) if isdir else val
   rows.append((name+('/' if isdir else ''),mode.encode()+b' '+name.encode()+b'\0'+h))
  raw=b''.join(v for _,v in sorted(rows));return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).digest()
 if digest(tree).hex()!=d['tree']:raise ValueError('Canonical tree index identity')
 sel=json.loads((root/'provenance/CANONICAL_SELECTION.json').read_text())['files']
 for row in sel:
  p=safe_path(root,row['path']);b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if sha(p)!=row['sha256'] or blob!=by[row['path'].removeprefix('canonical/')]['git_blob']:raise ValueError('Canonical selected blob '+row['path'])
 return {'commit':d['commit'],'tree':d['tree'],'selected_blob_count':len(sel),'scope':'Commit/tree inclusion proof for supplied selected canonical files; omitted canonical contents are not repackaged or reverified'}

def verify(root):
 root=Path(root).resolve();m=root/'MASTER_MANIFEST.json'
 if sha(m)!=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]:raise ValueError('Master manifest hash')
 rows=json.loads(m.read_text())['files'];expected={'MASTER_MANIFEST.json','MASTER_MANIFEST.sha256'}
 for row in rows:
  p=safe_path(root,row['path'])
  if row['path'] in expected:raise ValueError('Duplicate manifest file')
  expected.add(row['path'])
  if not p.is_file() or p.is_symlink() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise ValueError('Missing/tampered member '+row['path'])
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
 if expected!=actual:raise ValueError('Manifest census mismatch '+repr(sorted(expected^actual)))
 archives=[]
 for row in rows:
  if row['path'].endswith('.zip'):archives.append({'path':row['path'],'members':check_zip(root/row['path'],root),'sha256':row['sha256']})
 suites=json.loads((root/'replay/SUITES.json').read_text())['suites']
 seen_ids=set()
 for suite in suites:
  validate_suite_id(suite['id'])
  if suite['id'] in seen_ids:raise ValueError('Duplicate suite ID')
  seen_ids.add(suite['id'])
  for row in suite['modules']:
   validate_module(row['module'])
   p=safe_path(root,row['source']);check_source(p.read_text())
   if sha(p)!=row['sha256'] or imports(p.read_text())!=row['imports'] or public_targets(p.read_text())!=row['targets']:raise ValueError('Source/graph/target binding '+row['source'])
  if order_modules(suite['modules'])!=suite['module_order']:raise ValueError('Topological order mismatch')
 official_import_rows(root)
 refs=json.loads((root/'provenance/REPORT_REFERENCES.json').read_text())
 for name in refs['required_paths']:
  if not safe_path(root,name).exists():raise ValueError('Missing report reference '+name)
 report_mismatches=[]
 for row in refs.get('files',[]):
  if sha(safe_path(root,row['path']))!=row['sha256']:
   if refs.get('status')!='STAGING_REPORT_NOT_FINAL':raise ValueError('Report/source identity mismatch '+row['path'])
   report_mismatches.append(row['path'])
 if refs.get('report') and sha(safe_path(root,refs['report']['path']))!=refs['report']['sha256']:raise ValueError('Report DOCX identity mismatch')
 return {'status':'INTEGRITY_DEPENDENCY_CLOSURE_PASS','manifest_sha256':sha(m),'file_count':len(rows),'archives':archives,'canonical':verify_canonical_subset(root),'suite_count':len(suites),'report_reference_status':('PENDING_DRAFT_UPDATE' if report_mismatches else refs.get('status')),'draft_source_identity_mismatches':report_mismatches,'scope':'Bytes, safe archive members, selected canonical commit/tree inclusion and proof-source closure; fresh Lean replay and mathematical audit are separate evidence'}
