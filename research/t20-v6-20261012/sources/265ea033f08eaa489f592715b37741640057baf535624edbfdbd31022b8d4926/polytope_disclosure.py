"""Research-only exact three-criterion disclosure and linear-certificate checker.

Complete within a bounded rational input grammar; deliberately exponential.
The verifier checks witnesses/linear combinations, not the search algorithm.
"""
import hashlib
import itertools as it
import json
import re
from fractions import Fraction as F


SCOPE='RELATIVE_RATIONAL_POLYTOPE_DISCLOSURE_ONLY'
AUTHORITY='SUPPLIED_NOT_CERTIFIED'


def _q(x,bits=128):
    if isinstance(x,bool) or not isinstance(x,(int,str)):
        raise ValueError('Exact integer/rational input required')
    s=str(x)
    if len(s)>2*bits+8 or not re.fullmatch(r'[+-]?\d+(?:/\d+)?',s):
        raise ValueError('Rational syntax/resource bound')
    q=F(s)
    if abs(q.numerator).bit_length()>bits or q.denominator.bit_length()>bits:
        raise ValueError('Rational bit bound')
    return q


def _fields(x,keys):
    if not isinstance(x,dict) or set(x)!=set(keys):
        raise ValueError('Missing or unknown fields')


def _vector(x,n,bits=128):
    if not isinstance(x,list) or len(x)!=n:
        raise ValueError('Incorrect vector length')
    return tuple(_q(v,bits) for v in x)


def _compile(t,k,budget,depth=0):
    budget[0]+=1
    if not isinstance(t,dict) or budget[0]>64 or depth>12:
        raise ValueError('Target syntax/resource bound')
    op=t.get('op')
    if op in {'gt','ge'}:
        _fields(t,{'op','atom'})
        if type(t['atom']) is not int or not 0<=t['atom']<k:
            raise ValueError('Unknown atom')
        return (op,t['atom'])
    if op=='const':
        _fields(t,{'op','value'})
        if type(t['value']) is not bool: raise ValueError('Boolean constant required')
        return ('const',t['value'])
    if op=='not':
        _fields(t,{'op','arg'})
        return (op,_compile(t['arg'],k,budget,depth+1))
    if op in {'and','or'}:
        _fields(t,{'op','args'})
        if not isinstance(t['args'],list) or not 1<=len(t['args'])<=8:
            raise ValueError('Boolean arity bound')
        return (op,tuple(_compile(a,k,budget,depth+1) for a in t['args']))
    raise ValueError('Unknown target operation')


def _truth(code,signs):
    op=code[0]
    if op=='gt': return signs[code[1]]>0
    if op=='ge': return signs[code[1]]>=0
    if op=='const': return code[1]
    if op=='not': return not _truth(code[1],signs)
    values=(_truth(c,signs) for c in code[1])
    return all(values) if op=='and' else any(values)


def _parse(polytope,atoms,target):
    _fields(polytope,{'min_weight','extra_le','extra_eq'})
    eps=_q(polytope['min_weight'])
    if not 0<eps<=1: raise ValueError('Positive bounded minimum weight required')
    rows=[]
    for i in range(3):
        a=[F(0)]*4; a[i]=F(-1); rows.append((tuple(a),-eps))
    rows.extend([((F(1),F(1),F(1),F(0)),F(1)),
                 ((F(-1),F(-1),F(-1),F(0)),F(-1)),
                 ((F(0),F(0),F(0),F(-1)),F(0)),
                 ((F(0),F(0),F(0),F(1)),F(1))])
    for field,limit in [('extra_le',4),('extra_eq',2)]:
        values=polytope[field]
        if not isinstance(values,list) or len(values)>limit:
            raise ValueError('Linear restriction count bound')
        for row in values:
            _fields(row,{'coefficients','bound'})
            a=_vector(row['coefficients'],3)+(F(0),); b=_q(row['bound'])
            rows.append((a,b))
            if field=='extra_eq': rows.append((tuple(-v for v in a),-b))
    if not isinstance(atoms,list) or len(atoms)>3:
        raise ValueError('Prototype supports at most three affine atoms')
    parsed=[]
    for atom in atoms:
        _fields(atom,{'coefficients','offset'})
        parsed.append((_vector(atom['coefficients'],3),_q(atom['offset'])))
    code=_compile(target,len(parsed),[0])
    digest=hashlib.sha256(json.dumps([polytope,atoms,target],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return rows,parsed,code,digest


def _cell_rows(base,atoms,signs):
    rows=list(base)
    for (a,b),s in zip(atoms,signs):
        if s==0:
            rows.append((a+(F(0),),-b))
            rows.append((tuple(-v for v in a)+(F(0),),b))
        else:
            rows.append((tuple(-s*v for v in a)+(F(1),),s*b))
    return rows


def _dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))


def _solve_unique(matrix,rhs):
    """Unique solution of a possibly overdetermined exact linear system."""
    if not matrix: return None
    n=len(matrix[0]); a=[list(row)+[v] for row,v in zip(matrix,rhs)]
    pivot=0; locations=[]
    for col in range(n):
        found=next((r for r in range(pivot,len(a)) if a[r][col]),None)
        if found is None: continue
        a[pivot],a[found]=a[found],a[pivot]
        factor=a[pivot][col]; a[pivot]=[v/factor for v in a[pivot]]
        for r in range(len(a)):
            if r!=pivot and a[r][col]:
                factor=a[r][col]; a[r]=[v-factor*u for v,u in zip(a[r],a[pivot])]
        locations.append(col); pivot+=1
    if any(not any(row[:n]) and row[n] for row in a): return None
    if len(locations)!=n: return None
    out=[F(0)]*n
    for r,col in enumerate(locations): out[col]=a[r][n]
    return tuple(out)


