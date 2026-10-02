#!/usr/bin/env python3
"""Finite interpretation controls, not metaphysical-possibility certificates.

All cognitive/practical semantics are explicitly supplied, not inferred from
program behavior. The checks test omitted implications and conditional scope.
"""
from itertools import product
import json


def determined_by(rows, keys, output):
    values = {}
    for row in rows:
        k = tuple(row[x] for x in keys)
        values.setdefault(k, set()).add(row[output])
    return all(len(v) == 1 for v in values.values())


def knows(knowledge, facts, proposition):
    assert knowledge <= facts, 'Knowledge must be factive in each interpretation'
    return proposition in knowledge


def run():
    results = []
    def check(name, claim, interpretation, boundary):
        assert claim, name
        results.append(dict(name=name, passed=True,
                            interpretation=interpretation, boundary=boundary))

    # Necessary bearer/standing nature; variable actual completed acts.
    rows = [dict(world='w0', g_exists=True, standing='G', power=('A','B'),
                 act='A', outcome='x', intentional=True),
            dict(world='w1', g_exists=True, standing='G', power=('A','B'),
                 act='B', outcome='y', intentional=True)]
    check('standing_power_does_not_fix_actuality',
          not determined_by(rows, ('standing','power'), 'outcome'),
          rows, 'Generic source essence/capacity is informationally thin')
    check('completed_act_can_determine_effect',
          determined_by(rows, ('act',), 'outcome'), rows,
          'Conditional determination does not establish cognition or actual sourcehood')
    check('necessary_source_need_not_make_this_act_necessary_in_model',
          all(r['g_exists'] for r in rows) and not all(r['act']=='A' for r in rows),
          rows, 'Formal consistency only; actual modal alternatives need warrant')

    chance = [dict(world='c0', g_exists=True, supplied_all_efficacy=True,
                   intrinsic_exercise='C', outcome='x', intention=None),
              dict(world='c1', g_exists=True, supplied_all_efficacy=True,
                   intrinsic_exercise='C', outcome='y', intention=None)]
    check('complete_efficacy_is_not_contrastive_determination',
          all(r['supplied_all_efficacy'] for r in chance)
          and not determined_by(chance, ('intrinsic_exercise',), 'outcome'),
          chance, 'A chancy source is allowed by weaker premises, not thereby proved possible')

    impersonal = dict(actual_production=True, available_power={'x'},
                      source_cognition=False, recipient_cognition=True)
    check('producing_cognition_is_not_source_knowing',
          impersonal['actual_production'] and impersonal['recipient_cognition']
          and not impersonal['source_cognition'],
          {k: sorted(v) if isinstance(v,set) else v for k,v in impersonal.items()},
          'Original-giver priority is deliberately not assumed')
    check('actual_production_does_not_give_every_alternative_power',
          'x' in impersonal['available_power'] and 'y' not in impersonal['available_power'],
          {'possible_tasks':['x','y'], 'available_power':sorted(impersonal['available_power'])},
          'Possible task domain and eligibility cannot be expanded silently')

    # A true cognitive mirror and productive power coexist without representation
    # being used in the declared explanation of the act.
    coinherence = dict(facts={'outcome_x','disposition_Q','g_exists'},
                      knowledge={'outcome_x','disposition_Q','g_exists'},
                      production_basis={'disposition_Q'}, representation_guided=False)
    check('cognition_and_power_do_not_establish_agential_integration',
          knows(coinherence['knowledge'],coinherence['facts'],'outcome_x')
          and bool(coinherence['production_basis']) and not coinherence['representation_guided'],
          {k: sorted(v) if isinstance(v,set) else v for k,v in coinherence.items()},
          'This is a typed co-instantiation control, not a consciousness simulation')

    malicious = dict(facts={'a_good','b_bad','chooses_b','b_realized'},
                     knowledge={'a_good','b_bad','chooses_b','b_realized'},
                     objective_values={'a':1,'b':-1}, chosen='b', preferred='b')
    check('finite_exhaustive_cognition_does_not_give_good_orientation',
          malicious['knowledge']==malicious['facts']
          and malicious['objective_values'][malicious['chosen']]<0,
          {k: sorted(v) if isinstance(v,set) else v for k,v in malicious.items()},
          'Practical perfection is not included in the cognition predicate')
    check('optimization_of_preference_is_not_wisdom',
          malicious['chosen']==malicious['preferred']
          and malicious['objective_values'][malicious['chosen']]<0,
          {'chosen':'b','preferred':'b','objective_values':malicious['objective_values']},
          'An independently good end and fitting means need separate warrant')

    silent = dict(knows_p=True, can_address=True, fitting_practical_orientation=True,
                  actual_address=False)
    check('disclosure_capacity_does_not_entail_actual_address',
          silent['knows_p'] and silent['can_address'] and not silent['actual_address'],
          silent, 'No actual mission or revelation is asserted')
    signal = dict(p=True, causal_indicator=True, intentional_address=False)
    check('natural_information_is_not_intentional_address',
          signal['p'] and signal['causal_indicator'] and not signal['intentional_address'],
          signal, 'Intelligibility/information do not supply communicative intent')

    testimony = dict(p=False, spectacular=True, purported_authority=True,
                     known_false=True, author_identity_established=False)
    check('spectacular_effect_does_not_authenticate_true_testimony',
          testimony['spectacular'] and testimony['purported_authority'] and not testimony['p'],
          testimony, 'No truthful-authority premise is granted')
    check('source_knowledge_does_not_entail_recipient_uptake',
          knows({'p'},{'p'},'p') and not knows(set(),{'p'},'p'),
          {'facts':['p'],'source_knowledge':['p'],'recipient_knowledge':[]},
          'Requires an actual transmission/reception warrant')

    # A finite certificate for the purely conditional truthfulness inference.
    # Correct authentication/content is a premise here, never produced by power.
    conditional_cases = 0
    for p, assertion, authenticated, truthful_in_role in product((False,True),repeat=4):
        semantic_truthfulness = not (assertion and authenticated and truthful_in_role) or p
        if semantic_truthfulness:
            conditional_cases += 1
            assert not (assertion and authenticated and truthful_in_role) or p
    check('authenticated_role_truthfulness_supports_truth_conditionally',
          conditional_cases==15, {'admissible_boolean_cases':conditional_cases},
          'The role-truthfulness condition is explicit; this is not its proof')

    # Nonidentical original roles can jointly produce; none singularly covers all.
    roots={'a','b'}
    contributions={'a':{'cognitive_condition'},'b':{'power_condition'}}
    target={'cognitive_condition','power_condition'}
    check('joint_production_does_not_imply_single_complete_bearer',
          set.union(*contributions.values())==target
          and all(contributions[r]!=target for r in roots),
          {'roots':sorted(roots), 'contributions':{k:sorted(v) for k,v in contributions.items()}},
          'Genuine original plurality is a premise-denial, not two independently complete sources')

    withholding=dict(p=True, assert_p=False, assert_not_p=False)
    check('withholding_is_not_false_attestation',
          not withholding['assert_p'] and not withholding['assert_not_p'],
          withholding, 'No moral approval of every withholding or misdirection follows')

    return {'status':'PASS_SCOPED_FINITE_INTERPRETATION_CONTROLS',
            'controls':len(results), 'certifies_metaphysical_possibility':False,
            'certifies_cognition_or_goodness':False,
            'promotes_track_t':False, 'results':results}

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
