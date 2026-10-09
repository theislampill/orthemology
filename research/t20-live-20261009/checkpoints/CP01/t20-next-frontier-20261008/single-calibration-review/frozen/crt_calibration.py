"""One calibrated rational vector for every nonempty finite root signature.
Assumes the earlier independent support-dependent route-success response law.
Decoding does not factor huge numerators or observe hidden route labels.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import prod,gcd,isqrt


def subsets(mask,nonempty=False):
    return tuple(s for s in range(mask+1) if s&mask==s and (s or not nonempty))


def prime_factors(n):
    answer=set();p=2
    while p*p<=n:
        while n%p==0:answer.add(p);n//=p
        p+=1
    if n>1:answer.add(n)
    return answer


def is_prime(n):
    return n>=2 and all(n%k for k in range(2,isqrt(n)+1))


def next_primes(lower_exclusive,count):
    result=[];n=lower_exclusive+1
    while len(result)<count:
        if is_prime(n):result.append(n)
        n+=1
    return tuple(result)


def primitive_root(q):
    if q==2:return 1
    factors=prime_factors(q-1)
    return next(g for g in range(2,q) if all(pow(g,(q-1)//p,q)!=1 for p in factors))


def selector_exponents(root_count,selected):
    if root_count<1 or not 0<selected<1<<root_count:raise ValueError('A nonempty support is required.')
    inside=[i for i in range(root_count) if selected>>i&1]
    outside=[i for i in range(root_count) if not selected>>i&1]
    size=len(inside)
    result=[size]*root_count
    for i in inside[:-1]:result[i]=1
    result[inside[-1]]=-(size-1)
    return tuple(result)


def crt(residues,primes):
    modulus=prod(primes)
    return sum(value*(modulus//q)*pow(modulus//q,-1,q) for value,q in zip(residues,primes))%modulus


def valuation(value,prime):
    if value<=0:raise ValueError('A positive rational is required.')
    def multiplicity(n):
        result=0
        while n%prime==0:n//=prime;result+=1
        return result
    return multiplicity(value.numerator)-multiplicity(value.denominator)


@dataclass(frozen=True)
class Calibration:
    root_count: int
    denominator: int
    numerators: tuple
    private_primes: tuple
    primitive_roots: tuple
    exponent_rows: tuple
    residue_rows: tuple

    @property
    def universe(self):return (1<<self.root_count)-1
    @property
    def rates(self):return tuple(Q(b,self.denominator) for b in self.numerators)
    def failure(self,support):
        return 1-prod((rate for i,rate in enumerate(self.rates) if support>>i&1),start=Q(1))
    def probability(self,counts):
        return prod((self.failure(p)**n for p,n in counts.items()),start=Q(1))
    def diagonal(self):
        return tuple(valuation(self.failure(p),self.private_primes[p-1]) for p in subsets(self.universe,True))
    def decode(self,readout):
        answer={}
        for p,q,d in zip(subsets(self.universe,True),self.private_primes,self.diagonal()):
            power=valuation(readout,q)
            if power<0 or power%d:raise ValueError('Outside the exact calibration class.')
            if power:answer[p]=power//d
        if self.probability(answer)!=readout:raise ValueError('Additional unmodelled probability factors.')
        return answer


def construct(root_count):
    if not isinstance(root_count,int) or isinstance(root_count,bool) or root_count<1:
        raise ValueError('Positive finite root count required.')
    universe=(1<<root_count)-1
    primes=next_primes(root_count**2+1,universe)
    generators=tuple(primitive_root(q) for q in primes)
    exponents=tuple(selector_exponents(root_count,p) for p in subsets(universe,True))
    residues=tuple(tuple(pow(g,e%(q-1),q) for e in row) for row,g,q in zip(exponents,generators,primes))
    modulus=prod(primes)
    numerators=tuple(crt(tuple(row[i] for row in residues),primes) for i in range(root_count))
    return Calibration(root_count,modulus+1,numerators,primes,generators,exponents,residues)


def guarded_probability(calibration,counts,profile):
    return calibration.probability({p:sum(n for (p0,guard),n in counts.items() if p0==p and not guard&profile)
                                    for p in subsets(profile,True)})


def guarded_panel(calibration,counts):
    return {s:guarded_probability(calibration,counts,s) for s in subsets(calibration.universe,True)}


def recover_guarded(calibration,panel):
    aggregate={s:calibration.decode(q) for s,q in panel.items()}
    expected_profiles=subsets(calibration.universe,True)
    if set(aggregate)!=set(expected_profiles):raise ValueError('Every nonempty issued profile is required.')
    if any(p&s!=p for s,counts in aggregate.items() for p in counts):raise ValueError('Unissued positive root recovered.')
    result={}
    for p in expected_profiles:
        complement=calibration.universe^p
        for guard in subsets(complement):
            value=sum((-1)**(guard.bit_count()-w.bit_count())*aggregate[calibration.universe^w].get(p,0)
                      for w in subsets(guard))
            if value<0:raise ValueError('Negative recovered multiplicity.')
            if value:result[p,guard]=value
    if guarded_panel(calibration,result)!=panel:raise ValueError('Inconsistent exact panel.')
    return result
