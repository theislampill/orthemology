#!/usr/bin/env python3
"""Trust-zero replay of the source-instance addition; never rebuild prerequisites."""
import hashlib,json,os,pathlib,re,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
W=ROOT.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
LIB=pathlib.Path(os.environ.get('SOURCE_LIB',str(W/'hase-full-per-review-20261010/fresh-lib')))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for row in manifest['files']:
    assert sha(ROOT/row['path'])==row['sha256'],row['path']
inputs=json.loads((ROOT/'INPUTS.json').read_text())
for row in inputs['receipts_and_manifests']:
    assert sha(W/row['path'])==row['sha256'],row['path']
assert sha(LEAN)==inputs['lean_binary_sha256'],'Lean binary'
for row in inputs['reused_objects']:
    p=LIB/(row['module'].replace('.','/')+'.olean')
    assert sha(p)==row['sha256'],str(p)
for row in inputs['frozen_source_files']:
    assert sha(W/row['path'])==row['sha256'],row['path']
for row in inputs['fresh_acquisitions']:
    a=json.loads((ROOT/row['acquisition']).read_text())
    b=(ROOT/row['path']).read_bytes()
    assert b==a['content'].encode()
    assert sha(ROOT/row['path'])==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['sha']
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=ROOT/'validation'))
libs=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,LIB]+libs))}
logs=[subprocess.check_output([str(LEAN),'--version'],text=True)]
records=[]
for module in ['ClosedProofCanonicalisation','ClosedScalarInstances','Controls','DependencyAudit']:
    source=ROOT/(module+'.lean')
    if module!='DependencyAudit':
        code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
        code=re.sub(r'--[^\n]*','',code)
        assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),module
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(module+'.olean')),str(source)]
    result=subprocess.run(cmd,env=env,capture_output=True,text=True)
    output=result.stdout+result.stderr
    logs.append('$ '+' '.join(cmd)+'\n'+output)
    assert result.returncode==0,(module,output)
    assert not any(t in output for t in ['error:','warning:','sorryAx']),(module,output)
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output,re.S):
        assert set(re.sub(r'\s+','',match).split(','))<={'propext','Quot.sound','Classical.choice',''}
    records.append({'module':module,'source_sha256':sha(source),'object_sha256':sha(OUT/(module+'.olean')),'trust_zero':True,'exit_code':0})
    print(module,'PASS',flush=True)
(ROOT/'validation/FINAL_REPLAY.log').write_text('\n'.join(logs))
(ROOT/'validation/FINAL_REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(OUT.relative_to(ROOT)),
 'verified_reused_objects':len(inputs['reused_objects']),'modules':records,
 'scope':'Constructive closed-n source scalar instances; no universal bound-variable HasE target; prerequisite objects hash-verified and reused without rebuilding.'},indent=2)+'\n')
