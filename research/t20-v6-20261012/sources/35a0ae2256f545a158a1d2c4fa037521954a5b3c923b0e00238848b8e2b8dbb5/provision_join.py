"""Read-only adapter joining a selected resource interpretation to actual proofs.

The underlying engine is separately owned by the provision/identity lane.
Standing-resource originality here is an INTERPRETATION INPUT; it is not derived
from an issued act, a root label, event identity, or this adapter's computation.
Contribution incidences are not silently counted as extra created substances.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, importlib.util, json, sys
from itertools import combinations
sys.dont_write_bytecode = True

SOURCE = Path(__file__).resolve().parent.parent / 'provision-identity/src/provision_semantics.py'
spec = importlib.util.spec_from_file_location('t20_shared_provision_semantics',SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)

@dataclass(frozen=True)
class StandingResource:
    key: str
    bearer: str
    actual: bool
    designated_whole_original: bool

RESOURCES = {b:StandingResource('resource-'+b,b,True,True) for b in engine.ROOTS}

def inspect_case(case):
    rules = (engine.created_rules(case) if case == 'persistent_created_mechanism'
             else engine.direct_rules(case))
    executed = engine.run(rules,'AB')
    byname={r.name:r for r in rules}
    incidences=[]
    for event, root, rule in executed.contribution_relations():
        resource=RESOURCES[root]
        act=engine.ACTS[root]
        incidences.append({'effect_event':event, 'bearer':root, 'actual_rule':rule,
                           'standing_resource':resource.key, 'intrinsic_act':act.token})
    event_roots={e:sorted(executed.productive_roots(e)) for e in sorted(executed.events)}
    original_requisites={e:['input-'+root for root in roots] for e,roots in event_roots.items()}
    overlap_witnesses=[]
    for e,f in combinations(sorted(original_requisites),2):
        shared=sorted(set(original_requisites[e]) & set(original_requisites[f]))
        if shared: overlap_witnesses.append({'effects':[e,f], 'shared':shared})
    # A contribution-incidence has one original source in this operational
    # interpretation. This does not establish metaphysical CND for another
    # grain of productive contribution.
    nonempty=bool(incidences)
    witnesses=sorted({c['bearer'] for c in incidences if c['effect_event']=='e'})
    complete=sorted(b for b in engine.ROOTS
                    if witnesses and all(c['bearer']==b for c in incidences
                                         if c['effect_event']=='e'))
    first=[]
    for event, roots in event_roots.items():
        if len(roots)<2: continue
        used_rules=[byname[p.rule] for p in executed.proofs[event]]
        earlier_inputs=set().union(*(set(r.event_inputs) for r in used_rules))
        if not any(len(event_roots[k])>1 for k in earlier_inputs): first.append(event)
    participation_implies_complete=all(
        len(roots)==1 for roots in event_roots.values() if roots)
    return {'case':case,'created_bearer_events':sorted(executed.events),
            'issued_bearers':[a.bearer for a in executed.issued],
            'actual_contribution_incidences':incidences,'event_roots':event_roots,
            'original_requisites':original_requisites, 'overlap_witnesses':overlap_witnesses,
            'witness_bearers':witnesses,'complete_same_bearers':complete,
            'all_contributions_have_original_resource':nonempty and all(
                RESOURCES[c['bearer']].actual and
                RESOURCES[c['bearer']].designated_whole_original for c in incidences),
            'atomic_incidence_unique_source':nonempty and all(
                len([b for b in engine.ROOTS if b==c['bearer']])==1 for c in incidences),
            'participation_implies_complete':participation_implies_complete,
            'first_joint_events':sorted(first),
            'standing_resources':[asdict(r) for r in RESOURCES.values()],
            'semantic_limits':[
                'Standing-resource whole originality and exercise-resource linkage are stipulated application inputs.',
                'Issued acts alone do not identify effective productive participation.',
                'Actual proof incidence is at the declared operational signature, not a proof of metaphysical cause attribution.',
                'Contribution incidences need not be additional created bearer-events.',
                'Requisite overlap uses the same actually issued original input token through mediation, not equality of event-specific proof records.',
                'Per-incidence unique sourcing is definitional at this grain, not independent warrant for general CND.',
                'No source-mode perfection, necessity, wisdom or all-world completeness theorem is assumed satisfied.'
            ]}

def candidate_vs_used():
    rules=engine.direct_rules('priority_A')
    actual=engine.run(rules,'AB')
    return {'case':'priority_A','candidate_bearers':sorted(set().union(*(r.present for r in rules))),
            'actual_bearers':sorted(actual.productive_roots('e')),
            'issued_bearers':[a.bearer for a in actual.issued],
            'used_rules':sorted(p.rule for p in actual.proofs['e'])}

if __name__=='__main__':
    print(json.dumps({'source':str(SOURCE), 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'cases':[inspect_case(c) for c in ('coalescence','persistent_created_mechanism','priority_A')],
          'dormant_route':candidate_vs_used()},indent=2))
