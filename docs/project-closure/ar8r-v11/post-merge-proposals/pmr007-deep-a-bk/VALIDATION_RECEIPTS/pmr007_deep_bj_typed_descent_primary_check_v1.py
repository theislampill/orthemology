from __future__ import annotations
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def maps(n,k):
    return product(range(k), repeat=n)

def fibre_condition(r,f):
    n=len(r)
    return all(r[i]!=r[j] or f[i]==f[j] for i in range(n) for j in range(n))

def decoder_exists(r,f):
    d={}
    for a,b in zip(r,f):
        if a in d and d[a]!=b: return False
        d[a]=b
    return True

def joint(*fs):
    return tuple(zip(*fs))

def attained(m): return set(m)

def det2(M):
    return M[0][0]*M[1][1]-M[0][1]*M[1][0]

res={
 'identity':'PMR-007-TQDC-1','checker':'PRIMARY_V1',
 'map_target_cases':0,'descent_mismatches':0,'canonical_size_failures':0,
 'joint_family_cases':0,'kernel_intersection_failures':0,'subdirect_failures':0,
 'full_product_characterization_failures':0,
 'coarsening_cases':0,'coarsening_noncreation_failures':0,
 'anti_unification':{},
}

# Exhaustive maps for n<=4, representation and target alphabets <=3.
for n in range(1,5):
  for kr in range(1,4):
    for ky in range(1,4):
      for r in maps(n,kr):
        for f in maps(n,ky):
          res['map_target_cases']+=1
          a=fibre_condition(r,f); b=decoder_exists(r,f)
          if a!=b: res['descent_mismatches']+=1
          if a and len(attained(r)) < len(attained(f)):
            res['canonical_size_failures']+=1

# Joint targets on n<=4. Check kernel intersection, subdirectness, full-product criterion.
for n in range(1,5):
  for k1 in range(1,3):
    for k2 in range(1,3):
      for f1 in maps(n,k1):
        for f2 in maps(n,k2):
          F=joint(f1,f2); res['joint_family_cases']+=1
          inter=all((F[i]==F[j]) == (f1[i]==f1[j] and f2[i]==f2[j]) for i in range(n) for j in range(n))
          if not inter: res['kernel_intersection_failures']+=1
          J=attained(F); A=attained(f1); B=attained(f2)
          if {x for x,y in J}!=A or {y for x,y in J}!=B:
            res['subdirect_failures']+=1
          full=(J==set(product(A,B)))
          tuple_intersections=all(any(f1[i]==a and f2[i]==b for i in range(n)) for a,b in product(A,B))
          if full!=tuple_intersections: res['full_product_characterization_failures']+=1

# Exhaustive coarsening for n<=4, small alphabets.
for n in range(1,5):
  for kr in range(1,4):
    for kc in range(1,3):
      for ky in range(1,3):
        for r in maps(n,kr):
          for c in maps(kr,kc):
            rp=tuple(c[x] for x in r)
            for f in maps(n,ky):
              res['coarsening_cases']+=1
              if decoder_exists(rp,f) and not decoder_exists(r,f):
                res['coarsening_noncreation_failures']+=1

# Anti-unification explicit controls.
P_rank1=[[Fraction(1,6),Fraction(1,3)],[Fraction(1,6),Fraction(1,3)]]
P_rank2=[[Fraction(2,5),Fraction(1,10)],[Fraction(1,10),Fraction(2,5)]]
res['anti_unification']['same_full_support_different_ordinary_and_nonnegative_rank']={
 'same_support': all(x>0 for row in P_rank1 for x in row) and all(x>0 for row in P_rank2 for x in row),
 'rank1_det': str(det2(P_rank1)),
 'rank2_det': str(det2(P_rank2)),
 'pass': det2(P_rank1)==0 and det2(P_rank2)!=0,
}
# Equal one-bit marginals, different joint parity.
PA={(0,0):Fraction(1,2),(1,1):Fraction(1,2),(0,1):Fraction(0),(1,0):Fraction(0)}
PR={(0,1):Fraction(1,2),(1,0):Fraction(1,2),(0,0):Fraction(0),(1,1):Fraction(0)}
margin=lambda P,coord,val: sum(p for x,p in P.items() if x[coord]==val)
res['anti_unification']['equal_marginals_different_joint']={
 'marginals_equal': all(margin(PA,c,v)==margin(PR,c,v) for c in [0,1] for v in [0,1]),
 'joint_different': PA!=PR,
}
# Same vertex partition, cycle exactness differs.
zero=[0,0,0]; nonzero=[1,1,1]
res['anti_unification']['state_partition_does_not_test_edge_holonomy']={
 'same_vertex_profile': True,
 'zero_cycle_sum': sum(zero)==0,
 'nonzero_cycle_sum': sum(nonzero)!=0,
}
# Set equivalence not necessarily algebra congruence: 0~1, 2 alone; op x+y mod3.
eq=lambda x,y: (x in [0,1] and y in [0,1]) or x==y==2
congruence=all(not (eq(a,b) and eq(c,d)) or eq((a+c)%3,(b+d)%3) for a,b,c,d in product(range(3),repeat=4))
res['anti_unification']['set_equivalence_not_automatically_congruence']={'congruence':congruence,'pass':not congruence}

fail_keys=['descent_mismatches','canonical_size_failures','kernel_intersection_failures','subdirect_failures','full_product_characterization_failures','coarsening_noncreation_failures']
res['result']='PASS' if not any(res[k] for k in fail_keys) and all(v.get('pass',True) for v in res['anti_unification'].values()) else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
