import sympy as s
R=s.Rational
M=s.Matrix
def G(w):
 w=M(w); return s.diag(*w)-w*w.T/sum(w)
def eq(a,b): assert s.simplify(a-b)==s.zeros(*a.shape),(a,b)
# An unanchored binary cometric is not injective.
eq(G([1,1]),G([2,R(2,3)]))
# Loewner monotonicity need not be strict for an individual objective.
z=M([0,1,-1]); D=G([2,1,1])-G([1,1,1]); assert D!=s.zeros(3); assert (z.T*D*z)[0]==0
# Independent rational concave-r state with a genuinely noisy channel.
# r=sqrt(t), mu_i=1, density ratios chosen as squares.
mu=M([1,1,1]); p=M([R(1,9),R(4,9),R(4,9)])
K=M([[R(1,2),1,0],[R(1,2),0,1]])
w=M([s.sqrt(p[i]*mu[i]) for i in range(3)]); W=K*w
nu=K*mu; q=K*p; V=M([s.sqrt(nu[i]*q[i]) for i in range(2)])
B=s.diag(*W)-K*s.diag(*w)*K.T
D=G(V)-K*G(w)*K.T
eq(D,(G(V)-G(W))+B)
assert all(s.simplify(V[i]-W[i])>0 for i in range(2))
assert B[0,0]==R(1,12); assert s.simplify(D[0,0])>0
# Noisy channel at p proportional to mu: Jensen term vanishes, noise remains.
p=mu/3; w=M([s.sqrt(p[i]*mu[i]) for i in range(3)]); W=K*w
V=M([s.sqrt((K*mu)[i]*(K*p)[i]) for i in range(2)])
eq(V,W); assert G(V)-K*G(w)*K.T!=s.zeros(2)
# One output: matrix equality is vacuous although Jensen weights differ.
K=M([[1,1]]); mu=M([1,1]); p=M([R(1,5),R(4,5)])
w=M([s.sqrt(p[i]) for i in range(2)]); W=K*w; V=M([s.sqrt(2)])
assert V!=W; eq(G(V),K*G(w)*K.T)
# Concavity is essential to the monotone direction: r=t^2 reverses it.
K=M([[1,1,0],[0,0,1]]); mu=M([1,1,1]); p=M([R(1,10),R(2,5),R(1,2)])
w=M([x*x for x in p]); nu=K*mu; q=K*p; V=M([q[i]**2/nu[i] for i in range(2)])
assert (G(V)-K*G(w)*K.T)[0,0]<0
print('PASS: six independent discriminator groups (exact SymPy).')
