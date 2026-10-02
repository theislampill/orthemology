#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,subprocess,sys,os
P=Path(__file__).resolve().parents[1]/'reference.py'
assert P.exists(),'Missing effective rational reference'
spec=importlib.util.spec_from_file_location('reference',P);ref=importlib.util.module_from_spec(spec);sys.modules['reference']=ref;spec.loader.exec_module(ref)
checks=0

def check(x):
 global checks
 checks+=1
 assert x,checks

def a(i):return F(1,2**((i+1)**2))
def independent_rank(r):
 m=0;s=F(1)
 while s>r:s/=2;m+=1
 return m

def boundary(i):
 x=a(i);y=a(i+1);r=y/x;m=independent_rank(r)
 return x*min(F(3,4),max(F(3,2)*r,F(1,128*m)))

def oracle(n,k,e,d,mode):
 x=max(F(k,n),F(1,n));i=0
 while x<=boundary(i):i+=1
 ai=a(i);mean=F(k,n)
 if mode=='strict_width':
  if ai>(e-d)/(2*e):q=F(1,2)+e*mean;branch='empirical_head'
  else:q=F(1,2)+e*ai*(1-d*e);branch='shifted_tail'
 else:
  if ai>F(1,8):q=F(1,2)+e*mean;branch='empirical_head'
  else:
   s=e*ai*(1-e*e);h=2*e*e*ai*ai
   if mean<=ai:q=F(1,2)+s-h;branch='critical_left'
   else:q=F(1,2)+s+h;branch='critical_right'
 return i,q,branch

modes=[('strict_width',F(1,4),F()),('strict_width',F(1,4),F(1,16)),('strict_width',F(1,32),F(3,128)),('uniform_critical',F(1,16),F(1,16))]
for mode,e,d in modes:
 for n in range(1,9):
  for word in product('01',repeat=n):
   word=''.join(word);k=word.count('1');got=ref.decide_word(word,e,d,mode);want=oracle(n,k,e,d,mode)
   check((got.index,got.report,got.branch)==want)
   check(0<=got.report<=1)
   check(got.visited<=got.search_bound+1)
   check(got.index<=got.search_bound==(n-1).bit_length())
   check(got.centre==a(got.index));check(got.boundary==boundary(got.index))
   check(got.floored_mean>got.boundary)
   if got.index:check(got.floored_mean<=boundary(got.index-1))

