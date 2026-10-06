#!/usr/bin/env python3
"""Six interface rejections plus four compiled auditor poison tests.

These controls show that the stated *uses* and checker reject the altered inputs.
They are not proofs of logical independence or impossibility of other derivations.
Default: run from any directory in a fully built Lake package. Alternatively pass
--lean /absolute/path/to/lean with a complete existing LEAN_PATH for reused builds.
The audit module is freshly compiled in an isolated directory, never source-grepped.
"""
from pathlib import Path
import argparse
import json
import os
import re
import subprocess
import tempfile

PACKAGE = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', help='Lean executable; requires the caller\'s LEAN_PATH')
parser.add_argument('--logs', type=Path, default=PACKAGE / 'verification' / 'new-negative-control-logs')
args = parser.parse_args()
args.logs.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
if args.lean:
    lean = args.lean
else:
    def lake_env(*command):
        p = subprocess.run(['lake', 'env', *command], cwd=PACKAGE, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return p.stdout.strip()
    lean = lake_env('which', 'lean')
    env['LEAN_PATH'] = lake_env('printenv', 'LEAN_PATH')
# Lake may emit relative entries; resolve them before using the isolated cwd.
env['LEAN_PATH'] = ':'.join(str((PACKAGE / v).resolve()) if not Path(v).is_absolute() else v
                            for v in env.get('LEAN_PATH', '').split(':') if v)
controls = {
    'MissingStepRepresentation': ('application type mismatch', 'Represents g G'),
    'MissingObserverRepresentation': ('application type mismatch', 'Represents o O'),
    'MissingSemanticInput': ('type mismatch', 'F N'),
    'WrongRawEndpointRelation': ('type mismatch', 'Conv'),
    'WrongIdentityCarrier': ('type mismatch', 'raw.identity'),
    'SemanticExistenceIsNotCurrentTyping': ('type mismatch', 'Has'),
    'AuditorRejectsCustomAxiom': ('UNAPPROVED_KERNEL_AXIOM AuditPoison.custom',),
    'AuditorRejectsSorry': ('UNAPPROVED_KERNEL_AXIOM sorryAx',),
    'AuditorRejectsUnsafe': ('UNSAFE_KERNEL_DEPENDENCY AuditPoison.root',),
    'AuditorRejectsPartial': ('PARTIAL_KERNEL_DEPENDENCY AuditPoison.root._unsafe_rec',),
}
results = []
with tempfile.TemporaryDirectory(prefix='effective-negative-controls-') as temp:
    temp = Path(temp)
    (temp / 'verification').mkdir()
    env['LEAN_PATH'] = str(temp) + ':' + env['LEAN_PATH']
    audit_command = [lean, '-o', str(temp / 'verification' / 'KernelAudit.olean'),
                     str(PACKAGE / 'verification' / 'KernelAudit.lean')]
    audit = subprocess.run(audit_command, cwd=PACKAGE, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (args.logs / 'auditor-positive.log').write_text(audit.stdout)
    if audit.returncode or 'EFFECTIVE_KERNEL_AUDIT_PASS' not in audit.stdout:
        raise SystemExit('Auditor positive prerequisite failed; see auditor-positive.log')
    for name, markers in controls.items():
        command = [lean, str(PACKAGE / 'verification' / 'negative-controls' / (name + '.lean'))]
        p = subprocess.run(command, cwd=PACKAGE, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (args.logs / (name + '.log')).write_text(p.stdout)
        infrastructural = re.search(r'unknown module|unknown constant|unknown identifier|file not found', p.stdout)
        ok = p.returncode != 0 and not infrastructural and all(x in p.stdout for x in markers)
        result = dict(name=name, command=command, exit_code=p.returncode,
                      expected_diagnostic_fragments=markers, passed=bool(ok))
        results.append(result)
        print(('PASS ' if ok else 'FAIL ') + name)
        if not ok:
            print(p.stdout)
    summary = dict(schema=1, interface_controls=6, auditor_controls=4,
                   passed=sum(r['passed'] for r in results), controls=results,
                   boundary='Expected interface rejection is not an independence proof.')
    (args.logs / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    if not all(r['passed'] for r in results):
        raise SystemExit(1)
print('NEW_NEGATIVE_CONTROLS_PASS: 6 interface controls; 4 auditor poison controls')
