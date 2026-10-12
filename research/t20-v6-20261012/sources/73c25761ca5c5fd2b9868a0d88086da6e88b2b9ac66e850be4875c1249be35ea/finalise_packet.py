#!/usr/bin/env python3
"""Compile final documents, run finite controls, verify links/hashes, and seal.

The receipt separates machine results from the assistant's unavailable readable
result stream. It never turns corpus ingestion into a personal reading claim.
"""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,traceback,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1];DATA=ROOT.parent
sys.path.insert(0,str(ROOT))
from verify_packet import verify_directory,verify_zip,ignored

def sha(b):return hashlib.sha256(b).hexdigest()
def putjson(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
def load(p,default=None):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception:return default

def run(command,log,timeout=180):
    try:
        p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
        text=p.stdout+p.stderr;rc=p.returncode
    except Exception as e:text=repr(e)+'\n';rc=-1
    (ROOT/'evidence'/log).write_text(text,encoding='utf-8')
    (ROOT/'evidence'/(log+'.exitcode')).write_text(str(rc)+'\n')
    return rc,text

(ROOT/'evidence').mkdir(exist_ok=True)
if not (ROOT/'evidence/04_source_copy_integrity.json').exists():
    run([sys.executable,str(ROOT/'research/build_corpus.py')],'04_corpus_build_final_attempt.log',180)
summary=load(ROOT/'corpus/summary.json',{})
documents=load(ROOT/'corpus/documents.json',[])
archives=load(ROOT/'corpus/archives.json',[])
inputs=load(ROOT/'corpus/inputs.json',[])
integrity=load(ROOT/'evidence/04_source_copy_integrity.json',{})
if not summary:
    summary={'problems':[{'error':'Corpus inventory was not available at finalisation.'}],
             'model_visible_readback_certified':False}

# Preserve the previous deliverable in its original safe hierarchy, without fonts or recursive ZIP duplication.
old=DATA/'Orthemology_T20_Whole_Corpus_Synthesis_20261010.zip'
prior_result={'input':str(old),'extracted':0,'excluded':[],'errors':[]}
if old.is_file():
    try:
        with zipfile.ZipFile(old) as z:
            base=ROOT/'prior_work/previous_synthesis';base.mkdir(parents=True,exist_ok=True)
            for i in z.infolist():
                if i.is_dir():continue
                p=PurePosixPath(i.filename);suf=p.suffix.lower()
                unsafe=p.is_absolute() or '..' in p.parts or '\\' in i.filename or ((i.external_attr>>16)&0o170000)==0o120000
                if unsafe or suf in {'.zip','.ttf','.otf','.woff','.woff2','.eot','.pfb','.pfa','.pyc'} or '__pycache__' in p.parts:
                    prior_result['excluded'].append(i.filename);continue
                dest=base/str(p);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(i));prior_result['extracted']+=1
    except Exception as e:prior_result['errors'].append(repr(e))
else:prior_result['errors'].append('Original synthesis ZIP is missing.')
putjson(ROOT/'evidence/08_prior_recovery.json',prior_result)

# Stable archive anchors and source-level navigation to actual original report files.
atlas_path=ROOT/'Packet_Atlas.md'
if not atlas_path.exists():atlas_path.write_text('# Packet atlas unavailable\n\nSee corpus build errors in the verification report.\n')
atlas=atlas_path.read_text(encoding='utf-8')
atlas=re.sub(r'(### ([^\n]+)\n\n\*\*Archive:\*\* `(A-[a-f0-9]+)`)',lambda m:f'<a id="{m.group(3).lower()}"></a>\n\n'+m.group(1),atlas)
atlas_path.write_text(atlas,encoding='utf-8')
B={d['id']:d for d in documents}
anchors={
'Historical revision and transport':['historical_source_revision','gaussian_observation','gradient_realization'],
'Posterior and joint geometry':['posterior_gradient','fisher_endpoint','joint-atomic','transport-boundary','radial-quartic'],
'Discretisation and full-law preservation':['gradient-discretization','full-law-gradient','moving_objective'],
'Moment recovery and effectivity':['capped_tensor','determinate_moment','exponential_tail','stationary_selection'],
'Realisability and positive continuation':['initial_validity','determinate_initial','computable_positive','polynomial_functional','coercive','damping','killing'],
'Joint type completion and effective certificates':['joint_completion','full_rule_independence','raw_gap','fullper','finite_source_certificate','serialized_certificates','canonical_syntax','recursor'],
'Affirmative foundations and source-bound response':['sourcehood','wisdom','repentance','receptivity','self_praise','attestation','continuing_title','scriptural'],
'Warrant, proof support and collective investigation':['warrant','proof','inquiry','calibrat','discrimination']}
cor=['# Source correspondence for the synthesis','',
'These are navigation correspondences to actual archive names and their complete report files. They do not assert that a keyword match proves a theorem dependency, or that every listed source has been independently re-proved.','']
for topic,terms in anchors.items():
    matches=[a for a in archives if any(t in a.get('canonical_name','').lower() for t in terms)]
    cor+=['## '+topic,'']
    for a in matches:
        cor += [f"### {a.get('canonical_name',a['id'])}",'',f"Archive `{a['id']}`.",'']
        ds=[B[i] for i in a.get('direct_report_ids',[]) if i in B]
        if ds:
            cor+=['; '.join(f"[{d.get('title',d['id'])}]({d['copied_path']})" for d in ds[:8])+'.','']
        else:cor+=['Container or supporting archive: use the member register to follow its child packets.','']
    if not matches:cor+=['No archive-name match in the ingested bytes. Consult the report-level register rather than assuming absence of the topic.','']
