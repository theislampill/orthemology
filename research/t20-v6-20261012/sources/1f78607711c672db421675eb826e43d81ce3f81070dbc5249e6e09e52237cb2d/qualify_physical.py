#!/usr/bin/env python3
"""Fresh first-party Lean source rebuild and theorem/axiom readback.

Requires explicit official Lean and pinned Mathlib paths. Reuses only the
external package cache; rebuilds every local module into a NEW output directory.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from datetime import datetime,timezone

BASE_MODULES=['SelfVerifyingSupport', 'SupportStageCertificate', 'SupportFixtures', 'FiniteLikelihood', 'AdaptiveLikelihood', 'LikelihoodProducts', 'BlockController', 'CanonicalBlockPolicy']
QUANT_MODULES=['HellingerTree', 'BlockKernel', 'HellingerPolicy', 'SubprobHellinger', 'StoppedBlock', 'ResidualDeficit', 'DependentHellinger', 'StoppedPhasePolicy', 'ResetBudget', 'ResetLaw', 'WeightedPotential', 'ResetHellinger', 'LiveSourceCertificate', 'LiveStoppedController', 'FiniteBudgetAlmostSure', 'GuardedResetBudget', 'GuardedResetHellinger', 'GuardedLiveController', 'StoppedActionCost']
QUANT_MODULES += ['ResetTrajectory','ResetFutureCost','MarkovCharge','ResetExpectation','TrajectoryBudget','GeneratedLiveController']
QUANT_MODULES += ['StoppedNoExit', 'ZeroSupportFixture', 'RecursiveWinningCertificate', 'StoppedSupportUpdate', 'RecursivePhaseExtraction', 'RecursiveKernelEquivalence', 'RecursiveGeneratedController', 'RecordedTransition', 'RecordedCharge', 'RecordedBudgetTransfer', 'StoppedRecordActions', 'RecursiveRecordedController']
MODULES=BASE_MODULES+["dependencies.StatisticalRepair","dependencies.PhysicalFlattening"]+QUANT_MODULES
TARGETS=['Orthemology.Tranche2.affinity_lt_one', 'Orthemology.Tranche2.hellinger_tree_budget', 'Orthemology.Tranche2.selectedCost_uniform_bound', 'Orthemology.Tranche2.blockMass_normalized', 'Orthemology.Tranche2.blockMass_affinity', 'Orthemology.Tranche2.supportBlock_expected_selections_bound', 'Orthemology.Tranche2.hellinger_subprob_tree_budget', 'Orthemology.Tranche2.stoppedMass_normalized', 'Orthemology.Tranche2.survivalAffinity_product', 'Orthemology.Tranche2.survivalMass_product', 'Orthemology.Tranche2.certificate_implies_strict_residual', 'Orthemology.Tranche2.dependent_hellinger_tree_budget', 'Orthemology.Tranche2.stoppedPhase_MLE_eq_full', 'Orthemology.Tranche2.stoppedPhase_expected_selections_bound', 'Orthemology.Tranche2.resetCost_root_bound', 'Orthemology.Tranche2.resetLeafMass_normalized', 'Orthemology.Tranche2.resetLeafCost_eq_budget', 'Orthemology.Tranche2.weightedHellinger_step', 'Orthemology.Tranche2.reset_hellinger_budget', 'Orthemology.Tranche2.live_certificate_implies_strict_residual', 'Orthemology.Tranche2.live_stopped_controller_budget', 'Orthemology.Tranche2.finite_budget_eventually_avoids', 'Orthemology.Tranche2.expected_event_count_eq_tsum', 'Orthemology.Tranche2.finite_tree_budget_transfer', 'Orthemology.Tranche2.resetCost_guarded_root_bound', 'Orthemology.Tranche2.guarded_reset_hellinger_budget', 'Orthemology.Tranche2.guarded_live_stopped_controller_budget', 'Orthemology.Tranche2.stopped_bad_count_le_planned', 'Orthemology.Tranche2.plannedBadCount_pos_iff', 'Orthemology.Tranche2.stopped_bad_count_le_live_charge']

TARGETS += ['Orthemology.Tranche2.'+x for x in ['markovTrajectory_finite_law','resetCost_eq_mass_future','lmarginal_pathCharge','markovTrajectory_expected_charge','resetTransition_lintegral','markovExpectedCharge_eq_resetFuture','trajectory_expected_charge_eq_resetCost','trajectory_total_charge_bound','trajectory_nat_charge_eventually_zero','generated_live_controller_eventually_good']]

TARGETS += ['Orthemology.Tranche2.'+x for x in ['ZeroSupportFixture.generated_zero_support_eventually_good','ZeroSupportFixture.permission_change_control','recursiveWinning_iff_stage','phaseActs_spec','stopped_exit_witness','phaseNext_actual_support','phaseNext_rank_decreases','recursive_plans_nonempty_licensed','recursive_generated_eventually_good','recursive_finite_budget','recorded_expected_charge_bound','recorded_nat_charge_transfer','recursive_recorded_bad_eventually_zero','recursive_recorded_eventually_nonempty','recursive_physical_eventually_good']]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--lean-bin',type=Path,required=True)
    ap.add_argument('--mathlib',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    src=out/'source';src.mkdir()
    a.lean_bin=a.lean_bin.resolve();a.mathlib=a.mathlib.resolve()
    env=os.environ.copy();env.pop('LEAN_PATH',None)
    env['PATH']=str(a.lean_bin)+os.pathsep+env['PATH']
    version=subprocess.check_output([str(a.lean_bin/'lean'),'--version'],env=env,text=True).strip()
    if not version.startswith('Lean (version 4.19.0,'):
        raise SystemExit('Wrong Lean version: '+version)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.mathlib,text=True).strip()
    if revision!='c44e0c8ee63ca166450922a373c7409c5d26b00b':
        raise SystemExit('Wrong Mathlib revision: '+revision)
    base_path=subprocess.check_output([str(a.lean_bin/'lake'),'env','printenv','LEAN_PATH'],
                                     cwd=a.mathlib,env=env,text=True).strip()
    paths=[str((a.mathlib/p).resolve()) if not Path(p).is_absolute() else p for p in base_path.split(':')]
    env['LEAN_PATH']=':'.join([str(src)]+paths)
    report={'status':'RUNNING','started_utc':datetime.now(timezone.utc).isoformat(),
            'lean_version':version,'lean_sha256':sha(a.lean_bin/'lean'),
            'mathlib_revision':revision,'modules':[],'targets':TARGETS,
            'nonclaims':['No universal Python-to-Lean refinement',
              'No kernel formalization of necessity or universal Python-to-Lean refinement; physical flattening is an almost-sure pathwise endpoint',
              'No world/source authority, novelty, adoption or meniscus promotion']}
    for module in MODULES:
        p=(root/'lean'/f'{module}.lean') if module in BASE_MODULES else (root/'lean-quant'/Path(module.replace('.', '/')).with_suffix('.lean'))
        text=p.read_text()
        if re.search(r'\b(sorry|admit|sorryAx|native_decide)\b',text):
            raise SystemExit('Prohibited proof-hole/native-decision token in '+module)
        if re.search(r'^\s*(axiom|constant|unsafe)\b',text,re.M):
            raise SystemExit('Unapproved declaration kind in '+module)
        dest=src/Path(module.replace('.', '/')).with_suffix('.lean');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        if module=='dependencies.StatisticalRepair' and sha(dest)!='8e6a771ec5c6b853055f7f13dd1b93b319172a2e10a4f41d71284cc681627bf4':raise SystemExit('Dependency pin mismatch')
        if module=='dependencies.PhysicalFlattening' and sha(dest)!='3111f8189b6bc36447c9da68da38775f828ce660ed19f5725cd7f240ee451d63':raise SystemExit('Flattening dependency pin mismatch')
        assert sha(p)==sha(dest)
        cmd=[str(a.lean_bin/'lean'),'-j1',f'--root={src}','-o',str(src/Path(module.replace('.', '/')).with_suffix('.olean')),str(dest)]
        run=subprocess.run(cmd,cwd=a.mathlib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=out/f'{module}.log';log.write_text(run.stdout)
        report['modules'].append({'module':module,'source_sha256':sha(dest),
            'returncode':run.returncode,'log_sha256':sha(log),'diagnostics':run.stdout,
            'olean_sha256':sha(dest.with_suffix('.olean')) if dest.with_suffix('.olean').exists() else None})
        (out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
        if run.returncode or (not module.startswith('dependencies.') and run.stdout.strip()):
            report['status']='FAIL_CLOSED';(out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
            raise SystemExit(f'{module} did not compile cleanly; see {log}')
    audit=src/'Audit.lean'
    audit.write_text('\n'.join('import '+m for m in MODULES)+'\n\n'+
                     '\n'.join(f'#check {t}\n#print axioms {t}' for t in TARGETS)+'\n')
    cmd=[str(a.lean_bin/'lean'),'-j1',f'--root={src}',str(audit)]
    run=subprocess.run(cmd,cwd=a.mathlib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=out/'Audit.log';log.write_text(run.stdout)
    report['audit']={'source_sha256':sha(audit),'returncode':run.returncode,'log_sha256':sha(log)}
    axiom_lists=re.findall(r"depends on axioms: \[([^\]]*)\]",run.stdout)
    allowed={'propext','Classical.choice','Quot.sound'}
    used=set(x.strip() for l in axiom_lists for x in l.split(',') if x.strip())
    report['audit']['axioms']=sorted(used)
    report['audit']['axiom_readbacks']=len(axiom_lists)
    ok=run.returncode==0 and used<=allowed and len(axiom_lists)==len(TARGETS)
    report['status']='PASS' if ok else 'FAIL_CLOSED'
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    (out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'result':str(out/'RESULT.json'),
                      'modules':len(MODULES),'target_readbacks':len(TARGETS),'axioms':sorted(used)},indent=2))
    if not ok: raise SystemExit(1)

if __name__=='__main__':main()
