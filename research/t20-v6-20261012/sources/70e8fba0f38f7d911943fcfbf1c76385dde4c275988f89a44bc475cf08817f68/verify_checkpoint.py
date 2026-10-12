#!/usr/bin/env python3
"""Fresh-process, read-only verification of the outer seal and nested original.
Writes its report outside the archive; grants no theorem/adoption/review credit.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

CONTROL = {'MANIFEST.json','MANIFEST.json.sha256','RECEIPT.json','RECEIPT.json.sha256'}
INPUT_SHA = '050aac77db52ad70e0155bbeb76f903a4dae65a36977a4159c8dcaf5634bcab0'

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)

def members(z: zipfile.ZipFile) -> dict[str, bytes]:
    infos = z.infolist()
    names = [i.filename for i in infos]
    require(len(names)==len(set(names)), 'Duplicate ZIP names')
    for i in infos:
        n=i.filename; p=PurePosixPath(n)
        require(not i.is_dir() and not p.is_absolute() and '..' not in p.parts
            and '\\' not in n and str(p)==n, f'Unsafe/noncanonical member: {n}')
        require(((i.external_attr>>16)&0o170000)!=0o120000, f'Symlink member: {n}')
    require(z.testzip() is None,'ZIP CRC failure')
    return {n:z.read(n) for n in names}

def verify_rows(data: dict[str,bytes], rows: list[dict], key: str = 'path', blob: bool = False) -> int:
    seen=set()
    for row in rows:
        n=row[key]
        require(n not in seen,f'Duplicate binding: {n}');seen.add(n)
        require(n in data,f'Missing bound member: {n}')
        b=data[n]
        require(len(b)==row['bytes'],f'Byte-count mismatch: {n}')
        require(sha(b)==row['sha256'],f'SHA-256 mismatch: {n}')
        if blob:
            actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            require(actual==row['git_blob'],f'Git blob mismatch: {n}')
    return len(rows)

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--zip',type=Path,required=True)
    ap.add_argument('--sha256',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    require(not a.out.exists(),'Refusing to overwrite a verification report')
    report={'schema':'orthemology-p03-fresh-reopen-v1',
        'started_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'verifier_sha256':sha(Path(__file__).read_bytes()),
        'independent_process':True,'external_review_credit':False,
        'kernel_credit':False,'owner_adoption_credit':False,'historical_recovery_credit':False}
    try:
        raw=a.zip.read_bytes(); archive_sha=sha(raw)
        expected_line=f'{archive_sha}  {a.zip.name}\n'
        require(a.sha256.read_text()==expected_line,'Detached archive digest mismatch')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            data=members(z)
        require(CONTROL<=data.keys(),'Missing seal controls')
        m=json.loads(data['MANIFEST.json']); r=json.loads(data['RECEIPT.json'])
        require(set(x['path'] for x in m['files']).isdisjoint(CONTROL),'Circular manifest control entry')
        require(set(data)=={x['path'] for x in m['files']}|CONTROL,'Member-set mismatch')
        payload_count=verify_rows(data,m['files'])
        for name in ('MANIFEST.json','RECEIPT.json'):
            require(data[name+'.sha256']==f'{sha(data[name])}  {name}\n'.encode(),
                    f'Invalid detached inner digest: {name}')
        require(r['manifest_sha256']==sha(data['MANIFEST.json']),'Receipt/manifest link mismatch')
        require(r['manifest_sidecar_sha256']==sha(data['MANIFEST.json.sha256']),
                'Receipt/manifest-sidecar link mismatch')
        require(r['payload_files']==payload_count and r['archive_members']==len(data),
                'Receipt population mismatch')
        require(r['obligations']=={'U03':'PARTIAL','U04':'PARTIAL','Q1f':'PARTIAL'},'Unexpected obligation statuses')
        original=data['inputs/Orthemology_Pro_P03_Engine_Refinement.zip']
        require(sha(original)==INPUT_SHA and len(original)==1819667,'Original input identity mismatch')
        with zipfile.ZipFile(io.BytesIO(original)) as z:
            inp=members(z)
        im=json.loads(inp['CHECKPOINT_MANIFEST.json'])
        require(set(inp)=={x['path'] for x in im['files']}|{'CHECKPOINT_MANIFEST.json'},
                'Original manifest population mismatch')
        ic=verify_rows(inp,im['files'])
        ir=json.loads(inp['RECEIPT.json'])
        irc=verify_rows(inp,ir['output_hashes'])
        require(inp['RECEIPT.json.sha256']==f"{sha(inp['RECEIPT.json'])}  RECEIPT.json\n".encode(),
                'Original receipt detached mismatch')
        sc=verify_rows(inp,json.loads(inp['SOURCE_INVENTORY.json']),'packet_path',True)
        pc=verify_rows(inp,json.loads(inp['accepted-evidence/PROJECTION_BINDINGS.json']),'packet_path')
        ob={row['id']:verify_rows(inp,row['source_bindings'],'packet_path',True)
            for row in json.loads(inp['OBLIGATIONS.json'])}
        supplemental=json.loads(data['inputs/SUPPLEMENTAL_IDENTITIES.json'])
        sup=verify_rows(data,supplemental,'path',True)
        # Proposed changes retain exact preimages and test subject postimages.
        patchmap=json.loads(data['proposal/PATCH_MAP.json'])
        for repo,row in patchmap.items():
            rel=repo.removeprefix('experiments/orthemology-v5/source/')
            require(data['proposal/preimages/'+rel]==inp['source-main/'+repo],
                    f'Changed preimage: {repo}')
            require(sha(data['proposal/preimages/'+rel])==row['preimage_sha256'],f'Preimage digest: {repo}')
            require(sha(data['proposal/postimages/'+rel])==row['postimage_sha256'],f'Postimage digest: {repo}')
        final_runs={}
        for mode in ('normal','optimised'):
            total=0
            for kind,count in [('suite',183),('regressions',2),('contract',12),('exporter',2)]:
                label=f'final-{kind}-{mode}'
                cmd=json.loads(data[f'evidence/{label}/command.json'])
                require(cmd['exit_code']==0 and not cmd['timed_out'],f'Final run nonzero: {label}')
                for stream in ('stdout','stderr'):
                    b=data[f'evidence/{label}/{stream}.bin']
                    require(len(b)==cmd[stream]['bytes'] and sha(b)==cmd[stream]['sha256'],
                            f'Raw stream binding mismatch: {label}/{stream}')
                text=data[f'evidence/{label}/stderr.bin'].decode()
                require(f'Ran {count} tests in ' in text and '\nOK\n' in text,f'Unexpected unittest result: {label}')
                total+=count
            final_runs[mode]=total
        report.update({'status':'PASS','archive':{'filename':a.zip.name,'bytes':len(raw),'sha256':archive_sha},
          'payload_files_verified':payload_count,'control_members_verified':len(CONTROL),
          'archive_members_verified':len(data),'uncompressed_bytes':sum(map(len,data.values())),
          'outer_crc':'PASS','exact_member_set':'PASS','control_hash_chain':'PASS',
          'original_input':{'sha256':INPUT_SHA,'archive_members':len(inp),'crc':'PASS',
            'manifest_bindings':ic,'receipt_output_bindings':irc,'source_bindings':sc,
            'projection_bindings':pc,'obligation_source_bindings':ob},
          'supplemental_source_bindings':sup,'exact_proposed_preimages_postimages':len(patchmap),
          'final_test_methods_per_mode':final_runs,
          'members':[{'path':n,'bytes':len(b),'sha256':sha(b),
            'verification':'CONTROL_HASH_CHAIN_AND_OUTER_DIGEST' if n in CONTROL else 'MANIFEST_AND_OUTER_DIGEST'}
            for n,b in sorted(data.items())]})
    except Exception as exc:
        report.update({'status':'FAIL','error':repr(exc)})
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
    return 0 if report['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
