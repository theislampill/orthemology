"""Offline integrity checks; no research code or external source is executed here."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat
import tempfile
import zipfile

MAX_MEMBERS=512
MAX_BYTES=25_000_000


def safe_relative_name(name: str) -> PurePosixPath:
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\x00' in name:
        raise ValueError('Unsafe or nonportable relative path')
    p=PurePosixPath(name)
    if p.is_absolute() or any(x in ('','.', '..') for x in name.split('/')) or str(p)!=name:
        raise ValueError('Path is not a canonical safe relative path')
    return p


def verify_tree(root: Path) -> dict:
    root=Path(root)
    if not root.is_dir() or root.is_symlink(): raise ValueError('Expected a real directory')
    manifest=root/'MANIFEST.json';checksum=root/'MANIFEST.sha256'
    if not manifest.is_file() or not checksum.is_file() or manifest.is_symlink() or checksum.is_symlink():
        raise ValueError('Missing regular root manifest files')
    b=manifest.read_bytes()
    if len(b)>2_000_000:raise ValueError('Manifest too large')
    digest=hashlib.sha256(b).hexdigest()
    if checksum.read_text().strip()!=digest+'  MANIFEST.json':raise ValueError('Manifest checksum mismatch')
    m=json.loads(b)
    if m.get('schema')!='t20-deep-dive-manifest-v1' or not isinstance(m.get('files'),list):
        raise ValueError('Unsupported manifest schema')
    if len(m['files'])>MAX_MEMBERS:raise ValueError('Too many payload members')
    seen=set();total=0
    for row in m['files']:
        name=row.get('path');rel=safe_relative_name(name)
        if name in seen or name in ('MANIFEST.json','MANIFEST.sha256'):raise ValueError('Duplicate or recursive manifest entry')
        seen.add(name);p=root/rel
        if not p.is_file() or p.is_symlink():raise ValueError('Missing regular payload file: '+name)
        if not isinstance(row.get('bytes'),int) or row['bytes']<0:raise ValueError('Invalid size declaration')
        if not re.fullmatch('[0-9a-f]{64}',str(row.get('sha256',''))):raise ValueError('Invalid digest declaration')
        total+=row['bytes']
        if total>MAX_BYTES:raise ValueError('Payload byte limit exceeded')
        if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Payload identity mismatch: '+name)
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('Symlinks are not admitted')
        if p.is_file():actual.add(p.relative_to(root).as_posix())
        elif not p.is_dir():raise ValueError('Special filesystem object')
    if actual != seen|{'MANIFEST.json','MANIFEST.sha256'}:raise ValueError('Undeclared or missing tree member')
    return {'payload_files':len(seen),'payload_bytes':total,'manifest_sha256':digest}


def safe_extract(archive: Path, destination: Path) -> Path:
    """Stage and verify one-root file-only ZIP; commit only into a new destination.

    Existing paths are refused. The archive is bounded, and symlinks, duplicate
    members, encryption, directory entries and escaping/nonportable paths fail.
    The returned directory contains the manifest. No payload code runs.
    """
    archive=Path(archive);destination=Path(destination)
    if destination.exists() or destination.is_symlink():raise ValueError('Destination already exists')
    if not destination.parent.is_dir():raise ValueError('Destination parent must already exist')
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist()
        if not infos or len(infos)>MAX_MEMBERS+2:raise ValueError('Archive member limit')
        seen=set();roots=set();total=0
        for info in infos:
            rel=safe_relative_name(info.filename)
            if len(rel.parts)<2:raise ValueError('Archive needs exactly one top-level directory')
            roots.add(rel.parts[0]);total+=info.file_size
            if info.filename in seen:raise ValueError('Duplicate archive member')
            seen.add(info.filename)
            mode=info.external_attr>>16
            if info.is_dir() or stat.S_IFMT(mode) not in (0,stat.S_IFREG):raise ValueError('Only regular file entries admitted')
            if info.flag_bits&1:raise ValueError('Encrypted entries not admitted')
            if total>MAX_BYTES:raise ValueError('Archive uncompressed byte limit')
        if len(roots)!=1:raise ValueError('More than one archive root')
        top=next(iter(roots))
        if z.testzip() is not None:raise ValueError('CRC failure')
        with tempfile.TemporaryDirectory(prefix='t20-safe-',dir=destination.parent) as temp:
            staged=Path(temp)/'delivery';staged.mkdir()
            for info in infos:
                p=staged/PurePosixPath(info.filename);p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as f:f.write(z.read(info))
            verify_tree(staged/top)
            if destination.exists() or destination.is_symlink():raise ValueError('Destination appeared during validation')
            os.rename(staged,destination)
    return destination/top
