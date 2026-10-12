#!/usr/bin/env bash
# Recompute under build/, leaving the delivered evidence unchanged.
set -euo pipefail
cd "$(dirname "$0")"
PYTHON=${PYTHON:-python3}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p build/verification
for name in legacy_relational_checks legacy_reflexive_checks verify_integrated verify_v2 verify_revision verify_v4 verify_v5; do
 "$PYTHON" "verification/$name.py" --output "build/verification/$name.json" > "build/verification/$name.stdout"
done
"$PYTHON" verification/check_documents.py --output build/verification/document-checks.json
printf 'VERIFICATION_PASS\n'
