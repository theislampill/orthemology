#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$PWD/lean-4.19.0-linux/bin:$PATH"
export XDG_CACHE_HOME="$PWD/cache"
mkdir -p receipts
stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="receipts/verify-$stamp.log"
{
  lean --version
  test "$(lean --version)" = 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
  test "$(git -C mathlib4 rev-parse HEAD)" = c44e0c8ee63ca166450922a373c7409c5d26b00b
  python3 - <<'PY'
import json,pathlib,subprocess
manifest=json.load(open('SOURCE_V5_MANIFEST.json'))
for p in manifest['packages']:
    if p['name']=='mathlib': d=pathlib.Path('mathlib4')
    else: d=pathlib.Path('.lake/packages')/p['name']
    actual=subprocess.check_output(['git','-C',str(d),'rev-parse','HEAD'],text=True).strip()
    assert actual==p['rev'], (p['name'],actual,p['rev'])
    subprocess.run(['git','-C',str(d),'diff','--exit-code','HEAD','--'],check=True,stdout=subprocess.DEVNULL)
    print('PIN_OK_CLEAN',p['name'],actual)
PY
  lake build
  lake env lean Verification.lean
  sha256sum *.lean lean-toolchain lakefile.lean lake-manifest.json
} 2>&1 | tee "$log"
python3 - "$log" <<'PYVERIFY'
import pathlib,re,sys
text=pathlib.Path(sys.argv[1]).read_text()
required=[]
for line in pathlib.Path('Verification.lean').read_text().splitlines():
    if line.startswith('#print axioms '):
        required.append('Orthemology.Frontier.'+line.removeprefix('#print axioms '))
seen={}
for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text):
    axioms={a.strip() for a in body.split(',') if a.strip()}
    assert axioms <= {'propext','Classical.choice','Quot.sound'}, (name,axioms)
    seen[name]=sorted(axioms)
for name in re.findall(r"'([^']+)' does not depend on any axioms",text): seen[name]=[]
assert set(required)<=set(seen), ('missing audits',set(required)-set(seen))
assert not re.search(r'(^|\n).*error:',text), 'Compiler error in receipt'
import json
pathlib.Path(sys.argv[1]+'.axioms.json').write_text(json.dumps({n:seen[n] for n in required},indent=2)+'\n')
print('AXIOM_CEILING_OK',len(required),'required declarations')
PYVERIFY
echo "Verified; receipt $log"
