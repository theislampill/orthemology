#!/usr/bin/env python3
"""Twelve Boolean interface rejections and four compiled-auditor poison tests.

These are rejection tests of the displayed uses, not independence proofs.
The five Boolean modules and both audit modules are freshly compiled into an
isolated directory, before checking the failure fixtures. Imported predecessor
objects and dependencies come from the caller's existing build. Run inside a
built Lake package, or supply --lean with a complete LEAN_PATH.
"""
from pathlib import Path
import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile

PACKAGE = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--lean', help='Lean executable; requires an existing LEAN_PATH')
parser.add_argument('--logs', type=Path,
                    default=PACKAGE / 'verification' / 'boolean-negative-control-logs')
args = parser.parse_args()
args.logs.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
if args.lean:
    lean = str(Path(args.lean).resolve()) if '/' in args.lean else args.lean
else:
    def lake_env(*command):
        p = subprocess.run(['lake', 'env', *command], cwd=PACKAGE, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return p.stdout.strip()
    lean = lake_env('which', 'lean')
    env['LEAN_PATH'] = lake_env('printenv', 'LEAN_PATH')
env['LEAN_PATH'] = ':'.join(str((PACKAGE / v).resolve()) if not Path(v).is_absolute() else v
                            for v in env.get('LEAN_PATH', '').split(':') if v)

controls = {'MissingLeftTyping': ('type mismatch',), 'MissingRightTyping': ('type mismatch',), 'MissingLeftMembership': ('type mismatch',), 'MissingRightMembership': ('type mismatch',), 'MissingArgumentObservation': ('type mismatch',), 'WrongRecursionArity': ('type mismatch',), 'WrongDiscriminatorOrientation': ('type mismatch',), 'WrongParameterOrder': ('type mismatch',), 'RawToBoolCast': ('type mismatch',), 'SemanticValidityIsNotCurrentHas': ('type mismatch',), 'WrongIdentityCarrier': ('type mismatch',), 'FiniteBudgetIsNotAllTests': ('type mismatch',), 'AuditorRejectsCustomAxiom': ('UNAPPROVED_KERNEL_AXIOM BooleanAuditPoison.custom',), 'AuditorRejectsSorry': ('UNAPPROVED_KERNEL_AXIOM sorryAx',), 'AuditorRejectsUnsafe': ('UNSAFE_KERNEL_DEPENDENCY BooleanAuditPoison.root',), 'AuditorRejectsPartial': ('PARTIAL_KERNEL_DEPENDENCY BooleanAuditPoison.root._unsafe_rec',)}
fixtures = PACKAGE / 'verification' / 'boolean-negative-controls'
actual = {p.stem for p in fixtures.glob('*.lean')}
if actual != set(controls):
    raise SystemExit(f'Unexpected fixture inventory: missing={set(controls)-actual}; extra={actual-set(controls)}')
results = []
prerequisites = []
with tempfile.TemporaryDirectory(prefix='boolean-negative-controls-') as temp:
    temp = Path(temp)
    (temp / 'verification').mkdir()
    env['LEAN_PATH'] = str(temp) + ':' + env['LEAN_PATH']
    for module in ('EffectiveBooleanStandardness', 'EffectiveBooleanCertificates', 'EffectivePrimitiveRecursion', 'EffectiveBooleanInterfaces', 'EffectiveBooleanControls',
                   'verification/KernelAudit', 'verification/BooleanKernelAudit'):
        source = Path(module + '.lean')
        shutil.copy2(PACKAGE / source, temp / source)
        command = [lean, '-o', str(temp / (module + '.olean')), str(temp / source)]
        p = subprocess.run(command, cwd=temp, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = module.replace('/', '-') + '-positive.log'
        (args.logs / log).write_text(p.stdout)
        required_marker = ('BOOLEAN_KERNEL_AUDIT_PASS' if module.endswith('BooleanKernelAudit')
                           else 'EFFECTIVE_KERNEL_AUDIT_PASS' if module.endswith('KernelAudit')
                           else None)
        ok = (p.returncode == 0 and not re.search(r'warning:|error:', p.stdout)
              and (required_marker is None or required_marker in p.stdout))
        prerequisites.append(dict(module=module, exit_code=p.returncode, passed=bool(ok), log=log))
        if not ok:
            raise SystemExit(f'Fresh positive prerequisite failed: {module}; see {log}')
    for name, markers in controls.items():
        command = [lean, str(fixtures / (name + '.lean'))]
        p = subprocess.run(command, cwd=temp, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (args.logs / (name + '.log')).write_text(p.stdout)
        infrastructural = re.search(r'unknown module|unknown constant|unknown identifier|file not found', p.stdout)
        ok = p.returncode != 0 and not infrastructural and all(x in p.stdout for x in markers)
        results.append(dict(name=name, command=command, exit_code=p.returncode,
                            expected_diagnostic_fragments=markers, passed=bool(ok)))
        print(('PASS ' if ok else 'FAIL ') + name)
        if not ok:
            print(p.stdout)
    summary = dict(schema=1, fresh_positive_prerequisites=prerequisites,
                   interface_controls=12, auditor_controls=4,
                   passed=sum(r['passed'] for r in results), controls=results,
                   boundary='Expected interface rejection is not an independence proof.')
    (args.logs / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    if not all(r['passed'] for r in results):
        raise SystemExit(1)
print('BOOLEAN_NEGATIVE_CONTROLS_PASS: 12 interface controls; 4 auditor poison controls')
