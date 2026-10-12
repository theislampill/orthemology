#!/usr/bin/env python3
"""Read-only predecessor verification and fresh trust-zero replay of this addition."""
import hashlib,json,os,pathlib,re,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
W=ROOT.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
LIB=pathlib.Path(os.environ.get('SOURCE_LIB',str(W/'hase-imported-compiler-transport-20261010/validation/replay-bxNUv6')))
EXPECTED={
 'FullPER.lean':'2a0d01d92923a22c4b41f512e4c4b3524ea1c630d13478176c5c20d63afa7638',
 'ScalarFusionCore.lean':'975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618',
 'Application.lean':'6d57b65eb3c4ffc8b7c34ba66beea17b7705265dcc4fdd11e66b14d0c5702bb9',
}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[]
for name in ['hase-open-term-standardness-20261010','hase-imported-compiler-transport-20261010','hase-raw-motive-boundary-20261010']:
    p=W/name/'MANIFEST.json';m=json.loads(p.read_text())
    for x in m['files']:
        assert sha(W/name/x['path'])==x['sha256'],(name,x['path'])
    inputs.append({'directory':name,'manifest_sha256':sha(p),'all_listed_files_verified':True})
for name,digest in EXPECTED.items():assert sha(ROOT/name)==digest,name
scalar=json.loads((ROOT/'SCALAR_ACQUISITION.json').read_text())
b=(ROOT/'ScalarFusionCore.lean').read_bytes()
assert scalar['source_bytes'].encode()==b
assert scalar['response']['sha']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert scalar['sha256']==hashlib.sha256(b).hexdigest()
assert scalar['request']['ref']=='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
(ROOT/'INPUTS.json').write_text(json.dumps({'predecessors':inputs,'scalar_acquisition_verified':True},indent=2)+'\n')
OUT=pathlib.Path(tempfile.mkdtemp(prefix='replay-',dir=ROOT/'validation'))
libs=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,LIB]+libs))}
records=[];logs=[subprocess.check_output([str(LEAN),'--version'],text=True)]
for name in ['FullPER','ScalarFusionCore','Application','DependencyAudit']:
    source=ROOT/(name+'.lean')
    if name!='DependencyAudit':
        clean=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
        clean=re.sub(r'--[^\n]*','',clean)
        assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean)
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(name+'.olean')),str(source)]
    p=subprocess.run(cmd,env=env,capture_output=True,text=True)
    log=p.stdout+p.stderr;logs+=['$ '+' '.join(cmd)+'\n'+log]
    assert p.returncode==0,(name,log)
    assert 'sorryAx' not in log and 'warning:' not in log and 'error:' not in log,(name,log)
    for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
        assert set(re.sub(r'\s+','',match).split(','))<={'propext','Classical.choice','Quot.sound',''}
    records.append({'module':name,'source_sha256':sha(source),'exit_code':p.returncode,'trust_zero':True})
    print(name,'PASS',flush=True)
(ROOT/'validation/FINAL_REPLAY.log').write_text('\n'.join(logs))
(ROOT/'validation/FINAL_REPLAY.json').write_text(json.dumps({'status':'PASS','fresh_output':str(OUT.relative_to(ROOT)),
 'source_library':str(LIB.relative_to(W)) if LIB.is_relative_to(W) else str(LIB),
 'scope':'New whole-HasE interpretation and exact application compiled against verified pinned source closure; not a second 83-module rebuild.',
 'inputs_verified':True,'modules':records},indent=2)+'\n')
