#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
workspace=root.parents[2]
binding=json.loads((root/'SOURCE_BINDING.json').read_text())
for rec in binding['files']:
    p=workspace/rec['path']
    raw=p.read_bytes()
    if len(raw)!=rec['size'] or hashlib.sha256(raw).hexdigest()!=rec['sha256']:
        raise SystemExit(f'Frozen source mismatch: {rec["path"]}')
lean=Path('private-locator:cb50f30cfa35bdf3a0cf')
if hashlib.sha256(lean.read_bytes()).hexdigest()!=binding['lean_executable_sha256']:
    raise SystemExit('Compiler hash mismatch')
print(f'PASS: {len(binding["files"])} frozen source/review bytes and exact compiler hash.')
