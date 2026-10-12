"""Offline integrity/locator checks for an additive historical supplement, not proof review."""
from pathlib import Path,PurePosixPath
import json,hashlib,re,sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'historical_coverage'
def require(value,message):
 if not value:raise RuntimeError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def path(rel):
 require(isinstance(rel,str) and rel and '\\' not in rel and not rel.startswith('/') and ':' not in rel,'unsafe locator')
 require(all(p not in ('','.','..') for p in rel.split('/')),'unsafe relative locator '+rel)
 p=ROOT/rel
 require(not any(x.is_symlink() for x in [p,*p.parents] if x!=ROOT.parent),'symlink locator '+rel)
 return p
def load(rel):return json.loads(path(rel).read_text())
def main():
 for rel in ['FINAL_COVERAGE.json','FINAL_COVERAGE.md','OWNER_REVIEW_CASE.md','HISTORICAL_CROSS_FRONT_SYNTHESIS.md','REVIEW_DISPOSITIONS.json','SUPPLEMENT_INTERFACES.json','review_early_math/REPORT.md','review_early_math/FOLLOWUP_QUALIFICATION.json','review_foundations_operations/REVIEW.md','review_foundations_operations/SYNTHESIS_FOLLOWUP.json','review_later/REVIEW.md','review_later/INPUT_BINDINGS.json']:
  require(path('historical_coverage/'+rel).is_file(),'missing required final coverage/review member '+rel)
 prior=load('historical_coverage/V4_PRESERVATION.json')
 for row in prior['files']:
  p=path(row['path']);require(p.is_file(),'missing v4 member '+row['path']);require(digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],'changed v4 member '+row['path'])
 resolver=load('historical_coverage/SOURCE_PATH_RESOLVER.json');aliases={}
 for row in resolver['routes']:
  p=path(row['included_path']);require(p.is_file(),'missing source '+row['included_path']);require(digest(p)==row['sha256'],'source digest mismatch '+row['included_path'])
  if 'bytes' in row:require(p.stat().st_size==row['bytes'],'source size mismatch')
  alias=row['workspace_alias'];path(alias)
  if alias in aliases:require(aliases[alias]==row['sha256'],'conflicting workspace alias '+alias)
  aliases[alias]=row['sha256']
  if row['locator_field']!='source_packet_member':
   source=load(row['binding_document'])
   for key in row['selector']:source=source[key]
   require(source[row['locator_field']]==row['original_locator'],'source locator not present in exact ledger')
   candidates=[source.get(k) for k in ['actual_sha256','public_sha256','sha256','expected_public_sha256','original_sha256']]
   require(row['sha256'] in candidates,'source digest not owned by binding')
   if 'catalogue/objects/' in row['original_locator']:require(row['original_locator'].rsplit('/',1)[1]==row['sha256'],'catalogue source replaced by a derived projection')
 for row in resolver['exceptions']:
  require(row['disposition']=='PINNED_PUBLIC_ONLY_NOT_INCLUDED','unresolved source binding')
  require('/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/' in row['public_url'],'unpinned exception')
 for row in resolver['source_objects']:
  p=path(row['included_path']);require(digest(p)==row['sha256'],'supplementary source drift')
 if (H/'FINAL_COVERAGE.json').exists():
  final=load('historical_coverage/FINAL_COVERAGE.json');summary=final['summary']
  early=[]
  for rel,key in [('early_mathematics/COVERAGE.json','families'),('early_foundations/INDIVIDUAL_COVERAGE.json','families'),('early_operations/COVERAGE.json','rows'),('root_types/COVERAGE.json','families')]:
   rows=load('historical_coverage/'+rel)[key];early.extend(r['id'] for r in rows)
  registered=load('historical_coverage/pinned-baseline/registry.json')['results']
  overlay=load('historical_coverage/pinned-baseline/SIXTH_FINAL_OVERLAY.json')['new_results']
  expected={r['id'] for r in registered}
  require(len(expected)==68,'pinned early registry cardinality')
  require(len(early)==len(set(early))==68 and set(early)==expected,'early row population/overlap')
  require({r['id'] for r in final['early']}==expected and len(final['early'])==68,'final early row join')
  require(sum(r['final_reading_class']=='SCOPED_SOURCE_OR_REVIEW_EXAMINATION' for r in final['early'])==summary['early_scoped_source_or_review_examination'],'early reading count')
  for row in final['early']:
   require(digest(path('historical_coverage/'+row['coverage_record']))==row['coverage_sha256'],'final early ledger binding drift')
  original=load('package/coverage/CUMULATIVE_PROGRAMME_CROSSWALK.json')['inherited_result_bindings'];old={r['id']:r for r in original}
  later=load('historical_coverage/later_scopes/RESULT_AUDIT_262.json')
  require(len(later)==len({r['id'] for r in later})==262 and {r['id'] for r in later}==set(old),'later population')
  require(all(r['original_statement']==old[r['id']]['inherited_statement'] for r in later),'original later statements changed')
  require(len(final['later'])==262 and {r['id'] for r in final['later']}==set(old),'final later population')
  require(dict(Counter(r['final_audit_classification'] for r in final['later']))==summary['later_final_classes'],'later class counts')
  require(all(not r['fresh_kernel_replay'] and not r['whole_dependency_closure_examined'] for r in final['early']+final['later']),'coverage credit broadened')
 if (H/'REVIEW_DISPOSITIONS.json').exists():
  for row in load('historical_coverage/REVIEW_DISPOSITIONS.json')['items']:
   require(digest(path('historical_coverage/'+row['target']))==row['target_sha256'],'review disposition target drift')
   if row.get('receipt'):require(digest(path('historical_coverage/'+row['receipt']))==row['receipt_sha256'],'review disposition receipt drift')
 manifest_path=H/'CANDIDATE_CONTENTS.json'
 if manifest_path.exists():
  manifest=json.loads(manifest_path.read_text());expected={'historical_coverage/CANDIDATE_CONTENTS.json'}|{row['path'] for row in prior['files']}
  for row in manifest['files']:
   p=path(row['path']);require(p.is_file() and digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],'supplement member drift '+row['path']);expected.add(row['path'])
  actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
  require(actual==expected,'unexpected/missing supplement member')
 print(json.dumps({'status':'PASS','v4_files_unchanged':len(prior['files']),'exact_source_routes':len(resolver['routes']),'distinct_workspace_aliases':len(aliases),'pinned_public_only':len(resolver['exceptions']),'scope':'Mechanical integrity and resolver consistency only. Independent review readiness is a separate disposition; no new scientific, kernel or source-reading credit.'}))
if __name__=='__main__':main()
