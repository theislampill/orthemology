#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,sys
P=Path(__file__).resolve().parents[1]/'reference.py'
spec=importlib.util.spec_from_file_location('unbounded_reference',P);ref=importlib.util.module_from_spec(spec);sys.modules['unbounded_reference']=ref;spec.loader.exec_module(ref)
assert hasattr(ref,'decide_counts_unbounded'),'Missing uncapped exact-rational core'
assert hasattr(ref,'decide_word_unbounded'),'Missing uncapped finite-word adapter'
checks=0

def check(value):
 global checks
 checks+=1
 assert value,checks

def oracle(n,k,e,d,mode):
 floor=max(F(k,n),F(1,n));i=0
 while True:
  a=F(1,2**((i+1)**2));r=F(1,2**(2*i+3));b=a*min(F(3,4),max(3*r/2,F(1,128*(2*i+3))))
  if b<floor:break
  i+=1
 mean=F(k,n)
 if mode=='strict_width':q=F(1,2)+e*(mean if a>(e-d)/(2*e) else a*(1-d*e))
 elif a>F(1,8):q=F(1,2)+e*mean
 else:q=F(1,2)+e*a*(1-e*e)+(1 if mean>a else -1)*2*e*e*a*a
 return i,q

# The core agrees exactly with the guarded restriction on its domain.
for n in list(range(1,80))+[1024,1_000_000]:
 for k in sorted(set([0,1,n//2,n])):
  for mode,e,d in [('strict_width',F(1,4),F(1,16)),('uniform_critical',F(1,16),F(1,16))]:
   check(ref.decide_counts_unbounded(n,k,e,d,mode)==ref.decide_counts(n,k,e,d,mode))

# Every listed input is outside at least one old cap, yet valid for the core.
large_cases=[(1<<4096,0,F(1,16),F(1,16),'uniform_critical'),
 (1<<8192,0,F(1,1<<8192),F(1,1<<8192),'uniform_critical'),
 (1<<8192,1<<8191,F(1,4),F(1,16),'strict_width'),
 (17,1,F(1,1<<8192),F(),'strict_width')]
guard=sys.get_int_max_str_digits()
for n,k,e,d,mode in large_cases:
 got=ref.decide_counts_unbounded(n,k,e,d,mode);i,q=oracle(n,k,e,d,mode)
 check((got.index,got.report)==(i,q));check(0<=got.report<=1);check(got.visited<=got.search_bound+1)
 encoded=json.dumps(ref.to_jsonable(got));check(bool(encoded));check(sys.get_int_max_str_digits()==guard)
 try:ref.decide_counts(n,k,e,d,mode)
 except ValueError:check(True)
 else:raise AssertionError('Guarded wrapper silently expanded')

word='0'*1_000_001
check(ref.decide_word_unbounded(word,F(1,4),F(1,16))==ref.decide_counts_unbounded(len(word),0,F(1,4),F(1,16)))
try:ref.decide_word(word,F(1,4),F(1,16))
except ValueError:check(True)
else:raise AssertionError('Guarded word adapter silently expanded')

for f in [lambda:ref.decide_counts_unbounded(0,0),lambda:ref.decide_counts_unbounded(True,0),
 lambda:ref.decide_counts_unbounded(1,2),lambda:ref.decide_counts_unbounded(1,0,.25,F()),
 lambda:ref.decide_counts_unbounded(1,0,F(1,4),F(1,4),'strict_width'),
 lambda:ref.decide_word_unbounded(''),lambda:ref.decide_word_unbounded('001x')]:
 try:f()
 except (ValueError,TypeError):check(True)
 else:raise AssertionError('Invalid core input accepted')
print(json.dumps({'status':'PASS','exact_assertions':checks,'old_caps_crossed':True,'largest_summary_bits':8193,
 'largest_parameter_bits':8193,'guarded_wrapper_unchanged':True,'decimal_guard_unchanged':sys.get_int_max_str_digits()==guard,
 'scope':'No preset input-size ceiling in the core; termination is mathematical, with no physical-memory or latency guarantee.'},indent=2))
