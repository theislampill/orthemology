from pathlib import Path
import csv,json,hashlib,os,zipfile
b=Path('independent-five-front-supplement');e=b/'extracted/T20_Independent_Five_Front_Supplement'
rows=list(csv.DictReader((e/'SOURCE_LEDGER.csv').open()))
M={
'S01':('corroborative locator','brute-contingent-source-return/REPORT.md','Existing Dar8:126–136 scan-controlled asymmetry/taxonomy appraisal; earlier124–125 locus adds no identified new discriminator. Report/CSV scope differs.'),
'S02':('direct prior coverage','brute-contingent-source-return/REPORT.md','Dar8:131 lies within already inspected126–136; no new reading claim.'),
'S03':('corroborative locator','brute-contingent-source-return/REPORT.md','Same existence/nonexistence asymmetry directly established at127–131; exact121–122 body not reacquired here.'),
'S04':('direct prior coverage','brute-contingent-source-return/REPORT.md','Dar3:166–173 voice transition and response directly checked; Ibn Sina quotation is not uniformly Ibn Taymiyyah speech.'),
'S05':('semantic overlap; exact locus unresolved','essence-attribute-source-return/REPORT.md','Existing Dar1:280–282 and4:259–260 separate productive dependence from subject/concomitance. Exact4:239–240 not independently checked here.'),
'S06':('semantic overlap; exact locus unresolved','essence-attribute-source-return/REPORT.md','Same concrete essence/existence and nonreification safeguard directly checked atDar1:292–295; exact5:103 not independently checked here.'),
'S07':('direct prior scan coverage','simultaneous-nonduplication-source-return/jami/JAMI_VI_94_98_VERIFIED_RETURN.md','Print94–98 checks already establish source argument and index/page offset. CSV91–97 is broader than report94–97.'),
'S08':('direct prior coverage','simultaneous-nonduplication-source-return/PAGE_AND_VOICE_MAP.md','Majmu20:174–184 complete local source read and productive-condition/perfection analysis.'),
'S09':('direct prior coverage','simultaneous-nonduplication-source-return/PAGE_AND_VOICE_MAP.md','Dar9:342–345 item1769 within continuous336–367 source/voice audit.'),
'S10':('direct prior coverage','t20-next-frontier-20261008/bearer-eligibility/SOURCE_READS.json','Majmu2 item133 retained and read in bearer eligibility.'),
'S11':('full epistle prior coverage','essence-attribute-source-return/REPORT.md','Whole unique Akmaliyya6:68–140 already read; this andS21 are not independent witnesses.'),
'S12':('semantic overlap; exact locus unresolved','essence-attribute-source-return/REPORT.md','Mental universal versus concrete qualified bearer already directly supported; preciseDar5:126–127 not checked here.'),
'S13':('semantic overlap; exact locus unresolved','t20-next-frontier-20261008/bearer-eligibility/CURRENT_FINDING.md','Mental supposition is not external possibility already central to eligibility appraisal; precise5:134–135 not checked here.'),
'S14':('semantic overlap; exact locus unresolved','essence-attribute-source-return/REPORT.md','Concrete essence/existence distinction already established; precise5:143–144 not checked here.'),
'S15':('fresh bounded primary attribution','independent-five-front-supplement/sources/bayan4-item839.txt','Entire electronic unit read. Reported stronger anti-inference claim differs from author basic-recognition argument; no scan or universal factivity.'),
'S16':('fresh bounded primary attribution','independent-five-front-supplement/sources/bayan4-item844.txt','Entire electronic unit read. Cognitive-volitional opening precedes586 boundary; transmission continuation through590. Directed orientation, not neutral receptivity.'),
'S17':('corroborative locator; exact prior scope unresolved','t20-next-frontier-20261008/fitrah-warrant-bridge/PRIMARY_VERIFICATION.md','PriorDar8 signs/recognition/report distinctions substantially overlap; exactDar7:302–303 not independently checked here.'),
'S18':('inherited volume and thematic coverage','t20-next-frontier-20261008/fitrah-warrant-bridge/PRIMARY_VERIFICATION.md','Dar8 full electronic traversal and focused basic recognition unit already recorded; no fresh page347–348 match claimed.'),
'S19':('direct prior span coverage','t20-next-frontier-20261008/wise-determination/SOURCE_READS.json','Majmu8:135–137 inside direct118–153 reading. Item URL may differ; substantive interval controls.'),
'S20':('corroborative locator; exact prior scope unresolved','t20-next-frontier-20261008/productive-sufficiency-scope/REPORT.md','Token/series and beginningless-act safeguard already present inMajmu8 return; preciseMajmu12:224–229 not checked here.'),
'S21':('full epistle prior coverage','t20-next-frontier-20261008/productive-sufficiency-scope/REPORT.md','Appropriate-mode giver/perfection argument already examined6:76–90; same epistle asS11.'),
'S22':('prior source; exact early interval unresolved','t20-next-frontier-20261008/wise-determination/REPORT.md','Majmu8 item805 retained, focused direct118–153 plusAkmaliyya already supports result; precise88–90 not newly verified here.'),
'S23':('highest-priority separate active return','direct-anti-brute-return/','Parent separately assigned directDar3:288–289 contextual/print/inferential check. No duplicate acquisition or premature result here.'),
'S24':('parent fresh print control','necessity-domain-source-control/RESULT.md','Parent visually readIII239–242. Strengthens necessity-domain safeguard and member/whole-arrangement versus self-production distinction.'),
'S25':('parent fresh print control','necessity-domain-source-control/RESULT.md','Parent visually readIII17–18. Broad necessity, self-standingness and original efficient source are distinct domains.'),
'S26':('fresh bounded primary attribution','independent-five-front-supplement/sources/ahkam2-item198.txt','Whole electronic chapter unit read: opening before945 marker, continuation through953. Author reply begins before948 marker; developing directed capacity already covered byDar8/Shifa.'),
'R01':('prior full paper coverage','t20-next-frontier-20261008/modal-psr-bridge/RESULT.md','Published-format1999 article fully read; packet only publisher abstract checked.'),
'R02':('prior full paper coverage','epistemic-psr-warrant/RESULT.md','Full2020/2021 article21 pages including notes/references; restricts PSR to plural basic natural facts and central inference to metaknowledge.'),
'R03':('prior full paper coverage','t20-next-frontier-20261008/complete-overdetermination-audit/SOURCE_READS.json','Schaffer printed23–45 fully read; packet only abstract/opening definitions.'),
'R04':('prior full paper coverage','t20-next-frontier-20261008/qualitative-ontology-warrant/QUALITATIVE_ONTOLOGY_WARRANT.md','2009 complete-paper appraisal already distinguishes primitive material individuals from all possible bearers.'),
'R05':('prior full paper coverage','t20-next-frontier-20261008/collective-explanation-adequacy/REPORT.md','2014 all28 pages and49 notes already read; issue14(20) corrected and verified there.'),
'R06':('prior full paper coverage plus targeted returns','t20-next-frontier-20261008/modal-grounding-source/REPORT.md','Inherited2016 full read plus targeted plural-ground and autonomy/norm scope analysis; packet abstract not expansion.'),
'R07':('exact prior coverage not resolved; nonpriority','t20-next-frontier-20261008/fitrah-warrant-bridge/INDEPENDENT_ASSESSMENT.md','Local warrant distinction already developed; no fresh1993 book/chapter read claimed or needed to adjudicate supplement.'),
'R08':('exact prior coverage not resolved; nonpriority','t20-next-frontier-20261008/fitrah-warrant-bridge/INDEPENDENT_ASSESSMENT.md','Proper-function model versus actual factive warrant already distinguished; no fresh2000 book read claimed.'),
'R09':('inherited full article coverage','recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/historical-reading-projections/documents/Orthemology_Seventeenth_Foundational_Source_Guide_Final_v1_20261005.md','T17 records anthologyPDF71–117, body/bibliography/endnotes; packet institutional abstract adds no new coverage.'),
'R10':('exact prior coverage not resolved; nonpriority','positive-agency-source-return/REPORT.md','Packet itself only surveyed metadata; no whole-book claim. Existing primary wisdom/agency appraisal does not depend on this lead.'),
'R11':('secondary overview; nonpriority','epistemic-psr-warrant/RESULT.md','Existing targeted original-paper appraisal is more discriminating; overview is not new primary evidence.')}
assert set(M)=={r['source_id'] for r in rows}
with (b/'LEDGER_CROSSWALK.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])+['local_status','local_record','assessment']);w.writeheader()
 for r in rows:w.writerow(dict(r,local_status=M[r['source_id']][0],local_record=M[r['source_id']][1],assessment=M[r['source_id']][2]))
checks={}
for line in (e/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split(None,1);checks[n]=hashlib.sha256((e/n).read_bytes()).hexdigest()==h
z=next((b/'supplied').glob('*.zip'))
with zipfile.ZipFile(z) as f:crc=f.testzip()
main=next((b/'supplied').glob('Orthemology*.md'));comp=next((b/'supplied').glob('DOT*.md'))
prov=json.loads((b/'PROVENANCE.json').read_text())
for t in prov['transfers']:
 p=Path(t['workspace_path']);t['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();t['xattrs_verified']={k:os.getxattr(p,k).decode() for k in ['user.library-file-id','user.library-file-version']}
(b/'PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n')
inputs={}
for row in M.values():
 p=Path(row[1]);
 if p.is_file():inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [Path('t20-next-frontier-20261008/fitrah-warrant-bridge/warranting-basis-addendum/CLARIFICATION.md')]:inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(b/'INPUT_BINDINGS.json').write_text(json.dumps(inputs,indent=2)+'\n')
validation={'crc_failure_member':crc,'supplied_checksums':checks,'standalone_report_matches_zip':main.read_bytes()==(e/'INDEPENDENT_FIVE_FRONT_SOURCE_SUPPLEMENT.md').read_bytes(),'standalone_companion_matches_zip':comp.read_bytes()==(e/'DOT_COMPANION_MESSAGE.md').read_bytes(),'ledger_rows':len(rows),'unique_ids':len({r['source_id'] for r in rows}),'all_ids_in_report':all(r['source_id'] in main.read_text() for r in rows),'all_rows_crosswalked':len(M)==len(rows),'no_embedded_code':True,'no_existing_repository_files_modified':True}
(b/'VERIFICATION.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))
