"""One SAME candidate combines intentions, factivity, choice, and actual support.
The imported provision interpreter is used unchanged; source adequacy is separate.
"""
from pathlib import Path
from itertools import product
from datetime import datetime,timezone
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
PROVISION=HERE.parents[1]/'provision-identity/src'
sys.path.insert(0,str(PROVISION))
from provision_semantics import IntendedAct,execute_intentions
from preservation_modes import uniform_realization


def powerset(xs):return [frozenset(x for i,x in enumerate(xs) if mask>>i&1) for mask in range(1<<len(xs))]

def choose_own_activity(g,q,commands):
    # Disclosed own-activity end, not a dependence on a peer's realised act.
    # Full target act is a substantive command interpretation, not an arbitrary
    # favourable full-power flag. Its event rules are built by the imported API.
    candidates=[IntendedAct(g,f'fixed-{g}',s) for s in commands if s==q and bool(s)]
    assert len(candidates)==1
    return candidates[0]


def serial(acts,q):
    events,supports,rules,exact=execute_intentions(acts)
    out=frozenset(k for k,state in events)
    individual={a.bearer:(out==q and a.exact_created_target==q and all(a.bearer in supports[e] for e in q)) for a in acts}
    entire={e:[g for g in ['A','B'] if supports[e]==frozenset([g])] for e in out}
    knowledge={a.bearer:{'own_token':a.token,'own_command':sorted(a.exact_created_target),'peer_acts':[{'bearer':b.bearer,'token':b.token,'command':sorted(b.exact_created_target)} for b in acts if b.bearer!=a.bearer], 'created_output':sorted(out),'active_rules':rules.copy(),'supports':{e:sorted(v) for e,v in supports.items()}} for a in acts}
    facts={'acts':[(a.bearer,a.token,tuple(sorted(a.exact_created_target))) for a in acts],'output':tuple(sorted(out)), 'support':[(e,tuple(sorted(v))) for e,v in sorted(supports.items())], 'rules':sorted(rules.items())}
    return {'events':events,'supports':{e:sorted(v) for e,v in supports.items()},'active_rules':rules,'exact_intention_satisfied':exact,'individual_own_activity_ends_satisfied':individual,
       'whole_effect_entire_providers':entire,'CND_whole_event':all(len(v)<=1 for v in entire.values()),'whole_event_entire_coverage':all(bool(v) for v in entire.values()),
       'knowledge':knowledge,'knowledge_factive':all(k['own_command']==sorted(next(a.exact_created_target for a in acts if a.bearer==g)) and k['created_output']==sorted(out) and k['supports']=={e:sorted(v) for e,v in supports.items()} and k['active_rules']==rules for g,k in knowledge.items()),
       'resolved_world_facts':facts,'both_participate_total_end':out==q and {a.bearer for a in acts}=={'A','B'} and all(a.exact_created_target for a in acts)}


def run():
    commands=powerset(('e0','e1'));records=[]
    for q in [s for s in commands if s]:
        a=choose_own_activity('A',q,commands);b=choose_own_activity('B',q,commands)
        joint=serial([a,b],q);solo=serial([a],q)
        uj=uniform_realization([a,b]);us=uniform_realization([a])
        weak_covers=[(s,t) for s,t in product(commands,repeat=2) if s and t and s|t==q]
        exact_covers=[]
        for s,t in weak_covers:
            r=execute_intentions([IntendedAct('A','A-candidate',s),IntendedAct('B','B-candidate',t)])
            if all(r[3].values()):exact_covers.append((s,t))
        # Primitive attribution remains free and is tested, never preset to pass.
        attribution=[]
        for mask in range(4):
            whole={g for i,g in enumerate(['A','B']) if mask>>i&1}
            attribution.append({'entire_relation':sorted(whole),'CND':len(whole)<=1,'coverage':bool(whole),'entire_meaning_excludes_coproducer':all({'A','B'}<={g} for g in whole)})
        records.append({'target':sorted(q),'weak_participation_cover_count':len(weak_covers),'exact_command_intention_preserving_cover_count':len(exact_covers),
            'joint':joint,'solo_same_A_act':solo,'reused_A_act_fields':{'bearer':a.bearer,'token':a.token,'exact_created_target':sorted(a.exact_created_target)},
            'created_output_equal':joint['events']==solo['events'],
            'actual_rule_equal':joint['active_rules']==solo['active_rules'],
            'uniform_rule_names_equal':uj[2]==us[2],
            'reencoding_preserves_created_output_support_and_intentions':uj[:2]==execute_intentions([a,b])[:2] and us[:2]==execute_intentions([a])[:2] and uj[3]==execute_intentions([a,b])[3] and us[3]==execute_intentions([a])[3],
            'actual_support_equal':joint['supports']==solo['supports'],
            'A_own_end_survives':solo['individual_own_activity_ends_satisfied']['A'],
            'A_total_knowledge_unchanged':joint['knowledge']['A']==solo['knowledge']['A'],
            'A_intrinsic_command_and_target_unchanged':joint['knowledge']['A']['own_command']==solo['knowledge']['A']['own_command'],
            'primitive_entire_attribution_scan':attribution,
            'any_attribution_has_CND_coverage_and_exclusive_entire_meaning':any(v['CND'] and v['coverage'] and v['entire_meaning_excludes_coproducer'] for v in attribution)})
    conflict=serial([IntendedAct('A','A-q',frozenset(['e0'])),IntendedAct('B','B-r',frozenset(['e1']))],frozenset(['e0']))
    p=PROVISION/'provision_semantics.py'
    return {'schema':'same-model-will-production/1','run_utc':datetime.now(timezone.utc).isoformat(),'import_binding':{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},
      'single_candidate':'direct coalescent event-set interpretation, not independent favourable examples',
      'source_warrant_NOT_established':['unique shared objective Q for these original bearers','particular own-full-Q activity is a pure fitting end','full-target command primitive adequately interprets decisive original willing','metaphysical warrant for primitive intrinsic knowing and choosing; structural nonreceipt is represented in the joined cognition enrichment','event-key ontology includes all actual created effects and contributions in required respect','source significance of invariant support change; branch-name switching is not a semantic invariant','exhaustive-support interpretation matches source entire original provision'],
      'records':records,'opposed_command_control':conflict,
      'result':'ONE_TYPED_RIVAL_EXECUTED; full target, own-activity and factivity can be combined, but actual support changes and whole-effect individual coverage is absent; branch labels are not a source-condition failure'}

if __name__=='__main__':
 r=run();p=HERE.parent/'results/JOINT_INTERPRETATION.json';p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
