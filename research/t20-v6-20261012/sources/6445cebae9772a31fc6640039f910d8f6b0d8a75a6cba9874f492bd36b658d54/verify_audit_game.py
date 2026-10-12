#!/usr/bin/env python3
"""Exact saddle points of the promised modal-cut audit game.

The adversary selects a formal countermodel, not metaphysical reality.
Pure auditors query b of m blockers and choose a default for an all-negative
transcript. Any positive reply correctly reports failure of necessity.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def main():
    rows=[]; entries=0; checks=0
    for m in range(1,10):
        for b in range(m+1):
            questions=list(combinations(range(m),b))
            val=F(m,2*m-b); alpha=val
            adversary=[F(m-b,2*m-b)]+[F(1,2*m-b)]*m
            strategies=[(set(q),d) for q in questions for d in (0,1)]
            mix=[(alpha if d else 1-alpha)/len(questions) for q,d in strategies]
            payoff=[]
            for q,d in strategies:
                row=[F(d)] + [F(1 if h in q else 1-d) for h in range(m)]
                payoff.append(row); entries+=len(row)
            assert sum(mix)==1 and sum(adversary)==1
            for row in payoff:
                assert sum(a*v for a,v in zip(adversary,row))==val
                checks+=1
            for j in range(m+1):
                assert sum(p*row[j] for p,row in zip(mix,payoff))==val
                checks+=1
            rows.append({'m':m,'budget':b,'value':str(val),
                         'necessary_default_probability':str(alpha),
                         'adversary_safe_probability':str(adversary[0]),
                         'pure_auditor_strategies':len(strategies),'status':'PASS'})
    out={'status':'PASS','games':len(rows),'payoff_entries':entries,
         'exact_best_response_equalities':checks,'instances':rows,
         'scope':'promised family consisting of the safe absence complex and one added minimal cut; exact rational arithmetic'}
    (Path(__file__).resolve().parent/'audit_game_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='instances'},indent=2))

if __name__=='__main__': main()
