"""Exact finite P14 checks; all examples are synthetic, never historical evidence."""
from itertools import product, permutations, combinations_with_replacement
from fractions import Fraction as F
from pathlib import Path
import json, random, sys, time
from epistemic import target_decoder, weight_witness_2d, is_nash_2x2
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from restoration import classify_chain


def order_checks():
    posets = comparisons = 0
    for n in range(1, 5):
        pairs = [(x,y) for x in range(n) for y in range(n) if x != y]
        for mask in range(1 << len(pairs)):
            relation = {(x,x) for x in range(n)} | {p for i,p in enumerate(pairs) if mask >> i & 1}
            if any((y,x) in relation for x,y in relation if x != y): continue
            if any((x,z) not in relation for x,y in relation for yy,z in relation if y == yy): continue
            posets += 1
            chain = all((x,y) in relation or (y,x) in relation for x in range(n) for y in range(n))
            embedded = False
            for ranks in permutations(range(n)):
                comparisons += 1
                if all(((x,y) in relation) == (ranks[x] <= ranks[y])
                       for x in range(n) for y in range(n)):
                    embedded = True
            assert embedded == chain
    return {'labelled_posets_up_to_four_points': posets,
            'injective_rank_maps_checked': comparisons, 'embedding_mismatches': 0}


def decoder_checks():
    checked = 0
    for n in range(1, 5):
        for scores in product(range(min(n,3)), repeat=n):
            image = tuple(sorted(set(scores)))
            for targets in product((0,1), repeat=n):
                decoder = target_decoder(tuple(range(n)), lambda i:scores[i], lambda i:targets[i])
                brute = any(all(values[image.index(scores[i])] == targets[i] for i in range(n))
                            for values in product((0,1), repeat=len(image)))
                assert (decoder is not None) == brute
                checked += 1
    return {'finite_score_target_pairs': checked, 'decoder_existence_mismatches': 0}


def gain_on_segment(d, e, interior):
    # Independently search the exact sign cells cut by the two coordinate roots.
    cut = {F(0),F(1)}
    for j in range(2):
        delta = e[j]-d[j]
        if delta:
            t = -d[j]/delta
            if 0 <= t <= 1: cut.add(t)
    cut = sorted(cut)
    candidates = cut + [(a+b)/2 for a,b in zip(cut,cut[1:])]
    for t in candidates:
        v = tuple((1-t)*d[j]+t*e[j] for j in range(2))
        if (all(x>0 for x in v) if interior else all(x>=0 for x in v) and any(x>0 for x in v)):
            return True
    return False


def direct_gain_exists(gains, interior=False):
    # In R^2 any positive-quadrant intersection of a compact convex polygon
    # extends along a positive ray to a boundary edge, so pairs of vertices suffice.
    return any(gain_on_segment(d,e,interior) for d,e in combinations_with_replacement(gains,2))


def vector_checks():
    points = tuple(product(range(3),repeat=2))
    mixtures = [(F(i,4),F(j,4),F(4-i-j,4)) for i in range(5) for j in range(5-i)]
    checked = strong = weak = 0
    for table in product(points, repeat=3):
        for mixture in mixtures:
            value = tuple(sum(mixture[i]*table[i][j] for i in range(3)) for j in range(2))
            gains = tuple(tuple(F(p[j])-value[j] for j in range(2)) for p in table)
            positive = weight_witness_2d(gains)
            nonnegative = weight_witness_2d(gains,strict_positive=False)
            assert (positive is not None) == (not direct_gain_exists(gains,False)), (table,mixture,gains)
            assert (nonnegative is not None) == (not direct_gain_exists(gains,True)), (table,mixture,gains)
            strong += positive is not None
            weak += nonnegative is not None
            checked += 1
    return {'three_response_two_coordinate_mixed_cases': checked,
            'nonzero_cone_equilibria': strong, 'interior_cone_equilibria': weak,
            'weight_vs_direct_convex_gain_mismatches': 0}


