#!/usr/bin/env python3
"""Offline, source-bound successor replay with fresh isolated custom outputs.

Exit 0 means success at the reported scope; 1 means failure or an explicitly
resource-inconclusive run; 2 means a missing prerequisite. No network or shell.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
import re
import runpy
import shutil
import signal
import stat
import subprocess
import sys
import zipfile


LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
CACHE_POLICY = 'OFFICIAL_PINNED_CACHES_ONLY_FRESH_CUSTOM_OBJECTS'
REPLAY_KEYS = set('schema scope files modules module_order positive_roots audit_roots negative_roots runtime_roots official_imports target_names package_manifest_source_id packages tools external_inputs fixtures drivers stages build_roots'.split())
STAGE_KEYS = set('id kind driver_id argv cwd depends_on timeout_seconds output_paths control_ids expected_exit_codes expected_diagnostics'.split())
EVIDENCE_KEYS = set('schema descriptor_sha256 closure_sha256 runner_sha256 source_hashes_before source_hashes_after import_fingerprints tool_fingerprints dependency_checks driver_hashes stage_results target_audits control_diagnostics output_hashes cache_policy'.split())
ROLES = {'PROOF', 'AUDIT', 'NEGATIVE', 'RUNTIME', 'DRIVER', 'CONFIG', 'DATA', 'LOCK', 'REVIEW'}
KINDS = {'SOURCE_CHECK', 'LEAN_COMPILE', 'LEAN_AUDIT', 'POSITIVE_CONTROL', 'NEGATIVE_CONTROL', 'NATIVE_BUILD', 'NATIVE_RUN', 'REFERENCE_TESTS', 'DRIVER'}
RESERVED = {'_prerequisites', '_target_audit'}
LANGUAGE_RECIPES = {
    't14-occurrence-v1': {'sha256': 'a61800a28a1a7be9415072a949407dfe91085620ddf10d01df0c77219b7a9615',
        'lock': '54638026fd05b40e780d1ed5d51bbd286398926e074b487f746237b5dd816be0',
        'lock_name': 'source-lock.json', 'files': 70, 'checks': 82},
    't14-sense-v1': {'sha256': '5727a43f5207ec7e93aed9b9d6c4a26f83ce3af61bc4041122621bc101d2216d',
        'lock': '72293db56804c56c017582d7d22f8dc21a985ab37ff258ac789160c2dfeb7c63',
        'lock_name': 'sense-source-lock.json', 'files': 9, 'checks': 9},
}
SOURCE_RECIPES = {
    't10-uniform-completion-v1': 'a67f3ae196aa45d895f881b02787ec04db4a97c344b73a7aa7e126a0d6ded5c7',
    't10-nonuniform-completion-v1': '10d15cd1df71ca909c3598e98d090df25cdcd745861d8bbc9cea9ea9d513be13',
}
NORMAL_SOURCE_RECIPES = {
    't11-substitution-source-check-v1': '0998ba1ff76bd6620707f38035612431fa94f9e16e1a5105b5f527d12eef21ab',
    't11-normalization-source-check-v1': '59dfb863bd8f583993d9497f961db96d009343d805abb81fd4f67e5516600a23',
    't14-identity-verify_sources-v1': '5830996846ad5dfb951ad742c5904bb3d2d80e1940cf6c9c4d04789189ee3bb6',
}
# Full-suite promotion requires review of its complete original stage contract.
# Generic serial compilation is supported at COMPONENTS scope. Values here are
# code-reviewed suite and source-byte bindings, never producer approvals.
APPROVED_DECLARED_SUITES = {
    't15-identity': 'd71ae53e2219c144dbd4b22d83d34a96e0ba61e7f13036bd364025619e5539f3',
    't11-dependent-all': 'b87aca15fb03afe740abc50aa8dfc00d5a9dbf59de7f0b61591123163f47ec8b',
    't11-normalization': '4653066edcd7df7c05addf7c81aa48ee9680c36f58a216ccd5c55d04d5763da6',
    't11-nucleus': 'f8d2057ed34df1260efafe16a2227400a9f9f5b2d9cc13b3d86105bf7d269160',
    't11-substitution': '39e05def1e6370039143ff47862774fc6dd1c4f9865f9b39827cdff43186f090',
    't14-identity': 'c065f772862ca55a9d7ac6ceb29c11439aa1574bf8dd8e37918a65dc77e9abdf',
    'd06-core-runtime': '2c0c433ba860bc33862a87dff2e4c22f3ec1d584b580a0605a1ffc8163844f8b',
    'D04-T07-ATTRIBUTION-ORIGINAL': '7888e370d7f65783731bd93783041e9c35648db96d27e6e9d059894003731d15',
    'D04-T07-HISTORY-ORIGINAL': 'a0e55482d8bf7f6d9b5b77ee37d99ce54a5b27945cd7d816f9d00cb6d61711df',
}
EMPIRICAL_RECIPES = {
    't15-empirical-integrity-v1': '9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e',
    't15-empirical-tests-v1': 'afb1ba14ecbbf193f07ac81f985be30535abf9771387813e9dbd0bbbfc72fb50',
    't15-empirical-reanalyse-v1': '20110e73fd822e21651064578946cdf910edc493c973953b2c7d1bb74481dd94',
    't15-empirical-validate-v1': '7d9a4c8d071e2591c8d4568c88c277ab61834e52df21500a1367efb2ac7e060a',
}
T10_CHECKER = 'tranche10/research/occurrence-continuation/release-candidate-v1/checker'
T10_REVIEW = 'tranche10/reviews/occurrence-checker'
T10_FINITE_RECIPES = {
    't10-unit-v1': (T10_CHECKER + '/tests/test_contract.py', 'af8ae17bd3881ab703fc773bf91bffad9859a4fa8f9cb3559d39ed43b4696bf8'),
    't10-exhaustive-v1': (T10_CHECKER + '/exhaustive_validation.py', '7614ed0a2d9eca6c2e07c74ee0e02c902cff4956b07347ee9b1b47e70edd8ee2'),
    't10-source-release-v1': (T10_CHECKER + '/source_and_release_validation.py', 'd286e1099431a64390a14c9533d96cdd7aebc673f68ea74953c9c4852e5e24db'),
    't10-semantic-v1': (T10_CHECKER + '/semantic_mutations.py', '090c48a908c2780f5eccce07c7b211e3970f0f24ea1188d3528a5195fafe8130'),
    't10-independent-selftest-v1': (T10_REVIEW + '/independent_models.py', 'cf9ac967668e35fc47c89214efbd9f84aa97a820ec255ffff4d48b41b1af1d3a'),
    't10-independent-review-v1': (T10_REVIEW + '/run_independent_review.py', 'e1303f10bbe5da403553c2be7f2b7ff468f0567b501f63d854cfb3f908cabcf2'),
    't10-independent-mutations-v1': (T10_REVIEW + '/run_independent_mutations.py', 'b94b8df9b31c8b635743440afc3525fb6abff282336ef1ba9e2dd9a316f6fee4'),
    't10-two-card-v1': ('tranche10/reviews/bounded-release-application/check_observations.py', 'ba4f0fa9ed04750b629b5a504c976de589c3899c9c753742dd34cbb0cdcd644c'),
}
T10_FILES = dict(T10_FINITE_RECIPES.values()) | {
    T10_CHECKER + '/context_effects.py': '0f65f172926e61ff7280ec2e13fd36b4ff287ea530ebbfa00c9dce831f3355fa',
    T10_CHECKER + '/read_cover.py': '808a9297d27b903722b4fc04ad9a526d3cfc3e371b14e5047e1d33d1c6e3e79f',
    T10_CHECKER + '/fixtures/source_roles.json': '8d821ec871977ba5c22ff00d8cc27841c32aab682aae0c0d2cf99cb6f695169c',
    T10_CHECKER + '/CASE_TRACEABILITY.json': 'd43b730b8ada0ceba61bda31cae36e662547c7a883ccf643901d5c061e824a6b',
    T10_CHECKER + '/README.md': '08d2b29597f4ee32240d7c54ed0fa70b1aa6d1e35d6d16253fd3fde078ddb04d',
}
T10_OUTPUTS = {
    't10-exhaustive-v1': ['project/' + T10_CHECKER + '/logs/exhaustive_results.json'],
    't10-source-release-v1': ['project/' + T10_CHECKER + '/logs/source_release_results.json'],
    't10-semantic-v1': ['project/' + T10_CHECKER + '/logs/semantic_mutations.json'],
    't10-independent-mutations-v1': ['project/' + T10_REVIEW + '/INDEPENDENT_MUTATION_RESULTS.json', 'mutation-copies'],
}
T10_CHILD_DIAGNOSTICS = {
    'current_only': ('direct stack',),
    'compose_depth_abs_shift': ('split', 'left association', 'right association'),
    'drop_second_constraints': ('split', 'left association', 'right association'),
    'snapshot_blind_equality': ('wrong snapshot accepted',),
    'nonconvex_envelope': ('nonconvex accepted',),
    'retired_service_available': ('retired service treated available',),
    'locality_ignores_response': ('star accepted leak',),
    'adequacy_ignores_fibres': ('false adequate-coverage certification',),
    'replace_adaptive_with_cover': ('missed cheaper decision',),
}
CORE_RECIPE = 't08-semantic-core-runtime-v1'
CORE_ARCHIVE_SHA = 'bca5b48fbcbb65f032fb5b92f1cb9dec1e3bc3e340f424d0a2c6c2df54530da2'
CORE_FILES = {
    'replay.py': 'abef8d7017860e73b131c499357654323f0cf5f43ff0154439427ebb8a4e5dcc',
    'verify_dependency_identity.py': '7deeab885edfa67829f733766a1d8e9f08439157dec5bd54f05681371ed0e10e',
    'SOURCE_MANIFEST.json': '8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c',
    'DEPENDENCY_PINS.json': '9eaffaa788991447cf64938183de0e982b467d333dd9a369f11c0c99a0be595c',
    'MATHLIB_ARCHIVE_INVENTORY.json': '1c4d1fa63acf416d7b965ed519d16faea965022cb8eb8d74725d59d801db16f0',
}
ATTR_RECIPE = 't07-attribution-original-v1'
ATTR_CONTRACT = {
    'driver_sha256': 'fad631436eecb9b71bdf0360f78503bb8c863a5ebd23b0999e17ca059781b113',
    'driver_bytes': 9807, 'archive_sha256': '8c4c7e34347dc66e2cd05d8b106f0c7401fa28fde53675aec336ef8808cf019a',
    'archive_bytes': 554694, 'root': 'unknown-root-attribution-kernel-accepted-v1', 'driver_path': 'replay.py',
}
ATTR_DIAGNOSTICS = {'count_labels_as_roots': 'error: unsolved goals',
                    'drop_positive_class_size': 'error: omega could not prove the goal',
                    'drop_positive_fault_budget': 'error: omega could not prove the goal'}
ATTR_PATHS = [(name, 'sources/central-v1/legacy/' + name + '.lean', True) for name in ['DynamicInterlock', 'CoveringCore', 'UnknownRootAttribution']]
ATTR_PATHS += [(name, 'sources/central-v1/' + name + '.lean', True) for name in ['RootImage', 'Availability', 'FixedFamilies', 'Correspondence', 'ImageMinima', 'MapTransport']]
ATTR_PATHS += [(name, 'sources/central-v1/tests/' + name + '.lean', False) for name in ['TargetA', 'TargetB', 'TargetC', 'Regression']]
ATTR_PATHS += [('RootCosts', 'sources/controls-v1/RootCosts.lean', True), ('FamilyDeletionControls', 'sources/controls-v1/tests/FamilyDeletionControls.lean', False)]
ATTR_PATHS += [(name, 'review/' + name + '.lean', False) for name in ['IndependentChecks', 'DeletionControls', 'AxiomAudit']]
ATTR_PATHS += [(name, 'sources/controls-v1/mutation-controls/' + name + '.lean', False) for name in ATTR_DIAGNOSTICS]
ATTR_MANIFESTS = {'PUBLIC_MANIFEST.json': 'c68835c56e26dfb2749b8bf3ec895aaa36abc596e7cbecad4ba58cd035d347f2',
    'DEPENDENCIES.json': '4c6d10a5d818dda9b5f68b8c8bdd6d9ec8a053e584e6aaa70e8c014cb49fbb14',
    'dependencies/SOURCE_MANIFEST.json': 'b0f8592a23304950e2f4294404df242228ea78b5ebd60622d227a2623ba6d618',
    'sources/central-v1/MANIFEST.json': '2830c05f25dcda6f05617e6da58bac50eb3ea86cc9671f5b8301417bf2a1d295',
    'sources/controls-v1/MANIFEST.json': 'f29de5f526216178d1925281eef35a8f8558dc15810b6f7e40428324963f93e4',
    'review/REVIEW_RECEIPT.json': '59b6578ab2d25b7a5f00ba8cefc1777c23c4b59de95f9ba631c1109c80468de3',
    'ORIGINAL_TO_PUBLIC.json': '91bba08917dba9215cff4208e65b3ba4484b84e2f92fcfe8fb5938aa1689adaa'}
HISTORY_RECIPE = 't07-history-original-v1'
HISTORY_LEGACY_FAILED_RUNNER = '3342453bdd846fd1b28956736899137ca43b7fe8ad9af114bff91eb495ddcfd6'
HISTORY_CONTRACT = {
    'driver_sha256': 'c664ea7c1398e81359bd5684b25104caaea1991598e16d3476ce555e405ee06a',
    'driver_bytes': 10192, 'archive_sha256': 'ac825ff194e83f8ddd50da3a48e0739d320517374e66f19b129c386188c09aa0',
    'archive_bytes': 654716, 'root': '', 'driver_path': 'replay.py',
}
HISTORY_KERNEL = 'tranche7-restart/formal/interlock-history-kernel/'
HISTORY_DYNAMIC = 'tranche7-restart/delivery/unknown-root-attribution-accepted-v1/base-v2/dynamic_interlock.py'
HISTORY_ORIGIN_SHA = 'df8f13aa634a7c00256d7dc253bcc997bea13ab53000af9b00130a24698546fb'
HISTORY_FILES = {
    'PUBLIC_MANIFEST.json': 'a07397914c4703fbb1f89b939abaf9e592b720f0a5c77908e900c8b71e87f319',
    'ORIGINAL_TO_PUBLIC.json': 'f6d265bcfaf79357fb9869c106cde85047cc3337072932c85101094c1c1b916f',
    'MATHLIB_SOURCE_PIN.json': 'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431',
    HISTORY_KERNEL + 'SOURCE_BINDING.json': '91bd8ca31da36f6d575431cedd16312727728ebf3adb2eaab4fd9d2c2ee5f6b1',
    HISTORY_KERNEL + 'REVIEW_SNAPSHOT_V2.json': 'e253a2b1a537826094db7ede00768b561360ce25e3a6907354592a320a2de278',
    HISTORY_KERNEL + 'independent-review-v2/RECEIPT.json': 'e1432fdadf2bcaad8ce4c9cbfe62b3ef0d6905ebc94afbfb6e11ec018a4c4b36',
    HISTORY_KERNEL + 'check_controls.py': '90162a106383eedfb2f7be6a31236c42a81c78d563500d21090b1fb4e2fd3745',
    HISTORY_KERNEL + 'source_replay.py': 'cada8edbe323dcb7d3ca352103afc0e3e8a30622b0ed08687643672e4e13c6ba',
    HISTORY_DYNAMIC: 'd67b95645512d78c51cab469cc71fc4fc5fd622a7c379481f1ee178e1031052a',
}
HISTORY_PATHS = [(n, HISTORY_KERNEL + n + '.lean', True) for n in ['HistoryModel', 'HistoryInvariant', 'HistorySafety', 'HistoryTrace', 'NegativeControls']]
HISTORY_PATHS += [(n, HISTORY_KERNEL + 'tests/' + n + '.lean', False) for n in ['Targets', 'MultiEpoch']]
HISTORY_PATHS += [(n, HISTORY_KERNEL + 'independent-review-v2/' + n + '.lean', False) for n in ['ReviewChallenges', 'ReservationDomain']]
HISTORY_CLAIMS = {
    'revocation_omission_is_safe': '¬ BrokenLands revoked NoRevocation command 11',
    'target_only_checks_preserve_permission': '¬ BrokenLands delivered TargetOnly command 11',
    'cancellation_guard_is_redundant': '¬ BrokenLands cancelled NoCancellation command 11',
    'B_replies_are_enough': '¬ Lands cfg falselyClosed command 11',
    'mediation_is_redundant': '(bypass revoked).damaged = false',
    'approved_label_binds_substituted_bytes': '(land cfg prepared substituted 11).damaged = false',
    'old_action_still_authorized': 'Authorized command (cfg.source revoked.epoch)',
}
HISTORY_DIAGNOSTICS = ["tactic 'decide' proved that the proposition", 'is false']
HISTORY_CASES = [
    {'case': 'stale_local_after_revocation', 'baseline': 'NO_EFFECT', 'cached_votes': 'UNSAFE'},
    {'case': 'permission_only_epoch', 'baseline': 'NO_EFFECT', 'target_only': 'UNSAFE'},
    {'case': 'durable_cancellation', 'late': 'NO_EFFECT', 'reprepare': False, 'fresh_nonce': 'APPLIED'},
    {'case': 'too_small_cancel_threshold', 'late': 'APPLIED'}, {'case': 'same_budget_bypass', 'unsafe': True},
    {'case': 'same_command_binding', 'baseline': 'NO_EFFECT', 'substitution': 'UNSAFE'},
    {'case': 'two_epochs_reordered_delivery', 'final_epoch': 2, 'landing': 'APPLIED'},
]
HISTORY_CEILING = 'Original dynamic V2 conditional finite-history safety, durable cancellation, and stable-epoch goal preservation only.'
HISTORY_TERMINAL = ['PASS: 5 modules, 2 fixtures, 7 false-claim controls, 7 original-source scenarios, and both V2 reviewer check files.',
                    'All projected scientific bytes unchanged. No archive executable permissions used.']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def keys(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected), 'Unknown or missing fields')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def digest(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'Invalid SHA-256')
    return value


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode())


def declared_suite_fingerprint(suite, sources):
    return canonical({'suite': suite, 'sources': {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']}})


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite JSON number')
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', value), 'Invalid identifier')
    return value


def lean_name(value):
    require(isinstance(value, str) and value and all(part.rstrip("'").isidentifier() for part in value.split('.')), 'Invalid Lean name')
    return value


def string_list(value):
    require(isinstance(value, list) and all(isinstance(item, str) and item for item in value), 'Invalid string list')
    require(len(value) == len(set(value)), 'Duplicate list identity')
    return value


def indexed(value, field='id'):
    require(isinstance(value, list), 'Expected record array')
    result = {}
    for row in value:
        require(isinstance(row, dict) and field in row, 'Malformed record')
        name = identifier(row[field])
        require(name not in result, 'Duplicate record identity')
        result[name] = row
    return result


def relative(value, *, dot=False):
    if dot and value == '.':
        return value
    require(isinstance(value, str) and value and '\\' not in value and ':' not in value and '\x00' not in value, 'Unsafe relative path')
    parts = value.split('/')
    require(not value.startswith('/') and all(p not in {'', '.', '..', '.git'} for p in parts), 'Unsafe relative path')
    require(all(not p.endswith((' ', '.')) for p in parts), 'Ambiguous relative path')
    require(all(not re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', p) for p in parts), 'Reserved path')
    return value


def no_symlinks(path):
    path = Path(path).absolute()
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'Symlink path is not admitted')
    return path


def path_in(root, name, *, dot=False):
    relative(name, dot=dot)
    root = no_symlinks(root).resolve()
    path = no_symlinks(root / name)
    require(path.resolve().is_relative_to(root), 'Path escapes its declared root')
    return path


def tool_argument(definition, executable):
    kind = definition.get('path_kind', 'EXECUTABLE')
    require(kind in {'EXECUTABLE', 'BIN_DIRECTORY', 'DISTRIBUTION_ROOT'}, 'Unknown tool path meaning')
    path = Path(executable)
    return path if kind == 'EXECUTABLE' else path.parent if kind == 'BIN_DIRECTORY' else path.parent.parent


def extract_source_zip(source, destination):
    """Extract an already hash-verified input into a new source-only namespace."""
    destination = no_symlinks(destination); require(not destination.exists(), 'Archive projection must be absent')
    rows = []; seen = set(); total = 0
    with zipfile.ZipFile(no_symlinks(source)) as archive:
        for item in archive.infolist():
            name = relative(item.filename.rstrip('/') if item.is_dir() else item.filename)
            require(name.casefold() not in seen, 'Archive namespace collision'); seen.add(name.casefold())
            mode = item.external_attr >> 16
            require(stat.S_IFMT(mode) in {0, stat.S_IFDIR if item.is_dir() else stat.S_IFREG}, 'Nonregular archive member')
            require(Path(name).suffix.lower() not in {'.olean', '.ilean', '.o', '.so', '.dll', '.exe', '.a', '.pyc', '.pyo', '.pyd'}, 'Archive contains precompiled custom artifacts')
            if item.is_dir(): continue
            total += item.file_size
            require(total <= 256 * 1024 * 1024 and len(rows) < 10000, 'Archive exceeds reviewed source projection budget')
            rows.append((name, archive.read(item)))
    destination.mkdir(parents=True)
    for name, data in rows:
        path = path_in(destination, name); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    return {name: sha(data) for name, data in rows}


def public_bytes(root, source):
    expected = digest(source['public_sha256'])
    name = relative(source['public_path'])
    require(name.startswith('experiments/orthemology-v5-successors/source-store/' + expected + '/'), 'Source is not content-addressed')
    require(type(source['public_bytes']) is int and source['public_bytes'] >= 0, 'Invalid source length')
    path = path_in(root, name)
    require(path.is_file(), 'Missing projected source')
    data = path.read_bytes()
    require(len(data) == source['public_bytes'] and sha(data) == expected, 'Source bytes/hash changed')
    return data


def strip_lean(text):
    """Preserve newlines while removing nested comments and string contents."""
    out = []; index = 0; depth = 0; quoted = False
    while index < len(text):
        if depth:
            if text.startswith('/-', index): depth += 1; index += 2
            elif text.startswith('-/', index): depth -= 1; index += 2
            else:
                out.append('\n' if text[index] == '\n' else ' '); index += 1
        elif quoted:
            if text[index] == '\\': out.extend('  '); index += 2
            elif text[index] == '"': quoted = False; out.append(' '); index += 1
            else: out.append('\n' if text[index] == '\n' else ' '); index += 1
        elif text.startswith('/-', index): depth = 1; out.extend('  '); index += 2
        elif text.startswith('--', index):
            end = text.find('\n', index); end = len(text) if end < 0 else end
            out.extend(' ' * (end - index)); index = end
        elif text[index] == '"': quoted = True; out.append(' '); index += 1
        else: out.append(text[index]); index += 1
    require(depth == 0 and not quoted, 'Unclosed Lean comment/string')
    return ''.join(out)


def imports(text):
    body = strip_lean(text)
    result = [] if re.search(r'(?m)^\s*prelude\s*$', body) else ['Init']
    for line in body.splitlines():
        if re.match(r'^\s*(?:public\s+)?import\b', line):
            found = re.fullmatch(r'\s*(?:public\s+)?import\s+([^\r\n]+?)\s*', line)
            require(found is not None, 'Unsupported import form')
            for name in found.group(1).split():
                lean_name(name)
                if name not in result: result.append(name)
    return result


def _manifest_pins(data):
    result = {}
    def visit(value, label=None):
        if isinstance(value, dict):
            name = value.get('name', label)
            rev = value.get('rev', value.get('revision', value.get('commit')))
            if isinstance(name, str) and isinstance(rev, str): result[name] = rev
            for key, child in value.items():
                if key == 'dependency_revisions' and isinstance(child, dict): result.update(child)
                visit(child, key)
        elif isinstance(value, list):
            for child in value: visit(child)
    try: visit(json.loads(data.decode('utf-8')))
    except (UnicodeError, ValueError):
        for line in data.decode('utf-8').splitlines():
            found = re.fullmatch(r'([A-Za-z0-9_.-]+)==([^\s;]+)', line.strip())
            if found: result[found.group(1)] = found.group(2)
    return result


def _json_pointer(value, pointer):
    if pointer == 'files': return value['files']
    require(isinstance(pointer, str) and pointer.startswith('/'), 'Expected manifest object pointer')
    for key in pointer[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        require(isinstance(value, dict) and key in value, 'Missing manifest object')
        value = value[key]
    return value


# Exact Fifteenth formal source, control, audit and export contracts.
T15_FORMAL_APPROVAL='d71ae53e2219c144dbd4b22d83d34a96e0ba61e7f13036bd364025619e5539f3'
T15_PYTHON_SHA='e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f'
T15_SOURCE_RECIPES={
    't15-identity-verify_sources-v1':('verification/verify_sources.py','112baf13e9cee7a5bcbaf96ef4034b6a2ac82f46f29b7f430777abaef3a5828d','SOURCE_CHECK'),
    't15-identity-test_source_checks-v1':('verification/test_source_checks.py','ae6199af29a58180ef19f56ffa08adad84793adef1baa211ea3e46a2b374d10c','DRIVER'),
}
T15_PYTHON_INPUTS={
    'verification/verify_sources.py':'112baf13e9cee7a5bcbaf96ef4034b6a2ac82f46f29b7f430777abaef3a5828d',
    'verification/test_source_checks.py':'ae6199af29a58180ef19f56ffa08adad84793adef1baa211ea3e46a2b374d10c',
    'verification/check_inherited_negative_controls.py':'3b1401e00271b8ac00df4993f3f81ac409ed03341ad4efbeb82d6a2334cc3521',
    'verification/check_new_negative_controls.py':'ff989b2cdc32b4bf7a61d56de4256c9f92e44412a9195c9f6a9d8c40afa7f36e',
    'verification/check_complexity_negative_controls.py':'58e8663e8e625fb8648f3859373d8fa690c5377c42d1dd19afdb9c223ad25e00',
    'verification/check_boolean_negative_controls.py':'094ed316e0a75c9cbbcd4a409670c275e43266df0fccbb4c291e12f55c6f608e',
    'verification/check_restricted_negative_controls.py':'03e8621dd94ce6949e90bebbbfbc1234782b6346d1862dd9cffeff8e2f1bd6cd',
    'verification/check_polynomial_test_controls.py':'1581e22b5b9041e1ad23bd6d810054dcb4489adaeadd84877da9ba8fe8e32bbc',
    'verification/reuse_dependencies.py':'20999a8810e2835e66c48602340447dfc6fc3c55b7055f49ba54ea1fd310191e',
    'verification/verify_dependencies.py':'a7bd1dc419b6dd2b514df0d6d0ef43fa3ed855960b22d016079f83319acc4da6',
}
T15_LOCK_INPUTS={
    'verification/source-lock.json':'bd800ff0214d7a382feb5da185d706766185fa309794ab52b2ad9e26444f613c',
    'verification/preserved-module-lock.json':'7dc06e97812b481caac84ca86cc685c2fb255fdc119f650b83cc6851dc085e61',
    'MODULES.json':'5ca88d5793fb2283badb16c8d722b777e0e9eb49198043b9335a198d572060c7',
    'verification/historical/raw-v2-receipt.json':'24db3eb238d712fa242cb5c71a5c074d70a4a52434d34b41ada2f3d731327082',
    'verification/historical/unified-v3-receipt.json':'53cd30a370c0f94db9fc211d2005637af204cc5197e88f30c7edcbfed6a52a27',
    'verification/historical/unified-v4-receipt.json':'3ab3b08b87aef587b2b6dd3964f6a884fb90c3b547511157b73275ebe4f7d637',
    'verification/run_checks.sh':'f9e84ab28e27c5789dc0464d6c05ee91c3b03e3ce8c0bf4d02df970c65f7575b',
}
T15_EXPORT_SOURCE='verification/ExportDeclarationInventory.lean'
T15_EXPORT_SHA='d8cc868cfb48b5db265771fcccf9ff4b0fd902d35ac50be24800133d01dbe048'
T15_EXPORT_OUTPUT='project/.verification-results/declaration-inventory.json'
T15_AXES={'propext','Quot.sound','Classical.choice'}

def _t15_require(value,message):
    if not value:raise ValueError(message)

def _t15_data(plan,path):
    _t15_require(path in plan['file_paths'],'T15 source input is absent: '+path)
    sid=plan['file_paths'][path]['source_id']
    _t15_require(sid in plan['contents'],'T15 source bytes are absent')
    return plan['contents'][sid]

def _t15_path(value):
    _t15_require(isinstance(value,str)and value and '\\'not in value and '\x00'not in value,'Invalid T15 manifest path')
    p=PurePosixPath(value)
    _t15_require(not p.is_absolute()and not any(x in {'','.', '..'}for x in value.split('/'))and ':'not in value,'Unsafe T15 manifest path')
    return value

def _t15_array(plan,path,name):
    source=_t15_data(plan,path).decode()
    marker='def '+name+' : Array Name := #['
    _t15_require(source.count(marker)==1,'Changed T15 source-owned declaration array')
    raw=source.split(marker,1)[1].split(']',1)[0]
    values=re.findall(r'`([\w.]+)',raw)
    _t15_require(values and len(values)==len(set(values)),'Invalid T15 authored declaration inventory')
    return values

def source_checker_inputs_t15(plan):
    """Validate every original lock path before normal Python can read it."""
    for path,expected in (T15_PYTHON_INPUTS|T15_LOCK_INPUTS).items():
        _t15_require(hashlib.sha256(_t15_data(plan,path)).hexdigest()==expected,'Changed reviewed T15 input: '+path)
    actual_python={p for p in plan['file_paths']if p.endswith('.py')}
    _t15_require(actual_python==set(T15_PYTHON_INPUTS),'Unreviewed adjacent T15 Python import source')
    lock=json.loads(_t15_data(plan,'verification/source-lock.json'))
    _t15_require(set(lock)=={'new_modules','files','dependency_revisions'},'Wrong T15 lock schema')
    def check(rows,keys,count):
        _t15_require(isinstance(rows,list)and len(rows)==count,'Changed T15 lock census')
        seen=set()
        for row in rows:
            _t15_require(isinstance(row,dict)and set(row)==keys,'Wrong T15 lock row')
            path=_t15_path(row['path']);_t15_require(path not in seen,'Duplicate T15 lock path');seen.add(path)
            _t15_require(hashlib.sha256(_t15_data(plan,path)).hexdigest()==row['sha256'],'Changed T15 locked source: '+path)
        return seen
    check(lock['files'],{'path','sha256'},203)
    preserved=json.loads(_t15_data(plan,'verification/preserved-module-lock.json'))
    roots=check(preserved,{'path','sha256','source'},88)
    _t15_require(sum(r['source']=='unified-v3'for r in preserved)==76,'Changed T15 preserved predecessor census')
    modules=json.loads(_t15_data(plan,'MODULES.json'))
    _t15_require(isinstance(modules,list)and len(modules)==len(set(modules))==88 and
        all(isinstance(n,str)and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',n)for n in modules),'Changed T15 module inventory')
    expected={name+'.lean'for name in modules}
    actual={p for p in plan['file_paths']if '/'not in p and p.endswith('.lean')and p!='lakefile.lean'}
    _t15_require(roots==expected==actual,'T15 root coverage changed')
    new=lock['new_modules']
    _t15_require(isinstance(new,list)and len(new)==len(set(new))==22 and set(new)<=set(modules),'Changed T15 new-source inventory')
    for name in new:_t15_path(name+'.lean')
    manifest=json.loads(_t15_data(plan,'lake-manifest.json'))
    _t15_require({p['name']:p['rev']for p in manifest['packages']}==lock['dependency_revisions']and len(manifest['packages'])==9,'Changed T15 dependency closure')
    _t15_require(_t15_data(plan,'lean-toolchain').decode().strip()=='leanprover/lean4:v4.19.0','Changed T15 Lean toolchain')
    for path in ['verification/AllProjectProofAudit.lean',T15_EXPORT_SOURCE]:
        _t15_require(set(_t15_array(plan,path,'modules'))==set(modules),'Changed T15 complete audit module coverage')

def validate_t15_driver(driver,plan):
    _t15_require(driver['recipe']in T15_SOURCE_RECIPES,'Unknown T15 driver recipe')
    path,expected,_=T15_SOURCE_RECIPES[driver['recipe']]
    _t15_require(driver['sha256']==expected and driver['argument_meanings']=={}and driver['external_input_id']is None,
        'Changed T15 original driver binding')
    _t15_require(plan['files'][driver['source_id']]['path']==path and hashlib.sha256(_t15_data(plan,path)).hexdigest()==expected,'Changed T15 driver source/location')

def validate_t15_argv(stage,driver,plan):
    validate_t15_driver(driver,plan)
    path,_,kind=T15_SOURCE_RECIPES[driver['recipe']]
    _t15_require(stage['kind']==kind and stage['cwd']=='.'and stage['argv']==['{tool:python}','{project}/'+path]
        and stage['output_paths']==[]and stage['expected_exit_codes']==[0]and stage['control_ids']==[],
        'T15 original assertion-bearing driver requires exact normal-mode invocation')

def t15_export_stage(stage,plan):
    """Only this source-bound final exporter may create this fresh project child."""
    if not(stage['id']=='original-audit-verification-ExportDeclarationInventory'and stage['kind']=='LEAN_AUDIT'
        and stage['driver_id']is None and stage['cwd']=='.'and stage['argv']==['{tool:lean}','-j1','{project}/'+T15_EXPORT_SOURCE]
        and stage['output_paths']==[T15_EXPORT_OUTPUT]and stage['expected_exit_codes']==[0]):return False
    if T15_EXPORT_SOURCE not in plan['file_paths']or hashlib.sha256(_t15_data(plan,T15_EXPORT_SOURCE)).hexdigest()!=T15_EXPORT_SHA:return False
    target=T15_EXPORT_OUTPUT.removeprefix('project/')
    if any(p==target or p.startswith(target+'/')or target.startswith(p+'/')for p in plan['file_paths']):return False
    return True

def validate_t15_package(suite,plan):
    source_checker_inputs_t15(plan)
    _t15_require({d['recipe']for d in suite['replay']['drivers']}==set(T15_SOURCE_RECIPES),'Incomplete T15 original driver inventory')
    _t15_require('verification.ExportDeclarationInventory'not in suite['replay']['module_order'],'Exporter would create an undeclared earlier output')
    writers=[s for s in suite['replay']['stages']if s['argv'][-1]=='{project}/'+T15_EXPORT_SOURCE]
    _t15_require(len(writers)==1 and writers[0]==suite['replay']['stages'][-1]
        and t15_export_stage(writers[0],plan),'T15 exporter must execute once at its original final stage')

def verify_t15_python3(resolved,env):
    """Bind the source driver's literal child executable to the declared Python."""
    _t15_require('python'in resolved and isinstance(env.get('PATH'),str)and env['PATH'],'Missing T15 Python environment')
    actual=shutil.which('python3',path=env['PATH'])
    _t15_require(actual is not None,'T15 original child python3 is unavailable')
    selected=Path(resolved['python']);child=Path(actual)
    _t15_require(selected.resolve()==child.resolve()and hashlib.sha256(selected.read_bytes()).hexdigest()==T15_PYTHON_SHA
        and hashlib.sha256(child.read_bytes()).hexdigest()==T15_PYTHON_SHA,'Ambient python3 differs from the exact declared T15 interpreter')
    _t15_require(not any(k in env for k in ['PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME']),'T15 assertion-bearing Python environment is contaminated')
    return 'T15_AMBIENT_PYTHON3_BINDING_PASS executable_sha256='+T15_PYTHON_SHA

