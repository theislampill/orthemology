"""Finite read-contract checker. Synthetic exact observations, not permissions.

Adequacy/eligibility are supplied model fields; no flag authenticates evidence
or grants access in an external service. Costs are positive exact rationals.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from heapq import heappush,heappop
from math import inf
from context_effects import Origin,Invalid

class BadCoverage(Invalid):pass

@dataclass(frozen=True)
class Window:
    name:str
    coverage:frozenset
    cost:Fraction
    eligible:bool=True
    adequate:bool=True
    def __post_init__(self):
        if type(self.name) is not str or not self.name:raise Invalid('window name')
        if type(self.coverage) is not frozenset or any(type(x) is not Origin for x in self.coverage):raise Invalid('window origins')
        if type(self.cost) is not Fraction or self.cost<=0:raise Invalid('positive exact rational cost required')
        if type(self.eligible) is not bool or type(self.adequate) is not bool:raise Invalid('window flags')

@dataclass(frozen=True)
class Cover:
    cost:object
    plan:tuple

def active_menu(windows):
    windows=tuple(windows)
    if any(type(w) is not Window for w in windows):raise Invalid('window type')
    if len(set(w.name for w in windows))!=len(windows):raise Invalid('window IDs collide')
    return tuple(w for w in windows if w.eligible and w.adequate)

def _keys(keys):
    keys=frozenset(keys)
    if any(type(k) is not Origin for k in keys):raise Invalid('target key type')
    return keys

def cover_dp(keys,windows):
    """Exact subset-state shortest path; exponential, explicitly capped."""
    keys=sorted(_keys(keys));menu=active_menu(windows)
    if len(keys)>20:raise Invalid('checker target cap20')
    full=(1<<len(keys))-1
    masks=[sum(1<<i for i,k in enumerate(keys) if k in w.coverage) for w in menu]
    dist={0:Fraction(0)};paths={0:()};heap=[(Fraction(0),0)]
    while heap:
        cost,s=heappop(heap)
        if cost!=dist[s]:continue
        if s==full:return Cover(cost,paths[s])
        for w,mask in zip(menu,masks):
            t=s|mask
            if t==s:continue
            v=cost+w.cost
            if v<dist.get(t,inf):
                dist[t]=v;paths[t]=paths[s]+(w.name,);heappush(heap,(v,t))
    return Cover(inf,())

def interval_cover(keys,order,windows):
    """DP after adequate coverage is certified convex on demanded positions.

Raw byte interval endpoints do not establish this premise. All actual extra
reads belong in the same menu, even when they defeat a proposed cost contrast.
"""
    keys=_keys(keys);order=tuple(order);menu=active_menu(windows)
    if len(set(order))!=len(order) or any(type(k) is not Origin for k in order):raise BadCoverage('source order must list unique original keys')
    if not keys<=set(order):raise BadCoverage('target missing from source order')
    if any(not w.coverage<=set(order) for w in menu):raise BadCoverage('window key outside declared source order')
    demanded=[k for k in order if k in keys];m=len(demanded);bounds=[]
    for w in menu:
        ix=[i for i,k in enumerate(demanded) if k in w.coverage]
        if ix and ix!=list(range(ix[0],ix[-1]+1)):raise BadCoverage('justified role coverage is not convex on demanded origins')
        bounds.append(None if not ix else (ix[0],ix[-1]))
    f=[inf]*(m+1);plan=[()]*(m+1);f[m]=Fraction(0)
    for i in range(m-1,-1,-1):
        for w,b in zip(menu,bounds):
            if b is None or not b[0]<=i<=b[1]:continue
            v=w.cost+f[b[1]+1]
            if v<f[i]:f[i]=v;plan[i]=(w.name,)+plan[b[1]+1]
    return Cover(f[0],plan[0])

def role_decision(keys,known):
    keys=_keys(keys)
    for k in keys:
        if k in known and type(known[k]) is not bool:raise Invalid('role evidence must be a Boolean, not truthy data')
    if any(k in known and known[k] is False for k in keys):return False
    if all(k in known for k in keys):return True
    return None # unresolved, not total-decision completion

def _partitions(indices,worlds,fn):
    groups={}
    for i in indices:
        ans=fn(worlds[i])
        try:hash(ans)
        except TypeError:raise Invalid('finite observable response must be hashable')
        groups.setdefault(ans,[]).append(i)
    return tuple(tuple(v) for v in groups.values())

def minimax_cost(worlds,windows,target,response,metadata=lambda _:None):
    """Independent exact finite observation-tree optimisation.

Can analyse richer/correlated responses; does not call either cover solver.
Costs are worst-case over admitted worlds, not expected costs. Public metadata
is observed for free and can defeat a covering lower bound.
"""
    worlds=tuple(worlds);menu=active_menu(windows)
    if not worlds:raise Invalid('empty world family')
    if len(worlds)>256 or len(menu)>24:raise Invalid('finite checker resource cap')
    values=tuple(target(x) for x in worlds)
    if any(type(v) is not bool for v in values):raise Invalid('target must return a Boolean')
    @lru_cache(None)
    def solve(s):
        if len({values[i] for i in s})==1:return Fraction(0)
        best=inf
        for w in menu:
            parts=_partitions(s,worlds,lambda x:response(x,w))
            if len(parts)==1:continue # cannot improve knowledge; positive cost
            cost=w.cost+max(solve(p) for p in parts)
            best=min(best,cost)
        return best
    parts=_partitions(tuple(range(len(worlds))),worlds,metadata)
    return max(solve(p) for p in parts)

def star_locality(worlds,keys,windows,response,metadata=lambda _:None):
    """Check the sufficient all-positive star in a supplied finite table.

This does not establish that a real read service implements the table. Every
observable channel used by a policy must be included in metadata/response.
"""
    worlds=tuple(worlds);keys=_keys(keys);menu=active_menu(windows)
    if not worlds:return False
    for x in worlds:
        if any(k not in x or type(x[k]) is not int or x[k] not in (0,1) for k in keys):raise Invalid('binary target model fields')
    positives=[x for x in worlds if all(x[k]==1 for k in keys)]
    for pos in positives:
        good=True
        for o in keys:
            alternatives=[x for x in worlds if x[o]==0 and all(x[k]==1 for k in keys if k!=o)]
            found=False
            for alt in alternatives:
                if metadata(alt)!=metadata(pos):continue
                if all(response(alt,w)==response(pos,w) for w in menu if o not in w.coverage):found=True;break
            if not found:good=False;break
        if good:return True
    return False

def coverage_sufficiency(worlds,windows,response,metadata=lambda _:None):
    """Finite response-fibre sufficiency for the claimed covered role values.

Separate from star locality: a constant all-key response satisfies locality
vacuously but fails here. Passing is only a finite model-table fact, not source
truth, authentication, interpretive adequacy, permission or deployment evidence.
The complete table can supply a finite decoder when this condition holds.
"""
    worlds=tuple(worlds);menu=active_menu(windows)
    if not worlds:return False
    for win in menu:
        seen={}
        for world in worlds:
            if any(k not in world or type(world[k]) is not int or world[k] not in (0,1) for k in win.coverage):
                raise Invalid('binary covered role fields required')
            observation=(metadata(world),response(world,win))
            try:hash(observation)
            except TypeError:raise Invalid('finite response must be hashable')
            values=tuple((k,world[k]) for k in sorted(win.coverage))
            if observation in seen and seen[observation]!=values:return False
            seen[observation]=values
    return True
