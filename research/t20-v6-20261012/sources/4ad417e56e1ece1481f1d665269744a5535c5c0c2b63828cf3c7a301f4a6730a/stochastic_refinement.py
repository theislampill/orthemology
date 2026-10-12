"""Finite observation-compatible stochastic refinement certificates.

Exact for the declared local contract, not complete for all restorative migrations.
Warrant flags, public-state adequacy and model semantics remain supplied premises.
"""
from dataclasses import dataclass
from fractions import Fraction
from migration import coupling

@dataclass
class Refinement:
    source_obs:dict
    destination_obs:dict
    relation:set
    source_kernels:dict
    destination_kernels:dict
    reconstruct:dict
    abstract_actions:dict
    translate:dict
    update:dict
    source_eligible:set
    destination_eligible:set
    destination_warrant:set
    source_bad:set
    destination_bad:set
    source_safe:set
    destination_safe:set
    source_initial:dict
    destination_initial:dict
    initial_mode:dict
    readout_pairs:set | None = None


def verify_refinement(c,public_projection=None):
    """Check the all-public contract, or an explicit private/public projection.

    With a projection, finite modes are controller-private; only their projected
    public state may index warrant or public update consistency.
    """
    violations=[];witnesses={};public_updates={}
    modes={z for x,y,z in c.relation} | set(c.initial_mode.values()) | set(c.update.values())
    projection={z:z for z in modes} if public_projection is None else public_projection
    for z in modes:
        if z not in projection:violations.append(('missing_public_projection',z))
    source_states=set(c.source_obs);destination_states=set(c.destination_obs)
    def distribution(k,states,label):
        if (not isinstance(k,dict) or not k or not set(k)<=states
                or any((type(v) is not int and not isinstance(v,Fraction)) or v<=0 for v in k.values())
                or sum(k.values())!=1):
            violations.append(('invalid_distribution',label))
            return False
        return True
    initial_ok=distribution(c.source_initial,source_states,'source initial')
    initial_ok=distribution(c.destination_initial,destination_states,'destination initial') and initial_ok
    for role,kernels,states in (('source',c.source_kernels,source_states),
                                ('destination',c.destination_kernels,destination_states)):
        for key,choices in kernels.items():
            if not choices:violations.append(('empty_kernel_menu',role,key))
            for index,kernel in enumerate(choices):distribution(kernel,states,(role,key,index))
    if violations:
        return {'valid':False,'violations':violations,'step_couplings':{},'initial_coupling':None}
    for x,y,z in c.relation:
        if x not in source_states or y not in destination_states:
            violations.append(('unknown_related_state',x,y,z));continue
        observation=c.destination_obs[y]
        if ((z,observation) not in c.reconstruct or
                c.reconstruct[z,observation]!=c.source_obs[x]):
            violations.append(('observation_incompatibility',x,y,z))
        if y in c.destination_bad and x not in c.source_bad:
            violations.append(('bad_reflection',x,y,z))
        if x in c.source_safe and y not in c.destination_safe:
            violations.append(('safe_reflection',x,y,z))
        if c.readout_pairs is not None and (x,y) not in c.readout_pairs:
            violations.append(('readout',x,y,z))
        actions=c.abstract_actions.get((z,observation),())
        if not actions:
            violations.append(('empty_abstract_action_menu',z,observation))
        for a in actions:
            if (x,a) not in c.source_eligible:
                violations.append(('source_eligibility',x,a))
            if (z,observation,a) not in c.translate:
                violations.append(('missing_public_translation',z,observation,a));continue
            b=c.translate[z,observation,a]
            if (y,b) not in c.destination_eligible:
                violations.append(('destination_eligibility',y,b))
            if (projection[z],observation,b) not in c.destination_warrant:
                violations.append(('destination_warrant',projection[z],observation,b))
            sources=c.source_kernels.get((x,a),())
            destinations=c.destination_kernels.get((y,b),())
            if not sources or not destinations:
                violations.append(('missing_kernel_menu',x,y,z,a,b));continue
            for dst_index,destination_kernel in enumerate(destinations):
                allowed=set()
                for ny in destination_kernel:
                    next_observation=c.destination_obs[ny]
                    update_key=(z,observation,a,b,next_observation)
                    if update_key not in c.update:
                        violations.append(('missing_public_update',)+update_key);continue
                    nz=c.update[update_key]
                    public_key=(projection[z],observation,b,next_observation)
                    if public_key in public_updates and public_updates[public_key]!=projection[nz]:
                        violations.append(('nonpublic_mode_update',)+public_key)
                    else:
                        public_updates[public_key]=projection[nz]
                    for nx in source_states:
                        if (nx,ny,nz) in c.relation:allowed.add((nx,ny))
                found=None
                for src_index,source_kernel in enumerate(sources):
                    joint=coupling(source_kernel,destination_kernel,allowed)
                    if joint is not None:
                        found={'source_kernel_index':src_index,'coupling':joint}
                        break
                if found is None:
                    violations.append(('no_full_kernel_coupling',x,y,z,a,b,dst_index))
                else:
                    witnesses[x,y,z,a,dst_index]=found
    initial_allowed={(x,y) for x,y,z in c.relation
                     if y in c.destination_obs and
                     c.initial_mode.get(c.destination_obs[y],object())==z}
    initial_joint=coupling(c.source_initial,c.destination_initial,initial_allowed) if initial_ok else None
    if initial_joint is None:violations.append(('initial_coupling_absent',))
    return {'valid':not violations,'violations':violations,
            'step_couplings':witnesses,'initial_coupling':initial_joint,
            'mode_scope':('all_public' if public_projection is None else 'explicit_private_public_projection'),
            'scope':'Finite causal-coupling contract; semantic authority and actual-world adequacy are not inferred.'}
