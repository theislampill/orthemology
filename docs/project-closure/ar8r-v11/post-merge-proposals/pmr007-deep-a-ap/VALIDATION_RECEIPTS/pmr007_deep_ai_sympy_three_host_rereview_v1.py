#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, Xor
from sympy.logic.inference import satisfiable

HERE=Path(__file__).resolve(); ROOT=HERE.parents[1]
HASHFILE=ROOT/'PMR-007_DEEP_AI_V2_FROZEN_HASHES.sha256'
ASF=Path('EVIDENCE_ROOT/A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md')
ELT=Path('EVIDENCE_ROOT/El-Tobgui-dissertation-snapshot.md')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# frozen hash verification
hash_rows=[]; mismatch=[]
for row in HASHFILE.read_text().splitlines():
    if not row.strip(): continue
    expected,path=row.split(None,1); path=path.strip()
    p=Path(path) if path.startswith('/') else ROOT/path
    actual=sha(p); hash_rows.append((str(p),expected,actual))
    if actual!=expected: mismatch.append(str(p))
# source anchors
asf_lines=ASF.read_text().splitlines(); elt_lines=ELT.read_text().splitlines()
anchors=[
 (ASF,487,'The absolute is only absolute in the mind'),
 (ELT,4308,'the only thing existing in the external world is the individual entities'),
 (ELT,4310,'universal concepts existing solely in the mind'),
 (ELT,4314,'universal concepts are only abstractions of the mind'),
 (ELT,4325,'universal – is but a logical notion subsisting strictly within the mind'),
 (ELT,4335,'universal notions'),
 (ELT,4345,'universals (kulliyyāt) are strictly conceptual or notional realities subsisting in the mind'),
 (ELT,4599,'reason is dependent'),
 (ELT,4718,'abstract notions can exist only in the mind'),
]
anchor_fail=[]
for p,n,needle in anchors:
    lines=asf_lines if p==ASF else elt_lines
    got=lines[n-1] if n<=len(lines) else ''
    if needle not in got: anchor_fail.append({'path':str(p),'line':n,'needle':needle,'got':got})

# Three-host SAT model, independent from the two-host brute-force checker.
S,U,N=symbols('S U N')
M=symbols('M0:3'); R=symbols('R0:3'); G=symbols('G0:3'); H=symbols('H0:3'); P=symbols('P0:3')
base=[Implies(N,Or(*[And(M[i],R[i]) for i in range(3)]))]
base += [Implies(G[i],And(M[i],R[i])) for i in range(3)]
H7a=Implies(S,N)
H7b=Implies(And(S,U,N),Or(*G))
H7c=And(*[Implies(And(U,G[i]),H[i]) for i in range(3)])
H7d=And(*[Not(And(G[i],G[j])) for i in range(3) for j in range(i+1,3)])
full=And(*(base+[H7a,H7b,H7c,H7d]))
baseF=And(*base)

def sat(formula):
    m=satisfiable(formula, all_models=False)
    if m is False: return {'satisfiable':False,'model':None}
    # stable printable subset
    return {'satisfiable':True,'model':{str(k):bool(v) for k,v in sorted(m.items(),key=lambda kv:str(kv[0]))}}

exact_one_underived=Or(*[
    And(G[i],H[i],*[Not(G[j]) for j in range(3) if j!=i]) for i in range(3)
])
queries={
 'base_notional_without_host':sat(And(baseF,N,Not(Or(*M)))),
 'base_structure_underived_without_host':sat(And(baseF,S,U,Not(Or(*M)))),
 'base_notional_underived_without_ground':sat(And(baseF,N,U,Not(Or(*G)))),
 'h7a_b_d_without_transfer_no_underived_host':sat(And(And(*(base+[H7a,H7b,H7d])),S,U,Not(Or(*H)))),
 'full_bridge_failure_exactly_one_underived_constitutive_host':sat(And(full,S,U,Not(exact_one_underived))),
 'full_bridge_without_personality':sat(And(full,S,U,Not(Or(*P)))),
 'full_bridge_multiple_downstream_minds':sat(And(full,S,U,M[0],R[0],M[1],R[1],Not(G[0]),G[1])),
}
claims={
 'NM_HOST_entailment_independently_unsat':not queries['base_notional_without_host']['satisfiable'],
 'structure_underived_no_host_countermodel_sat':queries['base_structure_underived_without_host']['satisfiable'],
 'notional_underived_no_ground_countermodel_sat':queries['base_notional_underived_without_ground']['satisfiable'],
 'underivability_nontransfer_countermodel_sat':queries['h7a_b_d_without_transfer_no_underived_host']['satisfiable'],
 'full_bridge_exactly_one_underived_constitutive_host_unsat_failure':not queries['full_bridge_failure_exactly_one_underived_constitutive_host']['satisfiable'],
 'full_bridge_no_personality_countermodel_sat':queries['full_bridge_without_personality']['satisfiable'],
 'unique_constitutive_host_allows_multiple_downstream_representers':queries['full_bridge_multiple_downstream_minds']['satisfiable'],
}
res={
 'schema':'PMR007_DEEP_AI_DISTINCT_THREE_HOST_SAT_REREVIEW_RESULTS_V1',
 'frozen_hash_rows':len(hash_rows),'frozen_hash_mismatches':len(mismatch),
 'source_anchor_checks':len(anchors),'source_anchor_failures':len(anchor_fail),
 'host_count':3,'method':'SYMPY_SAT_THREE_HOST_SYMBOLIC',
 'queries':queries,'claims':claims,
 'overall':'PASS' if not mismatch and not anchor_fail and all(claims.values()) else 'FAIL',
 'notes':[
  'The positive conditional proves only what H7a-H7d explicitly specify.',
  'The source ontology is not Arabic-primary verified in this round.',
  'No metaphysical possibility, personality, or world-truth conclusion is drawn.'
 ]
}
out=HERE.with_name(HERE.stem+'_results.json')
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
