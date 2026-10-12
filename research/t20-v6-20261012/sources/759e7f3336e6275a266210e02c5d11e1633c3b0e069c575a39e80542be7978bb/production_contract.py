"""Two-layer actual-route/certificate contract over preserved models.
A route record is not automatically a new created entity. Exact IDs concern
one represented episode; no transworld origin-essentiality verdict is implied.
"""
from dataclasses import dataclass,replace
from pathlib import Path
from itertools import product,combinations
import sys,json,hashlib
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
CHECKPOINT=ROOT/'recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation'
sys.path.insert(0,str(CHECKPOINT/'provision-identity/src'))
import provision_semantics as inherited
sys.path.insert(0,str(CHECKPOINT/'sovereignty-choice-semantics/reactive-context-extension/src'))
import reactive_context as reactive

@dataclass(frozen=True)
class EffectID:
    episode: str
    key: str

@dataclass(frozen=True)
class BirthID:
    effect: EffectID
    ordinal: int=0

@dataclass(frozen=True)
class OperativeRoute:
    route_id: str
    birth: BirthID
    actual_positive_roots: frozenset
    absence_guards: frozenset

@dataclass(frozen=True)
class Certificate:
    proof_id: str
    conclusion: EffectID
    positive_facts: frozenset
    negative_facts: frozenset=frozenset()
    conclusion_state: str="exists-at-t"

@dataclass(frozen=True)
class Ledger:
    effects: tuple
    births: tuple
    operative_routes: tuple
    certificates: tuple=()
    effect_states: tuple=()
    program_id: str|None=None

    def roots(self,e):
        return frozenset().union(*(r.actual_positive_roots for r in self.operative_routes if r.birth.effect==e))
    def guarded_absences(self,e):
        return frozenset().union(*(r.absence_guards for r in self.operative_routes if r.birth.effect==e))
    def exhaustive_positive_sources(self,e):
        s=self.roots(e)
        return s if len(s)==1 else frozenset()
    def source_only_actual_routes(self,e):
        return frozenset(next(iter(r.actual_positive_roots)) for r in self.operative_routes
                         if r.birth.effect==e and len(r.actual_positive_roots)==1)
    def cited_sources(self,e):
        # Deliberately proof-sensitive comparator, not actual productive support.
        return frozenset().union(*(c.positive_facts for c in self.certificates if c.conclusion==e))
    def unique_birth_per_effect(self):
        return all(sum(b.effect==e for b in self.births)==1 for e in self.effects)


def program_identity(rules,disabled=()):
    data=[(r.name,sorted(r.present),sorted(r.absent),sorted(r.event_inputs),r.output.key,r.output.state) for r in rules]
    return hashlib.sha256(json.dumps([data,sorted(disabled)],sort_keys=True).encode()).hexdigest()


def adapt_run(run,rules,episode='actual-episode',disabled=()):
    # Do not invent route-occurrence lineage from inherited flattened proofs.
    if any(r.event_inputs for r in rules):
        raise NotImplementedError('Created-input lineage is not retained by this direct-route adapter.')
    if len({r.name for r in rules})!=len(rules):
        raise ValueError('Distinct primitive route records need distinct registered IDs.')
    ids={key:EffectID(episode,key) for key in run.events}
    births={key:BirthID(e) for key,e in ids.items()}
    routes=tuple(OperativeRoute(p.rule,births[key],p.roots,p.absent_guards)
                 for key,ps in sorted(run.proofs.items()) for p in sorted(ps,key=lambda p:p.rule))
    states=tuple((ids[k],v.state) for k,v in sorted(run.events.items()))
    return Ledger(tuple(ids.values()),tuple(births.values()),routes,effect_states=states,program_id=program_identity(rules,disabled))


def execute_program(rules,active,disabled=(),episode='actual-episode'):
    return adapt_run(inherited.run(rules,active,disabled),rules,episode,disabled)


@dataclass(frozen=True)
class FiniteLaw:
    effect: EffectID
    state: str
    table: tuple
    program_id: str|None=None

    def value(self,a,b):return dict(self.table)[(bool(a),bool(b))]


def program_law(rules,effect,state='exists-at-t',disabled=()):
    table=[]
    for a,b in product((False,True),repeat=2):
        active=[g for g,v in [('A',a),('B',b)] if v]
        run=inherited.run(rules,active,disabled)
        val=effect.key in run.events and run.events[effect.key].state==state
        table.append(((a,b),val))
    return FiniteLaw(effect,state,tuple(table),program_identity(rules,disabled))


def abstract_law(effect,fn,state='exists-at-t'):
    return FiniteLaw(effect,state,tuple(((a,b),bool(fn(a,b))) for a,b in product((False,True),repeat=2)))


def extend_certificates(ledger,*certs):return replace(ledger,certificates=ledger.certificates+tuple(certs))

def certificate_valid(cert,law):
    # Sound, nonvacuous, effect/state-bound implication; not actual causation.
    if not isinstance(law,FiniteLaw):raise TypeError('An effect-indexed finite law is required.')
    if cert.conclusion!=law.effect or cert.conclusion_state!=law.state:return False
    if cert.positive_facts & cert.negative_facts:return False
    if not (cert.positive_facts|cert.negative_facts)<=frozenset('AB'):return False
    matches=[]
    for (a,b),value in law.table:
        facts={'A':a,'B':b}
        if all(facts[x] for x in cert.positive_facts) and all(not facts[x] for x in cert.negative_facts):matches.append(value)
    return bool(matches) and all(matches)


def certificate_applicable(cert,law,active,ledger):
    active=frozenset(active)
    return law.program_id is not None and law.program_id==ledger.program_id and certificate_valid(cert,law) and cert.positive_facts<=active and not(cert.negative_facts&active) and (cert.conclusion,cert.conclusion_state) in ledger.effect_states


