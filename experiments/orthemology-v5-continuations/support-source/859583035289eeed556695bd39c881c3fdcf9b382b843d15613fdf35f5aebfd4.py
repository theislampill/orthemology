"""Trust-minimal exact certificate replay: standard library only, no LP solver."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent

def verify_file(file):
    raw=file.read_bytes();d=json.loads(raw);u=d['u'];b=d['b'];m=d['M'];B=Q(d['target'])
    assert b==4 and m==3 and u in (6,8,10,12)
    assert B==Q(1,(u-2)//2)
    cs=list(combinations(range(u),b));n=m*u+1;t=n-1
    # Rebuild all assumptions from their mathematical meanings, independently
    # of the generator's stored labels or float matrices.
    inequalities=[]
    for j in range(m):
        for i in range(u):
            coeff=[0]*n;coeff[j*u+i]=1;inequalities.append((coeff,B))
    for i in range(u-1):
        coeff=[0]*n;coeff[i+1]=1;coeff[i]=-1;inequalities.append((coeff,Q(0)))
    for j in range(1,m):
        for i in range(u):
            coeff=[0]*n;coeff[j*u+i]=1;coeff[0]=-1;inequalities.append((coeff,Q(0)))
    coeff=[0]*n;coeff[t]=-1;inequalities.append((coeff,-Q(2,u)))
    nodes=d['nodes'];assert nodes and nodes[0]['path']==[]
    seen=set();todo=[0];leaves=0;minimum=None;max_denominator=1
    while todo:
        k=todo.pop()
        if k in seen:continue
        seen.add(k);node=nodes[k]
        path=[tuple(p) for p in node['path']]
        assert len(path)==len(set(path)) and path==sorted(path)
        assert len({c for c,j in path})==len(path)
        assert all(0<=c<len(cs) and 0<=j<m for c,j in path)
        if 'certificate' in node:
            assert 'children' not in node and 'branch_scenario' not in node
            rows=inequalities[:]
            for c,j in path:
                coeff=[0]*n
                for i in cs[c]:coeff[j*u+i]=1
                coeff[t]=-1;rows.append((coeff,Q(0)))
            cert=node['certificate'];terms=cert['inequality_dual'];ys={}
            for pos,s in terms:
                assert pos not in ys and 0<=pos<len(rows)
                ys[pos]=Q(s);assert ys[pos]<=0
            zs=[Q(s) for s in cert['equality_dual']];assert len(zs)==m
            lhs=[Q(0)]*n;bound=sum(zs)
            for pos,y in ys.items():
                coeff,rhs=rows[pos];bound+=y*rhs
                for col,a in enumerate(coeff):lhs[col]+=y*a
            for j,z in enumerate(zs):
                for i in range(u):lhs[j*u+i]+=z
            assert all(v<=int(i==t) for i,v in enumerate(lhs)),(u,k,'dual coefficient')
            assert bound==Q(cert['lower_bound']) and bound>=B,(u,k,'lower bound')
            minimum=bound if minimum is None else min(minimum,bound)
            max_denominator=max(max_denominator,*[x.denominator for x in list(ys.values())+zs])
            leaves+=1
        else:
            assert set(node)=={'path','branch_scenario','children'}
            c=node['branch_scenario'];assert 0<=c<len(cs) and c not in {i for i,j in path}
            children=node['children'];assert len(children)==m
            for j,child in enumerate(children):
                assert isinstance(child,int) and 0<=child<len(nodes)
                expected=sorted(path+[(c,j)])
                assert [tuple(p) for p in nodes[child]['path']]==expected,(u,k,j,'branch coverage')
                todo.append(child)
    assert len(seen)==len(nodes),'Unreachable payload nodes'
    assert leaves==d['leaf_count'] and len(nodes)==d['node_count']
    # Counts and the generator's reported completion flag are not used to accept
    # any branch; every reachable branch/leaf above is reconstructed and checked.
    return {'u':u,'b':b,'M':m,'exact_lower_bound':str(B),'nodes':len(nodes),'verified_dual_leaves':leaves,'smallest_leaf_bound':str(minimum),'max_dual_denominator':max_denominator,'certificate_sha256':hashlib.sha256(raw).hexdigest()}

def main():
    out={'status':'PASS','trust_base':'Python standard library exact integers and Fraction; no numerical optimization calls','certificates':[verify_file(ROOT/f'EXACT_SENDER_TREE_u{u}.json') for u in [6,8,10,12]]}
    (ROOT/'EXACT_SENDER_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
