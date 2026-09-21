"""Finite CV-C probes. Exact rational arithmetic, not infinite proof evidence.

No changes to the frozen operational engine. This implements the finite-state
case and finite cylinder expressions from DEFECT_COMPUTABILITY.md.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

@dataclass(frozen=True)
class Mealy:
    rows: tuple[tuple[tuple[int,int],tuple[int,int]], ...]

    def __post_init__(self) -> None:
        n=len(self.rows)
        if not 1<=n<=16:raise ValueError('one to sixteen states required for this probe')
        for row in self.rows:
            if len(row)!=2:raise ValueError('exactly two input transitions required')
            for target,bit in row:
                if type(target) is not int or not 0<=target<n:raise ValueError('invalid state')
                if type(bit) is not int or bit not in (0,1):raise ValueError('invalid bit')

    def output(self, word:Iterable[int], state:int=0) -> tuple[int,...]:
        if type(state) is not int or not 0<=state<len(self.rows):raise ValueError('invalid initial state')
        out=[]
        for bit in word:
            if type(bit) is not int or bit not in (0,1):raise ValueError('invalid input bit')
            state,y=self.rows[state][bit];out.append(y)
        return tuple(out)

    def deterministic_states(self) -> frozenset[int]:
        n=len(self.rows);rel={(s,t) for s in range(n) for t in range(n)}
        while True:
            keep={(s,t) for s,t in rel
                  if all(self.rows[s][b][1]==self.rows[t][c][1] and
                         (self.rows[s][b][0],self.rows[t][c][0]) in rel
                         for b in (0,1) for c in (0,1))}
            if keep==rel:return frozenset(s for s in range(n) if (s,s) in rel)
            rel=keep

    def defect(self,state:int=0) -> Fraction:
        if type(state) is not int or not 0<=state<len(self.rows):raise ValueError('invalid initial state')
        deterministic=self.deterministic_states()
        reach=set(deterministic)
        while True:
            new=reach|{s for s,row in enumerate(self.rows) if any(t in reach for t,_ in row)}
            if new==reach:break
            reach=new
        if state in deterministic:return Fraction(0)
        if state not in reach:return Fraction(1)
        transient=sorted(reach-deterministic);index={s:i for i,s in enumerate(transient)}
        n=len(transient);matrix=[[Fraction(int(i==j)) for j in range(n)]+[Fraction(0)] for i in range(n)]
        for s,i in index.items():
            for t,_ in self.rows[s]:
                if t in deterministic:matrix[i][-1]+=Fraction(1,2)
                elif t in index:matrix[i][index[t]]-=Fraction(1,2)
        # Exact elimination. Reachability construction makes this system transient.
        for c in range(n):
            pivot=next((r for r in range(c,n) if matrix[r][c]),None)
            if pivot is None:raise ArithmeticError('unexpected singular transient system')
            matrix[c],matrix[pivot]=matrix[pivot],matrix[c]
            scale=matrix[c][c];matrix[c]=[x/scale for x in matrix[c]]
            for r in range(n):
                if r!=c:
                    scale=matrix[r][c]
                    matrix[r]=[x-scale*y for x,y in zip(matrix[r],matrix[c])]
        answer=1-matrix[index[state]][-1]
        if not 0<=answer<=1:raise ArithmeticError('invalid hitting probability')
        return answer

def soft_mass(masses:Iterable[Fraction],k:int) -> Fraction:
    if type(k) is not int or not 0<=k<=1024:raise ValueError('bounded nonnegative precision required')
    xs=list(masses)
    if any(not isinstance(x,Fraction) or x<0 for x in xs) or sum(xs,Fraction())!=1:
        raise ValueError('exact rational probability vector required')
    eps=Fraction(1,2**k)
    return sum((max(x-eps,Fraction()) for x in xs),Fraction())
