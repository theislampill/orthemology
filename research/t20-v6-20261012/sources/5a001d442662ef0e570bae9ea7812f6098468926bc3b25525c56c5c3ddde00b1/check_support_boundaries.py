#!/usr/bin/env python3
"""Exact small controls for the support-changing ordinary theorem.

This deliberately enumerates components and is not the root production solver.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random


def subsets(xs, nonempty=False):
    xs = tuple(xs)
    for k in range(int(nonempty), len(xs)+1):
        yield from map(frozenset, combinations(xs, k))


class Model:
    def __init__(self, rows, good, menu):
        self.P, self.G, self.menu = rows, tuple(map(frozenset, good)), menu
        self.Theta = frozenset(range(len(rows)))
        self.S = frozenset(range(len(rows[0])))
        self.A = frozenset(range(len(rows[0][0])))
        self.p = min(p for P in rows for ar in P for row in ar for p in row if p)
        for P in rows:
            assert len(P) == len(self.S)
            for ar in P:
                assert len(ar) == len(self.A)
                for row in ar:
                    assert len(row) == len(self.S) and min(row) >= 0 and sum(row) == 1
        self.win = {}
        self.trace = {}

    def update(self, B, e, y):
        s, a = e
        return frozenset(theta for theta in B if self.P[theta][s][a][y] > 0)

    def internal(self, B, e):
        return frozenset(y for y in self.S if self.update(B, e, y) == B)

    def exit_probability(self, B, theta, e):
        s, a = e
        return sum((self.P[theta][s][a][y] for y in self.S
                    if self.update(B, e, y) and self.update(B, e, y) < B), Q(0))

    def allowed(self, B, W):
        E = set()
        for s in W:
            for a in self.menu[B, s]:
                ok = True
                for y in self.S:
                    C = self.update(B, (s, a), y)
                    if C == B and y not in W:
                        ok = False
                    if C and C < B and y not in self.win[C]:
                        ok = False
                if ok:
                    E.add((s, a))
        return frozenset(E)

    def reach(self, B, E, target):
        X = set(target)
        while True:
            new = X | {s for s, a in E if self.internal(B, (s, a)) & X}
            if new == X:
                return frozenset(X)
            X = new

    def is_component(self, B, E):
        if not E:
            return False
        C = frozenset(s for s, a in E)
        return (all(self.internal(B, e) <= C for e in E)
                and all(self.reach(B, E, {t}) >= C for t in C))

    def match(self, theta, sigma, E, B=None, conditional=False):
        for s, a in E:
            r1, r2 = self.P[theta][s][a], self.P[sigma][s][a]
            if conditional:
                I = self.internal(B, (s, a))
                z1, z2 = sum(r1[y] for y in I), sum(r2[y] for y in I)
                if not z1 or not z2 or any(r1[y]/z1 != r2[y]/z2 for y in I):
                    return False
            elif r1 != r2:
                return False
        return True

    def targets(self, B, W, theta, allowed, conditional=False):
        candidates = allowed & self.G[theta]
        candidates = frozenset(e for e in candidates if self.exit_probability(B, theta, e) == 0)
        targets = set()
        for E in subsets(sorted(candidates), True):
            if self.is_component(B, E) and all(E <= self.G[sigma] for sigma in B
                if self.match(theta, sigma, E, B, conditional)):
                targets.update(s for s, a in E)
        return frozenset(targets)

    def stage(self, B, W, conditional=False):
        allowed = self.allowed(B, W)
        result = set(W)
        records = {}
        for theta in B:
            T = self.targets(B, W, theta, allowed, conditional)
            E = frozenset(s for s, a in allowed if self.exit_probability(B, theta, (s, a)) > 0)
            result &= self.reach(B, allowed, T | E)
            records[theta] = (T, E)
        return frozenset(result), allowed, records

    def solve(self, conditional=False):
        self.win, self.trace = {}, {}
        for B in subsets(sorted(self.Theta), True):
            W = self.S
            chain = [W]
            while True:
                nxt, _, _ = self.stage(B, W, conditional)
                assert nxt <= W
                if nxt == W:
                    break
                W = nxt; chain.append(W)
                assert len(chain) <= len(self.S)+1
            self.win[B], self.trace[B] = W, chain
        return self.win


def const_menu(k, n, acts):
    return {(B, s): frozenset(acts) for B in subsets(range(k), True) for s in range(n)}


def reveal_fixture(losing=False):
    P = [
        [[(Q(0),Q(1),Q(0))],[(Q(0),Q(1),Q(0))],[(Q(0),Q(0),Q(1))]],
        [[(Q(0),Q(0),Q(1))],[(Q(0),Q(1),Q(0))],[(Q(0),Q(0),Q(1))]]]
    G = [set() if losing else {(1,0)}, {(2,0)}]
    return Model(P, G, const_menu(2, 3, {0}))


def absent_exit_fixture(eta):
    P0 = [[(1-eta,eta)]*2,[(Q(0),Q(1))]*2]
    P1 = [[(Q(1),Q(0))]*2,[(Q(0),Q(1))]*2]
    return Model([P0,P1], [{(1,0),(1,1)},{(0,1)}], const_menu(2,2,{0,1}))


def conditional_row_fixture():
    P0 = [[(Q(1),Q(0))],[(Q(0),Q(1))]]
    P1 = [[(Q(1,2),Q(1,2))],[(Q(0),Q(1))]]
    return Model([P0,P1], [{(0,0)},{(1,0)}], const_menu(2,2,{0}))


def changing_menu_fixture():
    P = []
    for theta in range(2):
        rows=[]
        for s in range(3):
            rows.append([tuple(Q(t == (theta+1 if s == 0 and a == 0 else s))
                               for t in range(3)) for a in range(3)])
        P.append(rows)
    menu={}
    for B in subsets(range(2),True):
        for s in range(3):
            if s == 0: acts={0}
            elif B == {0}: acts={1}
            elif B == {1}: acts={2}
            else: acts={0}
            menu[B,s]=frozenset(acts)
    return Model(P, [{(s,1) for s in range(3)},{(s,2) for s in range(3)}], menu)


def solve_linear(A, b):
    n=len(b); aug=[list(A[i])+[b[i]] for i in range(n)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[pivot]=aug[pivot],aug[j]
        q=aug[j][j];aug[j]=[x/q for x in aug[j]]
        for i in range(n):
            if i != j:
                q=aug[i][j];aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [row[-1] for row in aug]


def check_navigation(m, counts):
    N, a = len(m.S),len(m.A)
    q=(m.p/a)**N; L=N/q
    for B, W in m.win.items():
        if not W:continue
        _, allowed, targets=m.stage(B,W)
        for theta in B:
            for phi in B:
                T=targets[phi][0]
                H=frozenset(e for e in allowed if m.P[theta][e[0]][e[1]] != m.P[phi][e[0]][e[1]])
                active=sorted(W-T)
                Qmat=[]
                for s in active:
                    acts=[a for u,a in allowed if u==s]
                    row=[]
                    for y in active:
                        row.append(sum((m.P[theta][s][a][y]/len(acts) for a in acts
                                        if (s,a) not in H and m.update(B,(s,a),y)==B),Q(0)))
                    Qmat.append(row)
                if not active:continue
                # Exact probability of avoiding every completed event for N steps.
                v=[Q(1)]*len(active)
                for _ in range(N):
                    v=[sum((Qmat[i][j]*v[j] for j in range(len(active))),Q(0)) for i in range(len(active))]
                assert all(1-x >= q for x in v)
                A=[[Q(i==j)-Qmat[i][j] for j in range(len(active))] for i in range(len(active))]
                waits=solve_linear(A,[Q(1)]*len(active))
                assert all(Q(0)<=t<=L for t in waits)
                counts['candidate_actual_navigation_chains']+=1
                counts['exact_start_state_waits']+=len(active)


def iid_reference(P, good, menus):
    # Direct transcription of the inherited scalar witness/stage condition,
    # independent of the observed-state component construction above.
    k,na,ny=len(P),len(P[0]),len(P[0][0]); win={}
    for B in subsets(range(k),True):
        def upd(a,y):return frozenset(t for t in B if P[t][a][y]>0)
        allow=frozenset(a for a in menus[B] if all(not upd(a,y) or upd(a,y)==B or win[upd(a,y)] for y in range(ny)))
        result=True
        for theta in B:
            progress=any(upd(a,y)<B and P[theta][a][y]>0 for a in allow for y in range(ny))
            sv=any(I<=good[theta] and all(I<=good[sigma] for sigma in B
                    if all(P[theta][a]==P[sigma][a] for a in I)) for I in subsets(sorted(allow),True))
            result &= progress or sv
        win[B]=result
    return win


def main():
    B=frozenset({0,1}); named={}
    ex=reveal_fixture();assert ex.solve()[B]=={0};named['pure_reveal']=[0]
    ex=reveal_fixture(True);assert ex.solve()[B]==set();named['losing_child']=[]
    for eta in (Q(1,2),Q(1,17),Q(1,65537)):
        ex=absent_exit_fixture(eta);assert ex.solve()[B]=={0}
    ex=absent_exit_fixture(Q(0));assert ex.solve()[B]==set()
    named['positive_vs_zero_exit']={'positive':['1/2','1/17','1/65537'],'positive_wins':[0],'zero_wins':[]}
    ex=conditional_row_fixture();assert ex.solve()[B]=={0}
    assert ex.solve(conditional=True)[B]==set()
    named['full_row_matching_required']={'full':[0],'conditional_no_exit':[],'true1_exact_mean_bad':2}
    ex=changing_menu_fixture();assert ex.solve()[B]=={0};named['state_support_menus']=[0]
    P=[[(Q(1),),(Q(1),)]]
    ex=Model([P,P],[{(0,0)},{(0,1)}],const_menu(2,1,{0,1}));assert ex.solve()[B]==set()
    named['identical_opposite']=[]
    words=0
    for n0 in range(1,9):
        for word in product((0,1),repeat=2*n0-1):
            ct=[0,0];stopped=False
            for a in word:
                ct[a]+=1
                if ct[a]>=n0:stopped=True;break
            assert stopped;words+=1
    named['absent_exit_pathwise_rejection']={'thresholds_checked':8,'all_action_words':words,'bound':'2*n0-1'}
    algebra=0
    for d in range(1,9):
        for n0 in range(1,10):
            for r in (Q(1,2),Q(2,3),Q(8,9),Q(50,51)):
                exact=r**n0+d*r**(n0+1)/(1-r)
                crude=d*r**n0/(1-r)
                assert exact<=crude
                exact_J=d*n0+2*d*exact/(1-r)
                crude_J=d*n0+2*d*d*r**n0/(1-r)**2
                assert exact_J<=crude_J;algebra+=1
    counts={'random_systems':0,'candidate_actual_navigation_chains':0,'exact_start_state_waits':0}
    rng=random.Random(391742)
    for trial in range(350):
        n=2 if trial<250 else 3;k=2+(trial%5==0);na=2
        Ps=[]
        for theta in range(k):
            P=[]
            for s in range(n):
                ar=[]
                for a in range(na):
                    ws=[rng.randrange(4) for _ in range(n)]
                    if not any(ws):ws[rng.randrange(n)]=1
                    ar.append(tuple(Q(w,sum(ws)) for w in ws))
                P.append(ar)
            Ps.append(P)
        G=[{(s,a) for s in range(n) for a in range(na) if rng.randrange(4)} for _ in range(k)]
        menu={(C,s):frozenset(a for a in range(na) if rng.randrange(5))
              for C in subsets(range(k),True) for s in range(n)}
        m=Model(Ps,G,menu);m.solve();check_navigation(m,counts);counts['random_systems']+=1
    iid_checks=0
    for trial in range(1200):
        k=2+(trial%3==0);na=2;ny=2
        P=[[tuple([1-(p:=rng.choice([Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)])),p]) for _ in range(na)] for _ in range(k)]
        G=[frozenset(a for a in range(na) if rng.randrange(2)) for _ in range(k)]
        menus={C:frozenset(a for a in range(na) if rng.randrange(4)) for C in subsets(range(k),True)}
        ref=iid_reference(P,G,menus)
        embedded=Model([[P[t] for _ in range(ny)] for t in range(k)],
                       [{(s,a) for s in range(ny) for a in G[t]} for t in range(k)],
                       {(C,s):menus[C] for C in menus for s in range(ny)})
        win=embedded.solve()
        for C in menus:
            assert win[C] == (embedded.S if ref[C] else frozenset());iid_checks+=1
    result={'status':'PASS','scope':'Exact finite boundary and navigation-event controls; ordinary stochastic theorem separate',
            'named':named,'milestone_geometric_sum_checks':algebra,**counts,
            'iid_systems':1200,'iid_support_crosswalks':iid_checks,'seed':391742,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
