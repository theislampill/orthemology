#!/usr/bin/env python3
"""Explicit bounded interpretation/search. No external dependencies or predicate labels."""
from itertools import product
from dataclasses import dataclass
from pathlib import Path
import json, hashlib, datetime

OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(exist_ok=True)

@dataclass(frozen=True)
class Vec:
    left: int
    right: int
    def __add__(self, other): return Vec(self.left + other.left, self.right + other.right)
    def as_list(self): return [self.left, self.right]

ZERO = Vec(0, 0)
TARGET = Vec(2, 2)  # source-neutral; one rigid token e with this exact state
COMMANDS = tuple(Vec(*v) for v in product(range(3), repeat=2))

# Root capacities are actual executable sets, invariant across peer interventions.
# The two agents have the SAME full set; the command, not capacity, is partial.
CAPACITIES = {'A': COMMANDS, 'B': COMMANDS}
@dataclass(frozen=True)
class Will:
    target: Vec
    command: Vec
    def issue(self, capacity):
        if self.command not in capacity: raise ValueError('Command exceeds intrinsic capacity')
        return self.command

ACTUAL_WILLS = {'A': Will(TARGET, Vec(1, 1)), 'B': Will(TARGET, Vec(1, 1))}

def additive_search():
    rows=[]
    for a,b in product(COMMANDS, repeat=2):
        out=a+b
        if out != TARGET: continue
        indispensable_a = b != TARGET
        indispensable_b = a != TARGET
        solo_a = a == TARGET
        solo_b = b == TARGET
        rows.append({'a':a.as_list(),'b':b.as_list(),'output':out.as_list(),
                     'both_indispensable':indispensable_a and indispensable_b,
                     'fixed_solo_a':solo_a,'fixed_solo_b':solo_b})
    assert len(rows)==9
    assert not any(r['both_indispensable'] and r['fixed_solo_a'] for r in rows)
    assert not any(r['fixed_solo_a'] and r['fixed_solo_b'] for r in rows)
    # Constructive eligible-target solo witness, with peer's bearer still present and idle.
    standing=[]
    for q in COMMANDS:
        for agent in ('A','B'):
            cmd=Will(q,q).issue(CAPACITIES[agent])
            assert cmd + ZERO == q
            standing.append({'agent':agent,'target':q.as_list(),'command':cmd.as_list()})
    a=ACTUAL_WILLS['A'].issue(CAPACITIES['A']); b=ACTUAL_WILLS['B'].issue(CAPACITIES['B'])
    assert a+b == TARGET and a != TARGET and b != TARGET
    # Hold entire remaining Will and capacity objects fixed. Delete only peer output.
    return {'commands_per_agent':9,'joint_command_profiles':81,'fixed_target_profiles':rows,
      'both_indispensable_count':sum(r['both_indispensable'] for r in rows),
      'both_fixed_solo_count':sum(r['fixed_solo_a'] and r['fixed_solo_b'] for r in rows),
      'standing_solo_witnesses':standing,
      'actual':{'target_token':'e','target_state':TARGET.as_list(),'A_command':a.as_list(),
               'B_command':b.as_list(),'joint_output':(a+b).as_list(),
               'delete_B_output':a.as_list(),'delete_A_output':b.as_list()},
      'B5':{'capacity_union_size':len(set(CAPACITIES['A'])|set(CAPACITIES['B'])),
            'each_already_contains_union':all(set(COMMANDS)<=set(CAPACITIES[g]) for g in ('A','B')),
            'missing_union_operations':{g:[c.as_list() for c in COMMANDS if c not in CAPACITIES[g]] for g in ('A','B')},
            'external_capacity_completion_events':[],
            'finite_bound_concentration_warning': 'The union of bounded command sets is not the combined additive resource. Two commands [2,2] jointly yield [4,4], outside this finite command set.',
            'unbounded_concentration_construction': 'For either same rigid g, issue(g,a+b)=a+b. Lean proves this for all natural-number vectors, not only the search bound.'},
      'limitation':'Complete global intention is explicit, but fixed actual command is not a complete independent determinant of e. Standing construction with an idle peer does not establish power over every conflicting peer command.'}


