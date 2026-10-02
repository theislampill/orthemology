"""Exact finite regressions for the continuum theorem, not a continuum proof."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib, json, random
HERE=Path(__file__).resolve().parent

def ceil(x): return -((-x.numerator)//x.denominator)
def partition_value(u,b):
    best=F(1); sizes=[]
    for s in range(1,u):
        v=max(min(F(c,s),F(b-c,u-s)) for c in range(max(0,b-(u-s)),min(b,s)+1))
        if v<best: best=v;sizes=[s]
        elif v==best:sizes.append(s)
    return best,sizes

def threshold_value(u,b):
    values={F(c,s) for s in range(1,u+1) for c in range(s+1)}
    return max(t for t in values if max(ceil(t*s)+ceil(t*(u-s)) for s in range(u+1))<=b)

def prefix_masks(order):
    out=[0]; z=0
    for i in order:z|=1<<i;out.append(z)
    return out

def independent(mask, prefixes, f):
    return all((mask&p).bit_count()<=v for p,v in zip(prefixes,f))

def rank_formula(A,prefixes,f):
    return min((A&~p).bit_count()+v for p,v in zip(prefixes,f))

def check_chain(u,t,order):
    prefs=prefix_masks(order);f=[((1-t)*k).__floor__() for k in range(u+1)]
    inds=[a for a in range(1<<u) if independent(a,prefs,f)]
    for A in range(1<<u):
        actual=max(I.bit_count() for I in inds if I&~A==0)
        assert actual==rank_formula(A,prefs,f),(u,t,A)
    return prefs,f,inds

def main():
    counts={"partition_vs_ceiling":0,"chain_rank_subsets":0,"all_two_ordering_instances":0,"random_rational_rows":0}
    examples=[]
    for u in range(2,41):
        for b in range(1,u):
            val,sizes=partition_value(u,b)
            assert val==threshold_value(u,b),(u,b,val)
            counts['partition_vs_ceiling']+=1
            if (u,b) in [(7,3),(11,5),(8,3),(9,4)]:examples.append({'u':u,'b':b,'value':str(val),'attaining_first_block_sizes':sizes})
    # Exact rank lemma at every breakpoint for small n.
    for u in range(1,8):
        for t in sorted({F(c,s) for s in range(1,u+1) for c in range(s+1)}):
            check_chain(u,t,tuple(range(u)))
            counts['chain_rank_subsets']+=1<<u
    # Fix the first ordering; enumerate every second permutation and every b.
    for u in range(2,8):
        for b in range(1,u):
            t,_=partition_value(u,b)
            f=[((1-t)*k).__floor__() for k in range(u+1)]
            p1=prefix_masks(range(u));q=u-b
            inds=[sum(1<<i for i in C) for C in combinations(range(u),q)]
            inds=[D for D in inds if independent(D,p1,f)]
            for order in permutations(range(u)):
                p2=prefix_masks(order)
                assert any(independent(D,p2,f) for D in inds),(u,b,order)
                counts['all_two_ordering_instances']+=1
    # Rational rows of mixed, non-common denominators, including zeros, ties,
    # duplicated rows, mass-one rows, and unequal support sizes.
    rng=random.Random(202610020055)
    witness_hash=hashlib.sha256()
    for u in range(2,15):
        for b in range(1,u):
            t,_=partition_value(u,b)
            for trial in range(24):
                rows=[]
                for j in range(2):
                    nums=[rng.randrange(0,100) if rng.randrange(4) else 0 for _ in range(u)]
                    if trial%8==0:nums=[int(i==(trial+j)%u) for i in range(u)]
                    if sum(nums)==0:nums[0]=1
                    rows.append([F(x,sum(nums)) for x in nums])
                if trial%9==0:rows[1]=rows[0][:]
                orders=[sorted(range(u),key=lambda i:(-p[i],i)) for p in rows]
                prefs=[prefix_masks(o) for o in orders]
                valid=[]
                for C in combinations(range(u),b):
                    mask=sum(1<<i for i in C)
                    if all((mask&P[k]).bit_count()>=ceil(t*k) for P in prefs for k in range(u+1)):
                        assert all(sum(p[i] for i in C)>=t for p in rows)
                        valid.append(C);break
                assert valid,(u,b,trial,t)
                witness_hash.update(repr((u,b,t,rows,valid[0])).encode())
                counts['random_rational_rows']+=1
    out={'status':'PASS','scope':'Finite exact regressions of the separately proved two-message continuum theorem; not a grid proof of continuum optimality','counts':counts,'examples':examples,'rational_witness_digest':witness_hash.hexdigest()}
    (HERE/'TWO_MESSAGE_EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
