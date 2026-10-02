"""Exact arithmetic controls for the proof; no probability grid or optimizer."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import gcd
from pathlib import Path
import random,json,hashlib
H=Path(__file__).resolve().parent

@lru_cache(None)
def partitions(u,m,lo=1):
    if m==1:return ((u,),) if u>=lo else ()
    return tuple((s,)+r for s in range(lo,u//m+1) for r in partitions(u-s,m-1,s))

def partition_profile(s):
    """Value for each N via exact jumps; independent of the claimed formula."""
    u=sum(s);m=len(s);values={F(c,d) for d in s for c in range(d+1)}
    answer=[None]*(u-m+1);answer[0]=F(0);prev=0
    for t in sorted(values):
        f=sum((t*d).__floor__() for d in s)
        for N in range(prev+1,min(f,u-m)+1):answer[N]=t
        prev=max(prev,f)
        if prev>=u-m:break
    assert all(x is not None for x in answer)
    return answer

def formula(u,b,m):
    N=b-m+1
    return max(F((q*N+m-1)//u,q) for q in range(1,u-m+2))

def transfer(s,a,q,N):
    """Execute the residue proof's contradiction construction on eligible data."""
    s=list(s);M=len(s);u=sum(s);delta=a*u-q*N
    assert 0<a<q and gcd(a,q)==1 and delta>=M
    k=next(k for k in range(1,q) if (a*k+1)%q==0);steps=0
    while True:
        f=sum(a*x//q for x in s);d=f-N;res=[a*x%q for x in s];zero=[j for j,r in enumerate(res) if r==0]
        assert d>=0
        if d>=len(zero):break
        donor=zero[0]
        if d>0:recipient=zero[1]
        else:recipient=next(j for j,r in enumerate(res) if r>=2)
        s[donor]-=k;s[recipient]+=k;steps+=1
        assert all(x>=1 for x in s) and sum(s)==u
        assert steps<=M
    t=F(a,q);eta=F(1,2*q*max(s));lower=t-eta
    assert lower<t and sum((lower*x).__floor__() for x in s)>=N
    return steps,tuple(s),lower

def main():
    counts={'partition_parameter_cases':0,'integer_partitions':0,'copy_block_parameter_cases':0,'residue_transfer_cases':0};dig=hashlib.sha256();examples=[]
    for u in range(2,29):
        for M in range(1,min(7,u)+1):
            best=[None]*(u-M+1);witness=[None]*len(best)
            for s in partitions(u,M):
                counts['integer_partitions']+=1
                prof=partition_profile(s)
                for N,t in enumerate(prof):
                    if best[N] is None or t<best[N]:best[N]=t;witness[N]=s
            for N,B in enumerate(best):
                b=N+M-1
                if b>=u:continue
                assert B==formula(u,b,M),(u,b,M,B,formula(u,b,M))
                if B:
                    delta=B.numerator*u-B.denominator*N
                    assert 0<=delta<=M-1
                    assert B.denominator<=u-M+1
                counts['partition_parameter_cases']+=1
                dig.update(repr((u,b,M,B,witness[N])).encode())
                if (u,b,M) in [(7,3,2),(11,5,2),(9,4,3),(10,4,3),(12,4,3),(11,5,4)]:examples.append({'u':u,'b':b,'M':M,'value':str(B),'partition':witness[N]})
    # Primary theorem hypotheses and chromatic obstruction arithmetic.
    for u in range(3,81):
        for b in range(1,u):
            for M in range(1,b+1):
                B=formula(u,b,M);a,q=B.numerator,B.denominator;N=b-M+1
                assert 0<a<q and q>=2 and q<=u-M+1
                assert B<=F(b,u)
                expanded=(q-a)*u;k=u-b
                assert q-a<=q and expanded>=q*k
                numerator=expanded-q*(k-1)
                chromatic=-((-numerator)//(q-1))
                assert chromatic>M
                assert numerator==q*M-(a*u-q*N)
                counts['copy_block_parameter_cases']+=1
    # Exact execution of the arithmetic transfer, deliberately generating both
    # zero-pair (positive-excess) and residue-donor (zero-excess) situations.
    rng=random.Random(202610020126);max_steps=0;positive_excess=0;zero_excess=0
    for trial in range(15000):
        q=rng.randrange(2,18);a=rng.randrange(1,q)
        if gcd(a,q)!=1:continue
        M=rng.randrange(2,10);s=[rng.randrange(1,2*q+1) for _ in range(M)]
        for j in range(rng.randrange(1,M+1)):s[j]=q*rng.randrange(1,3)
        f=sum(a*x//q for x in s);z=sum(a*x%q==0 for x in s)
        d=rng.randrange(z) if z else 0;N=f-d
        if N<1 or a*sum(s)-q*N<M:continue
        if N+M-1>=sum(s):continue
        steps,out,lower=transfer(s,a,q,N);max_steps=max(max_steps,steps)
        positive_excess+=d>0;zero_excess+=d==0;counts['residue_transfer_cases']+=1
        dig.update(repr((s,a,q,N,out,lower)).encode())
    assert positive_excess and zero_excess
    out={'status':'PASS','counts':counts,'transfer_positive_excess':positive_excess,'transfer_zero_excess':zero_excess,'maximum_transfer_steps':max_steps,'examples':examples,'arithmetic_digest':dig.hexdigest(),'scope':'Exact finite arithmetic regressions; all-real optimality relies on the written proof and cited partition-Kneser theorem'}
    (H/'GENERAL_FRONTIER_EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
