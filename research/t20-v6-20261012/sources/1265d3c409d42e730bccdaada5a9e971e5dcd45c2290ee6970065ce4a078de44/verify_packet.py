#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parents[1]
m=json.loads((b/'MANIFEST.json').read_text());expected={'MANIFEST.json'}
for r in m['files']:
 p=b/r['path'];assert p.resolve().is_relative_to(b) and p.is_file() and not p.is_symlink()
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'] and p.stat().st_size==r['bytes'],p
 assert r['path'] not in expected;expected.add(r['path'])
actual={str(p.relative_to(b)) for p in b.rglob('*') if p.is_file() or p.is_symlink()}
assert actual==expected,actual^expected
print('PASS',len(m['files']),'exact payload files')
