from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for driver in ['verify_inputs.py','verify_archive.py']:
 p=subprocess.run(['python',str(R/driver)],capture_output=True,text=True);assert p.returncode==0,(driver,p.stdout,p.stderr)
a=json.loads((R/'ASSESSMENT.json').read_text())
for name,row in a['evidence'].items():
 p=R/name;assert p.is_file() and p.stat().st_size==row['bytes'] and H(p)==row['sha256'],name
j=json.loads((R/'RESULT.json').read_text());assert j['status']=='FRESH_INDEPENDENT_BUILD_AND_AXIOM_READBACK_PASS';assert len(j['sources'])==27 and len(j['axioms'])==135
assert all(x['exit_code']==0 for x in j['builds']);assert all(set(v)<={'propext','Quot.sound','Classical.choice'} for v in j['axioms'].values())
for name,row in j['sources'].items():
 assert H(R/'sources'/(name+'.lean'))==row['sha256'];assert H(R/'lib'/(name+'.olean'))==row['olean_sha256']
c=json.loads((R/'INDEPENDENT_CONTROLS.json').read_text());assert c['theorem_count']==16;assert H(R/'sources/IndependentDependentControls.lean')==c['source_sha256'];assert H(R/'lib/IndependentDependentControls.olean')==c['olean_sha256']
assert H(R/'sources/IndependentAudit.lean')==j['audit_source_sha256'];assert H(R/'lib/IndependentAudit.olean')==j['audit_olean_sha256'];assert H(R/'readbacks.log')==j['audit_readback_sha256']
print('PASS: sealed 178-member archive; 27 fresh local implementation/import builds; 114 author + 21 independent declaration readbacks; 16 independent theorem controls; 3 expected mutation rejections; source/object/evidence identities; canonical main unchanged')
