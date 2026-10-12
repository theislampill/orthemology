"""Offline current-depth binding/closure verification; no mathematical proof claim."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(rel):return json.loads((P/rel).read_text())
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def main():
 for r in read('depth/V3_PRESERVATION.json')['files']:
  require(h(P/r['v4_path'])==r['v3_sha256'],'predecessor changed '+r['v3_path'])
 for r in read('PUBLIC_PROJECTION.json')['files']:
  for c in r.get('required_replay_copies',[]):require(h(P/c['path'])==c['sha256'],'replay source mismatch '+c['path'])
 for r in read('CLAIM_REGISTER.json')['claims']:
  require(h(P/r['record_file'])==r['record_file_sha256'],'claim owner changed '+r['id'])
  records=read(r['record_file'])[r['record_selector']['array']]
  require(any(c['id']==r['record_selector']['id'] for c in records),'missing claim '+r['id'])
 for r in read('depth/REVIEW_CURRENTNESS.json')['reviews']:
  require(h(P/r['report'])==r['report_sha256'],'reviewed report drift '+r['packet'])
  require(h(P/r['review'])==r['review_sha256'],'review body drift '+r['packet'])
  require(bool(r['binding_witnesses']),'missing structured review witness')
  for witness in r['binding_witnesses']:
   value=read(witness['path'])
   for key in witness['selector']:value=value[key]
   require(value==r['report_sha256']==witness['expected_report_sha256'],'review does not bind current report '+r['packet'])
  for c in r['current_binding_documents']:require(h(P/c['path'])==c['public_sha256'],'review binding drift')
 for r in read('DEPTH_REPLAY_VERIFICATION.json')['runs']:
  for c in r['suite_sources']:require(h(P/c['path'])==c['sha256'],'fresh suite source drift '+c['path'])
 for r in read('READER_PROJECTION.json')['v4_reader_files']:require(h(P/r['path'])==r['v4_sha256'],'current reader drift')
 for r in read('coverage/SELECTED_SOURCE_READS.json'):
  if r['id'] in ['S25','S26','S27','S28']:require(h(P/r['public_source'])==r['public_sha256'],'methodology route')
 def walk(value):
  if isinstance(value,dict):
   route=value.get('public_source');digest=value.get('public_sha256')
   if isinstance(route,str) and not route.startswith(('https://','CUSTODY_ONLY')):
    require((P/route).is_file(),'unresolved public source '+route)
    if digest:require(h(P/route)==digest,'public source digest drift '+route)
    if value.get('public_projection')=='EXACT' and value.get('sha256'):require(h(P/route)==value['sha256'],'false exact public source '+route)
   for item in value.values():walk(item)
  elif isinstance(value,list):
   for item in value:walk(item)
 for path in (P/'depth').rglob('*.json'):
  if 'inherited-v3' not in path.parts:walk(json.loads(path.read_text()))
 require(read('CURRENT_STATUS.json')['T21_started'] is False,'T21 incorrectly started')
 print(json.dumps({'status':'PASS','scope':'Current exact/public bindings, predecessor preservation, selected execution closure and methodology routes only. No proof, primary-reading or repository validation claim.'}))
if __name__=='__main__':main()
