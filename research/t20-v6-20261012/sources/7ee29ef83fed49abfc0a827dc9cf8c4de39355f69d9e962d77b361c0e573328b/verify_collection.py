#!/usr/bin/env python3
"""Read-only integrity verifier. This does not execute research proofs."""
import argparse, hashlib, io, json, pathlib, stat, zipfile

def sha(b): return hashlib.sha256(b).hexdigest()
def require(ok, message):
    if not ok: raise ValueError(message)
def checked_zip(z):
    infos=z.infolist(); names=[i.filename for i in infos]
    require(len(names)==len(set(names)), 'Duplicate archive member')
    require(sum(i.file_size for i in infos)<=1024**3, 'Declared archive exceeds 1 GiB limit')
    for i in infos:
        p=pathlib.PurePosixPath(i.filename)
        require(not p.is_absolute() and '..' not in p.parts and str(p)==i.filename, 'Unsafe member path')
        require('\\' not in i.filename and not i.is_dir(), 'Non-file member')
        mode=stat.S_IFMT(i.external_attr>>16)
        require(mode in (0,stat.S_IFREG), 'Nonregular member')
        require(not i.flag_bits & 1, 'Encrypted member')
    require(z.testzip() is None, 'CRC failure')
    return names

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=pathlib.Path);ap.add_argument('--expected-sha256');a=ap.parse_args()
    b=a.archive.read_bytes();digest=sha(b)
    if a.expected_sha256: require(digest==a.expected_sha256.lower(), 'Outer SHA-256 mismatch')
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=checked_zip(z); raw=z.read('MANIFEST.json');m=json.loads(raw)
        require(z.read('MANIFEST.sha256').decode().strip()==sha(raw),'Manifest digest mismatch')
        rows=m['files']; expected=[r['path'] for r in rows]
        require(len(expected)==len(set(expected)), 'Duplicate manifest entry')
        require(set(names)==set(expected)|{'MANIFEST.json','MANIFEST.sha256'},'Inventory mismatch')
        nested=[]
        for r in rows:
            content=z.read(r['path']); require(len(content)==r['bytes'] and sha(content)==r['sha256'], 'File mismatch: '+r['path'])
            if r['path'].endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(content)) as nz: nested.append({'path':r['path'],'entries':len(checked_zip(nz))})
        print(json.dumps({'status':'PASS_COLLECTION_INTEGRITY_ONLY','sha256':digest,'bytes':len(b),'manifest_sha256':sha(raw),'entries':len(names),'nested_archives':nested,'proof_replay_performed':False},indent=2))
if __name__=='__main__':main()
