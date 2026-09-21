"""A guarded fair-bit source with checked pure leaves and bounded prefix execution.
The unbounded tree's probability law is proved in MATHEMATICAL_PROOF.md, not by
these finite runs. Bits supplied by a caller need not be random; the probability
claims explicitly require independent fair bits.
"""
from dataclasses import dataclass
from boundaries import Rejection,load_json,dump_json
import reference as r
MAX_BITS=128
@dataclass(frozen=True)
class CheckedSampler:
    left:bytes
    right:bytes
    ty:tuple

def check(left,right)->CheckedSampler:
    l,rr=dump_json(left),dump_json(right)
    _,a=r.check(load_json(l));_,b=r.check(load_json(rr))
    if a!=b:raise Rejection('sampler: leaf types differ')
    return CheckedSampler(l,rr,a)

def run_prefix(p:CheckedSampler,bits)->dict:
    if type(p) is not CheckedSampler:raise Rejection('sampler: wrong checked object')
    # Recheck even caller-constructed dataclasses; no unchecked proof field accepted.
    good=check(load_json(p.left),load_json(p.right))
    if good!=p:raise Rejection('sampler: forged type')
    if type(bits) not in (list,tuple) or len(bits)>MAX_BITS or any(type(b) is not int or b not in (0,1) for b in bits):raise Rejection('sampler: bounded literal bits required')
    k,d=0,1
    for n,b in enumerate(bits,1):
        k,d=2*k+b,2*d
        if (k+1)*(k+1)+2*(k+1)*d-d*d<0:
            return {'status':'done','branch':'left','proof':load_json(p.left),'bits':n}
        if k*k+2*k*d-d*d>0:
            return {'status':'done','branch':'right','proof':load_json(p.right),'bits':n}
    return {'status':'pending','bits':len(bits),'cell':k}
