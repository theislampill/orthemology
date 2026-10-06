"""Read-only exact source identity checks. No fabricated Git metadata."""
from pathlib import Path, PurePosixPath
import hashlib, json, os, subprocess, tarfile

HERE = Path(__file__).resolve().parent
REVISION = 'c44e0c8ee63ca166450922a373c7409c5d26b00b'
ARCHIVE_SHA256 = '9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425'
EXCLUDED_GENERATED_ROOTS = {'.git', '.lake'}

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def regular_source_files(root, permitted_git_symlinks=frozenset()):
    """Exact file census; only ROOT/.git and ROOT/.lake are external metadata."""
    root=Path(root)
    found=set()
    for directory,dirs,files in os.walk(root,followlinks=False):
        relative=Path(directory).relative_to(root)
        if relative==Path('.'):
            dirs[:]=[x for x in dirs if x not in EXCLUDED_GENERATED_ROOTS]
            files=[x for x in files if x not in EXCLUDED_GENERATED_ROOTS]
        for name in dirs+files:
            p=Path(directory)/name
            if p.is_symlink():
                name=str(p.relative_to(root))
                if name not in permitted_git_symlinks:
                    raise ValueError('Source symlink is not allowed: '+name)
                # Git HEAD/status bind the literal link target. Do not follow it.
                found.add(name)
        for name in files:
            p=Path(directory)/name
            if p.is_symlink():continue
            if not p.is_file():raise ValueError('Non-regular source entry: '+str(p.relative_to(root)))
            found.add(str(p.relative_to(root)))
    return found

def verify_archive(root,archive,inventory_path=HERE/'MATHLIB_ARCHIVE_INVENTORY.json'):
    inventory=json.loads(Path(inventory_path).read_text())
    if inventory['revision']!=REVISION or inventory['archive_sha256']!=ARCHIVE_SHA256:
        raise ValueError('Wrong inventory identity')
    if digest(archive)!=ARCHIVE_SHA256:raise ValueError('Mathlib archive digest mismatch')
    expected={row['path']:row for row in inventory['files']}
    if len(expected)!=len(inventory['files']) or len(expected)!=6816:raise ValueError('Invalid inventory census')
    seen=set()
    with tarfile.open(archive,'r:gz') as tar:
        for member in tar:
            path=PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0]!=inventory['archive_prefix']:
                raise ValueError('Unsafe or unexpected archive member')
            if member.isdir():continue
            if not member.isfile() or len(path.parts)<2:raise ValueError('Non-regular archive member')
            relative=str(PurePosixPath(*path.parts[1:]))
            if relative in seen or relative not in expected:raise ValueError('Unexpected or repeated archive member: '+relative)
            seen.add(relative)
            f=tar.extractfile(member)
            h=hashlib.sha256();size=0
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
            row=expected[relative]
            if size!=row['bytes'] or h.hexdigest()!=row['sha256']:raise ValueError('Archive member mismatch: '+relative)
    if seen!=set(expected):raise ValueError('Archive inventory incomplete')
    actual=regular_source_files(root)
    if actual!=set(expected):
        raise ValueError('Extracted source census mismatch: '+repr(sorted(actual^set(expected))[:20]))
    for name,row in expected.items():
        p=Path(root)/name
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:
            raise ValueError('Extracted source mismatch: '+name)
    return {'mode':'EXACT_OFFICIAL_SOURCE_ARCHIVE','revision':REVISION,
            'archive_sha256':ARCHIVE_SHA256,'source_files_verified':len(expected),
            'inventory_sha256':digest(inventory_path),'excluded_generated_roots':sorted(EXCLUDED_GENERATED_ROOTS),
            'git_metadata_created':False}

def git_output(root,args):
    return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()

def verify_git(root,revision,name):
    if git_output(root,['rev-parse','HEAD'])!=revision:raise ValueError('Wrong Git revision: '+name)
    if git_output(root,['status','--porcelain','--untracked-files=all']):raise ValueError('Dirty/untracked Git checkout: '+name)
    # Do not permit ignored extra Lean sources to escape the Git status guard.
    tracked=set(subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0'))-{''}
    actual=regular_source_files(root,tracked)
    extra_sources=[p for p in actual-tracked if p.endswith('.lean')]
    if extra_sources:raise ValueError('Untracked/ignored Lean source: '+name+': '+repr(extra_sources[:10]))
    return {'name':name,'mode':'CLEAN_EXACT_GIT','revision':revision,'tracked_clean':True,'unexpected_lean_sources':False}

def verify_dependencies(mathlib,archive,pins):
    mathlib=Path(mathlib)
    if archive is not None:
        main=verify_archive(mathlib,Path(archive))
    else:
        main=verify_git(mathlib,REVISION,'mathlib')
    packages=[]
    for pkg in pins['packages']:
        if pkg['name']=='mathlib':
            if pkg['revision']!=REVISION:raise ValueError('Packet Mathlib pin disagrees')
            continue
        packages.append(verify_git(mathlib/'.lake/packages'/pkg['name'],pkg['revision'],pkg['name']))
    return {'mathlib':main,'packages':packages,'dependency_writes':False,'official_cache_objects_trusted':True}
