from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['files']
for row in inputs:
 p=ROOT/row['path']
 assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'], row['path']
manifest=json.loads((BASE/'MANIFEST.json').read_text())['files']
for row in manifest:
 p=BASE/row['path']
 assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'], row['path']
source=ROOT/'skyline-likelihood-score'
assert sha(source/'RESULT.md')=='ba6345d03e5fe9d2735f221ee45f5ee6b6f05508ce4d96f8ba9a86ceb3da5b5f'
for line in (source/'SHA256SUMS').read_text().splitlines():
 expected,name=line.split(maxsplit=1)
 assert sha(ROOT/name)==expected
assert (source/'CONTROL_RESULTS.json').read_bytes()==(BASE/'author_replay/CONTROL_RESULTS.json').read_bytes()
assert (source/'controls.py').read_bytes()==(BASE/'author_replay/controls.py').read_bytes()
r=json.loads((BASE/'CONTROL_RESULTS.json').read_text())
assert r['status']=='PASS' and r['admissible_case_count']==468
assert len(r['wrong_candidate_controls'])==3 and all(v['rejected_by_constant_40'] for v in r['wrong_candidate_controls'])
receipt=json.loads((BASE/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS' and receipt['review_sha256']==sha(BASE/'REVIEW.md')
assert receipt['accepted_author_result_sha256']==sha(source/'RESULT.md')
result={'status':'PASS','source_files_current':len(inputs),'review_payload_files_current':len(manifest),'author_manifest_current':True,'author_replay_byte_identical':True,'independent_admissible_cases':468,'wrong_candidate_controls_rejected':3,'accepted_author_result_sha256':sha(source/'RESULT.md'),'review_sha256':sha(BASE/'REVIEW.md'),'scope':'Localized written mathematical proof and deterministic controls only; no kernel assurance, statistical information rate, protected integration, floor certification, or closure.'}
(BASE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
