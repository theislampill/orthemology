from pathlib import Path
import importlib.util,json,hashlib,datetime
base=Path('t20-v6-20261011/operational_successors/global_auxiliary_roles/protocol_closure/exact_source')
p=base/'false-closure-selective-prediction-v2/analysis/analyze_fcsp2.py';s=importlib.util.spec_from_file_location('fcsp',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rules={'parameters':{'harm_margin_result_accuracy':.1,'alpha':.05,'harm_margin_structure_overhead':2,'max_failed_run_rate':.1,'minimum_important_effect_false_closure':.1,'minimum_important_effect_aurc':.1}}
def report(p,fc=-.2):return {'endpoints':{'false_closure_contrast':{'treatment_minus_baseline':fc,'holm_p':p},'aurc_contrast':{'treatment_minus_baseline':-.2,'holm_p':p},'result_accuracy_contrast':{'treatment_minus_baseline':0,'perm_p':1},'structure_overhead_ratio_on_controls':1},'failed_run_rate':{'baseline':0,'treatment':0}}
actual=m.perm_p_mean([1]*40);assert actual==0
results={str((x,h)):m.decide(report(x,h),rules) for x in [0,.0001] for h in [-.2,.2]}
assert results[str((0,-.2))].startswith('does not yet')
assert results[str((.0001,-.2))]=='supports incremental value'
assert results[str((0,.2))].startswith('does not yet')
assert results[str((.0001,.2))].startswith('evidence of harm')
e=base/'episode-reification-v2/analysis/analyze_er2.py';sp=importlib.util.spec_from_file_location('er',e);er=importlib.util.module_from_spec(sp);sp.loader.exec_module(er)
keys=[{'case':str(i),'archetype':'A'+str(i//4+1)} for i in range(20)]
cases={str(i):{'false_positive_on_legit':float(i==0)} for i in range(20)}
a,pooled=er.arch_pooled(cases,keys,'false_positive_on_legit');assert a['A1']==.25 and pooled==.05
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Independent exact-source finite function controls, not an empirical run or full CLI validation','sources':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,e]},'permutation_value':actual,'decisions':results,'archetype_rates':a,'pooled_rate':pooled,'checked_conditions':7,'assert_statements':6,'status':'PASS'}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
