"""Exact finite candidate solver for common-support hidden-target Markov models.
The ordinary stochastic correctness proof is supplied separately. This programme
contains no learning runtime and does not certify an empirical model.
"""
from fractions import Fraction
from dataclasses import dataclass
from collections import deque
import argparse,json

@dataclass
class ModelFamily:
    probabilities:list
    good:list
    menus:dict
    def validate(self):
        # Freeze extensional finite data once before equality or repeated traversal.
        self.probabilities=tuple(tuple(tuple(tuple(row) for row in actions) for actions in states) for states in self.probabilities)
        self.good=tuple(frozenset(g) for g in self.good)
        self.menus={s:frozenset(actions) for s,actions in self.menus.items()}
        if not self.probabilities:raise ValueError('At least one hidden model is required')
        self.m=len(self.probabilities);self.n=len(self.probabilities[0])
        if not self.n:raise ValueError('At least one observed state is required')
        self.a=len(self.probabilities[0][0])
        if len(self.good)!=self.m or set(self.menus)!=set(range(self.n)):raise ValueError('Dimension mismatch')
        for rows in self.probabilities:
            if len(rows)!=self.n:raise ValueError('State dimension mismatch')
            for actions in rows:
                if len(actions)!=self.a:raise ValueError('Action dimension mismatch')
                for row in actions:
                    if len(row)!=self.n or any(not isinstance(p,Fraction) or p<0 for p in row) or sum(row)!=1:
                        raise ValueError('Rows must be exact nonnegative rational probabilities summing to one')
        self.support={}
        for s in range(self.n):
            if not self.menus[s]<=set(range(self.a)):raise ValueError('Invalid menu action')
            for a in range(self.a):
                base=frozenset(t for t,p in enumerate(self.probabilities[0][s][a]) if p)
                if a in self.menus[s] and any(frozenset(t for t,p in enumerate(rows[s][a]) if p)!=base for rows in self.probabilities):
                    raise ValueError('Transition supports differ between hidden models')
                self.support[s,a]=base
        pairs={(s,a) for s in range(self.n) for a in range(self.a)}
        if any(not g<=pairs for g in self.good):raise ValueError('Invalid good pair')
        return self


def sccs(graph):
    # Iterative Kosaraju avoids a Python recursion-depth boundary.
    seen=set();order=[]
    for start in sorted(graph):
        if start in seen:continue
        stack=[(start,False)]
        while stack:
            s,done=stack.pop()
            if done:order.append(s);continue
            if s in seen:continue
            seen.add(s);stack.append((s,True))
            stack.extend((t,False) for t in sorted(graph[s],reverse=True) if t not in seen)
    reverse={s:set() for s in graph}
    for s,ts in graph.items():
        for t in ts:reverse[t].add(s)
    seen=set();out=[]
    for start in reversed(order):
        if start in seen:continue
        C=set();stack=[start];seen.add(start)
        while stack:
            s=stack.pop();C.add(s)
            for t in reverse[s]:
                if t not in seen:seen.add(t);stack.append(t)
        out.append(frozenset(C))
    return out


def maximal_end_components(family,W,allowed):
    pending=[frozenset(W)];out=[]
    while pending:
        C=pending.pop()
        while C:
            U={s:frozenset(a for a in allowed[s] if family.support[s,a]<=C) for s in C}
            D=frozenset(s for s in C if U[s])
            if D==C:break
            C=D
        if not C:continue
        graph={s:set().union(*(family.support[s,a] for a in U[s])) for s in C}
        components=sccs(graph)
        if len(components)==1:out.append((C,U))
        else:pending.extend(components)
    return sorted(out,key=lambda pair:tuple(sorted(pair[0])))


def verifying_components(family,W,theta):
    allowed={s:frozenset(a for a in family.menus[s] if (s,a) in family.good[theta]) for s in W}
    pending=maximal_end_components(family,W,allowed);out=[];deleted=0
    while pending:
        C,U=pending.pop();pairs={(s,a) for s in C for a in U[s]}
        same=[theta]
        V={s:frozenset(a for a in U[s] if all((s,a) in family.good[j] for j in same)) for s in C}
        removed=sum(len(U[s]-V[s]) for s in C);deleted+=removed
        if removed:pending.extend(maximal_end_components(family,C,V))
        else:out.append((C,U))
    return sorted(out,key=lambda pair:tuple(sorted(pair[0]))),deleted


def backward_reach(family,W,target):
    safe={s:frozenset(a for a in family.menus[s] if family.support[s,a]<=W) for s in W}
    reverse={s:set() for s in W}
    for s in W:
        for a in safe[s]:
            for t in family.support[s,a]:reverse[t].add(s)
    distance={s:0 for s in target};queue=deque(sorted(target))
    while queue:
        t=queue.popleft()
        for s in sorted(reverse[t]):
            if s not in distance:distance[s]=distance[t]+1;queue.append(s)
    return distance,safe


def solve(family):
    family.validate();W=frozenset(range(family.n));trace=[]
    while True:
        successor=set(W);certificates=[]
        for theta in range(family.m):
            components,deleted=verifying_components(family,W,theta)
            target=set().union(*(C for C,U in components)) if components else set()
            distances,safe=backward_reach(family,W,target)
            successor.intersection_update(distances)
            certificates.append({'model':theta,'target':sorted(target),'distances':distances,'components':[{'states':sorted(C),'actions':{s:sorted(U[s]) for s in C}} for C,U in components],'deleted_actions':deleted})
        trace.append({'region':sorted(W),'next_region':sorted(successor),'models':certificates})
        if successor==W:
            return {'status':'VALID','winning_states':sorted(W),'common_navigation_actions':{s:sorted(safe[s]) for s in W},'iterations':len(trace),'trace':trace,'scope':'Exact finite candidate region and component witnesses; stochastic theorem and learning implementation are separate'}
        W=frozenset(successor)


def from_json(obj):
    if not isinstance(obj,dict):raise ValueError("Input must be a JSON object")
    if not isinstance(obj.get("menus"),dict):raise ValueError("Menus must be a JSON object keyed by state")
    # Strings or integers only: binary floats must not silently determine support.
    def q(x):
        if isinstance(x,bool) or not isinstance(x,(str,int)):raise ValueError('Use integer or rational string probabilities, never floats')
        return Fraction(x)
    return ModelFamily([[[tuple(q(p) for p in row) for row in actions] for actions in states] for states in obj['probabilities']],
        [frozenset(tuple(pair) for pair in good) for good in obj['good']],
        {int(s):frozenset(actions) for s,actions in obj['menus'].items()})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');args=ap.parse_args()
    try:result=solve(from_json(json.load(open(args.input))))
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as error:result={'status':'INVALID','reason':str(error)}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
