#!/usr/bin/env python3
"""Verify the bounded review payload and replay independent controls."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
bindings=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
checks=0
for row in bindings['author_artifacts']:
    live=WORKSPACE/row['path'];snap=HERE/row['snapshot']
    assert sha(live)==row['sha256'],live
    assert sha(snap)==row['sha256'],snap
    assert len(live.read_bytes())==row['bytes']
    checks+=3
for row in bindings['prerequisite_sources']:
    path=WORKSPACE/row['path']
    assert sha(path)==row['sha256'],path
    checks+=1
for row in receipt['review_artifacts']:
    path=HERE/row['path']
    assert sha(path)==row['sha256'],path
    checks+=1
replay=subprocess.run([sys.executable,str(HERE/'independent_controls.py')],capture_output=True,text=True,check=True)
assert replay.stdout==(HERE/'INDEPENDENT_REPLAY.log').read_text()
results=json.loads(replay.stdout)
assert results['status']=='PASS' and results['assertions']==305
assert results==receipt['independent_controls']
checks+=3
result={'status':'PASS','binding_and_replay_checks':checks,'author_artifacts':len(bindings['author_artifacts']),
        'prerequisite_sources':len(bindings['prerequisite_sources']), 'independent_assertions':results['assertions'],
        'replay_byte_identical':True,'scope':'Digest integrity and fresh independent replay; proof verdict is REVIEW.md.'}
(HERE/'FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
