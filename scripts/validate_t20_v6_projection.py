#!/usr/bin/env python3
"""Validate the new public object, independently of the private package PASS.

All registered bodies are checked regardless of suffix. This is source integrity,
publication boundary and current-record binding, not mathematical acceptance.
"""
from __future__ import annotations
import collections
import hashlib
import json
import pathlib
import re
import sys
import subprocess
from functools import lru_cache

import validate_v5_successors as continuation_owners

from resolve_t20_v6_source import (
    HISTORICAL_PROSE, HISTORICAL_PROSE_PUBLIC_PATHS, HISTORICAL_PROSE_REVISION,
    historical_source_bytes, source_bytes, MEDIATOR_GUIDE, mediator_guide_source_bytes,
    HISTORICAL_PROSE_REVISIONS, MEDIATOR_APPROXIMATION, FISHER_AUDIT, readonly_git_diff,
    TYPED_GUIDES, typed_guide_source_bytes,
    ADMIN_GUIDES, administrative_guide_source_bytes,
    CONTINUATION_COPY_ROOT, continuation_duplicate_paths,
    CHECKPOINT_COPY_PATHS, checkpoint_duplicate_paths,
    CHECKPOINT_RECORD_COPY_PATHS, checkpoint_record_duplicate_paths,
    CHECKPOINT_PACKAGE_COPY_PATHS, checkpoint_package_duplicate_paths,
    CHECKPOINT_CODE_COPY_PATHS, checkpoint_code_duplicate_paths,
    CONTINUATION_REGISTRY_PATH,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'research/t20-v6-20261012'
MANIFEST = PREFIX + '/PUBLIC_PROJECTION_MANIFEST.json'
BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
SOURCE_UNIVERSE = 'a85d700cfe7dd69800da4568925e60f7e084987764ea135756674575912d55cb'
CONTRIBUTION_REGISTER = 'c8b485a2298809c94b6b1b682278d24e806002c448303326bd6ab46283bb8aaf'
SHA = re.compile(r'[0-9a-f]{64}\Z')
# Actual locators have a concrete component, unlike regex-only detection fixtures.
PRIVATE = re.compile(r'(?<![A-Za-z0-9/])/(?:workspace|mnt/(?:data|c)|home|tmp|Users|root|opt|usr/local)/[A-Za-z0-9_.-][^\s`"\'<>\[\]{}\\|]*|(?<![A-Za-z0-9])[A-Za-z]:\\(?:\\)?(?:Users|workspace)\\')
UUID = re.compile(r'\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b', re.I)
PUBLIC_CITATION_UUIDS = {
    'fa8a2dceb11330669cf39dbb5dd02ca0b58b949d699b61bfd5eb3d53eefe9da8': 'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8',
    '7f12edad1756dcfb5c29fd6c0c8ee2c1df9120bf2306028ba1cd2bb7f9a4309c': '480c45bd6774594309f907a1287f794299e81dcb4ed43827c253cd5d7704eca4',
    'd2afbb10e8c04806bc0e1244210c3c685c573ceaba06a4d17ab6c1eb3bdcb75b': 'bb074141092db975476a224663d6878c678a0de5a01a680030f98956bf7d54b2',
}
SYNTHETIC_FIXTURES = {
    '7230eb7f76593b74ed7872862c0ec7405c16389ebc1307b7260ece6992d11d37': {'/'+'tmp/no-source', '/'+'tmp/A.lean'},
    '9ecf81f0c65bcbc0f7eb2412810e6482f8dda2e0c21771ba96b7e7f7b8c2a5dc': {'/'+'home/private-owner/source.json', '/'+'home/private', '/'+'home/private/approval', '/'+'home/private/source'},
    'a7334c42d58f90331ef8de0e975763ae46bae46356e5503a89ea2f9d0980e1db': {'/'+'tmp/outside'},
    'd72dea559413e805a4e8ca87c5e9c081f853b5d81d348f568667c30b0f52ace0': {'/'+'tmp/a'},
}

# Exact reviewed synthetic controls and public scholarly citation occurrences.
# Body identity plus line/URL digest binds every exception; no suffix exemption.
REVIEWED_SCAN_LINES = {'00ace739e297ae488c5c2c89594e2c4364274d3b8e13a7ab92babdfd5d1fe68d': {'8adc14da5a8269b042e4b2b8b968c8b488603043ae180e847d56bc3eaaea9650'}, '083134fb77ea638e06c14bf7b508f2c242e9fa6832b61ce07b8b9cebfa711279': {'e79ce3cee29a2f99634dd1590e4715cd5e33955f8ab4bbfd65fa4c5ee64f8baa', '8adc14da5a8269b042e4b2b8b968c8b488603043ae180e847d56bc3eaaea9650'}, '174df8936e13cc7a743d07faddd1b9a2b15fcefce05732a680b28c020ee55e93': {'af5fa5b57318ae25d2b0227a51dbc03993f8ba32146252c4d31c9918812c8dbf', '228bee8692f41ca0a9e3f37eecdb4169cc4b15025be310bf7f7208235fa7f551', '99e0a3c235ce0d59e81ab0ccff8d279abbb41178182c316838cf2343b681f9d0', '64008f5930a70253e6907bcbd0e19eeeaafe8ee5e33560cacfa6b9a992db69e8', 'f715bde14d655246b1544a61caafee6493dd111a81692a124af3a4f3ec071a10', 'b5a866c42e6556f3e2bb18850d45e2f5cefc9c2884c61a0bfacaf3039bcc509d', 'a8a83ff898232d2002679976ad35bbbf19489d10daa6d39ca7b46889ac6d3c61'}, '1a651b5d929dac3cbeeb6f4fd0d1190ffc100e3dad7c1cb341071371cae01860': {'492b4ef20689176cf84ba092a811dd93ca0a713618ca00db6cca4a642f452988', 'eabb85ea7857d9e899de17706deee7f99ac7dd695471eb1a1bb88f740ec7ceb8', '32b904de45a6cd723d1bebb3648bb12ab3f82ece76bb745d7efe6ea4cfa6e8fa', '99726308da943e9b47f8316ec747663908b8bbd192f373f2cf1c5eb2d12cedad', '9ecee31a965f89a8367f907288d460853a0815225c8d84b0f005acdbb9166acb'}, '1aea34cc0b4c058f0e88583aa2c1a6430cb8a9c19f15722a0fc1f002ef23d208': {'657632ca779edc15a7dcc5fafc696c37227d949eada49cc0e8ce8c8e5c08069e'}, '2085d86e996ae1c83c74d17f8fe586296161fe5b93acd9e9a074707e9a373bd0': {'a16f6e0c17207774eec28d3fef54a8e6e38484dca963c29a2fbfce09caaa79f2', 'bf19c2c6477bdb223575c68a8e8a14b4598980c16ef94f0f01dcb419b88ecdcb'}, '20ee1f9e79572333cde5178f3fe7d8a690b946a803a4c847a2a4ae1c9f187a43': {'800de93d20615a255d2a883e970485032e752d0d13d7d80b16fce82c4a7d7c1a'}, '22cc02be8aaddb696fbd786397ab2f679b9897d80eb9f3fad3152fc7c81c4816': {'e79ce3cee29a2f99634dd1590e4715cd5e33955f8ab4bbfd65fa4c5ee64f8baa'}, '255d5d809b5ea19d0617127264c8bf90022cb5816671f823b6445aaff9c0a067': {'a2a9de617da3c5656a42bf58710e0825425702f4d66d7960ee397240d0d8c554'}, '2ee2ae53933789c7a81f4e4ee1d02afb482fd7ba3ffb6ddee00ff6de95f190e9': {'8867055ca530c6e885093d413d8cca510e455e6537e8780fd34d8260630d4ebb'}, '3ea1f8ad6ceeb009e45804d707d8dbcdfe8bbf887f04a60cf031c0d3e4e7b1e2': {'4e413ef146926e8efaa806792800d3c24e5157b56b3bcef5dbc52bae9456c102', '5a8325a1d2899585f60e5ea8c909456a45725f5bf2035f929fefa46a01dd6194', '6a83999493edabd8024bdfcea87398175423fe658a509160923a3f5c7e917763', '3231b83f4a8956c703d936bc4a7737f04605b00ab37a01b09bc2a39cddcda532', '3b2c42ce0e2aa8625253240b076dececc38f0cfa9a89fd9cf1f1ceb8197a8353'}, '59e319d456de31657819e7d2c6a66908eb37e758568a187e5ae6112a673c5f9a': {'e79ce3cee29a2f99634dd1590e4715cd5e33955f8ab4bbfd65fa4c5ee64f8baa', '8adc14da5a8269b042e4b2b8b968c8b488603043ae180e847d56bc3eaaea9650'}, '6fdc119704401d1628d8dc878d07663595373d1ef21a57b174d8c801967aadfc': {'91a72d045ae0254526699e718e97396cb5fe45b8e90a5b158c8aed8cd003a5ce', '586a696bf5c20873c55ce919c50ebbc51fe721a3819c73f951224f5fe3464cd3'}, '7fa3160392da81cb8ca2b80320e203ed61de00987a71cd77a83a86617ffea7b2': {'e79ce3cee29a2f99634dd1590e4715cd5e33955f8ab4bbfd65fa4c5ee64f8baa'}, '878c562eed0f42714da8f223c68e9342629be07cf3f08f14e76b904df9df8e41': {'c8fb159825d302cb299e616ff80f178be10c2ea22ef4a9a8171f02f743baefb5', '155f6da7b965677497605904a35bf95473bdb1ff239ec17bdffccfb2f5e843c3', 'b19e757960cf2d45eb8663c593c87d1b7d7341660e98db30314567ec90e7c7b2'}, 'a9244bab67ea1b6fcacdaea2c5a1b4be9afbe00b72b94267b3c7252c31c0de16': {'a2a9de617da3c5656a42bf58710e0825425702f4d66d7960ee397240d0d8c554'}, 'aa91bb26d41438eb25b18406b4e6616b8467d7bd89ec8cef03851ae10268aeb1': {'18867c72c6aaa19a47e6eef68e93d848296a4d22872fa778caf6c513cfbdfaa8', '9556893428546c36080659fd3cf8b58a85bd8aa4aa00c505bd7cf9a96af13dba'}, 'ad56a638e3108984e757b13c3ccd6f5a0bf17f299d50b7a390230ca07b941d4e': {'00ba328970aca373b998d3558024b002477e461d31111154df5334185024b0dd', '2bad279688229ea91406af28979c14d575f32e460c4635ac4aa76fec46730686', '063a453186549277acf9ffd8b8b112f4b60dad5c92df9020a65ac5349cda92df', '975eb8625bb572a1f8e0ebbd986ac19ed3dfabdf4bc7fe10832528b41f4ca0cd'}, 'f77e456b0b99b7b932013e84bacf105ebc07508e30384b5ca96bbeb4e23f17a4': {'ec6d8d3018acd8e69ce3dc1c42b407d3c859583022bad39ea330ee14ad3df80b'}, 'fabaae8ae786bc20a0b810c12a9cfa726ab991b18bc5d9b35a97da591d06a514': {'4b0e86e2da10c9c826fbe57b3d0003e3f1b46206b4cd2c789f9d74f069c2147f'}}
REVIEWED_PUBLIC_URLS = {'083134fb77ea638e06c14bf7b508f2c242e9fa6832b61ce07b8b9cebfa711279': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}, '335f6b5f8fb160818d98e06faac08d0ad15b5b9c7ce7b02089d077fc5a055baa': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}, '0a579c0f0db45194c35b4acdb14238dce71e56fcdfa33828053f78b282daf3d7': {'cd5b870ffb0a71bbb8413c6706384002b8cfe3e0716f2707c5e025a9e7782448', '60b2213e0c8fa56c913a2a07914bc3a84a783055c58812bb8539e1b9ceea56d4'}, '59e319d456de31657819e7d2c6a66908eb37e758568a187e5ae6112a673c5f9a': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}, '6c463a8abf407266514297d9945ad985b3b5c68aa4ac6b8462008a989907ee32': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}, '977790ceaeafcb93a6d45807d19ba80aba28ced6d9c60145c38b6eb1b96741fa': {'480c45bd6774594309f907a1287f794299e81dcb4ed43827c253cd5d7704eca4'}, 'd155bfb12a59f7fa2b87a31c15629e2c03153d437459bf834be3dd0470503ff9': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}, 'fc05a4fed7ddb378de932e2d92ddacdf073d66f240d7761e351b26575ba307e8': {'bfcbecef31a7ed9e6a2389cc3610eeb6f87e9ead3e00bac7bcab277459beeea8'}}

