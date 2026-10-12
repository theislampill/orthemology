"""Exact mathematical diagnostics for the T20 source/inference review.

Standard library only. All arithmetic is rational. These functions check their
specified finite structures; they do not authenticate metaphysical possibility,
causation, human knowledge, source attribution, or philosophical premise warrant.
The Boolean explanation interpretation is independently implemented from the
checkpoint-18 statement, not imported from or compiled by its Lean sources.
"""
from fractions import Fraction
from itertools import product
from math import comb, factorial


def _p(x):
    if not isinstance(x, (int, Fraction)):
        raise TypeError('Use int or Fraction, not a rounded floating-point probability')
    x = Fraction(x)
    if not 0 <= x <= 1:
        raise ValueError('Probability outside [0,1]')
    return x


def bayes_uncaused(caused_k, uncaused, type_likelihood):
    """P(U|K); inputs are P(C and K), P(U), P(K|U), with C=not U."""
    e, d, a = map(_p, (caused_k, uncaused, type_likelihood))
    if e > 1-d:
        raise ValueError('Caused-K mass cannot exceed all caused mass')
    den = e + a*d
    if den == 0:
        raise ValueError('Conditioning event has probability zero')
    return a*d/den


def posterior_interval(prior_h, likelihood_h, alternate_low, alternate_high):
    """Sharp posterior bounds for H over a declared alternate-likelihood interval.

    This takes the interval and prior as assumptions. It does not supply their
    epistemic warrant or interpret a mathematical law as an efficient cause.
    """
    p, l, lo, hi = map(_p, (prior_h, likelihood_h, alternate_low, alternate_high))
    if lo > hi:
        raise ValueError('Reversed likelihood interval')
    numerator = p*l
    def posterior(q):
        den = numerator + (1-p)*q
        if den == 0:
            raise ValueError('Undefined posterior at an interval endpoint')
        return numerator/den
    return posterior(hi), posterior(lo)


def validate_law(law):
    if not isinstance(law, dict) or not law:
        raise ValueError('A nonempty explicit probability table is required')
    n = len(next(iter(law)))
    if n > 14:
        raise ValueError('Finite exhaustive interface is bounded to 14 bits')
    for state, mass in law.items():
        if not isinstance(state, tuple) or len(state) != n or any(x not in (0,1) for x in state):
            raise ValueError('States must be equal-length binary tuples')
        _p(mass)
    if sum(law.values(), Fraction(0)) != 1:
        raise ValueError('Mass must sum exactly to one')
    return n


def exchangeable(law):
    n = validate_law(law)
    by_count = {}
    for s in product((0,1), repeat=n):
        k, mass = sum(s), law.get(s, Fraction(0))
        if k in by_count and by_count[k] != mass:
            return False
        by_count[k] = mass
    return True


def covariance(law):
    n = validate_law(law)
    if n < 2:
        raise ValueError('Two coordinates required')
    e1 = sum((mass*s[0] for s,mass in law.items()), Fraction(0))
    e2 = sum((mass*s[1] for s,mass in law.items()), Fraction(0))
    e12 = sum((mass*s[0]*s[1] for s,mass in law.items()), Fraction(0))
    return e12-e1*e2


def bernoulli_mixture(n, components):
    if not isinstance(n,int) or not 0 <= n <= 14 or not components:
        raise ValueError('Nonempty mixture and 0 <= n <= 14 required')
    components = [(_p(w),_p(p)) for w,p in components]
    if sum(w for w,p in components) != 1:
        raise ValueError('Mixture weights must sum to one')
    law = {s:sum((w*p**sum(s)*(1-p)**(n-sum(s)) for w,p in components),Fraction(0))
           for s in product((0,1),repeat=n)}
    validate_law(law)
    return law


def fixed_heads_law(n,k):
    if not isinstance(n,int) or not isinstance(k,int) or not 0 <= k <= n <= 14:
        raise ValueError('Require 0 <= k <= n <= 14')
    return {s:Fraction(1,comb(n,k)) for s in product((0,1),repeat=n) if sum(s)==k}


def uniform_beta_word(n,k):
    if not isinstance(n,int) or not isinstance(k,int) or not 0 <= k <= n:
        raise ValueError('Require integers 0 <= k <= n')
    # Integral_0^1 theta^k (1-theta)^(n-k) dtheta; probability of ONE word.
    return Fraction(factorial(k)*factorial(n-k),factorial(n+1))


def minimal_supports(n,table):
    """All minimal positive sufficient supports of an explicitly monotone Boolean table.

    Bit i encodes input i. Holding a support true must guarantee the output
    for EVERY completion of other inputs. No actual-cause criterion is inferred.
    """
    if not isinstance(n,int) or not 0 <= n <= 12 or len(table)!=(1<<n):
        raise ValueError('Wrong finite truth-table shape')
    if any(v not in (0,1) for v in table):
        raise ValueError('Truth values must be Boolean')
    for s in range(1<<n):
        for i in range(n):
            if table[s] and not table[s|(1<<i)]:
                raise ValueError('Only monotone positive-support models are admitted')
    winning = [s for s in range(1<<n) if table[s]]
    minimal = [s for s in winning if not any(t != s and t&s==t for t in winning)]
    return [tuple(i for i in range(n) if s&(1<<i)) for s in minimal]


