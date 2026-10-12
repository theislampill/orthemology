from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-coded-rule-templates-20261010';rows=json.loads((W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json').read_text());s=(W/'hase-joint-certificate-checker-20261010/CertificateRules.lean').read_text()
patterns=re.findall(r'^  \| (\w+)[ \t]*(.*)$',s.split('def Rule.conclusion')[0],re.M);assert len(patterns)==len(rows)==63
for (name,params),row in zip(patterns,rows):
 assert name==row['tag'];assert [list(x) for x in re.findall(r'\((\w+) : ([^)]*)\)',params)]==row['params']
for function,key in [('conclusion','claim'),('premises','plist'),('checkSide','side')]:
 seg=s.split('def Rule.'+function+' :',1)[1].split('\ndef ',1)[0].split('\ntheorem ',1)[0];branches=re.findall(r'^  \| \.(\w+)[ \t]+(.*?) => (.*)$',seg,re.M);assert len(branches)==63
 for (tag,params,rhs),row in zip(branches,rows):
  assert tag==row['tag'];assert params.split()==[p for p,t in row['params']]
  if function=='checkSide':assert rhs.startswith('decide (') and rhs.endswith(')');rhs=rhs[8:-1]
  assert rhs==row[key],(tag,function)
 print('EXACT_SOURCE_METADATA',function,63)
