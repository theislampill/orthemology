from pathlib import Path
import json,hashlib,re
D=Path('scoped-original-authority-20261010')
def ident(p,role=None):
 p=Path(p);b=p.read_bytes();d={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 if role:d['role']=role
 return d
def put(n,v): (D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
old=json.loads(Path('original-normative-authority-20261009/INPUT_BINDINGS.json').read_text())
checks=[]
for r in old['records']:
 p=Path(r['path']);m=ident(p);checks.append({**m,'expected_sha256':r['sha256'],'matches':m['sha256']==r['sha256']})
put('INHERITED_BINDING_CHECK.json',{'scope':'Exact files recorded by controlling report; not repository integration verification','checks':checks,'all_match':all(x['matches'] for x in checks)})
roles={
'original-normative-authority-20261009/REPORT.md':'Controlling report read in full',
'original-normative-authority-20261009/INPUT_BINDINGS.json':'Controlling source and input references; all recorded file hashes checked',
'original-normative-authority-20261009/SOURCE_READS.json':'Inherited acquisition and reading boundaries',
'original-normative-authority-20261009/CURRENTNESS.json':'Inherited bounded prior-history result; not rerun repository-wide',
'original-normative-authority-20261009/inputs/SCOPED_AUTHORITY_APPRAISAL.md':'Full CP02 appraisal',
'original-normative-authority-20261009/inputs/PRIMARY_QUOTATION_CHECK.md':'Full prior primary quotation check',
'original-normative-authority-20261009/inputs/HISTORICAL_PARAGRAPH_BINDINGS.json':'Full retained T17/T19 paragraph content; underlying DOCX not reopened',
'original-normative-authority-20261009/inputs/MIFTAH_CONTINUOUS_NOTES.md':'Selected entries on872-892,1058-1102,1118-1172 and keyword locators; no whole-note fresh reading',
'constructive-foundation-selection-20261009/inputs/CP23/intrinsic-normative-reasons-20261009/REPORT.md':'Full inherited due-relation appraisal',
'constructive-foundation-selection-20261009/inputs/CP23/affirmative-wise-determination-20261009/REPORT.md':'Selected full sections3-5 plus adjoining source/currentness context',
'directive-normative-qualification-20261009/REPORT.md':'Full inherited actual-address and added-goodness appraisal',
 'token-force-clarification-20261009/REPORT.md':'Full inherited actual-token-force appraisal',
 'token-force-clarification-20261009/inputs/SCOPED_OWNERSHIP_ADDENDUM.md':'Full retained-control/permission/grant distinction',
'wise-reason-asymmetry-20261010/REPORT.md':'Full inherited own-act efficacy and transferred-guilt application',
'wise-reason-asymmetry-20261010/INHERITANCE_CHECK.json':'Historical Word/body hash crosscheck',
'intrinsic-succession-origin-20261010/REPORT.md':'Full inherited particular/collective completion and successive-act boundary',
'wise-reason-root-20261010/READING_NOTE.md':'Full earlier root source-scope note'
}
put('INPUT_BINDINGS.json',{'date_utc':'2026-10-10','scope':'Read-only inherited inputs; no assertion of repository currentness beyond these received files','records':[ident(p,r) for p,r in roles.items()]})
put('SOURCE_READS.json',{
'source':{'author':'Ibn al-Qayyim','title':'Miftah dar al-saada','official_url':'https://ibnelqayem.com/ar/media/download/86','edition_identity':'Inherited exact-witness binding: Abd al-Rahman ibn Hasan ibn Qaid, third1440/2019, Dar Ataat al-Ilm/Dar Ibn Hazm; no fresh scan imprint check','word':ident('original-normative-authority-20261009/sources/miftah.doc'),'inherited_body':ident('original-normative-authority-20261009/sources/decoded-unvocalized.txt')},
'method':'Reuse inherited bounded UTF16LE body decode; select explicit trailing (volume/page) markers, all marker identities unique; normalize only control linebreaks, no Arabic emendation. Not a new general Word parser.',
'continuous_displayed_ranges':['1:12-23','2:872-892','2:1067-1091','2:1121-1143','2:1148-1156'],
'principal_complete_units':[
 {'pages':'1:17-18 opening','unit':'Standalone creation-and-command argument from وأيضا فإنه سبحانه له الخلق والأمر through ونظائر هذا في القرآن كثيرة; earlier/following examples provide context only'},
 {'pages':'2:878 closing-881 opening','unit':'Rational/fitting source-worship argument, Qur2:21-22 and YaSin illustration with adjacent object-of-worship contrasts'},
 {'pages':'2:886-891 before فصل','unit':'Moral-wisdom/non-abandonment argument and connected epistemic/revelatory comparison; next-act taxonomy at892 is context only'},
 {'pages':'2:1067-1090 opening','unit':'Complete numbered replies41-47; prior reply at1067 opening and reply48 after1090 opening are boundary/context only'},
 {'pages':'2:1121-1143 before reply62','unit':'Complete reply61: obligation, justice and self-obligation; reply62 after heading is context only'},
 {'pages':'2:1136-1142 plus1143 opening','unit':'Full self-obligation development to end of reply61, own-act digression and return at1141 retained'},
 {'pages':'2:1149-1156 before وأما ما ذكره الفلاسفة','unit':'General epistemic-need subargument within reply64; no claim to whole reply64 or book section'}
],
'local_selected_files':[ident(p) for p in sorted((D/'sources').glob('*.txt'))],
'reused_primary_extract':ident('original-normative-authority-20261009/sources/miftah-1074-1094.txt','Current displayed through1091; later pages not credited'),
'attribution_controls':['1123 positions reported;1124 preferred middle account;1136-1142 development is endorsed, not opponent doctrine','1133-34 concerns undeserved punishment and positively grounds worship; does not deny command title','1138 note attributes source to Majmu18:150 and1141 note to18:149; those loci were not directly read here and earn no independent witness credit','Quoted traditions and scriptural claims retain inherited status; no fresh hadith-chain investigation','Modern apparatus, weak report notices, and defective variants are not treated as authorial endorsements or silently repaired'],
'root_overlap':{'source':'Parent collaboration message on2026-10-10','reported_ranges':['2:1123-1135','2:1135-1143','2:1074-1083'],'role':'Participating root checking, not independent peer review or historical witness','scope_confirmed':'Conditional creature response indexes recipient standing, not superior lawgiver or donor of essential perfection; no temporal-new-norm inference'},
'prior_credit':'All normative doctrines are inherited. No first-programme reading, first argument discovery or independent witness credit;1:12-23 prior page-specific coverage was not independently established, so no first-reading credit is requested.',
'failed_access':[{'tool':'web.open','url':'https://ibnelqayem.com/ar/media/download/86','result':'URL inaccessible via this tool; local exact-bound Word witness available and hash verified. No global source-unavailability inference.'}],
'rights_boundary':'Full Word/body and edited textual extracts are local research intermediates excluded from compact authored manifest.'
})
paths=[str(p) for p in Path('.').glob('*/*.md') if not any(x in str(p) for x in ['user-checkpoints','scoped-original-authority'])]
put('PRIOR_STATUS.json',{
 'scope':'Bounded relevant-record check, not repository-wide absence or global philosophical novelty',
 'prior_results':[{'claim':'Owed practical allegiance and retained-control principle','owner':'CP02 and original-normative-authority-20261009'},{'claim':'Source testimony of obligation need not await independent title proof','owner':'T19 P164-165 retained paragraph bindings'},{'claim':'Actual address adds relational goodness, with obligation/title/force separate','owner':'directive-normative-qualification-20261009'},{'claim':'Miftah879 worship from benefaction;1067-76 directive formation;1133-34 desert and positive worship','owner':'MIFTAH_CONTINUOUS_NOTES selected entries, with1133-34 also wise-reason-asymmetry-20261010'},{'claim':'Self-obligation, own-act love efficacy, prior essential perfection','owner':'MIFTAH_CONTINUOUS_NOTES1133-1147;wise-reason-asymmetry-20261010'},{'claim':'Actual creature response can matter without donating essential perfection','owner':'CP23 affirmative-wise-determination-20261009 sections3-4'},{'claim':'Earlier intrinsic acts can matter without supplying original bearer; no token individuation licence','owner':'intrinsic-succession-origin-20261010'}],
 'search':{'method':'Regex search of current top-level research markdown files, plus direct inherited report and selected-note reads','terms':'self-imposition/self-obligation; recipient claim/right; promise/undertaking with normative terms; foreign obligation; Arabic كتب/حرم على نفسه','screened_files':paths,'matches_path':str(D/'inputs/PRIOR_ADJACENT_SEARCH.json'),'credit':'Search only for most screened files; not full reading'},
 'current_increment':'Source-contrast application to bounded selection rival; conditional beneficiary-right application to outside-legislator/foreign-perfection inference. Not found as exact worked applications in checked relevant records; ingredients inherited.',
 'not_achieved':'No new creature-directed selection title; no new temporal norm-creation or intrinsic-act individuation conclusion',
 'protected_edits':'none'
})
# Capture the referenced attributed dependence explicitly in the authored text.
p=D/'REPORT.md';t=p.read_text();t=t.replace('The modern apparatus is distinguished from the medieval author.','The modern apparatus is distinguished from the medieval author. The 1138 note attributes its source to Ibn Taymiyya’s Majmūʿ 18:150, and the 1141 note refers to 18:149; neither locus was directly read in this operation, so these are attributed dependencies, not new independent witnesses. The parent separately reports overlapping readings of 1123–1135, 1135–1143 and 1074–1083; this is participating source checking, not independent review.')
p.write_text(t)
manifest_files=['REPORT.md','INPUT_BINDINGS.json','SOURCE_READS.json','PRIOR_STATUS.json','INHERITED_BINDING_CHECK.json']
put('MANIFEST.json',{'scope':'Compact authored evidence only; primary research intermediates excluded','files':[ident(D/p) for p in manifest_files],'integration':'none','closure':'none'})
print('WROTE',len(manifest_files),'authored records; all11 controlling input matches:',all(x['matches'] for x in checks))
print('REPORT words:',len((D/'REPORT.md').read_text().split()))
