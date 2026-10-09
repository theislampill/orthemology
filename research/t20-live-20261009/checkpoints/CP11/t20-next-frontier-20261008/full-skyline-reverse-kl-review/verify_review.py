from pathlib import Path
import hashlib
import json

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
AUTHOR=ROOT/'full-skyline-reverse-kl'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['files']
for row in inputs:
    p=ROOT/row['path']
    assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
manifest=json.loads((BASE/'MANIFEST.json').read_text())['files']
for row in manifest:
    p=BASE/row['path']
    assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
for row in json.loads((AUTHOR/'MANIFEST.json').read_text())['artifacts']:
    p=AUTHOR/row['path']
    assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],row['path']
for row in json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())['sources']:
    p=AUTHOR/row['path']
    assert sha(p)==row['sha256'],row['path']
expected='4aa4bee754cf89284a327d4322f4d35a93314525da8aaa22e5d028754908e28a'
assert sha(AUTHOR/'RESULT.md')==expected
assert (AUTHOR/'controls.py').read_bytes()==(BASE/'author_replay/controls.py').read_bytes()
assert (AUTHOR/'CONTROL_RESULTS.json').read_bytes()==(BASE/'author_replay/CONTROL_RESULTS.json').read_bytes()
control=json.loads((BASE/'CONTROL_RESULTS.json').read_text())
assert control['status']=='PASS' and control['control_groups']==8 and control['author_code_imported'] is False
assert all(row['status']=='PASS' for row in control['controls'])
receipt=json.loads((BASE/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS' and receipt['review_sha256']==sha(BASE/'REVIEW.md')
assert receipt['accepted_author_result_sha256']==expected
result={'status':'PASS','source_files_current':len(inputs),'review_payload_files_current':len(manifest),'author_manifest_current':True,'author_dependencies_current':True,'author_replay_byte_identical':True,'independent_control_groups':8,'accepted_author_result_sha256':expected,'review_sha256':sha(BASE/'REVIEW.md'),'scope':'Written mathematical reverse-KL and scoped sequential lower-bound review only. Historical floor UNVERIFIED; no kernel assurance, integration, or closure.'}
(BASE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
