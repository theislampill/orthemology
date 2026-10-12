#!/usr/bin/env python3
"""Fresh trust-zero replay of the concrete whole-source countermodel addition.
Existing pinned baseline objects are reused read-only; no baseline rebuild.
"""
import hashlib,json,os,pathlib,re,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
W=ROOT.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
BASE=W/'hase-imported-compiler-transport-20261010/validation/replay-bxNUv6'
SCALAR=W/'hase-full-per-extension-20261010/validation'
SOURCES=[
 ('CaseOperational','homogeneous-per-model-20261010/operational/CaseOperational.lean','5575a1d8e69c8f857b0b15dc6f1358a4c3f44bd54a47bf528cf3295ae59c3708'),
 ('HomogeneousPER','homogeneous-per-closure-20261010/HomogeneousPER.lean','f06b84a8dd088a9cf82ab99dff2d476023ab50427fee0245ef5d210a8ec57f0f'),
 ('ConcreteUniverse','homogeneous-per-closure-20261010/ConcreteUniverse.lean','8fb9848611f88b2f2555a15469eb59c3ff98e9a831f92f701cdb0091dc2d6904'),
 ('SourceTransport','homogeneous-henkin-source-soundness-20261010/SourceTransport.lean','3e3e4bcbea2c19c58df20cb7f83c7e5e9a41e7a4c9dcfab6085e09fc2025987a'),
 ('HenkinSoundness','homogeneous-henkin-source-soundness-20261010/HenkinSoundness.lean','d0c9bc80e4014f2dc7ba685af95690b96ea02e166209101966e9a9e797fbcf5f'),
 ('LiteralCounterexample','homogeneous-per-model-20261010/LiteralCounterexample.lean','af219bfec917e3f083b093ffc9d1e07f54fec5d72e8f8a274915eaa030397c0c'),
 ('OriginalWNoninhabitation','homogeneous-per-model-20261010/OriginalWNoninhabitation.lean','b4c46829c268c37860114d5d99c08a2bc099373133a591664503ef07d8b75628'),
 ('OriginalIdentityNoninhabitation','homogeneous-per-model-20261010/OriginalIdentityNoninhabitation.lean','5ee0cbdab27fa18866d5e7b1b6b13131bbdb649b5bacab839a67c46e11619d08')]
PINS={
 'identity-frontier-inspection-20261009/ScalarFusionCore.lean':'975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618',
 'hase-full-per-extension-20261010/ScalarFusionCore.lean':'975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618',
 'identity-frontier-inspection-20261009/ExtensionalRepairSyntax.lean':'dc4415c2e367c957589f1162243804cce1955f28894355a0d73a4a0b7ef66d9f',
 'hase-full-per-extension-20261010/FullPER.lean':'2a0d01d92923a22c4b41f512e4c4b3524ea1c630d13478176c5c20d63afa7638',
 'hase-imported-compiler-transport-20261010/proofs/ImportedCompilerTransport.lean':'448e9f950a1c51a9267ca04671fe6ade3377a485692621bd8252925ae02fbdbc'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in PINS.items():assert sha(W/p)==h,p
for name,p,h in SOURCES:
    assert sha(W/p)==h,p
    s=re.sub(r'/\-.*?\-/','',(W/p).read_text(),flags=re.S)
    s=re.sub(r'--[^\n]*','',s)
    assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',s),p
(ROOT/'validation').mkdir(exist_ok=True)
OUT=pathlib.Path(tempfile.mkdtemp(prefix='fresh-',dir=ROOT/'validation'))
libs=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,[OUT,SCALAR,BASE]+libs))}
logs=[subprocess.check_output([str(LEAN),'--version'],text=True)]
records=[]
for name,p,h in SOURCES:
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/(name+'.olean')),str(W/p)]
    proc=subprocess.run(cmd,env=env,capture_output=True,text=True)
    log=proc.stdout+proc.stderr
    (OUT/(name+'.log')).write_text(log)
    logs.append('$ '+' '.join(cmd)+'\n'+log)
    assert proc.returncode==0,(name,log)
    assert 'sorryAx' not in log and 'error:' not in log,(name,log)
    warnings=re.findall(r'warning: ([^\n]*)',log)
    assert not warnings or (name=='HenkinSoundness' and warnings==['unused variable `hp`']),(name,warnings)
    for m in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
        assert set(re.sub(r'\s+','',m).split(','))<={'propext','Classical.choice','Quot.sound',''},(name,m)
    records.append({'module':name,'source':p,'source_sha256':h,'object_sha256':sha(OUT/(name+'.olean')),'exit_code':0,'trust_zero':True,'warnings':warnings})
    print(name,'PASS',flush=True)
receipt={'status':'PASS','fresh_output':str(OUT.relative_to(W)),
 'scope':'Fresh replay of eight new concrete countermodel modules; pinned original baseline objects reused read-only, not rebuilt.',
 'source_pins':PINS,'modules':records,
 'main_theorem':'HomogeneousOriginalW.original_W_uninhabited',
 'conclusion':'For every original Poly p, not original HasE [] p (original W original redundantExpr.closed).',
 'identity_corollary':'HomogeneousOriginalIdentity.literal_original_identity_uninhabited',
 'original_scalar_object_sha256':sha(SCALAR/'ScalarFusionCore.olean'),
 'baseline_ImportedCompilerTransport_object_sha256':sha(BASE/'ImportedCompilerTransport.olean')}
(OUT/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
(ROOT/'validation/REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
(ROOT/'validation/REPLAY.log').write_text('\n'.join(logs))
print('Receipt:',OUT/'REPLAY.json')
