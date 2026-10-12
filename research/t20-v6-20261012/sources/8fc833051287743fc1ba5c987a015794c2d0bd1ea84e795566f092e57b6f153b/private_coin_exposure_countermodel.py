"""A concrete finite controller realization that fails after private-memory exposure.

Plant: P (prediction phase), Q0/Q1 (locked adversarial prediction), G (good sink).
Observations: P, Q, G, hiding the 0/1 prediction in Q. Controller has a private
fair bit r sampled initially and on every return to P. At P it says wait; the
adversary then chooses Qh. At Qh the controller responds r. If r != h, go to G;
otherwise return to P, refreshing the private bit. No choice is available to the
adversary after the response. Every state except G is bad.

A source adversary sees full plant/action history, not r. At every P the new r
is conditionally fair and independent of that history. Thus every such history
policy leaves a 1/2 chance of reaching G in that round: AS reach G follows.
For executable finite-chain evidence we show h=0 and h=1. An exposed destination
adversary reads r at P and chooses h=r. The physical plant is identical and all
interface couplings can be identity couplings; the behavior-realization claim,
not the plant refinement or fresh-draw theorem, is what fails.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import json

states=[('P',0),('P',1)]+[(f'Q{h}',r) for h in range(2) for r in range(2)]+[('G',0)]
initial={('P',0):F(1,2),('P',1):F(1,2)}

def kernel(guess):
    K={}
    for s in states:
        phase,r=s
        if phase=='P': K[s]={(f'Q{guess(r)}',r):F(1)}
        elif phase=='G': K[s]={s:F(1)}
        elif int(phase[-1])!=r: K[s]={('G',0):F(1)}
        else: K[s]={('P',0):F(1,2),('P',1):F(1,2)}
        assert sum(K[s].values())==1
    return K

def reachable(K):
    reached=set(initial)
    while True:
        more=reached|{t for s in reached for t in K[s]}
        if more==reached:return reached
        reached=more

def bottom_sccs(K):
    R=reachable(K); reach={s:{s}|set(K[s]) for s in R}
    for _ in range(len(R)):
        reach={s:reach[s]|set().union(*(reach[t] for t in reach[s])) for s in R}
    classes={frozenset(t for t in R if t in reach[s] and s in reach[t]) for s in R}
    return [sorted(C) for C in classes if all(t in C for s in C for t in K[s])]

def distribution(K,n):
    d=initial
    for _ in range(n):
        nxt=defaultdict(F)
        for s,p in d.items():
            for t,q in K[s].items():nxt[t]+=p*q
        d=dict(nxt)
    return d

report={}
for name,guess in [('blind_always_zero',lambda r:0),('blind_always_one',lambda r:1),('memory_revealed_copy',lambda r:r)]:
    K=kernel(guess); bscc=bottom_sccs(K)
    restoration_as=all(all(s[0]=='G' for s in C) for C in bscc)
    prefix=[]
    for n in range(13):
        d=distribution(K,2*n); failure=1-d.get(('G',0),F(0))
        assert failure==(F(1) if name=='memory_revealed_copy' else F(1,2)**n)
        prefix.append(str(failure))
    report[name]={'reachable_states':[list(s) for s in sorted(reachable(K))],
                  'bottom_sccs':[[list(s) for s in C] for C in bscc],
                  'almost_sure_restoration':restoration_as,
                  'probability_not_yet_good_after_n_rounds':prefix}
assert report['blind_always_zero']['almost_sure_restoration']
assert report['blind_always_one']['almost_sure_restoration']
assert not report['memory_revealed_copy']['almost_sure_restoration']
report['claim_ceiling']={
  'source_guarantee':'Every full-plant/action-history nonanticipating adversary blind to the current private seed has roundwise conditional failure 1/2; restoration probability one.',
  'exposed_failure':'Reading the pre-sampled bit before the locked prediction permits perpetual failure with probability one.',
  'fresh_behavioral_controller':'Sample r freshly at Q after prediction is locked. It still wins AS even against memory-visible adversaries; no future coin exists to expose at P.',
  'refuted_upgrade':'Arbitrary randomized finite-memory realizations may not be substituted under a changed memory-exposure contract.',
  'not_refuted':'SR1 behavioral fresh-current-action gluing theorem, or deterministic history-updated finite memory with fresh draws.'}
Path(__file__).with_name('private_coin_exposure_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
