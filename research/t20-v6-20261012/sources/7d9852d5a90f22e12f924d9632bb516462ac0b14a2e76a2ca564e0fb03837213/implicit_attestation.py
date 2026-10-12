"""Nonconventional intentional indication as a finite action/reason process.

No credential rule or source endorsement sentence is stored or evaluated. A source
plans from an information need, known recognizability and competing practical goals.
The choice/reason model and action-to-audience expectations are substantive external
assumptions; synthetic calibration never authenticates them in a real person.
"""
from dataclasses import dataclass,asdict,replace
from itertools import product
from fractions import Fraction
import json

@dataclass(frozen=True)
class Situation:
    question_heard: bool=True
    audience_waiting: bool=True
    recently_seen_source_wearing_mantle: bool=True
    repair_needed: bool=False
    carrier_cold: bool=False
    source_believes_commission: bool=True
    commission_occurred: bool=True
    episode: str='novel'

@dataclass(frozen=True)
class Policy:
    communicate: int=6
    repair: int=4
    warmth: int=4
    courtesy: int=0
    question_courtesy: int=0
    deceive: int=0
    selective_courtesy: bool=False

@dataclass(frozen=True)
class Plan:
    means: str
    action: str
    utility: int
    aim: str


def feasible_plans(p,s):
    # One unit is the effort/material cost of sending or rejecting.
    # These values are controlled planning assumptions, not inferred human psychology.
    plans=[Plan('retain personal mantle','keep',0,'retain possession')]
    demand=s.question_heard and s.audience_waiting
    recognizable=s.recently_seen_source_wearing_mantle
    communication_weight=p.communicate
    selective=p.selective_courtesy and s.episode=='novel'
    if selective:communication_weight=0
    if demand:
        if s.source_believes_commission and recognizable:
            plans.append(Plan('answer the question through a source-distinctive object',
                              'send_mantle',communication_weight-1,'audience accepts present commission claim'))
        if not s.source_believes_commission:
            plans.append(Plan('withhold the object and reject the claim by gesture',
                              'reject_claim',communication_weight-1,'audience rejects present commission claim'))
        if recognizable:
            plans.append(Plan('give a personal courtesy gift in response to social attention',
                              'send_mantle',p.question_courtesy-1,'gratify the questioner with a gift'))
            if not s.source_believes_commission:
                plans.append(Plan('induce an acknowledged false belief through the object',
                                  'send_mantle',p.deceive-1,'audience accepts present commission claim'))
            if selective:
                plans.append(Plan('special-case courtesy gift at the novel occasion',
                                  'send_mantle',7,'gratify the questioner with a gift'))
    if s.repair_needed:
        plans.append(Plan('hand the damaged mantle to the carrier for repair',
                          'send_mantle',p.repair-1,'repair the mantle'))
    if s.carrier_cold:
        plans.append(Plan('lend the mantle to protect the carrier from cold',
                          'send_mantle',p.warmth-1,'warm the carrier'))
    plans.append(Plan('give the mantle as an ordinary courtesy gift',
                      'send_mantle',p.courtesy-1,'gratify the carrier with a gift'))
    return plans


def choose(p,s):
    plans=feasible_plans(p,s);best=max(x.utility for x in plans)
    return [x for x in plans if x.utility==best]


def action(p,s):
    options={x.action for x in choose(p,s)}
    if len(options)!=1:raise ValueError('action ambiguous; retain all optimal plans')
    return next(iter(options))


def outward_events(s,selected_action,appropriation=False):
    events=[]
    if s.question_heard:events.append(('household_question_reaches_source','Did you send E with the inventory message?'))
    if s.recently_seen_source_wearing_mantle:events.append(('witnessed_recent_possession','P','personal_mantle'))
    if selected_action=='send_mantle':events += [('P_removes_mantle'),('P_hands_mantle_to_E'),('E_carries_mantle')]
    elif selected_action=='reject_claim':events += [('P_retains_mantle'),('P_rejects_claim_by_gesture')]
    else:events += [('P_retains_mantle')]
    if appropriation:events += [('E_takes_mantle_without_permission'),('E_carries_mantle')]
    return events


def execute(p,s,appropriation=False):
    plans=choose(p,s);out=action(p,s)
    # All optimal routes are retained. No convenient tie-breaking proves intention.
    intention_values={x.aim=='audience accepts present commission claim' for x in plans}
    intended=next(iter(intention_values)) if len(intention_values)==1 else None
    actual_mission_events=[('P_assigns','E','inventory')] if s.commission_occurred else []
    truth=('P_assigns','E','inventory') in actual_mission_events
    return {'action':out,'selected_plans':[asdict(x) for x in plans],
            'intended_positive_claim':intended,'commission_claim_true':truth,
            'source_voluntary_transfer':out=='send_mantle',
            'token_reaches_E':out=='send_mantle' or appropriation,
            'observed_actions':outward_events(s,out,appropriation),
            'visible_circumstances':{'repair_needed':s.repair_needed,'carrier_cold':s.carrier_cold,
                'question_heard':s.question_heard,'audience_waiting':s.audience_waiting,
                'recent_custody':s.recently_seen_source_wearing_mantle},
            'prior_credential_rules':[],'source_endorsement_utterances':[],
            'source_reason_policy':asdict(p),'situation':asdict(s)}


