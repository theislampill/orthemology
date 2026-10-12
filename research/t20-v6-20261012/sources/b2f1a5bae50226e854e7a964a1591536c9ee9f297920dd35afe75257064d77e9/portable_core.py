#!/usr/bin/env python3
"""Offline integrity, safe extraction and pinned Lean source-closure helpers."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,re,stat,subprocess,zipfile,sys
if sys.flags.optimize:raise RuntimeError("Optimised Python execution is unsupported")
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
 code=re.sub(r'"(?:\\.|[^"\\])*"', '""', strip_comments(text))
 if re.search(r'\b(sorry|admit|sorryAx|native_decide|unsafe|axiom)\b|debug\.skipKernelTC|(?m:^\s*(?:(?:private|protected)\s+)?(?:axiom|constant|unsafe)\s)',code):raise ValueError('Unapproved proof-hole/axiom/unsafe token')
 return code
def check_diagnostics(text):
 if re.search(r"\bPANIC\b|\berror:|\bsorryAx\b|declaration uses[^\n]*sorry",text):raise ValueError('Invalid compiler diagnostic')

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


def verify_official(root,lean_bin,mathlib,pins,suites):
 rows=json.loads((root/'replay/OFFICIAL_IMPORTS.json').read_text())['imports'];by={r['module']:r for r in rows}
 needed={i for s in suites for r in s['modules'] for i in r['imports'] if i not in {x['module'] for x in s['modules']}}
 if not needed<=by.keys():raise ValueError('Unowned official imports '+repr(needed-by.keys()))
 repos={r['name']:r for r in pins['packages']}
 for m in sorted(needed):
  r=by[m];validate_module(m)
  if r['source']!=m.replace('.','/')+'.lean':raise ValueError('Official source/module mismatch')
  if r['repository']=='lean-release':
   source=Path(lean_bin).parent/'src/lean'/r['source']
   # Release-source digest is inherited from the independently checked release.
   if sha(source)!=r['sha256']:raise ValueError('Lean release source mismatch '+m)
  else:
   if r['repository'] not in repos:raise ValueError('Unknown official repository')
   repo=Path(mathlib) if r['repository']=='mathlib' else Path(mathlib)/'.lake/packages'/r['repository']
   raw=subprocess.check_output(['git','show',repos[r['repository']]['revision']+':'+r['source']],cwd=repo)
   if hashlib.sha256(raw).hexdigest()!=r['sha256'] or safe_path(repo,r['source']).read_bytes()!=raw:raise ValueError('Official ownership mismatch '+m)
 return {'verified_direct_imports':len(needed),'scope':'Pinned tracked direct source ownership; installed official object cache remains trusted'}

def verify(root):
 root=Path(root).resolve();m=root/'MASTER_MANIFEST.json'
 if sha(m)!=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]:raise ValueError('Master manifest hash')
 manifest=json.loads(m.read_text());rows=manifest['files'];expected={'MASTER_MANIFEST.json','MASTER_MANIFEST.sha256'}
 for r in rows:
  p=safe_path(root,r['path'])
  if r['path'] in expected:raise ValueError('Duplicate manifest path')
  expected.add(r['path'])
  if not p.is_file() or p.is_symlink() or sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']:raise ValueError('Input identity mismatch '+r['path'])
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
 if expected!=actual:raise ValueError('Input file census mismatch '+repr(sorted(expected^actual)))
 suites=json.loads((root/'replay/SUITES.json').read_text())['suites'];ids=set()
 for s in suites:
  validate_suite_id(s['id'])
  if s['id'] in ids:raise ValueError('Duplicate suite');
  ids.add(s['id']);names=set()
  for r in s['modules']:
   validate_module(r['module']);p=safe_path(root,r['source']);text=p.read_text();check_source(text)
   if r['module'] in names:raise ValueError('Duplicate module')
   names.add(r['module'])
   if sha(p)!=r['sha256'] or imports(text)!=r['imports']:raise ValueError('Source/import binding mismatch '+r['module'])
  if order_modules(s['modules'])!=s['module_order']:raise ValueError('Module ordering mismatch')
  if len(s['targets'])!=len(set(s['targets'])):raise ValueError('Duplicate target')
  for t in s['targets']:validate_module(t)
  if bind_target_sources(root,s)!=s['target_sources']:raise ValueError('Target/source binding mismatch')
 if {r['path'] for r in rows if r['path'].endswith('.zip')}!={r['path'] for r in manifest.get('archives',[])}:raise ValueError('Archive validation census mismatch')
 for r in manifest.get('archives',[]):
  p=safe_path(root,r['path'])
  if sha(p)!=r['sha256']:raise ValueError('Archive hash')
  check_zip(p)
 refs=root/'tranche3/report/REPORT_REFERENCES.json'
 if refs.exists():
  for r in json.loads(refs.read_text()).get('local_sources',[]):
   if sha(safe_path(root,r['path']))!=r['sha256']:raise ValueError('Report reference mismatch '+r['path'])
 return {'status':'INTEGRITY_AND_SOURCE_CLOSURE_PASS','manifest_sha256':sha(m),'file_count':len(rows),'suite_count':len(suites)}

def declared_targets(text):
 scopes=[];names=[]
 for line in strip_comments(text).splitlines():
  s=line.strip();m=re.match(r'namespace\s+(\S+)',s)
  if m:scopes.append(('namespace',m[1]));continue
  m=re.match(r'(?:noncomputable\s+)?section(?:\s+(\S+))?$',s)
  if m:scopes.append(('section',m[1]));continue
  if re.match(r'end(?:\s+\S+)?$',s):
   if scopes:scopes.pop()
   continue
  m=re.match(r"(?:@\[[^]]*\]\s*)*(?:(?:noncomputable|protected)\s+)?(?:def|abbrev|lemma|theorem|instance|structure|inductive|class)\s+([A-Za-z_][\w']*)",s)
  if m:names.append('.'.join([v for k,v in scopes if k=='namespace']+[m[1]]))
 return names

def bind_target_sources(root,suite):
 by={}
 for row in suite['modules']:
  for name in declared_targets(safe_path(root,row['source']).read_text()):by.setdefault(name,set()).add(row['module'])
 ans={}
 for t in suite['targets']:
  if t not in by or len(by[t])!=1:raise ValueError('Missing/ambiguous fully qualified target owner '+t)
  ans[t]=next(iter(by[t]))
 return ans
