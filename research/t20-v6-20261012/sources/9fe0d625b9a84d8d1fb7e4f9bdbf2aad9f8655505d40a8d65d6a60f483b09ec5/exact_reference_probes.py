"""Independent direct strict Fourier–Motzkin feasibility versus certificate search."""
import copy
import itertools as it
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

from polytope_disclosure import audit, verify
from test_polytope_disclosure import triangle, atom, cmp, conjunction


def simplify(rows):
    out={}
    for a,b,strict in rows:
        first=next((abs(v) for v in a if v),None)
        if first is None:
            if b<0 or (strict and b==0): return None
            continue
        a=tuple(v/first for v in a); b=b/first
        if a not in out or b<out[a][0]: out[a]=(b,strict)
        elif b==out[a][0]: out[a]=(b,strict or out[a][1])
    return [(a,b,s) for a,(b,s) in out.items()]


def direct_strict_feasible(polytope,atoms,signs):
    eps=F(polytope['min_weight']); rows=[]
    for i in range(3):
        a=[F(0)]*3;a[i]=F(-1);rows.append((tuple(a),-eps,False))
    rows.extend([((F(1),F(1),F(1)),F(1),False),((F(-1),F(-1),F(-1)),F(-1),False)])
    for name in ['extra_le','extra_eq']:
        for r in polytope[name]:
            a=tuple(F(v) for v in r['coefficients']);b=F(r['bound'])
            rows.append((a,b,False))
            if name=='extra_eq':rows.append((tuple(-x for x in a),-b,False))
    for atom,s in zip(atoms,signs):
        a=tuple(F(v) for v in atom['coefficients']);b=F(atom['offset'])
        if s:
            rows.append((tuple(-s*x for x in a),s*b,True))
        else:
            rows.append((a,-b,False));rows.append((tuple(-x for x in a),b,False))
    for _ in range(3):
        rows=simplify(rows)
        if rows is None:return False
        zero=[];positive=[];negative=[]
        for a,b,strict in rows:
            if a[0]>0:positive.append((tuple(x/a[0] for x in a[1:]),b/a[0],strict))
            elif a[0]<0:negative.append((tuple(x/(-a[0]) for x in a[1:]),b/(-a[0]),strict))
            else:zero.append((a[1:],b,strict))
        rows=zero+[(tuple(x+y for x,y in zip(a,c)),b+d,s or t)
                   for a,b,s in positive for c,d,t in negative]
    return simplify(rows) is not None


def main():
    totals=Counter(); kinds=Counter(); output_examples={}
    domains=[triangle(),triangle('1/3'),triangle('1/2'),
             triangle(eq=[{'coefficients':[1,-1,0],'bound':0}])]
    cases=[]
    for coeff in it.product([-1,0,1],repeat=3):
        for offset in [-1,0,1]:
            atoms=[{'coefficients':list(coeff),'offset':offset}]
            for p in domains:cases.append((p,atoms,cmp()))
    for low,high in it.product(['1/10','1/5','1/3','2/5','3/5','4/5'],repeat=2):
        atoms=[atom(0,str(-F(low))),atom(1,str(-F(high)))]
        target={'op':'or','args':[cmp(0),{'op':'not','arg':cmp(1,False)}]}
        for p in [domains[0],domains[3]]:cases.append((p,atoms,target))
    for bounds in it.product(['1/10','1/5','2/5'],repeat=3):
        atoms=[atom(i,str(-F(b))) for i,b in enumerate(bounds)]
        cases.append((triangle(),atoms,conjunction()))
    for p,atoms,target in cases:
        cert=audit(p,atoms,target)
        assert cert['status']!='INVALID'
        assert verify(p,atoms,target,cert)['accepted']
        totals['input_instances']+=1
        for cell in cert['cells']:
            truth=direct_strict_feasible(p,atoms,cell['signs'])
            assert truth==(cell['kind']=='POSITIVE_WITNESS'),(p,atoms,cell,truth)
            totals['sign_cells_compared']+=1;kinds[cell['kind']]+=1
        totals[cert['status']]+=1
    p=triangle();atoms=[atom(i) for i in range(3)];target=conjunction()
    cert=audit(p,atoms,target)
    with patch('polytope_disclosure._vertices',side_effect=AssertionError('Verifier called search')),\
         patch('polytope_disclosure._cone_certificate',side_effect=AssertionError('Verifier called search')):
        assert verify(p,atoms,target,cert)['accepted']
    rejected=0
    for field in cert:
        forged=copy.deepcopy(cert);forged.pop(field)
        assert not verify(p,atoms,target,forged)['accepted'];rejected+=1
        forged=copy.deepcopy(cert);forged[field]='tampered'
        assert not verify(p,atoms,target,forged)['accepted'];rejected+=1
    for i,cell in enumerate(cert['cells']):
        forged=copy.deepcopy(cert)
        if cell['kind']=='POSITIVE_WITNESS':forged['cells'][i]['point'][-1]='0'
        else:forged['cells'][i]['multipliers']=['0']*len(cell['multipliers'])
        assert not verify(p,atoms,target,forged)['accepted'];rejected+=1
    forged=copy.deepcopy(cert);forged['cells'][0]=copy.deepcopy(forged['cells'][1])
    assert not verify(p,atoms,target,forged)['accepted'];rejected+=1
    Path('interior_example.json').write_text(json.dumps({'polytope':p,'atoms':atoms,'target':target,'certificate':cert},indent=2)+'\n')
    results={'status':'EXACT_RESEARCH_CHECKS_NOT_KERNEL_PROOF','totals':dict(totals),
             'certificate_types':dict(kinds),'mismatches':0,
             'certificate_mutations_rejected':rejected,'verification_without_search':True}
    Path('probe_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