def _t15_one(text,pattern):
    rows=list(re.finditer('^'+pattern+'$',text,re.M))
    _t15_require(len(rows)==1,'Original T15 audit terminal is absent or duplicated')
    return rows[0]

def _t15_axes(raw,allowed=T15_AXES):
    values=[x.strip()for x in raw.split(',')if x.strip()]
    _t15_require(len(values)==len(set(values))and set(values)<=allowed,'Unapproved or duplicate T15 axiom readback')
    return set(values)

def _t15_summary(text,prefix,fields):
    patterns=[re.escape(k)+('=\\[([^\\]]*)\\]'if k=='axioms'else'=(\\d+)')for k in fields]
    row=_t15_one(text,re.escape(prefix)+'; '.join(patterns))
    result={k:(_t15_axes(v)if k=='axioms'else int(v))for k,v in zip(fields,row.groups())}
    for k in ['unsafeOrPartialDependencies','unsafeOrPartial']:
        if k in result:_t15_require(result[k]==0,'Unsafe/partial T15 proof dependency')
    return result

def _t15_safe_readbacks(path,text,plan,prefix='SAFE_CLOSURE_PASS',command='audit_safe_closure'):
    names=re.findall(r'^#'+command+r' ([\w.]+)$',_t15_data(plan,path).decode(),re.M)
    rows=re.findall(r'^'+prefix+r' ([^ ;\n]+); declarations=(\d+); axioms=\[([^\]]*)\]$',text,re.M)
    _t15_require([r[0]for r in rows]==names,'Missing, duplicate or foreign T15 safe-closure readback')
    for _,count,axes in rows:
        _t15_require(int(count)>0,'Empty T15 checked closure');_t15_axes(axes)

def _t15_namespace_rows(text,prefix,owners):
    rows=re.findall(r'^'+prefix+r'COMPILED_DECLARATION ([^ ;\n]+); theorem=(true|false); axioms=\[([^\]]*)\]$',text,re.M)
    aux=re.findall(r'^'+prefix+r'NONPROOF_RUNTIME_AUXILIARY ([^ ;\n]+); unsafe=(true|false); partial=(true|false)$',text,re.M)
    _t15_require(rows and len(rows)==len({r[0]for r in rows})and len(aux)==len({r[0]for r in aux}),'Duplicate/absent T15 namespace census')
    _t15_require(not({r[0]for r in rows}&{r[0]for r in aux}),'Compiler auxiliary counted as a safe proof root')
    for name,_,axes in rows:
        _t15_require(any(name.startswith(owner+'.')for owner in owners),'Unexpected T15 declaration owner');_t15_axes(axes)
    for name,unsafe,partial in aux:
        _t15_require(any(name.startswith(owner+'.')for owner in owners)and'true'in(unsafe,partial),'Invalid T15 compiler auxiliary role')
    return rows,aux

def _t15_census(info,rows,aux):
    _t15_require(info['safeRoots']==len(rows)and info['namespaceDeclarations']==len(rows)+len(aux)
        and info['namespaceTheorems']==sum(r[1]=='true'for r in rows)and info['nonproofRuntimeAuxiliaries']==len(aux)
        and info['reachableCheckedDeclarations']>=len(rows),'Inconsistent T15 declaration/closure census')

def _t15_export_result(stage,text,plan,output):
    _t15_require(t15_export_stage(stage,plan)and output is not None,'Unapproved T15 export stage')
    counts=_t15_summary(text,'DECLARATION_INVENTORY_PASS ',['modules','declarations'])
    path=Path(output)/T15_EXPORT_OUTPUT
    _t15_require(path.is_file()and not path.is_symlink(),'Missing fresh T15 declaration inventory')
    # The core path_in/fresh-output gates also check ancestor symlinks and collisions.
    rows=json.loads(path.read_text());modules=set(json.loads(_t15_data(plan,'MODULES.json')))
    _t15_require(isinstance(rows,list)and rows and counts['modules']==len(modules)==88 and counts['declarations']==len(rows),'T15 declaration export census mismatch')
    names=set()
    for row in rows:
        _t15_require(isinstance(row,dict)and set(row)=={'module','name','theorem','unsafe','partial'},'Wrong T15 declaration inventory row')
        _t15_require(isinstance(row['module'],str)and row['module']in modules and isinstance(row['name'],str)and row['name']and row['name']not in names,'Wrong T15 declaration inventory identity')
        names.add(row['name'])
        _t15_require(all(type(row[k])is bool for k in ['theorem','unsafe','partial']),'Non-Boolean T15 declaration metadata')

def check_t15_stage(stage,text,plan,output=None,inherited_checker=None):
    """Read original completion contracts; never synthesize child executions."""
    path=stage['argv'][-1].removeprefix('{project}/')
    if stage['kind']=='SOURCE_CHECK':
        _t15_require(text.strip()=='SOURCE_IDENTITY_PASS: 88 roots; 86 preserved v4 modules; 2 exact polynomial-test support modules; nine exact dependency pins','Original T15 source verification did not complete')
        return
    if path=='verification/test_source_checks.py':
        labels=re.findall(r"^run_mutation\('([^']+)'",_t15_data(plan,path).decode(),re.M)
        observed=re.findall(r'^EXPECTED_SOURCE_REJECTION: (.+)$',text,re.M)
        _t15_require(len(labels)==15 and observed==labels,'Original fifteen source mutations did not complete exactly')
        _t15_one(text,'SOURCE_CONTROL_MUTATIONS_PASS: fifteen deliberate invalid successors rejected')
        _t15_require(text.splitlines()==['EXPECTED_SOURCE_REJECTION: '+s for s in labels]+['SOURCE_CONTROL_MUTATIONS_PASS: fifteen deliberate invalid successors rejected'],'Unexpected source-mutation driver output')
        return
    if stage['kind']=='NEGATIVE_CONTROL':
        if '/inherited/negative-controls/'in path:
            errors=[line for line in text.splitlines()if': error:'in line]
            _t15_require(len(errors)==1 and re.search(r': error: (?:application )?type mismatch',errors[0]),'Original inherited control requires one intended type error')
        return
    if stage['id'].startswith(('complexity-positive-','boolean-positive-')):
        _t15_require(not re.search(r'warning:|error:',text),'Original fresh positive prerequisite emitted a warning/error')
    if path.startswith('verification/inherited/')or path=='ExtensionalRepairAudit.lean':
        _t15_require(inherited_checker is not None,'Missing reviewed inherited T14 parser')
        translated=dict(stage);translated['argv']=list(stage['argv']);translated['argv'][-1]=stage['argv'][-1].replace('/inherited/','/')
        aliases=dict(plan['file_paths'])
        aliases.update({p.replace('/inherited/','/'):r for p,r in plan['file_paths'].items()if p.startswith('verification/inherited/')})
        inherited_checker(translated,text,{**plan,'file_paths':aliases})
        return
    if path==T15_EXPORT_SOURCE:
        _t15_export_result(stage,text,plan,output);return
    if path=='CheckerControls.lean':
        _t15_require(re.findall(r'^(true|false)$',text,re.M)==['true','false','true','false','true'],'Original checker evaluation readback changed')
        return
    if path=='verification/KernelAudit.lean':
        rows,aux=_t15_namespace_rows(text,'',['P01AC.EffectiveCompleteness'])
        info=_t15_summary(text,'EFFECTIVE_KERNEL_AUDIT_PASS: ',['namespaceDeclarations','namespaceTheorems','authoredDeclarations','authoredTheorems','safeRoots','nonproofRuntimeAuxiliaries','reachableCheckedDeclarations','axioms','unsafeOrPartialDependencies'])
        _t15_census(info,rows,aux)
        authored=_t15_array(plan,path,'authored');theorems=_t15_array(plan,path,'authoredTheorems')
        _t15_require(info['authoredDeclarations']==len(authored)and info['authoredTheorems']==len(theorems)
            and set(authored)<={n for n,_,_ in rows}and set(theorems)<={n for n,t,_ in rows if t=='true'},'Changed T15 authored declaration/theorem census')
        _t15_safe_readbacks(path,text,plan);return
    if path in ['verification/ComplexityKernelAudit.lean','verification/BooleanKernelAudit.lean']:
        boolean='Boolean'in path;prefix='BOOLEAN'if boolean else'COMPLEXITY'
        owners=['P01AC.BooleanIdentity','P01AC.BooleanPrimitive','P01AC.BooleanControls']if boolean else['P01AC.EffectiveCompleteness','P01AC.IdentityComplexity']
        _t15_require(re.findall(r'^'+prefix+r'_NAMESPACE_AUDIT_PASS ([^;]+);',text,re.M)==owners,'Changed T15 namespace audit inventory')
        rows,aux=_t15_namespace_rows(text,prefix+'_',owners)
        for owner in owners:
            info=_t15_summary(text,prefix+'_NAMESPACE_AUDIT_PASS '+owner+'; ',['namespaceDeclarations','namespaceTheorems','safeRoots','nonproofRuntimeAuxiliaries','reachableCheckedDeclarations','axioms','unsafeOrPartialDependencies'])
            _t15_census(info,[r for r in rows if r[0].startswith(owner+'.')],[r for r in aux if r[0].startswith(owner+'.')])
        if boolean:
            info=_t15_summary(text,'BOOLEAN_KERNEL_AUDIT_PASS: ',['authoredDeclarations','authoredTheorems','safeRoots','reachableCheckedDeclarations','axioms','unsafeOrPartialDependencies'])
            authored=_t15_array(plan,path,'authoredBoolean');theorems=_t15_array(plan,path,'authoredBooleanTheorems')
            _t15_require(info['authoredDeclarations']==len(authored)and info['authoredTheorems']==len(theorems),'Changed Boolean authored census')
            roots=info['safeRoots']
        else:
            info=_t15_summary(text,'COMPLEXITY_KERNEL_AUDIT_PASS: ',['successorAuthoredDeclarations','successorAuthoredTheorems','predecessorAuthoredDeclarations','predecessorAuthoredTheorems','combinedSafeRoots','reachableCheckedDeclarations','axioms','unsafeOrPartialDependencies'])
            authored=_t15_array(plan,path,'successorAuthored');theorems=_t15_array(plan,path,'successorTheorems')
            prior=_t15_array(plan,'verification/KernelAudit.lean','authored');prior_theorems=_t15_array(plan,'verification/KernelAudit.lean','authoredTheorems')
            _t15_require(info['successorAuthoredDeclarations']==len(authored)and info['successorAuthoredTheorems']==len(theorems)
                and info['predecessorAuthoredDeclarations']==len(prior)and info['predecessorAuthoredTheorems']==len(prior_theorems),'Changed complexity authored census')
            authored+=prior;theorems+=prior_theorems;roots=info['combinedSafeRoots']
        _t15_require(roots==len(rows)and info['reachableCheckedDeclarations']>=roots
            and set(authored)<={n for n,_,_ in rows}and set(theorems)<={n for n,t,_ in rows if t=='true'},'Incomplete T15 combined closure/authored census')
        _t15_safe_readbacks(path,text,plan,prefix+'_SAFE_CLOSURE_PASS','audit_'+prefix.lower()+'_safe_closure');return
    simple={'verification/RestrictedKernelAudit.lean':('RESTRICTED','theorems'),
        'CheckerKernelAudit.lean':('V2','namespaceTheorems'),'PolynomialTestAudit.lean':('POLYNOMIAL_TEST','theorems')}
    if path in simple:
        prefix,theorems=simple[path]
        info=_t15_summary(text,prefix+'_KERNEL_AUDIT_PASS ',['safeRoots',theorems,'nonproofRuntimeAuxiliaries','reachableCheckedDeclarations','axioms','unsafeOrPartialDependencies'])
        aux=re.findall(r'^'+prefix+r'_NONPROOF_RUNTIME_AUXILIARY ([^ ;\n]+); unsafe=(true|false); partial=(true|false)$',text,re.M)
        owner=re.findall(r'let ns := `([\w.]+)',_t15_data(plan,path).decode())
        _t15_require(len(owner)==1 and all(name.startswith(owner[0]+'.')for name,_,_ in aux),'Foreign T15 compiler auxiliary owner')
        _t15_require(info['safeRoots']>0 and 0<info[theorems]<=info['safeRoots']<=info['reachableCheckedDeclarations']
            and info['nonproofRuntimeAuxiliaries']==len(aux)==len({r[0]for r in aux})and all('true'in r[1:]for r in aux),'Invalid T15 restricted/compiler auxiliary census')
        _t15_safe_readbacks(path,text,plan);return
    if path=='verification/RestrictedComputationalAudit.lean':
        count=int(_t15_one(text,r'INDEPENDENT_COMPUTABLE_CLOSURE_PASS declarations=(\d+); no classical choice or abstract polynomial dependency').group(1))
        row=_t15_summary(text,'INDEPENDENT_CHECKER_SAFE_CLOSURE ',['declarations','axioms'])
        _t15_require(count==row['declarations']and count>0 and'Classical.choice'not in row['axioms'],'Invalid T15 executable proof-closure readback')
        _t15_safe_readbacks(path,text,plan);return
    if path=='verification/AllProjectProofAudit.lean':
        row=_t15_summary(text,'INDEPENDENT_ALL_PROJECT_PROOF_AUDIT_PASS ',['modules','theoremRoots','checkedClosure','axioms','unsafeOrPartial'])
        _t15_require(row['modules']==len(_t15_array(plan,path,'modules'))==88 and 0<row['theoremRoots']<=row['checkedClosure'],'Incomplete T15 all-project proof census')


def _validate_argv(stage, plan):
    argv = stage['argv']
    require(isinstance(argv, list) and argv and all(isinstance(a, str) and a and '\x00' not in a for a in argv), 'Missing explicit argument vector')
    driver = plan['drivers'].get(stage['driver_id'])
    if driver is not None:
        recipe = driver['recipe']
        if recipe == CORE_RECIPE:
            validate_core_argv(stage, driver, plan)
            return
        if recipe == ATTR_RECIPE:
            validate_attribution_argv(stage, driver, plan)
            return
        if recipe == HISTORY_RECIPE:
            validate_history_argv(stage, driver, plan)
            return
        if recipe in T10_FINITE_RECIPES:
            validate_t10_argv(stage, driver, plan)
            return
        if recipe in LANGUAGE_RECIPES:
            require(argv[:4] == ['{tool:python}', '-I', '-B', '{driver:' + driver['id'] + '}'] and len(argv) == 5, 'Wrong reviewed Python recipe')
            match = re.fullmatch(r'\{(input|fixture):([^{}]+)\}', argv[4])
            require(match and match.group(2) in plan[match.group(1) + 's'], 'Undeclared driver input')
            require(stage['kind'] in {'REFERENCE_TESTS', 'NEGATIVE_CONTROL', 'DRIVER'}, 'Wrong language stage kind')
            return
        if recipe in SOURCE_RECIPES:
            require(stage['kind'] == 'SOURCE_CHECK' and argv == ['{builtin:source-check}'], 'Wrong source-check translation')
            return
        if recipe in T15_SOURCE_RECIPES:
            validate_t15_argv(stage, driver, plan)
            return
        if recipe in NORMAL_SOURCE_RECIPES:
            original = ['{tool:python}', '{project}/' + plan['files'][driver['source_id']]['path']] if 'files' in plan else None
            require(stage['kind'] == 'SOURCE_CHECK' and stage['cwd'] == '.' and not stage['output_paths'] and
                    argv in [original, ['{tool:python}', '-B', '{driver:' + driver['id'] + '}']], 'Original assertion-bearing checker requires exact normal-mode arguments')
            return
        if recipe in EMPIRICAL_RECIPES:
            require(stage['cwd'] == '.', 'Empirical package must keep its reviewed working directory')
            if recipe == 't15-empirical-integrity-v1':
                require(stage['kind'] == 'SOURCE_CHECK' and argv == ['{builtin:source-check}'] and not stage['output_paths'], 'Wrong empirical checksum recipe')
                return
            if recipe == 't15-empirical-tests-v1':
                require(stage['kind'] == 'REFERENCE_TESTS' and argv == ['{tool:python}', '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'] and not stage['output_paths'], 'Wrong empirical unittest recipe')
                return
            prefix = ['{tool:python}', '-B', '{driver:' + driver['id'] + '}', '--decisions-zip']
            require(argv[:4] == prefix and len(argv) in {7, 9} and argv[5:7] == ['--summary-xlsx', '{input:summary_xlsx}'], 'Wrong empirical driver arguments')
            require({'decisions_zip', 'summary_xlsx'} <= set(plan['inputs']), 'Missing empirical exact inputs')
            if stage['kind'] == 'NEGATIVE_CONTROL':
                match = re.fullmatch(r'\{fixture:([^{}]+)\}', argv[4])
                require(recipe == 't15-empirical-reanalyse-v1' and len(argv) == 7 and match and match.group(1) in plan['fixtures'], 'Wrong empirical negative fixture')
                fixture = plan['fixtures'][match.group(1)]
                require(fixture['input_id'] == 'decisions_zip' and fixture['operation'] == 'APPEND_CHANGED_BYTES' and fixture['path'] is None and not stage['output_paths'], 'Empirical fixture changes a different input')
            else:
                require(stage['kind'] == 'REFERENCE_TESTS' and argv[4] == '{input:decisions_zip}', 'Wrong empirical positive input')
                if recipe == 't15-empirical-reanalyse-v1':
                    require(len(argv) == 9 and argv[7] == '--output' and argv[8].startswith('{out}/'), 'Empirical output must be fresh and explicit')
                    require(stage['output_paths'] == [relative(argv[8][len('{out}/'):])], 'Empirical aggregate output not declared exactly')
                else: require(len(argv) == 7 and not stage['output_paths'], 'Unexpected validation output')
            return
        raise ValueError('Unapproved source-specific recipe')
    require(stage['driver_id'] is None, 'Unknown driver')
    require(argv[0] == '{tool:lean}' and argv[1:2] == ['-j1'], 'Undeclared executable or compiler options')
    require(stage['kind'] in {'LEAN_COMPILE', 'LEAN_AUDIT', 'POSITIVE_CONTROL', 'NEGATIVE_CONTROL'}, 'Unsupported built-in stage')
    if stage['kind'] == 'LEAN_COMPILE':
        require(len(argv) == 5 and argv[2] == '-o', 'Wrong serial compile argument vector')
    # The canonical compile vector has five tokens after the executable is counted.
    if len(argv) == 5 and argv[2] == '-o':
        output, source = argv[3:]
    else:
        require(len(argv) == 3 and stage['kind'] != 'LEAN_COMPILE', 'Undeclared Lean arguments')
        output, source = None, argv[2]
    require(source.startswith('{project}/'), 'Lean source is not a projected file')
    name = source[len('{project}/'):]
    relative(name)
    require(name in plan['file_paths'] and name.endswith('.lean'), 'Undeclared Lean source')
    row = plan['file_paths'][name]
    if output is not None:
        require(output.startswith(('{build}/', '{out}/')) and output.endswith('.olean'), 'Undeclared object output')
        object_rel = 'build/' + relative(output[len('{build}/'):]) if output.startswith('{build}/') else relative(output[len('{out}/'):])
        require(stage['output_paths'] == [object_rel], 'Object output is not declared exactly')
        require(row['role'] != 'NEGATIVE', 'Negative fixture cannot produce an accepted custom object')
        module = next((m for m in plan['modules'].values() if m['source_id'] == row['source_id']), None)
        require(module and any(object_rel == root + '/' + module['name'].replace('.', '/') + '.olean' for root in plan['build_roots']), 'Object module identity mismatch')
        lean_name(module['name'])
    else:
        require(stage['output_paths'] == [] or t15_export_stage(stage, plan), 'Interpretation stage has undeclared outputs')
    require((row['role'] == 'NEGATIVE') == (stage['kind'] == 'NEGATIVE_CONTROL'), 'Negative source/stage role mismatch')


def validate_t10_argv(stage, driver, plan):
    argv = stage['argv']; recipe = driver['recipe']
    if argv[:1] == ['{builtin:observe-child}']:
        require(recipe == 't10-independent-mutations-v1' and stage['kind'] == 'NEGATIVE_CONTROL' and
                len(argv) == 3 and argv[2] in T10_CHILD_DIAGNOSTICS, 'Unknown source child observation')
        parent = plan['stages'].get(argv[1])
        require(parent and parent['driver_id'] == driver['id'] and parent['kind'] == 'DRIVER' and argv[1] in stage['depends_on'], 'Observed child has a different physical parent')
        require(stage['expected_exit_codes'] == [1] and not stage['output_paths'] and stage['cwd'] == '.', 'Changed child rejection contract')
        return
    require(stage['kind'] == ('DRIVER' if recipe == 't10-independent-mutations-v1' else 'REFERENCE_TESTS'), 'Wrong written finite stage kind')
    prefix = ['{tool:python}', '-B']; optimized = '-O' in argv
    if optimized:
        require(recipe in {'t10-unit-v1', 't10-independent-review-v1', 't10-two-card-v1'}, 'Original assertion-bearing recipe cannot be optimized')
        prefix.append('-O')
    if recipe == 't10-unit-v1':
        require(stage['cwd'] == T10_CHECKER and argv == prefix + ['-m', 'unittest', 'discover', '-s', 'tests', '-v'] and not stage['output_paths'], 'Wrong original unit command')
        return
    prefix.append('{driver:' + driver['id'] + '}')
    outputs = T10_OUTPUTS.get(recipe, [])
    if recipe in {'t10-exhaustive-v1', 't10-source-release-v1', 't10-semantic-v1'}:
        require(stage['cwd'] == T10_CHECKER, 'Written checker working directory changed')
    else: require(stage['cwd'] == '.', 'Written reviewer working directory changed')
    if recipe == 't10-independent-review-v1':
        name = 'independent-optimized.json' if optimized else 'independent-normal.json'
        prefix += ['--candidate', '{project}/' + T10_CHECKER, '--output', '{out}/' + name]; outputs = [name]
    elif recipe == 't10-independent-mutations-v1':
        prefix += ['--candidate', '{project}/' + T10_CHECKER, '--directory', '{out}/mutation-copies']
    require(argv == prefix and set(stage['output_paths']) == set(outputs), 'Wrong original written arguments/outputs')


def validate_t10_package(suite, plan):
    require(suite['replay']['scope'] == 'FINITE' and suite['toolchain']['kind'] == 'PYTHON' and suite['toolchain']['version'].startswith('3.12.'), 'Written finite suite requires source-prescribed Python 3.12')
    for name, expected in T10_FILES.items():
        require(name in plan['file_paths'] and sha(plan['contents'][plan['file_paths'][name]['source_id']]) == expected, 'Written finite source closure changed: ' + name)
    require(all(not name.endswith('.py') or name in T10_FILES for name in plan['file_paths']), 'Unreviewed Python source in written finite closure')
    expected = ['t10-unit-v1'] * 2 + ['t10-exhaustive-v1', 't10-source-release-v1', 't10-semantic-v1', 't10-independent-selftest-v1'] + ['t10-independent-review-v1'] * 2 + ['t10-independent-mutations-v1'] + ['t10-two-card-v1'] * 2
    physical = [stage for stage in plan['stages'].values() if stage['argv'][:1] != ['{builtin:observe-child}']]
    require([plan['drivers'][s['driver_id']]['recipe'] for s in physical] == expected, 'Original written command census/order changed')
    require([('-O' in s['argv']) for s in physical] == [False, True, False, False, False, False, False, True, False, False, True], 'Original normal/optimized census changed')
    require([s['timeout_seconds'] for s in physical] == [180, 180, 300, 300, 300, 180, 300, 300, 900, 180, 180], 'Original written command budgets changed')
    observed = [s for s in plan['stages'].values() if s['argv'][:1] == ['{builtin:observe-child}']]
    require([s['argv'][2] for s in observed] == list(T10_CHILD_DIAGNOSTICS), 'Original written child census changed')
    for stage in observed:
        require(physical[6]['id'] in stage['depends_on'], 'Mutation child lacks completed independent positive prerequisite')


def core_tracer_argv(stage):
    return ['{tool:python}', '-B', '{adapter}', '--trace-core-runtime', stage['argv'][2],
            '{out}/traces/' + stage['id'], *stage['argv'][3:]]


def core_child_spec(child, source_id, source_path, archive_id):
    name = child.removeprefix('runtime/')
    build = None if name == 'RuntimeReadback' else 'original/runtime/build/' + name.replace('.', '/') + '.olean'
    base = '{archive:' + archive_id + '}'
    command = ['{tool:lean}', '-j1', '--root=' + base + ('/readbacks' if build is None else '/runtime/src')]
    if build: command += ['-o', '{out}/' + build]
    command.append(base + '/' + source_path)
    return {'id': child, 'source_id': source_id, 'source_path': source_path, 'output_path': build,
            'argv': command, 'log': 'original/runtime/logs/' + name + '.log'}


def validate_core_package(suite, plan):
    require(len(plan['drivers']) == len(plan['inputs']) == 1 and not plan['fixtures'], 'Core runtime uses one original archive and one driver')
    driver = next(iter(plan['drivers'].values())); iid = driver['external_input_id']; archive = plan['inputs'][iid]
    require(archive['kind'] == 'FILE' and archive['expected_sha256'] == CORE_ARCHIVE_SHA and archive['expected_bytes'] == 1286198, 'Wrong exact original core archive')
    for name, expected in CORE_FILES.items():
        if name == 'MATHLIB_ARCHIVE_INVENTORY.json': continue
        require(name in plan['file_paths'] and sha(t10_contents(plan, name)) == expected, 'Core helper/source manifest changed')
    manifest = json.loads(t10_contents(plan, 'SOURCE_MANIFEST.json'))
    expected = {row['path']: row for row in manifest['sources'] if row['path'].startswith('runtime/src/')}
    require(len(expected) == len(plan['modules']) == len(suite['replay']['module_order']) == 167, 'Original runtime closure census changed')
    require(set(plan['file_paths']) == set(expected) | {'readbacks/RuntimeReadback.lean', 'replay.py', 'verify_dependency_identity.py', 'SOURCE_MANIFEST.json', 'DEPENDENCY_PINS.json'}, 'Original runtime projection census changed')
    for name, row in expected.items():
        data = t10_contents(plan, name)
        require(sha(data) == row['sha256'] and len(data) == row['bytes'], 'Runtime source differs from original manifest')
    readback = next(row for row in manifest['sources'] if row['path'] == 'readbacks/RuntimeReadback.lean')
    require(sha(t10_contents(plan, readback['path'])) == readback['sha256'], 'Original runtime readback changed')
    require(set(imports(t10_contents(plan, readback['path']).decode())) <= set(plan['modules']) | set(plan['official']), 'Readback import closure is undeclared')
    require(suite['replay']['build_roots'] == ['original/runtime/build'], 'Runtime objects need their original isolated namespace')
    tools = {row['name']: row for row in suite['replay']['tools']}
    require(tools['lean-bin']['kind'] == 'LEAN' and tools['lean-bin']['path_kind'] == 'BIN_DIRECTORY' and tools['lean-bin']['executable_sha256'] == LEAN_SHA and tools['lean-bin']['version'] == '4.19.0', 'Core requires the official Lean bin directory')
    require(tools['python']['kind'] == 'PYTHON' and tools['python']['path_kind'] == 'EXECUTABLE', 'Core requires an explicit Python interpreter')
    children = {}
    for name in suite['replay']['module_order']:
        sid = plan['modules'][name]['source_id']; path = plan['files'][sid]['path']
        require(path == 'runtime/src/' + name.replace('.', '/') + '.lean', 'Wrong core module namespace')
        children['runtime/' + name] = core_child_spec('runtime/' + name, sid, path, iid)
    sid = plan['file_paths'][readback['path']]['source_id']
    children['runtime/RuntimeReadback'] = core_child_spec('runtime/RuntimeReadback', sid, readback['path'], iid)
    plan['core_children'] = children
    stages = list(plan['stages'].values())
    require(len(stages) == 169 and stages[0]['kind'] == 'DRIVER' and stages[0]['timeout_seconds'] == 36000, 'Original runtime parent contract changed')
    require([stage['argv'][2] for stage in stages[1:]] == list(children), 'Missing, duplicate or reordered original runtime observation')
    require(all(stage['argv'][1] == stages[0]['id'] and stage['driver_id'] == driver['id'] and stages[0]['id'] in stage['depends_on'] for stage in stages[1:]), 'Original runtime child belongs to another parent')


def validate_core_argv(stage, driver, plan):
    require(stage['cwd'] == '.' and stage['expected_exit_codes'] == [0] and not stage['expected_diagnostics'], 'Core runtime is a successful proof/counterexample contract')
    if stage['argv'][:1] == ['{builtin:observe-child}']:
        require(len(stage['argv']) == 3 and stage['argv'][2] in plan['core_children'] and not stage['output_paths'] and stage['timeout_seconds'] == 180, 'Wrong source-owned runtime observation')
        require(stage['kind'] == ('LEAN_AUDIT' if stage['argv'][2] == 'runtime/RuntimeReadback' else 'POSITIVE_CONTROL'), 'Wrong original runtime child role')
    else:
        require(stage['kind'] == 'DRIVER' and stage['output_paths'] == ['original'] and stage['argv'] ==
                ['{tool:python}', '-B', '{driver:' + driver['id'] + '}', '--lean-bin', '{tool:lean-bin}', '--mathlib', '{dependency:mathlib}', '--out', '{out}/original', '--mode', 'runtime'], 'Unreviewed original runtime invocation')


def attribution_specs(archive_id, plan=None):
    result = {}; base = '{archive:' + archive_id + '}'
    for name, source, emits in ATTR_PATHS:
        output = 'original/build/' + name + '.olean' if emits else None
        argv = ['{tool:lean}', '-j1'] + (['-o', '{out}/' + output] if output else []) + [base + '/' + source]
        result[name] = {'id': name, 'source_id': plan['modules'][name]['source_id'] if plan else None,
            'source_path': source, 'output_path': output, 'argv': argv,
            'cwd': base + '/' + str(PurePosixPath(source).parent),
            'log': 'original/' + ('mutants/' if name in ATTR_DIAGNOSTICS else 'logs/') + name + '.log',
            'exit_code': 1 if name in ATTR_DIAGNOSTICS else 0}
    return result


def validate_attribution_package(suite, plan):
    require(len(plan['drivers']) == len(plan['inputs']) == 1 and not plan['fixtures'], 'Attribution needs its one original archive/driver')
    driver = next(iter(plan['drivers'].values())); iid = driver['external_input_id']; archive = plan['inputs'][iid]
    require(archive['kind'] == 'FILE' and archive['expected_sha256'] == ATTR_CONTRACT['archive_sha256'] and archive['expected_bytes'] == ATTR_CONTRACT['archive_bytes'], 'Wrong attribution source archive')
    require(set(plan['modules']) == {row[0] for row in ATTR_PATHS} and suite['replay']['module_order'] == ['RootImage', 'Availability', 'FixedFamilies'] and plan['build_roots'] == ['original/build'], 'Original attribution module/target namespace changed')
    plan['attribution_children'] = attribution_specs(iid, plan)
    stages = list(plan['stages'].values())
    require(len(stages) == 22 and stages[0]['kind'] == 'DRIVER' and stages[0]['timeout_seconds'] == 3600, 'Original attribution parent contract changed')
    require([s['argv'][2] for s in stages[1:]] == list(plan['attribution_children']) and
            all(s['argv'][1] == stages[0]['id'] and s['driver_id'] == driver['id'] and stages[0]['id'] in s['depends_on'] for s in stages[1:]), 'Original attribution observation inventory changed')


