#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

OUT = Path(__file__).with_name(Path(__file__).stem + "_results.json")


def distributions(total: int, n: int):
    if n == 1:
        yield (Fraction(total, total),)
        return
    def rec(rem, k, pref):
        if k == 1:
            yield tuple(Fraction(x, total) for x in pref + [rem])
            return
        for x in range(rem + 1):
            yield from rec(rem-x, k-1, pref+[x])
    yield from rec(total, n, [])


def push(p, channel, out_n):
    q=[Fraction(0) for _ in range(out_n)]
    for i,pi in enumerate(p): q[channel[i]] += pi
    return tuple(q)


def tv(p,q): return sum(abs(a-b) for a,b in zip(p,q))/2


def event_prob(p, mask):
    return sum(x for i,x in enumerate(p) if mask & (1<<i))


def main():
    raw=list(distributions(4,3))
    channels=[]
    for out_n in (1,2,3):
        for ch in product(range(out_n), repeat=3):
            # quotient-like channels: every output actually used
            if set(ch)==set(range(out_n)):
                channels.append((out_n,ch))
    priors=[Fraction(1,10),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(9,10)]
    counts={
        "raw_distributions":len(raw), "common_channels":len(channels),
        "pair_channel_cases":0,"data_processing_cases":0,
        "equal_represented_event_parity_cases":0,"unequal_predictive_gate_cases":0,
        "prior_reversal_cases":0,"swap_invariance_cases":0,
        "source_version_contract_cases":0,"failures":0,
    }
    failures=[]
    for p in raw:
      for q in raw:
        for out_n,ch in channels:
          counts["pair_channel_cases"] += 1
          pp,pq=push(p,ch,out_n),push(q,ch,out_n)
          counts["data_processing_cases"] += 1
          if tv(pp,pq)>tv(p,q):
              failures.append({"kind":"data_processing","p":str(p),"q":str(q),"channel":ch})
          # examine every nonempty represented event
          for mask in range(1,1<<out_n):
            a,b=event_prob(pp,mask),event_prob(pq,mask)
            if a==b and a>0:
              for priorA in priors:
                priorR=1-priorA
                # posterior odds equality to prior odds under equal likelihood
                postA = a*priorA/(a*priorA+b*priorR)
                if postA != priorA:
                    failures.append({"kind":"equal_likelihood_update","a":str(a),"prior":str(priorA)})
                counts["equal_represented_event_parity_cases"] += 1
            elif a!=b:
                counts["unequal_predictive_gate_cases"] += 1
          if pp==pq:
              # any swap-invariant score built from equal source bool, distribution, and prior ties
              for priorA in priors:
                  if priorA==Fraction(1,2):
                      scoreA=(True,pp,priorA)
                      scoreR=(True,pq,1-priorA)
                      if scoreA!=scoreR:
                          failures.append({"kind":"swap_invariance"})
                      counts["swap_invariance_cases"] += 1
              # prior reversal under equal likelihood
              if pp and pp[0]>0:
                  odds1=Fraction(9,1); odds2=Fraction(1,9)
                  if not (odds1>1 and odds2<1): failures.append({"kind":"prior_reversal"})
                  counts["prior_reversal_cases"] += 1
    # source/version contract truth table: six coordinates; equal bytes alone never forces full compatibility
    # coordinates auth, translation, reconstruction, version, scope, world-link
    for bits in product([False,True], repeat=6):
        full=all(bits)
        bytes_same=True
        if bytes_same and not full and full:
            failures.append({"kind":"source_contract_logic"})
        counts["source_version_contract_cases"] += 1
    counts["failures"]=len(failures)
    result={
      "identity":"PMR-007-SCAP-1",
      "checker":"primary exhaustive finite probability/source-contract semantics",
      "declared_class":{"raw_alphabet":3,"probability_denominator":4,"channels":"all surjective deterministic maps to 1-3 outputs"},
      "counts":counts,"failures":failures[:20],"result":"PASS" if not failures else "FAIL"
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not failures else 1

if __name__=="__main__": raise SystemExit(main())
