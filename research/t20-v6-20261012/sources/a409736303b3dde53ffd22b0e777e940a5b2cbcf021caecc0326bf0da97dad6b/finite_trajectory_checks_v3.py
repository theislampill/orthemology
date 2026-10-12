#!/usr/bin/env python3
"""Exact finite models for source-independent regression comparisons, not physical evidence."""
from __future__ import annotations

from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
from typing import Callable, Hashable, Iterable, Sequence
import sys

if not __debug__:
    raise SystemExit("Optimised execution is not accepted as verification.")

def compositions(total: int, parts: int):
    if total < 0 or parts < 1:
        raise ValueError("Require a nonnegative total and positive part count.")
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total-first, parts-1):
            yield (first,) + rest

def _relation(allowed):
    value = tuple(frozenset(a) for a in allowed)
    if not value or any(not a for a in value):
        raise ValueError("This finite relation contract requires nonempty worlds and acceptable sets.")
    return value

def cover_number(allowed) -> int:
    allowed = _relation(allowed)
    universe = tuple(sorted(set().union(*allowed), key=repr))
    for size in range(1,len(universe)+1):
        for chosen in combinations(universe,size):
            if all(set(chosen) & a for a in allowed):
                return size
    raise RuntimeError("The full candidate universe failed to cover nonempty acceptable sets.")

def _partitions(n):
    if n == 0:
        yield ()
        return
    for previous in _partitions(n-1):
        for index in range(len(previous)):
            yield previous[:index]+(previous[index]+(n-1,),)+previous[index+1:]
        yield previous+((n-1,),)

def partition_number(allowed) -> int:
    allowed = _relation(allowed)
    best = len(allowed)
    for partition in _partitions(len(allowed)):
        if len(partition) >= best:
            continue
        if all(set.intersection(*(set(allowed[i]) for i in block))
               for block in partition):
            best = len(partition)
    return best

