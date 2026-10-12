"""A hidden co-Buechi plant whose action-word language is Buchi (Inf a)."""
from itertools import product
import json
from restoration import Controller, verify_controller, bounded_sure
from test_restoration import blind_game


def game():
    # 0 waits to guess the last a, 1 is bad after the guess, 2 is safe dead.
    return blind_game({0: {'a': (0,), 'b': (0, 1)},
                       1: {'a': (2,), 'b': (1,)},
                       2: {'a': (2,), 'b': (2,)}}, {1}, initial=(0,))


def lasso_controller(prefix, period):
    word = prefix + period
    m = tuple(range(len(word)))
    actions = dict(enumerate(word))
    update = {(i, a, 'o'): (i+1 if i+1 < len(word) else len(prefix))
              for i in m for a in ('a', 'b')}
    return Controller(0, actions, update)


def main():
    g = game()
    checked = 0
    largest_bound = 0
    for lp in range(5):
      for lc in range(1, 7):
       for prefix in product(('a', 'b'), repeat=lp):
        for period in product(('a', 'b'), repeat=lc):
            result = verify_controller(g, lasso_controller(prefix, period))
            expected = 'a' in period
            assert result['sure'] == expected, (prefix, period, result)
            checked += 1
            if result['sure']:
                largest_bound = max(largest_bound, result['max_bad_visits'])
    # Show bad-visit counts grow with increasing b-block lengths while the a
    # separator kills every previously committed bad path permanently.
    counters = {0: 0}
    maxima = []
    for block in range(1, 31):
        for action in ('b',)*block + ('a',):
            new = {}
            for x, burden in counters.items():
                for y, obs in g.transitions[0, x, action]:
                    new[y] = max(new.get(y, -1), burden + int(y == 1))
            counters = new
        maxima.append(max(counters.values()))
    assert maxima == list(range(1, 31))
    assert bounded_sure(g, 0).winning  # a forever is an alternative winner.
    print(json.dumps({'lassos_checked': checked, 'lasso_language_mismatches': 0,
                      'largest_lasso_bad_bound': largest_bound,
                      'increasing_block_prefix_maxima': maxima,
                      'alternative_zero_bad_policy_exists': True,
                      'scope': 'Finite probes plus written proof for all infinite action words; '
                               'not a general deterministic parity implementation.'}, indent=2))


if __name__ == '__main__': main()
