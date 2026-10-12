"""Exact finite checks of the NEW conditional synthesis.
No repository code is executed. Tests do not certify the source corpus or a physical model.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from collections import deque
import hashlib,json,math,sys,time
from pathlib import Path

def payoff(v,p,q):
    return sum(w*x for w,x in zip((p*q,p*(1-q),(1-p)*q,(1-p)*(1-q)),v))
def regrets(A,B,p,q):
    return (max(A[0]*q+A[1]*(1-q),A[2]*q+A[3]*(1-q))-payoff(A,p,q),
            max(B[0]*p+B[2]*(1-p),B[1]*p+B[3]*(1-p))-payoff(B,p,q))
def common(B,goods):
    if not B:raise ValueError('Empty belief is inconsistency, not a certificate.')
    return set.intersection(*(set(goods[w]) for w in B))
def decision_cost(worlds,goods,probes):
    """Nondestructive exact-observation, relation-valued minimax query cost."""
    @lru_cache(None)
    def solve(B):
        if common(B,goods):return F(0)
        vals=[]
        for cost,outputs in probes:
            if cost<=0:raise ValueError('Positive fixed probe cost required.')
            ys={outputs[w] for w in B}
            if len(ys)<2:continue
            children=[tuple(w for w in B if outputs[w]==y) for y in ys]
            vals.append(cost+max(solve(c) for c in children))
        return min(vals,default=math.inf)
    return solve(tuple(worlds))
def exhaustive_two_level_cost(worlds,goods,probes):
    """Separate concrete tree enumeration for populations of three worlds."""
    if common(worlds,goods):return F(0)
    best=math.inf
    for h,(cost,out) in enumerate(probes):
        ys=sorted({out[w] for w in worlds})
        for choices in product(range(-1,len(probes)),repeat=len(ys)):
            policy=dict(zip(ys,choices));worst=F(0);valid=True
            for y in ys:
                B=tuple(w for w in worlds if out[w]==y);k=policy[y]
                if k==-1:
                    if not common(B,goods):valid=False;break
                    worst=max(worst,cost)
                else:
                    c2,o2=probes[k]
                    for z in {o2[w] for w in B}:
                        leaf=tuple(w for w in B if o2[w]==z)
                        if not common(leaf,goods):valid=False;break
                    worst=max(worst,cost+c2)
                if not valid:break
            if valid:best=min(best,worst)
    return best

def reachability(initial,actions,observe):
    """Beliefs retain (current physical/model state, required INITIAL label)."""
    initial=frozenset(initial);Q=deque([initial]);seen={initial};edges={}
    while Q:
        B=Q.popleft();edges[B]=[]
        for act in actions:
            groups={}
            for w,label in B:
                v=act(w);groups.setdefault(observe(v),set()).add((v,label))
            succ=tuple(frozenset(x) for x in groups.values());edges[B].append(succ)
            for C in succ:
                if C not in seen:seen.add(C);Q.append(C)
        if len(seen)>4096:raise RuntimeError('Declared finite test scope exceeded.')
    rank={B:0 for B in seen if len({label for _,label in B})==1}
    while True:
        additions={B:1+min(max(rank[C] for C in ss) for ss in edges[B] if all(C in rank for C in ss))
                   for B in seen-rank.keys() if any(all(C in rank for C in ss) for ss in edges[B])}
        if not additions:break
        rank.update(additions)
    return {'reachable_beliefs':len(seen),'winning_beliefs':len(rank),'initial_winning':initial in rank,'initial_rank':rank.get(initial)}

def run():
    counts={};grid=(F(0),F(1,2),F(1));games=list(product((F(0),F(1)),repeat=8))
    n=0;ne_total=0
    for g in games:
        A,B=g[:4],g[4:];found=False
        for p,q in product(grid,repeat=2):
            r=regrets(A,B,p,q);assert all(x>=0 for x in r)
            direct=[]
            for i in range(2):
                baseline=payoff(A if i==0 else B,p,q)
                best=max(payoff(A if i==0 else B,a,q) if i==0 else payoff(B,p,a) for a in (F(0),F(1)))
                direct.append(best-baseline)
            assert tuple(direct)==r
            if r==(0,0):found=True;ne_total+=1
            n+=1
        assert found,'Binary 2x2 game has no candidate on declared grid.'
    counts['binary_bimatrix_game_profile_checks']=n;counts['binary_bimatrix_games']=len(games);counts['zero_regret_grid_profiles']=ne_total
    n=0
    for g in games:
        A,B=g[:4],g[4:];AA=tuple(A[2*i+j]+(F(7) if j==0 else F(-3)) for i,j in product(range(2),repeat=2));BB=tuple(B[2*i+j]+(F(11) if i==0 else F(-5)) for i,j in product(range(2),repeat=2))
        for p,q in product(grid,repeat=2):assert regrets(A,B,p,q)==regrets(AA,BB,p,q);n+=1
    counts['opponent_only_payoff_shift_checks']=n
    n=0;eps=F(1,2)
    for k in (0,1,42,255):
        g=games[k]
        for noise in product((-eps,eps),repeat=8):
            h=tuple(a+b for a,b in zip(g,noise))
            for p,q in product(grid,repeat=2):
                r=regrets(g[:4],g[4:],p,q);rr=regrets(h[:4],h[4:],p,q)
                assert all(abs(x-y)<=2*eps for x,y in zip(r,rr));n+=1
    counts['uniform_payoff_perturbation_checks']=n
    worlds=(0,1,2);outs=list(product((0,1),repeat=3));n=0
    acceptable=(frozenset(),frozenset({0}),frozenset({1}),frozenset({0,1}))
    for gs in product(acceptable,repeat=3):
        goods=dict(enumerate(gs))
        for a,b in product(outs,repeat=2):
            probes=((F(1),a),(F(2),b));v=decision_cost(worlds,goods,probes);w=exhaustive_two_level_cost(worlds,goods,probes)
            assert v==w,(gs,a,b,v,w);n+=1
    counts['relation_valued_inquiry_models_checked_against_tree_enumeration']=n
    # Unknown reference game: every game has NE, but no blind common equilibrium.
    g0=((F(1),F(1),F(0),F(0)),(F(1),F(0),F(1),F(0)))
    g1=((F(0),F(0),F(1),F(1)),(F(0),F(1),F(0),F(1)))
    assert regrets(*g0,F(1),F(1))==(0,0) and regrets(*g1,F(0),F(0))==(0,0)
    worst=min(max(*regrets(*g0,p,q),*regrets(*g1,p,q)) for p,q in product(grid,repeat=2));assert worst==F(1,2)
    # Common-certificate stopping need not identify a world or payoff tensor.
    assert decision_cost((0,1),{0:{'same'},1:{'same'}},())==0
    assert math.isinf(decision_cost((0,1),{0:{0},1:{1}},()))
    assert decision_cost((0,1),{0:{0},1:{1}},((F(1),(0,1)),))==1
    counts['unknown_game_minimax_blind_regret']=str(worst)
    # All finite integer 2x2 common-cost games; random-scan logit detailed balance.
    n=0;roots=0;states=list(product(range(2),repeat=2))
    for C in product(range(3),repeat=4):
        def cost(s):return C[2*s[0]+s[1]]
        for initial in states:
            seen=set()
            def walk(s,path):
                assert s not in path
                improving=[t for t in states if sum(a!=b for a,b in zip(s,t))==1 and cost(t)<cost(s)]
                if not improving:
                    assert all(cost(t)>=cost(s) for t in states if sum(a!=b for a,b in zip(s,t))==1)
                for t in improving:walk(t,path+(s,))
            walk(initial,());roots+=1
        for base in (2,3):
            weights={s:F(1,base**cost(s)) for s in states};Z=sum(weights.values());pi={s:weights[s]/Z for s in states}
            def trans(s,t):
                out=F(0)
                if t[1]==s[1]:out+=F(1,2)*weights[t]/sum(weights[(i,s[1])] for i in range(2))
                if t[0]==s[0]:out+=F(1,2)*weights[t]/sum(weights[(s[0],j)] for j in range(2))
                return out
            for s in states:
                assert sum(trans(s,t) for t in states)==1
                for t in states:assert pi[s]*trans(s,t)==pi[t]*trans(t,s);n+=1
            for t in states:assert sum(pi[s]*trans(s,t) for s in states)==pi[t]
            m=sum(cost(s)==min(C) for s in states)
            if m<4:
                gap=min(x-min(C) for x in C if x>min(C));ratio=F(4-m,m)*F(1,base**gap)
                outside=sum(pi[s] for s in states if cost(s)>min(C));assert outside<=ratio/(1+ratio)
    counts['potential_games']=81;counts['all_strict_improvement_path_start_checks']=roots;counts['exact_logit_detailed_balance_pairs']=n
    # Shared-cost anti-coordination: synchronous response cycles; interior saddle.
    C=(2,0,0,2);assert C[0]>C[2] and C[0]>C[1] and C[3]>C[1] and C[3]>C[2]
    assert F(0)*F(0)-F(-1,2)*F(-1,2)==F(-1,4)
    gibbs=(F(1,10),F(2,5),F(2,5),F(1,10));assert gibbs[0]+gibbs[3]==F(1,5);assert F(1,2)!=F(1,5)
    counts['synchronous_cycle']=[[0,0],[1,1],[0,0]];counts['interior_replicator_jacobian_determinant']='-1/4';counts['gibbs_conflict_probability']='1/5';counts['independent_marginal_product_conflict_probability']='1/2'
    a={'p':'t1','q':'t0','r':'t0','t0':'t0','t1':'t1'};b={'p':'t0','q':'t1','r':'t0','t0':'t0','t1':'t1'};obs={'p':'?','q':'?','r':'?','t0':'0','t1':'1'}
    destructive=reachability([('p',0),('q',0),('r',1)],[a.__getitem__,b.__getitem__],obs.__getitem__);assert not destructive['initial_winning']
    reconnect=reachability([((0,0),0),((0,1),1)],[lambda w:(1,w[1])],lambda w:(w[0],w[0]*w[1]));assert reconnect['initial_winning'] and reconnect['initial_rank']==1
    counts['destructive_observation_model']=destructive;counts['reconnection_model']=reconnect
    return counts

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Optimised Python disables this verifier; use ordinary Python.')
    target=Path(__file__).with_name('results.json');t=time.time()
    try:
        checks=run();receipt={'status':'PASS','scope':'Exact finite checks of explicitly specified synthetic models ONLY','counts':checks,'elapsed_seconds':round(time.time()-t,3),'python':sys.version,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'not_certified':['full source line-by-line review','general theorem machine checking','empirical agent learning','physical least-action bridge','repository adoption','meniscus break','strong-baseline advantage']}
    except Exception as e:
        import traceback
        receipt={'status':'FAIL','error':repr(e),'traceback':traceback.format_exc(),'elapsed_seconds':round(time.time()-t,3)}
    target.write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
    if receipt['status']!='PASS':sys.exit(1)