def table_search():
    tables=[]
    for values in product((0,1), repeat=4):
        def f(a,b): return values[2*a+b]
        monotone=all(f(a,b)<=f(c,d) for a,b,c,d in product((0,1),repeat=4) if a<=c and b<=d)
        relevanceA=any(f(0,b)!=f(1,b) for b in (0,1))
        relevanceB=any(f(a,0)!=f(a,1) for a in (0,1))
        fixed_solo=f(1,0)==1 and f(0,1)==1
        indispensability=f(1,1)==1 and f(1,0)==0 and f(0,1)==0
        controlA=all(any(all(f(a,b)==q for b in (0,1)) for a in (0,1)) for q in (0,1))
        controlB=all(any(all(f(a,b)==q for a in (0,1)) for b in (0,1)) for q in (0,1))
        tables.append({'table_00_01_10_11':list(values),'monotone':monotone,
          'no_spontaneous':f(0,0)==0,'actual_occurs':f(1,1)==1,
          'each_causally_relevant_somewhere':relevanceA and relevanceB,
          'both_fixed_solo':fixed_solo,'both_actual_indispensable':indispensability,
          'A_controls_both_targets':controlA,'B_controls_both_targets':controlB})
    assert len(tables)==16
    assert not any(t['both_actual_indispensable'] and t['both_fixed_solo'] for t in tables)
    assert not any(t['A_controls_both_targets'] and t['B_controls_both_targets'] for t in tables)
    productive=[t for t in tables if t['monotone'] and t['no_spontaneous'] and t['actual_occurs']]
    assert len(productive)==4
    relevant=[t for t in productive if t['each_causally_relevant_somewhere']]
    assert [t['table_00_01_10_11'] for t in relevant]==[[0,0,0,1],[0,1,1,1]]
    return {'tables_tested':16,'tables':tables,
      'monotone_no_spontaneous_actual_production_tables':len(productive),
      'both_relevant_productive_tables':len(relevant),
      'indispensable_and_fixed_solo_count':0,'both_rectangular_full_control_count':0}


BOOLVECS = tuple(Vec(*v) for v in product((0,1),repeat=2))
def sat(a,b): return Vec(max(a.left,b.left), max(a.right,b.right))

