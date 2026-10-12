from pathlib import Path
from hashlib import sha256, sha1
from datetime import datetime, timezone
import json

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
checks=[]
bindings=[]
def digest(p): return sha256(p.read_bytes()).hexdigest()
def check(name, ok, detail=None):
    row={'check':name,'passed':bool(ok)}
    if detail is not None: row['detail']=detail
    checks.append(row)
def bind(path, scope, role):
    p=ROOT/path
    b=p.read_bytes()
    bindings.append({'path':path,'bytes':len(b),'sha256':sha256(b).hexdigest(),'actual_read_scope':scope,'role':role})

expected={
'joint-disclosure-warrant-20261011/REPORT.md':'673c3a43b5908f353a59f165963c48e422dbde96070a4b81a0d9167315d1cfe2',
'joint-disclosure-warrant-20261011/MANIFEST.json':'082c2afe31cad9cd582f982b873fd1b0c4a1bc0b0f4f5f6f0ec60c1d118ebf3b',
'message-established-accountability-20261011/REPORT.md':'3de6fc30e0084b321c7d1f5651f949d66cfd2ddd050234aa8bcf1c5d6068e21a',
'message-established-accountability-20261011/FILES.sha256':'72d029b6666cd1fb2878abce2913ac79f202d4867e7a157bb1ee521509f1fa63'}
for p,h in expected.items():
    check('frozen_identity',digest(ROOT/p)==h,p)
    bind(p,'Complete report or manifest read','Review target or frozen custody')
J=ROOT/'joint-disclosure-warrant-20261011'
for r in json.loads((J/'MANIFEST.json').read_text()):
    p=J/r['path']; b=p.read_bytes()
    check('joint_manifest_entry',len(b)==r['bytes'] and sha256(b).hexdigest()==r['sha256'],r['path'])
for r in json.loads((J/'LOCAL_INPUT_BINDINGS.json').read_text()):
    b=(J/r['path']).read_bytes(); p=ROOT/r['source_path']
    check('joint_predecessor_copy',b==p.read_bytes() and sha256(b).hexdigest()==r['sha256'],r['source_path'])
for r in json.loads((J/'REMOTE_INPUT_BINDINGS.json').read_text()):
    b=(J/r['path']).read_bytes(); git=sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check('pinned_inherited_note_identity',sha256(b).hexdigest()==r['sha256'] and git==r['expected_git_blob_sha1'],r['path'])
js=json.loads((J/'SOURCE_READS.json').read_text())
u=(ROOT/js['primary']['unit']['path']).read_bytes(); par=(ROOT/js['primary']['parent_text']['path']).read_bytes()
check('dar_unit_contiguous',u in par)
for key in ['unit','parent_text','parent_html']:
    r=js['primary'][key]; check('dar_source_identity',digest(ROOT/r['path'])==r['sha256'],r['path'])
M=ROOT/'message-established-accountability-20261011'
for line in (M/'FILES.sha256').read_text().splitlines():
    h,p=line.split('  ',1);check('accountability_manifest_entry',digest(M/p)==h,p)
ms=json.loads((M/'SOURCE_RECORD.json').read_text())
for r in ms['raw_source_bindings']:
    check('accountability_parent_identity',digest(ROOT/r['path'])==r['sha256'],r['path'])
for r in ms['sources']:
    x=r['selection'];check('accountability_selection_identity',digest(ROOT/x['path'])==x['sha256'],x['path'])
for r in json.loads((M/'INPUT_BINDINGS.json').read_text())['predecessors']:
    check('accountability_predecessor_identity',digest(ROOT/r['path'])==r['sha256'],r['path'])
s=(ROOT/'original-normative-authority-20261009/sources/decoded-unvocalized.txt').read_text()
a=s.index('(2/871)')+len('(2/871)');b=s.index('(2/878)',a)+len('(2/878)')
sel=s[a:b].replace('\x0b','\n').replace('\x01','')
check('miftah_selection_extraction',sel.encode()==(M/'research-intermediates/MIFTAH_2_872_878.txt').read_bytes())
s=(ROOT/'particular-determination-semantics-20261010/sources/shifa002.txt').read_text()
a=s.index('ص -190-');b=s.index('ص -192-',a)
check('shifa_selection_extraction',s[a:b].encode()==(M/'research-intermediates/SHIFA_e190_e191.txt').read_bytes())
q=json.loads((M/'research-intermediates/quran28_44_50.json').read_text())
check('quran_complete_order',len(q)==7 and [(r['surah'],r['ayah']) for r in q]==[(28,n) for n in range(44,51)] and all(r['text'] for r in q))
r=json.loads((ROOT/'joint-disclosure-root-reading-20261011/BINDING.json').read_text())
check('joint_participating_binding',digest(ROOT/r['source_path'])==r['sha256'])
for r in json.loads((ROOT/'message-accountability-root-reading-20261011/BINDINGS.json').read_text())['files']:
    check('accountability_participating_binding',digest(ROOT/r['path'])==r['sha256'],r['path'])

