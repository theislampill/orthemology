"""Independent rational controls for catalogue sampling and reviewer extensions."""
from fractions import Fraction as F
from math import comb, factorial
import random


def det(rows):
    a=[[F(x) for x in row] for row in rows]; out=F(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None: return F(0)
        if p!=j: a[p],a[j]=a[j],a[p];out=-out
        v=a[j][j];out*=v
        for i in range(j+1,len(a)):
            c=a[i][j]/v
            for k in range(j+1,len(a)):a[i][k]-=c*a[j][k]
    return out


def solve(a,b):
    den=det(a);assert den
    return [det([[b[i] if j==col else a[i][j] for j in range(len(a))] for i in range(len(a))])/den for col in range(len(a))]


def binomial(z,R): return [comb(R,s)*z**s*(1-z)**(R-s) for s in range(R+1)]
def mean(b,p):return sum(x*y for x,y in zip(b,p))
def poisson_binomial(theta):
    p=[F(1)]
    for t in theta:
        out=[F(0)]*(len(p)+1)
        for s,v in enumerate(p):out[s]+=v*(1-t);out[s+1]+=v*t
        p=out
    return p


def contrast_rows(nodes):
    R=len(nodes)-1
    # Directly invert the matrix of complete binomial count probabilities.
    matrix=[binomial(z,R) for z in nodes]
    return [solve(matrix,[F(i==j) for j in range(len(nodes))]) for i in range(len(nodes))]


def exp_upper(x,M=40):
    # The positive Taylor remainder has successive-term ratio <=x/(M+2).
    assert 0<=x<M+2
    partial=sum(x**k/factorial(k) for k in range(M+1))
    return partial+x**(M+1)/factorial(M+1)/(1-x/F(M+2))


def run():
    rng=random.Random(6401); catalogues=[]
    for N in range(1,6):
        for _ in range(4):
            js=sorted(rng.sample(range(9),N))
            nodes=[F(3,4)**j for j in js]
            rows=contrast_rows(nodes);R=N-1
            assert all(sum(b[s] for b in rows)==1 for s in range(R+1))
            for i,b in enumerate(rows):
                assert [mean(b,binomial(z,R)) for z in nodes]==[F(i==j) for j in range(N)]
                D=R*max((abs(b[s+1]-b[s]) for s in range(R)),default=F(0))
                for z in (F(0),F(1,7),F(1,2),F(1)):
                    derivative=R*mean([b[s+1]-b[s] for s in range(R)],binomial(z,R-1)) if R else F(0)
                    assert abs(derivative)<=D
            catalogues.append((nodes,rows))
    print('PASS 20 catalogues independently inverted from complete binomial probability matrices')

    controls=0
    for nodes,rows in catalogues:
        R=len(nodes)-1
        if not R:continue
        for j,z in enumerate(nodes):
            for trial in range(3):
                theta=[min(F(1),max(F(0),z+F(rng.randrange(-5,6),100))) for _ in range(R)]
                p=poisson_binomial(theta)
                coordinate_error=sum(abs(t-z) for t in theta)
                assert sum(p)==1 and min(p)>=0
                for i,b in enumerate(rows):
                    c=max(abs(b[s+1]-b[s]) for s in range(R))
                    nominal=F(i==j)
                    assert abs(mean(b,p)-nominal)<=c*coordinate_error
                    assert c*coordinate_error<=R*c*max(abs(t-z) for t in theta)
                controls+=1
    assert F(1,2)*F(1)!=F(3,4)**2
    print(f'PASS {controls} nonidentical-propensity groups: exact Poisson-binomial expectation and adjacent-difference bias bound')

    tv_controls=0
    rho=F(1,11)
    for nodes,rows in catalogues:
        R=len(nodes)-1
        if not R:continue
        z=nodes[-1]
        theta=[max(F(0),z-F(s+1,200)) for s in range(R)]
        p=poisson_binomial(theta)
        q=[(1-rho)*v+rho*F(s==R) for s,v in enumerate(p)]
        tv=sum(abs(v-w) for v,w in zip(p,q))/2
        assert tv<=rho
        for i,b in enumerate(rows):
            B=max(b)-min(b);c=max(abs(b[s+1]-b[s]) for s in range(R))
            assert abs(mean(b,q)-mean(b,p))<=B*tv<=B*rho
            assert abs(mean(b,q)-F(i==len(nodes)-1))<=c*sum(abs(t-z) for t in theta)+B*rho
            tv_controls+=1
    print(f'PASS {tv_controls} joint-law contamination controls: oscillation-times-TV bias plus calibration bias')

    tails=0
    for n in (16,32,64):
        for theta in (F(1,4),F(1,2),F(3,4)):
            probabilities=binomial(theta,n)
            for t in (F(1,4),F(1,3),F(1,2)):
                tail=sum(p for s,p in enumerate(probabilities) if abs(F(s,n)-theta)>=t)
                alpha=2*n*t*t
                lower_for_hoeffding=2/exp_upper(alpha,80)
                assert tail<=lower_for_hoeffding
                tails+=1
    print(f'PASS {tails} exact finite binomial tails against rigorously bounded Hoeffding expressions')

    nodes=[F(1),F(3,4),F(9,16)];rows=contrast_rows(nodes)
    Bs=[max(b)-min(b) for b in rows]
    Ds=[2*max(abs(b[s+1]-b[s]) for s in range(2)) for b in rows]
    assert Bs==[F(6),F(50,3),F(32,3)] and Ds==[F(12),F(100,3),F(64,3)]
    assert sum(F(5**k,factorial(k)) for k in range(8))>120
    for B,D in zip(Bs,Ds):
        assert B*B*F(5,80000)<(F(1,6)-D/1000)**2
        assert B*B*F(5,80000)<(F(1,6)-D/1000-B/F(20000))**2
    assert F(1,6)-max(Ds)/1000-max(Bs)/20000==F(53,400)
    # Small-budget full two-group endpoint-count law, retaining the two counts.
    eta=F(1,4**8);R=3;weights=[F(1,2)]*2
    base=[sum(w*p[s] for w,p in zip(weights,[binomial(z,R) for z in nodes[1:]])) for s in range(R+1)]
    shifted=[sum(w*p[s] for w,p in zip(weights,[binomial(z*(1-eta),R) for z in nodes[1:]])) for s in range(R+1)]
    tv=sum(abs(base[s]*base[t]-shifted[s]*shifted[t]) for s in range(R+1) for t in range(R+1))/2
    assert 0<tv<=2*R*eta
    print('PASS 40000-group budget, added conditional joint-TV allowance 1/20000, and two-group rare-route TV control')
    print('ALL 5 INDEPENDENT CONTROL FAMILIES PASSED')

if __name__=='__main__':run()
