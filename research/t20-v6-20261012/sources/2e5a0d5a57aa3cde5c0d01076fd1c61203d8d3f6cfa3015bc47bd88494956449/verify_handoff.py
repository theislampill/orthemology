#!/usr/bin/env python3
"""Strict manifest verifier for the user-visible Orthemology handoff editions.
This verifies file/ZIP identities only; it does not run inherited code or check theorem truth.
Usage: python verify_handoff.py path/to/handoff.zip  [or path/to/extracted/root]
"""
import hashlib, json, pathlib, sys, zipfile

def h(b): return hashlib.sha256(b).hexdigest()
def verify(path):
    path=pathlib.Path(path)
    if path.is_dir():
        data=json.loads((path/'MANIFEST.json').read_text('utf8'))
        expected={v['path']:v for v in data['files']}
        actual={str(p.relative_to(path)).replace('\\','/') for p in path.rglob('*') if p.is_file()}-{'MANIFEST.json'}
        if actual!=set(expected):
            return {'ok':False,'reason':'file set mismatch','missing':sorted(set(expected)-actual)[:15], 'extra':sorted(actual-set(expected))[:15]}
        errors=[]
        for name,entry in expected.items():
            b=(path/name).read_bytes()
            if len(b)!=entry['bytes'] or h(b)!=entry['sha256']:errors.append(name)
        return {'ok':not errors,'edition':data['edition'],'files_checked':len(expected),'bad_files':errors[:15]}
    with zipfile.ZipFile(path) as z:
        members=[i.filename for i in z.infolist() if not i.is_dir()]
        if len(members)!=len(set(members)):
            return {'ok':False,'reason':'duplicate archive paths'}
        if any(x.startswith('/') or '/../' in '/'+x or '\\' in x for x in members):
            return {'ok':False,'reason':'unsafe archive member path'}
        roots={n.split('/')[0] for n in members}
        if len(roots)!=1:return {'ok':False,'reason':'not one archive root'}
        root=next(iter(roots))
        data=json.loads(z.read(root+'/MANIFEST.json'))
        expected={root+'/'+v['path']:v for v in data['files']}
        actual=set(members)-{root+'/MANIFEST.json'}
        if actual!=set(expected):
            return {'ok':False,'reason':'archive file set mismatch','missing':sorted(set(expected)-actual)[:15], 'extra':sorted(actual-set(expected))[:15]}
        errors=[]
        for name,e in expected.items():
            with z.open(name) as f:
                hashobj=hashlib.sha256();count=0
                while True:
                    b=f.read(4*1024*1024)
                    if not b:break
                    count+=len(b);hashobj.update(b)
                if count!=e['bytes'] or hashobj.hexdigest()!=e['sha256']:errors.append(name)
        return {'ok':not errors,'edition':data['edition'],'archive_root':root,'files_checked':len(expected),'bad_files':errors[:15], 'zip_crc_result':z.testzip() or 'PASS'}
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: verify_handoff.py ZIP_OR_EXTRACTED_ROOT')
    r=verify(sys.argv[1]);print(json.dumps(r,indent=2));raise SystemExit(0 if r['ok'] else 1)
