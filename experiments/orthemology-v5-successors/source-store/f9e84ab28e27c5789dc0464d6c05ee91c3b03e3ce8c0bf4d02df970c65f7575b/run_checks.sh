#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 verification/verify_sources.py
python3 verification/test_source_checks.py
for check in CheckTheorems AxiomAudit CheckCombined CombinedAxiomAudit IndependentKernelChecks; do
  lake env lean "verification/inherited/${check}.lean"
done
lake env lean ExtensionalRepairAudit.lean
python3 verification/check_inherited_negative_controls.py
lake env lean verification/CheckInterfaces.lean
mkdir -p .lake/build/lib/lean/verification
lake env lean -o .lake/build/lib/lean/verification/KernelAudit.olean verification/KernelAudit.lean
python3 verification/check_new_negative_controls.py
lake env lean verification/CheckComplexityInterfaces.lean
lake env lean verification/ComplexityKernelAudit.lean
python3 verification/check_complexity_negative_controls.py
lake env lean verification/CheckBooleanInterfaces.lean
lake env lean -o .lake/build/lib/lean/verification/BooleanKernelAudit.olean verification/BooleanKernelAudit.lean
python3 verification/check_boolean_negative_controls.py
lake env lean verification/CheckGateInterfaces.lean
lake env lean verification/RestrictedKernelAudit.lean
lake env lean CheckerControls.lean
lake env lean CheckerKernelAudit.lean
lake env lean verification/CheckRestrictedInterfaces.lean
python3 verification/check_restricted_negative_controls.py
lake env lean verification/RestrictedComputationalAudit.lean
lake env lean PolynomialTestAudit.lean
python3 verification/check_polynomial_test_controls.py
lake env lean verification/AllProjectProofAudit.lean
lake env lean verification/ExportDeclarationInventory.lean
printf '\nALL_UNIFIED_CHECKS_PASS\n'