(ROOT/'Source_Correspondence.md').write_text('\n'.join(cor),encoding='utf-8')

# Reference tests, including the seal verifier's mutation and path controls.
rc,test_output=run([sys.executable,'-m','unittest','discover','-s','tests','-v'],'09_reference_and_tamper_tests.log',180)
match=re.search(r'Ran (\d+) tests? in ([\d.]+)s',test_output)
tests={'returncode':rc,'count':int(match.group(1)) if match else None,
       'reported_seconds':float(match.group(2)) if match else None,
       'machine_pass':rc==0 and bool(re.search(r'^OK\s*$',test_output,re.M)),
       'log':'evidence/09_reference_and_tamper_tests.log',
       'scope':'New exact finite reference controls and packet-verifier controls; not inherited Lean or philosophical review.'}
compile_rc,_=run([sys.executable,'-m','compileall','-q','research','tests','verify_packet.py'],'10_python_compilation.log',90)

counts=(f"{summary.get('top_level_archives','unavailable')} top-level archives; "
        f"{summary.get('unique_archives','unavailable')} distinct recursively discovered archives; "
        f"{summary.get('unique_report_documents','unavailable')} unique text report documents; "
        f"{sum(x.get('origin')=='materialised Library recovery' for x in inputs)} materialised Library recovery inputs. "
        'See the register for hashes, aliases and individual packet coverage.')
coverage=('The archive and report counts describe machine ingestion and documentary inclusion. '
          'The tool-result stream did not return readable outputs to the assistant during this continuation, '
          'so exhaustive fresh model-visible reading and observed final verification are **not certified**. '
          'Machine-generated execution receipts are included for inspection and replay; inherited Lean and independent-review claims retain their original, unrefreshed status.')
narrative=(ROOT/'research/field_guide_narrative.md').read_text(encoding='utf-8')
narrative=narrative.replace('{{CORPUS_COUNTS}}',counts).replace('{{COVERAGE_NOTE}}',coverage)
(ROOT/'Field_Guide.md').write_text(narrative+'\n\n'+atlas,encoding='utf-8')

reports=[d for d in documents if d.get('report')]
anthology=(ROOT/'All_Research_Reports.md').read_text(encoding='utf-8') if (ROOT/'All_Research_Reports.md').exists() else ''
register=(ROOT/'Corpus_Register.md').read_text(encoding='utf-8') if (ROOT/'Corpus_Register.md').exists() else ''
report_coverage=bool(documents) and all(d['id'] in anthology and d['id'] in register for d in reports)
atlas_coverage=bool(archives) and all(a['id'] in atlas for a in archives)
verification={'generated_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
 'corpus':summary,'source_copy_integrity_all_match':integrity.get('all_match',False),
 'all_report_ids_in_anthology_and_register':report_coverage,'all_archive_ids_in_atlas':atlas_coverage,
 'new_reference_tests':tests,'python_compilation_returncode':compile_rc,
 'fresh_observed_model_readback':False,'fresh_inherited_lean_compilation':False,
 'independent_review_of_new_theorems':False,'worldwide_novelty_established':False,
 'repository_modified':False,'t20_programme_closed':False}
putjson(ROOT/'evidence/11_build_verification.json',verification)

