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


# Exact finite T15 source recipes; no generic stdin or generated-code interface.
"""Private proposal for two exact finite Python references, without new schema.

These hooks are spliced into the accepted core. The only stdin and PYTHONPATH
bindings are the original source-owned cases below; descriptors cannot provide
arbitrary input streams, environment fields, executables, or generated code.
"""
T15_REFERENCE_APPROVALS = {
    't15-json-reference': '25360314eadea6db85b8e75c044aabeed84920abe20a78e4c2791ff0977cf166',
    't15-univariate-reference': '169851b90219224dcc5d1531a9307346b4066125eef274cd94171d1ec36c11b3',
}
T15_REFERENCE_PYTHON = 'e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f'
T15_REFERENCE_FILES = {
    'python-reference/README.md': '373659d652481787fc1e9499261ee931b2e9150d003e640f9ae035258f6722fe',
    'python-reference/SOURCE_LOCK.json': 'f7bda53cf932963883223c7f14f305b1354b35207d2a50da3c0dfcc2e3813eec',
    'python-reference/certificate_checker.py': '8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef',
    'python-reference/examples/piecewise_instance.json': 'f2e38784e8358d65961a89cfc5faf38eadec97fd31a6ac10b68c199a00e7c781',
    'python-reference/examples/piecewise_certificate.json': 'd5326efbbe8ab9412afa98c91340df574ba4beedafcfbbaebfe542edb67f219a',
    'python-reference/examples/unequal_instance.json': 'f7807e76268ca56274e671d6ff2bf1753cd54b81f169ae4c2a3d25a2cbad0fa2',
    'python-reference/verification/test_certificate_checker.py': 'f2689d00865ed2964fa6dc4337d67da5017f23c34a870e5dad183ccc6ccd6bb9',
    'python-reference/verification/test_independent_checker.py': '27c5e18f459c5a6103a35f2fe0570ee2c229832490a02aa4f62064c8c6d25416',
    'univariate-reference/README.md': '92cb36221687dd71453d9df1f6b04061d2838956e410fb2e92e29d05ca98e7bb',
    'univariate-reference/SOURCE_ONLY_v1.sha256': 'f281d34cfdf3731f8c91244625146828c72a60acd7eacab60b51915caba1e644',
    'univariate-reference/root_extension_checker.py': 'bd796dc6d0157d0b8a125cc3b394a866812567f12ce132ee11d2fa3844e081d9',
    'univariate-reference/test_root_extension_checker.py': '23e55bf11880011ec5ae47c464e971d02b3e9af5e8541fcbaa7cc73b8d7f73e0',
    'univariate-reference/test_independent_adversarial.py': '24daa53895fbc95f6387a3de7b758356972edc2febf56243c26768547fe9223e',
}
T15_REFERENCE_RECIPES = {
    't15-json-reference-tests-v1': {
        'source': 'python-reference/verification/test_certificate_checker.py',
        'stage': 'json-reference-tests', 'cwd': 'python-reference', 'kind': 'REFERENCE_TESTS',
        'args': ['-m', 'unittest', 'discover', '-s', 'verification', '-p', 'test*.py', '-v'], 'meanings': {}},
    't15-json-reference-decide-example-v1': {
        'source': 'python-reference/certificate_checker.py', 'stage': 'json-reference-decide-example',
        'cwd': 'python-reference', 'kind': 'DRIVER', 'args': ['certificate_checker.py', 'decide'],
        'meanings': {'decide': 'LITERAL'}, 'stdin': 'python-reference/examples/piecewise_instance.json'},
    't15-json-reference-verify-example-v1': {
        'source': 'python-reference/certificate_checker.py', 'stage': 'json-reference-verify-example',
        'cwd': 'python-reference', 'kind': 'DRIVER', 'args': ['certificate_checker.py', 'verify'],
        'meanings': {'verify': 'LITERAL'}, 'stdin': 'python-reference/examples/piecewise_certificate.json'},
    't15-univariate-reference-tests-v1': {
        'source': 'univariate-reference/test_root_extension_checker.py', 'stage': 'univariate-reference-tests',
        'cwd': 'univariate-reference', 'kind': 'REFERENCE_TESTS',
        'args': ['-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py', '-v'], 'meanings': {}},
}


def t15_reference_data(plan, path):
    require(path in plan['file_paths'], 'Missing exact T15 reference source')
    sid = plan['file_paths'][path]['source_id']
    require(sid in plan['contents'], 'Missing exact T15 reference bytes')
    data = plan['contents'][sid]
    require(path in T15_REFERENCE_FILES and sha(data) == T15_REFERENCE_FILES[path], 'Changed T15 reference input')
    return data


def validate_t15_reference_driver(driver, plan):
    require(driver['recipe'] in T15_REFERENCE_RECIPES, 'Unknown T15 finite recipe')
    recipe = T15_REFERENCE_RECIPES[driver['recipe']]
    require(driver['sha256'] == T15_REFERENCE_FILES[recipe['source']] and
            driver['argument_meanings'] == recipe['meanings'] and driver['external_input_id'] is None and
            plan['files'][driver['source_id']]['path'] == recipe['source'], 'Changed T15 finite driver binding')
    t15_reference_data(plan, recipe['source'])


def validate_t15_reference_argv(stage, driver, plan):
    validate_t15_reference_driver(driver, plan)
    recipe = T15_REFERENCE_RECIPES[driver['recipe']]
    require(stage['id'] == recipe['stage'] and stage['kind'] == recipe['kind'] and stage['cwd'] == recipe['cwd'] and
            stage['argv'] == ['{tool:python}', *recipe['args']] and not stage['output_paths'] and
            not stage['control_ids'] and stage['expected_exit_codes'] == [0] and not stage['expected_diagnostics'],
            'Wrong original T15 reference arguments or stage role')


def validate_t15_reference_package(suite, plan, sources):
    require(T15_REFERENCE_APPROVALS.get(suite['id']) == declared_suite_fingerprint(suite, sources),
            'Original T15 finite suite has not been approved')
    require(suite['replay']['scope'] == 'FINITE' and suite['toolchain']['kind'] == 'PYTHON' and
            suite['toolchain']['executable_sha256'] == T15_REFERENCE_PYTHON and suite['toolchain']['version'] == '3.12.3',
            'T15 finite reference requires its exact selected Python environment')
    require(not suite['controls'] and not suite['toolchain']['packages'] and
            all(not suite['replay'][key] for key in ['modules', 'module_order', 'official_imports', 'target_names',
                'packages', 'tools', 'external_inputs', 'fixtures', 'build_roots']), 'T15 finite reference scope expanded')
    json_reference = suite['id'] == 't15-json-reference'
    expected = {path for path in T15_REFERENCE_FILES if path.startswith('python-reference/' if json_reference else 'univariate-reference/')}
    if not json_reference: expected.add('python-reference/certificate_checker.py')
    require(set(plan['file_paths']) == expected, 'Incomplete or shadowed T15 reference input inventory')
    for path in expected: t15_reference_data(plan, path)
    if json_reference:
        rows = json.loads(t15_reference_data(plan, 'python-reference/SOURCE_LOCK.json'))
        require(len(rows) == 6, 'Changed JSON reference lock inventory')
        paths = []
        for row in rows:
            path = 'python-reference/' + relative(row['path'])
            require(path in expected and sha(t15_reference_data(plan, path)) == row['sha256'], 'Changed JSON reference preservation lock')
            paths.append(path)
        require(len(set(paths)) == 6, 'Duplicate JSON reference preservation path')
    else:
        rows = t15_reference_data(plan, 'univariate-reference/SOURCE_ONLY_v1.sha256').decode().splitlines()
        require(len(rows) == 4, 'Changed univariate checksum inventory')
        paths = []
        for row in rows:
            match = re.fullmatch(r'([0-9a-f]{64})  ([^\r\n]+)', row)
            require(match is not None, 'Malformed univariate source checksum')
            path = 'univariate-reference/' + relative(match.group(2))
            require(path in expected and sha(t15_reference_data(plan, path)) == match.group(1), 'Changed univariate locked source')
            paths.append(path)
        require(len(set(paths)) == 4, 'Duplicate univariate checksum path')


def t15_reference_recipe(stage, plan):
    require(stage['driver_id'] in plan['drivers'], 'Unknown T15 finite driver')
    driver = plan['drivers'][stage['driver_id']]
    validate_t15_reference_argv(stage, driver, plan)
    return T15_REFERENCE_RECIPES[driver['recipe']]


def t15_reference_existing(project, path, plan):
    expected = t15_reference_data(plan, path)
    actual = path_in(project, path)
    require(actual.is_file() and actual.read_bytes() == expected, 'Changed projected T15 reference input')
    return actual


def t15_reference_environment(stage, plan, project, env):
    recipe = t15_reference_recipe(stage, plan)
    require(not any(key.startswith('PYTHON') and key != 'PYTHONDONTWRITEBYTECODE' for key in env),
            'Ambient Python configuration can change the original finite reference')
    result = dict(env)
    if recipe['cwd'] == 'univariate-reference':
        t15_reference_existing(project, 'python-reference/certificate_checker.py', plan)
        result['PYTHONPATH'] = str(path_in(project, 'python-reference'))
    return result


def t15_reference_stdin(stage, plan, project):
    recipe = t15_reference_recipe(stage, plan)
    return t15_reference_existing(project, recipe['stdin'], plan) if 'stdin' in recipe else None


def _t15_reference_input_process(argv, cwd, env, log, timeout, input_file):
    """Internal file-descriptor primitive, called only by the sealed CLI recipes.

    Lifecycle/timeout behavior matches accepted run_process. No stdin field is
    accepted from a descriptor, shell expression, or producer manifest.
    """
    started = utc(); log = Path(log); log.parent.mkdir(parents=True, exist_ok=True)
    with log.open('xb') as stream, no_symlinks(input_file).open('rb') as stdin:
        kwargs = {'start_new_session': True} if os.name != 'nt' else {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
        proc = subprocess.Popen([str(a) for a in argv], cwd=cwd, env=env, stdin=stdin,
                                stdout=stream, stderr=subprocess.STDOUT, shell=False, **kwargs)
        try:
            code = proc.wait(timeout=timeout)
            terminal = 'COMPLETED' if 0 <= code < 124 else 'INTERRUPTED'
            if terminal != 'COMPLETED': code = None
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
            terminal = 'TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED'; code = None
            _stop_process_group(proc)
    return {'terminal': terminal, 'exit_code': code, 'started_at': started, 'ended_at': utc(), 'log_sha256': sha(log.read_bytes())}


def run_t15_reference_stage(stage, argv, cwd, env, log, timeout, plan, project):
    recipe = t15_reference_recipe(stage, plan)
    require(argv[1:] == recipe['args'] and sha(no_symlinks(argv[0]).read_bytes()) == T15_REFERENCE_PYTHON and
            Path(cwd) == path_in(project, recipe['cwd']) and timeout == stage['timeout_seconds'], 'Expanded T15 finite invocation changed')
    selected_env = t15_reference_environment(stage, plan, project, env)
    stdin = t15_reference_stdin(stage, plan, project)
    if stdin is None: return run_process(argv, cwd, selected_env, log, timeout)
    return _t15_reference_input_process(argv, cwd, selected_env, log, timeout, stdin)


def t15_reference_test_names(plan):
    names = []
    for path in sorted(plan['file_paths']):
        if not PurePosixPath(path).name.startswith('test_') or not path.endswith('.py'): continue
        tree = ast.parse(t15_reference_data(plan, path))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                names.extend(PurePosixPath(path).stem + '.' + node.name + '.' + method.name for method in node.body
                             if isinstance(method, ast.FunctionDef) and method.name.startswith('test_'))
    require(len(names) == len(set(names)) and len(names) in {15, 22}, 'Wrong original T15 reference test inventory')
    return sorted(names)


def check_t15_reference_stage(stage, text, plan):
    recipe = t15_reference_recipe(stage, plan)
    if recipe['kind'] == 'REFERENCE_TESTS':
        expected = t15_reference_test_names(plan)
        rows = re.findall(r'(?m)^(test_\w+) \(([\w.]+)\) \.\.\. ok$', text)
        require(len(rows) == len(expected) and sorted(name for _, name in rows) == expected and
                all(name.rsplit('.', 1)[1] == method for method, name in rows), 'Original T15 test inventory did not pass completely')
        terminal = re.findall(r'(?m)^Ran (\d+) tests in [0-9.]+s$', text)
        require(terminal == [str(len(expected))] and text.rstrip().endswith('\nOK'), 'Incomplete original T15 unittest terminal')
        leftovers = re.sub(r'(?m)^test_\w+ \([\w.]+\) \.\.\. ok$|^-+$|^Ran \d+ tests in [0-9.]+s$|^OK$', '', text)
        require(not leftovers.strip(), 'Unexpected original T15 test failure, skip, warning or output')
    else:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, 'Duplicate key in CLI output readback')
                result[key] = value
            return result
        actual = json.loads(text, object_pairs_hook=unique)
        expected = {'equal': True, 'counterexample': None} if recipe['args'][-1] == 'decide' else {'accepted': True}
        require(canonical(actual) == canonical(expected), 'Original T15 CLI result changed')


"""Private source-bound finite runtime recipe; no generic generated-code API."""
T15_RUNTIME_RECIPE = 't15-restricted-runtime-agreement-v1'
T15_RUNTIME_APPROVAL = '62429564c5ca7c10107824965b5f4abbe3f180dc4ee0ba68b57396bf21f0fdbd'
T15_RUNTIME_CHECKER = '8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef'
T15_RUNTIME_PYTHON = 'e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f'
T15_RUNTIME_FILES = {
    'restricted-runtime/README.md': '02d23d9ee77fd60764c12d5f0412aa2e4c7d532c17209cbbf1ba595f19b69714',
    'restricted-runtime/BINDING.json': '3f4f57a24a27e3992d2f8836624b882fdbac3916dfabd56c2b3261be1b410f77',
    'restricted-runtime/SHA256SUMS': '18f002a663dc517f2380cc9f776d7817d4e5bb0988ab4cf88c7b1191134a102c',
    'restricted-runtime/VERIFIED_RESULT.json': '41a3a344e492deb878d274ff56bcf76a999baef234465202fed66b1e29c9a668',
    'restricted-runtime/check_runtime_agreement.py': 'dd69712d1a7b79bdb5fcb55c855c4c13a00725dda1cd8f4dfcdc4544afcbe8fd',
    'python-reference/certificate_checker.py': T15_RUNTIME_CHECKER,
}
T15_RUNTIME_SCOPE = 'Bounded runtime agreement on deterministic generated well-formed AST pairs; no parser or wire-format correspondence theorem.'
T15_RUNTIME_PREPARED = ['runtime/RuntimeAgreement.lean', 'runtime/cases.json', 'runtime/PREPARED_CASES.json']
T15_RUNTIME_ARGS = ['{tool:python}', '-B', 'restricted-runtime/check_runtime_agreement.py', 'python-reference/certificate_checker.py', '{out}/runtime']


def t15_runtime_data(plan, path):
    require(path in plan['file_paths'], 'Missing T15 runtime input')
    sid = plan['file_paths'][path]['source_id']
    require(sid in plan['contents'], 'Missing T15 runtime source bytes')
    data = plan['contents'][sid]
    require(path in T15_RUNTIME_FILES and sha(data) == T15_RUNTIME_FILES[path], 'Changed T15 runtime source input')
    return data


def validate_t15_runtime_driver(driver, plan):
    path = 'restricted-runtime/check_runtime_agreement.py'
    require(driver['recipe'] == T15_RUNTIME_RECIPE and driver['sha256'] == T15_RUNTIME_FILES[path] and
            driver['external_input_id'] is None and plan['files'][driver['source_id']]['path'] == path and
            driver['argument_meanings'] == {'checker': 'SOURCE_FILE', 'output': 'OUTPUT_DIRECTORY', '--verify-lean': 'LITERAL'},
            'Changed original T15 runtime driver binding')
    t15_runtime_data(plan, path)


def validate_t15_runtime_argv(stage, driver, plan):
    validate_t15_runtime_driver(driver, plan)
    expected = {
        'runtime-prepare': (T15_RUNTIME_ARGS, T15_RUNTIME_PREPARED, ['compile-IdentityChecker'], 600),
        'runtime-lean': (['{tool:lean}', '-j1', '{out}/runtime/RuntimeAgreement.lean'], ['runtime/lean-output.txt'], ['runtime-prepare'], 1800),
        'runtime-verify': (T15_RUNTIME_ARGS + ['--verify-lean'], ['runtime/VERIFIED_RESULT.json'], ['runtime-lean'], 600),
    }
    require(stage['id'] in expected, 'Unknown T15 runtime phase')
    argv, outputs, parents, budget = expected[stage['id']]
    require(stage['kind'] == 'DRIVER' and stage['cwd'] == '.' and stage['argv'] == argv and
            stage['output_paths'] == outputs and stage['depends_on'] == parents and stage['timeout_seconds'] == budget and
            stage['expected_exit_codes'] == [0] and not stage['control_ids'] and not stage['expected_diagnostics'],
            'Changed original T15 runtime phase arguments, outputs or edge')


def validate_t15_runtime_package(suite, plan, sources):
    require(suite['id'] == 't15-runtime-agreement' and declared_suite_fingerprint(suite, sources) == T15_RUNTIME_APPROVAL,
            'Complete T15 finite runtime recipe has not been approved')
    replay = suite['replay']
    require(replay['scope'] == 'FINITE' and suite['toolchain']['kind'] == 'PYTHON' and
            suite['toolchain']['version'] == '3.12.3' and suite['toolchain']['executable_sha256'] == T15_RUNTIME_PYTHON and
            not suite['controls'] and not replay['target_names'], 'T15 runtime scope or selected tool changed')
    require(len(replay['files']) == 83 and len(replay['modules']) == len(replay['module_order']) == 76 and
            replay['module_order'][-1] == 'IdentityChecker' and replay['build_roots'] == ['build'] and
            len(replay['stages']) == 79 and [s['id'] for s in replay['stages'][-3:]] == ['runtime-prepare', 'runtime-lean', 'runtime-verify'],
            'Incomplete fresh T15 runtime support closure or phase inventory')
    require({p for p in plan['file_paths'] if p.endswith('.py')} ==
            {'restricted-runtime/check_runtime_agreement.py', 'python-reference/certificate_checker.py'}, 'Unreviewed T15 runtime Python import source')
    for path in T15_RUNTIME_FILES: t15_runtime_data(plan, path)
    rows = t15_runtime_data(plan, 'restricted-runtime/SHA256SUMS').decode().splitlines()
    require(len(rows) == 4, 'Changed original runtime checksum inventory')
    seen = set()
    for row in rows:
        match = re.fullmatch(r'([0-9a-f]{64})  ([^\r\n]+)', row)
        require(match is not None, 'Malformed runtime checksum row')
        path = 'restricted-runtime/' + relative(match.group(2))
        require(path not in seen and sha(t15_runtime_data(plan, path)) == match.group(1), 'Changed original runtime checksum input')
        seen.add(path)


def t15_runtime_environment(env):
    require(not any(key.startswith('PYTHON') and key != 'PYTHONDONTWRITEBYTECODE' for key in env),
            'T15 assertion-bearing runtime driver has ambient Python configuration')


def t15_runtime_json(text):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'Duplicate key in runtime replay output')
            value[key] = item
        return value
    return json.loads(text, object_pairs_hook=unique)


def t15_runtime_term(expr, arity, depth=0):
    """Serialize only the original Nat/Fin/add/mul/ifZero generated grammar."""
    require(depth <= 16 and type(expr) is list and expr and type(expr[0]) is str, 'Invalid generated runtime expression')
    tag = expr[0]
    if tag in {'c', 'v'}:
        require(len(expr) == 2 and type(expr[1]) is int and expr[1] >= 0, 'Invalid runtime natural scalar')
        if tag == 'c': return f'(.constant {expr[1]})'
        require(expr[1] < arity, 'Generated runtime variable is out of scope')
        return f'(.variable ⟨{expr[1]}, by decide⟩)'
    require(tag in {'add', 'mul', 'if0'} and len(expr) == (4 if tag == 'if0' else 3), 'Out-of-grammar generated runtime expression')
    return '(.' + {'add': 'add', 'mul': 'mul', 'if0': 'ifZero'}[tag] + ' ' + ' '.join(t15_runtime_term(child, arity, depth + 1) for child in expr[1:]) + ')'


