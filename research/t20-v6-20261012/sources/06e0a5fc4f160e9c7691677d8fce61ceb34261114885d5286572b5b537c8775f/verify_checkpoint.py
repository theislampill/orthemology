from pathlib import Path
import hashlib,json,subprocess,tempfile,shutil,re
W=Path(__file__).resolve().parents[2];A=Path(__file__).resolve().parent;P=W/'t20-consolidation-20261011/projection/package-v3';V=P.with_name('package-v2')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
checks=[]
def record(name):checks.append(name)
require(h(V/'PACKAGE_CONTENTS.json')=='93649106196dd79e460ac054eb4bb667c2f84902f65a201d75405284cbaab16a','v2 manifest changed');record('v2 manifest immutable')
for row in json.loads((V/'PACKAGE_CONTENTS.json').read_text())['files']:
 require(h(V/row['path'])==row['sha256'] and (V/row['path']).stat().st_size==row['bytes'],'v2 source changed '+row['path'])
record('every original v2 member unchanged')
sourcecopies=[]
for row in json.loads((V/'PUBLIC_PROJECTION.json').read_text())['files']:
 sourcecopies += ([row['public_path']] if row.get('public_path') else [])+[x['path'] for x in row.get('required_replay_copies',[])]
for rel in sourcecopies:require(h(V/rel)==h(P/rel),'original public source changed '+rel)
record('1475 historical scientific source copy records unchanged')
for row in json.loads((P/'CLAIM_REGISTER.json').read_text())['claims']:
 require(h(P/row['record_file'])==row['record_file_sha256'],'claim record SHA mismatch')
 records=json.loads((P/row['record_file']).read_text())[row['record_selector']['array']]
 require(any(x['id']==row['record_selector']['id'] for x in records),'claim missing')
record('all 137 current claim index targets and hashes')
for row in json.loads((P/'READER_PROJECTION.json').read_text())['v3_reader_files']:require(h(P/row['path'])==row['v3_sha256'],'reader hash mismatch')
record('all current reader projection hashes')
for row in json.loads((P/'reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json').read_text())['targets']:
 require(h(P/row['public_target'])==row['public_sha256'],'review public binding mismatch')
 if row['projection']=='EXACT':require(row['public_sha256']==row['original_sha256'],'review false exact')
record('scientific independent-review target identities')
for row in json.loads((P/'REASSESSMENT_REPLAY_VERIFICATION.json').read_text())['runs']:
 for f in row['suite_sources']:require(h(P/f['path'])==f['sha256'],'fresh replay source drift')
record('all eight selected replay source closures current')
manifest=json.loads((P/'PACKAGE_CONTENTS.json').read_text()); manifestpaths={r['path'] for r in manifest['files']}
for bad in ['.library-helper','.helpers','OWNER_PRO_THREAD_INSTRUCTIONS','INDEPENDENT_DEPTH_ASSESSMENT','LIBRARY_IDENTITIES','Orthemology_T20_Dot_Recovery_Handoff_FULL']:
 require(not any(bad in path for path in manifestpaths),'excluded private/bulk file')
record('named private transfer/instruction/assessment and bulk-corpus exclusions')
with tempfile.TemporaryDirectory(prefix='final-whitespace-',dir=A) as t:
 root=Path(t);shutil.copytree(P,root/'candidate');subprocess.run(['git','init','-q',str(root)],check=True);subprocess.run(['git','-C',str(root),'add','--all'],check=True);r=subprocess.run(['git','-C',str(root),'diff','--cached','--check'],capture_output=True,text=True);diagnostics=[]
 for line in r.stdout.splitlines():
  m=re.match(r'candidate/(.+):(\d+): (.+)',line)
  if m:diagnostics.append({'path':m[1],'line':int(m[2]),'diagnostic':m[3]})
expected=json.loads((P/'EXACT_SOURCE_WHITESPACE.json').read_text());known={json.dumps(x,sort_keys=True) for row in expected['advisories'] for x in row['diagnostics']};actual={json.dumps(x,sort_keys=True) for x in diagnostics}
require(actual==known,'final whitespace accounting mismatch');record('final staged whitespace exactly matches scoped original-source advisories')
result={'status':'PASS','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'checks':checks,'whole_delta_strict_whitespace_exit_code':r.returncode,'whole_delta_strict_whitespace_pass':r.returncode==0,'authored_derived_whitespace_clean':True,'whitespace_diagnostics':len(diagnostics),'old_scientific_copy_records':len(sourcecopies),'v2_manifest_unchanged':True,'scope':'Local intermediate candidate and currentness verification only; no repository gates, upload, PR, or scientific closure.'}
(A/'UPDATE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
