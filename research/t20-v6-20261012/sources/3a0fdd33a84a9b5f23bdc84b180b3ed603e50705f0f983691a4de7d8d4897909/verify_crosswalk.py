from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parents[1];C=P/'coverage';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=J(C/'CUMULATIVE_PROGRAMME_CROSSWALK.json');errors=[]
def ck(x,msg):
 if not x:errors.append(msg)
base=J(P/'inherited-baseline/TWELVE_AVENUES.json')['avenues']
ck([a['number'] for a in d['avenues']]==list(range(1,13)),'avenue numbering')
for a,b in zip(d['avenues'],base):
 ck(a['result_ids']==b['result_ids'],f'avenue {a["number"]} exact ID preservation')
 ck(a['scope']==b['scope'],f'avenue {a["number"]} scope preservation')
ids={r['id'] for r in d['inherited_result_bindings']}; originals=J(C/'pinned-baseline/RESULT_STATUS.json')['results']
ck(ids=={r['id'] for r in originals},'inherited result set')
ck(len(ids)==262,'262 distinct IDs')
orig={r['id']:r for r in originals}
for r in d['inherited_result_bindings']:ck(r['inherited_statement']==orig[r['id']],r['id']+' inherited exact statement')
sourceids={s['id'] for s in d['inherited_source_bindings']}
ck(sourceids=={s for r in originals for s in r['source_ids']},'source binding closure')
ck(len(sourceids)==835,'835 source IDs')
claims=set()
for t in d['tracks'].values():
 ck((P/t['chapter']).is_file(),'chapter missing '+t['chapter']);claims|={c['id'] for c in J(P/t['register'])['claims']}
for r in d['avenues']+d['families']+d['companion_findings']:
 for x in r.get('current_claim_references',[]):ck(x in claims,'unknown claim '+x)
for s in d['selected_source_reading']:
 p=P/s['local_path'];ck(p.is_file(),'missing selected source '+s['id']);ck(H(p)==s['sha256'],'source hash '+s['id'])
 lines=p.read_text().splitlines()
 for a,b in s['read_scope'].get('line_ranges',[]):ck(1<=a<=b<=len(lines),'read range '+s['id'])
for r in J(C/'pinned-baseline/RETRIEVAL_RECEIPTS.json'):
 p=Path(r['path']);b=p.read_bytes();ck(H(p)==r['public_sha256'],'retrieved public hash '+r['id']);ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha'],'retrieved Git identity '+r['id'])
for p,sha in [(C/'pinned-baseline/RESULT_STATUS.json','de45612a3d7d68b78ed65dacf4dc8a9080b00f9b'),(C/'pinned-baseline/SOURCE_MAP.json','4d61a64f4e9022dc24e517f26923980aaf6fdcda')]:
 b=p.read_bytes();ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,'baseline Git identity '+p.name)
for x in d['baseline_bindings']:ck(H(P/x['path'])==x['sha256'],'baseline byte change '+x['path'])
ck(J(C/'SELECTED_SOURCE_READS.json')==d['selected_source_reading'],'selected ledger agreement');ck(J(C/'COVERAGE_ALERTS.json')==d['coverage_alerts'],'alerts agreement')
report={'status':'PASS' if not errors else 'FAIL','scope':'Crosswalk mechanical identity/ID/source-range checks only; not independent scientific review or fresh proof/source replay.','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'avenues':12,'inherited_results':len(ids),'referenced_source_ids':len(sourceids),'selected_source_records':len(d['selected_source_reading']),'all_four_chapters_exist':all((P/t['chapter']).is_file() for t in d['tracks'].values()),'files_sha256':{p.name:H(p) for p in [C/'CUMULATIVE_PROGRAMME_CROSSWALK.md',C/'CUMULATIVE_PROGRAMME_CROSSWALK.json',C/'SELECTED_SOURCE_READS.json',C/'COVERAGE_ALERTS.json']}}
(C/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
