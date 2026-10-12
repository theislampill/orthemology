#!/usr/bin/env python3
"""Hash-pinned fresh replay of the two all-Raw-context additions only."""
import hashlib,json,os,pathlib,re,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parent; W=R.parent
S=W/'hase-closed-scalar-instances-20261010'; T=W/'hase-church-structural-20261010'
E=W/'hase-effective-instance-assessment-20261010'
I=W/'hase-closed-church-identity-20261010'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
LIB=pathlib.Path(os.environ.get('SOURCE_LIB',str(W/'hase-full-per-review-20261010/fresh-lib')))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def verify_rows(base,rows):
    for row in rows: assert sha(base/row['path'])==row['sha256'],row['path']
def verify_manifest(base):
    rows=json.loads((base/'MANIFEST.json').read_text())['files']; verify_rows(base,rows); return len(rows)
verify_rows(W,json.loads((R/'INPUTS.json').read_text())['pinned_files'])
verify_manifest(R);verify_manifest(S);verify_manifest(T);verify_manifest(I)
verify_rows(W,json.loads((I/'INPUTS.json').read_text())['pinned_files'])
verify_rows(W,json.loads((T/'INPUTS.json').read_text())['pinned_files'])
x=json.loads((S/'INPUTS.json').read_text())
assert sha(LEAN)==x['lean_binary_sha256'],'Lean binary'
for key in ['receipts_and_manifests','frozen_source_files']: verify_rows(W,x[key])
for row in x['reused_objects']:
    assert sha(LIB/(row['module'].replace('.','/')+'.olean'))==row['sha256'],row['module']
for row in x['fresh_acquisitions']:
    a=json.loads((S/row['acquisition']).read_text());b=(S/row['path']).read_bytes()
    assert b==a['content'].encode();assert sha(S/row['path'])==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==a['sha']
def verify_replay(base):
    receipt=json.loads((base/'validation/FINAL_REPLAY.json').read_text());out=base/receipt['fresh_output']
    assert receipt['status']=='PASS'
    for row in receipt['modules']:
        assert sha(base/(row['module']+'.lean'))==row['source_sha256'],row['module']
        assert sha(out/(row['module']+'.olean'))==row['object_sha256'],row['module']
    return out,len(receipt['modules'])
scalar_lib,ns=verify_replay(S);structural_lib,nt=verify_replay(T)
nsource=verify_manifest(W/'hase-imported-compiler-transport-20261010')
ex=json.loads((E/'INPUTS.json').read_text())
verify_rows(W,ex['reused_objects']);verify_rows(W,ex['source_and_receipt_bindings'])
identity_lib,ni=verify_replay(I)
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
libs=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,identity_lib,structural_lib,scalar_lib,E/'validation',LIB]+libs))}
logs=[subprocess.check_output([str(LEAN),'--version'],text=True)];records=[]
for module in ['RawContextUniformity','RawContextControls']:
    source=R/(module+'.lean');code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),module
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(module+'.olean')),str(source)]
    result=subprocess.run(cmd,env=env,capture_output=True,text=True);output=result.stdout+result.stderr
    logs.append('$ '+' '.join(cmd)+'\n'+output)
    assert result.returncode==0,(module,output)
    assert not any(t in output for t in ['error:','warning:','sorryAx']),(module,output)
    axioms=[]
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',output,re.S):
        found=set(re.sub(r'\s+','',match).split(','));assert found<={'propext','Quot.sound','Classical.choice',''},(module,found);axioms.extend(found)
    records.append({'module':module,'source_sha256':sha(source),'object_sha256':sha(OUT/(module+'.olean')),'trust_zero':True,'exit_code':0,'axioms':sorted(set(axioms)-{''})})
    print(module,'PASS',flush=True)
(R/'validation/FINAL_REPLAY.log').write_text('\n'.join(logs))
(R/'validation/FINAL_REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(OUT.relative_to(R)),
 'verified_baseline_objects':len(x['reused_objects']),'verified_scalar_objects':ns,'verified_structural_objects':nt,
 'verified_identity_objects':ni,'verified_frozen_extractor_objects':1,'verified_imported_manifest_files':nsource,'modules':records,
 'scope':'Actual HasE source Church identity under all-Raw finite contexts, plus a single count uniform under arbitrary Raw substitutions and valuations. No arbitrary-context or arbitrary-type completeness, raw canonicity, strong normalization, universal scalar proof or #9 closure.'},indent=2)+'\n')
