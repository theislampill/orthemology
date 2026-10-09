"""Finite coherence check, not an analysis or simulation of knowledge.

Six fixed independent propositions. The source observes their values, reports
P0 truthfully, and reports the negation of the truth on each of P1..P5.
The recipient accepts each answer as given, using the same general procedure.
No variable means warrant, knowledge, competent inference, or proper function.
"""
from itertools import product
from pathlib import Path
import json

worlds=list(product((False,True), repeat=6))

def source(w):
    return (w[0],)+tuple(not bit for bit in w[1:])

def recipient(message):
    return tuple(message)

rows=[]
for w in worlds:
    m=source(w); b=recipient(m)
    rows.append({"valuation":list(w),"asserted_polarities":list(m),
                 "recipient_polarities":list(b),
                 "correct_components":sum(x==y for x,y in zip(w,m)),
                 "asserts_P0":m[0],"whole_report_true":all(x==y for x,y in zip(w,m))})
    assert m[0]==w[0]
    assert sum(x==y for x,y in zip(w,m))==1
    assert not all(x==y for x,y in zip(w,m))
    assert b==m

# E is the fixed assertion event 'the source asserts P0', not a varying true answer.
not_p=[row for row in rows if not row['valuation'][0]]
p=[row for row in rows if row['valuation'][0]]
assert len(not_p)==len(p)==32
assert all(not row['asserts_P0'] for row in not_p)
assert all(row['asserts_P0'] for row in p)
# Pair each p-world with its sole P0-flipped counterpart, keeping five other facts.
assert all(source((not w[0],)+w[1:])[0]!=source(w)[0] for w in worlds)
# The entire observed assertion sequence also differs in every false-target world.
actual=(True,True,True,True,True,True)
actual_message=source(actual)
full_message_false_target_matches=sum(source(w)==actual_message for w in worlds if not w[0])
assert full_message_false_target_matches==0
# No privileged 'this is the truthful component' marker is sent to the recipient.
assert all(len(source(w))==6 for w in worlds)

# Negative transport control: a target true at all admitted worlds gives no false-target cases.
necessary_target_rows=[{'target':True,'blind_assent':True,'other_facts':list(w[1:])} for w in worlds[:32]]
necessary_false_target=[r for r in necessary_target_rows if not r['target']]
assert len(necessary_false_target)==0

result={
 'scope':'Coherence of specified source policy and recipient response; no epistemic status assigned',
 'worlds':len(worlds), 'fixed_propositions':6,
 'true_components_per_report':1,'false_components_per_report':5,
 'whole_conjunction_true_count':sum(r['whole_report_true'] for r in rows),
 'false_target_worlds':len(not_p),'E_present_in_false_target_worlds':sum(r['asserts_P0'] for r in not_p),
 'true_target_worlds':len(p),'E_present_in_true_target_worlds':sum(r['asserts_P0'] for r in p),
 'local_channel_globally_sensitive':'E iff P0 throughout stipulated 64-world domain',
 'whole_source_fully_truthful':False,
 'actual_world':list(actual),'actual_message':list(actual_message),
 'complete_actual_message_matches_in_false_target_worlds':full_message_false_target_matches,
 'recipient_knows_reliability': 'Not modelled or assumed',
 'recipient_knows_P0':'Not modelled or concluded',
 'counterfactual_qualification':'Within this stipulated domain any selection of false-P0 worlds lacks E; actual modal domain not established',
 'necessary_target_false_world_count':len(necessary_false_target),
 'necessary_target_transport':'FAIL: no false-target contrast. Constant assent passes the vacuous screen as readily as a competent route.',
 'rows':rows}
Path(__file__).with_name('MODEL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
