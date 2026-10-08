"""Checks on published aggregates only; no dataset reconstruction is possible here."""
import json
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'calculation'))
sys.path.insert(0, str(ROOT / 'tail'))
from certified_exp import closed_bound, upward_decimal
from independent_oracles import closed_enclosure, exp_negative_enclosure
import tail_predicates as primary
import independent_tail_predicates_v1 as independent

def read(name):
    return json.loads((ROOT / 'aggregates' / name).read_text(encoding='utf-8'))

def rational(d):
    return primary.rational(d)

class AggregateCertificateChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = read('frozen_aggregate_certificate.json')
        cls.replication = read('independent_aggregate_certificate.json')
        cls.tail = read('post_inspection_tail_certificate.json')

    def test_scope_and_historical_replication_agreement(self):
        for d in (self.original, self.replication, self.tail):
            self.assertIs(d['raw_dataset_replay_in_this_package'], False)
        self.assertEqual(self.original['exact_description'], self.replication['independent_exact_description'])
        self.assertEqual(self.original['population_counts'], self.replication['count_agreement'])
        self.assertEqual(self.original['source_aggregate_sha256'], self.replication['original_aggregate_sha256'])
        self.assertIs(self.tail['post_inspection'], True)
        self.assertIs(self.tail['prospective_status_inherited'], False)

    def test_recorded_count_and_rational_identities(self):
        d = self.original['exact_description']
        self.assertEqual(d['games'], 75)
        self.assertEqual(d['roster_members'], 232)
        self.assertEqual(d['overall']['opportunities'], 48 * d['roster_members'])
        for kind in ('overall', 'disagreement'):
            c = d[kind]
            self.assertEqual(c['opportunities'], c['valid'] + c['absent'])
            self.assertLessEqual(c['exactly_50'], c['valid'])
        plus, minus = d['sides']['local_left'], d['sides']['global_left']
        q = rational
        self.assertEqual(q(d['T']), abs(q(d['S'])))
        self.assertEqual(q(d['S']), q(plus['Q']) - q(minus['Q']))
        self.assertEqual(q(d['H']), q(plus['M']) + q(minus['M']))
        self.assertEqual(q(d['S_R']), q(plus['V']) - q(minus['V']))
        self.assertEqual(q(d['availability_rate_difference']), q(plus['availability_rate']) - q(minus['availability_rate']))
        for side in (plus, minus):
            self.assertEqual(q(side['availability_rate']), q(side['V']) / q(side['M']))
            self.assertLessEqual(side['valid'], side['opportunities'])
        for key in ('opportunities', 'valid'):
            self.assertEqual(d['disagreement'][key], plus[key] + minus[key])

    def test_complete_frozen_upper_grid_two_implementations(self):
        d = self.original['exact_description']
        q = rational
        grid = self.original['sensitivity']['grid']
        expected = tuple(map(F, ('1', '11/10', '5/4', '3/2', '2', '3', '5', '10')))
        self.assertEqual(tuple(q(row['Gamma']) for row in grid[:-1]), expected)
        self.assertEqual(grid[-1]['Gamma'], 'unrestricted')
        self.assertEqual(len(self.replication['grid_certification']), 8)
        for row, historical_independent in zip(grid[:-1], self.replication['grid_certification']):
            gamma = q(row['Gamma'])
            result = closed_bound(q(d['T']), q(d['sum_abs_a']), q(d['V']), gamma)
            for key in ('Gamma', 'rho', 'D', 'exponent'):
                self.assertEqual(result[key], q(row[key]))
            self.assertEqual(result['interval'], tuple(map(q, row['interval'])))
            oracle = closed_enclosure(q(d['T']), q(d['sum_abs_a']), q(d['V']), gamma)
            self.assertEqual(oracle, tuple(map(q, historical_independent['independent_closed_bound_interval'])))
            self.assertEqual(oracle, result['interval'])
            self.assertEqual(exp_negative_enclosure(-result['exponent']), tuple(map(q, historical_independent['independent_exp_interval_512_bits'])))
            self.assertEqual(upward_decimal(result['interval'][1]), row['reported_upper_decimal_rounded_up_12_places'])
            self.assertEqual(result['interval'], (F(1), F(1)))
        self.assertEqual(tuple(map(q, grid[-1]['interval'])), (F(1), F(1)))
        self.assertEqual(q(self.replication['unrestricted_endpoint']), F(1))

    def test_two_strict_predicates_against_two_implementations(self):
        c = self.tail['certificate'];q = rational
        a = primary.evaluate(c['K'], c['R'], q(c['t']), q(c['V']))
        self.assertEqual(a, c)
        b = independent.evaluate(str(q(c['t'])), str(q(c['V'])), c['K'], c['R'])
        for name in ('A', 'B'):
            self.assertIs(b[name], c['checks'][name]['passed'])
            for independent_key, primary_key in [('lhs', 'left'), ('rhs', 'right'), ('margin', 'right_minus_left')]:
                self.assertEqual(F(b[name+'_'+independent_key]), q(c['checks'][name][primary_key]))
        self.assertEqual(F(b['strict_lower_bound']), q(c['strict_lower_bound']))
        self.assertEqual(q(c['strict_lower_bound'])-q(c['reference_level']), F(23,375))
        self.assertEqual(c['K'], self.original['exact_description']['games'])
        self.assertEqual(c['t'], self.original['exact_description']['T'])
        self.assertEqual(c['V'], self.original['exact_description']['V'])
        self.assertEqual(c['R'], 48)

    def test_frozen_elementary_rational_comparison(self):
        x = F(11,10)
        polynomial = x-x**3/6+x**5/40
        self.assertEqual(polynomial, F(11021153,12000000))
        self.assertEqual(F(23,25)-polynomial, F(18847,12000000))
        self.assertEqual(F(1,2)+F(5,12)*F(23,25), F(53,60))
        self.assertEqual(F(7,30)-2*F(61,1000), F(167,1500))
        self.assertGreater(F(167,1500), F(1,20))
        # Arithmetic checks do not prove the external Berry--Esseen theorem.

if __name__ == '__main__':
    unittest.main()