def game_checks(count=1200,seed=9301349):
    rng = random.Random(seed)
    weighted_eq = affine = 0
    for _ in range(count):
        tables = [tuple(tuple((F(rng.randrange(4)),F(rng.randrange(4))) for _ in range(2))
                        for _ in range(2)) for player in range(2)]
        p,q = F(rng.randrange(5),4),F(rng.randrange(5),4)
        player_options = [tuple(tuple(q*tables[0][i][0][j]+(1-q)*tables[0][i][1][j]
                                      for j in range(2)) for i in range(2)),
                          tuple(tuple(p*tables[1][0][i][j]+(1-p)*tables[1][1][i][j]
                                      for j in range(2)) for i in range(2))]
        weights=[]
        for options,mix in zip(player_options,(p,q)):
            value=tuple(mix*options[0][j]+(1-mix)*options[1][j] for j in range(2))
            gains=tuple(tuple(option[j]-value[j] for j in range(2)) for option in options)
            w=weight_witness_2d(gains)
            assert (w is not None)==(not direct_gain_exists(gains))
            weights.append(w)
        if all(w is not None for w in weights):
            scalar=[tuple(tuple(sum(w[j]*table[i][k][j] for j in range(2)) for k in range(2))
                           for i in range(2)) for table,w in zip(tables,weights)]
            assert is_nash_2x2(*scalar,p,q)
            weighted_eq+=1
        a=tuple(tuple(F(rng.randrange(-3,4)) for j in range(2)) for i in range(2))
        b=tuple(tuple(F(rng.randrange(-3,4)) for j in range(2)) for i in range(2))
        scale1,scale2=rng.randrange(1,5),rng.randrange(1,5)
        offset1,offset2=rng.randrange(-3,4),rng.randrange(-3,4)
        aa=tuple(tuple(scale1*x+offset1 for x in row) for row in a)
        bb=tuple(tuple(scale2*x+offset2 for x in row) for row in b)
        assert is_nash_2x2(a,b,p,q)==is_nash_2x2(aa,bb,p,q)
        affine+=1
    return {'seed':seed,'two_player_vector_profiles':count,
            'positive_weight_equilibrium_witnesses':weighted_eq,
            'affine_invariance_checks':affine,'mismatches':0}


def sharp_fixtures():
    a=((0,2),(1,0)); aa=((0,4),(1,0)); b=((1,0),(0,1))
    assert is_nash_2x2(a,b,F(1,2),F(2,3))
    assert not is_nash_2x2(aa,b,F(1,2),F(2,3))
    assert is_nash_2x2(aa,b,F(1,2),F(4,5))
    team=((2,0),(0,1))
    assert is_nash_2x2(team,team,F(0),F(0)) and team[1][1]<team[0][0]
    coordination=((1,0),(0,1))
    assert is_nash_2x2(coordination,coordination,F(1,2),F(1,2))
    profiles=tuple(product((0,1),repeat=2)); target={(0,0),(1,1)}
    independent={s:F(1,4) for s in profiles}
    correlated={s:F(1,2) for s in target}
    indep=classify_chain({s:independent for s in profiles},set(independent),set(profiles)-target)
    corr=classify_chain({s:correlated for s in profiles},set(correlated),set(profiles)-target)
    assert not indep['almost_sure'] and corr['sure']
    assert all(sum(mass for s,mass in independent.items() if s[i]==a)==
               sum(mass for s,mass in correlated.items() if s[i]==a)
               for i in (0,1) for a in (0,1))
    h=(F(88,100),F(56,100),F(61,100),F(94,100),F(73,100),F(81,100))
    r=(F(72,100),F(96,100),F(90,100),F(42,100),F(84,100),F(77,100))
    w=(F(15,100),F(30,100),F(20,100),F(10,100),F(15,100),F(10,100))
    v=(F(2,100),F(2,100),F(2,100),F(90,100),F(2,100),F(2,100))
    difference=lambda weights: sum(weight*(x-y) for weight,x,y in zip(weights,h,r))
    assert difference(w)<0<difference(v)
    # Curved compact convex counterexample: every sampled strictly positive
    # weight has a constructive improving point (-t²,t).
    for w1,w2 in product(range(1,10),repeat=2):
        t=min(F(1,2),F(w2,2*w1))
        assert 0<t<=1 and w1*(-t*t)+w2*t>0
    return {'nonlinear_mixed_equilibrium_columns':['2/3','4/5'],
            'suboptimal_common_interest_nash':True,
            'independent_mixed_nash_restores_almost_surely':False,
            'same_marginal_correlated_law_restores_surely':True,
            'schematic_pdf_weighted_differences':[str(difference(w)),str(difference(v))],
            'curved_payoff_positive_weight_obstructions':81,
            'historical_evidentiary_claims':False}


def main():
    start=time.monotonic()
    results={'finite_orders':order_checks(),'score_targets':decoder_checks(),
             'vector_scalarization':vector_checks(),'games_and_invariance':game_checks(),
             'sharp_fixtures':sharp_fixtures()}
    results['elapsed_seconds']=round(time.monotonic()-start,3)
    results['scope']='Exact rational synthetic checks; ordinary proofs establish general statements; no canonical or empirical adoption.'
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
