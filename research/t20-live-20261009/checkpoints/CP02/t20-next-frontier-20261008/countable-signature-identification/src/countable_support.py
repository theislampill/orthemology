"""Unknown finite support on countably indexed ports under one fixed calibration.
The code uses exact rational arithmetic and terminating elementary factorisation;
it makes no efficient-factorisation or physical-observation claim.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import prod


def encode_support(indices):
    indices=frozenset(indices)
    if not indices or any(type(i) is not int or i<0 for i in indices):
        raise ValueError('A nonempty finite subset of nonnegative integer indices is required.')
    return sum(1<<i for i in indices)


def decode_support(exponent):
    if type(exponent) is not int or exponent<1:raise ValueError('Positive support code required.')
    return frozenset(i for i in range(exponent.bit_length()) if exponent>>i&1)


def rate(index):
    if type(index) is not int or index<0:raise ValueError('Nonnegative port index required.')
    return Q(1,4**(1<<index))


def failure(exponent,base=4):return Q(base**exponent-1,base**exponent)


def probability(counts,base=4):
    if any(type(e) is not int or e<1 or type(n) is not int or n<0 for e,n in counts.items()):
        raise ValueError('Finite positive support codes and natural multiplicities required.')
    return prod((failure(e,base)**n for e,n in counts.items()),start=Q(1))


@lru_cache(maxsize=None)
def factor_integer(number):
    """Exact trial division, deliberately no unproved primality oracle."""
    if type(number) is not int or number<1:raise ValueError('Positive integer required.')
    n=number;result=[];divisor=2
    while divisor*divisor<=n:
        power=0
        while n%divisor==0:n//=divisor;power+=1
        if power:result.append((divisor,power))
        divisor=3 if divisor==2 else divisor+2
    if n>1:result.append((n,1))
    return tuple(result)


def valuation(value,prime):
    if value<=0:raise ValueError('Positive rational required.')
    def val(n):
        result=0
        while n%prime==0:n//=prime;result+=1
        return result
    return val(value.numerator)-val(value.denominator)


@lru_cache(maxsize=None)
def order_of_four(prime):
    if prime==2 or factor_integer(prime)!=((prime,1),):raise ValueError('An odd prime is required.')
    order=prime-1
    for divisor,_ in factor_integer(order):
        while order%divisor==0 and pow(4,order//divisor,prime)==1:order//=divisor
    assert pow(4,order,prime)==1
    assert all(pow(4,order//d,prime)!=1 for d,_ in factor_integer(order))
    return order


def denominator_weight(readout):
    denominator=readout.denominator
    if denominator&(denominator-1):raise ValueError('Denominator is not a power of four.')
    bit=denominator.bit_length()-1
    if bit%2:raise ValueError('Denominator is not a power of four.')
    return bit//2


def decode(readout):
    if type(readout) is int:readout=Q(readout)
    if not isinstance(readout,Q) or not 0<readout<=1:
        raise ValueError('An exact rational no-effect probability in (0,1] is required.')
    weight=denominator_weight(readout)
    factors=factor_integer(readout.numerator)
    candidates={}
    for prime,_ in factors:
        order=order_of_four(prime)
        if order>weight:raise ValueError('Prime order exceeds the observable denominator-weight bound.')
        candidates.setdefault(order,[]).append(prime)
    remaining=readout;counts={};steps=[]
    for exponent in sorted(candidates,reverse=True):
        prime=min(candidates[exponent]);factor=failure(exponent)
        coefficient=valuation(factor,prime)
        observed=valuation(remaining,prime)
        if coefficient<=0 or observed<0 or observed%coefficient:
            raise ValueError('Readout is outside the finite route class.')
        count=observed//coefficient
        if count:counts[exponent]=count;remaining/=factor**count
        steps.append({'exponent':exponent,'selected_prime':prime,'order':order_of_four(prime),
                      'factor_valuation':coefficient,'residual_valuation':observed,'count':count})
    if remaining!=1 or probability(counts)!=readout or sum(e*n for e,n in counts.items())!=weight:
        raise ValueError('Residual readout does not match the reconstructed histogram.')
    return counts,{'denominator_weight':weight,'numerator_factorisation':factors,'steps':steps,
                   'decoded_supports':{e:tuple(sorted(decode_support(e))) for e in counts},
                   'scope':'Finite integer histogram only; exact readout; no known largest port index supplied.'}


def primitive_prime_witness(exponent):
    return next((p for p,_ in factor_integer(4**exponent-1) if order_of_four(p)==exponent),None)


def hidden_guard_pair(profiles,excluded=()):
    """Pigeonhole search uses only 2^n+1 membership queries, not finite profiles."""
    seen={};excluded=frozenset(excluded)
    for index in range(2**len(profiles)+len(excluded)+1):
        if index in excluded:continue
        signature=tuple(bool(profile(index)) for profile in profiles)
        if signature in seen:return seen[signature],index,signature
        seen[signature]=index
    raise AssertionError('Finite pigeonhole principle violated.')


def guarded_probability(routes,profile):
    """routes=(finite positive-index set, finite absent-index set, count)."""
    factors=[]
    for positive,negative,count in routes:
        if not positive or positive&negative or count<0:raise ValueError('Invalid route.')
        if all(profile(i) for i in positive) and all(not profile(i) for i in negative):
            factors.append(failure(encode_support(positive))**count)
    return prod(factors,start=Q(1))


def finite_query_policy(oracle):
    """A small adaptive exact-query control, not the general impossibility proof."""
    transcript=[];profiles=[]
    def ask(name,profile):
        value=oracle(profile);transcript.append((name,value));profiles.append(profile);return value
    first=ask('all indices',lambda i:True)
    parity=0 if first<1 else 1
    second=ask(f'parity {parity}',lambda i:i%2==parity)
    residue=0 if second<=first else 1
    ask(f'mod3 {residue}',lambda i:i%3==residue)
    return tuple(transcript),tuple(profiles)


def greedy_infinite_prefix(target_exponent,last_exponent):
    """Finite prefix of an infinite real-product mimic, not a finite equality.

    The written proof uses Zsigmondy to rule out finite termination and the
    explicit error bound to establish the real-product limit.
    """
    if type(target_exponent) is not int or target_exponent<1 or last_exponent<=target_exponent:
        raise ValueError('Need positive target exponent and a later prefix bound.')
    target=failure(target_exponent);current=Q(1);counts={};records=[]
    for e in range(target_exponent+1,last_exponent+1):
        factor=failure(e);count=0
        while current*factor>=target:
            current*=factor;count+=1
        if count:counts[e]=count
        records.append({'exponent':e,'digit':count,'partial_product':current,
                        'error_upper_bound':target*(1/factor-1)})
    return counts,current,records


def compare_scope_queries(full_readout,restricted_readout):
    """A conditional witness classification, not authentication of an oracle.

    Soundness of a positive equality certificate requires the unguarded,
    independent, finite-support-per-route class (possibly infinitely many routes).
    """
    counts,trace=decode(full_readout)
    if type(restricted_readout) is int:restricted_readout=Q(restricted_readout)
    if not isinstance(restricted_readout,Q) or not 0<=restricted_readout<=1:
        raise ValueError('Exact probability required.')
    indices=frozenset().union(*(decode_support(e) for e in counts))
    if restricted_readout<full_readout:status='inconsistent_with_unguarded_restriction'
    elif restricted_readout==full_readout:status='conditional_finitude_certificate'
    else:status='finite_candidate_rejected_under_expanded_class'
    return {'candidate_counts':counts,'query_root_set':tuple(sorted(indices)),'status':status,
            'scope':'Exact supplied readouts and external response assumptions; not a finite-precision finiteness decision.'}
