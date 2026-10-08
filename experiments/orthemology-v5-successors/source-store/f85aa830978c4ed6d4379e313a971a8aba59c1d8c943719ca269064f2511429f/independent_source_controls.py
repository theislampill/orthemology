#!/usr/bin/env python3
"""Independent finite corroboration of the exact Python expression slice.
Not a frontend proof. Mutants execute only in fresh in-memory modules.
"""
import ast, collections, copy, datetime, hashlib, itertools, json, pathlib, random, sys, types
R=pathlib.Path(__file__).resolve().parents[1]
W=R.parents[2]
SRC=W/'tranche9/baseline/components/Eighth_Literal_Runtime_Counterexamples_20261002/prcodec.py'
COPY=W/'tranche9/baseline/components/Semantic_Control_Independent_Review_20261002/literal-snapshot/prcodec.py'
PIN='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
sha=lambda b:hashlib.sha256(b).hexdigest()
source=SRC.read_text()
assert sha(SRC.read_bytes())==PIN==sha(COPY.read_bytes())
assert not sys.flags.optimize

def module(text, name):
    m=types.ModuleType(name);sys.modules[name]=m
    exec(compile(text,str(SRC),'exec'),m.__dict__)
    return m
actual=module(source,'review_literal_prcodec')

class Stop(Exception):
    def __init__(self,reason):self.reason=reason

def ref(e,d,limit,bits,start):
    count=start
    def tick():
        nonlocal count
        count+=1
        if limit is not None and count>limit:raise Stop('Step limit; no semantic value returned')
    def check(v):
        if bits is not None and v.bit_length()>bits:raise Stop('Integer storage bound')
        return v
    def walk(t):
        tick();k=t[0]
        if k=='c':return check(t[1])
        if k=='v':return d.get(t[1],0)
        a=walk(t[1])
        if k=='pow2':
            tick()
            if bits is not None and a>=bits:raise Stop('Exponent storage bound')
            return 2**a
        b=walk(t[2]);tick()
        if k=='add':v=a+b
        elif k=='sub':v=0 if a<b else a-b
        elif k=='mul':v=a*b
        elif k=='div':v=0 if b==0 else a//b
        elif k=='mod':v=a if b==0 else a%b
        elif k=='le':v=1 if a<=b else 0
        elif k=='eq':v=1 if a==b else 0
        else:raise AssertionError(k)
        return check(v)
    try:return ('ok',walk(e),count)
    except Stop as ex:return ('err','ResourceLimit',ex.reason,count)

def call(m,e,d,limit,bits,start):
    meter=m.Meter(limit,bits,start)
    try:return ('ok',m.eval_expr(e,dict(d),meter),meter.steps)
    except Exception as ex:return ('err',type(ex).__name__,str(ex),meter.steps)

def cost(e):return 1 if e[0] in ('c','v') else 2+sum(map(cost,e[1:]))

leaves=[('c',n) for n in [0,1,2,3,7,8,15]]+[('v',r) for r in [0,1,2,99]]
ops=['add','sub','mul','div','mod','le','eq']
exprs=list(leaves)+[('pow2',e) for e in leaves]
exprs += [(op,a,b) for op,a,b in itertools.product(ops,leaves,leaves)]
rng=random.Random(908142)
for _ in range(120):
    a,b=rng.sample(leaves,2)
    inner=(rng.choice(ops),a,b)
    exprs.append((rng.choice(ops),inner,rng.choice(leaves)))
    exprs.append((rng.choice(ops),rng.choice(leaves),inner))
    exprs.append(('pow2',('mod',inner,('c',9))))
# Child-order faults and asymmetric operations.
exprs += [('add',('pow2',('v',1)),('c',256)),('sub',('c',8),('c',3)),
          ('div',('v',1),('c',0)),('mod',('v',1),('c',0)),
          ('pow2',('pow2',('c',3))),('add',('c',0),('v',1))]
