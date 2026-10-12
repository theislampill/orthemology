"""Exact interface composition, keeping middle-controller memory private."""
from collections import defaultdict
from fractions import Fraction
from stochastic_refinement import Refinement,verify_refinement


def glue_couplings(left,right):
    """Glue A×B and B×C laws with identical full B marginals into an A×C law."""
    if (not left or not right or sum(left.values())!=1 or sum(right.values())!=1
            or any((type(p) is not int and not isinstance(p,Fraction)) or p<=0
                   for p in list(left.values())+list(right.values()))):
        raise ValueError('Exact positive full probability laws required')
    middle_left=defaultdict(Fraction);middle_right=defaultdict(Fraction)
    for (x,y),p in left.items():middle_left[y]+=p
    for (y,z),p in right.items():middle_right[y]+=p
    if middle_left!=middle_right:raise ValueError('Middle marginals differ')
    result=defaultdict(Fraction)
    for (x,y),p in left.items():
        for (ny,z),q in right.items():
            if y==ny:result[x,z]+=p*q/middle_left[y]
    return dict(result)


def compose_refinements(first,second,first_projection=None,second_projection=None):
    """Compose two validated contracts over exactly the same middle plant.

    Returns the composite finite contract and its public projection. Source
    policy conformance and actual authority remain external proof obligations.
    """
    if not verify_refinement(first,first_projection)['valid']:
        raise ValueError('Invalid first interface')
    if not verify_refinement(second,second_projection)['valid']:
        raise ValueError('Invalid second interface')
    for left,right in ((first.destination_obs,second.source_obs),
            (first.destination_kernels,second.source_kernels),
            (first.destination_eligible,second.source_eligible),
            (first.destination_bad,second.source_bad),
            (first.destination_safe,second.source_safe),
            (first.destination_initial,second.source_initial)):
        if left!=right:raise ValueError('Middle plant/meaning/initial law differs')
    relation={(x,w,(q,r)) for x,y,q in first.relation
              for ny,w,r in second.relation if y==ny}
    modes={m for x,w,m in relation};observations=set(second.destination_obs.values())
    reconstruct={};menus={};translate={};update={}
    for q,r in modes:
        for o in observations:
            if (r,o) not in second.reconstruct:continue
            middle_o=second.reconstruct[r,o]
            if (q,middle_o) not in first.reconstruct:continue
            reconstruct[(q,r),o]=first.reconstruct[q,middle_o]
            actions=first.abstract_actions.get((q,middle_o),())
            middle_menu=second.abstract_actions.get((r,o),())
            for a in actions:
                b=first.translate[q,middle_o,a]
                if b not in middle_menu:raise ValueError('Intermediate action-menu mismatch')
                c=second.translate[r,o,b]
                translate[(q,r),o,a]=c
                for no in observations:
                    second_key=(r,o,b,c,no)
                    if second_key not in second.update:continue
                    nr=second.update[second_key]
                    if (nr,no) not in second.reconstruct:continue
                    middle_no=second.reconstruct[nr,no]
                    first_key=(q,middle_o,a,b,middle_no)
                    if first_key not in first.update:continue
                    nq=first.update[first_key]
                    update[(q,r),o,a,c,no]=(nq,nr)
            menus[(q,r),o]=actions
    initial={}
    for o,r in second.initial_mode.items():
        middle_o=second.reconstruct[r,o]
        initial[o]=(first.initial_mode[middle_o],r)
    all_modes=modes|set(initial.values())|set(update.values())
    projection={(q,r):(r if second_projection is None else second_projection[r])
                for q,r in all_modes}
    composite=Refinement(source_obs=first.source_obs,destination_obs=second.destination_obs,
        relation=relation,source_kernels=first.source_kernels,destination_kernels=second.destination_kernels,
        reconstruct=reconstruct,abstract_actions=menus,translate=translate,update=update,
        source_eligible=first.source_eligible,destination_eligible=second.destination_eligible,
        destination_warrant=second.destination_warrant,
        source_bad=first.source_bad,destination_bad=second.destination_bad,
        source_safe=first.source_safe,destination_safe=second.destination_safe,
        source_initial=first.source_initial,destination_initial=second.destination_initial,
        initial_mode=initial)
    # User-supplied readout relations are not composed implicitly. The caller
    # must supply/check the desired A-to-C readout meaning independently.
    result=verify_refinement(composite,projection)
    if not result['valid']:raise ValueError(('Constructed contract failed',result['violations']))
    return composite,projection
