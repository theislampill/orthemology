"""Bounded generation using authenticated held hashes, never held Python opens.

This is a separately qualified invocation route, not the literal generator CLI.
Production source and its input-exclusion policy remain unchanged.
"""
from pathlib import Path
import hashlib, json, os, subprocess, sys, types
import yaml

def import_file(path, name):
    path = Path(path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

def verified_hash_lookup(repo, held, git):
    repo = Path(repo).resolve()
    stage = {}
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            metadata, name = entry.split(b'\t', 1)
            mode, oid, level = metadata.decode().split()
            if level != '0': raise RuntimeError('Conflicted source index')
            stage[name.decode()] = (mode, oid)
    held_by_path = {row['path']: row for row in held}
    held_oids = {row['published_metadata']['git_blob'] for row in held}
    if len(held_by_path) != 5 or len(held_oids) != 5:
        raise RuntimeError('Held population differs')
    aliases = {path for path, (_, oid) in stage.items() if oid in held_oids}
    if aliases != set(held_by_path):
        raise RuntimeError('Held object aliases differ')
    for path, row in held_by_path.items():
        expected = row['published_metadata']
        if stage.get(path) != (expected['mode'], expected['git_blob']):
            raise RuntimeError('Held staged identity differs')
        p = repo / path
        if p.is_symlink() or not p.is_file() or p.stat().st_size != row['bytes'] or p.stat().st_mode & 0o111:
            raise RuntimeError('Held path metadata differs')
    # Native Git comparison is explicitly mechanical; it is outside the Python
    # open guard and is not described as no native access to protected objects.
    git(repo, 'diff', '--quiet', 'HEAD', '--', *sorted(held_by_path), shadow=True)
    uses = []
    def lookup(path):
        relative = Path(path).resolve().relative_to(repo).as_posix()
        if relative in held_by_path:
            uses.append(relative)
            return held_by_path[relative]['sha256']
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return lookup, uses, stage

def state_bytes(repo, held, git):
    repo = Path(repo)
    lookup, uses, stage = verified_hash_lookup(repo, held, git)
    module = import_file(repo / 'scripts/generate_current_state.py', 'bounded_current_state_' + str(os.getpid()))
    module.sha256 = lookup
    original = yaml.safe_load((repo / 'docs/current-state.yaml').read_text())
    document = {
        'schema': 'orthemology-current-state-v1',
        'note': ('GENERATED derived block — edit only the authored block, then run '
                 'scripts/generate_current_state.py. CI checks for drift.'),
        'authored': original.get('authored', {}),
        'derived': module.derive(),
    }
    value = yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=100).encode()
    if set(uses) != {r['path'] for r in held} or len(uses) != 5:
        raise RuntimeError('Unexpected held metadata lookup population in current state')
    return value, {'route': 'UNMODIFIED_DERIVE_WITH_AUTHENTICATED_HELD_HASH_CALLBACK',
                   'held_metadata_lookups': uses, 'tracked_paths': len(stage)}

def manifest_bytes(repo, held, git):
    repo = Path(repo)
    lookup, uses, stage = verified_hash_lookup(repo, held, git)
    excluded = 'docs/provenance/RELEASE-MANIFEST.sha256'
    paths = sorted(path for path in stage if path != excluded)
    value = ('\n'.join(lookup(repo / path) + '  ' + path for path in paths) + '\n').encode()
    if set(uses) != {r['path'] for r in held} or len(uses) != 5:
        raise RuntimeError('Unexpected held metadata lookup population in release manifest')
    return value, {'route': 'EXACT_SORTED_LF_MANIFEST_ALGORITHM_WITH_AUTHENTICATED_HELD_HASHES',
                   'held_metadata_lookups': uses, 'manifest_rows': len(paths)}

def check_state(repo, held, git):
    value, receipt = state_bytes(repo, held, git)
    if value != (Path(repo) / 'docs/current-state.yaml').read_bytes():
        raise RuntimeError('Metadata-backed state drift')
    manifest, manifest_receipt = manifest_bytes(repo, held, git)
    if manifest != (Path(repo) / 'docs/provenance/RELEASE-MANIFEST.sha256').read_bytes():
        raise RuntimeError('Metadata-backed manifest drift')
    return {'state': receipt, 'manifest': manifest_receipt}

def check_public_state_surfaces(repo, held, git):
    from types import SimpleNamespace
    repo = Path(repo)
    module = import_file(repo / 'scripts/validate_current_state.py', 'bounded_state_surfaces_' + str(os.getpid()))
    calls = []
    def bounded_delegate(argv, **kwargs):
        expected = [sys.executable, str(repo / 'scripts/generate_current_state.py'), '--check']
        if argv != expected or kwargs != {'cwd': str(repo), 'stdout': subprocess.DEVNULL}:
            raise RuntimeError('Unexpected child process in state-surface validator')
        value, receipt = state_bytes(repo, held, git)
        calls.append(receipt)
        return 0 if value == (repo / 'docs/current-state.yaml').read_bytes() else 1
    module.subprocess = SimpleNamespace(call=bounded_delegate, DEVNULL=subprocess.DEVNULL)
    try:
        module.main()
    except SystemExit as exc:
        if exc.code not in (None, 0): raise
    if len(calls) != 1 or module.FAILS:
        raise RuntimeError('Public state-surface checks did not finish successfully')
    return {'route': 'UNCHANGED_PUBLIC_STATE_ASSERTIONS_WITH_METADATA_BACKED_DRIFT_DELEGATE',
            'delegated_state_checks': calls}