for bits in [1,2,8,20,40,80,256,1024,4096]:
 n=(1<<(bits-1)) if bits>1 else 1
 for k in [0,1,n//16,n//2,n]:
  for mode,e,d in modes:
   got=ref.decide_counts(n,k,e,d,mode);want=oracle(n,k,e,d,mode)
   check((got.index,got.report,got.branch)==want)
   check(got.index<=got.search_bound);check(got.visited<=got.search_bound+1)

# Declared maximum binary-word length is exercised, not just its rejection edge.
for word in ['0'*1_000_000,'1'*1_000_000,'01'*500_000]:
 got=ref.decide_word(word,F(1,4),F(1,16),'strict_width')
 check((got.index,got.report,got.branch)==oracle(len(word),word.count('1'),F(1,4),F(1,16),'strict_width'))

# Exact ties at the empirical mean and at a cluster boundary.
got=ref.decide_counts(16,1,F(1,16),F(1,16),'uniform_critical')
check(got.index==1 and got.branch=='critical_left')
got=ref.decide_counts(32,3,F(1,16),F(1,16),'uniform_critical')
check(got.index==1 and got.branch=='critical_right' and got.floored_mean==boundary(0))

for r in [F(1,2),F(1,3),F(1,4),F(3,32),F(1,2**4096),F(7,2**127)]:
 m=ref.dyadic_rank(r);check(m==independent_rank(r));check(F(1,2**m)<=r<F(1,2**(m-1)))

invalid=[lambda:ref.decide_word('',F(1,4),F()),lambda:ref.decide_word('01x',F(1,4),F()),
 lambda:ref.decide_word(b'01',F(1,4),F()),lambda:ref.decide_word('0'*1_000_001,F(1,4),F()),
 lambda:ref.decide_counts(True,0,F(1,4),F()),lambda:ref.decide_counts(0,0,F(1,4),F()),
 lambda:ref.decide_counts(4,-1,F(1,4),F()),lambda:ref.decide_counts(4,5,F(1,4),F()),
 lambda:ref.decide_counts(4,1,.25,F()),lambda:ref.decide_counts(4,1,F(),F()),
 lambda:ref.decide_counts(4,1,F(1,3),F()),lambda:ref.decide_counts(4,1,F(1,4),F(-1,16)),
 lambda:ref.decide_counts(4,1,F(1,16),F(1,16),'strict_width'),
 lambda:ref.decide_counts(4,1,F(1,4),F(1,4),'uniform_critical'),
 lambda:ref.decide_counts(4,1,F(1,32),F(1,64),'uniform_critical'),
 lambda:ref.decide_counts(4,1,F(1,4),F(),'unknown'),
 lambda:ref.decide_counts(1<<4096,0,F(1,4),F()),
 lambda:ref.decide_counts(4,1,F(1,1<<4096),F()),
 lambda:ref.parse_fraction('1/0'),lambda:ref.parse_fraction('nan'),lambda:ref.parse_fraction('1e-4'),
 lambda:ref.parse_fraction('9'*1235+'/10')]
for f in invalid:
 try:f()
 except (ValueError,TypeError):check(True)
 else:raise AssertionError('Invalid input accepted')

# Chunked integer serialization includes zero, signs and far-longer magnitudes.
for integer in [0,1,-1,10**9-1,10**9,-10**9,10**10000+123,-(10**10000+123)]:
 text=ref.decimal_integer(integer);negative=text.startswith('-');digits=text.lstrip('-');restored=0
 for character in digits:restored=restored*10+ord(character)-48
 if negative:restored=-restored
 check(restored==integer)

# Serialize a valid report with more than4300 decimal denominator digits.
guard=sys.get_int_max_str_digits();tiny=F(1,1<<4095);big=ref.decide_counts(1<<4095,0,tiny,tiny,'uniform_critical')
obj=ref.to_jsonable(big);encoded=json.dumps(obj);check(sys.get_int_max_str_digits()==guard)
check(len(obj['report']['denominator'])>4300)
def parse_decimal(s):
 neg=s.startswith('-');s=s.lstrip('-');v=0
 for c in s:v=v*10+ord(c)-48
 return -v if neg else v
for key in ['epsilon','delta','centre','boundary','report','empirical_mean','floored_mean']:
 value=obj[key];frac=F(parse_decimal(value['numerator']),parse_decimal(value['denominator']))
 check(frac==getattr(big,key))

big_cli=subprocess.run([sys.executable,'-B',str(P),'--summary',ref.decimal_integer(1<<4095),'0','--epsilon','1/'+ref.decimal_integer(1<<4095),'--mode','uniform_critical'],text=True,capture_output=True)
check(big_cli.returncode==0);check(json.loads(big_cli.stdout)==obj)

r=subprocess.run([sys.executable,'-B',str(P),'--word','0000000000000001','--epsilon','1/16','--mode','uniform_critical'],text=True,capture_output=True)
check(r.returncode==0);j=json.loads(r.stdout);check(j['branch']=='critical_left');check(j['index']==1)
# Valid in-range decimal CLI input under a reduced host conversion guard.
low_guard=subprocess.run([sys.executable,'-B',str(P),'--summary','1'+'0'*1000,'0'],text=True,capture_output=True,env=dict(os.environ,PYTHONINTMAXSTRDIGITS='640'))
check(low_guard.returncode==0);low_obj=json.loads(low_guard.stdout);check(low_obj['n']=='1'+'0'*1000)
check(sys.get_int_max_str_digits()==guard)

for args in [['--word','01x'],['--word','1','--epsilon','1/0'],['--summary','0','0'],['--word','01','--summary','2','1']]:
 r=subprocess.run([sys.executable,'-B',str(P)]+args,text=True,capture_output=True)
 check(r.returncode!=0);check(not r.stdout.strip())
print(json.dumps({'status':'PASS','exact_assertions':checks,'modes':len(modes),'invalid_cases':len(invalid),
 'high_bit_case':4096,'decimal_guard_unchanged':sys.get_int_max_str_digits()==guard,'scope':'Restricted exact-rational executable tests, not an infinite statistical proof.'},indent=2))
