#!/usr/bin/env python3
"""Read-only frozen-byte verification, portable with the author packet."""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,default=HERE.parent/'nonnegative-moving-gradient-escape-20261011');p.add_argument('--original-workspace',type=Path);a=p.parse_args()
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
for f,d in receipt['review_files'].items():assert h(HERE/f)==d,f
snapshot=json.loads((HERE/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text())
for f,d in snapshot.items():assert h(a.author_dir/f)==d,f
sources=json.loads((HERE/'ORIGINAL_SOURCE_BINDINGS.json').read_text())
for f,d in sources.items():
 assert h(HERE/'inputs'/f)==d,f
 if a.original_workspace:assert h(a.original_workspace/f)==d,f
print(json.dumps({'status':'PASS','review_files':len(receipt['review_files']),'frozen_author_files':len(snapshot),'packaged_sources':len(sources),'original_sources_checked':bool(a.original_workspace),'scope':'Nonnegative-SOS moving-gradient escape with decreasing loss and positive surviving mass; no contradiction to common-energy theorem.'},indent=2))
