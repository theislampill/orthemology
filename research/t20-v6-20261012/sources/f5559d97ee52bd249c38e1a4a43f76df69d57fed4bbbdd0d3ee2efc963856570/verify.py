#!/usr/bin/env python3
"""Exact algebraic controls for the conditional gradient-transport theorem.
Finite controls supplement the ordinary proof; they are not formal certification.
"""
import sympy as s
from itertools import product
from pathlib import Path
import hashlib, json

Q=s.Rational
checks=[]
def check(label, cond):
    assert cond, label
    checks.append(label)
    print('PASS:', label)
def eq(a,b):
    if isinstance(a, s.MatrixBase):
        return a.shape == b.shape and all(s.simplify(x)==0 for x in a-b)
    return s.simplify(a-b)==0
def G(mu): return s.diag(*mu)-mu*mu.T/sum(mu)
def D(mu,p,q):
    d=p-q
    return (d.T*s.diag(*[1/x for x in mu])*d)[0]/2

a,b,c=s.symbols('a b c', positive=True)
mu=s.Matrix([a,b,c]); ones=s.ones(3,1); H=s.diag(1/a,1/b,1/c)
check('symbolic tangent cometric annihilates constants', eq(G(mu)*ones,s.zeros(3,1)))
check('symbolic duality identity H G = I - 1 mu^T/M', eq(H*G(mu),s.eye(3)-ones*mu.T/sum(mu)))
Kdet=s.Matrix([[1,1,0],[0,0,1]])
check('symbolic deterministic lumping commutes',eq(Kdet*G(mu)*Kdet.T,G(Kdet*mu)))

mu=s.Matrix([Q(1,2),Q(1,2)])
K=s.Matrix([[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]])
A=K*G(mu)*K.T; B=G(K*mu); C=B-A; z=s.Matrix(s.symbols('z0 z1'))
check('binary stochastic canonical discrepancy',eq(C,s.Matrix([[Q(3,16),-Q(3,16)],[-Q(3,16),Q(3,16)]])))
check('binary covariance variance sum',eq((z.T*C*z)[0],sum(mu[i]*(sum(K[j,i]*z[j]**2 for j in range(2))-sum(K[j,i]*z[j] for j in range(2))**2) for i in range(2))))
g=s.Matrix([1,0]); pf=-G(mu)*K.T*g
check('binary fine and projected velocities',eq(pf,s.Matrix([-Q(1,8),Q(1,8)])) and eq(K*pf,s.Matrix([-Q(1,16),Q(1,16)])))
check('binary canonical coarse velocity',eq(-B*g,s.Matrix([-Q(1,4),Q(1,4)])))
p0=s.Matrix([Q(1,2),Q(1,2)]); t=s.symbols('t',real=True)
pf_t=p0+t*pf; qc_t=K*p0-t*B*g
check('binary exact trajectories differ at t=1',eq(K*pf_t.subs(t,1),s.Matrix([Q(7,16),Q(9,16)])) and eq(qc_t.subs(t,1),s.Matrix([Q(1,4),Q(3,4)])))
p=s.Matrix([Q(3,4),Q(1,4)]); r=s.Matrix([Q(1,4),Q(3,4)])
check('binary divergence strictly contracts 1/2 to 1/8',eq(D(mu,p,r),Q(1,2)) and eq(D(K*mu,K*p,K*r),Q(1,8)))
check('binary gauge shift leaves both fields unchanged',eq(A*(g+7*s.ones(2,1)),A*g) and eq(B*(g+7*s.ones(2,1)),B*g))

mu3=s.ones(3,1)/3
K3=s.Matrix([[Q(3,4),Q(1,4),0],[Q(1,4),Q(3,4),0],[0,0,1]])
A3=K3*G(mu3)*K3.T; B3=G(K3*mu3); e1=s.Matrix([1,0,0])
vfine=-A3*e1; vcoarse=-B3*e1
check('ternary exact direction-changing noisy control',eq(vfine,s.Matrix([-Q(7,72),-Q(1,72),Q(1,9)])) and eq(vcoarse,s.Matrix([-Q(2,9),Q(1,9),Q(1,9)])))
check('ternary fields are not collinear', s.Matrix.hstack(vfine,vcoarse).rank()==2)
check('noisy channel preserves a selected block-constant objective',eq((B3-A3)*s.Matrix([1,1,0]),s.zeros(3,1)))

# Exhaustive finite grid: every 2 x 3 column-stochastic matrix with entries in {0,1/2,1}.
mu_enum=s.Matrix([Q(1,6),Q(1,3),Q(1,2)])
for cols in product([0,Q(1,2),1],repeat=3):
    k=s.Matrix([cols,[1-x for x in cols]])
    deficit=s.diag(*(k*mu_enum))-k*s.diag(*mu_enum)*k.T
    deterministic=all(x in (0,1) for x in cols)
    assert eq(deficit,s.zeros(2,2)) == deterministic
    assert deficit[0,0]>=0 and deficit.det()>=0
check('all 27 binary-output rational channels satisfy PSD and deterministic iff',True)

