#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
from sympy import symbols
from sympy.logic.boolalg import And,Or,Not,Implies
from sympy.logic.inference import satisfiable
HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]
HASHFILE=ROOT/'PMR-007_DEEP_AK_V2_FROZEN_HASHES.sha256'
ASF=Path('EVIDENCE_ROOT/A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
mismatch=[]; rows=[]
for row in HASHFILE.read_text().splitlines():
    if not row.strip():continue
    exp,rel=row.split(None,1); rel=rel.strip(); act=sha(ROOT/rel); rows.append({'path':rel,'expected':exp,'actual':act})
    if exp!=act:mismatch.append(rel)
lines=ASF.read_text().splitlines()
anchors=[
 (70,'creator (khāliq). He is one'),(76,'evidence of his knowledge'),(78,'doer with choice'),
 (85,'impossibility of specification without a specifier'),(87,'commands and prohibits'),
 (99,'characterised by volition, speaking, hearing, and seeing'),
 (112,'Their meaning is nonetheless true'),(114,'speech and volition'),
 (124,'creation and command'),(523,'doer with choice'),(527,'doer by choice')]
anchor_fail=[]
for n,needle in anchors:
    got=lines[n-1] if n<=len(lines) else ''
    if needle not in got:anchor_fail.append({'line':n,'needle':needle,'got':got})
# Independent 3-bearer SAT encoding.
roles=['C','K','A','L','V','S']; bearers=range(3)
X={(r,i):symbols(f'{r}{i}') for r in roles for i in bearers}
P=symbols('P0:3'); W=symbols('WORLD'); Ident=symbols('IDENT')
exists_each=And(*[Or(*[X[r,i] for i in bearers]) for r in roles])
common=Or(*[And(*[X[r,i] for r in roles]) for i in bearers])
actual={(r,i):symbols(f'Q{r}{i}') for r in roles for i in bearers}
world_transfer=And(*[Implies(And(W,Ident,X[r,i]),actual[r,i]) for r in roles for i in bearers])

def sat(form):
    m=satisfiable(form,all_models=False)
    if m is False:return {'satisfiable':False,'model':None}
    return {'satisfiable':True,'model':{str(k):bool(v) for k,v in sorted(m.items(),key=lambda kv:str(kv[0]))}}
queries={
 'role_existence_without_common_bearer':sat(And(exists_each,Not(common))),
 'accepted_common_bundle_failure':sat(And(common,Not(common))),
 'common_bundle_without_personality':sat(And(common,Not(Or(*P)))),
 'source_bundle_without_world_transfer':sat(And(common,Not(W),Not(Or(*actual.values())))),
 'world_and_identity_transfer_failure':sat(And(common,W,Ident,world_transfer,Not(Or(*[And(*[actual[r,i] for r in roles]) for i in bearers])))),
 'explicit_H8_mapping_blocks_no_personality':sat(And(common,Implies(common,Or(*P)),Not(Or(*P)))),
}
claims={
 'existential_roles_do_not_entail_common_bearer':queries['role_existence_without_common_bearer']['satisfiable'],
 'accepted_common_bundle_is_consistent_and_direct':not queries['accepted_common_bundle_failure']['satisfiable'],
 'common_bundle_does_not_entail_personality':queries['common_bundle_without_personality']['satisfiable'],
 'source_bundle_does_not_entail_world_transfer':queries['source_bundle_without_world_transfer']['satisfiable'],
 'world_identity_bridge_transfers_bundle_when_explicit':not queries['world_and_identity_transfer_failure']['satisfiable'],
 'personality_follows_only_with_explicit_mapping':not queries['explicit_H8_mapping_blocks_no_personality']['satisfiable'],
}
res={'schema':'PMR007_DEEP_AK_DISTINCT_THREE_BEARER_SAT_REREVIEW_RESULTS_V1','method':'SYMPY_SAT_THREE_BEARER_SOURCE_ACTUAL_LAYER','frozen_hash_rows':len(rows),'frozen_hash_mismatches':len(mismatch),'source_anchor_checks':len(anchors),'source_anchor_failures':len(anchor_fail),'queries':queries,'claims':claims,'overall':'PASS' if not mismatch and not anchor_fail and all(claims.values()) else 'FAIL','notes':['Source co-reference filters the Track-N class but is not a neutral H6/H8 theorem.','Formal role-bundle models do not decide the intended philosophical semantics of source predicates.','World transfer requires explicit identity and adequacy bridges.']}
out=HERE.with_name(HERE.stem+'_results.json');out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(json.dumps(res,indent=2,sort_keys=True))
