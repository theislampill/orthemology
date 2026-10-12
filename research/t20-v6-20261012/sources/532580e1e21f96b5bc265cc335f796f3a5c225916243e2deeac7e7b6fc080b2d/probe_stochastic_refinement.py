"""Exact finite-cylinder marginal checks and seeded causal-coupling fixtures."""
from collections import defaultdict
from fractions import Fraction as F
from random import Random
import json
from stochastic_refinement import Refinement,verify_refinement
from test_stochastic_refinement import fixture


def policy(obs,actions):
    # Genuine history dependence: current observation alone is insufficient.
    # All actions remain in the declared menu. No hidden state is consulted.
    if obs[-1]=='good':return {'hold':F(1)}
    p=F(1+actions.count('hold'),2+len(actions)+actions.count('hold'))
    return {'step':p,'hold':1-p}


def prefix_check(horizon=9):
    c=fixture();cert=verify_refinement(c);assert cert['valid']
    # Each state retains the full physical history and the virtual action history.
    joint={((x,),(y,),(),(0,)):p for (x,y),p in cert['initial_coupling'].items()}
    src={((x,),()):p for x,p in c.source_initial.items()}
    dst={((y,),(),(0,)):p for y,p in c.destination_initial.items()}
    records=[]
    for n in range(horizon+1):
        left=defaultdict(F);right=defaultdict(F)
        for (xs,ys,aa,zz),p in joint.items():
            left[xs,aa]+=p;right[ys,aa,zz]+=p
            assert all((x,y,z) in c.relation for x,y,z in zip(xs,ys,zz))
        assert dict(left)==src and dict(right)==dst
        assert sum(joint.values())==sum(src.values())==sum(dst.values())==1
        records.append({'steps':n,'joint_cylinders':len(joint),'source_cylinders':len(src),
                        'destination_cylinders':len(dst),'both_exact_marginals':True})
        if n==horizon:break
        nj=defaultdict(F);ns=defaultdict(F);nd=defaultdict(F)
        for (xs,ys,aa,zz),p in joint.items():
            x,y,z=xs[-1],ys[-1],zz[-1];o=c.destination_obs[y]
            for a,pa in policy(tuple(c.source_obs[q] for q in xs),aa).items():
                b=c.translate[z,o,a]
                for (nx,ny),pk in cert['step_couplings'][x,y,z,a,0]['coupling'].items():
                    nz=c.update[z,o,a,b,c.destination_obs[ny]]
                    nj[xs+(nx,),ys+(ny,),aa+(a,),zz+(nz,)]+=p*pa*pk
        # The independent source and destination loops use only their own kernels.
        for (xs,aa),p in src.items():
            for a,pa in policy(tuple(c.source_obs[q] for q in xs),aa).items():
                for nx,pk in c.source_kernels[xs[-1],a][0].items():
                    ns[xs+(nx,),aa+(a,)]+=p*pa*pk
        for (ys,aa,zz),p in dst.items():
            virtual=tuple(c.reconstruct[z,c.destination_obs[y]] for y,z in zip(ys,zz))
            y,z=ys[-1],zz[-1];o=c.destination_obs[y]
            for a,pa in policy(virtual,aa).items():
                b=c.translate[z,o,a]
                for ny,pk in c.destination_kernels[y,b][0].items():
                    nz=c.update[z,o,a,b,c.destination_obs[ny]]
                    nd[ys+(ny,),aa+(a,),zz+(nz,)]+=p*pa*pk
        joint,src,dst=map(dict,(nj,ns,nd))
    return records


def randdist(rng,states):
    weights=[rng.randrange(1,10) for _ in states];total=sum(weights)
    return {q:F(w,total) for q,w in zip(states,weights)}


def quotient_fixture(rng):
    # Source has hidden clone states and a phase visible to its controller.
    # Destination omits both; a publicly updated two-mode transducer recovers phase.
    n,k=rng.randrange(2,5),rng.randrange(1,4)
    xs=[(b,j,z) for b in range(n) for j in range(k) for z in range(2)]
    ys=list(range(n));oa={x:(x[0],x[2]) for x in xs};ob={y:y for y in ys}
    block={(y,b):tuple(randdist(rng,ys) for _ in range(2)) for y in ys for b in range(4)}
    src={}
    for x in xs:
        y,j,z=x
        for a in range(2):
            menu=[]
            for coarse in block[y,2*z+a]:
                law={}
                for ny,mass in coarse.items():
                    for nj,p in randdist(rng,list(range(k))).items():law[ny,nj,1-z]=mass*p
                menu.append(law)
            src[x,a]=tuple(menu)
    init=randdist(rng,ys);si={}
    for y,mass in init.items():
        for j,p in randdist(rng,list(range(k))).items():si[y,j,0]=mass*p
    return Refinement(source_obs=oa,destination_obs=ob,
        relation={(x,x[0],x[2]) for x in xs},source_kernels=src,destination_kernels=block,
        reconstruct={(z,y):(y,z) for z in range(2) for y in ys},
        abstract_actions={(z,y):(0,1) for z in range(2) for y in ys},
        translate={(z,y,a):2*z+a for z in range(2) for y in ys for a in range(2)},
        update={(z,y,a,2*z+a,ny):1-z for z in range(2) for y in ys for a in range(2) for ny in ys},
        source_eligible=set(src),destination_eligible=set(block),
        destination_warrant={(z,y,2*z+a) for z in range(2) for y in ys for a in range(2)},
        source_bad={x for x in xs if x[0]==0},destination_bad={0},
        source_safe=set(xs),destination_safe=set(ys),source_initial=si,destination_initial=init,
        initial_mode={y:0 for y in ys})


def validate_witnesses(c,r):
    assert r['valid'],r['violations'];count=0
    for (x,y,z,a,di),w in r['step_couplings'].items():
        b=c.translate[z,c.destination_obs[y],a];joint=w['coupling']
        source=c.source_kernels[x,a][w['source_kernel_index']]
        destination=c.destination_kernels[y,b][di]
        assert sum(joint.values())==1
        assert all(sum(p for (nx,ny),p in joint.items() if nx==q)==v for q,v in source.items())
        assert all(sum(p for (nx,ny),p in joint.items() if ny==q)==v for q,v in destination.items())
        for nx,ny in joint:
            nz=c.update[z,c.destination_obs[y],a,b,c.destination_obs[ny]]
            assert (nx,ny,nz) in c.relation
        count+=1
    return count


def run():
    rng=Random(202609301433);steps=0;negative=0
    for _ in range(250):
        c=quotient_fixture(rng);steps+=validate_witnesses(c,verify_refinement(c))
        # Corrupt only destination warrant: stochastic consistency remains intact.
        c.destination_warrant.clear();r=verify_refinement(c)
        assert not r['valid'] and any(v[0]=='destination_warrant' for v in r['violations']);negative+=1
        assert len(r['step_couplings'])==len(c.relation)*4
    result={'seed':202609301433,'finite_prefix_marginals':prefix_check(),
            'two_mode_quotient_fixtures':250,'exact_step_couplings_rechecked':steps,
            'independent_warrant_negative_controls':negative,'mismatches':0,
            'limits':'Finite exact probes; the infinite-path theorem is proved separately, not inferred from horizon 9.'}
    with open('stochastic_refinement_results.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
