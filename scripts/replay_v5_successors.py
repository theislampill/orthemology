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
    't11-dependent-all': 'b87aca15fb03afe740abc50aa8dfc00d5a9dbf59de7f0b61591123163f47ec8b',
    't11-normalization': '4653066edcd7df7c05addf7c81aa48ee9680c36f58a216ccd5c55d04d5763da6',
    't11-nucleus': 'f8d2057ed34df1260efafe16a2227400a9f9f5b2d9cc13b3d86105bf7d269160',
    't11-substitution': '39e05def1e6370039143ff47862774fc6dd1c4f9865f9b39827cdff43186f090',
    't14-identity': 'c065f772862ca55a9d7ac6ceb29c11439aa1574bf8dd8e37918a65dc77e9abdf',
    'd06-core-runtime': '2c0c433ba860bc33862a87dff2e4c22f3ec1d584b580a0605a1ffc8163844f8b',
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


def _validate_argv(stage, plan):
    argv = stage['argv']
    require(isinstance(argv, list) and argv and all(isinstance(a, str) and a and '\x00' not in a for a in argv), 'Missing explicit argument vector')
    driver = plan['drivers'].get(stage['driver_id'])
    if driver is not None:
        recipe = driver['recipe']
        if recipe == CORE_RECIPE:
            validate_core_argv(stage, driver, plan)
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
        require(stage['output_paths'] == [], 'Interpretation stage has undeclared outputs')
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


def traced_run(original_run, trace):
    """Capture actual subprocess.run calls without changing their return values."""
    count = 0
    def invoke(argv, *args, **kwargs):
        nonlocal count
        require(isinstance(argv, list) and argv and not args and not kwargs.get('shell') and
                kwargs.get('text') is True and kwargs.get('stdout') == subprocess.PIPE and
                kwargs.get('stderr') == subprocess.STDOUT, 'Unreviewed traced subprocess form')
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
            log = path_in(trace, f'{index:04}.log'); log.write_bytes(data)
            record.update(ended_at=utc(), terminal='TIMEOUT' if isinstance(error, subprocess.TimeoutExpired) else 'INTERRUPTED',
                          log_sha256=sha(data))
            write_json(destination, record)
            raise
        require(isinstance(result.stdout, str), 'Traced subprocess omitted its captured stdout')
        log = path_in(trace, f'{index:04}.log'); log.write_bytes(result.stdout.encode('utf-8'))
        completed = type(result.returncode) is int and 0 <= result.returncode < 124
        record.update(ended_at=utc(), terminal='COMPLETED' if completed else 'INTERRUPTED',
                      exit_code=result.returncode if completed else None, log_sha256=sha(log.read_bytes()))
        write_json(destination, record)
        return result
    return invoke


