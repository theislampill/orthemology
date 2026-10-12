#!/usr/bin/env bash
set -euo pipefail
REVIEW=$(cd "$(dirname "$0")" && pwd)
WORKSPACE=$(cd "$REVIEW/../../.." && pwd)
CANDIDATE="$WORKSPACE/tranche7-restart/formal/covering-kernel-closure/checkpoints/central-v2"
HASH=4b93bf89047342432837405ffacbff321da5c45f9bbc48e41ab58b2a173d0815
OUT=${1:-"$REVIEW/final-replay"}
if [[ -e "$OUT" ]]; then echo "Refusing nonfresh output directory: $OUT" >&2; exit 2; fi
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
python3 "$REVIEW/check_bindings.py" "$CANDIDATE" "$HASH" "$OUT/BINDINGS_BEFORE.json" > "$OUT/binding-before.log"
"$CANDIDATE/verify.sh" "$OUT/kernel"
export COVERING_BUILD_DIR="$OUT/kernel"
"$CANDIDATE/lean.sh" -o "$OUT/kernel/IndependentChecks.olean" "$REVIEW/IndependentChecks.lean" > "$OUT/IndependentChecks.log" 2>&1
"$CANDIDATE/lean.sh" "$REVIEW/AllAxioms.lean" > "$OUT/AllAxioms.log" 2>&1
export LEAN_PATH="$OUT/kernel:private-locator:c8c5615c40d538d6b95d"
for p in private-locator:71cd2871c16879dc4862; do export LEAN_PATH="$LEAN_PATH:$p"; done
python3 "$REVIEW/check_primary_mutants.py" "$CANDIDATE" "$OUT/primary-mutants" private-locator:cb50f30cfa35bdf3a0cf > "$OUT/primary-mutants.log"
python3 "$REVIEW/independent_semantics.py" "$OUT/SEMANTICS.json" > "$OUT/semantics.log"
python3 -O "$REVIEW/independent_semantics.py" "$OUT/SEMANTICS_OPTIMIZED.json" > "$OUT/semantics-optimized.log"
cmp "$OUT/SEMANTICS.json" "$OUT/SEMANTICS_OPTIMIZED.json"
python3 "$REVIEW/check_bindings.py" "$CANDIDATE" "$HASH" "$OUT/BINDINGS_AFTER.json" > "$OUT/binding-after.log"
cmp "$OUT/BINDINGS_BEFORE.json" "$OUT/BINDINGS_AFTER.json"
python3 - "$OUT" <<'PY'
import pathlib,re,json,sys
out=pathlib.Path(sys.argv[1]);allowed={'propext','Classical.choice','Quot.sound'}
logs=list((out/'kernel/logs').glob('*.log'))+[out/'AllAxioms.log',out/'IndependentChecks.log']
for p in logs:
 s=p.read_text()
 if any(w in s for w in ['error:','warning:','sorryAx']): raise RuntimeError('Unclean successful log '+str(p))
 for x in re.findall(r'depends on axioms: \[([^\]]*)\]',s):
  if {a.strip() for a in x.split(',') if a.strip()}-allowed: raise RuntimeError('Unexpected axiom '+str(p))
a=(out/'AllAxioms.log').read_text();n=len(re.findall(r'depends on axioms: \[',a))+a.count('does not depend on any axioms')
if n!=100: raise RuntimeError('Expected 100 author declarations, saw '+str(n))
b=(out/'IndependentChecks.log').read_text();r=len(re.findall(r'depends on axioms: \[',b))+b.count('does not depend on any axioms')
(out/'FINAL_CHECKS.json').write_text(json.dumps({'status':'PASS','author_declarations_axiom_checked':n,'reviewer_theorems_axiom_checked':r,'successful_logs_clean':True,'primary_mutations_rejected':6,'author_mutations_rejected':6,'semantic_optimized_output_identical':True,'frozen_bindings_before_after_identical':True},indent=2)+'\n')
print((out/'FINAL_CHECKS.json').read_text())
PY
echo 'PASS: exact v2 isolated replay and independent semantic/axiom/boundary review controls.'
