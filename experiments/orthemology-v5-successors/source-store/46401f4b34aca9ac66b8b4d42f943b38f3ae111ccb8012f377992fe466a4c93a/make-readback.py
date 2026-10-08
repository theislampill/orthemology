#!/usr/bin/env python3
"""Generate explicit public declaration readback and the inherited transitive gate."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parent.parent
modules=sorted(p for p in (root/'sources').glob('All*.lean') if p.stem!='AllReadback')
rows=[]
for p in modules:
    ns=[]
    for line_no,line in enumerate(p.read_text().splitlines(),1):
        m=re.match(r'^namespace\s+(\S+)',line)
        if m:ns.append(m.group(1));continue
        m=re.match(r'^end\s+(\S+)',line)
        if m:
            if ns:ns.pop()
            continue
        clean=re.sub(r'^\s*@\[[^]]*\]\s*','',line)
        m=re.match(r'^\s*(?:noncomputable\s+)?(def|theorem|abbrev|inductive|structure)\s+([^\s:{(]+)',clean)
        if m:
            name='.'.join(ns+[m.group(2)])
            rows.append({'name':name,'kind':m.group(1),'path':'sources/'+p.name,'line':line_no})
names=[r['name'] for r in rows]
assert len(names)==len(set(names)), 'duplicate public declaration'
text='/- Exact public readback and inherited transitive axiom gate. -/\nimport AuditSupport\n'
text+=''.join('import '+p.stem+'\n' for p in modules)
text+='\n'+''.join('#check '+n+'\n#print axioms '+n+'\n#ortho_audit '+n+'\n' for n in names)
(root/'sources'/'AllReadback.lean').write_text(text)
(root/'DECLARATION_CENSUS.json').write_text(json.dumps({'schema':'dependent-all-public-census-v1','declarations':rows},indent=2)+'\n')
print(json.dumps({'public_declarations':len(rows),'new_source_modules':len(modules)}))
