#!/usr/bin/env python3
"""Replay exact accepted polynomial-test fixtures; require intended diagnostics."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.verification-results/polynomial-test';OUT.mkdir(parents=True,exist_ok=True)
CASES={
 'PositiveInterfaces':None,
 'WrongEqualityPolarity':'rfl',
 'WrongSubtractionOrder':'rfl',
 'EmptyArityIsNotVacuous':'unsolved goals',
 'NoPureZeroTests':'invalid dotted identifier notation, unknown identifier `P01AC.PolynomialTestBoundary.Arithmetic.ifZero`',
 'NoNestedRootTests':'invalid dotted identifier notation, unknown identifier `P01AC.PolynomialTestBoundary.Arithmetic.equal`',
 'NoSyntacticIdentityCast':'type mismatch',
 'RejectCustomAxiom':'UNAPPROVED_KERNEL_AXIOM',
 'RejectAdmittedProof':'UNAPPROVED_KERNEL_AXIOM',
}
assert {p.stem for p in (ROOT/'verification/polynomial-test-controls').glob('*.lean')}==set(CASES),'Unexpected polynomial fixture inventory'
rows=[]
for name,token in CASES.items():
    source=Path('verification/polynomial-test-controls')/(name+'.lean')
    run=subprocess.run(['lake','env','lean',str(source)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/(name+'.log')).write_text(run.stdout)
    # Exact forbidden-constructor diagnostics are intentional, not missing imports.
    infrastructure_output=run.stdout.replace(token,'') if token is not None else run.stdout
    infrastructure=any(s in infrastructure_output.lower() for s in ['unknown module prefix','unknown identifier','object file','no such file','failed to read file'])
    good=run.returncode==0 if token is None else run.returncode!=0 and token in run.stdout and not infrastructure
    rows.append({'name':name,'expected_success':token is None,'exit':run.returncode,'passed':good})
    if not good:print(run.stdout);raise SystemExit(str(rows[-1]))
    print('POSITIVE_CONTROL_PASS' if token is None else 'EXPECTED_REJECTION','polynomial-test',name)
(OUT/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print('POLYNOMIAL_TEST_CONTROLS_PASS',len(rows),'cases')
