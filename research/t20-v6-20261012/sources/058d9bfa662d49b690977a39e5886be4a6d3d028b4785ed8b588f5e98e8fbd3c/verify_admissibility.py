#!/usr/bin/env python3
"""Offline byte/inventory/provenance verifier; Python 3.8+ standard library.

Does not execute research code or certify mathematical or philosophical truth.
Use an independently trusted archive SHA-256 to authenticate this verifier.
"""
import argparse,datetime,hashlib,json,os,re,stat,sys,zipfile
from pathlib import Path,PurePosixPath
IDENTITY='T20_Hessian_Admissibility_Research_Checkpoint_20261009'
MAX_BYTES=256*1024*1024

def need(ok,message):
    if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def safe(text):
    need(isinstance(text,str) and text and not any(ord(c)<32 for c in text),'Invalid path string')
    p=PurePosixPath(text)
    need(str(p)==text and not p.is_absolute() and '..' not in p.parts and '\\' not in text and ':' not in text,'Unsafe/noncanonical path: '+repr(text))
    need(all(x not in {'','.','..'} for x in p.parts),'Invalid path component')
    return p

def json_data(data):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'Duplicate JSON key: '+k);out[k]=v
        return out
    def nonfinite(value):raise ValueError('Nonfinite JSON constant: '+value)
    return json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=nonfinite)

def snapshot(root):
    need(root.is_dir() and not root.is_symlink(),'Package root must be a real directory')
    files={};dirs=set()
    for base,names,leaves in os.walk(root,followlinks=False):
        for name in names+leaves:
            p=Path(base)/name;rel=p.relative_to(root).as_posix();safe(rel)
            need(not p.is_symlink(),'Symlink forbidden: '+rel)
            if p.is_dir():dirs.add(rel)
            else:
                need(stat.S_ISREG(p.stat().st_mode),'Special file forbidden: '+rel);files[rel]=p.read_bytes()
    return files,dirs

def validate(files,dirs=None):
    need(sum(map(len,files.values()))<=MAX_BYTES,'Package exceeds safety size bound')
    for name in files:safe(name)
    need(len({x.casefold() for x in files})==len(files),'Case-folded path collision')
    need('MANIFEST.json' in files and 'MANIFEST.sha256' in files,'Missing manifest/checksums')
    manifest=json_data(files['MANIFEST.json'])
    need(manifest['checkpoint_id']==IDENTITY,'Wrong checkpoint identity')
    need(manifest['status']=='INTERMEDIATE_T20_ACTIVE','Wrong checkpoint status')
    rows=manifest['files'];need(type(rows)==list and manifest['file_count']==len(rows),'Manifest count mismatch')
    paths=[]
    for row in rows:
        p=str(safe(row['path']));paths.append(p)
        need(type(row['bytes'])==int and row['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',row['sha256']),'Malformed size or hash')
    need(len(paths)==len(set(paths)),'Duplicate manifest path')
    need(set(paths).isdisjoint({'MANIFEST.json','MANIFEST.sha256'}),'Self-referential manifest inventory')
    need(set(files)==set(paths)|{'MANIFEST.json','MANIFEST.sha256'},'Exact file inventory mismatch')
    expected_dirs={str(p) for x in files for p in PurePosixPath(x).parents if str(p)!='.'}
    if dirs is not None:need(dirs==expected_dirs,'Exact directory inventory mismatch')
    for row in rows:
        data=files[row['path']];need(len(data)==row['bytes'] and digest(data)==row['sha256'],'Payload mismatch: '+row['path'])
    sums={}
    for line in files['MANIFEST.sha256'].decode('utf-8').splitlines():
        parts=line.split('  ',1);need(len(parts)==2,'Malformed checksum line');h,p=parts;safe(p)
        need(re.fullmatch('[0-9a-f]{64}',h) and p not in sums,'Malformed/duplicate checksum');sums[p]=h
    need(set(sums)==set(paths)|{'MANIFEST.json'},'Checksum inventory mismatch')
    for p,h in sums.items():need(digest(files[p])==h,'Checksum mismatch: '+p)
    json_count=0
    for p,data in files.items():
        if p.endswith('.json'):json_data(data);json_count+=1
    bindings=json_data(files['BINDINGS.json']);need(type(bindings)==list,'Invalid binding ledger')
    for row in bindings:
        p=str(safe(row['path']));need(p in files,'Missing bound input: '+p);data=files[p]
        need(digest(data)==row['sha256'],'Bound source mismatch: '+p)
        if 'bytes' in row:need(len(data)==row['bytes'],'Bound byte count mismatch: '+p)
        if 'git_blob_sha1' in row:need(hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==row['git_blob_sha1'],'Git blob mismatch: '+p)
    return {'distributed_files':len(files),'payload_files':len(rows),'directories':len(expected_dirs),'json_files_parsed':json_count,'source_and_review_bindings':len(bindings),'manifest_sha256':digest(files['MANIFEST.json'])}

def archive_snapshot(path):
    files={};seen=set();total=0
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            name=info.filename;safe(name)
            need(name not in seen,'Duplicate ZIP member: '+name);seen.add(name)
            need(not info.is_dir(),'Unexpected ZIP directory member')
            mode=info.external_attr>>16;kind=stat.S_IFMT(mode)
            need(kind in {0,stat.S_IFREG},'ZIP symlink or special member forbidden')
            need(not info.flag_bits&1,'Encrypted ZIP member forbidden')
            p=PurePosixPath(name);need(len(p.parts)>1 and p.parts[0]==IDENTITY,'Unexpected ZIP root')
            rel='/'.join(p.parts[1:]);safe(rel);total+=info.file_size
            need(total<=MAX_BYTES,'ZIP exceeds safety size bound')
            data=z.read(info);need(len(data)==info.file_size,'ZIP size mismatch');files[rel]=data
    validate(files)
    return files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--output',type=Path,required=True,help='New receipt directory outside the package')
    parser.add_argument('--archive',type=Path,help='Also verify exact archive inventory and correspondence')
    parser.add_argument('--archive-sha256',help='Independent expected archive SHA-256')
    args=parser.parse_args();need(not args.root.is_symlink(),'Symlink root forbidden');root=args.root.resolve();out=args.output.absolute()
    need(not out.exists() and not out.is_symlink(),'Output exists; refusing overwrite')
    out=out.resolve();need(out!=root and root not in out.parents,'Output must be outside package')
    before,dirs=snapshot(root);summary=validate(before,dirs);archive_hash=None
    if args.archive:
        need(args.archive.is_file() and not args.archive.is_symlink(),'Invalid archive path')
        archive_hash=digest(args.archive.read_bytes())
        if args.archive_sha256:need(archive_hash==args.archive_sha256,'Archive SHA-256 mismatch')
        archived=archive_snapshot(args.archive);need(archived==before,'Archive differs from extracted package')
    else:need(args.archive_sha256 is None,'Archive hash provided without archive')
    after,after_dirs=snapshot(root);need(before==after and dirs==after_dirs,'Package changed during verification')
    receipt={'status':'PASS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint_id':IDENTITY,**summary,'archive_sha256':archive_hash,'package_bytes_unchanged':True,'research_code_executed':False,'lean_or_kernel_replay':False,'scope':'Byte identity, exact inventory, strict path checks, JSON readability and declared source/review bindings only. No proof, source-authentication, integration, cognitive/philosophical warrant, acceptance or T20 closure certification.'}
    out.mkdir(parents=True,exist_ok=False);(out/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
