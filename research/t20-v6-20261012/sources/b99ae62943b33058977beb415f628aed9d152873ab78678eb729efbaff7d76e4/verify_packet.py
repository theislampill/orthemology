#!/usr/bin/env python3
"""Verify a sealed T20 directory or ZIP; optionally run its own reference tests.

This verifies bytes and finite controls, not the truth of every inherited claim.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath


def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def _safe(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name

def _entries(manifest:dict)->dict:
    if manifest.get('schema')!=1 or not isinstance(manifest.get('files'),dict):
        raise ValueError('Unsupported or malformed manifest.')
    entries=manifest['files']
    for name,item in entries.items():
        if not _safe(name) or name=='MANIFEST.json':raise ValueError('Unsafe or recursive manifest entry.')
        if not isinstance(item,dict) or not isinstance(item.get('bytes'),int) or item['bytes']<0:
            raise ValueError('Invalid byte count.')
        h=item.get('sha256','')
        if len(h)!=64 or any(c not in '0123456789abcdef' for c in h):raise ValueError('Invalid SHA-256.')
    return entries

def ignored(name:str)->bool:
    p=PurePosixPath(name)
    return '__pycache__' in p.parts or p.suffix=='.pyc'

def verify_directory(root:Path)->dict:
    root=Path(root).resolve(); errors=[]
    try:
        raw=(root/'MANIFEST.json').read_bytes();manifest=json.loads(raw);entries=_entries(manifest)
    except Exception as exc:return {'ok':False,'errors':['manifest: '+repr(exc)]}
    for name,item in entries.items():
        p=root/name
        try:
            if p.is_symlink() or root not in p.resolve().parents:raise ValueError('Symlink or escaped path.')
            data=p.read_bytes()
            if len(data)!=item['bytes']:errors.append('size mismatch: '+name)
            if digest(data)!=item['sha256']:errors.append('hash mismatch: '+name)
        except Exception as exc:errors.append(name+': '+repr(exc))
    actual={str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*') if p.is_file() and not ignored(str(p.relative_to(root)))}
    extras=actual-set(entries)-{'MANIFEST.json'}
    if extras:errors.append('unexpected files: '+', '.join(sorted(extras)))
    return {'ok':not errors,'files_checked':len(entries),'manifest_sha256':digest(raw),'errors':errors}

def verify_zip(path:Path)->dict:
    errors=[]
    try:
        with zipfile.ZipFile(path) as z:
            names=[i.filename for i in z.infolist() if not i.is_dir()]
            if len(names)!=len(set(names)):raise ValueError('Duplicate ZIP member names.')
            if any(not _safe(n) for n in names):raise ValueError('Unsafe ZIP member name.')
            manifests=[n for n in names if PurePosixPath(n).name=='MANIFEST.json' and n.count('/')<=1]
            if len(manifests)!=1:raise ValueError('Require exactly one root manifest.')
            mn=manifests[0];prefix=mn[:-len('MANIFEST.json')]
            raw=z.read(mn);entries=_entries(json.loads(raw))
            for name,item in entries.items():
                try:
                    data=z.read(prefix+name) # zipfile also validates each member's CRC
                    if len(data)!=item['bytes']:errors.append('size mismatch: '+name)
                    if digest(data)!=item['sha256']:errors.append('hash mismatch: '+name)
                except Exception as exc:errors.append(name+': '+repr(exc))
            expected={prefix+n for n in entries}|{mn}
            if set(names)!=expected:errors.append('ZIP inventory differs from sealed manifest.')
            return {'ok':not errors,'files_checked':len(entries),'manifest_sha256':digest(raw),'errors':errors}
    except Exception as exc:return {'ok':False,'errors':[repr(exc)]}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path',nargs='?',default=str(Path(__file__).resolve().parent))
    parser.add_argument('--run-tests',action='store_true')
    args=parser.parse_args();path=Path(args.path)
    receipt=verify_zip(path) if path.is_file() else verify_directory(path)
    if args.run_tests:
        if path.is_file():receipt['test_error']='Extract the ZIP before requesting reference tests.';receipt['ok']=False
        else:
            run=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=path,text=True,capture_output=True,timeout=120)
            receipt['reference_test_returncode']=run.returncode
            receipt['reference_test_output']=run.stdout+run.stderr
            receipt['ok']=receipt['ok'] and run.returncode==0
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return 0 if receipt['ok'] else 1

if __name__=='__main__':raise SystemExit(main())
