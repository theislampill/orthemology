"""Independent bounded-safety model extraction and synthetic stress probes.

The reference construction tracks *sets of (actual state, exact visit count)*,
not maximum counter vectors. Temporal checking separately uses concrete cycles.
No repository or network state is modified.
"""
from collections import defaultdict, deque
from fractions import Fraction
from itertools import product, combinations
import json
import random
import time
from restoration import Game, Controller, bounded_sure, verify_controller, classify_mdp
from test_restoration import blind_game


def reference_augmented_subset(game, bound):
    initial = (game.initial_public, frozenset(
        (x, int((game.initial_public, x) not in game.target)) for x in game.initial))
    todo = [initial]
    arena = {}
    while todo:
        p = todo.pop()
        if p in arena:
            continue
        c, possibilities = p
        b = {x for x, j in possibilities}
        arena[p] = []
        if not b or any(j > bound or (c, x) not in game.safe for x, j in possibilities):
            continue
        for a in game.actions:
            if not game.allowed(c, b, a):
                continue
            if any(not game.transitions.get((c, x, a), ()) for x in b):
                arena[p].append((None,))
                continue
            observed = defaultdict(set)
            for x, j in possibilities:
                for y, o in game.transitions[c, x, a]:
                    nc = game.public_update[c, a, o]
                    observed[o].add((y, j + int((nc, y) not in game.target)))
            successors = []
            for o, outcomes in observed.items():
                nc = game.public_update[c, a, o]
                if any(j > bound or (nc, y) not in game.safe for y, j in outcomes):
                    successors.append(None)
                else:
                    successor = (nc, frozenset(outcomes))
                    successors.append(successor)
                    todo.append(successor)
            arena[p].append(tuple(successors))
    # Retrograde elimination is distinct from repeated whole-set greatest FP.
    losers = {p for p, actions in arena.items() if not actions}
    changed = True
    while changed:
        changed = False
        for p, actions in arena.items():
            if p not in losers and all(any(q is None or q in losers for q in action)
                                       for action in actions):
                losers.add(p)
                changed = True
    return initial not in losers, len(arena)


def check_case(game, bound):
    result = bounded_sure(game, bound)
    reference, size = reference_augmented_subset(game, bound)
    assert result.winning == reference, ('counter/reference mismatch', game, bound)
    if result.winning:
        direct = verify_controller(game, result.controller)
        assert direct['sure'], ('extracted controller cycle failure', game, bound, direct)
        assert direct['max_bad_visits'] <= bound, ('bound failure', game, bound, direct)
    return result.winning, result.explored, size


def exhaustive_two_state():
    tested = winning = 0
    max_primary = max_reference = 0
    # All nonempty successors for two actions and two states; all 3^2 safe,
    # target, unsafe labellings; every nonempty initial belief; blind/full obs.
    for masks in product(range(1, 4), repeat=4):
      for labels in product(range(3), repeat=2):
       for imask in range(1, 4):
        for visible in (False, True):
         initial = tuple(x for x in range(2) if imask >> x & 1)
         if visible and len(initial) > 1:
             continue  # a full initial observation reveals the actual state
         game = Game(states=(0, 1), public=(0,), actions=(0, 1),
             initial=initial, initial_public=0,
             transitions={(0, x, a): tuple((y, y if visible else 0)
                 for y in range(2) if masks[2*x+a] >> y & 1)
                 for x in range(2) for a in range(2)},
             public_update={(0, a, o): 0 for a in (0, 1) for o in (0, 1)},
             safe={(0, x) for x in range(2) if labels[x] != 0},
             target={(0, x) for x in range(2) if labels[x] == 2})
         for bound in (0, 1, 2):
            win, primary, reference = check_case(game, bound)
            winning += win
            tested += 1
            max_primary = max(max_primary, primary)
            max_reference = max(max_reference, reference)
    return {'bounded_instances': tested, 'winning_instances': winning,
            'mismatches': 0, 'largest_counter_arena': max_primary,
            'largest_exact_count_subset_arena': max_reference}


