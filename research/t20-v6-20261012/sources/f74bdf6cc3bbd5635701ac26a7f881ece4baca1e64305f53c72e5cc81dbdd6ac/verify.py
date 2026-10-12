"""Exact finite controls and clearly labeled numerical diagnostics.
These checks do not prove the universal C² characterization.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json, math

ROOT=Path(__file__).resolve().parent
checks=[]
def record(name,data): checks.append({'name':name,'status':'pass','details':data})
def norm(v):
    s=sum(v)
    assert s>0
    return tuple(x/s for x in v)
def quad(v):
    # Only use the exact all-active simplex projection in its verified domain.
    q=tuple(x+(1-sum(v))/len(v) for x in v)
    assert all(0<x<1 for x in q)
    return q
def D(x,y): return sum((a-b)**2 for a,b in zip(x,y))/2
def R(p,q):
    return sum(p[j]*D(tuple(Q(int(i==j)) for i in range(len(p))),q) for j in range(len(p)))

# The parent-specified valid two-outcome independent observation.
p=(Q(3,4),Q(1,4)); raw=tuple(x/2 for x in p); q=quad(raw)
assert q==(Q(5,8),Q(3,8))
assert R(p,p)==Q(3,16) and R(p,q)==Q(13,64)
assert R(p,q)-R(p,p)==Q(1,64)
gains=[]
for e in [(Q(1),Q(0)),(Q(0),Q(1))]:
    gains.append(D(e,raw)-D(e,q))
assert gains==[Q(1,16),Q(1,16)] and D(q,raw)==Q(1,16)
record('valid independent-channel quadratic countermodel',{
    'prior_risk':str(R(p,p)), 'updated_risk':str(R(p,q)),
    'implementation_regret':str(R(p,q)-R(p,p)),
    'each_state_repair_gain':str(gains[0])})

# A distinct negative control: weak composition itself fails for quadratic.
b=(Q(1,4),Q(1,4)); L=(Q(1,2),Q(1))
left=quad(tuple(x*l for x,l in zip(quad(b),L)))
right=quad(tuple(x*l for x,l in zip(b,L)))
assert left==(Q(3,8),Q(5,8)) and right==(Q(7,16),Q(9,16)) and left!=right
record('quadratic fails restricted weak contract',{'left':list(map(str,left)),'right':list(map(str,right))})

# Exact normalization equivariance and null-event neutrality over a finite grid.
count=0
for n in [2,3]:
    for b in product([Q(1,5),Q(2,5),Q(3,5)],repeat=n):
        for L in product([Q(1,4),Q(1,2),Q(3,4)],repeat=n):
            lb=tuple(x*l for x,l in zip(b,L))
            lp=tuple(x*l for x,l in zip(norm(b),L))
            assert norm(lb)==norm(lp)
            assert norm(tuple(x/3 for x in b))==norm(b)
            count+=1
record('normalization finite exact contract controls',{'cases':count})

# Exact proper-score decomposition and information-minus-regret over valid channels.
channels=0
for prior1 in [Q(1,4),Q(1,2),Q(3,4)]:
    p=(prior1,1-prior1)
    for l1,l2 in product([Q(1,4),Q(1,2),Q(3,4)],repeat=2):
        ls=[(l1,l2),(1-l1,1-l2)]
        ms=[sum(x*l for x,l in zip(p,L)) for L in ls]
        ps=[norm(tuple(x*l for x,l in zip(p,L))) for L in ls]
        reports=[quad(tuple(x*l for x,l in zip(p,L))) for L in ls]
        assert tuple(sum(m*r[i] for m,r in zip(ms,ps)) for i in [0,1])==p
        information=sum(m*D(r,p) for m,r in zip(ms,ps))
        regret=sum(m*D(r,q) for m,r,q in zip(ms,ps,reports))
        measured=R(p,p)-sum(m*R(r,q) for m,r,q in zip(ms,ps,reports))
        assert measured==information-regret
        raw=tuple(x/2 for x in p)
        # Use raw whose quadratic projection p_raw actually supplies the declared prior.
        p_raw=quad(raw)
        ms2=[sum(x*l for x,l in zip(p_raw,L)) for L in ls]
        ps2=[norm(tuple(x*l for x,l in zip(p_raw,L))) for L in ls]
        qs2=[quad(tuple(x*l for x,l in zip(p_raw,L))) for L in ls]
        lhs=R(p_raw,raw)-sum(m*R(r,q) for m,r,q in zip(ms2,ps2,qs2))
        rhs=D(p_raw,raw)+sum(m*(D(r,p_raw)-D(r,q)) for m,r,q in zip(ms2,ps2,qs2))
        assert lhs==rhs
        channels+=1
record('proper scoring and three-credit decomposition',{'exact_channels':channels})

# Exact duplicate-root transport: one root copied twice, not two independent signals.
p=(Q(1,2),Q(1,2)); root=(Q(4,5),Q(1,5))
correct=norm(tuple(x*l for x,l in zip(p,root)))
naive=norm(tuple(x*l*l for x,l in zip(p,root)))
sequential=norm(tuple(x*Q(1) for x in correct))
assert correct==(Q(4,5),Q(1,5)) and naive==(Q(16,17),Q(1,17))
assert sequential==correct and naive!=correct
record('exact duplicate-root countermodel',{'correct':list(map(str,correct)),'naive':list(map(str,naive)),
    'half_brier_regret':str(D(correct,naive))})

# Exact algebra in Q(sqrt(17)) for the weighted-entropy null-event example.
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y): return (x[0]*y[0]+17*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
q1=(Q(9,8),Q(-1,8));q2=(Q(-1,8),Q(1,8))
assert add(q1,q2)==(Q(1),Q(0))
assert q1==mul((Q(4),Q(0)),mul(q2,q2))
assert q1!=(Q(1,2),Q(0)) and q2!=(Q(1,2),Q(0))
# Positivity and <1 follow from 1<sqrt17<5 and 3<sqrt17<5, all checked by squaring.
assert 1<17<25 and 9<17<25
record('weighted-entropy exact unequal-neutrality countermodel',{
    'q1':'(9-sqrt(17))/8','q2':'(sqrt(17)-1)/8','relations':'sum=1, q1=4*q2^2, q!=prior'})

# Weighted composition: diagnostic floating-point replay, explicitly not a universal proof.
def weighted(v,weights):
    def total(lam): return sum(x*math.exp(lam/w) for x,w in zip(v,weights))
    lo,hi=-1.0,1.0
    while total(lo)>1:lo*=2
    while total(hi)<1:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if total(mid)<1:lo=mid
        else:hi=mid
    lam=(lo+hi)/2
    return tuple(x*math.exp(lam/w) for x,w in zip(v,weights))
max_error=0.0; diagnostic_count=0
for weights in [(1.,2.),(1.,2.,3.)]:
    n=len(weights)
    for b in product([.1,.2,.6],repeat=n):
        for L in product([.2,.7],repeat=n):
            pb=weighted(b,weights)
            lhs=weighted(tuple(x*l for x,l in zip(pb,L)),weights)
            rhs=weighted(tuple(x*l for x,l in zip(b,L)),weights)
            error=max(abs(x-y) for x,y in zip(lhs,rhs))
            assert error<2e-14
            max_error=max(max_error,error);diagnostic_count+=1
record('weighted composition numerical diagnostic',{'cases':diagnostic_count,'max_abs_error':max_error,'proof_status':'diagnostic_only'})

# Source bytes retained through the connector are checked against Git's own blob hashes.
bindings=json.loads((ROOT/'sources/SOURCE_BINDINGS.json').read_text())
for item in bindings:
    data=(ROOT/'sources'/item['path']).read_bytes()
    got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got==item['sha'],(item['path'],got,item['sha'])
record('pinned source-byte verification',{'files':len(bindings),'hash':'Git SHA-1 blob framing'})

out={'status':'pass','universal_proof':'written proofs in RESULT.md; finite checks are not universal proof',
     'checks':checks}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
