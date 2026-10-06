#!/usr/bin/env python3
"""Verify exact public contents and explicit original-to-public projections.

This performs artifact checks only, under normal and optimized Python alike.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, stat, sys, tempfile, zipfile
sys.dont_write_bytecode = True

ORIGINALS = {
 'A1_source':'923206fcb0d870806b6e77ca259f99e0604876ac872d97c0bf70c100fb460bd3',
 'A2_source':'83f7bef7b6c6b354aca11cd0ebb9b7603b541d960f8b0f2eb57d8c4c4117f7f1',
 'A3_source':'066c70a168d100051910999f9596a856f4e1964d7c3c8c16e0afeb601cd92f00',
 'A1_review':'f08ef43ebd11b8dd0632564d618181cc187fbe860147a6f9996afc1a6049625a',
 'A2_review':'da4448348e02d5ae906e986ef57be756b07b7a7c6e4d991365289ed8691aa554',
 'A3_review':'d8fa16f8a08ab87e8ffa4d67b50ae86c17799712d87f97a73ab5b8f990f3a79c',
 'A1_receipt':'35461135ce61a1b4b217fc1981d782795e2fbd10ceb35210cc50793e7db3ba5f',
 'A2_receipt':'862df64aff61f32f62f5fa4bd8eb4027a1101466c60372e5188226e9a0b813e9',
 'A3_receipt':'54800ed5d4d4928d0cd876e56772a4916f5f94e2c1ec83c9e278e3da5c404bae'}
FORBIDDEN_SUFFIXES = {'.olean','.ilean','.o','.a','.so','.pyc','.zip','.tar','.gz'}
def require(condition, message):
    if not condition:
        raise ValueError(message)
def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()
def safe_name(name):
    require(isinstance(name,str) and name != '', 'Empty/non-string member')
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name
            and str(p) == name and ':' not in name, 'Unsafe member: '+repr(name))
    return name
def census(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'Not a regular package directory')
    names = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs+files:
            p = Path(directory)/name
            require(not p.is_symlink(), 'Symlink rejected')
            require(p.is_dir() or p.is_file(), 'Nonregular entry rejected')
        for name in files:
            names.add(safe_name((Path(directory)/name).relative_to(root).as_posix()))
    return names
def json_read(path):
    def unique(pairs):
        d = {}
        for k,v in pairs:
            require(k not in d, 'Duplicate JSON key: '+k)
            d[k] = v
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)
def records(rows, path_key='path'):
    result = {}
    for row in rows:
        name = safe_name(row[path_key])
        require(name not in result, 'Duplicate record: '+name)
        result[name] = row
    return result
def check_row(root, path, row):
    f = Path(root)/safe_name(path)
    require(f.is_file() and not f.is_symlink(), 'Required file absent: '+path)
    require(f.stat().st_size == row['bytes'] and digest(f) == row['sha256'], 'File digest mismatch: '+path)

def verify(root, expected_manifest):
    root = Path(root)
    actual = census(root)
    require(digest(root/'MANIFEST.json') == expected_manifest, 'Public manifest mismatch')
    manifest = json_read(root/'MANIFEST.json')
    rows = records(manifest['files'])
    require(actual == set(rows)|{'MANIFEST.json'}, 'Exact package census mismatch')
    for name,row in rows.items():
        require(Path(name).suffix not in FORBIDDEN_SUFFIXES, 'Compiled/cache/archive member rejected')
        check_row(root,name,row)
        text = (root/name).read_text()
        host_markers = ['/'+x for x in ['workspace/','home/agent/','root/','tmp/']]
        require(not any(x in text for x in host_markers), 'Host path in public member: '+name)
    identities = json_read(root/'ORIGINAL_IDENTITIES.json')
    require(set(identities) == set(ORIGINALS), 'Original identity census mismatch')
    for key, expected in ORIGINALS.items():
        r = identities[key]
        require(r['sha256'] == expected and digest(root/safe_name(r['path'])) == expected, 'Original identity mismatch: '+key)
    included_science = {}
    mapping_count = 0
    omissions = 0
    for stage in ['A1','A2','A3']:
        for role in ['source','review']:
            binding = identities[stage+'_'+role]
            original = json_read(root/binding['path'])
            old = records(original['files'])
            projection = json_read(root/f'projection/{stage}_{role.upper()}_MAP.json')
            require(projection['original_manifest'] == binding, 'Projection manifest binding mismatch')
            mapped = records(projection['entries'], 'original_path')
            require(set(mapped) == set(old), 'Projection does not cover every original entry')
            for path, entry in old.items():
                r = mapped[path]
                require(r['original_sha256'] == entry['sha256'] and r['original_bytes'] == entry['bytes'], 'Altered original entry')
                target = r['public_path']
                if r['disposition'] == 'PRESERVED_EXACT':
                    require(target is not None, 'Preserved file has no destination')
                    check_row(root,target,entry)
                elif r['disposition'] == 'OMITTED':
                    require(target is None and r.get('reason'), 'Omitted file must have null destination and reason')
                    require(safe_name(r['public_replacement']) in actual, 'Missing replacement scope/view')
                    omissions += 1
                else:
                    raise ValueError('Unknown projection disposition')
                required = (role == 'source' and path.startswith('src/') and path.endswith('.lean')) or (role == 'review' and path.startswith('controls/') and path.endswith('.lean'))
                if required:
                    require(r['disposition'] == 'PRESERVED_EXACT', 'Required scientific/control source omitted')
                    included_science[target] = (stage, entry)
                if role == 'review' and path in ['finite_controls.py','check_replay_guards.py']:
                    require(r['disposition'] == 'PRESERVED_EXACT', 'Exact reviewer control script omitted')
                mapping_count += 1
    source_bindings = json_read(root/'PROOF_SOURCE_BINDINGS.json')
    bound = records(source_bindings['files'])
    require(set(bound) == set(included_science), 'Proof-source binding census mismatch')
    require(len(bound) == 12, 'Expected eight scientific and four reviewer modules')
    for path, (stage, entry) in included_science.items():
        r = bound[path]
        require(r['stage'] == stage and r['sha256'] == entry['sha256'] and r['bytes'] == entry['bytes'], 'Proof-source binding mismatch')
    require({n for n in actual if n.endswith('.lean')} == set(bound), 'Unexpected Lean source')
    return {'status':'PASS_PUBLIC_ARTIFACT_BINDING','manifest_sha256':expected_manifest,
            'members':len(actual),'original_entries_mapped':mapping_count,
            'explicit_omissions':omissions,'exact_lean_source_files':12,
            'new_kernel_check':False}

def unpack_checked_zip(archive, destination, expected_sha=None, expected_size=None, expected_members=None):
    archive = Path(archive)
    require(archive.is_file() and not archive.is_symlink(), 'Missing/nonregular archive')
    if expected_sha is not None:
        require(digest(archive) == expected_sha, 'Archive digest mismatch')
    if expected_size is not None:
        require(archive.stat().st_size == expected_size, 'Archive size mismatch')
    destination = Path(destination)
    require(not destination.exists(), 'Extraction destination must be absent')
    with zipfile.ZipFile(archive) as z:
        entries = z.infolist()
        names = set()
        for info in entries:
            name = safe_name(info.filename)
            require(name not in names and not info.is_dir(), 'Duplicate/directory archive member')
            names.add(name)
            mode = (info.external_attr >> 16) & 0o170000
            require(mode in (0,stat.S_IFREG), 'Nonregular archive member')
        if expected_members is not None:
            require(len(entries) == expected_members, 'Archive member count mismatch')
        require(z.testzip() is None, 'Archive CRC failure')
        destination.mkdir(parents=True)
        for info in entries:
            target = destination/info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(info))
    return destination

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path)
    p.add_argument('--archive',type=Path)
    p.add_argument('--expected-archive-sha256')
    p.add_argument('--expected-manifest-sha256',required=True)
    a = p.parse_args()
    require((a.root is None) != (a.archive is None), 'Supply exactly one of --root or --archive')
    if a.archive:
        require(a.expected_archive_sha256 is not None, 'Archive expected hash required')
        with tempfile.TemporaryDirectory(prefix='selector-verify-') as t:
            tree = unpack_checked_zip(a.archive,Path(t)/'packet',a.expected_archive_sha256)
            roots = [d for d in tree.iterdir() if d.is_dir()]
            require(len(roots)==1 and len(list(tree.iterdir()))==1, 'Expected one package root')
            result = verify(roots[0],a.expected_manifest_sha256)
    else:
        result = verify(a.root,a.expected_manifest_sha256)
    print(json.dumps(result,indent=2))
if __name__ == '__main__':
    main()
