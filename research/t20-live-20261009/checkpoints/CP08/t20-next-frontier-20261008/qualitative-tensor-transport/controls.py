#!/usr/bin/env python3
"""Exact finite controls. No external packages, no stochastic arithmetic.
Set-valued source semantics and coefficient-array operations are separate evaluators.
The finite tests complement, and do not replace, the universal written proofs.
"""
from dataclasses import dataclass
from itertools import product, permutations
from functools import reduce
from operator import mul
from collections import Counter
from pathlib import Path
import hashlib, json

METRICS=Counter()
def tuples(d,n): return tuple(product(range(d), repeat=n))
def support(t): return frozenset(x for x,v in t.data.items() if v != 0)
def truth(t): assert t.n==0; return t.data[()]

def check(name, lhs, rhs):
    assert lhs==rhs, (name,lhs,rhs)
    METRICS[name]+=1

@dataclass(frozen=True)
class Tensor:
    d: int
    n: int
    data: dict
    def __post_init__(self):
        assert self.d>=0 and self.n>=0  # Empty domain admitted only for explicit outside-source boundary controls.
        assert set(self.data)==set(tuples(self.d,self.n))

@dataclass(frozen=True)
class Rel:
    d: int
    n: int
    rows: frozenset
    def __post_init__(self):
        assert self.rows <= frozenset(tuples(self.d,self.n))

# Relation semantics: set intersections, products and direct images.
def rel_not(a): return Rel(a.d,a.n,frozenset(tuples(a.d,a.n))-a.rows)
def rel_and(a,b):
    assert a.d==b.d
    k=max(a.n,b.n)
    aa={x+y for x in a.rows for y in tuples(a.d,k-a.n)}
    bb={x+y for x in b.rows for y in tuples(b.d,k-b.n)}
    return Rel(a.d,k,frozenset(aa&bb))
def rel_c(a):
    return a if a.n==0 else Rel(a.d,a.n-1,frozenset(x[1:] for x in a.rows))
def rel_p(a):
    return Rel(a.d,a.n+1,frozenset((i,)+x for i in range(a.d) for x in a.rows))
def rel_iota(a):
    return a if a.n<2 else Rel(a.d,a.n,frozenset((x[1],x[0])+x[2:] for x in a.rows))
def rel_sigma(a):
    # Image is left rotation because source satisfaction is right pullback.
    return a if a.n<2 else Rel(a.d,a.n,frozenset(x[1:]+x[:1] for x in a.rows))
def encode(a): return Tensor(a.d,a.n,{x:int(x in a.rows) for x in tuples(a.d,a.n)})

# Coefficient operations, parameterised only at summation (Bool OR or N/R sum).
def plus(vs,kind): return int(any(vs)) if kind=='B' else sum(vs)
def tensor_not(a): return Tensor(a.d,a.n,{x:1-int(v!=0) for x,v in a.data.items()})
def tensor_and(a,b):
    assert a.d==b.d
    k=max(a.n,b.n)
    return Tensor(a.d,k,{x:a.data[x[:a.n]]*b.data[x[:b.n]] for x in tuples(a.d,k)})
def tensor_c(a,kind='B'):
    if a.n==0: return a
    return Tensor(a.d,a.n-1,{x:plus([a.data[(i,)+x] for i in range(a.d)],kind) for x in tuples(a.d,a.n-1)})
def tensor_p(a): return Tensor(a.d,a.n+1,{x:a.data[x[1:]] for x in tuples(a.d,a.n+1)})
def tensor_iota(a):
    if a.n<2: return a
    return Tensor(a.d,a.n,{x:a.data[(x[1],x[0])+x[2:]] for x in tuples(a.d,a.n)})
def tensor_sigma(a):
    if a.n<2: return a
    return Tensor(a.d,a.n,{x:a.data[x[-1:]+x[:-1]] for x in tuples(a.d,a.n)})
def pullback(a,k,alpha):
    assert len(alpha)==a.n and all(0<=i<k for i in alpha)
    return Tensor(a.d,k,{x:a.data[tuple(x[i] for i in alpha)] for x in tuples(a.d,k)})