def round_distribution(p, denominator: int):
    p = tuple(F(v) for v in p)
    if not p or any(v<0 for v in p) or sum(p)!=1 or denominator<1:
        raise ValueError("Require a probability distribution and positive denominator.")
    scaled = tuple(v*denominator for v in p)
    numerators = [v.numerator//v.denominator for v in scaled]
    missing = denominator-sum(numerators)
    order = sorted(range(len(p)), key=lambda i:(-(scaled[i]-numerators[i]),i))
    for i in order[:missing]:
        numerators[i]+=1
    return tuple(F(v,denominator) for v in numerators)

def expected_cost(cost,p,q):
    return sum(F(cost[i][j])*p[i]*q[j] for i in range(len(p)) for j in range(len(q)))

def cost_regret(cost,p,q,player:int):
    incumbent=expected_cost(cost,p,q)
    if player==0:
        alternatives=[sum(F(cost[i][j])*q[j] for j in range(len(q))) for i in range(len(p))]
    elif player==1:
        alternatives=[sum(F(cost[i][j])*p[i] for i in range(len(p))) for j in range(len(q))]
    else:
        raise ValueError("Two-player model: player must be 0 or 1.")
    return incumbent-min(alternatives)

def best_response_step(cost,state,player):
    if player not in (0,1) or state not in tuple(product((0,1),repeat=2)):
        raise ValueError("This model has two binary players.")
    alternate=list(state); alternate[player]=1-alternate[player]
    alternate=tuple(alternate)
    return alternate if cost[alternate[0]][alternate[1]]<cost[state[0]][state[1]] else state

def is_pure_equilibrium(cost,state):
    return all(best_response_step(cost,state,i)==state for i in (0,1))

def simultaneous_trace(cost,start,steps):
    if steps<0:
        raise ValueError("Negative number of steps.")
    path=[tuple(start)]
    for _ in range(steps):
        old=path[-1]
        next_state=tuple(best_response_step(cost,old,i)[i] for i in (0,1))
        path.append(next_state)
    return tuple(path)

def asynchronous_improvement(cost,start):
    path=[tuple(start)]
    while True:
        state=path[-1]
        next_state=next((best_response_step(cost,state,i) for i in (0,1)
                         if best_response_step(cost,state,i)!=state),None)
        if next_state is None:
            return tuple(path)
        if next_state in path or len(path)>=4:
            raise RuntimeError("A strict finite-potential path repeated or exceeded the state count.")
        path.append(next_state)

def logit_transition(cost,bases):
    if len(bases)!=2 or any(F(base)<=1 for base in bases):
        raise ValueError("Require two bases greater than one.")
    if any(int(v)!=v for row in cost for v in row):
        raise ValueError("Exact rational logit implementation uses integer potential values.")
    states=tuple(product((0,1),repeat=2))
    index={s:i for i,s in enumerate(states)}
    matrix=[[F(0) for _ in states] for _ in states]
    for row,state in enumerate(states):
        for player in (0,1):
            alternatives=[]
            for choice in (0,1):
                t=list(state);t[player]=choice;t=tuple(t)
                weight=F(bases[player])**(-int(cost[t[0]][t[1]]))
                alternatives.append((t,weight))
            total=sum(w for _,w in alternatives)
            for t,w in alternatives:
                matrix[row][index[t]]+=F(1,2)*w/total
    return tuple(tuple(row) for row in matrix)

def apply_law(law,matrix):
    return tuple(sum(law[i]*matrix[i][j] for i in range(len(law)))
                 for j in range(len(law)))

def marginals(law):
    if len(law)!=4 or sum(law)!=1:
        raise ValueError("Require a normalised two-by-two joint law.")
    return (law[0]+law[1],law[2]+law[3]),(law[0]+law[2],law[1]+law[3])

def product_law(p,q):
    return tuple(a*b for a in p for b in q)

def calibration_fibres():
    fibres={}
    for c,k in product((0,1),repeat=2):
        fibres.setdefault(c^k,set()).add((c,k))
    return {y:frozenset(v) for y,v in fibres.items()}

def coordinate_query(bits,query):
    if query<0 or query>=len(bits):
        raise ValueError("Query out of range.")
    # The requested coordinate is an actual read; it is not a stored all-answer vector.
    transcript=[]
    transcript.append((query,bits[query]))
    return transcript[-1][1],len(transcript)

def decision_game(initial,actions,transition,observation,terminal_good,candidates,legal,
                  max_beliefs=20000):
    """Least fixed point for a specified finite deterministic labelled-belief decision game.

    Each belief contains (current_state, immutable_initial_answer_label).
    Permissions must hold for every current possibility. Terminal candidates must
    satisfy the provided predicate at every labelled current possibility.
    No state-specific hidden advice enters action choice.
    """
    initial=frozenset(initial)
    actions=tuple(actions);candidates=tuple(candidates)
    if not initial or not candidates:
        raise ValueError("Require a nonempty initial belief and candidate universe.")
    if len({observation(s) for s,label in initial})!=1:
        raise ValueError("Split initial beliefs by their actually observed value first.")
    queue=deque([initial]);discovered={initial}
    graph={};terminal={}
    while queue:
        belief=queue.popleft()
        terminal[belief]=tuple(c for c in candidates
                              if all(terminal_good(c,s,label) for s,label in belief))
        edges=[]
        for a in actions:
            if not all(legal(a,s) for s,label in belief):
                continue
            observations={}
            for state,label in belief:
                successor=transition(a,state)
                observations.setdefault(observation(successor),set()).add((successor,label))
            successors=tuple(frozenset(v) for k,v in sorted(observations.items(),key=lambda v:repr(v[0])))
            if not successors:
                raise RuntimeError("A legal deterministic action produced no successor belief.")
            edges.append((a,successors))
            for successor in successors:
                if successor not in discovered:
                    discovered.add(successor)
                    if len(discovered)>max_beliefs:
                        raise RuntimeError("Declared exploration limit exceeded; no losing verdict inferred.")
                    queue.append(successor)
        graph[belief]=tuple(edges)
    rank={b:0 for b in discovered if terminal[b]}
    policy={b:("return",terminal[b][0]) for b in rank}
    while True:
        additions={}
        for belief in discovered:
            if belief in rank:
                continue
            options=[(1+max(rank[s] for s in succs),a) for a,succs in graph[belief]
                     if all(s in rank for s in succs)]
            if options:
                value,action=min(options,key=lambda pair:(pair[0],repr(pair[1])))
                additions[belief]=(value,action)
        if not additions:
            break
        for belief,(value,action) in additions.items():
            rank[belief]=value;policy[belief]=("act",action)
    # Verify the computed witness against the actually explored transition graph.
    for belief,value in rank.items():
        kind,decision=policy[belief]
        if kind=="return":
            if decision not in terminal[belief] or value!=0:
                raise RuntimeError("Unsound terminal witness.")
        else:
            edges=dict(graph[belief])
            if decision not in edges or not all(s in rank and rank[s]<value for s in edges[decision]):
                raise RuntimeError("Progress witness failed its own transition check.")
    return {"initial_winning":initial in rank,
            "initial_rank":rank.get(initial),
            "reachable_beliefs":len(discovered),
            "winning_beliefs":len(rank),
            "policy_certificate":[{"belief":repr(b),"rank":rank[b],"decision":repr(policy[b])}
                                  for b in sorted(rank,key=repr)],
            "scope":"The specified finite deterministic, exactly observed, initial-labelled model only."}
