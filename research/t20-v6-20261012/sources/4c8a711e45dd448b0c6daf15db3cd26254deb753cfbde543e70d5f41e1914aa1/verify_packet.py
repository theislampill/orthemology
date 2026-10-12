#!/usr/bin/env python3
"""Strict byte/inventory verification; no truth, authority or novelty inference."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,sys

class VerificationError(ValueError):pass

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b:break
            h.update(b)
    return h.hexdigest()

def safe(s):
    if not isinstance(s,str) or not s or '\\' in s or ':' in s or '\x00' in s:
        raise VerificationError('Unsafe manifest path')
    p=PurePosixPath(s)
    if p.is_absolute() or any(x in ('','.','..') for x in s.split('/')) or p.as_posix()!=s:
        raise VerificationError('Unsafe manifest path: '+s)
    return s

def verify(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():raise VerificationError('Root must be a real directory')
    mp=root/'MANIFEST.json';sp=root/'MANIFEST.sha256'
    if not mp.is_file() or not sp.is_file() or mp.is_symlink() or sp.is_symlink():
        raise VerificationError('Missing or linked manifest')
    try:
        words=sp.read_text(encoding='ascii').split()
        if len(words)!=2 or words[1]!='MANIFEST.json' or not re.fullmatch('[0-9a-f]{64}',words[0]):
            raise VerificationError('Malformed manifest digest')
        if digest(mp)!=words[0]:raise VerificationError('Manifest digest mismatch')
        m=json.loads(mp.read_text(encoding='utf-8'))
    except VerificationError:raise
    except Exception as e:raise VerificationError('Invalid manifest metadata: '+str(e)) from e
    if not isinstance(m,dict) or set(m)!={'format','files','directories'} or m['format']!='t20-synthesis-manifest-v1':
        raise VerificationError('Unrecognised manifest format')
    if not isinstance(m['files'],list) or not isinstance(m['directories'],list):raise VerificationError('Invalid inventory types')
    wanted={}
    for r in m['files']:
        if not isinstance(r,dict) or set(r)!={'path','bytes','sha256'}:raise VerificationError('Malformed file row')
        p=safe(r['path'])
        if p in wanted or p in ('MANIFEST.json','MANIFEST.sha256'):raise VerificationError('Duplicate or self-manifest path')
        if type(r['bytes']) is not int or r['bytes']<0 or not isinstance(r['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',r['sha256']):
            raise VerificationError('Invalid file binding')
        wanted[p]=r
    dirs=[safe(x) for x in m['directories']]
    if len(dirs)!=len(set(dirs)):raise VerificationError('Duplicate directory')
    actualfiles=set();actualdirs=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():raise VerificationError('Symlink forbidden: '+rel)
        if p.is_dir():actualdirs.add(rel)
        elif p.is_file():actualfiles.add(rel)
        else:raise VerificationError('Nonregular member: '+rel)
    if actualfiles != set(wanted)|{'MANIFEST.json','MANIFEST.sha256'}:
        raise VerificationError('File inventory mismatch: '+str(sorted(actualfiles.symmetric_difference(set(wanted)|{'MANIFEST.json','MANIFEST.sha256'}))[:12]))
    if actualdirs!=set(dirs):raise VerificationError('Directory inventory mismatch')
    for rel,r in wanted.items():
        p=root/rel
        if p.stat().st_size!=r['bytes'] or digest(p)!=r['sha256']:
            raise VerificationError('Payload binding mismatch: '+rel)
    return {'status':'PASS','files':len(wanted),'directories':len(dirs),'manifest_sha256':words[0],
            'scope':'Exact custody and inventory only; external authenticity requires a pinned archive hash'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',nargs='?',default='.')
    args=p.parse_args()
    try:print(json.dumps(verify(Path(args.root)),indent=2))
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e)},indent=2),file=sys.stderr);sys.exit(1)
