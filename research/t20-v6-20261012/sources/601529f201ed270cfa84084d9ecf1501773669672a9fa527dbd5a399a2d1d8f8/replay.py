#!/usr/bin/env python3
"""Replay the frozen inquiry-value result in a disposable copy only."""
from pathlib import Path
import hashlib,json,os,platform,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_manifest():
    obj=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
    for item in obj['files']:
        p=ROOT/item['path']
        if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            raise RuntimeError('Frozen file mismatch: '+item['path'])
    return obj
m=check_manifest();before={x['path']:sha(ROOT/x['path']) for x in m['files']}
b=json.loads((ROOT/'inquiry-value-independent-review-20261010/BINDINGS.json').read_text())
items=[x for val in b.values() if isinstance(val,list) for x in val
       if isinstance(x,dict) and 'path' in x and 'sha256' in x]
if len(items)!=13:raise RuntimeError('Unexpected number of exact bindings')
for item in items:
    p=ROOT/item['path']
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
        raise RuntimeError('Review binding mismatch: '+item['path'])
note=ROOT/'posterior-inquiry-value-20261010/RESULT.md'
if sha(note)!='5f6f84b1af7e5049139a381142a791eb7aeebdb57ebf9095e14fa49cfc652fcf':
    raise RuntimeError('Root note is not the reviewed final snapshot')
pending='An independent review is pending when this note is first written.'
if pending not in note.read_text():raise RuntimeError('Historical sentence was changed')
import sympy
runs=[]
with tempfile.TemporaryDirectory(prefix='inquiry-value-replay-') as td:
    work=Path(td)/'work';shutil.copytree(ROOT,work)
    for script,result in [
        ('posterior-inquiry-value-20261010/verify.py','posterior-inquiry-value-20261010/CONTROL_RESULTS.json'),
        ('inquiry-value-independent-review-20261010/check_inquiry_value.py','inquiry-value-independent-review-20261010/RESULTS.json'),
    ]:
        cp=subprocess.run([sys.executable,str(work/script)],cwd=work,text=True,capture_output=True,
                          env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        if cp.returncode:raise RuntimeError(f'Replay failed {script}\n{cp.stdout}\n{cp.stderr}')
        if json.loads(cp.stdout)!=json.loads((ROOT/result).read_text()):
            raise RuntimeError('JSON result mismatch: '+script)
        if (work/result).read_bytes()!=(ROOT/result).read_bytes():
            raise RuntimeError('Result byte mismatch: '+script)
        runs.append({'script':script,'exit_code':0,'expected_result':result,'json_equal':True,
                     'result_byte_equal':True,'stdout_sha256':hashlib.sha256(cp.stdout.encode()).hexdigest(),
                     'stderr':cp.stderr})
check_manifest();after={x['path']:sha(ROOT/x['path']) for x in m['files']}
if before!=after:raise RuntimeError('Frozen package changed during replay')
print(json.dumps({'status':'PASS','scope':'Preservation and exact replay only, no new research campaign, kernel, field-novelty or closure claim.',
    'package_manifest_sha256':sha(ROOT/'PACKAGE_MANIFEST.json'),'verified_frozen_files':len(before),
    'review_binding_entries_verified':len(items),'historical_pending_sentence_preserved':True,
    'subsequent_review_sha256':sha(ROOT/'inquiry-value-independent-review-20261010/REVIEW.md'),
    'python_version':platform.python_version(),'sympy_version':sympy.__version__,
    'runs':runs,'frozen_inputs_unchanged':True},indent=2))
