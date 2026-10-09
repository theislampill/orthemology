"""Research semantics, not an inference engine for metaphysical original provision.

Intrinsic acts, created events, production rules, and proof records are different
sorts. Event identities have no owner component. Rule guards and supports are
retained so that changing an operative production mode cannot be hidden.
"""
from dataclasses import dataclass
from itertools import product, combinations
from pathlib import Path
import json

ROOTS = ('A', 'B')

@dataclass(frozen=True)
class IntrinsicAct:
    bearer: str
    token: str
    intention_annotation: str = 'uninterpreted in the bare rule engine'

ACTS = {g: IntrinsicAct(g, 'act-' + g) for g in ROOTS}

@dataclass(frozen=True)
class Event:
    key: str
    state: str

E = Event('e', 'exists-at-t')
M = Event('m', 'operative-coupler')

@dataclass(frozen=True)
class Rule:
    name: str
    present: frozenset[str]
    absent: frozenset[str]
    event_inputs: frozenset[str]
    output: Event

@dataclass(frozen=True)
class Proof:
    rule: str
    roots: frozenset[str]
    absent_guards: frozenset[str]

@dataclass
class Run:
    events: dict[str, Event]
    proofs: dict[str, set[Proof]]
    issued: tuple[IntrinsicAct, ...]

    def history(self):
        # Complete CREATED history in this deliberately small ontology.
        return tuple(sorted((e.key, e.state) for e in self.events.values()))

    def firing_occurrence_history(self):
        # Rival ontology: each executed production rule makes a distinct
        # occurrence. Never call this the same target as the event-key model.
        return tuple(sorted((key, p.rule, self.events[key].state)
                            for key, ps in self.proofs.items() for p in ps))

    def contribution_relations(self):
        # A contribution TO an event is neither the event-bearer itself nor
        # an intrinsic act. Whether these grounded incidences are created
        # effects-in-the-bearer is precisely an interpretation question.
        return tuple(sorted((key, root, p.rule)
                            for key, ps in self.proofs.items() for p in ps for root in p.roots))

    def causally_enriched_history(self):
        return (self.history(), self.contribution_relations())

    def productive_roots(self, event='e'):
        return frozenset().union(*(p.roots for p in self.proofs.get(event, set())))

    def exhaustive_providers(self, event='e'):
        # Derived from all executed positive derivations, not arbitrary labels.
        roots = self.productive_roots(event)
        return frozenset(g for g in ROOTS if roots == frozenset([g]))

    def derivation_providers(self, event='e'):
        # Each actual derivation suffices on its own; distinct attribution rule.
        return frozenset(g for g in ROOTS if any(p.roots == frozenset([g])
                                               for p in self.proofs.get(event, set())))


def rule(name, present, absent=(), inputs=(), output=E):
    return Rule(name, frozenset(present), frozenset(absent), frozenset(inputs), output)


def direct_rules(policy):
    if policy == 'coalescence':
        return (rule('A-solo', 'A', 'B'), rule('B-solo', 'B', 'A'), rule('AB-joint', 'AB'))
    if policy == 'redundant':
        return (rule('A-direct', 'A'), rule('B-direct', 'B'))
    if policy == 'priority_A':
        return (rule('A-selected', 'A'), rule('B-if-no-A', 'B', 'A'))
    if policy == 'priority_B':
        return (rule('B-selected', 'B'), rule('A-if-no-B', 'A', 'B'))
    raise ValueError(policy)


def created_rules(policy):
    if policy == 'joint_created_mechanism':
        # m is itself jointly produced. No efficient root is smuggled in.
        return (rule('A-solo', 'A', 'B'), rule('B-solo', 'B', 'A'),
                rule('AB-m', 'AB', output=M), rule('m-e', (), inputs=['m']))
    if policy == 'persistent_created_mechanism':
        # Every nonempty profile produces the same m and e. Coalescence has
        # moved to the first node m; it has not been eliminated or explained
        # by a pre-existing independent third original.
        return (rule('A-m-solo', 'A', 'B', output=M),
                rule('B-m-solo', 'B', 'A', output=M),
                rule('AB-m-joint', 'AB', output=M),
                rule('m-e', (), inputs=['m']))
    if policy == 'A_created_mechanism':
        # At actual AB, B produces e through A's m; no intrinsic receipt.
        return (rule('A-m', 'A', output=M), rule('B-through-m', 'B', inputs=['m']))
    raise ValueError(policy)


