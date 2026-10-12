"""Independent reviewer: transition-monoid observation signatures, no author imports."""
import json, hashlib, itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'t20-depth-reassessment-20261011/occurrence_warrant'
r=json.loads((BASE/'sources/source_rows.json').read_text())['records']
row=[tuple(x['antecedents']) for x in r]+[('excluded',)]
voice=[x['role'] in {'direct_exposition','direct_exposition_with_reasons'} for x in r]+[None]
works=sorted({x['work_id'] for x in r})
identity=tuple(range(8))
ops=[tuple(7 if i==7 or r[i]['work_id']==w else i for i in range(8)) for w in works]
monoid={identity}; changed=True
while changed:
 new={tuple(op[t] for t in transform) for transform in monoid for op in ops}|monoid
 changed=new!=monoid; monoid=new
if len(monoid)!=8: raise ValueError('Expected exactly all subsets of excluded named works')
results={}
for name,use_voice,use_exclusion in [('content_only',False,False),('content_and_voice',True,False),('content_voice_and_work_exclusion',True,True)]:
 transforms=sorted(monoid) if use_exclusion else [identity]
 signatures=[tuple((row[t[i]],voice[t[i]] if use_voice else None) for t in transforms) for i in range(8)]
 fibres={z:{signatures[i] for i in range(8) if row[i]==z} for z in row}
 minimum=max(map(len,fibres.values()))
 counts={}
 for m in range(1,minimum+1):
  count=0
  for labels in itertools.product(range(m),repeat=7):
   labels=labels+(0,)
   # Every merged encoded pair must have equal observations after every compositional operation.
   if all(row[i]!=row[j] or labels[i]!=labels[j] or signatures[i]==signatures[j] for i in range(8) for j in range(i)):
    count+=1
  counts[str(m)]=count
 results[name]={'minimum_alphabet':minimum,'encoder_counts':counts,'blocks':len(set(signatures))}
expected=[(1,{'1':1},4),(2,{'1':0,'2':8},6),(3,{'1':0,'2':0,'3':108},8)]
if [(v['minimum_alphabet'],v['encoder_counts'],v['blocks']) for v in results.values()]!=expected: raise ValueError('Mismatch')
# Explicit attainable three-symbol sidecar; labels reused across distinct rows.
k=(0,0,1,1,2,2,0,0)
if len({(row[i],k[i]) for i in range(8)})!=8: raise ValueError('Attaining encoding failed')
# Stated scope guards: identity copy and absorbing exclusion retain no lost-record identity.
if not all(t[7]==7 for t in monoid): raise ValueError('Nonabsorbing exclusion')
# A restore-to-original operation could not be defined on this single excluded state.
restore_conflict=len({(row[i],voice[i],r[i]['work_id']) for i in range(7)})>1
receipt=json.loads((BASE/'READING_RECEIPT.json').read_text())
checks=[]
for s in receipt['sources']:
 p=ROOT/s['path']; b=p.read_bytes()
 ok=hashlib.sha256(b).hexdigest()==s['sha256'] and len(b)==s['bytes']
 if not ok: raise ValueError('Receipt drift '+s['id'])
 checks.append({'id':s['id'],'sha256':s['sha256'],'bytes':len(b)})
reg=json.loads((ROOT/'t20-consolidation-20261011/foundations/SOURCES_AND_READING.json').read_text())
sources=reg['sources']
missing='52fbe080e7bd57f6c06e695a28428052463702d3ccce72bf2c7ba6ad493250d0'
if len(sources)!=49 or missing in json.dumps(sources): raise ValueError('Coverage mismatch')
print(json.dumps({'status':'PASS','method':'Full generated transition monoid and future observation signatures; no author checker imported','transition_monoid_size':len(monoid),'contracts':results,'explicit_sidecar':k,'restoration_requires_richer_state':restore_conflict,'receipt_bindings_verified':checks,'foundational_register_count':len(sources),'source_return_separately_absent':True,'limits':'No primary authentication, source interpretation revalidation, or epistemic warrant test.'},indent=2))
