from fractions import Fraction as F
from itertools import product
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
b=json.loads((BASE/'source-audit-revision-semantics-20261010/OCCURRENCE_BINDINGS.json').read_text())
for row in b['files']:
 data=(BASE/row['path']).read_bytes()
 assert len(data)==row['bytes']
 assert hashlib.sha256(data).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
 if 'normalized_git_blob_sha1' in row:
  data=data[:-1]
  assert len(data)==row['normalized_bytes']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['normalized_git_blob_sha1']
for theta,y in product((0,1),repeat=2):
 d=theta^y
 assert theta==y^d
for theta,y,v in product((0,1),repeat=3):
 d=v^y
 assert y^d==v
 assert ((y^d)==theta)==(v==theta)
rows=[]
for a in (F(1,5),F(1,2),F(4,5),F(1)):
 law={(t,y,d):F(1,4)*(a if t==(y^d) else 1-a) for t,y,d in product((0,1),repeat=3)}
 for y,d in product((0,1),repeat=2):
  den=sum(law[t,y,d] for t in (0,1))
  assert den==F(1,4)
  assert law[y^d,y,d]/den==a
 rows.append({'a':str(a),'posterior_of_decoded_target':str(a)})
print(json.dumps({'status':'PASS','exact_comparator_cases':4,'fallible_logical_cases':8,
 'symmetric_random_report_models':rows,'bound_inputs_verified':len(b['files']),
 'scope':'Ordinary binary algebra and finite conditional probabilities only; not a System R derivation or knowledge certificate.'},indent=2))
