from pathlib import Path
import hashlib,json,zipfile
root=Path('private-locator:6e22bbac941f2662a0bd'); source=root/'Orthemology_v5_Frontier_Research_Return_20260930.zip'; out=root/'parts'; chunk_size=9_990_000
sha=lambda b:hashlib.sha256(b).hexdigest()
original=source.read_bytes(); assert len(original)==79884298 and sha(original)=='866c6ff6e74a67f2bc452b49a0ada05311c0c2601585ea166404719172bd8086'
chunks=[original[i:i+chunk_size] for i in range(0,len(original),chunk_size)]; spec=[]
for i,data in enumerate(chunks,1):
 name=f'Orthemology_v5_20260930_Part_{i:02d}_of_{len(chunks):02d}.zip'
 meta={'part':i,'parts':len(chunks),'chunk_bytes':len(data),'chunk_sha256':sha(data),'output_filename':source.name,'output_bytes':len(original),'output_sha256':sha(original)}
 with zipfile.ZipFile(out/name,'w',zipfile.ZIP_STORED) as z:
  z.writestr('part.json',json.dumps(meta,indent=2)+'\n');z.writestr('chunk.bin',data)
 assert (out/name).stat().st_size<10_000_000
 spec.append({**meta,'filename':name,'wrapper_bytes':(out/name).stat().st_size,'wrapper_sha256':sha((out/name).read_bytes())})
(out/'TRANSPORT_MANIFEST.json').write_text(json.dumps({'original_filename':source.name,'original_bytes':len(original),'original_sha256':sha(original),'parts':spec},indent=2)+'\n')
script='''#!/usr/bin/env python3
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
PARTS = '''+repr([(p['part'],p['chunk_bytes'],p['chunk_sha256']) for p in spec])+'''

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
'''
(out/'Reassemble_Orthemology_v5_20260930.py').write_text(script)
print(json.dumps({'parts':len(spec),'largest_wrapper_bytes':max(p['wrapper_bytes'] for p in spec),'unchanged_original_sha256':sha(original)},indent=2))
