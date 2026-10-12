"""P02 exact finite research models. No Lean or infinite-measure verification claimed."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from typing import Hashable, Mapping

Machine = tuple[tuple[tuple[int,int],tuple[int,int]], ...]

def validate_machine(m: Machine) -> None:
    if not isinstance(m,tuple) or not m:
        raise ValueError('A nonempty tuple of binary transition rows is required')
    for row in m:
        if not isinstance(row,tuple) or len(row)!=2:
            raise ValueError('Each state has exactly two equiprobable input transitions')
        for edge in row:
            if not isinstance(edge,tuple) or len(edge)!=2:
                raise ValueError('Each transition is (destination, output_bit)')
            t,b=edge
            if type(t) is not int or type(b) is not int:
                raise TypeError('State and output identifiers must be integers, not booleans')
            if not 0<=t<len(m) or b not in (0,1):
                raise ValueError('Destination or output outside the declared finite domain')

def deterministic_states(m: Machine) -> set[int]:
    """Greatest cross-input relation: every pair of input streams yields the same output."""
    validate_machine(m)
    relation=set(product(range(len(m)), repeat=2))
    while True:
        nxt={(s,t) for s,t in relation
             if all(b==c and (u,v) in relation for u,b in m[s] for v,c in m[t])}
        if nxt==relation:return {s for s in range(len(m)) if (s,s) in relation}
        relation=nxt

def deterministic_states_independent(m: Machine) -> set[int]:
    """Independent power-set evolution; no pair-relation or fixed-point code reused."""
    validate_machine(m); result=set()
    for start in range(len(m)):
        states=frozenset([start]);seen=set()
        while states not in seen:
            seen.add(states)
            if len({b for s in states for _,b in m[s]})!=1:break
            states=frozenset(t for s in states for t,_ in m[s])
        else:result.add(start)
    return result

def solve_linear(a: list[list[F]], b: list[F]) -> list[F]:
    """Exact Gauss-Jordan elimination, refusing singular systems."""
    n=len(b)
    if len(a)!=n or any(len(row)!=n for row in a):raise ValueError('Not a square system')
    x=[list(map(F,row))+[F(c)] for row,c in zip(a,b)]
    for col in range(n):
        pivot=next((i for i in range(col,n) if x[i][col]),None)
        if pivot is None:raise ValueError('Singular system')
        x[col],x[pivot]=x[pivot],x[col]
        scale=x[col][col];x[col]=[v/scale for v in x[col]]
        for i in range(n):
            if i!=col:
                q=x[i][col];x[i]=[v-q*w for v,w in zip(x[i],x[col])]
    return [row[-1] for row in x]

def atomic_mass(m: Machine) -> list[F]:
    """Least probability of reaching deterministic-output states from each state."""
    d=deterministic_states(m); reachable=set(d)
    while True:
        nxt=reachable|{s for s,row in enumerate(m) if any(t in reachable for t,_ in row)}
        if nxt==reachable:break
        reachable=nxt
    h=sorted(reachable-d);position={s:i for i,s in enumerate(h)}
    a=[[F(int(i==j)) for j in range(len(h))] for i in range(len(h))]
    b=[F(0) for _ in h]
    for i,s in enumerate(h):
        for t,_ in m[s]:
            if t in d:b[i]+=F(1,2)
            elif t in position:a[i][position[t]]-=F(1,2)
    solution=solve_linear(a,b)
    out=[F(int(s in d)) for s in range(len(m))]
    for s,v in zip(h,solution):out[s]=v
    return out

def check_law(law: Mapping[Hashable,F]) -> None:
    if not law or any(not isinstance(p,F) for p in law.values()):
        raise TypeError('Nonempty exact Fraction probability table required')
    if any(p<0 for p in law.values()) or sum(law.values())!=1:
        raise ValueError('Weights must be nonnegative and sum exactly to one')

def parity_law(n: int, parity: int) -> dict[tuple[int,...],F]:
    if type(n) is not int or n<1 or type(parity) is not int or parity not in (0,1):
        raise ValueError('Positive dimension and binary parity required')
    return {x:F(1,2**(n-1)) for x in product((0,1),repeat=n) if sum(x)%2==parity}

def marginal(law: Mapping[tuple[int,...],F], coordinates: tuple[int,...]) -> dict[tuple[int,...],F]:
    check_law(law);n=len(next(iter(law)))
    if any(len(x)!=n for x in law) or len(set(coordinates))!=len(coordinates) or any(type(i) is not int or not 0<=i<n for i in coordinates):
        raise ValueError('Invalid coordinate projection')
    out={}
    for x,p in law.items():
        key=tuple(x[i] for i in coordinates);out[key]=out.get(key,F(0))+p
    return {k:v for k,v in out.items() if v}

def mixture(left: Mapping[Hashable,F], right: Mapping[Hashable,F], weight: F) -> dict:
    check_law(left);check_law(right)
    if not isinstance(weight,F) or not 0<=weight<=1:raise ValueError('Exact unit-interval weight required')
    return {x:p for x in left.keys()|right.keys() if (p:=weight*left.get(x,F(0))+(1-weight)*right.get(x,F(0)))}

def selector_bracket(q: F, n: int) -> tuple[F,F,F]:
    """Masses decided below/above q after n fair bits; at most one live dyadic cell."""
    if not isinstance(q,F):raise TypeError('Rational threshold required, not a float')
    if not 0<=q<=1 or type(n) is not int or n<0:raise ValueError('Invalid threshold or depth')
    denominator=2**n
    below=(q.numerator*denominator)//q.denominator
    above=(q.numerator*denominator+q.denominator-1)//q.denominator
    return F(below,denominator),F(above,denominator),F(above-below,denominator)

def soft_mass(cylinders: Mapping[Hashable,F], k: int) -> F:
    check_law(cylinders)
    if type(k) is not int or k<0:raise ValueError('Nonnegative dyadic index required')
    return sum((max(p-F(1,2**k),F(0)) for p in cylinders.values()),F(0))
