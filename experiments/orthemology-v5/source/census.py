"""Declared finite checks only. Not a proof over all terms or semantic codes."""
from __future__ import annotations
import json, itertools, time
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import reference as r
import extensions as e

def require(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError('census: ' + label)

@lru_cache(None)
def types_exact(depth: int, size: int) -> tuple:
    if size == 1:
        return (('bottom',),) + tuple((('v', i) for i in range(depth)))
    if size < 1:
        return ()
    out = [('all', a) for a in types_exact(depth + 1, size - 1)]
    for n in range(1, size - 1):
        out += [('arr', a, b) for a in types_exact(depth, n) for b in types_exact(depth, size - 1 - n)]
    return tuple(out)

def types_upto(depth: int, size: int) -> tuple:
    return tuple((a for n in range(1, size + 1) for a in types_exact(depth, n)))

def run() -> dict:
    start = time.monotonic()
    out = {}
    n = 3
    pairs = list(itertools.product(range(n), repeat=2))
    edge_sets = [tuple((pair for k, pair in enumerate(pairs) if m >> k & 1)) for m in range(1 << 9)]
    sat = [tuple(e.saturated_masks(n, edges)) for edges in edge_sets]
    connectivity = []
    for edges in edge_sets:
        reachable = [[i == j for j in range(n)] for i in range(n)]
        for a, b in edges:
            reachable[a][b] = reachable[b][a] = True
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reachable[i][j] |= reachable[i][k] and reachable[k][j]
        connectivity.append(sum((1 << k for k, (i, j) in enumerate(pairs) if reachable[i][j])))
    count = 0
    for base in range(512):
        for extra in range(512):
            require((sat[base] == sat[base | extra]) == (extra & ~connectivity[base] == 0), 'substitution/invariant check at original line 43')
            count += 1
    out['relation_extension'] = {'carrier_size': 3, 'base_relations': 512, 'added_relations': 512, 'cases': count, 'claim': 'old invariant codes preserved iff new edges stay within old undirected components'}
    count = 0
    breakdown = {}
    for d in range(3):
        bs = types_upto(d + 1, 4)
        args = types_upto(d, 3)
        for b, a in itertools.product(bs, args):
            actual = r.instantiate_type(b, a)
            require(actual == e.named_instantiate(b, a), 'substitution/invariant check at original line 52')
            r._wf_type(actual, d)
            count += 1
        breakdown[str(d)] = {'body_types': len(bs), 'argument_types': len(args), 'pairs': len(bs) * len(args)}
    out['independent_substitution'] = {'body_max_nodes': 4, 'argument_max_nodes': 3, 'open_depths': [0, 1, 2], 'cases': count, 'breakdown': breakdown}
    count = 0
    for d in range(2):
        for b, a in itertools.product(types_upto(d + 1, 4), types_upto(d, 3)):
            inst = r.instantiate_type(b, a)
            for table in itertools.product(range(2), repeat=4):
                for rho in itertools.product(range(4), repeat=d):
                    require(e.eval_type(inst, rho, table, 2) == e.eval_type(b, (e.eval_type(a, rho, table, 2),) + rho, table, 2), 'substitution/invariant check at original line 64')
                    count += 1
    out['finite_interpretation'] = {'carrier_size': 2, 'application_tables': 16, 'cases': count, 'scope': 'substitution algebra only; NOT a model of SKI equations'}
    count = 0
    for n in range(1, 5):
        for obs in itertools.product((0, 1), repeat=n):
            represented = {tuple((g[o] for o in obs)) for g in itertools.product((0, 1), repeat=2)}
            require(len(represented) == 2 ** len(set(obs)), 'substitution/invariant check at original line 72')
            for vals in itertools.product((0, 1), repeat=n):
                constant = all((vals[i] == vals[j] for i in range(n) for j in range(n) if obs[i] == obs[j]))
                require((vals in represented) == constant, 'substitution/invariant check at original line 75')
                count += 1
    out['observation_factorisation'] = {'index_sizes': [1, 2, 3, 4], 'observations': 2, 'values': 2, 'cases': count}
    count = 0
    d = e.app(e.app(e.S, e.I), e.I)
    om = e.app(d, d)
    for which, f0 in enumerate((e.K, e.app(e.K, e.I))):
        f = f0
        for wrappers in range(33):
            _, trace = r.normalize(e.app(e.app(f, e.Z), e.O), 1000)
            cert = e.certify_selector(f, trace)
            require(cert.selector == which, 'substitution/invariant check at original line 83')
            require(cert.overhead == wrappers + 1 + which, 'substitution/invariant check at original line 84')
            for x, y in itertools.product((e.I, e.K, e.Z, e.O, om), repeat=2):
                tr = e.replay_selector(cert, x, y)
                require(tr[-1] == (x, y)[which], 'substitution/invariant check at original line 87')
                count += 1
            f = e.app(e.I, f)
    out['symbolic_specialisation'] = {'wrapped_selectors': 66, 'input_pairs_each': 25, 'cases': count, 'includes_divergent_inputs': True}
    count = 0
    for n in range(13):
        counts = {0: 0, 1: 0, None: 0}
        for bits in itertools.product((0, 1), repeat=n):
            counts[e.irrational_selector_prefix(bits)] += 1
            count += 1
        m = e.irrational_prefix_mass(n)
        require(m['first'] == F(counts[0], 1 << n), 'substitution/invariant check at original line 97')
        require(m['second'] == F(counts[1], 1 << n), 'substitution/invariant check at original line 98')
        require(counts[None] == 1, 'substitution/invariant check at original line 99')
    out['irrational_sampler'] = {'all_bit_prefixes_through_length': 12, 'cases': count, 'residual_at_depth_512': str(e.irrational_prefix_mass(512)['unresolved']), 'scope': 'exact finite prefixes; almost-sure termination and expected cost proved in prose'}
    out['status'] = 'PASS'
    out['elapsed_seconds'] = round(time.monotonic() - start, 3)
    return out
if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
