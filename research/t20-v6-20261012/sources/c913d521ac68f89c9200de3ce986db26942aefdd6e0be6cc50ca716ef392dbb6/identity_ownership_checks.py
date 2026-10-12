"""Whole-occurrence/rule and actual endpoint controls, independently authored."""
from dataclasses import replace
from itertools import product
import json
from independent_checks import load, WORDS

o=load('occurrence_model');m=load('continuation_model');full=m.resources(m.ROOTS)
w=m.World(1);parent=w.tokens[0];child=w.migrate(parent,'inverse',full);endpoint=child.identity
claim=o.Occurrence('new-report',o.Context(w.bearer(endpoint),'Operator',1,'lab'),'Assert',('duty','you','inspect','now',2))
rule=o.Attestation('authenticated-rule','Principal',w.bearer(endpoint),'service-duty',1,3,office_history=w)
trusted_rules={rule.rule_event:rule}
other_world=m.World(1);other_child=other_world.migrate(other_world.tokens[0],'inverse',full)
assert o.prospective_owner(claim,rule,trusted_rules,other_world,other_child.identity) is None
premises=o.RecipientPremises({claim.event:claim},frozenset({('Principal','service-duty')}))
assert o.warranted(claim,o.relay(claim),premises,rule,trusted_rules,w,endpoint)==('duty','Operator','inspect',1,3)
assert o.warranted(claim,o.relay(claim),premises) is None
rule_changes={'owner':'Counterfeit','carrier':'Other','domain':'finance','start':0,'end':99,'force':'Quote'}
for key,value in rule_changes.items():
    assert o.prospective_owner(claim,replace(rule,**{key:value}),trusted_rules,w,endpoint) is None
altered_occurrences=[replace(claim,force='Quote'),replace(claim,domain='finance'),
                     replace(claim,formula=('duty','you','transfer','now',2))]
for key,value in [('speaker','Principal'),('addressee','Other'),('time',2),('place','archive')]:
    altered_occurrences.append(replace(claim,context=replace(claim.context,**{key:value})))
for changed in altered_occurrences:
    assert o.warranted(changed,o.relay(changed),premises,rule,trusted_rules,w,endpoint) is None
# The actual same appointed endpoint remains in office during an outage.
assert w.is_current_successor(endpoint)
try: w.step(child,'read',m.resources({'archive'}))
except m.Unavailable: pass
else: raise AssertionError('Archive-only service unexpectedly available')
assert w.is_current_successor(endpoint)
assert w.step(child,'read',full)==('value',1)
# Same-ID counterfeit parent and operator cannot borrow the registry entry.
for token in [parent,child]:
    fake=m.Token(token.identity,token.encoding,0)
    for operation in [lambda:w.read_state(fake,full),lambda:w.step(fake,'read',full),lambda:w.migrate(fake,'direct',full)]:
        try: operation()
        except m.Unavailable: pass
        else: raise AssertionError('Unregistered endpoint was accepted')
# Exact observed data and full finite service can agree without constructor lineage.
history_pairs=0
for initial,encoding,first,second in product((0,1),('direct','inverse'),WORDS,WORDS):
    a,b=m.World(initial),m.World(initial)
    actual=a.migrate(a.tokens[0],encoding,full)
    twin=b.independent_twin(initial,encoding)
    assert a.read_state(actual,full)==b.read_state(twin,full)
    assert a.is_current_successor(actual.identity) and not b.is_current_successor(twin.identity)
    for request in first:
        assert a.step(actual,request,full)==b.step(twin,request,full)
    other='direct' if encoding=='inverse' else 'inverse'
    ac=a.migrate(actual,other,full);bc=b.migrate(twin,other,full)
    for request in second:
        assert a.step(ac,request,full)==b.step(bc,request,full)
    assert a.is_current_successor(ac.identity) and not b.is_current_successor(bc.identity)
    history_pairs+=1
# Already reported direct-source historical duty survives current-role retirement.
old=o.Occurrence('original-duty',o.Context('Principal','Operator',0,'lab'),'Assert',('duty','you','inspect','now',2))
op=o.RecipientPremises({old.event:old},frozenset({('Principal','service-duty')}))
grandchild=w.migrate(child,'direct',full)
assert not w.is_current_successor(endpoint)
assert o.warranted(claim,o.relay(claim),premises,rule,trusted_rules,w,endpoint) is None
assert o.warranted(old,o.relay(old),op)==('duty','Operator','inspect',0,2)
print(json.dumps({'positive_integrated_attestation':True,'same_named_other_office_rejected':True,'changed_same_id_rules_rejected':len(rule_changes),
 'changed_same_id_occurrences_rejected':len(altered_occurrences),'same_endpoint_outage_and_recovery':True,
 'counterfeit_endpoint_operations_rejected':6,'observational_twin_two_phase_pairs':history_pairs,
 'retired_role_blocks_new_attestation_preserves_old_duty':True},indent=2))
