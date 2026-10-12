"""Separate ultimate goal, intended means, foreseen uptake and public evidence.

The selected plan's causal recipe is supplied model structure, not observable private
intention. Public assessment below is explicitly defeasible, not an authenticated
truth label or a universal philosophical definition of assertion.
"""
from dataclasses import dataclass, asdict, replace
import json

@dataclass(frozen=True)
class Plan:
    name: str
    ultimate_goal: str
    selected_recipe: tuple
    foreseen_effects: tuple

# (parent,child) dependencies are the source's chosen means to its end.
# A separate list records known side effects that are not means in that chosen recipe.
COMMUNICATE=Plan('communicate', 'audience_accepts_q',
                (('send_mantle','recognize_source_response'),
                 ('recognize_source_response','audience_accepts_q')),
                ('audience_accepts_q',))
COURTESY_BY_ACKNOWLEDGMENT=Plan('courtesy_by_acknowledgment','audience_gratified',
                (('send_mantle','recognize_source_response'),
                 ('recognize_source_response','audience_accepts_q'),
                 ('audience_accepts_q','audience_gratified')),
                ('audience_accepts_q','audience_gratified'))
MATERIAL_COURTESY=Plan('material_courtesy','audience_gratified',
                (('send_mantle','material_gift_received'),
                 ('material_gift_received','audience_gratified')),
                ('audience_accepts_q','material_gift_received','audience_gratified'))


def selected_means_and_end(plan):
    ancestors={plan.ultimate_goal}
    changed=True
    while changed:
        old=set(ancestors)
        ancestors.update(a for a,b in plan.selected_recipe if b in ancestors)
        changed=old!=ancestors
    return ancestors


@dataclass(frozen=True)
class PublicEvidence:
    question_heard: bool=True
    source_recognizes_context: bool=True
    deliberate_source_response: bool=True
    response_action: str='send_mantle'
    audience_sees_handover: bool=True
    independently_understood_response: bool=True
    disclaimer_words: str=''

DISCLAIMER='This is a gift, not an answer to whether I commissioned E.'

def public_assessment(e):
    # This is a stated defeasible evidential rule. No private terminal-goal field enters.
    if e.disclaimer_words==DISCLAIMER:
        return 'overt_nonendorsement_qualification'
    if e.response_action in ['send_mantle','affirmative_gesture'] and all((e.question_heard,e.source_recognizes_context,e.deliberate_source_response,
            e.audience_sees_handover,e.independently_understood_response)):
        return 'contextually_supported_acknowledgment'
    return 'unresolved_from_this_rule'


def chosen_goal_achieved(plan, uptake_blocked=False):
    values={'send_mantle':True}
    for _ in range(len(plan.selected_recipe)+1):
        for _,node in plan.selected_recipe:
            parents=[a for a,b in plan.selected_recipe if b==node]
            if all(a in values for a in parents):
                values[node]=all(values[a] for a in parents)
                if node=='audience_accepts_q' and uptake_blocked:
                    values[node]=False
    return values[plan.ultimate_goal]


def run():
    evidence=PublicEvidence()
    rows=[]
    for plan in [COMMUNICATE,COURTESY_BY_ACKNOWLEDGMENT,MATERIAL_COURTESY]:
        means=selected_means_and_end(plan)
        rows.append({'plan':asdict(plan),
          'positive_terminal_goal':plan.ultimate_goal=='audience_accepts_q',
          'positive_uptake_is_chosen_means_or_end':'audience_accepts_q' in means,
          'positive_uptake_foreseen':'audience_accepts_q' in plan.foreseen_effects,
          'public_record':asdict(evidence),'public_assessment':public_assessment(evidence)})
    assert rows[0]['positive_terminal_goal'] and rows[0]['positive_uptake_is_chosen_means_or_end']
    assert not rows[1]['positive_terminal_goal'] and rows[1]['positive_uptake_is_chosen_means_or_end']
    assert not rows[2]['positive_terminal_goal'] and not rows[2]['positive_uptake_is_chosen_means_or_end']
    assert rows[2]['positive_uptake_foreseen']
    blockade={p.name:chosen_goal_achieved(p,uptake_blocked=True)
              for p in [COMMUNICATE,COURTESY_BY_ACKNOWLEDGMENT,MATERIAL_COURTESY]}
    assert blockade=={'communicate':False,'courtesy_by_acknowledgment':False,'material_courtesy':True}
    assert all(chosen_goal_achieved(p) for p in [COMMUNICATE,COURTESY_BY_ACKNOWLEDGMENT,MATERIAL_COURTESY])
    assert len({r['public_assessment'] for r in rows})==1
    qualified=replace(evidence,disclaimer_words=DISCLAIMER)
    assert public_assessment(qualified)=='overt_nonendorsement_qualification'
    assert asdict(qualified)!=asdict(evidence)
    # The gesture result distinguishes actions, not public adoption: both answer means
    # can receive exactly the same evidential treatment when understood as responses.
    gesture=replace(evidence,response_action='affirmative_gesture')
    gesture_public_assessment=public_assessment(gesture)
    assert asdict(gesture)!=asdict(evidence)
    assert gesture_public_assessment==public_assessment(evidence)
    return {'scope':'Stipulated plan semantics and public evidence; no actual private-intention oracle.',
            'plan_controls':rows,
            'same_ultimate_courtesy_goal_can_include_or_exclude_positive_uptake_as_means':True,
            'goal_achievement_if_uptake_blocked_but_material_gift_remains':blockade,
            'all_three_share_same_public_evidence_assessment':True,
            'explicit_nonendorsement_control':{'evidence':asdict(qualified),
                 'assessment':public_assessment(qualified),'old_observations_preserved':False},
            'gesture_record':asdict(gesture),
            'gesture_public_assessment':gesture_public_assessment,
            'gesture_probe_establishes_different_public_adoption':False,
            'stable_courtesy_result_alone_establishes_genuine_nonendorsement':False}

if __name__=='__main__':print(json.dumps(run(),indent=2))
