"""Reproduce finite evidence. No recovered file is written."""
from dataclasses import asdict,is_dataclass
import json
from pathlib import Path
from production_contract import *


def serial(x):
    if is_dataclass(x):return serial(asdict(x))
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(set,frozenset)):return sorted((serial(v) for v in x),key=repr)
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main():
    modes={}
    ledgers={}
    for mode in ('coalescence','redundant','priority_A'):
        rules=inherited.direct_rules(mode);l=execute_program(rules,'AB');e=l.effects[0]
        law=program_law(rules,e);ledgers[mode]=l
        modes[mode]={'ledger':l,'endpoint_table':law.table,
                     'minimal_certificates':minimal_true_certificates(law),
                     'positive_sources':l.roots(e),'source_only_active_routes':l.source_only_actual_routes(e),
                     'exhaustive_positive_sources':l.exhaustive_positive_sources(e)}
    base=(inherited.rule('A-actual','A'),)
    extra=base+(inherited.rule('AB-new-actual','AB'),)
    bl=execute_program(base,'AB');e=bl.effects[0]
    cert=Certificate('redundant-AB-proof',e,frozenset('AB'))
    enriched=extend_certificates(bl,cert)
    comparison={
        'base':bl,'certificate_enriched':enriched,'productive_enriched':execute_program(extra,'AB'),
        'certificate_sound_and_applicable':certificate_applicable(cert,program_law(base,e),'AB',bl),
        'erasure_commutes':erase_certificates(bl)==erase_certificates(enriched),
        'base_and_productive_same_entire_presence_table':program_law(base,e).table==program_law(extra,e).table,
        'cut_base':execute_program(base,'AB',disabled=('A-actual',)),
        'cut_productive':execute_program(extra,'AB',disabled=('A-actual',))}
    tensors={m:operative_tensor(ledgers[m],2) for m in ('coalescence','redundant')}
    tensor_record={m:{'tensor':t,'contracted':contract_route_axis(t),'co_membership':same_route_comembership(t)} for m,t in tensors.items()}
    reactive_record=[]
    for w in reactive_ledgers():
        reactive_record.append({'context':w['context'],'intentions_all_met':all(w['actual']['intentions'].values()),
                                'own_ends_all_met':all(w['actual']['own_activity_ends'].values()),
                                'forecasts_match':all(f==w['actual'] for f in w['forecasts'].values()),'ledger':w['ledger']})
    rules,one,two=indirect_occurrence_witness();old=inherited.run(rules,'A')
    indirect={'rules':rules,'supplied_histories':{'one_downstream':one,'two_downstream':two},
              'occurrence_counts':[len(one),len(two)],
              'both_project_to_same_full_run':all(project_occurrence_history(rules,'A',h)==old for h in (one,two)),
              'retained_run':inherited.serial_run(old),
              'inherited_per_proof_occurrence_count':len(old.firing_occurrence_history()),
              'fixed_lineage_cut_outputs':[project_occurrence_history(rules,'A',prune_occurrence_history(h,('m-left',))).history() for h in (one,two)],
              'rule_disable_closure_output':inherited.run(rules,'A',disabled=('A-m-left',)).history(),
              'scope':'Explicit richer supplied histories, not alternative executions of inherited deterministic closure. Fixed-lineage pruning does not reschedule.'}
    result={'scope':'Finite declared interfaces; effect/birth and actual-route interpretation are not metaphysical warrants.',
            'direct':modes,'certificate_vs_productive':comparison,'tensor':tensor_record,'reactive':reactive_record,'indirect':indirect}
    out=Path(__file__).resolve().parents[1]/'results/RESULTS.json'
    out.write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(out),'direct_modes':len(modes),'reactive_contexts':len(reactive_record),'indirect_counts':indirect['occurrence_counts']}))

if __name__=='__main__':main()