def run(rules, active, disabled=()):
    active, disabled = frozenset(active), frozenset(disabled)
    events, proofs = {}, {}
    # Least finite closure. Empty-root spontaneous rules are not disallowed by
    # the engine; the no-spontaneous check is a real test of a chosen program.
    while True:
        changed = False
        for r in rules:
            if r.name in disabled or not r.present <= active or r.absent & active:
                continue
            if not r.event_inputs <= events.keys():
                continue
            upstream = [proofs[k] for k in sorted(r.event_inputs)]
            for selected in product(*upstream):
                roots = r.present | frozenset().union(*(p.roots for p in selected))
                guards = r.absent | frozenset().union(*(p.absent_guards for p in selected))
                p = Proof(r.name, roots, guards)
                if r.output.key in events and events[r.output.key] != r.output:
                    raise ValueError('Conflicting same-event states')
                events[r.output.key] = r.output
                proofs.setdefault(r.output.key, set())
                if p not in proofs[r.output.key]:
                    proofs[r.output.key].add(p)
                    changed = True
        if not changed:
            break
    return Run(events, proofs, tuple(ACTS[g] for g in sorted(active)))


PROFILES = (frozenset(), frozenset('A'), frozenset('B'), frozenset('AB'))


def monoids(n):
    # Identity 0 and commutativity fixed. Every assignment to the free cells
    # is tried; associativity tested separately. Not a scan of all causation.
    cells = [(i,j) for i in range(1,n) for j in range(i,n)]
    for entries in product(range(n), repeat=len(cells)):
        op = [[0]*n for _ in range(n)]
        for i in range(n): op[0][i] = op[i][0] = i
        for (i,j), v in zip(cells,entries): op[i][j] = op[j][i] = v
        if all(op[op[a][b]][c] == op[a][op[b][c]] for a,b,c in product(range(n), repeat=3)):
            yield op


