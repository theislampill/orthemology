"""Prime-exponent instrument design for anonymous active positive supports.
No guard changes, no observed route labels, no metaphysical extra originals.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd,lcm


def supports(root_count):return tuple(range(1,1<<root_count))

def failure(support,rates):
    survival=Q(1)
    for i,p in enumerate(rates):
        if support>>i&1:survival*=p
    return 1-survival


def prime_exponents(q):
    if q<=0:raise ValueError('Nonzero rational failure required.')
    result={}
    for n,sign in ((q.numerator,1),(q.denominator,-1)):
        p=2
        while p*p<=n:
            while n%p==0:result[p]=result.get(p,0)+sign;n//=p
            p+=1
        if n>1:result[n]=result.get(n,0)+sign
    return {p:e for p,e in result.items() if e}


def probability(counts,rates):
    answer=Q(1)
    for support,n in counts.items():answer*=failure(support,rates)**n
    return answer


def matrix(probes):
    columns=supports(len(probes[0]));rows=[];labels=[]
    for probe_index,rates in enumerate(probes):
        factors=[prime_exponents(failure(s,rates)) for s in columns]
        primes=sorted(set().union(*(set(f) for f in factors)))
        for p in primes:
            rows.append([Q(f.get(p,0)) for f in factors]);labels.append((probe_index,p))
    return rows,labels


def rref(rows,column_count=None):
    a=[list(map(Q,row)) for row in rows];width=len(a[0]) if a else column_count or 0
    lead=0;pivots=[]
    for col in range(width):
        pivot=next((i for i in range(lead,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[lead],a[pivot]=a[pivot],a[lead]
        divisor=a[lead][col];a[lead]=[x/divisor for x in a[lead]]
        for i in range(len(a)):
            if i!=lead and a[i][col]:
                multiplier=a[i][col];a[i]=[x-multiplier*y for x,y in zip(a[i],a[lead])]
        pivots.append(col);lead+=1
        if lead==len(a):break
    return a,pivots


def rank(probes):
    rows,_=matrix(probes);return len(rref(rows)[1])


def kernel(probes):
    rows,_=matrix(probes);reduced,pivots=rref(rows)
    dimension=len(supports(len(probes[0])));basis=[]
    for free in range(dimension):
        if free in pivots:continue
        vector=[Q(0)]*dimension;vector[free]=1
        for i,pivot in enumerate(pivots):vector[pivot]=-reduced[i][free]
        denominator=lcm(*(v.denominator for v in vector));v=[int(x*denominator) for x in vector]
        divisor=gcd(*v);basis.append(tuple(x//abs(divisor) for x in v))
    return tuple(basis)


def recover(probes,readouts):
    rows,labels=matrix(probes);n=len(supports(len(probes[0])))
    if len(rref(rows)[1])<n:raise ValueError('Rank-deficient instrument on unrestricted counts.')
    augmented=[row+[Q(prime_exponents(readouts[k]).get(p,0))] for row,(k,p) in zip(rows,labels)]
    reduced,pivots=rref(augmented)
    if n in pivots:raise ValueError('Inconsistent readout.')
    values=[Q(0)]*n
    for i,pivot in enumerate(pivots):values[pivot]=reduced[i][-1]
    if any(v.denominator!=1 or v<0 for v in values):raise ValueError('Noninteger or negative reconstructed counts.')
    answer={s:int(v) for s,v in zip(supports(len(probes[0])),values) if v}
    if tuple(probability(answer,p) for p in probes)!=tuple(readouts):raise ValueError('Unmodelled prime factors in readout.')
    return answer


def subset_probes(root_count):
    return tuple(tuple(Q(1,2) if t>>i&1 else Q(0) for i in range(root_count)) for t in supports(root_count))


def recover_subset_panel(readouts,root_count):
    vals={0:0,**{t:prime_exponents(q).get(2,0) for t,q in zip(supports(root_count),readouts)}}
    answer={}
    for p in supports(root_count):
        weighted=sum((-1)**(p.bit_count()-t.bit_count())*vals[t] for t in range(p+1) if t&p==t)
        count=Q(-weighted,p.bit_count())
        if count.denominator!=1 or count<0:raise ValueError('Invalid subset-probe panel.')
        if count:answer[p]=int(count)
    if tuple(probability(answer,rates) for rates in subset_probes(root_count))!=tuple(readouts):
        raise ValueError('Inconsistent panel.')
    return answer


def guarded_probability(counts,profile,rates):
    answer=Q(1)
    for (p,n),count in counts.items():
        if p&profile==p and not n&profile:answer*=failure(p,rates)**count
    return answer


def lift_guard_kernel(vector,root_count):
    """Lift a full-profile kernel to equality at every issued profile."""
    universe=(1<<root_count)-1;positive={};negative={}
    for p,z in zip(supports(root_count),vector):
        complement=universe^p
        for n in range(complement+1):
            if n&complement==n:
                delta=(-1)**n.bit_count()*z
                if delta>0:positive[p,n]=delta
                elif delta<0:negative[p,n]=-delta
    # Shared baseline ensures unattenuated output at every nonempty profile.
    for i in range(root_count):
        key=(1<<i,0)
        positive[key]=positive.get(key,0)+1;negative[key]=negative.get(key,0)+1
    return positive,negative


def guarded_panel(counts,probes):
    return {s:tuple(guarded_probability(counts,s,p) for p in probes) for s in supports(len(probes[0]))}


def recover_guarded(probes,panel):
    root_count=len(probes[0]);universe=(1<<root_count)-1
    aggregate={s:recover(probes,panel[s]) for s in supports(root_count)}
    if any(p&s!=p for s,counts in aggregate.items() for p in counts):
        raise ValueError('A recovered support uses an unissued root.')
    answer={}
    for p in supports(root_count):
        complement=universe^p
        for n in range(complement+1):
            if n&complement!=n:continue
            value=sum((-1)**(n.bit_count()-w.bit_count())*aggregate[universe^w].get(p,0)
                      for w in range(n+1) if w&n==w)
            if value<0:raise ValueError('Negative guard multiplicity.')
            if value:answer[p,n]=value
    if guarded_panel(answer,probes)!=panel:raise ValueError('Inconsistent guarded panel.')
    return answer
