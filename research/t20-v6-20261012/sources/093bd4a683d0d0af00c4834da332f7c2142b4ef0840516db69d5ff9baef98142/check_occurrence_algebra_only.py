"""Packaging-only algebra replay. Does not replace the reviewer's custody check."""
from fractions import Fraction as F
from itertools import product
import json
for theta, report in product((0, 1), repeat=2):
    discrepancy = theta ^ report
    assert report ^ discrepancy == theta
for theta, report, verifier in product((0, 1), repeat=3):
    discrepancy = verifier ^ report
    assert report ^ discrepancy == verifier
    assert ((report ^ discrepancy) == theta) == (verifier == theta)
rows = []
for accuracy in (F(1, 5), F(1, 2), F(4, 5), F(1)):
    for report, discrepancy in product((0, 1), repeat=2):
        target_weights = [F(1, 4) * (accuracy if theta == (report ^ discrepancy) else 1 - accuracy)
                          for theta in (0, 1)]
        assert sum(target_weights) == F(1, 4)
        assert target_weights[report ^ discrepancy] / sum(target_weights) == accuracy
    rows.append({'accuracy': str(accuracy), 'decoded_target_posterior': str(accuracy)})
print(json.dumps({'status': 'PASS', 'exact_comparator_cases': 4, 'fallible_logical_cases': 8,
                  'probability_controls': rows, 'source_custody_checked': False,
                  'scope': 'Packaging-only ordinary algebra replay. Not an independent review, source custody replay, System R derivation, or knowledge certificate.'}, indent=2))
