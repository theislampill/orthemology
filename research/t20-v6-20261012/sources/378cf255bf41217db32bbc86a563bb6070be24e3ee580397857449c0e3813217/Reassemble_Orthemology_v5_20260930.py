#!/usr/bin/env python3
"""Reassemble the exact verified Orthemology v5 research ZIP.

Save this script and all eight Part ZIP attachments together. Do not extract
those Part ZIPs. Run with Python 3, for example:
  Windows with Python installed: py Reassemble_Orthemology_v5_20260930.py
  WSL, Linux or macOS: python3 Reassemble_Orthemology_v5_20260930.py

Uses only the Python standard library. No network, installs, or source-code
execution. Reads only the named research-part ZIPs in this script's folder.
It verifies every chunk and the full reconstructed ZIP; parts are preserved.
It refuses to overwrite an existing file unless that file is already exact.
"""
from pathlib import Path
import hashlib, json, sys, zipfile

OUTPUT = 'Orthemology_v5_Frontier_Research_Return_20260930.zip'
EXPECTED_BYTES = 79884298
EXPECTED_SHA256 = '866c6ff6e74a67f2bc452b49a0ada05311c0c2601585ea166404719172bd8086'
PARTS = [(1, 9990000, 'c9db5b30936e91c5e7cf6c27a629daea723c9774c5d3726111c5263d5c0639df'), (2, 9990000, 'b94a63617f1e1190b195e1d814b5322946974b0ece7fc23a3ed375be7d53547b'), (3, 9990000, '694744402f8939c603165a58dced9c730a462d9bd80307c3c0f66336362cdcae'), (4, 9990000, '5c9e473d165127ac65a1191d16dc035932507c88be6cc320c65e441d502e2e42'), (5, 9990000, '7d041d877ce78acf58cdb5d340b05ec8b0399852a75d8e28d24a154b9181533c'), (6, 9990000, '6697d4a0000ca5f20fc5fe20958219333c5a309dcf68560864e40ce88c1a0561'), (7, 9990000, '7f2153c54c33f5fb500c9bc4abb6e73bdc503d393c2624d3948a124da337818c'), (8, 9954298, '48e7b7d199527862e709e259f6ca9e604db0977308db6589755e4bbf0f5db0ba')]

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    folder=Path(__file__).resolve().parent
    target=folder/OUTPUT
    if target.exists():
        if target.is_file() and target.stat().st_size==EXPECTED_BYTES and digest(target)==EXPECTED_SHA256:
            print('The exact verified ZIP already exists: '+str(target)); return
        raise RuntimeError('Output already exists with different bytes; nothing was overwritten: '+str(target))
    expected={i:(size,hash_) for i,size,hash_ in PARTS}
    found={}
    for path in sorted(folder.glob('Orthemology_v5_20260930_Part_*.zip')):
        if path.is_symlink(): continue
        with zipfile.ZipFile(path) as z:
            if len(z.infolist())!=2 or set(z.namelist())!={'part.json','chunk.bin'}:
                raise RuntimeError('Unexpected contents in '+path.name)
            if z.getinfo('part.json').file_size>4096: raise RuntimeError('Invalid metadata size')
            meta=json.loads(z.read('part.json'))
            i=meta.get('part')
            if i not in expected: raise RuntimeError('Unexpected part number in '+path.name)
            size,hash_=expected[i]
            if z.getinfo('chunk.bin').file_size!=size: raise RuntimeError('Wrong chunk size in '+path.name)
            data=z.read('chunk.bin')
            if len(data)!=size or hashlib.sha256(data).hexdigest()!=hash_:
                raise RuntimeError('Chunk checksum failed: '+path.name)
            found[i]=data
    missing=[i for i,_,_ in PARTS if i not in found]
    if missing: raise RuntimeError('Missing verified part(s): '+', '.join(map(str,missing)))
    h=hashlib.sha256()
    for i,_,_ in PARTS: h.update(found[i])
    if sum(map(len,found.values()))!=EXPECTED_BYTES or h.hexdigest()!=EXPECTED_SHA256:
        raise RuntimeError('Reassembled checksum mismatch; no output was written')
    with target.open('xb') as f:
        for i,_,_ in PARTS: f.write(found[i])
    if target.stat().st_size!=EXPECTED_BYTES or digest(target)!=EXPECTED_SHA256:
        raise RuntimeError('Output verification failed; inspect '+str(target))
    print('Verified and reconstructed: '+str(target))
    print('Bytes: '+str(EXPECTED_BYTES))
    print('SHA256: '+EXPECTED_SHA256)

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('ERROR: '+str(exc),file=sys.stderr); sys.exit(1)
