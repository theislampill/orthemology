import hashlib,json,pathlib,os,re,subprocess,time
WS=pathlib.Path(__file__).resolve().parent.parent
OUT=WS/'hase-full-per-review-20261010'
LIB=OUT/'fresh-lib';LIB.mkdir(exist_ok=False)
ROOT=WS/'hase-imported-compiler-transport-20261010'
PKG=WS/'separating-projection-lean-20261009/.lake/packages'
LEAN=WS/'.toolchains/lean-4.19.0-linux/bin/lean'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest_checks=[]
for name in ['hase-open-term-standardness-20261010','hase-imported-compiler-transport-20261010','hase-raw-motive-boundary-20261010']:
 root=WS/name
 for r in json.loads((root/'MANIFEST.json').read_text())['files']:
  p=root/r['path'];assert sha(p)==r['sha256'],p
  if 'bytes' in r:assert p.stat().st_size==r['bytes'],p
 manifest_checks.append({'package':name,'manifest_sha256':sha(root/'MANIFEST.json'),'file_count':len(json.loads((root/'MANIFEST.json').read_text())['files'])})
acq=json.loads((ROOT/'ACQUISITION.json').read_text());items={r['module']:r for r in acq['sources']};assert len(items)==83 and not acq['missing']
index=json.loads((ROOT/'PINNED_SOURCE_INDEX.json').read_text());indexed={r['public_path']:r for r in index['sources']}
checks=[]
def decomment(s):
 o=[];d=0;i=0
 while i<len(s):
  if s[i:i+2]=='/-':d+=1;i+=2
  elif d and s[i:i+2]=='-/':d-=1;i+=2
  elif not d and s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j
  else:
   if not d or s[i]=='\n':o.append(s[i])
   i+=1
 assert not d
 return ''.join(o)
for m,r in items.items():
 p=ROOT/'sources'/f'{m}.lean';b=p.read_bytes();imports=[x for line in decomment(b.decode()).splitlines() if re.match(r'^\s*import\s',line) for x in line.split()[1:]]
 assert sha(p)==r['sha256'];assert imports==r['imports']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob']
 assert indexed[r['path']]['public_sha256']==r['sha256']
 checks.append({'module':m,'sha256':sha(p),'git_blob':r['git_blob'],'imports':imports,'indexed':True})
for name in ['OpenTermStandardness','FrozenCompilerMirror','PERInterface']:
 assert (ROOT/'proofs'/f'{name}.lean').read_bytes()==(WS/'hase-open-term-standardness-20261010'/f'{name}.lean').read_bytes()
mathlib=PKG/'mathlib'
assert subprocess.check_output(['git','-C',str(mathlib),'rev-parse','HEAD'],text=True).strip()=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
base=mathlib/'.lake/build/lib/lean/Mathlib'
for p in base.rglob('*'):
 if p.is_file():
  q=LIB/'Mathlib'/p.relative_to(base);q.parent.mkdir(parents=True,exist_ok=True);q.symlink_to(p)
libs=sorted(p/'.lake/build/lib/lean' for p in PKG.iterdir() if p.is_dir());env={**os.environ,'LEAN_PATH':':'.join(map(str,[LIB]+libs))}
(OUT/'lean_path.txt').write_text(env['LEAN_PATH']+'\n')
log=(OUT/'PREREQUISITE_REBUILD.log').open('w');version=subprocess.check_output([str(LEAN),'--version'],text=True).strip();log.write(version+'\n')
records=[]
def build(m,p,cwd):
 dest=LIB/pathlib.Path(*m.split('.')).with_suffix('.olean');assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True)
 cmd=[str(LEAN),'--trust=0','-o',str(dest),str(p)];start=time.time();run=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True)
 log.write('$ '+' '.join(cmd)+'\n'+run.stdout+run.stderr);log.flush()
 records.append({'module':m,'source_sha256':sha(p),'object_sha256':sha(dest) if dest.exists() else None,'trust_zero':True,'exit_code':run.returncode,'seconds':round(time.time()-start,3)})
 print(m,run.returncode,flush=True);assert run.returncode==0,run.stdout+run.stderr
for m in ['Mathlib.Algebra.MvPolynomial.Polynomial','Mathlib.Algebra.MvPolynomial.Funext']:
 p=mathlib/pathlib.Path(*m.split('.')).with_suffix('.lean');assert p.read_bytes()==subprocess.check_output(['git','-C',str(mathlib),'show','HEAD:'+str(p.relative_to(mathlib))]);build(m,p,mathlib)
seen=set();active=set()
def visit(m):
 if m not in items or m in seen:return
 assert m not in active;active.add(m)
 for dep in items[m]['imports']:visit(dep)
 build(m,ROOT/'sources'/f'{m}.lean',ROOT/'sources');active.remove(m);seen.add(m)
visit(acq['root']);assert set(items)==seen
for m in ['OpenTermStandardness','FrozenCompilerMirror','PERInterface','ImportedCompilerTransport']:build(m,ROOT/'proofs'/f'{m}.lean',ROOT/'proofs')
result={'status':'PASS','scope':'Fresh trust-zero prerequisite replay; no full-PER soundness claim','lean_version':version,'lean_binary_sha256':sha(LEAN),'manifest_checks':manifest_checks,'source_checks':checks,'build_records':records,'pin':acq['pin'],'mathlib_revision':'c44e0c8ee63ca166450922a373c7409c5d26b00b','external_library_objects_reused':True}
(OUT/'PREREQUISITE_REBUILD.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS prerequisites',flush=True)
