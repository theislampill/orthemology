"""Exact, bounded research checker for a continuous one-parameter bridge class.

It checks relative judgments, not substantive normative authority. It accepts
only rational profile data, an interval of strictly positive two-criterion
weights, and a closed Boolean language of affine score comparisons.
"""
import hashlib
import json
import re
from fractions import Fraction


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


KINDS = {'DESCRIPTIVE','NORMATIVE','MIXED','LOGICAL'}


def _fields(obj, names):
    if not isinstance(obj,dict) or set(obj) != set(names):
        raise ValueError('Missing or unknown fields')


def _fraction(x):
    if isinstance(x,bool) or not isinstance(x,(int,str)):
        raise ValueError('Exact integer or rational string required')
    if len(str(x)) > 128 or not re.fullmatch(r'[+-]?\d+(?:/\d+)?',str(x)):
        raise ValueError('Bounded rational syntax required')
    f=Fraction(x)
    if abs(f.numerator).bit_length()>128 or f.denominator.bit_length()>128:
        raise ValueError('Rational resource bound exceeded')
    return f


def _assumptions(rows, required=False):
    if not isinstance(rows,list) or len(rows)>64 or (required and not rows):
        raise ValueError('A bounded, explicit assumption list is required')
    seen=set()
    for r in rows:
        _fields(r,{'id','kind','text'})
        if (not isinstance(r['id'],str) or not r['id'] or len(r['id'])>128
                or r['id'] in seen or r['kind'] not in KINDS
                or not isinstance(r['text'],str) or not r['text'] or len(r['text'])>4096):
            raise ValueError('Invalid assumption record')
        seen.add(r['id'])


def _inputs(base, regime):
    _fields(base,{'schema','version','profiles','coordinate_kinds','extraction_assumptions'})
    if base['schema']!='profile-base-v1' or type(base['version']) is not int or base['version']<1:
        raise ValueError('Unsupported base schema/version')
    profiles=base['profiles']
    if not isinstance(profiles,dict) or not 1<=len(profiles)<=256:
        raise ValueError('A bounded nonempty profile set is required')
    parsed={}
    for name,values in profiles.items():
        if not isinstance(name,str) or not name or len(name)>128 or not isinstance(values,list) or len(values)!=2:
            raise ValueError('Exactly two coordinates per named profile are required')
        parsed[name]=tuple(map(_fraction,values))
    kinds=base['coordinate_kinds']
    if not isinstance(kinds,list) or len(kinds)!=2 or any(k not in KINDS for k in kinds):
        raise ValueError('Explicit coordinate kinds required')
    _assumptions(base['extraction_assumptions'])
    if any(k in {'NORMATIVE','MIXED'} for k in kinds) and not base['extraction_assumptions']:
        raise ValueError('Evaluated extraction needs disclosed assumptions')
    _fields(regime,{'schema','id','version','base_hash','lower','upper','orientation',
                    'admissibility_assumptions','authority_status'})
    if (regime['schema']!='two-criterion-weight-interval-v1'
            or not isinstance(regime['id'],str) or not regime['id']
            or len(regime['id'])>128
            or type(regime['version']) is not int or regime['version']<1):
        raise ValueError('Unsupported regime identity')
    if regime['base_hash']!=canonical_hash(base):
        raise ValueError('Regime is stale or bound to different data')
    if regime['authority_status']!='SUPPLIED_NOT_CERTIFIED':
        raise ValueError('The checker cannot certify substantive authority')
    _assumptions(regime['admissibility_assumptions'],required=True)
    orientation=regime['orientation']
    if (not isinstance(orientation,list) or len(orientation)!=2
            or any(type(v) is not int or v not in {-1,1} for v in orientation)):
        raise ValueError('Explicit signed coordinate orientation required')
    low,high=_fraction(regime['lower']),_fraction(regime['upper'])
    if not 0<low<1 or not 0<high<1:
        raise ValueError('Weight endpoints must be strictly between zero and one')
    pure=all(k in {'DESCRIPTIVE','LOGICAL'} for k in kinds) and all(
        a['kind'] in {'DESCRIPTIVE','LOGICAL'} for a in base['extraction_assumptions'])
    return parsed,orientation,low,high,pure