def positive_case():
    p=Policy();s=Situation();w=execute(p,s)
    w['communicative_goal_removed_still_sends']=action(replace(p,communicate=0),s)=='send_mantle'
    w['all_feasible_plans']=[asdict(x) for x in feasible_plans(p,s)]
    return w


def purpose_rivals():
    return {'positive':positive_case(),
            'maintenance':execute(Policy(communicate=0),Situation(repair_needed=True)),
            'courtesy':execute(Policy(communicate=0),Situation(carrier_cold=True)),
            'question_courtesy':execute(Policy(communicate=0,question_courtesy=4),Situation()),
            'appropriation':execute(Policy(communicate=0),Situation(),appropriation=True)}


def intervention_table():
    fixtures={'positive':(Policy(),Situation()),
              'maintenance':(Policy(communicate=0),Situation(repair_needed=True)),
              'courtesy':(Policy(communicate=0),Situation(carrier_cold=True)),
              'question_courtesy':(Policy(communicate=0,question_courtesy=4),Situation())}
    return {name:{'actual':action(p,s),
                  'remove_question':action(p,replace(s,question_heard=False)),
                  'remove_audience':action(p,replace(s,audience_waiting=False)),
                  'remove_practical_need':action(p,replace(s,repair_needed=False,carrier_cold=False)),
                  'remove_recognizability':action(p,replace(s,recently_seen_source_wearing_mantle=False)),
                  'known_false_claim':action(p,replace(s,source_believes_commission=False,commission_occurred=False))}
            for name,(p,s) in fixtures.items()}


def candidate_policies():
    return [Policy(*args) for args in product([0,3,6],[0,4],[0,4],[0,4],[0,4],[0,7])]


def calibration_episodes():
    # Separate hypothetical source-choice episodes, with known commission status.
    # No episode observes an intention label or establishes a token credential rule.
    return [
      (Situation(question_heard=False,episode='past-quiet'),'keep'),
      (Situation(source_believes_commission=False,commission_occurred=False,episode='past-false-claim'),'reject_claim'),
      (Situation(question_heard=False,repair_needed=True,episode='past-repair'),'send_mantle'),
      (Situation(question_heard=False,carrier_cold=True,episode='past-cold'),'send_mantle')]


def compatible(p,episodes):
    # Requiring each observed action to be predicted by every optimal plan avoids
    # selecting a favorable internal tie after observing the answer.
    return all({plan.action for plan in choose(p,s)}=={a} for s,a in episodes)


def calibration_result():
    episodes=calibration_episodes();ps=candidate_policies()
    survivors=[p for p in ps if compatible(p,episodes)]
    target=Situation()
    communicating=all(execute(p,target)['intended_positive_claim'] for p in survivors)
    mimic=replace(Policy(),selective_courtesy=True)
    same=compatible(mimic,episodes) and action(mimic,target)==action(Policy(),target)
    return {'initial_policies':len(ps),'surviving_policies':len(survivors),
            'survivors':[asdict(p) for p in survivors],
            'calibration_observations':[{'situation':asdict(s),'observed_action':a} for s,a in episodes],
            'all_regular_survivors_select_communicative_plan':communicating,
            'selective_courtesy_matches_calibration_and_target_action':same,
            'selective_courtesy_intends_positive_claim':execute(mimic,target)['intended_positive_claim'],
            'selective_courtesy_target':execute(mimic,target),
            'epistemic_status':'These are synthetic observations in a disclosed policy class. They do not authenticate actual source character or justify excluding the selective rival.'}


def false_claim_controls():
    return {'mistaken':execute(Policy(),Situation(source_believes_commission=True,commission_occurred=False)),
            'deceptive':execute(Policy(deceive=7),Situation(source_believes_commission=False,commission_occurred=False))}


def defeasible_sensitivity():
    # Once the complete observed behavior matches, Bayes cannot update relative
    # odds of the regular and selective-courtesy hypotheses from these observations.
    # p is an externally supplied post-background rival probability, not an estimate.
    return [{'supplied_selective_rival_probability':str(p),
             'conditional_purpose_probability':str(1-p),'strong_rival_retained':True,
             'likelihood_ratio_of_observed_sequence':1,'empirical_calibration':False}
            for p in [Fraction(1,1000),Fraction(1,100),Fraction(1,10),Fraction(1,2)]]


def run_all():
    return {'positive':positive_case(),'rivals':purpose_rivals(),'interventions':intervention_table(),
            'calibration':calibration_result(),'false_claims':false_claim_controls(),
            'defeasible_sensitivity':defeasible_sensitivity()}

if __name__=='__main__':print(json.dumps(run_all(),indent=2))
