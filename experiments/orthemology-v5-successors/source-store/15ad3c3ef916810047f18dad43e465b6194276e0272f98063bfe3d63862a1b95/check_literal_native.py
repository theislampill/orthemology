#!/usr/bin/env python3
"""Bounded parsed-code corroboration, separate from infinite-horizon Lean proof."""
from pathlib import Path
from fractions import Fraction
import argparse,ast,hashlib,importlib.util,itertools,json,sys,time
sys.dont_write_bytecode=True;sys.set_int_max_str_digits(0);sys.setrecursionlimit(100000)
p=argparse.ArgumentParser();p.add_argument('--readback',type=Path,required=True);p.add_argument('--codec',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
assert not a.out.exists()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(a.codec.read_bytes())=='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
spec=importlib.util.spec_from_file_location('literal_codec',a.codec);codec=importlib.util.module_from_spec(spec);sys.modules[spec.name]=codec;spec.loader.exec_module(codec)
values={line.split('=',1)[0]:line.split('=',1)[1] for line in a.readback.read_text().splitlines() if '_BYTES=' in line}
programs={};identities=[]
for name in ['OLD_FALSE','OLD_TRUE','COMPUTED_FALSE','COMPUTED_TRUE']:
 b=bytes(ast.literal_eval(values[name+'_BYTES']));prog=codec.decode_bytes(b);assert prog is not None and codec.encode_bytes(prog)==b
 programs[name]=prog;identities.append({'name':name,'arity':prog.arity,'bytes':len(b),'sha256':sha(b)})
def history_code(h):
 n=1
 for act,y in h:n=4*n+2*act+y
 return n
def reference(h,orientation,computed):
 phase=0;s=0;counts=[0]*4;symbols=[[0,0] for _ in range(4)];tol=Fraction(1,6) if computed else Fraction(2)
 for act,y in h:
  e=2*s+act;counts[e]+=1;symbols[e][y]+=1;candidate=orientation^(phase%2)
  reject=False
  for f in range(4):
   for z in range(2):
    trueprob=Fraction(1 if f%2==candidate else 2,3);prob=trueprob if z else 1-trueprob
    freq=Fraction(symbols[f][z],counts[f]) if counts[f] else Fraction(0)
    if phase<counts[f] and tol<=abs(freq-prob):reject=True
  if reject:phase+=1
  s=y
 return orientation^(phase%2)
t0=time.monotonic();cases=[]
for orientation in [0,1]:
 for computed in [False,True]:
  name=('COMPUTED' if computed else 'OLD')+'_'+('TRUE' if orientation else 'FALSE');prog=programs[name]
  for n in range(4):
   for h in itertools.product(itertools.product([0,1],repeat=2),repeat=n):
    expected=reference(h,orientation,computed);actual=codec.run(prog,[history_code(h)],step_limit=30_000_000)
    assert actual==expected,(name,h,actual,expected)
    cases.append({'program':name,'history':h,'actual':actual,'expected':expected})
  try:codec.run(prog,[1],step_limit=0)
  except codec.ResourceLimit:pass
  else:raise AssertionError('Zero resource bound fabricated a result')
result={'status':'PASS_BOUNDED_LITERAL_PARSED_CODE','readback_sha256':sha(a.readback.read_bytes()),'codec_sha256':sha(a.codec.read_bytes()),'elapsed_seconds':round(time.monotonic()-t0,3),'programs':identities,'history_cases':len(cases),'max_history_length':3,'all_results_match_independent_reference':True,'zero_resource_guard_passed':True,'selector_scope':'Both executable orientations evaluated; the Lean disjunction certifies at least one, not an evaluated selection of the retained orientation','infinite_parity_credit':'None from this finite check; see separate kernel theorem','cases':cases}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
