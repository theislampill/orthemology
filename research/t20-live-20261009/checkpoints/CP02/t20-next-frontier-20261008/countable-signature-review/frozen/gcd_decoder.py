"""Factorisation-free finite-histogram decoder in expanded rational bit size."""
from fractions import Fraction as Q
from math import gcd
from countable_support import denominator_weight,probability,decode_support


class InvalidReadout(ValueError):pass
class ResourceInconclusive(RuntimeError):pass


def strip_shared(number,history):
    divisions=0
    while True:
        common=gcd(number,history)
        if common==1:return number,divisions
        number//=common;divisions+=1


def decode_gcd(readout,early_stop=True,max_weight=None):
    if type(readout) is int:readout=Q(readout)
    if not isinstance(readout,Q):raise TypeError('Exact Fraction or integer required.')
    if not 0<readout<=1:raise InvalidReadout('Finite no-effect probability must lie in (0,1].')
    try:weight=denominator_weight(readout)
    except ValueError as exc:raise InvalidReadout(str(exc)) from exc
    if max_weight is not None and weight>max_weight:
        raise ResourceInconclusive('Readout exceeds the supplied weighted-size resource budget.')
    if readout==1:return {},{'weight':0,'largest_generator':0,'selectors':[],'counts':[],'algorithm':'gcd'}
    if readout.numerator==1:raise InvalidReadout('No positive finite inventory has unit numerator.')
    history=1;uncovered=readout.numerator;selectors=[]
    strip_divisions=0;maximum_history_bits=1
    for exponent in range(1,weight+1):
        a=(1<<(2*exponent))-1
        component,steps=strip_shared(a,history);strip_divisions+=steps
        checks={'nontrivial':component>1,'divides_generator':a%component==0,
                'new_prime_support':gcd(component,history)==1,
                'full_prime_valuations':gcd(component,a//component)==1}
        if not all(checks.values()):raise ArithmeticError('Primitive-component certificate failed.')
        selectors.append({'exponent':exponent,'generator':a,'component':component,'checks':checks,
                          'previous_history_bits':history.bit_length()})
        history*=a;maximum_history_bits=max(maximum_history_bits,history.bit_length())
        if early_stop:
            uncovered,steps=strip_shared(uncovered,a);strip_divisions+=steps
            if uncovered==1:break
    if early_stop and uncovered!=1:raise InvalidReadout('Uncovered numerator factors remain beyond the weight bound.')
    residual=readout.numerator;counts={};count_steps=[];weighted_count=0
    for item in reversed(selectors):
        exponent=item['exponent'];a=item['generator'];component=item['component']
        temporary=residual;count=0
        while temporary%component==0:temporary//=component;count+=1
        if count:
            if weighted_count+exponent*count>weight:raise InvalidReadout('Recovered weighted count exceeds the denominator bound.')
            whole_factor=a**count
            if residual%whole_factor:raise InvalidReadout('Partial primitive data do not contain the complete generator.')
            residual//=whole_factor;counts[exponent]=count;weighted_count+=exponent*count
        count_steps.append({'exponent':exponent,'count':count})
    if residual!=1 or weighted_count!=weight or probability(counts)!=readout:
        raise InvalidReadout('Residual or denominator-weight identity failed.')
    return counts,{'weight':weight,'largest_generator':len(selectors),'selectors':selectors,'counts':count_steps,
                   'strip_divisions':strip_divisions,'maximum_history_bits':maximum_history_bits,
                   'decoded_supports':{e:tuple(sorted(decode_support(e))) for e in counts},
                   'algorithm':'gcd; no prime factorisation or multiplicative-order computation',
                   'complexity_scope':'Polynomial in expanded binary numerator/denominator length; no compact-expression or sampling-cost claim.'}


def histograms_of_weight(weight,maximum=None):
    """Finite integer-partition enumeration, an independent small-case oracle."""
    maximum=weight if maximum is None else min(maximum,weight)
    if weight==0:
        yield {};return
    if maximum==0:return
    for count in range(weight//maximum+1):
        for smaller in histograms_of_weight(weight-count*maximum,maximum-1):
            answer=dict(smaller)
            if count:answer[maximum]=count
            yield answer
