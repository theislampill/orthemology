#!/usr/bin/env python3
"""Record source-only dependency order and exact identities; never invoke Lean."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parent.parent
src=root/'sources'
files={p.stem:p for p in src.glob('*.lean')}
accepted={e['path']:e['sha256'] for e in json.loads((root/'ACCEPTED_INPUTS.json').read_text())['sources']}
seen=set();order=[]
def visit(n):
    if n in seen:return
    seen.add(n)
    for dep in re.findall(r'^import\s+(\w+)\s*$',files[n].read_text(),re.M):
        if dep in files:visit(dep)
    order.append(n)
for n in sorted(files):visit(n)
rows=[]
for n in order:
    p=files[n];relative='sources/'+p.name;data=p.read_bytes();digest=hashlib.sha256(data).hexdigest()
    if relative in accepted:assert digest==accepted[relative],relative
    rows.append({'path':relative,'bytes':len(data),'sha256':digest,'role':'accepted-unchanged' if relative in accepted else 'new-dependent-all'})
(root/'dependency-order.txt').write_text('\n'.join(order)+'\n')
(root/'SOURCE_IDENTITIES.json').write_text(json.dumps({'schema':'dependent-all-source-manifest-v1','sources':rows},indent=2)+'\n')
print(json.dumps({'source_modules':len(rows),'unchanged_accepted_modules':len(accepted),'new_modules':len(rows)-len(accepted)}))
