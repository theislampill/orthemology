#!/usr/bin/env python3
"""Expected-rejection tests for archive membership, paths, types and byte hashes."""
from pathlib import Path
import argparse,json,stat,sys,tempfile,warnings,zipfile
sys.dont_write_bytecode=True
from safe_extract import extract
p=argparse.ArgumentParser();p.add_argument('archive');a=p.parse_args()
with zipfile.ZipFile(a.archive) as z:original=[(i,z.read(i)) for i in z.infolist()]
prefix=original[0][0].filename.split('/')[0]+'/'
target=next(i.filename for i,d in original if i.filename.endswith('/retained-skyline-likelihood/RESULT.md'))
cases=['payload_mutation','missing_member','extra_member','manifest_mutation','traversal','absolute_path','backslash_path','duplicate_member','symlink','multiple_roots']
rows=[]
with tempfile.TemporaryDirectory(prefix='t20-tenth-negative-') as temp:
    temp=Path(temp)
    for case in cases:
        archive=temp/(case+'.zip')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
                for info,data in original:
                    if case=='missing_member' and info.filename==target:continue
                    if case=='payload_mutation' and info.filename==target:data+=b'\nDELIBERATE TEST MUTATION\n'
                    if case=='manifest_mutation' and info.filename==prefix+'MANIFEST.json':data+=b' '
                    z.writestr(info,data)
                if case=='extra_member':z.writestr(prefix+'unexpected.txt',b'test')
                if case=='traversal':z.writestr(prefix+'../escape.txt',b'test')
                if case=='absolute_path':z.writestr('/escape.txt',b'test')
                if case=='backslash_path':z.writestr(prefix+'..\\escape.txt',b'test')
                if case=='duplicate_member':z.writestr(target,b'test')
                if case=='symlink':
                    info=zipfile.ZipInfo(prefix+'unsafe-link');info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(info,b'../../outside')
                if case=='multiple_roots':z.writestr('other-root/file.txt',b'test')
        destination=temp/(case+'-extract')
        try:
            extract(archive,destination)
            row={'case':case,'status':'FAIL_UNEXPECTED_ACCEPTANCE'}
        except (AssertionError,ValueError,KeyError,zipfile.BadZipFile) as exc:
            row={'case':case,'status':'PASS_EXPECTED_REJECTION','reason':str(exc),'no_destination_created':not destination.exists()}
        rows.append(row)
report={'status':'PASS' if all(r['status']=='PASS_EXPECTED_REJECTION' and r['no_destination_created'] for r in rows) else 'FAIL','controls':rows,'scope':'Fresh disposable malformed archives; expected rejections validate packaging guards, not mathematical claims.'}
print(json.dumps(report,indent=2));assert report['status']=='PASS'
