from pathlib import Path
import json,hashlib,datetime,re,sys
D=Path(__file__).resolve().parent;W=D.parents[1];P=W/'t20-consolidation-20261011/projection/package-v4';V=P.with_name('package-v3');R=W/'t20-depth-reassessment-20261011';checks=[]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def req(label,ok,detail=None):checks.append({'label':label,'pass':bool(ok),'detail':detail})
base=read(D/'V3_BASELINE_FILES.json');pres=read(P/'depth/V3_PRESERVATION.json')['files'];req('preservation exhaustive unique v3 paths',len(pres)==len(base) and {r['v3_path'] for r in pres}==set(base))
for r in pres:req('preimage '+r['v3_path'],r['v3_sha256']==base[r['v3_path']]['sha256']==h(P/r['v4_path']) and r['bytes']==base[r['v3_path']]['bytes'])
for lane in [p for p in (P/'depth').iterdir() if p.is_dir() and (R/p.name).is_dir()]:
 for f in lane.rglob('*'):
  if f.is_file() and f.suffix in ['.md','.py','.diff','.patch']:
   src=R/lane.name/f.relative_to(lane)
   req('new exact scientific source '+f.relative_to(P).as_posix(),src.is_file() and h(src)==h(f))
for r in read(P/'depth/REVIEW_CURRENTNESS.json')['reviews']:
 req('report exists '+r['packet'],h(P/r['report'])==r['report_sha256']);req('review exists '+r['packet'],h(P/r['review'])==r['review_sha256'])
 for w in r['binding_witnesses']:
  v=read(P/w['path'])
  for k in w['selector']:v=v[k]
  req('structured current report witness '+r['packet'],v==r['report_sha256']==w['expected_report_sha256'])
 for b in r['current_binding_documents']:
  rel=Path(b['path']);source=R/rel.parts[1]/Path(*rel.parts[2:]);req('current original review input '+str(source.relative_to(R)),h(source)==b['original_sha256']);req('current public review input '+b['path'],h(P/b['path'])==b['public_sha256'])
for r in read(P/'DEPTH_REPLAY_VERIFICATION.json')['runs']:
 for b in r['suite_sources']:req('replay closure '+b['path'],h(P/b['path'])==b['sha256'] and (P/b['path']).stat().st_size==b['bytes'])
for r in read(P/'depth/CLAIMS.json')['claims']:
 o=r['source_owner'];req('new claim owner '+r['id'],h(P/o['path'])==o['sha256'])
for r in read(P/'coverage/methodology/PROJECTION_BINDINGS.json'):
 p=P/'coverage/methodology'/r['file'];req('methodology projected digest '+r['source_id'],h(p)==r['public_sha256'] and p.stat().st_size==r['public_bytes'])
for r in read(P/'coverage/SELECTED_SOURCE_READS.json'):
 if r['id'] in ['S25','S26','S27','S28']:req('methodology navigation '+r['id'],h(P/r['public_source'])==r['public_sha256'])
# Exact delta accounting; generated self-members are intentionally excluded.
a=set(base);b={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()};delta=read(P/'depth/V3_TO_V4_DIFF.json');skip={'PACKAGE_CONTENTS.json','depth/V3_TO_V4_DIFF.json','depth/V3_TO_V4.patch'}
req('delta added set',set(r['path'] for r in delta['added'])==(b-a)-skip)
req('delta changed set',set(r['path'] for r in delta['changed'])=={r for r in a&b if h(P/r)!=base[r]['sha256']}-skip)
req('delta no removed',delta['removed']==sorted(a-b))
for r in delta['added']:req('delta addition '+r['path'],h(P/r['path'])==r['sha256'] and (P/r['path']).stat().st_size==r['bytes'])
for r in delta['changed']:req('delta change '+r['path'],base[r['path']]['sha256']==r['v3_sha256'] and h(P/r['path'])==r['v4_sha256'])
errors=[x for x in checks if not x['pass']];result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not errors else 'FAIL','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'checks':len(checks),'errors':errors};(D/'EXTRA_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(D/'EXTRA_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