def validate_attribution_argv(stage, driver, plan):
    require(stage['cwd'] == '.', 'Attribution wrapper/observation working directory changed')
    if stage['argv'][:1] == ['{builtin:observe-child}']:
        require(len(stage['argv']) == 3 and stage['argv'][2] in plan['attribution_children'] and not stage['output_paths'] and stage['timeout_seconds'] == 30, 'Wrong attribution observation')
        name = stage['argv'][2]; expected = ATTR_DIAGNOSTICS.get(name)
        require(stage['expected_exit_codes'] == ([1] if expected else [0]), 'Changed original attribution child exit')
        if expected:
            require(stage['kind'] == 'NEGATIVE_CONTROL' and stage['expected_diagnostics'] ==
                    [{'source_id': driver['source_id'], 'literal': expected, 'sha256': sha(expected.encode())}], 'Changed original attribution diagnostic')
        else: require(stage['kind'] in {'POSITIVE_CONTROL', 'LEAN_AUDIT'} and not stage['expected_diagnostics'], 'Changed original positive attribution role')
    else:
        require(stage['kind'] == 'DRIVER' and stage['output_paths'] == ['original'] and stage['expected_exit_codes'] == [0] and not stage['expected_diagnostics'] and stage['argv'] ==
            ['{tool:python}', '-B', '{driver:' + driver['id'] + '}', '--lean', '{tool:lean}', '--mathlib', '{dependency:mathlib}', '--output', '{out}/original'], 'Unreviewed attribution original invocation')


def attribution_source_check(root, plan=None):
    require(sha(path_in(root, 'replay.py').read_bytes()) == ATTR_CONTRACT['driver_sha256'] and
            {p.name for p in root.glob('*.py')} == {'replay.py'}, 'Unreviewed attribution driver/import source')
    for name, value in ATTR_MANIFESTS.items(): require(sha(path_in(root, name).read_bytes()) == value, 'Original attribution manifest changed')
    manifest = read_json(root / 'PUBLIC_MANIFEST.json')
    require(len(manifest['files']) == 125, 'Original attribution file census changed')
    names = set()
    for row in manifest['files']:
        name = relative(row['path']); require(name not in names, 'Duplicate original packet file'); names.add(name)
        data = path_in(root, name).read_bytes(); require(len(data) == row['size'] and sha(data) == row['sha256'], 'Original attribution packet bytes changed')
    require(names | {'PUBLIC_MANIFEST.json'} == {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}, 'Original attribution packet file census differs')
    for row in read_json(root / 'dependencies/SOURCE_MANIFEST.json')['files']: relative(row['path'])
    if plan:
        for name, source, emits in ATTR_PATHS:
            sid = plan['modules'][name]['source_id']
            require(path_in(root, source).read_bytes() == plan['contents'][sid], 'Archive/projected attribution scientific source differs')


def attribution_tracer_argv(stage):
    return ['{tool:python}', '-B', '{adapter}', '--trace-attribution', stage['argv'][2],
            '{out}/traces/' + stage['id'], *stage['argv'][3:]]


def verify_attribution_dependencies(source_root, mathlib):
    manifest = path_in(source_root, 'dependencies/SOURCE_MANIFEST.json')
    require(sha(manifest.read_bytes()) == ATTR_MANIFESTS['dependencies/SOURCE_MANIFEST.json'], 'Original dependency manifest changed')
    for row in read_json(manifest)['files']:
        data = path_in(mathlib, row['path']).read_bytes()
        require(len(data) == row['size'] and sha(data) == row['sha256'], 'Original attribution dependency source changed')


def trace_attribution_driver(driver, trace, arguments):
    require(len(arguments) == 6 and arguments[::2] == ['--lean', '--mathlib', '--output'], 'Unreviewed attribution arguments')
    driver = no_symlinks(driver); root = driver.parent; attribution_source_check(root)
    lean = no_symlinks(arguments[1]).resolve(); output = no_symlinks(arguments[5])
    require(sha(lean.read_bytes()) == LEAN_SHA and not output.exists() and output.name == 'original', 'Wrong compiler or reused original output')
    trace = no_symlinks(trace); require(not trace.exists(), 'Trace output must be absent'); trace.mkdir(parents=True)
    mappings = {'tool:lean': lean, 'archive:original': root, 'out': output.parent}
    specs = list(attribution_specs('original').values())
    commands = [[_expand(a, mappings) for a in spec['argv']] for spec in specs]
    directories = [Path(_expand(spec['cwd'], mappings)) for spec in specs]
    old_run = subprocess.run; old_argv = sys.argv; old_path = sys.path[:]
    try:
        subprocess.run = trace_reviewed_commands(old_run, trace, commands, [[str(lean), '--version']], None, working_directories=directories, record_outputs=True)
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(root)
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        subprocess.run = old_run; sys.argv = old_argv; sys.path[:] = old_path
    return 0


def history_claim_source(name):
    require(name in HISTORY_CLAIMS, 'Unreviewed history false claim')
    return ('import NegativeControls\nopen InterlockHistory InterlockHistory.Controls\n'
            'example : ' + HISTORY_CLAIMS[name] + ' := by decide\n').encode()


def history_specs(archive_id, plan=None):
    result = {}; base = '{archive:' + archive_id + '}'
    def add(name, source, emits=False, negative=False, scenario=False):
        output = 'original/build/' + name + '.olean' if emits else None
        actual_source = '{out}/original/controls/' + name + '.lean' if negative else base + '/' + source
        argv = ['{tool:python}', actual_source] if scenario else ['{tool:lean}', '-j1'] + (['-o', '{out}/' + output] if output else []) + [actual_source]
        sid = None
        if plan:
            sid = plan['file_paths']['control-source/' + ('check_controls.py' if negative else 'source_replay.py')]['source_id'] if negative or scenario else plan['modules'][name]['source_id']
        result[name] = {'id': name, 'source_id': sid, 'source_path': source, 'output_path': output, 'argv': argv,
                        'cwd': '{project}', 'log': 'original/' + ('controls/' if negative else 'logs/') + name + ('.json' if scenario else '.log'), 'exit_code': 1 if negative else 0}
    for name, path, emits in HISTORY_PATHS[:7]: add(name, path, emits)
    for name in HISTORY_CLAIMS: add(name, HISTORY_KERNEL + 'check_controls.py', negative=True)
    add('source-replay', HISTORY_KERNEL + 'source_replay.py', scenario=True)
    for name, path, emits in HISTORY_PATHS[7:]: add(name, path, emits)
    return result


def validate_history_package(suite, plan):
    require(len(plan['drivers']) == len(plan['inputs']) == 1 and not plan['fixtures'], 'History needs one original archive/driver')
    driver = next(iter(plan['drivers'].values())); iid = driver['external_input_id']; archive = plan['inputs'][iid]
    require(archive['kind'] == 'FILE' and archive['expected_sha256'] == HISTORY_CONTRACT['archive_sha256'] and archive['expected_bytes'] == HISTORY_CONTRACT['archive_bytes'], 'Wrong original history archive')
    require(set(plan['modules']) == {n for n, _, _ in HISTORY_PATHS} and suite['replay']['module_order'] == ['HistoryModel', 'HistoryInvariant', 'HistorySafety', 'HistoryTrace'] and plan['build_roots'] == ['original/build'], 'History target/import namespace changed')
    for name in ['check_controls.py', 'source_replay.py']:
        require(sha(plan['contents'][plan['file_paths']['control-source/' + name]['source_id']]) == HISTORY_FILES[HISTORY_KERNEL + name], 'Original history helper changed')
    plan['history_children'] = history_specs(iid, plan); stages = list(plan['stages'].values())
    require(len(stages) == 18 and stages[0]['kind'] == 'DRIVER' and stages[0]['timeout_seconds'] == 3600, 'History parent contract changed')
    require([s['argv'][2] for s in stages[1:]] == list(plan['history_children']) and
            all(s['argv'][1] == stages[0]['id'] and s['driver_id'] == driver['id'] and stages[0]['id'] in s['depends_on'] for s in stages[1:]), 'History physical observation order changed')


def validate_history_argv(stage, driver, plan):
    require(stage['cwd'] == '.', 'History working directory changed')
    if stage['argv'][:1] == ['{builtin:observe-child}']:
        require(len(stage['argv']) == 3 and stage['argv'][2] in plan['history_children'] and not stage['output_paths'] and stage['timeout_seconds'] == 30, 'Wrong history observation')
        negative = stage['argv'][2] in HISTORY_CLAIMS
        require(stage['expected_exit_codes'] == ([1] if negative else [0]), 'History child exit changed')
        require(stage['kind'] == ('NEGATIVE_CONTROL' if negative else 'POSITIVE_CONTROL'), 'History child role changed')
        expected = [{'source_id': driver['source_id'], 'literal': value, 'sha256': sha(value.encode())} for value in HISTORY_DIAGNOSTICS] if negative else []
        require(stage['expected_diagnostics'] == expected, 'History source diagnostic changed')
    else:
        require(stage['kind'] == 'DRIVER' and stage['output_paths'] == ['original'] and stage['expected_exit_codes'] == [0] and not stage['expected_diagnostics'] and stage['argv'] ==
            ['{tool:python}', '-B', '{driver:' + driver['id'] + '}', '--lean', '{tool:lean}', '--mathlib', '{dependency:mathlib}', '--output', '{out}/original'], 'Unreviewed history invocation')


def history_source_check(root, plan=None):
    require(sha(path_in(root, 'replay.py').read_bytes()) == HISTORY_CONTRACT['driver_sha256'] and
            {p.name for p in root.glob('*.py')} == {'replay.py'}, 'Unreviewed history driver/import source')
    for path, value in HISTORY_FILES.items(): require(sha(path_in(root, path).read_bytes()) == value, 'Original history source/manifest changed')
    manifest = read_json(root / 'PUBLIC_MANIFEST.json'); require(len(manifest['files']) == 168, 'History source census changed')
    require(len([p for p in root.rglob('*') if p.is_file()]) == 213, 'History archive file census changed')
    names = set()
    for row in manifest['files']:
        name = relative(row['path']); require(name not in names, 'Duplicate history source'); names.add(name)
        data = path_in(root, name).read_bytes(); require(len(data) == row['size'] and sha(data) == row['sha256'], 'History projected source changed')
    require(read_json(root / 'ORIGINAL_TO_PUBLIC.json')['source_archive_sha256'] == HISTORY_ORIGIN_SHA, 'Original history custody changed')
    tree = ast.parse(path_in(root, HISTORY_KERNEL + 'check_controls.py').read_text(encoding='utf-8'))
    claims = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'claims' for t in n.targets)]
    require(claims == [HISTORY_CLAIMS], 'Original history claim table changed')
    if plan:
        for spec in history_specs('original', plan).values():
            require(path_in(root, spec['source_path']).read_bytes() == plan['contents'][spec['source_id']], 'History archive/projected source differs')


def verify_history_dependencies(source_root, mathlib):
    path = path_in(source_root, 'MATHLIB_SOURCE_PIN.json')
    require(sha(path.read_bytes()) == HISTORY_FILES['MATHLIB_SOURCE_PIN.json'], 'History dependency manifest changed')
    rows = read_json(path)['files']; require(len(rows) == 6816, 'History dependency source census changed')
    for row in rows:
        data = path_in(mathlib, row['path']).read_bytes()
        require(len(data) == row['size'] and sha(data) == row['sha256'], 'History dependency source changed')


def history_tracer_argv(stage):
    return ['{tool:python}', '-B', '{adapter}', '--trace-history', stage['argv'][2], '{out}/traces/' + stage['id'], *stage['argv'][3:]]


def history_launch_cwd(driver):
    require(driver['recipe'] == HISTORY_RECIPE, 'Unreviewed archive working directory')
    identifier(driver['external_input_id'])
    return '{archive:' + driver['external_input_id'] + '}'


def trace_history_driver(driver, trace, arguments):
    require(len(arguments) == 6 and arguments[::2] == ['--lean', '--mathlib', '--output'], 'Unreviewed history arguments')
    driver = no_symlinks(driver); root = driver.parent; history_source_check(root)
    require(Path.cwd().resolve() == root.resolve(), 'History wrapper must launch from its exact archive root')
    lean = no_symlinks(arguments[1]).resolve(); output = no_symlinks(arguments[5])
    require(sha(lean.read_bytes()) == LEAN_SHA and not output.exists() and output.name == 'original', 'Wrong compiler or reused history output')
    trace = no_symlinks(trace); require(not trace.exists(), 'Trace output must be absent'); trace.mkdir(parents=True)
    mappings = {'tool:lean': lean, 'tool:python': Path(sys.executable), 'archive:original': root, 'out': output.parent}
    specs = list(history_specs('original').values()); commands = [[_expand(a, mappings) for a in spec['argv']] for spec in specs]
    hashes = {argv[-1]: sha(history_claim_source(spec['id']) if spec['id'] in HISTORY_CLAIMS else path_in(root, spec['source_path']).read_bytes()) for spec, argv in zip(specs, commands)}
    old_run = subprocess.run; old_argv = sys.argv; old_path = sys.path[:]
    try:
        subprocess.run = trace_reviewed_commands(old_run, trace, commands, [[str(lean), '--version']], None,
                                                  capture_output=True, source_hashes=hashes, record_outputs=True)
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(root)
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        subprocess.run = old_run; sys.argv = old_argv; sys.path[:] = old_path
    return 0


def check_history_scenarios(value, source):
    keys(value, {'status', 'source', 'cases', 'scope'})
    require(value['status'] == 'PASS' and value['source'] == source and value['scope'] == 'bounded source correspondence corroboration only' and
            canonical(value['cases']) == canonical(HISTORY_CASES), 'Original history source scenarios changed')


def history_collect_children(stage, parent, text, plan, output, mappings):
    result = read_json(path_in(output, 'original/REPLAY_RECEIPT.json'))
    require(result['status'] == 'PASS_PORTABLE_SOURCE_REPLAY' and result['compiler_sha256'] == LEAN_SHA and
            result['mathlib_commit'] == 'c44e0c8ee63ca166450922a373c7409c5d26b00b' and result['claim_ceiling'] == HISTORY_CEILING, 'Original history terminal or scope changed')
    for key, expected in {'public_manifest_sha256': HISTORY_FILES['PUBLIC_MANIFEST.json'], 'original_to_public_sha256': HISTORY_FILES['ORIGINAL_TO_PUBLIC.json'],
        'source_archive_sha256': HISTORY_ORIGIN_SHA, 'scientific_candidate_snapshot_sha256': HISTORY_FILES[HISTORY_KERNEL + 'REVIEW_SNAPSHOT_V2.json'],
        'scientific_review_receipt_sha256': HISTORY_FILES[HISTORY_KERNEL + 'independent-review-v2/RECEIPT.json']}.items():
        require(result[key] == expected, 'Original history receipt source changed')
    require(result['mathlib_source_files_verified'] == 6816 and result['false_claim_rejections'] == result['accepted_source_scenarios'] == 7 and
            result['compiled_cache_used_read_only'] is True and result['independent_cache_rebuild_claimed'] is False and
            result['archive_executable_modes_required'] is False and result['shell_scripts_executed'] == [] and result['all_projected_inputs_unchanged'] is True, 'History census/trust boundary changed')
    version = result['compiler_version']; require('version 4.19.0' in version and '6caaee842e94' in version and
        path_in(output, 'original/logs/toolchain.log').read_text(encoding='utf-8') == version + '\n' + LEAN_SHA + '\n', 'Original compiler readback changed')
    require(text.splitlines() == HISTORY_TERMINAL + ['Receipt: ' + str(path_in(output, 'original/REPLAY_RECEIPT.json'))], 'History parent terminal changed')
    rows = indexed(result['compiled_stages'], 'stage'); negatives = indexed(read_json(path_in(output, 'original/controls/RESULTS.json')), 'control')
    require(list(rows) == [n for n, _, _ in HISTORY_PATHS] and list(negatives) == list(HISTORY_CLAIMS), 'Original history child census/order changed')
    trace = path_in(output, 'traces/' + stage['id'])
    require({p.name for p in trace.iterdir()} == {f'{i:04}.{suffix}' for i in range(17) for suffix in ('json', 'log', 'stdout.log', 'stderr.log')}, 'History captured child census differs')
    trace_hash = _file_hashes(trace); children = {}; objects = {}; seen = set(); driver = plan['drivers'][stage['driver_id']]
    for index, spec in enumerate(plan['history_children'].values()):
        name = spec['id']; negative = name in HISTORY_CLAIMS; scenario = name == 'source-replay'
        captured = read_json(trace / f'{index:04}.json')
        keys(captured, {'index', 'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'stdout_sha256', 'stderr_sha256', 'source_sha256', 'output_hashes'})
        require(captured['index'] == index and captured['cwd'] == _expand(history_launch_cwd(driver), mappings), 'History physical child launch changed')
        stdout = (trace / f'{index:04}.stdout.log').read_bytes(); stderr = (trace / f'{index:04}.stderr.log').read_bytes(); data = stdout + stderr
        require(sha(stdout) == captured['stdout_sha256'] and sha(stderr) == captured['stderr_sha256'] and data == (trace / f'{index:04}.log').read_bytes() and sha(data) == captured['log_sha256'], 'History captured streams changed')
        actual_argv = [_expand(a, mappings) for a in spec['argv']]
        check_child_terminal({**captured, 'source_child_id': name, 'parent_stage_id': stage['id']}, parent, name, actual_argv, seen, spec['exit_code'])
        owner = plan['contents'][spec['source_id']]; source = history_claim_source(name) if negative else owner
        require(captured['source_sha256'] == sha(source) and no_symlinks(actual_argv[-1]).read_bytes() == source, 'History physical source/claim changed')
        if scenario:
            require(path_in(output, 'original/logs/source-replay.json').read_bytes() == stdout and path_in(output, 'original/logs/source-replay.stderr').read_bytes() == stderr and not stderr, 'Original history scenario stream differs')
            row = read_json(path_in(output, 'original/logs/source-replay.json'))
            archive_key = next(k for k in mappings if k.startswith('archive:'))
            check_history_scenarios(row, str(Path(mappings[archive_key]) / HISTORY_DYNAMIC))
        else:
            require(path_in(output, spec['log']).read_bytes() == data, 'History original and captured log differ')
            row = negatives[name] if negative else rows[name]
            require(type(row['exit_code']) is int and row['exit_code'] == captured['exit_code'], 'Contradictory history child terminal')
            if negative:
                keys(row, {'control', 'exit_code', 'expected_false_claim_rejected'})
                require(row['expected_false_claim_rejected'] is True, 'Original history claim was not rejected')
                assess_stage({'expected_exit_codes': [1], 'kind': 'NEGATIVE_CONTROL', 'depends_on': [],
                              'expected_diagnostics': [{'literal': value} for value in HISTORY_DIAGNOSTICS]}, captured, data.decode(), {})
            else:
                keys(row, {'stage', 'exit_code', 'command'}); require(row['command'] == actual_argv and not re.search(rb'sorryAx|warning:|error:', data), 'Original history positive child changed')
                names = source_readback_names_in_plan(spec['source_id'], plan)
                if names: check_original_readbacks(data.decode(), names)
        hashes = {}
        if spec['output_path']:
            path = path_in(output, spec['output_path']); hashes[spec['output_path']] = sha(path.read_bytes())
            require(captured['output_hashes'] == {str(path): hashes[spec['output_path']]}, 'History object changed after producer child'); objects.update(hashes)
        else: require(captured['output_hashes'] == {}, 'Unexpected history check-only object')
        children[(stage['id'], name)] = {'source_child_id': name, 'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'],
            'parser_id': HISTORY_RECIPE, 'mode': 'NONEXECUTING_OBSERVATION', 'argv_provenance': 'CAPTURED', 'argv': spec['argv'], 'cwd': history_launch_cwd(driver),
            'started_at': captured['started_at'], 'ended_at': captured['ended_at'], 'physical_run_sha256': trace_hash, 'parent_log_sha256': parent['log_sha256'],
            'terminal': 'COMPLETED', 'exit_code': spec['exit_code'], 'actual_outcome': 'REJECT' if negative else 'ACCEPT', 'log_sha256': captured['log_sha256'],
            'source_id': spec['source_id'], 'source_sha256': sha(owner), 'generated_source_sha256': sha(source) if negative else None, 'log_assembly': 'STDOUT_THEN_STDERR',
            'output_hashes': hashes, 'result_record_sha256': canonical(row)}
    require({p.relative_to(output).as_posix() for p in path_in(output, 'original/build').rglob('*.olean')} == set(objects), 'History fresh object census differs')
    invocation = {'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'], 'source_argv': stage['argv'], 'launch_argv': history_tracer_argv(stage), 'launch_cwd': history_launch_cwd(driver),
                  'runner_sha256': sha(Path(__file__).read_bytes()), 'trace_sha256': trace_hash, 'parent_log_sha256': parent['log_sha256'], 'child_count': 17}
    return children, invocation, objects


def traced_run(original_run, trace, *, capture_output=False):
    """Capture actual subprocess.run calls without changing their return values."""
    count = 0
    def invoke(argv, *args, **kwargs):
        nonlocal count
        streams = (kwargs.get('capture_output') is True and 'stdout' not in kwargs and 'stderr' not in kwargs) if capture_output else (kwargs.get('stdout') == subprocess.PIPE and kwargs.get('stderr') == subprocess.STDOUT and 'capture_output' not in kwargs)
        require(isinstance(argv, list) and argv and not args and not kwargs.get('shell') and kwargs.get('text') is True and streams, 'Unreviewed traced subprocess form')
        index = count; count += 1
        record = {'index': index, 'argv': [str(a) for a in argv], 'cwd': str(Path(kwargs.get('cwd', Path.cwd())).absolute()),
                  'started_at': utc(), 'ended_at': None, 'terminal': 'RUNNING', 'exit_code': None, 'log_sha256': None}
        destination = path_in(trace, f'{index:04}.json'); require(not destination.exists(), 'Trace record already exists')
        write_json(destination, record)
        try:
            result = original_run(argv, **kwargs)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            data = getattr(error, 'stdout', None) or b''
            if isinstance(data, str): data = data.encode('utf-8')
            if capture_output:
                stderr = getattr(error, 'stderr', None) or b''
                if isinstance(stderr, str): stderr = stderr.encode('utf-8')
                path_in(trace, f'{index:04}.stdout.log').write_bytes(data); path_in(trace, f'{index:04}.stderr.log').write_bytes(stderr)
                record.update(stdout_sha256=sha(data), stderr_sha256=sha(stderr)); data += stderr
            log = path_in(trace, f'{index:04}.log'); log.write_bytes(data)
            record.update(ended_at=utc(), terminal='TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED',
                          log_sha256=sha(data))
            write_json(destination, record)
            raise
        require(isinstance(result.stdout, str), 'Traced subprocess omitted its captured stdout')
        data = result.stdout.encode('utf-8')
        if capture_output:
            require(isinstance(result.stderr, str), 'Traced subprocess omitted its captured stderr')
            stderr = result.stderr.encode('utf-8')
            path_in(trace, f'{index:04}.stdout.log').write_bytes(data); path_in(trace, f'{index:04}.stderr.log').write_bytes(stderr)
            record.update(stdout_sha256=sha(data), stderr_sha256=sha(stderr)); data += stderr
        log = path_in(trace, f'{index:04}.log'); log.write_bytes(data)
        completed = type(result.returncode) is int and 0 <= result.returncode < 124
        record.update(ended_at=utc(), terminal='COMPLETED' if completed else 'INTERRUPTED',
                      exit_code=result.returncode if completed else None, log_sha256=sha(log.read_bytes()))
        write_json(destination, record)
        return result
    return invoke


def trace_reviewed_commands(original_run, trace, commands, read_only_commands, seconds, *, working_directories=None, record_outputs=False, capture_output=False, source_hashes=None):
    """Only reviewed physical commands enter the child ledger, in source order."""
    capture = traced_run(original_run, trace, capture_output=capture_output); position = 0
    def invoke(argv, *args, **kwargs):
        nonlocal position
        require(isinstance(argv, list) and all(isinstance(a, str) for a in argv) and not args and not kwargs.get('shell'), 'Unreviewed original subprocess form')
        if argv in read_only_commands:
            valid = kwargs == {'capture_output': True, 'text': True, 'check': True} if capture_output else (set(kwargs) <= {'stdout', 'check', 'text', 'timeout'} and kwargs.get('timeout') is None and kwargs.get('stdout') == subprocess.PIPE and kwargs.get('check') is True)
            require(valid, 'Changed read-only original command')
            return original_run(argv, **kwargs)
        require(position < len(commands) and argv == commands[position], 'Unreviewed or repeated original physical command')
        allowed = {'env', 'text', 'timeout'} | ({'capture_output'} if capture_output else {'stdout', 'stderr'}) | ({'cwd'} if working_directories is not None else set())
        require(set(kwargs) <= allowed and kwargs.get('timeout') == seconds, 'Original child budget or subprocess contract changed')
        if working_directories is not None:
            require(kwargs.get('cwd') == working_directories[position], 'Original child working directory changed')
        if '-o' in argv: require(not no_symlinks(argv[argv.index('-o') + 1]).exists(), 'Original child output already exists')
        if source_hashes is not None:
            require(argv[-1] in source_hashes and sha(no_symlinks(argv[-1]).read_bytes()) == source_hashes[argv[-1]], 'Original physical child source changed')
        position += 1
        result = capture(argv, **kwargs)
        if record_outputs:
            record = path_in(trace, f'{position - 1:04}.json'); row = read_json(record); hashes = {}
            if '-o' in argv:
                path = no_symlinks(argv[argv.index('-o') + 1])
                if path.is_file(): hashes[str(path)] = sha(path.read_bytes())
            row['output_hashes'] = hashes; write_json(record, row)
        if source_hashes is not None:
            require(sha(no_symlinks(argv[-1]).read_bytes()) == source_hashes[argv[-1]], 'Original physical child source changed during execution')
            record = path_in(trace, f'{position - 1:04}.json'); row = read_json(record)
            row['source_sha256'] = source_hashes[argv[-1]]; write_json(record, row)
        return result
    return invoke


def check_custody_driver(source, contract):
    require(source['projection'] == 'CUSTODY_ONLY' and source['public_sha256'] is None, 'Archive-only driver source role changed')
    require(source['original_sha256'] == contract['driver_sha256'] and source['original_bytes'] == contract['driver_bytes'], 'Original driver bytes differ')
    require(isinstance(source['member_chain'], list) and source['member_chain'] and source['origin_archive_sha256'] == contract['archive_sha256'] and source['member_chain'][-1] ==
            (contract['root'] + '/' if contract['root'] else '') + contract['driver_path'], 'Original driver archive member differs')


def trace_resource_inconclusive(trace):
    for path in trace.glob('*.json'):
        row = read_json(path)
        if row['terminal'] in {'TIMEOUT', 'INTERRUPTED'}: return True
        log = path.with_suffix('.log')
        if log.is_file():
            data = no_symlinks(log).read_bytes(); require(sha(data) == row['log_sha256'], 'Captured resource log changed')
            if re.search(rb'\(deterministic\) timeout|maximum number of heartbeats|maximum recursion depth|WALL_CLOCK_LIMIT|out of memory', data, re.I): return True
    return False


def trace_t10_driver(driver, trace, arguments):
    require(sys.flags.optimize == 0, 'Original mutation driver requires assertions enabled')
    require(sha(no_symlinks(driver).read_bytes()) == T10_FINITE_RECIPES['t10-independent-mutations-v1'][1], 'Unapproved traced driver')
    for name in ('run_independent_review.py', 'independent_models.py'):
        require(sha(path_in(Path(driver).parent, name).read_bytes()) == T10_FILES[T10_REVIEW + '/' + name], 'Traced reviewer closure changed')
    require({p.name for p in Path(driver).parent.glob('*.py')} == {'run_independent_mutations.py', 'run_independent_review.py', 'independent_models.py'}, 'Unreviewed adjacent traced Python source')
    require(not path_in(Path(driver).parent, 'INDEPENDENT_MUTATION_RESULTS.json').exists(), 'Original mutation result must be absent')
    require(len(arguments) == 4 and arguments[0] == '--candidate' and arguments[2] == '--directory', 'Unreviewed traced driver arguments')
    for name in ('context_effects.py', 'read_cover.py'):
        require(sha(path_in(arguments[1], name).read_bytes()) == T10_FILES[T10_CHECKER + '/' + name], 'Traced candidate source changed')
    require(not no_symlinks(arguments[3]).exists(), 'Traced mutation directory must be absent')
    trace = no_symlinks(trace); require(not trace.exists(), 'Trace output must be absent'); trace.mkdir(parents=True)
    original_run = subprocess.run; old_argv = sys.argv; old_path = sys.path[:]
    try:
        subprocess.run = traced_run(original_run, trace)
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(Path(driver).parent)
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        subprocess.run = original_run; sys.argv = old_argv; sys.path[:] = old_path
    return 0


def core_source_order(root, plan=None):
    for name, expected in CORE_FILES.items():
        require(sha(path_in(root, name).read_bytes()) == expected, 'Original core helper/input bytes changed')
    require({p.relative_to(root).as_posix() for p in root.rglob('*.py')} == {'replay.py', 'verify_dependency_identity.py'}, 'Unreviewed core Python import closure')
    manifest = read_json(root / 'SOURCE_MANIFEST.json'); rows = manifest['sources']
    names = [relative(row['path']) for row in rows]
    require(len(names) == len(set(names)) and set(names) == {p.relative_to(root).as_posix() for p in root.rglob('*.lean')}, 'Original complete Lean archive census changed')
    for row in rows:
        data = path_in(root, row['path']).read_bytes()
        require(sha(data) == row['sha256'] and len(data) == row['bytes'], 'Original archived Lean source changed')
    if plan:
        for name, item in plan['file_paths'].items():
            require(path_in(root, name).read_bytes() == plan['contents'][item['source_id']], 'Archive/public source binding differs')
    by = {name.removeprefix('runtime/src/').removesuffix('.lean').replace('/', '.'): name for name in names if name.startswith('runtime/src/')}
    order = []; seen = set()
    def visit(name, trail):
        require(name not in trail, 'Original runtime import cycle')
        if name in seen: return
        for dependency in imports(path_in(root, by[name]).read_text(encoding='utf8')):
            if dependency in by: visit(dependency, trail | {name})
            else: require(dependency.startswith(('Mathlib', 'Lean', 'Std', 'Init')), 'Unexpected original import')
        order.append(name); seen.add(name)
    visit('ExactRuntimeCounterexample', set())
    require(len(order) == len(by) == 167, 'Original runtime closure is incomplete')
    return order


def core_expand(argument, mappings):
    return '--root=' + _expand(argument[7:], mappings) if argument.startswith('--root=') else _expand(argument, mappings)


def trace_core_runtime(driver, trace, arguments):
    require(sys.flags.optimize == 0, 'Original core driver requires assertions enabled')
    require(len(arguments) == 8 and arguments[::2] == ['--lean-bin', '--mathlib', '--out', '--mode'] and arguments[-1] == 'runtime', 'Unreviewed core trace arguments')
    driver = no_symlinks(driver); root = driver.parent; order = core_source_order(root)
    require(driver.name == 'replay.py', 'Wrong core driver location')
    lean = (no_symlinks(arguments[1]) / 'lean').resolve(); mathlib = no_symlinks(arguments[3]).resolve(); output = no_symlinks(arguments[5])
    require(sha(lean.read_bytes()) == LEAN_SHA and not output.exists(), 'Changed compiler or reused original output')
    trace = no_symlinks(trace); require(not trace.exists(), 'Trace output must be absent'); trace.mkdir(parents=True)
    mappings = {'tool:lean': lean, 'archive:core': root, 'out': output.parent}
    require(output.name == 'original', 'Changed original runtime output namespace')
    specs = [core_child_spec('runtime/' + name, '', 'runtime/src/' + name.replace('.', '/') + '.lean', 'core') for name in order]
    specs.append(core_child_spec('runtime/RuntimeReadback', '', 'readbacks/RuntimeReadback.lean', 'core'))
    commands = [[core_expand(arg, mappings) for arg in spec['argv']] for spec in specs]
    pins = read_json(root / 'DEPENDENCY_PINS.json')
    readonly = [[str(lean), '--version']]
    for package in pins['packages']:
        directory = mathlib if package['name'] == 'mathlib' else path_in(mathlib, '.lake/packages/' + package['name'])
        for tail in [['rev-parse', 'HEAD'], ['status', '--porcelain', '--untracked-files=all'], ['ls-files', '-z']]:
            readonly.append(['git', '-C', str(directory), *tail])
    old_run = subprocess.run; old_argv = sys.argv; old_path = sys.path[:]
    try:
        subprocess.run = trace_reviewed_commands(old_run, trace, commands, readonly, 180)
        sys.argv = [str(driver), *arguments]; sys.path[0] = str(root)
        runpy.run_path(str(driver), run_name='__main__')
    finally:
        subprocess.run = old_run; sys.argv = old_argv; sys.path[:] = old_path
    return 0


