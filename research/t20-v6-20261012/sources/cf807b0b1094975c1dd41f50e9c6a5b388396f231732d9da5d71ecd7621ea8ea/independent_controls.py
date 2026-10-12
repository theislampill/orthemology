#!/usr/bin/env python3
"""Reviewer-authored exact bounded controls; no infinite theorem is inferred."""
from fractions import Fraction as F
from math import factorial, comb, prod, ceil
from itertools import product
from collections import Counter
from pathlib import Path
import json, hashlib, platform

HERE=Path(__file__).resolve().parent
COUNTS=Counter()
MUTATIONS=[]
def check(group, condition):
    if not condition: raise AssertionError(group)
    COUNTS[group]+=1

def shell(d,n):
    if d==1: return [(n,)]
    return [(j,)+tail for j in range(n+1) for tail in shell(d-1,n-j)]

def add(M,B,scale=F(1)):
    for x,w in B.items():
        M[x]=M.get(x,F(0))+scale*w
        if M[x]==0: del M[x]

def moment(M,beta):
    return sum((w*prod(xi**bi for xi,bi in zip(x,beta)) for x,w in M.items()),F(0))

def tensor(A,B):
    return {xa+xb:wa*wb for xa,wa in A.items() for xb,wb in B.items()}

def difference(alpha,R,mutation=None):
    # Construct by repeated one-dimensional forward-difference convolution,
    # not the author's multidimensional closed-form summation.
    joint={():F(1)}
    for a in alpha:
        one={0:F(1)}
        for _ in range(a):
            nxt={}
            for x,w in one.items():
                nxt[x]=nxt.get(x,F(0))-w
                nxt[x+R]=nxt.get(x+R,F(0))+w
            one=nxt
        denom=R**a*(1 if mutation=='omit_factorial' else factorial(a))
        joint=tensor(joint,{(x,):w/denom for x,w in one.items()})
    if mutation=='scale_power': joint={x:w*R for x,w in joint.items()}
    if mutation=='reverse_sign': joint={x:-w for x,w in joint.items()}
    return joint

for d in (1,2,3):
    for n in range(1,7):
        for alpha in shell(d,n):
            for R in (1,3,11):
                D=difference(alpha,R)
                for m in range(n+1):
                    for beta in shell(d,m):
                        check('finite_difference',moment(D,beta)==int(alpha==beta))
                for m in range(n):
                    actual=sum(abs(w)*sum(abs(xi) for xi in x)**m for x,w in D.items())
                    upper=F(2**n*n**m,prod(factorial(a) for a in alpha)*R**(n-m))
                    check('absolute_majorant',actual<=upper)

