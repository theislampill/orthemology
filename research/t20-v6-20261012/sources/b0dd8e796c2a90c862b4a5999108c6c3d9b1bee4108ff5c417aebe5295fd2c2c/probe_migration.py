"""Independent finite checks for synchronous and probabilistic certificates."""
from itertools import product
from fractions import Fraction as F
import json, random, time
from migration import coupling, verify_probabilistic_migration, verify_rank_migration
from restoration import classify_chain


def hall_test(mu, nu, relation):
    states = tuple(mu)
    for mask in range(1 << len(states)):
        subset = {x for i, x in enumerate(states) if mask >> i & 1}
        neighbors = {y for x, y in relation if x in subset and y in nu}
        if sum(mu[x] for x in subset) > sum(nu[y] for y in neighbors):
            return False
    return True


def coupling_checks():
    exact = sampled = 0
    for i, j, mask in product(range(1, 5), range(1, 5), range(16)):
        mu = {0: F(i, 5), 1: F(5-i, 5)}
        nu = {0: F(j, 5), 1: F(5-j, 5)}
        relation = {(x, y) for x, y in product(range(2), repeat=2) if mask >> (2*x+y) & 1}
        assert (coupling(mu, nu, relation) is not None) == hall_test(mu, nu, relation)
        exact += 1
    rng = random.Random(9301328)
    for _ in range(4000):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        left = [rng.randint(1, 9) for _ in range(n)]
        right = [rng.randint(1, 9) for _ in range(m)]
        mu = {x: F(w, sum(left)) for x, w in enumerate(left)}
        nu = {y: F(w, sum(right)) for y, w in enumerate(right)}
        relation = {(x, y) for x, y in product(range(n), range(m)) if rng.randrange(2)}
        assert (coupling(mu, nu, relation) is not None) == hall_test(mu, nu, relation)
        sampled += 1
    return {'exhaustive_two_by_two': exact, 'seeded_transport_problems': sampled,
            'seed': 9301328, 'max_flow_weighted_Hall_mismatches': 0}


def rank_checks():
    count = valid = 0
    choices = tuple(frozenset(x for x in range(2) if mask >> x & 1) for mask in range(1, 4))
    for source_edges in product(choices, repeat=2):
      source = dict(enumerate(source_edges))
      for bad_mask in range(4):
       bad_src = {x for x in range(2) if bad_mask >> x & 1}
       for values in product(range(3), repeat=2):
        ranks = dict(enumerate(values))
        if any(ranks[p] < int(p in bad_src) + ranks[np]
               for p in source for np in source[p]):
            continue
        for destination_edges in product(choices, repeat=2):
         destination = dict(enumerate(destination_edges))
         for bad_dst_mask in range(4):
          bad_dst = {x for x in range(2) if bad_dst_mask >> x & 1}
          for relation_mask in range(1, 16):
            relation = {(x, y) for x, y in product(range(2), repeat=2)
                        if relation_mask >> (2*x+y) & 1}
            result = verify_rank_migration(source, destination, bad_src, bad_dst,
                                          ranks, relation, relation, {0, 1})
            count += 1
            if result['valid']:
                valid += 1
                kernel = {q: {nq: F(1, len(nqs)) for nq in nqs}
                          for q, nqs in destination.items()}
                actual = classify_chain(kernel, {q for p, q in relation}, bad_dst)
                assert actual['sure'], ('unsound migration', source, destination, relation, ranks)
    return {'two_state_certificates': count, 'valid_certificates': valid,
            'direct_bad_cycle_failures': 0}


def stochastic_quotients(count=1000, seed=9301329):
    rng = random.Random(seed)
    for _ in range(count):
        levels = rng.randint(2, 5)
        fibres = {q: [(q, i) for i in range(rng.randint(1, 3))] for q in range(levels)}
        destination = {}
        for q in range(levels):
            weights = [rng.randint(1, 9) for _ in range(q+1)]
            destination[q] = {t: F(w, sum(weights)) for t, w in enumerate(weights)}
        source = {}
        for q, fibre in fibres.items():
            for p in fibre:
                source[p] = {}
                for nq, mass in destination[q].items():
                    weights = [rng.randint(1, 9) for _ in fibres[nq]]
                    for np, w in zip(fibres[nq], weights):
                        source[p][np] = mass * F(w, sum(weights))
        relation = {(p, q) for q, fibre in fibres.items() for p in fibre}
        bad_src = {p for p, q in relation if q > 0}
        bad_dst = set(range(1, levels))
        result = verify_probabilistic_migration(source, destination, bad_src, bad_dst,
                                               relation, relation, set(destination))
        assert result['valid'], result['violations']
        assert classify_chain(source, set(source), bad_src)['almost_sure']
        assert classify_chain(destination, set(destination), bad_dst)['almost_sure']
        # The upper levels have bad self-loops, so sure restoration fails.
        assert not classify_chain(source, set(source), bad_src)['sure']
        assert not classify_chain(destination, set(destination), bad_dst)['sure']
    return {'seed': seed, 'many_to_one_stochastic_quotients': count,
            'coupling_or_temporal_mismatches': 0}


def main():
    start = time.monotonic()
    results = {'coupling': coupling_checks(), 'sure_rank_migration': rank_checks(),
               'almost_sure_migration': stochastic_quotients()}
    results['elapsed_seconds'] = round(time.monotonic() - start, 3)
    results['scope'] = 'Conditional finite model certificates; no observed migration or source/warrant validation.'
    print(json.dumps(results, indent=2))


if __name__ == '__main__': main()
