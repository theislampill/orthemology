#!/usr/bin/env python3
"""Verify sealed bindings and replay copies without changing source artifacts."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
BASE=HERE.parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(mapping,root):
    for name,sha in mapping.items():
        p=root/name
        assert p.is_file(),f'missing bound file: {p}'
        assert digest(p)==sha,f'changed bound file: {p}'

manifest=json.loads((HERE/'REVIEW_MANIFEST.json').read_text())
bindings=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
prior=json.loads((HERE/'PRIOR_SHA256.json').read_text())
check(manifest['files'],HERE);check(bindings['files'],BASE);check(prior,BASE)

with tempfile.TemporaryDirectory(prefix='verification-replay-',dir=HERE) as tmp:
    root=Path(tmp)
    runs=[
        ('independent',HERE/'independent_controls.py','INDEPENDENT_CONTROLS.json',HERE/'INDEPENDENT_CONTROLS.json'),
        ('conditional',HERE/'conditional_cover_controls.py','CONDITIONAL_COVER_CONTROLS.json',HERE/'CONDITIONAL_COVER_CONTROLS.json'),
        ('discovery',HERE/'cover_discovery_controls.py','COVER_DISCOVERY_CONTROLS.json',HERE/'COVER_DISCOVERY_CONTROLS.json'),
        ('author',BASE/'bounded-interaction-detection'/'exact_controls.py','results/exact_controls.json',BASE/'bounded-interaction-detection'/'results'/'exact_controls.json'),
    ]
    for name,source,output,expected in runs:
        work=root/name;work.mkdir();(work/'results').mkdir()
        script=work/source.name;shutil.copyfile(source,script)
        if name=='independent':shutil.copyfile(HERE/'PRIOR_SHA256.json',work/'PRIOR_SHA256.json')
        env=dict(os.environ);env['PRIOR_BINDING_BASE']=str(BASE)
        proc=subprocess.run([sys.executable,str(script)],cwd=work,env=env,check=True,capture_output=True,text=True)
        assert (work/output).read_bytes()==expected.read_bytes(),f'{name} replay differs'
        assert json.loads((work/output).read_text())['status']=='PASS'

check(manifest['files'],HERE);check(bindings['files'],BASE);check(prior,BASE)
result={'status':'PASS','bound_review_files':len(manifest['files']),'bound_source_files':len(bindings['files']),'unchanged_prior_files':len(prior),'copied_replays':['independent','conditional','discovery','author'],'source_files_executed_in_place':False}
(HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
