"""Finite semantic consistency controls, not a recipient truth oracle."""
from dataclasses import replace
import json
from independent_checks import load

o=load('occurrence_model');m=load('continuation_model')
w=m.World(0);child=w.migrate(w.tokens[0],'inverse',m.resources(m.ROOTS));e=child.identity
claim=o.Occurrence('positive-owned',o.Context(w.bearer(e),'Operator',1,'lab'),'Assert',('duty','you','inspect','now',2))
rule=o.Attestation('rule-event','Principal',w.bearer(e),'service-duty',1,3,office_history=w)
trusted={rule.rule_event:rule}
owner=o.prospective_owner(claim,rule,trusted,w,e)
assert owner=='Principal'
p=o.resolve(claim.formula,claim.context)
valuation={p}
assert o.truth(p,valuation)
neg=replace(claim,event='contradictory-owned',formula=('not',claim.formula))
assert o.prospective_owner(neg,rule,trusted,w,e)=='Principal'
q=o.resolve(neg.formula,neg.context)
assert not o.truth(q,valuation)
# Veracity is a semantic property of owned in-domain actual reports, not its label.
def finite_scoped_veracity(actual_occurrences):
    return all(o.truth(o.resolve(c.formula,c.context),valuation) for c in actual_occurrences
               if c.domain=='service-duty' and o.prospective_owner(c,rule,trusted,w,e)=='Principal')
assert finite_scoped_veracity([claim])
assert not finite_scoped_veracity([neg])
assert not finite_scoped_veracity([claim,neg])
# Without a warranted scoped veracity premise, authenticated ownership alone
# is not an admissible instance of the special-source warrant API.
premises=o.RecipientPremises({neg.event:neg},frozenset())
assert o.warranted(neg,o.relay(neg),premises,rule,trusted,w,e) is None
print(json.dumps({'positive_history_has_satisfying_truth_valuation':True,
 'valid_role_and_adoption_can_own_false_report':True,
 'false_owned_report_falsifies_scoped_veracity':True,
 'opposite_owned_assertions_cannot_both_satisfy_scoped_veracity':True,
 'ownership_without_veracity_does_not_yield_testimonial_warrant':True,
 'limit':'The recipient is not asked to know the valuation or re-prove the duty; the valuation independently explains consistency and failure of the semantic veracity premise.'},indent=2))
