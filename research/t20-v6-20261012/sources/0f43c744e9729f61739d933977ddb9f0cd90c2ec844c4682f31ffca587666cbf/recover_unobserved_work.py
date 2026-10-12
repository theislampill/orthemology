#!/usr/bin/env python3
"""Recover bytes and machine evidence without assigning semantic-reading credit.
Original files are never changed. This is an operational recovery utility,
not a theorem verifier, a Lean build, or a semantic-reading certificate.
"""
from __future__ import annotations
import hashlib, io, json, os, re, shutil, stat, sys, tempfile, time, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path('/mnt/data')
DEST=ROOT/'t20_recovery_checkpoint_20261010'
DEST.mkdir(exist_ok=True)
EVID=DEST/'machine_evidence'; EVID.mkdir(exist_ok=True)
SAVED=DEST/'preserved'; SAVED.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def writej(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
source_names=[
'T20bigupdatenext.zip','T20bigupdateprev.zip','T20bigupdate(1).zip',
'T20bigupdateprev03.zip','T20bigupdateprev02.zip',
'T20_Scriptural_Recovery_Supplement_20261009.zip',
'T20_Warranted_Discrimination_Research_and_Lean_20261009.zip',
'Orthemology_T20_Whole_Corpus_Synthesis_20261010.zip',
'Orthemology_T20_Whole_Corpus_Synthesis_20261010.VERIFICATION.json',
'Orthemology_T20_All_Delivered_Research_Field_Guide_20261010.md',
'Orthemology_T20_Cross_Front_Mathematical_Synthesis_20261010.md',
'Orthemology_T20_Foundational_Crosswalk_20261010.md',
'Orthemology_T20_Dot_Synthesis_Handoff_20261010.md',
'Orthemology_T20_Corpus_Register_20261010.md',
'Orthemology_T20_Coverage_Limits_20261010.md']
inputs=[]
for name in source_names:
    p=ROOT/name
    if not p.is_file() or p.is_symlink():
        inputs.append({'name':name,'status':'NOT_RECOVERED_IN_RUNTIME'});continue
    data=p.read_bytes(); h=sha(data)
    target=SAVED/name
    if target.exists() and sha(target.read_bytes())!=h:
        raise RuntimeError('Refuse overwrite of different preserved file: '+str(target))
    if not target.exists(): target.write_bytes(data)
    inputs.append({'name':name,'bytes':len(data),'sha256':h,'status':'BYTE_COPY_REOPENED','copy_sha256':sha(target.read_bytes())})
writej(EVID/'original_input_identities.json',inputs)

# Recover existing working source, tests, reports and logs, but not build caches.
skip_dirs={'.git','.lake','.venv','venv','node_modules','__pycache__','cache','caches','toolchains','bin','obj'}
skip_suffix={'.olean','.ilean','.o','.a','.so','.dll','.exe','.pyc','.whl','.ttf','.otf','.woff','.woff2'}
workspace_names=['t20_complete_work','t20_crossfront_delivery','t20_synthesis_work']
workspace_records=[]
for name in workspace_names:
    source=ROOT/name
    if not source.is_dir():
        workspace_records.append({'workspace':name,'status':'NOT_FOUND'});continue
    for folder,dirs,filenames in os.walk(source,followlinks=False):
        dirs[:]=[d for d in dirs if d not in skip_dirs and not (Path(folder)/d).is_symlink()]
        for filename in filenames:
            p=Path(folder)/filename
            if p.is_symlink() or p.suffix.lower() in skip_suffix: continue
            if p.stat().st_size>100_000_000: continue
            rel=p.relative_to(source); target=SAVED/'working_copy'/name/rel
            data=p.read_bytes(); target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists() and target.read_bytes()!=data:
                alt=target.with_name(target.name+'.recovered-'+sha(data)[:12]); target=alt
            if not target.exists(): target.write_bytes(data)
            workspace_records.append({'workspace':name,'source_relative_path':str(rel),'saved_relative_path':str(target.relative_to(DEST)), 'bytes':len(data),'sha256':sha(data),'status':'BYTE_COPY_REOPENED'})
writej(EVID/'working_recovery.json',workspace_records)

# Recursive custody inventory of original source archives; derivative archive counted separately.
archive_rows=[]; member_rows=[]; visited=set(); issues=[]; decoded={}; total_uncompressed=0
MAX_TOTAL=3_000_000_000; MAX_MEMBER=300_000_000
text_ext={'.md','.txt','.lean','.py','.json','.jsonl','.yaml','.yml','.toml','.tex','.csv','.sh','.log','.rst','.html','.xml','.patch','.diff','.cfg','.ini'}
def safe_name(name):
    if '\\' in name or '\x00' in name: return False
    q=PurePosixPath(name)
    return not q.is_absolute() and '..' not in q.parts and not re.match(r'^[A-Za-z]:',name)
def scan(data,label,depth=0):
    global total_uncompressed
    h=sha(data)
    if h in visited: return
    if depth>20: issues.append({'path':label,'issue':'DEPTH_LIMIT'});return
    visited.add(h)
    try: z=zipfile.ZipFile(io.BytesIO(data))
    except Exception as e:
        issues.append({'path':label,'issue':'ZIP_OPEN_ERROR','detail':str(e)});return
    bad=z.testzip()
    archive_rows.append({'sha256':h,'bytes':len(data),'first_location':label,'member_count':len(z.infolist()),'crc_status':'PASS' if bad is None else 'FAIL','bad_member':bad})
    if bad: issues.append({'path':label,'issue':'CRC_ERROR','member':bad})
    seen_names=set()
    for info in z.infolist():
        nm=info.filename
        row={'archive_sha256':h,'path':nm,'bytes':info.file_size,'directory':info.is_dir()}
        mode=info.external_attr>>16
        if nm in seen_names: issues.append({'path':label+'!'+nm,'issue':'DUPLICATE_MEMBER_NAME'})
        seen_names.add(nm)
        if not safe_name(nm) or stat.S_ISLNK(mode):
            issues.append({'path':label+'!'+nm,'issue':'UNSAFE_OR_SYMLINK_MEMBER'})
        if info.is_dir(): member_rows.append(row);continue
        if info.file_size>MAX_MEMBER or total_uncompressed+info.file_size>MAX_TOTAL:
            row['status']='RESOURCE_BOUND_NOT_READ';issues.append({'path':label+'!'+nm,'issue':row['status']});member_rows.append(row);continue
        b=z.read(info);total_uncompressed+=len(b); row['sha256']=sha(b)
        suffix=Path(nm).suffix.lower()
        if suffix in text_ext:
            try:
                text=b.decode('utf-8-sig')
                row['text_status']='DECODED_NOT_SEMANTICALLY_READ'
                row['lines']=len(text.splitlines())
                if row['sha256'] not in decoded:
                    decoded[row['sha256']]={'first_location':label+'!'+nm,'lines':row['lines'],'bytes':len(b)}
            except UnicodeDecodeError: row['text_status']='NON_UTF8_NOT_INTERPRETED'
        member_rows.append(row)
        if suffix=='.zip': scan(b,label+'!'+nm,depth+1)
    z.close()
for rec in inputs:
    if rec.get('status')=='BYTE_COPY_REOPENED' and rec['name'].endswith('.zip') and not rec['name'].startswith('Orthemology_T20_Whole_Corpus'):
        scan((SAVED/rec['name']).read_bytes(),rec['name'])
writej(EVID/'recursive_archives.json',archive_rows)
writej(EVID/'recursive_members.json',member_rows)
writej(EVID/'recursive_issues.json',issues)
writej(EVID/'decoded_text_inventory_NOT_READING_CREDIT.json',decoded)

status={
 'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'delivery_kind':'OPERATIONAL_RECOVERY_NOT_COMPLETED_SYNTHESIS',
 'original_inputs_found':sum(x.get('status')=='BYTE_COPY_REOPENED' for x in inputs),
 'original_inputs_missing':[x['name'] for x in inputs if x.get('status')!='BYTE_COPY_REOPENED'],
 'distinct_source_zip_objects':len(archive_rows),'archive_member_occurrences':len(member_rows),
 'source_archive_crc_failures':sum(r['crc_status']!='PASS' for r in archive_rows),
 'recursive_inventory_issues':len(issues),'recovered_working_files':sum(x.get('status')=='BYTE_COPY_REOPENED' for x in workspace_records),
 'unique_utf8_text_objects':len(decoded),
 'assistant_readback':'UNAVAILABLE_AT_AUTHORING',
 'semantic_reading':'NO_NEW_CREDIT_FROM_THIS_SCRIPT',
 'lean_rebuild':'NOT_EXECUTED_BY_THIS_SCRIPT',
 'research_tests':'NOT_EXECUTED_BY_THIS_SCRIPT',
 'completion':'NOT_CLAIMED'}
writej(DEST/'RECOVERY_STATE.json',status)
(DEST/'START_HERE.md').write_text('''# T20 operational recovery checkpoint\n\nThis is NOT the completed all-T20 synthesis. It preserves original supplied bytes and recoverable working sources after the assistant lost all readable tool results.\n\nRead `RECOVERY_STATE.json`, then `machine_evidence/original_input_identities.json` and `machine_evidence/working_recovery.json`. The recursive inventory distinguishes exact duplicate archive objects from archive-member occurrences. UTF-8 decoding is NOT semantic reading. No new Lean or research-test pass is asserted by this recovery utility.\n\n## Resume the exact unfinished task\n\nThe owner requests a freshly read, fully verified synthesis of all supplied T20 research, with the plain-language guide, cross-front mathematical contributions, foundational/philosophical crosswalk and a handoff for Dot. Preserve the old synthesis and source archives unchanged. Recover the working copy before redoing anything.\n\nPrevious continuation reported 118 unique ZIPs and 17,042 archive members. Its discovered corrections were one-shot iterator consumption in the reference implementation and the need for an explicit jump-timing condition in the hybrid preservation theorem. These are pointers requiring actual code/log readback, not newly verified facts.\n\n1. Establish a functioning tool-result readback with a trivial command.\n2. Read and reconcile the saved work, tests, ledgers, manifests and all distinct substantive source bodies. Do not equate a file-open/hash/decode with semantic reading.\n3. Verify the reported iterator repairs and hybrid timing correction with failing controls and successful replays.\n4. Rerun the derivative packet tests and available source-package verifiers in disposable copies, binding outputs and dependency identities. Record inaccessible/omitted external inputs separately.\n5. Finish the guide and cross-front contributions from actual source reading, not filename extrapolation.\n6. Seal and reopen the successor; claim only the exact reading and verification scopes actually observed.\n\nThe active programme remains T20. Packaging does not close the research, adopt principles, authorise repository edits, or authorise merge.\n''',encoding='utf-8')
# Include the exact recovery utility so the custody work can be reproduced.
shutil.copy2(Path(__file__),DEST/'recover_unobserved_work.py')
manifest=[]
for p in sorted(DEST.rglob('*')):
    if p.is_file() and p.name!='MANIFEST.json':
        b=p.read_bytes();manifest.append({'path':str(p.relative_to(DEST)),'bytes':len(b),'sha256':sha(b)})
writej(DEST/'MANIFEST.json',{'purpose':'byte custody only','files':manifest})
out=ROOT/'Orthemology_T20_Operational_Recovery_20261010.zip'
tmp=out.with_suffix('.zip.tmp')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
    for p in sorted(DEST.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(DEST))
os.replace(tmp,out)
# Independent reopen against every manifested file: never just write-and-assume.
with zipfile.ZipFile(out) as z:
    if z.testzip() is not None: raise RuntimeError('Recovery ZIP CRC failed')
    actual=set(z.namelist()); expected={r['path'] for r in manifest}|{'MANIFEST.json'}
    if actual!=expected: raise RuntimeError('Recovery ZIP inventory mismatch')
    for r in manifest:
        b=z.read(r['path'])
        if len(b)!=r['bytes'] or sha(b)!=r['sha256']: raise RuntimeError('Recovery member mismatch: '+r['path'])
receipt={'archive':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'zip_crc':'PASS','manifest_reopen':'PASS','manifested_payload_files':len(manifest),'semantic_reading':'NOT_CERTIFIED','original_task_complete':False,'assistant_observation':'NOT_CLAIMED','state':status}
writej(ROOT/'Orthemology_T20_Operational_Recovery_20261010.RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
