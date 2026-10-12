"""Build and byte-verify the isolated research-return archive."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,zipfile

BASE=Path(__file__).resolve().parent
NAME='Control_Restoration_Research_Return'

def digest(data):return hashlib.sha256(data).hexdigest()
def write_json(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def detached(path):
    result=digest(path.read_bytes())
    path.with_name(path.name+'.sha256').write_text(result+'  '+path.name+'\n')
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sealed-at-utc',required=True,help='UTC time from the authoritative session clock')
    args=parser.parse_args()
    supplied=datetime.fromisoformat(args.sealed_at_utc.replace('Z','+00:00'))
    if supplied.utcoffset().total_seconds()!=0:raise ValueError('UTC required')
    verification=json.loads((BASE/'verification_report.json').read_text())
    assert verification['status']=='PASS' and verification['pinned_source_hashes_verified']
    files=[p for p in BASE.iterdir() if p.is_file() and
           (p.suffix in ('.py','.md','.json') or p.name.startswith('tdd-') or p.name=='verification-run.log')
           and p.name not in ('MANIFEST.json','RECEIPT.json','SEAL_VERIFICATION.json','EXTRACTED_REPLAY_VERIFICATION.json')]
    files += [BASE/'P14'/'P14_Completed_Research_Return.zip',
              BASE/'P14'/'P14_Completed_Research_Return.zip.sha256']
    files=sorted(files,key=lambda p:p.relative_to(BASE).as_posix())
    manifest={'schema':'control-restoration-manifest-v1','scope':'isolated research return; no canonical adoption',
        'files':[{'path':p.relative_to(BASE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files]}
    write_json(BASE/'MANIFEST.json',manifest);manifest_hash=detached(BASE/'MANIFEST.json')
    receipt={'schema':'control-restoration-receipt-v1','return_id':NAME,
        'sealed_at_utc':supplied.isoformat(),'timestamp_source':'session clock.curr_time; executor wall clock not used',
        'status':'SEALED_RESEARCH_RETURN_PENDING_FRESH_SYNTHESIS_REVIEW',
        'repository_commit':'03e2604dfcef278b01c60d19b05370fcec4194b6',
        'repository_tree':'3d06e80277ce39286c94307e0f14b215bc94ed83',
        'canonical_adoption':False,'actual_world_model_validation':False,'kernel_checked_theorem_claim':False,
        'manifest_sha256':manifest_hash,'manifest_artifacts':len(files),
        'verification_report_sha256':digest((BASE/'verification_report.json').read_bytes()),
        'unit_tests_control':34,'unit_tests_P14':7,'full_replay_status':'PASS',
        'P14_replay_dependency':verification['P14_external_replay_dependency'],
        'P14_immutable_archive_sha256':'437be32e1d2a909e353abd376f36bf99968c6679f1ccbcb401301aa48f8a4d37',
        'claim_boundaries':'INTERFACE_MAP.json','review_request':'Fresh synthesis review of combined assumptions, proofs and implementation scope; no automatic adoption.'}
    write_json(BASE/'RECEIPT.json',receipt);receipt_hash=detached(BASE/'RECEIPT.json')
    archive=BASE/(NAME+'.zip')
    members=files+[BASE/'MANIFEST.json',BASE/'MANIFEST.json.sha256',BASE/'RECEIPT.json',BASE/'RECEIPT.json.sha256']
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in members:z.write(p,NAME+'/'+p.relative_to(BASE).as_posix())
    archive_hash=detached(archive)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for item in manifest['files']:
            data=z.read(NAME+'/'+item['path'])
            assert len(data)==item['bytes'] and digest(data)==item['sha256']
        assert digest(z.read(NAME+'/MANIFEST.json'))==manifest_hash
        assert digest(z.read(NAME+'/RECEIPT.json'))==receipt_hash
        assert digest(z.read(NAME+'/P14/P14_Completed_Research_Return.zip'))==receipt['P14_immutable_archive_sha256']
    verification={'schema':'control-restoration-seal-verification-v1','archive':archive.name,
        'archive_bytes':archive.stat().st_size,'archive_sha256':archive_hash,
        'receipt_sha256':receipt_hash,'manifest_sha256':manifest_hash,
        'manifest_artifacts_read_back':len(files),'zip_CRC':'PASS','all_artifact_hashes':'PASS','P14_predecessor_identity':'PASS'}
    write_json(BASE/'SEAL_VERIFICATION.json',verification)
    print(json.dumps(verification,indent=2))

if __name__=='__main__':main()
