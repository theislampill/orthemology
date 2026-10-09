"""Endpoint-only identification under an explicit stochastic intervention law.

Counts concern distinct actual route occurrences in the supplied interpretation.
No readout exposes their IDs. Guards are evaluated on issued roots before any
incidence attenuation. Nothing here establishes that such actuators exist.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product

A,B,AB=1,2,3
TYPES=((A,0),(B,0),(AB,0),(A,B),(B,A))
RATES={A:Q(1,2),B:Q(1,3)}


def subsets(mask,nonempty=False):
    return tuple(s for s in range(mask+1) if s&mask==s and (s or not nonempty))


def enabled(positive,negative,profile):
    return positive&profile==positive and not negative&profile


def survival(positive,rates=RATES):
    result=Q(1)
    for root in (A,B):
        if positive&root:result*=rates[root]
    return result


def validate_model(model,effect_count):
    if not isinstance(effect_count,int) or effect_count<1:raise ValueError('A nonempty finite effect catalogue is required.')
    universe=(1<<effect_count)-1
    for (positive,negative,outputs),count in model.items():
        if (positive,negative) not in TYPES or not 0<outputs<=universe:
            raise ValueError('Outside the declared positive two-root direct-rule class.')
        if not isinstance(count,int) or isinstance(count,bool) or count<0:
            raise ValueError('Multiplicities are nonnegative integers.')


def absence_probability(model,profile,query,rates=RATES):
    """No queried effect occurs; independent productive incidences per route."""
    probability=Q(1)
    for (positive,negative,outputs),count in model.items():
        if outputs&query and enabled(positive,negative,profile):
            probability*=(1-survival(positive,rates))**count
    return probability


def prime_valuation(q,prime):
    if q<=0:raise ValueError('Exact finite-route absence probability is positive.')
    def val(n):
        result=0
        while n%prime==0:result+=1;n//=prime
        return result
    return val(q.numerator)-val(q.denominator)


def decode_ab(q):
    """Unique active root-support counts from a single exact rational readout."""
    c=prime_valuation(q,5);b=-prime_valuation(q,3)-c;a=b-c-prime_valuation(q,2)
    if min(a,b,c)<0 or Q(1,2)**a*Q(2,3)**b*Q(5,6)**c!=q:
        raise ValueError('Readout is outside the stipulated incidence model.')
    return a,b,c


def decode_solo(q,root):
    n=-prime_valuation(q,2) if root==A else -prime_valuation(q,3)
    if n<0 or (1-RATES[root])**n!=q:raise ValueError('Invalid solo readout.')
    return n


def endpoint_panel(model,effect_count):
    universe=(1<<effect_count)-1
    return {(profile,query):absence_probability(model,profile,query)
            for profile in (A,B,AB) for query in subsets(universe,True)}


def invert_hits(hits,effect_count):
    """Invert h(U)=sum_{T intersects U} n(T), with h(empty)=0."""
    universe=(1<<effect_count)-1
    h={0:0,**hits};total=h[universe]
    cumulative={v:total-h[universe^v] for v in subsets(universe)}
    return {t:sum((-1)**(t.bit_count()-v.bit_count())*cumulative[v] for v in subsets(t))
            for t in subsets(universe,True)}


def recover_model(panel,effect_count):
    universe=(1<<effect_count)-1
    hits={kind:{} for kind in TYPES}
    for query in subsets(universe,True):
        a,b,c=decode_ab(panel[AB,query])
        d=decode_solo(panel[A,query],A)-a
        e=decode_solo(panel[B,query],B)-b
        if min(d,e)<0:raise ValueError('Inconsistent guarded counts.')
        for kind,value in zip(TYPES,(a,b,c,d,e)):hits[kind][query]=value
    recovered={(*kind,t):count for kind,h in hits.items()
               for t,count in invert_hits(h,effect_count).items() if count}
    validate_model(recovered,effect_count)
    if endpoint_panel(recovered,effect_count)!=panel:
        raise ValueError('Panel is inconsistent with the declared class.')
    return recovered


@dataclass(frozen=True)
class Occurrence:
    token: str
    positive: int
    negative: int
    outputs: int


def unique_occurrences(records):
    by_id={}
    for record in records:
        if record.token in by_id and record!=by_id[record.token]:
            raise ValueError('Conflicting representations of one actual occurrence.')
        by_id[record.token]=record
    return tuple(by_id.values())


def occurrences(model):
    return tuple(Occurrence(f'{p}:{n}:{t}:{i}',p,n,t)
                 for (p,n,t),count in sorted(model.items()) for i in range(count))


def exact_distribution(records,profile,mode='incidence',rates=RATES,route_rate=Q(1,2)):
    """Independent finite enumeration; readout is only created-output subset.

    incidence: independent gate for each route/root incidence, guards frozen.
    shared_frozen: one efficacy gate per bearer, guards frozen.
    source_deletion: one gate per issued bearer, guards recomputed after deletion.
    route: one independent gate per active route, without root-selective rates.
    """
    records=unique_occurrences(records)
    active=tuple(r for r in records if enabled(r.positive,r.negative,profile))
    if mode=='incidence':
        gates={(r.token,g):rates[g] for r in active for g in (A,B) if r.positive&g}
    elif mode in ('shared_frozen','source_deletion'):
        gates={g:rates[g] for g in (A,B) if profile&g}
    elif mode=='route':gates={r.token:route_rate for r in active}
    else:raise ValueError(mode)
    keys=tuple(gates);distribution={}
    for values in product((False,True),repeat=len(keys)):
        assignment=dict(zip(keys,values));weight=Q(1)
        for key,value in assignment.items():weight*=gates[key] if value else 1-gates[key]
        outputs=0
        if mode=='source_deletion':
            resulting_profile=sum(g for g in (A,B) if assignment.get(g,False))
            surviving=(r for r in records if enabled(r.positive,r.negative,resulting_profile))
        elif mode=='incidence':
            surviving=(r for r in active if all(assignment[r.token,g] for g in (A,B) if r.positive&g))
        elif mode=='shared_frozen':
            surviving=(r for r in active if all(assignment[g] for g in (A,B) if r.positive&g))
        else:surviving=(r for r in active if assignment[r.token])
        for r in surviving:outputs|=r.outputs
        distribution[outputs]=distribution.get(outputs,Q(0))+weight
    return {k:v for k,v in distribution.items() if v}


def query_absence(distribution,query):
    return sum((p for outputs,p in distribution.items() if not outputs&query),Q(0))


def omitted_query_witness(effect_count,omitted):
    """Two nonnegative one-root models separated only by one hit coordinate."""
    universe=(1<<effect_count)-1;complement=universe^omitted
    positive={};negative={}
    # Common baseline makes every effect occur at unattenuated active A.
    for singleton in (1<<i for i in range(effect_count)):
        positive[A,0,singleton]=1;negative[A,0,singleton]=1
    for t in subsets(universe,True):
        if complement&t==complement:
            delta=(-1)**(t.bit_count()-complement.bit_count()+1)
            target=positive if delta>0 else negative
            target[A,0,t]=target.get((A,0,t),0)+1
    return positive,negative


def one_effect_fixture(kind):
    if kind=='coalescence':return {(AB,0,1):1,(A,B,1):1,(B,A,1):1}
    if kind=='redundant':return {(A,0,1):1,(B,0,1):1}
    if kind=='priority_A':return {(A,0,1):1,(B,A,1):1}
    raise ValueError(kind)
