#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
cd ..
BASE="$PWD"
LEAN="$BASE/.toolchains/lean-4.19.0-linux/bin/lean"
export LEAN_PATH="$ROOT/validation:$BASE/hase-closed-scalar-review-20261010/fresh-lib:$(cat "$BASE/hase-full-per-review-20261010/lean_path.txt")"
python "$ROOT/verify_certificate_inputs.py"
"$LEAN" --trust=0 -o "$ROOT/validation/ScalarCertificates.olean" "$ROOT/ScalarCertificates.lean" > "$ROOT/validation/SCALAR_CERTIFICATES.log" 2>&1
"$LEAN" --trust=0 --run "$ROOT/SourceExport.lean" > "$ROOT/validation/source_ast_reexport.json"
cmp "$ROOT/source_ast.json" "$ROOT/validation/source_ast_reexport.json"
"$LEAN" --trust=0 -o "$ROOT/validation/LiteralSourceQ.olean" "$ROOT/LiteralSourceQ.lean" > "$ROOT/validation/LITERAL_SOURCE_Q.log" 2>&1
(cd "$ROOT" && python -m unittest discover -v) > "$ROOT/validation/PYTHON_TESTS.log" 2>&1
python "$ROOT/generate_controls.py" > "$ROOT/validation/GENERATION.log"
"$LEAN" --trust=0 -o "$ROOT/validation/ConcreteScalarCertificates.olean" "$ROOT/ConcreteScalarCertificates.lean" > "$ROOT/validation/CONCRETE_KERNEL_REPLAY.log" 2>&1
"$LEAN" --trust=0 -o "$ROOT/validation/NegativeCertificateControls.olean" "$ROOT/NegativeCertificateControls.lean" > "$ROOT/validation/NEGATIVE_KERNEL_REPLAY.log" 2>&1
"$LEAN" --trust=0 -o "$ROOT/validation/OpenCertificateControl.olean" "$ROOT/OpenCertificateControl.lean" > "$ROOT/validation/OPEN_CERTIFICATE_REPLAY.log" 2>&1
if grep -E 'sorryAx|Lean.ofReduceBool|error:' "$ROOT/validation/CONCRETE_KERNEL_REPLAY.log"; then exit 1; fi
printf 'PASS: source hashes/export, Python adversarial tests, and concrete Lean certificate replay.\n'
