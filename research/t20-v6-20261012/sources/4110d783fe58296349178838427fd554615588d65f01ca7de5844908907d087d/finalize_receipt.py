from pathlib import Path
import hashlib,json,datetime,re
out=Path(__file__).resolve().parent; root=out.parent; expected='e253a2b1a537826094db7ede00768b561360ce25e3a6907354592a320a2de278'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(root/'REVIEW_SNAPSHOT_V2.json')==expected
files=json.loads((root/'REVIEW_SNAPSHOT_V2.json').read_text())['files']; checks=[]
for f in files:
 p=root/f['path']; assert digest(p)==f['sha256'] and p.stat().st_size==f['size'],f['path']
 checks.append({'path':f['path'],'size':p.stat().st_size,'sha256':digest(p),'pass':True})
assert len(files)==34
freeze=root/'frozen-candidate-v1'; assert digest(freeze/'REVIEW_SNAPSHOT_V1.json')=='9b2bafffd7b45f84db7ce6ca8f8e86e6027f8dd573f6e302d392fb5615d48c94'
for f in json.loads((freeze/'REVIEW_SNAPSHOT_V1.json').read_text())['files']:
 p=freeze/f['path']; assert digest(p)==f['sha256'] and p.stat().st_size==f['size']
prior=root/'independent-review-v1'; assert digest(prior/'RECEIPT.json')=='5683d622626ab11919a84bc832298568dee17edc428c95e82988906cee124bea'
for f in json.loads((prior/'RECEIPT.json').read_text())['artifacts']:
 p=prior/f['path']; assert digest(p)==f['sha256'] and p.stat().st_size==f['size']
for name in ['HistoryModel','HistoryInvariant','HistorySafety','HistoryTrace','NegativeControls','Targets','MultiEpoch']:
 assert not re.search(r'sorryAx|warning:|error:',(out/'replay/logs'/f'{name}.log').read_text())
for name in ['review-challenges.log','reservation-domain.log']:
 assert not re.search(r'sorryAx|warning:|error:',(out/name).read_text())
assert 'PASS: all five modules plus two target fixtures compiled; seven false-claim controls rejected; seven accepted-source scenarios passed; candidate and frozen inputs unchanged.' in (out/'verify-console.log').read_text()
assert (out/'replay/logs/candidate-before.json').read_bytes()==(out/'replay/logs/candidate-after.json').read_bytes()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'snapshot-after.json').write_text(json.dumps({'manifest_sha256':expected,'checked_utc':now,'count':34,'pass':True,'frozen_v1_and_review_unchanged':True,'checks':checks},indent=2)+'\n')
artifacts=[{'path':str(p.relative_to(out)),'size':p.stat().st_size,'sha256':digest(p)} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='RECEIPT.json']
r={
 'schema':'independent-interlock-history-review-receipt-v2','completed_utc':now,'disposition':'PASS',
 'review_type':'narrow independent delta review with full fresh replay and retained digest-bound V1 substantive assessment',
 'candidate_root':'tranche7-restart/formal/interlock-history-kernel',
 'candidate_snapshot':{'path':'REVIEW_SNAPSHOT_V2.json','sha256':expected,'file_count':34},
 'predecessor':{'manifest_sha256':'9b2bafffd7b45f84db7ce6ca8f8e86e6027f8dd573f6e302d392fb5615d48c94','frozen_files_verified':33,'review_sha256':digest(prior/'REVIEW.md'),'receipt_sha256':digest(prior/'RECEIPT.json'),'bound_artifacts_verified_unchanged':44},
 'input_hashes_stable_before_and_after':True,'canonical_mutations':False,'writes_restricted_to':'independent-review-v2',
 'source_delta':{'lean_file':'HistoryTrace.lean','exact_two_line_change_verified':True,'changes':['ValidPath c k added as Reservation antecedent','admitted.1 passed to Reservation in admitted_externally_authorized'],'central_model_and_proofs_unchanged':True,'reservation_domain_issue':'RESOLVED'},
 'verification':{
  'command_from_workspace':'./tranche7-restart/formal/interlock-history-kernel/verify.sh ./tranche7-restart/formal/interlock-history-kernel/independent-review-v2/replay',
  'exit_code':0,'compiled_modules':5,'candidate_fixtures':2,'false_claim_rejections':7,'accepted_source_scenarios':7,'frozen_source_review_bindings':11,
  'review_challenges_exit_code':0,'reservation_domain_checks_exit_code':0,
  'lean_version':'4.19.0','lean_commit':'6caaee842e94','lean_sha256':'92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
  'mathlib_commit':'c44e0c8ee63ca166450922a373c7409c5d26b00b','mathlib_archive_sha256':'9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425','source_files_compared':6816,'source_mismatches':0,'supplied_compiled_cache_consumed_read_only':True,'dependencies_changed_or_rebuilt':False,
  'reported_axioms':['propext','Classical.choice','Quot.sound']},
 'claim_ceiling':{
  'interface':'original accepted dynamic V2 finite-root/whole-binary-table interface only',
  'positive':['arbitrary finite-history internal safety and current/exact admitted writes','durable exclusion of the same cancelled full command after arbitrary finite continuation','whole-table restoration on admitted repair','stable-effective-epoch whole-table persistence'],
  'external_authorization':'conditional on explicit Reservation restricted to ValidPath commands',
  'required_premises':['authentic authoritative serial source','continuing lifetime-union fault superset/budget','coherent durable root-wide veto across all owned gate copies','same-command non-bypassable atomic physical mediation'],
  'progress_premises_separate':['honest actor policy','fresh nonces','all-good path addressability','independently bounded authenticated per-root control service'],
  'not_established':['mechanized Python-to-Lean refinement','real consent','physical or cryptographic realization','instantaneous/mobile-fault tolerance','horizon extension or full infinite liveness','complete liveness/covering/randomized theorem','automatic transport to typed compiled composition or unknown-label interface','R5 defeat']},
 'material_issues':[],'open_corrections':[],
 'artifacts':artifacts}
(out/'RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'disposition':r['disposition'],'candidate_sha256':expected,'unchanged_files':34,'artifacts_bound':len(artifacts),'review_sha256':digest(out/'REVIEW.md'),'receipt_sha256':digest(out/'RECEIPT.json')},indent=2))
