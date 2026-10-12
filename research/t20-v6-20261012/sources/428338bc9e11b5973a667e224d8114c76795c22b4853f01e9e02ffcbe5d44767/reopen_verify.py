#!/usr/bin/env python3
"""Independent fresh-process ZIP readback. Standard library only; no extraction or execution."""
from __future__ import annotations
from pathlib import Path,PurePosixPath
import datetime,hashlib,io,json,stat,sys,zipfile

def digest(data: bytes) -> str:return hashlib.sha256(data).hexdigest()
def verify(archive: Path,seal: dict) -> dict:
    errors=[];member_hashes=[]
    def check(ok: bool,msg: str) -> None:
        if not ok:errors.append(msg)
    data=archive.read_bytes()
    check(digest(data)==seal['zip_sha256'],'outer ZIP SHA-256 mismatch')
    check(len(data)==seal['zip_bytes'],'outer ZIP byte count mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        check(len(names)==len(set(names)),'duplicate ZIP member names')
        check(len(names)==seal['zip_members'],'member count mismatch')
        for info in infos:
            p=PurePosixPath(info.filename)
            check(not p.is_absolute() and '..' not in p.parts and not info.is_dir(),'unsafe or unexpected directory path '+info.filename)
            check(not stat.S_ISLNK(info.external_attr>>16),'symlink member '+info.filename)
        check(z.testzip() is None,'CRC failure')
        manifest_bytes=z.read('CHECKPOINT_MANIFEST.json');manifest=json.loads(manifest_bytes)
        check(digest(manifest_bytes)==seal['manifest_sha256'],'manifest detached hash mismatch')
        expected={r['path']:r for r in manifest['files']}
        check(len(expected)==len(manifest['files']),'duplicate manifest path')
        check(set(names)==set(expected)|{'CHECKPOINT_MANIFEST.json'},'manifest/member population differs')
        for info in infos:
            b=z.read(info);h=digest(b)
            member_hashes.append({'path':info.filename,'bytes':len(b),'sha256':h})
            if info.filename=='CHECKPOINT_MANIFEST.json':
                check(h==seal['manifest_sha256'],'manifest self-member hash mismatch')
            else:
                e=expected.get(info.filename,{})
                check(e.get('bytes')==len(b) and e.get('sha256')==h,'member hash mismatch '+info.filename)
        receipt_bytes=z.read('RECEIPT.json');receipt=json.loads(receipt_bytes)
        check(digest(receipt_bytes)==seal['receipt_sha256'],'receipt detached seal mismatch')
        check(z.read('RECEIPT.json.sha256').decode().split()[0]==digest(receipt_bytes),'receipt detached digest mismatch')
        for r in receipt['output_hashes']:
            b=z.read(r['path']);check(len(b)==r['bytes'] and digest(b)==r['sha256'],'receipt output binding '+r['path'])
        # The received original is preserved exactly and compared member-for-member against its extracted copy.
        original=z.read('inputs/Orthemology_Pro_P02_Measure_CV_R_C.zip')
        check(digest(original)=='70630d5b703fb3262e123b8424c19580e95bf604db3e9eb5d364653c333fdf13','original input archive identity mismatch')
        check(len(original)==1809066,'original input byte count mismatch')
        with zipfile.ZipFile(io.BytesIO(original)) as zi:
            check(zi.testzip() is None,'nested input CRC failure')
            original_names=zi.namelist()
            check(len(original_names)==620,'nested input population mismatch')
            for name in original_names:
                check(zi.read(name)==z.read('inputs/packet/'+name),'nested input/extracted copy differs '+name)
            inventory=json.loads(zi.read('SOURCE_INVENTORY.json'))
            for r in inventory:
                b=zi.read(r['packet_path']);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
                check(len(b)==r['bytes'] and digest(b)==r['sha256'] and blob==r['git_blob'],'nested source identity '+r['packet_path'])
        for f in ['CENSUS_RESULT.json','mealy_3state.jsonl']:
            check(z.read('evidence/finite-normal/'+f)==z.read('evidence/finite-optimised/'+f),'repeat mismatch '+f)
        rows=z.read('evidence/finite-normal/mealy_3state.jsonl').splitlines()
        check(len(rows)==46656,'raw finite row count mismatch')
        for i,line in enumerate(rows):
            r=json.loads(line);code=r['encoding']
            check(r['id']==i and len(code)==6 and all(type(c) is int and 0<=c<6 for c in code),'raw row encoding '+str(i))
            check(sum(c*6**(5-j) for j,c in enumerate(code))==i,'raw population order/gap '+str(i))
        obligations=json.loads(z.read('OBLIGATION_RESULTS.json'))['results']
        check({r['id'] for r in obligations}=={'U05','U08','CV-R','CV-C','Q1c'},'obligation inventory mismatch')
        check(all(r['obligation_status']=='PARTIAL' and not r['kernel_credit'] for r in obligations),'unexpected obligation/kernel promotion')
        check(receipt['main_commit']=='03e2604dfcef278b01c60d19b05370fcec4194b6' and receipt['main_tree']=='3d06e80277ce39286c94307e0f14b215bc94ed83','canonical identity record mismatch')
        check(receipt['repository_modified'] is False and receipt['kernel_verified'] is False,'unexpected effect or formal-credit marker')
        for key in ['FINAL_TEST_ROOT_NORMAL','FINAL_TEST_ROOT_OPTIMISED','CENSUS_NORMAL','CENSUS_OPTIMISED_REPEAT','HANDOFF_SHELL_SYNTAX']:
            c=json.loads(z.read('evidence/'+key+'/COMMAND.json'))
            check(c['exit_code']==0,'unexpected executed exit '+key)
            for stream in ['stdout','stderr']:
                b=z.read('evidence/'+key+'/'+stream+'.bin')
                check(digest(b)==c[stream+'_sha256'] and len(b)==c[stream+'_bytes'],'raw stream identity '+key+':'+stream)
    return {'schema':'orthemology-p02-independent-reopen-v1','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not errors else 'FAIL','archive':archive.name,'zip_bytes':len(data),'zip_sha256':digest(data),'hashed_and_verified_zip_members':len(member_hashes),'manifested_payload_members':len(expected),'manifest_sha256':digest(manifest_bytes),'manifest_self_hash_checked_against_detached_seal':True,'nested_input_members_compared':len(original_names),'nested_source_SHA256_and_git_blob_checks':len(inventory),'raw_finite_rows_inventory_checked':len(rows),'errors':errors,'member_hashes':member_hashes,'scope':'Archive integrity, exact retained input copies and receipt/result consistency. Not mathematical/kernel proof or independent external review.'}

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: reopen_verify.py ARCHIVE.zip SEAL.json REPORT.json')
    archive,seal_path,report_path=map(Path,sys.argv[1:])
    try: report=verify(archive,json.loads(seal_path.read_text()))
    except Exception as exc:report={'status':'FAIL','errors':[type(exc).__name__+': '+str(exc)]}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='member_hashes'},indent=2))
    raise SystemExit(0 if report['status']=='PASS' else 1)
