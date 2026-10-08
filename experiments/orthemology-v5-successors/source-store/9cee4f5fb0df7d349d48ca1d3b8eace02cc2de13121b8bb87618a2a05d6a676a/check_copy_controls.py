"""Independent exact-rational finite controls for trace-transfer scope.
This is newly written analysis code, not a repository executable or proof replay.
"""
from fractions import Fraction as F
from itertools import product
import json, pathlib
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
output=guarded_output(args.output,[Path(__file__).absolute().parent,Path(__file__).resolve().parent])
package=Path(__file__).resolve().parent
if output.is_relative_to(package): raise SystemExit('Receipt must be outside source package')
if not output.parent.is_dir(): raise SystemExit('Receipt parent must exist')
p=F(1,4);q=1-p

def law(word):
 out={}
 for mask in product([False,True],repeat=len(word)):
  w=''.join(b for b,m in zip(word,mask) if m)
  mass=F(1)
  for m in mask:mass*=p if m else q
  out[w]=out.get(w,F(0))+mass
 return out

def tv(a,b):return sum(abs(a.get(w,0)-b.get(w,0)) for w in set(a)|set(b))/2

def repeat_law(a,m):return {(w,)*m:v for w,v in a.items()}
A,B=law('00'),law('01');assert sum(A.values())==sum(B.values())==1
assert tv(A,B)==F(1,4)
assert sum(max(A.get(w,0),B.get(w,0)) for w in set(A)|set(B))/2==F(5,8)
# Exhaust every deterministic binary decision rule on the union output support.
ws=sorted(set(A)|set(B));scores=[]
for bits in product([0,1],repeat=len(ws)):
 score=sum(A.get(w,0) if b==0 else B.get(w,0) for w,b in zip(ws,bits))/2
 scores.append(score)
assert max(scores)==F(5,8)
rep=[]
for m in range(1,17):
 val=tv(repeat_law(A,m),repeat_law(B,m));assert val==F(1,4)
 rep.append(dict(copies=m,total_variation=str(val),empty_all_probability=str(q*q),independent_empty_all_probability=str((q*q)**m)))
# Known source word00 plus observed trace0 leaves the retained position ambiguous.
matching=[]
for mask in product([False,True],repeat=2):
 if ''.join(b for b,m in zip('00',mask) if m)=='0':
  mass=F(1)
  for m in mask:mass*=p if m else q
  matching.append((mask,mass))
assert len(matching)==2 and all(mass/sum(m for _,m in matching)==F(1,2) for _,mass in matching)
result={'status':'PASS_EXACT_FINITE_CONTROLS','retention_probability':str(p),'deletion_probability':str(q),'word00_law':{w:str(v) for w,v in A.items()},'word01_law':{w:str(v) for w,v in B.items()},'one_trace_total_variation':'1/4','equal_prior_optimal_binary_success':'5/8','all_deterministic_rules_enumerated':len(scores),'replicated_observation_checks':rep,'known_word_occurrence_masks':[{'mask':list(m),'conditional_probability':'1/2'} for m,_ in matching],'general_all_m_proof':'For m>=1, replication z -> (z,...,z) is injective and has first-coordinate recovery. Summing its pushforward masses therefore preserves TV exactly. Finite checks are illustrative; this argument handles every m.','limitations':['No OpenAI math repository theorem or decoder was executed.','Not a Lean kernel proof.','No actual transmission, participant data, source attribution or historical event was tested.','A common latent word is intended in iid trace reconstruction; only copying the same realised trace is replaced in the negative control.']}
with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
