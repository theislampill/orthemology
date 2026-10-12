#!/usr/bin/env python3
"""Small actual-run API controls. No parser/frontend or universal proof credit."""
from pathlib import Path
import hashlib,importlib.util,json,sys
if sys.flags.optimize:raise RuntimeError('Optimized controls refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'milestones/P1_v3/source/prcodec.py'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
spec=importlib.util.spec_from_file_location('p2_pinned_codec',SOURCE);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
C,V,E,S,Q,L,I=c.C,c.V,c.E,c.Set,c.Seq,c.Loop,c.If
fixtures=[
 ('empty',c.Program(0,0,Q()),[],(0,1,[]),None),
 ('singleton',c.Program(0,2,Q(S(2,C(0)))),[],(0,3,[(2,0)]),None),
 ('sequence_updates',c.Program(0,0,Q(S(0,C(4)),S(0,E('add',V(0),C(1))))),[],(5,8,[(0,4),(0,5)]),None),
 ('zero_loop',c.Program(0,0,L(0,C(0),Q())),[],(0,3,[]),None),
 ('three_empty_iterations',c.Program(0,0,L(0,C(3),Q())),[],(2,9,[]),None),
 ('body_overwrites_loop_register',c.Program(0,0,L(0,C(2),S(0,C(99)))),[],(99,9,[(0,99),(0,99)]),None),
 ('captured_bound',c.Program(1,1,Q(S(1,C(0)),L(2,V(0),Q(S(0,C(0)),S(1,E('add',V(1),C(1))))))),[3],(3,33,[(1,0),(0,0),(1,1),(0,0),(1,2),(0,0),(1,3)]),None),
 ('nonzero_branch',c.Program(1,0,I(V(0),Q(),S(0,C(0)))),[17],(17,3,[]),0),
 ('zero_branch',c.Program(1,0,I(V(0),S(0,C(99)),S(0,C(5)))),[0],(5,4,[(0,5)]),None),
 ('nested_loops',c.Program(0,3,Q(S(3,C(0)),L(0,C(2),L(1,C(2),S(3,E('add',V(3),C(1))))))),[],(4,38,[(3,0),(3,1),(3,2),(3,3),(3,4)]),None),
 ('unchecked_input_output',c.Program(1,0,Q()),[2**100],(2**100,1,[]),0),
 ('unchecked_loop_index',c.Program(1,1,L(1,V(0),Q())),[3],(2,9,[]),0),
]
results=[]
for name,p,args,expected,bits in fixtures:
 actual=c.run(p,args,step_limit=expected[1],max_bits=bits,trace=True)
 assert actual==expected,(name,actual,expected)
 assert c.run(p,args,step_limit=expected[1],max_bits=bits)==expected[0]
 results.append({'name':name,'value':actual[0],'steps':actual[1],'events':actual[2],'max_bits':bits})
failures=[
 ('empty_step_failure',c.Program(0,0,Q()),[],0,None,'Step limit; no semantic value returned'),
 ('final_repeat_tick',c.Program(0,0,L(0,C(0),Q())),[],2,None,'Step limit; no semantic value returned'),
 ('set_power_precheck',c.Program(0,0,S(0,E('pow2',C(3)))),[],None,3,'Exponent storage bound'),
 ('ready_tick_wins',c.Program(0,0,S(0,E('pow2',C(3)))),[],3,3,'Step limit; no semantic value returned'),
 ('set_binary_width',c.Program(0,0,S(0,E('add',C(7),C(1)))),[],None,3,'Integer storage bound'),
 ('branch_condition_width',c.Program(0,0,I(C(8),Q(),Q())),[],None,3,'Integer storage bound'),
 ('loop_bound_width',c.Program(0,0,L(0,C(8),Q())),[],None,3,'Integer storage bound'),
]
for name,p,args,limit,bits,message in failures:
 try:c.run(p,args,step_limit=limit,max_bits=bits,trace=True)
 except c.ResourceLimit as e:assert str(e)==message,(name,str(e));results.append({'name':name,'error':'ResourceLimit','message':str(e),'failure_steps_publicly_exposed':False})
 else:raise AssertionError((name,'Expected source failure'))
try:c.run(c.Program(1,0,Q()),[],step_limit=0)
except ValueError as e:assert str(e)=='Arity mismatch';results.append({'name':'arity_before_meter','error':'ValueError','message':str(e)})
else:raise AssertionError('Arity error missing')

def expr(e):
 if e[0]=='c':return f'(.constant {e[1]})'
 if e[0]=='v':return f'(.reg {e[1]})'
 if e[0]=='pow2':return f'(.pow2 {expr(e[1])})'
 return f'(.binary .{e[0]} {expr(e[1])} {expr(e[2])})'
def cmds(ss):return '.nil' if not ss else f'(.cons {stmt(ss[0])} {cmds(ss[1:])})'
def stmt(s):
 if s[0]=='set':return f'(.set {s[1]} {expr(s[2])})'
 if s[0]=='seq':return f'(.seq {cmds(s[1:])})'
 if s[0]=='loop':return f'(.loop {s[1]} {expr(s[2])} {stmt(s[3])})'
 return f'(.branch {expr(s[1])} {stmt(s[2])} {stmt(s[3])})'
lines=['import PythonRunnerAPI','open P02.PythonExpr P02.PythonRunner','namespace RunnerAuthorControls']
for name,p,args,(v,steps,events),bits in fixtures:
 ps=f'⟨{p.arity},{p.output},{stmt(p.body)}⟩';arg='['+','.join(map(str,args))+']';es='['+','.join(f'({r},{v})' for r,v in events)+']';b='none' if bits is None else f'(some {bits})'
 lines.append(f'def {name} : Program := {ps}')
 lines.append(f'example : callFuel true 80 {name} {arg} (some {steps}) {b} = .ok (some (.traced {v} {steps} {es})) := by rfl')
 lines.append(f'example : callFuel false 80 {name} {arg} (some {steps}) {b} = .ok (some (.value {v})) := by rfl')
lines.append('end RunnerAuthorControls')
(ROOT/'controls/P2Controls.lean').write_text('\n'.join(lines)+'\n')
print(json.dumps({'status':'PASS_BOUNDED_RUNNER_API_CONTROLS','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'success_programs':len(fixtures),'trace_true_false_calls':2*len(fixtures),'source_failures':len(failures),'arity_controls':1,'cases':results,'universal_credit':False,'parser_run':False},indent=2))