def saturated_candidate():
    # Each root emits one primitive token per coordinate. IDs distinguish emissions,
    # not effect e. Arbitrary ownership relations are allowed by cnd below.
    actual=Vec(1,1)
    owners={("A",0),("A",1),("B",2),("B",3)}
    emissions={0:('L',1),1:('R',1),2:('L',1),3:('R',1)}
    def cnd(rel): return all(sum((g,c) in rel for g in ('A','B'))<=1 for c in emissions)
    def entire(g,rel): return all((g,c) in rel for c in emissions)
    assert cnd(owners) and not entire('A',owners) and not entire('B',owners)
    assert not cnd(owners | {('B',0)})  # CND was not built into syntax.
    assert sat(actual,actual)==actual==sat(actual,ZERO)==sat(ZERO,actual)
    profiles=[]
    for a,b in product(BOOLVECS,repeat=2):
        out=sat(a,b)
        active=[i for i,value in enumerate((a.left,a.right,b.left,b.right)) if value]
        assert all(sum((g,c) in owners for g in ('A','B'))<=1 for c in active)
        profiles.append({'A':a.as_list(),'B':b.as_list(),'output':out.as_list(),
          'A_fixed_solo_same_output':sat(a,ZERO)==out,
          'B_fixed_solo_same_output':sat(ZERO,b)==out,
          'A_indispensable':sat(ZERO,b)!=out,'B_indispensable':sat(a,ZERO)!=out})
    # Concordant wills issue each full target; actual command remains 11 for target11.
    # Both evaluators independently calculate the lexicographic maximizer of a shared
    # abstract score. This is no efficient cross-edge, but shared intrinsic reasons are
    # a stipulated bounded family, not certified divine wisdom.
    reasons=[]
    for preferred in BOOLVECS:
        def intrinsic_score(v): return -(abs(v.left-preferred.left)+abs(v.right-preferred.right))
        a=max(BOOLVECS,key=intrinsic_score); b=max(BOOLVECS,key=intrinsic_score)
        assert a==b==preferred and sat(a,b)==preferred
        reasons.append({'intrinsic_preferred':preferred.as_list(),'A_determination':a.as_list(),
                        'B_determination':b.as_list(),'fixed_peer_deletion_preserves_target':sat(a,ZERO)==preferred})
    # All bounded targets remain eligible and executable. No Eligible=false escape.
    robust={g:[] for g in ('A','B')}
    for q in BOOLVECS:
        for g in ('A','B'):
            controls=any(all((sat(a,b) if g=='A' else sat(b,a))==q for b in BOOLVECS) for a in BOOLVECS)
            if controls: robust[g].append(q.as_list())
    assert robust=={'A':[[1,1]],'B':[[1,1]]}
    return {'target_token':'e','actual_target':[1,1],'capacity_commands':[v.as_list() for v in BOOLVECS],
      'actual_commands':{'A':[1,1],'B':[1,1]},'emission_payloads':emissions,
      'arbitrary_relation_ownership_fixture':sorted([list(v) for v in owners]),
      'all_16_profiles':profiles,'concordant_intrinsic_reason_profiles':reasons,
      'robust_targets_over_all_rival_commands':robust,
      'outcome_to_entire_provenance_counterexample_at_emission_signature':True,
      'both_actual_contributions_indispensable':False,
      'whole_target_attribution_probes': {
        'sufficient_alone_counts_as_entire_original_provision': {'A': True, 'B': True, 'whole_target_CND': False},
        'own_every_actual_emission_counts_as_entire_original_provision': {'A': entire('A',owners), 'B': entire('B',owners), 'whole_target_CND': True, 'whole_target_CND_is_vacuous': True},
        'inference_between_these_attribution_rules': 'NOT_ESTABLISHED'},
      'full_process_state_actual': {'A_emission':[1,1], 'B_emission':[1,1], 'output':[1,1]},
      'full_process_state_delete_B': {'A_emission':[1,1], 'B_emission':[0,0], 'output':[1,1]},
      'CND_duplicate_owner_negative_control':'REJECTED',
      'precise_limits':['Numeric e identity is rigid by interpretation; circuit evaluation does not prove that the exact metaphysical effect keeps identity when its full causal process changes.',
                       'The process has differentiated emitted inputs, but neither is indispensable to the saturated output. No claim of source-faithful original same-respect contribution follows.',
                       'Concordant reason profiles are stipulated as matching intrinsic contents. The score gives an executable choice rule but no independently warranted explanation of why two ultimate agents necessarily share those contents.',
                       'Both agents can execute every command; each fails robust sovereignty for three of four targets when arbitrary opposed rival commands are admitted.']}


def ownership_relation_search():
    entries=tuple(product(('A','B'),range(4)))
    valid=covered=duplicate=0
    for bits in product((0,1),repeat=len(entries)):
        rel={entry for entry,flag in zip(entries,bits) if flag}
        nondup=all(sum((g,c) in rel for g in ('A','B'))<=1 for c in range(4))
        exhaustive=all(any((g,c) in rel for g in ('A','B')) for c in range(4))
        valid += nondup
        covered += nondup and exhaustive
        duplicate += not nondup
    assert (valid,covered,duplicate)==(81,16,175)
    return {'relations_tested':256,'CND_satisfying':valid,'CND_and_every_token_owned':covered,
            'duplicate_owner_relations_rejected':duplicate,'tokens':'x0..x3; fixed original-emission respect'}


