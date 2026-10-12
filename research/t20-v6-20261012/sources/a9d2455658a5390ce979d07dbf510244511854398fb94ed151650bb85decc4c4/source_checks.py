#!/usr/bin/env python3
"""Portable source-witness/custody controls, not argument certification."""
from pathlib import Path
import argparse,hashlib,json
P=Path;ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=P,required=True);args=ap.parse_args();R=P(__file__).resolve().parent;out=args.output_dir.resolve()
if out==R or R in out.parents:raise SystemExit('Output must be outside bundle.')
out.mkdir(parents=True,exist_ok=True);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,value,detail=None):
 row={'name':name,'passed':bool(value)}
 if detail is not None:row['detail']=detail
 checks.append(row)
 if not value:raise RuntimeError(name+': '+str(detail))
C=json.loads((R/'SOURCE_CUSTODY.json').read_text());omitted={r['portable_exclusion_path']:r for r in C['deliberate_omissions']};maps={r['original_path']:r for r in C['portable_input_mappings']}
pins={
 'joint-disclosure-warrant-20261011/REPORT.md':'673c3a43b5908f353a59f165963c48e422dbde96070a4b81a0d9167315d1cfe2',
 'joint-disclosure-warrant-20261011/MANIFEST.json':'082c2afe31cad9cd582f982b873fd1b0c4a1bc0b0f4f5f6f0ec60c1d118ebf3b',
 'message-established-accountability-20261011/REPORT.md':'3de6fc30e0084b321c7d1f5651f949d66cfd2ddd050234aa8bcf1c5d6068e21a',
 'message-established-accountability-20261011/FILES.sha256':'72d029b6666cd1fb2878abce2913ac79f202d4867e7a157bb1ee521509f1fa63',
 'disclosure-purpose-independent-review-20261011/REVIEW.md':'fb0ad02ec6ae012cf93be18b3ca6dcb1a1a5171c24e93c3d0263cd97d039666b'}
for path,d in pins.items():check('frozen source/review pin',h(R/path)==d,path)
retained=excluded=0
J=R/'joint-disclosure-warrant-20261011'
for row in json.loads((J/'MANIFEST.json').read_text()):
 rel=str((J/row['path']).relative_to(R));p=R/rel
 if rel in omitted:
  check('explicit original manifest omission',not p.exists() and omitted[rel]['sha256']==row['sha256'] and omitted[rel]['bytes']==row['bytes'],rel);excluded+=1
 else:
  check('retained original manifest entry',p.stat().st_size==row['bytes'] and h(p)==row['sha256'],rel);retained+=1
for base in ['message-established-accountability-20261011','disclosure-purpose-independent-review-20261011']:
 for line in (R/base/'FILES.sha256').read_text().splitlines():
  d,f=line.split('  ',1);check('retained SHA256 manifest entry',h(R/base/f)==d,base+'/'+f)
for row in C['portable_input_mappings']:
 p=R/row['portable_path'];check('portable predecessor binding',p.stat().st_size==row['bytes'] and h(p)==row['sha256'],row['original_path'])
for row in json.loads((J/'LOCAL_INPUT_BINDINGS.json').read_text()):
 check('joint snapshot maps to original identity',maps[row['source_path']]['sha256']==row['sha256'] and h(J/row['path'])==row['sha256'],row['source_path'])
for row in json.loads((R/'message-established-accountability-20261011/INPUT_BINDINGS.json').read_text())['predecessors']:
 check('accountability portable predecessor coverage',maps[row['path']]['sha256']==row['sha256'],row['path'])
for row in C['included_witnesses']:
 p=R/row['portable_path'];check('bounded witness bytes',p.stat().st_size==row['bytes'] and h(p)==row['sha256'],row['portable_path'])
for row in C['deliberate_omissions']:check('excluded source stays excluded',not (R/row['portable_exclusion_path']).exists(),row['portable_exclusion_path'])
sr=json.loads((R/'message-established-accountability-20261011/SOURCE_RECORD.json').read_text());mx=json.loads((R/'source-witnesses/MIFTAH_authorial_excerpts.json').read_text());m=''.join(s['text'] for s in mx['segments']);sh=(R/'message-established-accountability-20261011/research-intermediates/SHIFA_e190_e191.txt').read_text()
check('Miftah derivation bound to unchanged selected witness',mx['source_selection_sha256']==sr['sources'][0]['selection']['sha256'])
for row in mx['segments']:check('derived authorial segment hash',hashlib.sha256(row['text'].encode()).hexdigest()==row['utf8_sha256'])
check('modern critical apparatus not reproduced in derived paragraphs','_________' not in m)
check('original locator typo remains unmodified','[الإسراء: 23]' in m)
for a in sr['load_bearing_anchors']:
 text=m if a['extract'].startswith('MIFTAH') else sh;check('exact source anchor preserved',a['exact_anchor'] in text,{'locator':a['locator'],'role':a['role']})
qx=json.loads((R/'source-witnesses/QURAN_28_44_50_text.json').read_text());q=qx['verses'];check('seven complete sequential verse identities',[(v['surah'],v['ayah']) for v in q]==[(28,n) for n in range(44,51)] and all(v['text'] for v in q));check('Quran projection bound to original response',qx['source_response_sha256']==sr['sources'][2]['selection']['sha256']);check('service metadata excluded',all(set(v)=={'surah','ayah','text'} for v in q))
for ayah,phrases in [(46,['رحمة','لتنذر']),(47,['لولا أرسلت إلينا رسولا']),(48,['فلما جاءهم الحق'])]:
 text=next(v['text'] for v in q if v['ayah']==ayah);check('Quran contextual anchor '+str(ayah),all(p in text for p in phrases))
d=(J/'private_sources/dar015-joint-disclosure-unit.txt').read_text();check('Dar second route prior-assent anchor','وإن لم يكن قبل ذلك قد تقدم من العبد معرفة الإقرار بالصانع' in d)
review=json.loads((R/'disclosure-purpose-independent-review-20261011/BINDINGS.json').read_text());adj=[r for r in review['files'] if 'selection_character_start' in r][0];check('reviewer adjacent context exact selection hash',h(R/'source-witnesses/SHIFA_e192_reviewer_adjacent_context.txt')==adj['selection_sha256'])
check('joint participating binding uses same held source',json.loads((R/'joint-disclosure-root-reading-20261011/BINDING.json').read_text())['sha256']==h(J/'private_sources/dar015-joint-disclosure-unit.txt'))
for row in json.loads((R/'message-accountability-root-reading-20261011/BINDINGS.json').read_text())['files']:
 if row['path'].endswith('MIFTAH_2_872_878.txt'):value=row['sha256']==mx['source_selection_sha256']
 else:value=row['sha256']==h(R/row['path'])
 check('participating accountability original identity',value,row['path'])
receipt={'status':'PASS','kind':'Portable custody, exact-anchor and context-order controls only; not proof or independent philosophical validation','joint_manifest_retained_entries':retained,'joint_manifest_explicitly_omitted_entries':excluded,'bounded_witnesses':len(C['included_witnesses']),'source_anchor_count':len(sr['load_bearing_anchors']),'raw_source_and_note_gaps_explicit':True,'checks':checks,'limitations':C['portable_limits']}
(out/'SOURCE_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['checks','limitations']},indent=2))
