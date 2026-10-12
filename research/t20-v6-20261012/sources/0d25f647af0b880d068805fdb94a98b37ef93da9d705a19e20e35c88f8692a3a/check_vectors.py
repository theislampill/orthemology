#!/usr/bin/env python3
"""Independent exact-Fraction oracle for all new finite-matrix execution rows."""
import pathlib,sys,json,itertools,collections,hashlib
from fractions import Fraction
receipt=pathlib.Path(sys.argv[1]);r=json.loads(receipt.read_text());assert r['status']=='PASS'
log=receipt.parent/'MatrixVectors.log';text=log.read_text();rows=[]
for line in text.splitlines():
 if line.split(',')[0] not in {'invalid','echo','mixed'}:continue
 name,N,k,a,d,H,integer,original=line.split(',');N,k,a,d,H=map(int,[N,k,a,d,H]);rows.append((name,N,k,a,d,H,integer,original))
assert len(rows)==3*4*4*10,len(rows)
assert len(set((n,N,k,a,d) for n,N,k,a,d,*_ in rows))==len(rows)
checks=[]
for name,N,k,a,d,H,integer,original in rows:
 counts=collections.Counter()
 for bits in itertools.product([False,True],repeat=N):
  prefix=1;out=[]
  for b in bits:
   prefix=2*prefix+int(b)
   out.append(False if name=='invalid' else b if name=='echo' else bool((prefix%2)*int(prefix<=5)))
  counts[tuple(out)]+=1
 expectedH=sum(c for c in counts.values() if Fraction(c,2**N)>=Fraction(1,2**k))
 q=Fraction(a,d) if d else Fraction(0)
 expected=q>=1 or q<=Fraction(expectedH,2**N)
 assert H==expectedH,(name,N,k,H,expectedH)
 assert (integer=='true')==expected and integer in {'true','false'},(name,N,k,a,d,'integer')
 assert (original=='true')==expected and original in {'true','false'},(name,N,k,a,d,'original')
 checks.append({'program':name,'N':N,'k':k,'numerator':a,'denominator':d,'heavy_count':H,'matrix':expected})
result={'status':'PASS','rows':len(rows),'exact_value_checks':len(rows)*3,'programs':['invalid','echo','mixed'],'depths':[0,1,2,3],'thresholds':[0,1,2,3],'rational_cases':10,'oracle':'Python Fraction and independent Boolean output-map counting','independent_receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'vector_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'checks':checks}
out=receipt.parent/'VECTOR_RESULT.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
