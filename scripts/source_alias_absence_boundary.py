"""Admission for the single-checkout hosted source-absence regression."""
from pathlib import Path
import os
import re
import stat

PROTECTED_PATHS = (
    'research/t20-v6-20261012/sources/815d2671067d5499f41aa4a77652789ea3a5aed3f299066fd00a6322bbd3bdf0/PRIVATE_RLGWO_R0F20.md',
    'research/t20-v6-20261012/sources/b2cbe07611a9fbe3ad609e90c7564d3aff0e63981a9d25e60ecf6c29db383150/OWNER_PUBLICATION_BOUNDARY.md',
    'research/t20-v6-20261012/sources/783ec97f86c27e118217bf7bf3b6b5a4588b98c7af51470df8844b11f13e5977/DAG.md',
    'research/t20-v6-20261012/sources/e6ac4075df1cea8288902ba64218355f279e8d395ec0d08b4f9a51d90523161e/READ_FIRST.md',
    'research/t20-v6-20261012/sources/984bac17f4801ecb3c8acb6456fca012a5d98919ee3f28070809834e6751a1cf/CODEX_PROMPT.md',
)

def validate_hosted_coordinates(repo, state, env, actual_head, actual_root, *, fresh):
    def require(value, message):
        if not value:
            raise RuntimeError(message)
    def ordinary(path):
        path = Path(path).absolute()
        require(all(not part.is_symlink() for part in (path, *path.parents)), 'Symlink in hosted coordinate')
        require(path.is_dir(), 'Hosted coordinate is not an ordinary directory')
        return path
    require(env.get('GITHUB_ACTIONS') == 'true'
            and env.get('GITHUB_REPOSITORY') == 'theislampill/orthemology'
            and env.get('GITHUB_EVENT_NAME') in ('push', 'pull_request')
            and env.get('RUNNER_OS') == 'Linux', 'Actual hosted repository admission is required')
    for key in ('GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT'):
        require(re.fullmatch(r'[1-9][0-9]*', env.get(key, '')) is not None, 'Missing hosted run identity')
    repo = ordinary(repo)
    temporary = ordinary(env.get('RUNNER_TEMP', ''))
    workspace = ordinary(env.get('GITHUB_WORKSPACE', ''))
    ordinary(repo / '.git')
    require(repo == workspace == Path(actual_root).absolute(), 'Hosted checkout root differs')
    require(not temporary.is_relative_to(repo) and not repo.is_relative_to(temporary), 'Runner state must be outside checkout')
    require(re.fullmatch(r'[0-9a-f]{40}', env.get('GITHUB_SHA', '')) is not None
            and actual_head == env['GITHUB_SHA'], 'Hosted checkout commit differs')
    state = Path(state).absolute()
    require(state == temporary / 'r0002-source-alias-absence' and not state.is_symlink(), 'Unexpected hosted state path')
    if fresh:
        require(not os.path.lexists(state), 'Hosted state is single-use')
    else:
        ordinary(state)
    require(not os.path.lexists(repo / '.git/objects/info/alternates'), 'Alternate checkout object stores are not admitted')
    return {'repository': env['GITHUB_REPOSITORY'], 'head': actual_head, 'repo': str(repo),
            'state': str(state), 'run_id': env['GITHUB_RUN_ID'], 'run_attempt': env['GITHUB_RUN_ATTEMPT'],
            'event': env['GITHUB_EVENT_NAME'], 'protected_body_integrity': 'UNKNOWN'}

def derive_held_metadata(repo, originals, stage, manifest):
    def require(value, message):
        if not value:
            raise RuntimeError(message)
    repo = Path(repo).absolute()
    rows = []
    for relative in PROTECTED_PATHS:
        require(relative in originals and relative in manifest, 'Required public protected metadata missing')
        mode, kind, blob, size = originals[relative]
        digest = Path(relative).parent.name
        require(mode == '100644' and kind == 'blob' and stage.get(relative) == (mode, blob),
                'Protected original/stage identity differs')
        require(re.fullmatch(r'[0-9a-f]{64}', digest) is not None and manifest[relative] == digest,
                'Protected public digest metadata differs')
        node = repo
        require(node.is_dir() and not node.is_symlink(), 'Unsafe protected root')
        for part in Path(relative).parts[:-1]:
            node /= part
            require(stat.S_ISDIR(node.lstat().st_mode), 'Protected ancestor is not an ordinary directory')
        info = (repo / relative).lstat()
        require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
                and info.st_nlink == 1 and info.st_size == size, 'Protected one-checkout metadata differs')
        rows.append({'path': relative, 'bytes': size, 'sha256': digest,
                     'published_metadata': {'mode': mode, 'type': kind, 'git_blob': blob}})
    held_oids = {row['published_metadata']['git_blob'] for row in rows}
    require(len(rows) == len(held_oids) == 5, 'Protected population is ambiguous')
    require({path for path, (_, oid) in stage.items() if oid in held_oids} == set(PROTECTED_PATHS),
            'Unexcluded protected stage alias')
    require({path for path, (_, kind, oid, _) in originals.items() if oid in held_oids} == set(PROTECTED_PATHS),
            'Unexcluded protected original alias')
    return rows