def common_requisite_check(worlds):
    worlds = list(worlds)
    if not worlds or any(len(row)!=3 or any(v not in (0,1) for v in row) for row in worlds):
        raise ValueError('A nonempty list of Boolean (P,N,R) worlds is required')
    premises = all((p or n) and (not p or r) and (not n or r) for p,n,r in worlds)
    conclusion = all(r for p,n,r in worlds)
    return {'premises':bool(premises),'r_necessary':bool(conclusion),
            'implication_valid':bool(not premises or conclusion)}


def rotating_witness_model():
    # A local counterinterpretation to moving from "some negative witness"
    # at each world to a single chosen witness at all worlds.
    worlds = [dict(p=1,r=1,n0=0,n1=0),dict(p=0,r=1,n0=1,n1=0),dict(p=0,r=0,n0=0,n1=1)]
    return {
        'worlds':worlds,
        'ns_prime':all(w['p'] or w['n0'] or w['n1'] for w in worlds),
        'negative_witnesses_entail_not_p':all(not (w['n0'] or w['n1']) or not w['p'] for w in worlds),
        'p_implies_r':all(not w['p'] or w['r'] for w in worlds),
        'n0_implies_r':all(not w['n0'] or w['r'] for w in worlds),
        'same_negative_witness_everywhere':any(all(w['p'] or w[key] for w in worlds) for key in ('n0','n1')),
        'r_contingent':any(w['r'] for w in worlds) and any(not w['r'] for w in worlds),
        'removed_r_world_has_another_negative_witness':bool(not worlds[2]['r'] and not worlds[2]['p'] and not worlds[2]['n0'] and worlds[2]['n1']),
    }


def _part(x,y): return (x&y)==x

def _members(mask,n): return [i+1 for i in range(n) if mask&(1<<i)]

def _singleton(f): return 1<<(f-1)


def restricted_explanation_model():
    # Nonempty subsets of two atoms. The target b is inside c but c is
    # neither a member nor a part of the target. E is stipulated, not endorsed.
    facts = [1,2,3]; b,c=2,3
    E = lambda x,S: x==c and S==_singleton(b)
    PE = lambda x,S: any(_part(x,z) and E(z,S) for z in facts)
    nec = all(not (PE(x,S) and y!=x and not _part(y,x)) or not PE(y,_singleton(x))
              for x in facts for S in range(1,8) for y in _members(S,3))
    full_trans = all(not(E(x,S) and E(y,T)) or E(x,T)
                     for x in facts for S in range(1,8) for y in _members(S,3) for T in range(1,8))
    partial_trans = all(not(PE(x,S) and E(y,T)) or PE(x,T)
                        for x in facts for S in range(1,8) for y in _members(S,3) for T in range(1,8))
    distribution = all(not(E(x,S) and _part(z,y)) or E(x,_singleton(z))
                       for x in facts for S in range(1,8) for y in _members(S,3) for z in facts)
    outside = c!=b and not _part(c,b)
    return {'facts':facts,'target':b,'explainer':c,'outside_target':outside,
            'target_part_of_explainer':_part(b,c),'reverse_externality':not _part(b,c),
            'restricted_package':bool(E(c,_singleton(b)) and outside and nec and full_trans and partial_trans and distribution),
            'no_extended_circles':nec,'complete_transitivity':full_trans,
            'partial_transitivity':partial_trans,'distribution':distribution,
            'metaphysical_explanation_authenticated':False}