def check_child_terminal(row, parent, child, argv, seen, expected_code=1):
    identity = (parent['id'], child)
    require(row['parent_stage_id'] == parent['id'] and row['source_child_id'] == child and identity not in seen, 'Wrong/duplicate physical child identity')
    require(parent['terminal'] == 'COMPLETED' and parent['exit_code'] == 0, 'Contradictory parent/child completion')
    require(row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == expected_code, 'Child lacks its actual required exit')
    require(row['argv'] == argv, 'Actual child argument vector differs')
    require(all(isinstance(row[k], str) and row[k].endswith('Z') for k in ('started_at', 'ended_at')) and
            parent['started_at'] <= row['started_at'] <= row['ended_at'] <= parent['ended_at'], 'Unmeasured or contradictory child interval')
    digest(row['log_sha256']); seen.add(identity)


def t10_tracer_argv(stage):
    return ['{tool:python}', '-B', '{adapter}', '--trace-t10-mutations', stage['argv'][2],
            '{out}/traces/' + stage['id'], *stage['argv'][3:]]


def t10_child_argv(child):
    directory = '{out}/mutation-copies/' + child
    return ['{tool:python}', '{project}/' + T10_REVIEW + '/run_independent_review.py',
            '--candidate', directory, '--output', directory + '/unexpected-pass.json']


def t10_contents(plan, name):
    return plan['contents'][plan['file_paths'][name]['source_id']]


def t10_collect_children(stage, parent, text, plan, output, mappings):
    artifact_root = path_in(output, 'mutation-copies')
    require({p.name for p in artifact_root.iterdir()} == set(T10_CHILD_DIAGNOSTICS), 'Unexpected mutation output census')
    artifacts = {}
    for name in T10_CHILD_DIAGNOSTICS:
        directory = path_in(artifact_root, name)
        require({p.name for p in directory.iterdir()} == {'context_effects.py', 'read_cover.py', 'run.log'}, 'Missing child source/log or unexpected pass artifact')
        artifacts[name] = {p.name: no_symlinks(p).read_bytes() for p in directory.iterdir()}
    originals = {name: t10_contents(plan, T10_CHECKER + '/' + name) for name in ('context_effects.py', 'read_cover.py')}
    parsed = _t10_checked_mutation_children(path_in(output, 'project/' + T10_REVIEW + '/INDEPENDENT_MUTATION_RESULTS.json').read_bytes(),
        text.encode(), originals, artifacts, t10_contents(plan, T10_REVIEW + '/run_independent_mutations.py'),
        t10_contents(plan, T10_REVIEW + '/run_independent_review.py'))
    trace = path_in(output, 'traces/' + stage['id'])
    require({p.name for p in trace.iterdir()} == {f'{i:04}.{suffix}' for i in range(9) for suffix in ('json', 'log')}, 'Missing or extra actual child trace')
    trace_hash = _file_hashes(trace); seen = set(); children = {}
    driver = plan['drivers'][stage['driver_id']]
    for index, normalized in enumerate(parsed):
        name = normalized['source_child_id']; captured = read_json(trace / f'{index:04}.json')
        keys(captured, {'index', 'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256'})
        require(captured['index'] == index and captured['cwd'] == str(path_in(output / 'project', stage['cwd'], dot=True)), 'Actual child launch identity changed')
        actual_argv = [_expand(a, mappings) for a in t10_child_argv(name)]
        check_child_terminal({**captured, 'source_child_id': name, 'parent_stage_id': stage['id']}, parent, name, actual_argv, seen)
        require(captured['exit_code'] == normalized['exit_code'] and captured['log_sha256'] == normalized['log_sha256'] == sha((trace / f'{index:04}.log').read_bytes()), 'Contradictory captured and original child summaries')
        children[(stage['id'], name)] = {**normalized, 'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'],
            'parser_id': 't10-independent-mutations-v1', 'mode': 'NONEXECUTING_OBSERVATION', 'argv_provenance': 'CAPTURED',
            'argv': t10_child_argv(name), 'cwd': '{project}', 'started_at': captured['started_at'], 'ended_at': captured['ended_at'],
            'physical_run_sha256': trace_hash, 'parent_log_sha256': parent['log_sha256']}
    invocation = {'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'], 'source_argv': stage['argv'],
        'launch_argv': t10_tracer_argv(stage), 'runner_sha256': sha(Path(__file__).read_bytes()), 'trace_sha256': trace_hash,
        'parent_log_sha256': parent['log_sha256'], 'child_count': 9}
    return children, invocation


def check_core_child(spec, row, captured, parent, text, actual_argv):
    require(row['suite'] == 'runtime' and 'runtime/' + row['module'] == spec['id'], 'Wrong original runtime child identity')
    require(parent['terminal'] == captured['terminal'] == 'COMPLETED' and parent['exit_code'] == 0 and type(captured['exit_code']) is int and captured['exit_code'] == 0, 'Runtime child did not complete successfully')
    require(type(row['exit_code']) is int and row['exit_code'] == captured['exit_code'] and row['command'] == captured['argv'] == actual_argv, 'Original/captured child terminal or command contradicts')
    require(parent['started_at'] <= captured['started_at'] <= captured['ended_at'] <= parent['ended_at'], 'Runtime child interval is outside its parent')
    require(row['log_sha256'] == captured['log_sha256'] == sha(text.encode()) and row['has_resource_diagnostic'] is False, 'Original/captured runtime log differs or is inconclusive')
    require(not re.search(r'error:|\b(sorry|admit|timeout)\b|declaration uses|WALL_CLOCK_LIMIT|maximum number of heartbeats|maximum recursion depth', text, re.I), 'Runtime child is not a clean positive')
    require(type(row['elapsed_seconds']) in {int, float} and math.isfinite(row['elapsed_seconds']) and row['elapsed_seconds'] >= 0, 'Invalid original measured duration')


def check_attribution_child(spec, row, captured, text, source_sha256):
    require(row['name'] == spec['id'] and row['source'] == spec['source_path'] and row['source_sha256'] == source_sha256 and row['log'] == spec['log'].removeprefix('original/'), 'Wrong original attribution child/source')
    require(type(row['exit_code']) is int and row['exit_code'] == spec['exit_code'] == captured['exit_code'] and captured['terminal'] == 'COMPLETED' and captured['log_sha256'] == sha(text.encode()), 'Contradictory original/captured attribution child')
    negative = spec['id'] in ATTR_DIAGNOSTICS
    require(row['status'] == ('EXPECTED_REJECTION' if negative else 'PASS'), 'Wrong original attribution disposition')
    if negative:
        assess_stage({'expected_exit_codes': [1], 'kind': 'NEGATIVE_CONTROL', 'depends_on': [],
                      'expected_diagnostics': [{'literal': ATTR_DIAGNOSTICS[spec['id']]}]}, captured, text, {})
    else: require(not re.search(r'sorryAx|warning:|error:', text), 'Unclean original positive attribution child')


def attribution_collect_children(stage, parent, text, plan, output, mappings):
    result = read_json(path_in(output, 'original/REPLAY_RECEIPT.json'))
    require(result['status'] == 'PASS' and result['lean_sha256'] == LEAN_SHA and result['mathlib_revision'] == 'c44e0c8ee63ca166450922a373c7409c5d26b00b', 'Original attribution driver did not complete')
    require(result['public_manifest_sha256'] == ATTR_MANIFESTS['PUBLIC_MANIFEST.json'] and
            result['central_manifest_sha256'] == ATTR_MANIFESTS['sources/central-v1/MANIFEST.json'] and
            result['controls_manifest_sha256'] == ATTR_MANIFESTS['sources/controls-v1/MANIFEST.json'] and
            result['independent_acceptance_sha256'] == ATTR_MANIFESTS['review/REVIEW_RECEIPT.json'], 'Original attribution input identity changed')
    require(result['public_entries'] == 125 and result['external_source_files_verified'] == 7506 and
            result['fresh_build'] is True and result['custom_oleans_reused'] is False and result['external_compiled_cache_trusted'] is True and
            result['successful_stages'] == 18 and result['expected_rejected_mutants'] == 3 and result['central_theorems_axiom_audited'] == 50, 'Original attribution census/trust boundary changed')
    specs = list(plan['attribution_children'].values()); rows = result['steps']; trace = path_in(output, 'traces/' + stage['id'])
    require(len(rows) == 21 and [r['name'] for r in rows] == list(plan['attribution_children']), 'Original attribution child census changed')
    expected_lines = [('EXPECTED_REJECTION: ' if spec['exit_code'] else 'PASS: ') + spec['id'] for spec in specs]
    expected_lines += ['PASS: exact central targets, Regression, supplement, independent proofs, axiom audit, and three expected mutant diagnostics']
    require(text.splitlines() == expected_lines, 'Original attribution progress/terminal changed')
    require({p.name for p in trace.iterdir()} == {f'{i:04}.{suffix}' for i in range(21) for suffix in ('json', 'log')}, 'Original attribution trace census differs')
    trace_hash = _file_hashes(trace); children = {}; objects = {}; seen = set(); driver = plan['drivers'][stage['driver_id']]
    for index, (spec, row) in enumerate(zip(specs, rows)):
        captured = read_json(trace / f'{index:04}.json')
        keys(captured, {'index', 'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes'})
        require(captured['index'] == index and captured['cwd'] == _expand(spec['cwd'], mappings), 'Attribution child launch identity changed')
        log = path_in(output, spec['log']); data = log.read_bytes()
        require(data == (trace / f'{index:04}.log').read_bytes(), 'Original attribution log differs from captured bytes')
        check_child_terminal({**captured, 'source_child_id': spec['id'], 'parent_stage_id': stage['id']}, parent, spec['id'],
                             [_expand(a, mappings) for a in spec['argv']], seen, spec['exit_code'])
        source = plan['contents'][spec['source_id']]; check_attribution_child(spec, row, captured, data.decode(), sha(source))
        hashes = {}
        if spec['output_path']:
            path = path_in(output, spec['output_path']); hashes[spec['output_path']] = sha(path.read_bytes())
            require(captured['output_hashes'] == {str(path): hashes[spec['output_path']]}, 'Original object changed after its physical child'); objects.update(hashes)
        else: require(captured['output_hashes'] == {}, 'Unexpected output credited to check-only child')
        if not spec['exit_code']:
            names = source_readback_names_in_plan(spec['source_id'], plan)
            if names: check_original_readbacks(data.decode(), names)
            if spec['id'] == 'AxiomAudit': require(len(names) == 50, 'Original 50-theorem readback census changed')
        children[(stage['id'], spec['id'])] = {'source_child_id': spec['id'], 'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'],
            'parser_id': ATTR_RECIPE, 'mode': 'NONEXECUTING_OBSERVATION', 'argv_provenance': 'CAPTURED', 'argv': spec['argv'], 'cwd': spec['cwd'],
            'started_at': captured['started_at'], 'ended_at': captured['ended_at'], 'physical_run_sha256': trace_hash, 'parent_log_sha256': parent['log_sha256'],
            'terminal': 'COMPLETED', 'exit_code': spec['exit_code'], 'actual_outcome': 'REJECT' if spec['exit_code'] else 'ACCEPT',
            'log_sha256': captured['log_sha256'], 'source_id': spec['source_id'], 'source_sha256': sha(source), 'output_hashes': hashes, 'result_record_sha256': canonical(row)}
    require({p.relative_to(output).as_posix() for p in path_in(output, 'original/build').rglob('*.olean')} == set(objects), 'Attribution fresh object census differs')
    invocation = {'parent_stage_id': stage['id'], 'driver_sha256': driver['sha256'], 'source_argv': stage['argv'],
        'launch_argv': attribution_tracer_argv(stage), 'runner_sha256': sha(Path(__file__).read_bytes()), 'trace_sha256': trace_hash,
        'parent_log_sha256': parent['log_sha256'], 'child_count': 21}
    return children, invocation, objects


def core_collect_children(stage, parent, text, plan, output, mappings):
    original = path_in(output, 'original'); result = read_json(original / 'RESULT.json')
    require(result['status'] == 'COMPLETED_FRESH_REPLAY' and result['mode'] == 'runtime' and result['source_manifest_sha256'] == CORE_FILES['SOURCE_MANIFEST.json'], 'Original runtime driver did not complete its declared mode')
    require(result['official_dependency_cache_trusted'] is True and result['custom_objects_reused'] is False and result['heartbeat_flags_added'] is False and result['original_runtime_mutant_retried'] is False and result['historical_statuses_unchanged'] is True, 'Original runtime trust/freshness boundary changed')
    require(type(result['parallel_processes']) is int and result['parallel_processes'] == 1 and type(result['wall_clock_per_module_seconds']) is int and result['wall_clock_per_module_seconds'] == 180, 'Original runtime compiler concurrency/budget changed')
    require(result['runtime'] == {'status': 'FRESH_EXACT_CLOSURE_AND_AXIOM_READBACK_PASS', 'custom_modules': 167, 'axiom_readbacks': 13,
            'semantic_result': 'EXACT_MUTATED_UNIVERSAL_STATEMENT_FALSE_BY_POSITIVE_MEASURE_COUNTEREXAMPLE',
            'selector_kind': 'KERNEL_CERTIFIED_CLASSICAL_EXISTENTIAL_NOT_EVALUATED_NATIVE_NUMERALS'}, 'Original runtime result contract changed')
    identity = result['dependency_identity']; pins = json.loads(t10_contents(plan, 'DEPENDENCY_PINS.json'))['packages']
    require(identity['dependency_writes'] is False and identity['official_cache_objects_trusted'] is True, 'Original dependency boundary changed')
    deps = {'mathlib': identity['mathlib'], **{item['name']: item for item in identity['packages']}}
    require(set(deps) == {p['name'] for p in pins}, 'Original dependency identity census changed')
    for pin in pins:
        require(deps[pin['name']]['mode'] == 'CLEAN_EXACT_GIT' and deps[pin['name']]['revision'] == pin['revision'] and deps[pin['name']]['tracked_clean'] is True and deps[pin['name']]['unexpected_lean_sources'] is False, 'Original dependency check did not complete')
    specs = list(plan['core_children'].values()); rows = result['runs']; trace = path_in(output, 'traces/' + stage['id'])
    require(len(rows) == len(specs) == 168 and text.splitlines() == ['runtime ' + spec['id'].split('/', 1)[1] + ' 0' for spec in specs], 'Original runtime child/progress census differs')
    require({p.name for p in trace.iterdir()} == {f'{i:04}.{suffix}' for i in range(len(specs)) for suffix in ('json', 'log')}, 'Original runtime trace is incomplete or duplicated')
    trace_hash = _file_hashes(trace); children = {}; object_hashes = {}
    for index, (spec, row) in enumerate(zip(specs, rows)):
        captured = read_json(trace / f'{index:04}.json')
        keys(captured, {'index', 'argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256'})
        require(captured['index'] == index and captured['cwd'] == str(output / 'project'), 'Original child index/working directory changed')
        log = path_in(output, spec['log']); body = log.read_text(encoding='utf8')
        require(log.read_bytes() == (trace / f'{index:04}.log').read_bytes() and row['log'] == spec['log'].removeprefix('original/'), 'Original child log differs from its actual captured stdout')
        actual_argv = [core_expand(arg, mappings) for arg in spec['argv']]
        check_core_child(spec, row, captured, parent, body, actual_argv)
        digest_value = sha(plan['contents'][spec['source_id']]); require(row['source_sha256'] == digest_value, 'Original child source differs from selected source')
        hashes = {}
        if spec['output_path']:
            path = path_in(output, spec['output_path']); require(path.is_file(), 'Missing freshly emitted original object')
            hashes[spec['output_path']] = sha(path.read_bytes())
            require(row['object_sha256'] == hashes[spec['output_path']], 'Original object identity differs'); object_hashes.update(hashes)
        else:
            names = source_readback_names_in_plan(spec['source_id'], plan)
            require(len(names) == 13, 'Original runtime theorem readback census changed'); check_original_readbacks(body, names)
        children[(stage['id'], spec['id'])] = {'source_child_id': spec['id'], 'parent_stage_id': stage['id'],
            'driver_sha256': CORE_FILES['replay.py'], 'parser_id': CORE_RECIPE, 'mode': 'NONEXECUTING_OBSERVATION',
            'argv_provenance': 'CAPTURED', 'argv': spec['argv'], 'cwd': '{project}', 'started_at': captured['started_at'],
            'ended_at': captured['ended_at'], 'physical_run_sha256': trace_hash, 'parent_log_sha256': parent['log_sha256'],
            'terminal': 'COMPLETED', 'exit_code': 0, 'actual_outcome': 'ACCEPT', 'log_sha256': captured['log_sha256'],
            'source_id': spec['source_id'], 'source_sha256': digest_value, 'output_hashes': hashes, 'result_record_sha256': canonical(row)}
    require({p.relative_to(output).as_posix() for p in (original / 'runtime/build').rglob('*.olean')} == set(object_hashes), 'Fresh original object census differs')
    invocation = {'parent_stage_id': stage['id'], 'driver_sha256': CORE_FILES['replay.py'], 'source_argv': stage['argv'],
        'launch_argv': core_tracer_argv(stage), 'runner_sha256': sha(Path(__file__).read_bytes()), 'trace_sha256': trace_hash,
        'parent_log_sha256': parent['log_sha256'], 'child_count': 168}
    return children, invocation, object_hashes