def minimal_true_certificates(law,actual=(True,True)):
    literals=[(g,v) for g,v in zip(('A','B'),actual)]
    valid=[]
    e=law.effect
    for size in range(3):
        for chosen in combinations(literals,size):
            c=Certificate(str(chosen),e,frozenset(g for g,v in chosen if v),frozenset(g for g,v in chosen if not v),law.state)
            if certificate_valid(c,law) and not any(s<=set(chosen) for s in valid):valid.append(set(chosen))
    return tuple(frozenset(x) for x in valid)


def reactive_ledgers():
    c=reactive.Catalogue(('e0','e1'));model=reactive.epistemic_model(c);out=[]
    for w in model['worlds']:
        a=w['actual'];ids={e:EffectID(f'ordinary-{w["context"]}',e) for e in sorted(a['events'])}
        births={e:BirthID(t) for e,t in ids.items()}
        routes=tuple(OperativeRoute(f'actual-direct-{e}',births[e],frozenset(a['supports'][e]),frozenset()) for e in ids)
        ledger=Ledger(tuple(ids.values()),tuple(births.values()),routes,effect_states=tuple((e,'exists-at-t') for e in ids.values()))
        out.append({'context':w['context'],'ledger':ledger,'actual':a,'forecasts':w['forecasts'],
                    'originals':w['originals'],'efficient_edges':w['efficient_edges'],'model_inherence':model['inherence'],'accessible':w['accessible'],'model_scope':model['scope']})
    return out


def operative_tensor(ledger,slots=None):
    # T[r,g,e]: primitive direct-route / original-root / created-effect incidence.
    # Numerical entries describe recorded incidence, not produced matter.
    roots=('A','B');effects=ledger.effects
    n=len(ledger.operative_routes);slots=n if slots is None else slots
    if slots<n:raise ValueError('Cannot erase an operative route by insufficient padding.')
    values=[]
    for i in range(slots):
        route=ledger.operative_routes[i] if i<n else None
        values.append(tuple(tuple(int(route is not None and route.birth.effect==e and g in route.actual_positive_roots) for e in effects) for g in roots))
    return tuple(values)


def contract_route_axis(tensor):
    if not tensor:return ()
    return tuple(tuple(sum(row[g][e] for row in tensor) for e in range(len(tensor[0][g]))) for g in range(2))


def same_route_comembership(tensor,e=0):
    return sum(row[0][e]*row[1][e] for row in tensor)


def erase_certificates(ledger):
    return ledger.effects,ledger.effect_states,ledger.births,ledger.operative_routes,ledger.program_id

@dataclass(frozen=True)
class Occurrence:
    """A supplied operative occurrence, not a proof discovered by closure.

    input_occurrences records one earlier provenance witness per input event.
    This is an explicit refinement contract. The inherited Rule does not choose
    this lineage or how often an enabled rule operates.
    """
    occurrence_id: str
    rule_id: str
    input_occurrences: tuple=()


def project_occurrence_history(rules,active,occurrences):
    """Validate a finite supplied acyclic schedule and erase its occurrence IDs.

    Equality to inherited.run is a separately tested saturation property; mere
    schedule validation does not assert that every enabled route was executed.
    """
    active=frozenset(active);registry={r.name:r for r in rules}
    if len(registry)!=len(rules):raise ValueError('Rule IDs must be distinct.')
    prior={};events={};proofs={}
    for occurrence in occurrences:
        if occurrence.occurrence_id in prior:raise ValueError('Occurrence IDs must be distinct.')
        if occurrence.rule_id not in registry:raise ValueError('Unregistered rule.')
        rule=registry[occurrence.rule_id]
        if not rule.present<=active or rule.absent&active:raise ValueError('Occurrence has false root conditions.')
        selected=[];keys=[]
        for oid in occurrence.input_occurrences:
            if oid not in prior:raise ValueError('Input occurrence must be earlier in this history.')
            upstream_event,upstream_proof=prior[oid]
            keys.append(upstream_event.key);selected.append(upstream_proof)
        if len(keys)!=len(set(keys)) or frozenset(keys)!=rule.event_inputs:
            raise ValueError('Supply one earlier provenance witness per required input event.')
        roots=rule.present|frozenset().union(*(p.roots for p in selected))
        guards=rule.absent|frozenset().union(*(p.absent_guards for p in selected))
        proof=inherited.Proof(rule.name,roots,guards)
        if rule.output.key in events and events[rule.output.key]!=rule.output:
            raise ValueError('Conflicting same-event states.')
        events[rule.output.key]=rule.output;proofs.setdefault(rule.output.key,set()).add(proof)
        prior[occurrence.occurrence_id]=(rule.output,proof)
    return inherited.Run(events,proofs,tuple(inherited.ACTS[g] for g in sorted(active)))


def prune_occurrence_history(occurrences,removed):
    """Hereditary deletion of fixed supplied lineage, without rescheduling."""
    removed=set(removed);kept=[]
    for o in occurrences:
        if o.occurrence_id in removed or any(i in removed for i in o.input_occurrences):
            removed.add(o.occurrence_id)
        else:kept.append(o)
    return tuple(kept)


def indirect_occurrence_witness():
    rules=(inherited.rule('A-m-left','A',output=inherited.M),
           inherited.rule('A-m-right','A',output=inherited.M),
           inherited.rule('m-e',(),inputs=('m',)))
    left=Occurrence('m-left','A-m-left');right=Occurrence('m-right','A-m-right')
    eleft=Occurrence('e-left','m-e',('m-left',))
    eright=Occurrence('e-right','m-e',('m-right',))
    return rules,(left,right,eleft),(left,right,eleft,eright)
