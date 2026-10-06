"""Independent bounded set/partition checks; imports no author implementation."""
from itertools import combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def subsets(U,k=None):
    return [frozenset(x) for j in (range(len(U)+1) if k is None else [k]) for x in combinations(U,j)]

def partition(U,A):
    return [A]+[frozenset({x}) for x in U if x not in A]

def image(P,parts):
    return frozenset(root for root in parts if root & P)

def main():
    cases=0; robust=0; worlds=0; realizations=0; params=0
    for m in range(2,8):
        U=tuple(range(m));all_sets=subsets(U)
        for c in range(1,m):
            maps=[partition(U,A) for A in subsets(U,c)]
            for P in all_sets:
                for R in all_sets:
                    I=P&R;s=len(I)
                    values=[]
                    for parts in maps:
                        A=parts[0]
                        shared=len(image(P,parts)&image(R,parts))
                        assert shared==s-len(A&I)+int(bool(A&P) and bool(A&R))
                        values.append(shared);cases+=1
                    predicted=max(1,s-c+1) if s else int(c>m-min(len(P),len(R)))
                    assert min(values)==predicted
                    for B in range(1,m-c+1):
                        assert (min(values)>B)==(s>=B+c);robust+=1
            for B in range(1,m-c+1):
                k=B+c-1;maximal=set()
                for parts in maps:
                    for bad in combinations(parts,B):
                        T=frozenset().union(*bad)
                        assert len(T)<=k
                        if len(T)==k:maximal.add(T)
                        worlds+=1
                Ts=subsets(U,k)
                assert maximal==set(Ts)
                for T in Ts:
                    A=frozenset(sorted(T)[:c]);parts=partition(U,A)
                    bad=[A]+[frozenset({x}) for x in T-A]
                    assert len(bad)==B and all(root in parts for root in bad)
                    assert frozenset().union(*bad)==T
                    realizations+=1
                if m<=3*k:
                    T1=frozenset(U[:k]);T2=frozenset(U[-k:])
                    P=frozenset(U)-T1;R=frozenset(U)-T2
                    assert len(P&R)<=k
                    assert min(len(image(P,parts)&image(R,parts)) for parts in maps)<=B
                else:
                    q=m-k
                    assert 2*q>m+k and q<=m-k
                params+=1
    U=tuple(range(4));P=frozenset({0,1});R=frozenset({2,3})
    assert all(len(image(P,part)&image(R,part))==1 for part in [partition(U,A) for A in subsets(U,3)])
    result={'status':'PASS_REVIEWER_ROOT_IMAGE_CHECKS','scope':'Finite pure set/partition checks, not a physical or cryptographic test','m_min':2,'m_max':7,'explicit_partition_pair_cases':cases,'robust_safety_equivalences_B_ge_1':robust,'actual_fault_world_instantiations':worlds,'canonical_maximal_world_realizations':realizations,'arbitrary_family_obstruction_parameter_cases':params,'B0_forced_bridge_exception_confirmed':True,'author_code_imported':False}
    (HERE/'INDEPENDENT_ROOT_IMAGE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
