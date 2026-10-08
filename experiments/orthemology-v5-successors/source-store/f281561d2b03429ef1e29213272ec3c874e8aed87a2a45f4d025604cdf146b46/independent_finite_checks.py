"""Bounded independent bit-mask oracle and discriminating controls; no author writes."""
from itertools import combinations, product
from pathlib import Path
import sys,json,math
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from grounded_support import minimal_supports, available_claims

def subset(x,y):return x&y==x

def minimal(xs):return {x for x in xs if not any(y!=x and subset(y,x) for y in xs)}

def hitcuts(f,n):return {c for c in range(1<<n) if all(c&s for s in f)}

def image(c,p):return sum(1<<r for r in {p[i] for i in range(len(p)) if c&(1<<i)})

def norm(p):
 seen={}
 return tuple(seen.setdefault(x,len(seen)) for x in p)

records=[]
for n in range(1,5):
 partitions=sorted({norm(p) for p in product(range(n),repeat=n)})
 families=[]
 supports=list(range(1,1<<n))
 for selection in range(1,1<<len(supports)):
  f=[s for i,s in enumerate(supports) if selection&(1<<i)]
  if all(not subset(x,y) and not subset(y,x) for x,y in combinations(f,2)):families.append(f)
 bad=0
 for f in families:
  label_cuts=hitcuts(f,n);label_minimal=minimal(label_cuts)
  best=min(c.bit_count() for c in label_cuts)
  cheapest=[c for c in label_cuts if c.bit_count()==best]
  for p in partitions:
   root_cuts=hitcuts({image(s,p) for s in f},max(p)+1)
   assert minimal({image(c,p) for c in label_minimal})==minimal(root_cuts),(n,f,p)
   wrong=min(image(c,p).bit_count() for c in cheapest)
   true=min(c.bit_count() for c in root_cuts)
   if wrong>true:bad+=1
 records.append(dict(labels=n,antichains=len(families),partitions=len(partitions),cases=len(families)*len(partitions),strict_failures=bad))
assert [r['cases'] for r in records]==[1,8,90,2490]
assert [r['strict_failures'] for r in records]==[0,0,0,40]

# Independent direct closure uses integer claim masks and all availability masks.
candidates=list(product(range(8),range(3)))
systems=profiles=0
for k in range(4):
 for rules in combinations(candidates,k):
  systems+=1
  result=minimal_supports([(0,0),(1,1)],[(frozenset(c for c in range(3) if body&(1<<c)),head) for body,head in rules])
  deriving={c:[] for c in range(3)}
  for alive in range(4):
   profiles+=1;closure=alive
   while True:
    nxt=closure
    for body,head in rules:
     if subset(body,closure):nxt|=1<<head
    if nxt==closure:break
    closure=nxt
   actual=available_claims(result,{r for r in range(2) if alive&(1<<r)})
   assert actual=={c for c in range(3) if closure&(1<<c)},(rules,alive)
   for c in range(3):
    if closure&(1<<c):deriving[c].append(alive)
  for c in range(3):
   got={sum(1<<r for r in support) for support in result.get(c,())}
   assert got==minimal(deriving[c]),(rules,c)
assert systems==sum(math.comb(24,k) for k in range(4))==2325
assert profiles==4*systems==9300

# Edge families omitted intentionally by the 2,589-case author's alias search.
edge_families=[[],[0],[0,1],[1,3],[1,2,3]]
edge_checks=0
for f in edge_families:
 for p in [(0,0),(0,1)]:
  assert minimal({image(c,p) for c in minimal(hitcuts(f,2))})==minimal(hitcuts({image(s,p) for s in f},max(p)+1))
  edge_checks+=1

# Distinguish full alternatives from a flattened union; require saturated aliases.
r=minimal_supports([('a','c'),('b','c')],[])
assert 'c' in available_claims(r,{'a'})
assert not {'a','b'}<={'a'}
r=minimal_supports([('a1','p'),('a2','q')],[({'p','q'},'c')])
assert 'c' not in available_claims(r,{'a1'})
assert 'c' in available_claims(r,{'a1','a2'})

# Retaining every cheapest label cut still loses the unique root optimum.
f=[0b0001,0b1010,0b1100];p=(0,0,0,1)
cs=hitcuts(f,4);lc={c for c in cs if c.bit_count()==min(map(int.bit_count,cs))}
rc=hitcuts({image(s,p) for s in f},2)
assert lc=={0b1001} and minimal(cs)=={0b1001,0b0111}
assert {c for c in rc if c.bit_count()==min(map(int.bit_count,rc))}=={0b01}
assert image(0b1001,p).bit_count()==2 and image(0b0111,p).bit_count()==1

out={'status':'PASS','oracle':'Independent integer-bitmask closure, subset/cut enumeration and partition generation; does not use author cut/minimization/search helpers','rule_domain':{'claims':3,'roots':2,'fixed_base':[[0,0],[1,1]],'possible_rules':24,'selected_rule_count_range':[0,3],'systems':systems,'availability_profiles':profiles},'alias_records':records,'alias_cases':sum(r['cases'] for r in records),'additional_edge_transport_checks':edge_checks,'discriminating_controls':['empty family','empty support','dominated/redundant supports','alternative versus union','saturated alias availability','unique cheapest four-label cut still wrong after aliasing']}
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path.cwd()/'INDEPENDENT_FINITE_CHECKS.json'
path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