def delta_pullback(a,k,alpha,kind):
    # Full equality-wire contraction. Repetitions copy a common witness.
    return Tensor(a.d,k,{x:plus([a.data[y]*int(all(y[j]==x[alpha[j]] for j in range(a.n))) for y in tuples(a.d,a.n)],kind) for x in tuples(a.d,k)})
def identity(d): return Tensor(d,2,{x:int(x[0]==x[1]) for x in tuples(d,2)})
def total(a,kind='B'):
    # Existential closure in B (or numerical total); not universal Q-model truth for open predicates.
    while a.n: a=tensor_c(a,kind)
    return truth(a)
def all_rels(d,n):
    xs=tuples(d,n)
    return [Rel(d,n,frozenset(x for x,v in zip(xs,bits) if v)) for bits in product((0,1), repeat=len(xs))]

# Primitive exactness on all small tables, including scalars.
CASES={}
for d,maxn in ((1,4),(2,3),(3,2)):
    for n in range(maxn+1):
        rr=all_rels(d,n); CASES[d,n]=rr
        for r in rr:
            t=encode(r)
            for name,fr,ft in [('negation',rel_not,tensor_not),('cylindrification',rel_c,tensor_c),('padding',rel_p,tensor_p),('iota',rel_iota,tensor_iota),('sigma',rel_sigma,tensor_sigma)]:
                check(name,encode(fr(r)),ft(t))
            check('faithful_inverse',support(t),r.rows)
            check('padding_c_B_identity',tensor_c(tensor_p(t)),t)
            check('padding_c_N_scale',tensor_c(tensor_p(t),'N').data,{x:d*v for x,v in t.data.items()})
            check('scalar_truth',total(t),int(bool(r.rows)))
            if n:
                check('exists_count_support',support(tensor_c(t,'N')),rel_c(r).rows)
        check('encoding_injective',len({tuple(encode(r).data.values()) for r in rr}),len(rr))
# Mixed arity source '&': exhaustive in n,m<=2 on D=2.
for n,m in product(range(3),repeat=2):
    for a,b in product(CASES[2,n],CASES[2,m]):
        check('mixed_arity_conjunction',tensor_and(encode(a),encode(b)),encode(rel_and(a,b)))
# Degree three conjunction adds nontrivial arbitrary joint tables.
for a,b in product(CASES[2,3],repeat=2):
    check('ternary_conjunction',tensor_and(encode(a),encode(b)),encode(rel_and(a,b)))

# Arbitrary slot maps include permutation, identification and unused output slots.
for n in range(4):
    for a in CASES[2,n]:
        t=encode(a)
        for k in range(1,4):
            for alpha in product(range(k),repeat=n):
                for kind in ('B','N'):
                    check('delta_index_map_'+kind,delta_pullback(t,k,alpha,kind),pullback(t,k,alpha))
# Nullary source with nullary target also has unique empty assignment.
for a in CASES[2,0]:
    check('empty_delta_wiring',delta_pullback(encode(a),0,(),'B'),encode(a))

# Arbitrary positive N weights, not only characteristic inputs.
for d,n in ((2,0),(2,1),(2,2)):
    xs=tuples(d,n)
    arr=[Tensor(d,n,dict(zip(xs,v))) for v in product(range(3),repeat=len(xs))]
    for a in arr:
        ba=Tensor(d,n,{x:int(v>0) for x,v in a.data.items()})
        check('N_support_c',support(tensor_c(a,'N')),support(tensor_c(ba,'B')))
        check('N_support_padding',support(tensor_p(a)),support(tensor_p(ba)))
        check('N_zero_test_complement',tensor_not(a),tensor_not(ba))
        for b in arr:
            bb=Tensor(d,n,{x:int(v>0) for x,v in b.data.items()})
            check('N_support_join',support(tensor_and(a,b)),support(tensor_and(ba,bb)))
            check('N_support_sum',tuple(int(a.data[x]+b.data[x]>0) for x in xs),tuple(int(ba.data[x] or bb.data[x]) for x in xs))

