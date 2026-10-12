#!/usr/bin/env python3
"""Offline source-return integrity checks. This does not certify mathematical truth."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

FORBIDDEN_SUFFIXES={'.olean','.ilean','.pyc','.o','.so','.a','.exe','.pdf','.html','.htm'}
FORBIDDEN_PARTS={'__pycache__','.git','research-inputs','research_inputs','primary-inputs',
                 'source-cache','raw-sources','toolchain','build','node_modules'}
CUSTODY={'durable_predecessor','exact_source_recovery','new_source','mixed_exact_and_new'}
QUALIFICATION={'historical_delivered_qualification','fresh_ordinary_review','fresh_finite_checks',
               'fresh_kernel_review','source_only','pending_review','fresh_implementation_review',
               'fresh_source_comparison','bounded_application_inference','fresh_report_review'}


def digest(data):return hashlib.sha256(data).hexdigest()


def identity(path,name):
    data=Path(path).read_bytes()
    return {'path':name,'bytes':len(data),'sha256':digest(data)}


def safe_path(root,name):
    if not isinstance(name,str) or not name or '\\' in name or '\x00' in name or ':' in name:
        raise ValueError('Unsafe path')
    if PurePosixPath(name).is_absolute() or any(p in {'','.','..'} for p in name.split('/')):
        raise ValueError('Unsafe path '+name)
    out=Path(root).joinpath(*PurePosixPath(name).parts)
    if not out.resolve().is_relative_to(Path(root).resolve()):raise ValueError('Escaping path '+name)
    return out


def hygiene(name,data):
    p=PurePosixPath(name)
    if p.suffix.lower() in FORBIDDEN_SUFFIXES or set(p.parts)&FORBIDDEN_PARTS:
        raise ValueError('Excluded payload '+name)
    if data.startswith((b'\x7fELF',b'MZ')):raise ValueError('Executable payload '+name)


def check_zip(path,depth=0):
    if depth>12:raise ValueError('Archive nesting limit')
    with zipfile.ZipFile(path) as z:
        names=set()
        for member in z.infolist():
            name=member.filename.rstrip('/')
            safe_path(Path('/not-extracted'),name)
            if name in names:raise ValueError('Duplicate archive member '+name)
            names.add(name)
            if stat.S_ISLNK(member.external_attr>>16):raise ValueError('Archive symlink')
            if member.is_dir():continue
            data=z.read(member);hygiene(name,data)
            if Path(name).suffix.lower() in {'.zip','.docx'}:check_zip(io.BytesIO(data),depth+1)
        if z.testzip() is not None:raise ValueError('Archive CRC failure')
        return len(names)


def collect(root):
    root=Path(root);rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_symlink():raise ValueError('Symlink forbidden')
        if not p.is_file():continue
        name=p.relative_to(root).as_posix();safe_path(root,name)
        if name in {'MASTER_MANIFEST.json','MASTER_MANIFEST.sha256'}:continue
        data=p.read_bytes();hygiene(name,data)
        if p.suffix.lower() in {'.zip','.docx'}:check_zip(p)
        rows.append(identity(p,name))
    return rows


def seal(root):
    root=Path(root)
    manifest={'schema':1,'scope':'File integrity only; scientific qualifications are explicitly scoped in EVIDENCE_REGISTRY.json',
              'files':collect(root)}
    p=root/'MASTER_MANIFEST.json'
    p.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (root/'MASTER_MANIFEST.sha256').write_text(digest(p.read_bytes())+'  MASTER_MANIFEST.json\n')


def verify(root):
    root=Path(root).resolve();m=root/'MASTER_MANIFEST.json'
    expected_digest=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]
    if digest(m.read_bytes())!=expected_digest:raise ValueError('Master manifest hash mismatch')
    manifest=json.loads(m.read_text());expected=manifest['files'];names=set()
    for row in expected:
        if row['path'] in names:raise ValueError('Duplicate manifest entry')
        names.add(row['path']);safe_path(root,row['path'])
    if expected!=collect(root):raise ValueError('File census or content identity mismatch')
    registry=json.loads((root/'EVIDENCE_REGISTRY.json').read_text());subjects=set()
    for subject in registry['subjects']:
        if subject['id'] in subjects:raise ValueError('Duplicate subject')
        subjects.add(subject['id'])
        if subject['custody'] not in CUSTODY or subject['qualification'] not in QUALIFICATION:
            raise ValueError('Unknown evidence category')
        if not subject.get('scope') or not subject.get('files'):raise ValueError('Unscoped or empty subject')
        for row in subject['files']:
            if row['path'] not in names:raise ValueError('Unmanifested subject file')
            p=safe_path(root,row['path'])
            if identity(p,row['path'])!=row:raise ValueError('Stale subject identity '+row['path'])
    for missing in registry.get('unavailable_prior_scopes',[]):
        if missing.get('status')!='unavailable' or missing.get('files'):
            raise ValueError('Unavailable scope must not claim payload')
    return {'status':'PASS_INTEGRITY','manifest_sha256':expected_digest,
            'files':len(expected),'subjects':len(subjects),
            'scope':'Exact file and scope-binding integrity; not a mathematical proof or replay result'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.root),indent=2))


if __name__=='__main__':main()
