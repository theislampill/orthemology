"""Exact transportation, incentive and finite-history correlation checks."""
from itertools import product
from fractions import Fraction as F
import json,random,time
from correlation import maximize_relation_mass,fixed_marginal_law_2x2
from restoration import classify_chain


def hall_deficit(mu,nu,relation):
    xs=tuple(mu);worst=F(0)
    for mask in range(1<<len(xs)):
        subset={x for i,x in enumerate(xs) if mask>>i&1}
        neighbors={y for x,y in relation if x in subset and y in nu}
        worst=max(worst,sum(mu[x] for x in subset)-sum(nu[y] for y in neighbors))
    return worst


def flow_checks(count=3000,seed=9301402):
    rng=random.Random(seed)
    for _ in range(count):
        n,m=rng.randrange(1,6),rng.randrange(1,6)
        left=[rng.randrange(1,10) for _ in range(n)];right=[rng.randrange(1,10) for _ in range(m)]
        mu={x:F(v,sum(left)) for x,v in enumerate(left)}
        nu={y:F(v,sum(right)) for y,v in enumerate(right)}
        relation={(x,y) for x,y in product(range(n),range(m)) if rng.randrange(2)}
        got=maximize_relation_mass(mu,nu,relation)
        assert got['minimum_violation']==hall_deficit(mu,nu,relation)
        law=got['coupling']
        assert sum(v for pair,v in law.items() if pair not in relation)==got['minimum_violation']
    return {'seed':seed,'rational_transport_instances':count,'hall_sharpness_mismatches':0}


def direct_ce(law,u,v):
    for a in range(2):
        if sum(law[a,b]*(u[a][b]-u[1-a][b]) for b in range(2))<0:return False
    for b in range(2):
        if sum(law[a,b]*(v[a][b]-v[a][1-b]) for a in range(2))<0:return False
    return True


def incentive_checks(count=4000,seed=9301403):
    rng=random.Random(seed);feasible=0
    pairs=tuple(product(range(2),repeat=2))
    for _ in range(count):
        p,q=F(rng.randrange(5),4),F(rng.randrange(5),4)
        target={pair for pair in pairs if rng.randrange(2)}
        allowed={pair for pair in pairs if rng.randrange(5)}
        games=[]
        for h in range(rng.randrange(3)):
            games.append(tuple(tuple(tuple(rng.randrange(3) for b in range(2)) for a in range(2))
                               for player in range(2)))
        actual=fixed_marginal_law_2x2(p,q,target,allowed=allowed,ce_games=games)
        # For integer payoffs 0..2 and quarter marginals, every interval endpoint
        # is a multiple of 1/48: CE slope denominator divides 4*lcm(1,2,3,4).
        # Hence this independent raw-inequality grid includes every LP vertex.
        candidates=[]
        for k in range(49):
            t=F(k,48);law={(0,0):t,(0,1):p-t,(1,0):q-t,(1,1):1-p-q+t}
            if any(v<0 for v in law.values()):continue
            if any(v>0 and pair not in allowed for pair,v in law.items()):continue
            if not all(direct_ce(law,*g) for g in games):continue
            candidates.append(sum(v for pair,v in law.items() if pair not in target))
        assert actual['feasible']==bool(candidates),(p,q,target,allowed,games,actual)
        if candidates:
            feasible+=1
            assert actual['minimum_violation']==min(candidates)
    return {'seed':seed,'constrained_or_robust_incentive_instances':count,
            'feasible_instances':feasible,'interval_vs_independent_vertex_grid_mismatches':0}


def temporal_checks(count=500,seed=9301404):
    rng=random.Random(seed)
    def survival(depth,path):
        if depth==0:return F(1)
        # Depend on the complete observed good-action history through this
        # recursively generated decision tree; marginals remain 3/4 and 1/4.
        t=F(rng.randrange(9),32)
        law={(0,0):t,(0,1):F(3,4)-t,(1,0):F(1,4)-t,(1,1):t}
        return sum(law[pair]*survival(depth-1,path+(pair,)) for pair in ((0,0),(1,1)))
    for _ in range(count):
        depth=rng.randrange(1,8)
        assert survival(depth,())<=F(1,2)**depth
    # Exact harmonic no-bad tail: defects 1/(t+2) are positive and divergent.
    for start in range(8):
        for length in range(1,20):
            value=F(1)
            for t in range(start,start+length):value*=1-F(1,t+2)
            assert value==F(start+1,start+length+1)
    # Hidden-state countermodel: public belief certification fails forever,
    # although every support path has at most one actual bad visit.
    kernel={0:{0:F(1)},1:{0:F(1)},2:{0:F(1,4),1:F(1,4),2:F(1,2)}}
    result=classify_chain(kernel,{2},{1})
    assert result['sure']
    belief={2}
    for _ in range(20):
        belief=set().union(*(set(kernel[x]) for x in belief))
        assert belief=={0,1,2} and not belief<={0,2}
    # Pairwise binary anticorrelation is feasible on every edge but not jointly
    # around a triangle; pairwise Hall tests do not solve a multiway coupling.
    half={0:F(1,2),1:F(1,2)};anti={(0,1),(1,0)}
    assert maximize_relation_mass(half,half,anti)['minimum_violation']==0
    global_profiles=[x for x in product((0,1),repeat=3)
                     if x[0]!=x[1] and x[1]!=x[2] and x[2]!=x[0]]
    assert not global_profiles
    return {'seed':seed,'adaptive_finite_history_tail_checks':count,
            'harmonic_product_checks':8*19,'public_certificate_gap_preserved':True,
            'pairwise_coupling_not_joint_fixture':True,
            'infinite_probability_theorem':'Proof and cited conditional Borel-Cantelli; not certified by finite tests.'}


def main():
    start=time.monotonic()
    r={'sharp_hall_deficit':flow_checks(),'incentive_constraints':incentive_checks(),
       'temporal_and_information_guards':temporal_checks()}
    r['elapsed_seconds']=round(time.monotonic()-start,3)
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
