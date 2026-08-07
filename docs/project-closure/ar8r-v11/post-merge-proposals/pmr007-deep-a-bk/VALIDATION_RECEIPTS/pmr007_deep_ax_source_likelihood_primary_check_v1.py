from fractions import Fraction
from itertools import product
import json, random
from pathlib import Path

OUT = Path(__file__).with_name(Path(__file__).stem + '_results.json')


def tv(p,q):
    return sum(abs(a-b) for a,b in zip(p,q))/2

# Independent binary-root cases with exact arithmetic.
vals=[Fraction(i,5) for i in range(1,5)]
independent_cases=0
independent_failures=0
posterior_parity_cases=0
posterior_parity_failures=0
for pA0,pR0,pA1,pR1 in product(vals, repeat=4):
    for y0,y1 in product([0,1], repeat=2):
        independent_cases += 1
        pa0 = pA0 if y0 else 1-pA0
        pr0 = pR0 if y0 else 1-pR0
        pa1 = pA1 if y1 else 1-pA1
        pr1 = pR1 if y1 else 1-pR1
        jointA=pa0*pa1; jointR=pr0*pr1
        L_joint=jointA/jointR
        L_prod=(pa0/pr0)*(pa1/pr1)
        if L_joint != L_prod:
            independent_failures += 1
        if pA0==pR0 and pA1==pR1:
            posterior_parity_cases += 1
            if L_joint != 1:
                posterior_parity_failures += 1

# Exact duplicated-root control: (Y,Y) has the same LR as Y.
duplicate_cases=0
duplicate_failures=0
for pA,pR in product(vals,repeat=2):
    for y in [0,1]:
        duplicate_cases += 1
        pa=pA if y else 1-pA; pr=pR if y else 1-pR
        # Joint probability of exact duplicate is just probability of the root symbol.
        if (pa/pr) != (pa/pr):
            duplicate_failures += 1

# Exhaustive small joint tables: record where product of marginals is not the joint LR.
# Integer weights 1..3 over four outcomes, normalized.
correlated_tables=0
naive_product_mismatches=0
minimal_mismatches=[]
weights=list(product(range(1,4),repeat=4))
for wa in weights:
    sa=sum(wa); PA=[Fraction(x,sa) for x in wa]
    for wr in weights:
        sr=sum(wr); PR=[Fraction(x,sr) for x in wr]
        correlated_tables += 1
        # marginals for first and second bit
        PA0=[PA[0]+PA[1],PA[2]+PA[3]]
        PA1=[PA[0]+PA[2],PA[1]+PA[3]]
        PR0=[PR[0]+PR[1],PR[2]+PR[3]]
        PR1=[PR[0]+PR[2],PR[1]+PR[3]]
        for idx,(b0,b1) in enumerate(product([0,1],repeat=2)):
            exact=PA[idx]/PR[idx]
            naive=(PA0[b0]/PR0[b0])*(PA1[b1]/PR1[b1])
            if exact != naive:
                naive_product_mismatches += 1
                if len(minimal_mismatches)<8:
                    minimal_mismatches.append({
                        'PA':[str(x) for x in PA], 'PR':[str(x) for x in PR],
                        'outcome':[b0,b1], 'exact':str(exact), 'naive':str(naive)
                    })

# Common binary stochastic translation channels contract TV.
channel_cases=0
channel_failures=0
for pA,pR,k00,k10 in product(vals, repeat=4):
    # P(Y=1)=p; channel gives P(Z=1|Y=0)=k00, P(Z=1|Y=1)=k10
    rawA=[1-pA,pA]; rawR=[1-pR,pR]
    zA=[rawA[0]*(1-k00)+rawA[1]*(1-k10),rawA[0]*k00+rawA[1]*k10]
    zR=[rawR[0]*(1-k00)+rawR[1]*(1-k10),rawR[0]*k00+rawR[1]*k10]
    channel_cases += 1
    if tv(zA,zR)>tv(rawA,rawR):
        channel_failures += 1

res={
 'schema':'pmr007-deep-ax-source-likelihood-primary-check-v1-results',
 'independent_cases':independent_cases,
 'independent_failures':independent_failures,
 'posterior_parity_cases':posterior_parity_cases,
 'posterior_parity_failures':posterior_parity_failures,
 'duplicate_cases':duplicate_cases,
 'duplicate_failures':duplicate_failures,
 'correlated_joint_table_pairs':correlated_tables,
 'naive_product_mismatches':naive_product_mismatches,
 'minimal_naive_product_mismatches':minimal_mismatches,
 'translation_channel_cases':channel_cases,
 'translation_channel_failures':channel_failures,
 'overall':'PASS_WITH_EXPECTED_CORRELATION_COUNTEREXAMPLES' if independent_failures==posterior_parity_failures==duplicate_failures==channel_failures==0 and naive_product_mismatches>0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
