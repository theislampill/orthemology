from pathlib import Path
from fractions import Fraction
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent

def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

author = load('crt_author_frozen',root/'frozen/crt_calibration.py')
review = load('crt_independent',root/'independent_crt_controls.py')
rng = random.Random(77331008)
cases = 0
nonunit = []
for roots in range(1,7):
    expected,primes,numerators,denominator = review.construct(roots)
    actual = author.construct(roots)
    assert actual.rates == expected
    assert actual.private_primes == primes
    assert actual.numerators == numerators
    assert actual.denominator == denominator
    for support,coefficient in enumerate(actual.diagonal(),1):
        if coefficient>1:
            nonunit.append({'roots':roots,'support':support,'prime':primes[support-1],'coefficient':coefficient})
    for _ in range(10):
        counts = {support:count for support in range(1,1<<roots) if (count := rng.randrange(4))}
        q = Fraction(1)
        for support,count in counts.items():
            q *= review.failure(support,expected)**count
        assert actual.decode(q)==counts
        cases += 1
receipt = {'calibrations_agree_through_roots':6,'independent_readout_author_decoder_cases':cases,'nonunit_diagonal_examples':nonunit}
(root/'results/CROSSCHECK_METRICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
