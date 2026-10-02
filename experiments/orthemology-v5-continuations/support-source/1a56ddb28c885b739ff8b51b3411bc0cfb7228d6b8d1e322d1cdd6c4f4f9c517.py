from fractions import Fraction as F
from itertools import combinations
from math import gcd,comb
from pathlib import Path
import json,random,hashlib
H=Path(__file__).resolve().parent

def value(u,b,m):
    assert 0<=b<u and m>=1
    if m>b:return F(0)
    N=b-m+1
    return max(F((q*N+m-1)//u,q) for q in range(1,u-m+2))

def construct(u,b,m):
    # The nonzero theorem uses m<=b. Zero menus need only b+1 singleton actions.
    if m>b:return (1,)*b+(u-b,)
    t=value(u,b,m);a,q=t.numerator,t.denominator;N=b-m+1
    dp=[[-1]*(u+1) for _ in range(m+1)];parent=[[None]*(u+1) for _ in range(m+1)];dp[0][0]=0
    for j in range(1,m+1):
        for total in range(j,u+1):
            for s in range(1,total-j+2):
                if dp[j-1][total-s]<0:continue
                candidate=dp[j-1][total-s]+a*s//q
                if candidate>dp[j][total]:dp[j][total]=candidate;parent[j][total]=s
    assert dp[m][u]>=N
    out=[];total=u
    for j in range(m,0,-1):s=parent[j][total];out.append(s);total-=s
    assert total==0 and sum(out)==u and len(out)==m and all(x>0 for x in out)
    assert sum((t*s).__floor__() for s in out)>=N
    return tuple(out)

def main():
    cases=[];counts={'constructed_partitions':0,'M1':0,'last_positive_boundary':0,'gcd_family':0,'N2':0,'zero_menus':0};dig=hashlib.sha256()
    for u in range(2,35):
        for b in range(u):
            for m in range(1,b+2):
                v=value(u,b,m);s=construct(u,b,m)
                counts['constructed_partitions']+=1;dig.update(repr((u,b,m,v,s)).encode())
                if m>b:assert v==0;counts['zero_menus']+=1
                if m==1:assert v==F(b,u);counts['M1']+=1
                if b>=1 and m==b:assert v==F(1,u-b+1);counts['last_positive_boundary']+=1
                if m<=b+1:
                    N=b-m+1
                    if gcd(u,N)>=m:assert v==F(N,u);counts['gcd_family']+=1
                    if N==2 and m>=2:assert v==F(1,(u-m+2)//2);counts['N2']+=1
    assert value(8,3,2)==F(1,4)>F(comb(3,2),comb(8,2))==F(3,28)
    for u in range(1,20):
        for b in range(u):
            for m in [b+1,u+1,2*u+7]:assert value(u,b,m)==0
    for args in [(7,3,2),(11,5,2),(9,4,3),(10,4,3),(12,4,3),(11,5,4),(20,8,5)]:
        v=value(*args);s=construct(*args);cases.append({'u':args[0],'b':args[1],'M':args[2],'value':str(v),'partition':s,'floor_sum':sum((v*x).__floor__() for x in s),'N':args[1]-args[2]+1})
    out={'status':'PASS','counts':counts,'examples':cases,'construction_digest':dig.hexdigest(),'algorithm_scope':'O(u) denominator candidates for the value; O(Mu^2) integer operations for the dynamic-programming partition, not O(u) policy construction'}
    (H/'GENERAL_CONSTRUCTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
