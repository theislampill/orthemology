#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
REVIEW=HERE.parent
WORKSPACE=REVIEW.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
checks=0
for row in receipt['prior_receipts']:
    assert sha(REVIEW/row['path'])==row['sha256'],row['path']
    checks+=1
current=subprocess.run([sys.executable,str(REVIEW/'representation_addendum'/'verify_current_review.py')],capture_output=True,text=True,check=True)
current_result=json.loads(current.stdout);assert current_result['status']=='PASS'
checks+=1
for row in receipt['author_artifacts']:
    assert sha(WORKSPACE/row['path'])==row['sha256'],row['path']
    assert sha(HERE/row['snapshot'])==row['sha256'],row['snapshot']
    checks+=2
for row in receipt['review_artifacts']:
    assert sha(HERE/row['path'])==row['sha256'],row['path']
    checks+=1
for row in receipt['verified_source_bindings']:
    assert sha(WORKSPACE/row['path'])==row['sha256'],row['path']
    checks+=1
primary=Path(receipt['primary_pdf']['local_path'])
assert sha(primary)==receipt['primary_pdf']['sha256']
checks+=1
script=HERE/'author_replay'/'exact_controls.py'
run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,check=True)
assert run.stdout==(HERE/'AUTHOR_REPLAY.log').read_text()
assert (script.parent/'results'/'exact_controls.json').read_bytes()==(HERE/'author_snapshot'/'results'/'exact_controls.json').read_bytes()
result=json.loads((script.parent/'results'/'exact_controls.json').read_text())
assert result['families_passed']==12
checks+=3
output={'status':'PASS','supplement_checks':checks,'source_binding_checks':len(receipt['verified_source_bindings']),
        'primary_pdf_hash_verified':True,'author_families':12,'author_stdout_and_json_byte_identical':True,
        'currentness_aware_predecessor_verifier':current_result,
        'scope':'Supplement-only verification, preserving all prior sealed receipts and their separate scopes.'}
(HERE/'FINAL_VERIFICATION.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print(json.dumps(output,indent=2,sort_keys=True))
