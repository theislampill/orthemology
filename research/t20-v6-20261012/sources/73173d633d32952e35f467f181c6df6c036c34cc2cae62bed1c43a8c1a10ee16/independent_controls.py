"""Independent exact review controls; pair-product reachability, not author refinement."""
from fractions import Fraction as Q
from collections import deque
from pathlib import Path
from itertools import combinations
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'provenance-learning-transport-20261009'

def N(v):
 s=sum(v);assert s>0
 return tuple(x/s for x in v)
def posterior(E,ls,p):
 v=list(p)
 for i in E: v=[a*b for a,b in zip(v,ls[i])]
 return N(v)
def transition(E,op):
 sign,i=op
 return E|{i} if sign=='A' else E-{i}
def distinguish(E,F,ops,output):
 # Search the paired transition system for an actual distinguishing common word.
 todo=deque([(E,F,())]);seen={(E,F)}
 while todo:
  e,f,w=todo.popleft()
  if output[e]!=output[f]: return w
  for op in ops:
   en,fn=transition(e,op),transition(f,op)
   if (en,fn) not in seen:
    seen.add((en,fn));todo.append((en,fn,w+(op,)))
 return None

cases=[
 {'name':'inverse_factors_three_states', 'p':(Q(1,2),Q(1,3),Q(1,6)),
  'ls':[(Q(2),Q(1),Q(1)),(Q(1,2),Q(1),Q(1)),(Q(1),Q(3),Q(1)),(Q(5),)*3]},
 {'name':'duplicates_three_states', 'p':(Q(1,5),Q(3,5),Q(1,5)),
  'ls':[(Q(2),Q(3),Q(4))]*3+[(Q(2),)*3]},
 {'name':'asymmetric_prior_four_states', 'p':(Q(1,10),Q(2,10),Q(3,10),Q(4,10)),
  'ls':[(Q(2),Q(1),Q(3),Q(4)),(Q(1,2),Q(1),Q(1,3),Q(1,4)),(Q(3),Q(2),Q(1),Q(2)),(Q(7),)*4]},
 {'name':'singleton_hypothesis', 'p':(Q(1),), 'ls':[(Q(2),),(Q(3),),(Q(5),)]},
 {'name':'empty_catalogue', 'p':(Q(1,3),Q(2,3)), 'ls':[]},
]
rows=[];pairs=merges=0
for case in cases:
 p,ls=case['p'],case['ls'];k=len(ls)
 stores=[frozenset(i for i in range(k) if m>>i&1) for m in range(1<<k)]
 out={E:posterior(E,ls,p) for E in stores}
 I=frozenset(i for i,L in enumerate(ls) if len(set(L))>1)
 for E in stores:
  for F in stores:
   got=N(tuple(a*b/c for a,b,c in zip(out[E],out[F],out[E&F])))
   assert got==out[E|F]
   merges+=1
 for names in ['A','D','AD']:
  ops=[(s,i) for s in names for i in range(k)]
  witnesses=[]
  for E,F in combinations(stores,2):
   word=distinguish(E,F,ops,out)
   assert (word is None)==(E&I==F&I),(case['name'],names,E,F,word)
   pairs+=1
   if word is not None:witnesses.append(len(word))
  rows.append({'case':case['name'],'alphabet':names,'expected_classes':1<<len(I),
               'current_posteriors':len(set(out.values())),
               'max_found_distinguishing_word':max(witnesses,default=0)})
 # Fully supported prior is essential to calling all nonconstant roots informative.
 if k and I:
  i=next(iter(I));assert out[frozenset({i})]!=out[frozenset()]

# Genuine exact cancellation: an empty store and a two-root store have the same posterior.
c=cases[0];assert posterior(frozenset(),c['ls'],c['p'])==posterior(frozenset({0,1}),c['ls'],c['p'])
assert posterior(frozenset(),c['ls'],c['p'])!=posterior(frozenset({1}),c['ls'],c['p'])
# One real log-odds dimension can injectively encode an arbitrarily large finite family.
p=(Q(2,3),Q(1,3));ls=[(Q(2**(2**i)),Q(1)) for i in range(5)]
assert len({posterior(frozenset(i for i in range(5) if m>>i&1),ls,p) for m in range(32)})==32
# Multiplying posterior readouts double-counts the prior even for empty evidence sets.
assert N(tuple(x*x for x in p))==(Q(4,5),Q(1,5))!=p
# Nonconstant likelihood can be idempotent when support is not full; excluded by the model.
assert N((Q(1)*Q(1),Q(0)*Q(2)))==(Q(1),Q(0))
# Dependence: two copies of one signal have one likelihood factor.
p=(Q(1,2),Q(1,2));L=(Q(2,3),Q(1,3))
assert N(tuple(a*b for a,b in zip(p,L)))==(Q(2,3),Q(1,3))
assert N(tuple(a*b*b for a,b in zip(p,L)))==(Q(4,5),Q(1,5))
# Informative selection invalidates an otherwise neutral root-only posterior.
selector=(Q(3,4),Q(1,4));neutral=(Q(1,2),Q(1,2))
selected=N(tuple(a*b*c for a,b,c in zip(p,selector,neutral)))
assert selected==(Q(3,4),Q(1,4)) and N(tuple(a*b for a,b in zip(p,neutral)))==p
# Administrative removal recomputes the stipulated store, not the unchanged historical posterior.
historical=N(tuple(a*b for a,b in zip(p,L)))
removed=posterior(frozenset(),[L],p)
assert historical!=removed

# Source custody and author snapshots, with no author-file writes.
source_rows=json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())
for r in source_rows:
 data=(ROOT.parent/r['local']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['blob_sha']
manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
for r in manifest:
 data=(AUTHOR/r['path']).read_bytes()
 assert len(data)==r['bytes']
 assert hashlib.sha256(data).hexdigest()==r['sha256']
expected=json.loads((AUTHOR/'CONTROL_RESULTS.json').read_text())
replayed=json.loads((ROOT/'AUTHOR_REPLAY.json').read_text())
assert replayed==expected
out={'status':'PASS','method':'independent paired-state BFS using exact rational posterior readouts',
 'pairs_checked':pairs,'overlap_pairs_checked':merges,'finite_cases':rows,
 'additional_controls':['inverse-factor collision','rank-one injective readout','prior double-counting',
 'full-support necessity','dependent duplicate','informative selection','administrative removal is not historical deconditioning'],
 'source_blobs_verified':len(source_rows),'author_manifest_entries_verified':len(manifest),
 'author_replay_equals_recorded_output':True,
 'proof_scope':'finite controls supplement written general proof review; no kernel certification'}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
