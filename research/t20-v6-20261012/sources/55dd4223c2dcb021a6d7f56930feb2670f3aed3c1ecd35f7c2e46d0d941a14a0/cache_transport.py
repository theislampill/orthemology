"""Cache-cut adapter for the inherited exact-support whole-DAG compiler.

Research reference only. Node identity is the complete immutable rule record
plus ordered child identities. Cached dependencies must be downward closed.
No source authentication, scheduling, physical cost or general host theorem.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode=True
WORK=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent/'inherited'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
g=load('proof_inquiry_inherited',BASE/'guarded-shared-dag-attainment-20261009/guarded_dag.py')
@dataclass(frozen=True)
class Node:
    rule: object
    children: tuple

from itertools import product

def footprint(node):
    result={node}
    for child in node.children: result.update(footprint(child))
    return frozenset(result)

def support(node):
    return node.rule.support.union(*(support(child) for child in node.children))

def incremental_cost(node,cache):
    return sum((n.rule.cost for n in footprint(node)-cache),F())

def valid_node(node,rules,inventory):
    r=node.rule
    if r not in rules or r.support-inventory: return False
    if len(node.children)!=len(r.premises): return False
    if tuple(n.rule.head for n in node.children)!=r.premises: return False
    if not all(valid_node(n,rules,inventory) for n in node.children): return False
    ss=tuple(support(n) for n in node.children)
    return r.allowed is None or ss in r.allowed

def active_cache(cache,rules,inventory):
    return frozenset(n for n in cache if valid_node(n,rules,inventory))

def require_cache(cache,rules,inventory):
    if not isinstance(cache,frozenset): raise ValueError('Cache must be frozen.')
    for n in cache:
        if not footprint(n)<=cache: raise ValueError('Cache must include dependencies.')
        if not valid_node(n,rules,inventory): raise ValueError('Cache is stale or invalid.')

def to_dag(node):
    nodes=[]; indices={}
    def visit(n):
        if n in indices: return indices[n]
        refs=tuple(visit(c) for c in n.children)
        indices[n]=len(nodes); nodes.append((n.rule,refs)); return indices[n]
    root=visit(node)
    return g.Dag(tuple(nodes),root)

def from_dag(dag):
    nodes=[]
    for r,refs in dag.nodes: nodes.append(Node(r,tuple(nodes[i] for i in refs)))
    return nodes[dag.root]

def refine(J,E,rules):
    """Reachable exact states and admitted refined rules, including cycles.

    This is Boolean reachability saturation, not cheapest-child optimization.
    """
    reached={q:set() for q in J}; refined={}; decoding={}
    while True:
        changed=False
        for r in rules:
            for ss in product(*(tuple(reached[q]) for q in r.premises)):
                if r.allowed is not None and ss not in r.allowed: continue
                S=r.support.union(*ss); key=(r.name,ss)
                if S not in reached[r.head]: reached[r.head].add(S); changed=True
                if key not in refined:
                    rr=g.unguarded.Rule(key,(r.head,S),tuple(zip(r.premises,ss)),r.support,r.cost)
                    refined[key]=rr;decoding[key]=r
        if not changed: break
    states=tuple((q,S) for q in J for S in sorted(reached[q],key=lambda z:tuple(sorted(z))))
    return states,tuple(refined.values()),decoding

def cached_optimum(J,E,rules,target,inventory,cache,exact_support=None):
    """Return exact marginal optimum and expanded actual proof, or (None,None).

    Whole-graph enumeration is inherited, exponentially large and deliberate.
    """
    J,E,rules=tuple(J),tuple(E),tuple(rules)
    g.guarded._validate(J,E,rules)
    if not inventory<=frozenset(E): raise ValueError('Inventory outside evidence universe.')
    require_cache(cache,rules,inventory)
    admissible=tuple(r for r in rules if r.support<=inventory)
    macros={}; names={r.name for r in rules}
    for i,n in enumerate(sorted(cache,key=repr)):
        name=('cache-macro',i)
        if name in names: raise ValueError('Reserved macro name collision.')
        macros[name]=n
    macro_rules=tuple(g.Rule(name,n.rule.head,(),support(n),F()) for name,n in macros.items())
    states,rr,decode=refine(J,E,admissible+macro_rules)
    if not states: return None,None
    compiled=g.unguarded.compile_dag(states,rr)
    choices=[]
    for state,frontier in compiled.items():
        q,S=state
        if q!=target or (exact_support is not None and S!=exact_support): continue
        for (_,price),dag in frontier.items():
            nodes=[]
            for refined,refs in dag.nodes:
                r=decode[refined.name]
                nodes.append(macros[r.name] if r.name in macros else Node(r,tuple(nodes[i] for i in refs)))
            node=nodes[dag.root]
            if not valid_node(node,rules,inventory): raise RuntimeError('Bad macro expansion.')
            actual=incremental_cost(node,cache)
            if actual>price: raise RuntimeError('Expansion increased marginal price.')
            choices.append((actual,node))
    if not choices: return None,None
    price,node=min(choices,key=lambda z:z[0])
    g.dag_value(to_dag(node),J,E,rules)
    return price,node

def dependency_frontier(cache,local_dependencies):
    """Minimum dependency antichains per exact state, for stipulated conjunction validity.

    local_dependencies must contain every material external dependency of each
    rule application. This function cannot discover undeclared dependencies.
    """
    memo={}
    def deps(n):
        if n not in memo:
            memo[n]=local_dependencies[n.rule.name].union(*(deps(ch) for ch in n.children))
        return memo[n]
    table={}
    for n in cache: table.setdefault((n.rule.head,support(n)),set()).add(deps(n))
    return {x:frozenset(D for D in ds if not any(E<D for E in ds)) for x,ds in table.items()}
