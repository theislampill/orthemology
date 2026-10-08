#!/usr/bin/env python3
"""Check every source identity and the exact import-derived closure; no compilation."""
from pathlib import Path
import hashlib,json,re
p=Path(__file__).resolve().parent.parent
manifest=json.loads((p/'SOURCE_IDENTITIES.json').read_text())
rows=manifest['sources']; files={Path(r['path']).stem:r for r in rows}
for r in rows:
 b=(p/r['path']).read_bytes()
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
seen=set();order=[]
def visit(n):
 if n in ('Init','Lean'):return
 if n in seen:return
 assert n in files,n
 seen.add(n)
 for d in re.findall(r'^import\s+(\w+)\s*$',(p/files[n]['path']).read_text(),re.M):visit(d)
 order.append(n)
visit('BoundaryReadback')
assert set(files)==seen,'unexpected or missing source'
recorded=(p/'dependency-order.txt').read_text().splitlines()
assert set(recorded)==seen and len(recorded)==len(seen)
positions={n:i for i,n in enumerate(recorded)}
for n in recorded:
 for d in re.findall(r'^import\s+(\w+)\s*$',(p/files[n]['path']).read_text(),re.M):
  if d in positions:assert positions[d]<positions[n],(n,d)
accepted=json.loads((p/'ACCEPTED_INPUTS.json').read_text())['sources']
for r in accepted:assert files[Path(r['path']).stem]['sha256']==r['sha256']
print(json.dumps({'status':'PASS','sources':len(rows),'unchanged_accepted':len(accepted)}))
