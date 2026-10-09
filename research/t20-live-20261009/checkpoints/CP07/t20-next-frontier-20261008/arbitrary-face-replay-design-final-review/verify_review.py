#!/usr/bin/env python3
"""Read-only exact-byte validation of this independent review receipt."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
verified=[]
for group in ('author_payloads','review_artifacts','directly_read_ancestry'):
    for row in receipt[group]:
        path=HERE/row['path']
        data=path.read_bytes()
        digest=hashlib.sha256(data).hexdigest()
        assert digest==row['sha256'],(group,row['path'],digest,row['sha256'])
        assert len(data)==row['bytes'],(group,row['path'],'size mismatch')
        verified.append({'group':group,'path':row['path'],'sha256':digest})
assert receipt['verdict']=='PASS'
print(json.dumps({'status':'PASS','count':len(verified),'scope':'Exact bindings only; the receipt does not hash itself or future author packaging.','verified':verified},indent=2))
