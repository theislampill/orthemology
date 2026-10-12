"""Diagnostic timing/provenance fixtures, explicitly synthetic.

Static root symbols are joint latent objects. Aliases query the same symbol;
mobile corruption is a different observation relation, not another root count.
"""
from itertools import product
import json
from restoration import Game, bounded_sure, verify_controller


def root_game(kind):
    if kind not in ('independent_static', 'aliased_static', 'mobile_sequential', 'mobile_simultaneous'):
        raise ValueError(kind)
    simultaneous = kind == 'mobile_simultaneous'
    queries = ('all',) if simultaneous else ('q0', 'q1', 'q2')
    actions = queries + ('repair0', 'repair1', 'hold')
    if kind == 'independent_static':
        latent = [(h, z) for h in (0, 1) for z in product((0, 1), repeat=3)
                  if sum(v != h for v in z) <= 1]
    elif kind == 'aliased_static':
        latent = [(h, (v,)) for h, v in product((0, 1), repeat=2)]
    else:
        latent = [(h, ()) for h in (0, 1)]
    states = tuple((h, z, s) for h, z in latent for s in ('start', 'goal', 'failure'))
    if simultaneous:
        public = ((),) + tuple((z,) for z in product((0, 1), repeat=3)) + ('done',)
    else:
        public = tuple(history for n in range(4) for history in product((0, 1), repeat=n)) + ('done',)
    initial = tuple((h, z, 'start') for h, z in latent)
    transitions = {}
    update = {}
    def observations(h, z, a):
        if a == 'all':
            return tuple(v for v in product((0, 1), repeat=3)
                         if sum(bit != h for bit in v) <= 1)
        if a.startswith('q'):
            if kind == 'mobile_sequential': return (0, 1)
            index = int(a[1]) if kind == 'independent_static' else 0
            return (z[index],)
        return ('ack',)
    for c, x, a in product(public, states, actions):
        h, z, s = x
        if a.startswith('repair'):
            ns = 'goal' if int(a[-1]) == h else 'failure'
        else:
            ns = s
        transitions[c, x, a] = tuple(((h, z, ns), o) for o in observations(h, z, a))
        for _, o in transitions[c, x, a]:
            if c == 'done' or a.startswith('repair') or a == 'hold': nc = 'done'
            elif a in queries and ((simultaneous and len(c) == 0) or (not simultaneous and len(c) < 3)):
                nc = c + (o,)
            else:
                nc = c
            update[c, a, o] = nc
    def warrant(c, b, a):
        if c == 'done': return a == 'hold'
        if simultaneous:
            return a == 'all' if len(c) == 0 else a.startswith('repair')
        return a == 'q' + str(len(c)) if len(c) < 3 else a.startswith('repair')
    return Game(states=states, public=public, actions=actions, initial=initial,
                initial_public=(), transitions=transitions, public_update=update,
                safe={(c, x) for c in public for x in states if x[2] != 'failure'},
                target={(c, x) for c in public for x in states if x[2] == 'goal'},
                warrant=warrant)


def main():
    results = {}
    for kind in ('independent_static', 'aliased_static', 'mobile_sequential', 'mobile_simultaneous'):
        game = root_game(kind)
        bound = 2 if kind == 'mobile_simultaneous' else 4
        actual = bounded_sure(game, bound)
        expected = kind in ('independent_static', 'mobile_simultaneous')
        assert actual.winning == expected, (kind, actual)
        results[kind] = {'winning': actual.winning, 'bad_visit_bound': bound,
                         'counter_states': actual.explored, 'hidden_states': len(game.states)}
        if actual.winning:
            check = verify_controller(game, actual.controller)
            assert check['sure'] and check['max_bad_visits'] <= bound
            results[kind]['direct_max_bad_visits'] = check['max_bad_visits']
    # The losing examples are genuine impossibility by two indistinguishable
    # hidden hypotheses after every possible diagnostic transcript, not solely
    # by failure at one bounded-synthesis parameter.
    results['scope'] = ('Three queried reports: one static independent root substitution is correctable; '
                        'three aliases of one corrupt root are not; mobile one-root-per-query corruption '
                        'is not; one simultaneous three-root vector with one substitution is correctable. '
                        'Root identity, feasible timing and authority are stipulated, not authenticated.')
    print(json.dumps(results, indent=2))


if __name__ == '__main__': main()
