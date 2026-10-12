"""Independent marginal and middle-witness checks for composed interfaces."""
from fractions import Fraction as F
from random import Random
import json
from stochastic_refinement import Refinement,verify_refinement
from refinement_composition import compose_refinements,glue_couplings
from probe_stochastic_refinement import quotient_fixture,randdist,validate_witnesses


def expand_destination(rng,first):
    states=list(first.destination_obs);copies=rng.randrange(1,4)
    dest=[(y,j) for y in states for j in range(copies)]
    actions=sorted({a for x,a in first.destination_kernels})
    kernels={}
    for y,j in dest:
        for a in actions:
            choices=[]
            for law in first.destination_kernels[y,a]:
                expanded={}
                for ny,p in law.items():
                    for nj,q in randdist(rng,list(range(copies))).items():expanded[ny,nj]=p*q
                choices.append(expanded)
            kernels[(y,j),a]=tuple(choices)
    initial={}
    for y,p in first.destination_initial.items():
        for j,q in randdist(rng,list(range(copies))).items():initial[y,j]=p*q
    obs=set(first.destination_obs.values())
    return Refinement(source_obs=first.destination_obs,destination_obs={(y,j):first.destination_obs[y] for y,j in dest},
        relation={(y,(y,j),0) for y,j in dest},source_kernels=first.destination_kernels,destination_kernels=kernels,
        reconstruct={(0,o):o for o in obs},abstract_actions={(0,o):tuple(actions) for o in obs},
        translate={(0,o,a):a for o in obs for a in actions},
        update={(0,o,a,a,no):0 for o in obs for a in actions for no in obs},
        source_eligible=first.destination_eligible,destination_eligible=set(kernels),
        destination_warrant={(0,o,a) for o in obs for a in actions},
        source_bad=first.destination_bad,destination_bad={(y,j) for y,j in dest if y in first.destination_bad},
        source_safe=first.destination_safe,destination_safe=set(dest),
        source_initial=first.destination_initial,destination_initial=initial,initial_mode={o:0 for o in obs})


def run():
    rng=Random(202609301449);step_count=0;initial_count=0
    for _ in range(100):
        first=quotient_fixture(rng);second=expand_destination(rng,first)
        r1=verify_refinement(first);r2=verify_refinement(second)
        composite,projection=compose_refinements(first,second)
        rc=verify_refinement(composite,projection);validate_witnesses(composite,rc)
        initial=glue_couplings(r1['initial_coupling'],r2['initial_coupling'])
        for x,w in initial:
            mode=composite.initial_mode[composite.destination_obs[w]]
            assert (x,w,mode) in composite.relation
        initial_count+=1
        # Construct each transitive local coupling directly through a middle
        # witness, independently of the composite's fresh transportation solve.
        for x,w,(q,r) in composite.relation:
            y=next(y for xx,y,qq in first.relation if xx==x and qq==q and (y,w,r) in second.relation)
            o=second.destination_obs[w];mo=second.reconstruct[r,o]
            for a in composite.abstract_actions[(q,r),o]:
                b=first.translate[q,mo,a];c=second.translate[r,o,b]
                for di in range(len(second.destination_kernels[w,c])):
                    witness2=r2['step_couplings'][y,w,r,b,di]
                    witness1=r1['step_couplings'][x,y,q,a,witness2['source_kernel_index']]
                    glued=glue_couplings(witness1['coupling'],witness2['coupling'])
                    source=first.source_kernels[x,a][witness1['source_kernel_index']]
                    dest=second.destination_kernels[w,c][di]
                    for nx,p in source.items():assert sum(v for (xx,ww),v in glued.items() if xx==nx)==p
                    for nw,p in dest.items():assert sum(v for (xx,ww),v in glued.items() if ww==nw)==p
                    for nx,nw in glued:
                        mode=composite.update[(q,r),o,a,c,composite.destination_obs[nw]]
                        assert (nx,nw,mode) in composite.relation
                    step_count+=1
    result={'seed':202609301449,'three_plant_compositions':100,
            'initial_gluings':initial_count,'independently_glued_step_laws':step_count,
            'mismatches':0,'scope':'Exact finite certificates and gluing; no empirical model truth or global synthesis claim.'}
    with open('refinement_composition_results.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
