#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./verify.sh
source env.sh
export LEAN_PATH="$PWD/dependency-build:$LEAN_PATH"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="receipts/solver-$stamp.log"
{
  lean --version
  lean -j1 -o MealySolver.olean MealySolver.lean
  echo EXECUTABLE_FIXTURES_BEGIN
  lean -j1 -o MealySolverFixtures.olean MealySolverFixtures.lean
  echo EXECUTABLE_FIXTURES_END
  lean -j1 SolverVerification.lean
  sha256sum Mealy*.lean Verification.lean SolverVerification.lean env.sh verify.sh verify-solver.sh
} 2>&1 | tee "$log"
python3 - "$log" <<'PY'
import json,pathlib,re,sys
text=pathlib.Path(sys.argv[1]).read_text()
required=['Orthemology.Frontier.MealyMeasure.'+line.removeprefix('#print axioms ') for line in pathlib.Path('SolverVerification.lean').read_text().splitlines() if line.startswith('#print axioms ')]
seen={}
for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text):
    axioms={a.strip() for a in body.split(',') if a.strip()}
    assert axioms <= {'propext','Classical.choice','Quot.sound'}, (name,axioms)
    seen[name]=sorted(axioms)
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):seen[name]=[]
assert set(required)<=set(seen), ('missing audits',set(required)-set(seen))
assert not re.search(r'(^|\n).*error:',text), 'Compiler error in receipt'
assert not re.search(r'\b(sorry|axiom)\b','\n'.join(pathlib.Path(p).read_text() for p in ['MealySolver.lean','MealySolverFixtures.lean'])), 'Proof hole or added axiom'
actual=text.split('EXECUTABLE_FIXTURES_BEGIN\n')[1].split('EXECUTABLE_FIXTURES_END')[0].strip().splitlines()
expected=['1','0','(1 : Rat)/2','(2 : Rat)/3','(1 : Rat)/3']
assert actual==expected, ('bad executable fixtures',actual,expected)
pathlib.Path(sys.argv[1]+'.axioms.json').write_text(json.dumps({n:seen[n] for n in required},indent=2)+'\n')
print('AXIOM_CEILING_OK',len(required),'solver declarations; EXECUTABLE_FIXTURES_OK',len(expected))
PY
echo "Verified solver; receipt $log"
