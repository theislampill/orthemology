#!/usr/bin/env python3
"""Independent, deterministic adversarial probes. Does not import or mutate the reviewed code.
Finite tests are checks, not a proof over all expressions or all model sizes.
"""
from dataclasses import dataclass
from itertools import product
from fractions import Fraction
from functools import lru_cache
from collections import Counter
from pathlib import Path
import random, json, hashlib

COUNTS=Counter()
def check(family, left, right):
    assert left == right, (family, left, right)
    COUNTS[family]+=1

def cube(d,n): return tuple(product(range(d), repeat=n))
@dataclass(frozen=True)
class E:
    op: str
    args: tuple=()
    n: int=0
    name: str=''

def atom(name,n): return E('atom',n=n,name=name)
def unary(op,a):
    return E(op,(a,),max(a.n-1,0) if op=='c' else a.n+1 if op=='p' else a.n)
def meet(a,b): return E('&',(a,b),max(a.n,b.n))
I=E('I',n=2)
ATOMS=(atom('Z',0),atom('F',1),atom('G',1),atom('R',2),atom('H',3),I)

def source(t,d,model,seq):
    """Direct completed Appendix sequence semantics; no set-valued intermediate tables."""
    if t.op=='atom': return seq[:t.n] in model[t.name]
    if t.op=='I': return seq[0]==seq[1]
    if t.op=='&': return source(t.args[0],d,model,seq) and source(t.args[1],d,model,seq)
    a=t.args[0]
    if t.op=='~': return not source(a,d,model,seq)
    if t.op=='c':
        return source(a,d,model,seq) if a.n==0 else any(source(a,d,model,(x,)+seq) for x in range(d))
    if t.op=='p': return source(a,d,model,seq[1:])
    if t.op=='i':
        env=seq if a.n<2 else (seq[1],seq[0])+seq[2:]
        return source(a,d,model,env)
    if t.op=='s':
        env=seq if a.n<2 else (seq[a.n-1],)+seq[:a.n-1]+seq[a.n:]
        return source(a,d,model,env)
    raise ValueError(t)

def evaluate(t,d,model,kind='B',weights=None):
    """Dense coefficient evaluator; weighted N/Fraction path uses a zero-test at negation."""
    @lru_cache(None)
    def ev(e):
        xs=cube(d,e.n)
        if e.op=='atom':
            return {x:(weights[e.name][x] if weights is not None else int(x in model[e.name])) for x in xs}
        if e.op=='I': return {x:int(x[0]==x[1]) for x in xs}
        a=e.args[0]; v=ev(a)
        if e.op=='&':
            b=e.args[1]; w=ev(b)
            return {x:v[x[:a.n]]*w[x[:b.n]] for x in xs}
        if e.op=='~': return {x:int(v[x]==0) for x in xs}
        if e.op=='c':
            if a.n==0: return dict(v)
            if kind=='B': return {x:int(any(v[(y,)+x] for y in range(d))) for x in xs}
            return {x:sum(v[(y,)+x] for y in range(d)) for x in xs}
        if e.op=='p': return {x:v[x[1:]] for x in xs}
        if e.op=='i': return {x:v[x if e.n<2 else (x[1],x[0])+x[2:]] for x in xs}
        if e.op=='s': return {x:v[x if e.n<2 else x[-1:]+x[:-1]] for x in xs}
        raise ValueError(e)
    return ev(t)

# All Boolean primitive tables on D=2 at arities 0..3.
for n in range(4):
    a=atom('A',n); xs=cube(2,n)
    for bits in product((0,1),repeat=len(xs)):
        model={'A':frozenset(x for x,v in zip(xs,bits) if v)}
        for op in ('~','c','p','i','s'):
            t=unary(op,a); array=evaluate(t,2,model)
            for x in cube(2,t.n):
                for tail in ((0,)*10,(1,)*10):
                    check('primitive_vs_sequence',array[x],int(source(t,2,model,x+tail)))

