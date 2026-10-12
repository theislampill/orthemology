"""Independent finite P01 probes, not a proof kernel or canonical-engine patch.

Syntax is immutable and uses tagged tuples. Lambda binders use de Bruijn
indices; free variables have a separate tag. Only explicit finite relations,
reduction paths and rational distributions are evaluated.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from typing import Callable, Mapping

Term = tuple
I: Term = ('I',)
K: Term = ('K',)
S: Term = ('S',)
ZERO: Term = ('zero',)
ONE: Term = ('one',)

def V(n: int) -> Term:
    if n < 0: raise ValueError('negative free variable')
    return ('v', n)

def A(*ts: Term) -> Term:
    if not ts: raise ValueError('application needs at least one term')
    z = ts[0]
    for t in ts[1:]: z = ('a', z, t)
    return z

@dataclass(frozen=True)
class Witness:
    rule: str
    path: tuple[int, ...]
    target: Term

def root(t: Term) -> tuple[str, Term] | None:
    if t[0] != 'a': return None
    f, x = t[1:]
    if f == I: return ('I', x)
    if f[0] == 'a' and f[1] == K: return ('K', f[2])
    if f[0] == 'a' and f[1][0] == 'a' and f[1][1] == S:
        g, h = f[1][2], f[2]
        return ('S', A(g, x, A(h, x)))
    return None

@lru_cache(maxsize=200000)
def step_edges(t: Term) -> tuple[Witness, ...]:
    out: list[Witness] = []
    r = root(t)
    if r: out.append(Witness(r[0], (), r[1]))
    if t[0] == 'a':
        for w in step_edges(t[1]):out.append(Witness(w.rule, (1,)+w.path, A(w.target,t[2])))
        for w in step_edges(t[2]):out.append(Witness(w.rule, (2,)+w.path, A(t[1],w.target)))
    return tuple(out)

def steps(t: Term) -> set[Term]: return {w.target for w in step_edges(t)}

def subst(t: Term, sigma: Mapping[int, Term]) -> Term:
    if t[0] == 'v': return sigma.get(t[1],t)
    if t[0] == 'a': return A(subst(t[1],sigma),subst(t[2],sigma))
    return t

def free(t: Term) -> set[int]:
    if t[0] == 'v': return {t[1]}
    if t[0] == 'a': return free(t[1])|free(t[2])
    return set()

# Lambda syntax: b/bound, f/free, c/inert constant, l/abstraction, a/application.
def L(t: Term) -> Term: return ('l',t)
def B(n: int) -> Term: return ('b',n)
LI=L(B(0))
LK=L(L(B(1)))
LS=L(L(L(A(B(2),B(0),A(B(1),B(0))))))

@lru_cache(maxsize=200000)
def translate(t: Term) -> Term:
    if t == I:return LI
    if t == K:return LK
    if t == S:return LS
    if t[0] == 'v':return ('f',t[1])
    if t[0] == 'a':return A(translate(t[1]),translate(t[2]))
    if t in (ZERO,ONE):return ('c',t[0])
    raise ValueError(f'unknown SKI term {t!r}')

def shift(t: Term, amount: int, cutoff: int=0) -> Term:
    if t[0]=='b':
        n=t[1]+amount if t[1]>=cutoff else t[1]
        if n<0:raise ValueError('ill-scoped de Bruijn shift')
        return B(n)
    if t[0]=='l':return L(shift(t[1],amount,cutoff+1))
    if t[0]=='a':return A(shift(t[1],amount,cutoff),shift(t[2],amount,cutoff))
    return t

def bsubst(t: Term, index: int, value: Term, depth: int=0) -> Term:
    if t[0]=='b':return shift(value,depth) if t[1]==index+depth else t
    if t[0]=='l':return L(bsubst(t[1],index,value,depth+1))
    if t[0]=='a':return A(bsubst(t[1],index,value,depth),bsubst(t[2],index,value,depth))
    return t

def beta(body: Term, value: Term) -> Term:
    return shift(bsubst(body,0,shift(value,1)),-1)

def lsteps(t: Term) -> set[Term]:
    out=set()
    if t[0]=='a':
        f,x=t[1:]
        if f[0]=='l':out.add(beta(f[1],x))
        out.update(A(u,x) for u in lsteps(f))
        out.update(A(f,u) for u in lsteps(x))
    elif t[0]=='l':out.update(L(u) for u in lsteps(t[1]))
    return out

def lcontract_at(t: Term, path: tuple[int,...]) -> Term:
    if not path:
        if t[0]!='a' or t[1][0]!='l':raise ValueError('not a beta redex')
        return beta(t[1][1],t[2])
    k,*rest=path
    if t[0]!='a' or k not in (1,2):raise ValueError('invalid applicative path')
    return A(lcontract_at(t[1],tuple(rest)),t[2]) if k==1 else A(t[1],lcontract_at(t[2],tuple(rest)))

def simulate(t: Term, witness: Witness) -> tuple[Term,...]:
    """Construct 1/2/3 beta steps, without normalising the translated endpoints."""
    if witness not in step_edges(t):raise ValueError('not a source step witness')
    local={'I':[()], 'K':[(1,),()], 'S':[(1,1),(1,),()]}[witness.rule]
    seq=[translate(t)]
    for q in local:seq.append(lcontract_at(seq[-1],witness.path+q))
    if seq[-1]!=translate(witness.target):raise AssertionError('simulation endpoint mismatch')
    return tuple(seq)

def lfree_subst(t: Term,sigma: Mapping[int,Term],depth: int=0) -> Term:
    if t[0]=='f':return shift(sigma[t[1]],depth) if t[1] in sigma else t
    if t[0]=='a':return A(lfree_subst(t[1],sigma,depth),lfree_subst(t[2],sigma,depth))
    if t[0]=='l':return L(lfree_subst(t[1],sigma,depth+1))
    return t

def trename(t: Term,r: Callable[[int],int]) -> Term:
    if t[0]=='t':return ('t',r(t[1]))
    if t[0]=='arr':return ('arr',trename(t[1],r),trename(t[2],r))
    if t[0]=='all':return ('all',trename(t[1],lambda n:0 if n==0 else r(n-1)+1))
    if t==('bot',):return t
    raise ValueError('unknown type')

def tsubst(t: Term,sigma: Callable[[int],Term]) -> Term:
    if t[0]=='t':return sigma(t[1])
    if t[0]=='arr':return ('arr',tsubst(t[1],sigma),tsubst(t[2],sigma))
    if t[0]=='all':
        return ('all',tsubst(t[1],lambda n:('t',0) if n==0 else trename(sigma(n-1),lambda k:k+1)))
    if t==('bot',):return t
    raise ValueError('unknown type')

@lru_cache(maxsize=200000)
def parallel(t: Term) -> frozenset[Term]:
    if t[0]!='a':return frozenset([t])
    f,x=t[1:]
    out={A(g,y) for g in parallel(f) for y in parallel(x)}
    if f==I:out.update(parallel(x))
    if f[0]=='a' and f[1]==K:out.update(parallel(f[2]))
    if f[0]=='a' and f[1][0]=='a' and f[1][1]==S:
        out.update(A(g,y,A(h,y)) for g in parallel(f[1][2]) for h in parallel(f[2]) for y in parallel(x))
    return frozenset(out)

@lru_cache(maxsize=200000)
def develop(t: Term) -> Term:
    if t[0]!='a':return t
    f,x=t[1:]
    if f==I:return develop(x)
    if f[0]=='a' and f[1]==K:return develop(f[2])
    if f[0]=='a' and f[1][0]=='a' and f[1][1]==S:
        return A(develop(f[1][2]),develop(x),A(develop(f[2]),develop(x)))
    return A(develop(f),develop(x))

D=A(S,I,I)

def omega_cycle() -> tuple[Term,Term,Term]:
    return A(D,D),A(A(I,D),A(I,D)),A(D,A(I,D))

def tower_depth(t: Term) -> int | None:
    n=0
    while t!=D:
        if t[0]!='a' or t[1]!=I:return None
        n+=1;t=t[2]
    return n

def omega_shape(t: Term) -> tuple[int,int] | None:
    if t[0]!='a':return None
    a,b=tower_depth(t[1]),tower_depth(t[2])
    return None if a is None or b is None else (a,b)

def abstract(variable: int,t: Term) -> Term:
    """Non-eta bracket abstraction, with the variable-free K optimisation."""
    if t==V(variable):return I
    if variable not in free(t):return A(K,t)
    if t[0]=='a':return A(S,abstract(variable,t[1]),abstract(variable,t[2]))
    raise ValueError('malformed open term')

def abstraction_path(variable: int,t: Term,value: Term) -> tuple[Term,...]:
    start=A(abstract(variable,t),value)
    if t==V(variable) or variable not in free(t):return (start,subst(t,{variable:value}))
    l,r=t[1:];bl,br=abstract(variable,l),abstract(variable,r)
    out=[start,A(A(bl,value),A(br,value))]
    lp=abstraction_path(variable,l,value)
    out.extend(A(v,A(br,value)) for v in lp[1:])
    rp=abstraction_path(variable,r,value)
    out.extend(A(lp[-1],v) for v in rp[1:])
    return tuple(out)

Distribution=dict[Term,Fraction]

def mass(e: tuple) -> Distribution:
    if e[0]=='pure':return {e[1]:Fraction(1)}
    out: Distribution={}
    if e[0]=='mix':
        p,l,r=e[1:]
        if not isinstance(p,Fraction) or not 0<=p<=1:raise ValueError('invalid rational weight')
        for w,d in ((p,mass(l)),(1-p,mass(r))):
            for x,m in d.items():out[x]=out.get(x,Fraction(0))+w*m
    elif e[0]=='eapp':
        for f,a in mass(e[1]).items():
            for x,b in mass(e[2]).items():out[A(f,x)]=out.get(A(f,x),Fraction(0))+a*b
    else:raise ValueError('unknown effect syntax')
    return {x:w for x,w in out.items() if w>0}

def diagonal_coupling(m: Distribution) -> dict[tuple[Term,Term],Fraction]:
    if sum(m.values())!=1 or any(v<=0 for v in m.values()):raise ValueError('not a probability distribution')
    return {(t,t):v for t,v in m.items()}

def marginals(c: dict) -> tuple[dict,dict]:
    left,right={},{}
    for (x,y),v in c.items():
        left[x]=left.get(x,Fraction(0))+v;right[y]=right.get(y,Fraction(0))+v
    return left,right

def fair_couplings(relation: set[tuple[int,int]]) -> list[dict]:
    """Witness search for the fixed fair two-point model, not a general solver.
    The endpoints suffice: any feasible allowed-support graph has one of the
    two perfect matchings. The midpoint is included as an explicit control.
    """
    out=[]
    for q in (Fraction(0),Fraction(1,4),Fraction(1,2)):
        c={(0,0):q,(0,1):Fraction(1,2)-q,(1,0):Fraction(1,2)-q,(1,1):q}
        c={p:v for p,v in c.items() if v>0}
        if set(c)<=relation:out.append(c)
    return out

@lru_cache(maxsize=None)
def terms_of_size(size: int,atoms: tuple[Term,...]) -> tuple[Term,...]:
    if size==1:return atoms
    if size<=0 or size%2==0:return ()
    return tuple(A(a,b) for l in range(1,size-1,2) for a in terms_of_size(l,atoms)
                 for b in terms_of_size(size-1-l,atoms))

def show(t: Term) -> str:
    if t[0]=='a':return f'({show(t[1])} {show(t[2])})'
    if t[0] in ('v','b','f'):return f'{t[0]}{t[1]}'
    if t[0]=='l':return f'(lambda {show(t[1])})'
    if t[0]=='c':return t[1]
    return t[0]

def abstract_eta(variable: int,t: Term) -> Term:
    """Separate diagnostic variant: adds the usual x-free f x eta shortcut.
    It is not used to define canonical conversion or the base bracket probe.
    """
    if t==V(variable):return I
    if variable not in free(t):return A(K,t)
    if t[0]=='a':
        if t[2]==V(variable) and variable not in free(t[1]):return t[1]
        return A(S,abstract_eta(variable,t[1]),abstract_eta(variable,t[2]))
    raise ValueError('malformed open term')
