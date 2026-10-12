# Dynamic V2 history-safety kernel: public projection

This package preserves the independently accepted V2 mathematical sources,
statements, reviews, controls and source bindings byte-for-byte. It adds a
portable replay entry point. No scientific result, protocol or claim is changed.

Two coordination PLAN.md bodies and ten historical generated custom .olean
objects are intentionally absent. Every custom Lean source is retained and rebuilt
fresh; external Mathlib caches are supplied separately. ORIGINAL_TO_PUBLIC.json
maps every original archive file to its unchanged public location or records the
omitted body's original size and SHA-256. The original top-level wrapper README
and manifest are preserved under provenance/. Historical source/review manifests
remain unchanged and may therefore name an omitted plan or generated object; the public mapping
explicitly accounts for those entries without distributing those bodies.

## Replay without executable permissions

Use Python 3 and explicitly supply the exact official Lean compiler and the
Mathlib source/cache root. The output directory must be new or empty:

python replay.py --lean /path/to/lean-4.19.0-linux/bin/lean --mathlib /path/to/mathlib-c44e0c8 --output /path/to/new-replay

No script from this archive is executed directly. The wrapper invokes the supplied
compiler and invokes Python source checks with the active Python interpreter.
Every distributed file may have mode 0644. The unchanged historical lean.sh and
verify.sh are preserved as evidence; the portable entry point does not call them
or rely on their old workspace paths. If manually using any shell script, invoke
it through bash rather than assuming ZIP executable modes were preserved.

The compiler SHA-256 is pinned to the reviewed official Lean 4.19.0 binary.
MATHLIB_SOURCE_PIN.json verifies every source file from exact commit
c44e0c8ee63ca166450922a373c7409c5d26b00b. Its compiled Mathlib and package caches
must already be present. Dependencies are not bundled, installed or rebuilt. The
source pin is not a claim of independent compiled-cache reproducibility.

The wrapper compiles all five original modules into a new isolated build directory,
then both fixtures, seven expected false-claim controls, seven original-Python
source scenarios, and both V2 reviewer proof files (ReviewChallenges and ReservationDomain). Before and after,
it checks the public manifest, complete original-to-public mapping, and the eleven
frozen owner-source/review bindings. It pins the manifest and mapping identities
at startup and refuses a metadata rewrite during replay. It cannot import historical candidate build
artifacts because LEAN_PATH starts with the fresh build and supplied dependency
caches only.

## Scientific claim ceiling

The accepted result is conditional finite-history safety, current/exact admitted
writes, durable cancellation of the same full command, and stable-epoch whole-table
preservation at the original dynamic V2 root/table interface. It retains authentic
serial authority, lifetime-union root bounds, coherent cross-copy root vetoes,
non-bypassable same-command mediation, and separate external reservation premises.
It does not establish physical implementation, actual consent, complete liveness,
covering/randomized search, or automatic transport to other interfaces.

The scientific acceptance is bound by ACCEPTANCE_BINDING.json and the V2 review
under tranche7-restart/formal/interlock-history-kernel/independent-review-v2/.
Publication/portability review is a separate distribution check, not new scientific
credit. Historical pending-review text inside the preserved candidate is superseded
by its separately bound final review receipt.
