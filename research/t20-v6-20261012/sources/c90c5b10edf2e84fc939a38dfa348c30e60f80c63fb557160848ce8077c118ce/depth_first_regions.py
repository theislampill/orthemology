#!/usr/bin/env python3
"""Exact scheduling control: bottom-up region storage versus return-one-bit DFS.

Local parity target computation is shared deliberately: this test isolates support
recursion/resource scheduling, not independent validity of the parity theorem.
No simulation or random census is used. Instrumentation stores only scalar counts.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

def subsets(xs):
    xs=tuple(xs)
    for j in range(1,len(xs)+1):
        for ys in combinations(xs,j): yield frozenset(ys)

def reachable(start,adj):
    seen=set(start); todo=list(start)
    while todo:
        s=todo.pop()
        for y in adj.get(s,()):
            if y not in seen: seen.add(y);todo.append(y)
    return seen

def sccs(nodes,adj):
    remaining=set(nodes);out=[]
    while remaining:
        s=min(remaining); fw=reachable([s],adj)
        C={y for y in remaining if y in fw and s in reachable([y],adj)}
        out.append(C);remaining-=C
    return out

def mecs(S,pairs,succ):
    todo=[set(S)]; out=[]
    while todo:
        C=todo.pop()
        while C:
            U={e for e in pairs if e[0] in C and succ[e]<=C}
            alive={s for s,a in U}
            if alive!=C: C=alive;continue
            adj={s:set() for s in C}
            for e in U: adj[e[0]]|=succ[e]
            comps=sccs(C,adj)
            if len(comps)==1: out.append(frozenset(U))
            else: todo.extend(comps)
            break
    return out

class System:
    def __init__(self,n,m,k,P,colors,menu=None):
        self.S=tuple(range(n));self.A=tuple(range(m));self.models=tuple(range(k))
        self.P=P;self.colors=colors;self.menu=menu or (lambda B,s,a:True)
        for row in P.values(): assert len(row)==n and sum(row)==1 and min(row)>=0
    def child(self,B,s,a,y):
        return frozenset(t for t in B if self.P[t,s,a][y]>0)
    def local_update(self,B,W,lower):
        allowed={(s,a) for s in W for a in self.A if lower[s,a] and all(
            self.child(B,s,a,y)!=B or y in W for y in self.S)}
        succ={e:{y for y in self.S if self.child(B,*e,y)==B} for e in allowed}
        adj={s:set() for s in W}
        for e in allowed: adj[e[0]]|=succ[e]
        retain=set(W)
        for theta in B:
            E={e for e in allowed if all(not self.P[theta,*e][y] or self.child(B,*e,y)==B for y in self.S)}
            rounds=0
            while True:
                ds=mecs(W,E,succ);keep=set().union(*ds) if ds else set();remove=set()
                for D in ds:
                    for sigma in B:
                        if all(self.P[sigma,*e]==self.P[theta,*e] for e in D):
                            d=min(self.colors[sigma,*e] for e in D)
                            if d%2: remove|={e for e in D if self.colors[sigma,*e]==d}
                new=keep-remove
                if new==E: break
                assert new<E
                rounds+=1;assert rounds<=len(self.S)*len(self.A);E=new
            targets={s for D in ds for s,a in D}
            targets|={s for s,a in allowed if any(self.P[theta,s,a][y]>0 and self.child(B,s,a,y)!=B for y in self.S)}
            retain&={s for s in W if reachable([s],adj)&targets}
        return frozenset(retain)
    def region_from_lower(self,B,lower):
        W=frozenset(self.S);rounds=0
        while True:
            nxt=self.local_update(B,W,lower)
            if nxt==W:return W
            assert nxt<W;rounds+=1;assert rounds<=len(self.S);W=nxt
    def bottom_up(self):
        regions={}
        for B in subsets(self.models):
            lower={}
            for s,a in product(self.S,self.A):
                lower[s,a]=self.menu(B,s,a)
                for y in self.S:
                    C=self.child(B,s,a,y)
                    if C and C!=B and y not in regions[C]:lower[s,a]=False
            regions[B]=self.region_from_lower(B,lower)
        return regions
    def dfs_bit(self,B,x,stats,depth=1):
        stats['calls']+=1;stats['peak_depth']=max(stats['peak_depth'],depth)
        assert depth<=len(self.models)
        lower={}
        for s,a in product(self.S,self.A):
            safe=self.menu(B,s,a)
            if safe:
                for y in self.S:
                    C=self.child(B,s,a,y)
                    if C and C!=B:
                        stats['child_queries']+=1
                        assert len(C)<len(B)
                        # Returned region is never retained, only this Boolean.
                        if not self.dfs_bit(C,y,stats,depth+1):safe=False;break
            lower[s,a]=safe
        W=self.region_from_lower(B,lower)
        return x in W

def dense(n,m,k,row_fn,color_fn,menu=None):
    return System(n,m,k,{(t,s,a):tuple(map(F,row_fn(t,s,a))) for t,s,a in product(range(k),range(n),range(m))},
                  {(t,s,a):color_fn(t,s,a) for t,s,a in product(range(k),range(n),range(m))},menu)

def compare(name,sys,expected=None):
    ref=sys.bottom_up();stats={'calls':0,'child_queries':0,'peak_depth':0};checks=0
    for B,W in ref.items():
        for s in sys.S:
            assert sys.dfs_bit(B,s,stats)==(s in W),(name,B,s,W)
            checks+=1
    if expected is not None:assert ref[frozenset(sys.models)]==frozenset(expected)
    return {'name':name,'models':len(sys.models),'states':len(sys.S),'actions':len(sys.A),
            'membership_comparisons':checks,'reference_regions':len(ref),**stats}

def named_controls():
    out=[]
    # All physical rows agree, so opposite coBuchi actions are impossible.
    out.append(compare('identical_opposite_objectives',dense(1,2,2,lambda t,s,a:(1,),lambda t,s,a:2 if a==t else 1),[]))
    out.append(compare('quarter_receipts_unbounded_memory',dense(2,2,2,
        lambda t,s,a:(F(3,4),F(1,4)) if t==0 else (F(1,4),F(3,4)),lambda t,s,a:2 if a==t else 1),[0,1]))
    out.append(compare('successive_odd_layers',dense(1,3,2,lambda t,s,a:(1,),
        lambda t,s,a:2*a if t==0 else [1,3,4][a]),[0]))
    out.append(compare('larger_odd_priority_is_allowed',dense(2,1,1,
        lambda t,s,a:(0,1) if s==0 else (1,0),lambda t,s,a:2+s),[0,1]))
    out.append(compare('revealing_child_wins',dense(2,1,2,
        lambda t,s,a:(1,0) if t==0 and s==0 else ((F(1,2),F(1,2)) if s==0 else (0,1)),
        lambda t,s,a:2 if t==0 or s==1 else 1),[0,1]))
    out.append(compare('revealing_child_loses',dense(2,1,2,
        lambda t,s,a:(1,0) if t==0 and s==0 else ((F(1,2),F(1,2)) if s==0 else (0,1)),
        lambda t,s,a:2 if t==0 else 1),[]))
    out.append(compare('nonmonotone_support_menu',dense(2,2,2,
        lambda t,s,a:(1,0) if t==0 else (0,1),lambda t,s,a:2,
        lambda B,s,a: a==(0 if len(B)==2 else 1)),[0,1]))
    # Every support deletion can leave k-1 models; duplicate action rows force
    # repeated child calls, rather than retaining child region tables.
    def stair(t,s,a):
        y=4 if s==4 or s==3 or t==s else s+1
        return tuple(int(j==y) for j in range(5))
    out.append(compare('four_model_depth_and_recomputation',dense(5,2,4,stair,lambda t,s,a:2),range(5)))
    assert out[-1]['peak_depth']==4
    assert out[-1]['calls']>out[-1]['reference_regions']*out[-1]['states']
    return out

if __name__=='__main__':
    named=named_controls()
    # A bounded complete grid, chosen to exercise zero support updates, NOT a
    # large random census: all 81 binary-state one-action two-model row kernels
    # over {Dirac0,Dirac1,half}, with four fixed priority patterns.
    rows=((F(1),F(0)),(F(0),F(1)),(F(1,2),F(1,2)))
    patterns=((2,2,2,2),(1,1,1,1),(2,1,1,2),(0,3,2,1))
    count=checks=calls=0;peak=0
    for row_ids in product(range(3),repeat=4):
        P={(t,s,0):rows[row_ids[2*t+s]] for t,s in product(range(2),repeat=2)}
        for cs in patterns:
            sys=System(2,1,2,P,{(t,s,0):cs[2*t+s] for t,s in product(range(2),repeat=2)})
            r=compare('complete_grid',sys)
            count+=1;checks+=r['membership_comparisons'];calls+=r['calls'];peak=max(peak,r['peak_depth'])
    result={'status':'PASS_EXACT_DEPTH_FIRST_EQUIVALENCE','named_controls':named,
        'bounded_complete_grid':{'systems':count,'membership_comparisons':checks,'dfs_calls':calls,'peak_depth':peak},
        'random_cases':0,'scope':'Recursion scheduling equivalence; shared local pruning is not an independent proof of that routine.',
        'space_evidence':'Scalar depth and call counters are finite controls, not empirical proof of asymptotic space complexity.'}
    print(json.dumps(result,indent=2,sort_keys=True))
