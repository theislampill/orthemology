import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path.cwd(); OUT=ROOT/'t20-depth-reassessment-20261011/cross_front_synthesis'; BASE='t20-depth-reassessment-20261011/'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
spec={
'B':('t20-consolidation-20261011/MATHEMATICAL_SYNTHESIS.md','Complete chapter read'),
'F':('t20-consolidation-20261011/FOUNDATIONAL_CROSSWALK.md','Complete chapter read'),
'FT':('t20-consolidation-20261011/foundations/FOUNDATIONAL_SYNTHESIS.md','Selected §§7–11 read; broad combined display truncated; no full-chapter credit'),
'GT':('t20-consolidation-20261011/geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','§§1–3 and §§7–9 read; other portions only partial combined display'),
'PT':('t20-consolidation-20261011/proofs/PROOF_TYPE_INQUIRY_SYNTHESIS.md','§§2–4 read, other portions partial combined display'),
'ET':('t20-consolidation-20261011/evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md','Selected §4.2 ET-14 paragraph and §§5–8; some combined output truncated, no whole-chapter credit')}
for key,d in [('A','audit_symmetries'),('R','restricted_controls'),('J','joint_correction'),('S','semantic_geometry'),('P','proof_inquiry'),('U','uncertainty_inquiry'),('G','grounding_provenance'),('D','decision_representation'),('C','collective_continuation'),('O','occurrence_warrant')]:
 scope='Substantive result and proof/scope sections read; independent review read separately where present'
 if key in ['R','S','P','U','D','C','O']: scope='Complete report read'
 if key=='A': scope='§§1–5 read fully; §6 partly displayed and independently summarized/qualified in AR; §7 not full-reading credit'
 if key=='J': scope='§§1–7 substantive extracts, including numerical/order/topology results; combined output truncated part of internal-method derivation; JR derivation and correction read; no full-report reading credit'
 if key=='G': scope='§§1–8 read across separate displays; initial broad display truncated other reports but retained G §§2–8'
 spec[key]=(BASE+d+'/RESULT.md',scope)
spec['OR']=('t20-consolidation-20261011/catalogue/objects/52/52fbe080e7bd57f6c06e695a28428052463702d3ccce72bf2c7ba6ad493250d0','Full source-return report read; its primary reading and print controls remain inherited, no fresh Arabic authentication')
reviews={'AR':'independent_review','JR':'joint_correction_review','SR':'semantic_geometry_review','PR':'proof_inquiry_review','UR':'uncertainty_inquiry_review','GR':'grounding_provenance_review','DR':'decision_representation_review','CR':'collective_continuation_review','OVR':'occurrence_warrant_review'}
for key,d in reviews.items():spec[key]=(BASE+d+'/REVIEW.md','Substantive review read; AR and UR broad combined display portions repeated in targeted reads; review evidence/ceilings incorporated')
spec['CRF']=(BASE+'collective_continuation_review/REFRESH.md','Complete exact prose-refresh note read; no fresh execution credited')
records=[]
for k,(p,scope) in spec.items():
 f=ROOT/p; records.append(dict(id=k,path=p,sha256=sha(f),bytes=f.stat().st_size,read_scope=scope,role='review' if k in reviews or k=='CRF' else 'synthesis' if k in ['B','F','FT','GT','PT','ET'] else 'result'))
# Verify exact inherited-object pointers in source ledgers without claiming to read their bodies.
ledgers=['audit_symmetries/SOURCE_BINDINGS.json','joint_correction/SOURCE_BINDINGS.json','semantic_geometry/SOURCE_BINDINGS.json','proof_inquiry/SOURCE_BINDINGS.json','uncertainty_inquiry/READ_LEDGER.json','grounding_provenance/INPUT_BINDINGS.json','decision_representation/READ_LEDGER.json','collective_continuation/INPUT_BINDINGS.json','occurrence_warrant/READING_RECEIPT.json']
anc=[]; seen=set()
def walk(x,ledger):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64:
   raw=x['path']; p=Path(raw); p=p if p.is_absolute() else ROOT/p
   tag=(str(p),x['sha256'])
   if tag not in seen:
    seen.add(tag); exists=p.is_file(); actual=sha(p) if exists else None
    anc.append(dict(path=raw,expected_sha256=x['sha256'],actual_sha256=actual,status='match' if actual==x['sha256'] else 'missing' if not exists else 'mismatch',via=ledger,body_read_credit='none from this identity check'))
  for v in x.values():walk(v,ledger)
 elif isinstance(x,list):
  for v in x:walk(v,ledger)
for rel in ledgers:
 f=ROOT/BASE/rel
 if f.exists():
  records.append(dict(id='ledger:'+rel.split('/')[0],path=str(f.relative_to(ROOT)),sha256=sha(f),bytes=f.stat().st_size,read_scope='Identity records parsed and hash-checked; not entire substantive ancestor bodies',role='upstream_identity_ledger'))
  walk(json.loads(f.read_text()),str(f.relative_to(ROOT)))
# Review-binding occurrence search in the actual review package, followed by actual hashing above.
review_for={'A':'independent_review','R':'independent_review','J':'joint_correction_review','S':'semantic_geometry_review','P':'proof_inquiry_review','U':'uncertainty_inquiry_review','G':'grounding_provenance_review','D':'decision_representation_review','C':'collective_continuation_review','O':'occurrence_warrant_review'}
current=[]
for k,d in review_for.items():
 rec=next(x for x in records if x['id']==k); hits=[]
 for f in (ROOT/BASE/d).glob('*'):
  if f.suffix in ['.json','.md'] and rec['sha256'] in f.read_text(errors='replace'):hits.append(str(f.relative_to(ROOT)))
 current.append(dict(id=k,actual_report_sha256=rec['sha256'],review_package=d,matching_digest_records=hits,current_review_binding_found=bool(hits)))
obj=dict(schema='t20.cross-front-synthesis.sources.v1',generated_utc=datetime.now(timezone.utc).isoformat(),sources=records,upstream_identity_checks=anc,review_currentness=current,scope='Direct chapter/report reading and identity checks only; no inherited mathematical replay, primary-text authentication or new kernel run')
(OUT/'SOURCE_BINDINGS.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'sources':len(records),'upstream_checks':len(anc),'upstream_nonmatches':[x for x in anc if x['status']!='match'],'reviews_without_current_binding':[x for x in current if not x['current_review_binding_found']]},indent=2))
