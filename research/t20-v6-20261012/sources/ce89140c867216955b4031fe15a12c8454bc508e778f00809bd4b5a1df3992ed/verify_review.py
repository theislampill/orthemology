#!/usr/bin/env python3
"""Read-only hash verification of the frozen review and its declared inputs."""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--workspace-root',type=Path,default=HERE.parent);args=parser.parse_args();root=args.workspace_root.resolve()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
for f,d in r['review_files'].items():assert h(HERE/f)==d,f
for f,d in json.loads((HERE/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text()).items():assert h(root/f)==d,f
for f,d in json.loads((HERE/'PREDECESSOR_BINDINGS.json').read_text()).items():assert h(root/f)==d,f
print(json.dumps({'status':'PASS','review_files':len(r['review_files']),'author_and_predecessor_bytes_preserved':True,'mathematical_scope':'Frozen narrow H² certificate theorem, general drift and factored mobility only.'},indent=2))
