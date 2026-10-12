#!/usr/bin/env python3
"""Verify the compact checkpoint manifest, including unexpected-file detection."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={r['path'] for r in manifest['files']}|{'MANIFEST.json','MANIFEST.sha256'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
errors=[]
if actual!=expected:errors.append({'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)})
for r in manifest['files']:
 p=root/r['path']
 if not p.is_file():continue
 data=p.read_bytes()
 if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:errors.append(r['path'])
for line in (root/'MANIFEST.sha256').read_text().splitlines():
 h,path=line.split('  ',1)
 p=root/path
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:errors.append('SHA256:'+path)
print(json.dumps({'status':'PASS' if not errors else 'FAIL','payload_files':len(manifest['files']),'errors':errors},indent=2))
raise SystemExit(bool(errors))
