"""Finite-description productive threshold source and its bounded interpreter.

The ideal source has states (n,k) for arbitrary finite n. `advance` below has an
explicit API cap, not a proof of unconditional termination. Each transition reads
ONE bit, so its unbounded specification is productive. The probability/cost
claims in the certificate are conditional on IID fair bits and are justified in
PROOFS_V4.md. They are not estimates of an arbitrary physical randomness source.
"""
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from boundaries import Rejection,load_json,dump_json
import productive as p
import reference as r

@dataclass(frozen=True)
class Program:
    source:bytes
    leaves:p.CheckedSampler
    max_bits:int

@dataclass(frozen=True)
class State:
    bits:int
    cell:int

def initial():return State(0,0)

def check(source)->Program:
    raw=dump_json(source);s=load_json(raw)
    if type(s) is not dict or set(s)!={'kind','left','right','max_bits'} or s['kind']!='quadratic':raise Rejection('sampler source: exact grammar required')
    n=s['max_bits']
    if type(n) is not int or not 1<=n<=p.MAX_BITS:raise Rejection('sampler source: finite cap')
    return Program(raw,p.check(s['left'],s['right']),n)

def validate_state(s:State):
    if type(s) is not State or type(s.bits) is not int or type(s.cell) is not int or not 0<=s.bits<p.MAX_BITS or not 0<=s.cell<(1<<s.bits):raise Rejection('sampler state: invalid bounded cell')
    d=1<<s.bits;k=s.cell
    low=k*k+2*k*d-d*d;high=low+2*k+1+2*d
    if not low<0<high:raise Rejection('sampler state: cell already settled')

def advance(s:State,bit:int):
    validate_state(s)
    if type(bit) is not int or bit not in (0,1):raise Rejection('sampler: literal bit required')
    # Counted transition kernel (validation and proof parsing are separate costs).
    n=s.bits+1;k=(s.cell<<1)+bit;d=1<<n
    low=k*k+((k*d)<<1)-d*d
    high=low+(k<<1)+1+(d<<1)
    branch='left' if high<0 else 'right' if low>0 else 'pending'
    return {'branch':branch,'next':State(n,k),
      'work':{'multiplications':3,'shifts':5,'additions':6,'subtractions':1,'comparisons':1 if high<0 else 2}}

def _recheck(program):
    if type(program) is not Program:raise Rejection('sampler source: expected checked Program')
    fresh=check(load_json(program.source))
    if fresh!=program:raise Rejection('sampler source: forged checked fields')
    return fresh

def run(program:Program,bits):
    program=_recheck(program)
    if type(bits) not in (tuple,list) or len(bits)>program.max_bits or any(type(x) is not int or x not in (0,1) for x in bits):raise Rejection('sampler: prefix exceeds source cap or is malformed')
    state=initial();work={k:0 for k in ('multiplications','shifts','additions','subtractions','comparisons')}
    for b in bits:
        q=advance(state,b);state=q['next']
        for k,v in q['work'].items():work[k]+=v
        if q['branch']!='pending':
            leaf=program.leaves.left if q['branch']=='left' else program.leaves.right
            return {'output':{'status':'done','branch':q['branch'],'proof':load_json(leaf),'bits':state.bits},'work':work,
              'work_scope':'transition arithmetic only; excludes state validation, parsing, checking, allocation and bit acquisition'}
    return {'output':{'status':'pending','bits':state.bits,'cell':state.cell},'work':work,
      'work_scope':'transition arithmetic only; excludes state validation, parsing, checking, allocation and bit acquisition'}

def pair(f):return [f.numerator,f.denominator]

def certificate(program:Program):
    program=_recheck(program);s=initial()
    for _ in range(program.max_bits):
        # Exactly one child straddles the irrational root at each depth.
        children=[advance(s,b) for b in (0,1)];remaining=[x['next'] for x in children if x['branch']=='pending']
        if len(remaining)!=1:raise Rejection('internal: unique boundary cell failed')
        s=remaining[0]
    d=1<<program.max_bits;tail=Fraction(1,d)
    return {'source_sha256':hashlib.sha256(program.source).hexdigest(),'status':'EXACT_DECLARED_FAIR_BIT_MODEL',
        'max_bits':program.max_bits,'left_mass':pair(Fraction(s.cell,d)),
        'right_mass':pair(Fraction(d-s.cell-1,d)),'pending_mass':pair(tail),
        'expected_bits':pair(2-2*tail),'ideal_expected_bits':[2,1],'ideal_second_moment_bits':[6,1],
        'assumptions':['independent fair input bits','declared quadratic threshold'],
        'cost_scope':'Expected bit count; arithmetic counters exclude validation, checking, allocation and bit acquisition',
        'kernel_verified':False}
