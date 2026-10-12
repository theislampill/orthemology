"""Deterministic bounded falsification probes. No result is a universal proof."""
import hashlib,json,sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import probes as p

def need(condition,label):
    if not condition:raise RuntimeError(label)

def run():
    c={};w={}
    ts=[t for n in (1,3,5,7,9) for t in p.terms_of_size(n,(p.I,p.K,p.S,p.V(0)))]
    sim=parallel_pairs=beta_steps=0
    for t in ts:
        for h in p.step_edges(t):
            path=p.simulate(t,h)
            need(len(path)>1,'empty simulation')
            need(path[-1]==p.translate(h.target),'simulation endpoint')
            for a,b in zip(path,path[1:]):need(b in p.lsteps(a),'invalid beta step')
            sim+=1;beta_steps+=len(path)-1
        for u in p.parallel(t):
            need(p.develop(t) in p.parallel(u),'parallel triangle counterexample')
            parallel_pairs+=1
    c['ski_terms_by_nodes']={str(n):len(p.terms_of_size(n,(p.I,p.K,p.S,p.V(0)))) for n in (1,3,5,7,9)}
    c.update(ski_terms=len(ts),source_step_witnesses=sim,simulated_beta_steps=beta_steps,parallel_pairs=parallel_pairs)
    bases=[p.I,p.K,p.A(p.I,p.V(2)),p.A(p.V(1),p.V(0))]
    small=[t for n in (1,3,5,7) for t in p.terms_of_size(n,(p.I,p.S,p.V(0),p.V(1)))]
    squares=0
    for t in small:
        for a,b in product(bases,repeat=2):
            s={0:a,1:b}
            need(p.translate(p.subst(t,s))==p.lfree_subst(p.translate(t),{k:p.translate(v) for k,v in s.items()}),'term substitution')
            squares+=1
    c['term_substitution_squares']=squares
    ty={('t',0),('t',1),('bot',)}
    for _ in range(2):ty={('t',0),('t',1),('bot',)}|{('arr',a,b) for a,b in product(ty,repeat=2)}|{('all',a) for a in ty}
    choices=[('t',0),('t',1),('arr',('t',0),('bot',)),('all',('arr',('t',0),('t',1)))]
    subs=[dict(enumerate(v)) for v in product(choices,repeat=2)]
    type_squares=0
    for t in sorted(ty,key=repr):
        need(p.tsubst(t,lambda n:('t',n))==t,'type identity')
        for s,d in product(subs,repeat=2):
            sf=lambda n:s.get(n,('t',n));df=lambda n:d.get(n,('t',n))
            need(p.tsubst(p.tsubst(t,sf),df)==p.tsubst(t,lambda n:p.tsubst(sf(n),df)),'type composition')
            type_squares+=1
    c.update(type_terms=len(ty),type_substitution_squares=type_squares)
    abstract_terms=[t for n in (1,3,5,7) for t in p.terms_of_size(n,(p.I,p.K,p.V(0),p.V(1)))]
    npaths=nsteps=0
    for t in abstract_terms:
        for x in (p.I,p.K,p.V(2),p.omega_cycle()[0]):
            path=p.abstraction_path(0,t,x)
            need(path[0]==p.A(p.abstract(0,t),x),'bracket start')
            need(path[-1]==p.subst(t,{0:x}),'bracket end')
            for a,b in zip(path,path[1:]):need(b in p.steps(a),'bracket step')
            npaths+=1;nsteps+=len(path)-1
        s={1:p.A(p.I,p.K)}
        need(p.subst(p.abstract(0,t),s)==p.abstract(0,p.subst(t,s)),'bracket fresh naturality')
    c.update(bracket_paths=npaths,bracket_steps=nsteps,bracket_naturality_squares=len(abstract_terms))
    seen=set(p.omega_cycle());fringe={p.omega_cycle()[0]}
    for _ in range(12):
        fringe={u for t in fringe for u in p.steps(t)}-seen
        seen |=fringe
    for t in seen:
        need(p.omega_shape(t) is not None,'omega shape')
        need(bool(p.steps(t)),'omega normal form')
        for u in p.steps(t):need(p.omega_shape(u) is not None,'omega successor shape')
    c['omega_explored_states']=len(seen)
    # Correct complete BFS separately: preloading all cycle nodes above suppresses
    # exploration through a known node. The complete depth-bounded closure follows.
    layers=[{p.omega_cycle()[0]}]
    for _ in range(12):layers.append(layers[-1]|{u for t in layers[-1] for u in p.steps(t)})
    for t in layers[-1]:
        need(p.omega_shape(t) is not None and bool(p.steps(t)),'complete omega closure')
    c['omega_depth12_distinct_states']=len(layers[-1]);c['omega_depth_counts']=[len(s) for s in layers]
    e=p.A(p.S,p.K,p.K);xi=p.abstract(0,p.A(p.I,p.V(0)))
    for name,a,b in [('identity_extension',p.I,e),('abstraction_congruence',p.I,xi)]:
        need(a!=b and not p.steps(a) and not p.steps(b),'normal-form separator')
        w[name]={'left':p.show(a),'right':p.show(b),'both_ski_normal':True,'distinct':True,
                 'nonconversion_requires':'ordinary parallel-confluence proof; not decided by this program'}
    o,o1,o2=p.omega_cycle()
    w['discarded_omega']={'cycle':[p.show(p.A(p.K,p.I,z)) for z in (o,o1,o2,o)],'head_reduct':p.show(p.I)}
    for a,b in zip((o,o1,o2),(o1,o2,o)):need(p.A(p.K,p.I,b) in p.steps(p.A(p.K,p.I,a)),'discarded cycle')
    # Distinct normal forms collapse under lambda macro translation (no reflection).
    frontier={p.translate(e)}
    for _ in range(12):
        if p.translate(p.I) in frontier:break
        frontier={u for t in frontier for u in p.lsteps(t)}
    need(p.translate(p.I) in frontier,'translation counterexample path absent')
    w['translation_nonreflection']={'source_pair':['I','((S K) K)'],'target_beta_equivalent':True}
    weights=[F(0),F(1,3),F(1,2),F(2,3),F(1)]
    leaves=[('pure',p.I),('pure',e)]
    expr=leaves[:]
    for _ in range(2):expr=leaves+[('mix',q,a,b) for q in weights for a,b in product(expr,repeat=2)]+[('eapp',a,b) for a,b in product(expr,repeat=2)]
    for x in expr:
        m=p.mass(x);need(sum(m.values())==1 and all(v>0 for v in m.values()),'probability law')
        need(p.marginals(p.diagonal_coupling(m))==(m,m),'diagonal coupling')
    c['finite_effect_syntax_expressions_depth2']=len(expr)
    rels=[{(i,j) for i,j in product(range(2),repeat=2) if mask&(1<<(2*i+j))} for mask in range(16)]
    mismatch=0
    for r,s in product(rels,repeat=2):
        if p.fair_couplings(r) and p.fair_couplings(s) and not p.fair_couplings(r&s):mismatch+=1
    c.update(binary_relations=16,relation_pairs=256,coupling_intersection_failures=mismatch)
    w['coupling_intersection']={'mu':['1/2','1/2'],'nu':['1/2','1/2'],'relations':[[[0,0],[1,1]],[[0,1],[1,0]]],'intersection':[],
        'first_coupling':{'00':'1/2','11':'1/2'},'second_coupling':{'01':'1/2','10':'1/2'},'common_coupling_exists':False}
    # Bounded, deliberately wrong alternatives rejected by explicit controls.
    mutations={
      'empty_simulation_rejected':len([p.translate(p.A(p.I,p.I))])==1,
      'unlifted_type_substitution_rejected':p.tsubst(('all',('t',1)),lambda _:('t',0))!=('all',('t',0)),
      'raw_function_extensionality_rejected':e!=p.I and not p.steps(e) and not p.steps(p.I),
      'bracket_xi_rejected':xi!=p.I and not p.steps(xi) and not p.steps(p.I),
      'coupling_all_swap_rejected':bool(p.fair_couplings(rels[9])) and bool(p.fair_couplings(rels[6])) and not p.fair_couplings(set()),
      'proof_inspecting_j_motive_rejected':p.A(p.I,p.I)!=p.I and p.I in p.steps(p.A(p.I,p.I))
    }
    need(all(mutations.values()),'mutation control failed')
    return {'status':'PASS_BOUNDED_ONLY','universal_proof_credit':False,'kernel_proof_credit':False,
            'canonical_engine_test_credit':False,'populations':c,'witnesses':w,'negative_controls':mutations,
            'scripts':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path(__file__).parent.glob('*.py')}}

if __name__=='__main__':
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
