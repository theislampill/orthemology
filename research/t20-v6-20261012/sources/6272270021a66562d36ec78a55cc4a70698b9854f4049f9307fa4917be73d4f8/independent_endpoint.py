#!/usr/bin/env python3
"""Fresh independent parser and recursive semantics for the two decoded codes.
Finite checks only; the universal stream/cost argument is ordinary mathematics.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,sys,copy
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'snapshot'))
import prcodec as retained

def parse(index):
 raw=index.to_bytes((index.bit_length()+7)//8,'big')
 assert raw[:1]==b'\x01' and raw[1:6]==b'P02L\x01'
 b=raw[1:];pos=5
 def byte():
  nonlocal pos
  if pos>=len(b):raise ValueError('truncated')
  x=b[pos];pos+=1;return x
 def uv():
  value=0;shift=0;start=pos
  while True:
   x=byte();value+=(x&127)<<shift
   if x<128:break
   shift+=7
  z=value;canonical=[]
  while z>=128:canonical.append(z%128+128);z//=128
  canonical.append(z)
  assert bytes(canonical)==b[start:pos]
  return value
 names={1:'c',2:'v',3:'add',4:'sub',5:'mul',6:'div',7:'mod',8:'le',9:'eq',10:'pow2'}
 def expr():
  tag=byte();name=names[tag]
  if tag in (1,2):return name,uv()
  if tag==10:return name,expr()
  return name,expr(),expr()
 def stmt():
  tag=byte()
  if tag==16:return 'set',uv(),expr()
  if tag==17:return ('seq',*(stmt() for _ in range(uv())))
  if tag==18:return 'loop',uv(),expr(),stmt()
  if tag==19:return 'if',expr(),stmt(),stmt()
  raise ValueError('bad statement')
 arity=uv();output=uv();body=stmt();assert pos==len(b)
 return arity,output,body,b

def expr(e,r):
 op=e[0]
 if op=='c':return e[1]
 if op=='v':return r.get(e[1],0)
 a=expr(e[1],r)
 if op=='pow2':return 2**a
 b=expr(e[2],r)
 if op=='add':return a+b
 if op=='sub':return max(a-b,0)
 if op=='mul':return a*b
 if op=='div':return a//b if b else 0
 if op=='mod':return a%b if b else a
 if op=='le':return int(a<=b)
 if op=='eq':return int(a==b)
 raise ValueError(op)

def statement(s,r):
 op=s[0];tasks=1
 if op=='set':r[s[1]]=expr(s[2],r)
 elif op=='seq':
  for sub in s[1:]:tasks+=statement(sub,r)
 elif op=='loop':
  count=expr(s[2],r)
  tasks+=count+1 # repeat tasks, including the terminal repeat
  for j in range(count):r[s[1]]=j;tasks+=statement(s[3],r)
 elif op=='if':tasks+=statement(s[2] if expr(s[1],r) else s[3],r)
 else:raise ValueError(op)
 return tasks

def execute(p,registers):
 r=dict(registers);tasks=statement(p[2],r);return r,tasks

def loss(a,q):
 return (q*q-(a*F(3,4)**2+(1-a)*F(1,2)**2),
         (1-q)**2-(a*F(1,4)**2+(1-a)*F(1,2)**2))

identity=json.loads((BASE/'snapshot/NATIVE_ENDPOINT.json').read_text())
cache=parse(int(identity['cache_index']));prefix=parse(int(identity['prefix_index']))
assert list(cache[3])==identity['cache_bytes'] and len(cache[3])==59 and len(prefix[3])==105
for p,name in [(cache,'cache'),(prefix,'prefix')]:
 decoded=retained.decode(int(identity[name+'_index']))
 assert (decoded.arity,decoded.output,decoded.body)==p[:3]
 assert retained.encode_bytes(decoded)==p[3]
assert cache[0:2]==(1,5) and prefix[0:2]==(2,5)
words=ticks=0
for n in range(11):
 for w in product([0,1],repeat=n):
  words+=1;L=R=1;code=1;seen=False
  for j,bit in enumerate(w):
   code=2*code+bit;seen=seen or bool(bit)
   regs,cost=execute(cache,{0:bit,2:L,4:R});L,R=regs[2],regs[4]
   assert cost==5 and R==1 and L==(0 if seen else 2**(j+1))
   assert regs[5]==int(seen)
   pr,pcost=execute(prefix,{0:j,1:code})
   assert pr[5]==int(seen) and pcost==6*(j+1)+10 and pr[3]==1
   assert retained.evaluate_index(int(identity['prefix_index']),j,code)==int(seen)
   ticks+=1
# Check arbitrary natural cache frames against the literal recurrence.
frames=0
for L,R,bit in product(range(17),range(17),[0,1]):
 regs,cost=execute(cache,{0:bit,2:L,4:R})
 expectedL=0 if bit else 2*L
 assert (regs[2],regs[4],regs[5],cost)==(expectedL,R,int(expectedL+1<=R),5);frames+=1
expected={(F(0),F(1,2)):(F(0),F(0)),(F(0),F(5,8)):(F(9,64),F(-7,64)),(F(1,2),F(1,2)):(F(-5,32),F(3,32)),(F(1,2),F(5,8)):(F(-1,64),F(-1,64))}
for pair,value in expected.items():assert loss(*pair)==value
# Enumerate actual fair-prefix masses and literal failures, including action0.
partial=[]
for horizon in range(11):
 total=F(0)
 for n in range(horizon+1):
  wrong=sum(not all(v<=0 for v in loss(F(1,2),F(5,8) if any(w) else F(1,2))) for w in product([0,1],repeat=n))
  assert wrong==1;total+=F(wrong,2**n)
 assert total==2-F(1,2)**horizon;partial.append(str(total))
# Named semantic failures, each under an explicit wrong adapter/convention.
assert execute(cache,{0:1,2:0,4:0})[0][5]==0 # invalid cold cache
post=execute(cache,{0:1,2:1,4:1})[0]
assert execute(cache,{0:0,2:post[2],4:post[4]})[0][5]==1
assert execute(cache,{0:0,2:1,4:1})[0][5]==0 # stale cache
assert int(1+1<=1)==0 and post[5]==1 # pre-update readout
assert retained.evaluate_index(int(identity['cache_index']),0,3)==0
assert execute(prefix,{0:1,2:1,4:1})[0][5]==0 # wrong cache-style call to prefix code
# Extra prefix iteration consumes the sentinel and changes a zero receipt.
def replace_bound(s):
 if s[0]=='loop':return ('loop',s[1],('add',('v',0),('c',2)),s[3])
 if s[0]=='seq':return ('seq',*(replace_bound(x) for x in s[1:]))
 return s
bad=(2,5,replace_bound(prefix[2]),prefix[3])
assert execute(prefix,{0:0,1:2})[0][5]==0 and execute(bad,{0:0,1:2})[0][5]==1
assert sum(F(1,2)**n for n in range(1,11))==F(1023,1024) # deleted initial charge
out={'status':'PASS_FRESH_INDEPENDENT_FINITE_ENDPOINT_REVIEW','words':words,'ticks':ticks,'arbitrary_cache_frames':frames,'independent_parser_matches_literal_indices':True,'independent_recursive_semantics_matches_retained_interpreter':True,'cache_tasks':5,'prefix_tasks':'6m+10','literal_loss_table':{str(k):list(map(str,v)) for k,v in expected.items()},'fair_partial_expected_errors':partial,'negative_controls':['cold cache','stale cache','pre-update output','cache code through indexed API','prefix code through cache-style API','one extra sentinel iteration','omitted initial action'],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite source checks; universal seen-one equality, infinite-law countable support and cost(0,2) are ordinary arguments in the report, not Lean replays.'}
(BASE/'evidence/INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