verify_md=f'''# Verification and coverage — read the statuses separately

## What this packet is

A source-linked field guide and documentary atlas of the ingested T20 corpus, a preserved text-report anthology, an additive mathematical and foundational contribution, exact finite reference controls, and a bounded handoff to Dot.

{counts}

## The unresolved fresh-read-back boundary

**The tool-result stream did not provide readable outputs to the assistant during this continuation. Therefore this packet does not certify the exhaustive fresh model-visible reading and observed final verification requested by the user.** Automated ingestion is not a substitute for that claim. This limitation is retained explicitly rather than assigning unobserved verification credit.

The documents and scripts were authored and submitted in this continuation. The following values are generated by the running programs, not recollected or manually invented test results.

## Machine-generated results

| Check | Recorded result |
|---|---|
| Recursive input archive CRC reads complete | {summary.get('archive_crc_read_complete','unavailable')} |
| Recorded ingestion problems | {len(summary.get('problems',[]))} |
| Copied sources match original member SHA-256 | {integrity.get('all_match','unavailable')} |
| Every classified text report ID occurs in anthology and register | {report_coverage} |
| Every discovered archive ID occurs in packet atlas | {atlas_coverage} |
| New reference and verifier tests | {tests.get('count')} tests; exit {rc}; machine PASS = {tests['machine_pass']} |
| Python source compilation | exit {compile_rc} |

Read `evidence/09_reference_and_tamper_tests.log`, `evidence/11_build_verification.json`, and `corpus/summary.json` for the actual recorded output and any errors. The external `.VERIFICATION.json` receipt is written after final directory and ZIP verification.

## What these checks establish

Source-copy hashes establish byte identity with the archive members actually read. Archive/member and report-ID checks establish documentary inclusion, not agreement with the source claims. Unit tests establish the listed finite controls on the new reference implementation. The written arguments, not a finite test count, supply the claimed mathematical generality.

The new suite contains controls for transported historical likelihoods, noisy-kernel merging, static sidecar label counts, joint-source correlations, rare conditioning, sharp relative-error bounds, source-support survival, dependency-local replay, active corrective changes, exact separable repair, audit-equivariant vector fields, the Euler counterexample, the rational positivity/descent/covariance step, and packet mutation/path attacks.

## What is not claimed

No fresh compilation of all inherited Lean, no independently observed rerun of all inherited programs, no new independent mathematical review, no source-by-source Arabic primary-text reappraisal, no empirical validation of the neural-weight paper, no worldwide originality finding, no production DAEE integration, no GitHub change, no merge, and no T20 or foundational programme closure.

The previous synthesis is preserved as earlier work. Its own receipts and review statements are inherited evidence, not silently refreshed here. Duplicate copies of a report do not count as independent witnesses.

## Replay

After extracting the ZIP, run from its top-level directory:

```bash
python verify_packet.py . --run-tests
```

This verifies the sealed directory and executes the packet's reference tests. The script does not download dependencies or run the inherited source programs. Python standard-library modules suffice.

A fresh verifier output is stronger evidence of this exact package's current bytes and finite controls than a summary sentence in a handoff. It still does not replace the separate semantic and philosophical reviews listed above.

## Ingestion issues and warnings

```json
{json.dumps({'problems':summary.get('problems',[]),'warnings':summary.get('warnings',[])},ensure_ascii=False,indent=2)}
```
'''
(ROOT/'Verification_and_Coverage.md').write_text(verify_md,encoding='utf-8')

status='''# Contribution status register

| Contribution | Supplied evidence | Boundary |
|---|---|---|
| Exact deterministic and stochastic historical-likelihood transport | Written iff proofs; exact finite controls | Full evidence contract; finite state/kernel formulation |
| Minimal static audit-profile supplement | Written necessity/sufficiency and counting proof; finite controls | Per-origin labels, not total distribution storage or all future dynamics |
| Sharp relative-likelihood posterior bound | Written sharp proof and attaining example; exact rational controls | Uniform positive relative-error contract; predictive calibration separate |
| Source-dependent replay and sensitivity | Written identities, ODE sensitivity and bounds; finite counterexamples | Historical, retrospective and prospective semantics kept distinct |
| Exact separable no-replay repair | Written commutation and explicit centred-weight solution; finite controls | Positions and accumulated factors unchanged by revision |
| Universal audit-covariant flow classification | Written log-odds/equivariance proof; tangent controls | Full positive audit family, labelled interior, unique local flow |
| Standard-metric separable-energy classification | Written affine-weight and off-diagonal derivative proof | Specified weighted transport/Fisher metric, fixed energy, connected product domain |
| Euler discrete audit failure | Exact rational counterexample | Does not diagnose the existing T20 integrator without inspecting it |
| Rational audit-covariant positive/descent step | Written positivity, covariance, descent and local derivative proof; finite controls | Fixed potentials and source-independent step selection; not a general convergence theorem |
| Joined evidence/geometry decision bound | Written total-variation/Lipschitz proof; finite controls | Bounded Lipschitz observables and justified transport error |
| Local-to-common-source bridge | Written gluing proof and countermodels | Philosophical overlap, coverage and source individuation still need their own warrant |
| Survival of unaffected affirmative warrants | Written support-family equivalence; finite controls | Complete material support and already checked witnesses |

These are authorial results with explicit proofs and finite reference controls. No global priority or new independent-review claim is made. Compare the classification and discretisation contributions with the corresponding original T20 packets before deciding whether they are new results, strengthened formulations or useful re-expressions of existing work.
'''
(ROOT/'Contribution_Status.md').write_text(status,encoding='utf-8')