# All mixed arities 0..2, independent sequence oracle.
for n,m in product(range(3), repeat=2):
    a,b=atom('A',n),atom('B',m); t=meet(a,b)
    for av in product((0,1),repeat=2**n):
        for bv in product((0,1),repeat=2**m):
            model={'A':frozenset(x for x,v in zip(cube(2,n),av) if v),'B':frozenset(x for x,v in zip(cube(2,m),bv) if v)}
            arr=evaluate(t,2,model)
            for x in cube(2,t.n): check('mixed_arity_vs_sequence',arr[x],int(source(t,2,model,x+(0,)*10)))

rng=random.Random(20261008)
def generated(depth):
    if depth==0 or rng.random()<.18: return rng.choice(ATOMS)
    op=rng.choice(('~','c','p','i','s','&'))
    a=generated(depth-1)
    if op=='&': return meet(a,generated(depth-1))
    if op=='p' and a.n>=4: op='c'
    return unary(op,a)

# Deliberate scalar, repeated projection, mixed-arity, nested-negation and identity expressions.
terms=list(ATOMS)+[generated(7) for _ in range(900)]
terms += [unary('c',unary('c',meet(ATOMS[3],I))),
          unary('~',unary('c',unary('~',ATOMS[1]))),
          unary('c',unary('p',ATOMS[0])),
          unary('s',unary('i',ATOMS[4]))]
for d in (1,2,3):
    for model_number in range(6):
        weighted={a.name:{x:Fraction(rng.randrange(5),rng.randrange(1,4)) for x in cube(d,a.n)} for a in ATOMS if a.op=='atom'}
        model={k:frozenset(x for x,v in vals.items() if v) for k,vals in weighted.items()}
        for t in terms:
            b=evaluate(t,d,model); n=evaluate(t,d,model,kind='Qnonnegative',weights=weighted)
            for x in cube(d,t.n):
                truth=int(source(t,d,model,x+(0,)*16))
                check('composite_sequence_B',b[x],truth)
                check('composite_positive_support_zero_test',int(n[x]>0),truth)
                check('completed_prefix_locality',source(t,d,model,x+(0,)*16),source(t,d,model,x+(d-1,)*16))

# Universal truth of an open predicate differs from existential closure.
F=ATOMS[1]; G=ATOMS[2]; R=ATOMS[3]
model={'F':frozenset({(0,)})}
farr=evaluate(F,2,model)
check('open_truth_is_universal',int(all(farr.values())),0)
check('existential_closure_is_different',evaluate(unary('c',F),2,model)[()],1)

# Literal unary iota does not preserve the declared first-slot locality.
literal_iota=lambda seq:int(seq[1]==0)
check('literal_unary_iota_nonlocal',[literal_iota((0,0)),literal_iota((0,1))],[1,0])
check('completed_unary_iota_local',[evaluate(unary('i',F),2,model)[(0,)]]*2,[1,1])
# A syntactically closed term c(i(F)) can also retain an environmental dependency
# under the literal clause; completing before induction is necessary, not cosmetic.
literal_closed=lambda seq:int(any(literal_iota((x,)+seq) for x in (0,1)))
check('literal_closed_term_nonlocal',[literal_closed((0,0)),literal_closed((1,0))],[1,0])

# Boundaries outside the source's nonempty-domain class.
one=atom('One',0); empty_model={'One':frozenset({()})}
check('empty_domain_scalar_unit',evaluate(one,0,empty_model),{():1})
check('empty_domain_scalar_c_identity',evaluate(unary('c',one),0,empty_model),{():1})
check('empty_domain_padding_exists_failure',evaluate(unary('c',unary('p',one)),0,empty_model),{():0})
check('empty_domain_universal_vacuity',evaluate(unary('~',unary('c',unary('~',unary('p',one)))),0,empty_model),{():1})

# Source orientation, shared witnesses, and plurality.
term=unary('c',unary('c',meet(meet(meet(F,unary('p',G)),R),unary('~',I))))
records=[]; results=[]
for edge in ((0,1),(1,0)):
    model={'F':frozenset({(0,)}),'G':frozenset({(1,)}),'R':frozenset({edge})}
    record=tuple(evaluate(unary('c',a) if a.n==1 else unary('c',unary('c',a)),2,model)[()] for a in (F,G,R))
    records.append(record); results.append(evaluate(term,2,model)[()])
    check('separate_shared_witness',evaluate(unary('c',meet(F,G)),2,model)[()],0)
    check('independent_witnesses',evaluate(unary('c',F),2,model)[()]*evaluate(unary('c',G),2,model)[()],1)
