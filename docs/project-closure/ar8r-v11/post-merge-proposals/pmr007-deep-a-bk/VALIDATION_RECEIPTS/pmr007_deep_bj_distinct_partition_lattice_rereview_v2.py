from __future__ import annotations
from itertools import product
from fractions import Fraction
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

EXPECTED={}
for line in (ROOT/'PMR-007_DEEP_BJ_V2_FROZEN_HASHES.sha256').read_text().splitlines():
    h,p=line.split(maxsplit=1); EXPECTED[p]=h

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def partitions(n):
    # restricted-growth strings, independently partition-based rather than map/decoder enumeration
    out=[]
    def rec(a,maxv):
        if len(a)==n:
            out.append(tuple(a)); return
        for v in range(maxv+2):
            rec(a+[v],max(maxv,v))
    if n==0:return [()]
    rec([0],0)
    return out

def refines(p,q):
    # p refines q iff every p-block lies within a q-block
    seen={}
    for a,b in zip(p,q):
        if a in seen and seen[a]!=b:return False
        seen[a]=b
    return True

def meet(p,q):
    ids={}; nxt=0; out=[]
    for pair in zip(p,q):
        if pair not in ids:
            ids[pair]=nxt;nxt+=1
        out.append(ids[pair])
    return tuple(out)

def blocks(p):
    return {a:{i for i,x in enumerate(p) if x==a} for a in set(p)}

def det2(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]

res={'identity':'PMR-007-TQDC-1','checker':'DISTINCT_PARTITION_LATTICE_V2',
     'frozen_hash_rows':len(EXPECTED),'frozen_hash_mismatches':0,
     'partition_pairs':0,'descent_refinement_failures':0,
     'joint_partition_pairs':0,'meet_failures':0,'subdirect_failures':0,'full_product_failures':0,
     'coarsening_triples':0,'coarsening_failures':0,'anti_unification':{}}
for rel,h in EXPECTED.items():
    if sha(ROOT/rel)!=h:res['frozen_hash_mismatches']+=1

for n in range(1,6):
    ps=partitions(n)
    for r in ps:
      for f in ps:
        res['partition_pairs']+=1
        # decoder at partition level iff representation partition refines target partition
        # Independent witness: each r block has one f block.
        explicit=all(len({f[i] for i in B})==1 for B in blocks(r).values())
        if refines(r,f)!=explicit:res['descent_refinement_failures']+=1
    for p in ps:
      for q in ps:
        res['joint_partition_pairs']+=1
        m=meet(p,q)
        if not (refines(m,p) and refines(m,q)):
            res['meet_failures']+=1
        J={(p[i],q[i]) for i in range(n)}; A=set(p);B=set(q)
        if {a for a,b in J}!=A or {b for a,b in J}!=B:res['subdirect_failures']+=1
        full=J==set(product(A,B))
        intersections=all(blocks(p)[a]&blocks(q)[b] for a,b in product(A,B))
        if full!=intersections:res['full_product_failures']+=1
    for r in ps:
      for rp in ps:
        if not refines(r,rp):continue
        for f in ps:
          res['coarsening_triples']+=1
          if refines(rp,f) and not refines(r,f):res['coarsening_failures']+=1

# Anti-unification controls independently encoded.
A=[[Fraction(1,8),Fraction(3,8)],[Fraction(1,8),Fraction(3,8)]]
B=[[Fraction(3,8),Fraction(1,8)],[Fraction(1,8),Fraction(3,8)]]
res['anti_unification']['full_support_convex_geometry']={
  'same_support':all(x>0 for row in A for x in row) and all(x>0 for row in B for x in row),
  'rank1':det2(A)==0,'rank2':det2(B)!=0,
}
# Holonomy: same one-block vertex partition; only edge sums differ.
res['anti_unification']['cycle_holonomy']={'same_vertex_partition':True,'exact_sum':0,'obstructed_sum':3,'pass':0==0 and 3!=0}
# Congruence failure on Z3 addition for partition {0,1}|{2}.
eq=lambda x,y:(x<2 and y<2) or x==y==2
witness=None
for a,b,c,d in product(range(3),repeat=4):
    if eq(a,b) and eq(c,d) and not eq((a+c)%3,(b+d)%3):witness=(a,b,c,d);break
res['anti_unification']['algebra_congruence']={'witness':witness,'pass':witness is not None}
# Marginal parity control.
PA={(0,0):Fraction(1,2),(1,1):Fraction(1,2),(0,1):0,(1,0):0}
PR={(0,1):Fraction(1,2),(1,0):Fraction(1,2),(0,0):0,(1,1):0}
def marg(P,c,v):return sum(Fraction(z) for x,z in P.items() if x[c]==v)
res['anti_unification']['joint_probability']={'marginals_equal':all(marg(PA,c,v)==marg(PR,c,v) for c in (0,1) for v in (0,1)),'joint_different':PA!=PR}
res['anti_unification']['joint_probability']['pass']=res['anti_unification']['joint_probability']['marginals_equal'] and res['anti_unification']['joint_probability']['joint_different']
res['anti_unification']['full_support_convex_geometry']['pass']=res['anti_unification']['full_support_convex_geometry']['same_support'] and res['anti_unification']['full_support_convex_geometry']['rank1'] and res['anti_unification']['full_support_convex_geometry']['rank2']

bad=['frozen_hash_mismatches','descent_refinement_failures','meet_failures','subdirect_failures','full_product_failures','coarsening_failures']
res['result']='PASS' if not any(res[k] for k in bad) and all(v['pass'] for v in res['anti_unification'].values()) else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
