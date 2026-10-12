"""Exact rational inverse-planning research model, not historical evidence.

Private source planning: activated positive-weight goals and selected causal paths.
Public data: menus, environments, selected actions, and resulting audience/material
outcomes. No private goal/recipe/utility enters the observation projection.

Decoded content means the audience INTERPRETS the event as presenting p. It is not
factive knowledge of the source's intention, acceptance of p, or truth of p.
The legacy output key intends_answer is specifically intention to indicate positive p;
the shared negative-correction goal is not misclassified as an affirmative answer.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product, combinations
import json

COMMUNICATION_EDGES = (
    ('act', 'attempt_to_indicate'),
    ('attempt_to_indicate', 'audience_decodes_p'),
    ('audience_decodes_p', 'audience_accepts_p'),
    ('audience_accepts_p', 'gratitude_for_reassurance'),
)
MATERIAL_EDGES = (('act', 'material_benefit'),
                  ('material_benefit', 'gratitude_for_gift'))
OTHER_EDGES = (('act', 'repair_completed'), ('act', 'carrier_warm'),
               ('act', 'false_claim_corrected'))

@dataclass(frozen=True)
class Policy:
    decode: F = F(0)
    accept: F = F(0)
    reassure: F = F(0)
    material: F = F(4)
    channel_belief: str = 'aligned'
    priority: tuple = ('keep', 'mantle', 'gesture', 'x', 'y', 'retry', 'reject')
    private_values: tuple = ()
    commitments: tuple = ('audience_decodes_p', 'audience_accepts_p',
                          'gratitude_for_reassurance', 'gratitude_for_gift',
                          'repair_completed', 'carrier_warm', 'false_claim_corrected')
    repair: F = F(4)
    warmth: F = F(4)
    correction: F = F(6)

@dataclass(frozen=True)
class Option:
    name: str
    decode_probability: F
    material_benefit: F
    cost: F
    can_carry_answer: bool = True
    repair_effect: F = F(0)
    warmth_effect: F = F(0)
    correction_effect: F = F(0)

@dataclass(frozen=True)
class Scene:
    options: tuple
    acceptance_given_decoding: F = F(1)
    believed_acceptance_given_decoding: F = F(1)
    name: str = ''


def ancestors(roots):
    reached = set(roots)
    while True:
        new = reached | {a for a, b in COMMUNICATION_EDGES + MATERIAL_EDGES + OTHER_EDGES
                         if b in reached}
        if new == reached:
            return reached
        reached = new


def belief_decode(p, a):
    if not a.can_carry_answer:
        return F(0)
    if p.channel_belief == 'aligned':
        return a.decode_probability
    if p.channel_belief == 'unaware_of_blocks':
        return F(1)
    raise ValueError(p.channel_belief)


def expected_outcomes(p, s, a):
    d = belief_decode(p, a)
    b = d * s.believed_acceptance_given_decoding
    return {'audience_decodes_p': d, 'audience_accepts_p': b,
            'gratitude_for_reassurance': b,
            'gratitude_for_gift': a.material_benefit,
            'repair_completed': a.repair_effect, 'carrier_warm': a.warmth_effect,
            'false_claim_corrected': a.correction_effect}


def weights(p):
    return (p.decode, p.accept, p.reassure, p.material, p.repair, p.warmth, p.correction)


def utility(p, s, a):
    # This is a score for ADOPTED planning goals. An appraisal can be positive
    # without being adopted: such a foreseen benefit is not optimized by this
    # bounded goal-directed planner. Goal adoption is explicit latent structure.
    e = expected_outcomes(p, s, a)
    ws = weights(p)
    return sum((w * v for w, (k, v) in zip(ws, e.items()) if k in p.commitments), F(0)) - a.cost + dict(p.private_values).get(a.name, F(0))


def plan(p, s, a):
    e = expected_outcomes(p, s, a)
    ws = weights(p)
    # A positively pursued attainable root contributes to this chosen action's
    # planning score. Zero-probability goals are not realized routes in this plan.
    roots = tuple(k for (k, v), w in zip(e.items(), ws)
                  if k in p.commitments and w > 0 and v > 0)
    nodes = ancestors(roots)
    selected_edges = [list(x) for x in COMMUNICATION_EDGES + MATERIAL_EDGES + OTHER_EDGES
                      if x[0] in nodes and x[1] in nodes]
    return {'action': a.name, 'adopted_goal_commitments': list(p.commitments),
            'active_terminal_goals': list(roots),
            'chosen_causal_recipe': selected_edges,
            'intends_answer': 'attempt_to_indicate' in nodes,
            'expected_outcomes': {k: str(v) for k, v in e.items()},
            'utility': str(utility(p, s, a))}


def optimal(p, s):
    scores = [utility(p, s, a) for a in s.options]
    best = max(scores)
    return tuple(a for a, v in zip(s.options, scores) if v == best)


def chosen(p, s):
    ranks = {x: i for i, x in enumerate(p.priority)}
    return min(optimal(p, s), key=lambda a: ranks[a.name])


def observe(p, s):
    a = chosen(p, s)
    return {'action': a.name,
            'menu': [{'name': x.name, 'cost': str(x.cost),
                      'decoding_probability': str(x.decode_probability),
                      'material_benefit': str(x.material_benefit)} for x in s.options],
            'actual_decoding_probability': str(a.decode_probability),
            'actual_acceptance_probability': str(a.decode_probability * s.acceptance_given_decoding),
            'material_benefit': str(a.material_benefit)}


def standard_scene(d_m=1, d_g=1, gift=1, assent=1, menu=('keep', 'mantle', 'gesture')):
    options = (Option('keep', F(0), F(0), F(0), False),
               Option('mantle', F(d_m), F(gift), F(1)),
               Option('gesture', F(d_g), F(0), F(1, 2)))
    return Scene(tuple(x for x in options if x.name in menu), F(assent), F(assent))


def menus(names):
    return [xs for n in range(1, len(names) + 1) for xs in combinations(names, n)]


def standard_interventions():
    for d_m, d_g, gift, assent in product([0, 1], repeat=4):
        for menu in menus(('keep', 'mantle', 'gesture')):
            yield standard_scene(d_m, d_g, gift, assent, menu)


def crossover(swap=False):
    # Two outwardly different delivery routes with stipulated equal material value
    # and cost. Swapping the channel changes only decoding efficacy. Exclusion
    # and source awareness are applicability premises, not tool-authenticated facts.
    return Scene((Option('keep', F(0), F(0), F(0), False),
                  Option('x', F(not swap), F(1), F(1)),
                  Option('y', F(swap), F(1), F(1))), name='swapped' if swap else 'first')


def calibration_scene(question=False, false_claim=False, repair=False, cold=False):
    # Stable context features, no episode-indexed exception. Material courtesy is
    # a response to current social attention, as in the retained strong rival.
    return Scene((Option('keep', F(0), F(0), F(0), False),
                  Option('mantle', F(question), F(question), F(1), True,
                         F(repair), F(cold)),
                  Option('reject', F(0), F(0), F(1), False,
                         correction_effect=F(question and false_claim))))


def retry_scene_at(cost):
    return Scene((Option('keep', F(0), F(0), F(0), False),
                  Option('retry', F(1), F(0), F(cost))))


def policy_record(p):
    return {'decode': str(p.decode), 'accept': str(p.accept),
            'reassure': str(p.reassure), 'material': str(p.material),
            'channel_belief': p.channel_belief, 'priority': p.priority,
            'private_values': {k: str(v) for k, v in p.private_values},
            'adopted_goal_commitments': p.commitments,
            'repair': str(p.repair), 'warmth': str(p.warmth), 'correction': str(p.correction)}


def run_experiment():
    material = Policy()
    mixed = Policy(decode=F(1, 4))
    base = standard_scene()
    rows = []
    for s in standard_interventions():
        left, right = optimal(material, s), optimal(mixed, s)
        same = len(left) == len(right) == 1 and left[0].name == right[0].name
        rows.append({'scene': observe(material, s), 'same_unique_action': same,
                     'material_plan': plan(material, s, left[0]),
                     'mixed_plan': plan(mixed, s, right[0])})
    recipes = {'indication_end': Policy(decode=F(3), material=F(0)),
               'belief_end': Policy(accept=F(3), material=F(0)),
               'gratitude_through_belief': Policy(reassure=F(3), material=F(0)),
               'material_only': material,
               'mixed_indication_material': mixed}
    recipe_plans = {k: plan(p, base, chosen(p, base)) for k, p in recipes.items()}
    hostile = standard_scene(assent=0)
    hostile_plan = plan(mixed, hostile, chosen(mixed, hostile))
    blocked = standard_scene(d_m=0, d_g=0)
    unaware = replace(mixed, channel_belief='unaware_of_blocks')
    failed_plan = plan(unaware, blocked, chosen(unaware, blocked))

    # Non-grid proof is in RESULT.md. This grid checks rational intermediate channel
    # reliability/acceptance values and every nonempty menu, including forced choices.
    dense_checked = 0
    for e in [F(1, 1000), F(1, 4), F(499, 1000)]:
        for d_m, d_g, assent in product([F(0), F(1, 3), F(1)], repeat=3):
            for gift in [0, 1]:
                for menu in menus(('keep', 'mantle', 'gesture')):
                    s = standard_scene(d_m, d_g, gift, assent, menu)
                    for p in [Policy(decode=e), Policy(accept=e), Policy(reassure=e),
                              Policy(decode=e/3, accept=e/3, reassure=e/3)]:
                        assert [x.name for x in optimal(p, s)] == [x.name for x in optimal(material, s)]
                        dense_checked += 1
    # The strict epsilon bound is sharp for this full intervention domain.
    boundary = standard_scene(gift=0, menu=('keep', 'gesture'))
    boundary_actions = [x.name for x in optimal(Policy(decode=F(1, 2)), boundary)]

    probes = [crossover(False), crossover(True)]
    profiles = []
    for d, a, r, g in product([F(0), F(1, 1000), F(1, 4), F(2)],
                              [F(0), F(2)], [F(0), F(2)], [F(2), F(4)]):
        for order in [('x', 'y', 'keep'), ('y', 'x', 'keep')]:
            p = Policy(d, a, r, g, priority=order)
            target = plan(p, probes[0], chosen(p, probes[0]))['intends_answer']
            profiles.append({'policy': policy_record(p), 'target': target,
                             'responses': tuple(chosen(p, s).name for s in probes)})
    collisions = {}
    for subset in [(), (0,), (1,), (0, 1)]:
        groups = {}
        for row in profiles:
            key = tuple(row['responses'][i] for i in subset)
            groups.setdefault(key, set()).add(row['target'])
        collisions[str(subset)] = any(len(v) > 1 for v in groups.values())
    minimal = min((len(xs) for xs in [(), (0,), (1,), (0, 1)]
                   if not collisions[str(xs)]), default=None)
    restricted_identified = all((row['responses'][0] != row['responses'][1]) == row['target'] for row in profiles)

    base_crossover_material = Policy(priority=('x', 'y', 'keep'))
    hidden = Policy(decode=F(1, 4), channel_belief='unaware_of_blocks', priority=('x', 'y', 'keep'))
    hidden_responses = [chosen(hidden, s).name for s in probes]
    material_responses = [chosen(base_crossover_material, s).name for s in probes]
    hidden_collision = hidden_responses == material_responses and plan(hidden, probes[0], chosen(hidden, probes[0]))['intends_answer']
    biased = Policy(decode=F(1, 4), priority=('x', 'y', 'keep'), private_values=(('x', F(1)),))
    biased_material = replace(biased, decode=F(0))
    bias_collision = [chosen(biased, s).name for s in probes] == [chosen(biased_material, s).name for s in probes]

    tied_policy = Policy(decode=F(1), material=F(0))
    tied_scene = standard_scene(menu=('keep', 'mantle'))
    tied = optimal(tied_policy, tied_scene)
    target_left = plan(material, base, chosen(material, base))
    target_right = plan(mixed, base, chosen(mixed, base))
    uncommitted = replace(mixed, commitments=('gratitude_for_gift',))
    uncommitted_plan = plan(uncommitted, base, chosen(uncommitted, base))
    # Following observed decoding failure and source learning the block, this
    # available fallback can pursue the still-adopted indication goal. The original
    # material gift has already been received; no second gift payoff is available.
    retry_scene = retry_scene_at(F(1, 8))
    retry_actions = {k: chosen(p, retry_scene).name for k, p in {
        'committed_mixed': mixed, 'material_only': material,
        'uncommitted_appraisal': uncommitted}.items()}
    calibration = [calibration_scene(), calibration_scene(question=True, false_claim=True),
                   calibration_scene(repair=True), calibration_scene(cold=True)]
    calibration_actions = {k: [chosen(p, s).name for s in calibration]
                           for k, p in {'material_only': material, 'committed_mixed': mixed}.items()}
    finite_retry_rows = []
    for n in range(1, 21):
        epsilon = F(1, 2 ** (n + 1))
        p = Policy(decode=epsilon)
        responses = [chosen(p, retry_scene_at(F(1, 2 ** j))).name for j in range(1, n + 1)]
        finite_retry_rows.append({'negative_probe_count': n, 'positive_witness': str(epsilon),
                                  'all_declined': all(x == 'keep' for x in responses)})
    detected = []
    for epsilon in [F(1, 1000), F(1, 4), F(1, 2 ** 30)]:
        # For a positive rational epsilon, this denominator-derived bound contains
        # a cost strictly below epsilon. A defective planner must fail a finite
        # witness check rather than make the diagnostic itself run forever.
        bound = epsilon.denominator.bit_length() + 1
        n = next((j for j in range(1, bound + 1)
                  if chosen(Policy(decode=epsilon), retry_scene_at(F(1, 2 ** j))).name == 'retry'), None)
        detected.append({'positive_goal_value': str(epsilon), 'first_strict_retry_probe': n,
                         'cost': str(F(1, 2 ** n)) if n is not None else None,
                         'finite_witness_bound': bound})
    floor = F(1, 8)
    floor_witness = Policy(decode=floor/2)
    floor_control = all(chosen(floor_witness, retry_scene_at(c)).name == 'keep'
                        for c in [floor, F(1, 4), F(1, 2), F(1), F(10)])
    return {
        'scope': 'Counterfactual exact-rational planning experiment. No historical experiment, authenticated source psychology, or public-adoption classifier.',
        'standard_decisions_checked': len(rows),
        'standard_pairs_same_unique_actions': all(x['same_unique_action'] for x in rows),
        'standard_pair_policies': [policy_record(material), policy_record(mixed)],
        'target_pair_differs_in_intended_answer': target_left['intends_answer'] != target_right['intends_answer'],
        'target_pair_plans': [target_left, target_right],
        'target_pair_same_public_observation': observe(material, base) == observe(mixed, base),
        'standard_rows': rows,
        'dense_rational_checks': dense_checked,
        'strict_upper_boundary': '1/2', 'boundary_actions': boundary_actions,
        'intended_answer_by_recipe': {k: x['intends_answer'] for k, x in recipe_plans.items()},
        'recipe_plans': recipe_plans,
        'hostility_indication_preserved': hostile_plan['intends_answer'],
        'hostile_recipient_accepts': observe(mixed, hostile)['actual_acceptance_probability'] != '0',
        'hostile_plan': hostile_plan,
        'failed_decoding_intended_answer': failed_plan['intends_answer'],
        'failed_decoding_actual_recognition': observe(unaware, blocked)['actual_decoding_probability'] != '0',
        'failed_decoding_plan': failed_plan,
        'uncommitted_positive_appraisal_intends_answer': uncommitted_plan['intends_answer'],
        'uncommitted_appraisal_still_positive': uncommitted.decode > 0,
        'uncommitted_plan': uncommitted_plan,
        'post_failure_retry_actions': retry_actions,
        'old_calibration_actions': calibration_actions,
        'old_calibration_plans': {k: [plan(p, s, chosen(p, s)) for s in calibration]
                           for k, p in {'material_only': material, 'committed_mixed': mixed}.items()},
        'finite_retry_nondetection_has_positive_witness': all(x['all_declined'] for x in finite_retry_rows),
        'finite_retry_rows': finite_retry_rows,
        'positive_cost_floor_retains_positive_witness': floor_control,
        'cost_floor_example': {'minimum_available_cost': str(floor), 'positive_goal_value': str(floor/2)},
        'tested_positive_values_eventually_retry_on_geometric_costs': all(x['first_strict_retry_probe'] is not None for x in detected),
        'geometric_retry_detections': detected,
        'post_failure_retry_plans': {k: plan(p, retry_scene, chosen(p, retry_scene))
            for k, p in {'committed_mixed': mixed, 'material_only': material,
                         'uncommitted_appraisal': uncommitted}.items()},
        'matched_crossover_minimal_probe_count': minimal,
        'matched_crossover_identifies_restricted_class': restricted_identified,
        'each_single_probe_has_opposite_intention_collision': collisions['(0,)'] and collisions['(1,)'],
        'matched_crossover_profiles': len(profiles),
        'crossover_subset_collisions': collisions,
        'crossover_rows': profiles,
        'hidden_channel_belief_collision': bool(hidden_collision),
        'hidden_channel_belief_responses': hidden_responses,
        'material_crossover_responses': material_responses,
        'private_action_value_collision': bias_collision,
        'private_action_value_responses': [chosen(biased, s).name for s in probes],
        'tie_actions': sorted(x.name for x in tied),
        'tie_intention_values': sorted({plan(tied_policy, tied_scene, x)['intends_answer'] for x in tied}),
        'observed_mantle_possibility_compatible': 'mantle' in [x.name for x in tied],
        'public_adoption_computed': False, 'commission_truth_in_planning': False,
    }

if __name__ == '__main__':
    print(json.dumps(run_experiment(), indent=2))
