#!/usr/bin/env python3
"""Exact controls for a uniform-response approximation obstruction."""
from fractions import Fraction as F
from pathlib import Path
import json
families={}
def check(k,b):
    if not b:raise AssertionError(k)
    families[k]=families.get(k,0)+1

def bound(N):return F(N**N,(N+1)**(N+1))

for N in range(1,65):
    tstar=F(N,N+1);maximum=bound(N)
    check('exact_maximizer',tstar**N*(1-tstar)==maximum)
    check('uniform_upper_bound',maximum<F(1,N+1))
    check('stationary_at_maximum',N-(N+1)*tstar==0)
    for t in [F(j,16) for j in range(17)]+[tstar]:
        u=t**N;a=1-u;ra=1-t
        gap=u*(1-t)
        check('uniform_gap_grid',0<=gap<=maximum)
        check('calibration_inverse_parameter',(1-ra)**N==1-a)
        derivative=N-(N+1)*t
        check('maximizer_derivative_sign',(derivative>0)==(t<tstar) and (derivative<0)==(t>tstar))
        for b in [F(j,8) for j in range(9)]:
            q0=u;qn=u*(1-b+b*t)
            check('independent_route_law',qn==(1-ra)**N*(1-ra*b))
            check('response_gap_identity',q0-qn==b*u*(1-t))
            check('uniform_square_bound',0<=q0-qn<=maximum)
            check('probability_range',0<=qn<=q0<=1)
            derivative_a=(1-b)+b*F(N+1,N)*t
            derivative_b=u*(1-t)
            check('common_response_coordinate_bounds',0<=derivative_a<=2 and 0<=derivative_b<=1)
            if 0<t<1 and b>0:
                check('positive_interaction_still_exactly_visible',qn/u==1-ra*b<1)
    for b in [F(0),F(1,3),F(1)]:
        check('a_zero_face',F(1)*(1-b+b)==1)
        check('a_one_face',F(0)*(1-b)==0)
    for a in [F(0),F(1,3),F(1)]:
        check('b_zero_face',(1-a)*(1-F(0))==1-a)
    # Calibration endpoint separation at commands tending to one.
    a=1-F(1,2)**N
    check('no_common_hidden_modulus',(1-a)==F(1,2)**N and F(1,2)/(1-a)==2**(N-1))

# A computable fixed alternative name, including its fine-precision branch.
def root_interval(u,N,bits):
    lo,hi=F(0),F(1)
    for _ in range(bits):
        mid=(lo+hi)/2;power=mid**N
        if power==u:return mid,mid
        if power<u:lo=mid
        else:hi=mid
    return lo,hi

def name(N,a,b,eps):
    if eps>F(1,N+1):return 1-a,'coarse'
    u=1-a;bits=1
    while True:
        lo,hi=root_interval(u,N,bits)
        qlo=u*(1-b+b*lo);qhi=u*(1-b+b*hi)
        if qhi-qlo<=eps:return (qlo+qhi)/2,'fine'
        bits*=2

for N in [1,2,3,8]:
    for t in [F(0),F(1,7),F(2,5),F(1)]:
        a=1-t**N
        for b in [F(0),F(2,7),F(1)]:
            true=(1-a)*(1-b+b*t)
            for eps in [F(1,2),F(1,16),F(1,256)]:
                response,branch=name(N,a,b,eps)
                check('fixed_total_name_validity',abs(response-true)<=eps)
                check('name_branch_contract',(branch=='coarse')==(eps>F(1,N+1)))

# Illustrative adaptive finite transcripts. These are controls, not an enumeration
# of all decision algorithms; the proof in RESULT.md handles arbitrary protocols.
def transcript(seed,oracle):
    state=seed+1;rows=[]
    for depth in range(9):
        mode=(state+depth)%5
        a=F(0) if mode==0 else F(1) if mode==1 else F(state%23+1,25)
        b=F(0) if mode==2 else F(1) if mode==3 else F((state*3)%19+1,21)
        eps=F(1,2**(depth+2)+(state%17))
        reply=oracle(a,b,eps)
        rows.append((a,b,eps,reply))
        state=reply.numerator+3*reply.denominator+seed+depth
        if depth>=2 and ((state+seed)%5==0 or depth==8):break
    output='present' if seed%8==0 else 'absent'
    return rows,output

base=lambda a,b,eps:1-a
transcripts=[]
for seed in range(64):
    rows,output=transcript(seed,base);emin=min(r[2] for r in rows)
    N=emin.denominator//emin.numerator+1
    check('finite_transcript_slack',F(1,N+1)<emin)
    alt=lambda a,b,eps,N=N:name(N,a,b,eps)[0]
    alternative=transcript(seed,alt)
    check('adaptive_transcript_identity',alternative==(rows,output))
    for a,b,eps,reply in rows:
        check('all_queried_locations_covered',bound(N)<eps and reply==1-a)
    transcripts.append((rows,output))
# One fixed oracle works simultaneously for a positive-probability seed event.
chosen=[rows for rows,output in transcripts if output=='absent']
threshold=min(row[2] for rows in chosen for row in rows)
N=threshold.denominator//threshold.numerator+1
copies=0
for seed,(rows,output) in enumerate(transcripts):
    if output=='absent':
        check('fixed_oracle_independent_of_seed',transcript(seed,lambda a,b,eps:name(N,a,b,eps)[0])==(rows,output))
        copies+=1
check('bounded_error_event_transfer',F(copies,len(transcripts))==F(7,8)>F(1,4))

out={'status':'PASS','arithmetic':'Exact integers, Fraction values, and rational root intervals; no floating-point signs or sampled data',
     'assertions':sum(families.values()),'families':families,
     'scope':'Finite deterministic diagnostics for the general written proof; transcript and seed controls do not enumerate arbitrary protocols.'}
p=Path(__file__).parent/'results'/'exact_controls.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
