"""Frozen archived-placement services: pure exact arithmetic and validation.

No archived files are opened at import; no predecessor or author code is imported.
Structural validation does not evaluate a placement/forecast relation. Placement
vectors and outcome records remain separate until summarize() is explicitly called.
"""
from __future__ import annotations
import ast
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from pathlib import Path
import re

DECIMAL_TOKEN = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')
STAGES = frozenset(('question', 'response', 'feedback'))
FORECAST = 'playerRound.data.value'
LOCAL_VECTOR = 'player.data.roundLocalAccurate'
PLACEMENT_VECTOR = 'player.data.roundLeftSide'
SIGNAL_VECTOR = 'player.data.roundSignals'
SCORE_FIELDS = ('playerRound.data.correct', 'playerRound.data.groupCorrect',
                'playerRound.data.groupVoteEmpty', 'playerRound.data.yesGroup')
AUXILIARY_REPEAT_FIELDS = ('playerRound.data.rewarded', 'playerRound.data.knowledgeOfSubject',
                           'player.data.score', 'round.data.ifp')
REQUIRED_FIELDS = ('batchId', 'gameId', 'playerId', 'round.index', 'stage.name',
                   'round.data.ifp', LOCAL_VECTOR, PLACEMENT_VECTOR, SIGNAL_VECTOR,
                   'player.data.localSource', 'player.data.globalSource',
                   'treatment.playerCount', 'treatment.reward', FORECAST) + SCORE_FIELDS + AUXILIARY_REPEAT_FIELDS[:-1]


class ValidationError(ValueError):
    """Sanitized, key-free gate code; never includes a raw token or identifier."""


def fail(code):
    raise ValidationError(code)


def parse_decimal(text):
    if not isinstance(text, str) or not DECIMAL_TOKEN.fullmatch(text.strip()):
        fail('invalid_decimal_token')
    try:
        return Fraction(text.strip())
    except (ValueError, OverflowError, ZeroDivisionError):
        fail('invalid_decimal_token')


def parse_forecast(text):
    if not isinstance(text, str):
        fail('invalid_forecast_field')
    if not text.strip():
        return None
    number = parse_decimal(text)
    if not 0 <= number <= 100:
        fail('forecast_out_of_range')
    return number


def parse_integer(text):
    number = parse_decimal(text)
    if number.denominator != 1:
        fail('nonintegral_index_or_capacity')
    return number.numerator


@lru_cache(maxsize=8192)
def event_bits(text):
    """Extract literal target booleans; never evaluate unrelated event payload."""
    try:
        node = ast.parse(text, mode='eval').body
        if not isinstance(node, ast.Dict):
            fail('event_not_dictionary')
        fields = {}
        seen = set()
        for key, value in zip(node.keys, node.values):
            if not isinstance(key, ast.Constant) or type(key.value) is not str:
                fail('event_key_not_literal_string')
            if key.value in seen:
                fail('duplicate_event_key')
            seen.add(key.value)
            if isinstance(key, ast.Constant) and key.value in ('willHappen', 'globalAccurate'):
                if key.value in fields:
                    fail('duplicate_event_target')
                if not isinstance(value, ast.Constant) or type(value.value) is not bool:
                    fail('nonboolean_event_target')
                fields[key.value] = value.value
        if set(fields) != {'willHappen', 'globalAccurate'}:
            fail('missing_event_target')
        return fields['willHappen'], fields['globalAccurate']
    except (SyntaxError, TypeError, RecursionError):
        fail('malformed_event_syntax')


@lru_cache(maxsize=8192)
def parse_vector(text, kind):
    try:
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError, TypeError, RecursionError):
        fail('malformed_vector')
    if type(value) is not list or len(value) != 48:
        fail('vector_not_48_entry_list')
    if kind == 'local':
        if any(type(x) is not bool for x in value):
            fail('nonboolean_local_vector')
        return tuple(value)
    if kind == 'placement':
        if any(type(x) is not str or x not in ('local', 'global') for x in value):
            fail('invalid_placement_alphabet')
        return tuple(value)
    if kind == 'signals':
        # Structural indexing check only. Selectors are never interpreted as strength.
        result = []
        for signal in value:
            if type(signal) is not dict or set(signal) != {'local', 'global'}:
                fail('signal_roles_invalid')
            pair = []
            for role in ('local', 'global'):
                inner = signal[role]
                if type(inner) is not dict or set(inner) != {'pro', 'against'}:
                    fail('signal_selector_schema_invalid')
                entries = (inner['pro'], inner['against'])
                if any(type(x) is not int for x in entries):
                    fail('signal_selector_not_integer')
                pair.append(entries)
            result.append(tuple(pair))
        return tuple(result)
    fail('unknown_vector_kind')


