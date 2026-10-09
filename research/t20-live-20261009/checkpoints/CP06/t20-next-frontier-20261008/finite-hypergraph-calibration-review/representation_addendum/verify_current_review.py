#!/usr/bin/env python3
"""Verify current accepted author bindings plus preserved older review payloads."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
REVIEW=HERE.parent
WORKSPACE=REVIEW.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
prior=REVIEW/'REVIEW_RECEIPT.json'
assert sha(prior)==receipt['prior_receipt_sha256']
prior_receipt=json.loads(prior.read_text())
unary=REVIEW/'unary_v2_addendum'/'REVIEW_RECEIPT.json'
assert sha(unary)==receipt['superseding_unary_receipt_sha256']
ur=json.loads(unary.read_text())
checks=2
for row in prior_receipt['review_artifacts']:
    assert sha(REVIEW/row['path'])==row['sha256'],row['path']
    checks+=1
for row in prior_receipt['author_artifacts']:
    assert sha(REVIEW/row['snapshot'])==row['sha256'],row['snapshot']
    current=ur['author_artifact']['sha256'] if row['path'].endswith('/ANCHORED_UNARY_COUNT.md') else row['sha256']
    assert sha(WORKSPACE/row['path'])==current,row['path']
    checks+=2
for row in prior_receipt['prerequisite_sources']:
    assert sha(WORKSPACE/row['path'])==row['sha256'],row['path']
    checks+=1
assert sha(unary.parent/ur['author_artifact']['snapshot'])==ur['author_artifact']['sha256']
assert sha(unary.parent/ur['review_artifact']['path'])==ur['review_artifact']['sha256']
checks+=2
for row in receipt['author_artifacts']:
    assert sha(WORKSPACE/row['path'])==row['sha256'],row['path']
    assert sha(HERE/row['snapshot'])==row['sha256'],row['snapshot']
    checks+=2
for row in receipt['review_artifacts']:
    assert sha(HERE/row['path'])==row['sha256'],row['path']
    checks+=1
results=[]
for script,log,want in [(REVIEW/'independent_controls.py',REVIEW/'INDEPENDENT_REPLAY.log',305),
                        (HERE/'independent_uniform_controls.py',HERE/'INDEPENDENT_REPLAY.log',251)]:
    run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,check=True)
    assert run.stdout==log.read_text()
    result=json.loads(run.stdout)
    summary=result.get('summary',result)
    assert summary['status']=='PASS' and summary['assertions']==want
    results.append(want)
    checks+=2
# Replays are permitted only because their deterministic outputs preserve all
# sealed payload bytes; verify that preservation explicitly after execution.
for row in prior_receipt['review_artifacts']:
    assert sha(REVIEW/row['path'])==row['sha256'],row['path']
    checks+=1
result={'status':'PASS','binding_and_replay_checks':checks,'original_assertions':results[0],
        'extension_assertions':results[1],'both_replays_byte_identical':True,
        'original_receipt_unchanged':True,'unary_supersession_applied':True,
        'scope':'Current author bindings, preserved predecessor review payloads, and two fresh independent replays.'}
(HERE/'FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
