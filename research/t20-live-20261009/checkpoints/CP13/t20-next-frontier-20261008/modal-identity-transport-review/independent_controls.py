#!/usr/bin/env python3
"""Independent exact finite tests; imports no author code. Not a general proof."""
from itertools import product, permutations, combinations
from fractions import Fraction
from collections import Counter, deque
from pathlib import Path
import json, hashlib, random

COUNTS = Counter()
def check(name, condition):
    COUNTS[name] += 1
    assert condition, name

def inv(p):
    return tuple(p.index(i) for i in range(len(p)))
def compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))
def direct_sections(n, m, edges, filters):
    return {s for s in product(range(n), repeat=m)
            if all(s[w] in filters[w] for w in range(m))
            and all(s[v] == p[s[u]] for u,v,p in edges)}
def transports(n, m, tree):
    adj = [[] for _ in range(m)]
    for u,v,p in tree:
        adj[u].append((v,p)); adj[v].append((u,inv(p)))
    t = [None]*m; t[0] = tuple(range(n)); q=deque([0])
    while q:
        u=q.popleft()
        for v,p in adj[u]:
            if t[v] is None:
                t[v]=compose(p,t[u]); q.append(v)
    assert all(v is not None for v in t)
    return t

def rooted(n, m, edges, filters, tree):
    t=transports(n,m,tree)
    hs=[compose(inv(t[v]),compose(p,t[u])) for u,v,p in edges]
    k={b for b in range(n) if all(h[b]==b for h in hs)}
    f={b for b in k if all(t[w][b] in filters[w] for w in range(m))}
    return k,f,{tuple(t[w][b] for w in range(m)) for b in f}

def test_graph(n,m,edges,filters,trees,rng):
    direct=direct_sections(n,m,edges,filters)
    full=direct_sections(n,m,edges,[set(range(n))]*m)
    for tree in trees:
        k,f,sections=rooted(n,m,edges,filters,tree)
        check('section_equals_rooted',direct==sections)
        check('tree_independent_root_values',f=={s[0] for s in direct})
        check('tree_independent_fixed_values',k=={s[0] for s in full})
        check('full_atlas_iff_all_extend',len(k)==n if len(full)==n else len(k)!=n)
    # A separate arithmetic sum/product tensor network with no logical shortcut.
    total=0
    for s in product(range(n),repeat=m):
        val=1
        for w in range(m): val*=int(s[w] in filters[w])
        for u,v,p in edges: val*=int(s[v]==p[s[u]])
        total+=val
    check('natural_count_equals_sections',total==len(direct))
    check('boolean_scalar_equals_nonempty',bool(total)==bool(direct))
    pis=[]
    for _ in range(m):
        p=list(range(n));rng.shuffle(p);pis.append(tuple(p))
    edge2=[(u,v,compose(pis[v],compose(p,inv(pis[u])))) for u,v,p in edges]
    a2=[{pis[w][x] for x in filters[w]} for w in range(m)]
    transformed=direct_sections(n,m,edge2,a2)
    check('passive_gauge_sections',transformed=={tuple(pis[w][s[w]] for w in range(m)) for s in direct})
    for tree in trees:
        t=transports(n,m,tree)
        tree2=[(u,v,compose(pis[v],compose(p,inv(pis[u])))) for u,v,p in tree]
        t2=transports(n,m,tree2)
        check('gauge_chart_conjugacy',all(t2[w]==compose(pis[w],compose(t[w],inv(pis[0]))) for w in range(m)))

rng=random.Random(20261008)
for n in range(4):
    ps=list(permutations(range(n)))
    masks=list(product((0,1),repeat=3*n))
    # All filters for n <= 2; a declared seeded sample plus empty/full at n=3.
    if n==3: masks=[(0,)*(3*n),(1,)*(3*n)]+rng.sample(masks,30)
    for p,q,r in product(ps,repeat=3):
        edges=[(0,1,p),(1,2,q),(0,2,r)]
        for mask in masks:
            filters=[{x for x in range(n) if mask[w*n+x]} for w in range(3)]
            test_graph(n,3,edges,filters,[list(t) for t in combinations(edges,2)],rng)

