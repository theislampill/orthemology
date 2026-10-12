"""Independent controls: stable asymmetric reasons and a new action alternative.

No episode-name branch is used. The source corrects believed false claims strongly,
while a personal social gift motivates sending on belief-true occasions. This is a
stipulated feasible policy, not a claim about the actual historical source's character.
"""
from pathlib import Path
from dataclasses import replace, asdict
from itertools import product
import importlib.util, sys, json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reviewed_implicit',HERE/'reviewed-implicit_attestation.py')
i=importlib.util.module_from_spec(spec);sys.modules[spec.name]=i;spec.loader.exec_module(i)


def stable_plans(s, affirmative_weight=0, corrective_weight=6, gesture_available=False):
    # Motives are stable across episodes. The only asymmetry is ordinary correction
    # versus affirmative communication, plus the original question-courtesy option.
    p=i.Policy(communicate=affirmative_weight, question_courtesy=4)
    plans=i.feasible_plans(p,s)
    plans=[replace(p,utility=corrective_weight-1)
           if p.action=='reject_claim' else p for p in plans]
    if gesture_available and s.question_heard and s.audience_waiting:
        # Assumption disclosed: this familiar affirmative gesture is understood in this
        # question context and has lower cost, but supplies no material/personal gift.
        if s.source_believes_commission:
            plans.append(i.Plan('answer the present question by an understood affirmative gesture',
                                'affirmative_gesture',affirmative_weight-0.5,
                                'audience accepts present commission claim'))
    return plans


def opt(plans):
    best=max(p.utility for p in plans)
    return [p for p in plans if p.utility==best]


def actions(plans):return {p.action for p in opt(plans)}
def aims(plans):return {p.aim=='audience accepts present commission claim' for p in opt(plans)}


def original_with_gesture(s):
    plans=i.feasible_plans(i.Policy(),s)
    if s.question_heard and s.audience_waiting and s.source_believes_commission:
        plans.append(i.Plan('answer the present question by an understood affirmative gesture',
                            'affirmative_gesture',6-0.5,'audience accepts present commission claim'))
    return plans


def latent_belief_control():
    episodes=i.calibration_episodes(); target=i.Situation()
    accepted=[]; checked=0; ambiguous_action_contexts=0
    for p in i.candidate_policies():
        for vals in product([False,True],repeat=7):
            ss=i.Situation(*vals)
            if len({x.action for x in i.choose(p,ss)})>1:
                ambiguous_action_contexts+=1
        for beliefs in product([False,True],repeat=5):
            checked+=1
            es=[(replace(s,source_believes_commission=b),a)
                for (s,a),b in zip(episodes,beliefs[:4])]
            ts=replace(target,source_believes_commission=beliefs[4])
            if i.compatible(p,es) and {x.action for x in i.choose(p,ts)}=={'send_mantle'}:
                assert {x.aim=='audience accepts present commission claim' for x in i.choose(p,ts)}=={True}
                accepted.append((p,beliefs))
    assert checked==3072 and len(accepted)==24
    assert len({p for p,_ in accepted})==3 and ambiguous_action_contexts==0
    return {'policy_belief_assignments_checked':checked,'accepted_assignments':len(accepted),
            'distinct_policies':len({p for p,_ in accepted}),
            'all_accepted_target_plans_have_positive_terminal_goal':True,
            'beliefs_supplied_as_hidden_alternatives_not_observations':True,
            'action_ambiguities_in_original_12288_context_grid':ambiguous_action_contexts}


def evaluate():
    equal=0; target_differences=0; action_ambiguities=0
    rows=[]
    for vals in product([False,True],repeat=7):
        s=i.Situation(*vals)
        regular=i.feasible_plans(i.Policy(),s)
        alternative=stable_plans(s)
        assert actions(regular)==actions(alternative),(s,actions(regular),actions(alternative))
        equal+=1
        if aims(regular)!=aims(alternative):target_differences+=1
        if len(actions(regular))!=1:action_ambiguities+=1
        rows.append({'situation':asdict(s),'actions':sorted(actions(regular)),
                     'regular_terminal_goal_positive':sorted(aims(regular)),
                     'stable_terminal_goal_positive':sorted(aims(alternative))})
    calibration=[]
    for s,a in i.calibration_episodes():
        assert actions(stable_plans(s))=={a}
        calibration.append({'episode':s.episode,'action':a})
    target=i.Situation()
    assert actions(stable_plans(target))==actions(i.feasible_plans(i.Policy(),target))=={'send_mantle'}
    assert aims(stable_plans(target))=={False}
    assert aims(i.feasible_plans(i.Policy(),target))=={True}
    # The added alternative actually separates these two bounded models.
    assert actions(original_with_gesture(target))=={'affirmative_gesture'}
    assert actions(stable_plans(target,gesture_available=True))=={'send_mantle'}
    # Existing compatibility routine is robust prediction rather than usual possibility
    # compatibility once the weight class is broadened to include action ties.
    tied=i.Policy(communicate=1,repair=0,warmth=0,courtesy=0)
    observed='send_mantle'
    options={p.action for p in i.choose(tied,target)}
    assert options=={'keep','send_mantle'}
    assert observed in options
    assert not i.compatible(tied,[(target,observed)])
    return {
       'scope':'Independent finite research controls; no historical attribution or closure.',
       'target_interpretation':'Terminal aim classification only. Different ultimate aims do not establish different intended intermediate effects or public adoption. See MEANS_END_RESULTS.json.',
       'stable_alternative':{'affirmative_goal_weight':0,'negative_correction_goal_weight':6,
                             'question_courtesy_weight':4,'repair_and_warmth_weights':4,
                             'episode_specific_branch':False},
       'all_existing_boolean_contexts':equal,
       'contexts_with_different_terminal_goal_classifiers':target_differences,
       'contexts_with_ambiguous_action':action_ambiguities,
       'four_calibrations_reproduced':calibration,
       'latent_belief_control':latent_belief_control(),
       'target_same_observed_handover_different_terminal_goal':True,
       'new_action_discriminator':{'assumptions':'Affirmative gesture is intelligible, available, cheaper, and not itself a personal gift.',
                                   'regular_policy':'affirmative_gesture','stable_courtesy_policy':'send_mantle'},
       'compatibility_semantics_control':{'optimal_actions':sorted(options),'observed_action':observed,
                                           'possibility_compatible':True,'author_robust_predictor_accepts':False},
       'context_rows':rows}

if __name__=='__main__':print(json.dumps(evaluate(),indent=2))
