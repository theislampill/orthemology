#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source env.sh
mkdir -p receipts dependency-build/P02A2
export LEAN_PATH="$PWD/dependency-build:$LEAN_PATH"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="receipts/verify-$stamp.log"
{
  lean --version
  test "$(lean --version)" = 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
  test "$(git -C private-locator:41bd9f979012c8bbc235 rev-parse HEAD)" = c44e0c8ee63ca166450922a373c7409c5d26b00b
  echo 'PIN_OK mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b'
  for name in PERRefinement MealyRefinement BlockMismatch; do
    echo "FRESH_DEPENDENCY $name"
    lean -j1 --root=private-locator:4b06887cf6b87610e5b8 -o "dependency-build/$name.olean" "private-locator:3b7b6ea7d1244d7e6032"
  done
  lean -j1 --root=private-locator:6e1cdd2685640ba2eef0 -o dependency-build/P02A2/MeasureCore.olean private-locator:a92a39d66d81831ff358
  lean -j1 --root=private-locator:6e1cdd2685640ba2eef0 -o dependency-build/Q8Measure.olean private-locator:f7dcb63e634dfd97f0e4
  for name in MealyMeasure MealyHitting MealyAtoms MealyRational MealyMeasureFixtures; do
    echo "FRESH_SOURCE $name"
    lean -j1 -o "$name.olean" "$name.lean"
  done
  lean -j1 Verification.lean
  sha256sum Mealy*.lean Verification.lean env.sh verify.sh
  sha256sum private-locator:4c25c8bd6eb6a63c8b96{PERRefinement,MealyRefinement,BlockMismatch}.lean private-locator:98f16bb1cca6a5179c45{P02A2/MeasureCore,Q8Measure}.lean
} 2>&1 | tee "$log"
python3 - "$log" <<'PY'
import json,pathlib,re,sys
text=pathlib.Path(sys.argv[1]).read_text()
required=['Orthemology.Frontier.MealyMeasure.'+line.removeprefix('#print axioms ') for line in pathlib.Path('Verification.lean').read_text().splitlines() if line.startswith('#print axioms ')]
seen={}
for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text):
    axioms={a.strip() for a in body.split(',') if a.strip()}
    assert axioms <= {'propext','Classical.choice','Quot.sound'}, (name,axioms)
    seen[name]=sorted(axioms)
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):seen[name]=[]
assert set(required)<=set(seen), ('missing audits',set(required)-set(seen))
assert not re.search(r'(^|\n).*error:',text), 'Compiler error in receipt'
assert not re.search(r'\b(sorry|axiom)\b','\n'.join(p.read_text() for p in pathlib.Path('.').glob('Mealy*.lean'))), 'Proof hole or added axiom'
pathlib.Path(sys.argv[1]+'.axioms.json').write_text(json.dumps({n:seen[n] for n in required},indent=2)+'\n')
print('AXIOM_CEILING_OK',len(required),'required declarations')
PY
echo "Verified; receipt $log"
