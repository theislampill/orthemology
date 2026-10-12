import json,hashlib,re
from pathlib import Path
from datetime import datetime,timezone
O=Path(__file__).resolve().parent; ROOT=O.parent.parent
B=json.loads((O/'SOURCE_BINDINGS.json').read_text());G=json.loads((O/'EDGES.json').read_text())
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
checks=[]
for r in B['sources']:
 p=ROOT/r['path'];require(p.is_file(),r['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'changed source '+r['path']);checks.append(r['id'])
for r in B['upstream_identity_checks']:require(r['status']=='match','unmatched ancestor '+r['path'])
for r in B['review_currentness']:require(r['current_review_binding_found'],'unbound review '+r['id'])
ids={r['id'] for r in B['sources']}
for n in G['nodes'].values():require(n['source_id'] in ids,'missing node source')
seen=set()
for e in G['edges']:
 require(e['id'] not in seen,'duplicate edge');seen.add(e['id']);require(e['type'] in G['edge_types'],'invalid edge type');require(e['source'] in G['nodes'] and e['target'] in G['nodes'],'missing node');require(bool(e['scope_or_failed_premise']),'missing scope')
 for ev in e['evidence']:require(ev.split()[0] in ids,'unresolved evidence '+ev)
s=(O/'RESULT.md').read_text()
for ref in re.findall(r'\[([^\]\n]+)\]',s):
 # Only source-reference brackets, not intervals/algebra.
 if ref[0].isalpha() and '§' in ref:
  for part in ref.split(';'):
   key=part.strip().split()[0].rstrip(',');require(key in ids,'unresolved prose reference '+key)
require('C³ chart potentials and C² mobility' in s,'missing regularity guard')
require('μ²≤ν≤μ' in s,'missing admissible moment guard')
require('full refinement-cell mass action' in s,'missing algorithm symmetry guard')
result={'schema':'t20.cross-front-synthesis.verification.v1','utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','bound_sources':len(checks),'upstream_identity_matches':len(B['upstream_identity_checks']),'current_reviewed_result_bindings':len(B['review_currentness']),'nodes':len(G['nodes']),'edges':len(G['edges']),'scope':'Document hashes, references, typed graph and explicit reviewer-required guards only; no mathematical checker replay or fresh theorem certification','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['VERIFICATION.json','MANIFEST.json']}}
(O/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