# Directly enumerate anchored full charts, independently of holonomy.
for n in range(4):
    ps=list(permutations(range(n))); ident=tuple(range(n))
    for p,q,r in product(ps,repeat=3):
        edges=[(0,1,p),(1,2,q),(0,2,r)]
        charts=[(ident,u,v) for u,v in product(ps,repeat=2)
                if all(compose((ident,u,v)[b],inv((ident,u,v)[a]))==g for a,b,g in edges)]
        sections=direct_sections(n,3,edges,[set(range(n))]*3)
        check('full_charts_iff_n_sections',bool(charts)==(len(sections)==n))
        check('root_anchored_charts_unique',len(charts)<=1)

for _ in range(250):
    n=rng.randrange(6);m=4;edges=[]
    for u,v in combinations(range(m),2):
        p=list(range(n));rng.shuffle(p);edges.append((u,v,tuple(p)))
    filters=[{x for x in range(n) if rng.randrange(2)} for w in range(m)]
    tree=[e for e in edges if e[0]==0]
    tree_alt=[next(e for e in edges if e[:2]==(u,u+1)) for u in range(m-1)]
    test_graph(n,m,edges,filters,[tree,tree_alt],rng)

# Copyability is computed coefficient-by-coefficient with exact arithmetic.
def copyable(c, boolean=False, modulus=None):
    norm=bool(any(c)) if boolean else sum(c)
    if modulus is not None: norm%=modulus
    if norm!=1:return False
    for i in range(len(c)):
        for j in range(len(c)):
            left=c[i] if i==j else 0
            right=(c[i] and c[j]) if boolean else c[i]*c[j]
            if modulus is not None: right%=modulus
            if left!=right:return False
    return True
for n in range(11):
    for c in product((0,1),repeat=n):
        check('boolean_copyable_iff_basis',copyable(c,True)==(sum(c)==1))
vals=[Fraction(-1),Fraction(-1,2),Fraction(0),Fraction(1,2),Fraction(1),Fraction(2)]
for n in range(5):
    for c in product(vals,repeat=n):
        onehot=all(x in (0,1) for x in c) and sum(c)==1
        check('rational_grid_copyable_iff_basis',copyable(c)==onehot)
check('z6_nonbasis_copyable',copyable((3,4),modulus=6) and (3,4) not in ((1,0),(0,1)))
check('swap_normalized_average_parallel',tuple(reversed((Fraction(1,2),)*2))==(Fraction(1,2),)*2)
check('swap_normalized_average_not_copyable',not copyable((Fraction(1,2),)*2))

# Every group element has a fixed point, but not one common fixed point.
h1=(0,1,3,2,5,4);h2=(1,0,2,3,5,4);ident=tuple(range(6))
group={ident};front=[ident]
while front:
    g=front.pop()
    for h in (h1,h2):
        gh=compose(g,h)
        if gh not in group:group.add(gh);front.append(gh)
check('klein_group_size',len(group)==4)
check('every_loop_has_some_fixed_point',all(any(g[x]==x for x in range(6)) for g in group))
check('no_point_fixed_by_all_loops',not any(all(g[x]==x for g in group) for x in range(6)))
figure8=[(0,1,ident),(1,2,ident),(0,2,h1),(0,3,ident),(3,4,ident),(0,4,h2)]
check('figure_eight_no_sections',not direct_sections(6,5,figure8,[set(range(6))]*5))

# Exhaust every relation and retained subset through n=3.
back_failures=0
for n in range(4):
    pairs=list(product(range(n),repeat=2))
    for bits in product((0,1),repeat=n*n):
        dep={pair for pair,bit in zip(pairs,bits) if bit}
        for keepbits in product((0,1),repeat=n):
            keep={x for x in range(n) if keepbits[x]}
            for b in keep:
                local=any((y,b) in dep for y in range(n))
                retained=any((y,b) in dep for y in keep)
                back=(not local) or retained
                check('back_iff_received_preserved',(local==retained)==back)
                check('back_iff_nonreceipt_preserved',((not local)==(not retained))==back)
                back_failures+=int(not back)
