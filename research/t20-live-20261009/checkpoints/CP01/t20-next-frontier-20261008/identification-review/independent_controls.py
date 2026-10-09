"""Independent exact controls of a frozen two-root reconstruction snapshot.

These are verification controls, not additional discoveries or proof counts.
The endpoint law is calculated by route-level distribution convolution, rather
than by the author's no-hit product or incidence-bit enumeration.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import importlib.util
import json
import random
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('frozen_identifiability', HERE/'frozen-v1/identifiability.py')
lib = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lib
spec.loader.exec_module(lib)
KINDS = ((1,0), (2,0), (3,0), (1,2), (2,1))
METRICS = {}


def independent_distribution(model, profile):
    law = {0: F(1)}
    for (positive, guard, output), count in model.items():
        if positive & profile != positive or guard & profile:
            continue
        chance = {1:F(1,2), 2:F(1,3), 3:F(1,6)}[positive]
        for _ in range(count):
            nxt = defaultdict(F)
            for state, mass in law.items():
                nxt[state] += mass * (1-chance)
                nxt[state | output] += mass * chance
            law = dict(nxt)
    assert sum(law.values()) == 1
    return law


def independent_panel(model, effects):
    panel = {}
    for profile in (1,2,3):
        law = independent_distribution(model, profile)
        for query in range(1,1 << effects):
            panel[profile, query] = sum((mass for state, mass in law.items() if state & query == 0), F())
    return panel


def solve(matrix, rhs):
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(matrix, rhs)]
    n = len(rhs)
    for col in range(n):
        pivot = next(row for row in range(col,n) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x/scale for x in a[col]]
        for row in range(n):
            if row != col:
                scale = a[row][col]
                a[row] = [x-scale*y for x,y in zip(a[row], a[col])]
    return [row[-1] for row in a]


class IndependentReview(unittest.TestCase):
    def test_valuation_decoder_against_linear_solve(self):
        matrix = ((-1,1,-1), (0,-1,-1), (0,0,1))
        for counts in product(range(9), repeat=3):
            rhs = [sum(x*y for x,y in zip(row, counts)) for row in matrix]
            self.assertEqual(solve(matrix, rhs), list(counts))
            q = F(1,2)**counts[0]*F(2,3)**counts[1]*F(5,6)**counts[2]
            self.assertEqual(lib.decode_ab(q), counts)
        METRICS['valuation_vectors'] = 9**3

    def test_random_panels_from_independent_distribution_convolution(self):
        rng = random.Random(80106202)
        cases = 0
        incidence_crosschecks = 0
        for effects in range(1,6):
            keys = [(p,n,t) for p,n in KINDS for t in range(1,1 << effects)]
            for _ in range(60):
                model = defaultdict(int)
                for _ in range(rng.randrange(21)):
                    model[rng.choice(keys)] += 1
                model = dict(model)
                panel = independent_panel(model, effects)
                self.assertEqual(lib.recover_model(panel, effects), model)
                if sum(model.values()) <= 6:
                    for profile in (1,2,3):
                        self.assertEqual(independent_distribution(model, profile),
                                         lib.exact_distribution(lib.occurrences(model), profile))
                        incidence_crosschecks += 1
                cases += 1
        METRICS['convolution_models'] = cases
        METRICS['incidence_distribution_crosschecks'] = incidence_crosschecks

    def test_omission_delta_by_independent_linear_algebra(self):
        cases = 0
        for effects in range(1,6):
            universe = (1 << effects)-1
            hit = [[int(bool(query & output)) for output in range(1,universe+1)] for query in range(1,universe+1)]
            for omitted in range(1,universe+1):
                inverse_column = solve(hit, [int(query == omitted) for query in range(1,universe+1)])
                left, right = lib.omitted_query_witness(effects, omitted)
                self.assertEqual(inverse_column, [left.get((1,0,t),0)-right.get((1,0,t),0) for t in range(1,universe+1)])
                lp, rp = independent_panel(left,effects), independent_panel(right,effects)
                differing = {key for key in lp if lp[key] != rp[key]}
                self.assertEqual(differing, {(1,omitted),(3,omitted)})
                cases += 1
        METRICS['omission_witnesses'] = cases

    def test_bounded_panels_grid_and_sup_norm_separation(self):
        keys = [(p,n,t) for p,n in KINDS for t in range(1,4)]
        models = [{}]
        for count in (1,2):
            for chosen in combinations_with_replacement(keys, count):
                model = defaultdict(int)
                for key in chosen:
                    model[key] += 1
                models.append(dict(model))
        panels = [tuple(independent_panel(m,2).values()) for m in models]
        self.assertEqual(len(set(panels)), len(panels))
        for panel in panels:
            self.assertTrue(all((q*36).denominator == 1 for q in panel))
        distance = min(max(abs(a-b) for a,b in zip(left,right)) for i,left in enumerate(panels) for right in panels[i+1:])
        self.assertGreaterEqual(distance, F(1,36))
        METRICS['bounded_models'] = len(models)
        METRICS['bounded_minimum_sup_distance'] = str(distance)

    def test_full_law_can_reconstitute_discarded_coordinate(self):
        left, right = lib.omitted_query_witness(2,3)
        law_left = independent_distribution(left,1)
        law_right = independent_distribution(right,1)
        self.assertNotEqual(law_left,law_right)
        self.assertNotEqual(law_left.get(0,F()), law_right.get(0,F()))
        self.assertEqual(sum(v for k,v in law_left.items() if not k&1), sum(v for k,v in law_right.items() if not k&1))
        self.assertEqual(sum(v for k,v in law_left.items() if not k&2), sum(v for k,v in law_right.items() if not k&2))
        METRICS['omission_oracle_limit'] = 'Retained coordinates only; full endpoint laws distinguish the witness.'

    def test_inherited_reactive_records_do_not_specify_bundle_gates(self):
        checkpoint = ROOT/'recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation'
        sys.path.insert(0,str(checkpoint/'sovereignty-choice-semantics/reactive-context-extension/src'))
        import reactive_context as reactive
        catalogue = reactive.Catalogue(('e0','e1'))
        actual = reactive.epistemic_model(catalogue)['worlds'][2]['actual']
        self.assertEqual(actual['events'], frozenset(('e0','e1')))
        self.assertEqual(actual['supports']['e0'], actual['supports']['e1'])
        bundled = {(3,0,3):1,(1,2,3):1,(2,1,3):1}
        separate = {(p,n,t):1 for p,n in ((3,0),(1,2),(2,1)) for t in (1,2)}
        for profile in (1,2,3):
            for model in (bundled,separate):
                records = lib.occurrences(model)
                self.assertEqual(lib.exact_distribution(records,profile,rates={1:F(1),2:F(1)}), {3:F(1)})
            self.assertNotEqual(independent_distribution(bundled,profile),independent_distribution(separate,profile))
        METRICS['reactive_transport_limit'] = 'Equal unattenuated per-event supports allow different joint attenuated laws.'

    def test_adaptive_targeting_is_not_fixed_act_suppression(self):
        checkpoint = ROOT/'recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation'
        sys.path.insert(0,str(checkpoint/'sovereignty-choice-semantics/reactive-context-extension/src'))
        import reactive_context as reactive
        catalogue = reactive.Catalogue(('e0','e1'))
        a = reactive.Exercise('A',0,1)
        b = reactive.Exercise('B',0,2)
        joint = reactive.execute(catalogue,a,b)
        fixed_solo = reactive.execute(catalogue,a,None)
        retargeted_solo = reactive.execute(catalogue,reactive.Exercise('A',0,catalogue.respond(0,None)),None)
        self.assertNotEqual(joint['events'],fixed_solo['events'])
        self.assertEqual(joint['events'],retargeted_solo['events'])
        self.assertNotEqual(a.setting,retargeted_solo['acts'][0].setting)
        METRICS['fixed_act_limit'] = 'Policy re-solving changes the intrinsic setting; it is not the same intervention.'


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentReview)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (HERE/'results/INDEPENDENT_METRICS.json').write_text(json.dumps(METRICS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
