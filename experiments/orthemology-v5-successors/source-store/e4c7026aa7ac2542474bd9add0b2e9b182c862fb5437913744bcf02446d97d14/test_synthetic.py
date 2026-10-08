"""Synthetic-only subset: finite arithmetic and schema controls; no actual data."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as F
import itertools
from pathlib import Path
import tempfile
import unittest
import placement_core as core
import certified_exp as interval

def rows_fixture(rosters=(1, 2)):
    rows = []
    for g, size in enumerate(rosters):
        for p in range(size):
            local = [True] * 48
            side = ['local' if r % 4 != 3 else 'global' for r in range(48)]
            signals = [{'local': {'pro': 0, 'against': 1},
                        'global': {'pro': 1, 'against': 0}} for _ in range(48)]
            for r in range(48):
                row = {
                    'gameId': f'synthetic-game-{g}', 'playerId': f'synthetic-player-{g}-{p}',
                    'batchId': 'synthetic-batch', 'round.index': str(r),
                    'treatment.playerCount': str(size), 'treatment.reward': 'individual',
                    'round.data.ifp': repr({'willHappen': True, 'globalAccurate': False}),
                    'player.data.roundLocalAccurate': repr(local),
                    'player.data.roundLeftSide': repr(side),
                    'player.data.roundSignals': repr(signals),
                    'player.data.localSource': 'synthetic-local-source',
                    'player.data.globalSource': 'synthetic-global-source',
                    'playerRound.data.value': '100', 'playerRound.data.correct': '',
                    'playerRound.data.groupCorrect': '',
                    'playerRound.data.groupVoteEmpty': '', 'playerRound.data.yesGroup': '',
                    'playerRound.data.rewarded': '', 'playerRound.data.knowledgeOfSubject': '',
                    'player.data.score': '',
                }
                for stage in ['question', 'response', 'feedback']:
                    rows.append(dict(row, **{'stage.name': stage}))
    return rows


def alter_opportunity(rows, index, field, value):
    for stage_offset in range(3):
        rows[3 * index + stage_offset][field] = value


def exact_tail(weights, t, intervals, direction='absolute'):
    """Test-only exhaustive endpoint-policy oracle, independent of production."""
    n = len(weights)
    histories = [h for k in range(n) for h in itertools.product((-1, 1), repeat=k)]
    best = F(0)
    for endpoints in itertools.product((0, 1), repeat=len(histories)):
        policy = dict(zip(histories, endpoints))
        total = F(0)
        for signs in itertools.product((-1, 1), repeat=n):
            s = sum((a * b for a, b in zip(weights, signs)), F(0))
            yes = abs(s) >= t if direction == 'absolute' else s >= t if direction == 'upper' else s <= -t
            if not yes:
                continue
            probability = F(1)
            for i, sign in enumerate(signs):
                q = intervals[i][policy[signs[:i]]]
                probability *= q if sign == 1 else 1 - q
            total += probability
        best = max(best, total)
    return best


class CoreControls(unittest.TestCase):
    def require_core(self):
        self.assertIsNotNone(core, 'placement_core implementation is absent')

    def test_exact_decimal_parser_and_absence(self):
        self.require_core()
        for token, expected in [('', None), (' \t', None), ('50', F(50)), ('5e1', F(50)),
                                ('0.1', F(1, 10)), ('99.9000', F(999, 10)),
                                ('+1E+2', F(100)), ('-0', F(0)), ('.25', F(1, 4))]:
            self.assertEqual(core.parse_forecast(token), expected)
        for token in ['nan', 'NaN', 'Infinity', '-1', '100.01', 'None', '1/2', '1_0', '0x20', 'true']:
            with self.assertRaises(core.ValidationError):
                core.parse_forecast(token)

    def test_exact_integer_semantics(self):
        self.require_core()
        for token in ['1', '1.0', '1e0', '+1']:
            self.assertEqual(core.parse_integer(token), 1)
        for token in ['1.1', 'NaN', '', 'True', '1/1']:
            with self.assertRaises(core.ValidationError):
                core.parse_integer(token)

    def test_event_truth_table_and_safe_parsing(self):
        self.require_core()
        for truth, local, global_ in itertools.product((False, True), repeat=3):
            bits = core.event_bits(repr({'willHappen': truth, 'globalAccurate': global_}))
            self.assertEqual(bits, (truth, global_))
            L, J, E = core.cues(truth, local, global_)
            self.assertEqual(L, truth if local else not truth)
            self.assertEqual(J, truth if global_ else not truth)
            self.assertEqual(E, local != global_)
        for text in ["{'willHappen': 1, 'globalAccurate': False}",
                     "{'willHappen': True, 'willHappen': False, 'globalAccurate': False}",
                     "{'willHappen': __import__('os').system('false'), 'globalAccurate': False}", '{}']:
            with self.assertRaises(core.ValidationError):
                core.event_bits(text)
        # Unrelated source payload expressions are parsed as syntax, never executed.
        self.assertEqual(core.event_bits("{'willHappen': True, 'globalAccurate': False, 'unused': foo() }"), (True, False))

    def test_complete_population_and_fixed_denominators(self):
        self.require_core()
        validated = core.validate_rows(rows_fixture())
        self.assertEqual(validated.receipt['counts']['opportunities'], 144)
        s = core.summarize(validated)
        self.assertEqual(s['S'], F(1, 2))
        self.assertEqual(s['H'], F(1))
        self.assertEqual(s['V'], F(1, 128))
        self.assertEqual(s['S'], s['sides']['local_left']['Q'] - s['sides']['global_left']['Q'])
        for game, size in validated.roster_sizes.items():
            self.assertEqual(size * 48 * core.opportunity_weight(2, size), F(1, 2))

    def test_game_with_no_disagreement_is_retained(self):
        self.require_core()
        rows = rows_fixture()
        for row in rows:
            if row['gameId'] == 'synthetic-game-0':
                row['round.data.ifp'] = repr({'willHappen': True, 'globalAccurate': True})
        s = core.summarize(core.validate_rows(rows))
        self.assertEqual(s['H'], F(1, 2))
        self.assertEqual(s['S'], F(1, 4))
        self.assertEqual(s['games'], 2)

    def test_absence_50_and_missing_score_are_distinct(self):
        self.require_core()
        present = rows_fixture()
        base = core.summarize(core.validate_rows(present))
        absent = copy.deepcopy(present)
        alter_opportunity(absent, 0, 'playerRound.data.value', '')
        neutral = copy.deepcopy(present)
        alter_opportunity(neutral, 0, 'playerRound.data.value', '5e1')
        a = core.summarize(core.validate_rows(absent))
        n = core.summarize(core.validate_rows(neutral))
        self.assertEqual(a['S'], base['S'] - F(1, 96))
        self.assertEqual(a['S'], n['S'])
        self.assertEqual(a['overall']['absent'], 1)
        self.assertEqual(n['overall']['exactly_50'], 1)
        self.assertEqual(a['overall']['valid'] + 1, n['overall']['valid'])
        altered_flags = copy.deepcopy(present)
        for row in altered_flags:
            row['playerRound.data.correct'] = 'False'
        self.assertEqual(core.summarize(core.validate_rows(altered_flags)), base)

    def test_forecast_stage_semantics(self):
        self.require_core()
        rows = rows_fixture((1,))
        rows[0]['playerRound.data.value'] = '1e2'
        rows[1]['playerRound.data.value'] = '100.000'
        core.validate_rows(rows)
        rows[2]['playerRound.data.value'] = '99'
        with self.assertRaises(core.ValidationError):
            core.validate_rows(rows)

    def test_structural_rejections(self):
        self.require_core()
        cases = []
        rows = rows_fixture((1,))
        cases.append(rows + [copy.deepcopy(rows[0])])
        cases.append(rows[1:])
        cases.append(rows[3:])
        for field, value in [('round.index', '48'), ('round.index', '0.5'),
                             ('gameId', ''), ('playerId', '  '), ('batchId', ''),
                             ('stage.name', 'other'), ('treatment.playerCount', '0'),
                             ('treatment.reward', 'other'),
                             ('player.data.roundLocalAccurate', repr([1] * 48)),
                             ('player.data.roundLeftSide', repr(['left'] * 48)),
                             ('player.data.roundLeftSide', repr(['local'] * 47)),
                             ('player.data.roundLocalAccurate', repr([True] * 47)),
                             ('playerRound.data.value', 'NaN')]:
            mutation = copy.deepcopy(rows)
            alter_opportunity(mutation, 0, field, value)
            cases.append(mutation)
        mutation = copy.deepcopy(rows)
        mutation[1]['player.data.roundLeftSide'] = repr(['global'] * 48)
        cases.append(mutation)
        mutation = copy.deepcopy(rows)
        alter_opportunity(mutation, 1, 'player.data.localSource', 'changed-source')
        cases.append(mutation)
        mutation = rows_fixture((2,))
        for row in mutation:
            row['treatment.playerCount'] = '1'
        cases.append(mutation)
        mutation = rows_fixture((2,))
        alter_opportunity(mutation, 48, 'round.data.ifp', repr({'willHappen': False, 'globalAccurate': False}))
        cases.append(mutation)
        for i, mutation in enumerate(cases):
            with self.subTest(case=i):
                with self.assertRaises(core.ValidationError):
                    core.validate_rows(mutation)

    def test_expected_counts_fail_without_subset_selection(self):
        self.require_core()
        with self.assertRaises(core.ValidationError):
            core.validate_rows(rows_fixture(), expected_counts={'opportunities': 143})

    def test_exact_byte_order_and_indexed_fields(self):
        self.require_core()
        rows = rows_fixture((1,))
        local = [r % 2 == 0 for r in range(48)]
        side = ['global' if r % 3 == 0 else 'local' for r in range(48)]
        for row in rows:
            row['player.data.roundLocalAccurate'] = repr(local)
            row['player.data.roundLeftSide'] = repr(side)
        v = core.validate_rows(rows)
        self.assertEqual([key[2] for key in v.order], list(range(48)))
        manual = F(0)
        for r in range(48):
            manual += F(int(local[r]), 48) * (1 if side[r] == 'local' else -1)
        self.assertEqual(core.summarize(v)['S'], manual)
        self.assertEqual(core.coordinate_order([('z','b',1), ('A','z',2), ('A','a',2), ('A','z',1)]),
                         [('A','z',1), ('A','a',2), ('A','z',2), ('z','b',1)])

    def test_sign_and_polarity_invariances(self):
        self.require_core()
        original = rows_fixture()
        base = core.summarize(core.validate_rows(original))
        swapped = copy.deepcopy(original)
        for row in swapped:
            values = __import__('ast').literal_eval(row['player.data.roundLeftSide'])
            row['player.data.roundLeftSide'] = repr(['global' if x == 'local' else 'local' for x in values])
        flipped = core.summarize(core.validate_rows(swapped))
        self.assertEqual(flipped['S'], -base['S'])
        self.assertEqual(flipped['T'], base['T'])
        for row in swapped:
            row['player.data.roundLocalAccurate'] = repr([False] * 48)
            row['round.data.ifp'] = repr({'willHappen': True, 'globalAccurate': True})
            row['player.data.localSource'], row['player.data.globalSource'] = row['player.data.globalSource'], row['player.data.localSource']
        self.assertEqual(core.summarize(core.validate_rows(swapped))['S'], base['S'])
        inverted = copy.deepcopy(original)
        for row in inverted:
            row['round.data.ifp'] = repr({'willHappen': False, 'globalAccurate': False})
            row['playerRound.data.value'] = '0'
        self.assertEqual(core.summarize(core.validate_rows(inverted))['S'], base['S'])

    def test_local_invariant_and_always_left_meaning(self):
        self.require_core()
        rows = rows_fixture((1,))
        self.assertEqual(core.summarize(core.validate_rows(rows))['S'], F(1, 2))
        for row in rows:
            r = int(row['round.index'])
            row['playerRound.data.value'] = '0' if r % 4 == 3 else '100'
        self.assertEqual(core.summarize(core.validate_rows(rows))['S'], 1)

    def test_all_zero_and_no_support(self):
        self.require_core()
        rows = rows_fixture((1,))
        for row in rows:
            row['playerRound.data.value'] = '50'
        s = core.summarize(core.validate_rows(rows))
        self.assertEqual((s['S'], s['T'], s['V']), (0, 0, 0))
        self.assertEqual(s['H'], 1)
        for row in rows:
            row['round.data.ifp'] = repr({'willHappen': True, 'globalAccurate': True})
        s = core.summarize(core.validate_rows(rows))
        self.assertEqual(s['H'], 0)
        self.assertIsNone(s['sides']['local_left']['availability_rate'])

    def test_digest_guard_detects_altered_copy(self):
        self.require_core()
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'synthetic.txt'
            p.write_bytes(b'synthetic predecessor')
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            core.verify_file(p, digest, p.stat().st_size)
            altered = Path(directory) / 'altered.txt'
            altered.write_bytes(p.read_bytes() + b'!')
            with self.assertRaises(core.ValidationError):
                core.verify_file(altered, digest, p.stat().st_size)
            self.assertEqual(p.read_bytes(), b'synthetic predecessor')

    def test_seven_projection_checks_and_exact_key_set(self):
        self.require_core()
        self.assertTrue(hasattr(core, 'validate_projection'), 'projection assurance is absent')
        validated = core.validate_rows(rows_fixture((1,)))
        projected = []
        for game, player, r in validated.order:
            o = validated.outcomes[(game, player, r)]
            projected.append({'gameId': game, 'playerId': player, 'roundIndex': str(r),
                              'forecast': str(o.forecast), 'accuracy': '', 'groupAccuracy': '',
                              'expN': str(o.capacity), 'globalAccuracy': str(int(o.global_correct)),
                              'localAccuracy': str(int(o.local_correct)), 'incentiveScheme': o.reward})
        receipt = core.validate_projection(projected, validated)
        self.assertEqual(receipt['checks_passed'], 7)
        for field, replacement in [('forecast', '99'), ('accuracy', '1'), ('groupAccuracy', '0'),
                                   ('expN', '2'), ('globalAccuracy', '1'), ('localAccuracy', '0'),
                                   ('incentiveScheme', 'group')]:
            mutated = copy.deepcopy(projected)
            mutated[0][field] = replacement
            with self.assertRaises(core.ValidationError):
                core.validate_projection(mutated, validated)
        for mutated in [projected[1:], projected + [projected[0]]]:
            with self.assertRaises(core.ValidationError):
                core.validate_projection(mutated, validated)

    def test_event_unpacking_or_dynamic_keys_fail_closed(self):
        self.require_core()
        for token in ["{'willHappen': True, 'globalAccurate': False, **{'willHappen': False}}",
                      "{'willHappen': True, 'globalAccurate': False, f(): 1}",
                      "{'willHappen': True, 'globalAccurate': False, 1: 'unused'}"]:
            with self.assertRaises(core.ValidationError):
                core.event_bits(token)

    def test_auxiliary_final_state_and_full_event_repeat_consistency(self):
        self.require_core()
        for field, value in [('player.data.score', 'changed'), ('playerRound.data.rewarded', 'True'),
                             ('playerRound.data.knowledgeOfSubject', 'some'),
                             ('round.data.ifp', "{'willHappen': True, 'globalAccurate': False, 'extra': 1}")]:
            rows = rows_fixture((1,))
            rows[0][field] = value
            with self.assertRaises(core.ValidationError):
                core.validate_rows(rows)


class IntervalControls(unittest.TestCase):
    def require_interval(self):
        self.assertIsNotNone(interval, 'certified_exp implementation is absent')

    def test_enclosure_accuracy_and_small_positive_upper(self):
        self.require_interval()
        for q in [F(0), F(1, 3), F(1), F(9), F(100), F(10000)]:
            lo, hi = interval.exp_neg_interval(q)
            self.assertTrue(0 <= lo <= hi <= 1)
            self.assertGreater(hi, 0)
            self.assertLessEqual(hi - lo, F(1, 10**12))
            with localcontext() as context:
                context.prec = 180
                point = (-(Decimal(q.numerator) / Decimal(q.denominator))).exp()
                self.assertTrue(Decimal(lo.numerator) / Decimal(lo.denominator) <= point <= Decimal(hi.numerator) / Decimal(hi.denominator))

    def test_256_bit_minimum_and_invalid_arguments(self):
        self.require_interval()
        with self.assertRaises(ValueError):
            interval.exp_neg_interval(F(-1))
        with self.assertRaises(ValueError):
            interval.exp_neg_interval(F(1), bits=128)

    def test_adaptive_counterexample_and_directed_tails(self):
        self.require_interval()
        bounds = [(F(1,4), F(3,4))] * 2
        self.assertEqual(exact_tail([F(1), F(1)], F(2), bounds), F(3,4))
        self.assertEqual(exact_tail([F(1), F(1)], F(2), bounds, 'upper'), F(9,16))
        self.assertEqual(exact_tail([F(1), F(1)], F(2), bounds, 'lower'), F(9,16))
        product = max(p*q + (1-p)*(1-q) for p, q in itertools.product((F(1,4), F(3,4)), repeat=2))
        self.assertEqual(product, F(5,8))
        _, unadjusted_hi = interval.exp_neg_interval(F(1))
        self.assertLess(2 * unadjusted_hi, F(3,4))
        _, corrected_hi = interval.closed_bound(F(2), F(2), F(2), F(3))['interval']
        self.assertGreaterEqual(corrected_hi, F(3,4))

    def test_mixed_sign_exhaustive_fixture(self):
        self.require_interval()
        bounds = [(F(1,4), F(2,5)), (F(1,5), F(4,5)), (F(1,3), F(3,4))]
        self.assertEqual(exact_tail([F(2), F(-1), F(3)], F(2), bounds), F(47,50))
        self.assertEqual(exact_tail([F(2), F(-1), F(3)], F(2), bounds, 'upper'), F(33,50))
        self.assertEqual(exact_tail([F(2), F(-1), F(3)], F(2), bounds, 'lower'), F(19,30))

    def test_bound_direction_all_declared_gammas_and_edge_cases(self):
        self.require_interval()
        for weights in [[F(1), F(1)], [F(2), F(-1), F(3)], [F(1,3), F(-1,7)], [F(0), F(0)], [F(-1)]]:
            total = sum(map(abs, weights), F(0))
            variance = sum((a*a for a in weights), F(0))
            for t in sorted({F(0), total / 2, total, total + 1}):
                previous = None
                for gamma in interval.GAMMAS:
                    bounds = [(1/(1+gamma), gamma/(1+gamma))] * len(weights)
                    actual = exact_tail(weights, t, bounds)
                    result = interval.closed_bound(t, total, variance, gamma)
                    lo, hi = result['interval']
                    self.assertGreaterEqual(hi, actual)
                    self.assertTrue(0 <= lo <= hi <= 1)
                    if previous is not None:
                        self.assertGreaterEqual(hi, previous[0])
                    previous = (lo, hi)
        self.assertEqual(exact_tail([F(1)], F(1), [(F(1,2), F(1,2))]), 1)
        self.assertEqual(exact_tail([F(1)], F(2), [(F(1,2), F(1,2))]), 0)

    def test_near_alpha_enclosure_and_upward_display(self):
        self.require_interval()
        # Rational exponent within 1e-60 of log(40), independently constructed.
        with localcontext() as context:
            context.prec = 180
            q = F(str(Decimal(40).ln().quantize(Decimal('1e-60'))))
        lo, hi = interval.exp_neg_interval(q)
        lo, hi = 2*lo, 2*hi
        self.assertLess(abs(hi - F(1,20)), F(1,10**59))
        rendered = interval.upward_decimal(hi, places=12)
        self.assertGreaterEqual(F(rendered), hi)
        self.assertEqual(interval.alpha_relation(F(1,25), F(1,16)), 'unresolved_enclosure')
        self.assertEqual(interval.alpha_relation(F(1,25), F(1,20)), 'upper_bound_at_or_below_reference')
        self.assertEqual(interval.alpha_relation(F(1,16), F(1,10)), 'bound_above_reference_not_lower_bound_on_p_star')

