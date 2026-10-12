from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile

ROOT = Path(__file__).resolve().parent
RECOVERY = ROOT.parent
LIST = json.loads((ROOT/'oct11-library-list.json').read_text())['structuredContent']['items']
BY_NAME = {x['name']: x for x in LIST if x.get('model_generated') and x['path'] == '/' + x['name']}
def sha(data):
    return hashlib.sha256(data).hexdigest()

def manifest_rows(value):
    if isinstance(value, dict) and 'files' in value:
        value = value['files']
    if isinstance(value, list):
        return [x for x in value if isinstance(x, dict) and isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str)]
    if isinstance(value, dict):
        rows = []
        for k,v in value.items():
            if isinstance(v,str) and len(v)==64 and all(c in '0123456789abcdefABCDEF' for c in v):
                rows.append({'path':k,'sha256':v})
            elif isinstance(v,dict) and isinstance(v.get('sha256'),str):
                rows.append({'path':k,**v})
        return rows
    return []

def check_archive(p, dest, origin):
    raw=p.read_bytes()
    result={'archive':str(p.relative_to(RECOVERY)), 'sha256':sha(raw), 'bytes':len(raw), 'origin':origin}
    with zipfile.ZipFile(p) as z:
        entries=z.infolist()
        names=[i.filename for i in entries]
        if len(set(names)) != len(names): raise ValueError(f'Duplicate entry in {p}')
        if sum(i.file_size for i in entries)>512*1024*1024: raise ValueError(f'Expanded size ceiling {p}')
        for i in entries:
            q=PurePosixPath(i.filename)
            if q.is_absolute() or '..' in q.parts or '\\' in i.filename or '\x00' in i.filename:
                raise ValueError(f'Unsafe entry {p}: {i.filename}')
            if not q.parts or ':' in q.parts[0]: raise ValueError(f'Unsafe entry {p}: {i.filename}')
            mode=i.external_attr>>16
            if stat.S_ISLNK(mode): raise ValueError(f'Symlink {p}: {i.filename}')
            if stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR): raise ValueError(f'Special file {p}: {i.filename}')
        bad=z.testzip()
        if bad: raise ValueError(f'Bad CRC {p}: {bad}')
        inventory=[]
        for i in entries:
            if i.is_dir(): continue
            data=z.read(i)
            inventory.append({'path':i.filename,'bytes':len(data),'sha256':sha(data)})
        filemap={x['path']:x for x in inventory}
        candidates=[n for n in names if PurePosixPath(n).name in ('MANIFEST.json','DELIVERY_MANIFEST.json','COLLECTION_MANIFEST.json')]
        manifests=[]
        if candidates:
            shallow=min(len(PurePosixPath(n).parts) for n in candidates)
            for name in candidates:
                if len(PurePosixPath(name).parts)!=shallow: continue
                rows=manifest_rows(json.loads(z.read(name)))
                checks=[]
                base=PurePosixPath(name).parent
                for row in rows:
                    path=(base/PurePosixPath(row['path'])).as_posix()
                    actual=filemap.get(path)
                    ok=actual is not None and actual['sha256']==row['sha256'].lower() and ('bytes' not in row or actual['bytes']==row['bytes'])
                    checks.append({'path':path,'match':ok,'expected_sha256':row['sha256'],'actual_sha256':actual['sha256'] if actual else None})
                bound=set(x['path'] for x in checks)
                uncovered=sorted(set(filemap)-bound-{name})
                manifests.append({'path':name,'checked':len(checks),'passed':sum(x['match'] for x in checks),'failed':[x for x in checks if not x['match']],'uncovered_files':uncovered})
        if dest.exists(): raise ValueError(f'Extraction destination exists: {dest}')
        dest.mkdir(parents=True)
        for i in entries:
            out=dest/PurePosixPath(i.filename)
            if not out.resolve().is_relative_to(dest.resolve()): raise ValueError('Path escaped destination')
            if i.is_dir(): out.mkdir(parents=True,exist_ok=True)
            else:
                out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('xb') as f: f.write(z.read(i))
        result.update({'crc_ok':True,'safe_paths':True,'entry_count':len(entries),'file_count':len(inventory),'expanded_bytes':sum(i.file_size for i in entries),'extracted_to':str(dest.relative_to(RECOVERY)),'top_level_manifests':manifests,'files':inventory})
        nested=[dest/PurePosixPath(i.filename) for i in entries if not i.is_dir() and i.filename.endswith('.zip')]
        return result,nested

reports=[]
pending=[]
for p in sorted(ROOT.glob('*.zip')):
    meta=BY_NAME[p.name]
    if p.stat().st_size!=meta['size_bytes']: raise ValueError(f'Library size mismatch {p}')
    info,nested=check_archive(p,ROOT/'safe-extracts'/p.stem,{'kind':'library','library_file_id':meta['library_file_id'],'file_id':meta['file_id'],'library_path':meta['path'],'created_at':meta['created_at'],'version_id':meta['version_id'],'size_matches':True})
    reports.append(info)
    pending += [(n,p.stem,1) for n in nested]
while pending:
    p,parent,depth=pending.pop(0)
    if depth>4: raise ValueError(f'Nested archive depth ceiling {p}')
    archive_hash=sha(p.read_bytes())
    info,nested=check_archive(p,ROOT/'nested-safe-extracts'/parent/(p.stem+'-'+archive_hash[:12]),{'kind':'nested_preserved_archive','parent_archive':parent,'depth':depth})
    reports.append(info)
    pending += [(n,p.stem,depth+1) for n in nested]

receipt={'scope':'Local-only restoration of remaining distinct current-Oct11 root research deliveries, excluding previously restored root/law archives and large predecessor/whole-corpus archives. No research scripts executed and no baseline files overwritten.','external_known_archive_hashes':'No external known outer archive hashes were supplied. Each available top-level delivered content manifest was checked against recovered bytes. Nested archive hashes can additionally be bound by parent manifests.','archives':reports}
(ROOT/'RECOVERY_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'archive_count':len(reports),'library_archives':sum(x['origin']['kind']=='library' for x in reports),'nested_archives':sum(x['origin']['kind']!='library' for x in reports),'zip_checks_passed':all(x['crc_ok'] and x['safe_paths'] for x in reports),'manifest_checks':sum(m['checked'] for x in reports for m in x['top_level_manifests']),'manifest_failed':sum(len(m['failed']) for x in reports for m in x['top_level_manifests']),'receipt':str(ROOT/'RECOVERY_VERIFICATION.json')},indent=2))