def audit_boolean_explanation_model(padded=False):
    """Exhaustive finite replay of the checkpoint-18 15-fact interpretation.

    Transitivity's all-target quantifier is checked by exact integer bit-set
    inclusion, avoiding a quadratic loop through the 32767 pluralities.
    padded=True deliberately adds all-target explaining power to q-fusion-a;
    it is a negative control for source-side weakening, not a proposed repair.
    """
    facts = list(range(1,16)); n=15; q,a,b,e=1,2,4,8
    limit = 1<<n
    all_targets = (1<<limit)-2
    targetsets={x: (all_targets if x==q or (padded and x==3) else
                    (1<<_singleton(e) if x in (a,b) else 0)) for x in facts}
    partialsets={x:0 for x in facts}
    for x in facts:
        for z in facts:
            if _part(x,z): partialsets[x] |= targetsets[z]
    axioms={
        'parthood_reflexive':all(_part(x,x) for x in facts),
        'parthood_antisymmetric':all(not(_part(x,y) and _part(y,x)) or x==y for x in facts for y in facts),
        'parthood_transitive':all(not(_part(x,y) and _part(y,z)) or _part(x,z) for x in facts for y in facts for z in facts),
        'strong_supplementation':all(_part(x,y) or any(_part(z,x) and not(z&y) for z in facts) for x in facts for y in facts),
        'all_nonempty_fusions':True,'fusion_overlap':True,'fusion_least_upper_bound':True,
        'unrestricted_plural_psr':True,'complete_transitivity':True,'partial_transitivity':True,
        'distribution_to_members_and_parts':True,'partial_source_closure':True,
        'no_extended_circles':True,'no_empty_explanation':all(not(ts&1) for ts in targetsets.values()),
        'total_explainer_unique':True,
    }
    for x in facts:
        for y in facts:
            if _part(x,y) and partialsets[y]&~partialsets[x]: axioms['partial_source_closure']=False
    first_nec_failure=None
    tested_memberships=0
    for S in range(1,limit):
        members=_members(S,n)
        fusion=0
        for y in members: fusion |= y
        full=[x for x in facts if (targetsets[x]>>S)&1]
        partial=[x for x in facts if (partialsets[x]>>S)&1]
        axioms['unrestricted_plural_psr'] &= bool(full)
        axioms['all_nonempty_fusions'] &= fusion in facts and all(_part(y,fusion) for y in members)
        for z in facts:
            axioms['fusion_overlap'] &= bool(z&fusion)==any(z&y for y in members)
            axioms['fusion_least_upper_bound'] &= _part(fusion,z)==all(_part(y,z) for y in members)
        for x in full:
            for y in members:
                tested_memberships+=1
                axioms['complete_transitivity'] &= not bool(targetsets[y]&~targetsets[x])
                for z in facts:
                    if _part(z,y):
                        axioms['distribution_to_members_and_parts'] &= bool((targetsets[x]>>_singleton(z))&1)
        for x in partial:
            for y in members:
                axioms['partial_transitivity'] &= not bool(targetsets[y]&~partialsets[x])
                if y!=x and not _part(y,x) and ((partialsets[y]>>_singleton(x))&1):
                    axioms['no_extended_circles']=False
                    if first_nec_failure is None: first_nec_failure={'x':x,'S':S,'y':y}
    total=[x for x in facts if (targetsets[x]>>(limit-1))&1]
    local=[x for x in facts if (targetsets[x]>>_singleton(e))&1]
    axioms['total_explainer_unique']=len(total)==1
    return {'facts':n,'nonempty_pluralities':limit-1,'full_explanation_member_checks':tested_memberships,
            'axioms':{k:bool(v) for k,v in axioms.items()},'total_explainers':total,'local_explainers':local,
            'padded_negative_control':bool(padded),'first_nec_failure':first_nec_failure,
            'mereological_union_is_not_logical_conjunction':True,
            'metaphysical_realisation_authenticated':False}


def hierarchy_examples():
    worlds=range(3); R={(0,0),(0,1),(1,1),(1,2),(2,2)}; p={0,1}
    know=lambda P:{w for w in worlds if all(v in P for u,v in R if u==w)}
    kp=know(p);kkp=know(kp)
    return {'worlds':list(worlds),'accessibility':sorted(R),'p':sorted(p),'kp':sorted(kp),'kkp':sorted(kkp),
            'first_order_known':0 in kp,'knows_that_knows':0 in kkp,
            'reflexive':all((w,w) in R for w in worlds),
            'transitive':all((u,w) in R for u,v in R for v2,w in R if v==v2),
            'semantic_model_not_real_cognitive_episode':True}


def semantic_transfer(name):
    if name!='fact_atomicity_to_attribute_identity': raise ValueError('Unknown registered transfer')
    return {'explanatory_facts':['q'],'bearers':['g'],'real_attribute_tokens':['knowledge-g','power-g'],
            'qualification':[['g','knowledge-g'],['g','power-g']],
            'fact_part_relation':[['q','q']],
            'antecedent':True,'conclusion':False,'bridge_supplied':False,
            'scope':'No cross-sort mapping supplied; not a metaphysical realisation.'}


def compatibility_components(left_size, right_size, edges):
    """Connected components of a declared finite bipartite compatibility graph.

    A common output f(left)=g(right) on all edges is constant on components.
    Isolated declared states are retained. The graph's edges are assumptions,
    not a certificate of metaphysical compossibility or independent agency.
    """
    if (not isinstance(left_size,int) or not isinstance(right_size,int)
            or not 1 <= left_size <= 1000 or not 1 <= right_size <= 1000):
        raise ValueError('Both state factors must have sizes in [1,1000]')
    vertices=[('A',i) for i in range(left_size)]+[('B',j) for j in range(right_size)]
    neighbours={v:set() for v in vertices}
    for pair in edges:
        if not isinstance(pair,(tuple,list)) or len(pair)!=2:
            raise ValueError('Edges must be pairs of state indices')
        a,b=pair
        if not isinstance(a,int) or not isinstance(b,int) or not 0<=a<left_size or not 0<=b<right_size:
            raise ValueError('Endpoint outside the declared state factors')
        x,y=('A',a),('B',b)
        neighbours[x].add(y); neighbours[y].add(x)
    seen=set(); components=[]
    for v in vertices:
        if v in seen: continue
        todo=[v]; component=[]; seen.add(v)
        while todo:
            x=todo.pop(); component.append(x)
            for y in sorted(neighbours[x]):
                if y not in seen: seen.add(y);todo.append(y)
        components.append(sorted(component))
    return components