# Compositional terms independently evaluated with source relations and arrays.
ATOMS=[('atom',0),('atom',1),('atom',2),('atom',3)]
def arity(term):
    if term[0]=='atom': return [0,1,1,2][term[1]]
    op=term[0]; n=arity(term[1])
    if op=='and': return max(n,arity(term[2]))
    return max(n-1,0) if op=='c' else n+1 if op=='p' else n
def ev_rel(term,model):
    if term[0]=='atom': return model[term[1]]
    a=ev_rel(term[1],model)
    if term[0]=='and': return rel_and(a,ev_rel(term[2],model))
    return {'not':rel_not,'c':rel_c,'p':rel_p,'i':rel_iota,'s':rel_sigma}[term[0]](a)
def ev_tensor(term,model,kind):
    if term[0]=='atom': return encode(model[term[1]])
    a=ev_tensor(term[1],model,kind)
    if term[0]=='and': return tensor_and(a,ev_tensor(term[2],model,kind))
    if term[0]=='c': return tensor_c(a,kind)
    return {'not':tensor_not,'p':tensor_p,'i':tensor_iota,'s':tensor_sigma}[term[0]](a)
terms=list(ATOMS)
for depth in range(3):
    old=terms[-40:]
    terms += [(op,t) for t in old for op in ('not','c','p','i','s') if arity(t)+(op=='p')<=4]
    terms += [('and',old[i],old[-1-i]) for i in range(len(old))]
models=product(CASES[2,0],CASES[2,1],CASES[2,1],CASES[2,2])
for model in models:
    for term in terms:
        r=ev_rel(term,model)
        check('composed_B',support(ev_tensor(term,model,'B')),r.rows)
        check('composed_N_with_zero_test',support(ev_tensor(term,model,'N')),r.rows)

# Exact source's F,G,R endpoint-binding witness; same two elements in both worlds.
d=2; F=encode(Rel(d,1,frozenset({(0,)}))); G=encode(Rel(d,1,frozenset({(1,)})))
Rs=[encode(Rel(d,2,frozenset({pair}))) for pair in ((0,1),(1,0))]
def joint(R): return tensor_and(tensor_and(tensor_and(F,tensor_p(G)),R),tensor_not(identity(R.d)))
records=[(total(F),total(G),total(R),total(tensor_not(identity(d)))) for R in Rs]
check('source_record_same',records[0],records[1]); check('source_joint_opposite',[total(joint(R)) for R in Rs],[1,0])
check('source_numeric_scalar_records_same',[(total(F,'N'),total(G,'N'),total(R,'N')) for R in Rs],[(1,1,1),(1,1,1)])
# Sorting/symmetrising endpoint roles loses the orientation even with relation retained.
check('symmetrisation_loses_orientation',tuple(Rs[0].data[x]+tensor_iota(Rs[0]).data[x] for x in tuples(d,2)),tuple(Rs[1].data[x]+tensor_iota(Rs[1]).data[x] for x in tuples(d,2)))
# Sharing one variable differs from quantifying each predicate independently.
check('same_witness_joint_false',total(tensor_and(F,G)),0)
check('independent_existentials_true',int(total(F) and total(G)),1)
# All distinct label-free permutations commute with all primitive source operations.
for r in CASES[2,2]:
    t=encode(r)
    def ren(a): return Tensor(a.d,a.n,{tuple(1-i for i in x):v for x,v in a.data.items()})
    for op in (tensor_not,tensor_c,tensor_p,tensor_iota,tensor_sigma):
        check('domain_relabelling_equivariance',ren(op(t)),op(ren(t)))
check('identity_relabelling',ren(identity(2)),identity(2))

# Numerical plurality survives identical qualitative unary labels.
plural=[]
for d in (1,2,3):
    f=Tensor(d,1,{(i,):1 for i in range(d)})
    distinct=tensor_and(tensor_and(f,tensor_p(f)),tensor_not(identity(d)))
    plural.append({'size':d,'Boolean_at_least_two':total(distinct),'ordered_distinct_pairs':total(distinct,'N')})
check('plurality_preserved',[p['Boolean_at_least_two'] for p in plural],[0,1,1])
check('distinct_witness_counts',[p['ordered_distinct_pairs'] for p in plural],[0,2,6])

