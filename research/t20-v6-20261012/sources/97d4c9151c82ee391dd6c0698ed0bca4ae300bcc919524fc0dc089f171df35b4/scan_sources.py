#!/usr/bin/env python3
"""Supplementary token check, in addition to transitive kernel axiom readback."""
import pathlib,re,json,hashlib,sys
receipt=pathlib.Path(sys.argv[1]);base=receipt.parent
r=json.loads(receipt.read_text()) if receipt.exists() else json.loads((base/'MANIFEST.json').read_text())
def code_only(s):
 out=[];i=0;depth=0;string=False
 while i<len(s):
  if depth:
   if s.startswith('/-',i):depth+=1;i+=2
   elif s.startswith('-/',i):depth-=1;i+=2
   else:out.append('\n' if s[i]=='\n' else ' ');i+=1
  elif string:
   if s[i]=='\\':i+=2
   elif s[i]=='"':string=False;i+=1
   else:out.append('\n' if s[i]=='\n' else ' ');i+=1
  elif s.startswith('/-',i):depth=1;i+=2
  elif s.startswith('--',i):
   while i<len(s) and s[i]!='\n':i+=1
  elif s[i]=='"':string=True;i+=1
  else:out.append(s[i]);i+=1
 return ''.join(out)
rows=[]
for m,v in r['sources'].items():
 p=base/'sources'/(m.replace('.','/')+'.lean');text=code_only(p.read_text())
 found=[{'line':text[:x.start()].count('\n')+1,'token':x.group(0)} for x in re.finditer(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide)\b|^\s*opaque\b',text,re.M)]
 rows.append({'module':m,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'findings':found})
result={'status':'PASS' if all(not x['findings'] for x in rows) else 'FINDINGS','scanned_modules':len(rows),'sources':rows}
(base/'SOURCE_SCAN_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'scanned_modules':len(rows)}));raise SystemExit(0 if result['status']=='PASS' else 1)