def reviewed_scan_text(text, body_sha256):
    lines = REVIEWED_SCAN_LINES.get(body_sha256, set())
    if lines:
        text = ''.join(('\n' if line.endswith('\n') else '')
                       if sha256(line.rstrip('\r\n').encode()) in lines else line
                       for line in text.splitlines(keepends=True))
    urls = REVIEWED_PUBLIC_URLS.get(body_sha256, set())
    for match in reversed(list(re.finditer(r'https?://[^\s<>`"\'{}\[\]]+', text))):
        url = match.group().rstrip(').,;]')
        if sha256(url.encode()) in urls:
            text = text[:match.start()] + (' ' * len(url)) + text[match.start()+len(url):]
    return text


def sha256(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('invalid repository path')
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or any(p in ('..', '.') for p in value.split('/')) or '' in value.split('/'):
        raise ValueError('unsafe repository path')
    return path

def private_locators(text):
    return {m.group().rstrip('.,;:)') for m in PRIVATE.finditer(text)}

def private_uuid(text, body_sha256):
    allowed = PUBLIC_CITATION_UUIDS.get(body_sha256)
    if allowed:
        # Remove only the exact reviewed public citation span. A repeated UUID
        # elsewhere in the prose or a changed source receives no exception.
        for match in re.finditer(r'https?://[^\s<>`"\']+', text):
            url = match.group().rstrip(').,;]')
            if sha256(url.encode()) == allowed:
                text = text[:match.start()] + (' ' * len(url)) + text[match.start()+len(url):]
    return bool(UUID.search(text))

@lru_cache(maxsize=8)
def _origin_records(root):
    document = json.loads((pathlib.Path(root) / PREFIX / 'ORIGIN_REFERENCES.json').read_bytes())
    if document.get('schema') != 't20-v6-exact-origin-references-v1':
        return {}
    return {row['repository_path']: row for row in document['records']}

def origin_reference_text(src, text, root):
    """Occurrence-local scan copy; original coordinates are not local promises.

    Full body identity and all occurrence counts are required. New prose,
    mutated sources and other documents receive no exemption.
    """
    if not src.startswith(PREFIX + '/'):
        return text
    try:
        row = _origin_records(str(root)).get(src)
        if not row or row.get('origin_context') != 'preserved_source_document' or sha256(text.encode('utf-8')) != row['public_sha256']:
            return text
        replacements = []
        for reference in row['references']:
            target = '/'.join(reference['components'])
            safe_path(target)
            if not reference['occurrences'] or text.count(target) != reference['occurrences']:
                return text
            replacements.append(target)
        for target in replacements:
            text = text.replace(target, 'original-reference:' + sha256(target.encode()))
        return text
    except (OSError, KeyError, ValueError, TypeError):
        return text

def check_object(root, row):
    errors = []
    identity = row.get('source_sha256', '')
    if not SHA.fullmatch(identity):
        errors.append('invalid source identity')
    disposition = row.get('disposition')
    if disposition in ('IDENTITY_ONLY', 'NOT_PUBLISHED'):
        if any(key in row for key in ('repository_path', 'public_sha256', 'public_bytes')):
            errors.append('nonpublished source has a public body')
        return errors
    if disposition not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
        return errors + ['unknown disposition']
    try:
        relative = safe_path(row['repository_path'])
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('source symlink or escaped root')
        if (relative.as_posix() in HISTORICAL_PROSE
                or relative.as_posix() == CONTINUATION_REGISTRY_PATH
                or relative.as_posix() in CHECKPOINT_RECORD_COPY_PATHS
                or relative.as_posix() in CHECKPOINT_CODE_COPY_PATHS
                or (relative.as_posix().startswith(CONTINUATION_COPY_ROOT) and relative.suffix == '.lean')):
            body = source_bytes(root, row)
        elif row.get('repository_revision') is not None:
            if disposition != 'REUSE' or row['repository_revision'] != BASE:
                raise ValueError('invalid pinned historical reuse')
            body = subprocess.check_output(['git', 'show', BASE + ':' + relative.as_posix()], cwd=root)
        else:
            body = path.read_bytes()
    except (KeyError, OSError, ValueError, subprocess.CalledProcessError):
        return errors + ['missing or unsafe public source']
    if sha256(body) != row.get('public_sha256') or len(body) != row.get('public_bytes'):
        errors.append('public body differs')
    if disposition in ('REUSE', 'ADD_EXACT') and (sha256(body) != identity or len(body) != row.get('source_bytes')):
        errors.append('false byte identity')
    if disposition == 'PROJECT' and sha256(body) == identity:
        errors.append('projection does not change identity')
    # Existing public objects retain their current bytes and existing repository gates.
    if disposition != 'REUSE':
        try:
            text = reviewed_scan_text(body.decode('utf-8'), sha256(body))
            allowed = SYNTHETIC_FIXTURES.get(identity, set()) if sha256(body) == identity else set()
            if private_locators(text) - allowed:
                errors.append('private machine locator')
            if re.search(r'(?:library-file:|project-file:|sandbox:/|libfile_[A-Za-z0-9]{12,}|file-[A-Za-z0-9]{16,})', text):
                errors.append('private platform linkage requires qualification')
            if private_uuid(text, sha256(body)):
                errors.append('nonpublic UUID linkage requires qualification')
        except UnicodeDecodeError:
            errors.append('unqualified binary source')
    return errors


def check_preserved_roots(root, objects):
    """Keep every protected baseline obligation and its finite typed changes.

    The original bodies and both proof occurrences authenticate before an
    absence can be admitted. Changed bytes, modes, renames or other removals
    are not historical-source dispositions. All source-universe rows remain.
    A complete authenticated current continuation-owner edition has its
    separate M-only admission; its original public bodies remain pinned.
    """
    errors, authenticated = [], set()
    for path, (blob, identity, size) in HISTORICAL_PROSE.items():
        try:
            if path in HISTORICAL_PROSE_PUBLIC_PATHS:
                row = objects.get(identity, {})
                if row.get('repository_path') != path:
                    raise ValueError('historical public source path differs')
                source_bytes(root, row)
            else:
                historical_source_bytes(root, path, HISTORICAL_PROSE_REVISIONS[path], blob)
            authenticated.add(path)
        except (KeyError, OSError, ValueError, subprocess.CalledProcessError) as exc:
            errors.append('historical prose: ' + path + ': ' + str(exc))
    guide_authenticated = False
    try:
        mediator_guide_source_bytes(root, allow_original=True)
        guide_authenticated = True
    except (ValueError, OSError):
        pass  # A guide change is never excused when this finite check fails.
    typed_guides_authenticated = set()
    for path in TYPED_GUIDES:
        try:
            typed_guide_source_bytes(root, path, allow_original=True)
            typed_guides_authenticated.add(path)
        except (ValueError, OSError):
            pass  # No exception for a changed, missing or unsafe guide.
    administrative_guides_authenticated = set()
    for path in ADMIN_GUIDES:
        try:
            administrative_guide_source_bytes(root, path, allow_original=True)
            administrative_guides_authenticated.add(path)
        except (ValueError, OSError):
            pass  # A changed, missing or unsafe guide receives no allowance.
    protected = ['experiments/orthemology-v5', 'experiments/orthemology-v5-continuations',
                 'experiments/orthemology-v5-successors', 'docs/provenance/v5-consolidation',
                 'docs/provenance/v5-research-continuations', 'docs/provenance/v5-successors',
                 'research/t20-live-20261009']
    # Check both boundaries: a staged M/T/A must not disappear behind a
    # combined worktree D or an unstaged return to original bytes.
    copy_authenticated = None
    owner_authenticated = None
    checkpoint_authenticated = None
    record_authenticated = None
    package_authenticated = None
    code_authenticated = None
    for cached in (True, False):
        result = readonly_git_diff(root,
            ['git', '--no-replace-objects', 'diff', *(['--cached'] if cached else []),
             '--no-ext-diff', '--no-textconv', '--no-renames', '--name-status',
             '-z', BASE, '--', *protected])
        try:
            changes = result.stdout.decode('utf-8').rstrip('\0').split('\0') if result.stdout else []
            if result.returncode or len(changes) % 2:
                raise ValueError('protected baseline comparison unavailable')
            if copy_authenticated is None and any(
                    status == 'D' and path.startswith(CONTINUATION_COPY_ROOT)
                    for status, path in zip(changes[::2], changes[1::2])):
                copy_authenticated = continuation_duplicate_paths(root)
            if checkpoint_authenticated is None and any(
                    status == 'D' and path in CHECKPOINT_COPY_PATHS
                    for status, path in zip(changes[::2], changes[1::2])):
                checkpoint_authenticated = checkpoint_duplicate_paths(root)
            if record_authenticated is None and any(
                    status == 'D' and path in CHECKPOINT_RECORD_COPY_PATHS
                    for status, path in zip(changes[::2], changes[1::2])):
                record_authenticated = checkpoint_record_duplicate_paths(root)
            if package_authenticated is None and any(
                    status == 'D' and path in CHECKPOINT_PACKAGE_COPY_PATHS
                    for status, path in zip(changes[::2], changes[1::2])):
                package_authenticated = checkpoint_package_duplicate_paths(root)
            if code_authenticated is None and any(
                    status == 'D' and path in CHECKPOINT_CODE_COPY_PATHS
                    for status, path in zip(changes[::2], changes[1::2])):
                code_authenticated = checkpoint_code_duplicate_paths(root)
            if owner_authenticated is None and any(
                    status == 'M' and path in continuation_owners.PRESERVATION_OWNER_PATHS
                    for status, path in zip(changes[::2], changes[1::2])):
                owner_authenticated = set()
                try:
                    # The projection gate needs these four literal owner
                    # descriptors, not a replacement preservation inventory.
                    original_owners = {
                        path: {'path': path, 'bytes': size, 'sha256': identity,
                               'git_blob_sha1': blob}
                        for path, (blob, identity, size) in
                        continuation_owners.PRESERVATION_OWNER_ORIGINAL.items()}
                    owner_authenticated = set(
                        continuation_owners._preservation_owner_bytes(root, original_owners))
                except (ValueError, OSError):
                    pass  # No modification allowance for an unqualified edition.
            if any(not ((status == 'D' and path in authenticated) or
                        (status == 'D' and path in (copy_authenticated or ())) or
                        (status == 'D' and path in (checkpoint_authenticated or ())) or
                        (status == 'D' and path in (record_authenticated or ())) or
                        (status == 'D' and path in (package_authenticated or ())) or
                        (status == 'D' and path in (code_authenticated or ())) or
                        (status == 'M' and path == MEDIATOR_GUIDE and guide_authenticated) or
                        (status == 'M' and path in typed_guides_authenticated) or
                        (status == 'M' and path in administrative_guides_authenticated) or
                        (status == 'M' and path in (owner_authenticated or ())))
                   for status, path in zip(changes[::2], changes[1::2])):
                errors.append('preserved v5 or prior T20 baseline changed')
        except (ValueError, UnicodeError):
            errors.append('preserved v5 or prior T20 baseline comparison unavailable')

    return list(dict.fromkeys(errors))


def check_public_inventory(root, rows, controls):
    """Keep every manifest row; authenticate the one finite ADD_EXACT absence."""
    declared = {r['repository_path'] for r in rows if r['disposition'] in ('ADD_EXACT', 'PROJECT')}
    expected = declared | set(controls['files']) | {MANIFEST, PREFIX + '/PUBLIC_CONTROLS.json'}
    actual = {p.relative_to(root).as_posix() for p in (root / PREFIX).rglob('*') if p.is_file()}
    for historical in (MEDIATOR_APPROXIMATION, FISHER_AUDIT):
        if historical not in expected or historical in actual:
            continue
        selected = [r for r in rows if r.get('repository_path') == historical]
        try:
            if len(selected) != 1:
                raise ValueError('missing or duplicate approximation owner')
            source_bytes(root, selected[0])
        except (KeyError, OSError, ValueError, subprocess.CalledProcessError):
            return ['public inventory has an unqualified historical absence']
        expected.remove(historical)
    if actual != expected:
        return ['public inventory differs: ' + str(sorted(actual ^ expected)[:10])]
    return []


def validate(root=ROOT):
    manifest_bytes = (root / MANIFEST).read_bytes()
    manifest = json.loads(manifest_bytes)
    errors = []
    if manifest.get('schema') != 'orthemology-t20-v6-public-projection-v1' or manifest.get('base_commit') != BASE:
        errors.append('wrong public object or baseline')
    if manifest.get('scientific_acceptance') is not False or manifest.get('t21_started') is not False:
        errors.append('unauthorized scientific state')
    rows = manifest['objects']
    by_hash = {r['source_sha256']: r for r in rows}
    if len(rows) != 28478 or len(by_hash) != len(rows):
        errors.append('source universe missing or duplicated')
    if sha256(('\n'.join(sorted(by_hash)) + '\n').encode()) != SOURCE_UNIVERSE:
        errors.append('source universe identity differs')
    counts = dict(collections.Counter(r['disposition'] for r in rows))
    if counts != manifest['counts'] or counts.get('REUSE') != 5625:
        errors.append('selection count or saved reuse differs')
    baseline_paths = set(subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASE], cwd=root, text=True).splitlines())
    errors.extend(check_preserved_roots(root, by_hash))
    for path, binding in _origin_records(str(root)).items():
        owner = by_hash.get(binding['source_sha256'], {})
        if owner.get('repository_path') != path or owner.get('public_sha256') != binding['public_sha256']:
            errors.append('original reference owner differs')
            continue
        text = (root / path).read_text(encoding='utf-8')
        if origin_reference_text(path, text, root) == text:
            errors.append('original reference occurrences differ')
    for row in rows:
        errors.extend(row['source_sha256'] + ': ' + error for error in check_object(root, row))
        if row['disposition'] == 'REUSE' and row['repository_path'] not in baseline_paths:
            errors.append('reused path absent from pinned baseline')
        if row['disposition'] in ('ADD_EXACT', 'PROJECT') and (row['repository_path'] in baseline_paths or not row['repository_path'].startswith(PREFIX + '/')):
            errors.append('new object is not additive in the public projection')
        for dependency in row.get('required_dependencies', []):
            if dependency not in by_hash:
                errors.append('undeclared dependency identity: ' + row['source_sha256'])
            elif row['disposition'] in ('REUSE', 'ADD_EXACT', 'PROJECT') and by_hash[dependency]['disposition'] not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
                errors.append('declared publication dependency is not available: ' + row['source_sha256'])
    # Manifest inventory is explicit; generated controls and navigation are separate.
    controls_bytes = (root / PREFIX / 'PUBLIC_CONTROLS.json').read_bytes()
    controls = json.loads(controls_bytes)
    for label, body in [('manifest', manifest_bytes), ('control inventory', controls_bytes)]:
        text = body.decode('utf-8')
        if private_locators(text) or private_uuid(text, sha256(body)) or re.search(r'(?:library-file:|project-file:|sandbox:/|libfile_[A-Za-z0-9]{12,}|file-[A-Za-z0-9]{16,})', text):
            errors.append('private identifier in public metadata: ' + label)
    for relative, digest in controls['files'].items():
        safe_path(relative)
        body = (root / relative).read_bytes()
        if sha256(body) != digest:
            errors.append('public control differs: ' + relative)
        text = body.decode('utf-8')
        if private_locators(text) or private_uuid(text, sha256(body)) or re.search(r'(?:library-file:|project-file:|sandbox:/|libfile_[A-Za-z0-9]{12,}|file-[A-Za-z0-9]{16,})', text):
            errors.append('private identifier in public control: ' + relative)
    errors.extend(check_public_inventory(root, rows, controls))
    register_bytes = (root / PREFIX / 'research-v6/synthesis/CROSS_CONTRIBUTIONS.json').read_bytes()
    register = json.loads(register_bytes)
    if sha256(register_bytes) != CONTRIBUTION_REGISTER:
        errors.append('qualified current contribution register differs')
    if len(register['records']) != 15:
        errors.append('contribution cardinality differs')
    for contribution in register['records']:
        row = by_hash.get(contribution['sha256'], {})
        if row.get('disposition') not in ('REUSE', 'ADD_EXACT', 'PROJECT'):
            errors.append('current contribution absent: ' + contribution['id'])
        if row.get('repository_path') != PREFIX + '/research-v6/' + contribution['artifact']:
            errors.append('current contribution artifact binding differs: ' + contribution['id'])
        review = root / PREFIX / 'research-v6' / contribution['independent_review']
        if not review.is_file():
            errors.append('current review absent: ' + contribution['id'])
    from resolve_t20_v6_source import validate_graph
    errors.extend(validate_graph(root, by_hash))
    return errors, counts

def main():
    errors, counts = validate()
    for error in errors:
        print('[FAIL]', error)
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'scope': 'PUBLIC_SOURCE_COVERAGE_AND_BOUNDARIES_ONLY', 'counts': counts, 'scientific_acceptance': False}, sort_keys=True))
    return int(bool(errors))

if __name__ == '__main__':
    sys.exit(main())
