"""Reviewer-owned exhaustive small decision checks. No candidate imports.

Finite partitions of concrete worlds certify exact answers, not authenticity,
permissions, morality or physical metadata opacity. Checks survive python -O.
"""
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path

W = tuple(product((0, 1), repeat=3))
STAR = tuple(w for w in W if sum(w) >= 2)
Q = lambda w: all(w)
V = lambda w: tuple(w)
LEFT = lambda w: (w[0], w[1])
RIGHT = lambda w: (w[1], w[2])
CARDS = (LEFT, RIGHT)
checks = {}

def check(name, observed, expected):
    if observed != expected:
        raise RuntimeError(f'{name}: observed {observed!r}, expected {expected!r}')
    checks[name] = observed

def blocks(worlds, observation):
    result = defaultdict(list)
    for w in worlds:
        result[observation(w)].append(w)
    return tuple(tuple(b) for b in result.values())

def homogeneous(worlds, target):
    return len({target(w) for w in worlds}) <= 1

def decidable(worlds, target, actions, budget):
    # Enumerate root actions; all observed branches need a completing policy.
    if homogeneous(worlds, target):
        return True
    if budget == 0:
        return False
    for i, action in enumerate(actions):
        partitions = blocks(worlds, action)
        if len(partitions) == 1:
            continue
        remaining = actions[:i] + actions[i+1:]
        if all(decidable(b, target, remaining, budget-1) for b in partitions):
            return True
    return False

def cost(worlds=W, target=Q, actions=CARDS, initial=lambda w: ()):
    initial_blocks = blocks(worlds, initial)
    for budget in range(len(actions)+1):
        if all(decidable(b, target, actions, budget) for b in initial_blocks):
            return budget
    return 'infinity'

for name, worlds in [('full_product', W), ('four_world_star', STAR)]:
    check(name+'_cards_only', cost(worlds), 2)
    for i, key in enumerate('abc'):
        check(name+'_fixed_'+key, cost(worlds, initial=lambda w, i=i:(i, w[i])), 2 if i==1 else 1)
        negative = tuple(w for w in worlds if w[i] == 0)
        check(name+'_known_false_'+key, cost(negative), 0)
    check(name+'_full_role_table', cost(worlds, initial=V), 0)
    check(name+'_valid_Q_verdict', cost(worlds, initial=Q), 0)
    check(name+'_value_dependent_origin_identity', cost(worlds, initial=lambda w:'a' if Q(w) else 'b'), 0)
    check(name+'_restored_source', cost(worlds, actions=CARDS+(V,)), 1)
    check(name+'_accepted_live_reader', cost(worlds, actions=CARDS+(Q,)), 1)
    check(name+'_uninformative_old_result_d', cost(worlds, initial=lambda w:1), 2)

# Additional observations change the problem even if they are not labelled Q.
check('correlated_outside_d_equals_Q', cost(initial=Q), 0)
check('correlated_outside_d_equals_a', cost(initial=lambda w:w[0]), 1)
for field in ('length', 'status', 'timing', 'authentication_payload', 'role_bearing_locator'):
    check('free_'+field+'_encodes_Q', cost(initial=lambda w:(field,Q(w))), 0)
check('rich_left_response_encodes_missing_c', cost(actions=(lambda w:(LEFT(w),w[2]), RIGHT)), 1)

# Different epistemic targets, permission menus, and actual contracts.
check('Q_verdict_insufficient_for_all_individual_roles', cost(target=V, initial=Q), 2)
check('edge_plus_opposite_card_answers_individual_roles', cost(target=V, initial=lambda w:w[0]), 1)
check('copies_only_of_a', cost(target=lambda w:w[0]), 1)
check('copies_do_not_add_new_role', all(Q(w)==all(w[i] for i in (2,0,1,0)) for w in W), True)
check('no_permitted_menu_cannot_complete', cost(actions=()), 'infinity')
check('only_left_permitted_cannot_complete', cost(actions=(LEFT,)), 'infinity')
check('retained_Q_needs_no_read_permission', cost(actions=(), initial=Q), 0)
check('safe_withholding_not_a_total_answer', homogeneous(W,Q), False)
check('budget_one_rejects_b_plan', decidable(tuple(w for w in W if w[1]),Q,CARDS,1), False)
check('renegotiated_budget_two_accepts_b_plan', decidable(tuple(w for w in W if w[1]),Q,CARDS,2), True)

# A lucky realised answer and high prior accuracy do not prove zero-error completion.
check('always_false_uniform_accuracy', str(Fraction(sum(not Q(w) for w in W),len(W))), '7/8')
check('all_positive_answer_true_can_be_lucky', Q((1,1,1)), True)
check('left_positive_transcript_has_both_answers', {Q(w) for w in W if LEFT(w)==(1,1)}=={False,True}, True)
# Concrete one-request randomized bounded-error policy: choose a card uniformly;
# if a zero is visible answer false, otherwise answer true with probability 2/3.
probabilities=[]
for w in W:
    p_true = sum(Fraction(1,2)*Fraction(2,3) for action in CARDS if all(action(w)))
    probabilities.append(p_true if Q(w) else 1-p_true)
check('one_request_bounded_error_policy_worst_success', str(min(probabilities)), '2/3')

print(json.dumps({'status':'PASS','worlds_full':len(W),'worlds_star':len(STAR),
    'method':'Exhaustive small decision-tree feasibility by observation partitions; no candidate imports.',
    'check_count':len(checks),'checks':checks}, indent=2, sort_keys=True))
