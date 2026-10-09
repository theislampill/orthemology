"""Certified arithmetic for a bounded-count, nonsaturating response instrument.
Intervals certify empirical log inversion. Statistical and causal assumptions
remain separate and are not authenticated by interval arithmetic.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import prod


class UncertifiedArithmetic(ValueError):pass


def exact(value):
    if isinstance(value,Q):return value
    if type(value) is int:return Q(value)
    raise TypeError('Certified arithmetic requires Fraction or exact integer inputs; floats are rejected.')


def subsets(mask,nonempty=False):
    return tuple(s for s in range(mask+1) if s&mask==s and (s or not nonempty))


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q
    def __post_init__(self):
        object.__setattr__(self,'lo',exact(self.lo));object.__setattr__(self,'hi',exact(self.hi))
        if self.lo>self.hi:raise ValueError('Reversed interval.')
    def __add__(self,other):return Interval(self.lo+other.lo,self.hi+other.hi)
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def scale(self,integer):return Interval(self.lo*integer,self.hi*integer) if integer>=0 else Interval(self.hi*integer,self.lo*integer)
    def divide(self,other):
        if other.lo<=0<=other.hi:raise UncertifiedArithmetic('Denominator interval includes zero.')
        values=[a/b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return Interval(min(values),max(values))


def log_interval(value,terms):
    """Rational artanh series with rigorous one-sided geometric tail."""
    value=exact(value)
    if type(terms) is not int or terms<1:raise ValueError('A positive integer term count is required.')
    if value<=0:raise ValueError('Positive rational and at least one term required.')
    z=(value-1)/(value+1)
    if not z:return Interval(Q(0),Q(0))
    partial=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)),Q(0))
    tail=2*abs(z)**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return Interval(partial,partial+tail) if z>0 else Interval(partial-tail,partial)


def general_log_interval(value,terms=16):
    """Range reduction keeps the certified log budget short even for large L/delta."""
    value=exact(value)
    if value<=0:raise ValueError('Positive value required.')
    exponent=0;reduced=value
    while reduced>=2:reduced/=2;exponent+=1
    while reduced<1:reduced*=2;exponent-=1
    return log_interval(reduced,terms)+log_interval(Q(2),terms).scale(exponent)


def parameters(root_count,bound):
    if type(root_count) is not int or type(bound) is not int or root_count<1 or bound<1:raise ValueError('r and valid route bound K must be positive integers.')
    p=Q(1,2*bound);epsilon=p**root_count/Q(16*2**root_count)
    return p,epsilon


def uniform_log_tail(terms):
    z=Q(3,5)
    return 2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))


def required_terms(root_count,bound):
    """Finite precision target on the statistical good event; no arbitrary cap."""
    p,_=parameters(root_count,bound)
    target=p**(2*root_count)/Q(64*2**root_count)
    terms=1
    while uniform_log_tail(terms)>target:terms*=2
    return terms


def certify_support_counts(estimates,root_count,bound,max_terms=None):
    p,_=parameters(root_count,bound);universe=(1<<root_count)-1
    estimates={key:exact(q) for key,q in estimates.items()}
    if set(estimates)!=set(subsets(universe,True)):raise ValueError('Complete nonempty mask panel required.')
    if any(not Q(1,4)<=q<=1 for q in estimates.values()):
        raise UncertifiedArithmetic('Empirical panel is outside the certified logarithm region.')
    terms=required_terms(root_count,bound)
    if max_terms is not None and terms>max_terms:
        raise UncertifiedArithmetic(f'Need {terms} series terms; supplied budget is {max_terms}.')
    logs={0:Interval(Q(0),Q(0)),**{mask:log_interval(q,terms) for mask,q in estimates.items()}}
    denominators={degree:log_interval(1-p**degree,terms) for degree in range(1,root_count+1)}
    result={};certificates={}
    for positive in subsets(universe,True):
        numerator=Interval(Q(0),Q(0))
        for mask in subsets(positive):
            value=logs[mask]
            numerator+=value if (positive.bit_count()-mask.bit_count())%2==0 else -value
        quotient=numerator.divide(denominators[positive.bit_count()])
        candidate=(quotient.lo+Q(1,2)).numerator//(quotient.lo+Q(1,2)).denominator
        if not quotient.lo>candidate-Q(1,2) or not quotient.hi<candidate+Q(1,2):
            raise UncertifiedArithmetic('The exact empirical inversion is not certified in one rounding cell.')
        if candidate<0:raise UncertifiedArithmetic('Negative recovered count.')
        if candidate:result[positive]=candidate
        certificates[positive]=quotient
    if sum(result.values())>bound:raise UncertifiedArithmetic('Recovered active route count exceeds K.')
    return result,{'series_terms':terms,'intervals':certificates,
                   'scope':'Rounding certificate for the empirical panel; truth requires the statistical good event and model assumptions.'}


def sample_budget(root_count,bound,coordinate_count,delta,robust_calibration=False):
    delta=exact(delta)
    if type(coordinate_count) is not int or coordinate_count<1 or not 0<delta<1:raise ValueError('Positive coordinate count and 0<delta<1 required.')
    p,epsilon=parameters(root_count,bound)
    sampling=epsilon/2 if robust_calibration else epsilon
    upper=general_log_interval(Q(2*coordinate_count)/delta).hi/(2*sampling*sampling)
    count=-((-upper.numerator)//upper.denominator)
    eta=epsilon/Q(2*bound*root_count) if robust_calibration else Q(0)
    return {'per_setting_trials':count,'sampling_tolerance':sampling,'total_probability_tolerance':epsilon,
            'per_incidence_calibration_tolerance':eta,'log_upper':general_log_interval(Q(2*coordinate_count)/delta).hi,
            'confidence_at_least':1-delta,'coordinate_count':coordinate_count}


def validate_model(model,root_count,effect_count,bound):
    root_universe=(1<<root_count)-1;effect_universe=(1<<effect_count)-1
    if effect_count<1 or sum(model.values())>bound:raise ValueError('Model exceeds declared catalogue/count class.')
    for (positive,negative,outputs),n in model.items():
        if not 0<positive<=root_universe or not 0<=negative<=root_universe or positive&negative or not 0<outputs<=effect_universe or not isinstance(n,int) or n<0:
            raise ValueError('Invalid histogram.')


def absence_probability(model,profile,mask,query,root_count,bound,rate_error=Q(0)):
    p,_=parameters(root_count,bound);answer=Q(1);rate_error=exact(rate_error)
    # An example bounded calibration perturbation; intended-zero masks may leak.
    rates={i:(p+(-1)**i*rate_error if mask>>i&1 else rate_error) for i in range(root_count)}
    if any(not 0<=v<=1 for v in rates.values()):raise ValueError('Invalid perturbed survival rate.')
    for (positive,negative,outputs),n in model.items():
        if positive&profile==positive and not negative&profile and outputs&query:
            survival=prod((rates[i] for i in range(root_count) if positive>>i&1),start=Q(1))
            answer*=(1-survival)**n
    return answer


def exact_panel(model,root_count,effect_count,bound,rate_error=Q(0)):
    validate_model(model,root_count,effect_count,bound)
    return {(s,t,u):absence_probability(model,s,t,u,root_count,bound,rate_error)
            for s in subsets((1<<root_count)-1,True) for t in subsets(s,True)
            for u in subsets((1<<effect_count)-1,True)}


def invert_hits(hits,effect_count):
    universe=(1<<effect_count)-1;h={0:0,**hits};total=h[universe]
    cumulative={v:total-h[universe^v] for v in subsets(universe)}
    return {t:sum((-1)**(t.bit_count()-v.bit_count())*cumulative[v] for v in subsets(t))
            for t in subsets(universe,True)}


def certify_guarded_effect_histogram(estimates,root_count,effect_count,bound,max_terms=None):
    roots=(1<<root_count)-1;effects=(1<<effect_count)-1
    expected={(s,t,u) for s in subsets(roots,True) for t in subsets(s,True) for u in subsets(effects,True)}
    if set(estimates)!=expected:raise ValueError('Incomplete issued-profile/mask/effect-query panel.')
    aggregate={};certificates={}
    for profile in subsets(roots,True):
        indices=[i for i in range(root_count) if profile>>i&1]
        def embed(local):return sum(1<<i for j,i in enumerate(indices) if local>>j&1)
        for query in subsets(effects,True):
            local={t:estimates[profile,embed(t),query] for t in subsets((1<<len(indices))-1,True)}
            counts,certificate=certify_support_counts(local,len(indices),bound,max_terms)
            aggregate[profile,query]={embed(p):n for p,n in counts.items()}
            certificates[profile,query]=certificate
    histogram={}
    for positive in subsets(roots,True):
        for negative in subsets(roots^positive):
            hits={u:sum((-1)**(negative.bit_count()-w.bit_count())*aggregate[roots^w,u].get(positive,0)
                        for w in subsets(negative)) for u in subsets(effects,True)}
            if any(v<0 for v in hits.values()):raise UncertifiedArithmetic('Inconsistent rounded guard counts.')
            for outputs,n in invert_hits(hits,effect_count).items():
                if n<0:raise UncertifiedArithmetic('Inconsistent rounded effect counts.')
                if n:histogram[positive,negative,outputs]=n
    validate_model(histogram,root_count,effect_count,bound)
    return histogram,certificates
