#!/usr/bin/env python3
"""Replay frozen reviewed modules into reviewer-owned objects, then inspect axioms."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'literal-shift-kernel-refinement-20261011'
LEAN = ROOT / '.toolchains/lean-4.19.0-linux/bin/lean'
MATHLIB = ROOT / '.toolchains/mathlib4-c44e0c8'
MODULES = [
    'LiteralShiftSyntax', 'LiteralShiftScan', 'LiteralShiftReplay',
    'LiteralShiftCorrect', 'LiteralShiftEndpoints',
    'LiteralShiftWord', 'LiteralShiftPrefix',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    source = HERE / 'sources'
    build = HERE / 'build'
    baseline_build = HERE / 'baseline-build'
    logs = HERE / 'logs'
    for directory in (source, build, baseline_build, logs):
        directory.mkdir(exist_ok=True)

    prerequisite = json.loads((AUTHOR / 'PREREQUISITE_REBUILD.json').read_text())
    original = json.loads((AUTHOR / 'inputs/BASELINE_REBUILD.json').read_text())
    original_sources = {entry['module']: entry['source_sha256'] for entry in original['modules']}
    dependency_checks = []
    for entry in prerequisite['modules']:
        module_path = Path(*entry['module'].split('.'))
        src = AUTHOR / 'baseline' / module_path.with_suffix('.lean')
        obj = AUTHOR / 'build' / module_path.with_suffix('.olean')
        require(entry['exit_code'] == 0, 'Prerequisite did not compile: ' + entry['module'])
        require(sha(src) == entry['source_sha256'] == original_sources[entry['module']],
                'Prerequisite source mismatch: ' + entry['module'])
        require(sha(obj) == entry['object_sha256'], 'Prerequisite object mismatch: ' + entry['module'])
        copied_object = baseline_build / module_path.with_suffix('.olean')
        copied_object.parent.mkdir(parents=True, exist_ok=True)
        copied_object.write_bytes(obj.read_bytes())
        dependency_checks.append(dict(entry))

    require(sha(AUTHOR / 'inputs/prcodec.py') == pins['python_source_sha256'], 'Python source mismatch')
    package_paths = sorted(MATHLIB.glob('.lake/packages/*/.lake/build/lib/lean'))
    search_paths = [build, baseline_build, MATHLIB / '.lake/build/lib/lean', *package_paths]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, search_paths)))
    records = []
    theorem_names = []
    for module in MODULES:
        original_path = AUTHOR / (module + '.lean')
        require(sha(original_path) == pins['modules'][module], 'Reviewed source changed: ' + module)
        content = original_path.read_text()
        require(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', content),
                'Disallowed proof-source token: ' + module)
        (source / original_path.name).write_bytes(original_path.read_bytes())
        theorem_names += ['P02.LiteralShift.' + name for name in re.findall(
            r'(?m)^(?:@\[[^\n]+\]\s+)?theorem\s+([A-Za-z0-9_]+)', content)]

    def invoke(module):
        command = [str(LEAN), '--trust=0', '-o', str(build / (module + '.olean')), module + '.lean']
        start = now()
        result = subprocess.run(command, cwd=source, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        (logs / (module + '.log')).write_text(result.stdout)
        record = {'module': module, 'command': command, 'started_utc': start,
                  'finished_utc': now(), 'exit_code': result.returncode,
                  'source_sha256': sha(source / (module + '.lean'))}
        if result.returncode == 0:
            record['object_sha256'] = sha(build / (module + '.olean'))
        records.append(record)
        (HERE / 'REPLAY_IN_PROGRESS.json').write_text(json.dumps(records, indent=2) + '\n')
        require(result.returncode == 0, 'Kernel replay failed: ' + module + '\n' + result.stdout)
        return result.stdout

    for module in MODULES:
        invoke(module)

    (source / 'InspectTypes.lean').write_text(
        '\n'.join('import ' + module for module in MODULES) + '\n\n' +
        '\n'.join('#check ' + name for name in theorem_names) + '\n')
    invoke('InspectTypes')
    (source / 'InspectAxioms.lean').write_text(
        '\n'.join('import ' + module for module in MODULES) + '\n\n' +
        '\n'.join('#print axioms ' + name for name in theorem_names) + '\n')
    axiom_text = invoke('InspectAxioms')
    require('sorryAx' not in axiom_text, 'sorryAx in theorem closure')
    require('Lean.ofReduceBool' not in axiom_text, 'Native reduction axiom in theorem closure')
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    axiom_lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', axiom_text)
    no_axiom = re.findall(r'does not depend on any axioms', axiom_text)
    require(len(axiom_lists) + len(no_axiom) == len(theorem_names), 'Incomplete axiom output')
    for group in axiom_lists:
        actual = {name.strip() for name in group.split(',') if name.strip()}
        require(actual <= allowed, 'Unexpected theorem axioms: ' + repr(actual - allowed))
    for module in MODULES:
        require(sha(AUTHOR / (module + '.lean')) == pins['modules'][module],
                'Author source changed during replay: ' + module)
    report = {
        'finished_utc': now(), 'status': 'PASS', 'trust': 0,
        'lean_version': subprocess.check_output([str(LEAN), '--version'], text=True).strip(),
        'lean_path': list(map(str, search_paths)), 'new_module_replays': records,
        'reused_verified_prerequisites': dependency_checks,
        'theorems_inspected': theorem_names,
        'allowed_axioms': sorted(allowed),
        'source_unchanged_after_replay': True,
        'scope': 'Kernel replay and axiom checks; Python transcription reviewed separately.',
    }
    (HERE / 'REPLAY.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'modules': len(MODULES),
                      'theorem_closures': len(theorem_names)}, indent=2))


if __name__ == '__main__':
    main()
