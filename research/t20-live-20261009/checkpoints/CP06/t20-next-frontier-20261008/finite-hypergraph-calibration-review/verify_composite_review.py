#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((HERE/'COMPOSITE_REVIEW_MANIFEST.json').read_text())
def verify_payloads():
    for row in manifest['payloads']:
        path=HERE/row['path']
        assert path.is_file() and sha(path)==row['sha256'],str(path)
        assert path.stat().st_size==row['bytes'],str(path)
verify_payloads()
run=subprocess.run([sys.executable,str(HERE/'packaging_addendum'/'verify_package.py')],capture_output=True,text=True,check=True)
chain=json.loads(run.stdout);assert chain['status']=='PASS'
verify_payloads()
result={'status':'PASS','payloads_verified_before_and_after_replay':len(manifest['payloads']),
        'sealed_receipts':len(manifest['receipt_chain']),'current_author_artifacts':len(manifest['current_author_artifacts']),
        'receipt_chain_verification':chain,
        'scope':'Complete preservation manifest and currentness-aware independent review evidence; no integration or closure authority.'}
(HERE/'COMPOSITE_FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
