from pathlib import Path
import json, hashlib, datetime
root=Path(__file__).resolve().parent.parent
out=Path(__file__).resolve().parent
m='wise-reason-asymmetry-20261010/sources/'
rows=[
 ('E01','Miftāḥ 2:969',m+'MIFTAH_2_964_971.txt','لأن الكمال محبوب للعالم به، والنقص مبغوض له','Perfection and defect are presented as grounds of love and aversion, rather than only labels for the result.'),
 ('E02','Miftāḥ 2:970',m+'MIFTAH_2_964_971.txt','وما ذاك إلا لكمال الأول ونقصان الثاني.','Explicit explanatory direction in the author’s response.'),
 ('E03','Miftāḥ 2:1128',m+'MIFTAH_2_1123_1135.txt','فأنكر على الطائفتين معا أصحاب التفسير الثالث، وقالوا: الصواب الذي دلت عليه النصوص:','The preferred interpretation of injustice is distinguished from the preceding rejected accounts.'),
 ('E04','Miftāḥ 2:1129',m+'MIFTAH_2_1123_1135.txt','ولا يعذب بما لم تكسب يداه ولم يكن سعى فيه','Acquisition and participation provide the report’s relational content.'),
 ('E05','Miftāḥ 2:1129',m+'MIFTAH_2_1123_1135.txt','دل على أن الظلم المنفي هو أن يعذبهم بغير جرم، وأنه إنما عذبهم بجرمهم وظلمهم','The author explicitly identifies the denied injustice and the recipient’s own offence.'),
 ('E06','Miftāḥ 2:1130',m+'MIFTAH_2_1123_1135.txt','أي: لا يعاقب العبد بغير إساءته، ولا يحرمه ثواب إحسانه','Corroboration independent of the difficult good-deeds condition at 1129.'),
 ('E07','Miftāḥ 2:1133',m+'MIFTAH_2_1123_1135.txt','لا لكونه قادرا عليهم وهم ملكه، بل لاستحقاقهم','Power and ownership alone do not explain punitive justice.'),
 ('E08','Miftāḥ 2:1138',m+'MIFTAH_2_1135_1143.txt','وتحريمه ما حرمه على نفسه متضمن لبغضه لذلك، وكراهته له، وأنه لا يفعله.','Self-prohibition supplies the aversion bridge; it is not inferred from an isolated bad aspect.'),
 ('E09','Miftāḥ 2:1139',m+'MIFTAH_2_1135_1143.txt','فمحبته تعالى وكراهته للأول توجب وقوعه وامتناعه، وأما محبته وكراهته للثاني فلا توجب وقوعه ولا امتناعه.','First refers to God’s own act; second to the creature’s act as God’s product. Context was read continuously.'),
 ('E10','Miftāḥ 2:1139',m+'MIFTAH_2_1135_1143.txt','إذ لم يحب فعله الذي هو إعانتهم وتوفيقهم وخلق ذلك لهم، ولو أحب ذلك لاستلزم طاعتهم وإيمانهم.','The source itself identifies the missing enabling-own-act antecedent.'),
 ('E11','Shifāʾ e177',m+'SHIFA_e176_e177.txt','فلا يوجب القدرة والعلم وقوع الفعل ما لم تقارنهما الإرادة.','Mere power plus knowledge is not actual willing.'),
 ('E12','Shifāʾ e180',m+'SHIFA_e180_e182.txt','هذا بالنظر إلى ذات هذا وهذا وأما باعتبار إفضائه إلى ما يحب ويكره فله حكم آخر','Intrinsic/respect-specific assessment and further consequences must not be conflated.'),
 ('E13','Shifāʾ e190',m+'SHIFA_e188_e190.txt','بل أفعاله سبحانه صادرة عن حكمة بالغة لأجلها فعل كما هي ناشئة عن أسباب بها فعل','For-which and through-which explanations are distinguished.'),
 ('E14','Shifāʾ e207',m+'SHIFA_e206_e210.txt','فتلك الحكمة صفته سبحانه وصفاته ليست غيرا له','Intrinsic wisdom is not a separately supplying other.'),
 ('E15','Shifāʾ e209',m+'SHIFA_e206_e210.txt','فإن الحكمة والعلة الغائية هي التي تجعل المريد مريدا فإنه إذا علم بمصلحة الفعل ونفعه وغايته انبعثت إرادته إليه','Known fitting ends have an operative practical role; this is not a sufficient explanation of every particular representation.'),
 ('E16','Shifāʾ e215',m+'SHIFA_e211_e216.txt','وإذا فعل ما يكرهه لم يفعله إلا لإفضائه إلى ما يحب وإن كان مكروها في نفسه','Strongest nearby respect/greater-good rival; does not override an independently established own self-prohibition.'),
 ('E17','Majmūʿ 16:305','particular-determination-semantics-20261010/selections/MAJMU16_300_305.txt','وتلك الصورة العلمية الإرادية حدثت بعد أن لم تكن . وهي حادثة بمشيئته وقدرته','Representation origination remains a separate explanandum.'),
]
records=[]
text=['# Exact received evidence for the independent review','','These are bounded excerpts, not substitutes for the continuous readings recorded in `READING_RECORD.json`. Every excerpt below was checked as an exact substring of the hash-bound received file. No emendation or new witness credit is implied.','']
for ident,loc,path,quote,role in rows:
 body=(root/path).read_text(); assert quote in body, (ident,quote)
 records.append({'id':ident,'locator':loc,'path':path,'source_sha256':hashlib.sha256((root/path).read_bytes()).hexdigest(),'quote':quote,'exact_substring_match':True,'role':role})
 text.extend([f'## {ident} {loc}',f'Source: `{path}`','',quote,'',role,''])
