#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./verify-solver.sh
source env.sh
export LEAN_PATH="$PWD/dependency-build:$LEAN_PATH"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="receipts/atoms-$stamp.log"
{
  lean --version
  for name in TargetMass PositiveAtomMass AtomEnumeration GeneratorEquality EffectiveAtoms AtomicReconstruction AtomicApproximation; do
    echo "FRESH_ATOM_SOURCE $name"
    lean -j1 -o "$name.olean" "$name.lean"
  done
  echo TARGET_FIXTURES_BEGIN
  lean -j1 -o TargetMassFixtures.olean TargetMassFixtures.lean
  echo TARGET_FIXTURES_END
  echo APPROXIMATION_FIXTURES_BEGIN
  lean -j1 -o AtomicApproximationFixtures.olean AtomicApproximationFixtures.lean
  echo APPROXIMATION_FIXTURES_END
  lean -j1 AtomVerification.lean
  sha256sum TargetMass.lean PositiveAtomMass.lean AtomEnumeration.lean GeneratorEquality.lean EffectiveAtoms.lean AtomicReconstruction.lean AtomicApproximation.lean TargetMassFixtures.lean AtomicApproximationFixtures.lean AtomVerification.lean verify-atoms.sh
} 2>&1 | tee "$log"
python3 - "$log" <<'PY'
import json,pathlib,re,sys
text=pathlib.Path(sys.argv[1]).read_text()
required=['Orthemology.Frontier.MealyMeasure.'+line.removeprefix('#print axioms ') for line in pathlib.Path('AtomVerification.lean').read_text().splitlines() if line.startswith('#print axioms ')]
seen={}
for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text):
    axioms={a.strip() for a in body.split(',') if a.strip()}
    assert axioms <= {'propext','Classical.choice','Quot.sound'}, (name,axioms)
    seen[name]=sorted(axioms)
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):seen[name]=[]
assert set(required)<=set(seen), ('missing audits',set(required)-set(seen))
assert not re.search(r'(^|\n).*error:',text), 'Compiler error in receipt'
sources=['TargetMass','PositiveAtomMass','AtomEnumeration','GeneratorEquality','EffectiveAtoms','AtomicReconstruction','AtomicApproximation','TargetMassFixtures','AtomicApproximationFixtures']
assert not re.search(r'\b(sorry|axiom)\b','\n'.join(pathlib.Path(p+'.lean').read_text() for p in sources)), 'Proof hole or added axiom'
expected={'TARGET':['1','0','0','(1 : Rat)/2','some ([], 1)','none'],'APPROXIMATION':['1','0']}
for tag,want in expected.items():
    actual=text.split(tag+'_FIXTURES_BEGIN\n')[1].split(tag+'_FIXTURES_END')[0].strip().splitlines()
    assert actual==want,(tag,actual,want)
pathlib.Path(sys.argv[1]+'.axioms.json').write_text(json.dumps({n:seen[n] for n in required},indent=2)+'\n')
print('AXIOM_CEILING_OK',len(required),'atom declarations; TARGET_FIXTURES_OK 6; APPROXIMATION_FIXTURES_OK 2')
PY
echo "Verified atoms; receipt $log"
