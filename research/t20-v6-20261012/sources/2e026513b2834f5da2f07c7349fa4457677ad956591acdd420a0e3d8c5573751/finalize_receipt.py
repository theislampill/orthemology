"""Bind this independent V1 review to the unchanged candidate and final outputs."""
from pathlib import Path
import hashlib, json, datetime, re
root = Path(__file__).resolve().parent.parent
out = root / 'independent-review-v1'
expected = '9b2bafffd7b45f84db7ce6ca8f8e86e6027f8dd573f6e302d392fb5615d48c94'
manifest = root / 'REVIEW_SNAPSHOT_V1.json'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(manifest) == expected
entries = json.loads(manifest.read_text())['files']
checks = []
for f in entries:
 p = root / f['path']; raw = p.read_bytes()
 checks.append({'path': f['path'], 'size': len(raw), 'sha256': digest(p),
                'pass': len(raw) == f['size'] and digest(p) == f['sha256']})
assert len(checks) == 33 and all(x['pass'] for x in checks)
time = datetime.datetime.now(datetime.timezone.utc).isoformat()
snapshot = {'time_utc': time, 'manifest_sha256': expected, 'count': len(checks),
            'pass': True, 'checks': checks}
(out / 'snapshot-after.json').write_text(json.dumps(snapshot, indent=2)+'\n')
console = (out / 'verify-console.log').read_text()
assert 'PASS: all five modules plus two target fixtures compiled; seven false-claim controls rejected; seven accepted-source scenarios passed; candidate and frozen inputs unchanged.' in console
for f in ['HistoryModel', 'HistoryInvariant', 'HistorySafety', 'HistoryTrace', 'NegativeControls', 'Targets', 'MultiEpoch']:
 assert not re.search(r'sorryAx|warning:|error:', (out / 'replay/logs' / (f+'.log')).read_text())
assert not re.search(r'sorryAx|warning:|error:', (out / 'review-challenges.log').read_text())
assert (out / 'replay/logs/candidate-before.json').read_bytes() == (out / 'replay/logs/candidate-after.json').read_bytes()
assert json.loads((out / 'replay/controls/RESULTS.json').read_text())['status'] == 'PASS'
assert json.loads((out / 'replay/logs/source-replay.json').read_text())['status'] == 'PASS'
artifacts = [{'path': str(p.relative_to(out)), 'size': p.stat().st_size, 'sha256': digest(p)}
             for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'RECEIPT.json']
r = {
 'schema': 'independent-interlock-history-review-receipt-v1',
 'completed_utc': time, 'disposition': 'PASS',
 'review_type': 'new independent cold review; not inherited base acceptance',
 'candidate_root': 'tranche7-restart/formal/interlock-history-kernel',
 'candidate_snapshot': {'path':'REVIEW_SNAPSHOT_V1.json','sha256':expected,'file_count':33},
 'inputs_match_before_and_after': True, 'candidate_or_predecessor_mutation': False,
 'writes_restricted_to': 'independent-review-v1',
 'verification': {
  'command_from_workspace': './tranche7-restart/formal/interlock-history-kernel/verify.sh ./tranche7-restart/formal/interlock-history-kernel/independent-review-v1/replay',
  'exit_code':0, 'compiled_modules':5, 'compiled_candidate_fixtures':2,
  'expected_false_claim_rejections':7, 'accepted_source_scenarios':7,
  'frozen_source_review_files':11, 'reviewer_challenge_compile_exit_code':0,
  'lean_version':'4.19.0', 'lean_commit':'6caaee842e94',
  'lean_sha256':'92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
  'mathlib_commit':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
  'mathlib_archive_sha256':'9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425',
  'mathlib_source_files_compared':6816, 'mathlib_source_mismatches':0,
  'supplied_compiled_cache_used_read_only':True, 'dependencies_changed_or_rebuilt':False,
  'reported_axioms':['propext','Classical.choice','Quot.sound']
 },
 'reviewer_challenges':[
  'Reachable delivery guard implies actual stored predecessor certificate and durable good-root closure',
  'Cancelled command cannot occur as any landing event in arbitrary continuation',
  'Threshold positivity follows from Config, including the zero-budget edge',
  'Pending request can precede lawful old-current landing; early acknowledgement closes without descriptor update',
  'Foreign requester cannot land and foreign cancellation cannot be acknowledged by a good root',
  'B-only cancellation state is reachable but insufficient',
  'Faulty root erasure and late reprepare cannot remove another root tombstone',
  'Good-root same-command reprepare is rejected after closure',
  'Fresh-nonce repair still has an actual trace after previous cancellation',
  'Zero-budget one-root actual repair trace is non-vacuous',
  'Arbitrarily long holds remain possible; safety alone is not progress',
  'External consent cannot be inferred without Reservation'
 ],
 'claim_ceiling': {
  'interface':'original accepted dynamic V2 finite-root, whole binary-table interface',
  'positive':['arbitrary finite-history internal write safety and current exact authorization','durable exclusion of the same cancelled full command for every finite continuation','whole-table restoration on admitted repair','stable-effective-epoch whole-table goal preservation'],
  'required_premises':['authoritative authenticated serial descriptor history','single lifetime-union fault superset and budget across the entire claimed history','coherent root-wide close-before-acknowledge across all owned gate copies','durable root-local memory','same-command non-bypassable atomic physical mediation'],
  'external_authorization':'requires the explicit displayed Reservation premise; V1 quantifies all descriptor-authorized commands, not only valid paths',
  'progress_premises_kept_separate':['honest actor policy','fresh nonces','direct all-good path addressability','independently bounded authenticated per-root control service'],
  'not_established':['mechanized Python-to-Lean refinement','physical or cryptographic realization','actual external consent','unrestricted mobile-fault tolerance','extension of a finite horizon','complete infinite liveness','full covering or randomized search result','automatic transport to typed compiled composition or unknown-label interface','R5 defeat']
 },
 'material_issues':[],
 'non_blocking_notes':[
  {'id':'V1-RESERVATION-DOMAIN','location':'HistoryTrace.lean:131-134','summary':'Reservation is sufficient but stronger than minimally needed: it includes descriptor-authorized commands with invalid path cardinality. Preserve that quantifier when citing the corollary; internal history safety is unaffected.'},
  {'id':'CONTROL-CEILING','summary':'Concrete mutation witnesses and false-claim reductions do not constitute exhaustive mutation testing or physical fault injection.'}
 ],
 'artifacts':artifacts
}
(out / 'RECEIPT.json').write_text(json.dumps(r, indent=2)+'\n')
print(json.dumps({'disposition':r['disposition'],'manifest_sha256':expected,'unchanged_files':33,'artifacts_bound':len(artifacts),'review_sha256':digest(out/'REVIEW.md'),'receipt_sha256':digest(out/'RECEIPT.json')},indent=2))
