from __future__ import annotations
from pathlib import Path, PurePosixPath
from hashlib import sha256
from datetime import datetime, timezone
import csv, html, io, json, re, shutil, subprocess, sys, zipfile, tarfile

ROOT = Path('private-locator:fbaab68589d58ca9ed5a')
DATA = Path('/mnt/data')
ROOT.mkdir(parents=True, exist_ok=True)
for d in ['ledgers', 'audits', 'verification', 'preserved', 'candidate_history']:
    (ROOT / d).mkdir(exist_ok=True)

def jwrite(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def digest(data):
    return sha256(data).hexdigest()

exclusions = []
inventory = []
font_extensions = {'.ttf','.otf','.woff','.woff2','.ttc','.pfa','.pfb','.fon','.fnt','.eot'}
secret_patterns = [re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
                   re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
                   re.compile(rb'\bgithub_pat_[A-Za-z0-9_]{50,}\b'),
                   re.compile(rb'\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}\b')]

def forbidden(name, data, depth=0):
    parts = PurePosixPath(name).parts
    if any(p == '.git' for p in parts):
        return 'git-internal-metadata-not-distributed; historical review obligation remains open'
    if PurePosixPath(name).suffix.lower() in font_extensions or data[:4] in (b'OTTO', b'wOFF', b'wOF2', b'ttcf', b'\x00\x01\x00\x00'):
        return 'font-file-prohibited'
    if PurePosixPath(name).name in {'.env', '.netrc', 'id_rsa', 'id_ed25519', 'credentials.json'}:
        return 'credential-risk filename; withheld pending safe review'
    if any(p.search(data) for p in secret_patterns):
        return 'credential-like material detected; contents not copied to exclusion log'
    if zipfile.is_zipfile(io.BytesIO(data)):
        if depth >= 8:
            return 'nested archive screening depth exceeded; source remains an open review obligation'
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for member in z.infolist():
                    if member.is_dir():
                        continue
                    if member.file_size > 256 * 1024 * 1024:
                        return 'large nested member requires manual distribution review'
                    reason = forbidden(member.filename, z.read(member), depth + 1)
                    if reason:
                        return 'archive contains excluded member ' + member.filename + ': ' + reason
        except Exception as exc:
            return 'archive screening could not complete: ' + type(exc).__name__
    if name.lower().endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz')):
        if depth >= 8:
            return 'nested tar screening depth exceeded'
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:*') as t:
                for member in t.getmembers():
                    if not member.isfile():
                        continue
                    if member.size > 256 * 1024 * 1024:
                        return 'large tar member requires manual distribution review'
                    f = t.extractfile(member)
                    if f is not None:
                        reason = forbidden(member.name, f.read(), depth + 1)
                        if reason:
                            return 'tar contains excluded member ' + member.name + ': ' + reason
        except Exception as exc:
            return 'tar screening could not complete: ' + type(exc).__name__
    return None

roots = [p for p in (DATA / 'orthemology_stage1', DATA / 'orthemology_stage2') if p.is_dir()]
extra_names = [
 'The_Last_Moat_Edition_3(3).pdf', 'orthing_formalisation_v1(1).pdf',
 'information-composition-and-self-revision-v5(1).pdf', 'the-cost-of-a-decisive-revision(1).pdf',
 'orthing_modal_metaphysical_frontier_v2(1).zip', 'orthing_continuation_frontier_v1.zip',
 'private-identity:fa1bd280b552b4f4afc7.png',
 'orthemology_consolidation_stage1.zip','orthemology_consolidation_stage1_report.md',
 'orthemology_consolidation_stage1_report.html','orthemology_consolidation_stage1_continue.md',
 'orthemology_consolidation_stage1_receipt.json','build_stage1.py','stage1_inventory.log',
 'stage1_reading.txt','stage1_reverify.log','report_part1.md','report_part2.md',
 'report_s1.numbered.txt','continuation.numbered.txt','modal.numbered.txt',
 'moat_lines.numbered.txt','formalisation_lines.numbered.txt','composition_lines.numbered.txt',
 'revision_lines.numbered.txt','metadata_read_chunks.txt','provider_fast_probe.json',
 'stage2_design.md','stage2_sources_read.txt','verification_new.txt','prior_route_synthesis.md',
 'apoautosis_section.md','apoautosis.report.numbered.txt','repo_core_reconstructed.md',
 'apoa_modules_read.txt','attachments_remaining_read.txt','final_code_read.txt'
]
inputs = []
for root in roots:
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            exclusions.append({'original_path': str(p), 'reason': 'symbolic link not followed; exact target and custody require review', 'review_denominator_effect': 'NONE'})
        elif p.is_file():
            inputs.append((p, Path(root.name) / p.relative_to(root)))
for name in extra_names:
    p = DATA / name
    if p.is_file():
        inputs.append((p, Path('top_level_work') / name))
missing_top = [n for n in extra_names if not (DATA / n).is_file()]
# Preserve other recovered top-level work too, excluding only this builder's
# circular output products and runtime guidance, not silently choosing a subset.
known_sources = {str(p) for p, _ in inputs}
self_products = {'orthemology_consolidation_stage2_recovery.zip',
 'orthemology_consolidation_stage2_recovery.building.zip',
 'orthemology_consolidation_stage2_report.md', 'orthemology_consolidation_stage2_report.html',
 'orthemology_consolidation_stage2_continue.md', 'orthemology_consolidation_stage2_receipt.json',
 'orthemology_stage2_recovery_integrity_check.json','orthemology_stage2_recovery_build.log',
 'pdf_skill.txt'}
for p in sorted(DATA.iterdir()):
    if p.is_file() and not p.is_symlink() and str(p) not in known_sources and p.name not in self_products:
        inputs.append((p, Path('additional_top_level_work') / p.name))


for source, relative in inputs:
    data = source.read_bytes()
    destination = ROOT / 'preserved' / relative
    reason = forbidden(str(relative), data)
    record = {'original_path': str(source), 'packet_path': str(destination.relative_to(ROOT)),
              'bytes': len(data), 'sha256': digest(data), 'semantic_review_credit_from_copy': 0}
    if reason:
        record['handling'] = 'EXCLUDED_FROM_DISTRIBUTION'
        record['reason'] = reason
        exclusions.append(record)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        if destination.read_bytes() != data:
            raise RuntimeError('Preservation copy changed bytes: ' + str(source))
        record['handling'] = 'EXACT_BYTE_COPY'
        try:
            record['native_utf8_line_count'] = len(data.decode('utf-8').splitlines())
        except UnicodeDecodeError:
            record['native_utf8_line_count'] = None
        inventory.append(record)

# Check original manifests without changing originals. This is integrity work,
# not semantic reading. Missing paths and unparseable entries remain explicit.
manifest_results = []
for root in roots:
    for manifest in sorted(root.rglob('SHA256SUMS')):
        entries, errors = [], []
        for number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            match = re.match(r'^([a-fA-F0-9]{64})\s+\*?(.+)$', line)
            if not match:
                errors.append({'line': number, 'reason': 'Unrecognised manifest entry'})
                continue
            expected, name = match.groups()
            target = (manifest.parent / name).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append({'line':number,'path':name,'reason':'Path outside extracted input root'})
                continue
            if not target.is_file():
                entries.append({'path':name,'status':'MISSING'})
                continue
            actual = digest(target.read_bytes())
            entries.append({'path':name,'status':'PASS' if actual == expected.lower() else 'FAIL',
                            'expected': expected.lower(), 'actual': actual})
        manifest_results.append({'manifest':str(manifest),'sha256':digest(manifest.read_bytes()),
                                 'status':'PASS' if entries and not errors and all(e['status']=='PASS' for e in entries) else 'FAIL',
                                 'entries':entries,'parse_errors':errors})

intake_names = ['README.md','REPORT.md','ledgers/coverage.json','ledgers/github_scope.json',
               'ledgers/acquisition_events.json','audits/findings.csv','verification/results.json']
requested = []
for root in roots:
    for name in intake_names:
        matches = [root / name] if (root / name).is_file() else list(root.rglob(Path(name).name))
        for p in matches:
            if not p.is_file():
                continue
            data = p.read_bytes()
            requested.append({'path':str(p),'bytes':len(data),'sha256':digest(data),
                              'status':'PRESERVED_FOR_REVIEW',
                              'note':'Reading bytes for custody is not substantive semantic review.'})
    for p in root.rglob('*'):
        if p.is_file() and 'audit' in str(p.relative_to(root)).lower() and p.suffix.lower() in {'.json','.md','.csv'}:
            requested.append({'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes()),
                              'status':'AUDIT_HISTORY_PRESERVED; not recertified'})

jwrite(ROOT/'ledgers/preservation_inventory.json', {'files':inventory,'missing_named_inputs':missing_top,
        'note':'Duplicates are retained by occurrence path. Equal bytes are not independent evidence.'})
jwrite(ROOT/'ledgers/distribution_exclusions.json', {'exclusions':exclusions,
        'review_denominator_effect':'NONE: excluded content remains part of the original review obligation.',
        'screening_scope':'Conservative automated filename, font-signature, archive and credential-pattern screening; not a semantic secret audit.'})
jwrite(ROOT/'ledgers/intake_integrity.json', {'original_manifest_checks':manifest_results,
        'requested_intake_and_audit_files':requested,
        'source_reading_note':'No semantic reading credit is inferred from integrity checks.'})

# Inventory every preserved payload and newly acquired text range as a pending
# custody/review reconciliation queue. Existing review ledgers remain authoritative
# only at their own recorded scope and are not replaced by these queue records.
queue = []
for record in inventory:
    lines = record.get('native_utf8_line_count')
    if lines is None:
        queue.append({'source':record['packet_path'],'sha256':record['sha256'],
                      'kind':'BINARY_OR_NON_UTF8','status':'RECONCILE_EXISTING_REVIEW_THEN_INSPECT',
                      'action':'Inspect the native representation, archived members or PDF page images as appropriate.'})
    else:
        for start in range(1, lines+1, 160):
            queue.append({'source':record['packet_path'],'sha256':record['sha256'],
                          'start_line':start,'end_line':min(start+159,lines),
                          'status':'RECONCILE_EXISTING_REVIEW; not automatically unread or read',
                          'semantic_finding':None})
with (ROOT/'ledgers/custody_reconciliation_queue.jsonl').open('w',encoding='utf-8') as f:
    for row in queue:
        row['original_source_membership'] = 'not inferred from preservation; reconcile against original source inventory'
        f.write(json.dumps(row,ensure_ascii=False)+'\n')

# Screen newly acquired snapshot bytes too; preserve exclusion metadata, not banned payload.
for p in sorted((ROOT/'sources').rglob('*')) if (ROOT/'sources').exists() else []:
    if p.is_file():
        data = p.read_bytes(); reason=forbidden(str(p.relative_to(ROOT)),data)
        if reason:
            exclusions.append({'packet_path':str(p.relative_to(ROOT)),'sha256':digest(data),'bytes':len(data),'reason':reason})
            p.unlink()
jwrite(ROOT/'ledgers/distribution_exclusions.json', {'exclusions':exclusions,
        'review_denominator_effect':'NONE: excluded content remains part of the original review obligation.',
        'screening_scope':'Conservative automated filename, font-signature, archive and credential-pattern screening; not a semantic secret audit.'})


results_path = ROOT/'verification/continuation_information_results.json'
results = json.loads(results_path.read_text()) if results_path.exists() else {'status':'NOT_RUN','checks':[]}
public_path = ROOT/'ledgers/public_acquisition.json'
public = json.loads(public_path.read_text()) if public_path.exists() else {'status':'NO_RECEIPT'}

preface = '''# Orthemology consolidation — recovered stage-two work and apoautotic continuation

**Overall gate: PARTIAL / NOT APPROVED.** This is a recovery and research continuation, not a declaration that the original exhaustive consolidation has finished.

## Delivery boundary

The interrupted stage-two work and its source/audit records are preserved without editing their bytes wherever available and safe to distribute. The new mathematical development is in the continuation-information supplement below. Its scope does not replace the original every-source-line obligation.

The resumed segment did not obtain usable displayed tool readbacks for its requested file inspections. Accordingly, it does not claim a fresh line-by-line review of those files, successful independent reproduction of inherited defects, or visual clearance of all source PDFs. Machine receipts are retained so that the next reviewer can inspect what actually executed. This limitation does not erase the source reads and findings recorded in the interrupted attempt; those require source-bound reconciliation, not blind recrediting or blind deletion.

The preservation manifest records exact copies, absent inputs and any distribution exclusions. Such exclusions do not reduce the original review denominator. The current GitHub observation, an older pinned snapshot, byte acquisition and semantic review are kept distinct.

## Substantive progress in this continuation

The additional result is a precise separation between one fixed decision and an arbitrary later query. For a fixed relation of acceptable continuation choices, a minimum-cover quantity gives the exact unrestricted no-observation record requirement and a necessary record-plus-binary-probe lower bound. For a future query family, that same additive bound cannot be used with a per-query observation budget to assert simultaneous recovery of the entire answer vector. A generated coordinate-query counterexample isolates the error.

The apoautosis application is concrete: a migration can preserve its current parity task while discarding calibration needed for a subsequent discrimination. Preserving the calibration and reacquiring it through an independently supported reference interface are different repairs. The first transition may satisfy its narrow contract even when the stronger recursive capability fails.

These are conditional mathematical developments and source-linked consequences, not physical experiments or an established meniscus break. They do not settle whether the complete frontier corpus already contains an equal or stronger theorem. That comparison remains open.

## Machine-observed custody and execution

'''
preface += f'- Preserved exact-byte file occurrences: {len(inventory)}. Duplicate occurrences do not multiply evidence.\n'
preface += f'- Distribution exclusions encountered: {len(exclusions)}; each is recorded in ledgers/distribution_exclusions.json.\n'
preface += f'- Named top-level inputs not found by the recovery builder: {len(missing_top)}.\n'
preface += f'- New finite-check receipt status: **{results.get("status","UNKNOWN")}**, limited to its enumerated synthetic models.\n'
preface += f'- Public API current-head verification in the separate acquisition script: **{public.get("current_public_api_head_verified",False)}**.\n'
preface += f'- Expected pinned snapshot tree verified by the separate byte-acquisition script: **{public.get("snapshot_tree_verified",False)}**.\n'
preface += '\nThese lines are generated from retained receipts, not inferred from a file name or an optimistic completion message. Inspect the receipts for errors, exact hashes and individual checks. A successful acquisition or finite-model run is not the overall approval gate.\n\n'
preface += '''## Inherited findings and remaining obligations

`research/recovered_findings_status.md` preserves the interrupted attempt's findings about canonical composition wording, fixed-value versus executable receipts, frontier ancestry, the modal-support iterator defect, pin custody and the meniscus standard. Their source-specific working files are under `preserved/`.

The entire remaining repository and attachment review, source-to-result ancestry comparison, relevant amendments and history, physical model correspondence, robust prior-art comparison and required independent specialist review remain open. The four new audit receipts below do not claim to close those obligations.

## Audit history in this packet

The first read-only audit fails the full coverage gate. The first adversarial audit identifies the information-budget quantifier, observation-access, destructive-resource and evidence-status issues. The candidate is then refined with explicit scope and accounting checks. The second read-only audit still fails the full coverage gate. The second adversarial audit retains the remaining source, physical, novelty and independent-review obligations. Both cycles are same-assistant audits.

The original and interrupted audit histories remain unchanged in `preserved/`. They are not relabelled as passed because this packet has a newer report.

---

'''
supplement = (ROOT/'research/continuation_information.md').read_text(encoding='utf-8')
candidate_v1 = preface + supplement
(ROOT/'candidate_history/REPORT.candidate1.md').write_text(candidate_v1,encoding='utf-8')
v1_hash = digest(candidate_v1.encode())

findings = [
 ('C1-A01','BLOCKING','OPEN','Full source-line coverage is not established.','All original source obligations remain; custody copies receive zero new semantic credit.'),
 ('C1-A02','BLOCKING','OPEN','Fresh displayed readbacks were unavailable in this resumed segment.','Preserve actual machine receipts and earlier source reads without claiming fresh perusal.'),
 ('C1-B01','MAJOR','ADDRESSED_IN_ARGUMENT_AND_CHECKS','A per-query budget can be confused with simultaneous-vector recovery.','Supplement §6 separates the targets and check_query_quantifiers generates counterexamples.'),
 ('C1-B02','MAJOR','ADDRESSED_IN_ARGUMENT_AND_CHECKS','Pairwise overlap can conceal empty global acceptable intersection.','Supplement §4 uses the full relation/cover and tests the three-way obstruction.'),
 ('C1-B03','MAJOR','ADDRESSED_IN_ARGUMENT_AND_CHECKS','A numerical bit budget does not establish access to discriminating probes.','Supplement §5 states a necessary bound and tests constant-response failure.'),
 ('C1-B04','MAJOR','ADDRESSED_IN_ARGUMENT_AND_CHECKS','Destructive inquiry can leave a known answer that is no longer executable.','Supplement §7 tracks origin and current state; resource-consuming control is generated.'),
 ('C1-B05','MAJOR','ADDRESSED_IN_TEXT','Recursive capability could be smuggled into the definition of first apoautosis.','Supplement §§1,3,8 keeps the stronger property separately indexed.'),
 ('C1-B06','MAJOR','OPEN','Inherited iterator repair and verifier-scope claims need source-bound reproduction.','Preserve reproducer/patch if available; new helper tests are not substituted for the old repair.'),
 ('C1-B07','BLOCKING','OPEN','Complete frontier and primary prior-art comparison is unfinished.','Conventional mechanism lineage is acknowledged; no independent novelty or meniscus promotion.'),
 ('C1-B08','MAJOR','REFINED','Side channels, changing support boundaries and budget horizons can invalidate accounting.','Candidate2 adds explicit publication/accounting checklist below.'),
 ('C2-A01','BLOCKING','OPEN','Repeat coverage audit still cannot certify all requested source ranges.','No success gate may be obtained by narrowing the request.'),
 ('C2-B01','MAJOR','OPEN','No physical implementation or empirical comparison validates the apoautotic instance.','Model-level result only; physical input/readout/calibration/support obligations remain.'),
 ('C2-B02','MAJOR','OPEN','Same-assistant proof checks and audits are not independent specialist review.','Label audit provenance explicitly and retain external review obligation.'),
 ('C2-B03','MAJOR','OPEN','A finite family result does not supply indefinite recursive liveness or replenishment.','Finite-horizon claims only; extended dynamics require separate proofs.'),
]
if results.get('status') != 'PASS':
    findings = [(i, sev, ('ARGUMENT_ADDRESSED_EXECUTION_OPEN' if status == 'ADDRESSED_IN_ARGUMENT_AND_CHECKS' else status), finding, disposition) for i, sev, status, finding, disposition in findings]
with (ROOT/'audits/findings.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['id','severity','status','finding','disposition']); w.writerows(findings)

refinement = '''

## 13. Second-cycle accounting and publication checks

The proof's record alphabet includes every source-dependent distinction actually available to the decoder. A selected destination, physical configuration, controller initialisation or timing channel cannot be omitted merely because it is not called a memory register. A probe budget states response arity, precision, worst-case versus expected depth, and whether it is per request or cumulative across a request sequence.

For source changes, the compared contract and target family retain explicit versions. A new candidate cannot preserve old evidence merely by reusing an identifier. If an observed current repository head differs from the requested historical pin, retain both snapshots and review the delta rather than calling the historical snapshot current.

For destructive operations, every terminal answer must satisfy the original task relation and the current execution/resource conditions. For recursive transitions, the exclusion boundary and continuing support obligations are recomputed at each declared step. Contract-permitted termination is not a disturbance the organisation is instructed to defeat.

The synthetic checker supplies finite model evidence only. Its result must not be used as a substitute for missing original-source reading, exact frontier ancestry, a physical realisation map, calibrated observations, prior-art novelty, comparative benefit or independent specialist review. The complete delivery remains unapproved until the original scope is actually met.
'''
final_report = candidate_v1 + refinement
(ROOT/'REPORT.md').write_text(final_report,encoding='utf-8')
final_hash = digest(final_report.encode())

for filename, cycle, kind, candidate_hash, ids in [
 ('cycle1_read_only.json',1,'read-only coverage and substantive advancement',v1_hash,['C1-A01','C1-A02']),
 ('cycle1_adversarial.json',1,'adversarial source and candidate review',v1_hash,[r[0] for r in findings if r[0].startswith('C1-B')]),
 ('cycle2_read_only.json',2,'repeated read-only coverage and advancement',final_hash,['C2-A01']),
 ('cycle2_adversarial.json',2,'repeated adversarial candidate and retained source obligations',final_hash,[r[0] for r in findings if r[0].startswith('C2-B')])]:
    jwrite(ROOT/'audits'/filename, {'cycle':cycle,'kind':kind,'reviewer':'same assistant; not independent review',
        'candidate_sha256':candidate_hash,'overall_original_request_gate':'NOT_APPROVED',
        'source_coverage_complete':False,'finding_ids':ids,
        'new_finite_check_status':results.get('status','UNKNOWN'),
        'scope':'Authored arguments, retained findings and machine custody records; not exhaustive re-reading of unreturned source content.'})

sections = []
lines = final_report.splitlines()
starts = [(i+1,l) for i,l in enumerate(lines) if l.startswith('## ')]
for j,(start,title) in enumerate(starts):
    end = starts[j+1][0]-1 if j+1<len(starts) else len(lines)
    sections.append({'report_section':title[3:],'start_line':start,'end_line':end,
        'report_sha256':final_hash,'type':'authored report range',
        'source_review_claim':'No automatic source-line coverage credit',
        'review_status':'Same-assistant authored-argument review; full audit gate remains open'})
jwrite(ROOT/'ledgers/report_range_map.json', {'sections':sections})
jwrite(ROOT/'ledgers/coverage.json', {'overall_status':'INCOMPLETE_NOT_APPROVED',
    'original_scope_preserved':True,'new_source_semantic_credit_from_acquisition_or_copy':0,
    'prior_review_receipts':'Preserved under preserved/; reconcile exact source/version/range before aggregation.',
    'authored_report_range_map':'ledgers/report_range_map.json',
    'pending_queue':'ledgers/custody_reconciliation_queue.jsonl',
    'queue_warning':'This queue is a reconciliation index, not proof of reading and not a replacement for prior completed receipts.',
    'missing_named_inputs':missing_top,'distribution_exclusions_count':len(exclusions),
    'source_coverage_complete':False,'both_audit_cycles_approved':False,'meniscus_reached':False})

# Standalone HTML using only system fonts; no externally loaded scripts or fonts.
try:
    import markdown
    body = markdown.markdown(final_report, extensions=['fenced_code','tables'])
except ImportError:
    body = '<pre class="fallback">' + html.escape(final_report) + '</pre>'
html_doc = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Orthemology consolidation — stage-two recovery</title><style>
body{font-family:system-ui,sans-serif;max-width:960px;margin:3rem auto;padding:0 1.4rem;line-height:1.65;color:#17212b;background:#fff}h1,h2,h3{line-height:1.2;margin-top:2em}h1{font-size:2.1rem}h2{border-bottom:1px solid #cbd5df;padding-bottom:.45rem}code,pre{font-family:ui-monospace,monospace}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f8;padding:1rem;border-radius:.35rem}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd3da;padding:.5rem;text-align:left}a{color:#07569c}.fallback{background:#fff}hr{border:0;border-top:1px solid #cbd5df;margin:2.5rem 0}@media print{body{max-width:none;margin:0;font-size:10pt}h2,h3{break-after:avoid}pre,table{break-inside:avoid}}</style></head><body>'''+body+'</body></html>'
(ROOT/'REPORT.html').write_text(html_doc,encoding='utf-8')

# Include this build script only if the same conservative distribution screen allows it.
build_src = Path(__file__)
build_bytes = build_src.read_bytes()
if forbidden(build_src.name,build_bytes) is None:
    (ROOT/'verification/build_recovery.py').write_bytes(build_bytes)
else:
    # It may contain a credential-pattern literal. Do not put any matched bytes in logs.
    exclusions.append({'original_path':str(build_src),'reason':'build-script screening withheld', 'sha256':digest(build_bytes),
                       'bytes':len(build_bytes),'review_denominator_effect':'None'})

# Machine receipt is intentionally not a success claim about the full user task.
receipt={'overall_gate':'PARTIAL_NOT_APPROVED','report_sha256':final_hash,
         'preserved_exact_byte_file_occurrences':len(inventory),'distribution_exclusions':len(exclusions),
         'new_finite_check_status':results.get('status','UNKNOWN'),
         'source_coverage_complete':False,'independent_review':False,
         'new_report':str(ROOT/'REPORT.md'),'archive_name':'orthemology_consolidation_stage2_recovery.zip'}
jwrite(ROOT/'DELIVERY_RECEIPT.json',receipt)

manifest_lines=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p != ROOT/'SHA256SUMS':
        manifest_lines.append(digest(p.read_bytes())+'  '+str(p.relative_to(ROOT)))
(ROOT/'SHA256SUMS').write_text('\n'.join(manifest_lines)+'\n',encoding='utf-8')
check=subprocess.run([sys.executable,str(ROOT/'verification/verify_package.py')],capture_output=True,text=True)
(DATA/'orthemology_stage2_recovery_integrity_check.json').write_text(check.stdout,encoding='utf-8')
if check.returncode:
    raise RuntimeError('The generated packet failed its own integrity check: '+check.stdout+check.stderr)

archive=DATA/'orthemology_consolidation_stage2_recovery.zip'
temporary_archive = archive.with_suffix('.building.zip')
with zipfile.ZipFile(temporary_archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():
            z.write(p,str(Path(ROOT.name)/p.relative_to(ROOT)))
with zipfile.ZipFile(temporary_archive) as z:
    bad=z.testzip()
    if bad:
        raise RuntimeError('Archive CRC failed: '+bad)
temporary_archive.replace(archive)
for name, dest in [('REPORT.md','orthemology_consolidation_stage2_report.md'),
                   ('REPORT.html','orthemology_consolidation_stage2_report.html'),
                   ('CONTINUE.md','orthemology_consolidation_stage2_continue.md')]:
    shutil.copyfile(ROOT/name,DATA/dest)
external={**receipt,'archive':str(archive),'archive_sha256':digest(archive.read_bytes()),
          'archive_bytes':archive.stat().st_size,'package_integrity':json.loads(check.stdout)}
jwrite(DATA/'orthemology_consolidation_stage2_receipt.json',external)
print(json.dumps(external,indent=2))
