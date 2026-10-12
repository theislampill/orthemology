#!/usr/bin/env python3
"""Independent exact-byte replay; inherited modules are verified and reused, never rebuilt."""
import hashlib, json, os, pathlib, re, subprocess, tempfile
R=pathlib.Path(__file__).resolve().parent; W=R.parent
C=W/'hase-raw-context-uniformity-20261010'
S=W/'hase-closed-scalar-instances-20261010'
T=W/'hase-church-structural-20261010'
I=W/'hase-closed-church-identity-20261010'
E=W/'hase-effective-instance-assessment-20261010'
BASE=W/'hase-full-per-review-20261010/fresh-lib'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(path,digest):
    actual=sha(path)
    assert actual==digest,(str(path),actual,digest)
    checks.append({'path':str(path.relative_to(W)),'sha256':actual})
def rows(base,rs):
    for r in rs: check(base/r['path'],r['sha256'])
def manifest(base):
    rs=json.loads((base/'MANIFEST.json').read_text())['files']; rows(base,rs); return len(rs)
for row in json.loads((R/'REVIEW_INPUTS.json').read_text())['frozen_files']:
    check(W/row['path'],row['sha256']); check(R/row['snapshot'],row['sha256'])
for package in [C,I,T,S]:
    manifest(package)
    config=json.loads((package/'INPUTS.json').read_text())
    if 'pinned_files' in config: rows(W,config['pinned_files'])
x=json.loads((S/'INPUTS.json').read_text())
check(LEAN,x['lean_binary_sha256'])
rows(W,x['receipts_and_manifests']); rows(W,x['frozen_source_files'])
for row in x['reused_objects']:
    check(BASE/(row['module'].replace('.','/')+'.olean'),row['sha256'])
for row in x['fresh_acquisitions']:
    doc=json.loads((S/row['acquisition']).read_text()); data=(S/row['path']).read_bytes()
    check(S/row['path'],row['sha256'])
    assert data==doc['content'].encode()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==doc['sha']
for package in ['hase-full-per-extension-20261010','hase-open-term-standardness-20261010','hase-imported-compiler-transport-20261010']:
    manifest(W/package)
extract=json.loads((E/'INPUTS.json').read_text())
rows(W,extract['reused_objects']); rows(W,extract['source_and_receipt_bindings'])
libs=[]; inherited=[]
for package in [I,T,S]:
    rec=json.loads((package/'validation/FINAL_REPLAY.json').read_text())
    assert rec['status']=='PASS'
    lib=package/rec['fresh_output']; libs.append(lib)
    for row in rec['modules']:
        check(package/(row['module']+'.lean'),row['source_sha256'])
        check(lib/(row['module']+'.olean'),row['object_sha256'])
        inherited.append(row['module'])
author=json.loads((C/'validation/FINAL_REPLAY.json').read_text())
assert author['status']=='PASS'
for row in author['modules']:
    check(C/(row['module']+'.lean'),row['source_sha256'])
    check(C/author['fresh_output']/(row['module']+'.olean'),row['object_sha256'])
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
packages=sorted((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,*libs,E/'validation',BASE,*packages]))}
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
assert 'version 4.19.0' in version
records=[]; log=[version]; negatives=[]
def run(source,expected=True):
    name=source.stem
    code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),name
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(name+'.olean')),str(source)]
    proc=subprocess.run(cmd,env=env,capture_output=True,text=True)
    output=proc.stdout+proc.stderr
    (OUT/(name+'.log')).write_text(output)
    log.append('$ '+' '.join(cmd)+'\n'+output)
    if not expected:
        assert proc.returncode!=0 and 'error:' in output,(name,output)
        negatives.append({'module':name,'source_sha256':sha(source),'expected_rejection':True,'exit_code':proc.returncode})
        print(name,'EXPECTED REJECTION',flush=True); return
    assert proc.returncode==0,(name,output)
    assert not any(s in output for s in ['error:','warning:','sorryAx']),(name,output)
    deps=set()
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output,re.S):
        deps.update(re.sub(r'\s+','',match).split(','))
    deps.discard('')
    assert deps <= {'propext','Classical.choice','Quot.sound'},(name,deps)
    records.append({'module':name,'source':str(source.relative_to(R)),'source_sha256':sha(source),'object_sha256':sha(OUT/(name+'.olean')),'trust_zero':True,'exit_code':0,'axioms':sorted(deps)})
    print(name,'PASS',flush=True)
for name in ['RawContextUniformity','RawContextControls']:
    run(R/'frozen'/(name+'.lean'))
if (R/'IndependentBoundaryChecks.lean').exists(): run(R/'IndependentBoundaryChecks.lean')
for file in sorted(R.glob('Reject*.lean')): run(file,False)
for row in json.loads((R/'REVIEW_INPUTS.json').read_text())['frozen_files']:
    check(W/row['path'],row['sha256'])
result={'status':'PASS','lean_version':version,'lean_binary_sha256':sha(LEAN),'fresh_output':str(OUT.relative_to(R)),'verified_baseline_objects':len(x['reused_objects']),'verified_inherited_addition_objects':inherited,'fresh_modules':records,'negative_controls':negatives,'all_hash_checks':checks,'baseline_rebuilt':False}
(R/'validation/REVIEW_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'validation/REVIEW_REPLAY.log').write_text('\n'.join(log))