def monoid_report(n):
    records=[]
    for op in monoids(n):
        absorption=[(a,b) for a,b in product(range(n), repeat=2) if b != 0 and op[a][b]==a]
        cancellative=all(op[a][b] != op[a][c] or b==c for a,b,c in product(range(n),repeat=3))
        nonzero_idempotents=[a for a in range(1,n) if op[a][a]==a]
        records.append({'operation':op,'absorptions':absorption,'cancellative':cancellative,
                        'nonzero_idempotents':nonzero_idempotents})
    return {'size':n,'candidate_tables':n**(n*(n-1)//2), 'monoids':len(records),
            'absorbing_monoids':sum(bool(r['absorptions']) for r in records),
            'cancellative_monoids':sum(r['cancellative'] for r in records),
            'records':records}


def serial_run(r):
    return {'created_history':r.history(),'firing_occurrence_history':r.firing_occurrence_history(),'contribution_relations':r.contribution_relations(),'issued_intrinsic_acts':[a.__dict__ for a in r.issued],
            'productive_roots':sorted(r.productive_roots()),
            'exhaustive_providers':sorted(r.exhaustive_providers()),
            'derivation_providers':sorted(r.derivation_providers()),
            'proofs':{k:[{'rule':p.rule,'roots':sorted(p.roots),'absent_guards':sorted(p.absent_guards)}
                         for p in sorted(v,key=lambda p:(p.rule,sorted(p.roots)))] for k,v in r.proofs.items()}}


def shared_grounding_dags(internal_count):
    # Two intrinsic root nodes, then topologically indexed created nodes.
    # Every created node has at least one earlier parent. Supports are
    # stipulated to be effective productive prerequisites, not mere arrows.
    parent_options = []
    for node in range(2, internal_count+2):
        parent_options.append([tuple(k for k in range(node) if mask & (1 << k))
                               for mask in range(1,1 << node)])
    total = joint_terminal = primitive_found = 0
    for graph in product(*parent_options):
        total += 1
        supports=[frozenset('A'),frozenset('B')]
        for parents in graph:
            supports.append(frozenset().union(*(supports[p] for p in parents)))
        if supports[-1] != frozenset('AB'): continue
        joint_terminal += 1
        first = next(i for i in range(2,len(supports)) if supports[i] == frozenset('AB'))
        assert all(supports[p] != frozenset('AB') for p in graph[first-2])
        primitive_found += 1
    return {'created_nodes':internal_count,'dag_programs':total,
            'joint_terminal_programs':joint_terminal,
            'first_joint_node_without_prior_joint_mechanism':primitive_found}


@dataclass(frozen=True)
class IntendedAct:
    bearer: str
    token: str
    exact_created_target: frozenset[str]


def execute_intentions(acts):
    # The intentions actually generate the event catalogue and commands.
    # This is a direct joint-event program, not the bare annotation above.
    by_root={a.bearer:a for a in acts}
    if len(by_root) != len(acts): raise ValueError('two active acts from same original')
    a=by_root['A'].exact_created_target if 'A' in by_root else frozenset()
    b=by_root['B'].exact_created_target if 'B' in by_root else frozenset()
    events=tuple(sorted((key,'exists-at-t') for key in a|b))
    supports={key:frozenset(g for g,t in [('A',a),('B',b)] if key in t) for key in a|b}
    rules={key:('AB-joint' if key in a&b else 'A-solo' if key in a else 'B-solo') for key in a|b}
    satisfied={act.bearer: a|b == act.exact_created_target for act in acts}
    return events,supports,rules,satisfied


def catalogue_report(n=4):
    # Direct event-set interpreter, not a physical saturation mechanism.
    keys=tuple('e'+str(i) for i in range(n))
    targets=[frozenset(keys[i] for i in range(n) if mask & (1 << i)) for mask in range(1<<n)]
    failures=[]
    for q in targets:
        def evaluate(a,b):
            events={key:Event(key,'exists-at-t') for key in a|b}
            support={key:frozenset(g for g,s in [('A',a),('B',b)] if key in s) for key in a|b}
            active_rule={key:('AB' if key in a&b else 'A-solo' if key in a else 'B-solo') for key in a|b}
            return events,support,active_rule
        joint,soloA,soloB=evaluate(q,q),evaluate(q,frozenset()),evaluate(frozenset(),q)
        if not (joint[0]==soloA[0]==soloB[0]): failures.append(sorted(q))
        if q:
            assert all(v==frozenset('AB') for v in joint[1].values())
            assert joint[2] != soloA[2]
    return {'event_catalogue_size':n,'all_target_sets_tested':len(targets),
            'full_created_event_set_fixed_solo_failures':failures,
            'operative_rule_switches_for_each_nonempty_target':len(targets)-1,
            'scope':'All subsets of this catalogue; generic Lean theorem covers arbitrary effect-index type and target predicate, not every metaphysical effect kind'}


def intention_report():
    q=frozenset(['e0','e1']); r=frozenset(['e2'])
    a=IntendedAct('A','alpha',q); b=IntendedAct('B','beta',q)
    conflict=IntendedAct('B','beta-prime',r)
    joint=execute_intentions([a,b]); solo=execute_intentions([a]); opposed=execute_intentions([a,conflict])
    return {'joint_exact_intentions_met':joint[3], 'solo_frozen_A_intention_met':solo[3],
            'created_history_unchanged_after_B_suppression':joint[0]==solo[0],
            'operative_rules_unchanged':joint[2]==solo[2],
            'different_target_intentions_met':opposed[3],
            'scope':'Semantic interpretation of command content; does not establish that intrinsic wisdom authorizes only matching intentions, or that causal derivations are complete original agency'}


def primitive_attribution_report():
    # R is deliberately free, not defined as a function, and not inferred
    # from the production DAG. The countercontrol changes only this relation.
    records=[]
    contributors=frozenset('AB')
    for mask in range(4):
        entire=frozenset(ROOTS[i] for i in range(2) if mask & (1<<i))
        cnd=len(entire)<=1
        sole_excludes_peer=all(contributors <= frozenset([g]) for g in entire)
        records.append({'primitive_entire_relation':sorted(entire),
                        'same_actual_production':'AB-joint -> e',
                        'same_created_event_history':[['e','exists-at-t']],
                        'whole_effect_CND':cnd,'whole_effect_coverage':bool(entire),
                        'entire_solo_meaning_excludes_coproducer':sole_excludes_peer})
    return records


def main():
    direct={p:{''.join(sorted(s)) or 'none':serial_run(run(direct_rules(p),s)) for s in PROFILES}
            for p in ('coalescence','redundant','priority_A','priority_B')}
    created={p:{''.join(sorted(s)) or 'none':serial_run(run(created_rules(p),s)) for s in PROFILES}
             for p in ('joint_created_mechanism','persistent_created_mechanism','A_created_mechanism')}
    # Mechanism cuts are NOT the same operation in the different ontologies;
    # compare only as an ontological diagnostic, not an empirically neutral test.
    cuts={p:{r.name:serial_run(run(direct_rules(p),'AB',[r.name])) for r in direct_rules(p)}
          for p in direct}
    output={'scope':'Finite operational/provenance interpretations only; no metaphysical premise validation',
            'direct':direct,'created':created,'rule_cut_diagnostics':cuts,
            'algebra':[monoid_report(n) for n in (2,3,4)],
            'grounding_dags':[shared_grounding_dags(n) for n in range(1,5)],
            'catalogue':catalogue_report(4), 'interpreted_intentions':intention_report(),
            'primitive_attribution':primitive_attribution_report()}
    out=Path(__file__).resolve().parents[1]/'results'/'SEMANTIC_RESULTS.json'
    out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'result':str(out),'algebra':[{k:v for k,v in x.items() if k!='records'} for x in output['algebra']],
                      'direct_actual':{p:direct[p]['AB'] for p in direct}},indent=2))

if __name__=='__main__': main()
