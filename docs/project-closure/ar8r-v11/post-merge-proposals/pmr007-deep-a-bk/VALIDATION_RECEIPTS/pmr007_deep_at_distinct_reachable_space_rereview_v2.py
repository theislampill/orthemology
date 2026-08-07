#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
RECEIPT=ROOT/"PMR-007_DEEP_AT_V2_FROZEN_HASHES.sha256"
ALPH=((0,0),(0,1),(1,0),(1,1))

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def row_mul(v,M):return tuple(sum(v[i]*M[i][j] for i in range(len(v))) for j in range(len(M[0])))
def dot(v,w):return sum(a*b for a,b in zip(v,w))

def add_basis(basis,v):
    v=list(v)
    for pivot,b in sorted(basis.items()):
        if v[pivot]:
            c=v[pivot]
            v=[x-c*y for x,y in zip(v,b)]
    pivot=next((i for i,x in enumerate(v) if x),None)
    if pivot is None:return False,None
    c=v[pivot];v=[x/c for x in v]
    # canonical reduced pivot in old rows
    for p,b in list(basis.items()):
        if b[pivot]:
            c2=b[pivot];basis[p]=tuple(x-c2*y for x,y in zip(b,v))
    basis[pivot]=tuple(v)
    return True,tuple(v)

def blockdiag(A,B):
    na=len(A);nb=len(B)
    rows=[]
    for r in A:rows.append(tuple(r)+tuple(Fraction(0) for _ in range(nb)))
    for r in B:rows.append(tuple(Fraction(0) for _ in range(na))+tuple(r))
    return tuple(rows)

def reachable_equiv(A,R):
    a0,Am=A;r0,Rm=R
    alpha=tuple(a0)+tuple(-x for x in r0)
    beta=tuple(Fraction(1) for _ in range(len(alpha)))
    mats={x:blockdiag(Am[x],Rm[x]) for x in ALPH}
    basis={};ok,v=add_basis(basis,alpha);queue=[(v,0)] if ok else []
    maxlen=0
    while queue:
        b,l=queue.pop(0);maxlen=max(maxlen,l)
        for x in ALPH:
            nv=row_mul(b,mats[x]);new,canon=add_basis(basis,nv)
            if new:queue.append((canon,l+1))
    equiv=all(dot(b,beta)==0 for b in basis.values())
    return equiv,len(basis),maxlen

def random_model(rng):
    vals=[Fraction(0),Fraction(1,2),Fraction(1)]
    p=rng.choice(vals);alpha=(p,1-p)
    e=[rng.choice(vals) for _ in range(2)]
    mats={}
    for u in (0,1):
      T=[]
      for s in range(2):
        q=rng.choice(vals);T.append((q,1-q))
      for o in (0,1):
        M=[]
        for s in range(2):
          M.append(tuple(T[s][sp]*(e[sp] if o else 1-e[sp]) for sp in range(2)))
        mats[(u,o)]=tuple(M)
    return alpha,mats

def word_probs(M,maxh):
    alpha,mats=M;front={():alpha};res={():Fraction(1)}
    for _ in range(maxh):
      new={}
      for w,v in front.items():
       for x in ALPH:
        vv=row_mul(v,mats[x]);ww=w+(x,);new[ww]=vv;res[ww]=sum(vv)
      front=new
    return res

def det_models():
 for tb in range(16):
  nxt=tuple(tuple((tb>>(s*2+a))&1 for a in range(2)) for s in range(2))
  for ob in range(4):
   out=tuple((ob>>s)&1 for s in range(2))
   for init in range(2):yield(init,nxt,out)
def det_sig(m,maxh):
 init,nxt,out=m;res={}
 for k in range(maxh+1):
  for acts in product((0,1),repeat=k):
   s=init;obs=[]
   for a in acts:s=nxt[s][a];obs.append(out[s])
   res[acts]=tuple(obs)
 return res

def simulate_policy(m,policy,horizon):
 init,nxt,out=m;s=init;obs=();acts=[]
 for t in range(horizon):
  a=policy[(t,obs)];acts.append(a);s=nxt[s][a];obs=obs+(out[s],)
 return tuple(acts),obs

def main():
 fail=[];counts={"frozen_files":0,"hash_mismatches":0,"random_model_pairs":0,"reachable_space_cases":0,
                 "bound_comparison_cases":0,"distinct_trace_equivalent_pair_controls":0,
                 "adaptive_policies_checked":0,"delayed_witness_controls":0,"failures":0}
 for line in RECEIPT.read_text().splitlines():
  exp,rel=line.split(maxsplit=1);p=ROOT/rel;counts["frozen_files"]+=1
  if sha(p)!=exp:fail.append({"kind":"hash","path":rel});counts["hash_mismatches"]+=1
 rng=random.Random(20260806)
 for t in range(200):
  A,R=random_model(rng),random_model(rng)
  eq,dim,maxlen=reachable_equiv(A,R)
  pa,pr=word_probs(A,5),word_probs(R,5)
  bound_eq=all(pa[w]==pr[w] for w in pa if len(w)<=3)
  long_eq=all(pa[w]==pr[w] for w in pa)
  if eq!=long_eq or bound_eq!=long_eq or maxlen>3:
   fail.append({"kind":"reachable_bound","trial":t,"eq":eq,"bound":bound_eq,"long":long_eq,"dim":dim,"maxlen":maxlen})
  counts["random_model_pairs"]+=1;counts["reachable_space_cases"]+=1;counts["bound_comparison_cases"]+=1
 # Find a distinct deterministic pair with the same complete trace signature.
 mods=list(det_models());groups={}
 for idx,m in enumerate(mods):
  key=tuple(det_sig(m,7).items());groups.setdefault(key,[]).append(idx)
 pair=next((v[:2] for v in groups.values() if len(v)>=2 and mods[v[0]]!=mods[v[1]]),None)
 if pair is None:fail.append({"kind":"no_distinct_equivalent_pair"})
 else:
  i,j=pair;counts["distinct_trace_equivalent_pair_controls"]+=1
  # enumerate all deterministic policies through horizon 3: actions at root, 2 length-1 histories, 4 length-2 histories
  histories=[(0,()),*( (1,(o,)) for o in (0,1)),*( (2,(a,b)) for a,b in product((0,1),repeat=2))]
  for bits in product((0,1),repeat=len(histories)):
   pol={h:b for h,b in zip(histories,bits)}
   if simulate_policy(mods[i],pol,3)!=simulate_policy(mods[j],pol,3):
    fail.append({"kind":"adaptive_policy","pair":pair});break
   counts["adaptive_policies_checked"]+=1
 # delayed witness from repaired primary
 mA=(1,((1,1),(0,1),(2,1)),(1,1,1));mR=(1,((0,2),(0,0),(1,1)),(1,0,1))
 sA,sR=det_sig(mA,3),det_sig(mR,3)
 eq2=all(sA[a]==sR[a] for a in sA if len(a)<=2);eq3=all(sA[a]==sR[a] for a in sA if len(a)<=3)
 if not eq2 or eq3:fail.append({"kind":"delayed_witness"})
 counts["delayed_witness_controls"]+=1
 counts["failures"]=len(fail)
 res={"identity":"PMR-007-NIBE-1","rereview":"distinct reachable-row-space linear algebra and adaptive-policy semantics",
      "counts":counts,"failures":fail[:20],"result":"PASS" if not fail else "FAIL",
      "scope_notes":["finite controlled weighted systems","common candidate-independent policies","registered trace algebra only","ontology and source truth not inferred"]}
 OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n");print(json.dumps(res,indent=2,sort_keys=True));return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
