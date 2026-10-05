#!/usr/bin/env python3
"""Offline, source-bound successor replay with fresh isolated custom outputs.

Exit 0 means success at the reported scope; 1 means failure or an explicitly
resource-inconclusive run; 2 means a missing prerequisite. No network or shell.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys


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
# Full-suite promotion requires review of its complete original stage contract.
# Generic serial compilation is supported at COMPONENTS scope. Values here are
# code-reviewed canonical replay descriptor digests, never producer approvals.
APPROVED_DECLARED_SUITES = {}
EMPIRICAL_RECIPES = {
    't15-empirical-integrity-v1': '9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e',
    't15-empirical-tests-v1': 'afb1ba14ecbbf193f07ac81f985be30535abf9771387813e9dbd0bbbfc72fb50',
    't15-empirical-reanalyse-v1': '20110e73fd822e21651064578946cdf910edc493c973953b2c7d1bb74481dd94',
    't15-empirical-validate-v1': '7d9a4c8d071e2591c8d4568c88c277ab61834e52df21500a1367efb2ac7e060a',
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
        if recipe in LANGUAGE_RECIPES:
            require(argv[:4] == ['{tool:python}', '-I', '-B', '{driver:' + driver['id'] + '}'] and len(argv) == 5, 'Wrong reviewed Python recipe')
            match = re.fullmatch(r'\{(input|fixture):([^{}]+)\}', argv[4])
            require(match and match.group(2) in plan[match.group(1) + 's'], 'Undeclared driver input')
            require(stage['kind'] in {'REFERENCE_TESTS', 'NEGATIVE_CONTROL', 'DRIVER'}, 'Wrong language stage kind')
            return
        if recipe in SOURCE_RECIPES:
            require(stage['kind'] == 'SOURCE_CHECK' and argv == ['{builtin:source-check}'], 'Wrong source-check translation')
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
    else:
        require(stage['output_paths'] == [], 'Interpretation stage has undeclared outputs')
    require((row['role'] == 'NEGATIVE') == (stage['kind'] == 'NEGATIVE_CONTROL'), 'Negative source/stage role mismatch')


def validate_suite(suite, sources, root):
    """Offline checks only. Neither a descriptor nor a review Boolean authorises code."""
    try:
        replay = suite['replay']; keys(replay, REPLAY_KEYS)
        require(replay['schema'] == 'orthemology-v5-replay-v1', 'Unknown replay schema')
        require(replay['scope'] in {'COMPONENTS', 'DECLARED_SUITE', 'FINITE'}, 'Unknown replay scope')
        if replay['scope'] == 'DECLARED_SUITE':
            require(APPROVED_DECLARED_SUITES.get(suite['id']) == canonical(replay), 'Complete original suite recipe has not been approved')
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
            require(Path(name).suffix.lower() not in {'.olean', '.ilean', '.o', '.so', '.dll', '.exe', '.a', '.zip', '.gz'}, 'Precompiled/archive payload is not a public source projection')
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
            if files[sid]['role'] != 'NEGATIVE': lean_name(name)
            require(files[sid]['path'].endswith(name.replace('.', '/') + '.lean'), 'Module/project path mismatch')
            require(files[sid]['role'] in {'PROOF', 'AUDIT', 'NEGATIVE', 'RUNTIME'}, 'Nonmodule source role')
            require(string_list(row['imports']) == imports(contents[sid].decode('utf-8')), 'Declared imports differ from source')
            require(set(row['imports']) <= set(modules) | set(official), 'Missing import dependency')
        order = string_list(replay['module_order']); require(set(order) <= set(modules), 'Unknown ordered module')
        for index, name in enumerate(order):
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
            require(row['external_input_id'] is None, 'Archive recipe is not approved by this adapter version')
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
            else:
                require(SOURCE_RECIPES.get(row['recipe']) == row['sha256'], 'Unknown/unreviewed driver recipe')
        stages = indexed(replay['stages']); require(stages and not (set(stages) & RESERVED), 'Missing stages or reserved stage ID')
        controls = indexed(suite['controls']); covered = []; produced = set(); prior = []
        plan = {'files': files, 'file_paths': file_paths, 'contents': contents, 'modules': modules, 'official': official,
                'drivers': drivers, 'inputs': inputs, 'input_manifests': input_manifests, 'fixtures': fixtures,
                'stages': stages, 'targets': names, 'packages': packages, 'build_roots': string_list(replay['build_roots'])}
        for name in plan['build_roots']:
            relative(name); require(name != 'project' and not name.startswith('project/'), 'Build root overlaps projected sources')
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
                relative(output); require(output not in produced and not output.startswith('project/'), 'Output collision or source overwrite'); produced.add(output)
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
        require(text.count(start + '\n') == 1 and text.count(end) == 1, 'Missing/duplicate target readback')
        block = text.split(start + '\n', 1)[1].split(end, 1)[0]
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
    for path in build_roots: path.mkdir(parents=True, exist_ok=True)
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
    results = {r['id']: r for r in evidence['stage_results']}; completed = {}; controls = {r['id']: r for r in suite['controls']}
    current = results['_prerequisites']; current['started_at'] = utc(); prerequisite_log = logs / 'prerequisites.log'
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
        mappings = {'project': project, 'out': output, 'build': output / 'build'}
        mappings.update({'tool:' + name: path for name, path in resolved.items()})
        mappings.update({'input:' + name: Path(path) for name, path in inputs.items()})
        mappings.update({'driver:' + name: path_in(project, plan['files'][d['source_id']]['path']) for name, d in plan['drivers'].items()})
        for sid, stage in plan['stages'].items():
            current = results[sid]; current['started_at'] = utc(); log = logs / (sid + '.log')
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
            else:
                argv = [_expand(a, mappings) for a in stage['argv']]
                run = run_process(argv, path_in(project, stage['cwd'], dot=True), env, log, stage['timeout_seconds'])
            current.update(run); text = log.read_text(encoding='utf-8', errors='replace')
            if run['terminal'] != 'COMPLETED':
                receipt.update(outcome='RESOURCE_INCONCLUSIVE', exit_code=1)
                raise ValueError('Resource-inconclusive stage')
            assess_stage(stage, run, text, completed)
            if stage['driver_id'] in plan['drivers'] and plan['drivers'][stage['driver_id']]['recipe'] in LANGUAGE_RECIPES:
                _language_result(plan['drivers'][stage['driver_id']], stage, text, plan)
            if stage['driver_id'] in plan['drivers'] and plan['drivers'][stage['driver_id']]['recipe'] in EMPIRICAL_RECIPES:
                _empirical_result(plan['drivers'][stage['driver_id']], stage, text, plan, output)
            if any(row['recipe'] in SOURCE_RECIPES for row in plan['drivers'].values()) and stage['argv'][-1].startswith('{project}/'):
                path = stage['argv'][-1][len('{project}/'):]
                if path.endswith('.lean'):
                    body = plan['contents'][plan['file_paths'][path]['source_id']].decode()
                    names = re.findall(r'^#print axioms\s+(\S+)\s*$', body, re.M)
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
        for sid, row in plan['files'].items(): require(path_in(project, row['path']).read_bytes() == plan['contents'][sid], 'Projected source changed during replay')
        evidence['source_hashes_after'] = {sid: sha(public_bytes(root, sources[sid])) for sid in suite['source_ids']}
        receipt['target_readbacks'] = [{key: target[key] for key in ('source_id', 'target_sha256')} | {'target_id': target['id'], 'outcome': 'CHECKED'} for target in suite['targets']]
        selected = suite['replay']['scope']
        outcome = {'FINITE': 'FINITE_ONLY', 'COMPONENTS': 'FRESH_KERNEL_COMPONENTS', 'DECLARED_SUITE': 'QUALIFIED_DECLARED_SUITE'}[selected]
        receipt.update(outcome=outcome, exit_code=0, proof_scope=selected)
    except (FileNotFoundError, ValueError, OSError, subprocess.SubprocessError) as error:
        if isinstance(error, MissingInput): receipt.update(outcome='BLOCKED_EXTERNAL_INPUT', exit_code=2)
        elif isinstance(error, MissingTool): receipt.update(outcome='BLOCKED_TOOLCHAIN', exit_code=2)
        elif receipt['outcome'] != 'RESOURCE_INCONCLUSIVE': receipt.update(outcome='FAILED', exit_code=1)
        receipt['proof_scope'] = 'NONE'
        if current['terminal'] == 'SKIPPED':
            private_log = logs / (current['id'] + '-failure.log'); private_log.write_text(type(error).__name__ + ': ' + str(error) + '\n')
            current.update(terminal='MISSING' if isinstance(error, FileNotFoundError) else 'COMPLETED',
                           exit_code=None if isinstance(error, FileNotFoundError) else 1, ended_at=utc(), log_sha256=sha(private_log.read_bytes()))
    receipt['ended_at'] = utc(); save()
    validate_receipt(receipt, suite, sources, root)
    return receipt


def validate_receipt(receipt, suite, sources, root):
    plan = validate_suite(suite, sources, root); evidence = receipt['replay_evidence']; keys(evidence, EVIDENCE_KEYS)
    require(evidence['schema'] == 'orthemology-v5-replay-evidence-v1' and evidence['cache_policy'] == CACHE_POLICY, 'Unknown replay evidence/cache policy')
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


def main():
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
