from pathlib import Path
import hashlib,json,re,datetime
ROOT=Path.cwd();BASE=ROOT/'owed-response-specification-20261010'
def bind(p,**rest):
 p=Path(p);data=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),**rest}
def write(name,value): (BASE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
inputs=[
 ('scoped-original-authority-20261010/REPORT.md','Full report'),
 ('original-normative-authority-20261009/REPORT.md','Full report'),
 ('owned-obligation-dependency-20261010/REPORT.md','Full report'),
 ('source-conditional-right-review-20261010/REPORT.md','Full report'),
 ('token-force-clarification-20261009/REPORT.md','Full report'),
 ('objective-goodness-source-check-20261010/NOTE.md','Full note'),
 ('original-normative-authority-20261009/inputs/SCOPED_AUTHORITY_APPRAISAL.md','Full appraisal'),
 ('original-normative-authority-20261009/inputs/PRIMARY_QUOTATION_CHECK.md','Full check'),
 ('original-normative-authority-20261009/INPUT_BINDINGS.json','Input custody schema and hash verification'),
 ('constructive-foundation-selection-20261009/inputs/CP23/intrinsic-normative-reasons-20261009/REPORT.md','Selected title/obedience/worship/specification matches; no full report reread'),
 ('token-force-clarification-20261009/inputs/T19_ARABIC_INDEX.md','Keyword location search only; no complete index read'),
 ('original-normative-authority-20261009/inputs/MIFTAH_CONTINUOUS_NOTES.md','Keyword location search only; no complete notes read')]
write('INPUT_BINDINGS.json',{'date_utc':'2026-10-10','records':[bind(ROOT/p,read_scope=s) for p,s in inputs],'protected_changes':'none'})
inherited=json.loads((ROOT/'original-normative-authority-20261009/INPUT_BINDINGS.json').read_text())
check=[]
for record in inherited['records']:
 p=ROOT/record['path'];b=bind(p);check.append({'path':record['path'],'sha256_matches':record['sha256']==b['sha256'],'bytes_match':record.get('bytes',b['bytes'])==b['bytes']})
write('INHERITED_BINDING_CHECK.json',{'records':check,'all_pass':all(r['sha256_matches'] and r['bytes_match'] for r in check),'meaning':'Mechanical byte identity only; does not confer fresh reading or verification credit for the contents.'})
sp=BASE/'sources';s=(sp/'ubudiyya-majmu10-direction-clean.txt').read_text();matches=list(re.finditer(r'ج/\s*10\s*ص\s*-(\d+)-',s));pages={int(m[1]):s[m.start():matches[i+1].start() if i+1<len(matches) else len(s)] for i,m in enumerate(matches)}
extract_checks=[]
for p in sorted(sp.glob('ubudiyya-[0-9]*-[0-9]*.txt')):
 a,b=map(int,re.fullmatch(r'ubudiyya-(\d+)-(\d+)\.txt',p.name).groups());expected='\n\n'.join(pages[n] for n in range(a,b+1));extract_checks.append({'path':str(p.relative_to(ROOT)),'exact_against_received_page_map':p.read_text()==expected})
read_record={
 'primary':{'url':'https://quranislam.github.io/fatwa/ibn-taymiyyah/fatwa147.html','attribution':'Ibn Taymiyya, al-Ubudiyya, as electronically displayed in Majmu al-fatawa 10:149-236','witness_status':'Modern electronic presentation of the attributed primary work. No verified imprint, print scan, manuscript or independent historical transmission.'},
 'parallel':{'url':'https://islamweb.net/ar/library/content/22/1008/','read_scope':'Returned contextual windows for love+submission at153, name/context/intention226-228, semantic conclusion232-233, two-principles234-235, obligatory/recommended173 and218-220. No continuous full-page read or whole-article credit.','comparison_status':'Same attributed work in another electronic presentation; not an independent historical witness.'},
 'page_coverage':[[149,158],[169,174],[186,195],[202,236]],
 'actual_local_display_order':[[149,158],[188,194],[209,218],[224,236],[186,187],[195,195],[202,208],[219,223],[169,174]],
 'continuous_argument_units':[
  {'pages':[149,158],'complete_unit':'Opening question, general worship account, love/submission, and causal-versus-voluntary servanthood through first paragraph158','boundary':'Rest of158 begins discussion of responding to providence and ends mid-sentence; not a completed new unit.'},
  {'pages':[169,174],'complete_unit':'Private taste versus source-conforming practice, prescribed causes, recommended/obligatory distinction, and two-principles/sincerity-correctness account through first paragraph174','boundary':'169 begins inside prior polemic;174 next question and grammar discussion continue past read boundary.'},
  {'pages':[186,195],'complete_unit':'Wealth/position attachments from189, love of beloved preferences190-193, and twofold dependence193-195 opening','boundary':'186 starts mid-discussion;195 subsequently begins a further submission argument ending beyond read boundary. Adjacent displays, not a single sequential read.'},
  {'pages':[202,218],'complete_unit':'Love and intimate friendship203-206, errors about worship and love206-208, claims of exemption209-214, practical affection and allegiance214-218 opening','boundary':'202 is continuing Abraham context;218 introduces the next fana classification. Adjacent displays with full coverage, not a single sequential read.'},
  {'pages':[218,225],'complete_unit':'Three types of fana and further distinctions of awareness through225','boundary':'Begins midway through218 and ends before late225 transition. Context for semantic argument, not new affirmation of every theological or historical claim.'},
  {'pages':[225,233],'complete_unit':'From late225 wayubayyinu dhalika ... through concluding paragraph233; isolated-name substitution, contextual answer, intention, activity ellipsis and terminology','boundary':'225 earlier text belongs to previous unit.'},
  {'pages':[234,236],'complete_unit':'Concluding two-principles and messenger-obedience account through end of treatise','boundary':'Download links after final blessing are site metadata.'}
 ],
 'parent_participating_reads':{'reported_page_ranges':[[224,236],[149,158],[188,194],[209,218],[169,174]],'credit':'Overlapping source checking, not independent historical witness or independent review.'},
 'processing':'HTML parsed with Python HTMLParser; script/style content suppressed; paragraph-like tags introduce line breaks. A separate received derivative strips only Unicode directional controls and normalizes repeated blank lines. Arabic wording and artifacts retained. Page extracts use explicit displayed page markers.',
 'artifacts_not_corrected':['Principal received228 contains garbled quoted phrase where Islamweb displays normal qul Allah wording. No inference rests on silent emendation.','Principal witness has other reference and transcription anomalies, including Yusuf verse numbers; none is used as a separately verified scriptural locator.'],
 'negative_claims':['No whole-treatise reading despite full-page download.','No new hadith authentication, manuscript or scan collation.','No new title theorem or contemporary substitution permission.','No corpus-wide novelty certification.'],
 'page_markers':{'count':len(matches),'unique':len(pages),'minimum':min(pages),'maximum':max(pages)},
 'files':[bind(p) for p in sorted(sp.iterdir()) if p.is_file()],
 'extract_verification':extract_checks
}
write('SOURCE_READS.json',read_record)
write('VERIFICATION.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inherited_input_hashes_pass':all(r['sha256_matches'] and r['bytes_match'] for r in check),'source_extract_identity_pass':all(r['exact_against_received_page_map'] for r in extract_checks),'principal_page_markers_unique':len(matches)==len(pages),'meaning':'Mechanical custody and derived-page identity checks. The report separately states argumentative conclusions and actual reading credit.','protected_changes':'none'})
write('MANIFEST.json',{'artifact_kind':'Separate source-bound research successor; no integration or closure authority','authored_records':[bind(BASE/n) for n in ['REPORT.md','INPUT_BINDINGS.json','INHERITED_BINDING_CHECK.json','SOURCE_READS.json','VERIFICATION.json','build_receipts.py','inputs/prior-worship-search.json']],'raw_source_disposition':'Saved source bodies and exact extracts are research intermediates, referenced and bound in SOURCE_READS.json.'})
print(json.dumps({'report':str(BASE/'REPORT.md'),'inherited_bindings':len(check),'source_files':len(read_record['files']),'source_extracts':len(extract_checks),'all_checks_pass':all(r['sha256_matches'] and r['bytes_match'] for r in check) and all(r['exact_against_received_page_map'] for r in extract_checks)},indent=2))