stores=[{}, {0:0,1:9,2:257}, {0:11,1:256,2:0}]
records=[];counts=collections.Counter();cases=[]
for e,d,start in itertools.product(exprs,stores,[0,5]):
    ticks=cost(e)
    for lim,bits in itertools.product([None,0,start,start+1,start+ticks-1,start+ticks], [None,0,1,3,8,9]):
        case=(e,d,lim,bits,start)
        want=ref(*case);got=call(actual,*case)
        assert got==want,(case,want,got)
        counts[got[0] if got[0]=='ok' else got[2]]+=1
        cases.append(case)

# Directly observe which source lines execute, using representative branch grid.
seen=set()
def trace(frame,event,arg):
    if event=='line' and frame.f_code.co_filename==str(SRC):seen.add(frame.f_lineno)
    return trace
sys.settrace(trace)
for op in ops:
    for a,b in [(3,0),(0,3),(3,3),(8,2)]:
        for lim,bits in [(None,None),(0,None),(None,0),(3,10)]:call(actual,(op,('c',a),('c',b)),{},lim,bits,0)
for e in [('c',0),('v',99),('pow2',('c',0)),('pow2',('v',0))]:
    for lim,bits in [(None,None),(0,0),(None,0),(None,1)]:call(actual,e,{0:9},lim,bits,0)
sys.settrace(None)
# All executable lines reachable on the admitted expression domain are visited.
# Unknown-operation raise 156 is excluded by the well-formedness contract;
# final invariant-failure branch 158 is unreachable on valid inputs, while its
# test and successful exit are exercised.
required_lines={128,129,131,132,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,157,158,159}
assert seen==required_lines,(sorted(required_lines-seen),sorted(seen-required_lines))

# Instrument only entry/final boundary and fixed pop count. The original body is
# otherwise byte-for-byte translated by the Python AST compiler.
tree=ast.parse(source)
fun=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='eval_expr'))
fun.name='seeded_expr';fun.args.args += [ast.arg(arg='tail'),ast.arg(arg='values'),ast.arg(arg='pops')]
fun.body[:2]=ast.parse('stack=list(tail)+[(e,False)]; vals=list(values)').body
loop=next(n for n in fun.body if isinstance(n,ast.While))
loop.test=ast.parse('pops > 0 and stack',mode='eval').body
loop.body.insert(0,ast.parse('pops -= 1').body[0])
loopidx=fun.body.index(loop)
fun.body=fun.body[:loopidx+1]+ast.parse('return stack, vals, meter.steps, pops').body
new=ast.fix_missing_locations(ast.Module(body=[fun],type_ignores=[]))
exec(compile(new,'<review-seeded-boundary>','exec'),actual.__dict__)
seeded=0
for e,d in itertools.product(exprs[::7],stores):
    want=ref(e,d,None,None,13)
    for tail,vs in [([],[]),([(('c',77),False)],[999,0,3]),
                    ([(('sub',('c',9),('c',4)),True),(('pow2',('v',2)),False)],[1,2])]:
        m=actual.Meter(None,None,13)
        got=actual.seeded_expr(e,dict(d),m,tail,vs,cost(e))
        assert got==(tail,vs+[want[1]],want[2],0),(e,got)
        seeded+=1