# Independently compute the inherited Lambda prefix by Gaussian elimination.
FIRST=((0,0),(2,1),(1,2),(1,1),(1,0),(0,1),(2,0),(0,2),(3,0),(0,3))
ORDER=list(FIRST)+[(4-b,b) for b in range(5)]
INDEX={a:i for i,a in enumerate(ORDER)}
J=[F(1),F(1),F(1),F(4)]
def lam(a):
    if any(x%2 for x in a): return F(0)
    return J[INDEX[tuple(x//2 for x in a)]]
def solve(A,b):
    n=len(b); rows=[list(row)+[rhs] for row,rhs in zip(A,b)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if rows[i][j])
        rows[j],rows[pivot]=rows[pivot],rows[j]
        t=rows[j][j]; rows[j]=[v/t for v in rows[j]]
        for i in range(n):
            if i!=j:
                t=rows[i][j]
                rows[i]=[u-t*v for u,v in zip(rows[i],rows[j])]
    return [row[-1] for row in rows]
def gram(exponents):
    return [[lam(tuple(x+y for x,y in zip(a,b))) for b in exponents] for a in exponents]
for i in range(4,15):
    A=gram(ORDER[:i])
    v=[lam(tuple(x+y for x,y in zip(a,ORDER[i]))) for a in ORDER[:i]]
    w=solve(A,v)
    J.append(1+sum(x*y for x,y in zip(v,w)))
check('inherited_seed',J[:12]==list(map(F,[1,1,1,4,17,17,290,81515,81798,6644043123,479723268580926]))+[F(5,4)])
W={(0,0):F(1),(4,2):F(1),(2,4):F(1),(2,2):F(-1)}
check('inherited_witness',sum(c*lam(a) for a,c in W.items())==-1)

rho={(0,0):F(1)}; P=dict(rho); N={}; prev=0; BLOCKS=[]
for n in range(1,9):
    residual={a:lam(a)-moment(rho,a) for a in shell(2,n)}
    bound=sum(abs(v)*F(2**n,prod(factorial(ai) for ai in a)) for a,v in residual.items())
    R=max(1,prev+1,ceil(2**n*n**(n-1)*bound))
    B={}
    for a,r in residual.items(): add(B,difference(a,R),r)
    check('block_zero_mass',moment(B,(0,0))==0)
    for m in range(n):
        radial=sum(abs(w)*sum(abs(xi) for xi in x)**m for x,w in B.items())
        check('summable_tail',radial<=F(1,2**n))
    add(rho,B)
    add(P,{x:w for x,w in B.items() if w>0})
    add(N,{x:-w for x,w in B.items() if w<0})
    for degree in range(n+1):
        for beta in shell(2,degree): check('corrected_prefix',moment(rho,beta)==lam(beta))
    check('jordan_sum_identity',all(P.get(x,0)-N.get(x,0)==rho.get(x,0) for x in set(P)|set(N)|set(rho)))
    check('mass_normalization',moment(P,(0,0))==1+moment(N,(0,0)))
    check('negative_mass_bound',0<=moment(N,(0,0))<=F(1,2))
    BLOCKS.append({'degree':n,'radius_bits':R.bit_length(),'block_atoms':len(B),'prefix_atoms':len(rho)})
    prev=R

def apply(M,W):return sum(c*moment(M,a) for a,c in W.items())
check('signed_witness',apply(rho,W)==-1)
check('signed_witness',apply(P,W)-apply(N,W)==-1)
check('signed_witness',apply(P,W)>=F(3,4)*moment(P,(0,0)))
check('signed_witness',apply(N,W)>=F(3,4)*moment(N,(0,0)))
check('strict_negative_mass',0<moment(N,(0,0)))

# Mutations are required to be observably rejected by their named invariant.
for mutation,a,R in [('omit_factorial',(3,1),3),('scale_power',(2,1),5),('reverse_sign',(1,2),7)]:
    obtained=moment(difference(a,R,mutation),a)
    check('mutation_rejection',obtained!=1)
    MUTATIONS.append({'mutation':mutation,'invariant':'target degree moment must equal one','obtained':str(obtained)})
# A unit radius need not make the correction small in total variation.
bad=difference((1,),1)
check('mutation_rejection',sum(abs(w) for w in bad.values())>F(1,2))
MUTATIONS.append({'mutation':'omit_large_radius_choice','invariant':'degree-one TV <= 1/2','obtained':str(sum(abs(w) for w in bad.values()))})
# A stopped series has no authority over the next full moment; calculate one.
next_residuals={a:lam(a)-moment(rho,a) for a in shell(2,9) if any(v%2 for v in a)}
check('mutation_rejection',any(v for v in next_residuals.values()))
MUTATIONS.append({'mutation':'stop_series_after_degree_eight','invariant':'all later moments match','nonzero_degree_nine_residuals':sum(bool(v) for v in next_residuals.values())})
# Replacing +N by -N destroys the genuine initial law, already at mass.
n0=moment(N,(0,0)); C=1+n0
check('mutation_rejection',(1-n0)/C!=1)
MUTATIONS.append({'mutation':'subtract_N_in_initial_mixture','invariant':'initial mass one','rejected':True})
check('mutation_rejection',(1+n0)!=1)
MUTATIONS.append({'mutation':'omit_C_normalizer','invariant':'initial mass one','rejected':True})
for Ap,Agp,a,Ag in [(F(2),F(3),F(5),F(7)),(F(-1),F(4),F(3,2),F(5,3))]:
    derivative=(-Agp*a+Ap*Ag)/a**2
    rhs=-Agp/a+(Ag/a)*(Ap/a)
    check('quotient_ode',derivative==rhs)
    check('mutation_rejection',(-Agp*a-Ap*Ag)/a**2!=rhs)
MUTATIONS.append({'mutation':'wrong_sign_a_derivative','invariant':'normalized hierarchy','rejected':True})
# The active classical moment identity's square completion holds exactly.
for j in range(-12,13):
    for m in range(15): check('lattice_shift_identity',F(m*j)-F(j*j,2)==F(m*m,2)-F((j-m)**2,2))

result={'status':'PASS','python':platform.python_version(),'assertions':sum(COUNTS.values()),'groups':dict(COUNTS),'prefix_blocks':BLOCKS,'mutations':MUTATIONS,'scope':'Reviewer-authored finite exact arithmetic controls only. Infinite series, full strict positivity, arbitrary schedules and positive-time nonrepresentation require the separately reviewed ordinary proof.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
