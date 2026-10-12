import json,os,subprocess,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; W=ROOT.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
env={**os.environ,**json.loads((ROOT/'lean_env.json').read_text())}
records=[]
def run(label,cmd,cwd=None,expect_success=True):
    p=subprocess.run(list(map(str,cmd)),env=env,cwd=cwd or W,capture_output=True,text=True)
    out=p.stdout+p.stderr; (ROOT/'validation'/f'{label}.log').write_text(out)
    print(label,p.returncode,flush=True)
    if expect_success:assert p.returncode==0,(label,out)
    if expect_success:assert not any(s in out for s in ['error:','warning:','sorryAx']),(label,out)
    records.append({'label':label,'command':list(map(str,cmd)),'exit_code':p.returncode})
    return p
for mod in ['ScalarCertificates','LiteralSourceQ']:
    run(mod,[LEAN,'--trust=0','-o',ROOT/'fresh-lib'/f'{mod}.olean',ROOT/'sources'/f'{mod}.lean'])
p=run('SOURCE_REEXPORT',[LEAN,'--trust=0','--run',ROOT/'sources/SourceExport.lean'])
assert p.stdout.encode()==(ROOT/'sources/source_ast.json').read_bytes()
run('PYTHON_AUTHOR_TESTS',['python','-m','unittest','discover','-v'],ROOT/'sources')
original=(ROOT/'sources/ConcreteScalarCertificates.lean').read_bytes()
run('GENERATE_CERTIFICATES',['python',ROOT/'sources/generate_controls.py'])
assert original==(ROOT/'sources/ConcreteScalarCertificates.lean').read_bytes()
for mod in ['ConcreteScalarCertificates']:
    run(mod,[LEAN,'--trust=0','-o',ROOT/'fresh-lib'/f'{mod}.olean',ROOT/'sources'/f'{mod}.lean'])
(ROOT/'REPLAY_RECORDS.json').write_text(json.dumps(records,indent=2)+'\n')