def _compile(target, profiles, orientation, atoms, budget, depth=0):
    budget[0]+=1
    if depth>16 or budget[0]>256 or not isinstance(target,dict):
        raise ValueError('Target syntax/resource limit')
    op=target.get('op')
    if op in {'gt','ge'}:
        _fields(target,{'op','left','right'})
        if target['left'] not in profiles or target['right'] not in profiles:
            raise ValueError('Unknown comparison profile')
        left,right=profiles[target['left']],profiles[target['right']]
        d=[orientation[i]*(left[i]-right[i]) for i in range(2)]
        a,b=d[0]-d[1],d[1]
        atoms.append((a,b))
        return ('cmp',op,a,b)
    if op=='const':
        _fields(target,{'op','value'})
        if type(target['value']) is not bool:
            raise ValueError('Boolean constant required')
        return ('const',target['value'])
    if op=='not':
        _fields(target,{'op','arg'})
        return ('not',_compile(target['arg'],profiles,orientation,atoms,budget,depth+1))
    if op in {'and','or'}:
        _fields(target,{'op','args'})
        if not isinstance(target['args'],list) or not 1<=len(target['args'])<=16:
            raise ValueError('Bounded nonempty Boolean argument list required')
        return (op,tuple(_compile(a,profiles,orientation,atoms,budget,depth+1) for a in target['args']))
    raise ValueError('Unknown target operation')


def _evaluate(code, alpha):
    if code[0]=='cmp':
        gain=code[2]*alpha+code[3]
        return gain>0 if code[1]=='gt' else gain>=0
    if code[0]=='const':
        return code[1]
    if code[0]=='not':
        return not _evaluate(code[1],alpha)
    vals=(_evaluate(c,alpha) for c in code[1])
    return all(vals) if code[0]=='and' else any(vals)


def analyze(base, regime, target):
    try:
        profiles,orientation,low,high,pure=_inputs(base,regime)
        atoms=[]
        code=_compile(target,profiles,orientation,atoms,[0])
        common={
            'base_declared_purely_descriptive':pure,
            'partition_check':'DECLARED_KINDS_ONLY_NOT_SEMANTIC_CERTIFICATION',
            'authority_status':'SUPPLIED_NOT_CERTIFIED',
            'scope':'RELATIVE_MODEL_DISCLOSURE_ONLY',
        }
        if low>high:
            return {**common,'status':'NO_ADMISSIBLE_EXTENSION','checked_cells':0,'witnesses':[]}
        cuts={low,high}
        for a,b in atoms:
            if a and low<=-b/a<=high:
                cuts.add(-b/a)
        cuts=sorted(cuts)
        representatives=set(cuts)
        representatives.update((a+b)/2 for a,b in zip(cuts,cuts[1:]))
        seen={}
        for alpha in sorted(representatives):
            val=_evaluate(code,alpha)
            if val not in seen:
                seen[val]={'alpha':str(alpha),'value':val}
        status=('DISAGREEMENT' if len(seen)==2 else
                'INVARIANT_TRUE' if True in seen else 'INVARIANT_FALSE')
        return {**common,'status':status,'checked_cells':len(representatives),
                'witnesses':list(seen.values())}
    except (ValueError,TypeError,KeyError,ZeroDivisionError,OverflowError) as e:
        return {'status':'INVALID','reason':str(e),'scope':'NO_CONCLUSION'}


def build_certificate(base, regime, target):
    r=analyze(base,regime,target)
    if r['status']=='INVALID':
        return {'schema':'gap-certificate-v1','status':'INVALID','reason':r['reason']}
    return {'schema':'gap-certificate-v1','base_hash':canonical_hash(base),
            'regime_hash':canonical_hash(regime),'target_hash':canonical_hash(target),
            'status':r['status'],'checked_cells':r['checked_cells'],'witnesses':r['witnesses'],
            'proof_rule':'AFFINE_ATOM_SIGN_PARTITION_V1',
            'scope':r['scope'],'authority_status':r['authority_status'],
            'base_declared_purely_descriptive':r['base_declared_purely_descriptive'],
            'partition_check':r['partition_check']}


def verify_certificate(base, regime, target, certificate):
    expected=build_certificate(base,regime,target)
    try:
        # Python structural equality equates True with 1 and False with 0.
        # Compare typed JSON encodings instead; these are certificate data.
        valid=(expected['status']!='INVALID' and isinstance(certificate,dict)
               and json.dumps(certificate,sort_keys=True,separators=(',',':'))
                   ==json.dumps(expected,sort_keys=True,separators=(',',':')))
    except (ValueError,TypeError,OverflowError,RecursionError):
        valid=False
    return {'accepted':valid,'scope':'RELATIVE_MODEL_DISCLOSURE_ONLY' if valid else 'NO_CONCLUSION',
            'reason':'Exact certificate readback matches' if valid else 'Input or certificate mismatch'}
