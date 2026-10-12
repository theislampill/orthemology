#!/usr/bin/env python3
"""Reopen a closed P01 ZIP and verify its complete layered integrity seal.

No extraction, imports from the archive, mathematical acceptance, or digital
signature/authorship verification. Every member is covered by the outer digest;
non-seal members additionally require the manifest, and seal members are chained.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,re,stat,sys,zipfile
from pathlib import Path,PurePosixPath

SEALS={'MANIFEST.json','RECEIPT.json','RECEIPT.json.sha256'}
DIGEST=re.compile(r'^[0-9a-f]{64}$')

def h(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def need(condition:bool,message:str)->None:
    if not condition:
        raise ValueError(message)

def detached(data:bytes,expected_name:str)->str:
    lines=data.decode('utf-8').splitlines()
    need(len(lines)==1,'detached digest must contain exactly one line')
    parts=lines[0].split(maxsplit=1)
    need(len(parts)==2 and DIGEST.fullmatch(parts[0]) is not None,'malformed detached digest')
    need(parts[1].lstrip('*')==expected_name,'detached digest filename mismatch')
    return parts[0]

def verify_checkpoint(path:Path|str,sha256_file:Path|str)->dict:
    path=Path(path);side=Path(sha256_file)
    result={'status':'FAIL','archive_filename':path.name,'errors':[],
      'verification_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'mathematical_or_kernel_acceptance':False,'external_review_credit':False,
      'signature_or_authorship_verification':False,'members_verified':0}
    try:
        raw=path.read_bytes();digest=h(raw)
        result.update(archive_bytes=len(raw),archive_sha256=digest)
        need(detached(side.read_bytes(),path.name)==digest,'outer archive digest mismatch')
        # zipfile reads the on-disk archive afresh, not the builder's buffers.
        with zipfile.ZipFile(path,'r') as archive:
            info=archive.infolist();names=[x.filename for x in info]
            need(len(names)==len(set(names)),'duplicate ZIP member')
            need(SEALS.issubset(names),'missing seal member')
            for i in info:
                q=PurePosixPath(i.filename)
                need(not q.is_absolute() and '..' not in q.parts and '\\' not in i.filename
                     and ':' not in i.filename and q.as_posix()==i.filename
                     and not i.is_dir(),'unsafe/noncanonical member path: '+i.filename)
                need(not stat.S_ISLNK(i.external_attr>>16),'symlink member: '+i.filename)
                need(not (i.flag_bits&1),'encrypted ZIP member')
            need(archive.testzip() is None,'ZIP CRC failure')
            data={n:archive.read(n) for n in names}
            # Detect change between the initial digest and later ZIP read.
            need(h(path.read_bytes())==digest,'archive changed during verification')
            rec=data['RECEIPT.json'];man=data['MANIFEST.json']
            need(detached(data['RECEIPT.json.sha256'],'RECEIPT.json')==h(rec),
                 'receipt detached digest mismatch')
            receipt=json.loads(rec);manifest=json.loads(man)
            b=receipt['manifest_binding']
            need(b['path']=='MANIFEST.json' and b['sha256']==h(man) and b['bytes']==len(man),
                 'manifest-to-receipt binding mismatch')
            need(manifest['algorithm']=='sha256','unsupported manifest algorithm')
            excluded=manifest['excluded_seal_members']
            need(len(excluded)==len(set(excluded)) and set(excluded)==SEALS,'wrong seal exclusions')
            rows=manifest['files'];listed=[r['path'] for r in rows]
            need(len(listed)==len(set(listed)),'duplicate manifest path')
            need(set(listed)==set(names)-SEALS,'manifest coverage mismatch')
            need(manifest['payload_file_count']==len(rows),'payload count mismatch')
            need(manifest['payload_bytes']==sum(len(data[n]) for n in listed),'payload size mismatch')
            for row in rows:
                n=row['path'];payload=data[n]
                need(row['bytes']==len(payload) and row['sha256']==h(payload),
                     'payload hash/length mismatch: '+n)
            identities=[]
            for n in sorted(names):
                scope='manifest_and_outer_archive'
                if n=='MANIFEST.json':scope='receipt_binding_and_outer_archive'
                elif n=='RECEIPT.json':scope='receipt_detached_digest_and_outer_archive'
                elif n=='RECEIPT.json.sha256':scope='outer_archive_digest'
                identities.append({'path':n,'bytes':len(data[n]),'sha256':h(data[n]),'verified_by':scope})
            result.update(status='PASS',zip_crc='PASS',exact_member_coverage=True,
                payload_files_verified=len(rows),seal_members_verified=3,members_verified=len(names),
                uncompressed_bytes=sum(len(x) for x in data.values()),
                manifest_sha256=h(man),receipt_sha256=h(rec),all_member_identities=identities)
    except Exception as e:
        result['errors'].append(f'{type(e).__name__}: {e}')
    result['verification_finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    return result

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path);p.add_argument('--sha256-file',type=Path,required=True)
    p.add_argument('--report',type=Path,help='new external report; never placed inside the already sealed ZIP')
    a=p.parse_args()
    if a.report and a.report.exists():p.error('report path already exists; overwrite refused')
    result=verify_checkpoint(a.archive,a.sha256_file)
    rendered=json.dumps(result,indent=2)+'\n'
    if a.report:a.report.write_text(rendered)
    print(rendered,end='')
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