def parse_optional_bool(text):
    if not isinstance(text, str):
        fail('invalid_optional_boolean_field')
    text = text.strip()
    if not text:
        return None
    if text == 'True':
        return True
    if text == 'False':
        return False
    fail('invalid_optional_boolean_token')


def cues(truth, local_correct, global_correct):
    if any(type(x) is not bool for x in (truth, local_correct, global_correct)):
        fail('cue_arguments_not_boolean')
    local = truth if local_correct else not truth
    global_ = truth if global_correct else not truth
    return local, global_, local != global_


def coordinate_order(keys):
    return sorted(keys, key=lambda key: (key[0].encode('utf-8'), key[2], key[1].encode('utf-8')))


def verify_file(path, expected_sha256, expected_bytes=None):
    path = Path(path)
    with path.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    size = path.stat().st_size
    if digest != expected_sha256 or (expected_bytes is not None and size != expected_bytes):
        fail('input_digest_or_size_mismatch')
    return {'sha256': digest, 'bytes': size}


def csv_rows(path, fields=REQUIRED_FIELDS):
    """Yield only allowlisted fields; no direct-account/demographic fields used."""
    with Path(path).open('r', encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            fail('missing_or_duplicate_csv_header')
        if not set(fields).issubset(reader.fieldnames):
            fail('required_csv_columns_missing')
        for row in reader:
            if None in row or any(row.get(field) is None for field in fields):
                fail('malformed_csv_row_width')
            yield {field: row[field] for field in fields}


@dataclass(frozen=True)
class Outcome:
    truth: bool
    global_correct: bool
    local_correct: bool
    forecast: Fraction | None
    scores: tuple
    capacity: int
    reward: str


@dataclass
class Validated:
    # Private in-memory keyed records. No serializer exports these maps.
    outcomes: dict
    placements: dict
    roster_sizes: dict
    order: list
    receipt: dict


def validate_rows(rows, expected_counts=None):
    """Validate whole planned population; never compute eligibility-by-placement.

    The structural receipt deliberately contains no placement marginals, cue
    disagreement counts, response/placement cross-tabs, coefficients or S values.
    """
    seen_stages = defaultdict(set)
    repeated = {}
    members = defaultdict(set)
    game_attributes = {}
    participant_attributes = {}
    round_attributes = {}
    outcomes, placements = {}, {}
    forecast_tokens = {}  # retained privately until stage semantic checks finish
    total_rows = 0
    for row in rows:
        if any(field not in row for field in REQUIRED_FIELDS):
            fail('required_row_fields_missing')
        game, player, batch = (row[field] for field in ('gameId', 'playerId', 'batchId'))
        if any(not isinstance(x, str) or not x.strip() for x in (game, player, batch)):
            fail('empty_game_player_or_batch_key')
        r = parse_integer(row['round.index'])
        if not 0 <= r < 48:
            fail('round_outside_zero_based_schedule')
        stage = row['stage.name']
        if stage not in STAGES:
            fail('unexpected_stage_name')
        key = (game, player, r)
        if stage in seen_stages[key]:
            fail('duplicate_opportunity_stage')
        seen_stages[key].add(stage)
        total_rows += 1
        capacity = parse_integer(row['treatment.playerCount'])
        if capacity < 1:
            fail('capacity_not_positive')
        reward = row['treatment.reward']
        if reward not in ('individual', 'group'):
            fail('unexpected_reward_condition')
        game_attr = (batch, capacity, reward)
        if game in game_attributes and game_attributes[game] != game_attr:
            fail('conflicting_game_attributes')
        game_attributes[game] = game_attr
        members[game].add(player)
        local_vector = parse_vector(row[LOCAL_VECTOR], 'local')
        placement_vector = parse_vector(row[PLACEMENT_VECTOR], 'placement')
        signals = parse_vector(row[SIGNAL_VECTOR], 'signals')
        sources = (row['player.data.localSource'], row['player.data.globalSource'])
        if any(not isinstance(s, str) or not s.strip() for s in sources):
            fail('missing_source_descriptor')
        participant_attr = (sources, local_vector, placement_vector, signals)
        member_key = (game, player)
        if member_key in participant_attributes and participant_attributes[member_key] != participant_attr:
            fail('conflicting_participant_sources_or_vectors')
        participant_attributes[member_key] = participant_attr
        placements[member_key] = placement_vector
        truth, global_correct = event_bits(row['round.data.ifp'])
        game_round = (game, r)
        if game_round in round_attributes and round_attributes[game_round] != (truth, global_correct):
            fail('conflicting_game_round_cue_bits')
        round_attributes[game_round] = (truth, global_correct)
        forecast = parse_forecast(row[FORECAST])
        scores = tuple(parse_optional_bool(row[field]) for field in SCORE_FIELDS)
        outcome = Outcome(truth, global_correct, local_vector[r], forecast, scores, capacity, reward)
        # In addition to whole-vector and game/member checks, final state is
        # compared semantically across stages, including decimal forecast tokens.
        final_state = (outcome, tuple(row[field] for field in AUXILIARY_REPEAT_FIELDS))
        if key in repeated and repeated[key] != final_state:
            fail('conflicting_repeated_final_state')
        repeated[key] = final_state
        forecast_tokens.setdefault(key, []).append(row[FORECAST])
        outcomes[key] = outcome
    if not members:
        fail('empty_population')
    expected_keys = {(g, p, r) for g, players in members.items() for p in players for r in range(48)}
    if set(outcomes) != expected_keys:
        fail('missing_scheduled_opportunity')
    if any(stages != STAGES for stages in seen_stages.values()):
        fail('missing_required_stage')
    roster_sizes = {game: len(players) for game, players in members.items()}
    if any(game_attributes[g][1] < size for g, size in roster_sizes.items()):
        fail('exported_roster_exceeds_capacity')
    valid = sum(outcome.forecast is not None for outcome in outcomes.values())
    counts = {'games': len(members), 'distinct_player_ids': len({p for ps in members.values() for p in ps}),
              'game_player_pairs': sum(roster_sizes.values()), 'game_rounds': len(round_attributes),
              'opportunities': len(outcomes), 'stage_rows': total_rows,
              'valid_forecasts': valid, 'absent_forecasts': len(outcomes) - valid,
              'exactly_50_forecasts': sum(outcome.forecast == 50 for outcome in outcomes.values()),
              'valid_forecasts_missing_correctness': sum(outcome.forecast is not None and outcome.scores[0] is None for outcome in outcomes.values())}
    if expected_counts is not None:
        for name, expected in expected_counts.items():
            if name not in counts or counts[name] != expected:
                fail('expected_inventory_count_mismatch:' + name)
    receipt = {'status': 'STRUCTURAL_VALIDATION_PASS', 'counts': counts,
               'checks': ['exact nonempty preserved text keys', 'unique complete three-stage schedule',
                          'complete 48-opportunity exported rosters', 'exact integer round/capacity fields',
                          'semantic forecast agreement and finite [0,100] decimals',
                          'literal boolean cue fields and local vectors', 'stable complete placement vectors',
                          'stable source descriptors and selector vectors', 'stable game batch/capacity/reward',
                          'truth/global agreement within game-round', 'nominal capacity covers exported roster'],
               'placement_forecast_relation_computed': False,
               'privacy': 'Aggregate structural receipt only; no identifiers or row records.'}
    return Validated(outcomes, placements, roster_sizes, coordinate_order(outcomes), receipt)


PROJECTION_FIELDS = ('gameId', 'playerId', 'roundIndex', 'forecast', 'accuracy', 'groupAccuracy',
                     'expN', 'globalAccuracy', 'localAccuracy', 'incentiveScheme')


def projection_bool(text, optional=False):
    if optional and not text.strip():
        return None
    if text.strip() in ('True', 'False'):
        return text.strip() == 'True'
    number = parse_decimal(text)
    if number not in (0, 1):
        fail('projection_boolean_not_zero_or_one')
    return bool(number)


def validate_projection(rows, validated):
    """Exactly the seven inherited agreements, on the entire raw key set."""
    seen = set()
    for row in rows:
        if any(field not in row for field in PROJECTION_FIELDS):
            fail('projection_columns_missing')
        key = (row['gameId'], row['playerId'], parse_integer(row['roundIndex']))
        if key in seen:
            fail('duplicate_projection_key')
        seen.add(key)
        if key not in validated.outcomes:
            fail('projection_key_not_in_raw_population')
        o = validated.outcomes[key]
        actual = (parse_forecast(row['forecast']), projection_bool(row['accuracy'], optional=True),
                  projection_bool(row['groupAccuracy'], optional=True), parse_integer(row['expN']),
                  projection_bool(row['globalAccuracy']), projection_bool(row['localAccuracy']), row['incentiveScheme'])
        expected = (o.forecast, o.scores[0], o.scores[1], o.capacity, o.global_correct, o.local_correct, o.reward)
        if actual != expected:
            fail('projection_field_disagreement')
    if seen != set(validated.outcomes):
        fail('projection_key_set_mismatch')
    return {'status': 'SEVEN_PROJECTION_CHECKS_PASS', 'checks_passed': 7,
            'rows': len(seen), 'same_complete_key_set': True,
            'fields': ['forecast', 'stored_correct', 'group_correct', 'nominal_capacity',
                       'global_cue_correctness', 'local_cue_correctness', 'reward_condition']}


def opportunity_weight(games, roster_size):
    if type(games) is not int or type(roster_size) is not int or min(games, roster_size) < 1:
        fail('invalid_weight_denominator')
    return Fraction(1, games * roster_size * 48)


def summarize(validated):
    """Compute descriptive aggregates from explicitly supplied validated input."""
    games = len(validated.roster_sizes)
    zero = Fraction(0)
    S, H, total_abs, variance = zero, zero, zero, zero
    sides = {name: {'M': zero, 'V': zero, 'Q': zero, 'opportunities': 0, 'valid': 0}
             for name in ('local_left', 'global_left')}
    overall = {'opportunities': len(validated.order), 'valid': 0, 'absent': 0, 'exactly_50': 0}
    disagreement = {'opportunities': 0, 'valid': 0, 'absent': 0, 'exactly_50': 0}
    for game, player, r in validated.order:
        outcome = validated.outcomes[(game, player, r)]
        local, _, eligible = cues(outcome.truth, outcome.local_correct, outcome.global_correct)
        forecast = outcome.forecast
        available = forecast is not None
        overall['valid' if available else 'absent'] += 1
        overall['exactly_50'] += int(forecast == 50)
        # Every coordinate is visited in the prescribed order, including zeros.
        c = opportunity_weight(games, validated.roster_sizes[game]) * int(eligible)
        Y = (2 * int(local) - 1) * (forecast / 50 - 1) if available else zero
        a = c * Y
        side = validated.placements[(game, player)][r]
        sign = 1 if side == 'local' else -1
        S += a * sign
        H += c
        total_abs += abs(a)
        variance += a * a
        if eligible:
            disagreement['opportunities'] += 1
            disagreement['valid' if available else 'absent'] += 1
            disagreement['exactly_50'] += int(forecast == 50)
            d = sides['local_left' if sign == 1 else 'global_left']
            d['M'] += c
            d['V'] += c * int(available)
            d['Q'] += a
            d['opportunities'] += 1
            d['valid'] += int(available)
    for side in sides.values():
        side['availability_rate'] = side['V'] / side['M'] if side['M'] else None
    plus, minus = sides['local_left'], sides['global_left']
    if S != plus['Q'] - minus['Q'] or not abs(S) <= total_abs <= H <= 1:
        fail('exact_statistic_identity_failure')
    rate_difference = (plus['availability_rate'] - minus['availability_rate']
                       if plus['M'] and minus['M'] else None)
    return {'games': games, 'roster_members': sum(validated.roster_sizes.values()),
            'overall': overall, 'disagreement': disagreement,
            'S': S, 'T': abs(S), 'H': H, 'sum_abs_a': total_abs, 'V': variance,
            'sides': sides, 'S_R': plus['V'] - minus['V'],
            'availability_rate_difference': rate_difference,
            'support_status': 'no_disagreement_support' if H == 0 else 'all_directional_coefficients_zero' if variance == 0 else 'directional_support',
            'crosscheck_S_equals_Qplus_minus_Qminus': True}
