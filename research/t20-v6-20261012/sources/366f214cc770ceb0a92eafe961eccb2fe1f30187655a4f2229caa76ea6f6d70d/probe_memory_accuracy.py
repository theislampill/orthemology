"""Exact stationary-error controls; mean accuracy does not imply coBuchi."""
from fractions import Fraction as F
import json
from restoration import classify_chain


def sticky_chain(states,p,epsilon):
    L=states-1;out={}
    for i in range(states):
        row={}
        if i==0:
            row={0:1-epsilon*p,1:epsilon*p}
        elif i==L:
            row={L-1:epsilon*(1-p),L:1-epsilon*(1-p)}
        else:row={i-1:1-p,i+1:p}
        out[i]={j:v for j,v in row.items() if v}
    return out


def stationary(states,p,epsilon):
    r=p/(1-p);L=states-1
    weights={i:(r**i if i in (0,L) else epsilon*r**i) for i in range(states)}
    total=sum(weights.values());return {i:w/total for i,w in weights.items()}


def optimal_bayes_error(pi_p,pi_q):
    return sum(min(pi_p[i],pi_q[i]) for i in pi_p)/2


def run():
    examples=[];checked=0
    for S in range(2,22):
        for epsilon in (F(1),F(1,2),F(1,10),F(1,100),F(1,1000)):
            laws=[]
            for p in (F(2,3),F(1,3)):
                kernel=sticky_chain(S,p,epsilon);pi=stationary(S,p,epsilon)
                assert all(sum(pi[i]*kernel[i].get(j,F(0)) for i in pi)==pi[j] for j in pi)
                # Even just the wrong endpoint is recurrent, so eventual correct
                # decisions fail under either hypothesis for any threshold rule.
                wrong={0 if p>F(1,2) else S-1}
                verdict=classify_chain(kernel,{S//2},wrong)
                assert not verdict['almost_sure']
                laws.append(pi);checked+=1
            error=optimal_bayes_error(*laws);bound=F(1,1+2**(S-1))
            assert error>=bound
            if S==3:assert error==(1+epsilon)/(5+2*epsilon)
            examples.append({'states':S,'epsilon':str(epsilon),'stationary_bayes_error':str(error),
                'epsilon_to_zero_limit':str(bound),'restoration_probability_each_hypothesis':'0'})
    # With epsilon=0 and initial state 1, the S=3 rule samples once and freezes.
    for p in (F(2,3),F(1,3)):
        k=sticky_chain(3,p,F(0));law={1:F(1)}
        for _ in range(12):
            law={j:sum(v*k[i].get(j,F(0)) for i,v in law.items()) for j in range(3)}
            wrong=0 if p>F(1,2) else 2
            assert law[wrong]==F(1,3)
    result={'stationary_laws_and_bad_BSCCs_checked':checked,'score_examples':examples,
        'singular_limit':{'states':3,'initial_state':1,
            'first_time_then_epsilon_error':'1/5','first_epsilon_then_time_error':'1/3'},
        'mismatches':0,'scope':'Exact fixed-machine calculations; no proof of the classical universal optimality lower bound is implemented.'}
    with open('memory_accuracy_results.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='score_examples'},indent=2))

if __name__=='__main__':run()
