"""A common bad-visit rank prevents progress resets across controller changes."""
from fractions import Fraction as F
import json
from restoration import classify_chain


def main():
    dynamics = {'A': {'b0': 'b1', 'b1': 'g', 'g': 'g'},
                'B': {'b0': 'g', 'b1': 'b0', 'g': 'g'}}
    rank = {'A': {'b0': 2, 'b1': 1, 'g': 0},
            'B': {'b0': 1, 'b1': 2, 'g': 0}}
    standalone = {}
    for mode, dyn in dynamics.items():
        chain = {s: {ns: F(1)} for s, ns in dyn.items()}
        standalone[mode] = classify_chain(chain, set(dyn), {'b0', 'b1'})['sure']
        assert standalone[mode]
    union = {s: {ns: F(1, len(set(dyn[s] for dyn in dynamics.values())))
                  for ns in set(dyn[s] for dyn in dynamics.values())}
             for s in ('b0', 'b1', 'g')}
    # Probabilities only let classify_chain inspect all support cycles; the
    # semantic claim here is sure winning under adversarial mode switching.
    unrestricted = classify_chain(union, {'b0'}, {'b0', 'b1'})['sure']
    assert not unrestricted
    combined = {}
    for mode, ranks in rank.items():
        for s in ranks:
            outcomes = {(chosen, dynamics[chosen][s]) for chosen in dynamics
                        if rank[chosen][s] <= ranks[s]}
            assert outcomes
            combined[mode, s] = {v: F(1, len(outcomes)) for v in outcomes}
            for next_mode, ns in outcomes:
                assert ranks[s] >= int(s != 'g') + rank[next_mode][ns]
    certified = classify_chain(combined, set(combined),
                                {v for v in combined if v[1] != 'g'})['sure']
    assert certified
    print(json.dumps({'standalone_sure': standalone,
                      'unrestricted_switching_sure': unrestricted,
                      'rank_nonincreasing_switching_sure': certified,
                      'blocked_progress_resets': [['A', 'b1', 'B', 1, 2],
                                                  ['B', 'b0', 'A', 1, 2]],
                      'scope': 'One mode selection per plant step; no silent fairness or Zeno assumption.'},
                     indent=2))


if __name__ == '__main__': main()
