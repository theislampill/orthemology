#!/usr/bin/env python3
"""Independent bounded replay. Never writes to any author or predecessor path."""
import hashlib,json,os,pathlib,re,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parent; W=R.parent
C=W/'hase-structured-context-uniformity-20261010'
S=W/'hase-closed-scalar-instances-20261010'; T=W/'hase-church-structural-20261010'
I=W/'hase-closed-church-identity-20261010'; RAW=W/'hase-raw-context-uniformity-20261010'
E=W/'hase-effective-instance-assessment-20261010'
BASE=W/'hase-full-per-review-20261010/fresh-lib'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(path,digest):
    got=sha(path); assert got==digest,(str(path),got,digest)
    checks.append({'path':str(path.relative_to(W)),'sha256':got})
def rows(base,rs):
    for row in rs:check(base/row['path'],row['sha256'])
def manifest(base):
    rs=json.loads((base/'MANIFEST.json').read_text())['files']; rows(base,rs);return len(rs)
config=json.loads((R/'REVIEW_INPUTS.json').read_text())
def frozen_check():
    for row in config['frozen_files']:
        check(W/row['path'],row['sha256']);check(R/row['snapshot'],row['sha256'])
    rows(W,config['protected_predecessors'])
frozen_check();check(C/'MANIFEST.json',config['frozen_manifest_sha256'])
if (R/'MANIFEST.json').exists():manifest(R)
for package in [C,RAW,I,T,S]:
    manifest(package)
    inputs=json.loads((package/'INPUTS.json').read_text())
    if 'pinned_files' in inputs:rows(W,inputs['pinned_files'])
rows(W,json.loads((C/'INPUTS.json').read_text())['retained_objects'])
x=json.loads((S/'INPUTS.json').read_text());check(LEAN,x['lean_binary_sha256'])
for key in ['receipts_and_manifests','frozen_source_files']:rows(W,x[key])
for row in x['reused_objects']:check(BASE/(row['module'].replace('.','/')+'.olean'),row['sha256'])
for row in x['fresh_acquisitions']:
    doc=json.loads((S/row['acquisition']).read_text()); data=(S/row['path']).read_bytes()
    check(S/row['path'],row['sha256']);assert data==doc['content'].encode()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==doc['sha']
for name in ['hase-full-per-extension-20261010','hase-open-term-standardness-20261010','hase-imported-compiler-transport-20261010']:
    manifest(W/name)
e=json.loads((E/'INPUTS.json').read_text())
rows(W,e['reused_objects']);rows(W,e['source_and_receipt_bindings'])
libs=[];inherited=[]
for package in [RAW,I,T,S]:
    receipt=json.loads((package/'validation/FINAL_REPLAY.json').read_text());assert receipt['status']=='PASS'
    lib=package/receipt['fresh_output'];libs.append(lib)
    for row in receipt['modules']:
        check(package/(row['module']+'.lean'),row['source_sha256'])
        check(lib/(row['module']+'.olean'),row['object_sha256']);inherited.append(row['module'])
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
packages=sorted((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,*libs,E/'validation',BASE,*packages]))}
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip();assert 'version 4.19.0' in version
records=[];negatives=[];logs=[version]
def run(source,expected=True):
    name=source.stem
    code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S);code=re.sub(r'--[^\n]*','',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),name
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(name+'.olean')),str(source)]
    proc=subprocess.run(cmd,env=env,capture_output=True,text=True); output=proc.stdout+proc.stderr
    (OUT/(name+'.log')).write_text(output);logs.append('$ '+' '.join(cmd)+'\n'+output)
    if not expected:
        assert proc.returncode!=0 and 'error:' in output,(name,output)
        negatives.append({'module':name,'source_sha256':sha(source),'expected_rejection':True,'exit_code':proc.returncode,'log_sha256':sha(OUT/(name+'.log'))})
        print(name,'EXPECTED REJECTION',flush=True);return
    assert proc.returncode==0,(name,output)
    assert not any(s in output for s in ['error:','warning:','sorryAx']),(name,output)
    deps=set()
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output,re.S):deps.update(re.sub(r'\s+','',match).split(','))
    deps.discard('');assert deps<={'propext','Classical.choice','Quot.sound'},(name,deps)
    records.append({'module':name,'source':str(source.relative_to(R)),'source_sha256':sha(source),'object_sha256':sha(OUT/(name+'.olean')),'trust_zero':True,'exit_code':0,'axioms':sorted(deps),'log_sha256':sha(OUT/(name+'.log'))})
    print(name,'PASS',flush=True)
for name in ['StructuredContextUniformity','StructuredContextControls']:run(R/'frozen'/(name+'.lean'))
if (R/'IndependentStructuredChecks.lean').exists():run(R/'IndependentStructuredChecks.lean')
for file in sorted(R.glob('Reject*.lean')):run(file,False)
frozen_check()
# Recheck every transitively verified input, not only the directly frozen packet.
for row in list(checks):assert sha(W/row['path'])==row['sha256'],row['path']
result={'status':'PASS','lean_version':version,'lean_binary_sha256':sha(LEAN),'fresh_output':str(OUT.relative_to(R)),'verified_baseline_objects':len(x['reused_objects']),'verified_inherited_addition_objects':inherited,'fresh_modules':records,'negative_controls':negatives,'all_hash_checks':checks,'baseline_rebuilt':False,'originals_and_predecessors_unchanged':True,'scope':'Opaque-context source identity and arbitrary-context observation-to-identity only. Neither original graph bridge, universal W judgment, nor its negation is established.'}
(OUT/'REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'REPLAY.log').write_text('\n'.join(logs))
(R/'validation/REVIEW_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'validation/REVIEW_REPLAY.log').write_text('\n'.join(logs))