def read_t15_runtime_prepared(plan, output):
    cases = t15_runtime_json(path_in(output, 'runtime/cases.json').read_text())
    report = t15_runtime_json(path_in(output, 'runtime/PREPARED_CASES.json').read_text())
    require(type(cases) is list and len(cases) == 720, 'Incomplete generated T15 runtime case set')
    parts = ['import IdentityChecker\nopen P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n']
    for n, case in enumerate(cases):
        require(type(case) is dict and set(case) == {'r', 'left', 'right', 'equal', 'witness'} and
                type(case['r']) is int and case['r'] == n // 120 and type(case['equal']) is bool, 'Changed T15 runtime case schema/order')
        r = case['r']; witness = case['witness']
        require((witness is None) == case['equal'], 'Runtime witness/verdict shape mismatch')
        if witness is not None:
            require(type(witness) is list and len(witness) == r and all(type(v) is int and v >= 0 for v in witness), 'Malformed runtime witness')
        left = t15_runtime_term(case['left'], r); right = t15_runtime_term(case['right'], r)
        parts.append(f'def e{n} : Expr {r} := {left}\ndef f{n} : Expr {r} := {right}\n')
        parts.append(f'#eval [identityCheck e{n} f{n}, verifyCertificate e{n} f{n} (makeCertificate e{n}), verifyCertificate e{n} e{n} (makeCertificate e{n})]\n')
    generated = ''.join(parts).encode()
    require(path_in(output, 'runtime/RuntimeAgreement.lean').read_bytes() == generated, 'Generated Lean source differs from the exact closed runtime grammar/cases')
    expected = {'seed': 151005, 'arities': list(range(6)), 'expression_pairs': len(cases),
                'equal_pairs': sum(c['equal'] for c in cases), 'unequal_pairs': sum(not c['equal'] for c in cases),
                'direct_expression_evaluations': sum(2 * 3 ** c['r'] for c in cases),
                'negative_witnesses_checked': sum(c['witness'] is not None for c in cases),
                'checker_sha256': T15_RUNTIME_CHECKER, 'lean_source_sha256': sha(generated),
                'lean_runtime_rows_verified': 0, 'formal_refinement_claim': False, 'scope': T15_RUNTIME_SCOPE}
    require(canonical(report) == canonical(expected), 'Prepared runtime counts/source binding/scope differ from actual generated cases')
    t15_runtime_data(plan, 'python-reference/certificate_checker.py')
    return {'cases': cases, 'report': report}


def read_t15_runtime_rows(text, cases):
    lines = text.splitlines()
    require(len(lines) == len(cases), 'Missing, duplicate or extra Lean runtime output rows')
    rows = []
    for line, case in zip(lines, cases):
        row = t15_runtime_json(line)
        require(type(row) is list and len(row) == 3 and all(type(x) is bool for x in row) and
                row == [case['equal'], case['equal'], True], 'Lean runtime Boolean observations differ from generated cases')
        rows.append(row)
    return rows


def check_t15_runtime_inputs(stage, plan, output, evidence):
    if stage['id'] == 'runtime-prepare': return
    require(stage['id'] in {'runtime-lean', 'runtime-verify'}, 'Unknown generated runtime phase')
    paths = T15_RUNTIME_PREPARED + (['runtime/lean-output.txt'] if stage['id'] == 'runtime-verify' else [])
    for path in paths:
        require(path in evidence['output_hashes'] and sha(path_in(output, path).read_bytes()) == evidence['output_hashes'][path],
                'Prior fresh runtime output is missing, unobserved, or changed')
    prepared = read_t15_runtime_prepared(plan, output)
    if stage['id'] == 'runtime-verify':
        read_t15_runtime_rows(path_in(output, 'runtime/lean-output.txt').read_text(), prepared['cases'])


def capture_t15_runtime_stdout(stage, log, output):
    require(stage['id'] == 'runtime-lean' and stage['output_paths'] == ['runtime/lean-output.txt'], 'Unapproved runtime output sink')
    target = path_in(output, 'runtime/lean-output.txt')
    require(not target.exists(), 'Runtime stdout sink is not fresh')
    # The original README redirects both stdout and stderr. Preserve the exact
    # accepted run_process combined log, including a partial failed attempt.
    with target.open('xb') as stream: stream.write(no_symlinks(log).read_bytes())


def check_t15_runtime_stage(stage, text, plan, output):
    prepared = read_t15_runtime_prepared(plan, output)
    if stage['id'] == 'runtime-prepare':
        require(canonical(t15_runtime_json(text)) == canonical(prepared['report']), 'Original preparation stdout differs from its actual output file')
    elif stage['id'] == 'runtime-lean':
        captured = path_in(output, 'runtime/lean-output.txt').read_text()
        require(captured == text, 'Captured original combined runtime stdout/log changed')
        read_t15_runtime_rows(captured, prepared['cases'])
    else:
        require(stage['id'] == 'runtime-verify', 'Unknown runtime completion stage')
        read_t15_runtime_rows(path_in(output, 'runtime/lean-output.txt').read_text(), prepared['cases'])
        actual = t15_runtime_json(path_in(output, 'runtime/VERIFIED_RESULT.json').read_text())
        expected = {**prepared['report'], 'lean_runtime_rows_verified': len(prepared['cases'])}
        require(canonical(actual) == canonical(expected) == canonical(t15_runtime_json(text)), 'Original verifier stdout/result differs from actual prepared cases and Lean rows')


def _validate_argv(stage, plan):
    argv = stage['argv']
    require(isinstance(argv, list) and argv and all(isinstance(a, str) and a and '\x00' not in a for a in argv), 'Missing explicit argument vector')
    driver = plan['drivers'].get(stage['driver_id'])
    if driver is not None:
        recipe = driver['recipe']
        if recipe in OPERATIONAL_RECIPES:
            operational_validate_argv(stage, plan)
            return
        if recipe in D04_RECIPES:
            d04_validate_argv(stage, driver, plan)
            return
        if recipe == portable_admission.RECIPE:
            portable_admission.validate_argv(_portable_api(), stage, driver, plan)
            return
        if recipe == CORE_RECIPE:
            validate_core_argv(stage, driver, plan)
            return
        if recipe == ATTR_RECIPE:
            validate_attribution_argv(stage, driver, plan)
            return
        if recipe == HISTORY_RECIPE:
            validate_history_argv(stage, driver, plan)
            return
        if recipe in T15_REFERENCE_RECIPES:
            validate_t15_reference_argv(stage, driver, plan)
            return
        if recipe == T15_RUNTIME_RECIPE:
            validate_t15_runtime_argv(stage, driver, plan)
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
    if p1_tail_finish_handles(suite): return p1_tail_finish_validate_suite(p1_api(), suite, sources, root)
    if p1_tail_handles(suite): return p1_tail_validate_suite(p1_api(), suite, sources, root)
    """Offline checks only. Neither a descriptor nor a review Boolean authorises code."""
    if selector_g1_handles(suite):
        family = selector_g1_load_family()
        return family.selector_g1_validate_suite(family.selector_g1_adapter_view(globals()), suite, sources, root)
    if isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_schema:
        return p1_validate_suite(p1_api(), suite, sources, root)
    try:
        operational_precheck(suite, sources)
        replay = suite['replay']; keys(replay, REPLAY_KEYS)
        require(replay['schema'] == 'orthemology-v5-replay-v1', 'Unknown replay schema')
        require(replay['scope'] in {'COMPONENTS', 'DECLARED_SUITE', 'FINITE'}, 'Unknown replay scope')
        if replay['scope'] == 'DECLARED_SUITE':
            require(APPROVED_DECLARED_SUITES.get(suite['id']) == declared_suite_fingerprint(suite, sources) or d04_declared_admitted(suite, sources), 'Complete original suite recipe has not been approved')
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
            if row['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE, portable_admission.RECIPE} | D04_RECIPES | OPERATIONAL_RECIPES:
                require(row['external_input_id'] in inputs, 'Original core archive is undeclared')
            else: require(row['external_input_id'] is None, 'Archive recipe is not approved by this adapter version')
            admitted_role = 'LOCK' if row['recipe'] == 't15-empirical-integrity-v1' else 'DRIVER'
            if row['recipe'] in OPERATIONAL_RECIPES: operational_validate_driver(row, source)
            elif row['recipe'] in D04_RECIPES: d04_check_driver_source(row['recipe'], source)
            elif row['recipe'] == portable_admission.RECIPE: portable_admission.validate_driver(_portable_api(), row, source)
            elif row['recipe'] == ATTR_RECIPE: check_custody_driver(source, ATTR_CONTRACT)
            elif row['recipe'] == HISTORY_RECIPE: check_custody_driver(source, HISTORY_CONTRACT)
            else: require(row['source_id'] in contents and files[row['source_id']]['role'] == admitted_role, 'Driver is not an exact projected source')
            if row['recipe'] in OPERATIONAL_RECIPES: pass
            elif row['recipe'] in D04_RECIPES:
                d04_validate_driver(row, sources)
            elif row['recipe'] in LANGUAGE_RECIPES:
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
            elif row['recipe'] in T15_REFERENCE_RECIPES:
                validate_t15_reference_driver(row, {'files': files, 'file_paths': file_paths, 'contents': contents})
            elif row['recipe'] == T15_RUNTIME_RECIPE:
                validate_t15_runtime_driver(row, {'files': files, 'file_paths': file_paths, 'contents': contents})
            elif row['recipe'] in NORMAL_SOURCE_RECIPES:
                require(NORMAL_SOURCE_RECIPES[row['recipe']] == row['sha256'] and row['argument_meanings'] == {}, 'Changed original source-check recipe')
            elif row['recipe'] == portable_admission.RECIPE:
                portable_admission.validate_driver(_portable_api(), row, source)
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
        operational_validate_package(suite, sources, plan)
        for name in plan['build_roots']:
            relative(name); require(name != 'project' and not name.startswith('project/'), 'Build root overlaps projected sources')
        for driver in drivers.values():
            if driver['recipe'] in NORMAL_SOURCE_RECIPES: source_checker_inputs(driver, plan)
            if driver['recipe'] == 't14-identity-verify_sources-v1': check_checksum_manifest(plan, 90)
        if any(row['recipe'] in D04_RECIPES for row in drivers.values()): d04_validate_package(suite, plan, sources)
        if any(row['recipe'] in T15_SOURCE_RECIPES for row in drivers.values()): validate_t15_package(suite, plan)
        if any(row['recipe'] in T15_REFERENCE_RECIPES for row in drivers.values()): validate_t15_reference_package(suite, plan, sources)
        if any(row['recipe'] == T15_RUNTIME_RECIPE for row in drivers.values()): validate_t15_runtime_package(suite, plan, sources)
        if any(row['recipe'] in T10_FINITE_RECIPES for row in drivers.values()): validate_t10_package(suite, plan)
        if any(row['recipe'] == CORE_RECIPE for row in drivers.values()): validate_core_package(suite, plan)
        if any(row['recipe'] == ATTR_RECIPE for row in drivers.values()): validate_attribution_package(suite, plan)
        if any(row['recipe'] == HISTORY_RECIPE for row in drivers.values()): validate_history_package(suite, plan)
        if any(row['recipe'] == portable_admission.RECIPE for row in drivers.values()): portable_admission.validate_package(_portable_api(), suite, plan)
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
                custody_literal = custody_literal or d04_diagnostic_allowed(driver, diagnostic)
                custody_literal = custody_literal or (driver.get('recipe') == portable_admission.RECIPE and portable_admission.diagnostic(_portable_api(), diagnostic, sources))
                custody_literal = custody_literal or operational_diagnostic(stage, diagnostic, plan)
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
    if isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_schema:
        return p1_project_suite(p1_api(), suite, sources, root, output)
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


def _stop_process_group(proc):
    """Stop the owned group even when its leader exits during termination."""
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        try: proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill(); proc.wait()
        return
    try: os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError: pass
    try:
        try: proc.wait(timeout=2)
        except subprocess.TimeoutExpired: pass
    finally:
        # A completed leader wait does not imply that its descendants stopped.
        try: os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        proc.wait()


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
            _stop_process_group(proc)
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
    original_owned = any(row['recipe'] in {CORE_RECIPE, ATTR_RECIPE, HISTORY_RECIPE, portable_admission.RECIPE} | D04_RECIPES | OPERATIONAL_RECIPES for row in plan['drivers'].values())
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
    if p1_tail_finish_handles(suite): return p1_tail_finish_execute_suite(p1_api(), suite, sources, root, output, tools, inputs, scope=scope, reviews=reviews)
    if p1_tail_handles(suite): return p1_tail_execute_suite(p1_api(), suite, sources, root, output, tools, inputs, scope=scope, reviews=reviews)
    if selector_g1_handles(suite):
        family = selector_g1_load_family()
        return family.selector_g1_execute(family.selector_g1_adapter_view(globals()), suite, sources, root, output, tools, inputs, scope, reviews=reviews)
    if isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_schema:
        return p1_execute_suite(p1_api(), suite, sources, root, output, tools, inputs, scope, reviews)
    require(not portable_admission.is_portable(suite), 'Portable views require the single physical family executor')
    if d04_is_suite(suite): return d04_execute_suite(suite, sources, root, output, tools, inputs, scope, reviews=reviews)
    if isinstance(suite, dict) and isinstance(suite.get('id'), str) and suite['id'] in _OPERATIONAL_DATA['suites']:
        return operational_execute_suite(suite, sources, root, output, tools, inputs, scope, reviews=reviews)
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
                if recipe == T15_RUNTIME_RECIPE:
                    t15_runtime_environment(env)
                    check_t15_runtime_inputs(stage, plan, output, evidence)
                if recipe in T15_REFERENCE_RECIPES:
                    run = run_t15_reference_stage(stage, argv, launch_cwd, stage_environment(stage, plan, output, env), log, stage['timeout_seconds'], plan, project)
                else:
                    run = run_process(argv, launch_cwd, stage_environment(stage, plan, output, env), log, stage['timeout_seconds'])
                if recipe == T15_RUNTIME_RECIPE and sid == 'runtime-lean': capture_t15_runtime_stdout(stage, log, output)
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
            if recipe in T15_REFERENCE_RECIPES: check_t15_reference_stage(stage, text, plan)
            if recipe == T15_RUNTIME_RECIPE: check_t15_runtime_stage(stage, text, plan, output)
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



HC_SCHEMA = 'orthemology-v5-history-audit-continuation-v1'
HC_SUITE = 'D04-T07-HISTORY-ORIGINAL'
HC_SUITE_SHA256 = 'c5a8b9fd56f2ba8c53866902ac7b3c484613678e0679a5d2f2447df0b1983d1f'
HC_APPROVAL = 'a0e55482d8bf7f6d9b5b77ee37d99ce54a5b27945cd7d816f9d00cb6d61711df'
HC_ORIGINAL_RUNNER = 'd0abd261c37cc8dee4c34a8c5b74be6f8079237680bf518ddc0c2d0b51a1d65c'
HC_TRACE = '9826bd11df643d8b89b07668c2d10f4d58164b95e3cadd5271f673d43725d9eb'
HC_RETAINED_TREE = 'ad701f3907e168ba62774e276796242ae64bf75508d75d54a650b4b3a2e88a19'
HC_PROJECT_TREE = '56ed0c004dcb31d2548cc4da1fd18d931752991532a3a58d448daa77cb2cb47b'
HC_AUDIT_SOURCE = '3911f7c0b3238a647879f7598042837beee62a71d337c38a921c2ec6b0af9300'
# Exact complete offline collection, reconciled to the retained source/captures.
HC_COLLECTION_SHA256 = 'e4106e2948e59f7b4c99e4f383919f62d7f5255d189adb18c47d5081f287b810'
HC_SOURCE_AUDIT_SHA256 = 'b1490cd37087246e724db545da4d8f567993ba0f78d4bd82d7c56b90803e839e'
HC_REVIEWED_EXECUTOR_HASHES = frozenset({'8da2b65123a442cf6ccc2f97702b9b899c5ce4d7ca738260061ac5213121a239'})
HC_CACHE_POLICY = 'PINNED_OFFICIAL_CACHES_REUSED_CAMPAIGN_EXECUTION_FRESH_COLLECTION_AND_AUDIT'
HC_PRIOR = {
    'receipt_sha256': 'd7d6637266cef987c04138390571bfd854151d4d1c8e05e681986b635018a53a',
    'receipt_canonical_sha256': 'b5b425d462f87f378a6d3fffd4e28b93d1a41e2cf8e4bae9e32d22249081ff4b',
    'receipt_bytes': 27543,
    'failure_record_sha256': 'c5f860f06173146b224c1ea6318479c3aabe54b85a76561ceb336a0c418e2886',
    'original_receipt_sha256': '843c7cacb88fabb73fc9edee61ca560a7bbf456b7037968d8f21cd76ecc48d95',
    'original_receipt_canonical_sha256': 'f9365626bc5d339f3674d1dbac6075e73c32f6c10dc6962f658f696db47dc36a',
    'original_receipt_bytes': 5585,
}
HC_OBJECTS = {
    'original/build/HistoryInvariant.olean': '98e4fb02229c9ba201a0c146d473e24dad3c387f8e30ea98033986746d6dc6b6',
    'original/build/HistoryModel.olean': '49edb6394209cf07c7c2603ef1e016a7b188d0e266a178130723d5557c3f33f0',
    'original/build/HistorySafety.olean': '811a4b785d2b95c9cc98423cf1e277cfa0fe4d0f81b0c0fc17d0e15790f362bd',
    'original/build/HistoryTrace.olean': '13490150fffe6c6689c467dac2c62baf0752d8ea49c07dd0f00d816976d52713',
    'original/build/NegativeControls.olean': 'e08485587d16ce4b89820c6100dd968b15f712583dbe3db6c1bf611742aaeaf2',
}
HC_RECEIPT_KEYS = set('id suite_id family suite_sha256 source_hashes review_hashes toolchain_sha256 outcome target_readbacks controls stages invocation started_at ended_at exit_code log_sha256 axioms proof_scope replay_evidence'.split())
HC_EVIDENCE_KEYS = set('schema descriptor_sha256 closure_sha256 runner_sha256 source_hashes_before source_hashes_after import_fingerprints tool_fingerprints dependency_checks stage_results target_audits output_hashes cache_policy prior retained_input_checks fresh_audit accounting retained_collection'.split())
HC_COLLECTION_KEYS = set('parser_id parser_revision collector_runner_sha256 observed_at driver_invocations child_observations stage_results control_diagnostics output_hashes source_audit_sha256'.split())
HC_RETAINED_KEYS = set('mode stage_ids physical_trace_sha256 original_result_sha256 child_ledger_sha256 driver_invocations_sha256 archive_sha256 retained_tree_before_sha256 retained_tree_after_sha256 project_sources_before_sha256 project_sources_after_sha256 custom_objects_before custom_objects_after official_cache_measurements'.split())
HC_STAGE_KEYS = set('id argv cwd budget_seconds started_at ended_at terminal exit_code log_sha256 output_hashes'.split())
HC_FRESH_KEYS = set('recipe generated_source_sha256 resolved_invocation_sha256 argv_provenance traversal_bound distinct_declaration_accounting fresh_custom_objects'.split())
HC_AUDIT_KEYS = set('target_id name type_sha256 axioms closure_status checked_declarations stage_id log_sha256'.split())
HC_ACCOUNTING = {'reused_source_owned_physical_runs': 1, 'reused_child_executions': 17, 'reused_custom_objects': 5,
    'reused_source_scenarios': 7, 'new_source_owned_physical_runs': 0, 'new_child_compilations': 0,
    'new_custom_objects': 0, 'new_target_audit_processes': 1, 'independent_evidence_increment': 0}


def _hc_require(value, message):
    if not value: raise ValueError(message)


def _hc_keys(value, expected):
    _hc_require(isinstance(value, dict) and set(value) == expected, 'Unknown or missing history continuation fields')


def _hc_time(value):
    _hc_require(isinstance(value, str) and value.endswith('Z'), 'History continuation time is not UTC')
    return datetime.fromisoformat(value[:-1] + '+00:00')


def _hc_collection_digest(collection, adapter):
    # Capture times and the original physical runner remain included. Only new
    # parser attribution/times vary when exact original bytes are read again.
    content = {key: value for key, value in collection.items() if key not in {'collector_runner_sha256', 'observed_at'}}
    content['child_observations'] = [{k: v for k, v in row.items() if k != 'observed_at'} for row in collection['child_observations']]
    content['stage_results'] = [{k: v for k, v in row.items() if k not in {'started_at', 'ended_at'}} for row in collection['stage_results']]
    return adapter.canonical(content)


def _hc_prior(evidence, suite, sources, root, adapter, plan):
    binding = evidence['prior']; _hc_keys(binding, set(HC_PRIOR) | {'receipt'})
    _hc_require(type(binding['receipt_bytes']) is int and type(binding['original_receipt_bytes']) is int
             and all(binding[key] == value for key, value in HC_PRIOR.items()), 'Changed history prior trust anchor')
    prior = binding['receipt']; _hc_keys(prior, HC_RECEIPT_KEYS)
    _hc_require(adapter.canonical(prior) == HC_PRIOR['receipt_canonical_sha256'], 'Changed original failed history receipt')
    old = prior['replay_evidence']
    _hc_require(prior['outcome'] == 'FAILED' and prior['proof_scope'] == 'NONE'
             and type(prior['exit_code']) is int and prior['exit_code'] == 1
             and old['schema'] == 'orthemology-v5-replay-evidence-v2'
             and old['runner_sha256'] == HC_ORIGINAL_RUNNER, 'Original failed history semantics changed')
    # Only the unchanged FAILED original is sent through the ordinary v2 branch.
    adapter.validate_receipt(prior, suite, sources, root)
    stages = adapter.indexed(old['stage_results'])
    _hc_require(list(stages) == ['_prerequisites', *plan['stages'], '_target_audit'], 'Changed original history stage inventory')
    for sid, row in stages.items():
        executed = sid in {'_prerequisites', 'original-driver'}
        _hc_require((row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == 0)
                 if executed else (row['terminal'] == 'SKIPPED' and row['exit_code'] is None
                                   and row['log_sha256'] == adapter.sha(b'')), 'Ineligible original history stage')
        _hc_require(row['output_hashes'] == {}, 'Original collection already claimed outputs')
    _hc_require(all(old[key] == [] for key in ('child_observations', 'control_diagnostics', 'target_audits'))
             and old['output_hashes'] == {} and prior['controls'] == []
             and prior['target_readbacks'] == [] and prior['axioms'] == [], 'Partial original collection cannot be generalized')
    launches = old['driver_invocations']
    _hc_require(len(launches) == 1 and launches[0]['trace_sha256'] == HC_TRACE
             and type(launches[0]['child_count']) is int and launches[0]['child_count'] == 17,
             'Original history physical capture differs')
    return prior, old, stages


def _hc_collection(receipt, evidence, prior, old, old_stages, plan, suite, adapter):
    collection = evidence['retained_collection']; _hc_keys(collection, HC_COLLECTION_KEYS)
    _hc_require(collection['parser_id'] == 't07-history-original-v1'
             and collection['parser_revision'] == 'history-source-bound-import-readbacks-v2'
             and collection['collector_runner_sha256'] == evidence['runner_sha256'], 'Unreviewed history collector identity')
    _hc_require(HC_COLLECTION_SHA256 is not None and HC_SOURCE_AUDIT_SHA256 is not None,
             'Actual D03 collection/source-readback pins are not installed')
    _hc_require(collection['source_audit_sha256'] == HC_SOURCE_AUDIT_SHA256
             and _hc_collection_digest(collection, adapter) == HC_COLLECTION_SHA256, 'Changed complete history capture/source collection')
    _hc_require(collection['driver_invocations'] == old['driver_invocations'], 'Old physical runner relabelled as collector')
    observed = adapter.indexed(collection['stage_results'])
    declared = {sid: row for sid, row in plan['stages'].items() if sid != 'original-driver'}
    _hc_require(list(observed) == list(declared), 'Missing or reordered history collection stages')
    start, end = _hc_time(receipt['started_at']), _hc_time(receipt['ended_at'])
    parsed = _hc_time(collection['observed_at'])
    audit_start = _hc_time(adapter.indexed(evidence['stage_results'])['_target_audit']['started_at'])
    _hc_require(_hc_time(prior['ended_at']) < start <= parsed <= audit_start <= end, 'Collection is not a new pre-audit observation')
    assembled = {sid: old_stages[sid] for sid in ('_prerequisites', 'original-driver')}
    for sid, row in observed.items():
        _hc_keys(row, HC_STAGE_KEYS); expected = declared[sid]
        _hc_require(row['argv'] == expected['argv'] and row['cwd'] == expected['cwd']
                 and type(row['budget_seconds']) is int and row['budget_seconds'] == expected['timeout_seconds']
                 and row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int
                 and row['exit_code'] in expected['expected_exit_codes'] and row['output_hashes'] == {}
                 and set(expected['depends_on']) <= set(assembled), 'Unfulfilled or executing history collection stage')
        _hc_require(parsed <= _hc_time(row['started_at']) <= _hc_time(row['ended_at']) <= audit_start,
                 'History observation interval outside fresh collection')
        adapter.digest(row['log_sha256']); assembled[sid] = row
    children = adapter.indexed(collection['child_observations'], 'stage_id')
    _hc_require(list(children) == list(declared), 'Missing or reordered physical history children')
    # A separate NONEXECUTING collection view uses the old physical runner. It is
    # never a rewritten receipt and is never passed as a successful v2 receipt.
    view = {'runner_sha256': old['runner_sha256'], 'driver_invocations': collection['driver_invocations'],
        'child_observations': collection['child_observations'], 'output_hashes': collection['output_hashes']}
    adapter.validate_child_evidence(view, plan, assembled, True)
    objects = {}
    for child in children.values():
        _hc_require(parsed <= _hc_time(child['observed_at']) <= audit_start, 'History child uses an old/new execution time as observation')
        for path, digest in child['output_hashes'].items():
            _hc_require(path not in objects, 'Duplicate history object producer'); objects[path] = digest
    _hc_require(objects == collection['output_hashes'] == HC_OBJECTS, 'Changed retained five-object producer union')
    diagnostics = adapter.indexed(collection['control_diagnostics'], 'control_id')
    controls = adapter.indexed(suite['controls'])
    _hc_require(set(diagnostics) == set(controls), 'Incomplete retained history control diagnostics')
    expected_controls = {}
    for sid, stage in declared.items():
        for cid in stage['control_ids']:
            row = diagnostics[cid]; actual = observed[sid]; expected = controls[cid]
            _hc_keys(row, set('control_id stage_id prerequisite_stage_ids expected observed_log_sha256 match'.split()))
            _hc_require(row == {'control_id': cid, 'stage_id': sid, 'prerequisite_stage_ids': stage['depends_on'],
                'expected': stage['expected_diagnostics'], 'observed_log_sha256': actual['log_sha256'], 'match': 'MATCHED'},
                'Wrong retained history diagnostic/source association')
            expected_controls[cid] = {key: expected[key] for key in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
                'actual_outcome': expected['expected_outcome'], 'actual_outcome_sha256': adapter.sha(expected['expected_outcome'].encode()),
                'terminal': actual['terminal'], 'exit_code': actual['exit_code'], 'log_sha256': actual['log_sha256']}
    _hc_require(receipt['controls'] == [expected_controls[row['id']] for row in suite['controls']]
             and all(type(row['exit_code']) is int for row in receipt['controls']), 'History controls lack exact retained child evidence')
    return collection


def _hc_retained(checks, collection, suite, plan, adapter):
    _hc_keys(checks, HC_RETAINED_KEYS)
    expected = {'mode': 'REUSED_CAMPAIGN_EXECUTION', 'stage_ids': ['_prerequisites', 'original-driver'],
        'physical_trace_sha256': HC_TRACE, 'original_result_sha256': HC_PRIOR['original_receipt_sha256'],
        'child_ledger_sha256': adapter.canonical(collection['child_observations']),
        'driver_invocations_sha256': adapter.canonical(collection['driver_invocations']),
        'archive_sha256': suite['replay']['external_inputs'][0]['expected_sha256'],
        'retained_tree_before_sha256': HC_RETAINED_TREE, 'retained_tree_after_sha256': HC_RETAINED_TREE,
        'project_sources_before_sha256': HC_PROJECT_TREE, 'project_sources_after_sha256': HC_PROJECT_TREE,
        'custom_objects_before': HC_OBJECTS, 'custom_objects_after': HC_OBJECTS}
    _hc_require(all(checks[key] == value for key, value in expected.items()), 'Changed retained history inputs')
    caches = adapter.indexed(checks['official_cache_measurements'], 'root_id')
    _hc_require(set(caches) == {'lean'} | set(plan['packages']), 'Missing/foreign history official cache root')
    for row in caches.values():
        _hc_keys(row, set('root_id measurement_phase tree_before_sha256 tree_after_sha256 file_count cache_policy'.split()))
        _hc_require(row['measurement_phase'] == 'CONTINUATION_ONLY' and type(row['file_count']) is int, 'Cache time/count differs')
        if row['cache_policy'] == 'ABSENT_UNIMPORTED_PINNED_PACKAGE_CACHE':
            _hc_require(row['root_id'] == 'Cli' and row['file_count'] == 0 and row['tree_before_sha256'] == adapter.canonical({})
                     and not any(item['package'] == 'Cli' for item in plan['official'].values()), 'Wrong absent history package cache')
        else:
            _hc_require(row['cache_policy'] == 'TRUSTED_PINNED_OFFICIAL_CACHE' and row['file_count'] > 0, 'Wrong history official cache policy')
        adapter.digest(row['tree_before_sha256']); adapter.digest(row['tree_after_sha256'])
        _hc_require(row['tree_before_sha256'] == row['tree_after_sha256'], 'Official history cache changed')


def _hc_fresh(receipt, evidence, prior, adapter):
    stages = adapter.indexed(evidence['stage_results'])
    _hc_require(list(stages) == ['_prerequisites', '_target_audit'], 'Fresh history ledger relabels or reruns original work')
    start, end = _hc_time(receipt['started_at']), _hc_time(receipt['ended_at'])
    _hc_require(_hc_time(prior['ended_at']) < start <= end, 'Old or reversed history continuation interval')
    last = start
    for sid, row in stages.items():
        _hc_keys(row, HC_STAGE_KEYS)
        argv = ['{builtin:prerequisites}'] if sid == '_prerequisites' else ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean']
        _hc_require(row['argv'] == argv and row['cwd'] == '.' and type(row['budget_seconds']) is int
                 and row['budget_seconds'] == (30 if sid == '_prerequisites' else 300), 'Changed fresh history invocation/budget')
        rs, re = _hc_time(row['started_at']), _hc_time(row['ended_at'])
        _hc_require(last <= rs <= re <= end, 'Invalid fresh history stage interval'); last = re
        _hc_require(row['terminal'] in {'COMPLETED', 'TIMEOUT', 'INTERRUPTED'}, 'Missing actual history audit process')
        if row['terminal'] == 'COMPLETED':
            _hc_require(type(row['exit_code']) is int and 0 <= row['exit_code'] < 124, 'Invalid fresh history exit')
        else: _hc_require(row['exit_code'] is None, 'Resource failure receives concrete exit credit')
        adapter.digest(row['log_sha256']); _hc_require(row['output_hashes'] == {}, 'New history custom object falsely claimed')
    pre = stages['_prerequisites']
    _hc_require(pre['terminal'] == 'COMPLETED' and pre['exit_code'] == 0, 'New history prerequisites not established')
    _hc_require(receipt['stages'] == [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')}
                                  for row in evidence['stage_results']]
             and receipt['log_sha256'] == adapter.canonical({sid: row['log_sha256'] for sid, row in stages.items()}),
             'Top/fresh history stage or log association differs')
    return stages['_target_audit']


def _hc_validate(receipt, suite, sources, root, adapter):
    json.dumps(receipt, ensure_ascii=False, allow_nan=False)
    _hc_keys(receipt, HC_RECEIPT_KEYS)
    _hc_require(suite['id'] == HC_SUITE and adapter.canonical(suite) == HC_SUITE_SHA256
             and adapter.APPROVED_DECLARED_SUITES.get(HC_SUITE) == HC_APPROVAL, 'Wrong approved history suite')
    plan = adapter.validate_suite(suite, sources, root)
    evidence = receipt['replay_evidence']; _hc_keys(evidence, HC_EVIDENCE_KEYS)
    _hc_require(evidence['schema'] == HC_SCHEMA and evidence['cache_policy'] == HC_CACHE_POLICY, 'Wrong history continuation schema/policy')
    prior, old, old_stages = _hc_prior(evidence, suite, sources, root, adapter, plan)
    _hc_require(isinstance(receipt['id'], str) and receipt['id'].startswith(HC_SUITE + '-audit-continuation-')
             and len(receipt['id']) > len(HC_SUITE + '-audit-continuation-') and receipt['id'] != prior['id'], 'History continuation needs a new identity')
    _hc_require(receipt['invocation'] == ['replay_v5_successors.py', '--history-audit-continuation', '--suite', HC_SUITE,
                                        '--prior', '{prior}', '--out', '{out}'], 'Not the audit-only history invocation')
    for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256'):
        _hc_require(receipt[key] == prior[key], 'Changed history suite/source/review/toolchain binding')
    for key in ('descriptor_sha256', 'closure_sha256', 'source_hashes_before', 'source_hashes_after',
                'import_fingerprints', 'tool_fingerprints', 'dependency_checks'):
        _hc_require(evidence[key] == old[key], 'Changed history source/import/tool/dependency identity')
    adapter.digest(evidence['runner_sha256'])
    _hc_require((evidence['runner_sha256'] == adapter.sha(Path(adapter.__file__).read_bytes())
                 or evidence['runner_sha256'] in HC_REVIEWED_EXECUTOR_HASHES)
             and evidence['runner_sha256'] != HC_ORIGINAL_RUNNER, 'Unreviewed history continuation executor')
    audit = _hc_fresh(receipt, evidence, prior, adapter)
    collection = _hc_collection(receipt, evidence, prior, old, old_stages, plan, suite, adapter)
    _hc_retained(evidence['retained_input_checks'], collection, suite, plan, adapter)
    _hc_keys(evidence['accounting'], set(HC_ACCOUNTING))
    _hc_require(all(type(evidence['accounting'][key]) is int and evidence['accounting'][key] == value
                 for key, value in HC_ACCOUNTING.items()), 'Invented history build/run/independence credit')
    fresh = evidence['fresh_audit']; _hc_keys(fresh, HC_FRESH_KEYS)
    generated = adapter.sha(adapter._audit_source(list(plan['targets'].values())).encode())
    _hc_require(generated == HC_AUDIT_SOURCE and fresh['generated_source_sha256'] == generated
             and fresh['recipe'] == 'history-retained-closure-audit-v1' and fresh['argv_provenance'] == 'RESOLVED_FROM_BOUND_INPUTS'
             and type(fresh['traversal_bound']) is int and fresh['traversal_bound'] == 1000000
             and fresh['distinct_declaration_accounting'] == 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED'
             and type(fresh['fresh_custom_objects']) is int and fresh['fresh_custom_objects'] == 0,
             'Changed history auditor or false fresh custom builds')
    adapter.digest(fresh['resolved_invocation_sha256'])
    _hc_require(evidence['output_hashes'] == {'generated/V5SuccessorReadback.lean': generated}, 'Wrong new history audit outputs')
    successful = receipt['outcome'] == 'QUALIFIED_DECLARED_SUITE'
    if not successful:
        expected = 'FAILED' if audit['terminal'] == 'COMPLETED' else 'RESOURCE_INCONCLUSIVE'
        _hc_require(receipt['outcome'] == expected and receipt['proof_scope'] == 'NONE'
                 and type(receipt['exit_code']) is int and receipt['exit_code'] == 1
                 and (audit['terminal'] != 'COMPLETED' or audit['exit_code'] > 0)
                 and receipt['target_readbacks'] == [] and evidence['target_audits'] == [] and receipt['axioms'] == [],
                 'Failed history audit acquired qualification/partial target credit')
    else:
        _hc_require(receipt['proof_scope'] == 'DECLARED_SUITE' and type(receipt['exit_code']) is int
                 and receipt['exit_code'] == 0 and audit['terminal'] == 'COMPLETED' and audit['exit_code'] == 0,
                 'History audit not fully successful')
        audits = adapter.indexed(evidence['target_audits'], 'target_id')
        _hc_require(set(audits) == set(plan['targets']), 'Missing or foreign history target audit')
        axes = set()
        for tid, row in audits.items():
            _hc_keys(row, HC_AUDIT_KEYS)
            _hc_require(row['name'] == plan['targets'][tid]['name'] and row['closure_status'] == 'CHECKED_SAFE'
                     and type(row['checked_declarations']) is int and row['checked_declarations'] > 0
                     and row['stage_id'] == '_target_audit' and row['log_sha256'] == audit['log_sha256'], 'Wrong history target/log/safe-closure association')
            adapter.digest(row['type_sha256'])
            _hc_require(isinstance(row['axioms'], list) and len(set(row['axioms'])) == len(row['axioms'])
                     and set(row['axioms']) <= adapter.AXIOMS, 'Unapproved or repeated history target axiom')
            axes.update(row['axioms'])
        expected = [{'target_id': row['id'], 'source_id': row['source_id'], 'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']]
        _hc_require(receipt['target_readbacks'] == expected and receipt['axioms'] == sorted(axes), 'Wrong history source/readback/axiom summary')
    return {'suite_id': HC_SUITE, 'outcome': receipt['outcome'], 'scope': 'HISTORY_CONTINUATION_ENVELOPE_AND_PRIOR_ELIGIBILITY_ONLY'}


def validate_history_continuation(receipt, suite, sources, root, *, adapter):
    """Validate the exact history02 composition, without running or rewriting it."""
    try:
        return _hc_validate(receipt, suite, sources, root, adapter)
    except (TypeError, KeyError, IndexError, OverflowError) as error:
        raise ValueError('Malformed history continuation envelope') from error


def _hc_exec_prior(prior, adapter):
    a = adapter; raw = a.path_in(prior, 'RECEIPT.json').read_bytes()
    a.require(len(raw) == a.HC_PRIOR['receipt_bytes'] and a.sha(raw) == a.HC_PRIOR['receipt_sha256'], 'Wrong original history receipt bytes')
    receipt = json.loads(raw)
    a.require(a.canonical(receipt) == a.HC_PRIOR['receipt_canonical_sha256'], 'Wrong original history receipt value')
    original = a.path_in(prior, 'original/REPLAY_RECEIPT.json').read_bytes()
    a.require(len(original) == a.HC_PRIOR['original_receipt_bytes'] and a.sha(original) == a.HC_PRIOR['original_receipt_sha256']
              and a.canonical(json.loads(original)) == a.HC_PRIOR['original_receipt_canonical_sha256'], 'Changed source-owned history terminal')
    a.require(a.sha(a.path_in(prior, 'FAILURE.json').read_bytes()) == a.HC_PRIOR['failure_record_sha256'], 'Changed history collection failure')
    return {**a.HC_PRIOR, 'receipt': receipt}


def _hc_exec_retained(prior, plan, suite, adapter):
    a = adapter; _, tree = _ac_exec_inventory(prior, a)
    a.require(tree == a.HC_RETAINED_TREE, 'Retained history run changed')
    project = a.path_in(prior, 'project'); _, projected = _ac_exec_inventory(project, a)
    a.require(projected == a.HC_PROJECT_TREE, 'Retained history projection changed')
    for sid, row in plan['files'].items():
        a.require(a.path_in(project, row['path']).read_bytes() == plan['contents'][sid], 'Retained history selected source changed')
    objects = _ac_exec_objects(prior, a.HC_OBJECTS, suite['replay']['build_roots'], a)
    return tree, projected, objects


def _hc_exec_generate(output, plan, adapter):
    a = adapter; raw = a._audit_source(list(plan['targets'].values())).encode('utf-8')
    a.require(a.sha(raw) == a.HC_AUDIT_SOURCE, 'Changed history audit generator')
    folder = a.path_in(output, 'generated'); a.require(not folder.exists(), 'History generated audit must be fresh')
    folder.mkdir(); path = folder / 'V5SuccessorReadback.lean'
    with path.open('xb') as stream: stream.write(raw)
    a.require(a.sha(path.read_bytes()) == a.HC_AUDIT_SOURCE, 'History audit source readback changed')
    return path


def _hc_exec_source_audit(suite, plan, prior, old, adapter):
    a = adapter; rows = []
    for name, spec in plan['history_children'].items():
        if name in a.HISTORY_CLAIMS or name == 'source-replay': continue
        sid = spec['source_id']; body = plan['contents'][sid]
        names = a.source_readback_names_in_plan(sid, plan)
        log = a.path_in(prior, spec['log']); a.check_original_readbacks(log.read_text(), names)
        closure = set(); queue = [name]
        while queue:
            current = queue.pop()
            if current in closure or current not in plan['modules']: continue
            closure.add(current); queue.extend(plan['modules'][current]['imports'])
        owners = {}
        for owner in sorted(closure):
            owner_id = plan['modules'][owner]['source_id']
            declarations, _ = a._readback_source_symbols(plan['contents'][owner_id].decode())
            for declared, line in declarations:
                if declared in names:
                    owners.setdefault(declared, []).append({'module': owner, 'source_id': owner_id,
                        'source_sha256': a.sha(plan['contents'][owner_id]), 'line': line + 1})
        a.require(set(owners) == set(names) and all(len(value) == 1 for value in owners.values()), 'History readback declaration owner is not unique')
        rows.append({'module': name, 'source_id': sid, 'source_sha256': a.sha(body), 'expected_names': names,
            'declaration_owners': owners, 'log_sha256': a.sha(log.read_bytes()), 'axioms_checked': True,
            'import_closure': [{'module': n, 'source_sha256': a.sha(plan['contents'][plan['modules'][n]['source_id']]),
                               'imports': plan['modules'][n]['imports']} for n in sorted(closure)]})
    return {'schema': 'history-source-bound-readback-audit-v1', 'parser_revision': 'history-source-bound-import-readbacks-v2',
        'suite_sha256': a.canonical(suite), 'original_receipt_sha256': a.sha(a.path_in(prior, 'original/REPLAY_RECEIPT.json').read_bytes()),
        'readbacks': rows, 'literal_print_count': sum(len(row['expected_names']) for row in rows),
        'source_hashes': old['source_hashes_before'], 'scope': 'OFFLINE_SOURCE_AND_RETAINED_LOG_ASSOCIATION_NO_NEW_EXECUTION'}


def _hc_exec_collection(suite, plan, prior, old, resolved, tools, adapter):
    a = adapter; observed_at = a.utc(); driver = next(iter(plan['drivers'].values())); iid = driver['external_input_id']
    archive = a.path_in(prior, 'archives/' + iid); a.history_source_check(archive, plan)
    stages = a.indexed(old['stage_results']); stage = plan['stages']['original-driver']; parent = stages['original-driver']
    mappings = {'project': prior / 'project', 'out': prior, 'build': prior / 'build', 'archive:' + iid: archive,
        'driver:' + driver['id']: archive / 'replay.py', 'tool:lean': resolved['lean'], 'tool:python': resolved['python'],
        'dependency:mathlib': tools['mathlib']}
    parent_log = a.path_in(prior, 'logs/original-driver.log')
    a.require(a.sha(parent_log.read_bytes()) == parent['log_sha256'], 'Retained history parent log changed')
    children, invocation, objects = a.history_collect_children(stage, parent, parent_log.read_text(), plan, prior, mappings)
    physical = old['driver_invocations'][0]
    a.require({**invocation, 'runner_sha256': physical['runner_sha256']} == physical, 'Physical history invocation cannot be relabelled')
    source_audit = _hc_exec_source_audit(suite, plan, prior, old, a)
    collection = {'parser_id': a.HISTORY_RECIPE, 'parser_revision': 'history-source-bound-import-readbacks-v2',
        'collector_runner_sha256': a.sha(Path(a.__file__).read_bytes()), 'observed_at': observed_at,
        'driver_invocations': [physical], 'child_observations': [], 'stage_results': [], 'control_diagnostics': [],
        'output_hashes': objects, 'source_audit_sha256': a.canonical(source_audit)}
    completed = {sid: {**row, 'matched': True} for sid, row in stages.items() if row['terminal'] == 'COMPLETED'}
    for sid, spec in list(plan['stages'].items())[1:]:
        started = a.utc(); observed = children[tuple(spec['argv'][1:])]
        log = a.path_in(prior, plan['history_children'][spec['argv'][2]]['log'])
        a.require(a.sha(log.read_bytes()) == observed['log_sha256'], 'Retained history child log changed')
        run = {'terminal': observed['terminal'], 'exit_code': observed['exit_code'], 'started_at': started,
               'ended_at': a.utc(), 'log_sha256': observed['log_sha256']}
        a.assess_stage(spec, run, log.read_text(), completed)
        collection['child_observations'].append({**observed, 'stage_id': sid, 'observed_at': run['ended_at']})
        collection['stage_results'].append({**stages[sid], **run})
        completed[sid] = {**run, 'matched': True}
        for cid in spec['control_ids']:
            collection['control_diagnostics'].append({'control_id': cid, 'stage_id': sid, 'prerequisite_stage_ids': spec['depends_on'],
                'expected': spec['expected_diagnostics'], 'observed_log_sha256': run['log_sha256'], 'match': 'MATCHED'})
    a.require(a.canonical(source_audit) == a.HC_SOURCE_AUDIT_SHA256 and a._hc_collection_digest(collection, a) == a.HC_COLLECTION_SHA256,
              'Complete source-bound history collection changed')
    return collection, source_audit


def _hc_exec_controls(suite, plan, collection, adapter):
    a = adapter; stages = a.indexed(collection['stage_results']); controls = {}
    for sid, stage in plan['stages'].items():
        if sid not in stages: continue
        for cid in stage['control_ids']:
            a.require(cid not in controls, 'Duplicate retained history control')
            controls[cid] = stages[sid]
    a.require(set(controls) == {row['id'] for row in suite['controls']}, 'Incomplete collected history controls')
    return [{key: row[key] for key in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
        'actual_outcome': row['expected_outcome'], 'actual_outcome_sha256': a.sha(row['expected_outcome'].encode()),
        'terminal': controls[row['id']]['terminal'], 'exit_code': controls[row['id']]['exit_code'],
        'log_sha256': controls[row['id']]['log_sha256']} for row in suite['controls']]


def _execute_history_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews, adapter):
    """Recollect the pinned completed history producer and run its missing audit."""
    a = adapter
    a.require(suite['id'] == a.HC_SUITE and a.canonical(suite) == a.HC_SUITE_SHA256
              and a.APPROVED_DECLARED_SUITES.get(suite['id']) == a.HC_APPROVAL, 'Unapproved history continuation suite')
    a.require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'Missing current history review identities')
    plan = a.validate_suite(suite, sources, root); prior = a.no_symlinks(prior).absolute()
    if not prior.is_dir(): raise a.MissingInput('Original history run is unavailable')
    protected = [root, prior, *inputs.values()]
    if 'mathlib' in tools: protected.append(tools['mathlib'])
    protected.extend(Path(path).resolve().parent.parent for name, path in tools.items() if name != 'mathlib')
    output = _ac_exec_output(output, protected, a)
    started = a.utc(); run = None; runner = a.sha(Path(a.__file__).read_bytes())
    output.mkdir(parents=True, exist_ok=False); (output / 'logs').mkdir()
    try:
        binding = _hc_exec_prior(prior, a)
        original, old, old_stages = a._hc_prior({'prior': binding}, suite, sources, root, a, plan)
        a.require({rid: reviews[rid]['review_sha256'] for rid in suite['review_ids']} == original['review_hashes'], 'History review identity changed')
        hashes = {sid: a.sha(a.public_bytes(root, sources[sid])) for sid in suite['source_ids']}
        a.require(hashes == original['source_hashes'] == old['source_hashes_before'] == old['source_hashes_after']
                  and a.canonical(suite['replay']) == old['descriptor_sha256'] and a.closure_fingerprint(suite, sources) == old['closure_sha256']
                  and a.import_fingerprints(suite, sources) == old['import_fingerprints'], 'History source/import binding changed')
        tree_before, project_before, objects_before = _hc_exec_retained(prior, plan, suite, a)
        before = output / 'prerequisites-before'; before.mkdir(); pre_start = a.utc()
        resolved, fingerprints, dependencies, env, input_hashes = a._verify_environment(suite, plan, tools, inputs, before)
        a.require(fingerprints == old['tool_fingerprints'] and dependencies == old['dependency_checks'], 'History tool/dependency binding changed')
        roots, libraries = _ac_exec_cache_roots(resolved, tools, plan, a)
        cache_rows, inventories = _ac_exec_caches(roots, plan, a)
        env['LEAN_PATH'] = os.pathsep.join(str(p) for p in [*[a.path_in(prior, name) for name in suite['replay']['build_roots']], *libraries])
        collection, source_audit = a._hc_exec_collection(suite, plan, prior, old, resolved, tools, a)
        a.require(a.canonical(source_audit) == a.HC_SOURCE_AUDIT_SHA256
                  and collection['source_audit_sha256'] == a.HC_SOURCE_AUDIT_SHA256
                  and a._hc_collection_digest(collection, a) == a.HC_COLLECTION_SHA256, 'History collection/source-audit pin changed')
        controls = _hc_exec_controls(suite, plan, collection, a)
        a.write_json(output / 'RETAINED_COLLECTION.json', collection); a.write_json(output / 'SOURCE_READBACK_AUDIT.json', source_audit)
        pre_log = output / 'logs/prerequisites.log'
        pre_log.write_text('Current history source, complete retained physical collection, custom objects, tools and dependency pins verified.\n'
                           'Official caches measured only now; no new producer, object or independent evidence is claimed.\n', encoding='utf-8')
        pre = {'id': '_prerequisites', 'argv': ['{builtin:prerequisites}'], 'cwd': '.', 'budget_seconds': 30,
               'started_at': pre_start, 'ended_at': a.utc(), 'terminal': 'COMPLETED', 'exit_code': 0,
               'log_sha256': a.sha(pre_log.read_bytes()), 'output_hashes': {}}
        audit = _hc_exec_generate(output, plan, a)
        argv = [resolved['lean'], '-j1', audit]; cwd = a.path_in(prior, 'project')
        invocation = output / 'RESOLVED_AUDIT_INVOCATION.json'
        a.write_json(invocation, {'argv': [str(arg) for arg in argv], 'cwd': str(cwd), 'timeout_seconds': 300,
            'lean_path': env['LEAN_PATH'].split(os.pathsep), 'runner_sha256': runner, 'generated_source_sha256': a.HC_AUDIT_SOURCE,
            'scope': 'ONE_FRESH_HISTORY_TARGET_AUDIT_REUSING_PINNED_CAMPAIGN_OBJECTS'})
        log = output / 'logs/target-audit.log'; run = a.run_process(argv, cwd, env, log, 300)
        a.require(a.sha(log.read_bytes()) == run['log_sha256'], 'History audit log differs from its actual process')
        outcome, audits = _ac_exec_result(run, log.read_text(encoding='utf-8'), list(plan['targets'].values()), a)
        after = output / 'prerequisites-after'; after.mkdir()
        checked, fingerprints_after, dependencies_after, _, inputs_after = a._verify_environment(suite, plan, tools, inputs, after)
        a.require(checked == resolved and fingerprints_after == fingerprints and dependencies_after == dependencies
                  and inputs_after == input_hashes, 'History tool/dependency/input changed during audit')
        roots_after, libraries_after = _ac_exec_cache_roots(checked, tools, plan, a)
        rows_after, inventories_after = _ac_exec_caches(roots_after, plan, a)
        a.require(roots_after == roots and libraries_after == libraries and rows_after == cache_rows and inventories_after == inventories,
                  'History official cache changed during audit')
        tree_after, project_after, objects_after = _hc_exec_retained(prior, plan, suite, a)
        a.require(_hc_exec_prior(prior, a) == binding, 'History prior failure/source-owned receipt changed')
        a.require({sid: a.sha(a.public_bytes(root, sources[sid])) for sid in suite['source_ids']} == hashes, 'History public source changed')
        a.require(a.sha(audit.read_bytes()) == a.HC_AUDIT_SOURCE and a.sha(Path(a.__file__).read_bytes()) == runner, 'History auditor/runner changed')
        audit_stage = {'id': '_target_audit', 'argv': ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'],
                       'cwd': '.', 'budget_seconds': 300, **run, 'output_hashes': {}}
        evidence = {key: old[key] for key in ('descriptor_sha256', 'closure_sha256', 'source_hashes_before', 'source_hashes_after',
                    'import_fingerprints', 'tool_fingerprints', 'dependency_checks')}
        evidence.update(schema=a.HC_SCHEMA, runner_sha256=runner, cache_policy=a.HC_CACHE_POLICY, prior=binding,
            stage_results=[pre, audit_stage], retained_collection=collection,
            target_audits=[{'target_id': tid, **row, 'stage_id': '_target_audit', 'log_sha256': run['log_sha256']} for tid, row in audits.items()],
            output_hashes={'generated/V5SuccessorReadback.lean': a.HC_AUDIT_SOURCE},
            retained_input_checks={'mode': 'REUSED_CAMPAIGN_EXECUTION', 'stage_ids': ['_prerequisites', 'original-driver'],
                'physical_trace_sha256': a.HC_TRACE, 'original_result_sha256': a.HC_PRIOR['original_receipt_sha256'],
                'child_ledger_sha256': a.canonical(collection['child_observations']), 'driver_invocations_sha256': a.canonical(collection['driver_invocations']),
                'archive_sha256': suite['replay']['external_inputs'][0]['expected_sha256'],
                'retained_tree_before_sha256': tree_before, 'retained_tree_after_sha256': tree_after,
                'project_sources_before_sha256': project_before, 'project_sources_after_sha256': project_after,
                'custom_objects_before': objects_before, 'custom_objects_after': objects_after, 'official_cache_measurements': cache_rows},
            fresh_audit={'recipe': 'history-retained-closure-audit-v1', 'generated_source_sha256': a.HC_AUDIT_SOURCE,
                'resolved_invocation_sha256': a.sha(invocation.read_bytes()), 'argv_provenance': 'RESOLVED_FROM_BOUND_INPUTS',
                'traversal_bound': 1000000, 'distinct_declaration_accounting': 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED', 'fresh_custom_objects': 0},
            accounting=dict(a.HC_ACCOUNTING))
        receipt = {key: original[key] for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256')}
        success = outcome == 'QUALIFIED_DECLARED_SUITE'
        receipt.update(id=suite['id'] + '-audit-continuation-' + a.sha((started + a.sha(invocation.read_bytes())).encode())[:16],
            invocation=['replay_v5_successors.py', '--history-audit-continuation', '--suite', suite['id'], '--prior', '{prior}', '--out', '{out}'],
            outcome=outcome, proof_scope='DECLARED_SUITE' if success else 'NONE', exit_code=0 if success else 1,
            started_at=started, ended_at=a.utc(), replay_evidence=evidence, controls=controls,
            stages=[{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in [pre, audit_stage]],
            log_sha256=a.canonical({row['id']: row['log_sha256'] for row in [pre, audit_stage]}),
            target_readbacks=[{'target_id': row['id'], 'source_id': row['source_id'], 'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']] if success else [],
            axioms=sorted({axiom for value in audits.values() for axiom in value['axioms']}))
        a.validate_history_continuation(receipt, suite, sources, root, adapter=a)
        a.write_json(output / 'RECEIPT.json', receipt)
        return receipt
    except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
        a.write_json(output / 'REFUSAL.json', {'status': 'HISTORY_CONTINUATION_REFUSED', 'started_at': started, 'ended_at': a.utc(),
            'audit_process': run, 'error': type(error).__name__ + ': ' + str(error),
            'prior_receipt_sha256': a.HC_PRIOR['receipt_sha256'], 'qualified_receipt_written': False})
        raise


def execute_history_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews=None):
    return _execute_history_audit_continuation(suite, sources, root, prior, output, tools, inputs,
                                             reviews=reviews, adapter=SimpleNamespace(**globals()))



COVERING_REVIEWED_EXECUTOR_HASHES = frozenset({'f77e456b0b99b7b932013e84bacf105ebc07508e30384b5ca96bbeb4e23f17a4'})


def covering_continuation_load():
    """Load the exact covering continuation helper and its retained-data pins."""
    path = no_symlinks(Path(__file__).with_name('v5_covering_continuation.py'))
    raw = path.read_bytes()
    require(sha(raw) == 'ebed39c4cf80983b9ef667a656d519decfc449585004245395eec578948adba7',
            'Unreviewed covering continuation helper')
    namespace = {'__file__': str(path), '__name__': 'v5_covering_continuation'}
    exec(compile(raw, str(path), 'exec'), namespace)
    # Executor compatibility belongs to the adapter, so the reviewed helper and
    # its data remain byte-identical when a later adapter admits an earlier run.
    namespace['REVIEWED_EXECUTOR_HASHES'] = COVERING_REVIEWED_EXECUTOR_HASHES
    helper = SimpleNamespace(**namespace)
    helper.data(SimpleNamespace(**globals()))
    return helper


def execute_covering_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews=None):
    return covering_continuation_load().execute(suite, sources, root, prior, output, tools, inputs,
                                               reviews=reviews, adapter=SimpleNamespace(**globals()))


SELECTOR_CONTINUATION_REVIEWED_EXECUTORS = frozenset({'46136526f8107b702873c82fed6fa9cdb23c061526acaeefd638e56917c57bef'})
SELECTOR_CONTINUATION_ASSETS = {'v5_selector_continuation.py': '439e07450f1c3ce2a7cea2442ee9ebddf48453beecb6fcad4711409c90f9e8bf', 'v5_selector_executor.py': 'c3d24b36478ea25835fc92242747eab4f023c8b99548c93a9d36a132f6b4dff3'}


def selector_continuation_load():
    """Verify both code-owned selector modules before executing either."""
    checked = []
    for name, digest in SELECTOR_CONTINUATION_ASSETS.items():
        path = no_symlinks(Path(__file__).with_name(name)); raw = path.read_bytes()
        require(sha(raw) == digest, 'Unreviewed selector continuation asset')
        checked.append((path, raw))
    modules = []
    for path, raw in checked:
        namespace = {'__file__': str(path), '__name__': path.stem}
        exec(compile(raw, str(path), 'exec'), namespace)
        if path.name == 'v5_selector_continuation.py':
            namespace['SC_REVIEWED_EXECUTORS'] = SELECTOR_CONTINUATION_REVIEWED_EXECUTORS
        modules.append(SimpleNamespace(**namespace))
    return tuple(modules)


def execute_selector_audit_continuation(suite, sources, root, prior, output, tools, inputs, *, reviews=None):
    helper, executor = selector_continuation_load()
    return executor.execute(suite, sources, root, prior, output, tools, inputs,
                            reviews=reviews, api=SimpleNamespace(**globals()), helper=helper)


D04_PUBLIC_HELPER_SHA256 = '77d12f0b4c9bf40ea0f75ab735ec2f25af46083e918a37d32ce57e928e645b35'


def d04_public_receipt_load():
    """Load the sealed public-summary helper from verified non-symlink bytes."""
    path = no_symlinks(Path(__file__).with_name('v5_d04_public_receipt.py'))
    raw = path.read_bytes()
    require(sha(raw) == D04_PUBLIC_HELPER_SHA256, 'Unreviewed D04 public receipt helper')
    namespace = {'__file__': str(path), '__name__': 'v5_d04_public_receipt'}
    exec(compile(raw, str(path), 'exec'), namespace)
    return SimpleNamespace(**namespace)

def validate_receipt(receipt, suite, sources, root):
    if p1_tail_finish_handles(suite): return p1_tail_finish_validate_receipt(p1_api(), receipt, suite, sources, root)
    if p1_tail_handles(suite): return p1_tail_validate_receipt(p1_api(), receipt, suite, sources, root)
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == 'orthemology-v5-selector-audit-continuation-v1':
        helper, _ = selector_continuation_load()
        return helper.validate_selector_continuation(receipt, suite, sources, root, api=SimpleNamespace(**globals()))
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == 'orthemology-v5-covering-audit-continuation-v1':
        return covering_continuation_load().validate_receipt(receipt, suite, sources, root, adapter=SimpleNamespace(**globals()))
    if selector_g1_handles(suite):
        family = selector_g1_load_family()
        return family.selector_g1_validate_receipt(family.selector_g1_adapter_view(globals()), receipt, suite, sources, root)
    if isinstance(suite, dict) and isinstance(suite.get('replay'), dict) and suite['replay'].get('schema') == p1_schema:
        return p1_validate_receipt(p1_api(), receipt, suite, sources, root)
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == portable_family.EVIDENCE_SCHEMA:
        return portable_family.validate_receipt(_portable_api(), receipt, suite, sources, root)
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == HC_SCHEMA:
        return validate_history_continuation(receipt, suite, sources, root, adapter=SimpleNamespace(**globals()))
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and receipt['replay_evidence'].get('schema') == AC_SCHEMA:
        return validate_audit_continuation(receipt, suite, sources, root, adapter=SimpleNamespace(**globals()))
    if isinstance(receipt, dict) and isinstance(receipt.get('replay_evidence'), dict) and isinstance(receipt['replay_evidence'].get('schema'), str) and receipt['replay_evidence']['schema'] in {'orthemology-v5-d04-public-receipt-v1', 'orthemology-v5-d04-public-covering-continuation-v1'}:
        return d04_public_receipt_load().validate_receipt(receipt, suite, sources, root, adapter=SimpleNamespace(**globals()))
    plan = validate_suite(suite, sources, root); evidence = receipt['replay_evidence']
    has_children = any(row['argv'][:1] == ['{builtin:observe-child}'] for row in plan['stages'].values())
    keys(evidence, EVIDENCE_KEYS | ({'child_observations', 'driver_invocations'} if has_children else set()))
    require(evidence['schema'] == ('orthemology-v5-replay-evidence-v2' if has_children else 'orthemology-v5-replay-evidence-v1') and evidence['cache_policy'] == CACHE_POLICY, 'Unknown replay evidence/cache policy')
    return _validate_receipt_body(receipt, suite, sources, root, plan, evidence, has_children, validate_child_evidence)


def _validate_receipt_body(receipt, suite, sources, root, plan, evidence, has_children, child_validator):
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
    if has_children: child_validator(evidence, plan, stages, successful)
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
    if 'operational_packet' in plan:
        return operational_validate_child_evidence(evidence, plan, stages, successful)
    if 'd04_family' in plan: return d04_validate_child_evidence(evidence, plan, stages, successful)
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


# Private D03 splice proposal. This fragment plans/checks; it never runs science.
D04_DATA_SHA256 = '11541cb7ca6fe3355f4f0994f5dff642122b146c1fee7998c1d52bdd58cc09b5'
D04_RECIPES = {
    't07-criterion-translated-v1', 't07-covering-translated-v1',
    't07-composition-projection-v1', 't07-composition-packaging-translated-v1',
    't07-composition-original-v1', 't07-composition-review-translated-v1',
    't07-composition-serial-mutations-v1', 't07-dynamic-base-v1',
    't07-dynamic-attribution-v1', 't07-dynamic-independent-root-image-v1',
}


def d04_contracts():
    path = Path(__file__).with_name('v5_d04_recipes.json')
    require(sha(no_symlinks(path).read_bytes()) == D04_DATA_SHA256, 'D04 reviewed contract data changed')
    data = read_json(path)
    require(data['schema'] == 'orthemology-private-d04-contracts-v1' and set(data['recipes']) == D04_RECIPES, 'D04 recipe inventory changed')
    return data


def d04_check_descriptor(suite):
    families = d04_contracts()['families']
    matches = [(family, row) for family, row in families.items() if row['suite_id'] == suite.get('id')]
    require(len(matches) == 1, 'Unknown D04 suite')
    family, contract = matches[0]
    require(canonical(suite) == contract['descriptor_sha256'], 'D04 descriptor differs from reviewed source contracts')
    return family


def d04_validate_argv(stage, driver, plan):
    suite = plan.get('d04_suite')
    require(isinstance(suite, dict), 'D04 exact suite binding missing')
    d04_check_descriptor(suite)
    original = next((row for row in suite['replay']['stages'] if row['id'] == stage.get('id')), None)
    declared_driver = next((row for row in suite['replay']['drivers'] if row['id'] == driver.get('id')), None)
    require(original is not None and canonical(stage) == canonical(original), 'D04 stage vector/cwd/budget/meaning changed')
    require(declared_driver is not None and canonical(driver) == canonical(declared_driver), 'D04 driver binding changed')


def d04_check_driver_source(recipe, source):
    data = d04_contracts(); row = data['recipes'][recipe]; family = data['families'][row['family']]
    member = '/'.join(part for part in [family['archive_root'], row['source_member']] if part)
    require(source['id'] == row['source_id'] and source['original_sha256'] == row['source_sha256'] and
            type(source['original_bytes']) is int and source['original_bytes'] == row['source_bytes'], 'D04 original driver identity changed')
    require(source['origin_archive_sha256'] == family['archive_sha256'] and source['member_chain'][-1] == member, 'D04 driver archive member changed')
    require(source['projection'] in {'EXACT', 'CUSTODY_ONLY'} and source['public_sha256'] in {None, row['source_sha256']}, 'D04 original driver cannot be a changed projection')


def d04_source_inventory(recipe, source_root):
    data = d04_contracts(); contract = data['families'][data['recipes'][recipe]['family']]
    root = no_symlinks(source_root).resolve(); require(root.is_dir(), 'D04 source root missing')
    inventory = {}
    for path in sorted(root.rglob('*')):
        no_symlinks(path)
        if path.is_file(): inventory[path.relative_to(root).as_posix()] = sha(path.read_bytes())
    require(len(inventory) == contract['source_files'] and canonical(inventory) == contract['source_inventory_sha256'], 'D04 complete source inventory differs')
    return inventory


def d04_command_plan(recipe, source_root):
    require(recipe in D04_RECIPES, 'Unreviewed D04 recipe')
    d04_source_inventory(recipe, source_root)
    return d04_contracts()['recipes'][recipe]


def d04_resolve_child(recipe, child_id, source_root, bindings):
    row = d04_command_plan(recipe, source_root)
    children = [child for child in row['children'] if child['id'] == child_id]
    require(len(children) == 1, 'Unknown D04 physical child')
    maps = {**bindings, 'source': no_symlinks(source_root).resolve()}
    def expand(value):
        if isinstance(value, str):
            result = re.sub(r'\{([^{}]+)\}', lambda m: str(maps[m.group(1)]), value)
            require(not re.search(r'[{}]', result), 'Unresolved D04 path token')
            return result
        if isinstance(value, list): return [expand(x) for x in value]
        if isinstance(value, dict): return {k: expand(v) for k, v in value.items()}
        return value
    return expand(children[0])


def d04_bind_temporary_cwd(recipe, actual_cwd, output, bindings):
    contract = d04_contracts()['recipes'][recipe].get('temporary_cwd_binding')
    require(contract is not None, 'Recipe has no original temporary cwd')
    token = contract['token'][1:-1]
    actual = no_symlinks(actual_cwd).resolve(); tmp = no_symlinks(Path(output) / 'tmp').resolve()
    require(actual.is_dir() and actual != tmp and actual.is_relative_to(tmp), 'D04 temporary cwd escapes the fresh replay')
    prefix = 'dynamic-interlock-replay-' if recipe == 't07-dynamic-base-v1' else 'root-attribution-replay-'
    require(actual.name.startswith(prefix), 'D04 temporary cwd differs from original construction')
    require(token not in bindings or Path(bindings[token]).resolve() == actual, 'D04 original temporary cwd rebound')
    return {**bindings, token: actual}


def d04_check_invocation(spec, argv, cwd, *, timeout_seconds, capture, stdin):
    require(argv == spec['argv'] and all(isinstance(x, str) for x in argv), 'D04 actual argv differs')
    require(str(cwd) == spec['cwd'], 'D04 actual cwd differs; project cwd cannot substitute for source/build cwd')
    require((timeout_seconds is None and spec['timeout_seconds'] is None) or
            (type(timeout_seconds) is int and timeout_seconds == spec['timeout_seconds']), 'D04 child timeout differs')
    require(capture == spec['capture'], 'D04 capture mode differs from original source')
    require(stdin == {'mode': 'INHERITED_NO_INPUT', 'data_sha256': None}, 'D04 original child has no supplied stdin')
    if '-o' in argv and argv[-1].endswith('.lean'):
        source = Path(argv[-1]); source = source if source.is_absolute() else Path(cwd) / source
        require(source.resolve().is_relative_to(Path(cwd).resolve()), 'Lean output source lies outside its reviewed module root')


def d04_producer_hash(binding, recipe, producers, replay_id):
    owner = binding.get('producer_recipe') or recipe
    path = binding.get('predecessor_path', binding['path'])
    key = (owner, binding['producer'], path)
    require(key in producers, 'D04 fresh predecessor producer is missing')
    row = producers[key]
    require(row['replay_id'] == replay_id and row['recipe'] == owner and row['child_id'] == binding['producer'] and row['path'] == path,
            'D04 predecessor belongs to another replay/producer/path')
    require(row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int and row['exit_code'] == 0, 'D04 predecessor was not successfully produced')
    digest(row['sha256']); digest(row['producer_record_sha256'])
    require(isinstance(row['source_hashes'], dict) and row['source_hashes'], 'D04 predecessor lacks source identity')
    for value in row['source_hashes'].values(): digest(value)
    captured = row.get('producer_record')
    require(isinstance(captured, dict) and canonical(captured) == row['producer_record_sha256'], 'D04 predecessor record digest is not bound to captured facts')
    require(all(captured.get(name) == row[name] for name in ['replay_id', 'recipe', 'child_id', 'terminal', 'exit_code', 'source_hashes']),
            'D04 predecessor summary differs from captured producer')
    require(isinstance(captured.get('output_hashes'), dict) and captured['output_hashes'].get(path) == row['sha256'],
            'D04 predecessor output hash differs from captured producer')
    if owner == 't07-composition-original-v1' and binding['producer'].startswith('compile-'):
        original = next(child for child in d04_contracts()['recipes'][owner]['children'] if child['id'] == binding['producer'])
        expected_hashes = {source['member']: source['sha256'] for source in original['sources'] if source['kind'] == 'ORIGINAL_SOURCE'}
        require(all(row['source_hashes'].get(name) == value for name, value in expected_hashes.items()), 'D04 fresh predecessor source binding changed')
    return row['sha256']


def d04_check_launch_files(recipe, spec, producers, replay_id):
    """Called before the actual child by D03; no execution or overwrite occurs."""
    actual_inputs = {}
    for binding in spec['sources']:
        if binding['kind'] == 'TOOL_PROBE': continue
        if binding['kind'] == 'ORIGINAL_SOURCE': expected = binding['sha256']
        else:
            require(binding['kind'] == 'GENERATED_BY_ORIGINAL', 'Unknown D04 source binding class')
            expected = binding['expected_sha256'] or d04_producer_hash(binding, recipe, producers, replay_id)
        path = no_symlinks(binding['path']); require(path.is_file(), 'D04 actual child input missing')
        actual = sha(path.read_bytes()); require(actual == expected, 'D04 actual child input bytes differ')
        actual_inputs[str(path)] = actual
    replacements = {row['path']: row for row in spec['replace_fresh_predecessor']}
    require(set(replacements) <= set(spec['outputs']), 'D04 replacement is not an exact declared output')
    for name in spec['outputs']:
        path = no_symlinks(name)
        if name in replacements:
            require(path.is_file() and sha(path.read_bytes()) == d04_producer_hash(replacements[name], recipe, producers, replay_id),
                    'D04 replacement lacks exact fresh predecessor object bytes')
        else: require(not path.exists(), 'D04 output already exists outside the exact replacement contract')
    return actual_inputs


def d04_assess_captured_child(spec, row, log_bytes, parent):
    """Validate captured facts; parent spans never invent child terminal/time."""
    d04_check_invocation(spec, row['argv'], row['cwd'], timeout_seconds=row['timeout_seconds'], capture=row['capture'], stdin=row['stdin'])
    require(row['id'] == spec['id'] and row['log_sha256'] == sha(log_bytes), 'D04 child/log association changed')
    def instant(value):
        require(isinstance(value, str) and (value.endswith('Z') or value.endswith('+00:00')), 'D04 measured UTC child interval missing')
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(instant(parent['started_at']) <= instant(row['started_at']) <= instant(row['ended_at']) <= instant(parent['ended_at']), 'D04 child interval does not belong to its physical parent')
    text = log_bytes.decode('utf-8')
    if row['terminal'] in {'TIMEOUT','INTERRUPTED','LAUNCH_ERROR','RUNNING'}:
        require(row['exit_code'] is None, 'D04 unknown terminal cannot carry a fabricated semantic exit')
        return {'outcome':'RESOURCE_INCONCLUSIVE', 'rejection_credit':False}
    require(row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int, 'Unknown D04 terminal')
    if re.search(r'timed out|out of memory|maximum (?:number of heartbeats|recursion depth)|deterministic timeout|WALL_CLOCK_LIMIT', text, re.I):
        return {'outcome':'RESOURCE_INCONCLUSIVE', 'rejection_credit':False}
    require(row['exit_code'] == spec['expected_exit_code'], 'D04 child exit differs from source contract')
    require(isinstance(row['output_hashes'], dict) and set(row['output_hashes']) == set(spec['outputs']), 'D04 actual output inventory incomplete')
    for value in row['output_hashes'].values(): digest(value)
    require(all(x in text for x in spec['required_diagnostics']) and all(x not in text for x in spec['forbidden_diagnostics']), 'D04 intended control diagnostic differs')
    if row['exit_code'] == 0:
        require('sorryAx' not in text, 'D04 child reported a proof hole')
    if row['exit_code']:
        require(not re.search(r'unknown (?:module|constant|identifier|namespace)|no such file|file not found|failed to read file|object file|must be contained in root directory', text, re.I), 'D04 infrastructure failure is not semantic rejection')
    outcome = 'ACCEPT' if row['exit_code'] == 0 else 'REJECT'
    return {'outcome':outcome, 'rejection_credit':outcome == 'REJECT'}


def d04_check_complete_child_order(recipe, rows):
    expected = [child['id'] for child in d04_contracts()['recipes'][recipe]['children']]
    require([row['id'] for row in rows] == expected, 'D04 original physical child omitted, duplicated or reordered')


def d04_translation_binding(recipe, translation):
    row = d04_contracts()['recipes'][recipe]
    require(row['translation_sha256'] is not None and sha(no_symlinks(translation).read_bytes()) == row['translation_sha256'], 'D04 adapter translation differs from reviewed bytes')
    return {'original_source_sha256':row['source_sha256'], 'translation_sha256':row['translation_sha256'], 'source_argv':row['parent_stage']['argv']}


# D04-only dispatch and admission; all generic frozen validation remains active.
def d04_is_suite(suite):
    return suite.get('id') in {row['suite_id'] for row in d04_contracts()['families'].values()}


def d04_admit_sources(suite, sources):
    family = d04_check_descriptor(suite)
    expected = d04_contracts()['families'][family]['sources']
    require(all(sid in sources and canonical(sources[sid]) == canonical(row) for sid, row in expected.items()), 'D04 selected or custody source record changed')
    return family


def d04_declared_admitted(suite, sources):
    if not d04_is_suite(suite): return False
    family = d04_admit_sources(suite, sources)
    require(family != 'dynamic' and suite['replay']['scope'] == 'DECLARED_SUITE', 'D04 dynamic scope cannot be promoted')
    return True


def d04_validate_driver(driver, sources):
    recipe = driver['recipe']; data = d04_contracts(); contract = data['recipes'][recipe]
    expected = next(row for row in data['families'][contract['family']]['suite']['replay']['drivers'] if row['id'] == driver['id'])
    require(driver == expected, 'D04 exact driver or argument meaning changed')
    d04_check_driver_source(recipe, sources[driver['source_id']])


def d04_validate_package(suite, plan, sources):
    family = d04_admit_sources(suite, sources); data = d04_contracts(); contract = data['families'][family]
    plan.update(d04_family=family, d04_suite=suite, d04_sources={sid:sources[sid] for sid in contract['sources']})
    recipes = {r['recipe'] for r in plan['drivers'].values()}
    require(recipes == {rid for rid,r in data['recipes'].items() if r['family'] == family}, 'D04 original recipe inventory incomplete')
    require(list(plan['inputs']) == ['source-archive'], 'D04 archive inventory changed')
    require(plan['inputs']['source-archive'] == contract['suite']['replay']['external_inputs'][0], 'D04 original archive input changed')
    declared = {(s['argv'][1],s['argv'][2]) for s in suite['replay']['stages'] if s['argv'][0] == '{builtin:observe-child}'}
    expected = {(r['parent_stage']['id'],child['id']) for rid,r in data['recipes'].items() if rid in recipes for child in r['children']}
    require(declared == expected, 'D04 physical child observation census differs')
    for sid,body in plan['contents'].items():
        require(sha(body) == sources[sid]['public_sha256'], 'D04 exact public source changed')


def d04_diagnostic_allowed(driver, diagnostic):
    if driver.get('recipe') not in D04_RECIPES: return False
    row = d04_contracts()['recipes'][driver['recipe']]
    stages = d04_contracts()['families'][row['family']]['suite']['replay']['stages']
    return any(diagnostic in stage['expected_diagnostics'] for stage in stages if stage['driver_id'] == driver['id'])


def d04_expand(value, bindings):
    if isinstance(value, str):
        return re.sub(r'\{([^{}]+)\}', lambda match: str(bindings[match.group(1)]), value)
    if isinstance(value, list): return [d04_expand(item, bindings) for item in value]
    if isinstance(value, dict): return {key:d04_expand(item, bindings) for key,item in value.items()}
    return value


def d04_asset(name):
    row = d04_contracts()['adapter_assets'][name]
    path = no_symlinks(Path(__file__).with_name('v5_d04_assets') / name)
    require(path.is_file() and sha(path.read_bytes()) == row['sha256'], 'D04 adapter-owned helper changed')
    return path


def d04_child_environment(recipe, spec, base, bindings):
    if spec['environment_policy'] == 'SYNTHETIC_TEST_ONLY': return dict(base)
    env = dict(base)
    if recipe in {'t07-criterion-translated-v1','t07-covering-translated-v1','t07-composition-review-translated-v1','t07-composition-packaging-translated-v1'}:
        env = {k:v for k,v in env.items() if not k.startswith(('LEAN_','PYTHON','LD_')) and k != 'DYLD_INSERT_LIBRARIES'}
        paths = []
        if recipe != 't07-composition-packaging-translated-v1': paths.append(str(Path(bindings['tool:lean']).parent))
        if recipe in {'t07-criterion-translated-v1','t07-covering-translated-v1','t07-composition-packaging-translated-v1'}:
            key = 'tool:python312' if recipe == 't07-criterion-translated-v1' else 'tool:python'
            paths.append(str(Path(bindings[key]).parent))
        env.update(PYTHONDONTWRITEBYTECODE='1', PATH=os.pathsep.join(paths + [os.defpath]))
    for key,value in spec['source_environment_overrides'].items():
        expanded = d04_expand(value, bindings)
        env[key] = os.pathsep.join(expanded) if isinstance(expanded, list) else expanded
    return env


def d04_replacement_evidence(recipe, spec, producers, replay_id):
    rows=[]
    for binding in spec['replace_fresh_predecessor']:
        value=d04_producer_hash(binding,recipe,producers,replay_id)
        key=(binding.get('producer_recipe')or recipe,binding['producer'],binding.get('predecessor_path',binding['path']))
        require(sha(no_symlinks(binding['path']).read_bytes())==value,'D04 copied predecessor changed before replacement')
        rows.append({**binding,'actual_sha256':value,'producer_capture_sha256':producers[key]['producer_record']['capture_record_sha256']})
    return rows


class D04CaptureSession:
    """Capture exact physical Popen calls while preserving source return values.

    The only CLI caller supplies a code-owned contract after source/tool checks.
    Tests may construct explicit synthetic contracts; there is no CLI recipe for
    them. One physical child may be active at a time, including serial mutants.
    """
    def __init__(self, context, contract, base_env, producers):
        import threading
        self.context = context; self.contract = contract; self.base_env = dict(base_env)
        self.recipe = context['recipe']; self.trace = no_symlinks(context['trace'])
        self.bindings = dict(context['bindings'], source=context['source_root'], out=context['output'], trace=context['trace'])
        self.producers = dict(producers); self.position = 0; self.probes = 0
        self.active = []; self.lock = threading.RLock(); self.original_popen = subprocess.Popen

    def next_spec(self, argv, cwd):
        probes = self.contract.get('tool_probes', [])
        if self.probes < len(probes) and argv == d04_expand(probes[self.probes]['argv'], self.bindings):
            source = d04_contracts()['recipes'][self.recipe]
            row = {**probes[self.probes], 'id':'probe-' + str(self.probes), 'sources':[{'kind':'TOOL_PROBE'}],
                   'outputs':[], 'replace_fresh_predecessor':[], 'source_environment_overrides':{},
                   'environment_policy':'SANITIZED_PARENT_WITH_EXACT_SOURCE_OVERRIDES',
                   'source_binding':{'kind':'TOOL_PROBE','tool_name':'lean','executable_sha256':LEAN_SHA,'driver_sha256':source['source_sha256']}}
            return d04_expand(row,self.bindings), True
        require(self.probes == len(probes), 'D04 original tool probe missing or reordered')
        require(self.position < len(self.contract['children']), 'Extra D04 physical child')
        if self.contract.get('temporary_cwd_binding'):
            self.bindings = d04_bind_temporary_cwd(self.recipe,cwd,self.context['output'],self.bindings)
        return d04_expand(self.contract['children'][self.position],self.bindings), False

    def prepare(self, argv, positional, kwargs):
        require(not positional and isinstance(argv,list) and all(isinstance(x,str) for x in argv), 'D04 unreviewed process argv form')
        allowed = {'cwd','env','stdout','stderr','text','universal_newlines','start_new_session','shell','stdin'}
        require(set(kwargs) <= allowed and kwargs.get('shell',False) is False and kwargs.get('stdin') is None, 'D04 process options or supplied stdin changed')
        cwd = str(Path(kwargs.get('cwd',Path.cwd())).absolute())
        spec, probe = self.next_spec(argv,cwd)
        require(argv == spec['argv'] and cwd == spec['cwd'], 'D04 actual argv/cwd differs from original recipe')
        capture = spec['capture']; text = kwargs.get('text',kwargs.get('universal_newlines',False))
        stdout = kwargs.get('stdout'); stderr = kwargs.get('stderr')
        if capture == 'FILE_MERGED_BYTES':
            require(text is False and hasattr(stdout,'name') and str(Path(stdout.name).absolute()) == spec['log'] and stderr == subprocess.STDOUT, 'D04 original file stream contract changed')
        else:
            expected = {'MERGED_BYTES':(False,subprocess.STDOUT),'MERGED_TEXT':(True,subprocess.STDOUT),
                        'SEPARATE_BYTES':(False,subprocess.PIPE),'STDOUT_TEXT':(True,None)}
            require(capture in expected and stdout == subprocess.PIPE and (text,stderr) == expected[capture], 'D04 original pipe stream contract changed')
        expected_env = d04_child_environment(self.recipe,spec,self.base_env,self.bindings)
        require(kwargs.get('env',self.base_env) == expected_env, 'D04 actual child environment differs')
        session = self.recipe in {'t07-covering-translated-v1','t07-composition-review-translated-v1'}
        require(kwargs.get('start_new_session',False) is session, 'D04 original process-session contract changed')
        require(not any(p.poll() is None for p in self.active), 'Concurrent D04 child is not an admitted serial recipe')
        actual = d04_check_launch_files(self.recipe,spec,self.producers,self.context['replay_id'])
        inputs = []; source_hashes = {}
        for item in spec['sources']:
            if item['kind'] == 'TOOL_PROBE': continue
            digest_value = actual[item['path']]
            inputs.append({**item,'actual_sha256':digest_value})
            source_hashes[item.get('member') or item.get('origin_member') or item['path']] = digest_value
        binding = dict(spec['source_binding'])
        if binding['kind'] == 'GENERATED_BY_ORIGINAL': binding['generated_sha256'] = inputs[0]['actual_sha256']
        index = self.probes if probe else self.position
        name = ('probe-' if probe else '') + f'{index:04}'
        record = {'id':spec['id'],'index':index,'probe':probe,'recipe':self.recipe,'replay_id':self.context['replay_id'],
                  'parent_stage_id':self.context['parent_stage_id'],'argv':argv,'cwd':cwd,'timeout_seconds':spec['timeout_seconds'],
                  'capture':capture,'stdin':{'mode':'INHERITED_NO_INPUT','data_sha256':None},
                  'environment_sha256':canonical(expected_env),'source_binding':binding,'input_bindings':inputs,'source_hashes':source_hashes,
                  'replacement_bindings':d04_replacement_evidence(self.recipe,spec,self.producers,self.context['replay_id']),
                  'started_at':utc(),'ended_at':None,'terminal':'RUNNING','exit_code':None,'log_sha256':None,
                  'stream_hashes':{},'output_hashes':{},'log_file':name+'.log'}
        destination = path_in(self.trace,name+'.json'); require(not destination.exists(), 'D04 capture collision')
        write_json(destination,record)
        if probe: self.probes += 1
        else: self.position += 1
        return spec,record,destination

    def finish(self, process, terminal, stdout=b'', stderr=b''):
        if process.d04_record['terminal'] != 'RUNNING': return
        spec = process.d04_spec; row = process.d04_record
        def data(value): return value.encode('utf-8') if isinstance(value,str) else value or b''
        if spec['capture'] == 'FILE_MERGED_BYTES':
            stdout = no_symlinks(spec['log']).read_bytes() if Path(spec['log']).exists() else b''
        stdout,stderr = data(stdout),data(stderr); log = stdout + stderr
        if spec['capture'] == 'SEPARATE_BYTES':
            prefix = process.d04_destination.stem
            for name,value in [('stdout',stdout),('stderr',stderr)]:
                path_in(self.trace,prefix+'.'+name+'.log').write_bytes(value)
            row['stream_hashes'] = {'stdout':sha(stdout),'stderr':sha(stderr)}
        path_in(self.trace,row['log_file']).write_bytes(log)
        row.update(terminal=terminal,ended_at=utc(),exit_code=process.returncode if terminal == 'COMPLETED' else None,log_sha256=sha(log))
        for path in spec['outputs']:
            if no_symlinks(path).is_file(): row['output_hashes'][path] = sha(Path(path).read_bytes())
        write_json(process.d04_destination,row)
        # Bind pre/post source bytes; failure cannot erase the physical terminal.
        for item in row['input_bindings']:
            require(sha(no_symlinks(item['path']).read_bytes()) == item['actual_sha256'], 'D04 child input changed while running')
        if terminal == 'COMPLETED' and row['exit_code'] == 0:
            for path,digest_value in row['output_hashes'].items():
                producer = {'replay_id':row['replay_id'],'recipe':self.recipe,'child_id':row['id'],'terminal':'COMPLETED',
                            'exit_code':0,'source_hashes':row['source_hashes'],'output_hashes':row['output_hashes'],
                            'capture_record_sha256':canonical(row)}
                self.producers[(self.recipe,row['id'],path)] = {**producer,'path':path,'sha256':digest_value,
                    'producer_record':producer,'producer_record_sha256':canonical(producer)}

    def popen_type(self):
        owner = self; original = self.original_popen
        class CapturedPopen(original):
            def __init__(self, argv, *args, **kwargs):
                with owner.lock:
                    self.d04_spec,self.d04_record,self.d04_destination = owner.prepare(argv,args,kwargs)
                    self.d04_communicating = False
                    try: super().__init__(argv,**kwargs)
                    except OSError as error:
                        self.returncode = None; owner.finish(self,'LAUNCH_ERROR',str(error).encode()); raise
                    owner.active.append(self)

            def communicate(self, input=None, timeout=None):
                if self.d04_record['terminal'] != 'RUNNING': return super().communicate(input=input,timeout=timeout)
                require(input is None, 'D04 original process has no supplied stdin')
                expected = self.d04_spec['timeout_seconds']
                require((timeout is None and expected is None) or (type(timeout) is int and timeout == expected), 'D04 source child timeout changed')
                self.d04_communicating = True
                try:
                    out,err = super().communicate(input=input,timeout=timeout)
                except subprocess.TimeoutExpired as error:
                    owner.finish(self,'TIMEOUT',error.output,error.stderr); raise
                except (KeyboardInterrupt,SystemExit):
                    owner.stop(); raise
                finally: self.d04_communicating = False
                terminal = 'COMPLETED' if type(self.returncode) is int and 0 <= self.returncode < 124 else 'INTERRUPTED'
                owner.finish(self,terminal,out,err)
                return out,err

            def wait(self, timeout=None):
                if self.d04_communicating or self.d04_record['terminal'] != 'RUNNING': return super().wait(timeout=timeout)
                expected = self.d04_spec['timeout_seconds']
                require((timeout is None and expected is None) or (type(timeout) is int and timeout == expected), 'D04 source child timeout changed')
                try: code = super().wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    owner.finish(self,'TIMEOUT'); raise
                except (KeyboardInterrupt,SystemExit):
                    owner.stop(); raise
                terminal = 'COMPLETED' if type(code) is int and 0 <= code < 124 else 'INTERRUPTED'
                owner.finish(self,terminal)
                return code
        return CapturedPopen

    def stop(self):
        for process in self.active:
            if process.poll() is None:
                try:
                    if self.recipe in {'t07-covering-translated-v1','t07-composition-review-translated-v1'}: os.killpg(process.pid,signal.SIGTERM)
                    else: process.terminate()
                    self.original_popen.wait(process,timeout=2)
                except (ProcessLookupError,subprocess.TimeoutExpired):
                    try: process.kill(); self.original_popen.wait(process,timeout=2)
                    except ProcessLookupError: pass
            if process.d04_record['terminal']!='RUNNING':continue
            out=err=b''
            if process.d04_spec['capture']!='FILE_MERGED_BYTES':
                communicating=process.d04_communicating;process.d04_communicating=True
                try:out,err=self.original_popen.communicate(process,timeout=2)
                except subprocess.TimeoutExpired as error:out,err=error.output,error.stderr
                finally:process.d04_communicating=communicating
            self.finish(process,'INTERRUPTED',out,err)


def d04_launch_description(recipe, bindings):
    row = d04_contracts()['recipes'][recipe]
    root = PurePosixPath(bindings['source'])
    source = root/row['source_member']
    if row['asset']:
        helper = PurePosixPath(bindings['adapter']).parent/'v5_d04_assets'/row['asset']; arguments = d04_expand(row['parent_stage']['argv'][2:],bindings)
        if recipe == 't07-composition-serial-mutations-v1': arguments = ['--output-dir' if arg == '--output' else arg for arg in arguments]
        return helper, ['--source-root',str(root),*arguments], root
    if recipe == 't07-dynamic-independent-root-image-v1':
        destination = PurePosixPath(bindings['out'])/'independent-root-image/independent_root_image_checks.py'
        return destination, [], destination.parent
    return source, d04_expand(row['parent_stage']['argv'][3:],bindings), source.parent


def d04_check_bindings(recipe, bindings, output):
    family=d04_contracts()['families'][d04_contracts()['recipes'][recipe]['family']]
    names={'lean'}|{row['name']for row in family['suite']['replay']['tools']}
    expected={'out','project','build','adapter','source'}|{'tool:'+name for name in names}
    if family['suite']['replay']['packages']:expected|={'dependency:mathlib','locked:mathlib-package-libraries'}
    keys(bindings,expected)
    require(all(bindings[key]==str(PurePosixPath(output)/suffix)for key,suffix in [('out','.'),('project','project'),('build','build')]),'D04 fixed replay output binding changed')
    require(bindings['source']==str(PurePosixPath(output)/'archives/source-archive'/family['archive_root']),'D04 archive root binding changed')
    for key,value in bindings.items():
        if key=='locked:mathlib-package-libraries':continue
        require(isinstance(value,str)and PurePosixPath(value).is_absolute()and '..'not in PurePosixPath(value).parts,'D04 absolute typed path binding required')


def d04_trace_entry(context_path):
    import tempfile
    context = read_json(no_symlinks(context_path))
    keys(context,{'recipe','parent_stage_id','source_root','output','trace','bindings','replay_id','launch_cwd','producers'})
    recipe = context['recipe']; require(recipe in D04_RECIPES,'Unreviewed D04 internal recipe')
    contract = d04_command_plan(recipe,context['source_root'])
    require(context['parent_stage_id'] == contract['parent_stage']['id'],'D04 parent identity changed')
    output = no_symlinks(context['output']).resolve(); trace = no_symlinks(context['trace']).resolve()
    require(trace == path_in(output,'traces/'+context['parent_stage_id']).resolve(),'D04 trace escaped replay root')
    require(no_symlinks(context_path).resolve() == path_in(output,'contexts/'+context['parent_stage_id']+'.json').resolve(),'D04 context escaped replay root')
    source = no_symlinks(context['source_root']).resolve(); require(not output.is_relative_to(source),'D04 output overlaps original sources')
    bindings = dict(context['bindings'],source=str(source),out=str(output),trace=str(trace))
    family = d04_contracts()['families'][contract['family']]
    d04_check_bindings(recipe,context['bindings'],str(output))
    require(source==path_in(output,str(PurePosixPath('archives/source-archive')/family['archive_root'])).resolve(),'D04 internal source root is not its fresh archive extraction')
    require(context['bindings']['adapter']==str(Path(__file__).resolve()),'D04 internal runner path changed')
    definitions = {'lean':family['suite']['toolchain'],**{r['name']:r for r in family['suite']['replay']['tools']}}
    for name,row in definitions.items():
        require(sha(Path(bindings['tool:'+name]).read_bytes()) == row['executable_sha256'],'D04 internal execution tool changed')
    require(Path(bindings['tool:python']).resolve() == Path(sys.executable).resolve(),'D04 original interpreter changed')
    if 'tool:leanc' in bindings: require(Path(bindings['tool:lean']).with_name('leanc').resolve() == Path(bindings['tool:leanc']).resolve(),'Original leanc sibling differs')
    helper,arguments,cwd = d04_launch_description(recipe,bindings)
    helper=Path(helper);cwd=Path(cwd)
    if contract['asset']:require(helper==d04_asset(contract['asset']),'D04 helper is not the hash-checked adapter asset')
    require(str(cwd) == context['launch_cwd'],'D04 original launch cwd changed')
    if recipe == 't07-dynamic-independent-root-image-v1':
        require(not helper.exists(),'Root-image disposable script exists'); helper.parent.mkdir(parents=True,exist_ok=True)
        helper.write_bytes(path_in(source,contract['source_member']).read_bytes())
    producers = {(r['recipe'],r['child_id'],r['path']):r for r in context['producers']}
    require(len(producers) == len(context['producers']),'Duplicate fresh producer binding')
    trace.mkdir(parents=True,exist_ok=False)
    write_json(trace/'LAUNCH.json',{'recipe':recipe,'parent_stage_id':context['parent_stage_id'],
        'context_sha256':sha(Path(context_path).read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),
        'original_source_sha256':contract['source_sha256'],'helper_sha256':sha(helper.read_bytes()),
        'helper_argv':[str(helper),*arguments],'helper_cwd':str(cwd),'mechanism':'RUNPY_IN_TRACER'})
    (output/'tmp').mkdir(exist_ok=True)
    os.environ['TMPDIR'] = str(output/'tmp'); tempfile.tempdir = None
    session = D04CaptureSession(context,contract,dict(os.environ),producers)
    original_popen = subprocess.Popen; old_argv = sys.argv; old_path = list(sys.path); old_cwd = Path.cwd()
    old_handlers = {sig:signal.getsignal(sig) for sig in [signal.SIGTERM,signal.SIGINT]}
    def interrupted(signum,frame): session.stop(); raise SystemExit(128+signum)
    code = 0
    try:
        for sig in old_handlers: signal.signal(sig,interrupted)
        subprocess.Popen = session.popen_type(); sys.argv = [str(helper),*arguments]
        sys.path.insert(0,str(helper.parent)); os.chdir(cwd)
        try: runpy.run_path(str(helper),run_name='__main__')
        except SystemExit as error:
            code = error.code if type(error.code) is int else 0 if error.code is None else 1
            if code: raise
        require(session.position == len(contract['children']) and session.probes == len(contract.get('tool_probes',[])),'D04 original physical child census incomplete')
        d04_source_inventory(recipe,source)
    finally:
        session.stop(); subprocess.Popen = original_popen; sys.argv = old_argv; sys.path[:] = old_path; os.chdir(old_cwd)
        for sig,handler in old_handlers.items(): signal.signal(sig,handler)
    return code


def d04_parent_paths(recipe, output):
    names = {'t07-criterion-translated-v1':'original','t07-covering-translated-v1':'original',
        't07-composition-original-v1':'original','t07-composition-packaging-translated-v1':'packaging',
        't07-composition-review-translated-v1':'review','t07-composition-serial-mutations-v1':'mutants',
        't07-dynamic-base-v1':'base','t07-dynamic-attribution-v1':'attribution',
        't07-dynamic-independent-root-image-v1':'independent-root-image'}
    return path_in(output,names[recipe]) if recipe in names else Path(output)


def d04_runtime_bindings(plan, mappings):
    bindings = {key:str(value) for key,value in mappings.items() if key.startswith(('tool:','dependency:')) or key in {'out','project','build','adapter'}}
    if 'dependency:mathlib' in bindings:
        root = Path(bindings['dependency:mathlib'])
        actual=sorted(no_symlinks(path) for path in (root/'.lake/packages').glob('*/.lake/build/lib/lean'))
        expected=set()
        for name,row in plan['packages'].items():
            if row['kind']=='GIT' and row['path'].startswith('.lake/packages/'):
                library=path_in(root,row['path']+'/.lake/build/lib/lean')
                expected.update(package_library(name,library,plan['official']))
        require(set(actual)==expected,'D04 original package-library glob differs from exact declared pinned packages')
        bindings['locked:mathlib-package-libraries'] = os.pathsep.join(str(p) for p in actual)
    return bindings


def d04_run_parent(stage, driver, plan, output, mappings, env, log, replay_id, producers):
    recipe = driver['recipe']; contract = d04_contracts()['recipes'][recipe]
    root = Path(mappings['archive:'+driver['external_input_id']]); bindings = d04_runtime_bindings(plan,mappings)
    bindings['source'] = str(root)
    helper,arguments,cwd = d04_launch_description(recipe,bindings)
    context_path = path_in(output,'contexts/'+stage['id']+'.json'); context_path.parent.mkdir(exist_ok=True)
    require(not context_path.exists(),'D04 context already exists')
    trace = path_in(output,'traces/'+stage['id'])
    context = {'recipe':recipe,'parent_stage_id':stage['id'],'source_root':str(root),'output':str(output),'trace':str(trace),
        'bindings':bindings,'replay_id':replay_id,'launch_cwd':str(cwd),'producers':list(producers.values())}
    write_json(context_path,context)
    launch = ['{tool:python}','-B','{adapter}','--trace-d04','{out}/contexts/'+stage['id']+'.json']
    actual = [_expand(arg,mappings) for arg in launch]
    parent_env = dict(env,TMPDIR=str(path_in(output,'tmp')))
    invocation = {'parent_stage_id':stage['id'],'recipe':recipe,'driver_sha256':driver['sha256'],
        'source_argv':stage['argv'],'launch_argv':launch,'actual_launch_argv':actual,'launch_cwd':str(cwd),
        'helper_argv':[str(helper),*arguments],'helper_sha256':contract['translation_sha256'] or contract['source_sha256'],
        'runner_sha256':sha(Path(__file__).read_bytes()),'contract_data_sha256':D04_DATA_SHA256,
        'context_sha256':sha(context_path.read_bytes()),'source_root':str(root),'output_root':str(output),
        'bindings':bindings,'replay_id':replay_id,'trace_sha256':None,'trace_manifest':{},'trace_launch':None,
        'parent_log_sha256':sha(b''),'child_count':0,'probe_count':0,'capture_records':[],
        'normalization':None,'normalization_sha256':None,'qualified_objects':{},'capture_error':None,'raw_capture_files':{}}
    # Actual parent cwd is source-owned; descriptor cwd remains its symbolic identity.
    run = run_process(actual,cwd,parent_env,log,stage['timeout_seconds'])
    invocation['parent_log_sha256'] = run['log_sha256']
    try:
        d04_collect_capture(invocation,contract,trace,run,plan)
    except (ValueError,OSError,KeyError,TypeError) as error:
        invocation['capture_error']=type(error).__name__+': '+str(error)
        if trace.exists():
            invocation['raw_capture_files']={p.relative_to(trace).as_posix():p.read_bytes().hex() for p in sorted(trace.rglob('*')) if p.is_file() and not p.is_symlink()}
            invocation['trace_manifest']={name:sha(bytes.fromhex(value)) for name,value in invocation['raw_capture_files'].items()}
            invocation['trace_sha256']=canonical(invocation['trace_manifest']) if invocation['trace_manifest'] else None
    return run,invocation


def d04_object_outputs(plan, recipe, invocation):
    objects=d04_expected_objects(plan,invocation)
    for name,value in objects.items():
        path=path_in(invocation['output_root'],name)
        require(path.is_file() and sha(path.read_bytes())==value,'D04 target object changed after original producer')
    return objects


def d04_execute_suite(suite, sources, root, output, tools, inputs, scope=None, *, reviews=None):
    require(scope is None or scope==suite['replay']['scope'],'Execute only the exact D04 descriptor scope')
    require(isinstance(reviews,dict) and set(suite['review_ids'])<=set(reviews),'Missing source-bound D04 reviews')
    plan = validate_suite(suite,sources,root); project_suite(suite,sources,root,output)
    output = Path(output).absolute(); project = output/'project'; logs = output/'logs'; logs.mkdir()
    receipt = _initial_receipt(suite,sources,reviews); evidence = receipt['replay_evidence']
    results = {row['id']:row for row in evidence['stage_results']}; completed = {}; captured = {}; producers = {}
    replay_id = canonical({'suite':canonical(suite),'output':str(output),'started_at':receipt['started_at'],'runner':evidence['runner_sha256']})
    current = results['_prerequisites']; current['started_at'] = utc(); prerequisite_log = logs/'prerequisites.log'
    controls = indexed(suite['controls']); archive = None; archive_inventory = None
    def save():
        receipt['stages'] = [{key:row[key] for key in ('id','terminal','exit_code','log_sha256')} for row in evidence['stage_results']]
        receipt['log_sha256'] = canonical({row['id']:row['log_sha256'] for row in evidence['stage_results']})
        write_json(output/'RECEIPT.json',receipt)
    save()
    try:
        resolved,fingerprints,dependencies,env,input_hashes = _verify_environment(suite,plan,tools,inputs,output)
        evidence['tool_fingerprints']=fingerprints; evidence['dependency_checks']=dependencies
        family = d04_contracts()['families'][plan['d04_family']]
        archive = path_in(output,'archives/source-archive'); archive_inventory = extract_source_zip(inputs['source-archive'],archive)
        source_root = path_in(archive,family['archive_root'],dot=True) if family['archive_root'] else archive
        for driver in plan['drivers'].values(): d04_source_inventory(driver['recipe'],source_root)
        prerequisite_log.write_text('Exact D04 tools, dependencies, archive and original source inventory verified.\n')
        current.update(terminal='COMPLETED',exit_code=0,ended_at=utc(),log_sha256=sha(prerequisite_log.read_bytes()))
        mappings = {'project':project,'out':output,'build':output/'build','adapter':Path(__file__).resolve(),'archive:source-archive':source_root}
        mappings.update({'tool:'+name:path.resolve() for name,path in resolved.items()})
        if 'mathlib' in tools:mappings['dependency:mathlib']=Path(tools['mathlib']).resolve()
        for did,driver in plan['drivers'].items():mappings['driver:'+did]=path_in(source_root,d04_contracts()['recipes'][driver['recipe']]['source_member'])
        for sid,stage in plan['stages'].items():
            current=results[sid];current['started_at']=utc();log=logs/(sid+'.log');driver=plan['drivers'].get(stage['driver_id'])
            for parent in stage['depends_on']:require(completed.get(parent,{}).get('matched')is True,'D04 prior stage did not satisfy its contract')
            for name in stage['output_paths']:
                path=path_in(output,name);require(not path.exists(),'D04 declared output already exists');path.parent.mkdir(parents=True,exist_ok=True)
            if stage['argv'][:1]==['{builtin:observe-child}']:
                pid,child=stage['argv'][1:];observed=captured[(pid,child)]
                child_log=path_in(output,observed['captured_log_path']);require(sha(child_log.read_bytes())==observed['log_sha256'],'D04 captured child log changed before observation')
                log.write_bytes(child_log.read_bytes())
                run={'terminal':observed['terminal'],'exit_code':observed['exit_code'],'started_at':current['started_at'],'ended_at':utc(),'log_sha256':observed['log_sha256']}
                evidence['child_observations'].append({**observed,'stage_id':sid,'observed_at':run['ended_at']})
            elif driver:
                run,invocation=d04_run_parent(stage,driver,plan,output,mappings,env,log,replay_id,producers)
                evidence['driver_invocations'].append(invocation);current.update(run);save()
                resource=(run['terminal']!='COMPLETED' or any(row['record']['terminal']in{'TIMEOUT','INTERRUPTED','RUNNING'} or
                    re.search(r'timed out|out of memory|maximum (?:number of heartbeats|recursion depth)|deterministic timeout|WALL_CLOCK_LIMIT',
                        bytes.fromhex(row['log_hex']or'').decode('utf-8',errors='replace'),re.I) for row in invocation['capture_records']))
                if resource:receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1)
                require(invocation['capture_error'] is None,'D04 physical capture could not be parsed: '+str(invocation['capture_error']))
                require(not resource,'Resource-inconclusive D04 physical parent/child')
                require(run['exit_code']==0,'D04 original/translated physical parent failed')
                d04_validate_captured_invocation(invocation,plan,current,True)
                normalization=d04_normalize(driver['recipe'],source_root,d04_parent_paths(driver['recipe'],output),run,log.read_text(encoding='utf-8'))
                qualified={**invocation,'normalization':normalization,'normalization_sha256':canonical(normalization)}
                d04_bind_normalization(qualified)
                qualified['qualified_objects']=d04_object_outputs(plan,driver['recipe'],qualified)
                children,new_producers=d04_observations(qualified,plan,current)
                invocation.update(qualified)
                evidence['output_hashes'].update(invocation['qualified_objects'])
                captured.update(children);producers.update(new_producers)
            else:
                argv=[_expand(arg,mappings)for arg in stage['argv']]
                run=run_process(argv,path_in(project,stage['cwd'],dot=True),stage_environment(stage,plan,output,env),log,stage['timeout_seconds'])
            current.update(run);text=log.read_text(encoding='utf-8',errors='replace')
            if run['terminal']!='COMPLETED':receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1);raise ValueError('Resource-inconclusive D04 stage')
            assess_stage(stage,run,text,completed)
            if driver is None and stage['argv'][-1].startswith('{project}/'):
                name=stage['argv'][-1][len('{project}/'):]
                names=source_readback_names_in_plan(plan['file_paths'][name]['source_id'],plan)
                if names:check_original_readbacks(text,names)
            current['output_hashes']={name:_file_hashes(path_in(output,name))for name in stage['output_paths']}
            evidence['output_hashes'].update(current['output_hashes']);completed[sid]={**run,'matched':True}
            for cid in stage['control_ids']:
                control=controls[cid];actual=control['expected_outcome']
                receipt['controls'].append({key:control[key]for key in('id','source_id','target_id','role','expected_outcome_sha256')}|{
                    'actual_outcome':actual,'actual_outcome_sha256':sha(actual.encode()),'terminal':run['terminal'],'exit_code':run['exit_code'],'log_sha256':run['log_sha256']})
                evidence['control_diagnostics'].append({'control_id':cid,'stage_id':sid,'prerequisite_stage_ids':stage['depends_on'],
                    'expected':stage['expected_diagnostics'],'observed_log_sha256':run['log_sha256'],'match':'MATCHED'})
            save()
        if plan['targets']:
            d04_verify_target_objects(plan,evidence,output)
            generated=output/'generated';generated.mkdir();audit=generated/'V5SuccessorReadback.lean'
            audit.write_text(_audit_source(list(plan['targets'].values())),encoding='utf-8')
            current=results['_target_audit'];log=logs/'target-audit.log'
            run=run_process([resolved['lean'],'-j1',audit],project,env,log,current['budget_seconds']);current.update(run)
            if run['terminal']!='COMPLETED':receipt.update(outcome='RESOURCE_INCONCLUSIVE',exit_code=1)
            require(run['terminal']=='COMPLETED'and run['exit_code']==0,'D04 target proof-closure audit failed')
            audits=parse_readbacks(log.read_text(encoding='utf-8'),list(plan['targets'].values()))
            evidence['target_audits']=[{'target_id':tid,**value,'stage_id':'_target_audit','log_sha256':run['log_sha256']}for tid,value in audits.items()]
            receipt['axioms']=sorted({a for value in audits.values()for a in value['axioms']})
        for name,path in resolved.items():require(sha(path.read_bytes())==fingerprints[name]['executable_sha256'],'D04 tool changed during execution')
        for iid,row in plan['inputs'].items():require(_input_inventory(row,inputs[iid],plan)==input_hashes[iid],'D04 external archive changed')
        actual={p.relative_to(archive).as_posix():sha(no_symlinks(p).read_bytes())for p in archive.rglob('*')if p.is_file()}
        require(actual==archive_inventory,'D04 original extracted source bytes changed')
        for sid,row in plan['files'].items():require(path_in(project,row['path']).read_bytes()==plan['contents'][sid],'D04 public projection changed')
        evidence['source_hashes_after']={sid:sha(public_bytes(root,sources[sid]))for sid in suite['source_ids']}
        receipt['target_readbacks']=[{key:target[key]for key in('source_id','target_sha256')}|{'target_id':target['id'],'outcome':'CHECKED'}for target in suite['targets']]
        selected=suite['replay']['scope'];receipt.update(outcome={'COMPONENTS':'FRESH_KERNEL_COMPONENTS','DECLARED_SUITE':'QUALIFIED_DECLARED_SUITE'}[selected],exit_code=0,proof_scope=selected)
    except (FileNotFoundError,ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        write_json(output/'FAILURE.json',{'stage_id':current['id'],'observed_at':utc(),'error':type(error).__name__+': '+str(error)})
        if isinstance(error,MissingInput):receipt.update(outcome='BLOCKED_EXTERNAL_INPUT',exit_code=2)
        elif isinstance(error,MissingTool):receipt.update(outcome='BLOCKED_TOOLCHAIN',exit_code=2)
        elif receipt['outcome']!='RESOURCE_INCONCLUSIVE':receipt.update(outcome='FAILED',exit_code=1)
        receipt['proof_scope']='NONE'
        if current['terminal']=='SKIPPED':
            failure=logs/(current['id']+'-failure.log');failure.write_text(type(error).__name__+': '+str(error)+'\n')
            current.update(terminal='MISSING'if isinstance(error,FileNotFoundError)else'COMPLETED',exit_code=None if isinstance(error,FileNotFoundError)else 1,ended_at=utc(),log_sha256=sha(failure.read_bytes()))
    receipt['ended_at']=utc();save();validate_receipt(receipt,suite,sources,root)
    return receipt


def d04_record_bytes(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8')


def d04_collect_capture(invocation, contract, trace, parent, plan):
    if not trace.exists(): return
    manifest = {p.relative_to(trace).as_posix():sha(no_symlinks(p).read_bytes()) for p in sorted(trace.rglob('*')) if p.is_file()}
    invocation['trace_manifest']=manifest;invocation['trace_sha256']=canonical(manifest)
    launch=trace/'LAUNCH.json'
    if launch.is_file():invocation['trace_launch']=read_json(launch)
    paths=sorted(trace.glob('[0-9][0-9][0-9][0-9].json'))+sorted(trace.glob('probe-[0-9][0-9][0-9][0-9].json'))
    for path in paths:
        row=read_json(path);log=path_in(trace,row['log_file'])
        streams={}
        if row['capture']=='SEPARATE_BYTES':
            for stream in ['stdout','stderr']:
                p=trace/(path.stem+'.'+stream+'.log')
                if p.is_file():streams[stream]=p.read_bytes().hex()
        invocation['capture_records'].append({'record':row,'record_file':path.name,'record_file_sha256':sha(path.read_bytes()),
            'log_hex':log.read_bytes().hex()if log.is_file()else None,'stream_hex':streams})
    invocation['child_count']=sum(not row['record']['probe'] for row in invocation['capture_records'])
    invocation['probe_count']=sum(row['record']['probe'] for row in invocation['capture_records'])


def d04_normalizer_module(name):
    import importlib.util
    path=d04_asset(name+'.py');spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module


def d04_normalize(recipe, source_root, output, physical, parent_text):
    base=d04_normalizer_module('v5_d04_normalizers_base');translated=d04_normalizer_module('v5_d04_normalizers_translated')
    if recipe=='t07-criterion-translated-v1':result=translated.criterion(source_root,output,physical)
    elif recipe=='t07-covering-translated-v1':result=translated.covering(source_root,output,physical)
    elif recipe=='t07-composition-projection-v1':result=translated.composition_projection(source_root,physical,parent_text)
    elif recipe=='t07-composition-packaging-translated-v1':result=translated.composition_packaging(source_root,output,physical)
    elif recipe=='t07-composition-original-v1':result=translated.composition_main(source_root,output,physical)
    elif recipe=='t07-composition-review-translated-v1':result=translated.composition_review(source_root,output,physical)
    elif recipe=='t07-composition-serial-mutations-v1':result=translated.composition_mutations(source_root,output,physical,d04_asset('check_mutations_serial.py'))
    elif recipe in {'t07-dynamic-base-v1','t07-dynamic-attribution-v1'}:
        children,summary,sources=base.dynamic(recipe.removesuffix('-v1'),source_root,output)
        result={'children':children,'summary':summary,'source_hashes_read_back':sources}
    elif recipe=='t07-dynamic-independent-root-image-v1':
        require(physical['terminal']=='COMPLETED' and physical['exit_code']==0,'Independent root-image physical parent failed')
        detail=base.read_json(output,'INDEPENDENT_ROOT_IMAGE_RESULTS.json')
        require(detail['status']=='PASS_REVIEWER_ROOT_IMAGE_CHECKS' and detail['m_min']==2 and detail['m_max']==7 and detail['B0_forced_bridge_exception_confirmed']is True and detail['author_code_imported']is False,'Incomplete independent finite root-image controls')
        for key in ['explicit_partition_pair_cases','robust_safety_equivalences_B_ge_1','actual_fault_world_instantiations','canonical_maximal_world_realizations','arbitrary_family_obstruction_parameter_cases']:
            require(type(detail[key])is int and detail[key]>0,'Missing original finite root-image counter')
        result={'children':[],'summary':detail}
    else:raise ValueError('No D04 normalizer fallback')
    return {'recipe':recipe,'normalizer_assets':{name:row['sha256']for name,row in d04_contracts()['adapter_assets'].items()if name.startswith('v5_d04_normalizers_')},'result':result}


def d04_fixed_summary(recipe):
    return d04_contracts()['recipes'][recipe].get('fixed_summary')


def d04_bind_normalization(invocation):
    normalization=invocation['normalization'];require(normalization is not None and canonical(normalization)==invocation['normalization_sha256'],'Missing/mutated D04 normalization')
    keys(normalization,{'recipe','normalizer_assets','result'})
    require(normalization['recipe']==invocation['recipe'],'D04 normalization belongs to another recipe')
    require(normalization['normalizer_assets']=={name:row['sha256']for name,row in d04_contracts()['adapter_assets'].items()if name.startswith('v5_d04_normalizers_')},'D04 normalizer identity changed')
    captures={row['record']['id']:row['record']for row in invocation['capture_records']if not row['record']['probe']}
    result=normalization['result'];children=result.get('children',[])
    expected=set(captures)
    if invocation['recipe']=='t07-composition-serial-mutations-v1':expected={name for name in expected if name.endswith('/runtime')}
    require({row['id']for row in children}==expected and len(children)==len(expected),'D04 normalized original child census differs')
    for row in children:
        captured=captures[row['id']]
        require(row['log_sha256']==captured['log_sha256'],'D04 normalizer attached another child log')
        if 'exit_code'in row:require(row['exit_code']==captured['exit_code'],'D04 normalized child exit differs from actual capture')
        if 'terminal'in row:require(row['terminal']==captured['terminal'],'D04 normalized child terminal differs from actual capture')
        for key in ['argv','actual_argv']:
            if key in row:require(row[key]==captured['argv'],'D04 source journal argv differs from physical capture')
        if 'cwd'in row:require(row['cwd']==captured['cwd'],'D04 source journal cwd differs from physical capture')
        if 'started_at'in row:require(row['started_at']<=captured['started_at']<=captured['ended_at']<=row['ended_at'],'D04 source journal does not enclose actual physical child')
    summary=result['summary'];recipe=invocation['recipe']
    if recipe in {'t07-criterion-translated-v1','t07-covering-translated-v1','t07-composition-original-v1','t07-composition-review-translated-v1'}:
        actual_objects={Path(path).stem:value for row in captures.values()for path,value in row['output_hashes'].items()if path.endswith('.olean')and row['exit_code']==0}
        require(result.get('objects')==actual_objects,'D04 normalizer objects differ from actual captured producer outputs')
    if recipe in {'t07-dynamic-base-v1','t07-dynamic-attribution-v1'}:
        require(result.get('source_hashes_read_back')==d04_contracts()['recipes'][recipe]['normalized_source_hashes'],'D04 original source readback inventory differs')
    fixed=d04_fixed_summary(recipe)
    if fixed is not None:require(summary==fixed,'D04 exact source-owned finite summary changed')
    expected_summary={
        't07-criterion-translated-v1':{'tests':44,'repair_cases':393216,'installation_cases':4096,'source_bytes':3013},
        't07-composition-packaging-translated-v1':{'packaging_tests':4},
        't07-composition-original-v1':{'native_assertions':88,'wrapper_tests':7,'finite_cases':{'revocation':80,'cancellation':60,'open_withheld':20,'two_batch_taint_sets':5,'macro_attempts':40},'source_bytes':3013},
        't07-composition-review-translated-v1':{'native_assertions':25,'monotonicity_readbacks':3},
        't07-composition-serial-mutations-v1':{'runtime_mutants':6,'actual_driver_processes':66}}
    if recipe in expected_summary:require(summary==expected_summary[recipe],'D04 source-specific normalized result meaning changed')
    elif recipe=='t07-covering-translated-v1':
        require(summary['status']=='PASS'and summary['author_mutations_rejected']==6 and summary['independent_primary_mutations_rejected']==6 and summary['lean_sha256']==LEAN_SHA and summary['mathlib_revision']=='c44e0c8ee63ca166450922a373c7409c5d26b00b','D04 covering result meaning changed')
        require(all(summary[key]is True for key in ['normal_and_optimized_semantic_results_match_archived_evidence','immutable_payload_before_after','successful_compiler_logs_clean']),'D04 covering result condition omitted')
    elif recipe=='t07-composition-projection-v1':
        require(summary['status']=='PASS'and summary['scope']=='Explicit public projection; no claim of full original-packet inclusion','D04 projection claim changed')
        require(all(type(summary[key])is int and summary[key]>=0 for key in ['retained','independent_review','added','excluded']),'D04 projection census invalid')
    elif recipe=='t07-dynamic-independent-root-image-v1':
        require(summary['status']=='PASS_REVIEWER_ROOT_IMAGE_CHECKS'and summary['m_min']==2 and summary['m_max']==7 and summary['B0_forced_bridge_exception_confirmed']is True and summary['author_code_imported']is False,'D04 root-image claim changed')
    elif recipe in {'t07-dynamic-base-v1','t07-dynamic-attribution-v1'}:
        require(isinstance(summary['finite_counts'],dict)and summary['finite_counts'],'D04 finite source census omitted')
        if recipe=='t07-dynamic-base-v1':
            require(summary['finite_adverse_outcomes']=={'cached_votes':'UNSAFE','mutable_payload':'UNSAFE','current_authorization_deleted':'UNSAFE','common_downstream_writer':'UNSAFE','common_selector_omitted':'SAFE_BUT_NEVER_RESTORED','two_B_plus_one_failed_candidate':'UNSAFE','immediate_external_revocation':'UNSAFE','instantaneous_budget_failed_candidate':'FAILS_LIFETIME_PREMISE','perpetual_version_change_prefix':'SAFE_NONPERSISTENT_PREFIX','too_small_cancellation_certificate':'LATE_WRITE_AFTER_FALSE_CANCELLATION'},'D04 finite adverse outcomes changed')
        else:require(set(summary['finite_counterexamples'])=={'five_labels_four_gate_liveness_failure','five_labels_stale_landing','two_cancel_labels_not_two_roots','forced_alias_bridge'},'D04 fixed-map counterexample census changed')


def d04_capture_specs(invocation):
    contract=d04_contracts()['recipes'][invocation['recipe']];bindings=dict(invocation['bindings'],source=invocation['source_root'],out=invocation['output_root'],trace=invocation['output_root']+'/traces/'+invocation['parent_stage_id'])
    if contract.get('temporary_cwd_binding'):
        children=[item['record']for item in invocation['capture_records']if not item['record']['probe']]
        if children:
            cwd=PurePosixPath(children[0]['cwd']);tmp=PurePosixPath(invocation['output_root'])/'tmp'
            prefix='dynamic-interlock-replay-'if invocation['recipe']=='t07-dynamic-base-v1'else'root-attribution-replay-'
            require(cwd.parent==tmp and cwd.name.startswith(prefix),'D04 captured temporary module root escaped fresh output')
            bindings[contract['temporary_cwd_binding']['token'][1:-1]]=str(cwd)
    return contract,bindings


def d04_validate_captured_invocation(invocation, plan, parent, require_complete):
    keys(invocation,{'parent_stage_id','recipe','driver_sha256','source_argv','launch_argv','actual_launch_argv','launch_cwd','helper_argv','helper_sha256',
        'runner_sha256','contract_data_sha256','context_sha256','source_root','output_root','bindings','replay_id','trace_sha256','trace_manifest',
        'trace_launch','parent_log_sha256','child_count','probe_count','capture_records','normalization','normalization_sha256','qualified_objects','capture_error','raw_capture_files'})
    recipe=invocation['recipe'];contract,bindings=d04_capture_specs(invocation)
    family=d04_contracts()['families'][contract['family']]
    require(family['suite_id']==plan['d04_suite']['id'] and invocation['parent_stage_id']==contract['parent_stage']['id'],'D04 captured recipe/parent mismatch')
    require(invocation['source_argv']==contract['parent_stage']['argv'] and invocation['driver_sha256']==contract['source_sha256'],'D04 source-facing invocation changed')
    require(invocation['contract_data_sha256']==D04_DATA_SHA256,'D04 execution contract data differs')
    output=PurePosixPath(invocation['output_root']);require(output.is_absolute(),'D04 replay output identity is not absolute')
    d04_check_bindings(recipe,invocation['bindings'],str(output))
    expected_source=output/'archives/source-archive'/family['archive_root']
    require(invocation['source_root']==str(expected_source),'D04 original archive root differs')
    require(invocation['bindings']['out']==str(output),'D04 replay binding changed')
    launch=['{tool:python}','-B','{adapter}','--trace-d04','{out}/contexts/'+invocation['parent_stage_id']+'.json']
    require(invocation['launch_argv']==launch and invocation['actual_launch_argv']==d04_expand(launch,bindings),'D04 actual tracer launch differs')
    helper,args,cwd=d04_launch_description(recipe,bindings)
    require(invocation['helper_argv']==[str(helper),*args]and invocation['launch_cwd']==str(cwd),'D04 actual helper argv/cwd differs')
    require(invocation['helper_sha256']==(contract['translation_sha256']or contract['source_sha256']),'D04 actual helper identity differs')
    require(invocation['parent_log_sha256']==parent['log_sha256'],'D04 physical parent/log association differs')
    digest(invocation['runner_sha256']);digest(invocation['context_sha256']);digest(invocation['replay_id'])
    if invocation['capture_error'] is not None:
        require(not require_complete and invocation['normalization'] is None and invocation['normalization_sha256'] is None and invocation['qualified_objects']=={},'D04 unparsed capture acquired qualification')
        require(isinstance(invocation['capture_error'],str) and invocation['capture_error'],'D04 malformed capture error')
        manifest={}
        for name,payload in invocation['raw_capture_files'].items():
            relative(name);manifest[name]=sha(bytes.fromhex(payload))
        require(manifest==invocation['trace_manifest'] and invocation['trace_sha256']==(canonical(manifest) if manifest else None),'D04 failed raw capture custody differs')
        return
    require(invocation['raw_capture_files']=={},'D04 successful parser has unexplained raw capture fallback')
    manifest={};raw_launch=invocation['trace_launch']
    if raw_launch is not None:
        require(raw_launch=={'recipe':recipe,'parent_stage_id':invocation['parent_stage_id'],'context_sha256':invocation['context_sha256'],
            'runner_sha256':invocation['runner_sha256'],'original_source_sha256':contract['source_sha256'],
            'helper_sha256':invocation['helper_sha256'],'helper_argv':invocation['helper_argv'],'helper_cwd':invocation['launch_cwd'],'mechanism':'RUNPY_IN_TRACER'},'D04 traced helper launch changed')
        manifest['LAUNCH.json']=sha(d04_record_bytes(raw_launch))
    rows=[item for item in invocation['capture_records']if not item['record']['probe']]
    probes=[item for item in invocation['capture_records']if item['record']['probe']]
    require(invocation['child_count']==len(rows)<=len(contract['children'])and invocation['probe_count']==len(probes)<=len(contract.get('tool_probes',[])),'D04 physical child census invalid')
    require([item['record']['id']for item in rows]==[row['id']for row in contract['children'][:len(rows)]],'D04 omitted/reordered/repeated child')
    require([item['record']['index']for item in probes]==list(range(len(probes))),'D04 omitted/reordered/repeated tool probe')
    if require_complete:require(len(rows)==len(contract['children'])and len(probes)==len(contract.get('tool_probes',[]))and raw_launch is not None,'D04 successful parent lacks complete physical capture')
    last=parent['started_at']
    for item in [*probes,*rows]:
        row=item['record']
        require(last is not None and last<=row['started_at'],'D04 original serial physical intervals overlap or reorder')
        last=row['ended_at']
    for item in invocation['capture_records']:
        keys(item,{'record','record_file','record_file_sha256','log_hex','stream_hex'})
        row=item['record'];probe=row['probe'];index=row['index'];require(type(index)is int and index>=0 and type(probe)is bool,'D04 capture index malformed')
        keys(row,{'id','index','probe','recipe','replay_id','parent_stage_id','argv','cwd','timeout_seconds','capture','stdin','environment_sha256',
            'source_binding','input_bindings','source_hashes','replacement_bindings','started_at','ended_at','terminal','exit_code','log_sha256','stream_hashes','output_hashes','log_file'})
        name=('probe-'if probe else'')+f'{index:04}'
        require(item['record_file']==name+'.json'and row['log_file']==name+'.log','D04 capture/log filename association differs')
        require(sha(d04_record_bytes(row))==item['record_file_sha256'],'D04 physical record digest differs')
        manifest[name+'.json']=item['record_file_sha256']
        require(row['recipe']==recipe and row['parent_stage_id']==invocation['parent_stage_id']and row['replay_id']==invocation['replay_id'],'D04 capture belongs to another physical run')
        if probe:
            require(index<len(contract.get('tool_probes',[])),'D04 foreign tool probe')
            spec=d04_expand(contract['tool_probes'][index],bindings)
            require(row['id']=='probe-'+str(index)and row['argv']==spec['argv']and row['cwd']==spec['cwd']and row['timeout_seconds']is None and row['capture']==spec['capture'],'D04 original probe contract differs')
            require(row['source_binding']=={'kind':'TOOL_PROBE','tool_name':'lean','executable_sha256':LEAN_SHA,'driver_sha256':contract['source_sha256']}and row['input_bindings']==[]and row['source_hashes']=={}and row['output_hashes']=={},'D04 tool probe acquired scientific identity')
            require(row['replacement_bindings']==[],'D04 tool probe acquired replacement authority')
        else:
            require(index<len(contract['children'])and contract['children'][index]['id']==row['id'],'D04 original child index differs')
            spec=d04_expand(contract['children'][index],bindings)
            d04_check_invocation(spec,row['argv'],row['cwd'],timeout_seconds=row['timeout_seconds'],capture=row['capture'],stdin=row['stdin'])
            expected_inputs=[binding for binding in spec['sources']if binding['kind']!='TOOL_PROBE']
            require(len(row['input_bindings'])==len(expected_inputs),'D04 captured source inventory differs')
            expected_hashes={}
            for actual,expected in zip(row['input_bindings'],expected_inputs):
                require({k:v for k,v in actual.items()if k!='actual_sha256'}==expected,'D04 child actual source binding differs')
                digest(actual['actual_sha256'])
                expected_digest=expected.get('sha256')or expected.get('expected_sha256')
                if expected_digest is not None:require(actual['actual_sha256']==expected_digest,'D04 child used changed source bytes')
                expected_hashes[expected.get('member')or expected.get('origin_member')or expected['path']]=actual['actual_sha256']
            require(row['source_hashes']==expected_hashes,'D04 source hash summary differs from actual inputs')
            binding=dict(spec['source_binding'])
            if binding['kind']=='GENERATED_BY_ORIGINAL':binding['generated_sha256']=row['input_bindings'][0]['actual_sha256']
            require(row['source_binding']==binding,'D04 executed source classification/identity differs')
            require(set(row['output_hashes'])<=set(spec['outputs']),'D04 captured foreign output')
            require(len(row['replacement_bindings'])==len(spec['replace_fresh_predecessor']),'D04 exact fresh replacement evidence omitted')
            for actual,expected in zip(row['replacement_bindings'],spec['replace_fresh_predecessor']):
                require({k:v for k,v in actual.items()if k not in{'actual_sha256','producer_capture_sha256'}}==expected,'D04 changed replacement contract')
                digest(actual['actual_sha256']);digest(actual['producer_capture_sha256'])
        digest(row['environment_sha256'])
        require(row['stdin']=={'mode':'INHERITED_NO_INPUT','data_sha256':None},'D04 original stdin contract changed')
        for value in row['output_hashes'].values():digest(value)
        require(isinstance(row['started_at'],str)and row['started_at'].endswith('Z')and parent['started_at']<=row['started_at']<=parent['ended_at'],'D04 child start outside actual parent interval')
        if row['terminal']=='RUNNING':
            require(not require_complete and row['ended_at']is None and row['exit_code']is None and item['log_hex']is None and row['log_sha256']is None and row['output_hashes']=={} and row['stream_hashes']=={} and item['stream_hex']=={},'D04 running child has fabricated terminal credit')
            continue
        require(row['terminal']in{'COMPLETED','TIMEOUT','INTERRUPTED','LAUNCH_ERROR'}and isinstance(row['ended_at'],str)and row['started_at']<=row['ended_at']<=parent['ended_at'],'D04 actual child terminal/interval differs')
        if row['terminal']=='COMPLETED':require(type(row['exit_code'])is int and 0<=row['exit_code']<124,'D04 invalid completed exit')
        else:require(row['exit_code']is None,'D04 incomplete child has fabricated exit')
        log=bytes.fromhex(item['log_hex']);require(sha(log)==row['log_sha256'],'D04 actual child log changed')
        manifest[name+'.log']=row['log_sha256']
        if row['capture']=='SEPARATE_BYTES':
            require(set(item['stream_hex'])==set(row['stream_hashes'])=={'stdout','stderr'},'D04 separate streams missing')
            streams={key:bytes.fromhex(value)for key,value in item['stream_hex'].items()}
            require(log==streams['stdout']+streams['stderr'],'D04 original byte-stream assembly differs')
            for key,value in streams.items():require(sha(value)==row['stream_hashes'][key],'D04 stream digest differs');manifest[name+'.'+key+'.log']=sha(value)
        else:require(item['stream_hex']=={}and row['stream_hashes']=={},'D04 unexpected separate stream evidence')
        if require_complete:
            if probe:require(row['terminal']=='COMPLETED'and row['exit_code']==0,'D04 original tool probe failed')
            else:require(d04_assess_captured_child(spec,row,log,parent)['outcome']in{'ACCEPT','REJECT'},'D04 resource-limited child cannot qualify')
    require(manifest==invocation['trace_manifest'],'D04 trace manifest differs from captured files')
    require(invocation['trace_sha256']==(canonical(manifest)if manifest else None),'D04 physical trace digest differs')


def d04_observations(invocation, plan, parent):
    recipe=invocation['recipe'];contract,bindings=d04_capture_specs(invocation);children={};producers={}
    for item in invocation['capture_records']:
        row=item['record']
        if row['probe']:continue
        spec=d04_expand(contract['children'][row['index']],bindings)
        outcome=d04_assess_captured_child(spec,row,bytes.fromhex(item['log_hex']),parent)['outcome']
        observation={'source_child_id':row['id'],'parent_stage_id':invocation['parent_stage_id'],'driver_sha256':invocation['driver_sha256'],
            'parser_id':recipe,'mode':'NONEXECUTING_OBSERVATION','argv_provenance':'CAPTURED','source_binding':row['source_binding'],
            'argv':row['argv'],'cwd':row['cwd'],'started_at':row['started_at'],'ended_at':row['ended_at'],
            'physical_run_sha256':invocation['trace_sha256'],'parent_log_sha256':invocation['parent_log_sha256'],
            'terminal':row['terminal'],'exit_code':row['exit_code'],'actual_outcome':outcome,'log_sha256':row['log_sha256'],
            'result_record_sha256':canonical(row),'output_hashes':row['output_hashes'],
            'captured_log_path':'traces/'+invocation['parent_stage_id']+'/'+row['log_file']}
        children[(invocation['parent_stage_id'],row['id'])]=observation
        if row['exit_code']==0:
            for path,value in row['output_hashes'].items():
                captured={'replay_id':row['replay_id'],'recipe':recipe,'child_id':row['id'],'terminal':'COMPLETED','exit_code':0,
                    'source_hashes':row['source_hashes'],'output_hashes':row['output_hashes'],'capture_record_sha256':canonical(row)}
                producers[(recipe,row['id'],path)]={**captured,'path':path,'sha256':value,'producer_record':captured,'producer_record_sha256':canonical(captured)}
    return children,producers


def d04_verify_target_objects(plan, evidence, output):
    definitions=d04_contracts()['families'][plan['d04_family']]['object_producers']
    stages=indexed(evidence['stage_results']);launches=indexed(evidence['driver_invocations'],'parent_stage_id')
    for module,producer in definitions.items():
        path=d04_expand(producer['path'],{'out':str(output)});relative_path=Path(path).relative_to(output).as_posix()
        require(Path(path).is_file()and sha(no_symlinks(path).read_bytes())==evidence['output_hashes'].get(relative_path),'D04 target/import object is absent or not its exact fresh output')
        if 'stage_id'in producer:
            row=stages[producer['stage_id']];require(row['terminal']=='COMPLETED'and row['exit_code']==0 and row['output_hashes'].get(relative_path)==evidence['output_hashes'][relative_path],'D04 target object lacks its explicit closure compiler stage')
        else:
            pid=d04_contracts()['recipes'][producer['recipe']]['parent_stage']['id'];invocation=launches[pid]
            require(invocation['qualified_objects'].get(relative_path)==evidence['output_hashes'][relative_path],'D04 target object is not qualified from its original producer')


def d04_expected_objects(plan, invocation):
    definitions=d04_contracts()['families'][plan['d04_family']]['object_producers']
    rows={item['record']['id']:item['record']for item in invocation['capture_records']if not item['record']['probe']};objects={}
    for module,producer in definitions.items():
        if producer.get('recipe')!=invocation['recipe']:continue
        row=rows[producer['child_id']];path=d04_expand(producer['path'],invocation['bindings'])
        source_id=plan['modules'][module]['source_id'];expected=sha(plan['contents'][source_id])
        require(any(item['actual_sha256']==expected and (item.get('sha256')or item.get('expected_sha256'))==expected for item in row['input_bindings']),'D04 target producer source differs from exact selected module')
        require(row['terminal']=='COMPLETED' and row['exit_code']==0 and path in row['output_hashes'],'D04 target lacks successful physical object producer')
        objects[producer['path'].removeprefix('{out}/')]=row['output_hashes'][path]
    return objects


def d04_validate_child_evidence(evidence, plan, stages, successful):
    parents={s['id']:s for s in plan['stages'].values()if s['driver_id']and s['argv'][0]!='{builtin:observe-child}'}
    declared={s['id']:s for s in plan['stages'].values()if s['argv'][0]=='{builtin:observe-child}'}
    launches=indexed(evidence['driver_invocations'],'parent_stage_id');observed=indexed(evidence['child_observations'],'stage_id')
    require(set(launches)<=set(parents)and set(observed)<=set(declared),'D04 foreign parent/child evidence')
    require(list(launches)==list(parents)[:len(launches)],'D04 physical parent launch order differs from source-owned stages')
    previous=None
    for sid in plan['stages']:
        row=stages.get(sid)
        if row is None or row.get('terminal')=='SKIPPED':continue
        require(previous is None or previous<=row['started_at'],'D04 actual sequential stage intervals overlap or reorder')
        previous=row['ended_at']
    if successful:require(set(launches)==set(parents)and set(observed)==set(declared),'D04 mandatory packaging/reviewer/original/child evidence omitted')
    expected_children={};qualified={};runs=set();producer_hashes={}
    for pid,invocation in launches.items():
        parent=stages[pid];require(invocation['runner_sha256']==evidence['runner_sha256'],'D04 child runner identity differs')
        complete=invocation['normalization']is not None
        if successful:require(complete and parent['terminal']=='COMPLETED'and parent['exit_code']==0,'D04 successful suite has an unqualified parent')
        d04_validate_captured_invocation(invocation,plan,parent,complete)
        if invocation['trace_sha256']is not None:
            require(invocation['trace_sha256']not in runs,'D04 duplicate physical trace credit');runs.add(invocation['trace_sha256'])
        if complete:
            require(parent['terminal']=='COMPLETED'and parent['exit_code']==0,'D04 failed parent cannot supply qualification')
            d04_bind_normalization(invocation)
            children,producers=d04_observations(invocation,plan,parent);expected_children.update(children)
            # Every generated input is tied to this run's prior successful producer.
            for item in invocation['capture_records']:
                row=item['record']
                for source in row['input_bindings']:
                    if source['kind']!='GENERATED_BY_ORIGINAL'or source.get('expected_sha256')is not None:continue
                    owner=source.get('producer_recipe')or invocation['recipe'];path=source.get('predecessor_path',source['path'])
                    key=(owner,source['producer'],path)
                    require(key in producer_hashes and producer_hashes[key]['sha256']==source['actual_sha256'],'D04 generated input has no exact earlier physical producer')
                for source in row['replacement_bindings']:
                    key=(source.get('producer_recipe')or invocation['recipe'],source['producer'],source.get('predecessor_path',source['path']))
                    require(key in producer_hashes and producer_hashes[key]=={'sha256':source['actual_sha256'],'record':source['producer_capture_sha256']},'D04 replacement lacks its exact fresh source/object/producer binding')
                if row['terminal']=='COMPLETED'and row['exit_code']==0:
                    for path,value in row['output_hashes'].items():producer_hashes[(invocation['recipe'],row['id'],path)]={'sha256':value,'record':canonical(row)}
            for path,value in invocation['qualified_objects'].items():
                require(path not in qualified and evidence['output_hashes'].get(path)==value,'D04 qualified object association changed');qualified[path]=value
            require(invocation['qualified_objects']==d04_expected_objects(plan,invocation),'D04 target object differs from its exact physical producer')
        else:require(invocation['normalization_sha256']is None and invocation['qualified_objects']=={},'D04 incomplete parent acquired normalized/object credit')
    for sid,row in observed.items():
        stage=declared[sid];key=tuple(stage['argv'][1:]);require(key in expected_children,'D04 observation lacks a qualified captured child')
        expected=expected_children[key]
        require({k:v for k,v in row.items()if k not in{'stage_id','observed_at'}}==expected,'D04 observation changed actual child facts')
        require(row['terminal']==stages[sid]['terminal']and row['exit_code']==stages[sid]['exit_code']and row['log_sha256']==stages[sid]['log_sha256'],'D04 observation stage differs from physical child')
        require(stages[key[0]]['ended_at']<=stages[sid]['started_at']<=row['observed_at']<=stages[sid]['ended_at'],'D04 observation time is not its actual parsing interval')
    expected_outputs=dict(qualified)
    for stage in stages.values():
        for name,value in stage.get('output_hashes',{}).items():
            require(name not in expected_outputs or expected_outputs[name]==value,'D04 stage/object output association differs')
            expected_outputs[name]=value
    require(evidence['output_hashes']==expected_outputs,'D04 output ledger differs from actual stage/qualified-object identities')


# Exact sibling helpers are loaded from verified source bytes. This adapter is
# also imported by file path without an entry in sys.modules or sys.path.
PORTABLE_HELPER_HASHES = {
    'portable_admission': '792f1256e5ebf0347ce6ea98092a5010fa5d3bdc7ba34801543763b331b3ce41',
    'portable_source': '51660284c5373639bab1e2ddf815295d29f94d753984c556738ffcf10111c3e5',
    'portable_collector': 'e28f3e2a4129b8834c3326d7810f460f38a524b92d6e1f099da71b34d9df78fc',
    'portable_capture': '362882a0e923d88bedf5266f52ccf3e685f4fd0fa0d57a8efb4538816fcf98a9',
    'portable_family': 'd4ad85333af8f8f90c9304873f574d5263b753661c40dadee0beecb0a7acfe7b',
}
PORTABLE_BINDINGS_SHA = '6eb339e70f570056a9bc7b110ae5d8652956646e749cce6062ccfd5b0fff8468'


def _portable_asset_bytes():
    directory = Path(__file__).resolve().parent
    payloads = {}
    for name, expected in PORTABLE_HELPER_HASHES.items():
        path = no_symlinks(directory / (name + '.py'))
        require(path.is_file(), 'Portable helper is unavailable: ' + name)
        data = path.read_bytes()
        require(sha(data) == expected, 'Portable helper bytes changed: ' + name)
        payloads[name] = (path, data)
    binding = no_symlinks(directory / 'portable_bindings_v2.json')
    require(binding.is_file() and sha(binding.read_bytes()) == PORTABLE_BINDINGS_SHA,
            'Portable binding bytes changed')
    return payloads


def _load_portable_components():
    from types import ModuleType
    payloads = _portable_asset_bytes()
    prior = {name: sys.modules[name] for name in payloads if name in sys.modules}
    loaded = {}
    try:
        for name, (path, data) in payloads.items():
            module = ModuleType(name)
            module.__file__ = str(path)
            module.__package__ = ''
            sys.modules[name] = module
            exec(compile(data, str(path), 'exec'), module.__dict__)
            loaded[name] = module
    finally:
        for name in payloads:
            if name in prior:
                sys.modules[name] = prior[name]
            else:
                sys.modules.pop(name, None)
    return tuple(loaded[name] for name in PORTABLE_HELPER_HASHES)


def _portable_api():
    _portable_asset_bytes()
    return SimpleNamespace(**globals())


(portable_admission, portable_source, portable_collector,
 portable_capture, portable_family) = _load_portable_components()
APPROVED_DECLARED_SUITES.update(portable_admission.APPROVED)





# Packaging-only: exact reviewed data and helper source, all hashes checked before execution.
OPERATIONAL_ASSETS_V1 = [('v5_operational_recipes_v1.json', 'b12cd58910c251d779c03bd49b86589d953e220c0bbc96e9c4975e3937bb856b', 3765409), ('v5_operational_assets_v1/admission.py', '30e181f2f78edba4b04c194d321ecf36ed6ec96f0dbe4115f37b4708154ffac6', 7050), ('v5_operational_assets_v1/direct_capture.py', '3a8a236b48071b97bdbd856fc51a30b2261773e1b29bf5763b79f7aef28bcfcb', 32638), ('v5_operational_assets_v1/process_capture.py', '67e3dc202456dc65477e9be1a5acd30392cd10e52a64686463040c4252db7614', 11464), ('v5_operational_assets_v1/normalizers.py', 'eb17520317ff8bc3b460240ef1d1e4ff956ccb877b0a50e558ac6677eca16ed1', 10775), ('v5_operational_assets_v1/runtime.py', '9a623fa6fa067fbf3db056681c9b516ee7bc47f416c7c4988cfe0aaf15703ed1', 10615), ('v5_operational_assets_v1/collection.py', 'eea54635fc257417b93cafee5a5ee24ddc3e290e09d481bf225de497eceeb20c', 22080), ('v5_operational_assets_v1/execution.py', '75ecd59d453a24da9554a907deafcf207a1ed13043687ccf57f6df5057b1e8f3', 17411)]

def _operational_asset_bytes_v1(name, expected, size):
    try:
        path = no_symlinks(Path(__file__).parent / name)
        require(path.is_file(), 'Missing operational asset')
        raw = path.read_bytes()
        require(len(raw) == size and sha(raw) == expected, 'Changed operational asset')
        return path, raw
    except (OSError, ValueError) as error:
        raise ValueError('Missing or changed operational asset: ' + name) from error

def _load_operational_assets_v1():
    global _OPERATIONAL_DATA
    verified = [_operational_asset_bytes_v1(*row) for row in OPERATIONAL_ASSETS_V1]
    _OPERATIONAL_DATA = json.loads(verified[0][1].decode('utf-8'))
    # Preserve the original adapter namespace, including __file__ and monkeypatch targets.
    # These are reviewed local assets, never producer-selected paths or archive programs.
    for path, raw in verified[1:]:
        exec(compile(raw, str(path), 'exec'), globals())

_load_operational_assets_v1()

# P1 assets are part of this reviewed adapter version, not descriptor inputs.
p1_asset_pins = {
    'v5_p1_recipes.json': {
        'sha256': '4ae8810e2dac517987ef93f383c597407792dc9bb8e37b7aa1fc1e4ef2967a81',
        'bytes': 24964,
    },
    'v5_p1_assets/p1_recipe.py': {
        'sha256': 'f4fbbcc61093bc3ec6467c836a65b8e97294eb9960c722701ba64bed0a91f7ab',
        'bytes': 102535,
    },
}


def p1_load_assets():
    from pathlib import Path
    import hashlib
    import json

    root = Path(__file__).absolute().parent
    content = {}
    for name, pin in p1_asset_pins.items():
        path = root / name
        if any(item.is_symlink() for item in (path, *path.parents)):
            raise ValueError('P1 asset path contains a symlink: ' + name)
        try:
            data = path.read_bytes()
        except OSError as error:
            raise ValueError('P1 reviewed asset is unavailable: ' + name) from error
        if len(data) != pin['bytes'] or hashlib.sha256(data).hexdigest() != pin['sha256']:
            raise ValueError('P1 reviewed asset identity changed: ' + name)
        content[name] = data
    # Check both assets before installing any P1 helper. The adapter namespace
    # retains its __file__, so source-facing tracing and runner identity agree.
    globals()['p1_meta'] = json.loads(content['v5_p1_recipes.json'])
    exec(compile(content['v5_p1_assets/p1_recipe.py'], str(root / 'v5_p1_assets/p1_recipe.py'), 'exec'), globals())


p1_load_assets()

# Exact, separately reviewed P1 tail continuation assets.
p1_tail_asset_pins = {'v5_p1_tail_recipes.json': {'sha256': '6efa11d4de88866abfaedb180d6c7a91ff6bd6a6bbe22d942ece3b52f4265d40', 'bytes': 200673}, 'v5_p1_tail_assets/p1_tail_recipe.py': {'sha256': '9892182cc5b2be498c146c35cd0dad1ab44aeb952e0fb601058c40438ae896be', 'bytes': 62081}}


def p1_tail_load_assets():
    content = {}
    base = Path(__file__).absolute().parent
    for name, pin in p1_tail_asset_pins.items():
        path = no_symlinks(base / name)
        try:
            data = path.read_bytes()
        except OSError as error:
            raise ValueError('P1 tail reviewed asset missing: ' + name) from error
        require(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'P1 tail reviewed asset identity changed: ' + name)
        content[name] = data
    globals()['p1_tail_meta'] = json.loads(content['v5_p1_tail_recipes.json'])
    exec(compile(content['v5_p1_tail_assets/p1_tail_recipe.py'], str(base / 'v5_p1_tail_assets/p1_tail_recipe.py'), 'exec'), globals())


p1_tail_load_assets()


# Accepted failed-tail receipts remain readable through this unrelated additive family.
p1_tail_accepted_predecessors = {**globals().get('p1_tail_accepted_predecessors', {}),
    'adf77b78db8b4d0cfb234f40aba6945b62de05972dc1e449a07e47ac6aed8ee1': p1_tail_clone(p1_tail_asset_pins)}
p1_tail_finish_asset_pins = {'v5_p1_tail_finish_recipes.json': {'sha256': '3e2252f43e8a1746f85cf84d4574a349004bcdad22f12d587ae769c3a15abfbc', 'bytes': 5643}, 'v5_p1_tail_finish_assets/p1_tail_finish_recipe.py': {'sha256': 'ec4f73806de730cc5d06493c32893dee3ec8ea43fc53e51823db5a26bde875b6', 'bytes': 39293}}

def p1_tail_finish_load_assets():
    base = Path(__file__).resolve().parent
    content = {}
    for name, pin in p1_tail_finish_asset_pins.items():
        raw = no_symlinks(path_in(base, name)).read_bytes()
        require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'P1 finish reviewed asset identity changed: ' + name)
        content[name] = raw
    globals()['p1_tail_finish_meta'] = json.loads(content['v5_p1_tail_finish_recipes.json'])
    name = 'v5_p1_tail_finish_assets/p1_tail_finish_recipe.py'
    exec(compile(content[name], str(base / name), 'exec'), globals())

p1_tail_finish_load_assets()




# Hash-bound selector/G1 assets. This does not admit a descriptor or run.
SELECTOR_G1_FAMILY_ASSET = 'replay_v5_successor_assets/selector_g1/replay_selector_g1.py'
SELECTOR_G1_FAMILY_SHA256 = '5d1d68841a1b9c7bccf1f3ac0918935ca4b25276c9c37e4171be7430d5b69c77'
SELECTOR_G1_FAMILY_BYTES = 89836
SELECTOR_G1_RECIPES = {'t09-selector-original-v2':'selector','t09-g1-author-original-v2':'g1','t09-g1-review-original-v2':'g1-review'}
SELECTOR_G1_IDS = {'d06-selector':'selector','d08-g1':'g1','d08-g1-review':'g1-review'}

def selector_g1_handles(suite):
    if not isinstance(suite,dict):return False
    if isinstance(suite.get('id'), str) and suite['id'] in SELECTOR_G1_IDS:return True
    replay=suite.get('replay');drivers=replay.get('drivers') if isinstance(replay,dict) else None
    return isinstance(drivers,list) and any(isinstance(d,dict) and isinstance(d.get('recipe'), str) and d['recipe'] in SELECTOR_G1_RECIPES for d in drivers)

def selector_g1_family_path():
    return no_symlinks(path_in(Path(__file__).resolve().parent,SELECTOR_G1_FAMILY_ASSET))

def selector_g1_load_family():
    import importlib.util
    path=selector_g1_family_path();raw=path.read_bytes()
    require(len(raw)==SELECTOR_G1_FAMILY_BYTES and sha(raw)==SELECTOR_G1_FAMILY_SHA256,'Changed selector/G1 family module')
    spec=importlib.util.spec_from_file_location('_v5_selector_g1_bound_family',path)
    module=importlib.util.module_from_spec(spec)
    # Execute the exact checked source bytes, without package initialization,
    # stale bytecode, import-path search, module caching or global registration.
    exec(compile(raw,str(path),'exec'),module.__dict__)
    require(module.SELECTOR_G1_RECIPES==SELECTOR_G1_RECIPES and module.SELECTOR_G1_IDS==SELECTOR_G1_IDS,'Changed family dispatch ownership')
    return module


def main():
    if sys.argv[1:2] == ['--trace-selector-g1']:
        require(len(sys.argv) == 4, 'Malformed internal selector/G1 trace invocation')
        family = selector_g1_load_family()
        return family.selector_g1_trace_main(family.selector_g1_adapter_view(globals()), sys.argv[2], Path(sys.argv[3]))
    if sys.argv[1:2] == ['--trace-p1-original']:
        return p1_trace_entry(p1_api(), sys.argv[2:])
    if sys.argv[1:2] == ["--trace-operational"]:
        require(len(sys.argv) >= 6, "Malformed internal operational trace invocation")
        return operational_trace(sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5:])
    if sys.argv[1:2] == ["--trace-operational-batch-source"]:
        require(len(sys.argv) == 12, "Malformed internal nested operational trace invocation")
        return operational_trace_batch_source(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    if sys.argv[1:2] == ['--trace-portable']:
        require(len(sys.argv) == 13, 'Malformed internal portable trace invocation')
        return portable_capture.trace_driver(_portable_api(), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5:])
    if sys.argv[1:2] == ['--portable-family']:
        return portable_family.command_line(_portable_api(), sys.argv[2:])
    if sys.argv[1:2] == ['--trace-d04']:
        require(len(sys.argv) == 3, 'Malformed D04 internal trace invocation')
        return d04_trace_entry(Path(sys.argv[2]))
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
    for name in ('list', 'check', 'project', 'execute', 'audit-continuation', 'history-audit-continuation', 'covering-audit-continuation', 'selector-audit-continuation'): mode.add_argument('--' + name, action='store_true')
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
        if args.selector_audit_continuation:
            require(args.prior is not None, 'Selector continuation requires the exact retained --prior run directory')
            receipt = execute_selector_audit_continuation(suite, sources, args.root, args.prior, args.out, tools, inputs, reviews=reviews)
        elif args.covering_audit_continuation:
            require(args.prior is not None, 'Covering continuation requires the exact retained --prior run directory')
            receipt = execute_covering_audit_continuation(suite, sources, args.root, args.prior, args.out, tools, inputs, reviews=reviews)
        elif args.history_audit_continuation:
            require(args.prior is not None, 'History continuation requires the exact retained --prior run directory')
            receipt = execute_history_audit_continuation(suite, sources, args.root, args.prior, args.out, tools, inputs, reviews=reviews)
        elif args.audit_continuation:
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
