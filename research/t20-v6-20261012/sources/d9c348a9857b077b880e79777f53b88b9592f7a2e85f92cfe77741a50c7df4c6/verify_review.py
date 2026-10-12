#!/usr/bin/env python3
"""Verify review file digests and the frozen adjacent author snapshot."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
receipt=json.loads((H/'REVIEW_RECEIPT.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,digest in receipt['files'].items():assert sha(H/rel)==digest,rel
snapshot=json.loads((H/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text())
author=H.parent/snapshot['author_directory']
assert sha(author/'AUTHOR_RECEIPT.json')==snapshot['receipt_sha256']
for rel,digest in snapshot['frozen_files'].items():assert sha(author/rel)==digest,rel
sources=0
for rel,digest in snapshot['source_files'].items():
    p=H.parent/rel
    if p.exists():assert sha(p)==digest,rel;sources+=1
    assert sha(H/'isolated-replay'/rel)==digest,rel
print(json.dumps({'status':'PASS','review_files_verified':len(receipt['files']),'frozen_author_files_verified':len(snapshot['frozen_files'])+1,'live_source_files_verified':sources,'copied_source_files_verified':len(snapshot['source_files'])},sort_keys=True))
