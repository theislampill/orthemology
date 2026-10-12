"""Join bounded reading records without upgrading source or proof status."""
from pathlib import Path
import json,hashlib,collections
B=Path(__file__).resolve().parent

def require(c,m):
 if not c: raise RuntimeError(m)
def read(p):return json.loads((B/p).read_text())
def sha(p):return hashlib.sha256((B/p).read_bytes()).hexdigest()
reg={r['id']:r for r in read('pinned-baseline/registry.json')['results']}
inputs=[('early_mathematics/COVERAGE.json','families','audit_depth'),('early_foundations/INDIVIDUAL_COVERAGE.json','families',None),('early_operations/COVERAGE.json','rows','coverage'),('root_types/COVERAGE.json','families','audit_depth')]
early=[]
for path,key,depthkey in inputs:
 for r in read(path)[key]:
  rid=r['id']; rawdepth=r.get(depthkey) if depthkey else 'selected_source_comparison'
  only=rawdepth in ['registry_and_source_identity_only','INDEX_REFERENCE_ONLY']
  early.append({'id':rid,'tranche':6 if rid.startswith('S6F-') else int(rid[1:rid.index('-')]),'group':'sixth_final_navigation' if rid.startswith('S6F-') else 'original_continuation_family','original_title':reg[rid]['title'],'original_claim':reg[rid]['claim'],'original_limit':reg[rid]['limit'],'coverage_record':path,'coverage_sha256':sha(path),'as_recorded_depth':rawdepth,'final_reading_class':'INDEX_OR_REFERENCE_ONLY' if only else 'SCOPED_SOURCE_OR_REVIEW_EXAMINATION','whole_dependency_closure_examined':False,'fresh_kernel_replay':False,'review_deltas':[]})
require(len(early)==68 and len({r['id'] for r in early})==68,'68 unique early rows')
require({r['id'] for r in early}==set(reg),'Exact early registry coverage')
loss='review_early_math/T6_LOSS_SUPPLEMENTAL_COVERAGE.json';delta=read(loss);r=next(r for r in early if r['id']=='T6-LOSS');require(r['final_reading_class']=='INDEX_OR_REFERENCE_ONLY','T6-LOSS prior depth');r['final_reading_class']='SCOPED_SOURCE_OR_REVIEW_EXAMINATION';r['review_deltas'].append({'path':loss,'sha256':sha(loss),'scope':delta['record']['supplemental_audit_depth']})
late=read('later_scopes/RESULT_AUDIT_262.json');require(len(late)==262 and len({r['id'] for r in late})==262,'262 unique later rows')
later=[]
for r in late:
 c=r['audit_classification']; later.append({'id':r['id'],'tranche':r['tranche'],'title':r['title'],'coverage_record':'later_scopes/RESULT_AUDIT_262.json','as_recorded_classification':c,'historical_source_association':bool(r['historical_selected_source_read_ids']),'final_audit_classification':c,'review_deltas':[],'whole_dependency_closure_examined':False,'fresh_kernel_replay':False})
t12='review_later/SUPPLEMENTAL_READ_T12_TOTAL_INTEGER.json';d=read(t12);r=next(r for r in later if r['id']==d['result_id']);require(r['as_recorded_classification']=='indexed_preserved_reference','T12 previousdepth');r['final_audit_classification']=d['supplemental_classification'];r['review_deltas'].append({'path':t12,'sha256':sha(t12),'scope':'Full117-line named protocol only; underlying law and second row source not freshly read.'})
counts=collections.Counter(r['final_reading_class'] for r in early)
require(counts=={'SCOPED_SOURCE_OR_REVIEW_EXAMINATION':48,'INDEX_OR_REFERENCE_ONLY':20},'Early depth arithmetic')
old_assoc=sum(r['historical_source_association'] for r in later); require(old_assoc==77,'77historicalassociation')
classes=collections.Counter(r['final_audit_classification'] for r in later)
# Carry the exact first audit categories; one explicit delta changes only T12.
summary={'early_rows':68,'early_original_families':42,'early_sixth_final_groups':26,'early_scoped_source_or_review_examination':48,'early_index_reference_only':20,'later_rows':262,'later_historical_selected_source_association':77,'later_original_no_association':185,'later_original_no_association_now_bounded_examination_lower_bound':16,'later_original_no_association_remaining_reference_credit':169,'later_final_classes':dict(classes),'total_registered_family_and_result_rows':330,'unique_theorem_count_claim':False,'all_sources_reread_claim':False,'all_possible_cross_contributions_claim':False,'fresh_Lean_replay_claim':False}
by={}
for n in range(1,21):
 es=[r for r in early if r['tranche']==n];ls=[r for r in later if r['tranche']==n]
 by[str(n)]={'early_rows':len(es),'early_scoped_examinations':sum(r['final_reading_class']=='SCOPED_SOURCE_OR_REVIEW_EXAMINATION' for r in es),'early_index_only':sum(r['final_reading_class']=='INDEX_OR_REFERENCE_ONLY' for r in es),'later_rows':len(ls),'later_classes':dict(collections.Counter(r['final_audit_classification'] for r in ls))}
out={'schema':'T20-bounded-historical-coverage-join-v1','baseline_commit':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','scope':'Individual record triage and selected source/review examination; additive review deltas preserve original ledgers. Counts are coverage of overlapping family/result records, not distinct theorems.','summary':summary,'by_tranche':by,'early':early,'later':later,'unchanged_v4_current_research':{'claim_register':'package/CLAIM_REGISTER.json','claim_navigation_records':161,'cross_front_interfaces':'package/CROSS_FRONT_INTERFACES.json','relationships':49,'note':'Separate current research layer; not replaced or exhausted by the 330 historical family/result rows.'},'separate_ancestry':'Four H lineages and criticism/roadmap owners are in the named source reports; they are not invented extra tranche IDs.'}
(B/'FINAL_COVERAGE.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Final bounded coverage register','','All 68 early rows and 262 later rows are explicitly accounted for. These are overlapping family/result records, not 330 independent theorems.','', 'Early: 48 have scoped source/review examination; 20 remain index/reference-only. Later: 77 retain historical selected-source association; among the 185 initially unassociated, 16 now have bounded later/fresh examination evidence and 169 retain reference-only credit in this audit. Empty association does not mean no historical substantive work. No figure measures whole-proof or whole-source reading.','','The unchanged v4 current research layer separately retains 161 claim-navigation records and 49 cross-front relationships. This historical register does not replace or exhaust it.','','## By tranche','','| Tranche | Early rows | Scoped early examination | Index-only early | Later rows |','|---|---:|---:|---:|---:|']
for n,r in by.items():lines.append(f"| {n} | {r['early_rows']} | {r['early_scoped_examinations']} | {r['early_index_only']} | {r['later_rows']} |")
lines+=['','## Early individual records','','| ID | Final reading level | Owner ledger |','|---|---|---|']
for r in early:lines.append(f"| {r['id']} | {r['final_reading_class']} | {r['coverage_record']} |")
lines+=['','The JSON retains every later row and exact classification. The original 262-row ledger retains full statements, assumptions and limits; the two separately attributed review upgrades are T6-LOSS and T12-TOTAL-INTEGER-REPORT. See the seven-part synthesis and reviews for actual cross-contributions.','']
(B/'FINAL_COVERAGE.md').write_text('\n'.join(lines))
print(json.dumps(summary,indent=2))
