"""Small fail-closed primitives shared by the portable successor tools."""
from pathlib import Path, PurePosixPath
import hashlib,json,re,stat,zipfile
ALLOWED_AXIOMS={'propext','Classical.choice','Quot.sound'}
OFFICIAL_ROOTS={'Init','Lean','Std','Lake','Mathlib','Batteries','Aesop','Qq','ProofWidgets','LeanSearchClient','Plausible','ImportGraph','Cli'}
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def safe_path(root,name):
 p=PurePosixPath(name)
 if not name or '\\' in name or p.is_absolute() or any(x in ('..','.') for x in name.split('/')):raise ValueError('Unsafe path: '+name)
 r=Path(root).resolve();q=r.joinpath(*p.parts)
 if q.is_symlink() or any(x.is_symlink() for x in q.parents if x!=r and r in x.parents):raise ValueError('Symlink forbidden: '+name)
 if not q.resolve().is_relative_to(r):raise ValueError('Path escape: '+name)
 return q
def validate_files(root,manifest):
 seen=set()
 for row in manifest['files']:
  name=row['path']
  if name in seen:raise ValueError('Duplicate manifest member: '+name)
  seen.add(name);p=safe_path(root,name)
  if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise ValueError('Integrity mismatch: '+name)
 return len(seen)
def strip_comments(text):
 # Lean block comments nest. Strings are retained; import statements only occur at line starts.
 out=[];i=0;depth=0
 while i<len(text):
  if text[i:i+2]=='/-':depth+=1;i+=2;continue
  if depth and text[i:i+2]=='-/':depth-=1;i+=2;continue
  if not depth and text[i:i+2]=='--':
   j=text.find('\n',i);i=len(text) if j<0 else j;continue
  if not depth or text[i]=='\n':out.append(text[i])
  i+=1
 if depth:raise ValueError('Unterminated Lean block comment')
 return ''.join(out)
def imports(text):
 return [m for line in strip_comments(text).splitlines() if re.match(r'^\s*(?:public\s+)?import\s+',line) for m in re.sub(r'^\s*(?:public\s+)?import\s+','',line).split()]
def order_modules(sources,roots):
 visiting=set();seen=set();ordered=[]
 def walk(m):
  if m in visiting:raise ValueError('Custom source cycle at '+m)
  if m in seen:return
  if m not in sources:
   if m.split('.')[0] in OFFICIAL_ROOTS:return
   raise ValueError('Missing custom source dependency: '+m)
  visiting.add(m)
  for dep in imports(sources[m]):walk(dep)
  visiting.remove(m);seen.add(m);ordered.append(m)
 for m in roots:walk(m)
 return ordered

def parse_audit(text,targets):
 if len(set(targets))!=len(targets) or not targets:raise ValueError('Empty or duplicate target list')
 if re.search(r'\bsorryAx\b|\berror:|declaration uses .sorry.',text):raise ValueError('Invalid audit diagnostic')
 seen={}
 for n,body in re.findall(r"^'(.+)' (does not depend on any axioms|depends on axioms: \[[^\]]*\])$",text,re.M):
  if n in seen:raise ValueError('Duplicate axiom readback: '+n)
  vals=[] if body.startswith('does not') else [v.strip() for v in body.split('[',1)[1][:-1].split(',') if v.strip()]
  if not set(vals)<=ALLOWED_AXIOMS:raise ValueError('Unapproved axioms for '+n)
  seen[n]=sorted(vals)
 if set(seen)!=set(targets):raise ValueError('Axiom target set mismatch')
 for n in targets:
  if not re.search(r'(?m)^@?'+re.escape(n)+r'(?:\.\{[^}]*\})?\s*:',text):raise ValueError('Missing declaration type: '+n)
 return seen

def extract_zip(archive,out):
 out=Path(out)
 if out.exists():raise ValueError('Fresh absent extraction directory required')
 with zipfile.ZipFile(archive) as z:
  names=set()
  for f in z.infolist():
   name=f.filename.rstrip('/')
   safe_path(out,name)
   if name in names:raise ValueError('Duplicate zip member '+name)
   names.add(name)
   if stat.S_ISLNK(f.external_attr>>16):raise ValueError('ZIP symlink forbidden')
  if z.testzip() is not None:raise ValueError('ZIP CRC mismatch')
  out.mkdir(parents=True);z.extractall(out)
 return out

def write_json(path,obj):Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def verify_git_snapshot(archive,identity):
 """Recompute every Git blob and the root tree, independent of a .git directory."""
 tree={}
 entries=identity['git_entries']
 with zipfile.ZipFile(archive) as z:
  names={p.filename for p in z.infolist() if not p.is_dir()}
  if names!={p['path'] for p in entries}:raise ValueError('Canonical archive census mismatch')
  for e in entries:
   if e['type']!='blob':raise ValueError('Unsupported canonical Git object type')
   b=z.read(e['path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
   if blob!=e['git_blob']:raise ValueError('Canonical Git blob mismatch: '+e['path'])
   node=tree;parts=e['path'].split('/')
   for part in parts[:-1]:node=node.setdefault(part,{})
   node[parts[-1]]=(e['mode'],bytes.fromhex(blob))
 def digest(node):
  rows=[]
  for name,val in node.items():
   directory=isinstance(val,dict);mode,h=('40000',digest(val)) if directory else val
   rows.append((name+('/' if directory else ''),mode.encode()+b' '+name.encode()+b'\0'+h))
  raw=b''.join(value for key,value in sorted(rows));return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).digest()
 if digest(tree).hex()!=identity['tree']:raise ValueError('Canonical root Git tree mismatch')
 return len(entries)

def verify_manifest(root,expected_digest=None):
 root=Path(root);manifest=root/'MASTER_MANIFEST.json';digest=sha(manifest)
 if digest!=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]:raise ValueError('Master manifest seal mismatch')
 if expected_digest is not None and digest!=expected_digest:raise ValueError('Master manifest changed during replay')
 validate_files(root,json.loads(manifest.read_text()));return digest

