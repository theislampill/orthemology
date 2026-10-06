#!/usr/bin/env python3
"""Small exact-source edge controls. These are corroboration, not theorem evidence."""
from pathlib import Path
import hashlib,importlib.util,json,sys
if sys.flags.optimize: raise RuntimeError("Optimized verification is refused")
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source/prcodec.py'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
spec=importlib.util.spec_from_file_location('p1_pinned_codec',SOURCE)
c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
cases=[]
def check(name,e,regs,limit,bits,start,expected,steps,error=None):
    meter=c.Meter(limit,bits,start)
    try:
        v=c.eval_expr(e,regs,meter)
        assert error is None,(name,'unexpected success',v)
        assert type(v) is int and v==expected,(name,v,expected)
        observed={'value':v}
    except c.ResourceLimit as exc:
        assert error is not None and str(exc)==error,(name,str(exc),error)
        observed={'error':'ResourceLimit','message':str(exc)}
    assert meter.steps==steps,(name,meter.steps,steps)
    cases.append({'name':name,'steps':steps,**observed})
C=lambda n:('c',n)
B=lambda op,a,b:(op,C(a),C(b))
for op,a,b,v in [('add',2,3,5),('sub',2,5,0),('mul',3,4,12),('div',7,2,3),('div',9,0,0),('mod',9,4,1),('mod',9,0,9),('le',5,2,0),('le',2,5,1),('eq',2,2,1),('eq',2,3,0)]:
    check(f'{op}_{a}_{b}',B(op,a,b),{},None,None,0,v,4)
check('missing_register',('v',99),{},1,0,0,0,1)
check('unchecked_register_width',('v',0),{0:2**100},1,0,0,2**100,1)
check('tick_before_constant_check',C(8),{},0,0,0,None,1,'Step limit; no semantic value returned')
check('constant_storage_failure',C(8),{},None,3,0,None,1,'Integer storage bound')
check('power_precheck_failure',('pow2',C(3)),{},None,3,0,None,3,'Exponent storage bound')
check('ready_tick_before_power_check',('pow2',C(3)),{},2,3,0,None,3,'Step limit; no semantic value returned')
check('power_exact_budget',('pow2',C(3)),{},3,4,0,8,3)
check('left_error_before_right_visit',B('add',8,0),{},None,3,0,None,2,'Integer storage bound')
check('shared_start_success',B('add',2,3),{},11,None,7,5,11)
check('shared_start_failure',B('add',2,3),{},10,None,7,None,11,'Step limit; no semantic value returned')
check('nested_expression',('add',('pow2',C(3)),B('sub',9,4)),{},None,None,0,13,9)
# These observations delimit the unproved direct-AST/host API endpoint.
try:c.run(c.Program(1,0,c.Seq()),[True])
except ValueError:cases.append({'name':'boolean_argument_refused','error':'ValueError'})
else:raise AssertionError('Boolean argument accepted')
assert c.run(c.Program(0,0,('set',0,('c',-1))),[])==-1
cases.append({'name':'raw_negative_constant_outside_domain','value':-1})
assert c.run(c.Program(0,0,('set',0,('c',True))),[]) is True
cases.append({'name':'raw_boolean_constant_outside_domain','value':True})
assert c.run(c.Program(1,0,c.Seq()),[2**100],max_bits=0)==2**100
cases.append({'name':'run_does_not_bound_input_or_output_width','value':2**100})
print(json.dumps({'status':'PASS_BOUNDED_PYTHON_EDGE_CONTROLS','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'cases':cases,'case_count':len(cases),'universal_semantic_credit':False,'whole_program_replay_attempted':False},indent=2))
