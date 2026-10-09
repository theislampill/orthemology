"""Finite grounded rule compiler, with separate tree and once-per-node DAG costs."""
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

@dataclass(frozen=True)
class Tree:
    rule: Rule
    children: tuple

@dataclass(frozen=True)
class Dag:
    nodes: tuple
    root: int

def _validate(judgements, rules):
    if len(set(judgements)) != len(judgements):
        raise ValueError('Judgement labels must be distinct.')
    if len({r.name for r in rules}) != len(rules):
        raise ValueError('Rule identities must be distinct.')
    known = set(judgements)
    for r in rules:
        if r.head not in known or not set(r.premises) <= known:
            raise ValueError('Every head and premise must be a declared scoped judgement.')
        if not isinstance(r.cost, (int, Fraction)) or r.cost < 0:
            raise ValueError('This implementation requires exact nonnegative integer/rational prices.')


def normalize(candidates):
    """Pareto-minimize a pair -> witness dictionary; a tie keeps one witness."""
    return {p: w for p, w in candidates.items()
            if not any(o != p and o[0] <= p[0] and o[1] <= p[1]
                       for o in candidates)}


def tree_step(judgements, rules, old):
    new = {q: dict(old[q]) for q in judgements}
    for r in rules:
        choices = [tuple(old[q].items()) for q in r.premises]
        for selected in product(*choices):
            support = r.support.union(*(p[0] for p, _ in selected))
            cost = r.cost + sum(p[1] for p, _ in selected)
            witness = Tree(r, tuple(t for _, t in selected))
            new[r.head].setdefault((support, cost), witness)
    return {q: normalize(new[q]) for q in judgements}


def compile_tree(judgements, rules):
    """Return exact tree frontiers with witnesses and all n+1 synchronous snapshots."""
    judgements, rules = tuple(judgements), tuple(rules)
    _validate(judgements, rules)
    current = {q: {} for q in judgements}
    history = [{q: frozenset(current[q]) for q in judgements}]
    for _ in judgements:
        current = tree_step(judgements, rules, current)
        history.append({q: frozenset(current[q]) for q in judgements})
    return current, history

def compile_dag(judgements, rules):
    """Enumerate one rule or absent per judgement; check only each root's graph."""
    judgements, rules = tuple(judgements), tuple(rules)
    _validate(judgements, rules)
    result = {q: {} for q in judgements}
    options = [(None,) + tuple(r for r in rules if r.head == q) for q in judgements]
    for selected in product(*options):
        chosen = dict(zip(judgements, selected))
        for root in judgements:
            nodes, built, visiting = [], {}, set()

            def build(q):
                if q in built:
                    return built[q]
                if q in visiting or chosen[q] is None:
                    raise ValueError('Missing premise or unsupported cycle.')
                visiting.add(q)
                rule = chosen[q]
                refs = tuple(build(p) for p in rule.premises)
                visiting.remove(q)
                built[q] = len(nodes)
                nodes.append((rule, refs))
                return built[q]

            try:
                root_index = build(root)
            except ValueError:
                continue
            witness = Dag(tuple(nodes), root_index)
            _, support, cost, _ = dag_value(witness)
            result[root].setdefault((support, cost), witness)
    return {q: normalize(result[q]) for q in judgements}

def tree_value(t):
    """Independently traverse/check a witness; return head, support, cost, height, size."""
    if len(t.children) != len(t.rule.premises) or t.rule.cost < 0:
        raise ValueError('Invalid tree rule application.')
    children = tuple(tree_value(c) for c in t.children)
    if tuple(c[0] for c in children) != t.rule.premises:
        raise ValueError('A premise has the wrong scoped judgement.')
    return (t.rule.head, t.rule.support.union(*(c[1] for c in children)),
            t.rule.cost + sum(c[2] for c in children),
            1 + max((c[3] for c in children), default=0),
            1 + sum(c[4] for c in children))

def dag_value(t):
    """Check a premise-first indexed DAG; charge reachable rule nodes once."""
    if not 0 <= t.root < len(t.nodes):
        raise ValueError('Missing root.')
    for i, (rule, refs) in enumerate(t.nodes):
        if (len(refs) != len(rule.premises) or rule.cost < 0
                or any(not 0 <= j < i for j in refs)):
            raise ValueError('Invalid application or non-acyclic topological indexing.')
        if tuple(t.nodes[j][0].head for j in refs) != rule.premises:
            raise ValueError('A premise has the wrong scoped judgement.')
    reached, stack = set(), [t.root]
    while stack:
        i = stack.pop()
        if i not in reached:
            reached.add(i)
            stack.extend(t.nodes[i][1])
    if reached != set(range(len(t.nodes))):
        raise ValueError('A certificate may not contain unreachable charged nodes.')
    return (t.nodes[t.root][0].head,
            frozenset().union(*(t.nodes[i][0].support for i in reached)),
            sum(t.nodes[i][0].cost for i in reached), len(reached))

def prune_tree(t):
    tree_value(t)

    def descendant_with_head(children, head):
        for child in children:
            if child.rule.head == head:
                return child
            found = descendant_with_head(child.children, head)
            if found is not None:
                return found
        return None

    def reduce(node):
        same = descendant_with_head(node.children, node.rule.head)
        if same is not None:
            return reduce(same)
        return Tree(node.rule, tuple(reduce(c) for c in node.children))

    return reduce(t)

def prune_dag(t):
    dag_value(t)
    earliest = {}
    for i, (rule, _) in enumerate(t.nodes):
        earliest.setdefault(rule.head, i)
    nodes, built = [], {}

    def build(q):
        if q in built:
            return built[q]
        rule, refs = t.nodes[earliest[q]]
        new_refs = tuple(build(t.nodes[i][0].head) for i in refs)
        built[q] = len(nodes)
        nodes.append((rule, new_refs))
        return built[q]

    root = build(t.nodes[t.root][0].head)
    reduced = Dag(tuple(nodes), root)
    dag_value(reduced)
    return reduced
