#!/usr/bin/env python3
"""Verify each file in a T20 Dot handoff against its embedded SHA256 manifest."""
from pathlib import Path
from zipfile import ZipFile
import hashlib, json, sys

def main():
    package=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
    if package.is_dir():
        manifest=json.loads((package/'MANIFEST.json').read_text())
        expected=manifest['files']; actual={p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
        if actual-set(expected)-{'MANIFEST.json'} or set(expected)-actual:
            raise SystemExit('MISMATCH: extra or missing paths')
        def get(name):return (package/name).read_bytes()
    else:
        with ZipFile(package) as z:
            if z.testzip() is not None:raise SystemExit('ZIP CRC FAILURE')
            names=z.namelist();found=[n for n in names if n.endswith('/MANIFEST.json')]
            if len(found)!=1:raise SystemExit('MISSING OR DUPLICATE MANIFEST')
            prefix=found[0][:-len('MANIFEST.json')]
            manifest=json.loads(z.read(found[0]));expected=manifest['files']
            if set(names)-{prefix+'MANIFEST.json'}!={prefix+x for x in expected}:
                raise SystemExit('ZIP NAMES MISMATCH')
            for name,meta in expected.items():
                if '..' in Path(name).parts or name.startswith('/'):
                    raise SystemExit('UNSAFE NAME '+name)
                data=z.read(prefix+name)
                if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:
                    raise SystemExit('FILE MISMATCH '+name)
            print('PASS',len(expected),'file hashes; package:',package)
            return
    for name,meta in expected.items():
        data=get(name)
        if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:
            raise SystemExit('FILE MISMATCH '+name)
    print('PASS',len(expected),'file hashes; directory:',package)

if __name__=='__main__': main()