# Full-rank and rank-deficient quotient controls.
mu4=s.Matrix([Q(1,10),Q(2,10),Q(3,10),Q(4,10)])
Kfull=s.Matrix([[1,Q(1,2),0,Q(1,4)],[0,Q(1,2),1,Q(1,4)],[0,0,0,Q(1,2)]])
Krank=s.Matrix([[Q(1,2),Q(1,4),0],[Q(1,2),Q(1,4),0],[0,Q(1,2),1]])
for label,u,k,h0 in [('full-rank',mu4,Kfull,s.Matrix([1,-1,0,0])),('rank-deficient',mu3,Krank,s.Matrix([1,-1,0]))]:
    a=k*G(u)*k.T; ap=a.pinv(); H=s.diag(*[1/x for x in u]); w=k*h0
    v=G(u)*k.T*ap*w
    check(label+' quotient lift feasible and tangent',eq(k*v,w) and eq(sum(v),0))
    check(label+' quotient energy identity',eq((v.T*H*v)[0],(w.T*ap*w)[0]))
    null=s.Matrix.vstack(k,s.ones(1,len(u))).nullspace()
    for h in null:
        assert eq((v.T*H*h)[0],0)
        assert eq(((v+h).T*H*(v+h))[0],(w.T*ap*w)[0]+(h.T*H*h)[0])
    check(label+' quotient lift orthogonality and Pythagorean identity',True)
    check(label+' rank is rank(K)-1',a.rank()==k.rank()-1)
    g=s.Matrix(list(range(1,k.rows+1)))
    check(label+' quotient metric identifies A g as gradient',eq((a*g).T*ap*w,g.T*w))

# A constant noisy channel has a single reachable law, no reachable tangent.
Kreset=s.Matrix([[Q(1,3),Q(1,3)],[Q(2,3),Q(2,3)]])
check('rank-one reset has zero induced cometric',eq(Kreset*G(mu)*Kreset.T,s.zeros(2,2)))
check('canonical reset-output cometric remains nonzero',not eq(G(Kreset*mu),s.zeros(2,2)))

# Deterministic commutation cannot ensure all-time interior fine existence.
mu_u=s.ones(3,1); pp=s.Matrix([Q(1,12),Q(5,12),Q(1,2)]); gg=s.Matrix([1,0])
v=-G(mu_u)*Kdet.T*gg
check('deterministic fine boundary at t=1/4 with coarse state interior',eq(pp+v/4,s.Matrix([0,Q(1,3),Q(2,3)])) and eq(Kdet*(pp+v/4),s.Matrix([Q(1,3),Q(2,3)])))
check('deterministic projected velocity equals coarse before boundary',eq(Kdet*v,-G(Kdet*mu_u)*gg))

# Noisy block channel changes even a target-directed quadratic correction direction.
rstar=s.Matrix([Q(1,6),Q(1,3),Q(1,2)]); q0=s.ones(3,1)/3
grad=s.diag(3,3,3)*(q0-rstar)
check('canonical target-divergence flow points directly to its target',eq(-B3*grad,rstar-q0))
check('noisy projected target-divergence flow has another direction',s.Matrix.hstack(-A3*grad,rstar-q0).rank()==2)

# Full-Hessian embedding at an exact noncoherent point.
x,y,z=s.symbols('x y z',positive=True); bvec=s.Matrix([x,y,z]); mass=x+y+z
F=sum(bvec[i]**2/mu3[i] for i in range(3))/(2*mass)+(mass-1)**2/2
J=(K3*(bvec/mass))[0]; E=(mass-1)**2/2+J
HF=s.hessian(F,(x,y,z)); dE=s.Matrix([s.diff(E,v) for v in (x,y,z)])
point={x:Q(1,2),y:Q(1,3),z:Q(1,6)}
# Use total mass 2, so radial and tangent both active.
point={v:2*c for v,c in point.items()}; bb=bvec.subs(point); ss=sum(bb); pp=bb/ss
velocity=-HF.subs(point).inv()*dE.subs(point)
sdot=-(ss-1)
pdot=-G(mu3)*K3.T*e1/ss
check('augmented full-Hessian velocity has stated mass/simplex split',eq(velocity,pp*sdot+ss*pdot))
# Radial-only transport for genuinely noisy K remains exact.
radial=-(ss-1)*pp
check('normalization-only radial field still commutes for noisy K',eq(K3*radial,-(ss-1)*(K3*bb)/ss))

# Tangent objective descent need not improve every truth-state loss.
HFcoarse=s.diag(2,2); pcoherent=s.Matrix([Q(1,2),Q(1,2)])
vcoherent=-G(mu)*K.T*s.Matrix([1,0])
derivatives=[((pcoherent-s.eye(2)[:,i]).T*HFcoarse*vcoherent)[0] for i in range(2)]
check('tangent objective increases one truth loss while decreasing another', derivatives==[Q(1,4),-Q(1,4)])

print(f'\n{len(checks)} exact control groups passed. No floating-point sampling or optimizer used.')
