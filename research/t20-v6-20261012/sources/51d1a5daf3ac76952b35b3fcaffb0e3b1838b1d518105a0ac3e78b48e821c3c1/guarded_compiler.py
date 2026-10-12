"""Finite exact-support tree compiler. No DAG sharing or source-soundness claim.

A fixed guard is represented extensionally by its permitted ordered tuples of
premise supports. None means every tuple is permitted. Thus no guard can inspect
proof shape, current inventory, runtime history, or a changing external service.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

@dataclass(frozen=True)
class Rule:
    name: str
    head: str
    premises: tuple
    support: frozenset
    cost: Fraction
    allowed: object = None

@dataclass(frozen=True)
class Tree:
    rule: Rule
    children: tuple


def _validate(judgements, evidence, rules):
    if len(set(judgements)) != len(judgements) or len(set(evidence)) != len(evidence):
        raise ValueError('Judgement and evidence identities must be distinct.')
    if len({r.name for r in rules}) != len(rules):
        raise ValueError('Rule identities must be distinct.')
    J,E=set(judgements),frozenset(evidence)
    for r in rules:
        if not isinstance(r.premises,tuple) or not isinstance(r.support,frozenset):
            raise ValueError('Premises and local supports must have immutable tuple/set types.')
        if r.head not in J or not set(r.premises)<=J or not r.support<=E:
            raise ValueError('A rule refers to an undeclared judgement or token.')
        if not isinstance(r.cost,(int,Fraction)) or r.cost<0:
            raise ValueError('Exact nonnegative integer/rational costs required.')
        if r.allowed is not None:
            if not isinstance(r.allowed,frozenset):
                raise ValueError('Guards must be immutable support-tuple tables.')
            if any(not isinstance(ss,tuple) or len(ss)!=len(r.premises)
                   or any(not isinstance(s,frozenset) or not s<=E for s in ss)
                   for ss in r.allowed):
                raise ValueError('Guard tuples must use declared premise supports.')


def exact_step(judgements, rules, old):
    """One synchronous round: discard only dearer proofs of the SAME exact support."""
    new={q:dict(old[q]) for q in judgements}
    for r in rules:
        choices=[tuple(old[q].items()) for q in r.premises]
        for selected in product(*choices):
            ss=tuple(s for s,_ in selected)
            if r.allowed is not None and ss not in r.allowed:
                continue
            support=r.support.union(*ss)
            cost=r.cost+sum(row[0] for _,row in selected)
            if support not in new[r.head] or cost<new[r.head][support][0]:
                new[r.head][support]=(cost,Tree(r,tuple(row[1] for _,row in selected)))
    return new


def compile_exact(judgements, evidence, rules):
    """Return global exact-support minima/witnesses and H+1 cost snapshots.

    H = |J|(|E|+1), height counts rule nodes. All H rounds are intentionally
    executed; fixed-point equality concerns complete support/price tables.
    """
    judgements,evidence,rules=tuple(judgements),tuple(evidence),tuple(rules)
    _validate(judgements,evidence,rules)
    current={q:{} for q in judgements}
    history=[{q:{} for q in judgements}]
    for _ in range(len(judgements)*(len(evidence)+1)):
        current=exact_step(judgements,rules,current)
        history.append({q:{s:row[0] for s,row in current[q].items()} for q in judgements})
    return current,history


def tree_value(tree, rules):
    """Traverse a concrete witness and recheck each admitted rule and guard.

    Returns judgement, exact support, tree price, node height, node count.
    This does not authenticate evidence or justify the admitted rule licences.
    """
    r=tree.rule
    if r not in rules or len(tree.children)!=len(r.premises) or r.cost<0:
        raise ValueError('Missing rule admission or malformed application.')
    children=tuple(tree_value(c,rules) for c in tree.children)
    if tuple(c[0] for c in children)!=r.premises:
        raise ValueError('Wrong scoped premise judgement.')
    ss=tuple(c[1] for c in children)
    if r.allowed is not None and ss not in r.allowed:
        raise ValueError('Proof support tuple fails its rule guard.')
    return (r.head,r.support.union(*ss),r.cost+sum(c[2] for c in children),
            1+max((c[3] for c in children),default=0),1+sum(c[4] for c in children))


def prune_exact(tree, rules):
    """Delete only ancestor/descendant repetitions of the same (head, support)."""
    tree_value(tree,rules)

    def matching_descendant(children,key):
        for child in children:
            if tree_value(child,rules)[:2]==key:
                return child
            found=matching_descendant(child.children,key)
            if found is not None:
                return found
        return None

    def reduce(t):
        found=matching_descendant(t.children,tree_value(t,rules)[:2])
        if found is not None:
            return reduce(found)
        return Tree(t.rule,tuple(reduce(c) for c in t.children))

    return reduce(tree)
