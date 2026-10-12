"""Finite diagnostics, not a metaphysical possibility certificate."""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json


def optimal_profiles(commands, output, objective):
    profiles=list(product(commands, repeat=2))
    top=max(objective(output(*p)) for p in profiles)
    return [p for p in profiles if objective(output(*p)) == top]


def knowledge(worlds, w, observer, proposition):
    """S5 knowledge through equality of independently specified observations."""
    accessible=[v for v in worlds if observer(v)==observer(w)]
    assert w in accessible
    return all(proposition(v) for v in accessible)


def undominated(commands, rivals, value, weak=True):
    def dominates(b,a):
        differences=[value(b,r)-value(a,r) for r in rivals]
        return (all(d>=0 for d in differences) and any(d>0 for d in differences)) if weak else all(d>0 for d in differences)
    return [a for a in commands if not any(b!=a and dominates(b,a) for b in commands)]


def fixedpoints(commands,f,g):
    return [(a,b) for a,b in product(commands,repeat=2) if a==f(b) and b==g(a)]


def anonymous_optima(worlds):
    return [w for w in worlds if w==(w[1],w[0])]


def scalar_power(agent, command):
    assert agent in ['A','B']
    assert command>=0
    return command


def run():
    c=tuple(range(3)); target=2
    add=lambda a,b:a+b
    quality=lambda y:-(y-target)**2
    worlds=optimal_profiles(c,add,quality)
    w=(1,1)
    prechoice=lambda p:('same necessary intrinsic power/reason facts',)
    postA=lambda p:p[0]
    epistemic={
        'worlds':worlds,
        'prechoice_A_knows_target':knowledge(worlds,w,prechoice,lambda p:add(*p)==target),
        'prechoice_A_knows_B_command_1':knowledge(worlds,w,prechoice,lambda p:p[1]==1),
        'postchoice_A_knows_B_command_1':knowledge(worlds,w,postA,lambda p:p[1]==1),
        'prechoice_knows_disjunction_of_three_plans':knowledge(worlds,w,prechoice,lambda p:p in [(0,2),(1,1),(2,0)]),
        'coarse_frames_are_information_ablation_controls_not_divine_ignorance':True,
        'omniscient_identity_frame_at_each_world':[{ 'world':v,'knows_own_command':knowledge(worlds,v,lambda p:p,lambda p:p[0]==v[0]),'knows_peer_command':knowledge(worlds,v,lambda p:p,lambda p:p[1]==v[1]),'knows_all_true_subset_propositions':all(knowledge(worlds,v,lambda p:p,lambda p:p in prop)==(v in prop) for mask in range(1<<len(worlds)) for prop in [{x for i,x in enumerate(worlds) if mask>>i&1}])} for v in worlds],
        'all_subset_propositions_factive':all(not knowledge(worlds,w,obs,lambda p:p in prop) or w in prop for obs in [prechoice,postA,lambda p:p] for mask in range(1<<len(worlds)) for prop in [{v for i,v in enumerate(worlds) if mask>>i&1}]),
    }
    # Factivity constrains truthful forecasts but does not select a joint plan.
    forecasts=[]
    for a,b,ka,kb in product(c,repeat=4):
        if ka==b and kb==a and a==target-ka and b==target-kb:
            forecasts.append((a,b,ka,kb))
    # Rules are expressed without an owner-labelled target or peer command input.
    anonymous=[]
    for q in range(1,7):
        cs=tuple(range(q+1)); W=optimal_profiles(cs,add,lambda y:-(y-q)**2)
        anonymous.append({'target':q,'optimal_profiles':W,'anonymous_fixed_profiles':anonymous_optima(W),'rational_anonymous_profile':[str(Fraction(q,2)),str(Fraction(q,2))], 'rational_target_attained':Fraction(q,2)+Fraction(q,2)==q})
    # Equal standing operations do not imply numeric identity of intrinsic roles.
    # The role norm is a disclosed extra warrant burden, not a discovered divine fact.
    q=Fraction(3); roles={'A':Fraction(1),'B':Fraction(2)}
    role_policy=lambda role: q*role/sum(roles.values())
    asymmetric={
        'source_neutral_target':str(q),
        'intrinsic_role_weights':{g:str(v) for g,v in roles.items()},
        'role_selected_commands':{g:str(role_policy(v)) for g,v in roles.items()},
        'equal_target_capacity':all(scalar_power(g,q)==q for g in roles),
        'whole_outcome':str(sum(role_policy(v) for v in roles.values())),
        'renaming_bearers_preserving_roles_preserves_commands':all(role_policy(roles[old])==role_policy({'Y':roles['A'],'X':roles['B']}[new]) for old,new in [('A','Y'),('B','X')]),
        'same_bearer_after_role_swap':{'A':str(role_policy(roles['B'])),'B':str(role_policy(roles['A']))},
        'peer_actual_exercise_input':False,
        'constitutive_norm_warrant':'UNESTABLISHED: actual equal originals have such permissible intrinsically distinct practical roles',
    }
    # OR: objective 1 is better than 0; there is no assigned preferred command.
    bor=lambda a,b:int(bool(a or b))
    ORworlds=optimal_profiles((0,1),bor,lambda y:y)
    dominance={
        'or_output_optima':ORworlds,
        'or_weakly_undominated_full_operational_domain':undominated((0,1),(0,1),bor,True),
        'or_strictly_undominated_full_operational_domain':undominated((0,1),(0,1),bor,False),
        'or_weakly_undominated_if_peer_known_active':undominated((0,1),(1,),bor,True),
        'or_weakly_undominated_if_peer_known_inactive':undominated((0,1),(0,),bor,True),
        'additive_weakly_undominated_full_domain':undominated(c,c,lambda a,b:quality(a+b),True),
    }
    fprules=list(product((0,1),repeat=2))
    fp=[]
    for f,g in product(fprules,repeat=2):
        fp.append({'A_rule':f,'B_rule':g,'fixedpoints':fixedpoints((0,1),lambda b:f[b],lambda a:g[a])})
    unique_cycle=fixedpoints(c,lambda b:min(b+1,2),lambda a:min(a+1,2))
    # Frozen command, with the peer present but its produced contribution suppressed.
    controls=[]
    for name,F,q,a,b in [('additive',add,2,1,1),('saturating',bor,1,1,1)]:
        controls.append({'family':name,'whole_intended_target':q,'actual_commands':[a,b], 'actual_output':F(a,b),'after_B_suppression_same_A':F(a,0),'after_A_suppression_same_B':F(0,b),'fixed_A_suffices':F(a,0)==q,'fixed_B_suffices':F(0,b)==q,'A_has_full_target_constructor':scalar_power('A',q)==q,'B_has_full_target_constructor':scalar_power('B',q)==q})
    # Pair transitions generated without peer inputs. All cycles are admissible
    # bi-infinite histories unless a further boundary or phase relation is supplied.
    def cycles(mapping):
        nodes=list(mapping); found=set()
        for start in nodes:
            seen=[]; x=start
            while x not in seen:
                seen.append(x);x=mapping[x]
            cyc=seen[seen.index(x):]
            canonical=min(tuple(cyc[i:]+cyc[:i]) for i in range(len(cyc)))
            found.add(canonical)
        return sorted(found)
    histories={}
    for name,f in [('constant_one',lambda x:1),('identity',lambda x:x),('negation',lambda x:1-x)]:
        mapping={(a,b):(f(a),f(b)) for a,b in product((0,1),repeat=2)}
        cyc=cycles(mapping)
        histories[name]={'pair_cycles':cyc,'all_biinfinite_histories_concordant':all(a==b for cycle in cyc for a,b in cycle)}
    # Same observed profile, different dependencies. No productive conclusion
    # follows from the shared observation alone.
    dependency_models={
        'independent_intrinsic':{'actual':[1,1],'efficient_edges':[],'do_A_0_result':[0,1]},
        'B_receives_A_activation':{'actual':[1,1],'efficient_edges':[['A','B']],'do_A_0_result':[0,0]},
        'external_activation':{'actual':[1,1],'efficient_edges':[['T','A'],['T','B']],'do_A_0_result':[0,1]},
        'mutual_equilibrium_ternary':{'actual':unique_cycle,'efficient_edges_if_causal_reading':[['A','B'],['B','A']], 'unique_fixed_point_does_not_validate_productive_priority':True},
    }
    concentration=[{'A':a,'B':b,'sum':a+b,'same_A_executes_sum':scalar_power('A',a+b)==a+b,'same_B_executes_sum':scalar_power('B',a+b)==a+b} for a,b in product(range(9),repeat=2)]
    return {'schema':'intrinsic-willing-research/1','run_utc':datetime.now(timezone.utc).isoformat(),'scope':'Finite reason/knowledge/policy diagnostics. No full necessary-original model; no source-mode axiom.', 'epistemic':epistemic,'factive_forecast_choice_solutions':forecasts,'anonymous_rules':anonymous,'asymmetric_intrinsic_roles':asymmetric,'dominance':dominance,'boolean_forecast_fixedpoint_distribution':dict(Counter(len(r['fixedpoints']) for r in fp)),'boolean_forecast_rules':fp,'unique_mutual_ternary_fixedpoint':unique_cycle,'fixed_command_controls':controls,'autonomous_histories':histories,'dependency_models':dependency_models,'same_bearer_concentration':concentration}

if __name__=='__main__':
    result=run()
    output=Path(__file__).resolve().parents[1]/'results/EXPERIMENTS.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['boolean_forecast_rules','same_bearer_concentration']},indent=2))