def verify_source_graph(root,suites,graph):
 expected={(s['id'],m) for s in suites for m in s['module_order']};actual={(r['suite'],r['module']) for r in graph}
 if expected!=actual or len(actual)!=len(graph):raise ValueError('Dependency graph module census mismatch')
 rows={(r['suite'],r['module']):r for r in graph};count=0
 for s in suites:
  for m in s['module_order']:
   rel=s['source_root']+'/'+m.replace('.','/')+'.lean';f=safe_path(root,rel);r=rows[(s['id'],m)]
   if r['source']!=rel or sha(f)!=r['sha256'] or imports(f.read_text())!=r['imports']:raise ValueError('Dependency graph/source mismatch: '+s['id']+'/'+m)
   count+=1
 return count

def reject_custom_shadows(official_libraries,modules):
 for library in official_libraries:
  for module in modules:
   path=Path(library)/Path(*module.split('.')).with_suffix('.olean')
   if path.exists():raise ValueError('Official cache shadows custom module: '+str(path))

def check_fixture_stdout(text,expected):
 actual=text.strip().splitlines()
 if actual!=expected:raise ValueError('Executable fixture output mismatch: '+repr(actual)+' != '+repr(expected))
 return actual

def verify_replay_evidence(root,entries,suites):
 """Check retained replay data, without claiming to rerun Lean or authenticate history."""
 current={s['id']:s for s in suites};covered={}
 for entry in entries:
  path=safe_path(root,entry['receipt'])
  if sha(path)!=entry['sha256']:raise ValueError('Replay receipt digest mismatch')
  result=json.loads(path.read_text())
  if result['status']!='PASS':raise ValueError('Non-passing replay receipt')
  if result.get('manifest_sha256')!=entry['input_snapshot_manifest_sha256']:raise ValueError('Recorded input snapshot identity mismatch')
  for record in result['suites']:
   sid=record['id']
   if sid not in current or sid in covered:raise ValueError('Unknown/duplicate recorded suite '+sid)
   suite=current[sid]
   if record['status']!='FRESH_CUSTOM_SOURCE_BUILD_AND_TYPE_AXIOM_READBACK_PASS':raise ValueError('Non-passing recorded suite '+sid)
   expected_paths={m.replace('.','/')+'.lean' for m in suite['module_order']}
   if set(record['sources'])!=expected_paths:raise ValueError('Recorded source census mismatch '+sid)
   for rel,binding in record['sources'].items():
    source=safe_path(root,suite['source_root']+'/'+rel)
    if sha(source)!=binding['sha256'] or source.stat().st_size!=binding['bytes']:raise ValueError('Recorded source binding mismatch '+sid+'/'+rel)
   builds={}
   for build in record['modules']:
    name=build['module']
    if name in builds or build['exit_code']!=0:raise ValueError('Ambiguous or failed recorded command '+sid+'/'+name)
    builds[name]=build
    for stream in ['stdout','stderr']:
     p=safe_path(root,entry['log_root']+'/'+sid+'/'+name+'.'+stream)
     if sha(p)!=build[stream+'_sha256']:raise ValueError('Recorded output digest mismatch '+str(p))
   for module,expected in suite.get('stdout_expectations',{}).items():
    if module not in builds:raise ValueError('Missing recorded fixture module '+module)
    log=safe_path(root,entry['log_root']+'/'+sid+'/'+module+'.stdout').read_text()
    actual=check_fixture_stdout(log,expected)
    if 'fixture_output' in builds[module] and builds[module]['fixture_output']!=actual:raise ValueError('Recorded fixture metadata mismatch '+module)
   for module in suite['module_order']:
    if module not in builds or len(builds[module].get('olean_sha256',''))!=64:raise ValueError('Missing recorded custom artifact binding '+module)
   if set(record['claim_sets'])!=set(suite['targets']):raise ValueError('Claim-set census mismatch '+sid)
   target_counts={}
   for claim,targets in suite['targets'].items():
    name='PortableAudit_'+re.sub('[^A-Za-z0-9_]','_',claim)
    if name not in builds:raise ValueError('Missing recorded audit command '+sid+'/'+claim)
    log=safe_path(root,entry['log_root']+'/'+sid+'/'+name+'.stdout').read_text();decls=parse_audit(log,targets)
    if record['claim_sets'][claim]['declarations']!=decls or record['claim_sets'][claim]['target_count']!=len(targets):raise ValueError('Recorded audit mismatch '+sid+'/'+claim)
    target_counts[claim]=len(targets)
   covered[sid]={'receipt':entry['receipt'],'receipt_sha256':entry['sha256'],'source_modules':len(expected_paths),'target_counts_by_claim_set':target_counts}
 if set(covered)!=set(current):raise ValueError('Missing recorded replay coverage: '+repr(sorted(set(current)-set(covered))))
 return {'status':'RECORDED_REPLAY_SOURCE_LOG_TARGET_BINDINGS_PASS','suites':covered,'scope':'Consistency of retained source hashes, command status, output logs and type/axiom readbacks. This does not rerun Lean, authenticate historical execution, or add target counts across overlapping suites.'}

def verify_commit_identity(raw,expected_commit,expected_tree):
 actual=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if actual!=expected_commit:raise ValueError('Canonical Git commit object mismatch')
 if raw.split(b'\n',1)[0]!=('tree '+expected_tree).encode():raise ValueError('Canonical commit/tree linkage mismatch')
 return True
