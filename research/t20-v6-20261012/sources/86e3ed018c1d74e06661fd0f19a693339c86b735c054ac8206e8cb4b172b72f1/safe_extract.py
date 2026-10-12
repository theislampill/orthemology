#!/usr/bin/env python3
"""Safely extract a sealed checkpoint ZIP into a new directory, then validate it."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,stat,zipfile
def extract(archive,destination):
    destination=Path(destination);assert not destination.exists(),'Destination must be new'
    with zipfile.ZipFile(archive) as z:
        entries=z.infolist();names=[i.filename for i in entries]
        assert len(names)==len(set(names)),'Duplicate member'
        roots=set()
        for i in entries:
            p=PurePosixPath(i.filename)
            assert i.filename and '\\' not in i.filename and not p.is_absolute() and '..' not in p.parts,'Unsafe member'
            assert ':' not in p.parts[0] and p.parts[0] not in {'.','..'},'Unsafe root'
            assert str(p)==i.filename and len(p.parts)>1,'Non-canonical member'
            assert not i.is_dir(),'Only explicit file members accepted'
            mode=i.external_attr>>16
            assert stat.S_IFMT(mode) in {0,stat.S_IFREG},'Unsafe file type'
            assert not (i.flag_bits&1),'Encrypted member unsupported'
            roots.add(p.parts[0])
        assert len(roots)==1,'Multiple roots'
        rootname=next(iter(roots));prefix=rootname+'/'
        manifest=json.loads(z.read(prefix+'MANIFEST.json'))
        assert hashlib.sha256(z.read(prefix+'MANIFEST.json')).hexdigest()==z.read(prefix+'MANIFEST.sha256').decode().split()[0],'Manifest digest mismatch'
        assert len(manifest['files'])==manifest['file_count']
        assert len({r['path'] for r in manifest['files']})==manifest['file_count'],'Duplicate manifest record'
        expected={prefix+r['path'] for r in manifest['files']}|{prefix+'MANIFEST.json',prefix+'MANIFEST.sha256'}
        assert set(names)==expected,'Member inventory differs from manifest'
        for row in manifest['files']:
            data=z.read(prefix+row['path'])
            assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'Payload digest mismatch: '+row['path']
        destination.mkdir(parents=True)
        for i in entries:
            path=destination/Path(*PurePosixPath(i.filename).parts)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(i))
    return {'status':'PASS','member_count':len(names),'root_name':rootname,'manifest_hash_and_payload_check':'PASS','archive_code_executed':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('destination');a=p.parse_args()
    print(json.dumps(extract(a.archive,a.destination),indent=2))
