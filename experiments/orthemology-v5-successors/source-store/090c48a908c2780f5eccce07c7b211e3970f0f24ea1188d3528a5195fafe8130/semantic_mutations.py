"""Executed semantic mutation controls; no source files are modified.

These are explicit wrong-interface/algorithm variants, not a claim of compiler
mutation coverage or a comparison with the strongest conventional baseline.
"""
from context_effects import Origin,Effect,Ref,Invalid,compile_effect,compose,apply_effect,resolve_demands
from read_cover import Window,cover_dp,interval_cover,role_decision,minimax_cost,star_locality,coverage_sufficiency
from fractions import Fraction as F
from itertools import product
from math import inf,ceil
from dataclasses import replace
from pathlib import Path
import json
A,B,C=[Origin('model',x) for x in 'abc']
w=lambda n,s,c=1,**kw:Window(n,frozenset(s),F(c),**kw)
rows=[]
def record(name,correct,bad,mechanism):
    assert correct!=bad,(name,correct,bad)
    rows.append({'id':name,'status':'KILLED','correct':repr(correct),'mutant':repr(bad),'mechanism':mechanism})
def obs(x,win):return tuple((k,x[k]) for k in sorted(win.coverage))

# A current-state summary misses restored contexts.
e=compile_effect([('enter',B),('leave',),('emit','t')])
record('M01_CURRENT_TOP_ONLY',apply_effect(e,[A])[1],(('t',B),),'ignore scope restoration')
# Keep the mutant well-formed while changing its meaning.
e=compile_effect([('leave',),('enter',B)])
bad=Effect(1,(B,),0,())
try:correct=apply_effect(e,[A])
except Invalid:correct='rejected'
record('M02_NET_HEIGHT_ONLY',correct,apply_effect(bad,[A]),'erase consumed incoming frame and prefix underflow')
# Drop the exact binding precondition, but preserve legal depth.
e=compile_effect([('exit',A)])
try:correct=apply_effect(e,[B,C])
except Invalid:correct='rejected'
record('M03_DROP_KEYED_EXIT',correct,apply_effect(Effect(e.depth,e.prefix,e.consumed,e.emissions),[B,C]),'omit source-origin equality')
# Count copies or collapse different originals.
copied_origins=[A,A]
record('M04_COPY_AS_NEW_ROOT',len(set(copied_origins)),len(copied_origins),'count carrier occurrences as independent original dependencies')
record('M05_SAME_TEXT_COLLAPSE',role_decision({A,B},{A:True}),role_decision({A},{A:True}),'drop unresolved different-origin occurrence because text matches')
menu=[w('wide',[A,B],100),w('a',[A]),w('b',[B])]
bad_greedy=max((win for win in menu if A in win.coverage),key=lambda win:len(win.coverage)).cost
record('M06_WEIGHTED_FURTHEST_RIGHT',interval_cover([A,B],[A,B],menu).cost,bad_greedy,'apply unit-cost greedy rule to unequal weights')
menu=[w('ac',[A,C]),w('b',[B])]
order=[A,B,C]
bad_menu=[replace(win,coverage=frozenset(order[min(order.index(k) for k in win.coverage):max(order.index(k) for k in win.coverage)+1])) for win in menu]
record('M07_FILL_RAW_INTERVAL_HOLE',cover_dp([A,B,C],menu).cost,cover_dp([A,B,C],bad_menu).cost,'pretend nonconvex adequate-role coverage contains middle key')
blocked=[w('a',[A],eligible=False)]
record('M08_ADDRESS_IMPLIES_QUERY_RIGHT',cover_dp([A],blocked).cost,cover_dp([A],[replace(win,eligible=True) for win in blocked]).cost,'ignore successor eligibility')
answer=role_decision({A,B},{})
record('M09_SOUND_ABSTENTION_IS_COMPLETION',type(answer) is bool,answer is None or type(answer) is bool,'incorrect completion guard accepts an always-unresolved policy')
# An uncounted response channel can beat bare-cover arithmetic.
worlds=tuple(dict(zip([A,B],bits)) for bits in product((0,1),repeat=2))
menu=[w('a',[A])];rich=lambda x,_:(x[A],x[B])
weak_independence=len({(x[A],x[B]) for x in worlds})==4
record('M10_MARGINALS_IMPLY_LOCALITY',star_locality(worlds,[A,B],menu,rich),weak_independence,'ignore richer response field disclosing b')
# A positive snapshot signature is not enough when response reveals no values.
constant=lambda _x,_w:'constant';menu=[w('all',[A,B])]
record('M11_LOCALITY_IMPLIES_ADEQUACY',coverage_sufficiency(worlds,menu,constant),star_locality(worlds,[A,B],menu,constant),'all-key locality is vacuous; response may be uninformative')
record_with_scope={'local_speaker':'author','document_author':'author','global_role':False}
record('M12_LOCAL_SPEAKER_IS_GLOBAL_ROLE',role_decision({A},{A:record_with_scope['global_role']}),record_with_scope['local_speaker']==record_with_scope['document_author'],'author name inside an enclosing source quotation')
cards=[w('ab',[A,B]),w('bc',[B,C])]
count_heuristic=ceil(len({A,C})/max(len(win.coverage) for win in cards))
record('M13_RETAINED_COUNT_ONLY',cover_dp([A,C],cards).cost,F(count_heuristic),'treat carrying middle b as equivalent to carrying edge a')
worlds3=tuple(dict(zip([A,B,C],bits)) for bits in product((0,1),repeat=3));target=lambda x:all(x.values())
signal=lambda x:A if target(x) else B
record('M14_HIDE_SELECTOR_CHANNEL',minimax_cost(worlds3,cards,target,obs,metadata=signal),cover_dp([A,B,C],cards).cost,'ignore an agreed label-dependent retained-origin code')
record('M15_DISCARD_WHOLE_SOURCE_ALTERNATIVE',cover_dp([A,B,C],cards+[w('whole',[A,B,C])]).cost,cover_dp([A,B,C],cards).cost,'artificially omit a genuinely available read')
packet={'original_role':True,'current_force':'report'}
bad_force='assertion' if packet['original_role'] else packet['current_force']
record('M16_PROMOTE_SOURCE_FORCE_TO_CARRIER',packet['current_force'],bad_force,'copy original-author role into current quotation force')
result={'status':'PASS','semantic_mutants':len(rows),'killed':len(rows),'results':rows,'scope':'Explicit faulty semantic/algorithm alternatives; not production/compiler mutation coverage.'}
Path('logs/semantic_mutations.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