def trace_reviewed_commands(original_run, trace, commands, read_only_commands, seconds):
    """Only reviewed physical commands enter the child ledger, in source order."""
    capture = traced_run(original_run, trace); position = 0
    def invoke(argv, *args, **kwargs):
        nonlocal position
        require(isinstance(argv, list) and all(isinstance(a, str) for a in argv) and not args and not kwargs.get('shell'), 'Unreviewed original subprocess form')
        if argv in read_only_commands:
            require(set(kwargs) <= {'stdout', 'check', 'text', 'timeout'} and kwargs.get('timeout') is None and kwargs.get('stdout') == subprocess.PIPE and kwargs.get('check') is True, 'Changed read-only original command')
            return original_run(argv, **kwargs)
        require(position < len(commands) and argv == commands[position], 'Unreviewed or repeated original physical command')
        require(set(kwargs) <= {'env', 'stdout', 'stderr', 'text', 'timeout'} and kwargs.get('timeout') == seconds, 'Original child budget or subprocess contract changed')
        if '-o' in argv: require(not no_symlinks(argv[argv.index('-o') + 1]).exists(), 'Original child output already exists')
        position += 1
        return capture(argv, **kwargs)
    return invoke


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
            names = source_readback_names(plan['contents'][spec['source_id']].decode(), plan['targets'].values())
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
            if row['recipe'] == CORE_RECIPE:
                require(row['external_input_id'] in inputs, 'Original core archive is undeclared')
            else: require(row['external_input_id'] is None, 'Archive recipe is not approved by this adapter version')
            admitted_role = 'LOCK' if row['recipe'] == 't15-empirical-integrity-v1' else 'DRIVER'
            require(row['source_id'] in contents and files[row['source_id']]['role'] == admitted_role, 'Driver is not an exact projected source')
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
            elif row['recipe'] in NORMAL_SOURCE_RECIPES:
                require(NORMAL_SOURCE_RECIPES[row['recipe']] == row['sha256'] and row['argument_meanings'] == {}, 'Changed original source-check recipe')
            elif row['recipe'] == CORE_RECIPE:
                require(row['sha256'] == CORE_FILES['replay.py'] and row['argument_meanings'] ==
                        {'--lean-bin': 'LEAN_BIN_DIRECTORY', '--mathlib': 'MATHLIB_ROOT', '--out': 'OUTPUT_DIRECTORY', '--mode': 'LITERAL'}, 'Changed original core recipe')
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
        if any(row['recipe'] in T10_FINITE_RECIPES for row in drivers.values()): validate_t10_package(suite, plan)
        if any(row['recipe'] == CORE_RECIPE for row in drivers.values()): validate_core_package(suite, plan)
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
                admitted_child = output in T10_OUTPUTS.get(recipe, []) and output.removeprefix('project/') not in file_paths
                require(output not in produced and (not output.startswith('project/') or admitted_child), 'Output collision or source overwrite'); produced.add(output)
            codes = stage['expected_exit_codes']
            require(isinstance(codes, list) and codes and len(codes) == len(set(codes)) and all(type(c) is int and 0 <= c < 124 for c in codes), 'Nonsemantic/invalid expected exit code')
            for diagnostic in stage['expected_diagnostics']:
                keys(diagnostic, {'source_id', 'literal', 'sha256'})
                require(diagnostic['source_id'] in contents and isinstance(diagnostic['literal'], str) and diagnostic['literal'], 'Unowned diagnostic')
                require(diagnostic['literal'].encode() in contents[diagnostic['source_id']] and diagnostic['sha256'] == sha(diagnostic['literal'].encode()), 'Diagnostic differs from source contract')
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
    original_owned = any(row['recipe'] == CORE_RECIPE for row in plan['drivers'].values())
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
        todo := info.type.getUsedConstants.toList ++ todo
        if let some value := info.value? true then todo := value.getUsedConstants.toList ++ todo
        match info with
        | .inductInfo value => todo := value.ctors ++ todo
        | .recInfo value =>
          for rule in value.rules do todo := rule.rhs.getUsedConstants.toList ++ todo
        | _ => pure ()
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
        prerequisite_log.write_text('Exact tool, package, official import and external input prerequisites verified.\n')
        current.update(terminal='COMPLETED', exit_code=0, ended_at=utc(), log_sha256=sha(prerequisite_log.read_bytes()))
        mappings = {'project': project, 'out': output, 'build': output / 'build', 'adapter': Path(__file__).resolve()}
        main_name = 'lean' if suite['toolchain']['kind'] == 'LEAN' else 'python'
        definitions = {main_name: {'path_kind': 'EXECUTABLE'}, **{row['name']: row for row in suite['replay']['tools']}}
        mappings.update({'tool:' + name: tool_argument(definitions[name], path) for name, path in resolved.items()})
        if 'mathlib' in tools: mappings['dependency:mathlib'] = Path(tools['mathlib']).resolve()
        mappings.update({'input:' + name: Path(path) for name, path in inputs.items()})
        mappings.update({'driver:' + name: path_in(project, plan['files'][d['source_id']]['path']) for name, d in plan['drivers'].items()})
        for name, driver in plan['drivers'].items():
            if driver['recipe'] == CORE_RECIPE:
                iid = driver['external_input_id']; archive = path_in(output, 'archives/' + iid)
                inventory = extract_source_zip(inputs[iid], archive)
                require(core_source_order(archive, plan) == suite['replay']['module_order'], 'Original/declared runtime compile order differs')
                archive_hashes[iid] = inventory
                mappings['archive:' + iid] = archive; mappings['driver:' + name] = archive / 'replay.py'
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
                child_log = path_in(output, plan['core_children'][child_id]['log'] if recipe == CORE_RECIPE else 'mutation-copies/' + child_id + '/run.log')
                require(sha(child_log.read_bytes()) == observed['log_sha256'], 'Captured child log changed before observation')
                log.write_bytes(child_log.read_bytes())
                # This interval measures observation only. Actual child times are
                # retained separately and never replaced with the parent span.
                run = {'terminal': observed['terminal'], 'exit_code': observed['exit_code'], 'started_at': current['started_at'],
                       'ended_at': utc(), 'log_sha256': observed['log_sha256']}
                evidence['child_observations'].append({**observed, 'stage_id': sid, 'observed_at': run['ended_at']})
            else:
                launch = (core_tracer_argv(stage) if recipe == CORE_RECIPE else
                          t10_tracer_argv(stage) if recipe == 't10-independent-mutations-v1' else stage['argv'])
                if recipe in {CORE_RECIPE, 't10-independent-mutations-v1'}:
                    evidence['driver_invocations'].append({'parent_stage_id': sid, 'driver_sha256': driver['sha256'],
                        'source_argv': stage['argv'], 'launch_argv': launch, 'runner_sha256': evidence['runner_sha256'],
                        'trace_sha256': None, 'parent_log_sha256': sha(b''), 'child_count': 0})
                argv = [_expand(a, mappings) for a in launch]
                run = run_process(argv, path_in(project, stage['cwd'], dot=True), stage_environment(stage, plan, output, env), log, stage['timeout_seconds'])
            current.update(run); text = log.read_text(encoding='utf-8', errors='replace')
            if recipe in {CORE_RECIPE, 't10-independent-mutations-v1'} and stage['kind'] == 'DRIVER':
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
            if recipe == CORE_RECIPE and stage['kind'] == 'DRIVER':
                children, invocation, objects = core_collect_children(stage, current, text, plan, output, mappings)
                captured_children.update(children)
                require(evidence['driver_invocations'][-1] == invocation, 'Instrumented core parent trace changed during parsing')
                evidence['output_hashes'].update(objects)
            if (suite['id'] in APPROVED_DECLARED_SUITES or any(row['recipe'] in SOURCE_RECIPES for row in plan['drivers'].values())) and stage['argv'][-1].startswith('{project}/'):
                path = stage['argv'][-1][len('{project}/'):]
                if path.endswith('.lean'):
                    body = plan['contents'][plan['file_paths'][path]['source_id']].decode()
                    names = source_readback_names(body, plan['targets'].values())
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
        for iid, row in plan['inputs'].items(): require(_input_inventory(row, inputs[iid], plan) == input_hashes[iid], 'External input changed during replay')
        for iid, inventory in archive_hashes.items():
            archive = mappings['archive:' + iid]
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


