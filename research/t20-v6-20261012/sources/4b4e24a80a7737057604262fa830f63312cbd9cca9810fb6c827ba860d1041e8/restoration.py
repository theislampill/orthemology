"""Bounded-visit synthesis and independent finite-controller checks.

This module operates on declared finite synthetic models. It does not authenticate
observations, create authority, or establish that a model fits an actual system.
"""
from dataclasses import dataclass, field
from collections import deque, defaultdict
from typing import Callable, Hashable


@dataclass
class Game:
    states: tuple
    public: tuple
    actions: tuple
    initial: tuple
    initial_public: Hashable
    transitions: dict
    public_update: dict
    safe: set
    target: set
    eligibility: set | None = None
    warrant: Callable | None = None

    def allowed(self, c, belief, a):
        return ((self.eligibility is None or
                 all((c, x, a) in self.eligibility for x in belief))
                and (self.warrant is None or self.warrant(c, frozenset(belief), a)))


@dataclass
class Controller:
    initial: Hashable
    action: dict
    update: dict


@dataclass
class Result:
    winning: bool = False
    controller: Controller | None = None
    explored: int = 0
    winning_states: int = 0


def bounded_sure(game, bound):
    """Exactly synthesize a controller permitting <= bound concrete bad visits.

    Current-state visits, including the initial state, count. Counter value -1
    denotes unreachable. Losing successor branches are retained as explicit None.
    """
    if bound < 0:
        raise ValueError('bound must be nonnegative')
    index = {x: i for i, x in enumerate(game.states)}
    c0 = game.initial_public
    f0 = tuple(int((c0, x) not in game.target) if x in game.initial else -1
               for x in game.states)
    initial = (c0, f0)
    queue = deque([initial])
    edges = {}
    while queue:
        state = queue.popleft()
        if state in edges:
            continue
        c, f = state
        belief = tuple(x for x, v in zip(game.states, f) if v >= 0)
        menu = {}
        edges[state] = menu
        if (not belief or max(f) > bound or
                any((c, x) not in game.safe for x in belief)):
            continue
        for a in game.actions:
            if not game.allowed(c, belief, a):
                continue
            # Missing transitions are a loss, never a vacuous successful action.
            if any(not game.transitions.get((c, x, a), ()) for x in belief):
                menu[a] = {None: None}
                continue
            by_observation = defaultdict(list)
            for x in belief:
                for y, o in game.transitions[c, x, a]:
                    by_observation[o].append((x, y))
            successors = {}
            for o, pairs in by_observation.items():
                nc = game.public_update[c, a, o]
                nf = [-1] * len(game.states)
                for x, y in pairs:
                    j = index[y]
                    count = f[index[x]] + int((nc, y) not in game.target)
                    nf[j] = max(nf[j], count)
                ns = (nc, tuple(nf))
                if max(nf) > bound or any((nc, y) not in game.safe for _, y in pairs):
                    successors[o] = None
                else:
                    successors[o] = ns
                    if ns not in edges:
                        queue.append(ns)
            menu[a] = successors
    winning = set(edges)
    while True:
        nxt = {s for s in winning if any(
            succ and all(t in winning for t in succ.values())
            for succ in edges[s].values())}
        if nxt == winning:
            break
        winning = nxt
    if initial not in winning:
        return Result(False, None, len(edges), len(winning))
    actions = {}
    updates = {}
    for s in winning:
        a = next(a for a, succ in edges[s].items()
                 if succ and all(t in winning for t in succ.values()))
        actions[s] = a
        updates.update({(s, a, o): t for o, t in edges[s][a].items()})
    return Result(True, Controller(initial, actions, updates), len(edges), len(winning))


def strongly_connected(graph):
    """Iterative Kosaraju; independent of the safety fixed point."""
    seen = set()
    order = []
    for start in graph:
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, iter(graph[start]))]
        while stack:
            v, children = stack[-1]
            try:
                w = next(children)
                if w not in seen:
                    seen.add(w)
                    stack.append((w, iter(graph[w])))
            except StopIteration:
                order.append(v)
                stack.pop()
    rev = {v: set() for v in graph}
    for v, children in graph.items():
        for w in children:
            rev[w].add(v)
    seen.clear()
    components = []
    for start in reversed(order):
        if start in seen:
            continue
        component = set()
        stack = [start]
        seen.add(start)
        while stack:
            v = stack.pop()
            component.add(v)
            for w in rev[v] - seen:
                seen.add(w)
                stack.append(w)
        components.append(component)
    return components