def random_public_games(count=2000, seed=9301322):
    rng = random.Random(seed)
    tested = wins = checked_controllers = 0
    max_p = max_r = 0
    for _ in range(count):
        n = rng.choice((2, 3, 4))
        cs = tuple(range(rng.choice((1, 2, 3))))
        states = tuple(range(n))
        actions = (0, 1)
        observations = (0, 1)
        transitions = {}
        for c, x, a in product(cs, states, actions):
            outcomes = list(product(states, observations))
            rng.shuffle(outcomes)
            transitions[c, x, a] = tuple(outcomes[:rng.randint(1, min(3, 2*n))])
        update = {(c, a, o): rng.choice(cs) for c, a, o in product(cs, actions, observations)}
        safe = {(c, x) for c, x in product(cs, states) if rng.randrange(9)}
        target = {p for p in safe if rng.randrange(3)}
        eligibility = {(c, x, a) for c, x, a in product(cs, states, actions) if rng.randrange(9)}
        # A concrete public warrant table, distinct from pointwise eligibility.
        table = {(c, mask, a): bool(rng.randrange(9))
                 for c in cs for mask in range(1, 1 << n) for a in actions}
        warrant = lambda c, b, a, tab=table: tab[c, sum(1 << x for x in b), a]
        initial = tuple(x for x in states if rng.randrange(2)) or (rng.choice(states),)
        game = Game(states=states, public=cs, actions=actions, initial=initial,
                    initial_public=rng.choice(cs), transitions=transitions,
                    public_update=update, safe=safe, target=target,
                    eligibility=eligibility, warrant=warrant)
        bound = rng.randrange(4)
        win, np, nr = check_case(game, bound)
        wins += win; tested += 1
        max_p = max(max_p, np); max_r = max(max_r, nr)
        # Independently generate finite controllers. A sure finite winner must
        # be accepted by bounded synthesis at its directly computed bad bound.
        memory = tuple(range(rng.choice((1, 2, 3))))
        controller = Controller(initial=0,
            action={m: rng.choice(actions) for m in memory},
            update={(m, a, o): rng.choice(memory)
                    for m, a, o in product(memory, actions, observations)})
        direct = verify_controller(game, controller)
        if direct['sure']:
            checked_controllers += 1
            assert bounded_sure(game, direct['max_bad_visits']).winning
    return {'seed': seed, 'bounded_instances': tested, 'winning_instances': wins,
            'mismatches': 0, 'independent_random_sure_controllers': checked_controllers,
            'largest_counter_arena': max_p, 'largest_exact_count_subset_arena': max_r}


def brute_end_components(supports):
    states = tuple(supports)
    end_components = []
    for mask in range(1, 1 << len(states)):
        s = frozenset(v for i, v in enumerate(states) if mask >> i & 1)
        closed = {v: [t for t in supports[v] if t <= s] for v in s}
        if any(not actions for actions in closed.values()):
            continue
        graph = {v: set().union(*actions) for v, actions in closed.items()}
        connected = True
        for v in s:
            reached = {v}
            todo = [v]
            while todo:
                q = todo.pop()
                for y in graph[q] - reached:
                    reached.add(y); todo.append(y)
            if reached != s:
                connected = False; break
        if connected:
            end_components.append(s)
    return {s for s in end_components if not any(s < t for t in end_components)}


def random_mdp_checks(count=3000, seed=9301323):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(1, 6)
        supports = {}
        kernels = {}
        for x in range(n):
            actions = []
            for _ in range(rng.randint(1, 3)):
                subset = frozenset(y for y in range(n) if rng.randrange(2)) or frozenset({rng.randrange(n)})
                actions.append(subset)
            supports[x] = tuple(actions)
            kernels[x] = tuple({y: Fraction(1, len(s)) for y in s} for s in actions)
        bad = {x for x in range(n) if rng.randrange(2)}
        # Start all states so the independent brute test need not filter reachability.
        actual = classify_mdp(kernels, set(range(n)), bad)
        expected = brute_end_components(supports)
        assert set(actual['maximal_end_components']) == expected
        assert actual['almost_sure_all_adversaries'] == (not any(s & bad for s in expected))
    return {'seed': seed, 'finite_mdps': count, 'mec_mismatches': 0}


def main():
    started = time.monotonic()
    output = {'exhaustive_two_state': exhaustive_two_state(),
              'random_public_custody': random_public_games(),
              'stochastic_end_components': random_mdp_checks()}
    output['elapsed_seconds'] = round(time.monotonic() - started, 3)
    output['scope'] = ('D1 bounded synthesis versus independently extracted exact-count subsets; '
                       'positive policies also checked on concrete cycles. No full parity '
                       'determinization or arbitrary-model adequacy is claimed.')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
