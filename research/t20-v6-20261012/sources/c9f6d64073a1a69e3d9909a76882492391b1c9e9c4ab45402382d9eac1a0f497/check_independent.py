#!/usr/bin/env python3
"""Independent exact finite controls. General proofs are in REVIEW.md."""
import sympy as s
from fractions import Fraction
Q=s.Rational
count=0

def ok(name, condition):
    global count
    if condition is not True and condition != s.true:
        raise AssertionError((name,condition))
    count += 1
    print('PASS',name)

def eq(name,a,b):
    if hasattr(a,'shape'):
        ok(name, a.shape==b.shape and all(s.simplify(c)==0 for c in a-b))
    else: ok(name,s.simplify(a-b)==0)

def G(mu):
    return s.diag(*mu)-mu*mu.T/sum(mu)
def D(p,q,mu): return sum((x-y)**2/w for x,y,w in zip(p,q,mu))/2

p=s.Matrix([Q(3,8),Q(3,8),Q(1,4)])
q=s.Matrix([Q(1,4),Q(1,4),Q(1,2)])
K=s.Matrix([[1,1,0],[0,0,1]])
R=s.Matrix([[Q(1,2),0],[Q(1,2),0],[0,1]])
mu=s.ones(3,1); nu=K*mu
for name,v in [('p',p),('q',q),('mu',mu)]: eq('common reverse recovers '+name,R*K*v,v)
eq('fine half-Brier regret',D(p,q,mu),Q(3,64))
eq('reset coarse half-Brier regret',D(K*p,K*q,s.ones(2,1)),Q(1,16))
eq('transported coarse weighted regret',D(K*p,K*q,nu),Q(3,64))
ok('standard Brier regrets also differ',2*D(p,q,mu)!=2*D(K*p,K*q,s.ones(2,1)))
def expected_half_brier(truth,forecast,ref):
    return sum(truth[i]*D(s.eye(len(truth))[:,i],forecast,ref) for i in range(len(truth)))
