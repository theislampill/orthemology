#!/usr/bin/env python3
"""Portable mechanical binding/replay checks; not a theorem prover or authority grant."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys,shutil
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(rel):return json.loads((ROOT/rel).read_text())
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bind(record,path_key='path'):
 p=ROOT/record[path_key]
 assert p.is_file() and sha(p)==record['sha256'],('digest mismatch',record[path_key])
 if 'bytes' in record:assert p.stat().st_size==record['bytes'],('size mismatch',record[path_key])
 if record.get('git_blob_sha'):
  data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob==record['git_blob_sha'],('Git blob mismatch',record[path_key])
  if record.get('expected_git_blob_sha'):assert blob==record['expected_git_blob_sha']

def check_unit_manifest(folder,filename='MANIFEST.json'):
 m=read(folder+'/'+filename)['files'];count=0
 if isinstance(m,dict):
  for n,d in m.items():assert sha(ROOT/folder/n)==d,(folder,n);count+=1
 else:
  for r in m:bind({**r,'path':folder+'/'+r['path']});count+=1
 return count

def check_bindings():
 top=read('MANIFEST.json')
 for r in top['files']:bind(r)
 expected={r['path'] for r in top['files']}|{'MANIFEST.json'}
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
 assert expected==actual,('unlisted or missing files',actual-expected,expected-actual)
 assert not any(Path(p).suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.html','.jsonl'} for p in actual)
 old=read('geometry-transport-independent-review-20261009/REVIEW_RECEIPT.json')
 assert old['status']=='PASS_FOR_EXACT_LISTED_VERSIONS'
 for r in old['reviewed_inputs']:bind(r)
 assert sha(ROOT/'geometry-transport-independent-review-20261009/REVIEW.md')==old['review_report_sha256']
 scope=read('SCOPE_AND_REVIEW_BINDINGS.json')
 for rel,digest in scope['approved_addition_digests'].items():assert sha(ROOT/rel)==digest,rel
 new=read('tensor-moment-independent-review-20261009/INPUT_BINDINGS.json')
 for r in new['inputs']:bind(r)
 counts={}
 for d in ['information-geometry-transport-20261009','noetic-gradient-transport-20261009','state-dependent-gradient-obstruction-20261009','tensor-moment-continuation-20261009','tensor-moment-independent-review-20261009']:
  counts[d]=check_unit_manifest(d)
 counts['geometry-transport-independent-review-20261009']=check_unit_manifest('geometry-transport-independent-review-20261009','REVIEW_MANIFEST.json')
 all_sources=[]
 for d in ['information-geometry-transport-20261009','noetic-gradient-transport-20261009','state-dependent-gradient-obstruction-20261009']:
  for r in read(d+'/SOURCE_LEDGER.json')['local_sources']:bind(r);all_sources.append(r)
 for r in read('tensor-moment-continuation-20261009/SOURCE_BINDINGS.json')['sources']:bind(r,'local_path');all_sources.append(r)
 remote=read('geometry-transport-independent-review-20261009/REMOTE_SOURCE_BINDINGS.json')['records']
 for r in remote:
  matches=[x for x in all_sources if x.get('url')==r['url']]
  assert matches and all(x.get('git_blob_sha')==r['returned_git_blob'] for x in matches),r['url']
 duty=read('information-duty-bridge-20261009/MANIFEST.json');bind(duty['output'])
 included=0;omitted=0
 for r in duty['input_bindings']:
  if (ROOT/r['path']).exists():bind(r);included+=1
  else:omitted+=1
 assert omitted==3 and included==4
 assert scope['philosophical_note']['independently_mathematically_reviewed'] is False
 return {'payload_files':len(top['files'])+1,'scope_A_reviewed_input_bindings':len(old['reviewed_inputs']),'scope_B_reviewed_input_bindings':len(new['inputs']),'unit_manifest_entries':counts,'selected_source_binding_records':len(all_sources),'retained_remote_pin_observations':len(remote),'duty_note_retained_inputs':included,'duty_note_metadata_only_omissions':omitted,'philosophical_note_not_mathematically_reviewed':True,'unlisted_files':0,'excluded_binary_acquisitions':0}

parser=argparse.ArgumentParser();parser.add_argument('--output-dir',required=True);args=parser.parse_args()
out=Path(args.output_dir).expanduser().resolve()
assert out!=ROOT and ROOT not in out.parents,'Output must be outside the immutable packet'
assert not out.exists(),'Use a new output directory'
out.mkdir(parents=True)
before=check_bindings();print('PASS exhaustive payload, two review scopes and selected source bindings')
# Reconstruct every exact old-stage byte in an external directory, including its own manifest.
hist=read('history/PRIOR_STAGE_MAP.json');oldroot=out/'restored-prior-stage';oldroot.mkdir()
for r in hist['files']:
 src=ROOT/r['archived_path'];assert sha(src)==r['sha256'] and src.stat().st_size==r['bytes']
 dst=oldroot/r['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 assert sha(dst)==r['sha256'] and dst.stat().st_size==r['bytes']
assert len(hist['files'])==43
om=json.loads((oldroot/'STAGING_MANIFEST.json').read_text())
for r in om['files']:
 p=oldroot/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
assert {r['path'] for r in om['files']}|{'STAGING_MANIFEST.json'}=={str(p.relative_to(oldroot)) for p in oldroot.rglob('*') if p.is_file()}
print('PASS exact reconstruction of all 43 prior-stage files')
processes=[]
for job in read('REPLAY_JOBS.json'):
 stdout=out/(job['id']+'.stdout.txt');stderr=out/(job['id']+'.stderr.txt')
 oh=stdout.open('wb');eh=stderr.open('wb')
 p=subprocess.Popen([sys.executable,job['script']],cwd=ROOT,stdout=oh,stderr=eh)
 processes.append((job,p,oh,eh,stdout,stderr))
runs=[]
for job,p,oh,eh,stdout,stderr in processes:
 code=p.wait();oh.close();eh.close()
 assert code==0,(job['id'],code,stderr.read_text(),stdout.read_text())
 expected=ROOT/job['expected_log'];assert stdout.read_bytes()==expected.read_bytes(),('stdout differs',job['id'])
 assert job['success_marker'] in stdout.read_text(),('count marker absent',job['id'])
 assert stderr.stat().st_size==0,('unexpected stderr',job['id'])
 runs.append({'id':job['id'],'script':job['script'],'command':[sys.executable,job['script']],'cwd':str(ROOT),'exit_code':code,'exact_control_count':job['count'],'count_marker':job['success_marker'],'stdout_path':str(stdout),'stdout_sha256':sha(stdout),'preserved_log':job['expected_log'],'preserved_log_sha256':sha(expected),'byte_identical_to_preserved_log':True,'stderr_path':str(stderr),'stderr_bytes':0})
 print('PASS',job['id'],job['count'],'exact controls; byte-identical output')
after=check_bindings();assert before==after
receipt={'status':'PASS','date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_root':str(ROOT),'manifest_sha256':sha(ROOT/'MANIFEST.json'),'binding_checks_before':before,'runs':runs,'binding_checks_after':after,'prior_stage_reconstruction':{'file_count':43,'path':str(oldroot),'all_bytes_match':True},'scope':'Mechanical exact-byte verification and six unchanged control replays. Distinct ordinary mathematical reviews remain bounded. No new proof certification, field-priority claim, philosophical review, new checkpoint, integration, owner acceptance or T20 closure.'}
dump(out/'REPLAY_RECEIPT.json',receipt)
print('PASS six separate control sets and unchanged post-replay bindings')
print('REPLAY_RECEIPT',out/'REPLAY_RECEIPT.json')
