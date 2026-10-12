"""Read-only receipt/source/object verification for this independent audit."""
from pathlib import Path
import json, hashlib, re
R=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((R/'ASSESSMENT.json').read_text())
for f,row in a['evidence'].items():
 assert H(R/f)==row['sha256'],f
 assert (R/f).stat().st_size==row['bytes'],f
for mode in ['p01','p03','measure']:
 j=json.loads((R/mode/'RESULT.json').read_text())
 assert j['status']=='FRESH_INDEPENDENT_BUILD_AND_AXIOM_READBACK_PASS'
 assert all(x['exit_code']==0 for x in j['builds'])
 assert all(set(v)<={'propext','Quot.sound','Classical.choice'} for v in j['axioms'].values())
 for m,row in j['sources'].items():
  assert H(R/mode/'sources'/(m.replace('.','/')+'.lean'))==row['sha256'],m
  assert H(R/mode/'lib'/(m.replace('.','/')+'.olean'))==row['fresh_olean_sha256'],m
j=json.loads((R/'native-case-replay/RESULT.json').read_text())
assert j['status']=='PASS' and j['cases_run']==188 and all(x['exit_code']==0 for x in j['modules'])
for row in j['cases']:
 assert H(R/'native-case-replay/fixtures'/(row['name']+'.json'))==row['raw_sha256']
assert j['outcomes']=={'accept':54,'refuse':134} and j['duplicate_cases']==41 and j['native_cases']==147
c=json.loads((R/'p01/evidence/IndependentEffectControls.json').read_text())
assert c['exit_code']==0
assert H(R/'p01/sources/IndependentEffectControls.lean')==c['source_sha256']
assert H(R/'p01/lib/IndependentEffectControls.olean')==c['olean_sha256']
s=(R/'p01/evidence/IndependentControlsAudit.stdout').read_text()
assert 'sorryAx' not in s and len(re.findall(r"'SuccessorIndependentAudit\.[^']+' (?:does not depend|depends)",s))==13
print('PASS: receipt/source/object identity; 151 + 30 + 84 target audits; 188 concrete native comparisons; 13 independent effect controls')