eq('fine absolute expected half-Brier score',expected_half_brier(p,q,mu),Q(3,8))
eq('coarse reset absolute expected half-Brier score',expected_half_brier(K*p,K*q,s.ones(2,1)),Q(1,4))
eq('fine Bayes half-Brier score',expected_half_brier(p,p,mu),Q(21,64))
eq('coarse reset Bayes half-Brier score',expected_half_brier(K*p,K*p,s.ones(2,1)),Q(3,16))
eq('coarse transported absolute expected weighted score',expected_half_brier(K*p,K*q,nu),Q(3,16))
ok('pair-divergence equality is not absolute score equality',expected_half_brier(p,q,mu)!=expected_half_brier(K*p,K*q,nu))
# Same two-law reverse does not in general recover an independently selected reference.
mu_unequal=s.Matrix([1,2,1]); nun=K*mu_unequal
eq('unequal-reference fine energy',D(p,q,mu_unequal),Q(11,256))
eq('unequal-reference coarse energy',D(K*p,K*q,nun),Q(1,24))
ok('two-law sufficiency alone does not force weighted equality',D(K*p,K*q,nun)<D(p,q,mu_unequal))
ok('reference recovery fails under the declared reverse',R*K*mu_unequal!=mu_unequal)
eq('deterministic canonical mobility equality',K*G(mu)*K.T,G(nu))
# Noisy, invertible channel contracts and has strictly different tangent mobility.
L=s.Matrix([[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]])
m=s.Matrix([Q(1,2),Q(1,2)]); g=s.Matrix([1,0])
B=L*G(m)*L.T; C=G(L*m)-B
eq('noisy projected velocity',-B*g,s.Matrix([-Q(1,16),Q(1,16)]))
eq('noisy canonical velocity',-G(L*m)*g,s.Matrix([-Q(1,4),Q(1,4)]))
eq('noisy mobility defect',C,Q(3,16)*s.Matrix([[1,-1],[-1,1]]))
ok('invertibility alone does not imply stochastic recoverability',any(x<0 for x in L.inv()))
eq('same-mass normalization commutes',K*(3*p)/sum(3*p),K*(3*p)/sum(K*(3*p)))
# Positive, full mass reference; rank-deficient output image W = span(1,1,-2).
A=s.Matrix([[Q(1,2),0,Q(1,4)],[Q(1,2),0,Q(1,4)],[0,1,Q(1,2)]])
u=s.Matrix([1,2,3]); H=s.diag(*[1/x for x in u]); GG=G(u)
BB=A*GG*A.T; v=s.Matrix([1,1,-2]); pinv=BB.pinv()
h=GG*A.T*pinv*v
z=s.Matrix([-Q(1,2),-Q(1,2),1])
eq('quotient mobility exact rank',BB.rank(),1)
eq('minimum-energy lift is fine tangent',sum(h),0)
eq('minimum-energy lift is feasible',A*h,v)
eq('null perturbation is tangent',sum(z),0)
eq('null perturbation has zero output',A*z,s.zeros(3,1))
eq('least-energy lift is orthogonal to fibre kernel',(h.T*H*z)[0],0)
eq('least energy is pseudoinverse form',(h.T*H*h)[0],(v.T*pinv*v)[0])
eq('quotient energy exact value',(v.T*pinv*v)[0],Q(96,17))
t=s.symbols('t', real=True)
eq('all feasible lifts obey Pythagoras',((h+t*z).T*H*(h+t*z))[0],(v.T*pinv*v)[0]+t*t*(z.T*H*z)[0])
w=s.Matrix([1,-1,0]); eq('unreachable direction is annihilated',BB*w,s.zeros(3,1))
ok('unreachable direction is outside image',BB.row_join(w).rank()>BB.rank())
# A nonorthogonal coordinate re-expression preserves the intrinsic minimum energy.
S=s.Matrix([[1,2,0],[0,1,1],[0,0,2]])
newB=S*BB*S.T; newv=S*v
eq('quotient energy independent of nonorthogonal coordinates',(newv.T*newB.pinv()*newv)[0],(v.T*pinv*v)[0])
eq('least lift independent of nonorthogonal coordinates',GG*A.T*S.T*newB.pinv()*newv,h)
# No arbitrary-convex-generator extension: the quartic reference Bregman gap grows.
p4=s.Matrix([Q(19,100),Q(1,100),Q(4,5)])
q4=s.Matrix([Q(31,100),Q(29,100),Q(2,5)])
def quarticD(p,q,mu):
    return sum(w*((x/w)**4-(y/w)**4-4*(y/w)**3*((x-y)/w)) for x,y,w in zip(p,q,mu))
ok('quartic densities positive',all(x>0 for x in list(p4)+list(q4)))
eq('quartic p coherent',sum(p4),1); eq('quartic q coherent',sum(q4),1)
gap=s.factor(quarticD(K*p4,K*q4,nu)-quarticD(p4,q4,mu))
eq('quartic contraction counterexample gap',gap,Q(921,1562500))
ok('arbitrary weighted Bregman contraction is false',gap>0)
# Global interior preservation is not automatic for a tangent objective flow.
pstart=s.Matrix([Q(1,4),Q(3,4)]); velocity=-G(m)*g
end=pstart+velocity
ok('canonical linear objective reaches boundary at finite time',end[0]==0)
# Equality criterion and covariance defect in a full exact stochastic example.
T=s.Matrix([[Q(1,2),Q(1,3),0],[Q(1,4),Q(1,3),Q(1,4)],[Q(1,4),Q(1,3),Q(3,4)]])
r=s.Matrix([2,3,5]); x=s.Matrix([s.symbols('x0'),s.symbols('x1'),s.symbols('x2')])
CC=G(T*r)-T*G(r)*T.T
variance=sum(r[i]*(sum(T[j,i]*x[j]**2 for j in range(3))-sum(T[j,i]*x[j] for j in range(3))**2) for i in range(3))
eq('variance defect polynomial identity',(x.T*CC*x)[0],variance)
eq('defect annihilates constants',CC*s.ones(3,1),s.zeros(3,1))
eq('defect trace is sum of column impurity',s.trace(CC),sum(r[i]*(1-sum(T[j,i]**2 for j in range(3))) for i in range(3)))
print(f'ALL {count} EXACT INDEPENDENT CONTROLS PASSED')
