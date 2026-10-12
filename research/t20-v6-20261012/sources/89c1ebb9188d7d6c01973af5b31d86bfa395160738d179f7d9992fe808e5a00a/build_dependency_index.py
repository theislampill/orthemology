#!/usr/bin/env python3
"""Unify edge direction without upgrading relationships into implications."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent.parent

def read(path): return json.loads((B/path).read_text())
def main():
    edges=[]
    for c in read('foundations/FOUNDATIONAL_CLAIMS.json')['claims']:
        for e in c.get('dependencies',[]):
            edges.append({'claim':c['id'],'references':e['target'],'relationship':e['type'],'justification':e['relation'],'owner_file':'foundations/FOUNDATIONAL_CLAIMS.json'})
    for c in read('geometry/GEOMETRY_MOMENTS_CLAIMS.json')['claims']:
        for e in c.get('dependencies',[]):
            edges.append({'claim':c['id'],'references':e['claim_or_owner'],'relationship':e.get('dependency_type','unclassified_source_relation'),'justification':e['relationship'],'owner_file':'geometry/GEOMETRY_MOMENTS_CLAIMS.json'})
    for e in read('evidence/DEPENDENCY_EDGES.json')['edges']:
        edges.append({'claim':e['source'],'references':e['target'],'relationship':e['type'],'justification':e['justification'],'owner_file':'evidence/DEPENDENCY_EDGES.json'})
    for e in read('proofs/DEPENDENCY_EDGES.json')['edges']:
        edges.append({'claim':e['target'],'references':e['source'],'relationship':e['type'],'justification':e['justification'],'owner_file':'proofs/DEPENDENCY_EDGES.json'})
    ids={c['id'] for c in read('CLAIM_REGISTER.json')['claims']}
    for e in edges:
        e['reference_status']='local_claim' if e['references'] in ids else 'inherited_or_external_owner'
        if e['claim'] not in ids: raise SystemExit('Consumer missing: '+e['claim'])
    result={'schema':'t20-consolidated-typed-reference-index-v1','orientation':'claim references another result or owner. Relationship specifies use; the arrow is not an unconditional logical implication. Proof-track source-to-consumer edges were reversed to this common orientation.', 'scope':'The entire research-reference graph need not be acyclic: comparisons and currentness links are not proof dependencies. No new master theorem is asserted.','edge_count':len(edges),'edges':edges,'cross_front_interfaces':'CROSS_FRONT_INTERFACES.json'}
    (B/'DEPENDENCY_INDEX.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'edges':len(edges),'external_owner_references':sum(e['reference_status']!='local_claim' for e in edges)}))
if __name__=='__main__': main()
