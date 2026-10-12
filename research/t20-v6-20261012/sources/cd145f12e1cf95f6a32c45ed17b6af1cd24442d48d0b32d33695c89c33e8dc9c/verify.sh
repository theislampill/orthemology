#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
lean --version | tee logs/toolchain-version.log
lake --version | tee logs/lake-version.log
lake clean
lake build ResetContinuation Checks Verify 2>&1 | tee logs/clean-build.log
for src in ResetContinuation.lean Checks.lean Verify.lean; do
  lake env lean -DwarningAsError=true "$src" 2>&1 | tee "logs/final-${src%.lean}.log"
done
if grep -nE '(^|[[:space:]])(sorry|admit|axiom|unsafe)([[:space:]]|$)' ResetContinuation.lean Checks.lean Verify.lean; then
  echo 'Disallowed placeholder/custom-axiom/unsafe token found' >&2
  exit 1
fi
python3 verify_controls.py
sha256sum ResetContinuation.lean Checks.lean Verify.lean lakefile.toml lake-manifest.json lean-toolchain | tee logs/source-hashes.log
