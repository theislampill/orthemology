#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python3 verification/verify_sources.py
lake env lean verification/CheckTheorems.lean
lake env lean verification/AxiomAudit.lean
lake env lean verification/CheckCombined.lean
lake env lean verification/CombinedAxiomAudit.lean
lake env lean verification/IndependentKernelChecks.lean
lake env lean ExtensionalRepairAudit.lean
python3 verification/check_negative_controls.py
