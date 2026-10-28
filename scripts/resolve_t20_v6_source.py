#!/usr/bin/env python3
"""Resolve preserved source identities and reconstruct a qualified isolated suite.

This tool copies verified sources; it does not execute historical wrappers or
certify scientific acceptance. Same-named historical variants stay separate.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import os
import pathlib
import re
import stat
import struct
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'research/t20-v6-20261012'
PUBLIC = {'ADD_EXACT', 'PROJECT', 'REUSE'}
CURRENT_GRAPH_SHA256 = 'ce15fabe3966d210aadbbf51b0d1213c45d6f9397a3dfebbaa66257afc32b5ff'

# A finite current-copy class, separate from historical prose recovery. Its
# members are derived from existing frozen maps, not a second path catalogue.
CONTINUATION_COPY_ROOT = 'experiments/orthemology-v5-continuations/source-store/'
CONTINUATION_RETAINED_ROOT = 'experiments/orthemology-v5-successors/source-store/'
CONTINUATION_COPY_BASE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
CONTINUATION_LEGACY_BASE = '19de267cd41d2a5eeeb3eaf0b91562f706e2a916'
CONTINUATION_COPY_COUNT = 258
CONTINUATION_COPY_EXCLUDED = 'b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183'
CONTINUATION_COPY_METADATA = {
    'docs/provenance/v5-research-continuations/SOURCE_MAP.json':
        (5987769, '610fcbd8b9a46cf2d6fdd6a162721ec2dd63402ba08b341f3ed974bf20ccdd72'),
    'docs/provenance/v5-successors/SOURCE_MAP.json':
        (4978847, 'db90ad110ccc9c6a63454cf91ecec4605eed7fe243d18883d3cf501c58cb4883'),
    'docs/provenance/v5-successors/PRESERVATION.json':
        (379708, 'cd81d3b80d5183c1c01b637207d0afefd2b143ce4ee346808ca473a15eea6c4a'),
}


# Exactly reviewed historical-only prose, not a suffix/directory exemption.
# Ordinary reading uses the existing recognition chapter; original identities
# and the duplicate CP20 proof occurrence remain independently authenticated.
HISTORICAL_PROSE_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
HISTORICAL_PROSE = {
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/REPORT.md':
        ('15e864dd9b9a31a5203f31fe9b080261afc7de4e',
         '4bd8f0e5bcac178bf9eb890544fcba9fd60f6a1d08cdf2e0cc12bb6d2c4b4c1c', 15381),
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/VARIABLE_SHARING_REDUCTION.md':
        ('512266ec363346b6302292f69dafad32f1e067a9',
         '9420d38627e0dea98af9e8838485fb68ab08feb184ae254953f08585cfe2e71d', 1587),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md':
        ('cf657a78f972b7f98190139b2275a3381d288b66',
         '52631c602c1c8fede28dbe6da34480094caf6f441c1aec0293229cdfdf28a0be', 15839),
}
# Capture the original five-path contract before any later finite admissions.
ORIGINAL_HISTORICAL_PROSE_PATHS = tuple(HISTORICAL_PROSE)

# Two independently incorporated mediator bodies have a later exact audit anchor.
# The original five source revisions and their identities remain unchanged.
MEDIATOR_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
MEDIATOR_COORDINATION = 'experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md'
MEDIATOR_APPROXIMATION = 'research/t20-v6-20261012/research-v6/type_collective/ROBUST_FINITE_MEDIATOR_BOUND.md'
MEDIATOR_PROSE = {
    MEDIATOR_COORDINATION: ('a949e7e8fdb1fcf386d3580a034d9cb14f34e7d5',
        'c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7', 13985),
    MEDIATOR_APPROXIMATION: ('8c8b327bb642570307e50ddaef35850b508a80e6',
        '6d8c1b108c74df4638da79a147e6480b6edb9c2b562028c0d17758ab08d45406', 4388),
}
HISTORICAL_PROSE.update(MEDIATOR_PROSE)
HISTORICAL_PROSE_REVISIONS = {
    path: MEDIATOR_PROSE_REVISION if path in MEDIATOR_PROSE else HISTORICAL_PROSE_REVISION
    for path in HISTORICAL_PROSE}
HISTORICAL_PROSE_DISPOSITIONS = {
    path: 'ADD_EXACT' if path == MEDIATOR_APPROXIMATION else 'REUSE'
    for path in HISTORICAL_PROSE}
# This ADD_EXACT source is anchored at its actual original publication,
# independently of the five REUSE sources and two mediator dispositions.
FISHER_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
FISHER_AUDIT = 'research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md'
HISTORICAL_PROSE[FISHER_AUDIT] = (
    '4dd0bce99ab60c34752bda1e4102341b67350c79',
    '178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b', 29666)
HISTORICAL_PROSE_REVISIONS[FISHER_AUDIT] = FISHER_PROSE_REVISION
HISTORICAL_PROSE_DISPOSITIONS[FISHER_AUDIT] = 'ADD_EXACT'

# Four fully incorporated prose bodies; their formal/review components remain
# current, separate obligations. These literals extend only the finite route.
TYPED_PROSE_REVISION = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
TYPED_PROSE_IDENTITIES = {
    't13-opaque': ('b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236',
        'OPAQUE_ATOM_COMPLETENESS_PROOF_v3.md', 'ab7ccee9a98d5a88b8b79a6f0d6a010298bf3204',
        26969, 'identity-src-18324561d5a479234e08'),
    't13-residual': ('7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e',
        'RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md', '0692dd6d775e0391498c97c5b77e8c83cf32eb41',
        11482, 'identity-src-36405a21fb515a544d13'),
    't13-bridge': ('02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe',
        'HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md', 'a4d90c7d566d79394ca4755bf1d792e810d66880',
        19906, 'identity-src-210a260c6b65330bbabb'),
    't14-separation': ('5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a',
        'Intensional_Identity_Separation_and_Closed_Identity_Conversion.md', '4920e71de4ac0c17fa8a93f02cd891d65ea8ad74',
        48239, 'identity-src-ae495071a75fcc65a509'),
}
TYPED_SOURCE_KEYS = {key: 'experiments/orthemology-v5-successors/source-store/' + row[0] + '/' + row[1]
                     for key, row in TYPED_PROSE_IDENTITIES.items()}
TYPED_PROSE = {TYPED_SOURCE_KEYS[key]: (row[2], row[0], row[3])
               for key, row in TYPED_PROSE_IDENTITIES.items()}
TYPED_V5_SOURCE_IDS = {TYPED_SOURCE_KEYS[key]: row[4] for key, row in TYPED_PROSE_IDENTITIES.items()}
HISTORICAL_PROSE.update(TYPED_PROSE)
HISTORICAL_PROSE_REVISIONS.update({path: TYPED_PROSE_REVISION for path in TYPED_PROSE})
HISTORICAL_PROSE_DISPOSITIONS.update({path: 'REUSE' for path in TYPED_PROSE})

TYPED_GUIDES = {
    'experiments/orthemology-v5-successors/groups/t13-identity/README.md': (
        '0d228b107878098508dc31368517ac07fe688dff',
        '9492d888f684355f2f72f15e1da7ddca3525b2523e3a670c2da25d811c6eaf96', 7880,
        {'t13-opaque': 1, 't13-residual': 2, 't13-bridge': 1}),
    'experiments/orthemology-v5-successors/groups/t14-identity/README.md': (
        '09ea18f06905c0e5116375b2163737cf380755eb',
        'bd58d620ac8a0dd0bbd8a3eb51e0c254b73cf14ae795a48dc19c347ee69b9961', 16523,
        {'t14-separation': 5}),
}

MEDIATOR_GUIDE = 'experiments/orthemology-v5-successors/groups/t12-written/README.md'
MEDIATOR_GUIDE_BLOB = '7c6a9bfdeaf8372d3ea73ff8a06f4aefb17ef838'
MEDIATOR_GUIDE_SHA256 = 'e86297f6ff2e0b8abce4fd8d1fe66e57c64e43e83ecec664422b4ed7abf3440e'
MEDIATOR_GUIDE_BYTES = 18763

# The inherited duplicate is a path obligation, not an extra manifest object.
HISTORICAL_PROSE_PUBLIC_PATHS = tuple(
    path for path in HISTORICAL_PROSE
    if path != 'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md')


def historical_source_bytes(root, path, revision, git_blob):
    """Authenticate one finite original and reject any unsafe or wrong copy.

    Missing physical prose may use the pinned original Git object. A present
    copy must still match. No source is written, no fallback follows a failed
    read, and these checks do not qualify custody or historical execution.
    """
    binding = HISTORICAL_PROSE.get(path)
    if not binding or revision != HISTORICAL_PROSE_REVISIONS[path] or git_blob != binding[0]:
        raise ValueError('unqualified historical prose binding')
    root = pathlib.Path(root)
    if path in MEDIATOR_PROSE:
        require_mediator_context(root)
    elif path == FISHER_AUDIT:
        require_fisher_context(root)
    elif path in TYPED_PROSE:
        require_typed_context(root)
    blob, identity, size = binding

    def git(*args):
        result = subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs', *args],
            cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required historical Git objects unavailable')
        return result.stdout

    if git('cat-file', '-t', revision) != b'commit\n':
        raise ValueError('historical revision is not the pinned commit')
    expected_entry = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if git('ls-tree', '-z', revision, '--', path) != expected_entry:
        raise ValueError('historical path, blob or mode differs')
    body = git('cat-file', 'blob', blob)
    raw = b'blob ' + str(len(body)).encode() + b'\0' + body
    if (len(body), digest(body), hashlib.sha1(raw).hexdigest()) != (size, identity, blob):
        raise ValueError('historical source bytes differ')

    # A combined baseline/worktree diff can show D while the index contains a
    # wrong blob, mode or unresolved merge. Bind the actual staged original too.
    indexed = git('ls-files', '--stage', '-z', '--', path)
    expected_index = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    if indexed not in (b'', expected_index):
        raise ValueError('historical source index is conflicted or differs from its pinned original')

    target, entry = root, None
    parts = path.split('/')
    for index, part in enumerate(parts):
        target = target / part
        try:
            entry = target.lstat()
        except FileNotFoundError:
            entry = None
            continue
        if stat.S_ISLNK(entry.st_mode):
            raise ValueError('historical source path contains a symlink')
        if index < len(parts) - 1 and not stat.S_ISDIR(entry.st_mode):
            raise ValueError('historical source ancestor is not a directory')
    if entry is not None:
        if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
            raise ValueError('historical source is not a regular nonexecutable file')
        if target.read_bytes() != body:
            raise ValueError('present historical source differs from its pinned edition')
    return body


def require_fisher_context(root):
    """Bind this one Fisher source to the current inquiry chapter and review.

    This is a finite reader/source-owner contract. It does not re-prove the
    mathematics, retire the original, or qualify other incoming body links.
    """
    root = pathlib.Path(root)
    owner_path = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    cross_path = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    try:
        owners = json.loads(_regular_current_bytes(root, owner_path))
        cross = json.loads(_regular_current_bytes(root, cross_path))
        expected = dict(path=FISHER_AUDIT, repository_revision=FISHER_PROSE_REVISION,
            git_blob=HISTORICAL_PROSE[FISHER_AUDIT][0], role='historical-source',
            reading_source='consolidated-information-and-inquiry',
            basis='scientific-consolidation-review')
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] == FISHER_AUDIT]
        if bindings != [expected]:
            raise ValueError('the exact Fisher source disposition is required')
        for key, path, role in (
            ('consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current Fisher reading owner')
            admission, current_source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or current_source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or current_source['sha256'] != digest(current)):
                raise ValueError('current Fisher scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current Fisher work has lost its review owner')
        original = cross['sources']['fisher']
        forms = [f for w in cross['works'] for f in w.get('reading_forms', [])
                 if f.get('source') == 'fisher']
        relation = {'from': 'fisher', 'to': 'consolidated-information-and-inquiry',
                    'kind': 'logical-content-incorporated-historical-source-retained',
                    'basis': 'scientific-consolidation-review'}
        relations = [r for r in cross['relations'] if r.get('from') == 'fisher'
                     and r.get('kind') == relation['kind']]
        if (original['path'] != FISHER_AUDIT or original['sha256'] != HISTORICAL_PROSE[FISHER_AUDIT][1]
                or forms != [{'source': 'fisher', 'relationship': 'historical-source'}]
                or relations != [relation]
                or any('fisher' in j.get('source_keys', []) for j in cross['reader_journeys'])):
            raise ValueError('Fisher reader source is not explicitly historical-only')
        journeys = [j for j in cross['reader_journeys'] if j.get('id') == 'J06']
        if len(journeys) != 1 or journeys[0].get('source_keys') != [
                'tensor', 'coercive', 'consolidated-information-and-inquiry', 'sidecar']:
            raise ValueError('the Fisher journey must retain its exact current reading route')
    except (KeyError, TypeError, UnicodeError) as exc:
        raise ValueError('invalid current Fisher owner bindings') from exc


def _regular_current_bytes(root, path):
    target = pathlib.Path(root)
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('current reading dependency contains a symlink')
    entry = target.stat()
    if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
        raise ValueError('current reading dependency is not regular nonexecutable data')
    return target.read_bytes()


def typed_guide_source_bytes(root, path, *, allow_original=False):
    """Return one original guide after authenticating its exact link adaptation."""
    if path not in TYPED_GUIDES:
        raise ValueError('unqualified typed guide')
    blob, identity, size, replacements = TYPED_GUIDES[path]

    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required typed guide objects unavailable')
        return result.stdout

    expected = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if (git('cat-file', '-t', TYPED_PROSE_REVISION) != b'commit\n'
            or git('ls-tree', '-z', TYPED_PROSE_REVISION, '--', path) != expected):
        raise ValueError('typed guide original path, blob or mode differs')
    original = git('cat-file', 'blob', blob)
    actual_blob = hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest()
    if (len(original), digest(original), actual_blob) != (size, identity, blob):
        raise ValueError('typed guide original identity differs')
    adapted = original
    for key, count in replacements.items():
        source = TYPED_SOURCE_KEYS[key]
        old = ('../../source-store/' + source.split('/source-store/', 1)[1]).encode()
        new = ('https://github.com/theislampill/orthemology/blob/' + TYPED_PROSE_REVISION + '/' + source).encode()
        if original.count(old) != count:
            raise ValueError('typed guide original link count differs')
        adapted = adapted.replace(old, new)
    current = _regular_current_bytes(root, path)
    if current != adapted and not (allow_original and current == original):
        raise ValueError('typed guide is not its exact navigation adaptation')
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    indexed = git('ls-files', '--stage', '-z', '--', path)
    choices = {('100644 ' + oid + ' 0\t' + path + '\0').encode(): body
               for oid, body in ((blob, original), (adapted_blob, adapted))}
    if indexed not in choices:
        raise ValueError('typed guide index is absent, conflicted or unqualified')
    if git('cat-file', 'blob', indexed.split()[1].decode()) != choices[indexed]:
        raise ValueError('typed guide staged object differs or is unavailable')
    return original


def require_typed_context(root):
    """Bind prose history to current logic without retiring distinct evidence.

    This authenticates current owner records and bytes, not the mathematics,
    original review validity, formal replay, custody or permission to remove.
    """
    root = pathlib.Path(root)
    try:
        owners = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'))
        cross = json.loads(_regular_current_bytes(root,
            'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'))
        expected = [dict(path=path, repository_revision=TYPED_PROSE_REVISION,
            git_blob=TYPED_PROSE[path][0], role='historical-source',
            reading_source='consolidated-encodings-and-witnesses', basis='scientific-consolidation-review')
            for path in TYPED_PROSE]
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] in TYPED_PROSE]
        if len(bindings) != 4 or any(bindings.count(row) != 1 for row in expected):
            raise ValueError('all four exact typed prose dispositions are required')
        for key, path, role in (
            ('consolidated-encodings-and-witnesses', 'logic/encodings-and-witnesses.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current typed reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current typed scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current typed work has lost its review owner')
        result_ids = {
            't13-opaque': ['T13-OPAQUE-REPRESENTATION'],
            't13-residual': ['T13-RESIDUAL-HAS', 'T13-RESIDUAL-PLUS'],
            't13-bridge': ['T13-ATOM-APPLICATION-BRIDGE'],
            't14-separation': ['T14-CLOSED-PLUS-IDENTITY', 'T14-I-SKK-HAS', 'T14-I-SKK-PLUS'],
        }
        for key, path in TYPED_SOURCE_KEYS.items():
            source = cross['sources'][key]
            works = [w for w in cross['works'] if w.get('key') == key]
            if len(works) != 1:
                raise ValueError('typed original work identity is absent or duplicated')
            work = works[0]
            forms = [{'source': key, 'relationship': 'historical-source'}]
            source_keys, support = [key], []
            if key == 't14-separation':
                forms.append({'source': 't14-separation-lean', 'relationship': 'formal-component'})
                source_keys.append('t14-separation-lean')
                support = ['t14-written-review', 't14-review', 't14-suite']
            all_forms = [f for w in cross['works'] for f in w.get('reading_forms', [])
                         if f.get('source') == key]
            relation = {'from': key, 'to': 'consolidated-encodings-and-witnesses',
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            relations = [r for r in cross['relations'] if r.get('from') == key
                         and r.get('kind') == relation['kind']]
            if (source['path'] != path or source['sha256'] != TYPED_PROSE[path][1]
                    or work['source_keys'] != source_keys or work['reading_forms'] != forms
                    or work['supporting_source_keys'] != support or work['existing_result_ids'] != result_ids[key]
                    or all_forms != [forms[0]] or relations != [relation]
                    or any(key in j.get('source_keys', []) for j in cross['reader_journeys'])):
                raise ValueError('typed source, current reading or retained component relationship differs')
        retained = {
            't14-separation-lean': ('48c216af205451ec75f6d761f0dbee97a0ba279dfaa386cfd125676b96d6975c', 'IntensionalIdentityTheorems.lean'),
            't14-written-review': ('996107254670edb11d47dddc03ce0b6dd4fe045ae41b6d73b2079f3c827862f1', 'Orthemology_Fourteenth_Checkpoint_Verification_v1_20261005.json'),
            't14-review': ('e9c756ef20f5eb9b5188c3d55c9808fb0462280caa8a6048182ad7b3d55c9cbb', 'Orthemology_Fourteenth_Completion_Verification_v1_20261005.json'),
        }
        for key, (identity, name) in retained.items():
            source = cross['sources'][key]
            if (source['path'] != 'experiments/orthemology-v5-successors/source-store/' + identity + '/' + name
                    or source['sha256'] != identity):
                raise ValueError('distinct typed formal or review source identity differs')
        suite = cross['sources']['t14-suite']
        if (suite['path'] != 'experiments/orthemology-v5-successors/suites/t14-identity.json'
                or suite['sha256'] != 'c71afd9b7487ee8f14a6ae9d32a4eb90f427f6ad37c69ada645665aadf731386'):
            raise ValueError('distinct typed suite identity differs')
        for path in TYPED_GUIDES:
            typed_guide_source_bytes(root, path)
    except (KeyError, TypeError, UnicodeError) as error:
        raise ValueError('malformed typed current-owner contract') from error


def mediator_guide_source_bytes(root, *, allow_original=False):
    """Keep the original guide identity and admit exactly three pinned links.

    The guide must remain physically present. This is a finite navigation
    adaptation, never another prose absence or an unbounded source fallback.
    """
    root = pathlib.Path(root)
    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required guide Git objects unavailable')
        return result.stdout
    expected = ('100644 blob ' + MEDIATOR_GUIDE_BLOB + '\t' + MEDIATOR_GUIDE + '\0').encode()
    if git('cat-file', '-t', MEDIATOR_PROSE_REVISION) != b'commit\n' or git(
            'ls-tree', '-z', MEDIATOR_PROSE_REVISION, '--', MEDIATOR_GUIDE) != expected:
        raise ValueError('original guide revision/path/blob/mode differs')
    original = git('cat-file', 'blob', MEDIATOR_GUIDE_BLOB)
    if (len(original), digest(original)) != (MEDIATOR_GUIDE_BYTES, MEDIATOR_GUIDE_SHA256):
        raise ValueError('original guide identity differs')
    old = ('../../source-store/' + MEDIATOR_COORDINATION.split('/source-store/', 1)[1]).encode()
    new = ('https://github.com/theislampill/orthemology/blob/' + MEDIATOR_PROSE_REVISION +
           '/' + MEDIATOR_COORDINATION).encode()
    if original.count(old) != 3:
        raise ValueError('original guide does not contain its three bound links')
    adapted = original.replace(old, new)
    current = _regular_current_bytes(root, MEDIATOR_GUIDE)
    if current != adapted and not (allow_original and current == original):
        raise ValueError('guide is not the exact three-link navigation adaptation')
    adapted_blob = hashlib.sha1(b'blob ' + str(len(adapted)).encode() + b'\0' + adapted).hexdigest()
    indexed = git('ls-files', '--stage', '-z', '--', MEDIATOR_GUIDE)
    choices = {('100644 ' + blob + ' 0\t' + MEDIATOR_GUIDE + '\0').encode(): data
               for blob, data in ((MEDIATOR_GUIDE_BLOB, original), (adapted_blob, adapted))}
    if indexed not in choices:
        raise ValueError('guide index is absent, conflicted or has an unqualified edition/mode')
    indexed_blob = indexed.split()[1].decode()
    if git('cat-file', 'blob', indexed_blob) != choices[indexed]:
        raise ValueError('guide staged object is unavailable or differs')
    return original


def require_mediator_context(root):
    """Require the existing current scholarship, review and explicit source roles."""
    root = pathlib.Path(root)
    owner_path = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    cross_path = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    try:
        owners = json.loads(_regular_current_bytes(root, owner_path))
        cross = json.loads(_regular_current_bytes(root, cross_path))
        expected_bindings = [dict(path=path, repository_revision=MEDIATOR_PROSE_REVISION,
            git_blob=MEDIATOR_PROSE[path][0], role='historical-source',
            reading_source='consolidated-collective-inquiry', basis='scientific-consolidation-review')
            for path in MEDIATOR_PROSE]
        bindings = [r for r in owners['historical_source_bindings'] if r['path'] in MEDIATOR_PROSE]
        if len(bindings) != 2 or any(bindings.count(row) != 1 for row in expected_bindings):
            raise ValueError('both exact mediator source dispositions are required')
        for key, path, role in (
            ('consolidated-collective-inquiry', 'mathematics/collective-inquiry-and-strategic-coordination.md', 'work-source'),
            ('scientific-consolidation-review', 'docs/scientific-consolidation-review.md', 'review')):
            selected = [r for r in owners['source_additions'] if r['key'] == key]
            if len(selected) != 1:
                raise ValueError('missing or duplicate current mediator reading owner')
            admission, source = selected[0], cross['sources'][key]
            current = _regular_current_bytes(root, path)
            oid = hashlib.sha1(b'blob ' + str(len(current)).encode() + b'\0' + current).hexdigest()
            if (admission['path'] != path or source['path'] != path or admission['role'] != role
                    or admission['mode'] != '100644' or admission['git_oid'] != oid
                    or admission['bytes'] != len(current) or admission['sha256'] != digest(current)
                    or source['sha256'] != digest(current)):
                raise ValueError('current mediator scholarship or review edition differs')
            if role == 'work-source' and 'scientific-consolidation-review' not in admission['supporting_source_keys']:
                raise ValueError('current mediator work has lost its review owner')
        for key, path in (('coordination', MEDIATOR_COORDINATION),
                          ('t20-c03-6d8c1b108c74df46', MEDIATOR_APPROXIMATION)):
            source = cross['sources'][key]
            forms = [f for w in cross['works'] for f in w.get('reading_forms', []) if f.get('source') == key]
            relation = {'from': key, 'to': 'consolidated-collective-inquiry',
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            relations = [r for r in cross['relations'] if r.get('from') == key and r.get('kind') == relation['kind']]
            if (source['path'] != path or source['sha256'] != MEDIATOR_PROSE[path][1]
                    or forms != [{'source': key, 'relationship': 'historical-source'}]
                    or relations != [relation]
                    or any(key in j.get('source_keys', []) for j in cross['reader_journeys'])):
                raise ValueError('mediator source has lost its exact current reading relationship')
        mediator_guide_source_bytes(root)
    except (KeyError, TypeError, UnicodeError) as error:
        raise ValueError('malformed mediator current-owner contract') from error


def _require_self_contained_index_v2(body):
    """Accept the bounded SHA-1 v2 format without shared or opaque dependencies."""
    end = len(body) - 20
    if (end < 12 or body[:4] != b'DIRC'
            or struct.unpack('>I', body[4:8])[0] != 2
            or hashlib.sha1(body[:end]).digest() != body[end:]):
        raise ValueError('unsupported index format')
    count = struct.unpack('>I', body[8:12])[0]
    offset = 12
    if count > (end - offset) // 64:
        raise ValueError('invalid index entry count')
    for _ in range(count):
        start = offset
        if offset + 62 > end:
            raise ValueError('truncated index entry')
        flags = struct.unpack('>H', body[offset + 60:offset + 62])[0]
        name = offset + 62
        stop = body.find(b'\0', name, end)
        if (flags & 0x4000 or stop <= name
                or (flags & 0xFFF) != min(stop - name, 0xFFF)):
            raise ValueError('unsupported index entry')
        offset = start + ((stop + 1 - start + 7) // 8) * 8
        if offset > end or any(body[stop:offset]):
            raise ValueError('invalid index padding')
    while offset < end:
        if offset + 8 > end:
            raise ValueError('truncated index extension')
        signature = body[offset:offset + 4]
        size = struct.unpack('>I', body[offset + 4:offset + 8])[0]
        # No split-index link, sparse index, monitor/cache dependency, or
        # unknown extension is interpreted or silently rebuilt here.
        if signature not in {b'TREE', b'REUC', b'EOIE', b'IEOT'}:
            raise ValueError('unsupported index dependency')
        offset += 8 + size
        if offset > end:
            raise ValueError('truncated index extension payload')


def readonly_git_diff(root, command):
    """Run an existing diff against an exact private index, preserving its mtime.

    Git's normal stat-only filtering remains enabled. Any refresh is confined
    to the disposable copy. Unsupported inputs return an unavailable comparison;
    the active index is never rewritten or restored by this helper.
    """
    command = list(command)

    def unavailable():
        return subprocess.CompletedProcess(command, 128, b'',
                                           b'read-only index comparison unavailable')

    def query(*args):
        return subprocess.run(['git', '--no-replace-objects', *args],
                              cwd=root, capture_output=True, check=False)

    def state(info):
        return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
                info.st_mtime_ns, info.st_ctime_ns)

    if command[:2] != ['git', 'diff'] and command[:3] != ['git', '--no-replace-objects', 'diff']:
        return unavailable()
    try:
        split = query('config', '--type=bool', '--get', 'core.splitIndex')
        if not ((split.returncode == 1 and not split.stdout)
                or (split.returncode == 0 and split.stdout == b'false\n')):
            return unavailable()
        algorithm = query('rev-parse', '--show-object-format=storage')
        location = query('rev-parse', '--path-format=absolute', '--git-path', 'index')
        if algorithm.returncode or algorithm.stdout != b'sha1\n' or location.returncode:
            return unavailable()
        active = pathlib.Path(os.fsdecode(location.stdout.removesuffix(b'\n')))
        if not active.is_absolute():
            return unavailable()
        initial = active.lstat()
        if not stat.S_ISREG(initial.st_mode):
            return unavailable()
        with active.open('rb') as source:
            if state(os.fstat(source.fileno())) != state(initial):
                return unavailable()
            body = source.read()
            if len(body) != initial.st_size or state(active.lstat()) != state(initial):
                return unavailable()
            _require_self_contained_index_v2(body)
            with tempfile.TemporaryDirectory(prefix='readonly-git-index-') as directory:
                shadow = pathlib.Path(directory) / 'index'
                shadow.write_bytes(body)
                shadow.chmod(0o600)
                os.utime(shadow, ns=(initial.st_atime_ns, initial.st_mtime_ns))
                if shadow.read_bytes() != body or shadow.stat().st_mtime_ns != initial.st_mtime_ns:
                    return unavailable()
                env = dict(os.environ, GIT_INDEX_FILE=str(shadow))
                result = subprocess.run(command, cwd=root, env=env,
                                        capture_output=True, check=False)
            source.seek(0)
            if (state(active.lstat()) != state(initial)
                    or state(os.fstat(source.fileno())) != state(initial)
                    or source.read() != body):
                return unavailable()
            return result
    except (OSError, ValueError):
        return unavailable()


def digest(body):
    return hashlib.sha256(body).hexdigest()


def _continuation_git(root, *args):
    result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                            cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise ValueError('continuation copy Git identity unavailable')
    return result.stdout


def _continuation_object(root, kind, identity):
    body = _continuation_git(root, 'cat-file', kind, identity)
    header = kind.encode() + b' ' + str(len(body)).encode() + b'\0'
    if hashlib.sha1(header + body).hexdigest() != identity:
        raise ValueError('continuation copy Git object bytes differ')
    return body


def _continuation_copy_catalog(root):
    root = pathlib.Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('continuation copy requires an ordinary repository root')
    documents = {}
    for path, expected in CONTINUATION_COPY_METADATA.items():
        body = _regular_current_bytes(root, path)
        if (len(body), digest(body)) != expected:
            raise ValueError('continuation copy frozen metadata differs')
        documents[path] = json.loads(body)
    legacy = documents['docs/provenance/v5-research-continuations/SOURCE_MAP.json']['sources']
    successor = documents['docs/provenance/v5-successors/SOURCE_MAP.json']['sources']
    preservation = documents['docs/provenance/v5-successors/PRESERVATION.json']
    if preservation['base_commit'] != CONTINUATION_LEGACY_BASE:
        raise ValueError('continuation copy original version differs')
    preserved = {row['path']: row for row in preservation['files']}
    originals, retained = collections.defaultdict(list), collections.defaultdict(dict)
    for row in legacy:
        path = row.get('path') or ''
        if re.fullmatch(re.escape(CONTINUATION_COPY_ROOT) + r'[0-9a-f]{64}\.lean', path):
            originals[path].append(row)
    for row in successor:
        path = row.get('public_path') or ''
        if re.fullmatch(re.escape(CONTINUATION_RETAINED_ROOT) + r'[0-9a-f]{64}/[^/]+\.lean', path):
            identity = path[len(CONTINUATION_RETAINED_ROOT):].split('/')[0]
            if (row.get('projection') == 'EXACT' and row.get('derivation') is None
                    and row.get('original_sha256') == row.get('public_sha256') == identity
                    and row.get('original_bytes') == row.get('public_bytes')):
                retained[identity][path] = row
    result = {}
    for path, records in originals.items():
        identity = path[len(CONTINUATION_COPY_ROOT):-5]
        copies = retained.get(identity, {})
        if len(copies) != 1:
            continue
        canonical, copy = next(iter(copies.items()))
        size = copy['public_bytes']
        if any(row.get('projection') != 'EXACT' or row.get('derivation') is not None
               or row.get('original_sha256') != identity or row.get('sha256') != identity
               or row.get('original_bytes') != size or row.get('bytes') != size for row in records):
            raise ValueError('continuation copy source-ID identity differs')
        inventory = preserved.get(path, {})
        blob = inventory.get('git_blob_sha1')
        if ((inventory.get('bytes'), inventory.get('sha256')) != (size, identity)
                or not re.fullmatch('[0-9a-f]{40}', blob or '')):
            raise ValueError('continuation copy original inventory differs')
        result[path] = {'canonical': canonical, 'sha256': identity, 'bytes': size,
                        'blob': blob, 'sources': records, 'legacy_tree': preservation['base_tree']}
    excluded = CONTINUATION_COPY_ROOT + CONTINUATION_COPY_EXCLUDED + '.lean'
    if len(result) != CONTINUATION_COPY_COUNT + 1 or excluded not in result:
        raise ValueError('continuation copy finite class differs')
    del result[excluded]
    return result


def _continuation_bound_bytes(root, path, binding):
    root = pathlib.Path(root)
    canonical, blob = binding['canonical'], binding['blob']
    for revision, names in ((CONTINUATION_LEGACY_BASE, (path,)),
                            (CONTINUATION_COPY_BASE, (path, canonical))):
        commit = _continuation_object(root, 'commit', revision)
        if revision == CONTINUATION_LEGACY_BASE and not commit.startswith(
                ('tree ' + binding['legacy_tree'] + '\n').encode()):
            raise ValueError('continuation copy original tree differs')
        expected = {('100644 blob ' + blob + '\t' + name).encode() for name in names}
        actual = set(_continuation_git(root, 'ls-tree', '-z', revision, '--', *names).split(b'\0')) - {b''}
        if actual != expected:
            raise ValueError('continuation copy original or retained mode/blob differs')
    original = _continuation_object(root, 'blob', blob)
    body = _regular_current_bytes(root, canonical)
    if (len(body), digest(body)) != (binding['bytes'], binding['sha256']) or original != body:
        raise ValueError('continuation retained copy or original Git bytes differ')
    indexed = collections.defaultdict(list)
    for raw in _continuation_git(root, 'ls-files', '--stage', '-z', '--', path, canonical).split(b'\0'):
        if raw:
            metadata, name = raw.split(b'\t', 1)
            indexed[name.decode()].append(metadata.decode())
    expected = ['100644 ' + blob + ' 0']
    if indexed[path] not in ([], expected) or indexed[canonical] != expected:
        raise ValueError('continuation copy staged identity differs')
    target = root
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('continuation original path contains a symlink')
    if os.path.lexists(target) and _regular_current_bytes(root, path) != body:
        raise ValueError('present continuation original differs')
    return body


def continuation_copy_bytes(root, path, identity=None, size=None, source=None):
    """Authenticate an exact current copy; never recover arbitrary missing files."""
    if not re.fullmatch(re.escape(CONTINUATION_COPY_ROOT) + r'[0-9a-f]{64}\.lean', path):
        raise ValueError('unqualified continuation copy path')
    binding = _continuation_copy_catalog(root).get(path)
    if (binding is None or (identity is not None and identity != binding['sha256'])
            or (size is not None and size != binding['bytes'])
            or (source is not None and source not in binding['sources'])):
        raise ValueError('unqualified continuation copy or source-ID binding')
    return _continuation_bound_bytes(root, path, binding)


def continuation_duplicate_paths(root):
    """Return only actual absences authenticated by the finite current-copy rule."""
    result = set()
    for path, binding in _continuation_copy_catalog(root).items():
        if not os.path.lexists(pathlib.Path(root) / path):
            _continuation_bound_bytes(root, path, binding)
            result.add(path)
    return result


def source_bytes(root, row):
    path = pathlib.PurePosixPath(row['repository_path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('unsafe source path')
    if str(path) in HISTORICAL_PROSE:
        blob, identity, size = HISTORICAL_PROSE[str(path)]
        if (row['repository_path'] != str(path) or str(path) not in HISTORICAL_PROSE_PUBLIC_PATHS
                or row.get('disposition') != HISTORICAL_PROSE_DISPOSITIONS[str(path)]
                or row.get('source_sha256') != identity or row.get('source_bytes') != size):
            raise ValueError('historical public source owner differs')
        body = historical_source_bytes(root, str(path), row.get('repository_revision'), row.get('git_blob'))
    elif str(path).startswith(CONTINUATION_COPY_ROOT) and str(path).endswith('.lean'):
        if row.get('repository_revision') is not None:
            raise ValueError('current continuation copy cannot use historical reuse')
        if not os.path.lexists(root / path):
            if (row.get('disposition') != 'REUSE' or row.get('source_sha256') != row.get('public_sha256')
                    or row.get('source_bytes') != row.get('public_bytes')):
                raise ValueError('continuation public source identity differs')
            body = continuation_copy_bytes(root, str(path), row['public_sha256'], row['public_bytes'])
        else:
            body = _regular_current_bytes(root, str(path))
    elif row.get('repository_revision'):
        if row['repository_revision'] != HISTORICAL_PROSE_REVISION:
            raise ValueError('invalid pinned historical reuse')
        body = subprocess.check_output(['git', 'show', row['repository_revision'] + ':' + str(path)], cwd=root)
    else:
        target = root / path
        if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
            raise ValueError('unsafe source target')
        body = target.read_bytes()
    if digest(body) != row['public_sha256'] or len(body) != row['public_bytes']:
        raise ValueError('source identity differs: ' + row['source_sha256'])
    return body


def lean_imports(text):
    """Read import commands, masking nested Lean comments and strings."""
    out = list(text)
    i, depth, quoted = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                out[i:i+2] = '  '
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                out[i:i+2] = '  '
                i += 2
            else:
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif quoted:
            if text[i] == '\\' and i + 1 < len(text):
                out[i:i+2] = '  '
                i += 2
            else:
                quoted = text[i] != '"'
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif text.startswith('/-', i):
            depth = 1
            out[i:i+2] = '  '
            i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out[i:end] = ' ' * (end-i)
            i = end
        elif text[i] == '"':
            quoted = True
            out[i] = ' '
            i += 1
        else:
            i += 1
    imports = []
    for line_number, line in enumerate(''.join(out).splitlines(), 1):
        match = re.match(r'^\s*import\s+(.+)$', line)
        if match:
            for module in match[1].split():
                if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', module):
                    raise ValueError('unsupported Lean import syntax')
                imports.append((line_number, module))
    return imports


def closure(graph, root_hash):
    edges = collections.defaultdict(list)
    for edge in graph['edges']:
        edges[edge['parent_sha256']].append(edge['target_sha256'])
    seen, active, ordered = set(), set(), []

    def visit(identity):
        if identity in active:
            raise ValueError('cyclic custom import graph')
        if identity in seen:
            return
        active.add(identity)
        for child in edges[identity]:
            visit(child)
        active.remove(identity)
        seen.add(identity)
        ordered.append(identity)

    visit(root_hash)
    return ordered


def validate_graph(root, objects):
    errors = []
    graph_bytes = (root / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes()
    graph = json.loads(graph_bytes)
    if digest(graph_bytes) != CURRENT_GRAPH_SHA256:
        errors.append('qualified current source graph differs')
    nodes = {n['source_sha256']: n for n in graph['nodes']}
    if len(nodes) != len(graph['nodes']):
        errors.append('duplicate current source node')
    declarations = collections.defaultdict(list)
    for edge in graph['edges']:
        parent, target = edge['parent_sha256'], edge['target_sha256']
        declarations[parent].append((edge['line'], edge['module']))
        if target not in nodes or edge['module'] not in nodes[target]['modules']:
            errors.append('custom import module binding differs: ' + parent)
        if objects.get(target, {}).get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + target)
    for edge in graph['official_import_edges']:
        declarations[edge['parent_sha256']].append((edge['line'], edge['module']))
        if edge['module'].split('.')[0] not in ('Init', 'Lean', 'Std', 'Mathlib'):
            errors.append('unqualified official import')
    for identity in nodes:
        row = objects.get(identity, {})
        if row.get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + identity)
            continue
        try:
            body = source_bytes(root, row)
            if digest(body) != identity:
                errors.append('current formal source must retain exact original bytes: ' + identity)
            actual = lean_imports(body.decode('utf-8'))
            if collections.Counter(actual) != collections.Counter(declarations[identity]):
                errors.append('actual import declarations differ: ' + identity)
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
            errors.append('missing or changed current source: ' + identity)
    if set(declarations) - set(nodes):
        errors.append('import parent absent from source graph')
    reached = set()
    for suite in graph['suites']:
        ordered = closure(graph, suite['root_sha256'])
        reached.update(ordered)
        mapping = suite['modules']
        if any(not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', module) for module in mapping):
            errors.append('unsafe suite module name: ' + suite['id'])
        if set(mapping.values()) != set(ordered) or len(mapping) != len(ordered):
            errors.append('isolated suite coverage differs: ' + suite['id'])
        if any(module not in nodes.get(identity, {}).get('modules', []) for module, identity in mapping.items()):
            errors.append('isolated suite module binding differs: ' + suite['id'])
        for edge in graph['edges']:
            if edge['parent_sha256'] in ordered and mapping.get(edge['module']) != edge['target_sha256']:
                errors.append('isolated suite imports a different variant: ' + suite['id'])
    if reached != set(nodes):
        errors.append('current source graph contains missing or unrooted nodes')
    for edge in graph['ordinary_proof_dependencies']:
        for key in ('parent_sha256', 'target_sha256'):
            if objects.get(edge[key], {}).get('disposition') not in PUBLIC:
                errors.append('ordinary proof support unavailable: ' + edge[key])
        try:
            body = source_bytes(root, objects[edge['parent_sha256']]).decode('utf-8')
            if edge['evidence_text'] not in body:
                errors.append('ordinary proof evidence binding differs: ' + edge['parent_sha256'])
        except (OSError, ValueError, KeyError):
            errors.append('ordinary proof parent unavailable: ' + edge['parent_sha256'])
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('find').add_argument('query')
    sub.add_parser('resolve').add_argument('source_sha256')
    export = sub.add_parser('export-suite')
    export.add_argument('suite')
    export.add_argument('destination', type=pathlib.Path)
    args = parser.parse_args()
    document = json.loads((ROOT / PREFIX / 'PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
    objects = {r['source_sha256']: r for r in document['objects']}
    if args.command == 'find':
        query = args.query.casefold()
        for row in objects.values():
            if query in ' '.join([row['source_sha256'], row.get('repository_path', ''), *row.get('source_names', [])]).casefold():
                print(json.dumps(row, ensure_ascii=False))
    elif args.command == 'resolve':
        row = objects[args.source_sha256.removeprefix('source-sha256:')]
        if row['disposition'] in PUBLIC:
            source_bytes(ROOT, row)
        print(json.dumps(row, ensure_ascii=False, indent=2))
    else:
        errors = validate_graph(ROOT, objects)
        if errors:
            raise SystemExit('\n'.join(errors))
        graph = json.loads((ROOT / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes())
        suite = next(s for s in graph['suites'] if s['id'] == args.suite)
        destination = args.destination.resolve()
        if destination.is_relative_to(ROOT):
            raise SystemExit('Reconstruct outside the repository in a fresh directory')
        # Verify all bytes before creating the fresh destination.
        modules = {identity: module for module, identity in suite['modules'].items()}
        plan = [(modules[h], source_bytes(ROOT, objects[h])) for h in closure(graph, suite['root_sha256'])]
        destination.mkdir(parents=True, exist_ok=False)
        for module, body in plan:
            path = destination / (module.replace('.', '/') + '.lean')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        (destination / 'REPLAY_ORDER.txt').write_text('\n'.join(m.replace('.', '/') for m, _ in plan) + '\n')
        (destination / 'RECONSTRUCTION.json').write_text(json.dumps(suite, indent=2) + '\n')
        print(json.dumps({'suite': suite['id'], 'verified_sources': len(plan), 'executed': False}))


if __name__ == '__main__':
    main()
