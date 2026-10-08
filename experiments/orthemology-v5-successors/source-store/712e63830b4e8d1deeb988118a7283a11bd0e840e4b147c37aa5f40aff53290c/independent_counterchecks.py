#!/usr/bin/env python3
"""Independent exact enumeration using retained index subsets, no author/root code."""
from fractions import Fraction as F
from itertools import combinations,product
from collections import defaultdict
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent
import argparse
import os
from pathlib import Path

def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True,help='New receipt file outside the entire source package')
args=parser.parse_args()
if args.output.exists() or args.output.is_symlink(): raise SystemExit('Refusing existing receipt path')
output=guarded_output(args.output,[Path(__file__).absolute().parent.parent,Path(__file__).resolve().parent.parent])
package=Path(__file__).resolve().parent.parent
if output.is_relative_to(package): raise SystemExit('Receipt must be outside source package')
if not output.parent.is_dir(): raise SystemExit('Receipt parent must exist')
alphabet=[(),(0,),(1,),(0,0),(0,1),(1,0),(1,1)]
words=list(product((0,1),repeat=2))
def observations(word,p):
 result=[]
 for size in range(3):
  for inds in combinations(range(2),size):
   result.append((inds,tuple(word[i] for i in inds),p**size*(1-p)**(2-size)))
 return result
def law(word,p):
 result=dict.fromkeys(alphabet,F(0))
 for inds,trace,weight in observations(word,p):result[trace]+=weight
 return result
def dist(a,b):return sum(abs(a.get(t,F(0))-b.get(t,F(0))) for t in a.keys()|b.keys())/2
def copies(a,m):
 out=defaultdict(F)
 for t,p in a.items():out[(t,)*m]+=p
 return dict(out)
def fresh_by_masks(word,p,m):
 out=defaultdict(F)
 for samples in product(observations(word,p),repeat=m):
  prob=F(1)
  for _,_,v in samples:prob*=v
  out[tuple(x[1] for x in samples)]+=prob
 return dict(out)
checks=[]
for p in map(F,[0,F(1,4),F(1,2),F(3,4),1]):
 for w in words:
  a=law(w,p);assert sum(a.values())==1 and min(a.values())>=0
  assert a[()]==(1-p)**2
  for source in [0,1]:assert law(w,p)==a
 a,b=law((0,0),p),law((0,1),p)
 assert dist(a,b)==p
 for m in range(5):
  ca,cb=copies(a,m),copies(b,m);fa,fb=fresh_by_masks((0,0),p,m),fresh_by_masks((0,1),p,m)
  assert sum(ca.values())==sum(cb.values())==sum(fa.values())==sum(fb.values())==1
  assert dist(ca,cb)==(p if m else 0)
  assert dist(fa,fb)==1-(1-p)**m
  optimal=sum(max(fa.get(t,F(0)),fb.get(t,F(0))) for t in fa.keys()|fb.keys())/2
  assert optimal==1-(1-p)**m/2
  checks.append(dict(retention=str(p),M=m,copied_tv=str(dist(ca,cb)),fresh_tv=str(dist(fa,fb)),fresh_success=str(optimal)))
a,b=law((0,0),F(1,4)),law((0,1),F(1,4))
scores=[]
for h in product((F(0),F(1)),repeat=7):
 scores.append(sum(a[t]*(1-v)+b[t]*v for t,v in zip(alphabet,h))/2)
assert len(scores)==128 and max(scores)==F(5,8)
random_scores=[]
for h in product((F(0),F(1,3),F(1)),repeat=7):
 s=sum(a[t]*(1-v)+b[t]*v for t,v in zip(alphabet,h))/2
 assert s<=F(5,8);random_scores.append(s)
assert len(random_scores)==2187
# Removing empty observations changes the service by selection/renormalization.
conditional_a={t:v/(1-a[()]) for t,v in a.items() if t};conditional_b={t:v/(1-b[()]) for t,v in b.items() if t}
assert dist(conditional_a,conditional_b)==F(4,7)
# Retention vs deletion convention reversal is observable.
assert dist(law((0,0),F(3,4)),law((0,1),F(3,4)))==F(3,4)
# Two copied coordinates are not conditionally independent, despite identical marginals.
ca,fa=copies(a,2),fresh_by_masks((0,0),F(1,4),2)
assert ca[((),())]==F(9,16) and fa[((),())]==F(81,256)
assert ca.get(((),(0,)),0)==0 and fa[((),(0,))]==F(27,128)
for j in [0,1]:
 for trace in alphabet:
  assert sum(v for z,v in ca.items() if z[j]==trace)==a[trace]
  assert sum(v for z,v in fa.items() if z[j]==trace)==a[trace]
# Known00, first trace0: any positive-probability second fresh output leaves position posterior1/2.
pos=[]
for second_trace in [(),(0,),(0,0)]:
 event=defaultdict(F)
 for first,second in product(observations((0,0),F(1,4)),repeat=2):
  if first[1]==(0,) and second[1]==second_trace:event[first[0]]+=first[2]*second[2]
 assert set(event)=={(0,),(1,)}
 total=sum(event.values());assert all(v/total==F(1,2) for v in event.values())
 pos.append(dict(second_trace=list(second_trace),first_position_posterior=["1/2","1/2"]))
# If mask identities were exposed, the sample space would be a different service.
exposed=[]
for word in [(0,0),(0,1)]:exposed.append({(inds,t):p for inds,t,p in observations(word,F(1,4))})
assert dist(*exposed)==F(1,4) # This pair has same TV, yet attribution is now exact.
receipt=dict(status='PASS_INDEPENDENT_EXACT_COUNTERCHECKS',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),channel='retained index subsets on all four words; seven complete traces',endpoint_retention_values=['0','1/4','1/2','3/4','1'],finite_product_checks=checks,deterministic_rules_complete_alphabet=128,randomized_grid_rules=2187,randomized_grid='0,1/3,1 independently at each of seven traces; finite evidence only',optimal_success='5/8',condition_nonempty_tv='4/7',copied_joint_empty='9/16',fresh_joint_empty='81/256',copy_offdiagonal_empty_zero='0',fresh_offdiagonal_empty_zero='27/128',known_word_mask_fresh_observation_checks=pos,mask_exposure_caveat='Exposing original retained positions changes attribution even when this pair TV happens to remain1/4.',limit='Finite checks are not all-M kernel proofs or asymptotic convergence; root/author enumerations were not reused.')
with output.open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='finite_product_checks'},indent=2))
