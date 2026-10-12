"""Cross-interface controls; positive reduced-signature credit, no metaphysical certificate."""
from pathlib import Path
from dataclasses import replace
import sys,json,time
BASE=Path(__file__).resolve().parent
FRONT=BASE.parents[1]
sys.path[:0]=[str(FRONT/'intrinsic-willing/src'),str(FRONT/'provision-identity/src')]
from joint_interpretation import powerset,choose_own_activity
from intrinsic_knower import forecast_from_intrinsic_reasons,actual_execution,StandingKnowledge
from provision_semantics import IntendedAct,execute_intentions
from preservation_modes import uniform_realization,preserve


def join_with_preservation():
    commands=powerset(('e0','e1'))
    cases=[]
    for q in [x for x in commands if x]:
        a=choose_own_activity('A',q,commands)
        b=choose_own_activity('B',q,commands)
        before=forecast_from_intrinsic_reasons(q,commands)
        predicted_active=tuple(bool(before['commands'].get(g)) for g in ('A','B'))
        predicted_temporal=preserve([predicted_active]*3)
        predicted_stage_facts={(key,t,state) for key,_ in before['events'] for _,t,state in predicted_temporal['stage_facts']}
        actual=actual_execution([a,b])
        assert before==actual
        # This is a fixed standing attribute, not a created mechanism.
        K={g:StandingKnowledge(g,'K_'+g) for g in ('A','B')}
        episode_joint=uniform_realization([a,b])
        episode_solo=uniform_realization([a])
        assert episode_joint[0]==episode_solo[0]
        assert episode_joint[2]==episode_solo[2]
        assert episode_joint[1]!=episode_solo[1]
        # Each event has the same ongoing-preservation law. No event exists
        # independently before stage0; total absence later is terminal here.
        actual_active=tuple(bool(actual['commands'].get(g)) for g in ('A','B'))
        J=preserve([actual_active]*3)
        S=preserve([(True,False)]*3)
        joint_facts={(key,t,state) for key in q for _,t,state in J['stage_facts']}
        solo_facts={(key,t,state) for key in q for _,t,state in S['stage_facts']}
        assert joint_facts==solo_facts
        assert predicted_stage_facts==joint_facts
        # 'Contribution' here means actual participation in a real stage fact,
        # NOT sole entire source-owned contribution. The latter is disputed.
        a_participation={fact for fact in joint_facts if 'A' in episode_joint[1][fact[0]]}
        b_participation={fact for fact in joint_facts if 'B' in episode_joint[1][fact[0]]}
        entire={fact:tuple(g for g in ('A','B') if episode_joint[1][fact[0]]==frozenset([g])) for fact in joint_facts}
        assert not any(entire.values())
        premise_mask={
            'nonempty_real_stage_effect_participation':bool(a_participation and b_participation),
            'fixed_A_manifestation_equal_solo_facts':a_participation==solo_facts,
            'same_respect_participation_disjointness':not(a_participation & b_participation),
            'all_actual_stage_facts_retained':(a_participation|b_participation)<=joint_facts,
            'CND_held_with_no_entire_provider_at_joint_stage':all(len(owners)<=1 for owners in entire.values()),
            'participation_tokens_already_justified_as_each_sole_entire_contribution':False,
        }
        assert all(premise_mask[k] for k in ('nonempty_real_stage_effect_participation','fixed_A_manifestation_equal_solo_facts','all_actual_stage_facts_retained'))
        assert not premise_mask['same_respect_participation_disjointness']
        cases.append({'target':sorted(q),'ordinary_policy_forecast_factive':True,
                      'full_temporal_forecast_from_known_policies_factive':True,
                      'standing_knowing_tokens':{g:K[g].token for g in K},
                      'own_full_target_command_and_uniform_rule_preserved_under_suppression':True,
                      'actual_root_support_preserved':False,
                      'same_entire_created_stage_facts':True,
                      'created_stage_fact_count':len(joint_facts),
                      'trace_premise_mask':premise_mask})
    return {'cases':cases,'scope':'Same command/cognition interpreter plus supplied preservation law. Equal stage facts do not give disjoint entire-owned tokens. Frozen ordinary forecast is not claimed factive under suppression. No full temporal-original metaphysics.'}


def nonvacuity_intention_scope():
    q=frozenset(['e']);f='f'
    a=IntendedAct('A','a',q);b=IntendedAct('B','b',q)
    original=execute_intentions([a,b])
    a_f=replace(a,exact_created_target=q|{f})
    enlarged=execute_intentions([a_f,b])
    world=frozenset(e for e,_ in enlarged[0])
    assert enlarged[1][f]==frozenset(['A'])
    assert enlarged[1]['e']==frozenset(['A','B'])
    assert enlarged[3]=={'A':True,'B':False}
    # A local-scope goal WOULD tolerate unrelated f, but it is a disclosed
    # different intentional interpretation, never counted as exact-global Q.
    b_local_scope_met=(world & q)==q
    assert b_local_scope_met
    return {'A_only_f_makes_Entire_inhabited_in_same_world':True,
            'cooperative_e_still_has_no_individual_entire_provider':True,
            'B_exact_global_Q_intention_preserved':False,
            'B_positive_or_scoped_Q_intention_preserved':b_local_scope_met,
            'interpretation_change_required':'Global exact target vs local scoped target; not a defect in universal CND or in the original empty-Entire interpretation.'}


def trace_inequality_vs_growth():
    solo={0};own={0};peer={1};joint={1}
    premises={'solo_exact_own':solo==own,'peer_nonempty':bool(peer),'disjoint':not(peer&own),'peer_retained':peer<=joint}
    assert all(premises.values())
    assert joint-solo and not solo<=joint
    # Adding the prose's own-token retention gives genuine strict inclusion.
    retained_joint=own|peer
    assert solo < retained_joint
    return {'general_lemma_premises_hold':True,'joint_has_new_token':True,
            'solo_subset_joint_without_own_retention':False,
            'strict_inclusion_with_own_and_peer_retention':True,
            'scope':'Checks precise strength of displayed theorem; it does not refute its true conclusion.'}

if __name__=='__main__':
    start=time.perf_counter()
    r={'preservation_join':join_with_preservation(),'same_world_CND_intention_scope':nonvacuity_intention_scope(),'trace_lemma_scope':trace_inequality_vs_growth()}
    r['measured_execution_seconds']=time.perf_counter()-start
    (BASE/'INDEPENDENT_JOINED_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