# No fixed supplier is needed; each world's contingent supplier can suffice.
E=[{0,1},{0,2}];deps=[{(1,0)},{(2,0)}];necessary=E[0]&E[1]
check('necessary_filter_is_singleton',necessary=={0})
check('changing_suppliers_received_everywhere',all(any((y,0) in d for y in range(3)) for d in deps))
check('necessary_filter_loses_receipt',all(not any((y,0) in d for y in necessary) for d in deps))
check('existing_sources_and_targets',all(y in E[w] and b in E[w] for w,d in enumerate(deps) for y,b in d))
check('generic_reception_fixture',all(not any(any((y,b) in d for y in range(3)) for d in deps) or all(b not in E[w] or any((y,b) in deps[w] for y in range(3)) for w in range(2)) for b in range(3)))
keep={2}; dep={(0,2)}
check('coherent_subset_loses_receipt',any((y,2) in dep for y in range(3)) and not any((y,2) in dep for y in keep))
check('coherent_subset_loses_realisation',bool({0}) and not bool({0}&keep))
check('back_not_supplier_closure',any((y,2) in {(1,2),(0,2)} for y in {1,2}) and 0 not in {1,2})
# Even exact Back for Received fails to preserve supplier multiplicity.
check('back_not_all_quantifiers',len({y for y in range(3) if (y,2) in {(0,2),(1,2)}})==2 and len({y for y in {1,2} if (y,2) in {(0,2),(1,2)}})==1)

# Back and actual Realisation do not preserve every FullPremises formula.
# Bearer 0 is necessary; omitted 1 is actual and contingent; C and Dep are empty.
# Full ContingencyNeed is false at 1, while the restriction satisfies it vacuously.
E_univ=[{0,1},{0}]; keep_univ={0}
def need_on(domain):
    return all(b not in E_univ[0] or all(b in e for e in E_univ) for b in domain)
check('back_and_realisation_not_full_premises',not need_on({0,1}) and need_on(keep_univ)
      and all(not any(False for y in {0,1}) for b in keep_univ)
      and any(b==0 and b in E_univ[0] for b in keep_univ))
check('coherent_identity_does_not_force_E_persistence',bool(direct_sections(1,2,[(0,1,(0,))],[{0},{0}]))
      and not direct_sections(1,2,[(0,1,(0,))],[{0},set()]))
# The corresponding Realisation Back condition is exact for existence-guarded witnesses.
for n in range(4):
    for exists, intrinsic, kept in product(product((0,1),repeat=n),repeat=3):
        full=any(exists[x] and intrinsic[x] for x in range(n))
        retained=any(kept[x] and exists[x] and intrinsic[x] for x in range(n))
        back=(not full) or retained
        check('realisation_back_iff_existential_preserved',(full==retained)==back)

# A relational first-order modal evaluator in two independently organized models.
# Local box transports the assignment by destination_chart o inverse_current_chart.
def eval_global(f,w,env,E,D,acc,n,actualist):
    op=f[0]
    if op=='E':return env[f[1]] in E[w]
    if op=='D':return (env[f[1]],env[f[2]]) in D[w]
    if op=='=':return env[f[1]]==env[f[2]]
    if op=='not':return not eval_global(f[1],w,env,E,D,acc,n,actualist)
    if op=='and':return all(eval_global(g,w,env,E,D,acc,n,actualist) for g in f[1:])
    if op=='box':return all(eval_global(f[1],v,env,E,D,acc,n,actualist) for v in acc[w])
    if op in ('ex','all'):
        dom=E[w] if actualist else range(n)
        values=[eval_global(f[2],w,dict(env,**{f[1]:b}),E,D,acc,n,actualist) for b in dom]
        return any(values) if op=='ex' else all(values)
    raise ValueError(f)
def eval_local(f,w,env,E,D,acc,n,charts,actualist):
    op=f[0]
    if op=='E':return env[f[1]] in E[w]
    if op=='D':return (env[f[1]],env[f[2]]) in D[w]
    if op=='=':return env[f[1]]==env[f[2]]
    if op=='not':return not eval_local(f[1],w,env,E,D,acc,n,charts,actualist)
    if op=='and':return all(eval_local(g,w,env,E,D,acc,n,charts,actualist) for g in f[1:])
    if op=='box':
        iw=inv(charts[w])
        return all(eval_local(f[1],v,{x:charts[v][iw[b]] for x,b in env.items()},E,D,acc,n,charts,actualist) for v in acc[w])
    if op in ('ex','all'):
        dom=E[w] if actualist else range(n)
        values=[eval_local(f[2],w,dict(env,**{f[1]:b}),E,D,acc,n,charts,actualist) for b in dom]
        return any(values) if op=='ex' else all(values)
    raise ValueError(f)
