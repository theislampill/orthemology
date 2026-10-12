import sympy as s
from itertools import product
R=s.Rational
checks=[]
def ck(name, value):
    assert value,name
    checks.append(name)
def eq(a,b):
    d=a-b
    return all(s.simplify(x)==0 for x in d) if isinstance(d,s.MatrixBase) else s.simplify(d)==0
def G(w):
    w=s.Matrix(w); return s.diag(*w)-w*w.T/sum(w)
x,y,z=s.symbols('x y z',positive=True)
w=s.Matrix([x,y,z]); one=s.ones(3,1)
ck('tangent mass',eq(one.T*G(w),s.zeros(1,3)))
ck('tangent duality',eq(s.diag(*[1/a for a in w])*G(w),s.eye(3)-one*w.T/sum(w)))
u,v=s.symbols('u v',positive=True)
ck('binary injectivity numerator',eq(u*z/(u+z)-v*z/(v+z),z*z*(u-v)/((u+z)*(v+z))))
e,l=s.symbols('epsilon lambda',positive=True)
mu=s.Matrix([e*l,e*(1-l),1-e]); p=s.Matrix([e*l*x,e*(1-l)*y,1-e*(l*x+(1-l)*y)])
ck('normalized buffer',s.simplify(sum(mu)-1)==0 and s.simplify(sum(p)-1)==0)
K=s.Matrix([[1,1,0],[0,0,1]])
ck('partition symbolic mobility',eq(K*G(w)*K.T,G(K*w)))
pa=s.Matrix([R(1,100),R(49,100),R(1,2)])
pb=s.Matrix([R(1,4),R(1,4),R(1,2)])
for label,mu,expected in [('root',s.Matrix([1,1,2]),[R(4,9),R(1,2)]),('normalized',s.Matrix([R(1,100),R(1,100),R(49,50)]),[R(14,195),R(7,80)])]:
    ck(label+' same fibre',K*pa==K*pb)
    for p,c in zip([pa,pb],expected):
        w=s.Matrix([s.sqrt(mi*pi) for mi,pi in zip(mu,p)])
        ck(label+' actual collision '+str(c),eq(K*G(w)*K.T,c*s.Matrix([[1,-1],[-1,1]])))
    nu=K*mu;q=K*pa;V=s.Matrix([s.sqrt(mi*pi) for mi,pi in zip(nu,q)])
    ck(label+' canonical equals aligned',eq(G(V),expected[1]*s.Matrix([[1,-1],[-1,1]])))
a,b,t=s.symbols('a b t',positive=True)
phi=((a*t+b)*s.log(a*t+b)-(a*t+b))/a**2
ck('shifted entropy second derivative',eq(s.diff(phi,t,2),1/(a*t+b)))
ck('quadratic second derivative',eq(s.diff(t*t/(2*b),t,2),1/b))
mu=s.Matrix([R(1,5),R(3,10),R(1,2)]);p=pa;w=a*p+b*mu
for cols in product([0,1],repeat=3):
    if len(set(cols))<2:continue
    k=s.Matrix([[int(j==cols[i]) for i in range(3)] for j in range(2)])
    ck('affine deterministic '+str(cols),eq(k*G(w)*k.T,G(a*k*p+b*k*mu)))
k=s.Matrix([[R(3,4),R(1,4),0],[R(1,4),R(3,4),1]])
ck('affine noisy exact difference',eq(G(k*w)-k*G(w)*k.T,s.diag(*(k*w))-k*s.diag(*w)*k.T))
m1,m2,m3,r1,r2,g1,g2=s.symbols('m1 m2 m3 r1 r2 g1 g2',positive=True)
w=s.Matrix([m1*r1,m2*r1,m3*r2]);g=s.Matrix([g1,g2]);fine=-G(w)*K.T*g;coarse=K*fine
ck('aligned-section invariance first',eq(fine[0],m1/(m1+m2)*coarse[0]))
ck('aligned-section invariance second',eq(fine[1],m2/(m1+m2)*coarse[0]))
d1,d2=s.symbols('d1 d2',nonnegative=True)
W=s.Matrix([x,y]);D=s.Matrix([d1,d2]);V=W+D;gg=s.Matrix([u,v])
cW=(W.dot(gg))/sum(W);cV=(V.dot(gg))/sum(V)
rhs=sum(D[i]*(gg[i]-cV)**2 for i in range(2))+sum(W)*(cV-cW)**2
ck('general weight-gap identity',eq((gg.T*(G(V)-G(W))*gg)[0],rhs))
kk=s.Matrix([[R(3,4),R(1,4),0],[R(1,4),R(3,4),1]])
ww=s.Matrix([x,y,z]);var=sum(ww[i]*(sum(kk[j,i]*gg[j]**2 for j in range(2))-(sum(kk[j,i]*gg[j] for j in range(2)))**2) for i in range(3))
ck('channel variance identity',eq((gg.T*(s.diag(*(kk*ww))-kk*s.diag(*ww)*kk.T)*gg)[0],var))
P,Q,MU=s.symbols('P Q MU',positive=True)
ph=lambda tt: ((a*tt+b)*s.log(a*tt+b)-(a*tt+b))/a**2
phprime=s.diff(ph(t),t)
breg=MU*(ph(P/MU)-ph(Q/MU)-phprime.subs(t,Q/MU)*(P-Q)/MU)
wp=a*P+b*MU;wq=a*Q+b*MU
blended=(wp*s.log(wp/wq)-wp+wq)/a**2
ck('affine-blend divergence identity',s.simplify(s.expand_log(breg-blended,force=True))==0)
ck('affine-blend Fisher pullback',eq((a+b*MU)/a**2 * (a/(a+b*MU))**2 / ((a*P+b*MU)/(a+b*MU)),1/(a*P+b*MU)))
print('\n'.join('PASS '+x for x in checks))
print(f'ALL {len(checks)} EXACT CONTROLS PASSED')
