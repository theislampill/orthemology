"""Independent exact controls. Standard library only; finite checks, not proofs."""
from fractions import Fraction as F
from math import comb
from itertools import permutations
import random


def det(rows):
    a = [[F(v) for v in row] for row in rows]
    d = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            d = -d
        pivot = a[j][j]
        d *= pivot
        for i in range(j+1, len(a)):
            ratio = a[i][j] / pivot
            for t in range(j+1, len(a)):
                a[i][t] -= ratio * a[j][t]
    return d


def cramer(a, b):
    denominator = det(a)
    assert denominator
    return [det([[b[i] if j == col else a[i][j] for j in range(len(a))]
                 for i in range(len(a))]) / denominator for col in range(len(a))]


def moment(law, r):
    return sum(w*z**r for z, w in law)


def count_law(law, R):
    return [comb(R,t)*sum(w*z**t*(1-z)**(R-t) for z,w in law) for t in range(R+1)]


def signed_minor_pair(nodes):
    # Compute the kernel by signed maximal minors, rather than reciprocal products.
    rows = [[z**r for z in nodes] for r in range(len(nodes)-1)]
    c = [(-1)**j*det([row[:j]+row[j+1:] for row in rows]) for j in range(len(nodes))]
    assert all(v for v in c)
    if c[0] < 0:
        c = [-v for v in c]
    for row in rows:
        assert sum(x*y for x,y in zip(row,c)) == 0
    norm = sum(v for v in c if v > 0)
    pos = [(z,v/norm) for z,v in zip(nodes,c) if v>0]
    neg = [(z,-v/norm) for z,v in zip(nodes,c) if v<0]
    assert sum(w for z,w in pos)==sum(w for z,w in neg)==1
    return pos, neg


def code(hist):
    q=F(1)
    for e,n in hist.items():
        q *= (1-F(1,4**e))**n
    return q


def pair_independent(q,r):
    return [q*r,q*(1-r),(1-q)*r,(1-q)*(1-r)]


def run():
    for k in range(1,7):
        nodes=[F(3,4)**j for j in range(1,2*k+1)]
        A,B=signed_minor_pair(nodes)
        assert len(A)==len(B)==k
        assert all(0<z<1 and w>0 for z,w in A+B)
        assert count_law(A,2*k-2)==count_law(B,2*k-2)
        assert moment(A,2*k-1)!=moment(B,2*k-1)
        A,B=signed_minor_pair(nodes+[F(3,4)**(2*k+1)])
        assert sorted((len(A),len(B)))==[k,k+1]
        assert count_law(A,2*k-1)==count_law(B,2*k-1)
        assert moment(A,2*k)!=moment(B,2*k)
    print('PASS 12 signed-minor sharpness witnesses; all components nonempty; complete count laws agree')

    rng=random.Random(8247)
    completed=0
    for s in range(1,5):
        for trial in range(9):
            nodes=set()
            while len(nodes)<s:
                nodes.add(code({e:rng.randrange(3) for e in range(1,5)}))
            nodes=sorted(nodes)
            raw=[rng.randrange(1,8) for _ in nodes]
            law=list(zip(nodes,[F(w,sum(raw)) for w in raw]))
            m=[moment(law,r) for r in range(2*s+1)]
            for t in range(s):
                assert det([[m[i+j] for j in range(t+1)] for i in range(t+1)])>0
            assert det([[m[i+j] for j in range(s+1)] for i in range(s+1)])==0
            p=cramer([[m[i+j] for j in range(s)] for i in range(s)],[-m[i+s] for i in range(s)])+[F(1)]
            assert all(sum(c*z**i for i,c in enumerate(p))==0 for z in nodes)
            assert sum(p[i]*p[j]*m[i+j] for i in range(s+1) for j in range(s+1))==0
            recovered=cramer([[z**r for z in nodes] for r in range(s)],m[:s])
            assert recovered==[w for z,w in law]
            R=2*s
            counts=count_law(law,R)
            assert sum(counts)==1 and min(counts)>=0
            for r in range(R+1):
                assert sum(F(comb(t,r),comb(R,r))*counts[t] for t in range(r,R+1))==m[r]
            # Any nonroot actual code has a strictly positive squared annihilator.
            z=F(3,4)
            while z in nodes:
                z*=F(3,4)
            assert sum(c*z**i for i,c in enumerate(p))**2>0
            completed+=1
    print('PASS 36 independently generated mixtures: determinant stopping, Cramer annihilator/weights, factorial-count reconstruction')

    stationary=0
    for s in range(2,6):
        nodes=[F(3,4)**j for j in range(s)]
        perms=list(permutations(range(s)))
        for trial in range(8):
            chosen=rng.sample(perms,min(4,len(perms)))
            ws=[rng.randrange(1,6) for _ in chosen]
            transitions={}
            for perm,w in zip(chosen,ws):
                for i,j in enumerate(perm):
                    transitions[i,j]=transitions.get((i,j),F(0))+F(w,s*sum(ws))
            assert all(sum(w for (i,j),w in transitions.items() if i==a)==F(1,s) for a in range(s))
            assert all(sum(w for (i,j),w in transitions.items() if j==a)==F(1,s) for a in range(s))
            m2=sum(z*z for z in nodes)/s
            cross=sum(w*nodes[i]*nodes[j] for (i,j),w in transitions.items())
            sq=sum(w*(nodes[i]-nodes[j])**2 for (i,j),w in transitions.items())
            changed=sum(w for (i,j),w in transitions.items() if i!=j)
            gap=min(abs(a-b) for a in nodes for b in nodes if a!=b)
            assert sq==2*(m2-cross) and changed<=min(1,sq/gap**2)
            stationary+=1
    print('PASS 32 stationary permutation-mixture transitions: square identity and discrete change bound')

    # Stronger removal-of-stationarity witness: even the complete observed pair law
    # and equal observable one-time marginals imitate persistence at q=3/4.
    q=F(3,4); successors=[(F(1),F(3,7)),(F(9,16),F(4,7))]
    assert moment(successors,1)==q
    observed=[sum(w*pair_independent(q,r)[j] for r,w in successors) for j in range(4)]
    assert observed==pair_independent(q,q)==[F(9,16),F(3,16),F(3,16),F(1,16)]
    first_m2=q*q; second_m2=moment(successors,2)
    cross=sum(w*q*r for r,w in successors)
    square=sum(w*(q-r)**2 for r,w in successors)
    assert first_m2==cross==F(9,16)
    assert second_m2==F(39,64) and square==F(3,64)
    assert all(r!=q for r,w in successors)
    print('PASS stronger nonstationarity counterfeit: whole pair (9,3,3,1)/16; equal observable marginals; histogram changes always')
    print('  first m2=c=9/16; second m2=39/64; squared scalar change=3/64')

    a,b=F(3,4),F(9,16)
    ab=[F(v,512) for v in (225,159,63,65)]
    ba=[ab[0],ab[2],ab[1],ab[3]]
    observed=[(x+y)/2 for x,y in zip(ab,ba)]
    persistent=[(x+y)/2 for x,y in zip(pair_independent(a,a),pair_independent(b,b))]
    assert observed==persistent==[F(v,512) for v in (225,111,111,65)]
    assert ab[0]+ab[1]==a and ab[0]+ab[2]==b and ab!=pair_independent(a,b)
    print('PASS independent corroboration of the stationary correlated-emission counterfeit')
    print('ALL 5 INDEPENDENT CONTROL FAMILIES PASSED')

if __name__=='__main__':
    run()