forms=[('ex','x',('box',('E','x'))),('box',('ex','x',('E','x'))),
       ('all','x',('box',('ex','y',('D','y','x')))),
       ('ex','x',('and',('E','x'),('box',('not',('ex','y',('D','y','x')))))),
       ('box',('all','x',('ex','y',('and',('=','x','y'),('box',('E','y')))))),
       ('not',('ex','x',('box',('not',('=','x','x'))))),
       ('all','x',('box',('all','y',('box',('D','x','y')))))]
for _ in range(500):
    n=rng.randrange(5);m=3
    charts=[]
    for w in range(m):
        p=list(range(n));rng.shuffle(p);charts.append(tuple(p))
    E=[{x for x in range(n) if rng.randrange(2)} for w in range(m)]
    D=[{xy for xy in product(range(n),repeat=2) if rng.randrange(2)} for w in range(m)]
    acc=[{v for v in range(m) if rng.randrange(2)} for w in range(m)]
    LE=[{charts[w][x] for x in E[w]} for w in range(m)]
    LD=[{(charts[w][x],charts[w][y]) for x,y in D[w]} for w in range(m)]
    for f,w,actualist in product(forms,range(m),(False,True)):
        check('modal_semantics_chart_preserved',eval_global(f,w,{},E,D,acc,n,actualist)==eval_local(f,w,{},LE,LD,acc,n,charts,actualist))

# Outer-domain Barcan commutation is valid; arbitrary E-guarded versions can fail.
forall_box=('all','x',('box',('D','x','x')))
box_forall=('box',('all','x',('D','x','x')))
acc_b=[{1},set()];dep_b=[set(),{(0,0)}]
for E_b,expected in [([{0},{0,1}],(True,False)),([{0,1},{0}],(False,True))]:
    outer=tuple(eval_global(f,0,{},E_b,dep_b,acc_b,2,False) for f in (forall_box,box_forall))
    guarded=tuple(eval_global(f,0,{},E_b,dep_b,acc_b,2,True) for f in (forall_box,box_forall))
    check('outer_domain_barcan_commutation',outer[0]==outer[1])
    check('actualist_barcan_direction_fails',guarded==expected)

# Local records alone lose cross-world binding; gauge-transforming edges repairs it.
def necessary_truth(E0,E1,p):return any(x in E0 and p[x] in E1 for x in range(len(p)))
check('local_iso_not_de_re',necessary_truth({0},{0},(0,1)) and not necessary_truth({0},{1},(0,1)))
check('local_iso_passive_repair',necessary_truth({0},{1},(1,0)))
check('empty_bearer_domain_no_sections',not direct_sections(0,1,[],[set()]))
check('single_world_empty_filter_no_sections',not direct_sections(1,1,[],[set()]))
check('vacuous_box_not_actuality',all([]) and not bool(set()))

report={'status':'PASS','seed':20261008,'assertions':sum(COUNTS.values()),'counts':dict(sorted(COUNTS.items())),
        'exhaustive_triangle_scope':'n=0,1,2: all edge permutations and all filters; n=3: all edge permutations and 32 declared seeded/endpoint filters',
        'complete_four_vertex_scope':'250 seeded instances, n=0..5, two trees each',
        'receipt_scope':'all relations and retained subsets on n=0..3; all retained targets',
        'modal_scope':'500 seeded three-world models, n=0..4, seven formulas at every world under possibilist and guarded actualist quantifiers',
        'copy_scope':'all Boolean vectors through dimension 10; exact six-value rational grid through dimension 4; explicit Z/6 control',
        'receipt_loss_cases':back_failures,
        'author_code_imported':False,'limitations':'Finite verification is not the general proof, semantic authentication, metaphysical warrant, or closure.'}
print(json.dumps(report,indent=2,sort_keys=True))
Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
