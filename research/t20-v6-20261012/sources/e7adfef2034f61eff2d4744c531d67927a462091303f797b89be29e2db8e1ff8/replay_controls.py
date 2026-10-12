#!/usr/bin/env python3
"""Replay the author's frozen semantic controls against reviewer-owned objects."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import datetime

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'literal-shift-kernel-refinement-20261011'
SOURCE = HERE / 'sources'
LEAN = HERE.parent / '.toolchains/lean-4.19.0-linux/bin/lean'
CONTROL_SHA = '95b4fd5cabd7ae348c5d4da73483329df11b0d9f14008e58007000b51c9f4976'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(condition, text):
    if not condition:
        raise RuntimeError(text)


def main():
    replay = json.loads((HERE / 'REPLAY.json').read_text())
    require(replay['status'] == 'PASS', 'Core independent replay not passed')
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(replay['lean_path']))
    src = AUTHOR / 'LiteralShiftControls.lean'
    require(sha(src) == CONTROL_SHA, 'Frozen positive controls changed')
    content = src.read_text()
    require(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', content), 'Disallowed control source token')
    (SOURCE / src.name).write_bytes(src.read_bytes())
    records = []

    def run(module, expected_success):
        cmd = [str(LEAN), '--trust=0', '-o', str(HERE / 'build' / (module + '.olean')), module + '.lean']
        result = subprocess.run(cmd, cwd=SOURCE, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        (HERE / 'logs' / (module + '.log')).write_text(result.stdout)
        record = {'module': module, 'source_sha256': sha(SOURCE / (module + '.lean')),
                  'exit_code': result.returncode, 'expected_success': expected_success,
                  'command': cmd}
        if expected_success:
            require(result.returncode == 0, 'Positive control failed: ' + module + '\n' + result.stdout)
        else:
            require(result.returncode != 0, 'False proposition unexpectedly accepted: ' + module)
            require("tactic 'decide' proved" in result.stdout and 'is false' in result.stdout,
                    'Rejection did not establish intended false proposition: ' + module + '\n' + result.stdout)
            require(not any(s in result.stdout for s in ('unknown identifier', 'failed to synthesize', 'maximum recursion')),
                    'Nonsemantic control failure: ' + module)
            record['intended_false_proposition_diagnostic'] = True
        records.append(record)
        return result.stdout

    run('LiteralShiftControls', True)
    names = re.findall(r'(?m)^theorem\s+([A-Za-z0-9_]+)', content)
    (SOURCE / 'InspectControlAxioms.lean').write_text('import LiteralShiftControls\n' +
        '\n'.join('#print axioms P02.LiteralShift.Controls.' + name for name in names) + '\n')
    output = run('InspectControlAxioms', True)
    groups = re.findall(r'depends on axioms:\s*\[([^\]]*)\]', output)
    absent = re.findall(r'does not depend on any axioms', output)
    require(len(groups) + len(absent) == len(names), 'Incomplete control axiom output')
    for group in groups:
        actual = {x.strip() for x in group.split(',') if x.strip()}
        require(actual <= {'propext', 'Classical.choice', 'Quot.sound'}, 'Unexpected control axioms')
    for path in sorted((AUTHOR / 'negative-controls').glob('*.lean')):
        require(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', path.read_text()),
                'Disallowed negative control token')
        (SOURCE / path.name).write_bytes(path.read_bytes())
        run(path.stem, False)
        require(sha(path) == sha(SOURCE / path.name), 'Negative control changed during replay')
    require(sha(src) == CONTROL_SHA, 'Positive controls changed during replay')
    result = {'status': 'PASS', 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'positive_theorems': names, 'negative_count': sum(not r['expected_success'] for r in records),
              'records': records, 'native_reduction_axiom_present': False,
              'scope': 'Frozen author controls replayed independently; false assertions, not new source mutations.'}
    (HERE / 'CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'positive_theorems': len(names), 'negative_files': result['negative_count']}))


if __name__ == '__main__':
    main()
