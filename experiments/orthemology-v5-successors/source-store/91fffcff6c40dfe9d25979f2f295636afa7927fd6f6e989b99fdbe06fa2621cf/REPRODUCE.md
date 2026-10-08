# Optional bounded reproduction

This manual recipe derives from the independent review's successful Lean 4.19.0 commands. The compiler commands were executed historically; the portable path guard is a packaging addition and has only guard-level checks. Preparing this source-only packet does not run Lean, download or install dependencies, or repeat an older proof campaign.

Prerequisites are Python 3.9 or newer (for Path.is_relative_to), a POSIX shell and an existing official Linux Lean 4.19.0 installation. The historical executable SHA-256 is 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023. Version output identifies commit 6caaee842e94, Release. This recipe pins that executable; another platform binary needs a separately reviewed identity. The sole distinct direct author import is Init, which is both implicit and explicit. ReviewerProbes imports the newly compiled control. No Mathlib installation is required.

Set PACKET to the absolute directory containing this README and the selected author Lean files; LEAN419 to the absolute external bin/lean executable; and FRESH_OUT to an absolute, nonexistent output directory whose parent already exists. Source, compiler installation and output must be separate trees. Existing output paths, symlink ancestors, escaping symlinks in protected input trees, and input/output containment in either direction are refused. Do not change the inputs or paths concurrently with this sequence. Run the complete block below in a POSIX shell; it stops on unexpected positive-command failure. Every compiler output goes into the newly created directory.

```sh
(
set -eu
: "${PACKET:?Set absolute PACKET}"
: "${LEAN419:?Set absolute LEAN419}"
: "${FRESH_OUT:?Set absolute FRESH_OUT}"
python3 -I - "$PACKET" "$LEAN419" "$FRESH_OUT" <<'PY_GUARD'
from pathlib import Path
import hashlib, os, sys

packet, lean, out = [Path(p) for p in sys.argv[1:]]
def require_plain_absolute(p):
    if not p.is_absolute() or '..' in p.parts:
        raise SystemExit('Use absolute paths without parent traversal')
    for q in (p, *p.parents):
        if q.is_symlink():
            raise SystemExit('Symlink path or ancestor refused')
    if p.resolve() != p:
        raise SystemExit('Noncanonical path refused')
for p in (packet, lean, out):
    require_plain_absolute(p)
if out.exists() or out.is_symlink():
    raise SystemExit('Output must not exist')
if not out.parent.is_dir():
    raise SystemExit('Output parent must already exist')
if not packet.is_dir() or not lean.is_file() or not os.access(lean, os.X_OK):
    raise SystemExit('Existing source directory and executable compiler required')
compiler_root = lean.parent.parent
if packet.is_relative_to(compiler_root) or compiler_root.is_relative_to(packet):
    raise SystemExit('Source and compiler trees must be disjoint')
for protected in (packet, compiler_root):
    if out.is_relative_to(protected) or protected.is_relative_to(out):
        raise SystemExit('Input and output trees must be disjoint')
    for parent, dirs, files in os.walk(protected, followlinks=False):
        for name in dirs + files:
            p = Path(parent) / name
            if p.is_symlink() and not p.resolve().is_relative_to(protected):
                raise SystemExit('Escaping input-tree symlink refused')
expected = {
    'OriginationTypeControl.lean': 'e3e5480db5b874448b7f4448ce6bce66e426995afbcb45e31ce61f755e03fdfe',
    'OverreachRejected.lean': '6dfd3ab5400bad336045e449400bb50f5066c003cf10c9413b447b8d36d09c60',
    'review/ReviewerProbes.lean': 'f176d255baf686b29e4516dfd5796907ed3345befa0370d9812f57faeab826b7',
}
for name, digest in expected.items():
    p = packet / name
    require_plain_absolute(p)
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        raise SystemExit('Selected source identity mismatch')
if hashlib.sha256(lean.read_bytes()).hexdigest() != '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':
    raise SystemExit('Compiler identity mismatch')
out.mkdir()
PY_GUARD
cp "$PACKET/OriginationTypeControl.lean" "$FRESH_OUT/"
cp "$PACKET/OverreachRejected.lean" "$FRESH_OUT/"
cp "$PACKET/review/ReviewerProbes.lean" "$FRESH_OUT/"
cd "$FRESH_OUT"
export LEAN_PATH="$FRESH_OUT"
"$LEAN419" --version > lean-version.log 2>&1
"$LEAN419" --help > lean-help.log 2>&1
"$LEAN419" --deps OriginationTypeControl.lean > direct-imports.log 2>&1
"$LEAN419" -t 0 -o OriginationTypeControl.olean OriginationTypeControl.lean > final-check.log 2>&1
"$LEAN419" -t 0 -o ReviewerProbes.olean ReviewerProbes.lean > probes.log 2>&1
if "$LEAN419" -t 0 OverreachRejected.lean > overreach-rejection.log 2>&1; then
    echo 'Unexpected success of deliberately false controls' >&2
    exit 1
else
    negative_exit=$?
    test "$negative_exit" -eq 1
fi
python3 -I - <<'PY_CHECK'
from pathlib import Path
main = Path('final-check.log').read_text()
probes = Path('probes.log').read_text()
negative = Path('overreach-rejection.log').read_text()
deps = set(Path('direct-imports.log').read_text().strip().splitlines())
checks = {
    'seven author readbacks': main.count("'T20.OntologyTypeControl.") == 7,
    'seven reviewer readbacks': probes.count("'IndependentReview.") == 7,
    'no positive errors or admissions': 'error:' not in main + probes and 'sorryAx' not in main + probes,
    'two substantive false-proposition rejections': negative.count("error: tactic 'decide' proved that the proposition") == 2,
    'no other negative errors': negative.count('error:') == 2 and negative.count('is false') == 2,
    'one distinct direct Init dependency': len(deps) == 1 and next(iter(deps)).endswith('/Init.olean'),
}
failed = [name for name, passed in checks.items() if not passed]
if failed:
    raise SystemExit('Failed checks: ' + ', '.join(failed))
print('Bounded checks passed; inspect new logs and record new run identity separately.')
PY_CHECK
)
```

The positive run must print the seven author readbacks; the reviewer module prints seven additional readbacks. The only historically reported axioms are propext and Quot.sound, with several axiom-free results. The deliberately false controls must fail on their false propositions. Import, syntax or resource failures do not count as a successful negative test. Compare substantive output against final-check.log, review/probes.log and overreach-rejection.log in this packet; only environment-specific dependency prefixes may differ. Any new execution is a new run and needs its own dated receipt. The guards do not authenticate a metaphysical interpretation or add source-reading credit.
