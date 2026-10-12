#!/usr/bin/env python3
"""Exact-pin research qualification of repaired P02 candidate sources; no adoption."""
import pathlib,json,re,subprocess,hashlib,os,time,shutil
ROOT=pathlib.Path(__file__).resolve().parent
ORIGINAL=pathlib.Path('private-locator:ed0f0021a1fad46fb3c4')
TOOL=pathlib.Path('private-locator:d97af50b47918e94879b')
MATHLIB=pathlib.Path('private-locator:41bd9f979012c8bbc235')
ENV={**os.environ,'PATH':str(TOOL)+':'+os.environ['PATH'],'LEAN_NUM_THREADS':'2'}
for k in ('LEAN_PATH','LEAN_SYSROOT'):ENV.pop(k,None)
R=ROOT/'receipts'/('qualification-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()))
R.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,args,cwd=ROOT):
    t=time.time();p=subprocess.run(args,cwd=cwd,env=ENV,capture_output=True)
    (R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr)
    (R/(label+'.command.json')).write_text(json.dumps({'command':args,'cwd':str(cwd),'started':t,'ended':time.time(),'exit':p.returncode,'stdout_sha256':sha(R/(label+'.stdout')),'stderr_sha256':sha(R/(label+'.stderr'))},indent=2))
    if p.returncode:raise RuntimeError(f'{label}: exit {p.returncode}: {p.stdout.decode()[-1000:]} {p.stderr.decode()[-1000:]}')
    return p.stdout.decode()+p.stderr.decode()
result={'status':'INCOMPLETE','canonical_adoption':False,'complete_obligations':False,'input_zip_sha256':'f90e399269ccd33c1df42b13c085f09d4e85ea6e2ecfd6f6ee9501de6671d0e2'}
try:
    assert run('lean-version',['lean','--version']).strip()=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
    assert run('lake-version',['lake','--version']).strip()=='Lake version 5.0.0-6caaee8 (Lean version 4.19.0)'
    deps=[]
    for p in json.loads((ORIGINAL/'formal/lake-manifest.json').read_text())['packages']:
        d=MATHLIB if p['name']=='mathlib' else MATHLIB/'.lake/packages'/p['name']
        assert run('pin-'+p['name'],['git','rev-parse','HEAD'],d).strip()==p['rev']
        assert not run('clean-'+p['name'],['git','status','--porcelain','--untracked-files=no'],d).strip()
        deps.append({'name':p['name'],'revision':p['rev']})
    inv=json.loads((ORIGINAL/'provenance/FORMAL_INVENTORY.json').read_text())['theorems']
    sourcepaths=sorted({pathlib.Path(t['source']).relative_to('formal') for t in inv})
    sourcehashes={str(p):sha(ROOT/p) for p in sourcepaths}
    headerchecks=[]
    for p in sourcepaths:
        a=(ORIGINAL/'formal'/p).read_text();b=(ROOT/p).read_text()
        pat=r'(?m)^theorem\s+([\w.]+)\b([\s\S]*?)\s*:='
        aa={n:re.sub(r'\s+','',h) for n,h in re.findall(pat,a)}
        bb={n:re.sub(r'\s+','',h) for n,h in re.findall(pat,b)}
        assert aa==bb, ('statement change',str(p))
        headerchecks.append({'source':str(p),'theorems':len(aa),'statement_headers_whitespace_equivalent':True,'original_sha256':sha(ORIGINAL/'formal'/p),'repaired_sha256':sha(ROOT/p)})
    (R/'SourceStatements.json').write_text(json.dumps(headerchecks,indent=2))
    build=ROOT/'.lake/build'
    if build.exists():shutil.move(str(build),str(R/'incremental-build-preseal'))
    began=time.time()
    modules=['P02.MeasureCore','P02.T300ThreeBit','P02','P02A2.MeasureCore','P02A2.Mixture','P02A2.Refinement','P02A2.FiniteLaw','P02A2.AllNParity','P02A2.Flow','P02A2.ObserverCore','P02A2.Fibres','P02A2.Observation','P02A2.Stationary','P02A2.SimplexStationary','P02A2.ParityBridge','P02A2.FiniteMeasureBridge','P02A2']
    for m in modules:
        run('fresh-build-'+m,['lake','build',m]); print('BUILT',m,flush=True)
    artifacts=[]
    for m in sorted({t['module'] for t in inv}):
        p=build/'lib/lean'/pathlib.Path(*m.split('.')).with_suffix('.olean')
        assert p.exists() and p.stat().st_size>0 and p.stat().st_mtime>=began-2, m
        artifacts.append({'module':m,'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
    audit=ROOT/'QualificationAudit.lean';audit.write_text('import P02\nimport P02A2\nset_option pp.universes true\n'+''.join('#check @'+t['declaration']+'\n#print axioms '+t['declaration']+'\n' for t in inv))
    out=run('all-types-and-axioms',['lake','env','lean',str(audit)])
    assert 'sorryAx' not in out and not re.search(r'(^|\n).*error:',out)
    seen={}
    for n,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):
        assert n not in seen
        seen[n]=[a.strip() for a in ax.split(',') if a.strip()]
    for n in re.findall(r"'([^']+)' does not depend on any axioms",out):
        assert n not in seen;seen[n]=[]
    names={t['declaration'] for t in inv};assert set(seen)==names
    for n,ax in seen.items():
        assert set(ax)<= {'propext','Classical.choice','Quot.sound'},(n,ax)
        assert any(s.lstrip('@').startswith(n+' :') or s.lstrip('@').startswith(n+'.{') for s in out.splitlines()),('missing type',n)
    assert sourcehashes=={str(p):sha(ROOT/p) for p in sourcepaths}
    result.update(status='REPAIRED_130_TARGETS_KERNEL_CHECKED',compiled_target_count=len(inv),new_attempt2_target_count=sum(t['origin']=='NEW_ATTEMPT_0002' for t in inv),source_statements_unchanged=True,dependencies=deps,source_sha256=sourcehashes,artifacts=artifacts,axioms=seen,lean_binary_sha256=sha(TOOL/'lean'),lake_binary_sha256=sha(TOOL/'lake'),audit_sha256=sha(audit),scope='Authored candidates only; explicit absent bridges remain open')
except Exception as ex:
    result.update(status='FAIL_CLOSED',failure=str(ex));raise
finally:
    (R/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'LATEST_QUALIFICATION.txt').write_text(str(R)+'\n')
print(json.dumps({'status':result['status'],'targets':result.get('compiled_target_count'),'receipt':str(R)},indent=2))
