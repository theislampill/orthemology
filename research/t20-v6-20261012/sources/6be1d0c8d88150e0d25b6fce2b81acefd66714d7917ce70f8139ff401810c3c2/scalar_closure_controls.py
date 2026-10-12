"""Exact finite controls, not an analytic or kernel proof."""
from fractions import Fraction as Q
import json

points = [(Q(1, 2), Q(7, 20), Q(7, 20)), (Q(2, 5),) * 3]
models = {
    'polynomial': lambda x: 1 / (1 + x*x),
    'bernoulli_entropy': lambda x: x * (1 - x),
    'constant_positive': lambda x: Q(2),
    'affine_positive': lambda x: 2*x + 1,
}
result = {}
for name, q in models.items():
    rows = []
    for b in points:
        z = sum(b); defect = z-1; S = sum(map(q, b))
        V = tuple(-defect*q(x) for x in b)
        W = tuple(x/S for x in V)
        gain = []
        for j in range(3):
            dloss = sum((b[i] - (1 if i == j else 0))*V[i]/q(b[i]) for i in range(3))
            assert dloss == -defect**2
            gain.append(dloss)
        assert sum(V) == -defect*S
        assert sum(W) == -defect
        rows.append(dict(b=list(map(str, b)), z=str(z), objective=str(defect**2/2),
                         mobility=str(S), zdot=str(sum(V)), normalized_zdot=str(sum(W)),
                         truth_state_derivatives=list(map(str,gain))))
    same_rate = rows[0]['zdot'] == rows[1]['zdot']
    assert same_rate == (name in {'constant_positive','affine_positive'})
    result[name] = rows
assert result['polynomial'][0]['mobility'] == '5796/2245'
assert result['polynomial'][1]['mobility'] == '75/29'
assert result['bernoulli_entropy'][0]['mobility'] == '141/200'
assert result['bernoulli_entropy'][1]['mobility'] == '18/25'
print(json.dumps({'status':'PASS', 'scope':'exact finite algebra controls', 'models':result},indent=2))
