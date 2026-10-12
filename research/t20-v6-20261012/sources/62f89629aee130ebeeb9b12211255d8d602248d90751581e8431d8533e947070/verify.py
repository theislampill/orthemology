#!/usr/bin/env python3
"""Small exact controls, not a proof by enumeration of Theorem 1."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = []


def row(*items):
    return tuple(F(x) for x in items)


def check_channel(channel):
    assert channel
    n = len(channel[0])
    assert all(len(r) == n for r in channel)
    assert all(x >= 0 for r in channel for x in r)
    assert all(sum(r[i] for r in channel) == 1 for i in range(n))


def bayes(p, likelihood):
    raw = tuple(a * b for a, b in zip(p, likelihood))
    alpha = sum(raw)
    return alpha, None if alpha == 0 else tuple(x / alpha for x in raw)


def mix(weights, points):
    assert sum(weights) == 1 and all(w >= 0 for w in weights)
    return tuple(sum(w * q[i] for w, q in zip(weights, points))
                 for i in range(len(points[0])))


def barycenter(p, channel):
    branches = [bayes(p, r) for r in channel]
    live = [(a, q) for a, q in branches if a > 0]
    assert mix([a for a, q in live], [q for a, q in live]) == p
    return branches


def block_partition(channel):
    groups = {}
    for i in range(len(channel[0])):
        column = tuple(r[i] for r in channel)
        groups.setdefault(column, []).append(i)
    return list(groups.values())


def conditional(p, block):
    weight = sum(p[i] for i in block)
    if weight == 0:
        return weight, None
    return weight, tuple(p[i] / weight if i in block else F(0)
                         for i in range(len(p)))


def norm2(p, centre):
    return sum((a - b) ** 2 for a, b in zip(p, centre))


def record(name, **details):
    RESULTS.append({"control": name, "status": "PASS", **details})


def globally_stable_inequality():
    channel = [row('3/4', '3/4', '1/4'), row('1/4', '1/4', '3/4')]
    check_channel(channel)
    assert block_partition(channel) == [[0, 1], [2]]
    vertices = [row(1, 0, 0), row('1/2', '1/2', 0), row(0, 0, 1)]
    for v in vertices:
        for a, q in barycenter(v, channel):
            assert q == v
    p = row('1/2', '1/4', '1/4')
    branches = barycenter(p, channel)
    assert branches == [(F(5, 8), row('3/5', '3/10', '1/10')),
                        (F(3, 8), row('1/3', '1/6', '1/2'))]
    for a, q in branches:
        assert q[0] >= q[1]
        assert q[0] / q[1] == p[0] / p[1]
    record("globally_stable_inequality", branches=branches)


def curved_local_not_global():
    u = row('1/3', '1/3', '1/3')
    channel = [row('3/4', '1/4', '1/2'), row('1/4', '3/4', '1/2')]
    check_channel(channel)
    assert block_partition(channel) == [[0], [1], [2]]
    first = barycenter(u, channel)
    assert first == [(F(1, 2), row('1/2', '1/6', '1/3')),
                     (F(1, 2), row('1/6', '1/2', '1/3'))]
    assert all(norm2(q, u) == F(1, 18) for a, q in first)
    second = barycenter(first[0][1], channel)
    assert second == [(F(7, 12), row('9/14', '1/14', '2/7')),
                      (F(5, 12), row('3/10', '3/10', '2/5'))]
    assert norm2(second[0][1], u) == F(1, 6) > F(1, 18)
    assert norm2(second[1][1], u) == F(1, 150) < F(1, 18)
    record("curved_local_not_global", first=first, second=second,
           radius_squared=F(1, 18), failed_distance_squared=F(1, 6))


def zero_likelihoods():
    # Last row is impossible for every prior; the first two disclose the block.
    channel = [row(1, 1, 0), row(0, 0, 1), row(0, 0, 0)]
    check_channel(channel)
    assert block_partition(channel) == [[0, 1], [2]]
    p = row('1/2', '1/4', '1/4')
    branches = barycenter(p, channel)
    assert branches == [(F(3, 4), row('2/3', '1/3', 0)),
                        (F(1, 4), row(0, 0, 1)), (F(0), None)]
    assert bayes(row(0, 0, 1), channel[0]) == (F(0), None)
    record("zero_likelihood_defined_branches", branches=branches)


def minimal_hull():
    channel = [row('3/4', '3/4', '1/4', '1/2'),
               row('1/4', '1/4', '3/4', '1/2')]
    check_channel(channel)
    blocks = block_partition(channel)
    assert blocks == [[0, 1], [2], [3]]
    p = row('1/6', '1/3', '1/2', 0)
    conds = [conditional(p, b) for b in blocks]
    assert conds == [(F(1, 2), row('1/3', '2/3', 0, 0)),
                     (F(1, 2), row(0, 0, 1, 0)), (F(0), None)]
    live = [(w, q) for w, q in conds if w > 0]
    assert mix([w for w, q in live], [q for w, q in live]) == p
    for a, q in barycenter(p, channel):
        assert q[3] == 0
        assert conditional(q, blocks[0])[1] == conds[0][1]
        assert conditional(q, blocks[1])[1] == conds[1][1]
    # Every selected point is in the same two-vertex hull, including its endpoints.
    for t in [F(0), F(1, 5), F(1, 2), F(4, 5), F(1)]:
        q = mix([t, 1-t], [live[0][1], live[1][1]])
        for likelihood in channel:
            alpha, image = bayes(q, likelihood)
            new_t = image[0] + image[1]
            assert image == mix([new_t, 1-new_t], [live[0][1], live[1][1]])
            assert bayes(image, tuple(1/x for x in likelihood))[1] == q
    record("minimal_hull_components_and_inverse", blocks=blocks, conditionals=conds)


def topology_and_convexity():
    channel = [row('3/4', '1/4'), row('1/4', '3/4')]
    check_channel(channel)
    for p in [row('1/2', '1/2'), row('1/10', '9/10')]:
        for a, q in barycenter(p, channel):
            assert all(x > 0 for x in q)
    vertices = [row(1, 0), row(0, 1)]
    for p in vertices:
        assert all(q == p for a, q in barycenter(p, channel))
    assert mix([F(1, 2), F(1, 2)], vertices) not in vertices
    record("nonclosed_and_nonconvex_boundaries")


def single_likelihood():
    p = row('1/2', '1/2')
    channel = [row('2/3', '1/3'), row('1/3', '2/3')]
    check_channel(channel)
    assert bayes(p, row(2, 1))[1] == row('2/3', '1/3')
    assert bayes(p, channel[0])[1] == row('2/3', '1/3')
    assert bayes(p, channel[1])[1] == row('1/3', '2/3')
    for t in [F(1, 2), F(3, 4), F(1)]:
        assert bayes(row(t, 1-t), row(2, 1))[1][0] >= F(1, 2)
    record("single_likelihood_is_not_complete_channel")


def copied_vs_fresh():
    u = row('1/3', '1/3', '1/3')
    likelihood = row('3/4', '1/4', '1/2')
    alpha, q = bayes(u, likelihood)
    copied = bayes(q, row(1, 1, 1))[1]
    fresh = bayes(q, likelihood)[1]
    joint_fresh = bayes(u, tuple(x*x for x in likelihood))[1]
    joint_copy = bayes(u, likelihood)[1]
    assert copied == q == joint_copy
    assert fresh == joint_fresh != copied
    record("copied_vs_fresh", copied=copied, fresh=fresh)


def changing_state():
    channel = [row('3/4', '1/4'), row('1/4', '3/4')]
    reset = row('1/2', '1/2')
    check_channel(channel)
    instruments = [[[likelihood[i] * reset[k] for k in range(2)]
                    for i in range(2)] for likelihood in channel]
    assert all(sum(M[i][k] for M in instruments for k in range(2)) == 1
               for i in range(2))
    for p in [reset, row('1/3', '2/3'), row(1, 0)]:
        for M in instruments:
            raw = tuple(sum(p[i] * M[i][k] for i in range(2)) for k in range(2))
            assert tuple(x / sum(raw) for x in raw) == reset
    # Passive old-target updating instead changes this same nondegenerate prior.
    assert bayes(reset, channel[0])[1] != reset
    record("state_changing_instrument", fixed_new_state=reset)


def block_indicators():
    channel = [row('1/4', '1/4', '1/2', '3/4'),
               row('3/4', '3/4', '1/2', '1/4')]
    check_channel(channel)
    blocks = block_partition(channel)
    columns = [tuple(r[b[0]] for r in channel) for b in blocks]
    indicators = []
    for j, block in enumerate(blocks):
        f = [F(1)] * 4
        for k, other in enumerate(blocks):
            if k == j:
                continue
            y = next(y for y in range(len(channel)) if columns[j][y] != columns[k][y])
            for i in range(4):
                f[i] *= ((channel[y][i] - columns[k][y]) /
                         (columns[j][y] - columns[k][y]))
        assert f == [F(int(i in block)) for i in range(4)]
        indicators.append(f)
    assert all(sum(f[i] for f in indicators) == 1 for i in range(4))
    assert all(x*x == x for f in indicators for x in f)
    p = row('1/8', '1/8', '1/4', '1/2')
    recovered = [sum(a*b for a, b in zip(p, f)) for f in indicators]
    assert recovered == [F(1, 4), F(1, 4), F(1, 2)]
    record("exact_block_indicator_interpolation", indicators=indicators,
           recovered_block_masses=recovered)


def unchanged_inputs():
    manifest = json.loads((HERE / 'INPUT_BINDINGS.json').read_text())
    for entry in manifest['inputs']:
        data = (HERE / entry['source_path']).read_bytes()
        assert len(data) == entry['bytes'], entry['source_path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['source_path']
    return len(manifest['inputs'])


def main():
    globally_stable_inequality()
    curved_local_not_global()
    zero_likelihoods()
    minimal_hull()
    topology_and_convexity()
    single_likelihood()
    copied_vs_fresh()
    changing_state()
    block_indicators()
    count = unchanged_inputs()
    payload = {'status': 'PASS', 'exact_control_groups': len(RESULTS),
               'bound_inherited_inputs_unchanged': count,
               'scope': 'Small exact rational controls; no universal theorem by enumeration.',
               'results': RESULTS}
    text = json.dumps(payload, indent=2, default=str) + '\n'
    (HERE / 'CHECK_RESULTS.json').write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
