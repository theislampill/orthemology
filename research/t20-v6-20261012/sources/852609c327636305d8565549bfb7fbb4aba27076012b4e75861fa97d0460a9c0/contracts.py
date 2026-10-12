"""Finite, exact reference methods for the T20 cross-front synthesis.

This module is a new research diagnostic, not an Orthemology/DAEE production
patch. It checks a declared finite contract, not the truth of its interpretation.
All arithmetic used for decisions is fractions.Fraction. No external packages.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from typing import Mapping, Sequence, Hashable
from types import MappingProxyType


def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError('Use exact integers or Fraction values, not floats/bools')
    return F(x)


@dataclass(frozen=True)
class Contract:
    states: tuple
    actions: tuple
    outcomes: tuple
    labels: Mapping
    enabled: Mapping
    costs: Mapping
    kernels: Mapping

    def __post_init__(self):
        for name in ('states','actions','outcomes'):
            object.__setattr__(self,name,tuple(getattr(self,name)))
        for name in ('states','actions','outcomes'):
            xs=getattr(self,name)
            if not xs or len(xs)!=len(set(xs)):
                raise ValueError(name+' must be a nonempty unique sequence')
        ss=set(self.states); aa=set(self.actions); oo=set(self.outcomes)
        if set(self.labels)!=ss or set(self.enabled)!=ss:
            raise ValueError('Missing or extra state labels/action menus')
        pairs=set()
        for s in self.states:
            actions=self.enabled[s]
            if len(actions)!=len(set(actions)) or not set(actions)<=aa:
                raise ValueError('Invalid action menu')
            for a in actions:
                pairs.add((s,a))
        if set(self.costs)!=pairs or set(self.kernels)!=pairs:
            raise ValueError('Costs/kernels must cover exactly the enabled pairs')
        # Validate and freeze each transition row in the SAME iteration:
        # a one-shot iterable must not be consumed by validation and then lost.
        frozen_kernels={}
        for key in pairs:
            if rational(self.costs[key])<0:
                raise ValueError('Negative cost outside this contract')
            mass=F(0); frozen_row=[]
            for o,t,p in self.kernels[key]:
                if o not in oo or t not in ss:
                    raise ValueError('Unknown outcome or successor')
                p=rational(p)
                if p<0: raise ValueError('Negative transition probability')
                mass+=p; frozen_row.append((o,t,p))
            if mass!=1: raise ValueError('Every enabled row must have total mass one')
            frozen_kernels[key]=tuple(frozen_row)
        # Freeze copies so validation cannot silently be invalidated by a caller.
        for value in self.labels.values():
            try: hash(value)
            except TypeError as e: raise ValueError('Labels must be immutable/hashable') from e
        object.__setattr__(self,'labels',MappingProxyType(dict(self.labels)))
        object.__setattr__(self,'enabled',MappingProxyType({s:tuple(a) for s,a in self.enabled.items()}))
        object.__setattr__(self,'costs',MappingProxyType({k:rational(v) for k,v in self.costs.items()}))
        object.__setattr__(self,'kernels',MappingProxyType(frozen_kernels))


def _blocks_from_keys(states,keys):
    groups={}
    for s in states:
        groups.setdefault(keys[s],[]).append(s)
    return tuple(tuple(v) for v in groups.values())


def _block_map(blocks):
    return {s:i for i,b in enumerate(blocks) for s in b}


def _row_signature(c,s,a,bmap,nblocks):
    out=[]
    for o in c.outcomes:
        for j in range(nblocks):
            out.append(sum((rational(p) for oo,t,p in c.kernels[s,a] if oo==o and bmap[t]==j),F(0)))
    return tuple(out)


def valid_partition(c,blocks,coarse=None):
    # Snapshot the partition ONCE; later validation must see the same blocks.
    blocks=tuple(tuple(b) for b in blocks)
    flat=[s for b in blocks for s in b]
    if not blocks or any(not b for b in blocks) or len(flat)!=len(set(flat)) or set(flat)!=set(c.states):
        return False
    if coarse is not None and set(coarse)!=set(c.states):
        return False
    bm=_block_map(blocks)
    for b in blocks:
        s=b[0]
        for t in b[1:]:
            if coarse is not None and coarse[s]!=coarse[t]: return False
            if c.labels[s]!=c.labels[t] or set(c.enabled[s])!=set(c.enabled[t]): return False
            for a in c.enabled[s]:
                if c.costs[s,a]!=c.costs[t,a]: return False
                if _row_signature(c,s,a,bm,len(blocks))!=_row_signature(c,t,a,bm,len(blocks)): return False
    return True


def coarsest_refinement(c,coarse):
    """Coarsest strong, branch-labelled probabilistic bisimulation refining r.

    Labels, available actions, and immediate costs are included in the initial
    partition. Each later refinement splits on joint outcome/next-block mass.
    """
    if set(coarse)!=set(c.states): raise ValueError('coarse map must cover states')
    keys={s:(coarse[s],c.labels[s],tuple(a for a in c.actions if a in c.enabled[s]),
               tuple(rational(c.costs[s,a]) for a in c.actions if a in c.enabled[s]))
          for s in c.states}
    blocks=_blocks_from_keys(c.states,keys)
    trace=[{'round':0,'blocks':[list(b) for b in blocks]}]
    for step in range(1,len(c.states)+1):
        bm=_block_map(blocks)
        keys={s:(bm[s],tuple((a,_row_signature(c,s,a,bm,len(blocks)))
                             for a in c.actions if a in c.enabled[s])) for s in c.states}
        new=_blocks_from_keys(c.states,keys)
        if new==blocks:
            if not valid_partition(c,blocks,coarse):
                raise RuntimeError('Internal stability verification failed')
            return blocks,trace
        if len(new)<=len(blocks): raise RuntimeError('Refinement failed to progress')
        blocks=new
        trace.append({'round':step,'blocks':[list(b) for b in blocks]})
    raise RuntimeError('Finite refinement bound exceeded')


def quotient(c,blocks):
    if not valid_partition(c,blocks): raise ValueError('Partition does not preserve contract')
    names=tuple('B'+str(i) for i in range(len(blocks)))
    mapping={s:names[i] for i,b in enumerate(blocks) for s in b}
    labels={}; enabled={}; costs={}; kernels={}
    for i,b in enumerate(blocks):
        name=names[i]; s=b[0]; labels[name]=c.labels[s]; enabled[name]=tuple(c.enabled[s])
        for a in enabled[name]:
            costs[name,a]=rational(c.costs[s,a]); rows={}
            for o,t,p in c.kernels[s,a]:
                key=(o,mapping[t]); rows[key]=rows.get(key,F(0))+rational(p)
            kernels[name,a]=tuple((o,t,p) for (o,t),p in rows.items() if p)
    return Contract(names,c.actions,c.outcomes,labels,enabled,costs,kernels),mapping


def sidecar(c,coarse,blocks):
    """Minimal finite alphabet for kappa when the coarse key remains available.

    The returned colour may be reused in different coarse fibres. A standalone
    colour without the coarse key is not promised to identify the refined state.
    """
    if not valid_partition(c,blocks,coarse): raise ValueError('Invalid augmented record')
    fibres={}; out={}
    for i,b in enumerate(blocks):
        z=coarse[b[0]]; fibres.setdefault(z,[]).append(i)
    for ids in fibres.values():
        for colour,i in enumerate(ids):
            for s in blocks[i]: out[s]=colour
    alphabet=max(len(ids) for ids in fibres.values())
    return out,alphabet,(alphabet-1).bit_length()


def finite_values(c,horizon,terminal_loss):
    """Finite-horizon optimal values for a finite fully observed contract.

    Terminal loss is paid at the horizon, or immediately at a state with no
    enabled action. This is not an optimisation over inaccessible hidden state.
    """
    if type(horizon) is not int or horizon<0: raise ValueError('Nonnegative horizon required')
    if set(terminal_loss)!=set(c.states): raise ValueError('Terminal loss must cover states')
    v={s:rational(terminal_loss[s]) for s in c.states}
    for _ in range(horizon):
        v={s:(min(rational(c.costs[s,a])+sum((rational(p)*v[t] for o,t,p in c.kernels[s,a]),F(0))
                  for a in c.enabled[s]) if c.enabled[s] else rational(terminal_loss[s])) for s in c.states}
    return v


def as_reaches(c,start,target,policy):
    """Exact finite-chain almost-sure reachability for a fixed stationary policy."""
    target=frozenset(target)  # reuse target through validation, graph and closure
    if start not in c.states or not set(target)<=set(c.states): raise ValueError('Invalid states')
    succ={}
    for s in c.states:
        if s in target: succ[s]={s}; continue
        if not c.enabled[s]: succ[s]={s}; continue
        a=policy.get(s)
        if a not in c.enabled[s]: raise ValueError('Policy action not enabled')
        succ[s]={t for o,t,p in c.kernels[s,a] if p>0}
    reachable={start}
    while True:
        new=reachable|set().union(*(succ[s] for s in reachable))
        if new==reachable: break
        reachable=new
    can=set(target)
    while True:
        new=can|{s for s in c.states if succ[s]&can}
        if new==can: break
        can=new
    return reachable<=can


def audit_distribution(verifier_accuracy=F(4,5)):
    a=rational(verifier_accuracy)
    if not 0<=a<=1: raise ValueError('Invalid accuracy')
    result={}
    for h,r,v in product((0,1),repeat=3):
        audit=r^v
        result[h,r,audit]=result.get((h,r,audit),F(0))+F(1,4)*(a if v==h else 1-a)
    return result


def posterior(joint,evidence):
    indexes={'H':0,'R':1,'A':2}
    if any(k not in indexes or v not in (0,1) for k,v in evidence.items()): raise ValueError('Invalid evidence')
    vals=[(s,p) for s,p in joint.items() if all(s[indexes[k]]==v for k,v in evidence.items())]
    den=sum((p for s,p in vals),F(0))
    if not den: raise ValueError('Zero-probability observation has no posterior')
    return sum((p for s,p in vals if s[0]==1),F(0))/den


def pair_marginals(joint):
    result={}
    for i,j in combinations(range(3),2):
        tab={}
        for x,p in joint.items(): tab[x[i],x[j]]=tab.get((x[i],x[j]),F(0))+p
        result[i,j]=tab
    return result


def inquiry_values():
    p=(F(0),F(1,2),F(1)); cost=F(5,32); baseline=F(1,2)
    def value(w): return baseline-sum((wi*min(pi,1-pi) for wi,pi in zip(w,p)),F(0))-cost
    return value((F(3,16),F(10,16),F(3,16))),value((F(2,16),F(12,16),F(2,16)))


def total_variation(p,q):
    if len(p)!=len(q): raise ValueError('Dimension mismatch')
    for x in (p,q):
        if any(rational(t)<0 for t in x) or sum(x,F(0))!=1: raise ValueError('Not a probability vector')
    return sum((abs(a-b) for a,b in zip(p,q)),F(0))/2


def conditioned(p,likelihood):
    if len(p)!=len(likelihood) or any(rational(x)<0 for x in p) or sum(p,F(0))!=1: raise ValueError('Invalid prior')
    if any(rational(x)<0 for x in likelihood): raise ValueError('Negative likelihood')
    weights=tuple(a*b for a,b in zip(p,likelihood)); z=sum(weights,F(0))
    if z<=0: raise ValueError('Zero event is not a posterior')
    return tuple(x/z for x in weights)


def _poly_multiply(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return tuple(out)


def moment_witness(d):
    """Positive coordinates fool all polynomial-square tests of degree < d.

    Lower moments come from the uniform law on {1,...,d}. Only moment 2d is
    reduced, by 1/2. The monic polynomial vanishing on the support certifies
    non-realisability. This is a static necessary-condition control, not an ODE.
    """
    if type(d) is not int or d<1: raise ValueError('Positive integer depth required')
    moments=tuple(sum((F(j)**r for j in range(1,d+1)),F(0))/d for r in range(2*d+1))
    altered=moments[:-1]+(moments[-1]-F(1,2),)
    p=(F(1),)
    for j in range(1,d+1): p=_poly_multiply(p,(-F(j),F(1)))
    square=_poly_multiply(p,p)
    return {'degree':d,'moments':altered,'original_moments':moments,'polynomial':p,
            'square_expectation':sum((a*b for a,b in zip(square,altered)),F(0)),
            'original_square_expectation':sum((a*b for a,b in zip(square,moments)),F(0))}


def row_reduce(rows):
    if not rows: return ()
    n=len(rows[0]); a=[list(map(rational,r)) for r in rows]
    if not n or any(len(r)!=n for r in a): raise ValueError('Invalid matrix')
    pivot=0
    for j in range(n):
        idx=next((i for i in range(pivot,len(a)) if a[i][j]),None)
        if idx is None: continue
        a[pivot],a[idx]=a[idx],a[pivot]; scale=a[pivot][j]
        a[pivot]=[x/scale for x in a[pivot]]
        for i in range(len(a)):
            if i!=pivot and a[i][j]:
                scale=a[i][j]; a[i]=[x-scale*y for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a): break
    return tuple(tuple(r) for r in a[:pivot])


def multiply_row(v,a):
    if len(v)!=len(a) or not a or any(len(r)!=len(a[0]) for r in a): raise ValueError('Dimension mismatch')
    v=tuple(map(rational,v));a=tuple(tuple(map(rational,r)) for r in a)
    return tuple(sum((v[i]*a[i][j] for i in range(len(v))),F(0)) for j in range(len(a[0])))


def closure_basis(outputs,actions):
    # The same allowed updates are needed during validation and every round.
    actions=tuple(tuple(tuple(row) for row in a) for a in actions)
    b=row_reduce(outputs)
    if not b: return (),[]
    n=len(b[0])
    if any(len(a)!=n or any(len(r)!=n for r in a) for a in actions): raise ValueError('Non-square action')
    trace=[len(b)]
    for _ in range(n+1):
        new=row_reduce(b+tuple(multiply_row(v,a) for a in actions for v in b))
        if new==b: return b,trace
        if len(new)<=len(b): raise RuntimeError('Closure did not progress')
        b=new; trace.append(len(b))
    raise RuntimeError('Finite linear closure bound exceeded')


def geometric_cometric(l,g):
    """Exact L G^{-1} L^T, specialised to a two-dimensional SPD example."""
    if len(g)!=2 or any(len(r)!=2 for r in g) or g[0][1]!=g[1][0]: raise ValueError('Need symmetric 2x2 Hessian')
    g=tuple(tuple(map(rational,r)) for r in g);l=tuple(tuple(map(rational,r)) for r in l)
    a,b=g[0]; _,c=g[1]; det=a*c-b*b
    if a<=0 or det<=0: raise ValueError('Hessian is not positive definite')
    inv=((c/det,-b/det),(-b/det,a/det))
    if not l or any(len(r)!=2 for r in l): raise ValueError('Invalid projection')
    rows=[multiply_row(v,inv) for v in l]
    return tuple(tuple(sum((x*y for x,y in zip(v,w)),F(0)) for w in l) for v in rows)
