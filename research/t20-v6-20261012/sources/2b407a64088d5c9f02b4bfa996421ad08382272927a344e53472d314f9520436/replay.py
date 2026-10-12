#!/usr/bin/env python3
"""Verify this bounded archive and replay exact controls without original inputs."""
import argparse, hashlib, json, pathlib, subprocess, sys

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,o): p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
p=argparse.ArgumentParser(); p.add_argument('--output',required=True); args=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
out=pathlib.Path(args.output).resolve()
assert not out.exists(), 'Replay output must be new'
assert root not in out.parents, 'Replay output must be outside archived payload'
manifest=json.loads((root/'MANIFEST.json').read_text())
def verify_payload():
    found={str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}
    assert found==set(manifest)|{'MANIFEST.json'}, 'Unexpected or missing payload file'
    for name,info in manifest.items():
        f=root/name
        assert digest(f)==info['sha256'] and f.stat().st_size==info['bytes'], name
verify_payload()
evidence=root/'evidence'
author=evidence/'continuous-signed-finite-rank-20261010'
review=evidence/'continuous-signed-finite-rank-review-20261010'
receipt=json.loads((review/'REVIEW_RECEIPT.json').read_text())
exclusions=json.loads((root/'EXCLUDED_SOURCE_BODIES.json').read_text())
checked=0; omitted={}
for group in ['author_files','review_files','retained_inputs']:
    for name,expected in receipt[group].items():
        f=evidence/name
        if f.exists():
            assert digest(f)==expected,(group,name)
            checked+=1
        else:
            assert name in exclusions and exclusions[name]['sha256']==expected,(group,name)
            omitted[name]=expected
assert digest(author/'RESULT.md')==receipt['reviewed_result_sha256']
for name,expected in json.loads((author/'INPUT_BINDINGS.json').read_text()).items():
    f=evidence/name
    assert (digest(f) if f.exists() else exclusions[name]['sha256'])==expected,name
out.mkdir(parents=True)
results={}
for label,code,expected in [('author',author/'verify.py',author/'verification.txt'),('independent',review/'check_review.py',review/'INDEPENDENT_CONTROLS.json')]:
    run=subprocess.run([sys.executable,str(code)],cwd=out,capture_output=True,check=True)
    (out/(label+'.stdout')).write_bytes(run.stdout)
    (out/(label+'.stderr')).write_bytes(run.stderr)
    assert run.stdout==expected.read_bytes(),label+' replay differs'
    results[label]={'returncode':run.returncode,'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),'byte_identical':True}
assert (author/'verification.txt').read_bytes()==(review/'AUTHOR_REPLAY.txt').read_bytes()
verify_payload()
summary={'status':'PASS','payload_files_verified':len(manifest),'review_bindings_verified':checked,'excluded_source_body_bindings_not_replayed':omitted,'reviewed_result_sha256':digest(author/'RESULT.md'),'review_receipt_sha256':digest(review/'REVIEW_RECEIPT.json'),'controls':results,'payload_unchanged':True,'python':sys.version,'sympy':__import__('sympy').__version__,'scope':'Ordinary evidence and exact controls; no universal finite-enumeration proof, formal kernel, source rereading, protected edits, integration, upload, or T20 closure.'}
dump(out/'REPLAY_RECEIPT.json',summary)
print(json.dumps(summary,indent=2))
