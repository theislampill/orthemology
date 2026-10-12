#!/usr/bin/env python3
"""Extract a verified ZIP to an absent private directory, retaining safe Unix modes.

Preflights names/types/conflicts/CRC before writing. Does not edit a repository,
invoke a build, or confer authenticity on the archive. Verify its digest first.
"""
import argparse
import os
from pathlib import Path
import shutil
import stat
import sys
import zipfile

MAX_BYTES = 256 * 1024 * 1024
MAX_MEMBERS = 20000

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unpack(archive_path, destination):
    destination = Path(os.path.abspath(destination))
    for path in (destination, *destination.parents):
        require(not path.is_symlink(), 'Symlink destination/ancestor refused')
    require(not destination.exists(), 'Destination already exists; choose a new private directory')
    with zipfile.ZipFile(archive_path) as archive:
        members = archive.infolist()
        require(0 < len(members) <= MAX_MEMBERS, 'Empty or oversized archive')
        require(sum(m.file_size for m in members) <= MAX_BYTES, 'Expanded size exceeds launch bound')
        entries = []; seen = {}; parent_spelling = {}
        for member in members:
            name = member.filename
            require(member.orig_filename == name and '\x00' not in name, 'NUL/truncated ZIP name')
            directory = member.is_dir()
            parts = (name[:-1] if directory else name).split('/')
            require(parts and '\\' not in name and ':' not in name
                    and all(p not in ('', '.', '..') and p.rstrip(' .').casefold() != '.git' for p in parts),
                    'Unsafe ZIP path: ' + name)
            require(all(p == p.rstrip(' .') for p in parts), 'Ambiguous trailing character: ' + name)
            key = '/'.join(parts).casefold()
            require(key not in seen, 'Duplicate/case-colliding ZIP path: ' + name)
            mode = member.external_attr >> 16
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR), 'Nonregular ZIP member: ' + name)
            require(not mode & 0o7000, 'Privileged ZIP permissions refused: ' + name)
            require(not (stat.S_ISDIR(mode) and not directory), 'Directory type mismatch: ' + name)
            seen[key] = directory
            for end in range(1, len(parts)):
                parent = '/'.join(parts[:end]); folded = parent.casefold()
                require(folded not in parent_spelling or parent_spelling[folded] == parent,
                        'Case-colliding parent directory: ' + name)
                parent_spelling[folded] = parent
            entries.append((member, parts, directory, stat.S_IMODE(mode) or (0o755 if directory else 0o644)))
        for _, parts, _, _ in entries:
            for end in range(1, len(parts)):
                parent = '/'.join(parts[:end]).casefold()
                require(parent not in seen or seen[parent], 'File is also a parent directory')
        require(archive.testzip() is None, 'ZIP CRC failure')
        destination.mkdir(parents=True, exist_ok=False)
        for member, parts, directory, mode in entries:
            path = destination.joinpath(*parts)
            if directory:
                path.mkdir(parents=True, exist_ok=True)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, path.open('xb') as target:
                shutil.copyfileobj(source, target)
            if os.name == 'posix':
                path.chmod(mode)
    print('PASS_UNPACKED', len(entries))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--dest', type=Path, required=True)
    args = parser.parse_args()
    unpack(args.archive, args.dest)

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        print('REFUSED:', error, file=sys.stderr)
        sys.exit(1)