check('source_scalar_record_collision',records,[(1,1,1),(1,1,1)])
check('source_joint_target_separates',results,[1,0])
plural=unary('c',unary('c',meet(meet(F,unary('p',F)),unary('~',I))))
for d in range(5):
    model={'F':frozenset(cube(d,1))}
    check('plurality_B',evaluate(plural,d,model)[()],int(d>=2))
    check('plurality_N',evaluate(plural,d,model,'N')[()],d*(d-1))

# Full equality networks: arbitrary weights, repeated / unused output slots,
# including the unique nullary-to-nullary map and zero-coordinate domains.
for d in (0,1,2,3):
    for n,k in product(range(4),repeat=2):
        table={x:Fraction(rng.randrange(8),3) for x in cube(d,n)}
        for alpha in product(range(k),repeat=n):
            for x in cube(d,k):
                direct=table[tuple(x[i] for i in alpha)]
                network=sum(table[y]*int(all(y[j]==x[alpha[j]] for j in range(n))) for y in cube(d,n))
                check('equality_wire_arbitrary_nonnegative',network,direct)

# Signed obstruction and exact basis transport. Fractions avoid numerical cancellation artefacts.
check('signed_support_cancellation',int(sum((1,-1))!=0),0)
check('signed_boolean_projection',int(any(x!=0 for x in (1,-1))),1)
check('positive_part_not_multiplicative',int((-1)*(-1)>0),1)
check('positive_part_factors_false',int(-1>0)*int(-1>0),0)
g=((1,0),(-1,1)); gi=((1,0),(1,1)); v=(1,0)
new=tuple(sum(g[i][j]*v[j] for j in range(2)) for i in range(2))
epsnew=tuple(sum(gi[i][j] for i in range(2)) for j in range(2))
check('basis_inverse',tuple(tuple(sum(g[i][k]*gi[k][j] for k in range(2)) for j in range(2)) for i in range(2)),((1,0),(0,1)))
check('basis_frozen_epsilon_wrong',sum(new),0)
check('basis_transported_epsilon_right',sum(epsnew[j]*new[j] for j in range(2)),1)

# Truth-wire networks evaluated by literal tensor-index summation, including NOT and copy.
def rail(b): return (int(b==0),int(b==1))
def gate(fn,inputs):
    r=len(inputs)
    return tuple(int(any(all(inputs[j][a[j]] for j in range(r)) and b==fn(*a) for a in product((0,1),repeat=r))) for b in (0,1))
for bits in product((0,1),repeat=5):
    rails=list(map(rail,bits))
    # Nonmonotone nested circuit: NOT ((x0 AND x1) OR (NOT x2 AND x3) OR x4).
    x01=gate(lambda a,b:a and b,rails[:2]); not2=gate(lambda a:1-a,[rails[2]])
    x23=gate(lambda a,b:a and b,[not2,rails[3]])
    disj=gate(lambda a,b,c:a or b or c,[x01,x23,rails[4]])
    out=gate(lambda a:1-a,[disj])
    want=int(not ((bits[0] and bits[1]) or ((not bits[2]) and bits[3]) or bits[4]))
    check('nested_truth_wire_circuit',out,rail(want))
for b in (0,1):
    copied={(i,j):int(any(rail(b)[k] and k==i==j for k in (0,1))) for i,j in product((0,1),repeat=2)}
    check('truth_wire_copy',copied,{(i,j):int(i==b and j==b) for i,j in product((0,1),repeat=2)})

out={'status':'PASS','seed':20261008,'total_assertions':sum(COUNTS.values()),'assertions_by_family':dict(sorted(COUNTS.items())),'expressions':len(terms),'composite_models':18,'independence':'No import from reviewed controls.py; direct completed source sequence semantics vs dense weighted arrays.','boundary':'Finite checks only. General all-syntax warrant is the structural induction in REVIEW.md.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('INDEPENDENT_PROBE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