for p in ['SOURCE_READS.json','LOCAL_INPUT_BINDINGS.json','REMOTE_INPUT_BINDINGS.json','VERIFICATION.json']:
    bind('joint-disclosure-warrant-20261011/'+p,'Full structured metadata read or mechanically checked','Author custody; no philosophical validation')
for p in ['INPUT_BINDINGS.json','SOURCE_RECORD.json','READING_LEDGER.json','VERIFICATION.json']:
    bind('message-established-accountability-20261011/'+p,'Full structured metadata read or mechanically checked','Author custody; no philosophical validation')
for p in sorted((J/'inputs').glob('L*')):
    if p.name.startswith('L13'): scope='Edition and inherited read metadata only; not a complete fresh primary reread'
    else: scope='Complete report or participating-root record read'
    bind(str(p.relative_to(ROOT)),scope,'Closest inherited comparison or participating source control')
for p,scope in [
('joint-disclosure-warrant-20261011/inputs/DAR9_READING_LOG.md','Methods and first-pass01–03 including first-pass02 two repairs/copyist; no full-log reading claim'),
('joint-disclosure-warrant-20261011/inputs/DAR8_PRIOR_NOTES.md','Complete Segment A; opening Segment B and rational/scriptural provenance passage; no full-note reading claim'),
('joint-disclosure-warrant-20261011/private_sources/dar015-joint-disclosure-unit.txt','Full retained 42-line authorial unit, 16379 bytes; no print or manuscript collation'),
('message-established-accountability-20261011/research-intermediates/MIFTAH_2_872_878.txt','Full retained continuous2:872–878, apparatus distinguished; larger chapter not reread'),
('message-established-accountability-20261011/research-intermediates/SHIFA_e190_e191.txt','Full retained electronic190–191, including complete first consequence reply; longer detailed replies continue'),
('message-established-accountability-20261011/research-intermediates/quran28_44_50.json','Seven full Arabic verses28:44–50 read in order; service display metadata is data, not instructions')]:
    bind(p,scope,'Primary held source or deduplication control')
for p in [
'wise-reason-asymmetry-20261010/REPORT.md',
'constructive-foundation-selection-20261009/WISE_FRONTIER_NOTE.md',
'commissioned-content-access-test-20261009/REPORT.md',
'scoped-original-authority-20261010/REPORT.md',
'continuing-title-source-test-20261010/REPORT.md',
'responsive-demonstration-20261011/REPORT.md',
'uthaymin-question-purpose-20261011/REPORT.md',
'original-adequacy-currentness-20261011/RESULT.md',
'joint-disclosure-root-reading-20261011/READING_NOTE.md',
'joint-disclosure-root-reading-20261011/BINDING.json',
'message-accountability-root-reading-20261011/READING_NOTE.md',
'message-accountability-root-reading-20261011/BINDINGS.json']:
    bind(p,'Complete report, note or binding read','Closest predecessor or participating-root source control')
a=s.index('ص -192-');b=s.index('ص -193-',a);frag=s[a:b].encode()
bindings.append({'path':'particular-determination-semantics-20261010/sources/shifa002.txt','bytes':(ROOT/'particular-determination-semantics-20261010/sources/shifa002.txt').stat().st_size,'sha256':digest(ROOT/'particular-determination-semantics-20261010/sources/shifa002.txt'),'actual_read_scope':'Only electronic192 freshly read as adjoining context; completes paragraph interrupted by e191 boundary. Detailed reply sequence continues beyond this read.','selection_character_start':a,'selection_character_end_exclusive':b,'selection_sha256':sha256(frag).hexdigest(),'role':'Adjacent context in same held witness, no new witness'})
now=datetime.now(timezone.utc).isoformat()
(OUT/'BINDINGS.json').write_text(json.dumps({'recorded_utc':now,'inheritance_pin':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','reviewer':'review_disclosure_purpose_arguments','authority':'Bounded independent argument/source review only; no integration or closure','independence':'Reviewer did not author either target. Root participating readings are not independent witnesses. Held source bytes are shared evidence.','files':bindings,'credit':'New independent review only. No new primary discovery, historical authentication, whole-book read, source collation, or duration claim.'},indent=2,ensure_ascii=False)+'\n')
passed=all(x['passed'] for x in checks)
(OUT/'VERIFICATION.json').write_text(json.dumps({'verified_utc':now,'passed':passed,'scope':'Byte custody, extraction and range/order checks only. No proof count, checksum or review agreement supplies philosophical premises.','checks':checks},indent=2,ensure_ascii=False)+'\n')
for row in checks:
    if not row['passed']: print('FAIL',row)
print(json.dumps({'passed':passed,'scope':'Custody checks only'}))
raise SystemExit(0 if passed else 1)
