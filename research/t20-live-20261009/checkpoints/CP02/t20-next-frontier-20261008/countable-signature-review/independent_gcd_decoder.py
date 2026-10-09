"""Factorization-free independent decoder using an LCM prime-support history.

This differs from the proposed product-history implementation. All arithmetic
is exact; no primality testing or integer factorization is called.
"""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json
import random

ROOT=Path(__file__).resolve().parent


def probability(counts):
    q=F(1)
    for exponent,count in counts.items():
        q*=F(4**exponent-1,4**exponent)**count
    return q


def decode(q):
    if not isinstance(q,F) or not 0<q<=1:
        raise ValueError('Positive exact probability required.')
    denominator=q.denominator
    weight=0
    while denominator%4==0:
        denominator//=4
        weight+=1
    if denominator!=1:
        raise ValueError('Non-model denominator.')
    history=1
    uncovered=q.numerator
    selectors={}
    operation_count=0
    maximum_history_bits=1
    for exponent in range(1,weight+1):
        if uncovered==1:
            break
        whole=4**exponent-1
        private=whole
        while (common:=gcd(private,history))>1:
            private//=common
            operation_count+=1
        assert private>1
        assert whole%private==0
        assert gcd(private,history)==1
        assert gcd(private,whole//private)==1
        selectors[exponent]=(whole,private)
        history=lcm(history,whole)
        maximum_history_bits=max(maximum_history_bits,history.bit_length())
        while (common:=gcd(uncovered,whole))>1:
            uncovered//=common
            operation_count+=1
    if uncovered!=1:
        raise ValueError('Numerator has unrecognized prime support.')
    residual=q.numerator
    answer={}
    for exponent in sorted(selectors,reverse=True):
        whole,private=selectors[exponent]
        test=residual
        count=0
        while test%private==0:
            test//=private
            count+=1
            operation_count+=1
        if count:
            divisor=whole**count
            if residual%divisor:
                raise ValueError('Inconsistent full factor multiplicity.')
            residual//=divisor
            answer[exponent]=count
    if residual!=1 or sum(e*n for e,n in answer.items())!=weight or probability(answer)!=q:
        raise ValueError('Reconstruction failed.')
    return answer,{'stopping_exponent':max(selectors,default=0),'weighted_count':weight,'successful_gcd_or_power_divisions':operation_count,'maximum_history_bits':maximum_history_bits,'explicit_readout_bits':q.numerator.bit_length()+q.denominator.bit_length()}


if __name__=='__main__':
    rng=random.Random(900808)
    examples=[{}, {32:1},{1:1000},{3:9,12:3,24:2},{16:2,1:3}]
    for _ in range(50):
        counts={e:count for e in range(1,33) if (count:=rng.randrange(3))}
        examples.append(counts)
    traces=[]
    for counts in examples:
        recovered,trace=decode(probability(counts))
        assert recovered==counts
        assert trace['stopping_exponent']==max(counts,default=0)
        traces.append(trace)
    for q in (F(0),F(2),F(1,2),F(1,4),F(3,16),F(5,16),F(7,64)):
        try:
            decode(q)
        except ValueError:
            pass
        else:
            raise AssertionError(('Invalid readout accepted',q))
    receipt={'model_reconstructions':len(examples),'algorithm':'LCM history, repeated gcd stripping, descending composite-power extraction; no factorization or primality testing.','traces':traces}
    (ROOT/'GCD_DECODER_METRICS.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'model_reconstructions':len(examples),'maximum_tested_support_code':32,'high_multiplicity_trace':traces[2],'algorithm':receipt['algorithm']},indent=2))
