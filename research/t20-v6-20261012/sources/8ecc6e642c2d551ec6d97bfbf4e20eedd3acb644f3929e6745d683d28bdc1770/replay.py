#!/usr/bin/env python3
"""Replay only the three new structural modules after verifying frozen prerequisites."""
import hashlib,json,os,pathlib,re,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parent
W=R.parent
S=W/'hase-closed-scalar-instances-20261010'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
LIB=pathlib.Path(os.environ.get('SOURCE_LIB',str(W/'hase-full-per-review-20261010/fresh-lib')))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((R/'INPUTS.json').read_text())
for row in inputs['pinned_files']:
    assert sha(W/row['path'])==row['sha256'],row['path']
for row in json.loads((R/'MANIFEST.json').read_text())['files']:
    assert sha(R/row['path'])==row['sha256'],row['path']
# Same checks as the closed-scalar replay, without recompiling that package.
for row in json.loads((S/'MANIFEST.json').read_text())['files']:
    assert sha(S/row['path'])==row['sha256'],row['path']
x=json.loads((S/'INPUTS.json').read_text())
assert sha(LEAN)==x['lean_binary_sha256'],'Lean binary'
for key in ['receipts_and_manifests','frozen_source_files']:
    for row in x[key]:
        assert sha(W/row['path'])==row['sha256'],row['path']
for row in x['reused_objects']:
    assert sha(LIB/(row['module'].replace('.','/')+'.olean'))==row['sha256'],row['module']
for row in x['fresh_acquisitions']:
    a=json.loads((S/row['acquisition']).read_text());b=(S/row['path']).read_bytes()
    assert b==a['content'].encode()
    assert sha(S/row['path'])==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['sha']
sr=json.loads((S/'validation/FINAL_REPLAY.json').read_text())
scalar_lib=S/sr['fresh_output']
for row in sr['modules']:
    assert sha(S/(row['module']+'.lean'))==row['source_sha256'],row['module']
    assert sha(scalar_lib/(row['module']+'.olean'))==row['object_sha256'],row['module']
# Verify the original finite structural source port against the pinned manifest.
original=W/'hase-imported-compiler-transport-20261010'
original_manifest=json.loads((original/'MANIFEST.json').read_text())
for row in original_manifest['files']:
    assert sha(original/row['path'])==row['sha256'],row['path']
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
libs=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,scalar_lib,LIB]+libs))}
logs=[subprocess.check_output([str(LEAN),'--version'],text=True)]
records=[]
for module in ['HasEStructuralBase','HasEStructuralRename','HasEClosedWeakening']:
    source=R/(module+'.lean')
    code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),module
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(module+'.olean')),str(source)]
    result=subprocess.run(cmd,env=env,capture_output=True,text=True)
    output=result.stdout+result.stderr
    logs.append('$ '+' '.join(cmd)+'\n'+output)
    assert result.returncode==0,(module,output)
    assert not any(t in output for t in ['error:','warning:','sorryAx']),(module,output)
    axioms=[]
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output,re.S):
        found=set(re.sub(r'\s+','',match).split(','))
        assert found<={'propext','Quot.sound',''},(module,found)
        axioms.extend(found)
    records.append({'module':module,'source_sha256':sha(source),'object_sha256':sha(OUT/(module+'.olean')),'trust_zero':True,'exit_code':0,'axioms':sorted(set(axioms)-{''})})
    print(module,'PASS',flush=True)
(R/'validation/FINAL_REPLAY.log').write_text('\n'.join(logs))
(R/'validation/FINAL_REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(OUT.relative_to(R)),
 'verified_reused_objects':len(x['reused_objects']),'verified_scalar_objects':len(sr['modules']),
 'verified_imported_manifest_files':len(original_manifest['files']),'modules':records,
 'scope':'Actual 20-rule HasE structural renaming and exact closed weakening. No baseline rebuild, protected repository change, integration, or closure.'},indent=2)+'\n')
