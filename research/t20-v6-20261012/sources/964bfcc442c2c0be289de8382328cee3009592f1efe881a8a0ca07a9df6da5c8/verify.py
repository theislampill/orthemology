#!/usr/bin/env python3
"""Exact finite controls, not a solver or a universal proof."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
checks = []

def check(name, condition, detail):
    assert condition, name
    checks.append({'name': name, 'passed': True, 'detail': detail})

def vec(*xs):
    return tuple(F(x) for x in xs)

def scale(a, x):
    return tuple(a*t for t in x)

def add(x, y):
    return tuple(a+b for a,b in zip(x,y))

def mass(x):
    return sum(x, F(0))

def bayes(p, likelihood):
    v = tuple(a*b for a,b in zip(p,likelihood))
    a = mass(v)
    return a, None if a == 0 else scale(1/a,v)

def rref(rows):
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return a, []
    m,n = len(a),len(a[0]); r=0; pivots=[]
    for c in range(n):
        pivot = next((i for i in range(r,m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        s = a[r][c]; a[r]=[x/s for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                s=a[i][c]; a[i]=[x-s*y for x,y in zip(a[i],a[r])]
        pivots.append(c); r+=1
        if r == m:
            break
    return a,pivots

def nullspace(rows):
    rr,pivots=rref(rows)
    n=len(rows[0]); free=[i for i in range(n) if i not in pivots]
    basis=[]
    for f in free:
        v=[F(0)]*n; v[f]=F(1)
        for row,p in zip(rr,pivots):
            v[p]=-row[f]
        basis.append(tuple(v))
    return basis,len(pivots)

# Classical instrument and law/average distinction.
p=vec(F(1,2),F(1,2)); lp=vec(F(3,4),F(1,4)); lm=vec(F(1,4),F(3,4))
a,qp=bayes(p,lp); b,qm=bayes(p,lm)
check('classical identity instrument', add(lp,lm)==vec(1,1) and a==b==F(1,2)
      and qp==lp and qm==lm and add(scale(a,qp),scale(b,qm))==p,
      'Both posteriors differ from the prior, and their weighted mean is the prior.')
check('classical impossible outcome', bayes(vec(1,0),vec(0,1))==(F(0),None),
      'Zero branch mass has no normalized posterior.')

# Scalar branches on a symbolic normalized four-coordinate Bloch state.
rho=vec(1,F(1,4),F(1,3),F(1,5))
for c in [F(0),F(1,4),F(3,4),F(1)]:
    out=scale(c,rho)
    assert out[0]==c
    if c:
        assert scale(1/c,out)==rho
    else:
        assert out==vec(0,0,0,0)
check('scalar and zero branches', True,
      'For c=0,1/4,3/4,1, trace mass is c and normalization is unchanged iff c>0.')

# Mixed classical/PSD summands, with state rho inside the second summand.
w=vec(F(2,5),F(3,5)); coeff=vec(F(3,4),F(1,4))
prob,neww=bayes(w,coeff)
check('mixed direct-sum Bayes weights',prob==F(9,20) and neww==vec(F(2,3),F(1,3)),
      'A R_+ plus Herm_2+ state changes summand weights from (2/5,3/5) to (2/3,1/3).')
second=scale(w[1]*coeff[1],rho)
check('within-summand state retained', scale(1/second[0],second)==rho,
      'The occupied PSD summand keeps its normalized internal state.')

# Fixed-mass feasible cone, including its whole parametric cone on a rational grid.
pr=lambda x:vec(x[1],x[1],0)
ps=lambda x:vec(x[2],0,x[2])
for aa in [F(0),F(1,7),F(1),F(5,2)]:
    for bb in [F(0),F(2,9),F(1),F(3)]:
        x=vec(aa+bb,aa,bb)
        assert add(pr(x),ps(x))==x
        assert pr(pr(x))==pr(x) and ps(ps(x))==ps(x)
        assert pr(ps(x))==ps(pr(x))==vec(0,0,0)
        assert all(t>=0 for t in pr(x)+ps(x))
p=vec(F(1,2),F(1,4),F(1,4)); apr=mass(pr(p)); aps=mass(ps(p))
check('fixed-mass cone instrument',apr==aps==F(1,2)
      and scale(1/apr,pr(p))==vec(F(1,2),F(1,2),0)
      and scale(1/aps,ps(p))==vec(F(1,2),0,F(1,2)),
      'Complementary positive cone projections give the two endpoint states.')
ns,rank=nullspace([[1,-1,0],[1,0,-1]])
check('ambient diagonal preservation is scalar',ns==[vec(1,1,1)] and rank==2,
      'The equations L1=L2 and L1=L3 leave exactly the scalar likelihoods.')
# D_L r = r forces L1=1; D_L s=0 forces L1=0.
aug=[[1,0,0,1],[0,1,0,1],[1,0,0,0],[0,0,1,0]]
rr,piv=rref(aug)
check('no passive projection lift',any(all(x==0 for x in row[:3]) and row[3]!=0 for row in rr),
      'The exact linear system for D_L|V_C=P_r is inconsistent.')
for p in [vec(F(1,2),F(1,4),F(1,4)),vec(F(1,2),F(1,8),F(3,8))]:
    ll=vec(p[1]/p[0],1,0)
    aa,q=bayes(p,ll)
    assert aa==mass(pr(p)) and q==scale(1/aa,pr(p))
check('prior-dependent local splitting',True,
      'The first row changes from (1/2,1,0) to (1/4,1,0) for the two priors.')

# Six Pauli projectors. Use vectors (1,+/-e_k); scaling by 1/2 is irrelevant.
# Unknowns are the 16 real entries of T and six ray eigenvalues a_j.
projectors=[]
for k in range(1,4):
    for sign in [1,-1]:
        v=[F(1),F(0),F(0),F(0)];v[k]=F(sign);projectors.append(v)
eq=[]
for j,v in enumerate(projectors):
    for i in range(4):
        row=[F(0)]*22
        for k in range(4): row[i*4+k]=v[k]
        row[16+j]=-v[i]
        eq.append(row)
ns,rank=nullspace(eq)
identity_solution=tuple(F(int(i==j)) for i in range(4) for j in range(4))+(F(1),)*6
check('six-projector scalar rigidity',rank==21 and ns==[identity_solution],
      'The exact 24 by 22 linear system has nullity one, generated by scalar identity.')

# Hermitian A=(t I+x sigma_x+y sigma_y+z sigma_z)/2.
def determinant(v):
    t,x,y,z=v
    return (t*t-x*x-y*y-z*z)/4
j0=lambda v:vec((v[0]+v[3])/2,0,0,(v[0]+v[3])/2)
j1=lambda v:vec((v[0]-v[3])/2,0,0,-(v[0]-v[3])/2)
px=vec(1,1,0,0); mixed=vec(1,0,0,0)
check('physical measurement changes nonselective state',add(j0(px),j1(px))==mixed and mixed!=px,
      'z measurement sends x-pure input to I/2 while preserving trace.')
check('local fixed state is weaker',add(j0(mixed),j1(mixed))==mixed
      and j0(mixed)[0]==j1(mixed)[0]==F(1,2),
      'The same measurement fixes I/2 without fixing every state.')
diff=add(px,scale(F(-1),j0(px)))
check('domination failure has negative determinant',determinant(diff)==F(-1,4),
      'I-J0 is not positive, with the exact witness determinant -1/4.')

# The square-base cone has rays r1,r2,r3,r4; r4=-r1+r2+r3.
r1=vec(1,1,1);r2=vec(1,1,-1);r3=vec(1,-1,1);r4=vec(1,-1,-1)
assert add(scale(F(-1),r1),add(r2,r3))==r4
# A ray-scaling T in this basis must have t1=t4,t2=t4,t3=t4.
ns,rank=nullspace([[1,0,0,-1],[0,1,0,-1],[0,0,1,-1]])
check('signed extreme-basis support forces a connected component',rank==3 and ns==[vec(1,1,1,1)],
      'The fourth extreme ray uses all three basis coordinates, including a negative coefficient.')

# Direct arithmetic for the nonclosed cone counterexample.
for x in [vec(1,1),vec(F(1,10),7),vec(8,F(1,9))]:
    tx=vec(x[0]/4,3*x[1]/4);sx=vec(3*x[0]/4,x[1]/4)
    assert all(t>0 for t in tx+sx) and add(tx,sx)==x
check('nonclosed-cone branch control',True,
      'The nonscalar diagonal map and its complement preserve the strict quadrant; its indecomposability is proved in RESULT.md.')

# Hashes bind read material. Frozen copies ensure standalone reproducibility.
bind=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for item in bind['inputs']:
    path=HERE/item['snapshot_path']
    blob=path.read_bytes()
    assert len(blob)==item['bytes'] and hashlib.sha256(blob).hexdigest()==item['sha256'],item['snapshot_path']
check('bound input snapshots unchanged',True,
      f"All {len(bind['inputs'])} inspected source snapshots match their bound byte counts and SHA-256 digests.")
result={'status':'pass','check_count':len(checks),'exact_arithmetic':'fractions.Fraction',
        'scope':'Finite calculation checks; universal results are established by written proofs, not enumeration.',
        'checks':checks}
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
for item in checks: print('PASS:',item['name'])
print(f"PASS: {len(checks)} exact control groups")
