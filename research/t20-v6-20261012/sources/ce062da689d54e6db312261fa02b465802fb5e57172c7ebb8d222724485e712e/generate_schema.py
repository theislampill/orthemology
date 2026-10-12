#!/usr/bin/env python3
"""Generate explicit candidate grammar from retained finite constructor declarations.
The emitted equations/proofs are checked by Lean; this generator is not trusted.
"""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parent;W=R.parent
sorts={'Term':0,'TypeCode':1,'Poly':2,'Ty':3,'Nat':4,'Tel':5,'List P01AC.Ty':5,'StepCert':6,'RedCert':7,'FiniteCert':8,'PolyCert':9,'LookupCert':10,'Claim':11,'Rule':12,'SerialCert':13,'SerialCertList':14}
full={'Term':'OrthemologyV2.Term','TypeCode':'OrthemologyV2.TypeCode','Poly':'P01D.Poly','Ty':'P01AC.Ty','Nat':'Nat','Tel':'P01AC.Tel','List P01AC.Ty':'List P01AC.Ty'}
for n in ['StepCert','RedCert','FiniteCert','PolyCert','LookupCert']:full[n]='AuxiliaryCertificates.'+n
for n in ['Claim','Rule','SerialCert','SerialCertList']:full[n]='JointCertificates.'+n
alias={v:k for k,v in full.items()};alias.update({k:k for k in full})
def decls(typ,path):
 s=path.read_text(); m=re.search(r'inductive '+typ+r'\b[^\n]*\n(.*?)(?:\n\s*deriving |\n\ndef |\nend)',s,re.S)
 if not m:raise ValueError(typ)
 cs=[]
 for line in m.group(1).splitlines():
  if not line.strip().startswith('|'):continue
  n=re.match(r'\s*\|\s+(\w+)',line).group(1);fields=[]
  for names,ft in re.findall(r'\(([^():]+)\s*:\s*([^()]+)\)',line):
   ft=ft.strip();ft=alias.get(ft,ft)
   if ft not in sorts:raise ValueError((typ,n,ft))
   fields.extend([ft]*len(names.split()))
  cs.append(dict(name=n,fields=fields))
 return cs
schema=[]
aux=W/'hase-joint-certificate-auxiliary-20261010/AuxiliaryCertificates.lean'
for typ in ['StepCert','RedCert','FiniteCert','PolyCert','LookupCert']:schema.append(dict(type=typ,sort=sorts[typ],ctors=decls(typ,aux)))
schema.append(dict(type='Claim',sort=11,ctors=[dict(name=n,fields=f) for n,f in [('ctxJ',['Tel']),('formJ',['Tel','Ty']),('hasJ',['Tel','Poly','Ty']),('ctxE',['Tel']),('formE',['Tel','Ty']),('hasE',['Tel','Poly','Ty'])]]))
schema.append(dict(type='Rule',sort=12,ctors=decls('Rule',W/'hase-joint-certificate-checker-20261010/CertificateRules.lean')))
schema.extend([dict(type='SerialCert',sort=13,ctors=[dict(name='node',fields=['Rule','SerialCertList'])]),dict(type='SerialCertList',sort=14,ctors=[dict(name='nil',fields=[]),dict(name='cons',fields=['SerialCert','SerialCertList'])])])
for t in schema:
 for tag,ctor in enumerate(t['ctors']):
  ctor['tag']=tag;ctor['wrapped']=[not (x==t['type'] or {x,t['type']} <= {'SerialCert','SerialCertList'}) for x in ctor['fields']]
  ctor['sorts']=[sorts[x] for x in ctor['fields']]
assert [len(t['ctors']) for t in schema]==[5,2,7,8,2,6,63,1,2]
(R/'SCHEMA.json').write_text(json.dumps(schema,indent=2)+'\n')
lines=['import ConstructorDescriptors','import StepCode','import PolyCode','import SerializedCertificateCodec','namespace CertificateCodeValidity','open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability','open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates','set_option maxRecDepth 16384','set_option maxHeartbeats 1000000','attribute [local irreducible] Nat.pair','']
for t in schema:
 desc=t['type'][0].lower()+t['type'][1:]+'Description';t['description']=desc
 rows=['['+', '.join('('+str(w).lower()+', '+str(k)+')' for w,k in zip(c['wrapped'],c['sorts']))+']' for c in t['ctors']]
 lines.append('def '+desc+' : Description := [\n  '+',\n  '.join(rows)+']\n')
 for c in t['ctors']:
  if t['type']=='StepCert':c['lemma']='AuxiliaryCodeComputability.encode_step_'+c['name'];continue
  if t['type']=='PolyCert':c['lemma']='AuxiliaryCodeComputability.encode_poly_'+c['name'];continue
  name='encode_'+t['type']+'_'+c['name'];c['lemma']=name
  args=['a'+str(i) for i in range(len(c['fields']))]
  bind=' '.join('('+a+' : '+full[ty]+')' for a,ty in zip(args,c['fields']))
  encfields=['leaf (encode '+a+')' if w else 'encode '+a for a,w in zip(args,c['wrapped'])]
  ctor='('+full[t['type']]+'.'+c['name']+(' '+' '.join(args) if args else '')+')'
  lines.append('@[simp] theorem '+name+' '+bind+' : encode '+ctor+' = pack '+str(c['tag'])+' ['+', '.join(encfields)+'] := rfl\n')
(R/'CertificateDescriptions.lean').write_text('\n'.join(lines)+'\nend CertificateCodeValidity\n')
(R/'SCHEMA.json').write_text(json.dumps(schema,indent=2)+'\n')
print([(t['type'],len(t['ctors'])) for t in schema])
