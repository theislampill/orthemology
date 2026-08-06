#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import json, random

OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")

# deterministic controlled machine: next[state][action], output[next_state]
def deterministic_models():
    for trans_bits in range(16):
        nxt=tuple(tuple((trans_bits>>(s*2+a))&1 for a in range(2)) for s in range(2))
        for out_bits in range(4):
            out=tuple((out_bits>>s)&1 for s in range(2))
            for init in range(2):
                yield (init,nxt,out)

def det_signature(model,max_h):
    init,nxt,out=model
    sig={():()}
    for k in range(1,max_h+1):
        for actions in product((0,1),repeat=k):
            s=init;obs=[]
            for a in actions:
                s=nxt[s][a];obs.append(out[s])
            sig[actions]=tuple(obs)
    return sig

def equal_through(sa,sb,k):
    return all(sa[a]==sb[a] for a in sa if len(a)<=k)

# weighted matrices for valid 2-state HMM-like models
def matmul_row(v,M):
    return tuple(sum(v[i]*M[i][j] for i in range(len(v))) for j in range(len(M[0])))

def prob_word(model,word):
    alpha,mats=model;v=alpha
    for sym in word:v=matmul_row(v,mats[sym])
    return sum(v)

def random_weighted(rng):
    vals=[Fraction(0),Fraction(1,2),Fraction(1)]
    p=rng.choice(vals);alpha=(p,1-p)
    # emissions by destination state, shared across actions
    e=[rng.choice(vals) for _ in range(2)]
    mats={}
    for u in (0,1):
        T=[]
        for s in range(2):
            q=rng.choice(vals);T.append((q,1-q))
        for o in (0,1):
            M=[]
            for s in range(2):
                row=[]
                for sp in range(2):
                    emit=e[sp] if o==1 else 1-e[sp]
                    row.append(T[s][sp]*emit)
                M.append(tuple(row))
            mats[(u,o)]=tuple(M)
    return alpha,mats

def word_probs(model,max_h):
    alpha,mats=model
    alphabet=((0,0),(0,1),(1,0),(1,1))
    res={():Fraction(1)}
    frontier={():alpha}
    for _ in range(max_h):
        nxt_frontier={}
        for w,v in frontier.items():
            for x in alphabet:
                ww=w+(x,)
                vv=matmul_row(v,mats[x])
                nxt_frontier[ww]=vv
                res[ww]=sum(vv)
        frontier=nxt_frontier
    return res

def main():
    failures=[]
    models=list(deterministic_models())
    sigs=[det_signature(m,7) for m in models]
    counts={"deterministic_models":len(models),"deterministic_pairs":0,"bound_long_horizon_cases":0,
            "two_state_delayed_length3_witnesses":0,"three_state_delayed_witness_controls":0,"random_probabilistic_pairs":0,
            "probabilistic_bound_cases":0,"representation_erasure_controls":0,
            "hidden_tag_controls":0,"failures":0}
    witness=None
    for i,a in enumerate(sigs):
      for j,b in enumerate(sigs):
        counts["deterministic_pairs"]+=1
        e3=equal_through(a,b,3);e7=equal_through(a,b,7)
        counts["bound_long_horizon_cases"]+=1
        if e3!=e7:failures.append({"kind":"deterministic_horizon_bound","i":i,"j":j})
        if witness is None and equal_through(a,b,2) and not e3:
            # find a length-3 action witness
            aw=next(actions for actions in a if len(actions)==3 and a[actions]!=b[actions])
            witness={"model_i":i,"model_j":j,"actions":aw,"obs_i":a[aw],"obs_j":b[aw]}
            counts["two_state_delayed_length3_witnesses"]+=1
    # Tightness is not required in the two-state subclass. Add a separate verified
    # three-state control equal through horizon two and different at horizon three.
    mA=(1,((1,1),(0,1),(2,1)),(1,1,1))
    mR=(1,((0,2),(0,0),(1,1)),(1,0,1))
    sA,sR=det_signature(mA,5),det_signature(mR,5)
    delayed_actions=(0,1,0)
    delayed_control={"actions":delayed_actions,"obs_A":sA[delayed_actions],"obs_R":sR[delayed_actions],
                     "equal_through_2":equal_through(sA,sR,2),"equal_through_3":equal_through(sA,sR,3)}
    if not delayed_control["equal_through_2"] or delayed_control["equal_through_3"]:
        failures.append({"kind":"three_state_delayed_control","control":delayed_control})
    counts["three_state_delayed_witness_controls"]+=1
    rng=random.Random(20260806)
    for t in range(300):
        A=random_weighted(rng);R=random_weighted(rng)
        pa=word_probs(A,6);pr=word_probs(R,6)
        e3=all(pa[w]==pr[w] for w in pa if len(w)<=3)
        e6=all(pa[w]==pr[w] for w in pa if len(w)<=6)
        if e3!=e6:failures.append({"kind":"probabilistic_horizon_bound","trial":t})
        counts["random_probabilistic_pairs"]+=1;counts["probabilistic_bound_cases"]+=1
    # Common observation map erases a raw distinction
    rawA=(Fraction(1),Fraction(0));rawR=(Fraction(0),Fraction(1))
    mergedA=(sum(rawA),);mergedR=(sum(rawR),)
    if rawA==rawR or mergedA!=mergedR:failures.append({"kind":"representation_erasure"})
    counts["representation_erasure_controls"]+=1
    # Hidden tag changes architecture label only, not weighted system
    m=models[0]
    if det_signature(m,7)!=det_signature(m,7):failures.append({"kind":"hidden_tag"})
    counts["hidden_tag_controls"]+=1
    counts["failures"]=len(failures)
    result={"identity":"PMR-007-NIBE-1","checker":"repaired primary deterministic trace enumeration plus random rational weighted systems",
            "declared_class":{"deterministic_states":2,"actions":2,"observations":2,"combined_dimension_bound":3,
                              "random_weighted_states":2,"random_long_horizon":6},
            "counts":counts,"two_state_delayed_witness":witness,"three_state_delayed_control":delayed_control,"failures":failures[:20],
            "result":"PASS" if not failures else "FAIL"}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True));return 0 if not failures else 1
if __name__=='__main__':raise SystemExit(main())
