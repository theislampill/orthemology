"""Finite, exact certificates for a DECLARED observation-law grammar.

No estimator for arbitrary measures. The host is responsible for connecting the
model to a real data source. Two independently specified carriers are supported:
(1) a finite discrete program carrier; (2) a rational mixture of disjoint labelled
unit intervals, uniform within each. On an interval, view 0 hides its coordinate,
positive view m reveals its equal-width bin, and -1 reveals the real coordinate.
The full measurable event repertoire is explicit, never inferred from finite
source predicates. Actual random streams are not silently used as program outputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from boundaries import Rejection, bound_tree, dump_json

MAX_COMPONENTS=64
MAX_COARSE_BINS=256

def rational(x) -> Fraction:
    if type(x) not in (tuple,list) or len(x)!=2 or any(type(n) is not int for n in x):raise Rejection('probability: rational pair required')
    n,d=x
    if d<=0 or n<0 or n>d or max(n.bit_length(),d.bit_length())>128:raise Rejection('probability: bounded [0,1] rational required')
    return Fraction(n,d)

def pair(x:Fraction) -> list[int]:
    if max(x.numerator.bit_length(),x.denominator.bit_length())>256:raise Rejection('resource: probability arithmetic bits')
    return [x.numerator,x.denominator]

def total(xs) -> Fraction:
    s=Fraction(0)
    for x in xs:s+=x;pair(s)
    return s

@dataclass(frozen=True)
class Model:
    space:str
    law:str
    weights:tuple[Fraction,...]
    view:tuple[int,...]
    fingerprint:str
    defect:Fraction


def check(spec) -> Model:
    bound_tree(spec)
    if type(spec) is not dict or set(spec)!={'space','law','weights','view','events'}:raise Rejection('observation: exact model fields required')
    if spec['space'] not in ('finite-programs','tagged-uniform-intervals'):raise Rejection('observation: unsupported carrier (not an arbitrary-measure estimator)')
    if type(spec['law']) is not str or not 1<=len(spec['law'])<=128:raise Rejection('observation: law identity required')
    if spec['events']!='full-measurable':raise Rejection('observation: unrestricted measurable repertoire must be explicit')
    ws,vs=spec['weights'],spec['view']
    if type(ws) not in (list,tuple) or type(vs) not in (list,tuple) or not 1<=len(ws)<=MAX_COMPONENTS or len(ws)!=len(vs):raise Rejection('observation: finite component shape')
    weights=tuple(rational(w) for w in ws)
    if total(weights)!=1:raise Rejection('probability: law is not normalised')
    if any(type(v) is not int for v in vs):raise Rejection('observation: literal view indices required')
    if spec['space']=='finite-programs':
        if any(not 0<=v<=4096 for v in vs):raise Rejection('observation: finite carrier cannot acquire continuous outcomes by labelling')
        defect=Fraction(0)
    else:
        if any(not -1<=v<=128 for v in vs) or sum(max(v,1) for v in vs if v!=-1)>MAX_COARSE_BINS:raise Rejection('resource: finite observation bins')
        defect=total(w for w,v in zip(weights,vs) if v==-1)
    return Model(spec['space'],spec['law'],weights,tuple(vs),hashlib.sha256(dump_json(spec)).hexdigest(),defect)


def refinement(coarse, fine) -> dict:
    a,b=check(coarse),check(fine)
    if (a.space,a.law,a.weights)!=(b.space,b.law,b.weights):raise Rejection('refinement: base law/carrier changed')
    fibres=[]
    if a.space=='finite-programs':
        h={}
        for old,new in zip(a.view,b.view):
            if new in h and h[new]!=old:raise Rejection('refinement: no coarsening factorisation')
            h[new]=old
        for label in sorted(set(a.view)):
            weight=total(w for w,v in zip(a.weights,a.view) if v==label)
            if weight:fibres.append({'class':label,'weight':pair(weight),'conditional_defect':[0,1]})
    else:
        for i,(w,old,new) in enumerate(zip(a.weights,a.view,b.view)):
            allowed=(old==-1 and new==-1) or (old in (0,1)) or (old>1 and (new==-1 or new>0 and new%old==0))
            if not allowed:raise Rejection('refinement: coordinate information discarded or bins incompatible')
            if old!=-1 and w:
                bins=max(old,1)
                for j in range(bins):fibres.append({'component':i,'bin':j,'weight':pair(w/bins),'conditional_defect':[int(new==-1),1]})
    increment=total(Fraction(*x['weight'])*Fraction(*x['conditional_defect']) for x in fibres)
    if b.defect!=a.defect+increment:raise Rejection('internal: refinement identity failure')
    return {'status':'CHECKED_DECLARED_MODEL','theorem':'V4-Q1','coarse_fingerprint':a.fingerprint,'fine_fingerprint':b.fingerprint,
            'coarse_defect':pair(a.defect),'fine_defect':pair(b.defect),'increment':pair(increment),
            'positive_coarse_fibres':fibres,'equality':increment==0,
            'scope':'full measurable event family in declared law grammar; not empirical model identification'}


def certify(spec,epsilon) -> dict:
    m=check(spec);eps=rational(epsilon)
    if m.defect>eps:raise Rejection('probability: revised universal-failure obligation exceeds tolerance')
    return {'status':'CHECKED_DECLARED_MODEL','theorem':'V4-Q2/Q3','observation_fingerprint':m.fingerprint,
            'space':m.space,'law':m.law,'events':'full-measurable','defect':pair(m.defect),'epsilon':pair(eps),
            'scope':'finite exact symbolic calculation; external law identification is a trusted-host obligation'}
