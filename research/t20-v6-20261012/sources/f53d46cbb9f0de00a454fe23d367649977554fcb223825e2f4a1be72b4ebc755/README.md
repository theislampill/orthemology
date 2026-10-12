# P03 minimal native Lean 4.19.0 execution packet

All candidate sources are UNVERIFIED. No compiler or .olean is included.
This is a new graph-plus-guarded-VCT formalisation proposal, not historical recovery.

Use the exact official native Linux Lean 4.19.0 compiler (commit6caaee842e94),
with its matching core library. These modules use Init only; no Mathlib download
is needed for this scoped run. The larger mapped project separately pins
Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b.

From this extracted directory, supply an independently verified compiler path:

```bash
set -euo pipefail
: "${LEAN419_NATIVE:?Set the exact native Lean4.19 compiler path}"
AUDITROOT="$(mktemp -d "${TMPDIR:-/tmp}/p03-lean419-audit.XXXXXX")"
python3 -B tools/run_formal419.py --lean "$LEAN419_NATIVE" --out "$AUDITROOT/build"
```

The runner refuses existing output, wrong/native-spoofed compiler paths,
missing/failing builds, altered frozen sources, absent or empty artifacts,
errors/sorry and missing or unexpected theorem/axiom readbacks. It records
actual compiler/core/source/artifact hashes, raw stdout/stderr and exits.
Fourteen theorem targets are expected, but currently none has been observed.

A future successful runner exit is BUILD_READBACK_PASS_PENDING_INDEPENDENT_TYPE_AND_ORIGIN_REVIEW.
Inspect the full printed types, main-type restatement, definitions and axiom
readbacks against the exact VCT guards. Verify official compiler origin and
repeat independently before granting scoped kernel credit. The runner does not
change canonical status or grant Q1f/owner adoption automatically. Do not accept
a wrong-version run, a stale artifact, sorryAx or a hypothesis that merely
assumes the entire intended conclusion. Preserve failed candidate preimages.

The parent attempt-0002 checkpoint carries exact statement comparison, ordinary
proofs, countermodels, precursor identities and complete provenance. Optional
TRC/P12/DAEE, real authority/source truth and world-model claims are not included.

MANIFEST.json binds all payload files; its sidecar binds the manifest. The
parent checkpoint binds this exact ZIP, avoiding a self-referential seal.
