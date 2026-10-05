"""Pure finite source-context effects. No parsing or source authentication.

Origin fields are opaque equality/routing labels in the mathematical API.
Their Python strings are not cryptographic evidence or semantic role oracles.
"""
from dataclasses import dataclass
from typing import Mapping

class Invalid(ValueError): pass
class MissingBinding(Invalid): pass

@dataclass(frozen=True, order=True)
class Origin:
    snapshot: str
    locus: str
    def __post_init__(self):
        if any(type(x) is not str or not x or len(x)>4096 for x in (self.snapshot,self.locus)):
            raise Invalid('origin: nonempty bounded opaque labels required')

@dataclass(frozen=True, order=True)
class Ref:
    index: int
    def __post_init__(self):
        if type(self.index) is not int or self.index<0: raise Invalid('negative/noninteger input reference')

@dataclass(frozen=True)
class Effect:
    depth: int
    prefix: tuple
    consumed: int
    emissions: tuple
    constraints: tuple = ()
    impossible: bool = False

EMPTY = Effect(1,(),0,(),(),True)

def _normal(depth,prefix,consumed,emissions,constraints):
    eq={}
    for expr,key in constraints:
        if not isinstance(key,Origin): raise Invalid('constraint target is not an origin')
        if isinstance(expr,Origin):
            if expr!=key:return EMPTY
        elif isinstance(expr,Ref):
            if expr.index in eq and eq[expr.index]!=key:return EMPTY
            eq[expr.index]=key
        else:raise Invalid('invalid constraint expression')
    e=Effect(depth,tuple(prefix),consumed,tuple(emissions),tuple((Ref(i),eq[i]) for i in sorted(eq)))
    _check(e)
    return e

def _check(e):
    if type(e) is not Effect:raise Invalid('effect type')
    if type(e.depth) is not int or e.depth<1 or type(e.consumed) is not int or not 0<=e.consumed<e.depth:
        raise Invalid('effect depth/tail invariant')
    if type(e.impossible) is not bool:raise Invalid('effect impossible flag')
    if any(type(o) is not Origin for o in e.prefix):raise Invalid('invalid prefix')
    ids=[]
    for t,x in e.emissions:
        if type(t) is not str or not t:raise Invalid('output ID')
        ids.append(t)
        if type(x) is not Origin and not(type(x) is Ref and x.index<e.depth):raise Invalid('emission out of domain')
    if len(ids)!=len(set(ids)):raise Invalid('output occurrence IDs collide')
    for x,o in e.constraints:
        if type(x) is not Ref or x.index>=e.depth or type(o) is not Origin:raise Invalid('constraint out of domain')

def compile_effect(events,selected=None):
    events=tuple(events)
    if len(events)>100000:raise Invalid('checker event cap')
    selected=None if selected is None else frozenset(selected)
    depth=1; prefix=[]; consumed=0; emissions=[]; constraints=[]; seen=set()
    for ev in events:
        if type(ev) not in (tuple,list) or not ev:raise Invalid('event encoding')
        op=ev[0]
        if op=='enter' and len(ev)==2 and type(ev[1]) is Origin:
            prefix.insert(0,ev[1])
        elif op in ('leave','exit'):
            if op=='leave' and len(ev)!=1:raise Invalid('leave arity')
            if op=='exit':
                if len(ev)!=2 or type(ev[1]) is not Origin:raise Invalid('exit origin')
                constraints.append((prefix[0] if prefix else Ref(consumed),ev[1]))
            if prefix:prefix.pop(0)
            else:consumed+=1;depth=max(depth,consumed+1)
        elif op=='emit' and len(ev)==2:
            t=ev[1]
            if type(t) is not str or not t or t in seen:raise Invalid('fresh output ID required')
            seen.add(t)
            if selected is None or t in selected:
                emissions.append((t,prefix[0] if prefix else Ref(consumed)))
        else:raise Invalid('unknown or malformed event')
    if selected is not None and not selected<=seen:raise Invalid('selected output absent from fragment')
    return _normal(depth,prefix,consumed,emissions,constraints)

def compose(f,g):
    _check(f);_check(g)
    if f.impossible or g.impossible:return EMPTY
    if set(t for t,_ in f.emissions)&set(t for t,_ in g.emissions):raise Invalid('alpha-rename output occurrences before composition')
    p=len(f.prefix)
    def subst(x):
        if type(x) is Origin:return x
        return f.prefix[x.index] if x.index<p else Ref(f.consumed+x.index-p)
    depth=max(f.depth,g.depth-(p-f.consumed))
    if g.consumed<p:prefix=g.prefix+f.prefix[g.consumed:];consumed=f.consumed
    else:prefix=g.prefix;consumed=f.consumed+g.consumed-p
    emissions=f.emissions+tuple((t,subst(x)) for t,x in g.emissions)
    constraints=f.constraints+tuple((subst(x),o) for x,o in g.constraints)
    return _normal(depth,prefix,consumed,emissions,constraints)

def rename_outputs(e,namespace):
    _check(e)
    if type(namespace) is not str or not namespace:raise Invalid('namespace')
    if e.impossible:return e
    # Length prefix avoids accidental namespace/name delimiter ambiguity.
    return Effect(e.depth,e.prefix,e.consumed,tuple((f'{len(namespace)}:{namespace}{t}',x) for t,x in e.emissions),e.constraints)

def apply_effect(e,stack):
    _check(e);stack=tuple(stack)
    if e.impossible or len(stack)<e.depth or any(type(o) is not Origin for o in stack):raise Invalid('effect not applicable to input stack')
    if any(stack[x.index]!=o for x,o in e.constraints):raise Invalid('source-cut origin constraint failed')
    def value(x):return x if type(x) is Origin else stack[x.index]
    return e.prefix+stack[e.consumed:],tuple((t,value(x)) for t,x in e.emissions)

def resolve_demands(e,boundary:Mapping[int,Origin]):
    """Resolve selected dependencies after supplied boundary identity evidence.

This does not acquire absent identities, validate natural-language paths, or
establish that the supplied source-to-boundary map describes a real source.
"""
    _check(e)
    if e.impossible:raise Invalid('empty effect domain')
    def value(x):
        if type(x) is Origin:return x
        if x.index not in boundary:raise MissingBinding(f'input context I_{x.index} is not identified')
        o=boundary[x.index]
        if type(o) is not Origin:raise Invalid('boundary origin type')
        return o
    if any(value(x)!=o for x,o in e.constraints):raise Invalid('boundary constraint fails')
    return frozenset(value(x) for _,x in e.emissions)