readme=f'''# Orthemology T20 — reconciled research packet

## Read first

[Field guide, including every discovered packet](Field_Guide.md) · [New mathematical contribution](Cross_Front_Theorems.md) · [Foundational synthesis](Foundational_Synthesis.md) · [Ready-to-send Dot handoff](Dot_Handoff.md)

{counts}

## The principal new handoff

The joint audit/geometry classification and discrete acceptance test connect historical source revision to the actual state-and-weight correction programme. In the declared universal audit class, the vector-field form is characterised exactly. A positive, energy-decreasing Euler step can still fail audit covariance; a rational positive, descending, audit-covariant reference step is supplied and proved.

The companion results give exact historical-likelihood transport, a minimal finite static audit supplement, a sharp positive relative-error bound, dependency-directed replay, a combined evidence/geometry decision margin, and a conditional common-source bridge for the foundations.

## Evidence boundary

{coverage}

Read [verification and coverage](Verification_and_Coverage.md) before assigning completion or PASS credit. This packet is not a claim that the user's requested exhaustive fresh reading and observed final verification have been completed.

## Navigating the sources

[Corpus register](Corpus_Register.md) lists every unique archive and classified text report with hashes and original identities. [Packet atlas](Packet_Atlas.md) organises the actual packets and supplies source-owned excerpts. [Complete text-report anthology](All_Research_Reports.md) preserves every classified text report. [Source correspondence](Source_Correspondence.md) provides topic-to-source navigation. [Revision ledger](Revision_Ledger.md) preserves source-local correction, recovery and supersession cues.

Original text files are copied unchanged under `sources/`. Binary source documents such as PDFs are copied where supported and indexed in `corpus/documents.json`; their inclusion is not a fresh visual or primary-source review. Build artefacts, fonts and recursive ZIP duplicates are not republished. The exact original ZIPs remain identified by their input hashes.

[Earlier-synthesis reconciliation](Prior_Synthesis_Reconciliation.md) explains what is retained and what the larger corpus changes. Its safe original file hierarchy is preserved under `prior_work/previous_synthesis/` as recorded in the recovery receipt.

## Research review and replay

[Contribution status](Contribution_Status.md) and [author's adversarial review](Research_Review.md) distinguish proof scope from finite controls and unresolved independent review.

```bash
python verify_packet.py . --run-tests
```

The verifier checks the manifest and runs only this packet's new standard-library reference suite. No inherited source program is automatically executed. No repository has been modified and no research programme has been closed by this packet.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')

# Validate links authored by this build, ignoring inherited quotation/fenced contents.
owned=['README.md','Field_Guide.md','Packet_Atlas.md','Corpus_Register.md','Source_Correspondence.md',
       'Cross_Front_Theorems.md','Foundational_Synthesis.md','Dot_Handoff.md','Verification_and_Coverage.md',
       'Contribution_Status.md','Research_Review.md','Prior_Synthesis_Reconciliation.md']
link_errors=[];link_count=0
for name in owned:
    path=ROOT/name
    if not path.is_file():link_errors.append({'file':name,'error':'missing owned document'});continue
    fence=None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.lstrip().startswith('>'):continue
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            token=m.group(1)
            if fence is None:fence=token
            elif token[0]==fence[0] and len(token)>=len(fence):fence=None
            continue
        if fence:continue
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',line):
            target=target.strip().split(' "')[0]
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
            rel=unquote(target.split('#')[0]);link_count+=1
            if rel and not (path.parent/rel).exists():link_errors.append({'file':name,'target':target,'error':'missing linked path'})
putjson(ROOT/'evidence/12_owned_link_check.json',{'links_checked':link_count,'all_paths_exist':not link_errors,'errors':link_errors})

# Preserve source-led binary navigation in the human register without altering originals.
reg=ROOT/'Corpus_Register.md'
if reg.is_file():
    s=reg.read_text(encoding='utf-8')
    if '## Binary source documents' not in s:
        binary=[d for d in documents if d.get('kind')=='binary-source']
        s+='\n\n## Binary source documents\n\nCopied and indexed, not freshly visually reviewed in this continuation.\n\n'
        for d in binary:s+=f"- `{d['id']}`: [{d['names'][0]}]({d['copied_path']}) — {d['bytes']} bytes.\n"
        reg.write_text(s,encoding='utf-8')

# All exact bytes below are sealed; post-seal receipts are written outside the directory.
files={}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=str(p.relative_to(ROOT)).replace('\\','/')
    if rel=='MANIFEST.json' or ignored(rel):continue
    if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.eot','.pfb','.pfa'}:continue
    b=p.read_bytes();files[rel]={'sha256':sha(b),'bytes':len(b)}
manifest={'schema':1,'created_utc':datetime.now(timezone.utc).isoformat(),
          'scope':'Exact bytes of this derivative research packet; not semantic proof certification.',
          'files':files}
putjson(ROOT/'MANIFEST.json',manifest)
directory_receipt=verify_directory(ROOT)
zip_path=DATA/'Orthemology_T20_Reconciled_Research_20261010.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in list(files)+['MANIFEST.json']:z.write(ROOT/name,ROOT.name+'/'+name)
zip_receipt=verify_zip(zip_path)
zip_hash=sha(zip_path.read_bytes())

standalone={
 'README.md':'Orthemology_T20_START_HERE_20261010_R2.md',
 'Field_Guide.md':'Orthemology_T20_Field_Guide_20261010_R2.md',
 'Cross_Front_Theorems.md':'Orthemology_T20_Cross_Front_Theorems_20261010_R2.md',
 'Foundational_Synthesis.md':'Orthemology_T20_Foundational_Synthesis_20261010_R2.md',
 'Dot_Handoff.md':'Orthemology_T20_Dot_Handoff_20261010_R2.md',
 'Corpus_Register.md':'Orthemology_T20_Corpus_Register_20261010_R2.md',
 'Verification_and_Coverage.md':'Orthemology_T20_Verification_and_Coverage_20261010_R2.md',
 'Packet_Atlas.md':'Orthemology_T20_Packet_Atlas_20261010_R2.md'}
standalone_receipts=[]
for source,name in standalone.items():
    if (ROOT/source).is_file():
        shutil.copyfile(ROOT/source,DATA/name)
        standalone_receipts.append({'path':str(DATA/name),'sha256':sha((DATA/name).read_bytes()),'bytes':(DATA/name).stat().st_size})
final={'generated_utc':datetime.now(timezone.utc).isoformat(),'directory':directory_receipt,'zip':zip_receipt,
       'zip_path':str(zip_path),'zip_bytes':zip_path.stat().st_size,'zip_sha256':zip_hash,
       'standalone_files':standalone_receipts,'build_verification':verification,
       'owned_link_check':{'count':link_count,'errors':link_errors},
       'machine_checks_pass':directory_receipt.get('ok',False) and zip_receipt.get('ok',False) and tests['machine_pass'] and compile_rc==0 and not link_errors and report_coverage and atlas_coverage and integrity.get('all_match',False) and not summary.get('problems'),
       'fresh_exhaustive_model_visible_reading_certified':False,
       'fresh_model_observed_verification_certified':False}
receipt=DATA/'Orthemology_T20_Reconciled_Research_20261010.VERIFICATION.json';putjson(receipt,final)
(DATA/'Orthemology_T20_Reconciled_Research_20261010.sha256').write_text(zip_hash+'  '+zip_path.name+'\n')
print(json.dumps({'zip':str(zip_path),'zip_bytes':zip_path.stat().st_size,'machine_checks_pass':final['machine_checks_pass'],
                  'reference_tests':tests,'unique_archives':summary.get('unique_archives'),
                  'unique_text_reports':summary.get('unique_report_documents'),
                  'receipt':str(receipt),'standalone':standalone_receipts},indent=2))

if __name__=='__main__':pass
