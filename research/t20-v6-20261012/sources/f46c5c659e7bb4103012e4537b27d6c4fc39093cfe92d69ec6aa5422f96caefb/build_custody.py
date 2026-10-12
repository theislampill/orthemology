from pathlib import Path
from hashlib import sha256,sha1
from datetime import datetime,timezone
import json,re,unicodedata
root=Path(__file__).parent
workspace=root.parent
s=(root/'sources/intisar.txt').read_text()
for name,start,end in [('intisar44-49.txt','(الكتاب/43)','(الكتاب/49)'),('intisar265-276.txt','(الكتاب/264)','(الكتاب/276)')]:
 a=s.index(start)+len(start);b=s.index(end,a)+len(end)
 (root/'sources'/name).write_text(s[a:b].strip()+'\n')
paths=[
 'basic-recognition-correction-20261009/REPORT.md',
 'basic-recognition-correction-20261009/inputs/CP20_REPORT.md',
 'basic-recognition-correction-20261009/inputs/CP19__necessary-truth-operative-basing-20261009__REPORT.md',
 'basic-recognition-correction-20261009/inputs/CP19__recognition-operative-content-20261009__REPORT.md',
 'basic-recognition-correction-20261009/inputs/CP03__t20-next-frontier-20261008__fitrah-warrant-bridge__PRIMARY_VERIFICATION.md',
 'evidence-withdrawal-warrant-20261009/REPORT.md',
 'evidence-withdrawal-warrant-20261009/sources/dar014.txt',
 'source-audit-revision-20261010/RESULT.md',
 'source-audit-revision-semantics-20261010/OCCURRENCE_INFERENCE.md',
 'noetic-correction-semantics-20261009/REPORT.md',
 'noetic-correction-semantics-20261009/SOURCE_BINDINGS.json',
 'intrinsic-representation-dependency-20261010/REPORT.md',
 'intrinsic-representation-dependency-20261010/LOCAL_SHIP_APPLICATION.md',
 't20-continuation-20261008/source-dependencies/PIN_BINDINGS.json',
 't20-continuation-20261008/source-dependencies/readbacks/atomics/skill/references/sound-reason-epistemology.md',
 'noetic-correction-semantics-20261009/sources/atomics/skill/references/procedures/P1-fitrah-restoration.md',
 'noetic-correction-semantics-20261009/sources/atomics/skill/references/tactics/M1-self-refutation.md',
 'user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/post-merge-pmr001-source/FITRAH_REMINDER_RESTORATION_SOURCE_FINDING_PMR001.md',
]
def binding(p):
 b=p.read_bytes();return {'path':str(p.relative_to(workspace)),'bytes':len(b),'sha256':sha256(b).hexdigest(),'git_blob_sha1':sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
(root/'INPUT_BINDINGS.json').write_text(json.dumps({'recorded_utc':datetime.now(timezone.utc).isoformat(),'inputs':[binding(workspace/p) for p in paths]},indent=2)+'\n')
reads={
 'primary_work':{'author':'Ibn Taymiyya','title':'al-Intisar li-ahl al-athar (published under Naqd al-mantiq)','editor':'Abd al-Rahman ibn Hasan Qaid','edition':'third 1440/2019; first for Dar Ibn Hazm','publishers':['Dar Ataat al-Ilm','Dar Ibn Hazm'],'isbn':'978-9959-857-87-3','edition_verification':'PDF title/copyright pages 1 and 2 visually inspected','transcription_url':'https://islamcontent.com/ar/content/19669','pdf_url':'https://islamcontent.com/storage/contents/19669/ar-alaintisar-liahl-alathr.pdf','same_edition_witnesses':True,'independent_manuscript_collation':False,'continuous_transcription_read':['printed 44-49','printed 265-276'],'selective_context':['printed 37-40','first authorial paragraph on printed 50','editor introduction on title/attribution, not whole introduction'],'visual_controls':{'pdf_one_based':[1,2,3,4,5,100,102,320,321,326,327,328,329,330,331],'focal_printed':[45,47,265,266,271,272,273,274,275,276]},'apparatus_limit':'Printed 47 edits base-witness la yuhiss to yuhiss. Report does not depend on that emended clause; succeeding independent sentence about known effective inference supports the bounded point. Printed274 and its scan both read taqillu muqaddimatuhu in a clause apparently in tension with the following comparison. No emendation, manuscript judgement or premise-count theorem is adopted. Hadith authentication and historical polemical claims not independently checked.','reading_credit':'New direct bounded verification relative to inspected files; no first-programme or whole-work claim.'},
 'inheritance':{'reports_read':'Named recognition/currentness/factive-ground/withdrawal/noetic/representation reports as identified in INPUT_BINDINGS; source-audit RESULT read for result and prior-ownership context only, not full probability proof; occurrence addendum read in full.','native_substrate_scope':'sound-reason sections 1-2 and 5 plus nearby source/provenance context; P1 source-floor, stages 2-5, table, readiness, failure/routing controls; M1 selective operating context. Not whole DAEE source corpus.','dar_scope':'Already-read electronic014 antecedent-acquaintance and acquisition/self-appraisal sequence reread selectively. No new Dar whole-unit credit.','prior_search':'PRIOR_SOURCE_SEARCH.json is a name/phrase screen of accessible local md/json/txt/yaml files, not all archived or remote sources. No exact-locus prior read found.'},
 'access_limits':[{'url':'https://library.oapen.org/bitstream/20.500.12657/37977/1/9789004412866_webready_content_text.pdf','result':'HTTP403; no reading credit, no repeated attempt'},{'url':'https://brill.com/display/book/9789004412866/BP000005.xml','result':'web internal error; no reading credit'}],
 'modern_reconstruction_limit':'El-Tobgui wording examined through the saved substrate and prior finding; original 2020 printed 271 was not retrieved. No new claim of his exact intended global/local interpretation.',
 'rejected_candidate':'recognition-correction-transfer-20261010/DISPOSITION.md records excluded Barrett-Keil screen; no empirical result is used.',
 'distribution':'Full source bodies, linked PDF, and page images are research intermediates. Share REPORT and provenance metadata separately; do not redistribute raw witnesses in a user-facing package.'
}
(root/'SOURCE_READS.json').write_text(json.dumps(reads,ensure_ascii=False,indent=2)+'\n')
# Verify fixed frozen source identities against the inherited ledgers.
expected={
 paths[14]:'d7fa4425d014225940cbbbe86983f8d9a3dc3da5',
 paths[15]:'3d84b7a94a1fe47714588e2b2eee9f8f6cecab83'
}
checks=[]
for p,e in expected.items():
 actual=binding(workspace/p)['git_blob_sha1'];checks.append({'path':p,'expected':e,'actual':actual,'passed':actual==e})
assert all(c['passed'] for c in checks)
(root/'VERIFICATION.json').write_text(json.dumps({'scope':'Source identity and custody only; no theorem, actual cognition, or current-branch verification','checks':checks},indent=2)+'\n')
files=[binding(p) for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
(root/'MANIFEST.json').write_text(json.dumps({'recorded_utc':datetime.now(timezone.utc).isoformat(),'scope':'Bounded source-grounded local rational corrigibility; no protected edits or integration','files':files},indent=2)+'\n')
print('bound',len(paths),'inherited files;',len(files),'output files; frozen identities passed')
