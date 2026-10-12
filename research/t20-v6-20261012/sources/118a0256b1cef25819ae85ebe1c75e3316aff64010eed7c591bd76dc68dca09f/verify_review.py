#!/usr/bin/env python3
"""Verify this independent review's sealed files and, when present, live targets."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent; W=R.parent
receipt=json.loads((R/'REVIEW_RECEIPT.json').read_text())
count=0
for row in receipt['review_files']:
 p=R/row['path']; data=p.read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],p
 count+=1
live=0
for row in json.loads((R/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text()):
 p=W/row['author']
 if p.exists():
  assert p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
  live+=1
print(json.dumps({'status':'PASS','sealed_review_files':count,'unchanged_live_author_files':live},indent=2))