(out/'EVIDENCE.md').write_text('\n'.join(text))
(out/'EVIDENCE_CHECK.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records},ensure_ascii=False,indent=2)+'\n')
reading={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reviewer':'independent scoped native reviewer; not author or participating root',
 'target':'wise-reason-asymmetry-20261010/REPORT.md',
 'primary_received_direct_reading':[
 {'source':'Miftah','file_prefix':m,'continuous_ranges':['2:872–878','2:964–971','2:1114–1119','2:1123–1143'],'apparatus':'all displayed apparatus in selected edited-text extracts; no new scan collation'},
 {'source':'Shifa','file_prefix':m,'continuous_ranges':['e173–182','e188–190','e206–216'],'truncation_repair':'The combined display lost part of e209; the complete e209 was separately redisplayed and read. e180 overlaps two selections; e176–177 was read as part of e173–179. No overlap is counted twice.','pagination':'received electronic markers, not independently certified print pages'},
 {'source':'Majmu','path':'particular-determination-semantics-20261010/selections/MAJMU16_300_305.txt','range':'16:300–305','limit':'Received markup residue was preserved, not treated as source prose.'}],
 'secondary_direct_reading':[
 {'path':'wise-reason-asymmetry-20261010/REPORT.md','scope':'complete'},
 {'path':'wise-reason-asymmetry-20261010/INPUT_BINDINGS.json','scope':'complete'},
 {'path':'wise-reason-asymmetry-20261010/SOURCE_READS.json','scope':'complete'},
 {'path':'wise-reason-asymmetry-20261010/INHERITANCE_CHECK.json','scope':'complete'},
 {'path':'wise-reason-asymmetry-20261010/MANIFEST.json','scope':'complete'},
 {'path':'wise-reason-root-20261010/FIDELITY_CHECK.md','scope':'complete; participant check, not independent source evidence'},
 {'path':'particular-determination-semantics-20261010/REPORT.md','scope':'complete'},
 {'path':'intrinsic-representation-dependency-20261010/REPORT.md','scope':'opening through step A of section 4; not full reading'},
 {'path':'constructive-foundation-selection-20261009/WISE_FRONTIER_NOTE.md','scope':'complete'},
 {'path':'constructive-foundation-selection-20261009/inputs/CP20/wise-particular-determination-return-20261009/REPORT.md','scope':'opening through first part of regress arguments; targeted inheritance control'},
 {'path':'constructive-foundation-selection-20261009/inputs/CP23/intrinsic-normative-reasons-20261009/REPORT.md','scope':'targeted result and prior-work controls plus practical-authority/punishment argument; combined display was truncated, so no full-read credit'},
 {'path':'original-normative-authority-20261009/inputs/MIFTAH_CONTINUOUS_NOTES.md','scope':'targeted overlap search and displayed notes at 1043–1147, with separate complete 1138–1141 bounded-reread note; no full-notebook reading'}],
 'identity_only_not_reading':'Other input files in ORIGINALS_BEFORE.json were hash-checked and/or used for a bounded keyword search; their inclusion is not full-content reading credit.',
 'excluded_credit':['No independent historical witness','No new primary acquisition','No independent validation of initial Word decoding','No authentication of every historical report','No root e183–187 or e191–193 credit','No foundational reappraisal','No metaphysical truth inferred from textual agreement'],
 'mutation_scope':'Only wise-reason-independent-review-20261010 is written.'}
(out/'READING_RECORD.json').write_text(json.dumps(reading,ensure_ascii=False,indent=2)+'\n')
print('Saved 17 exact evidence checks and scoped reading record.')
