#!/usr/bin/env python3
"""Verify frozen inputs, then replay only disposable copies. Does not modify this package."""
from pathlib import Path
import hashlib, json, os, platform, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify_manifest():
    manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
    for item in manifest['files']:
        path=ROOT/item['path']
        if not path.is_file() or path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:
            raise RuntimeError('Frozen file mismatch: '+item['path'])
    return manifest

def verify_bindings(base,path,expected_count):
    obj=json.loads((base/path).read_text())
    items=[item for value in obj.values() if isinstance(value,list) for item in value
           if isinstance(item,dict) and 'path' in item and 'sha256' in item]
    if len(items)!=expected_count:
        raise RuntimeError('Unexpected binding count: '+path)
    for item in items:
        target=base/item['path']
        if sha(target)!=item['sha256']:
            raise RuntimeError('Bound input mismatch: '+item['path'])
        if 'bytes' in item and target.stat().st_size!=item['bytes']:
            raise RuntimeError('Bound byte count mismatch: '+item['path'])
    return len(items)

manifest=verify_manifest()
before={i['path']:sha(ROOT/i['path']) for i in manifest['files']}
bindings={}
for path,count in [
    ('audit-continuation-transport-20261010/INPUT_BINDINGS.json',8),
    ('posterior-continuation-independent-review-20261010/INPUT_BINDINGS.json',3),
    ('posterior-continuation-independent-review-20261010/FINAL_PACKET_BINDINGS.json',24),
]:
    bindings[path]=verify_bindings(ROOT,path,count)
import sympy
runs=[]
with tempfile.TemporaryDirectory(prefix='audit-continuation-replay-') as tmp:
    work=Path(tmp)/'work'
    shutil.copytree(ROOT,work)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    specs=[
      ('audit-continuation-transport-20261010/verify.py','audit-continuation-transport-20261010/CONTROL_RESULTS.json',False),
      ('audit-aware-correction-root-20261010/check_binary_audit_quotient.py','audit-aware-correction-root-20261010/BINARY_QUOTIENT_CHECKS.json',True),
      ('posterior-continuation-independent-review-20261010/independent_checks.py','posterior-continuation-independent-review-20261010/INDEPENDENT_RESULTS.json',False),
      ('posterior-continuation-independent-review-20261010/final_transport_checks.py','posterior-continuation-independent-review-20261010/FINAL_TRANSPORT_RESULTS.json',False),
    ]
    for script,expected,stdout_is_file in specs:
        cp=subprocess.run([sys.executable,str(work/script)],cwd=work,env=env,text=True,capture_output=True)
        if cp.returncode:
            raise RuntimeError(f'Replay failed: {script}\n{cp.stdout}\n{cp.stderr}')
        actual=json.loads(cp.stdout)
        want=json.loads((ROOT/expected).read_text())
        if actual!=want:
            raise RuntimeError('Exact result mismatch: '+script)
        actual_bytes=cp.stdout.encode() if stdout_is_file else (work/expected).read_bytes()
        if actual_bytes!=(ROOT/expected).read_bytes():
            raise RuntimeError('Result byte mismatch: '+script)
        runs.append({
            'script':script,'exit_code':cp.returncode,'expected_json':expected,
            'json_equal':True,'result_byte_equal':True,
            'stdout_sha256':hashlib.sha256(cp.stdout.encode()).hexdigest(),'stderr':cp.stderr,
        })
verify_manifest()
after={i['path']:sha(ROOT/i['path']) for i in manifest['files']}
if before!=after:
    raise RuntimeError('Frozen package changed during replay')
print(json.dumps({
    'status':'PASS',
    'scope':'Exact scratch-package replay; no kernel or field-novelty or programme-closure claim.',
    'package_manifest_sha256':sha(ROOT/'PACKAGE_MANIFEST.json'),
    'verified_frozen_files':len(before),'bound_input_counts':bindings,
    'python_version':platform.python_version(),'sympy_version':sympy.__version__,
    'runs':runs,'frozen_inputs_unchanged':True,
},indent=2))