def validate_receipt(receipt, suite, sources, root):
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
        keys(row, {'parent_stage_id', 'driver_sha256', 'source_argv', 'launch_argv', 'runner_sha256', 'trace_sha256', 'parent_log_sha256', 'child_count'})
        stage = plan['stages'][pid]; driver = plan['drivers'][stage['driver_id']]
        is_core = driver['recipe'] == CORE_RECIPE
        require(driver['recipe'] in {CORE_RECIPE, 't10-independent-mutations-v1'}, 'Unapproved observed original recipe')
        launch = core_tracer_argv(stage) if is_core else t10_tracer_argv(stage)
        count = 168 if is_core else 9
        require(row['driver_sha256'] == driver['sha256'] and row['source_argv'] == stage['argv'] and row['launch_argv'] == launch, 'Changed instrumented parent invocation')
        require(row['runner_sha256'] == evidence['runner_sha256'] and row['parent_log_sha256'] == stages[pid]['log_sha256'], 'Wrong parent execution/log binding')
        require(type(row['child_count']) is int and 0 <= row['child_count'] <= count, 'Invalid actual child census')
        if row['trace_sha256'] is not None:
            digest(row['trace_sha256']); require(row['trace_sha256'] not in physical_runs, 'Duplicate physical run credit'); physical_runs.add(row['trace_sha256'])
        if successful: require(row['trace_sha256'] is not None and row['child_count'] == count, 'Incomplete actual child census')
    seen = set()
    for sid, row in observed.items():
        stage = declared[sid]; pid, child = stage['argv'][1:]; driver = plan['drivers'][stage['driver_id']]
        is_core = driver['recipe'] == CORE_RECIPE
        fields = {'source_id', 'source_sha256', 'output_hashes'} if is_core else {'mutated_source_sha256', 'matched_source_literals'}
        keys(row, fields | {'stage_id', 'source_child_id', 'parent_stage_id', 'driver_sha256', 'parser_id', 'mode', 'argv_provenance',
                   'argv', 'cwd', 'started_at', 'ended_at', 'observed_at', 'physical_run_sha256', 'parent_log_sha256',
                   'terminal', 'exit_code', 'actual_outcome', 'log_sha256', 'result_record_sha256'})
        require(pid in launches and row['physical_run_sha256'] == launches[pid]['trace_sha256'] and row['parent_log_sha256'] == stages[pid]['log_sha256'], 'Observation belongs to another physical run')
        require(row['driver_sha256'] == driver['sha256'] and row['parser_id'] == driver['recipe'], 'Wrong original parser authority')
        require(row['mode'] == 'NONEXECUTING_OBSERVATION' and row['argv_provenance'] == 'CAPTURED' and row['cwd'] == '{project}', 'Derived command or duplicate execution credited as observation')
        spec = plan['core_children'][child] if is_core else None
        check_child_terminal(row, stages[pid], child, spec['argv'] if is_core else t10_child_argv(child), seen, 0 if is_core else 1)
        require(row['actual_outcome'] == ('ACCEPT' if is_core else 'REJECT') and row['terminal'] == stages[sid]['terminal'] and row['exit_code'] == stages[sid]['exit_code'] and row['log_sha256'] == stages[sid]['log_sha256'], 'Contradictory observation stage summary')
        require(isinstance(row['observed_at'], str) and row['observed_at'].endswith('Z') and
                stages[pid]['ended_at'] <= stages[sid]['started_at'] <= row['observed_at'] <= stages[sid]['ended_at'], 'Observation time is not its actual parsing interval')
        if is_core:
            require(row['source_id'] == spec['source_id'] and row['source_sha256'] == sha(plan['contents'][spec['source_id']]), 'Wrong observed source identity')
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
    if sys.argv[1:2] == ['--trace-core-runtime']:
        require(len(sys.argv) == 12, 'Malformed internal core trace invocation')
        return trace_core_runtime(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    if sys.argv[1:2] == ['--trace-t10-mutations']:
        require(len(sys.argv) == 8, 'Malformed internal trace invocation')
        return trace_t10_driver(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    for name in ('list', 'check', 'project', 'execute'): mode.add_argument('--' + name, action='store_true')
    parser.add_argument('--suite'); parser.add_argument('--out', type=Path)
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
        receipt = execute_suite(suite, sources, args.root, args.out, tools, inputs, reviews={r['id']: r for r in bundle['reviews']})
        print(json.dumps({key: receipt[key] for key in ('suite_id', 'outcome', 'proof_scope', 'exit_code')})); return receipt['exit_code']
    except (ValueError, OSError, KeyError) as error:
        print('Replay refused: ' + str(error), file=sys.stderr); return 1


if __name__ == '__main__':
    raise SystemExit(main())
