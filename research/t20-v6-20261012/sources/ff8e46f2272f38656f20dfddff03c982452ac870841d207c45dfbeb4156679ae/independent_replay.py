#!/usr/bin/env python3
"""Independent read-only source checks and clean replay, separate from author outputs."""
import hashlib, json, os, pathlib, re, subprocess, time
ROOT=pathlib.Path(__file__).resolve().parent.parent
WS=ROOT.parent
OUT=ROOT/'validation/independent-lib'
OUT.mkdir(exist_ok=False)
PKG=WS/'separating-projection-lean-20261009/.lake/packages'
LEAN=WS/'.toolchains/lean-4.19.0-linux/bin/lean'
PRIOR=WS/'hase-open-term-standardness-20261010'
sha=lambda b:hashlib.sha256(b).hexdigest()
def snapshot(p): return {str(f.relative_to(p)):sha(f.read_bytes()) for f in p.rglob('*') if f.is_file()}
prior_before=snapshot(PRIOR)
acq=json.loads((ROOT/'ACQUISITION.json').read_text())
items={r['module']:r for r in acq['sources']}
assert len(items)==len(acq['sources'])==83
assert not acq['missing']
# Strip nested block and single-line comments before finding imports.
def decomment(s):
    out=[]; depth=0; i=0
    while i<len(s):
        if s[i:i+2]=='/-': depth+=1;i+=2
        elif depth and s[i:i+2]=='-/':depth-=1;i+=2
        elif not depth and s[i:i+2]=='--':
            j=s.find('\n',i);i=len(s) if j<0 else j
        else:
            if not depth or s[i]=='\n':out.append(s[i])
            i+=1
    assert depth==0
    return ''.join(out)
checks=[]
for m,r in items.items():
    p=ROOT/'sources'/f'{m}.lean'; b=p.read_bytes()
    imports=[x for line in decomment(b.decode()).splitlines() if re.match(r'^\s*import\s',line) for x in line.split()[1:]]
    assert sha(b)==r['sha256'],m
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],m
    assert r['sha256'] in pathlib.PurePosixPath(r['path']).parts,m
    assert pathlib.PurePosixPath(r['path']).name==p.name,m
    assert imports==r['imports'],(m,imports,r['imports'])
    checks.append({'module':m,'sha256':sha(b),'git_blob':r['git_blob'],'imports_verified':True})
assert {p.stem for p in (ROOT/'sources').glob('*.lean')}==set(items)
for name in ['OpenTermStandardness','FrozenCompilerMirror','PERInterface']:
    assert (ROOT/'proofs'/f'{name}.lean').read_bytes()==(PRIOR/f'{name}.lean').read_bytes(),name
for r in json.loads((PRIOR/'MANIFEST.json').read_text())['files']:
    assert sha((PRIOR/r['path']).read_bytes())==r['sha256'],r['path']
for r in json.loads((PRIOR/'SOURCE_BINDINGS.json').read_text())['sources']:
    assert (ROOT/'sources'/r['name']).read_bytes()==(PRIOR/r['local_path']).read_bytes()
# Only read existing Mathlib artifacts; all 83 project modules get rebuilt here.
mathlib=PKG/'mathlib'
assert subprocess.check_output(['git','-C',str(mathlib),'rev-parse','HEAD'],text=True).strip()=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
assert not subprocess.check_output(['git','-C',str(mathlib),'status','--porcelain'],text=True).strip()
base=mathlib/'.lake/build/lib/lean/Mathlib'
for p in base.rglob('*'):
    if p.is_file():
        q=OUT/'Mathlib'/p.relative_to(base);q.parent.mkdir(parents=True,exist_ok=True);q.symlink_to(p)
libs=sorted(p/'.lake/build/lib/lean' for p in PKG.iterdir() if p.is_dir())
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT]+libs))}
log=(ROOT/'validation/INDEPENDENT_REPLAY.log').open('w')
log.write(subprocess.check_output([str(LEAN),'--version'],text=True))
log.write('LEAN_PATH='+env['LEAN_PATH']+'\n');log.flush()
records=[]
def build(name,path,cwd,trust0=False):
    dest=OUT/pathlib.Path(*name.split('.')).with_suffix('.olean')
    assert not dest.exists(),f'Already exists: {dest}'
    dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=[str(LEAN)]+(['--trust=0'] if trust0 else [])+['-o',str(dest),str(path)]
    t=time.time();p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
    log.write('$ '+' '.join(cmd)+'\n'+p.stdout+p.stderr);log.flush()
    records.append({'module':name,'source_sha256':sha(path.read_bytes()),'exit_code':p.returncode,'seconds':round(time.time()-t,3),'trust_zero':trust0})
    print(name,p.returncode,flush=True)
    assert p.returncode==0,p.stdout+p.stderr
for name in ['Mathlib.Algebra.MvPolynomial.Polynomial','Mathlib.Algebra.MvPolynomial.Funext']:
    src=mathlib/pathlib.Path(*name.split('.')).with_suffix('.lean')
    tracked=subprocess.check_output(['git','-C',str(mathlib),'show','HEAD:'+str(src.relative_to(mathlib))])
    assert src.read_bytes()==tracked
    build(name,src,mathlib)
seen=set();active=set()
def visit(name):
    if name not in items or name in seen:return
    assert name not in active,'Cyclic imports';active.add(name)
    for dep in items[name]['imports']:visit(dep)
    build(name,ROOT/'sources'/f'{name}.lean',ROOT/'sources')
    active.remove(name);seen.add(name)
visit(acq['root']);assert set(items)==seen
for name in ['OpenTermStandardness','FrozenCompilerMirror','PERInterface']:
    build(name,ROOT/'proofs'/f'{name}.lean',ROOT/'proofs')
# A final source snapshot is separately checked after the author's last update.
assert snapshot(PRIOR)==prior_before
result={'status':'PASS','source_closure_count':len(seen),'external_recompiled_count':2,'frozen_proof_files_unchanged':True,'frozen_package_unchanged':True,'pin_label':acq['pin'],'pin_membership_independently_verified':False,'mathlib_revision':'c44e0c8ee63ca166450922a373c7409c5d26b00b','lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'source_checks':checks,'build_records':records}
(ROOT/'validation/INDEPENDENT_SOURCE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS source closure and frozen proof rebuild',flush=True)