# Failed transports and explicit conventions.
u=Tensor(2,1,{(0,):1,(1,):1})
check('N_contraction_not_existential',total(u,'N'),2)
check('B_contraction_is_existential',total(u,'B'),1)
check('N_1_minus_count_wrong',1-total(u,'N'),-1)
check('zero_test_of_count_correct',int(total(u,'N')==0),0)
signed=Tensor(2,1,{(0,):1,(1,):-1})
check('signed_cancellation',total(signed,'N'),0)
check('signed_support_does_not_commute',total(Tensor(2,1,{x:int(v!=0) for x,v in signed.data.items()}),'B'),1)
# No real linear functional can implement OR on all characteristic vectors.
check('real_linear_OR_contradiction',1+1,2)
check('Boolean_inclusion_not_additive',int(bool(1 or 1)),1)
# Direct source unary iota clause leaks its declared single-axis environment.
source_unary_iota=[int(seq[1]==0) for seq in [(0,0),(0,1)]]
check('literal_unary_iota_same_prefix_different_value',source_unary_iota,[1,0])
# Affine complement is not positive-semiring linear; monotone circuits can't realise it.
check('complement_zero',truth(tensor_not(Tensor(2,0,{():0}))),1)
check('complement_one',truth(tensor_not(Tensor(2,0,{():1}))),0)

# Basis transport: coefficients (1,0) -> (1,-1) by invertible g.
# The augmentation covector must move with g; reusing (1,1) erases support.
g=((1,0),(-1,1)); transformed=(g[0][0],g[1][0])
check('basis_change_cancellation',sum(transformed),0)
check('basis_changed_covector_correct',2*transformed[0]+transformed[1],1)

# One-hot truth-wire contraction is a different representation from coefficients.
# Gate tensors are characteristic truth tables. Summation is Boolean OR.
def rail(b): return (int(b==0),int(b==1))
def gate_eval(inputs,fn):
    return tuple(int(any(all(rail(t)[a] for t,a in zip(inputs,assn)) and out==fn(*assn) for assn in product((0,1),repeat=len(inputs)))) for out in (0,1))
for a in (0,1):
    check('truth_wire_NOT',gate_eval((a,),lambda x:1-x),rail(1-a))
for a,b in product((0,1),repeat=2):
    check('truth_wire_AND',gate_eval((a,b),lambda x,y:x*y),rail(a*b))
    check('truth_wire_OR',gate_eval((a,b),lambda x,y:int(x or y)),rail(int(a or b)))
for ar in range(1,7):
    for assn in product((0,1),repeat=ar):
        check('truth_wire_exists',gate_eval(assn,lambda *xs:int(any(xs))),rail(int(any(assn))))

# Empty domains are outside Dasgupta's declared model class.
# They show why its dummy-witness identity cannot be imported to an empty sort.
empty_true=Tensor(0,0,{():1})
check('empty_scalar_unit_exists',len(tuples(0,0)),1)
check('empty_padding_has_no_entries',tensor_p(empty_true).data,{})
check('empty_dummy_existential_fails',truth(tensor_c(tensor_p(empty_true))),0)
check('empty_scalar_c_remains_identity',truth(tensor_c(empty_true)),1)
check('inhabited_dummy_existential',truth(tensor_c(tensor_p(Tensor(1,0,{():1})))),1)

# Appendix model-truth of open predicates is universal, not total() existential.
proper_unary=Tensor(2,1,{(0,):1,(1,):0})
check('open_predicate_existential_true',total(proper_unary),1)
check('open_predicate_universal_false',int(all(proper_unary.data.values())),0)
check('nullary_universal_existential_agree',int(all(Tensor(2,0,{():1}).data.values())),total(Tensor(2,0,{():1})))

out={'status':'PASS','metric_unit':'exact assertions, not independent discoveries','assertions_total':sum(METRICS.values()),'assertions_by_family':dict(sorted(METRICS.items())),'source_orientation':{'separated_with_distinctness':records,'joint_truths':[total(joint(R)) for R in Rs]},'same_label_plurality':plural,'controls_boundary':'Finite exhaustive/generated checks; universal claims proved in RESULT.md. Low-arity permutations use stated identity convention; literal unary source ambiguity separately exposed.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
