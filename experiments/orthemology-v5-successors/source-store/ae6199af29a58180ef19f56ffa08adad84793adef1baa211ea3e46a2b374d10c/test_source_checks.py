#!/usr/bin/env python3
"""Mutation tests for source validation, on temporary source-only copies."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def run_mutation(label, mutate, expected):
    with tempfile.TemporaryDirectory(prefix='semantic-source-control-') as td:
        d=Path(td)/'package'
        shutil.copytree(ROOT,d,ignore=shutil.ignore_patterns('*.olean','*.ilean','.lake'))
        mutate(d)
        r=subprocess.run(['python3','verification/verify_sources.py'],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        assert r.returncode!=0 and expected in r.stdout,(label,r.returncode,r.stdout)
        print(f'EXPECTED_SOURCE_REJECTION: {label}')

def edit(d,name,replace,update=False):
    p=d/name;p.write_text(replace(p.read_text()))
    if update:
        lock=d/'verification/source-lock.json';data=json.loads(lock.read_text())
        for item in data['files']:
            if item['path']==name:item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        lock.write_text(json.dumps(data,indent=2)+'\n')

run_mutation('changed inherited source',lambda d:edit(d,'AllPredicates.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('changed new source',lambda d:edit(d,'EffectivePrimitiveRecursion.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('proof hole despite refreshed local source hash',lambda d:edit(d,'EffectivePrimitiveRecursion.lean',lambda s:s+'\nexample : True := by sorry\n',True),'Forbidden new-source token')
run_mutation('new axiom despite refreshed local source hash',lambda d:edit(d,'EffectivePrimitiveRecursion.lean',lambda s:s+'\naxiom forbidden : True\n',True),'Forbidden new-source token')
run_mutation('omitted default root',lambda d:edit(d,'lakefile.lean',lambda s:s.replace(', `EffectiveBooleanControls',''),True),'Lake default-root coverage changed')
run_mutation('changed dependency revision',lambda d:edit(d,'lake-manifest.json',lambda s:s.replace('c44e0c8ee63ca166450922a373c7409c5d26b00b','0000000000000000000000000000000000000000'),True),'AssertionError')
run_mutation('changed gate source',lambda d:edit(d,'BareBooleanGatePositive.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('changed restricted compiler',lambda d:edit(d,'RestrictedCompiler.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('changed restricted checker',lambda d:edit(d,'IdentityChecker.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('changed polynomial bridge',lambda d:edit(d,'PolynomialTestBoundary.lean',lambda s:s+'\n-- mutation\n'),'Source digest mismatch')
run_mutation('polynomial proof hole despite refreshed local source hash',lambda d:edit(d,'PolynomialTestBoundary.lean',lambda s:s+'\nexample : True := by sorry\n',True),'Forbidden new-source token')
run_mutation('polynomial axiom despite refreshed local source hash',lambda d:edit(d,'PolynomialTestBoundary.lean',lambda s:s+'\naxiom forbidden : True\n',True),'Forbidden new-source token')
run_mutation('omitted polynomial audit root',lambda d:edit(d,'verification/AllProjectProofAudit.lean',lambda s:s.replace(', `PolynomialTestBoundary',''),True),'Complete module audit coverage changed')
run_mutation('omitted polynomial inventory root',lambda d:edit(d,'verification/ExportDeclarationInventory.lean',lambda s:s.replace(', `PolynomialTestBoundary',''),True),'Complete module audit coverage changed')
run_mutation('changed v4 historical receipt',lambda d:edit(d,'verification/historical/unified-v4-receipt.json',lambda s:s+'\n',True),'Historical receipt changed')
print('SOURCE_CONTROL_MUTATIONS_PASS: fifteen deliberate invalid successors rejected')
