"""Exact interfaces for reactive coalescence and provenance-aware composition.
All source labels are settings/target codes, not quantities of created matter.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import sys
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'sovereignty-choice-semantics/reactive-context-extension/src'))
from reactive_context import Catalogue, Original, own_policy, execute
C=Catalogue(('e0','e1'))

@dataclass(frozen=True)
class Leaf:
    token: str
    bearer: str
    setting: int

@dataclass(frozen=True)
class Branch:
    left: object
    right: object

def evaluate(tree):
    """Computational code re-encoding for a proposed aggregate summary.
    A branch is not an original agent or an executed created intermediate.
    Feeding its output CODE back to combine explicitly tests an additional
    closure assumption; it is not the untyped physical creation law.
    """
    return tree.setting if isinstance(tree,Leaf) else C.combine(evaluate(tree.left),evaluate(tree.right))

def flatten(tree):
    return Counter([tree]) if isinstance(tree,Leaf) else flatten(tree.left)+flatten(tree.right)

@dataclass(frozen=True)
class Act:
    bearer: str
    setting: Q
    goal: Q
    def __post_init__(self):
        if self.bearer not in ('A','B'):raise ValueError('Only the same two bearers are used.')
        object.__setattr__(self,'setting',Q(self.setting))
        object.__setattr__(self,'goal',Q(self.goal))

def merge(a,b):
    """Compatible map union: repeated records do not create repeated acts."""
    if any(a[k]!=b[k] for k in a.keys()&b.keys()):
        raise ValueError('Conflicting descriptions of the same act identifier.')
    return a|b

def summary(state):
    return sum((a.setting for a in state.values()),Q(0)),len(state)

def merge_disjoint_summaries(a,b):
    """Valid for disjoint actual-act sets only, not arbitrary aliased record merge."""
    return a[0]+b[0],a[1]+b[1]

def visible(state):
    """Source-neutral summary/target code, not an intrinsic act or created object."""
    s,n=summary(state)
    return None if n==0 else s/n

def support(state):return frozenset(a.bearer for a in state.values())

def created_output(state):
    value=visible(state)
    # Every rational is a positive target label, including 0. None alone is idle.
    return frozenset() if value is None else frozenset({('created-profile',value)})

def issue_response(state,bearer,token,target):
    if token in state:raise ValueError('A reactive fresh act must have a fresh identifier.')
    s,n=summary(state);target=Q(target)
    return {token:Act(bearer,(n+1)*target-s,target)}

def own_end(state,bearer,target):
    owned=[a for a in state.values() if a.bearer==bearer]
    return bool(owned) and all(a.goal==Q(target) for a in owned) and visible(state)==Q(target) and bool(created_output(state))

def suppress(state,token):return {k:v for k,v in state.items() if k!=token}

def mod3_bag_mean(values):
    """Faithful singleton/binary original law; partial when count is 0 mod 3."""
    n=len(values)
    if not n:return None
    if n%3==0:raise ValueError('Count has no inverse in Z3.')
    return (sum(values)*pow(n,-1,3))%3

def equal_count_weighted_mean(a,b):
    return (a+b)/2

def semantic_Z3_extension(values):
    """A disclosed changed n>=3 rule using the actual target-set semantics.
    Preserves the exact binary table, but not full higher-arity reactivity.
    """
    values=tuple(values)
    if not values:return None
    if len(values)==1:return values[0]
    if len(values)==2:return C.combine(*values)
    union=frozenset().union(*(C.targets[q] for q in values))
    return C.targets.index(union)

def ternary_symmetric_reactive_census():
    """All symmetric ternary 3-label tables with fixed unanimous diagonal.
    Exact narrow finite class; no metaphysical or all-bearer power inference.
    """
    from itertools import combinations_with_replacement,product
    keys=tuple(combinations_with_replacement(range(3),3))
    fixed={(q,q,q):q for q in range(3)}
    free=tuple(k for k in keys if k not in fixed)
    survivors=[];tested=0
    for values in product(range(3),repeat=len(free)):
        table=fixed|dict(zip(free,values));tested+=1
        if all({table[tuple(sorted((a,b,c)))] for c in range(3)}==set(range(3))
               for a,b in product(range(3),repeat=2)):
            survivors.append(table)
    return {'unordered_keys':len(keys),'fixed_unanimity_keys':len(fixed),'free_keys':len(free),
            'tested':tested,'survivors':len(survivors)}

def owner_group_Z3_mean(state):
    """Partial, provenance-sensitive exact extension of inherited two-act law.
    Average within each bearer, then equally across active bearers.
    Owner counts divisible by 3 are deliberately unsupported.
    """
    groups={g:[] for g in ('A','B')}
    for act in state.values():
        if act.setting.denominator!=1 or int(act.setting) not in range(3):
            raise ValueError('This decoder retains the original three-setting catalogue.')
        groups[act.bearer].append(int(act.setting))
    means=[mod3_bag_mean(values) for values in groups.values() if values]
    return mod3_bag_mean(means)