def controller_product(game, controller):
    """Build concrete product directly, never using synthesis counters.

    Belief is recalculated solely to evaluate the public license contract; it is
    not used to decide the temporal acceptance condition.
    """
    b0 = frozenset(game.initial)
    starts = {(game.initial_public, x, b0, controller.initial) for x in b0}
    queue = deque(starts)
    graph = {}
    invalid = []
    while queue:
        v = queue.popleft()
        if v in graph:
            continue
        c, x, belief, m = v
        graph[v] = set()
        if (c, x) not in game.safe:
            invalid.append(('unsafe', v))
        if m not in controller.action:
            invalid.append(('missing_action', v))
            continue
        a = controller.action[m]
        if a not in game.actions or not game.allowed(c, belief, a):
            invalid.append(('unlicensed', v))
            continue
        outputs = defaultdict(set)
        for bx in belief:
            outcomes = game.transitions.get((c, bx, a), ())
            if not outcomes:
                invalid.append(('dead_end', v, bx))
            for by, o in outcomes:
                outputs[o].add(by)
        for y, o in game.transitions.get((c, x, a), ()):
            if (m, a, o) not in controller.update:
                invalid.append(('missing_update', v, o))
                continue
            nc = game.public_update[c, a, o]
            nm = controller.update[m, a, o]
            w = (nc, y, frozenset(outputs[o]), nm)
            graph[v].add(w)
            if w not in graph:
                queue.append(w)
    return starts, graph, invalid


def verify_controller(game, controller):
    starts, graph, invalid = controller_product(game, controller)
    components = strongly_connected(graph)
    bad_cycles = [scc for scc in components
                  if (len(scc) > 1 or any(v in graph[v] for v in scc))
                  and any((v[0], v[1]) not in game.target for v in scc)]
    sure = not invalid and not bad_cycles
    max_bad = None
    rank = {}
    if sure:
        # Max-plus relaxation yields exact maximal future bad visits; no bad
        # cycle means convergence, although target cycles need not be left.
        rank = {v: int((v[0], v[1]) not in game.target) for v in graph}
        while True:
            nr = {v: int((v[0], v[1]) not in game.target)
                     + max((rank[w] for w in children), default=0)
                  for v, children in graph.items()}
            if nr == rank:
                break
            rank = nr
        max_bad = max((rank[v] for v in starts), default=0)
    return {'sure': sure, 'invalid': invalid, 'product_states': len(graph),
            'bad_cycle_components': len(bad_cycles), 'max_bad_visits': max_bad,
            'rank': rank}


def _validated_support(kernel, states):
    if not kernel or any(p <= 0 for p in kernel.values()) or sum(kernel.values()) != 1:
        raise ValueError('Each fixed kernel must be nonempty, positive, and sum exactly to one')
    if not set(kernel) <= states:
        raise ValueError('Kernel successor outside declared states')
    return frozenset(kernel)


def _reachable(graph, initial):
    reached = set(initial)
    if not reached <= set(graph):
        raise ValueError('Initial state outside declared graph')
    todo = list(reached)
    while todo:
        v = todo.pop()
        for w in graph[v] - reached:
            reached.add(w)
            todo.append(w)
    return reached


def classify_chain(kernel, initial, bad, unsafe=frozenset()):
    """Exact qualitative finite, fixed, time-homogeneous Markov-chain test."""
    states = set(kernel)
    graph = {v: _validated_support(k, states) for v, k in kernel.items()}
    reachable = _reachable(graph, initial)
    graph = {v: graph[v] for v in reachable}
    sccs = strongly_connected(graph)
    bottoms = [frozenset(s) for s in sccs if all(graph[v] <= s for v in s)]
    bad_bottoms = [s for s in bottoms if s & set(bad)]
    bad_cycles = [frozenset(s) for s in sccs if set(bad) & s and
                  (len(s) > 1 or any(v in graph[v] for v in s))]
    safe = not reachable & set(unsafe)
    return {'sure': safe and not bad_cycles,
            'almost_sure': safe and not bad_bottoms,
            'bottom_components': bottoms,
            'bad_bottom_components': bad_bottoms,
            'bad_cycle_components': bad_cycles,
            'reachable': reachable}


def classify_mdp(kernels, initial, bad, unsafe=frozenset()):
    """Exact adversarial AS co-Buechi test for finitely many fixed kernels.

    The controller has already been fixed; each residual action is an
    adversary's kernel choice. No vanishing-probability kernel family is inferred.
    """
    states = set(kernels)
    if any(not ks for ks in kernels.values()):
        raise ValueError('Every MDP state must have a nonempty finite kernel menu')
    supports = {v: tuple(_validated_support(k, states) for k in ks)
                for v, ks in kernels.items()}
    graph = {v: frozenset().union(*ks) for v, ks in supports.items()}
    reachable = _reachable(graph, initial)
    candidates = [set(s) for s in strongly_connected(
        {v: graph[v] for v in reachable})]
    mecs = []
    while candidates:
        candidate = candidates.pop()
        # Remove vertices with no action that can keep all mass in candidate.
        while True:
            trimmed = {v for v in candidate if any(k <= candidate for k in supports[v])}
            if trimmed == candidate:
                break
            candidate = trimmed
        if not candidate:
            continue
        closed_graph = {v: frozenset().union(*(k for k in supports[v] if k <= candidate))
                        for v in candidate}
        pieces = strongly_connected(closed_graph)
        if len(pieces) == 1:
            mecs.append(frozenset(candidate))
        else:
            candidates.extend(pieces)
    bad_mecs = [s for s in mecs if s & set(bad)]
    return {'almost_sure_all_adversaries': not (reachable & set(unsafe)) and not bad_mecs,
            'maximal_end_components': mecs, 'bad_maximal_end_components': bad_mecs,
            'reachable': reachable}