def graph_checks():
    # Equations are deliberately acyclic and preserve source roots in interventions.
    nodes={}; edges=[]
    for g in ('A','B'):
        for name in ('bearer','capacity','reason','will','act','emission'):
            nodes[g+'.'+name]=name
        edges += [(g+'.bearer',g+'.capacity'),(g+'.bearer',g+'.reason'),
                  (g+'.reason',g+'.will'),(g+'.capacity',g+'.act'),
                  (g+'.will',g+'.act'),(g+'.act',g+'.emission'),(g+'.emission','effect')]
    nodes['effect']='created_effect'
    # 'bearer -> capacity' is constitutive expression, not efficient origination.
    efficient=[e for e in edges if not e[1].endswith(('.capacity','.reason'))]
    adjacency={n:[] for n in nodes}
    for a,b in efficient: adjacency[a].append(b)
    def paths(n,seen):
        assert n not in seen, ('efficient_priority_cycle',n)
        for v in adjacency[n]: paths(v,seen|{n})
    for n in nodes: paths(n,set())
    for g in ('A','B'):
        other='B' if g=='A' else 'A'
        def reaches(n,t,seen=None):
            seen=set() if seen is None else seen
            if n==t: return True
            if n in seen:return False
            return any(reaches(v,t,seen|{n}) for v in adjacency[n])
        assert not any(reaches(other+'.'+p,g+'.'+q) for p in ('will','act','emission') for q in ('capacity','reason','will','act'))
    return {'nodes':nodes,'constitutive_edges':[list(e) for e in edges if e not in efficient],
            'efficient_edges':[list(e) for e in efficient],
            'cycle_check':'ACYCLIC','peer_to_intrinsic_capacity_reason_will_act_paths':[],
            'scope':'Typed structural equations; no external origin of the roots. This is a finite interpretation of unreceived agency, not a proof that these roots exist metaphysically.'}


def negative_controls():
    # Each malformed rival destroys a different retained condition.
    return [
      {'id':'NC_CHANGED_COMMAND','intervention':'A 11 becomes 22 after B is deleted',
       'target_attained':Vec(2,2)+ZERO==TARGET,'fixed_actual_state_preserved':False},
      {'id':'NC_SOURCE_INDEXED_TARGET','intervention':'replace e with e_A and e_B',
       'same_numerical_target_preserved':False},
      {'id':'NC_UNEQUAL_PARTIAL_CAPACITY','A_commands':[[0,0],[1,0]],'B_commands':[[0,0],[0,1]],
       'equal_eligible_target_power':False},
      {'id':'NC_VACUOUS_ELIGIBILITY','eligible_targets':[], 'nonempty_eligible_target_domain':False},
      {'id':'NC_DUPLICATE_ORIGINAL_OWNER','effect_contribution':0,'owners':['A','B'],'CND':False},
      {'id':'NC_BORROWED_CAPACITY','added_edge':['B.emission','A.capacity'],'intrinsic_nonreceipt':False},
      {'id':'NC_CIRCULAR_WILL','added_edges':[['A.will','B.will'],['B.will','A.will']],'acyclic_efficient_priority':False},
      {'id':'NC_UNWARRANTED_CONCORD','excluded_profiles':'all opposite commands',
       'rectangular_independent_control_proved':False,'philosophical_concord_warrant_supplied':False}]

if __name__=='__main__':
    result={'schema':'fixed-target-cooperation-v1','run_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'additive':additive_search(),'all_boolean_maps':table_search(),'saturation':saturated_candidate(),
      'intrinsic_graph':graph_checks(),'ownership_relations':ownership_relation_search(),'negative_controls':negative_controls(),
      'full_philosophical_countermodel':'NOT_ESTABLISHED',
      'classification':'RESEARCH: fresh bounded model construction and exhaustive search; not replay of prior model tables.'}
    (OUT/'SEARCH_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','additive_profiles':81,'boolean_tables':16,'saturation_profiles':16,
      'full_countermodel':'NOT_ESTABLISHED','output':'results/SEARCH_RESULT.json'},indent=2))
