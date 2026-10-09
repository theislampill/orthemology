#!/usr/bin/env python3
"""Independent exhaustive oracle reference; load only author function AST, no side effects."""
import ast, hashlib, json
from pathlib import Path
from fractions import Fraction
from itertools import combinations_with_replacement, product
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'finite-skyline-readout'/'controls.py'
tree=ast.parse(SOURCE.read_text())
selected=ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in {'extract','grid_resolution'}],type_ignores=[])
ns={'Fraction':Fraction}; exec(compile(selected,str(SOURCE),'exec'),ns)
extract=ns['extract']; resolution=ns['grid_resolution']
def reference(points):
    # Scan columns and retain the first strictly lower column minimum.
    answer=[]; best=None
    for x in sorted(set(x for x,y in points)):
        y=min(y for xx,y in points if xx==x)
        if best is None or y<best:
            answer.append((x,y));best=y
    return answer
checks={}; query_max={}
for L in [1,2,3]:
    atoms=list(product(range(L+1),repeat=2)); count=0; most=0
    for mask in range(1<<len(atoms)):
        points=[a for i,a in enumerate(atoms) if mask&(1<<i)]
        answer,calls=extract(points,L); expected=reference(points)
        assert answer==expected,(points,answer,expected)
        d=L.bit_length() # ceil(log2(L+1)) exactly
        assert calls<=1+len(answer)*(1+2*d),(L,points,calls)
        assert calls>=1
        count+=1; most=max(most,calls)
    checks[str(L)]=count; query_max[str(L)]=most
duplicates=0
atoms=list(product(range(3),repeat=2))
for N in range(7):
    for points in combinations_with_replacement(atoms,N):
        got,calls=extract(points,2)
        assert got==reference(points)
        assert calls<=1+len(got)*5
        duplicates+=1
quantized=0; collision_free=0; loss=0
D=6; atoms=list(product(range(D+1),repeat=2))
for L in range(1,7):
    for N in range(4):
        for points in combinations_with_replacement(atoms,N):
            q=[((L*x+D-1)//D,(L*y+D-1)//D) for x,y in points]
            k=len(reference(points)); kg=len(reference(q))
            assert kg<=k
            cf=all(len({p[j] for p in q})==N for j in [0,1])
            if cf:assert kg==k;collision_free+=1
            if kg<k:loss+=1
            for p,qp in zip(points,q):
                for coord in [0,1]:
                    for j in range(L+1):
                        assert (L*p[coord]<=D*j)==(qp[coord]<=j)
            quantized+=1
resolutions=0
for n,R,eta in product(range(1,21),[1,2,17,100],[Fraction(1,1000),Fraction(2,7),Fraction(99,100)]):
    l=resolution(n,R,eta)
    A=Fraction(n*(n+1)*R,1)/eta
    assert l**n>=A**(n+1)
    assert l==1 or (l-1)**n<A**(n+1)
    resolutions+=1
# Include general helper boundary cases A<1 and A=1, beyond theorem parameters.
for eta in [Fraction(2),Fraction(3),Fraction(100)]:
    l=resolution(1,1,eta); A=Fraction(2)/eta
    assert l>=1 and l>=A*A and (l==1 or l-1<A*A)
    resolutions+=1
report={'status':'PASS','all_subsets_by_L':checks,'max_queries_by_L':query_max,'multiset_cases_grid_L2_through_N6':duplicates,'quantization_cases':quantized,'collision_free_cases':collision_free,'strict_count_loss_cases':loss,'exact_resolution_cases':resolutions,'author_controls_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