def _vertices(rows):
    out=set()
    for chosen in it.combinations(rows,4):
        point=_solve_unique([r[0] for r in chosen],[r[1] for r in chosen])
        if point is not None and all(_dot(a,point)<=b for a,b in rows): out.add(point)
    return sorted(out)


def _cone_certificate(rows,target):
    generators=[a+(b,) for a,b in rows]
    for size in range(1,6):
        for indices in it.combinations(range(len(rows)),size):
            matrix=[[generators[i][j] for i in indices] for j in range(5)]
            coeff=_solve_unique(matrix,target)
            if coeff is not None and all(v>=0 for v in coeff):
                full=[F(0)]*len(rows)
                for i,v in zip(indices,coeff): full[i]=v
                return full
    return None


def _status(values):
    return ('NO_ADMISSIBLE_EXTENSION' if not values else 'DISAGREEMENT' if len(values)==2
            else 'INVARIANT_TRUE' if True in values else 'INVARIANT_FALSE')


def audit(polytope,atoms,target):
    try:
        base,parsed,code,digest=_parse(polytope,atoms,target)
    except (ValueError,TypeError,KeyError,ZeroDivisionError,OverflowError) as e:
        return {'status':'INVALID','reason':str(e),'scope':'NO_CONCLUSION'}
    cells=[]; values=set()
    for signs in it.product([-1,0,1],repeat=len(parsed)):
        rows=_cell_rows(base,parsed,signs); vertices=_vertices(rows)
        positive=next((v for v in vertices if v[-1]>0),None)
        if positive is not None:
            cell={'signs':list(signs),'kind':'POSITIVE_WITNESS','point':[str(v) for v in positive]}
            values.add(_truth(code,signs))
        else:
            goal=(F(0),F(0),F(0),F(1),F(0)) if vertices else (F(0),F(0),F(0),F(0),F(-1))
            multipliers=_cone_certificate(rows,goal)
            if multipliers is None:
                raise RuntimeError('Exact certificate search failed: no verdict is licensed')
            cell={'signs':list(signs),'kind':'DUAL_ZERO_BOUND' if vertices else 'FARKAS_CONTRADICTION',
                  'multipliers':[str(v) for v in multipliers]}
        cells.append(cell)
    return {'schema':'three-criterion-cell-certificate-v1','input_hash':digest,
            'status':_status(values),'realized_values':sorted(values),'cells':cells,
            'scope':SCOPE,'authority_status':AUTHORITY}


def verify(polytope,atoms,target,certificate):
    """Check linear certificates and complete pattern coverage; never call LP search."""
    try:
        base,parsed,code,digest=_parse(polytope,atoms,target)
        _fields(certificate,{'schema','input_hash','status','realized_values','cells','scope','authority_status'})
        if (certificate['schema']!='three-criterion-cell-certificate-v1'
                or certificate['input_hash']!=digest or certificate['scope']!=SCOPE
                or certificate['authority_status']!=AUTHORITY):
            raise ValueError('Identity or scope mismatch')
        cells=certificate['cells']; count=3**len(parsed)
        if not isinstance(cells,list) or len(cells)!=count: raise ValueError('Incomplete cell coverage')
        patterns=set(); values=set()
        for c in cells:
            if not isinstance(c,dict): raise ValueError('Cell object required')
            signs=c.get('signs')
            if (not isinstance(signs,list) or len(signs)!=len(parsed)
                    or any(type(s) is not int or s not in {-1,0,1} for s in signs)):
                raise ValueError('Exact ternary sign pattern required')
            sig=tuple(signs)
            if sig in patterns: raise ValueError('Duplicate sign pattern')
            patterns.add(sig); rows=_cell_rows(base,parsed,sig)
            kind=c.get('kind')
            if kind=='POSITIVE_WITNESS':
                _fields(c,{'signs','kind','point'}); point=_vector(c['point'],4,4096)
                if point[-1]<=0 or any(_dot(a,point)>b for a,b in rows):
                    raise ValueError('Invalid strict cell witness')
                values.add(_truth(code,sig))
            elif kind in {'DUAL_ZERO_BOUND','FARKAS_CONTRADICTION'}:
                _fields(c,{'signs','kind','multipliers'}); y=_vector(c['multipliers'],len(rows),4096)
                if any(v<0 for v in y): raise ValueError('Negative certificate multiplier')
                vector=tuple(sum((y[i]*rows[i][0][j] for i in range(len(rows))),F(0)) for j in range(4))
                bound=sum((v*b for v,(_,b) in zip(y,rows)),F(0))
                if kind=='DUAL_ZERO_BOUND':
                    if vector!=(0,0,0,1) or bound>0: raise ValueError('Invalid dual bound')
                elif vector!=(0,0,0,0) or bound>=0: raise ValueError('Invalid Farkas contradiction')
            else: raise ValueError('Unknown cell certificate')
        expected=set(it.product([-1,0,1],repeat=len(parsed)))
        if patterns!=expected: raise ValueError('Incomplete sign coverage')
        reported=certificate['realized_values']
        if (not isinstance(reported,list) or any(type(v) is not bool for v in reported)
                or reported!=sorted(values) or certificate['status']!=_status(values)):
            raise ValueError('Verdict mismatch')
        return {'accepted':True,'scope':SCOPE,'authority_status':AUTHORITY}
    except (ValueError,TypeError,KeyError,ZeroDivisionError,OverflowError,RecursionError) as e:
        return {'accepted':False,'scope':'NO_CONCLUSION','reason':str(e)}