# Source-sensitive counterfactual controls, each with a fixed witness.
mutations=[
 ('operand_order','b=vals.pop();a=vals.pop()','a=vals.pop();b=vals.pop()',(('sub',('c',8),('c',3)),{},None,None,0)),
 ('child_order','reversed(t[1:])','t[1:]',(('div',('c',8),('c',2)),{},None,None,0)),
 ('skipped_ready_tick','t,ready=stack.pop();meter.tick();k=t[0]','t,ready=stack.pop();k=t[0]\n        if not ready:meter.tick()',(('add',('c',1),('c',2)),{},3,None,0)),
 ('checked_variable','vals.append(regs.get(t[1],0))','vals.append(meter.check(regs.get(t[1],0)))',(('v',1),{1:256},None,0,0)),
 ('wrong_default','regs.get(t[1],0)','regs.get(t[1],1)',(('v',99),{},None,None,0)),
 ('strict_step_boundary','self.steps>self.limit','self.steps>=self.limit',(('c',0),{},1,0,0)),
 ('strict_bits_boundary','x.bit_length()>self.max_bits','x.bit_length()>=self.max_bits',(('c',0),{},None,0,0)),
 ('offbyone_power','a+1>meter.max_bits','a>meter.max_bits',(('pow2',('c',1)),{},None,1,0)),
 ('wrong_power_fault',"ResourceLimit('Exponent storage bound')","ResourceLimit('Integer storage bound')",(('pow2',('v',1)),{1:9},None,1,0)),
 ('unchecked_constant','vals.append(meter.check(t[1]))','vals.append(t[1])',(('c',8),{},None,3,0)),
 ('unchecked_arithmetic','vals.append(meter.check(v))','vals.append(v)',(('mul',('v',0),('v',1)),{0:8,1:8},None,3,0)),
 ('wrong_div_zero','v=a//b if b else 0','v=a//b if b else a',(('div',('c',3),('c',0)),{},None,None,0)),
 ('wrong_mod_zero','v=a%b if b else a','v=a%b if b else 0',(('mod',('c',3),('c',0)),{},None,None,0)),
 ('unsaturated_sub','v=max(0,a-b)','v=a-b',(('sub',('c',1),('c',2)),{},None,None,0)),
 ('strict_le','v=int(a<=b)','v=int(a<b)',(('le',('c',2),('c',2)),{},None,None,0)),
 ('wrong_eq','v=int(a==b)','v=int(a!=b)',(('eq',('c',2),('c',2)),{},None,None,0)),
 ('tick_after_tag','t,ready=stack.pop();meter.tick();k=t[0]','t,ready=stack.pop();k=t[0];meter.tick()', ((),{},0,None,0)),
 ('power_postcheck_instead_of_precheck',"if meter.max_bits is not None and a+1>meter.max_bits:raise ResourceLimit('Exponent storage bound')\n            vals.append(1<<a)","vals.append(meter.check(1<<a))",(('pow2',('v',1)),{1:9},None,1,0)),
]
for i,(name,old,new,case) in enumerate(mutations):
    assert source.count(old)==1,(name,source.count(old))
    changed=source.replace(old,new)
    m=module(changed,'review_mutant_'+str(i))
    original=call(actual,*case);mutant=call(m,*case)
    assert original!=mutant,(name,case,original,mutant)
    records.append({'name':name,'case':case,'original':original,'mutant':mutant,'changed_source_sha256':sha(changed.encode()),'detected':True})

# Outside-domain observations establish why the theorem cannot admit malformed
# direct tuples, bools, negative literals or arbitrary host dictionary objects.
malformed=[]
for e in [(),('c',),('c',-1),('c',True),('v',False),('unknown',),('unknown',('c',1),('c',2)),('add',('c',1)),('c',1,2),('pow2',('c',-1)),('pow2',('c',1),('c',2))]:
    malformed.append({'input_repr':repr(e),'observation':call(actual,e,{0:6},None,None,0)})

asts={}
for node in ast.parse(source).body:
    if getattr(node,'name',None) in ['Meter','eval_expr']:
        asts[node.name]={'first_line':node.lineno,'last_line':node.end_lineno,
            'ast_sha256':sha(ast.dump(node,include_attributes=False).encode())}
report={'status':'PASS_FINITE_INDEPENDENT_CONTROLS','source_sha256':PIN,
  'script_sha256':sha(pathlib.Path(__file__).read_bytes()),'independent_literal_copy_sha256':sha(COPY.read_bytes()),
  'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'differential_cases':len(cases),'outcome_counts':dict(counts),'seeded_boundary_cases':seeded,
  'observed_source_lines':sorted(seen),'source_ast_bindings':asts,'mutation_controls':records,
  'outside_domain_observations':malformed,'python_version':sys.version,
  'limits':'Finite corroboration only; no proof about CPython, parser, statements, arbitrary direct ASTs or host resource exhaustion.'}
(R/'evidence/INDEPENDENT_SOURCE_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','differential_cases','outcome_counts','seeded_boundary_cases','source_ast_bindings']},indent=2))
print('Detected mutations:',len(records))
