#!/usr/bin/env python3
"""Independent fresh replay of the five frozen probability-bridge modules."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'literal-shift-probability-20261011'
PRIOR = ROOT / 'literal-shift-kernel-independent-review-20261011'
LEAN = ROOT / '.toolchains/lean-4.19.0-linux/bin/lean'
MATHLIB = ROOT / '.toolchains/mathlib4-c44e0c8'
MODULES = ['LiteralShiftPersistence', 'LiteralShiftWeights', 'LiteralShiftMixture',
           'LiteralShiftDefect', 'LiteralShiftFirstBit']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    start = timestamp()
    source, build, baseline, literal, logs = [HERE / x for x in
        ('sources', 'build', 'baseline-build', 'literal-build', 'logs')]
    for path in (source, build, baseline, literal, logs):
        path.mkdir(exist_ok=True)
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    require(pins == json.loads((AUTHOR / 'SOURCE_PINS.json').read_text()), 'Author freeze differs')

    original = json.loads((AUTHOR / 'inputs/BASELINE_REBUILD.json').read_text())
    original_pins = {x['module']: x['source_sha256'] for x in original['modules']}
    prereq = json.loads((AUTHOR / 'PREREQUISITE_REBUILD.json').read_text())
    require(len(prereq['modules']) == 34, 'Final 34-module prerequisite receipt not ready')
    dependency_records = []
    for entry in prereq['modules']:
        module_path = Path(*entry['module'].split('.'))
        src = AUTHOR / 'inherited/baseline' / module_path.with_suffix('.lean')
        obj = AUTHOR / 'build' / module_path.with_suffix('.olean')
        require(entry['exit_code'] == 0, 'Prerequisite failed: ' + entry['module'])
        require(sha(src) == entry['source_sha256'] == original_pins[entry['module']],
                'Inherited baseline source mismatch: ' + entry['module'])
        require(sha(obj) == entry['object_sha256'], 'Baseline object mismatch: ' + entry['module'])
        target = baseline / module_path.with_suffix('.olean')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(obj.read_bytes())
        dependency_records.append(entry)

    prior_pins = json.loads((PRIOR / 'SOURCE_PINS.json').read_text())['modules']
    prior_replay = json.loads((PRIOR / 'REPLAY.json').read_text())
    prior_objects = {x['module']: x['object_sha256'] for x in prior_replay['new_module_replays']}
    literal_records = []
    for module, expected in prior_pins.items():
        src = AUTHOR / 'inherited/literal' / (module + '.lean')
        obj = PRIOR / 'build' / (module + '.olean')
        require(sha(src) == expected == sha(PRIOR / 'sources' / src.name),
                'Prior literal source changed: ' + module)
        require(sha(obj) == prior_objects[module], 'Prior independently checked object changed: ' + module)
        (literal / obj.name).write_bytes(obj.read_bytes())
        literal_records.append({'module': module, 'source_sha256': expected,
                                'object_sha256': prior_objects[module],
                                'origin': 'previous independent review, unchanged'})

    require(sha(AUTHOR / 'inputs/prcodec.py') ==
            'dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c',
            'Original Python source mismatch')
    package_paths = sorted(MATHLIB.glob('.lake/packages/*/.lake/build/lib/lean'))
    search_paths = [build, literal, baseline, MATHLIB / '.lake/build/lib/lean', *package_paths]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, search_paths)))
    public_names = []
    for module in MODULES:
        path = AUTHOR / (module + '.lean')
        require(sha(path) == pins[module], 'New source pin mismatch: ' + module)
        text = path.read_text()
        require(not re.search(r'\b(sorry|admit|native_decide)\b', text), 'Forbidden proof token: ' + module)
        require(not re.search(r'^\s*(axiom|constant)\s', text, re.M), 'New assumption: ' + module)
        (source / path.name).write_bytes(path.read_bytes())
        public_names += ['P02.LiteralShift.' + name for name in re.findall(
            r'(?m)^\s*(?:@\[[^\n]+\]\s*)?theorem\s+([A-Za-z0-9_]+)', text)]
    require(len(public_names) == 64, 'Exported theorem set differs from announced freeze')
    records = []

    def invoke(module, success=True):
        command = [str(LEAN), '--trust=0', '-o', str(build / (module + '.olean')), module + '.lean']
        begun = timestamp()
        result = subprocess.run(command, cwd=source, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
        (logs / (module + '.log')).write_text(result.stdout)
        record = {'module': module, 'source_sha256': sha(source / (module + '.lean')),
                  'started_utc': begun, 'finished_utc': timestamp(), 'command': command,
                  'exit_code': result.returncode, 'expected_success': success}
        if success:
            require(result.returncode == 0, 'Kernel replay failure: ' + module + '\n' + result.stdout)
            record['object_sha256'] = sha(build / (module + '.olean'))
        else:
            require(result.returncode != 0, 'False assertion unexpectedly accepted: ' + module)
            require("tactic 'decide' proved" in result.stdout and 'is false' in result.stdout,
                    'Negative failure was not the intended contradiction: ' + module + '\n' + result.stdout)
            require(not any(s in result.stdout for s in ('unknown identifier', 'failed to synthesize', 'maximum recursion')),
                    'Nonsemantic control failure: ' + module)
            record['intended_false_proposition_diagnostic'] = True
        records.append(record)
        (HERE / 'REPLAY_IN_PROGRESS.json').write_text(json.dumps(records, indent=2) + '\n')
        return result.stdout

    for module in MODULES:
        invoke(module)
    (source / 'InspectTypesAxioms.lean').write_text(
        '\n'.join('import ' + module for module in MODULES) + '\n\n' +
        '\n'.join('#check ' + name + '\n#print axioms ' + name for name in public_names) + '\n')
    axiom_text = invoke('InspectTypesAxioms')
    closures = {}
    for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", axiom_text):
        closures[name] = [x.strip() for x in values.split(',') if x.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", axiom_text):
        closures[name] = []
    require(set(closures) == set(public_names), 'Incomplete compiled theorem inspection')
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    for name, axioms in closures.items():
        require(set(axioms) <= allowed, 'Unexpected axiom closure: ' + name + ' ' + repr(axioms))

    negative_pins = {}
    for path in sorted((AUTHOR / 'negative-controls').glob('*.lean')):
        text = path.read_text()
        require(not re.search(r'\b(sorry|admit|native_decide)\b', text), 'Forbidden control token')
        (source / path.name).write_bytes(path.read_bytes())
        negative_pins[path.name] = sha(path)
        invoke(path.stem, success=False)
        require(sha(path) == negative_pins[path.name], 'Control changed during replay')
    require(len(negative_pins) == 2, 'Unexpected negative-control inventory')
    for module, expected in pins.items():
        require(sha(AUTHOR / (module + '.lean')) == expected, 'Author source changed during replay')

    result = {'status': 'PASS', 'started_utc': start, 'finished_utc': timestamp(), 'trust': 0,
              'lean_version': subprocess.check_output([str(LEAN), '--version'], text=True).strip(),
              'lean_path': list(map(str, search_paths)), 'records': records,
              'new_theorem_count': len(public_names), 'theorem_axiom_closures': closures,
              'verified_baseline_dependencies': dependency_records,
              'reused_previous_independent_literal_dependencies': literal_records,
              'negative_control_pins': negative_pins,
              'prerequisite_receipt_sha256': sha(AUTHOR / 'PREREQUISITE_REBUILD.json'),
              'source_unchanged_after_replay': True,
              'scope': 'New probability bridge only; previous seven literal modules reused without recompilation. Python-to-AST correspondence remains ordinary.'}
    (HERE / 'REPLAY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'new_modules': len(MODULES),
                      'theorem_types_and_closures': len(public_names), 'negative_controls': len(negative_pins)}, indent=2))


if __name__ == '__main__':
    main()
