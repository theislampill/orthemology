from __future__ import annotations
from fractions import Fraction
from itertools import product, combinations
import json, random
from pathlib import Path

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def det2(M): return M[0][0]*M[1][1]-M[0][1]*M[1][0]

def total(M): return sum(sum(r) for r in M)

def normalize(M):
    s=total(M)
    return [[Fraction(x,s) for x in row] for row in M]

def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Fraction(0)) for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A): return [list(x) for x in zip(*A)]

def canonical_x_factorization(P):
    # P = U V with H=X: U is diagonal row-mass, V is P(Y|X).
    m,n=len(P),len(P[0])
    U=[[Fraction(0) for _ in range(m)] for _ in range(m)]
    V=[[Fraction(0) for _ in range(n)] for _ in range(m)]
    for x in range(m):
        w=sum(P[x])
        U[x][x]=w
        if w:
            for y in range(n): V[x][y]=P[x][y]/w
    return U,V

def factor_to_latent(U,V):
    # P=UV. Convert each nonzero rank-one term into lambda*a*b.
    m,r=len(U),len(U[0]); n=len(V[0])
    comps=[]
    for h in range(r):
        s=sum(U[x][h] for x in range(m)); t=sum(V[h][y] for y in range(n))
        if s*t==0: continue
        lam=s*t
        a=[U[x][h]/s for x in range(m)]
        b=[V[h][y]/t for y in range(n)]
        comps.append((lam,a,b))
    return comps

def latent_to_matrix(comps,m,n):
    return [[sum((lam*a[x]*b[y] for lam,a,b in comps),Fraction(0)) for y in range(n)] for x in range(m)]

def deterministic_coarsen(P,row_map,col_map,m2,n2):
    Q=[[Fraction(0) for _ in range(n2)] for __ in range(m2)]
    for i,row in enumerate(P):
        for j,v in enumerate(row): Q[row_map[i]][col_map[j]]+=v
    return Q

def integer_compositions(total,parts):
    if parts==1:
        yield (total,); return
    for i in range(total+1):
        for rest in integer_compositions(total-i,parts-1): yield (i,)+rest

res={
 'identity':'PMR-007-ILRC-1','checker':'PRIMARY_V1','field':'exact_rationals_for_executable_witnesses; theorem_candidate_over_nonnegative_reals',
 'two_by_two_tables':0,'two_by_two_rank1':0,'two_by_two_rank2':0,'canonical_factorization_failures':0,
 'factor_normalization_trials':0,'factor_normalization_failures':0,
 'coarsening_trials':0,'coarsening_factorization_failures':0,
 'explicit_rank_witnesses':{},'zero_term_handling':'NOT_EXPLICITLY_ATTACKED_IN_V1'
}

# Exhaust all 2x2 count tables of totals 1..14. In 2x2, ordinary rank is 1 or 2,
# and nonnegative rank equals ordinary rank. Check canonical H=X realization exactly.
for N in range(1,15):
    for a,b,c,d in integer_compositions(N,4):
        M=[[a,b],[c,d]]; P=normalize(M); res['two_by_two_tables']+=1
        rank=1 if det2(P)==0 else 2
        res['two_by_two_rank1' if rank==1 else 'two_by_two_rank2']+=1
        U,V=canonical_x_factorization(P)
        if matmul(U,V)!=P: res['canonical_factorization_failures']+=1

# Random nonnegative factors -> normalized P -> latent normalization -> exact reconstruction.
rng=random.Random(20260806)
for _ in range(50000):
    m=rng.randint(2,5); n=rng.randint(2,5); r=rng.randint(1,5)
    U=[[Fraction(rng.randint(0,5)) for _ in range(r)] for __ in range(m)]
    V=[[Fraction(rng.randint(0,5)) for _ in range(n)] for __ in range(r)]
    P0=matmul(U,V); s=total(P0)
    if not s: continue
    U=[[u/s for u in row] for row in U]
    P=matmul(U,V)
    comps=factor_to_latent(U,V)
    res['factor_normalization_trials']+=1
    if sum(c[0] for c in comps)!=1 or latent_to_matrix(comps,m,n)!=P:
        res['factor_normalization_failures']+=1

# Common deterministic coarsening pushes the canonical factorization forward.
for _ in range(50000):
    m=rng.randint(2,6); n=rng.randint(2,6)
    counts=[[rng.randint(0,9) for _ in range(n)] for __ in range(m)]
    if total(counts)==0: counts[0][0]=1
    P=normalize(counts); U,V=canonical_x_factorization(P)
    m2=rng.randint(1,m); n2=rng.randint(1,n)
    rm=[rng.randrange(m2) for _ in range(m)]; cm=[rng.randrange(n2) for _ in range(n)]
    Q=deterministic_coarsen(P,rm,cm,m2,n2)
    # A U and V B^T
    A=[[Fraction(int(rm[i]==a)) for i in range(m)] for a in range(m2)]
    B=[[Fraction(int(cm[j]==b)) for j in range(n)] for b in range(n2)]
    pushedU=matmul(A,U); pushedV=matmul(V,transpose(B))
    res['coarsening_trials']+=1
    if matmul(pushedU,pushedV)!=Q: res['coarsening_factorization_failures']+=1

# Exact lower/upper witnesses by ordinary rank and canonical factorization.
for n in range(2,7):
    P=[[Fraction(int(i==j),n) for j in range(n)] for i in range(n)]
    U,V=canonical_x_factorization(P)
    res['explicit_rank_witnesses'][f'identity_{n}']={
      'ordinary_rank':n,'canonical_width':n,'factorization_pass':matmul(U,V)==P,
      'interpretation':'ordinary rank lower bound and H=X upper bound force nonnegative rank n'
    }

res['result']='PASS' if not any(res[k] for k in ['canonical_factorization_failures','factor_normalization_failures','coarsening_factorization_failures']) else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
