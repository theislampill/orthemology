#!/usr/bin/env python3
"""Recheck frozen fixtures; missing infrastructure never counts as rejection."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.verification-results/restricted';OUT.mkdir(parents=True,exist_ok=True)
cases={
 'restricted-v1-controls':{
 'PositiveInterface':None,'WrongZeroBranch':'type mismatch','WrongProjectionBound':'decide',
 'MissingEndpointMembership':'type mismatch','SemanticValidityIsNotHas':'type mismatch',
 'ArityZeroIsNotOneArrow':'type mismatch','RejectCustomAxiom':'UNAPPROVED_KERNEL_AXIOM','RejectAdmittedProof':'UNAPPROVED_KERNEL_AXIOM'},
 'restricted-v2-controls':{
 'PositiveExactInterface':None,'PositiveOrthantRequired':'decide','ZeroAtZeroIsNotZeroMap':'decide',
 'EmptyZeroArityCertificate':'decide','ForgedCoefficient':'decide','WrongZeroConditional':'decide',
 'NoSyntacticIdentityCompleteness':'type mismatch','InvalidVariableIndex':'decide',
 'RejectCustomAxiom':'UNAPPROVED_KERNEL_AXIOM','RejectAdmittedProof':'UNAPPROVED_KERNEL_AXIOM'},
 'restricted-independent-controls':{
 'INDEPENDENT_MissingPositivity':'invalid field notation',
 'INDEPENDENT_DuplicateRowsCannotCoverMasks':'decide',
 'INDEPENDENT_ExternalPairMismatch':'decide',
 'INDEPENDENT_DeadExponentForgery':'decide',
 'INDEPENDENT_Admission':'UNAPPROVED_KERNEL_AXIOM',
 'INDEPENDENT_CustomAxiom':'UNAPPROVED_KERNEL_AXIOM',
 'INDEPENDENT_SinglePositivePoint':'type mismatch'} }
rows=[]
for group,cs in cases.items():
    assert {p.stem for p in (ROOT/'verification'/group).glob('*.lean')}==set(cs),'Unexpected fixture inventory'
    for name,token in sorted(cs.items(),key=lambda x:x[1] is not None):
        source=Path('verification')/group/(name+'.lean')
        p=subprocess.run(['lake','env','lean',str(source)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (OUT/(group+'-'+name+'.log')).write_text(p.stdout)
        infrastructure=any(s in p.stdout.lower() for s in ['unknown module prefix','unknown identifier','object file','no such file','failed to read file'])
        good=p.returncode==0 if token is None else p.returncode!=0 and token in p.stdout and not infrastructure
        row={'group':group,'name':name,'expected_success':token is None,'exit':p.returncode,'pass':good}; rows.append(row)
        if not good:print(p.stdout);raise SystemExit(str(row))
        print('POSITIVE_CONTROL_PASS' if token is None else 'EXPECTED_REJECTION',group,name)
(OUT/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print('RESTRICTED_CONTROLS_PASS',len(rows),'cases')