def t10_result(stage, text, plan, output, suite):
    recipe = plan['drivers'][stage['driver_id']]['recipe']
    if stage['argv'][:1] == ['{builtin:observe-child}'] or recipe == 't10-independent-mutations-v1': return
    if recipe == 't10-unit-v1':
        tree = ast.parse(t10_contents(plan, T10_FINITE_RECIPES[recipe][0]))
        controls = [{'class': cls.name, 'name': node.name} for cls in tree.body if isinstance(cls, ast.ClassDef)
                    for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
        _t10_checked_unit_output(text.encode(), controls); return
    if recipe == 't10-independent-selftest-v1':
        require(text.strip() == 'independent reference self-tests: PASS', 'Original independent model self-test did not complete'); return
    value = _t10_load(text.encode())
    if stage['output_paths']:
        require(len(stage['output_paths']) == 1 and read_json(path_in(output, stage['output_paths'][0])) == value, 'Original stdout/result artifact differ')
    if recipe == 't10-exhaustive-v1':
        require(value['status'] == 'PASS' and value['runtime'] == suite['toolchain']['version'], 'Original exhaustive runtime/status changed')
        _t10_checked_count_map(value['counts'], T10_GROUPS['exhaustive'])
    elif recipe == 't10-source-release-v1':
        require(set(value) == {'source_fixture', 'release_fixture'} and all(v['status'] == 'PASS' for v in value.values()), 'Original source/release fixtures incomplete')
    elif recipe == 't10-semantic-v1':
        _t10_checked_semantic_assertions(text.encode(), T10_GROUPS['semantic'])
    elif recipe == 't10-independent-review-v1':
        require(value['status'] == 'PASS' and value['optimized'] is ('-O' in stage['argv']), 'Original independent mode/status changed')
        _t10_checked_count_map(value['counts'], T10_GROUPS['independent'])
        expected = {PurePosixPath(name).name: digest for name, digest in T10_FILES.items() if str(PurePosixPath(name).parent) == T10_CHECKER and name.endswith('.py')}
        require(value['candidate_hashes'] == expected and value['candidate'] == str(output / 'project' / T10_CHECKER), 'Original independent candidate binding changed')
        require(value['review_hashes'] == {name: T10_FILES[T10_REVIEW + '/' + name] for name in ('independent_models.py', 'run_independent_review.py')}, 'Original independent reviewer binding changed')
    elif recipe == 't10-two-card-v1':
        require(value['status'] == 'PASS' and type(value['check_count']) is int and value['check_count'] == 48 and
                value['worlds_full'] == 8 and value['worlds_star'] == 4 and set(value['checks']) == set(T10_GROUPS['two_card']), 'Original two-card finite census changed')
    else: raise ValueError('Missing source-specific written result parser')


def validate_suite(suite, sources, root):
    """Offline checks only. Neither a descriptor nor a review Boolean authorises code."""
    try:
        replay = suite['replay']; keys(replay, REPLAY_KEYS)
        require(replay['schema'] == 'orthemology-v5-replay-v1', 'Unknown replay schema')
        require(replay['scope'] in {'COMPONENTS', 'DECLARED_SUITE', 'FINITE'}, 'Unknown replay scope')
        if replay['scope'] == 'DECLARED_SUITE':
            require(APPROVED_DECLARED_SUITES.get(suite['id']) == declared_suite_fingerprint(suite, sources), 'Complete original suite recipe has not been approved')
        identifier(suite['id']); string_list(suite['source_ids'])
        require(suite['source_ids'], 'No suite sources')
        contents = {sid: public_bytes(root, sources[sid]) for sid in suite['source_ids']}
        files = indexed(replay['files'], 'source_id')
        require(set(files) == set(suite['source_ids']), 'Projection does not exactly cover suite sources')
        file_paths = {}; folded = set()
        for row in files.values():
            keys(row, {'source_id', 'path', 'role'}); name = relative(row['path'])
            require(row['role'] in ROLES, 'Unknown source role')
            require(name.casefold() not in folded, 'Projection path collision'); folded.add(name.casefold())
            require(Path(name).suffix.lower() not in {'.olean', '.ilean', '.o', '.so', '.dll', '.exe', '.a', '.zip', '.gz', '.pyc', '.pyo', '.pyd'}, 'Precompiled/archive payload is not a public source projection')
            file_paths[name] = row
        modules = indexed(replay['modules'], 'name'); official = indexed(replay['official_imports'], 'module')
        require(not (set(modules) & set(official)), 'Custom module shadows an official module')
        for row in official.values():
            keys(row, {'module', 'package', 'path', 'sha256'}); lean_name(row['module']); relative(row['path']); digest(row['sha256'])
            require(row['path'] == row['module'].replace('.', '/') + '.lean', 'Official module/path mismatch')
        module_sources = set()
        for name, row in modules.items():
            keys(row, {'name', 'source_id', 'imports'})
            sid = row['source_id']; require(sid in files and sid not in module_sources, 'Module source identity collision'); module_sources.add(sid)
            if files[sid]['role'] not in {'NEGATIVE', 'AUDIT'}: lean_name(name)
            require(files[sid]['path'].endswith(name.replace('.', '/') + '.lean'), 'Module/project path mismatch')
            require(files[sid]['role'] in {'PROOF', 'AUDIT', 'NEGATIVE', 'RUNTIME'}, 'Nonmodule source role')
            require(string_list(row['imports']) == imports(contents[sid].decode('utf-8')), 'Declared imports differ from source')
            require(set(row['imports']) <= set(modules) | set(official), 'Missing import dependency')
        order = string_list(replay['module_order']); require(set(order) <= set(modules), 'Unknown ordered module')
        for index, name in enumerate(order):
            lean_name(name)
            require(files[modules[name]['source_id']]['role'] != 'NEGATIVE', 'Negative module in build order')
            require(set(modules[name]['imports']) & set(modules) <= set(order[:index]), 'Module order is not dependency complete')
        for field, role in [('positive_roots', 'PROOF'), ('audit_roots', 'AUDIT'), ('negative_roots', 'NEGATIVE'), ('runtime_roots', 'RUNTIME')]:
            for name in string_list(replay[field]):
                require(name in modules and files[modules[name]['source_id']]['role'] == role, 'Root role mismatch')
        negatives = {name for name, row in modules.items() if files[row['source_id']]['role'] == 'NEGATIVE'}
        require(negatives == set(replay['negative_roots']), 'Negative fixture inventory is incomplete')
        visited = set()
        def visit(name, trail):
            require(name not in trail, 'Import cycle')
            require(name not in negatives, 'Negative fixture reaches an accepted import closure')
            if name in visited: return
            if name in modules:
                for dep in modules[name]['imports']: visit(dep, trail | {name})
            visited.add(name)
        for name in replay['positive_roots'] + replay['audit_roots']: visit(name, set())
        targets = indexed(suite['targets']); names = indexed(replay['target_names'], 'target_id')
        require(set(names) <= set(targets), 'Foreign target name')
        if replay['scope'] != 'FINITE': require(set(names) == set(targets) and names, 'Formal target coverage is incomplete')
        for tid, row in names.items():
            keys(row, {'target_id', 'module', 'name'}); lean_name(row['name'])
            require(row['module'] in order and modules[row['module']]['source_id'] == targets[tid]['source_id'], 'Target module/source not freshly built')
            require(files[targets[tid]['source_id']]['role'] != 'NEGATIVE', 'Negative proof is an accepted target')
        toolchain = suite['toolchain']
        require(toolchain['kind'] in {'LEAN', 'PYTHON', 'REFERENCE'}, 'Unknown primary tool kind')
        digest(toolchain['executable_sha256'])
        if toolchain['kind'] == 'LEAN':
            require(toolchain['version'] == '4.19.0', 'Wrong Lean version')
            if toolchain['platform'] == 'linux-x86_64': require(toolchain['executable_sha256'] == LEAN_SHA, 'Wrong official compiler digest')
        packages = indexed(replay['packages'], 'name'); pins = indexed(toolchain['packages'], 'name')
        require(set(packages) == set(pins), 'Package pins/closure differ')
        for name, row in packages.items():
            keys(row, {'name', 'kind', 'path', 'manifest_source_id'})
            require(row['kind'] in {'GIT', 'PYTHON_DISTRIBUTION'}, 'Unknown package kind'); relative(row['path'], dot=True)
            require(row['manifest_source_id'] in contents, 'Missing package manifest source')
            pin = pins[name]; keys(pin, {'name', 'revision', 'sha256'})
            require(pin['sha256'] == canonical({'name': name, 'revision': pin['revision']}), 'Wrong package fingerprint')
            require(_manifest_pins(contents[row['manifest_source_id']]).get(name) == pin['revision'], 'Package pin differs from its source manifest')
            if row['kind'] == 'GIT': require(re.fullmatch('[0-9a-f]{40}', pin['revision']), 'Malformed Git pin')
        require((replay['package_manifest_source_id'] is None and not packages) or replay['package_manifest_source_id'] in contents, 'Missing source-specific package lock')
        require(all(row['package'] == 'lean-release' or row['package'] in packages for row in official.values()), 'Undeclared official package')
        extra_tools = indexed(replay['tools'], 'name')
        require(('lean' if toolchain['kind'] == 'LEAN' else 'python') not in extra_tools, 'Extra tool replaces primary tool')
        for row in extra_tools.values():
            keys(row, {'name', 'kind', 'version', 'executable_sha256', 'platform', 'path_kind'})
            require(row['kind'] in {'LEAN', 'PYTHON', 'NATIVE_COMPILER'}, 'Forbidden tool kind')
            require(row['path_kind'] in {'EXECUTABLE', 'BIN_DIRECTORY', 'DISTRIBUTION_ROOT'}, 'Unknown tool argument meaning'); digest(row['executable_sha256'])
        inputs = indexed(replay['external_inputs']); input_manifests = {}
        for iid, row in inputs.items():
            keys(row, {'id', 'source_id', 'kind', 'manifest_source_id', 'manifest_key', 'expected_sha256', 'expected_bytes', 'role'})
            require(row['kind'] in {'FILE', 'TREE'} and row['role'] == 'INPUT', 'Unknown external input kind/role')
            manifest = None
            if row['manifest_source_id'] is not None:
                require(row['manifest_source_id'] in contents, 'Missing input manifest source')
                manifest = _json_pointer(json.loads(contents[row['manifest_source_id']]), row['manifest_key'])
                input_manifests[iid] = manifest
            if row['kind'] == 'TREE':
                require(row['source_id'] is None and row['expected_sha256'] is None and row['expected_bytes'] is None and isinstance(manifest, list), 'Bad selected-tree contract')
                seen = set()
                for item in manifest:
                    name = relative(item['path']); require(name not in seen, 'Duplicate locked input path'); seen.add(name)
                    digest(item['sha256']); require(type(item['bytes']) is int and item['bytes'] >= 0, 'Bad locked input length')
            else:
                digest(row['expected_sha256']); require(type(row['expected_bytes']) is int and row['expected_bytes'] >= 0, 'Bad external file length')
                owner = sources.get(row['source_id']) if row['source_id'] else manifest
                require(isinstance(owner, dict), 'External file has no exact identity owner')
                require(row['expected_sha256'] == owner.get('original_sha256', owner.get('sha256')) and row['expected_bytes'] == owner.get('original_bytes', owner.get('bytes')), 'External identity differs from manifest/source')
        fixtures = indexed(replay['fixtures'])
        for row in fixtures.values():
            keys(row, {'id', 'input_id', 'operation', 'path'})
            require(row['input_id'] in inputs, 'Fixture has no positive input')
            require(row['operation'] in {'ABSENT', 'NON_DIRECTORY', 'OMIT', 'APPEND_CHANGED_BYTES'}, 'Unapproved fixture transformation')
            if inputs[row['input_id']]['kind'] == 'FILE':
                require(row['operation'] in {'ABSENT', 'APPEND_CHANGED_BYTES'} and row['path'] is None, 'Unsupported file fixture operation')
            elif row['operation'] in {'ABSENT', 'NON_DIRECTORY'}: require(row['path'] is None, 'Unexpected fixture path')
            else: require(row['path'] in {p['path'] for p in input_manifests.get(row['input_id'], [])}, 'Fixture changes an unlocked path')
        drivers = indexed(replay['drivers'])
        for row in drivers.values():
            keys(row, {'id', 'source_id', 'recipe', 'sha256', 'argument_meanings', 'external_input_id'})
            source = sources[row['source_id']]; digest(row['sha256'])
            require(row['sha256'] == (source['public_sha256'] or source['original_sha256']), 'Wrong driver hash')
            if row['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE}:
                require(row['external_input_id'] in inputs, 'Original core archive is undeclared')
            else: require(row['external_input_id'] is None, 'Archive recipe is not approved by this adapter version')
            admitted_role = 'LOCK' if row['recipe'] == 't15-empirical-integrity-v1' else 'DRIVER'
            if row['recipe'] == ATTR_RECIPE: check_custody_driver(source, ATTR_CONTRACT)
            elif row['recipe'] == HISTORY_RECIPE: check_custody_driver(source, HISTORY_CONTRACT)
            else: require(row['source_id'] in contents and files[row['source_id']]['role'] == admitted_role, 'Driver is not an exact projected source')
            if row['recipe'] in LANGUAGE_RECIPES:
                recipe = LANGUAGE_RECIPES[row['recipe']]
                require(row['sha256'] == recipe['sha256'] and row['argument_meanings'] == {'source_dir': 'INPUT_TREE'}, 'Wrong approved language recipe')
                adjacent = str(PurePosixPath(files[row['source_id']]['path']).with_name(recipe['lock_name']))
                require(adjacent in file_paths and sha(contents[file_paths[adjacent]['source_id']]) == recipe['lock'], 'Changed adjacent driver lock')
            elif row['recipe'] in EMPIRICAL_RECIPES:
                require(EMPIRICAL_RECIPES[row['recipe']] == row['sha256'], 'Changed original empirical driver')
                meanings = {} if row['recipe'] in {'t15-empirical-integrity-v1', 't15-empirical-tests-v1'} else {'--decisions-zip': 'INPUT_FILE', '--summary-xlsx': 'INPUT_FILE'}
                if row['recipe'] == 't15-empirical-reanalyse-v1': meanings['--output'] = 'FRESH_OUTPUT_FILE'
                require(row['argument_meanings'] == meanings, 'Changed empirical argument meaning')
            elif row['recipe'] in T15_SOURCE_RECIPES:
                validate_t15_driver(row, {'files': files, 'file_paths': file_paths, 'contents': contents})
            elif row['recipe'] in NORMAL_SOURCE_RECIPES:
                require(NORMAL_SOURCE_RECIPES[row['recipe']] == row['sha256'] and row['argument_meanings'] == {}, 'Changed original source-check recipe')
            elif row['recipe'] == CORE_RECIPE:
                require(row['sha256'] == CORE_FILES['replay.py'] and row['argument_meanings'] ==
                        {'--lean-bin': 'LEAN_BIN_DIRECTORY', '--mathlib': 'MATHLIB_ROOT', '--out': 'OUTPUT_DIRECTORY', '--mode': 'LITERAL'}, 'Changed original core recipe')
            elif row['recipe'] == ATTR_RECIPE:
                require(row['sha256'] == ATTR_CONTRACT['driver_sha256'] and row['argument_meanings'] ==
                        {'--lean': 'LEAN_EXECUTABLE', '--mathlib': 'MATHLIB_ROOT', '--output': 'FRESH_OUTPUT_DIRECTORY'}, 'Changed original attribution recipe')
            elif row['recipe'] == HISTORY_RECIPE:
                require(row['sha256'] == HISTORY_CONTRACT['driver_sha256'] and row['argument_meanings'] ==
                        {'--lean': 'LEAN_EXECUTABLE', '--mathlib': 'MATHLIB_ROOT', '--output': 'FRESH_OUTPUT_DIRECTORY'}, 'Changed original history recipe')
            elif row['recipe'] in T10_FINITE_RECIPES:
                expected_path, expected_hash = T10_FINITE_RECIPES[row['recipe']]
                require(row['sha256'] == expected_hash and files[row['source_id']]['path'] == expected_path, 'Changed original written finite recipe')
                meaning = {'--candidate': 'PROJECT_SOURCE_DIRECTORY', '--output': 'FRESH_OUTPUT_FILE'} if row['recipe'] == 't10-independent-review-v1' else {}
                if row['recipe'] == 't10-independent-mutations-v1': meaning = {'--candidate': 'PROJECT_SOURCE_DIRECTORY', '--directory': 'FRESH_OUTPUT_DIRECTORY'}
                require(row['argument_meanings'] == meaning, 'Changed written finite argument meaning')
            else:
                require(SOURCE_RECIPES.get(row['recipe']) == row['sha256'], 'Unknown/unreviewed driver recipe')
        stages = indexed(replay['stages']); require(stages and not (set(stages) & RESERVED), 'Missing stages or reserved stage ID')
        controls = indexed(suite['controls']); covered = []; produced = set(); prior = []
        plan = {'files': files, 'file_paths': file_paths, 'contents': contents, 'modules': modules, 'official': official,
                'drivers': drivers, 'inputs': inputs, 'input_manifests': input_manifests, 'fixtures': fixtures,
                'stages': stages, 'targets': names, 'packages': packages, 'build_roots': string_list(replay['build_roots'])}
        for name in plan['build_roots']:
            relative(name); require(name != 'project' and not name.startswith('project/'), 'Build root overlaps projected sources')
        for driver in drivers.values():
            if driver['recipe'] in NORMAL_SOURCE_RECIPES: source_checker_inputs(driver, plan)
            if driver['recipe'] == 't14-identity-verify_sources-v1': check_checksum_manifest(plan, 90)
        if any(row['recipe'] in T15_SOURCE_RECIPES for row in drivers.values()): validate_t15_package(suite, plan)
        if any(row['recipe'] in T10_FINITE_RECIPES for row in drivers.values()): validate_t10_package(suite, plan)
        if any(row['recipe'] == CORE_RECIPE for row in drivers.values()): validate_core_package(suite, plan)
        if any(row['recipe'] == ATTR_RECIPE for row in drivers.values()): validate_attribution_package(suite, plan)
        if any(row['recipe'] == HISTORY_RECIPE for row in drivers.values()): validate_history_package(suite, plan)
        if any(row['recipe'] in EMPIRICAL_RECIPES for row in drivers.values()):
            _empirical_package(plan)
            require(replay['scope'] == 'FINITE' and toolchain['kind'] == 'PYTHON' and toolchain['version'].startswith('3.12.'), 'Empirical execution is source-prescribed Python 3.12 finite scope')
            requirements_id = file_paths['requirements.txt']['source_id']
            required_packages = _manifest_pins(contents[requirements_id])
            require({name: pin['revision'] for name, pin in pins.items()} == required_packages and len(required_packages) == 4,
                    'Empirical runtime must check every original pinned distribution')
            require(all(row['kind'] == 'PYTHON_DISTRIBUTION' and row['manifest_source_id'] == requirements_id for row in packages.values()), 'Empirical dependency manifest/type changed')
            require({row['recipe'] for row in drivers.values()} == set(EMPIRICAL_RECIPES), 'Incomplete original empirical driver inventory')
            require([drivers[stage['driver_id']]['recipe'] for stage in stages.values()] ==
                    ['t15-empirical-integrity-v1', 't15-empirical-tests-v1', 't15-empirical-reanalyse-v1', 't15-empirical-validate-v1', 't15-empirical-reanalyse-v1'], 'Original empirical stage inventory/order changed')
        for sid, stage in stages.items():
            keys(stage, STAGE_KEYS); require(stage['kind'] in KINDS, 'Unknown stage kind')
            relative(stage['cwd'], dot=True)
            require(type(stage['timeout_seconds']) is int and 0 < stage['timeout_seconds'] <= 86400, 'Invalid stage budget')
            require(set(string_list(stage['depends_on'])) <= set(prior), 'Nonexistent/forward stage prerequisite')
            for output in string_list(stage['output_paths']):
                relative(output)
                recipe = drivers.get(stage['driver_id'], {}).get('recipe')
                admitted_child = (output in T10_OUTPUTS.get(recipe, []) and output.removeprefix('project/') not in file_paths) or (output == T15_EXPORT_OUTPUT and t15_export_stage(stage, plan))
                require(output not in produced and (not output.startswith('project/') or admitted_child), 'Output collision or source overwrite'); produced.add(output)
            codes = stage['expected_exit_codes']
            require(isinstance(codes, list) and codes and len(codes) == len(set(codes)) and all(type(c) is int and 0 <= c < 124 for c in codes), 'Nonsemantic/invalid expected exit code')
            for diagnostic in stage['expected_diagnostics']:
                keys(diagnostic, {'source_id', 'literal', 'sha256'})
                require(isinstance(diagnostic['literal'], str) and diagnostic['literal'] and diagnostic['sha256'] == sha(diagnostic['literal'].encode()), 'Malformed source diagnostic')
                driver = drivers.get(stage['driver_id'], {})
                custody_literal = driver.get('recipe') == ATTR_RECIPE and diagnostic['source_id'] == driver['source_id'] and diagnostic['literal'] in ATTR_DIAGNOSTICS.values()
                custody_literal = custody_literal or (driver.get('recipe') == HISTORY_RECIPE and diagnostic['source_id'] == driver['source_id'] and diagnostic['literal'] in HISTORY_DIAGNOSTICS)
                require(custody_literal or (diagnostic['source_id'] in contents and diagnostic['literal'].encode() in contents[diagnostic['source_id']]), 'Diagnostic differs from source contract')
            for cid in string_list(stage['control_ids']):
                require(cid in controls and cid not in covered, 'Missing/duplicate control association'); covered.append(cid)
                expected = controls[cid]
                require(expected['expected_outcome'] == ('REJECT' if expected['role'] == 'MUTATION_REJECTION' else 'ACCEPT'), 'Control role substitution')
                if expected['expected_outcome'] == 'REJECT':
                    require(stage['kind'] == 'NEGATIVE_CONTROL' and 0 not in codes and stage['expected_diagnostics'], 'Missing intended-rejection contract')
                    require(any(stages[p]['expected_exit_codes'] == [0] and stages[p]['kind'] != 'NEGATIVE_CONTROL' for p in stage['depends_on']), 'Negative control lacks positive infrastructure prerequisite')
                else: require(codes == [0], 'Positive control permits failure')
            _validate_argv(stage, plan); prior.append(sid)
        require(set(covered) == set(controls), 'Declared control omitted from replay')
        for name in string_list(replay['build_roots']): relative(name)
        if names: require(replay['build_roots'] and {'Lean.Elab.Command', 'Lean.Util.CollectAxioms'} <= set(official), 'Missing target audit imports/build root')
        return plan
    except (KeyError, TypeError, UnicodeError, OSError, AttributeError) as exc:
        raise ValueError('Malformed or unavailable replay source/descriptor: ' + str(exc)) from exc


def closure_fingerprint(suite, sources):
    return canonical({'suite_id': suite['id'], 'sources': {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']},
                      'toolchain': suite['toolchain'], 'replay': suite['replay']})


def import_fingerprints(suite, sources):
    return {row['name']: canonical({'source': sources[row['source_id']]['public_sha256'],
            'imports': row['imports'], 'toolchain': suite['toolchain']}) for row in suite['replay']['modules']}


def project_suite(suite, sources, root, output):
    plan = validate_suite(suite, sources, root)
    output = no_symlinks(output).absolute()
    require(not output.exists(), 'Output must be absent; retain prior evidence')
    require(not output.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside repository')
    output.mkdir(parents=True, exist_ok=False)
    project = output / 'project'; project.mkdir()
    for row in plan['files'].values():
        destination = path_in(project, row['path']); destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(plan['contents'][row['source_id']])
    write_json(output / 'PLAN.json', {'suite_id': suite['id'], 'suite_sha256': canonical(suite), 'replay': suite['replay'],
                                    'closure_sha256': closure_fingerprint(suite, sources)})
    return {'project': str(project), 'output': str(output)}


def run_process(argv, cwd, env, log, timeout):
    """Retain real child terminals; a process group timeout is not a rejection."""
    started = utc(); log = Path(log); log.parent.mkdir(parents=True, exist_ok=True)
    with log.open('xb') as stream:
        kwargs = {'start_new_session': True} if os.name != 'nt' else {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
        proc = subprocess.Popen([str(a) for a in argv], cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, shell=False, **kwargs)
        try:
            code = proc.wait(timeout=timeout)
            terminal = 'COMPLETED' if 0 <= code < 124 else 'INTERRUPTED'
            if terminal != 'COMPLETED': code = None
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            terminal = 'TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED'; code = None
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            else: os.killpg(proc.pid, signal.SIGTERM)
            try: proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                if os.name == 'nt': proc.kill()
                else: os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    return {'terminal': terminal, 'exit_code': code, 'started_at': started, 'ended_at': utc(), 'log_sha256': sha(log.read_bytes())}


def assess_stage(stage, result, text, completed):
    require(result['terminal'] == 'COMPLETED' and type(result['exit_code']) is int and result['exit_code'] in stage['expected_exit_codes'], 'Stage lacks its exact expected terminal')
    for parent in stage['depends_on']:
        require(parent in completed and completed[parent].get('matched') is True and completed[parent]['terminal'] == 'COMPLETED', 'Stage positive/dependency prerequisite did not complete')
    remainder = text
    for row in stage['expected_diagnostics']:
        require(row['literal'] in text, 'Intended diagnostic absent')
        remainder = remainder.replace(row['literal'], '')
    if stage['kind'] == 'NEGATIVE_CONTROL':
        require(result['exit_code'] > 0 and stage['expected_diagnostics'], 'Negative result has no concrete rejection')
        require(not re.search(r'unknown module|unknown constant|unknown identifier|no such file|file not found|failed to read file|object file|timed out|out of memory|maximum (?:recursion|heartbeats)|deterministic timeout', remainder, re.I), 'Infrastructure/resource failure is not intended rejection')
    return True


def parse_readbacks(text, targets):
    result = {}
    for row in targets:
        name = row['name']; start = 'V5_BEGIN ' + name; end = 'V5_END ' + name
        starts = list(re.finditer(r'(?m)^' + re.escape(start) + r'\r?$', text))
        ends = list(re.finditer(r'(?m)^' + re.escape(end) + r'\r?$', text))
        require(len(starts) == len(ends) == 1 and starts[0].end() < ends[0].start(), 'Missing/duplicate target readback')
        block = text[starts[0].end():ends[0].start()].lstrip('\r\n')
        axiom_rows = re.findall(r"'" + re.escape(name) + r"' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])", block)
        require(len(axiom_rows) == 1, 'Missing/duplicate exact axiom readback')
        axes = sorted(x.strip() for x in axiom_rows[0][1].split(',') if x.strip())
        require(set(axes) <= AXIOMS, 'Unapproved axiom in checked target')
        owner = re.findall(r'V5_OWNER ' + re.escape(name) + r' (\S+)', block)
        require(owner == [row['module']], 'Readback target belongs to another source module')
        safe = re.findall(r'V5_SAFE ' + re.escape(name) + r' ([0-9]+) \[([^\]]*)\]', block)
        require(len(safe) == 1 and int(safe[0][0]) > 0, 'Incomplete proof closure traversal')
        closure_axes = {a.strip() for a in safe[0][1].split(',') if a.strip()}
        require(closure_axes <= AXIOMS and set(axes) <= closure_axes, 'Invalid closure axiom footprint')
        type_text = block.split("'" + name + "'", 1)[0].strip()
        require(re.match(r'^@?' + re.escape(name) + r'(?:\.\{[^}]*\})?\s*:', type_text), 'Missing exact target type')
        result[row['target_id']] = {'name': name, 'type_sha256': sha(type_text.encode()), 'axioms': sorted(closure_axes),
                                    'closure_status': 'CHECKED_SAFE', 'checked_declarations': int(safe[0][0])}
    return result


class MissingTool(FileNotFoundError):
    pass


class MissingInput(FileNotFoundError):
    pass


def package_library(name, library, official):
    if library.is_dir(): return [library]
    if any(row['package'] == name for row in official.values()):
        raise MissingTool('Required imported package cache is unavailable: ' + name)
    # Cli is a pinned Lake/tool dependency without a proof-library cache.
    # Its Git revision and clean tree are still checked by the caller.
    return []


def _clean_environment():
    return {key: value for key, value in os.environ.items()
            if not key.startswith(('LEAN_', 'PYTHON')) and key not in {'LD_PRELOAD', 'DYLD_INSERT_LIBRARIES'}}


def stage_environment(stage, plan, output, env):
    """Only declared fresh prerequisites may precede the canonical custom roots."""
    preferred = []
    rows = [stage] + [plan['stages'][name] for name in stage['depends_on']]
    for row in rows:
        for name in row['output_paths']:
            if not name.endswith('.olean'): continue
            for root in plan['build_roots']:
                if name.startswith(root + '/'):
                    preferred.append(str(path_in(output, root)))
    result = dict(env)
    if preferred:
        result['LEAN_PATH'] = os.pathsep.join(dict.fromkeys(preferred + env.get('LEAN_PATH', '').split(os.pathsep)))
    return result


def source_checker_inputs(driver, plan):
    """Prevalidate producer manifest paths before executing the exact checker."""
    driver_path = plan['files'][driver['source_id']]['path']
    require(not any(name.startswith('scripts/') and name.endswith('.py') and name != driver_path
                    for name in plan['file_paths']), 'Unreviewed adjacent Python import source')
    def data(name):
        require(name in plan['file_paths'], 'Original source checker input is absent')
        return plan['contents'][plan['file_paths'][name]['source_id']]
    def check(rows, field):
        require(isinstance(rows, list) and rows, 'Original source inventory is absent')
        seen = set()
        for row in rows:
            name = relative(row[field]); require(name not in seen, 'Duplicate original source path'); seen.add(name)
            value = data(name)
            require(type(row['bytes']) is int and len(value) == row['bytes'] and sha(value) == row['sha256'], 'Original source-check input changed')
    if driver['recipe'] == 't11-substitution-source-check-v1':
        require(plan['files'][driver['source_id']]['path'] == 'scripts/verify-inputs.py', 'Original checker location changed')
        raw = data('INPUT_SOURCE_MANIFEST.json'); inputs = json.loads(raw)
        candidate = json.loads(data('CANDIDATE_v1.json'))
        require(sha(raw) == candidate['input_manifest_sha256'], 'Original input manifest changed')
        check(inputs, 'local_path'); check(candidate['modules'], 'path')
        review = json.loads(data('review/VERIFICATION.json'))
        require(sha(data('review/sources/IndependentControls.lean')) == review['independent_controls_sha256'], 'Original independent control bytes changed')
    elif driver['recipe'] == 't11-normalization-source-check-v1':
        require(plan['files'][driver['source_id']]['path'] == 'scripts/verify-sources.py', 'Original checker location changed')
        check(json.loads(data('SOURCE_IDENTITIES.json'))['sources'], 'path')
        check(json.loads(data('ACCEPTED_INPUTS.json'))['sources'], 'path')
        for name in data('dependency-order.txt').decode().splitlines(): lean_name(name)
    elif driver['recipe'] == 't14-identity-verify_sources-v1':
        require(driver_path == 'verification/verify_sources.py', 'Original checker location changed')
        for name in plan['file_paths']:
            if name.startswith('verification/') and name.endswith('.py') and name != driver_path:
                require(name == 'verification/check_negative_controls.py' and
                        sha(data(name)) == '1cb604255f2dbee1ba0281a5deb405a17474da143d766278b5fd472ecb02335c', 'Unreviewed adjacent Python import source')
        lock = json.loads(data('verification/source-lock.json')); seen = set()
        for group, count in [('baseline', 53), ('intensional', 6), ('extensional', 6)]:
            require(isinstance(lock[group], list) and len(lock[group]) == count, 'Original source group census changed')
            for row in lock[group]:
                keys(row, {'file', 'sha256'} if group == 'baseline' else {'file', 'sha256', 'bytes'}); name = relative(row['file'])
                require('/' not in name and name.endswith('.lean') and name not in seen, 'Invalid original root source path')
                seen.add(name); require(sha(data(name)) == row['sha256'], 'Original source-check input changed')
                if group != 'baseline': require(type(row['bytes']) is int and len(data(name)) == row['bytes'], 'Original source byte count changed')
        require(seen == {name for name in plan['file_paths'] if '/' not in name and name.endswith('.lean') and name != 'lakefile.lean'}, 'Original root inventory changed')
        for name in ['lakefile.lean', 'lake-manifest.json', 'lean-toolchain']: data(name)
    else: raise ValueError('Unapproved normal source checker')


def check_checksum_manifest(plan, expected_count):
    require('SHA256SUMS' in plan['file_paths'], 'Missing original package checksum manifest')
    raw = plan['contents'][plan['file_paths']['SHA256SUMS']['source_id']].decode()
    seen = set()
    for line in raw.splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Malformed original checksum row')
        name = relative(match.group(2)); require(name not in seen and name in plan['file_paths'], 'Missing or duplicate original checksum path')
        seen.add(name)
        require(sha(plan['contents'][plan['file_paths'][name]['source_id']]) == match.group(1), 'Original package checksum mismatch')
    require(len(seen) == expected_count and set(plan['file_paths']) == seen | {'SHA256SUMS'}, 'Original package checksum inventory changed')


def check_t14_stage(stage, text, plan):
    """Read the exact T14 source-owned checks without inventing audit counts."""
    path = stage['argv'][-1].removeprefix('{project}/')
    def match(pattern):
        rows = re.findall('^' + pattern + '$', text, re.M)
        require(len(rows) == 1, 'Original T14 audit terminal is absent or duplicated')
        return rows[0]
    def axioms(rows):
        require(rows and len({row[0] for row in rows}) == len(rows), 'Original T14 declaration census is absent or duplicated')
        for name, raw in rows:
            require(name.startswith('P01AC.'), 'Unexpected T14 declaration owner')
            require({x.strip() for x in raw.split(',') if x.strip()} <= AXIOMS, 'Unapproved original T14 axiom')
    if stage['kind'] == 'SOURCE_CHECK':
        require(text.strip() == 'SOURCE_AUDIT_PASS: 53 unchanged baseline + 6 frozen intensional + 6 frozen extensional modules; all 65 registered; exact retained grammars; 9 official Git pins; no forbidden proof tokens.', 'Original T14 source audit did not complete')
    elif stage['kind'] == 'NEGATIVE_CONTROL':
        errors = [line for line in text.splitlines() if ': error:' in line]
        require(len(errors) == 1 and re.search(r': error: (?:application )?type mismatch', errors[0]), 'Original T14 control requires one intended type error')
    elif path == 'verification/AxiomAudit.lean':
        source = plan['contents'][plan['file_paths'][path]['source_id']].decode()
        names = re.findall(r'`([\w.]+)', source.split('let checks : Array Name := #[', 1)[1].split(']', 1)[0])
        rows = re.findall(r'^(P01AC\.[^ :]+): \[([^\]]*)\]$', text, re.M); axioms(rows)
        require([row[0] for row in rows] == names, 'Original T14 theorem audit inventory changed')
        require(int(match(r'AXIOM_AUDIT_PASS: (\d+) checked theorem closures contain no extra assumptions\.')) == len(rows), 'Original T14 theorem audit count changed')
    elif path == 'verification/CombinedAxiomAudit.lean':
        rows = re.findall(r'^DECLARATION ([^ ;]+); theorem=(true|false); axioms=\[([^\]]*)\]$', text, re.M)
        axioms([(name, raw) for name, _, raw in rows])
        total, theorems = map(int, match(r'COMBINED_AXIOM_AUDIT_PASS: constants=(\d+); theorems=(\d+)'))
        require(total == len(rows) == 156 and theorems == sum(kind == 'true' for _, kind, _ in rows), 'Original T14 combined declaration census changed')
        match(r'DECISIVE_THEOREM_KIND_PASS: 11 actual theorem declarations')
    elif path == 'ExtensionalRepairAudit.lean':
        rows = re.findall(r'^TRANSITIVE_AXIOMS ([^ :]+): \[([^\]]*)\]$', text, re.M); axioms(rows)
        total = int(match(r'AUDIT_PASS: (\d+) namespace declarations transitively checked; no sorryAx or new assumptions\.'))
        require(total == len(rows) and total > 50, 'Original T14 namespace audit count changed')
        source = plan['contents'][plan['file_paths'][path]['source_id']].decode()
        expected = re.findall(r'\(`([^,]+), (\d+)\)', source.split('let counts : Array', 1)[1].split('for (n, expected)', 1)[0])
        counts = re.findall(r'^CONSTRUCTOR_COUNT ([^ =]+) = (\d+)$', text, re.M)
        require(counts == expected, 'Original T14 constructor census changed')
        names = re.findall(r'`([\w.]+)', source.split('let checks : Array Name := #[', 1)[1].split(']', 1)[0])
        require(re.findall(r'^DECLARATION ([^ \n]+)$', text, re.M) == names, 'Original T14 declaration readback changed')
    elif path == 'verification/IndependentKernelChecks.lean':
        rows = re.findall(r'^INDEPENDENT_AXIOMS ([^ :]+): \[([^\]]*)\]$', text, re.M); axioms(rows)
        total, auxiliaries = map(int, match(r'INDEPENDENT_AXIOM_PASS (\d+) declarations; (\d+) compiler auxiliaries; no new axioms'))
        aux = re.findall(r'^COMPILER_AUXILIARY ([^ :]+): unsafe=(true|false) partial=(true|false)$', text, re.M)
        require(total == len(rows) and total >= 156 and auxiliaries == len(aux) == len({n for n, _, _ in aux}), 'Original T14 independent declaration census changed')
        require(all(n in {row[0] for row in rows} and 'true' in (unsafe, partial) for n, unsafe, partial in aux), 'Invalid T14 compiler auxiliary readback')
        roots, visited = map(int, match(r'LOGICAL_SAFETY_CLOSURE_PASS (\d+) safe namespace roots; (\d+) total reachable declarations; no unsafe or partial dependencies'))
        require(roots == total - auxiliaries and visited >= roots, 'Compiler auxiliaries were counted as safe proof roots')
        retained = re.findall(r'^EXACT_RETAINED_CONSTRUCTOR ([^ =]+) = ([^ \n]+)$', text, re.M)
        require(len(retained) == len(set(retained)) == 54, 'Original T14 retained constructor census changed')
        require(re.findall(r'^EXACT_NEW_SCHEMA ([^ \n]+)$', text, re.M) == ['P01AC.ExtensionalRepair.HasE.piExt', 'P01AC.ExtensionalRepair.HasE.allExt'], 'Original T14 new schema inventory changed')
        match(r'CONVERSION_EXACT_EIGHT_IMPORTED_GENERATORS')
        match(r'WITNESS_FINITE_SYNTACTIC_CONSTRUCTION_PASS PiExt=#?\[P01AC.ExtensionalRepair.arrow_identity_has\] AllExt=#?\[P01AC.ExtensionalRepair.separation_has\]')


def _input_inventory(row, path, plan):
    path = no_symlinks(path)
    if row['kind'] == 'FILE':
        if not path.is_file(): raise MissingInput('Required external file is unavailable: ' + row['id'])
        data = path.read_bytes()
        require(len(data) == row['expected_bytes'] and sha(data) == row['expected_sha256'], 'External file identity mismatch')
        return {'sha256': sha(data), 'bytes': len(data)}
    if not path.is_dir(): raise MissingInput('Required external selected tree is unavailable: ' + row['id'])
    records = {}
    for item in plan['input_manifests'][row['id']]:
        source = path_in(path, item['path'])
        if not source.is_file(): raise MissingInput('Required locked input file is unavailable')
        data = source.read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Locked external source changed')
        if 'blob_sha1' in item:
            require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == item['blob_sha1'], 'Locked Git blob identity mismatch')
        records[item['path']] = {'sha256': item['sha256'], 'bytes': item['bytes']}
    return records


def _verify_environment(suite, plan, tools, inputs, output):
    main_name = 'lean' if suite['toolchain']['kind'] == 'LEAN' else 'python'
    definitions = {main_name: {**suite['toolchain'], 'path_kind': 'EXECUTABLE'}}
    definitions.update({r['name']: r for r in suite['replay']['tools']})
    resolved = {}; fingerprints = {}; logs = output / 'logs'; env = _clean_environment()
    for name, definition in definitions.items():
        if name not in tools: raise MissingTool('Required explicit tool is unavailable: ' + name)
        raw = Path(tools[name]).absolute()
        # Interpreter symlinks (e.g. a venv) resolve to a hash-checked executable;
        # source, input, project and output paths never use this exception.
        if definition['path_kind'] == 'BIN_DIRECTORY': raw = raw / ('lean' if definition['kind'] == 'LEAN' else 'python')
        elif definition['path_kind'] == 'DISTRIBUTION_ROOT': raw = raw / 'bin' / ('lean' if definition['kind'] == 'LEAN' else 'python')
        if not raw.is_file(): raise MissingTool('Required executable is unavailable: ' + name)
        require(sha(raw.read_bytes()) == definition['executable_sha256'], 'Executable hash mismatch: ' + name)
        log = logs / ('tool-' + name + '.log')
        result = run_process([raw, '--version'], output, env, log, 30)
        text = log.read_text(encoding='utf-8', errors='replace')
        require(result['terminal'] == 'COMPLETED' and result['exit_code'] == 0, 'Tool version readback failed')
        require(re.search(r'(?<![0-9.])' + re.escape(definition['version']) + r'(?![0-9.])', text), 'Tool version mismatch')
        if definition['kind'] == 'LEAN': require('6caaee842e94' in text and 'x86_64-unknown-linux-gnu' in text, 'Wrong official Lean build')
        resolved[name] = raw
        fingerprints[name] = {'kind': definition['kind'], 'version': definition['version'], 'platform': definition['platform'],
                              'executable_sha256': definition['executable_sha256'], 'version_log_sha256': result['log_sha256']}
    libraries = []; repositories = {}; dependencies = {}
    git = shutil.which('git')
    pins = {r['name']: r for r in suite['toolchain']['packages']}
    for name, row in plan['packages'].items():
        pin = pins[name]
        if row['kind'] == 'PYTHON_DISTRIBUTION':
            script = 'import importlib.metadata,sys; print(importlib.metadata.version(sys.argv[1]))'
            log = logs / ('package-' + name + '.log')
            result = run_process([resolved['python'], '-I', '-B', '-c', script, name], output, env, log, 30)
            require(result['terminal'] == 'COMPLETED' and result['exit_code'] == 0 and log.read_text().strip() == pin['revision'], 'Python distribution version mismatch: ' + name)
            dependencies[name] = {'kind': 'PYTHON_DISTRIBUTION', 'revision': pin['revision'], 'manifest_sha256': sha(plan['contents'][row['manifest_source_id']]), 'log_sha256': result['log_sha256']}
            continue
        base = tools.get('mathlib')
        if base is None or not Path(base).is_dir() or git is None: raise MissingTool('Pinned Git dependency prerequisites are unavailable')
        repo = path_in(base, row['path'], dot=True)
        if not repo.is_dir(): raise MissingTool('Pinned dependency is unavailable: ' + name)
        head_log = logs / (name + '-head.log'); clean_log = logs / (name + '-clean.log')
        head = run_process([git, '-C', repo, 'rev-parse', 'HEAD'], output, env, head_log, 30)
        clean = run_process([git, '-C', repo, 'status', '--porcelain', '--untracked-files=no'], output, env, clean_log, 30)
        require(head['exit_code'] == 0 and head_log.read_text().strip() == pin['revision'], 'Wrong dependency revision: ' + name)
        require(clean['exit_code'] == 0 and not clean_log.read_text().strip(), 'Dirty pinned dependency: ' + name)
        library = path_in(repo, '.lake/build/lib/lean')
        libraries.extend(package_library(name, library, plan['official'])); repositories[name] = repo
        dependencies[name] = {'kind': 'GIT', 'revision': pin['revision'], 'manifest_sha256': sha(plan['contents'][row['manifest_source_id']]),
                              'tracked_clean': True, 'cache_policy': 'TRUSTED_PINNED_OFFICIAL_CACHE', 'head_log_sha256': head['log_sha256'], 'status_log_sha256': clean['log_sha256']}
    if 'lean' in resolved:
        distribution = resolved['lean'].resolve().parent.parent
        builtin = distribution / 'lib/lean'
        libraries.append(builtin)
        for module, row in plan['official'].items():
            base = distribution / 'src/lean' if row['package'] == 'lean-release' else repositories[row['package']]
            source = path_in(base, row['path'])
            if not source.is_file(): raise MissingTool('Official import source is unavailable: ' + module)
            require(sha(source.read_bytes()) == row['sha256'], 'Official import source mismatch: ' + module)
            if not any((lib / (module.replace('.', '/') + '.olean')).is_file() for lib in libraries):
                raise MissingTool('Official import object is unavailable: ' + module)
        for library in libraries:
            for module in plan['modules']:
                require(not (library / (module.replace('.', '/') + '.olean')).exists(), 'Custom module shadows/uses external cached object')
    input_hashes = {}
    for iid, row in plan['inputs'].items():
        if iid not in inputs: raise MissingInput('Required explicit external input is unavailable: ' + iid)
        input_hashes[iid] = _input_inventory(row, inputs[iid], plan)
    build_roots = [path_in(output, p) for p in suite['replay']['build_roots']]
    original_owned = any(row['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE} for row in plan['drivers'].values())
    for path in build_roots:
        if not original_owned: path.mkdir(parents=True, exist_ok=True)
    if 'lean' in resolved:
        env['LEAN_PATH'] = os.pathsep.join(str(p) for p in [*build_roots, *libraries])
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PATH'] = os.pathsep.join(dict.fromkeys([str(p.parent) for p in resolved.values()] + ([str(Path(git).parent)] if git else []) + ([os.defpath] if os.name != 'nt' else [os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32'])))
    return resolved, fingerprints, dependencies, env, input_hashes


def _make_fixture(row, plan, inputs, output):
    destination = path_in(output, 'fixtures/' + row['id'])
    require(not destination.exists(), 'Fixture output already exists')
    if row['operation'] == 'ABSENT': return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    if row['operation'] == 'NON_DIRECTORY':
        destination.write_bytes(b'negative fixture, not a source directory\n'); return destination
    if plan['inputs'][row['input_id']]['kind'] == 'FILE':
        require(row['operation'] == 'APPEND_CHANGED_BYTES' and row['path'] is None, 'Unsupported file fixture')
        destination.write_bytes(no_symlinks(inputs[row['input_id']]).read_bytes() + b'\nchanged-byte-control\n')
        return destination
    destination.mkdir()
    for item in plan['input_manifests'][row['input_id']]:
        if item['path'] == row['path'] and row['operation'] == 'OMIT': continue
        data = path_in(inputs[row['input_id']], item['path']).read_bytes()
        if item['path'] == row['path']: data += b'\nchanged-byte-control\n'
        target = path_in(destination, item['path']); target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    return destination


def _expand(argument, mappings):
    found = re.match(r'^\{([^{}]+)\}(.*)$', argument)
    if not found:
        require('{' not in argument and '}' not in argument, 'Malformed symbolic argument')
        return argument
    name, suffix = found.groups(); require(name in mappings, 'Unresolved argument binding')
    if suffix:
        require(suffix.startswith('/'), 'Unreviewed symbolic flag form')
        relative(suffix[1:])
    return str(mappings[name]) + suffix


def _file_hashes(path):
    path = no_symlinks(path)
    require(path.exists(), 'Declared output is absent')
    if path.is_file(): return sha(path.read_bytes())
    require(path.is_dir(), 'Declared output is not a file/directory')
    rows = {}
    for item in sorted(path.rglob('*')):
        no_symlinks(item)
        if item.is_file(): rows[item.relative_to(path).as_posix()] = sha(item.read_bytes())
    return canonical(rows)


def _language_result(driver, stage, text, plan):
    value = json.loads(text)
    require(isinstance(value, dict), 'Original verifier did not produce a JSON object')
    if stage['kind'] == 'NEGATIVE_CONTROL':
        fixture_id = stage['argv'][-1].removeprefix('{fixture:').removesuffix('}')
        fixture = plan['fixtures'][fixture_id]; operation = fixture['operation']
        if operation in {'ABSENT', 'NON_DIRECTORY'}: expected = 'source directory is missing or is not a directory'
        elif operation == 'OMIT': expected = 'missing or unreadable locked file: ' + fixture['path']
        else: expected = ('custody:' if driver['recipe'] == 't14-occurrence-v1' else 'source identity mismatch: ') + fixture['path']
        require(value == {'status': 'FAIL', 'reason': expected}, 'Original verifier rejected a different condition')
    else:
        recipe = LANGUAGE_RECIPES[driver['recipe']]
        require(value.get('status') == 'PASS' and len(value.get('checks', [])) == recipe['checks'] and all(r.get('pass') is True for r in value['checks']), 'Original verifier count/check contract failed')
        if driver['recipe'] == 't14-occurrence-v1': require(value.get('custody_files_checked') == 70, 'Occurrence source closure count changed')
        else: require(value.get('source_files_checked') == 9 and value.get('occurrence_data_checks') == 0, 'Supplemental source/occurrence scope changed')


def _empirical_package(plan):
    require('SHA256SUMS' in plan['file_paths'], 'Missing original empirical checksum manifest')
    data = plan['contents'][plan['file_paths']['SHA256SUMS']['source_id']]
    require(sha(data) == EMPIRICAL_RECIPES['t15-empirical-integrity-v1'], 'Empirical checksum manifest changed')
    names = set()
    for line in data.decode().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Malformed original checksum row')
        expected, name = match.groups(); relative(name)
        require(name not in names and name in plan['file_paths'], 'Missing/duplicate original empirical file')
        names.add(name)
        require(sha(plan['contents'][plan['file_paths'][name]['source_id']]) == expected, 'Original empirical dependency source changed')
    require(len(names) == 11 and set(plan['file_paths']) == names | {'SHA256SUMS'}, 'Empirical package inventory changed')
    return names


def check_unittest_log(text, names):
    actual = re.findall(r'(?m)^(test_\w+) \([^\n]+\) \.\.\. ok\s*$', text)
    require(len(actual) == len(names) and set(actual) == set(names), 'Original unittest success inventory incomplete')
    require(re.search(r'(?m)^Ran ' + str(len(names)) + r' tests? in ', text) and text.rstrip().endswith('\nOK'), 'Original unittest terminal/count changed')


def check_original_readbacks(text, names):
    rows = re.findall(r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])", text)
    require(len(rows) == len(names) and {name for name, _ in rows} == set(names), 'Original axiom readback inventory changed')
    for _, axes in rows:
        require({a.strip() for a in axes.split(',') if a.strip()} <= AXIOMS, 'Original readback contains an unapproved axiom')


def source_readback_names(text, targets):
    """Resolve literal readbacks through their exact lexical namespace frames.

    The source-selected target map disambiguates existing qualified constants.
    No suffix match to an arbitrary log declaration is accepted.
    """
    known = {row['name'] for row in targets}; frames = []; current = ''; names = []
    stripped = strip_lean(text)
    if not re.search(r'(?m)^\s*#print\s+axioms\s+', stripped): return []
    for line in stripped.splitlines():
        line = line.strip()
        found = re.fullmatch(r'namespace\s+([^\s]+)', line)
        if found:
            name = found.group(1); lean_name(name)
            frames.append(current)
            current = (current + '.' if current else '') + name
        elif line == 'mutual' or re.fullmatch(r'(?:noncomputable\s+)?section(?:\s+[^\s]+)?', line):
            frames.append(current)
        elif re.fullmatch(r'end(?:\s+[^\s]+)?', line):
            require(frames, 'Unmatched namespace/section end')
            current = frames.pop()
        else:
            # A dotted literal can name a theorem declared in this lexical
            # namespace without being among the suite's selected targets.
            # Use only explicit prior source declarations, never log suffixes.
            declared = re.match(r"theorem\s+([A-Za-z_][A-Za-z0-9_'.]*)(?=\s|[({:])", line)
            if declared:
                name = declared.group(1)
                known.add(name[len('_root_.'):] if name.startswith('_root_.') else
                          (current + '.' if current else '') + name)
            found = re.fullmatch(r'#print\s+axioms\s+([^\s]+)', line)
            if not found: continue
            literal = found.group(1); lean_name(literal)
            if literal.startswith('_root_.'):
                names.append(literal[len('_root_.'):]); continue
            prefixes = current.split('.') if current else []
            candidates = ['.'.join(prefixes[:i] + [literal]) for i in range(len(prefixes), -1, -1)]
            resolved = next((name for name in candidates if name in known), None)
            # Fully qualified literals outside a namespace and local lexical
            # names are source identities even when only a subset is targeted.
            if resolved is None: resolved = literal if '.' in literal or not current else current + '.' + literal
            names.append(resolved)
    return names


def _readback_source_symbols(text):
    """Read explicit declarations and scoped simple opens, never compiler output."""
    token = r"[A-Za-z_][A-Za-z0-9_'.]*"
    lines = strip_lean(text).splitlines(); declarations = []; prints = []
    current = ''; frames = []; opened = []; index = 0
    while index < len(lines):
        number = index; line = lines[index].strip(); index += 1
        if line.startswith('open ') and '(' in line:
            while line.count('(') > line.count(')'):
                require(index < len(lines), 'Unclosed named open')
                line += ' ' + lines[index].strip(); index += 1
        found = re.fullmatch(r'namespace\s+(' + token + ')', line)
        if found:
            frames.append((current, list(opened))); name = found.group(1)
            current = name[7:] if name.startswith('_root_.') else (current + '.' if current else '') + name
            continue
        if line == 'mutual' or re.fullmatch(r'(?:noncomputable\s+)?section(?:\s+[^\s]+)?', line):
            frames.append((current, list(opened))); continue
        if re.fullmatch(r'end(?:\s+[^\s]+)?', line):
            require(frames, 'Unmatched readback source scope')
            current, opened = frames.pop(); continue
        if line.startswith('open '):
            if line.startswith('open scoped '): continue
            named = re.fullmatch(r'open\s+(' + token + r')\s*\(([^()]*)\)', line)
            if named:
                selected = named.group(2).split()
                require(selected and all(re.fullmatch(token, n) for n in selected), 'Unsupported named open')
                opened.append((current, named.group(1), selected))
            else:
                require(re.fullmatch(r'open\s+' + token + r'(?:\s+' + token + r')*', line) and
                        not set(line.split()) & {'in', 'hiding', 'renaming'}, 'Unsupported readback open form')
                opened.extend((current, name, None) for name in line[5:].split())
            continue
        declaration = re.sub(r'^(?:@\[[^\]]*\]\s*)+', '', line)
        found = re.match(r'((?:(?:private|protected|noncomputable|unsafe|partial)\s+)*)(?:theorem|lemma|def|abbrev|opaque|axiom|inductive|structure|class)\s+(' + token + r')(?=\s|[({:]|$)', declaration)
        if found and 'private' not in found.group(1).split():
            name = found.group(2)
            name = name[7:] if name.startswith('_root_.') else (current + '.' if current else '') + name
            declarations.append((name, number))
        found = re.fullmatch(r'#print\s+axioms\s+(' + token + ')', line)
        if found: prints.append((found.group(1), current, list(opened), number))
    require(not frames, 'Unclosed readback source scope')
    return declarations, prints


def source_readback_names_in_plan(source_id, plan):
    """Add source-owned open/import resolution to the established lexical reader.

    Only exact explicit declarations in the validated transitive custom imports
    can resolve an open name. Existing fully qualified/generated-name handling
    remains unchanged. Ambiguity is refused rather than inferred from a log.
    """
    text = plan['contents'][source_id].decode('utf-8')
    baseline = source_readback_names(text, plan['targets'].values())
    if not baseline: return []
    modules = plan['modules']; roots = [n for n, row in modules.items() if row['source_id'] == source_id]
    require(len(roots) == 1, 'Readback source has no unique module owner')
    selected = {}; active = set()
    def visit(name):
        require(name not in active, 'Readback import cycle')
        if name in selected: return
        if name not in modules:
            require(name in plan['official'], 'Missing readback import source'); return
        active.add(name); row = modules[name]; body = plan['contents'][row['source_id']].decode('utf-8')
        require(imports(body) == row['imports'], 'Readback imports differ from exact source')
        for dependency in row['imports']: visit(dependency)
        selected[name] = _readback_source_symbols(body); active.remove(name)
    visit(roots[0]); local = roots[0]; prints = selected[local][1]
    require(len(prints) == len(baseline), 'Readback source command census changed')
    result = []
    for fallback, (literal, current, opened, position) in zip(baseline, prints):
        available = {}
        for module, (declarations, _) in selected.items():
            for name, line in declarations:
                if module != local or line < position: available.setdefault(name, []).append(module)
        prefixes = current.split('.') if current else []
        lexical = [literal[7:]] if literal.startswith('_root_.') else ['.'.join(prefixes[:i] + [literal]) for i in range(len(prefixes), -1, -1)]
        resolved = next((name for name in lexical if name in available), None)
        if resolved is None and not literal.startswith('_root_.'):
            matches = set()
            for context, namespace, only in opened:
                if only is not None and literal not in only: continue
                parts = context.split('.') if context else []
                candidates = [namespace[7:]] if namespace.startswith('_root_.') else ['.'.join(parts[:i] + [namespace]) for i in range(len(parts), -1, -1)]
                namespace = next((n for n in candidates if any(key.startswith(n + '.') for key in available)), None)
                if namespace is not None and namespace + '.' + literal in available: matches.add(namespace + '.' + literal)
            require(len(matches) <= 1, 'Ambiguous source-owned open readback')
            if matches: resolved = next(iter(matches))
        if resolved is not None: require(len(available[resolved]) == 1, 'Ambiguous readback declaration owner')
        result.append(resolved if resolved is not None else fallback)
    return result


def _empirical_result(driver, stage, text, plan, output):
    recipe = driver['recipe']
    if recipe == 't15-empirical-tests-v1':
        body = plan['contents'][driver['source_id']].decode()
        names = re.findall(r'^    def (test_\w+)\(', body, re.M)
        require(len(names) == 13 and set(stage['control_ids']) == set(names), 'Original empirical unit control identity changed')
        check_unittest_log(text, names)
    elif recipe == 't15-empirical-reanalyse-v1':
        if stage['kind'] == 'NEGATIVE_CONTROL':
            require(text.strip() == 'Analysis failed: Source SHA-256 mismatch' and stage['expected_exit_codes'] == [2], 'Different empirical input failure')
        else:
            actual = read_json(path_in(output, stage['output_paths'][0]))
            expected = json.loads(plan['contents'][plan['file_paths']['AGGREGATE.json']['source_id']])
            def compare(a, b):
                if isinstance(b, bool): return a is b
                if isinstance(b, list): return isinstance(a, list) and len(a) == len(b) and all(compare(x, y) for x, y in zip(a, b))
                return type(a) in {int, float} and math.isfinite(a) and math.isclose(a, b, abs_tol=1e-7, rel_tol=0)
            require(isinstance(actual, dict) and set(actual) == set(expected) and all(compare(actual[k], v) for k, v in expected.items()), 'Original aggregate/reference contract failed')
    elif recipe == 't15-empirical-validate-v1':
        value = json.loads(text)
        require(set(value) == {'status', 'max_abs_sensitivity_difference', 'aggregate_reference'} and value['status'] == 'pass' and value['aggregate_reference'] == 'pass', 'Original numerical/reference validation failed')
        difference = value['max_abs_sensitivity_difference']
        require(type(difference) in {int, float} and math.isfinite(difference) and 0 <= difference < 1e-6, 'Original numerical agreement tolerance failed')


def _source_checks(plan, driver=None):
    if driver and driver['recipe'] == 't15-empirical-integrity-v1':
        return json.dumps({'status': 'PASS', 'checked_files': len(_empirical_package(plan))}) + '\n'
    checked = []
    for sid, row in plan['files'].items():
        if row['role'] in {'PROOF', 'AUDIT'} and row['path'].endswith('.lean'):
            text = plan['contents'][sid].decode('utf-8')
            require(not re.search(r'\b(sorry|admit|axiom)\b|set_option\s+(maxHeartbeats|maxRecDepth)', text), 'Original T10 source scan rejected a declaration/option')
            checked.append(sid)
    require(checked, 'Source scan has no declared sources')
    return json.dumps({'status': 'PASS', 'source_ids': checked}, sort_keys=True) + '\n'


def _audit_source(targets):
    # This checked-environment traversal follows the source-bound T15
    # AllProjectProofAudit algorithm, restricted to these exact target roots.
    header = '\n'.join('import ' + name for name in dict.fromkeys([r['module'] for r in targets] + ['Lean.Elab.Command', 'Lean.Util.CollectAxioms']))
    core = r'''
open Lean Elab Command
namespace V5SuccessorCheckedAudit
def permitted : Array Name := #[`propext, `Classical.choice, `Quot.sound]
def audit (root : Name) : CommandElabM (Nat × Array Name) := do
  let env ← getEnv
  let mut todo := [root]
  let mut scheduled : NameSet := ({} : NameSet).insert root
  let mut seen : NameSet := {}
  let mut axes : Array Name := #[]
  let mut count := 0
  for _ in [:1000000] do
    match todo with
    | [] => break
    | n :: rest =>
      todo := rest
      unless seen.contains n do
        seen := seen.insert n
        count := count + 1
        let some info := env.checked.get.find? n | throwError "UNCHECKED_DEPENDENCY {n}"
        if info.isUnsafe || info.isPartial then throwError "UNSAFE_OR_PARTIAL_DEPENDENCY {n}"
        if info.isAxiom then
          unless permitted.contains n do throwError "UNAPPROVED_AXIOM {n}"
          axes := axes.push n
        let mut dependencies := info.type.getUsedConstants.toList
        if let some value := info.value? true then dependencies := value.getUsedConstants.toList ++ dependencies
        match info with
        | .inductInfo value => dependencies := value.ctors ++ dependencies
        | .recInfo value =>
          for rule in value.rules do dependencies := rule.rhs.getUsedConstants.toList ++ dependencies
        | _ => pure ()
        for dependency in dependencies do
          unless scheduled.contains dependency do
            scheduled := scheduled.insert dependency
            todo := dependency :: todo
  unless todo.isEmpty do throwError "INCOMPLETE_PROOF_CLOSURE"
  return (count, axes)
end V5SuccessorCheckedAudit
set_option pp.universes true
set_option pp.explicit true
'''
    parts = [header, core]
    for row in targets:
        name = row['name']
        parts.append(f'''#eval IO.println "V5_BEGIN {name}"
#check @{name}
#print axioms {name}
run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdxFor? `{name} | throwError "MISSING_TARGET_OWNER"
  logInfo m!"V5_OWNER {name} {{env.header.moduleNames[idx.toNat]!}}"
  let (count, axes) ← V5SuccessorCheckedAudit.audit `{name}
  logInfo m!"V5_SAFE {name} {{count}} {{axes.toList}}"
#eval IO.println "V5_END {name}"
''')
    return '\n'.join(parts)


def _initial_receipt(suite, sources, reviews):
    now = utc(); empty = sha(b'')
    source_hashes = {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']}
    stages = []
    planned = [{ 'id': '_prerequisites', 'argv': ['{builtin:prerequisites}'], 'cwd': '.', 'timeout_seconds': 30}, *suite['replay']['stages']]
    if suite['replay']['target_names']:
        planned.append({'id': '_target_audit', 'argv': ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'], 'cwd': '.', 'timeout_seconds': 300})
    for row in planned:
        stages.append({'id': row['id'], 'argv': row['argv'], 'cwd': row['cwd'], 'budget_seconds': row['timeout_seconds'],
                       'started_at': now, 'ended_at': now, 'terminal': 'SKIPPED', 'exit_code': None, 'log_sha256': empty, 'output_hashes': {}})
    evidence = {'schema': 'orthemology-v5-replay-evidence-v1', 'descriptor_sha256': canonical(suite['replay']),
        'closure_sha256': closure_fingerprint(suite, sources), 'runner_sha256': sha(Path(__file__).read_bytes()),
        'source_hashes_before': source_hashes, 'source_hashes_after': dict(source_hashes),
        'import_fingerprints': import_fingerprints(suite, sources),
        'tool_fingerprints': {}, 'dependency_checks': {}, 'driver_hashes': {d['id']: d['sha256'] for d in suite['replay']['drivers']},
        'stage_results': stages, 'target_audits': [], 'control_diagnostics': [], 'output_hashes': {}, 'cache_policy': CACHE_POLICY}
    if any(row['argv'][:1] == ['{builtin:observe-child}'] for row in suite['replay']['stages']):
        evidence.update(schema='orthemology-v5-replay-evidence-v2', child_observations=[], driver_invocations=[])
    return {'id': suite['id'] + '-replay', 'suite_id': suite['id'], 'family': suite['family'], 'suite_sha256': canonical(suite),
        'source_hashes': source_hashes, 'review_hashes': {rid: reviews[rid]['review_sha256'] for rid in suite['review_ids']},
        'toolchain_sha256': canonical(suite['toolchain']), 'outcome': 'NOT_RUN', 'target_readbacks': [], 'controls': [], 'stages': [],
        'invocation': ['replay_v5_successors.py', '--execute', '--suite', suite['id'], '--out', '{out}'],
        'started_at': now, 'ended_at': now, 'exit_code': None, 'log_sha256': empty, 'axioms': [], 'proof_scope': 'NONE', 'replay_evidence': evidence}


def execute_suite(suite, sources, root, output, tools, inputs, scope=None, *, reviews=None):
    require(scope is None or scope == suite['replay']['scope'], 'Execute the exact declared scope; use a separately scoped descriptor for components')
    require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'Missing source-bound review identities')
    plan = validate_suite(suite, sources, root)
    project_suite(suite, sources, root, output)
    output = Path(output).absolute(); project = output / 'project'; logs = output / 'logs'; logs.mkdir()
    receipt = _initial_receipt(suite, sources, reviews); evidence = receipt['replay_evidence']
    results = {r['id']: r for r in evidence['stage_results']}; completed = {}; controls = {r['id']: r for r in suite['controls']}; captured_children = {}
    current = results['_prerequisites']; current['started_at'] = utc(); prerequisite_log = logs / 'prerequisites.log'; archive_hashes = {}
    def save():
        receipt['stages'] = [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in evidence['stage_results']]
        receipt['log_sha256'] = canonical({row['id']: row['log_sha256'] for row in evidence['stage_results']})
        write_json(output / 'RECEIPT.json', receipt)
    save()
    try:
        resolved, fingerprints, dependencies, env, input_hashes = _verify_environment(suite, plan, tools, inputs, output)
        evidence['tool_fingerprints'] = fingerprints; evidence['dependency_checks'] = dependencies
        t15_note = verify_t15_python3(resolved, env) + '\n' if any(row['recipe'] in T15_SOURCE_RECIPES for row in plan['drivers'].values()) else ''
        prerequisite_log.write_text('Exact tool, package, official import and external input prerequisites verified.\n' + t15_note)
        current.update(terminal='COMPLETED', exit_code=0, ended_at=utc(), log_sha256=sha(prerequisite_log.read_bytes()))
        mappings = {'project': project, 'out': output, 'build': output / 'build', 'adapter': Path(__file__).resolve()}
        main_name = 'lean' if suite['toolchain']['kind'] == 'LEAN' else 'python'
        definitions = {main_name: {'path_kind': 'EXECUTABLE'}, **{row['name']: row for row in suite['replay']['tools']}}
        mappings.update({'tool:' + name: tool_argument(definitions[name], path) for name, path in resolved.items()})
        if 'mathlib' in tools: mappings['dependency:mathlib'] = Path(tools['mathlib']).resolve()
        mappings.update({'input:' + name: Path(path) for name, path in inputs.items()})
        mappings.update({'driver:' + name: path_in(project, plan['files'][d['source_id']]['path']) for name, d in plan['drivers'].items() if d['source_id'] in plan['files']})
        for name, driver in plan['drivers'].items():
            if driver['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE}:
                iid = driver['external_input_id']; archive = path_in(output, 'archives/' + iid)
                inventory = extract_source_zip(inputs[iid], archive)
                archive_hashes[iid] = (archive, inventory)
                if driver['recipe'] == CORE_RECIPE:
                    require(core_source_order(archive, plan) == suite['replay']['module_order'], 'Original/declared runtime compile order differs')
                    source_root = archive
                elif driver['recipe'] == ATTR_RECIPE:
                    source_root = path_in(archive, ATTR_CONTRACT['root']); attribution_source_check(source_root, plan)
                else:
                    source_root = archive; history_source_check(source_root, plan)
                mappings['archive:' + iid] = source_root; mappings['driver:' + name] = source_root / 'replay.py'
        for sid, stage in plan['stages'].items():
            current = results[sid]; current['started_at'] = utc(); log = logs / (sid + '.log')
            driver = plan['drivers'].get(stage['driver_id']); recipe = driver['recipe'] if driver else None
            for parent in stage['depends_on']: require(completed.get(parent, {}).get('matched') is True, 'Prior stage did not satisfy its contract')
            for arg in stage['argv']:
                match = re.fullmatch(r'\{fixture:([^{}]+)\}', arg)
                if match and 'fixture:' + match.group(1) not in mappings:
                    require(stage['depends_on'], 'Fixture lacks completed positive prerequisite')
                    mappings['fixture:' + match.group(1)] = _make_fixture(plan['fixtures'][match.group(1)], plan, inputs, output)
            for name in stage['output_paths']:
                path = path_in(output, name); require(not path.exists(), 'Declared output already exists'); path.parent.mkdir(parents=True, exist_ok=True)
            if stage['argv'] == ['{builtin:source-check}']:
                log.write_text(_source_checks(plan, plan['drivers'][stage['driver_id']]), encoding='utf-8')
                run = {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': current['started_at'], 'ended_at': utc(), 'log_sha256': sha(log.read_bytes())}
            elif stage['argv'][:1] == ['{builtin:observe-child}']:
                parent_id, child_id = stage['argv'][1:]
                observed = captured_children[(parent_id, child_id)]
                child_log = path_in(output, plan['core_children'][child_id]['log'] if recipe == CORE_RECIPE else
                                   plan['attribution_children'][child_id]['log'] if recipe == ATTR_RECIPE else
                                   plan['history_children'][child_id]['log'] if recipe == HISTORY_RECIPE else 'mutation-copies/' + child_id + '/run.log')
                require(sha(child_log.read_bytes()) == observed['log_sha256'], 'Captured child log changed before observation')
                log.write_bytes(child_log.read_bytes())
                # This interval measures observation only. Actual child times are
                # retained separately and never replaced with the parent span.
                run = {'terminal': observed['terminal'], 'exit_code': observed['exit_code'], 'started_at': current['started_at'],
                       'ended_at': utc(), 'log_sha256': observed['log_sha256']}
                evidence['child_observations'].append({**observed, 'stage_id': sid, 'observed_at': run['ended_at']})
            else:
                launch = (history_tracer_argv(stage) if recipe == HISTORY_RECIPE else attribution_tracer_argv(stage) if recipe == ATTR_RECIPE else core_tracer_argv(stage) if recipe == CORE_RECIPE else
                          t10_tracer_argv(stage) if recipe == 't10-independent-mutations-v1' else stage['argv'])
                if recipe in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE, 't10-independent-mutations-v1'}:
                    evidence['driver_invocations'].append({'parent_stage_id': sid, 'driver_sha256': driver['sha256'],
                        'source_argv': stage['argv'], 'launch_argv': launch, 'runner_sha256': evidence['runner_sha256'],
                        'trace_sha256': None, 'parent_log_sha256': sha(b''), 'child_count': 0})
                    if recipe == HISTORY_RECIPE: evidence['driver_invocations'][-1]['launch_cwd'] = history_launch_cwd(driver)
                argv = [_expand(a, mappings) for a in launch]
                launch_cwd = Path(_expand(history_launch_cwd(driver), mappings)) if recipe == HISTORY_RECIPE else path_in(project, stage['cwd'], dot=True)
                run = run_process(argv, launch_cwd, stage_environment(stage, plan, output, env), log, stage['timeout_seconds'])
            current.update(run); text = log.read_text(encoding='utf-8', errors='replace')
            if recipe in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE, 't10-independent-mutations-v1'} and stage['kind'] == 'DRIVER':
                trace = path_in(output, 'traces/' + sid)
                evidence['driver_invocations'][-1].update(parent_log_sha256=run['log_sha256'],
                    trace_sha256=_file_hashes(trace) if trace.exists() else None,
                    child_count=len(list(trace.glob('*.json'))) if trace.exists() else 0)
                if trace.exists() and trace_resource_inconclusive(trace):
                    receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
                    raise ValueError('Resource-inconclusive original child')
            if run['terminal'] != 'COMPLETED':
                receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
                raise ValueError('Resource-inconclusive stage')
            assess_stage(stage, run, text, completed)
            if suite['id'] == 't14-identity': check_t14_stage(stage, text, plan)
            if suite['id'] == 't15-identity': check_t15_stage(stage, text, plan, output, check_t14_stage)
            if stage['driver_id'] in plan['drivers'] and plan['drivers'][stage['driver_id']]['recipe'] in LANGUAGE_RECIPES:
                _language_result(plan['drivers'][stage['driver_id']], stage, text, plan)
            if stage['driver_id'] in plan['drivers'] and plan['drivers'][stage['driver_id']]['recipe'] in EMPIRICAL_RECIPES:
                _empirical_result(plan['drivers'][stage['driver_id']], stage, text, plan, output)
            if recipe in T10_FINITE_RECIPES:
                t10_result(stage, text, plan, output, suite)
                if recipe == 't10-independent-mutations-v1' and stage['kind'] == 'DRIVER':
                    children, invocation = t10_collect_children(stage, current, text, plan, output, mappings)
                    captured_children.update(children)
                    require(evidence['driver_invocations'][-1] == invocation, 'Instrumented parent trace changed during parsing')
            if recipe in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE} and stage['kind'] == 'DRIVER':
                collector = core_collect_children if recipe == CORE_RECIPE else attribution_collect_children if recipe == ATTR_RECIPE else history_collect_children
                children, invocation, objects = collector(stage, current, text, plan, output, mappings)
                captured_children.update(children)
                require(evidence['driver_invocations'][-1] == invocation, 'Instrumented core parent trace changed during parsing')
                evidence['output_hashes'].update(objects)
            if (suite['id'] in APPROVED_DECLARED_SUITES or any(row['recipe'] in SOURCE_RECIPES for row in plan['drivers'].values())) and stage['argv'][-1].startswith('{project}/'):
                path = stage['argv'][-1][len('{project}/'):]
                if path.endswith('.lean'):
                    names = source_readback_names_in_plan(plan['file_paths'][path]['source_id'], plan)
                    if names: check_original_readbacks(text, names)
            current['output_hashes'] = {name: _file_hashes(path_in(output, name)) for name in stage['output_paths']}
            evidence['output_hashes'].update(current['output_hashes'])
            completed[sid] = {**run, 'matched': True}
            for cid in stage['control_ids']:
                control = controls[cid]; actual = control['expected_outcome']
                receipt['controls'].append({key: control[key] for key in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
                    'actual_outcome': actual, 'actual_outcome_sha256': sha(actual.encode()), 'terminal': run['terminal'], 'exit_code': run['exit_code'], 'log_sha256': run['log_sha256']})
                evidence['control_diagnostics'].append({'control_id': cid, 'stage_id': sid, 'prerequisite_stage_ids': stage['depends_on'],
                    'expected': stage['expected_diagnostics'], 'observed_log_sha256': run['log_sha256'], 'match': 'MATCHED'})
            save()
        if plan['targets']:
            for name in suite['replay']['module_order']:
                object_name = name.replace('.', '/') + '.olean'
                candidates = [path_in(output, p + '/' + object_name) for p in suite['replay']['build_roots']]
                require(any(p.is_file() and evidence['output_hashes'].get(p.relative_to(output).as_posix()) == sha(p.read_bytes()) for p in candidates), 'Target/import custom object was not freshly generated by this run')
            generated = output / 'generated'; generated.mkdir(); audit = generated / 'V5SuccessorReadback.lean'
            audit.write_text(_audit_source(list(plan['targets'].values())), encoding='utf-8')
            current = results['_target_audit']; log = logs / 'target-audit.log'
            run = run_process([resolved['lean'], '-j1', audit], project, env, log, current['budget_seconds']); current.update(run)
            if run['terminal'] != 'COMPLETED': receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
            require(run['terminal'] == 'COMPLETED' and run['exit_code'] == 0, 'Target proof-closure audit failed')
            audits = parse_readbacks(log.read_text(encoding='utf-8'), list(plan['targets'].values()))
            evidence['target_audits'] = [{'target_id': tid, **value, 'stage_id': '_target_audit', 'log_sha256': run['log_sha256']} for tid, value in audits.items()]
            receipt['axioms'] = sorted({a for value in audits.values() for a in value['axioms']})
        for driver in plan['drivers'].values():
            if driver['recipe'] in {ATTR_RECIPE, HISTORY_RECIPE}:
                verifier = verify_attribution_dependencies if driver['recipe'] == ATTR_RECIPE else verify_history_dependencies
                verifier(mappings['archive:' + driver['external_input_id']], mappings['dependency:mathlib'])
                for name, path in resolved.items():
                    require(sha(path.read_bytes()) == fingerprints[name]['executable_sha256'], 'Attribution execution tool changed during replay')
        for iid, row in plan['inputs'].items(): require(_input_inventory(row, inputs[iid], plan) == input_hashes[iid], 'External input changed during replay')
        for iid, (archive, inventory) in archive_hashes.items():
            actual = {p.relative_to(archive).as_posix(): sha(no_symlinks(p).read_bytes()) for p in archive.rglob('*') if p.is_file()}
            require(actual == inventory, 'Original extracted source/input bytes changed during replay')
        for sid, row in plan['files'].items(): require(path_in(project, row['path']).read_bytes() == plan['contents'][sid], 'Projected source changed during replay')
        evidence['source_hashes_after'] = {sid: sha(public_bytes(root, sources[sid])) for sid in suite['source_ids']}
        receipt['target_readbacks'] = [{key: target[key] for key in ('source_id', 'target_sha256')} | {'target_id': target['id'], 'outcome': 'CHECKED'} for target in suite['targets']]
        selected = suite['replay']['scope']
        outcome = {'FINITE': 'FINITE_ONLY', 'COMPONENTS': 'FRESH_KERNEL_COMPONENTS', 'DECLARED_SUITE': 'QUALIFIED_DECLARED_SUITE'}[selected]
        receipt.update(outcome=outcome, exit_code=0, proof_scope=selected)
    except (FileNotFoundError, ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        write_json(output / 'FAILURE.json', {'stage_id': current['id'], 'observed_at': utc(), 'error': type(error).__name__ + ': ' + str(error)})
        if isinstance(error, MissingInput): receipt.update(outcome='BLOCKED_EXTERNAL_INPUT', exit_code=2)
        elif isinstance(error, MissingTool): receipt.update(outcome='BLOCKED_TOOLCHAIN', exit_code=2)
        elif receipt['outcome'] != 'RESOURCE_INCONCLUSIVE': receipt.update(outcome='FAILED', exit_code=1)
        receipt['proof_scope'] = 'NONE'
        if current['terminal'] == 'SKIPPED':
            private_log = logs / (current['id'] + '-failure.log'); private_log.write_text(type(error).__name__ + ': ' + str(error) + '\n')
            current.update(terminal='MISSING' if isinstance(error, FileNotFoundError) else 'COMPLETED',
                           exit_code=None if isinstance(error, FileNotFoundError) else 1, ended_at=utc(), log_sha256=sha(private_log.read_bytes()))
        for invocation in evidence.get('driver_invocations', []):
            if invocation['parent_stage_id'] == current['id']: invocation['parent_log_sha256'] = current['log_sha256']
    receipt['ended_at'] = utc(); save()
    validate_receipt(receipt, suite, sources, root)
    return receipt


AC_SCHEMA = 'orthemology-v5-audit-continuation-v1'
AC_CACHE_POLICY = 'PINNED_OFFICIAL_CACHES_REUSED_CAMPAIGN_CUSTOM_OBJECTS_FRESH_AUDIT'
AC_SUITE_SHA256 = 'a775764e1ba9d626f9eebaf6642428769a1016f9d779c1832d1f0b3814722128'
AC_APPROVAL = '2c0c433ba860bc33862a87dff2e4c22f3ec1d584b580a0605a1ffc8163844f8b'
AC_AUDIT_SOURCE = 'ab2b1c9265ec5dbd1d3a24f4a664b5bbcd3da1e9ece871119499a1cb8b3bd4d8'
# Add only independently reviewed executor bytes; receipt fields cannot add trust.
# Every entry remains subject to the exact auditor, suite and source checks below.
AC_REVIEWED_EXECUTOR_HASHES = frozenset({'37f79cecd8cc76604c37a0d48288898abd22bd2fccdc0353f753ac31bdc34e89'})
AC_PRIOR = {
    'receipt_sha256': '71306bdd74347b64600cff1eb99cddcc21970f8ff9e82345e91e06666c57ad8e',
    'receipt_canonical_sha256': 'a83603f4b746920aab44f8c7a599298c49a7750327811a81773fef641254166c',
    'receipt_bytes': 509311,
    'runner_sha256': '18b4e09215cd521361058cd54160a5587803bc7ce79b044a730a2d670e8e9ee0',
    'failed_audit_source_sha256': 'b02b41837b2b617bd3bcb8d399a866cc5aa95b077fea5e45c2d986674fcc92fc',
    'failed_audit_log_sha256': '26f349531c72aadcdb91c72df3746b46567811c77699c2fa1811dfda61098ae6',
    'failure_record_sha256': '544f32f8a7d2e79c456a68081c9b5f1d6570a7eaf92feb8a547dbe0cbb0821a3',
    'physical_trace_sha256': '76719061dcee7c07eac0a76f72e184de2fb945d63a1136d1ad704894f265284e',
    'original_result_sha256': '260dd5a450a9d1874562aa7fbc696a8567a7f62e9c16c03d56433c772a116958',
}
# Assessment-time retained inputs, using the adapter's existing _file_hashes
# algorithm (canonical relative-path -> SHA256 map), not historical measurements.
AC_RETAINED_TREE = '748a5d8d993637c120afc3b0998bf0109b5c6658c7f2de0ff29f426859a524a8'
AC_PROJECT_TREE = '814e0bc51656238428d09176456b50199ac00363b7f78ff8d7fdc9625db5c510'
AC_RECEIPT_KEYS = set('id suite_id family suite_sha256 source_hashes review_hashes toolchain_sha256 outcome target_readbacks controls stages invocation started_at ended_at exit_code log_sha256 axioms proof_scope replay_evidence'.split())
AC_EVIDENCE_KEYS = set('schema descriptor_sha256 closure_sha256 runner_sha256 source_hashes_before source_hashes_after import_fingerprints tool_fingerprints dependency_checks stage_results target_audits output_hashes cache_policy prior retained_input_checks fresh_audit accounting'.split())
AC_PRIOR_KEYS = set('receipt_sha256 receipt_canonical_sha256 receipt_bytes receipt failed_audit_source_sha256 failed_audit_log_sha256 failure_record_sha256'.split())
AC_RETAINED_KEYS = set('mode stage_ids physical_trace_sha256 original_result_sha256 child_ledger_sha256 driver_invocations_sha256 archive_sha256 retained_tree_before_sha256 retained_tree_after_sha256 project_sources_before_sha256 project_sources_after_sha256 custom_objects_before custom_objects_after official_cache_measurements'.split())
AC_FRESH_KEYS = set('recipe generated_source_sha256 resolved_invocation_sha256 argv_provenance traversal_bound distinct_declaration_accounting fresh_custom_objects'.split())
AC_STAGE_KEYS = set('id argv cwd budget_seconds started_at ended_at terminal exit_code log_sha256 output_hashes'.split())
AC_AUDIT_KEYS = set('target_id name type_sha256 axioms closure_status checked_declarations stage_id log_sha256'.split())
AC_ACCOUNTING = {'reused_source_owned_physical_runs': 1, 'reused_child_executions': 168,
    'reused_custom_objects': 167, 'reused_original_readbacks': 13, 'new_source_owned_physical_runs': 0,
    'new_child_compilations': 0, 'new_custom_objects': 0, 'new_target_audit_processes': 1,
    'independent_evidence_increment': 0}


def _ac_require(value, message):
    if not value:
        raise ValueError(message)


def _ac_keys(value, expected):
    _ac_require(isinstance(value, dict) and set(value) == expected, 'Unknown or missing continuation fields')


def _ac_time(value):
    _ac_require(isinstance(value, str) and value.endswith('Z'), 'Continuation timestamp is not UTC')
    return datetime.fromisoformat(value[:-1] + '+00:00')


def _ac_eligible_prior(evidence, suite, sources, root, adapter, plan):
    binding = evidence['prior']; _ac_keys(binding, AC_PRIOR_KEYS)
    _ac_require(type(binding['receipt_bytes']) is int, 'Invalid original byte count')
    _ac_require(all(binding[key] == AC_PRIOR[key] for key in AC_PRIOR_KEYS - {'receipt'}), 'Changed prior trust anchor')
    prior = binding['receipt']; _ac_keys(prior, AC_RECEIPT_KEYS)
    _ac_require(adapter.canonical(prior) == AC_PRIOR['receipt_canonical_sha256'], 'Substituted original receipt')
    old = prior['replay_evidence']
    _ac_require(old['schema'] == 'orthemology-v5-replay-evidence-v2'
             and old['runner_sha256'] == AC_PRIOR['runner_sha256']
             and prior['outcome'] == 'FAILED' and prior['proof_scope'] == 'NONE'
             and type(prior['exit_code']) is int and prior['exit_code'] == 1,
             'Original failed receipt semantics changed')
    # Never make a fake successful copy to reuse the old validator.
    adapter.validate_receipt(prior, suite, sources, root)
    stages = adapter.indexed(old['stage_results'])
    _ac_require(list(stages) == ['_prerequisites', *plan['stages'], '_target_audit'], 'Incomplete original stage set/order')
    audit = stages['_target_audit']
    _ac_require(audit['terminal'] == 'COMPLETED' and type(audit['exit_code']) is int and audit['exit_code'] == 1
             and audit['log_sha256'] == AC_PRIOR['failed_audit_log_sha256']
             and old['target_audits'] == [] and prior['target_readbacks'] == [], 'Ineligible original audit failure')
    prerequisite = stages['_prerequisites']
    _ac_require(prerequisite['terminal'] == 'COMPLETED' and type(prerequisite['exit_code']) is int
             and prerequisite['exit_code'] == 0, 'Original prerequisite was not fulfilled')
    completed = {'_prerequisites'}
    for sid, declared in plan['stages'].items():
        actual = stages[sid]
        _ac_require(actual['terminal'] == 'COMPLETED' and type(actual['exit_code']) is int
                 and actual['exit_code'] in declared['expected_exit_codes']
                 and set(declared['depends_on']) <= completed
                 and set(actual['output_hashes']) == set(declared['output_paths']), 'Unfulfilled original source-owned stage')
        completed.add(sid)
    adapter.validate_child_evidence(old, plan, stages, True)
    launches = old['driver_invocations']
    _ac_require(len(launches) == 1 and launches[0]['trace_sha256'] == AC_PRIOR['physical_trace_sha256']
             and launches[0]['child_count'] == 168 and len(old['child_observations']) == 168,
             'Wrong retained physical-run identity/census')
    controls = adapter.indexed(prior['controls']); expected_controls = adapter.indexed(suite['controls'])
    diagnostics = adapter.indexed(old['control_diagnostics'], 'control_id')
    _ac_require(set(controls) == set(diagnostics) == set(expected_controls), 'Incomplete original controls')
    for cid, expected in expected_controls.items():
        actual = controls[cid]; diagnostic = diagnostics[cid]; stage = stages[diagnostic['stage_id']]
        _ac_require(all(actual[key] == expected[key] for key in ('source_id', 'target_id', 'role', 'expected_outcome_sha256'))
                 and actual['actual_outcome'] == expected['expected_outcome']
                 and actual['actual_outcome_sha256'] == adapter.sha(expected['expected_outcome'].encode())
                 and diagnostic['match'] == 'MATCHED' and actual['terminal'] == stage['terminal'] == 'COMPLETED'
                 and type(actual['exit_code']) is int and actual['exit_code'] == stage['exit_code']
                 and actual['log_sha256'] == stage['log_sha256'], 'Unfulfilled original control/diagnostic')
    objects = {}
    for child in old['child_observations']:
        for path, digest in child['output_hashes'].items():
            _ac_require(path not in objects, 'Duplicate physical custom-object producer')
            objects[path] = digest
    expected_paths = {suite['replay']['build_roots'][0] + '/' + name.replace('.', '/') + '.olean'
                      for name in suite['replay']['module_order']}
    _ac_require(len(objects) == 167 and set(objects) == expected_paths
             and objects == {name: value for name, value in old['output_hashes'].items() if name.endswith('.olean')},
             'Missing or unproduced transitive custom object')
    return prior, old, stages, objects


def _ac_retained_inputs(checks, prior, old, stages, objects, suite, adapter, plan):
    _ac_keys(checks, AC_RETAINED_KEYS)
    _ac_require(checks['mode'] == 'REUSED_CAMPAIGN_EXECUTION'
             and checks['stage_ids'] == [sid for sid in stages if sid != '_target_audit'], 'Retained stages misclassified')
    expected = {'physical_trace_sha256': AC_PRIOR['physical_trace_sha256'], 'original_result_sha256': AC_PRIOR['original_result_sha256'],
        'child_ledger_sha256': adapter.canonical(old['child_observations']),
        'driver_invocations_sha256': adapter.canonical(old['driver_invocations']),
        'archive_sha256': suite['replay']['external_inputs'][0]['expected_sha256'],
        'retained_tree_before_sha256': AC_RETAINED_TREE, 'retained_tree_after_sha256': AC_RETAINED_TREE,
        'project_sources_before_sha256': AC_PROJECT_TREE, 'project_sources_after_sha256': AC_PROJECT_TREE,
        'custom_objects_before': objects, 'custom_objects_after': objects}
    _ac_require(all(checks[key] == value for key, value in expected.items()), 'Changed retained inputs or producer association')
    caches = adapter.indexed(checks['official_cache_measurements'], 'root_id')
    _ac_require(set(caches) == {'lean'} | set(plan['packages']), 'Missing or foreign official cache root')
    for row in caches.values():
        _ac_keys(row, set('root_id measurement_phase tree_before_sha256 tree_after_sha256 file_count cache_policy'.split()))
        _ac_require(row['measurement_phase'] == 'CONTINUATION_ONLY'
                 and type(row['file_count']) is int, 'Cache measurement has wrong time/scope')
        if row['cache_policy'] == 'ABSENT_UNIMPORTED_PINNED_PACKAGE_CACHE':
            # The exact suite/source validation already binds all nine package
            # revisions and manifests, including this unimported Cli package.
            _ac_require(row['root_id'] == 'Cli' and row['file_count'] == 0
                     and row['tree_before_sha256'] == adapter.canonical({})
                     and not any(item['package'] == 'Cli' for item in plan['official'].values()),
                     'Absent cache is not the exact unimported pinned Cli package')
        else:
            _ac_require(row['cache_policy'] == 'TRUSTED_PINNED_OFFICIAL_CACHE'
                     and row['file_count'] > 0, 'Cache measurement has wrong time/scope')
        adapter.digest(row['tree_before_sha256']); adapter.digest(row['tree_after_sha256'])
        _ac_require(row['tree_before_sha256'] == row['tree_after_sha256'], 'Official cache changed during continuation')


def _ac_fresh_stages(receipt, evidence, prior, adapter):
    stages = adapter.indexed(evidence['stage_results'])
    _ac_require(list(stages) == ['_prerequisites', '_target_audit'], 'Fresh ledger contains reused or missing stages')
    start, end = _ac_time(receipt['started_at']), _ac_time(receipt['ended_at'])
    _ac_require(_ac_time(prior['ended_at']) < start <= end, 'Continuation reused original or reversed times')
    last = start
    for sid, row in stages.items():
        _ac_keys(row, AC_STAGE_KEYS)
        argv = ['{builtin:prerequisites}'] if sid == '_prerequisites' else ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean']
        _ac_require(row['argv'] == argv and row['cwd'] == '.' and type(row['budget_seconds']) is int
                 and row['budget_seconds'] == (30 if sid == '_prerequisites' else 300), 'Changed continuation invocation/budget')
        row_start, row_end = _ac_time(row['started_at']), _ac_time(row['ended_at'])
        _ac_require(last <= row_start <= row_end <= end, 'Invalid fresh stage interval/order')
        last = row_end
        _ac_require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'Unexecuted fresh audit is not a composite')
        if row['terminal'] == 'COMPLETED':
            _ac_require(type(row['exit_code']) is int and 0 <= row['exit_code'] < 124, 'Invalid fresh completed exit')
        else:
            _ac_require(row['exit_code'] is None, 'Resource failure has concrete process credit')
        adapter.digest(row['log_sha256']); _ac_require(row['output_hashes'] == {}, 'Fresh stage relabels outputs')
    pre = stages['_prerequisites']
    _ac_require(pre['terminal'] == 'COMPLETED' and pre['exit_code'] == 0, 'Continuation prerequisites not established')
    _ac_require(receipt['stages'] == [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')}
                                  for row in evidence['stage_results']], 'Top/fresh stage association differs')
    _ac_require(receipt['log_sha256'] == adapter.canonical({sid: row['log_sha256'] for sid, row in stages.items()}),
             'Fresh log map differs')
    return stages['_target_audit']


def _ac_validate(receipt, suite, sources, root, adapter):
    # Also reject nonfinite numeric values in otherwise opaque bound subobjects.
    json.dumps(receipt, ensure_ascii=False, allow_nan=False)
    _ac_keys(receipt, AC_RECEIPT_KEYS)
    _ac_require(suite['id'] == 'd06-core-runtime' and adapter.canonical(suite) == AC_SUITE_SHA256
             and adapter.APPROVED_DECLARED_SUITES.get(suite['id']) == AC_APPROVAL, 'Unapproved continuation suite')
    plan = adapter.validate_suite(suite, sources, root)
    evidence = receipt['replay_evidence']; _ac_keys(evidence, AC_EVIDENCE_KEYS)
    _ac_require(evidence['schema'] == AC_SCHEMA and evidence['cache_policy'] == AC_CACHE_POLICY, 'Unknown continuation schema/policy')
    prior, old, stages, objects = _ac_eligible_prior(evidence, suite, sources, root, adapter, plan)
    _ac_require(isinstance(receipt['id'], str) and receipt['id'].startswith('d06-core-runtime-audit-continuation-')
             and len(receipt['id']) > len('d06-core-runtime-audit-continuation-') and receipt['id'] != prior['id'], 'Continuation needs a new identity')
    for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256'):
        _ac_require(receipt[key] == prior[key], 'Changed continuation suite/source/review/toolchain binding')
    _ac_require(receipt['invocation'] == ['replay_v5_successors.py', '--audit-continuation', '--suite', suite['id'],
                                      '--prior', '{prior}', '--out', '{out}'], 'Not an audit-only invocation')
    for key in ('descriptor_sha256', 'closure_sha256', 'source_hashes_before', 'source_hashes_after',
                'import_fingerprints', 'tool_fingerprints', 'dependency_checks'):
        _ac_require(evidence[key] == old[key], 'Stale continuation source/import/tool/dependency evidence')
    adapter.digest(evidence['runner_sha256'])
    _ac_require((evidence['runner_sha256'] == adapter.sha(Path(adapter.__file__).read_bytes())
                 or evidence['runner_sha256'] in AC_REVIEWED_EXECUTOR_HASHES)
             and evidence['runner_sha256'] != AC_PRIOR['runner_sha256'], 'Wrong executing continuation runner')
    _ac_retained_inputs(evidence['retained_input_checks'], prior, old, stages, objects, suite, adapter, plan)
    _ac_keys(evidence['accounting'], set(AC_ACCOUNTING))
    _ac_require(all(type(evidence['accounting'][key]) is int and evidence['accounting'][key] == value
                 for key, value in AC_ACCOUNTING.items()), 'Duplicate or invented execution/build credit')
    fresh = evidence['fresh_audit']; _ac_keys(fresh, AC_FRESH_KEYS)
    generated = adapter.sha(adapter._audit_source(list(plan['targets'].values())).encode())
    _ac_require(generated == AC_AUDIT_SOURCE and fresh['recipe'] == 'checked-closure-deduplicated-enqueue-v1'
             and fresh['generated_source_sha256'] == generated
             and fresh['argv_provenance'] == 'RESOLVED_FROM_BOUND_INPUTS'
             and type(fresh['traversal_bound']) is int and fresh['traversal_bound'] == 1000000
             and fresh['distinct_declaration_accounting'] == 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED'
             and type(fresh['fresh_custom_objects']) is int and fresh['fresh_custom_objects'] == 0,
             'Changed auditor recipe/bound or false fresh builds')
    adapter.digest(fresh['resolved_invocation_sha256'])
    _ac_require(evidence['output_hashes'] == {'generated/V5SuccessorReadback.lean': generated}, 'Wrong genuinely new audit artifacts')
    audit = _ac_fresh_stages(receipt, evidence, prior, adapter)
    _ac_require(receipt['controls'] == prior['controls'], 'Original controls changed or relabeled fresh')
    successful = receipt['outcome'] == 'QUALIFIED_DECLARED_SUITE'
    if not successful:
        expected = 'FAILED' if audit['terminal'] == 'COMPLETED' else 'RESOURCE_INCONCLUSIVE'
        _ac_require(receipt['outcome'] == expected and receipt['proof_scope'] == 'NONE'
                 and type(receipt['exit_code']) is int and receipt['exit_code'] == 1
                 and (audit['terminal'] != 'COMPLETED' or audit['exit_code'] > 0)
                 and receipt['target_readbacks'] == [] and evidence['target_audits'] == [] and receipt['axioms'] == [],
                 'Failed audit acquired success/partial target credit')
    else:
        _ac_require(receipt['proof_scope'] == 'DECLARED_SUITE' and type(receipt['exit_code']) is int
                 and receipt['exit_code'] == 0 and audit['terminal'] == 'COMPLETED' and audit['exit_code'] == 0,
                 'Continuation lacks complete successful fresh audit')
        audits = adapter.indexed(evidence['target_audits'], 'target_id')
        _ac_require(set(audits) == set(plan['targets']), 'Incomplete or foreign safe target audits')
        axes = set()
        for tid, row in audits.items():
            _ac_keys(row, AC_AUDIT_KEYS)
            _ac_require(row['name'] == plan['targets'][tid]['name'] and row['closure_status'] == 'CHECKED_SAFE'
                     and type(row['checked_declarations']) is int and row['checked_declarations'] > 0
                     and row['stage_id'] == '_target_audit' and row['log_sha256'] == audit['log_sha256'],
                     'Changed target/log/safe-closure binding')
            adapter.digest(row['type_sha256'])
            _ac_require(isinstance(row['axioms'], list) and len(set(row['axioms'])) == len(row['axioms'])
                     and set(row['axioms']) <= adapter.AXIOMS, 'Unapproved or duplicated axiom')
            axes.update(row['axioms'])
        expected_readbacks = [{'target_id': row['id'], 'source_id': row['source_id'],
            'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']]
        _ac_require(receipt['target_readbacks'] == expected_readbacks and receipt['axioms'] == sorted(axes),
                 'Fresh readback/source/axiom summary differs')
    return {'suite_id': suite['id'], 'outcome': receipt['outcome'],
            'scope': 'CONTINUATION_ENVELOPE_AND_PRIOR_ELIGIBILITY_ONLY'}


def validate_audit_continuation(receipt, suite, sources, root, *, adapter):
    """Validate one bounded composition without processes, writes or resealing."""
    try:
        return _ac_validate(receipt, suite, sources, root, adapter)
    except (TypeError, KeyError, IndexError, OverflowError) as error:
        raise ValueError('Malformed continuation envelope') from error


def _ac_exec_output(output, protected, adapter):
    output = adapter.no_symlinks(output).absolute()
    adapter.require(not output.exists(), 'Continuation output must be absent')
    for original in protected:
        original = Path(original).resolve()
        adapter.require(not output.is_relative_to(original) and not original.is_relative_to(output),
                        'Continuation output overlaps a consumed input')
    return output


def _ac_exec_inventory(root, adapter):
    root = adapter.no_symlinks(root)
    adapter.require(root.is_dir(), 'Retained input tree is absent')
    rows = {}
    for path in sorted(root.rglob('*')):
        adapter.no_symlinks(path)
        if path.is_file():
            rows[path.relative_to(root).as_posix()] = adapter.sha(path.read_bytes())
        else:
            adapter.require(path.is_dir(), 'Nonregular retained input')
    return rows, adapter.canonical(rows)


def _ac_exec_objects(prior, expected, build_roots, adapter):
    adapter.require(isinstance(expected, dict) and expected, 'Missing retained producer objects')
    actual = {}
    for name in expected:
        adapter.require(name.endswith('.olean'), 'Retained custom artifact is not an object')
        path = adapter.path_in(prior, name)
        adapter.require(path.is_file(), 'Retained custom object is missing')
        actual[name] = adapter.sha(path.read_bytes())
    adapter.require(actual == expected, 'Retained object differs from original producer')
    census = set()
    for root in build_roots:
        build = adapter.path_in(prior, root)
        adapter.require(build.is_dir(), 'Retained build root is absent')
        for path in build.rglob('*.olean'):
            adapter.no_symlinks(path)
            adapter.require(path.is_file(), 'Retained object is not a regular file')
            census.add(path.relative_to(prior).as_posix())
    adapter.require(census == set(expected), 'Foreign or missing retained custom object')
    return actual


def _ac_exec_caches(roots, plan, adapter):
    adapter.require(set(roots) == {'lean'} | set(plan['packages']), 'Missing or foreign official cache root')
    rows = []; inventories = {}
    for name, path in sorted(roots.items()):
        path = adapter.no_symlinks(path)
        if path.is_dir():
            inventory, digest = _ac_exec_inventory(path, adapter)
            adapter.require(inventory, 'Declared official cache is empty')
            policy = 'TRUSTED_PINNED_OFFICIAL_CACHE'
        else:
            adapter.require(not path.exists() and name == 'Cli' and not any(row['package'] == name for row in plan['official'].values()),
                            'Imported or unreviewed official cache is missing')
            inventory = {}; digest = adapter.canonical(inventory)
            policy = 'ABSENT_UNIMPORTED_PINNED_PACKAGE_CACHE'
        inventories[name] = inventory
        rows.append({'root_id': name, 'measurement_phase': 'CONTINUATION_ONLY',
                     'tree_before_sha256': digest, 'tree_after_sha256': digest,
                     'file_count': len(inventory), 'cache_policy': policy})
    return rows, inventories


def _ac_exec_generate(output, plan, adapter):
    body = adapter._audit_source(list(plan['targets'].values())).encode('utf-8')
    adapter.require(adapter.sha(body) == adapter.AC_AUDIT_SOURCE, 'Changed continuation audit generator')
    folder = adapter.path_in(output, 'generated')
    adapter.require(not folder.exists(), 'Generated audit output must be fresh')
    folder.mkdir()
    path = folder / 'V5SuccessorReadback.lean'
    with path.open('xb') as stream:
        stream.write(body)
    adapter.require(adapter.sha(path.read_bytes()) == adapter.AC_AUDIT_SOURCE, 'Generated audit readback mismatch')
    return path


def _ac_exec_result(run, text, targets, adapter):
    if run['terminal'] in {'TIMEOUT', 'INTERRUPTED'}:
        adapter.require(run['exit_code'] is None, 'Resource terminal has concrete process credit')
        return 'RESOURCE_INCONCLUSIVE', {}
    adapter.require(run['terminal'] == 'COMPLETED' and type(run['exit_code']) is int and 0 <= run['exit_code'] < 124,
                    'Unexecuted or invalid continuation terminal')
    if run['exit_code']:
        return 'FAILED', {}
    return 'QUALIFIED_DECLARED_SUITE', adapter.parse_readbacks(text, targets)


def _ac_exec_prior(prior, adapter):
    data = adapter.path_in(prior, 'RECEIPT.json').read_bytes()
    adapter.require(len(data) == adapter.AC_PRIOR['receipt_bytes'] and adapter.sha(data) == adapter.AC_PRIOR['receipt_sha256'],
                    'Wrong original receipt bytes')
    record = json.loads(data)
    adapter.require(adapter.canonical(record) == adapter.AC_PRIOR['receipt_canonical_sha256'], 'Wrong original receipt value')
    for name, key in [('generated/V5SuccessorReadback.lean', 'failed_audit_source_sha256'),
                      ('logs/target-audit.log', 'failed_audit_log_sha256'), ('FAILURE.json', 'failure_record_sha256'),
                      ('original/RESULT.json', 'original_result_sha256')]:
        adapter.require(adapter.sha(adapter.path_in(prior, name).read_bytes()) == adapter.AC_PRIOR[key],
                        'Original failure or source-owned result changed')
    return {key: record if key == 'receipt' else adapter.AC_PRIOR[key] for key in adapter.AC_PRIOR_KEYS}


def _ac_exec_retained(prior, plan, objects, suite, adapter):
    _, tree = _ac_exec_inventory(prior, adapter)
    adapter.require(tree == adapter.AC_RETAINED_TREE, 'Retained original run changed')
    project = adapter.path_in(prior, 'project')
    _, project_tree = _ac_exec_inventory(project, adapter)
    adapter.require(project_tree == adapter.AC_PROJECT_TREE, 'Retained projected source tree changed')
    for sid, row in plan['files'].items():
        adapter.require(adapter.path_in(project, row['path']).read_bytes() == plan['contents'][sid],
                        'Retained projected source differs from the current source binding')
    measured = _ac_exec_objects(prior, objects, suite['replay']['build_roots'], adapter)
    return tree, project_tree, measured


def _ac_exec_cache_roots(resolved, tools, plan, adapter):
    distribution = Path(resolved['lean']).resolve().parent.parent
    roots = {'lean': distribution / 'lib/lean'}
    libraries = []
    for name, row in plan['packages'].items():
        adapter.require(row['kind'] == 'GIT' and 'mathlib' in tools, 'Unreviewed continuation package kind')
        library = adapter.path_in(tools['mathlib'], row['path'], dot=True) / '.lake/build/lib/lean'
        roots[name] = library
        libraries.extend(adapter.package_library(name, library, plan['official']))
    libraries.append(roots['lean'])
    return roots, libraries


def _execute_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews, adapter):
    """Reuse the one pinned completed producer and execute only its missing audit.

    A prerequisite or post-processing refusal is a separate private artifact,
    never a replacement process exit or a successful clone of the failed run.
    """
    a = adapter
    a.require(suite['id'] == 'd06-core-runtime' and a.canonical(suite) == a.AC_SUITE_SHA256
              and a.APPROVED_DECLARED_SUITES.get(suite['id']) == a.AC_APPROVAL, 'Unapproved audit-continuation suite')
    a.require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'Missing current review identities')
    plan = a.validate_suite(suite, sources, root)
    prior = a.no_symlinks(prior).absolute()
    if not prior.is_dir(): raise a.MissingInput('Original run is unavailable')
    protected = [root, prior, *inputs.values()]
    if 'mathlib' in tools: protected.append(tools['mathlib'])
    for name, path in tools.items():
        if name != 'mathlib': protected.append(Path(path).resolve().parent.parent)
    output = _ac_exec_output(output, protected, a)
    started = a.utc(); run = None; runner_sha256 = a.sha(Path(a.__file__).read_bytes())
    output.mkdir(parents=True, exist_ok=False); (output / 'logs').mkdir()
    try:
        binding = _ac_exec_prior(prior, a)
        old_receipt, old, original_stages, objects = a._ac_eligible_prior({'prior': binding}, suite, sources, root, a, plan)
        a.require({rid: reviews[rid]['review_sha256'] for rid in suite['review_ids']} == old_receipt['review_hashes'],
                  'Current review identities differ from the original')
        hashes = {sid: a.sha(a.public_bytes(root, sources[sid])) for sid in suite['source_ids']}
        a.require(hashes == old_receipt['source_hashes'] == old['source_hashes_before'] == old['source_hashes_after']
                  and a.canonical(suite['replay']) == old['descriptor_sha256']
                  and a.closure_fingerprint(suite, sources) == old['closure_sha256']
                  and a.import_fingerprints(suite, sources) == old['import_fingerprints'], 'Current source/import binding changed')
        tree_before, project_before, objects_before = _ac_exec_retained(prior, plan, objects, suite, a)
        before = output / 'prerequisites-before'; before.mkdir()
        pre_start = a.utc()
        resolved, fingerprints, dependencies, env, input_hashes = a._verify_environment(suite, plan, tools, inputs, before)
        a.require(fingerprints == old['tool_fingerprints'] and dependencies == old['dependency_checks'],
                  'Current tool/dependency readback differs from the original binding')
        cache_roots, libraries = _ac_exec_cache_roots(resolved, tools, plan, a)
        cache_rows, cache_inventories = _ac_exec_caches(cache_roots, plan, a)
        env['LEAN_PATH'] = os.pathsep.join(str(p) for p in [*[a.path_in(prior, name) for name in suite['replay']['build_roots']], *libraries])
        pre_log = output / 'logs/prerequisites.log'
        pre_log.write_text('Current source, retained producer, custom objects, exact tools and dependency pins verified.\n'
                           'Official caches measured at continuation time; no historical cache measurement or fresh cache build claimed.\n', encoding='utf-8')
        pre = {'id': '_prerequisites', 'argv': ['{builtin:prerequisites}'], 'cwd': '.', 'budget_seconds': 30,
               'started_at': pre_start, 'ended_at': a.utc(), 'terminal': 'COMPLETED', 'exit_code': 0,
               'log_sha256': a.sha(pre_log.read_bytes()), 'output_hashes': {}}
        audit = _ac_exec_generate(output, plan, a)
        argv = [resolved['lean'], '-j1', audit]; cwd = a.path_in(prior, 'project')
        invocation = output / 'RESOLVED_AUDIT_INVOCATION.json'
        a.write_json(invocation, {'argv': [str(arg) for arg in argv], 'cwd': str(cwd), 'timeout_seconds': 300,
                                 'lean_path': env['LEAN_PATH'].split(os.pathsep), 'runner_sha256': runner_sha256,
                                 'generated_source_sha256': a.AC_AUDIT_SOURCE,
                                 'scope': 'ONE_FRESH_TARGET_AUDIT_REUSING_PINNED_CAMPAIGN_OBJECTS'})
        audit_log = output / 'logs/target-audit.log'
        run = a.run_process(argv, cwd, env, audit_log, 300)
        a.require(a.sha(audit_log.read_bytes()) == run['log_sha256'], 'Fresh audit log differs from its actual process')
        outcome, audits = _ac_exec_result(run, audit_log.read_text(encoding='utf-8'), list(plan['targets'].values()), a)
        after = output / 'prerequisites-after'; after.mkdir()
        checked_resolved, checked_fingerprints, checked_dependencies, _, checked_inputs = a._verify_environment(suite, plan, tools, inputs, after)
        a.require(checked_resolved == resolved and checked_fingerprints == fingerprints and checked_dependencies == dependencies
                  and checked_inputs == input_hashes, 'Consumed tool, dependency or external input changed during continuation')
        after_roots, after_libraries = _ac_exec_cache_roots(checked_resolved, tools, plan, a)
        a.require(after_roots == cache_roots and after_libraries == libraries, 'Official search roots changed')
        after_rows, after_inventories = _ac_exec_caches(after_roots, plan, a)
        a.require(after_rows == cache_rows and after_inventories == cache_inventories, 'Official cache changed during continuation')
        tree_after, project_after, objects_after = _ac_exec_retained(prior, plan, objects, suite, a)
        a.require(_ac_exec_prior(prior, a) == binding, 'Original receipt or failure artifacts changed during continuation')
        a.require({sid: a.sha(a.public_bytes(root, sources[sid])) for sid in suite['source_ids']} == hashes,
                  'Public source binding changed during continuation')
        a.require(a.sha(audit.read_bytes()) == a.AC_AUDIT_SOURCE, 'Generated auditor changed during continuation')
        a.require(a.sha(Path(a.__file__).read_bytes()) == runner_sha256, 'Executing adapter changed during continuation')
        audit_stage = {'id': '_target_audit', 'argv': ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'],
                       'cwd': '.', 'budget_seconds': 300, **run, 'output_hashes': {}}
        evidence = {key: old[key] for key in ('descriptor_sha256', 'closure_sha256', 'source_hashes_before', 'source_hashes_after',
                    'import_fingerprints', 'tool_fingerprints', 'dependency_checks')}
        evidence.update(schema=a.AC_SCHEMA, runner_sha256=runner_sha256, cache_policy=a.AC_CACHE_POLICY,
            prior=binding, stage_results=[pre, audit_stage],
            target_audits=[{'target_id': tid, **value, 'stage_id': '_target_audit', 'log_sha256': run['log_sha256']} for tid, value in audits.items()],
            output_hashes={'generated/V5SuccessorReadback.lean': a.AC_AUDIT_SOURCE},
            retained_input_checks={'mode': 'REUSED_CAMPAIGN_EXECUTION', 'stage_ids': [sid for sid in original_stages if sid != '_target_audit'],
                'physical_trace_sha256': a.AC_PRIOR['physical_trace_sha256'], 'original_result_sha256': a.AC_PRIOR['original_result_sha256'],
                'child_ledger_sha256': a.canonical(old['child_observations']), 'driver_invocations_sha256': a.canonical(old['driver_invocations']),
                'archive_sha256': suite['replay']['external_inputs'][0]['expected_sha256'],
                'retained_tree_before_sha256': tree_before, 'retained_tree_after_sha256': tree_after,
                'project_sources_before_sha256': project_before, 'project_sources_after_sha256': project_after,
                'custom_objects_before': objects_before, 'custom_objects_after': objects_after, 'official_cache_measurements': cache_rows},
            fresh_audit={'recipe': 'checked-closure-deduplicated-enqueue-v1', 'generated_source_sha256': a.AC_AUDIT_SOURCE,
                'resolved_invocation_sha256': a.sha(invocation.read_bytes()), 'argv_provenance': 'RESOLVED_FROM_BOUND_INPUTS',
                'traversal_bound': 1000000, 'distinct_declaration_accounting': 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED', 'fresh_custom_objects': 0},
            accounting=dict(a.AC_ACCOUNTING))
        receipt = {key: old_receipt[key] for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256', 'controls')}
        successful = outcome == 'QUALIFIED_DECLARED_SUITE'
        receipt.update(id=suite['id'] + '-audit-continuation-' + a.sha((started + a.sha(invocation.read_bytes())).encode())[:16],
            invocation=['replay_v5_successors.py', '--audit-continuation', '--suite', suite['id'], '--prior', '{prior}', '--out', '{out}'],
            outcome=outcome, proof_scope='DECLARED_SUITE' if successful else 'NONE', exit_code=0 if successful else 1,
            started_at=started, ended_at=a.utc(), replay_evidence=evidence,
            stages=[{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in [pre, audit_stage]],
            log_sha256=a.canonical({row['id']: row['log_sha256'] for row in [pre, audit_stage]}),
            target_readbacks=[{'target_id': row['id'], 'source_id': row['source_id'], 'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']] if successful else [],
            axioms=sorted({axiom for value in audits.values() for axiom in value['axioms']}))
        a.validate_audit_continuation(receipt, suite, sources, root, adapter=a)
        a.write_json(output / 'RECEIPT.json', receipt)
        return receipt
    except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
        a.write_json(output / 'REFUSAL.json', {'status': 'CONTINUATION_REFUSED', 'started_at': started, 'ended_at': a.utc(),
                                             'audit_process': run, 'error': type(error).__name__ + ': ' + str(error),
                                             'prior_receipt_sha256': a.AC_PRIOR['receipt_sha256'], 'qualified_receipt_written': False})
        raise


def execute_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews=None):
    return _execute_audit_continuation(suite, sources, root, prior, output, tools, inputs,
                                      reviews=reviews, adapter=SimpleNamespace(**globals()))



def validate_receipt(receipt, suite, sources, root):
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == AC_SCHEMA:
        return validate_audit_continuation(receipt, suite, sources, root, adapter=SimpleNamespace(**globals()))
    plan = validate_suite(suite, sources, root); evidence = receipt['replay_evidence']
    has_children = any(row['argv'][:1] == ['{builtin:observe-child}'] for row in plan['stages'].values())
    keys(evidence, EVIDENCE_KEYS | ({'child_observations', 'driver_invocations'} if has_children else set()))
    require(evidence['schema'] == ('orthemology-v5-replay-evidence-v2' if has_children else 'orthemology-v5-replay-evidence-v1') and evidence['cache_policy'] == CACHE_POLICY, 'Unknown replay evidence/cache policy')
    require(receipt['suite_sha256'] == canonical(suite) and receipt['toolchain_sha256'] == canonical(suite['toolchain']), 'Stale suite/toolchain receipt')
    hashes = {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']}
    require(receipt['source_hashes'] == hashes and evidence['source_hashes_before'] == hashes and evidence['source_hashes_after'] == hashes, 'Stale source receipt')
    require(evidence['descriptor_sha256'] == canonical(suite['replay']) and evidence['closure_sha256'] == closure_fingerprint(suite, sources), 'Stale replay/import closure receipt')
    require(evidence['import_fingerprints'] == import_fingerprints(suite, sources), 'Stale import fingerprints')
    digest(evidence['runner_sha256'])
    require(evidence['driver_hashes'] == {r['id']: r['sha256'] for r in suite['replay']['drivers']}, 'Stale driver receipt')
    stages = indexed(evidence['stage_results']); declared = plan['stages']; expected_ids = {'_prerequisites'} | set(declared)
    if plan['targets']: expected_ids.add('_target_audit')
    require(set(stages) == expected_ids, 'Missing/extra executed-stage ledger entry')
    require(receipt['stages'] == [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in evidence['stage_results']], 'Top-level and detailed stage terminals differ')
    completed = {}; successful = receipt['outcome'] in {'FINITE_ONLY', 'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}
    for sid, row in stages.items():
        keys(row, {'id', 'argv', 'cwd', 'budget_seconds', 'started_at', 'ended_at', 'terminal', 'exit_code', 'log_sha256', 'output_hashes'})
        digest(row['log_sha256']); require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'SKIPPED', 'INTERRUPTED', 'MISSING'}, 'Unknown stage terminal')
        if row['terminal'] == 'COMPLETED': require(type(row['exit_code']) is int and 0 <= row['exit_code'] < 124, 'Invalid completed stage exit')
        else: require(row['exit_code'] is None, 'Noncompleted stage has terminal process credit')
        require(row['started_at'].endswith('Z') and row['ended_at'].endswith('Z') and row['started_at'] <= row['ended_at'], 'Invalid stage timestamps')
        if sid in declared:
            stage = declared[sid]
            require(row['argv'] == stage['argv'] and row['cwd'] == stage['cwd'] and row['budget_seconds'] == stage['timeout_seconds'], 'Receipt invocation/budget differs from descriptor')
            if successful:
                require(row['terminal'] == 'COMPLETED' and row['exit_code'] in stage['expected_exit_codes'], 'Successful receipt has an unfulfilled stage')
                require(set(row['output_hashes']) == set(stage['output_paths']), 'Missing successful output identity')
                require(set(stage['depends_on']) <= set(completed), 'Receipt prerequisite order/terminal failed')
        else:
            expected_argv = ['{builtin:prerequisites}'] if sid == '_prerequisites' else ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean']
            require(row['argv'] == expected_argv and row['cwd'] == '.' and row['budget_seconds'] == (30 if sid == '_prerequisites' else 300), 'Reserved audit/prerequisite invocation changed')
            if successful: require(row['terminal'] == 'COMPLETED' and row['exit_code'] == 0, 'Successful receipt lacks prerequisites or target audit')
        for value in row['output_hashes'].values(): digest(value)
        if row['terminal'] == 'COMPLETED': completed[sid] = row
    require(receipt['log_sha256'] == canonical({row['id']: row['log_sha256'] for row in evidence['stage_results']}), 'Receipt log identity mismatch')
    if has_children: validate_child_evidence(evidence, plan, stages, successful)
    observations = indexed(evidence['control_diagnostics'], 'control_id'); controls = indexed(receipt['controls'])
    if successful: require(set(observations) == set(controls) == set(indexed(suite['controls'])), 'Incomplete successful control coverage')
    for cid, row in observations.items():
        keys(row, {'control_id', 'stage_id', 'prerequisite_stage_ids', 'expected', 'observed_log_sha256', 'match'})
        require(cid in controls and row['stage_id'] in declared, 'Foreign diagnostic evidence')
        stage = declared[row['stage_id']]; actual_stage = stages[row['stage_id']]
        require(cid in stage['control_ids'] and row['expected'] == stage['expected_diagnostics'] and row['prerequisite_stage_ids'] == stage['depends_on'], 'Changed control diagnostic/prerequisite contract')
        require(row['observed_log_sha256'] == actual_stage['log_sha256'] == controls[cid]['log_sha256'], 'Control log/stage association mismatch')
        require(row['match'] in {'MATCHED', 'NOT_MATCHED', 'NOT_RUN'}, 'Unknown diagnostic match enum')
        if successful:
            require(row['match'] == 'MATCHED' and actual_stage['terminal'] == 'COMPLETED', 'Control diagnostic not established')
            require(controls[cid]['exit_code'] == actual_stage['exit_code'] and controls[cid]['terminal'] == actual_stage['terminal'], 'Control process terminal differs from stage')
    audits = indexed(evidence['target_audits'], 'target_id')
    if successful and plan['targets']: require(set(audits) == set(plan['targets']), 'Incomplete successful target audits')
    for tid, row in audits.items():
        keys(row, {'target_id', 'name', 'type_sha256', 'axioms', 'closure_status', 'checked_declarations', 'stage_id', 'log_sha256'})
        require(tid in plan['targets'] and row['name'] == plan['targets'][tid]['name'], 'Wrong target audit identity')
        digest(row['type_sha256']); require(set(row['axioms']) <= AXIOMS, 'Unapproved target axiom')
        require(row['closure_status'] == 'CHECKED_SAFE' and type(row['checked_declarations']) is int and row['checked_declarations'] > 0, 'Target closure not checked completely')
        require(row['stage_id'] == '_target_audit' and row['log_sha256'] == stages['_target_audit']['log_sha256'] and stages['_target_audit']['exit_code'] == 0, 'Target audit log/terminal mismatch')
    if successful:
        expected_outcome = {'FINITE': 'FINITE_ONLY', 'COMPONENTS': 'FRESH_KERNEL_COMPONENTS', 'DECLARED_SUITE': 'QUALIFIED_DECLARED_SUITE'}[suite['replay']['scope']]
        require(receipt['outcome'] == expected_outcome and receipt['proof_scope'] == suite['replay']['scope'] and receipt['exit_code'] == 0, 'Requested/evidenced scope differs')
        main_name = 'lean' if suite['toolchain']['kind'] == 'LEAN' else 'python'
        definitions = {main_name: suite['toolchain'], **{row['name']: row for row in suite['replay']['tools']}}
        require(isinstance(evidence['tool_fingerprints'], dict) and set(evidence['tool_fingerprints']) == set(definitions), 'Successful receipt lacks a declared tool check')
        for name, definition in definitions.items():
            actual = evidence['tool_fingerprints'][name]
            keys(actual, {'kind', 'version', 'platform', 'executable_sha256', 'version_log_sha256'})
            require(all(actual[key] == definition[key] for key in ('kind', 'version', 'platform', 'executable_sha256')), 'Substituted tool fingerprint')
            digest(actual['version_log_sha256'])
        require(set(evidence['dependency_checks']) == set(plan['packages']), 'Successful receipt lacks dependency checks')
        pins = {row['name']: row for row in suite['toolchain']['packages']}
        for name, definition in plan['packages'].items():
            actual = evidence['dependency_checks'][name]
            fields = {'kind', 'revision', 'manifest_sha256'}
            fields |= {'tracked_clean', 'cache_policy', 'head_log_sha256', 'status_log_sha256'} if definition['kind'] == 'GIT' else {'log_sha256'}
            keys(actual, fields)
            require(actual['kind'] == definition['kind'] and actual['revision'] == pins[name]['revision']
                    and actual['manifest_sha256'] == sha(plan['contents'][definition['manifest_source_id']]), 'Substituted dependency revision/manifest')
            if definition['kind'] == 'GIT':
                require(actual['tracked_clean'] is True and actual['cache_policy'] == 'TRUSTED_PINNED_OFFICIAL_CACHE', 'Unchecked/dirty dependency cache')
                digest(actual['head_log_sha256']); digest(actual['status_log_sha256'])
            else: digest(actual['log_sha256'])
        for control in suite['controls']:
            if control['role'] == 'COUNTEREXAMPLE_PROOF': require(control['target_id'] in audits, 'Counterexample lacks exact safe target proof audit')
    return {'suite_id': suite['id'], 'outcome': receipt['outcome'], 'scope': 'RECEIPT_IDENTITY_AND_DECLARED_EXECUTION_CONTRACT'}


def validate_child_evidence(evidence, plan, stages, successful):
    declared = {sid: row for sid, row in plan['stages'].items() if row['argv'][:1] == ['{builtin:observe-child}']}
    parents = {row['argv'][1] for row in declared.values()}
    launches = indexed(evidence['driver_invocations'], 'parent_stage_id')
    observed = indexed(evidence['child_observations'], 'stage_id')
    require(set(launches) <= parents and set(observed) <= set(declared), 'Foreign physical parent/child observation')
    if successful: require(set(launches) == parents and set(observed) == set(declared), 'Missing actual parent/child trace evidence')
    physical_runs = set()
    for pid, row in launches.items():
        stage = plan['stages'][pid]; driver = plan['drivers'][stage['driver_id']]
        is_core = driver['recipe'] == CORE_RECIPE; is_attribution = driver['recipe'] == ATTR_RECIPE; is_history = driver['recipe'] == HISTORY_RECIPE
        fields = {'parent_stage_id', 'driver_sha256', 'source_argv', 'launch_argv', 'runner_sha256', 'trace_sha256', 'parent_log_sha256', 'child_count'}
        if is_history:
            if 'launch_cwd' in row:
                fields.add('launch_cwd')
                require(row['launch_cwd'] == history_launch_cwd(driver), 'Changed history archive launch directory')
            else:
                # The sole earlier history launcher failed on its first child,
                # before objects or controls. Preserve that historical failure
                # without admitting its implicit cwd for any current execution.
                require(not successful and not observed and evidence['runner_sha256'] == HISTORY_LEGACY_FAILED_RUNNER
                        and row['child_count'] in (0, 1) and stages[pid]['terminal'] == 'COMPLETED'
                        and stages[pid]['exit_code'] == 1, 'Missing actual history launch directory')
        keys(row, fields)
        require(driver['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE, 't10-independent-mutations-v1'}, 'Unapproved observed original recipe')
        launch = history_tracer_argv(stage) if is_history else attribution_tracer_argv(stage) if is_attribution else core_tracer_argv(stage) if is_core else t10_tracer_argv(stage)
        count = 17 if is_history else 21 if is_attribution else 168 if is_core else 9
        require(row['driver_sha256'] == driver['sha256'] and row['source_argv'] == stage['argv'] and row['launch_argv'] == launch, 'Changed instrumented parent invocation')
        require(row['runner_sha256'] == evidence['runner_sha256'] and row['parent_log_sha256'] == stages[pid]['log_sha256'], 'Wrong parent execution/log binding')
        require(type(row['child_count']) is int and 0 <= row['child_count'] <= count, 'Invalid actual child census')
        if row['trace_sha256'] is not None:
            digest(row['trace_sha256']); require(row['trace_sha256'] not in physical_runs, 'Duplicate physical run credit'); physical_runs.add(row['trace_sha256'])
        if successful: require(row['trace_sha256'] is not None and row['child_count'] == count, 'Incomplete actual child census')
    seen = set()
    for sid, row in observed.items():
        stage = declared[sid]; pid, child = stage['argv'][1:]; driver = plan['drivers'][stage['driver_id']]
        is_core = driver['recipe'] == CORE_RECIPE; is_attribution = driver['recipe'] == ATTR_RECIPE; is_history = driver['recipe'] == HISTORY_RECIPE
        is_original = is_core or is_attribution or is_history
        fields = {'source_id', 'source_sha256', 'output_hashes'} if is_original else {'mutated_source_sha256', 'matched_source_literals'}
        if is_history: fields.update({'generated_source_sha256', 'log_assembly'})
        keys(row, fields | {'stage_id', 'source_child_id', 'parent_stage_id', 'driver_sha256', 'parser_id', 'mode', 'argv_provenance',
                   'argv', 'cwd', 'started_at', 'ended_at', 'observed_at', 'physical_run_sha256', 'parent_log_sha256',
                   'terminal', 'exit_code', 'actual_outcome', 'log_sha256', 'result_record_sha256'})
        require(pid in launches and row['physical_run_sha256'] == launches[pid]['trace_sha256'] and row['parent_log_sha256'] == stages[pid]['log_sha256'], 'Observation belongs to another physical run')
        require(row['driver_sha256'] == driver['sha256'] and row['parser_id'] == driver['recipe'], 'Wrong original parser authority')
        spec = plan['history_children'][child] if is_history else plan['attribution_children'][child] if is_attribution else plan['core_children'][child] if is_core else None
        expected_code = spec['exit_code'] if is_attribution or is_history else 0 if is_core else 1
        require(row['mode'] == 'NONEXECUTING_OBSERVATION' and row['argv_provenance'] == 'CAPTURED' and row['cwd'] == (history_launch_cwd(driver) if is_history else spec['cwd'] if is_attribution else '{project}'), 'Derived command or duplicate execution credited as observation')
        check_child_terminal(row, stages[pid], child, spec['argv'] if is_original else t10_child_argv(child), seen, expected_code)
        require(row['actual_outcome'] == ('ACCEPT' if expected_code == 0 else 'REJECT') and row['terminal'] == stages[sid]['terminal'] and row['exit_code'] == stages[sid]['exit_code'] and row['log_sha256'] == stages[sid]['log_sha256'], 'Contradictory observation stage summary')
        require(isinstance(row['observed_at'], str) and row['observed_at'].endswith('Z') and
                stages[pid]['ended_at'] <= stages[sid]['started_at'] <= row['observed_at'] <= stages[sid]['ended_at'], 'Observation time is not its actual parsing interval')
        if is_original:
            require(row['source_id'] == spec['source_id'] and row['source_sha256'] == sha(plan['contents'][spec['source_id']]), 'Wrong observed source identity')
            if is_history:
                require(row['generated_source_sha256'] == (sha(history_claim_source(child)) if child in HISTORY_CLAIMS else None), 'History generated claim differs from reviewed source')
                require(row['log_assembly'] == 'STDOUT_THEN_STDERR', 'History log stream order changed')
            outputs = row['output_hashes']; expected = {spec['output_path']} if spec['output_path'] else set()
            require(isinstance(outputs, dict) and set(outputs) == expected, 'Wrong observed object identity')
            for path, value in outputs.items():
                digest(value); require(evidence['output_hashes'].get(path) == value, 'Observed object not bound to physical producer')
            digest(row['result_record_sha256']); continue
        require(string_list(row['matched_source_literals']) and set(row['matched_source_literals']) <= set(T10_CHILD_DIAGNOSTICS[child]), 'Wrong original child diagnostic category')
        _, filename, changes = next(item for item in _t10_MUTATIONS if item[0] == child)
        body = t10_contents(plan, T10_CHECKER + '/' + filename).decode()
        for before, after in changes:
            require(before in body, 'Original source mutation no longer applies'); body = body.replace(before, after)
        require(row['mutated_source_sha256'] == sha(body.encode()), 'Observed mutation source differs')
        digest(row['result_record_sha256'])


_t10_MUTATION_DRIVER_SHA256 = 'b94b8df9b31c8b635743440afc3525fb6abff282336ef1ba9e2dd9a316f6fee4'

_t10_REVIEW_DRIVER_SHA256 = 'e1303f10bbe5da403553c2be7f2b7ff468f0567b501f63d854cfb3f908cabcf2'

_t10_ORIGINAL_HASHES = {'context_effects.py': '0f65f172926e61ff7280ec2e13fd36b4ff287ea530ebbfa00c9dce831f3355fa', 'read_cover.py': '808a9297d27b903722b4fc04ad9a526d3cfc3e371b14e5047e1d33d1c6e3e79f'}

_t10_MUTATIONS = [('current_only', 'context_effects.py', [('Ref(consumed)', 'Ref(0)')]), ('compose_depth_abs_shift', 'context_effects.py', [('depth=max(f.depth,g.depth-(p-f.consumed))', 'depth=max(f.depth,g.depth+abs(p-f.consumed))')]), ('drop_second_constraints', 'context_effects.py', [('constraints=f.constraints+tuple((subst(x),o) for x,o in g.constraints)', 'constraints=f.constraints')]), ('snapshot_blind_equality', 'context_effects.py', [('from dataclasses import dataclass', 'from dataclasses import dataclass, field'), ('    snapshot: str', '    snapshot: str = field(compare=False)')]), ('nonconvex_envelope', 'read_cover.py', [("if ix and ix!=list(range(ix[0],ix[-1]+1)):raise BadCoverage('justified role coverage is not convex on demanded origins')", "if False:raise BadCoverage('justified role coverage is not convex on demanded origins')")]), ('retired_service_available', 'read_cover.py', [('if w.eligible and w.adequate', 'if w.adequate')]), ('locality_ignores_response', 'read_cover.py', [('if all(response(alt,w)==response(pos,w) for w in menu if o not in w.coverage):found=True;break', 'if True:found=True;break')]), ('adequacy_ignores_fibres', 'read_cover.py', [('if observation in seen and seen[observation]!=values:return False', 'if observation in seen and seen[observation]!=values:return True')]), ('replace_adaptive_with_cover', 'read_cover.py', [('return max(solve(p) for p in parts)', 'return cover_dp(tuple(worlds[0].keys()),menu).cost')])]

_t10_DIAGNOSTICS = {'current_only': ('direct stack',), 'compose_depth_abs_shift': ('split', 'left association', 'right association'), 'drop_second_constraints': ('split', 'left association', 'right association'), 'snapshot_blind_equality': ('wrong snapshot accepted',), 'nonconvex_envelope': ('nonconvex accepted',), 'retired_service_available': ('retired service treated available',), 'locality_ignores_response': ('star accepted leak',), 'adequacy_ignores_fibres': ('false adequate-coverage certification',), 'replace_adaptive_with_cover': ('missed cheaper decision',)}

def _t10_load(data):

    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result

    def nonfinite(value):
        raise ValueError('Nonfinite JSON value')
    require(type(data) is bytes, 'Expected exact UTF-8 result bytes')
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=nonfinite)

def _t10_seconds(value):
    require(type(value) in (int, float) and math.isfinite(value) and (value >= 0), 'Invalid elapsed-time field')

def _t10_checked_mutation_children(result_bytes, parent_stdout, original_sources, child_artifacts, mutation_driver, review_driver):
    """Return actual child terminals; never turn the aggregate exit into REJECT.

    child_artifacts maps each exact mutation name to the two Python source files
    and run.log, all as bytes. The collector MUST reject unexpected-pass.json and
    any unrecorded terminal before calling this parser. Other byproducts receive
    no control credit. Driver argv and child argv are bound by the adapter's
    reviewed source-specific recipe, not reconstructed as observed data here.
    """
    require(sha(mutation_driver) == _t10_MUTATION_DRIVER_SHA256, 'Wrong mutation driver')
    require(sha(review_driver) == _t10_REVIEW_DRIVER_SHA256, 'Wrong independent reviewer')
    require(set(original_sources) == set(_t10_ORIGINAL_HASHES), 'Original source set differs')
    require({k: sha(v) for k, v in original_sources.items()} == _t10_ORIGINAL_HASHES, 'Original candidate source changed')
    value = _t10_load(result_bytes)
    require(isinstance(value, dict) and set(value) == {'status', 'count', 'mutation_boundary', 'source_hashes', 'records'}, 'Wrong mutation aggregate shape')
    require(value['status'] == 'PASS' and type(value['count']) is int and (value['count'] == 9), 'Incomplete mutation aggregate')
    require(value['mutation_boundary'] == 'only reviewer-owned file copies; original files unchanged', 'Changed mutation boundary')
    require(value['source_hashes'] == _t10_ORIGINAL_HASHES, 'Mutation aggregate names different originals')
    names = [row[0] for row in _t10_MUTATIONS]
    require(set(child_artifacts) == set(names), 'Missing or foreign child artifact set')
    records = value['records']
    require(isinstance(records, list) and len(records) == 9 and all((isinstance(r, dict) for r in records)), 'Incomplete mutation records')
    require([r.get('name') for r in records] == names, 'Missing, duplicate or reordered mutation record')
    require(parent_stdout.decode('utf-8').splitlines() == [name + ' KILLED' for name in names], 'Aggregate progress differs from complete child inventory')
    outputs = []
    for record, (name, filename, changes) in zip(records, _t10_MUTATIONS):
        require(set(record) == {'name', 'candidate_file', 'mutated_sha256', 'replacements', 'exit', 'killed_by_independent_assertion', 'last_line', 'seconds'}, 'Wrong child record shape')
        require(record['candidate_file'] == filename, 'Wrong mutated source owner')
        require(type(record['exit']) is int and record['exit'] == 1, 'Child did not terminate with the intended assertion exit')
        require(record['killed_by_independent_assertion'] is True, 'Child rejection was not recorded')
        _t10_seconds(record['seconds'])
        artifacts = child_artifacts[name]
        require(set(artifacts) == {'context_effects.py', 'read_cover.py', 'run.log'}, 'Missing child source/log or unexpected pass artifact')
        mutated = original_sources[filename].decode('utf-8')
        replacements = []
        for before, after in changes:
            count = mutated.count(before)
            require(count > 0, 'Reviewed literal mutation no longer applies')
            replacements.append({'old': before, 'new': after, 'occurrences': count})
            mutated = mutated.replace(before, after)
        require(record['replacements'] == replacements, 'Literal mutation contract changed')
        expected = dict(original_sources)
        expected[filename] = mutated.encode('utf-8')
        require(all((artifacts[fn] == data for fn, data in expected.items())), 'Child source differs beyond exact reviewed mutation')
        require(record['mutated_sha256'] == sha(expected[filename]), 'Mutated source digest differs')
        log = artifacts['run.log'].decode('utf-8')
        lines = log.strip().splitlines()
        require(lines and lines[-1] == record['last_line'] and lines[-1].startswith('AssertionError:'), 'Missing exact terminal assertion diagnostic')
        require('Traceback (most recent call last):' in log, 'Missing child exception traceback')
        require(not re.search('ModuleNotFoundError|ImportError|FileNotFoundError|PermissionError|MemoryError|RecursionError|TimeoutError|SyntaxError|NameError|KeyboardInterrupt', log), 'Infrastructure/resource diagnostic cannot earn rejection')
        matches = [literal for literal in _t10_DIAGNOSTICS[name] if literal in lines[-1]]
        require(matches and all((literal in review_driver.decode('utf-8') for literal in matches)), 'Child rejected an unreviewed property')
        outputs.append({'source_child_id': name, 'terminal': 'COMPLETED', 'exit_code': record['exit'], 'actual_outcome': 'REJECT', 'log_sha256': sha(artifacts['run.log']), 'mutated_source_sha256': sha(artifacts[filename]), 'matched_source_literals': matches, 'result_record_sha256': sha(json.dumps(record, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8'))})
    return outputs

def _t10_checked_count_map(value, expected_keys):
    require(isinstance(value, dict) and set(value) == set(expected_keys), 'Missing or foreign finite count group')
    require(all((type(n) is int and n > 0 for n in value.values())), 'Unexecuted or invalid count group')
    return value

def _t10_checked_semantic_assertions(data, names):
    value = _t10_load(data)
    require(isinstance(value, dict) and set(value) == {'status', 'semantic_mutants', 'killed', 'results', 'scope'}, 'Wrong semantic assertion shape')
    require(value['status'] == 'PASS' and type(value['semantic_mutants']) is int and (type(value['killed']) is int) and (value['semantic_mutants'] == value['killed'] == len(names) == 16), 'Incomplete semantic assertions')
    rows = value['results']
    require(isinstance(rows, list) and len(rows) == 16 and all((isinstance(r, dict) for r in rows)), 'Incomplete semantic result rows')
    require([r.get('id') for r in rows] == list(names), 'Missing or duplicate semantic result')
    for row in rows:
        require(set(row) == {'id', 'status', 'correct', 'mutant', 'mechanism'}, 'Wrong semantic result shape')
        require(row['status'] == 'KILLED' and isinstance(row['correct'], str) and isinstance(row['mutant'], str) and (row['correct'] != row['mutant']) and isinstance(row['mechanism'], str) and row['mechanism'], 'Semantic assertion did not distinguish its alternatives')
    return [{'source_control_id': r['id'], 'actual_outcome': 'ACCEPT'} for r in rows]

def _t10_checked_unit_output(data, controls):
    text = data.decode('utf-8')
    expected = {r['name'] + ' (test_contract.' + r['class'] + '.' + r['name'] + ') ... ok' for r in controls}
    observed = [line.strip() for line in text.splitlines() if re.match('^test_\\w+ \\(', line)]
    require(len(expected) == len(controls) == 49 and len(observed) == 49 and (set(observed) == expected), 'Missing, duplicate, skipped or failed unittest')
    require(len(re.findall('(?m)^Ran 49 tests in [0-9.]+s$', text)) == 1 and text.rstrip().endswith('\nOK'), 'Incomplete unittest terminal')
    require(not re.search('(?m)^(FAIL|ERROR|FAILED|OK \\()', text), 'Unittest failure/skip diagnostic')
    return [{'source_control_id': r['class'] + '.' + r['name'], 'actual_outcome': 'ACCEPT'} for r in controls]

T10_GROUPS = {'exhaustive': ['all_boolean_menu_adaptive_cover_cases',
                'interval_menu_cost_demand_cases',
                'keyed_binary_splits',
                'keyed_direct_cases',
                'keyed_words',
                'unkeyed_binary_splits',
                'unkeyed_direct_cases',
                'unkeyed_triple_parenthesisations',
                'unkeyed_words'],
 'independent': ['adaptive_product_menus',
                 'association_stack_triples',
                 'complete_response_leaks',
                 'convex_interval_instances',
                 'cover_subfamily_instances',
                 'direct_stack_pairs',
                 'effect_named_controls',
                 'effect_words',
                 'exact_unkeyed_depths',
                 'general_observation_tables',
                 'known_false_empty_query',
                 'locality_adequacy_separation',
                 'malformed_contract_rejections',
                 'nonconvex_rejections',
                 'positive_cost_rejections',
                 'public_evidence_cost_zero',
                 'public_metadata_leaks',
                 'retirement_controls',
                 'split_stack_pairs',
                 'star_only_family',
                 'whole_source_competitor'],
 'semantic': ['M01_CURRENT_TOP_ONLY',
              'M02_NET_HEIGHT_ONLY',
              'M03_DROP_KEYED_EXIT',
              'M04_COPY_AS_NEW_ROOT',
              'M05_SAME_TEXT_COLLAPSE',
              'M06_WEIGHTED_FURTHEST_RIGHT',
              'M07_FILL_RAW_INTERVAL_HOLE',
              'M08_ADDRESS_IMPLIES_QUERY_RIGHT',
              'M09_SOUND_ABSTENTION_IS_COMPLETION',
              'M10_MARGINALS_IMPLY_LOCALITY',
              'M11_LOCALITY_IMPLIES_ADEQUACY',
              'M12_LOCAL_SPEAKER_IS_GLOBAL_ROLE',
              'M13_RETAINED_COUNT_ONLY',
              'M14_HIDE_SELECTOR_CHANNEL',
              'M15_DISCARD_WHOLE_SOURCE_ALTERNATIVE',
              'M16_PROMOTE_SOURCE_FORCE_TO_CARRIER'],
 'two_card': ['full_product_cards_only',
              'full_product_fixed_a',
              'full_product_known_false_a',
              'full_product_fixed_b',
              'full_product_known_false_b',
              'full_product_fixed_c',
              'full_product_known_false_c',
              'full_product_full_role_table',
              'full_product_valid_Q_verdict',
              'full_product_value_dependent_origin_identity',
              'full_product_restored_source',
              'full_product_accepted_live_reader',
              'full_product_uninformative_old_result_d',
              'four_world_star_cards_only',
              'four_world_star_fixed_a',
              'four_world_star_known_false_a',
              'four_world_star_fixed_b',
              'four_world_star_known_false_b',
              'four_world_star_fixed_c',
              'four_world_star_known_false_c',
              'four_world_star_full_role_table',
              'four_world_star_valid_Q_verdict',
              'four_world_star_value_dependent_origin_identity',
              'four_world_star_restored_source',
              'four_world_star_accepted_live_reader',
              'four_world_star_uninformative_old_result_d',
              'correlated_outside_d_equals_Q',
              'correlated_outside_d_equals_a',
              'free_length_encodes_Q',
              'free_status_encodes_Q',
              'free_timing_encodes_Q',
              'free_authentication_payload_encodes_Q',
              'free_role_bearing_locator_encodes_Q',
              'rich_left_response_encodes_missing_c',
              'Q_verdict_insufficient_for_all_individual_roles',
              'edge_plus_opposite_card_answers_individual_roles',
              'copies_only_of_a',
              'copies_do_not_add_new_role',
              'no_permitted_menu_cannot_complete',
              'only_left_permitted_cannot_complete',
              'retained_Q_needs_no_read_permission',
              'safe_withholding_not_a_total_answer',
              'budget_one_rejects_b_plan',
              'renegotiated_budget_two_accepts_b_plan',
              'always_false_uniform_accuracy',
              'all_positive_answer_true_can_be_lucky',
              'left_positive_transcript_has_both_answers',
              'one_request_bounded_error_policy_worst_success']}


def main():
    if sys.argv[1:2] == ['--trace-history']:
        require(len(sys.argv) == 10, 'Malformed internal history trace invocation')
        return trace_history_driver(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    if sys.argv[1:2] == ['--trace-attribution']:
        require(len(sys.argv) == 10, 'Malformed internal attribution trace invocation')
        return trace_attribution_driver(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    if sys.argv[1:2] == ['--trace-core-runtime']:
        require(len(sys.argv) == 12, 'Malformed internal core trace invocation')
        return trace_core_runtime(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    if sys.argv[1:2] == ['--trace-t10-mutations']:
        require(len(sys.argv) == 8, 'Malformed internal trace invocation')
        return trace_t10_driver(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    for name in ('list', 'check', 'project', 'execute', 'audit-continuation'): mode.add_argument('--' + name, action='store_true')
    parser.add_argument('--suite'); parser.add_argument('--out', type=Path); parser.add_argument('--prior', type=Path)
    parser.add_argument('--tool', action='append', default=[]); parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--lean-bin', type=Path); parser.add_argument('--mathlib', type=Path); parser.add_argument('--python', type=Path)
    args = parser.parse_args()
    try:
        import validate_v5_successors as records
        bundle = records.load_bundle(args.root)
        suites = {row['id']: row for row in bundle['suites']}; sources = {row['id']: row for row in bundle['sources']}
        if args.list:
            print(json.dumps({'suites': [{'id': row['id'], 'scope': row['replay']['scope']} for row in suites.values()]})); return 0
        require(args.suite in suites, 'Unknown suite ID'); suite = suites[args.suite]
        if args.check:
            validate_suite(suite, sources, args.root); print(json.dumps({'suite_id': args.suite, 'status': 'VALID_DESCRIPTOR', 'executed': False})); return 0
        require(args.out is not None, 'An absent external --out directory is required')
        if args.project:
            project_suite(suite, sources, args.root, args.out); print(json.dumps({'suite_id': args.suite, 'status': 'PROJECTED', 'executed': False})); return 0
        def mapping(rows):
            result = {}
            for item in rows:
                require('=' in item, 'Expected NAME=PATH'); key, value = item.split('=', 1)
                require(key not in result and value, 'Duplicate/empty path binding'); result[identifier(key)] = Path(value)
            return result
        tools = mapping(args.tool); inputs = mapping(args.input)
        if args.lean_bin: require('lean' not in tools, 'Duplicate Lean binding'); tools['lean'] = args.lean_bin / ('lean.exe' if os.name == 'nt' else 'lean')
        if args.mathlib: require('mathlib' not in tools, 'Duplicate Mathlib binding'); tools['mathlib'] = args.mathlib
        if args.python: require('python' not in tools, 'Duplicate Python binding'); tools['python'] = args.python
        reviews = {r['id']: r for r in bundle['reviews']}
        if args.audit_continuation:
            require(args.prior is not None, 'Audit continuation requires the exact retained --prior run directory')
            receipt = execute_audit_continuation(suite, sources, args.root, args.prior, args.out, tools, inputs, reviews=reviews)
        else:
            require(args.prior is None, '--prior is only valid for audit continuation')
            receipt = execute_suite(suite, sources, args.root, args.out, tools, inputs, reviews=reviews)
        print(json.dumps({key: receipt[key] for key in ('suite_id', 'outcome', 'proof_scope', 'exit_code')})); return receipt['exit_code']
    except (MissingTool, MissingInput) as error:
        print('Replay prerequisites unavailable: ' + str(error), file=sys.stderr); return 2
    except (ValueError, OSError, KeyError) as error:
        print('Replay refused: ' + str(error), file=sys.stderr); return 1


if __name__ == '__main__':
    raise SystemExit(main())
