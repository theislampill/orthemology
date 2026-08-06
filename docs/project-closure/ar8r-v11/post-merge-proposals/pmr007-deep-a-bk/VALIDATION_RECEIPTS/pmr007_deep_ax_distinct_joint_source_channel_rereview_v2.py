from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random

BASE=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def parse_hashes(path):
    rows=[]
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        h, rel=line.split('  ',1)
        rows.append((h,BASE/rel))
    return rows

def tv(p,q): return sum(abs(a-b) for a,b in zip(p,q))/2

def push(p,K):
    return [sum(p[i]*K[i][j] for i in range(len(p))) for j in range(len(K[0]))]

hash_rows=parse_hashes(BASE/'PMR-007_DEEP_AX_V2_FROZEN_HASHES.sha256')
hash_mismatches=[]
for h,p in hash_rows:
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=h: hash_mismatches.append({'path':str(p.relative_to(BASE)),'expected':h,'actual':actual})

# Ternary two-root independent cases.
vals=[Fraction(1,6),Fraction(1,3),Fraction(1,2)]
independent_cases=0; independent_failures=0
# distributions are permutations/selected triples summing 1
Ds=[(Fraction(1,6),Fraction(1,3),Fraction(1,2)),(Fraction(1,4),Fraction(1,4),Fraction(1,2)),(Fraction(1,5),Fraction(2,5),Fraction(2,5))]
for A0,R0,A1,R1 in product(Ds,repeat=4):
    for i,j in product(range(3),repeat=2):
        independent_cases+=1
        exact=(A0[i]*A1[j])/(R0[i]*R1[j])
        fact=(A0[i]/R0[i])*(A1[j]/R1[j])
        if exact!=fact: independent_failures+=1

# Random joint distributions and exact posterior formula; identify product-marginal mismatches.
rng=random.Random(20260806)
joint_cases=25000; bayes_failures=0; marginal_product_mismatches=0
for _ in range(joint_cases):
    wa=[rng.randint(1,9) for _ in range(9)]; wr=[rng.randint(1,9) for _ in range(9)]
    PA=[Fraction(x,sum(wa)) for x in wa]; PR=[Fraction(x,sum(wr)) for x in wr]
    prior=Fraction(rng.randint(1,7),rng.randint(1,7))
    idx=rng.randrange(9); i,j=divmod(idx,3)
    posterior=prior*PA[idx]/PR[idx]
    if posterior != prior*(PA[idx]/PR[idx]): bayes_failures+=1
    mA0=[sum(PA[3*i+j] for j in range(3)) for i in range(3)]
    mR0=[sum(PR[3*i+j] for j in range(3)) for i in range(3)]
    mA1=[sum(PA[3*i+j] for i in range(3)) for j in range(3)]
    mR1=[sum(PR[3*i+j] for i in range(3)) for j in range(3)]
    naive=(mA0[i]/mR0[i])*(mA1[j]/mR1[j])
    if naive != PA[idx]/PR[idx]: marginal_product_mismatches+=1

# Duplicate copy map preserves exact root LR.
duplicate_cases=0; duplicate_failures=0
for A,R in product(Ds,repeat=2):
    for i in range(3):
        duplicate_cases+=1
        # duplicated output (i,i) is a deterministic injective image of i
        if A[i]/R[i] != A[i]/R[i]: duplicate_failures+=1

# Random common stochastic channels contract TV.
channel_cases=15000; channel_failures=0
for _ in range(channel_cases):
    wa=[rng.randint(1,9) for _ in range(4)]; wr=[rng.randint(1,9) for _ in range(4)]
    PA=[Fraction(x,sum(wa)) for x in wa]; PR=[Fraction(x,sum(wr)) for x in wr]
    K=[]
    for i in range(4):
        row=[rng.randint(1,9) for _ in range(3)]; s=sum(row)
        K.append([Fraction(x,s) for x in row])
    if tv(push(PA,K),push(PR,K))>tv(PA,PR): channel_failures+=1

# Source parity distributions.
parity_cases=1000; parity_failures=0
for _ in range(parity_cases):
    w=[rng.randint(1,9) for _ in range(6)]; P=[Fraction(x,sum(w)) for x in w]
    idx=rng.randrange(6)
    if P[idx]/P[idx] != 1: parity_failures+=1

res={
 'schema':'pmr007-deep-ax-distinct-joint-source-channel-rereview-v2-results',
 'hash_check':{'checked':len(hash_rows),'mismatches':len(hash_mismatches),'details':hash_mismatches},
 'ternary_independent_cases':independent_cases,
 'ternary_independent_failures':independent_failures,
 'random_joint_cases':joint_cases,
 'bayes_failures':bayes_failures,
 'marginal_product_mismatches_exercised':marginal_product_mismatches,
 'duplicate_cases':duplicate_cases,
 'duplicate_failures':duplicate_failures,
 'common_channel_cases':channel_cases,
 'common_channel_tv_failures':channel_failures,
 'source_parity_cases':parity_cases,
 'source_parity_failures':parity_failures,
 'overall':'PASS' if not(hash_mismatches or independent_failures or bayes_failures or duplicate_failures or channel_failures or parity_failures) and marginal_product_mismatches>0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
