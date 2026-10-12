from pathlib import Path
import json,re,hashlib
W=Path.cwd(); C=W/'hase-certificate-code-validity-20261010';R=W/'hase-certificate-domain-independent-review-20261010'
schema=json.loads((C/'SCHEMA.json').read_text());sources={}
for t in schema:
 name=t['type']
 if name in ['StepCert','RedCert','FiniteCert','PolyCert','LookupCert']:p=W/'hase-joint-certificate-auxiliary-20261010/AuxiliaryCertificates.lean'
 elif name=='Rule':p=W/'hase-joint-certificate-checker-20261010/CertificateRules.lean'
 elif name=='Claim':p=W/'hase-joint-certificate-checker-20261010/CertificateFramework.lean'
 else:p=W/'hase-joint-certificate-codec-20261010/SerializedCertificateCodec.lean'
 text=p.read_text().split('inductive '+name,1)[1].split('where',1)[1]
 lines=[]
 for line in text.splitlines():
  if line.strip().startswith('|'):lines.append(line)
  elif lines:break
 names=[re.match(r'\s*\|\s*(\w+)',x)[1] for x in lines]
 assert names==[x['name'] for x in t['ctors']],name
 for line,c in zip(lines,t['ctors']):
  if ':' in line and not '(' in line:
   fields=[x.strip() for x in line.split(':',1)[1].split('→')[:-1]]
  else:
   fields=[]
   for raw in re.findall(r'\((.*?)\)',line):
    var,ty=raw.split(':');fields += [ty.strip()]*len(var.split())
  fields=[x.replace('OrthemologyV2.','').replace('P01D.','').replace('P01AC.','').replace('AuxiliaryCertificates.','') for x in fields]
  expected=[x.replace('P01AC.','') for x in c['fields']]
  assert fields==expected,(name,c['name'],fields,expected)
 sources[str(p.relative_to(W))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
receipt={'status':'PASS','constructor_total':sum(len(t['ctors']) for t in schema),'retained_source_declarations_checked':9,'names_order_arities_and_field_types_match':True,'sources':sources}
(R/'SCHEMA_COVERAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
