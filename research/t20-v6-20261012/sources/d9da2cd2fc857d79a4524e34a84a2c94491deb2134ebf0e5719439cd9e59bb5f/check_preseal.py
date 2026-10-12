#!/usr/bin/env python3
"""Read-only consistency check of this unsealed research payload, not Lean."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
from verify_input import verify

def H(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def need(ok:bool,msg:str)->None:
    if not ok:raise ValueError(msg)
root=Path(__file__).resolve().parents[1]
jsonfiles=sorted(root.rglob('*.json'))
for path in jsonfiles:json.loads(path.read_text())
for path in root.rglob('*.jsonl'):
    for line in path.read_text().splitlines():
        if line.strip():json.loads(line)
ci=json.loads((root/'proposals/CANDIDATE_INVENTORY.json').read_text())
need(len(ci['files'])==4 and len(ci['theorem_targets'])==14,'candidate inventory population')
for r in ci['files']:
    b=(root/r['path']).read_bytes()
    need(len(b)==r['bytes'] and H(b)==r['sha256'],'changed candidate: '+r['path'])
    need(not re.search(r'^\s*(axiom|sorry)\b',b.decode(),re.M),'forbidden new axiom/sorry declaration')
claims=json.loads((root/'research/CLAIMS.json').read_text())
need(len(claims)==19 and len({x['id'] for x in claims})==19,'claim population')
for c in claims:
    need((root/c['proof_file']).is_file(),'missing proof file')
    need(c['kernel_verified_here'] is False and c['novelty']=='NOT_CLAIMED','false proof/novelty credit')
criteria=json.loads((root/'research/CRITERIA_MATRIX.json').read_text())
need({c['obligation'] for c in criteria}=={'U09','U10','U11'},'obligation mismatch')
need(all(c['overall_status']=='PARTIAL' and not c['gate_changed'] for c in criteria),'gate/status mismatch')
need(not list(root.rglob('*.olean')),'unexpected formal artifact')
commands=0
for p in root.rglob('*.command.json'):
    d=json.loads(p.read_text());base=Path(str(p)[:-len('.command.json')])
    for field,ext in [('stdout_sha256','stdout'),('stderr_sha256','stderr')]:
        if field in d:need(H(Path(str(base)+'.'+ext).read_bytes())==d[field],'raw stream drift: '+str(p))
    if 'exit' in d:need(int(Path(str(base)+'.exit').read_text())==d['exit'],'exit drift: '+str(p))
    commands+=1
census=json.loads((root/'evidence/probes/preseal_census.stdout').read_text())
need(census['status']=='PASS_BOUNDED_ONLY','census status')
for n,s in census['scripts'].items():
    need(H((root/'proposals/python'/n).read_bytes())==s,'census source drift: '+n)
packet=root/'inputs/Orthemology_Pro_P01_Foundational_Formal.zip'
v=verify(packet)
need(v['status']=='PASS','input verification failed')
import zipfile
with zipfile.ZipFile(packet) as z:
    need(z.read('OBLIGATIONS.json')==(root/'obligations/EXACT_INPUT_OBLIGATIONS.json').read_bytes(),'obligation copy drift')
    for n in ['DEPENDENCY_DAG.json','CONCEPT_SOURCE_RESOLUTION.json']:
        need(z.read(n)==(root/'obligations'/n).read_bytes(),'governance copy drift')
print(json.dumps({'status':'PASS_PAYLOAD_CONSISTENCY_ONLY','json_files_parsed':len(jsonfiles),
    'command_records_verified':commands,'candidate_sources_verified':4,'unverified_theorem_targets':14,
    'scoped_claims':19,'input_counts':v['counts'],'input_identity_kind':v['identity_kind'],
    'kernel_proof_credit':False,'full_repository_tree_credit':False},indent=2))
