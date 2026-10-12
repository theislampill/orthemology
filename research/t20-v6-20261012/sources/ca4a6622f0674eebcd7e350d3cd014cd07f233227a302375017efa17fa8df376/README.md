# Sixth bounded control follow-up, 2 October 2026

Both merged baseline controls remain **INCONCLUSIVE**. This packet records:

- A fresh Lean real-number check of the cost mutation's exact scalar premise
  obstruction. This is not full cost-mutant rejection.
- A fresh 162-module exact runtime positive closure, three selected endpoint
  type/axiom readbacks, and the unchanged runtime mutant's whnf timeout at
  200,000 heartbeats. No timeout is counted as semantic rejection.

This is Sixth baseline revalidation only, with no Seventh theorem credit and
no canonical repository edits. Start with REVIEW.md and FINDINGS.json.

## What is included

runtime/src contains all 162 custom sources needed for FullControllerCanonicalLaw,
including the three nested custom core modules. No predecessor archive is needed
for that target. Both exact mutant files, their hash-bound diffs, the relevant
original cost sources, and the limited scalar probes are included. Completed
execution receipts and logs are under evidence/. Pinned public baseline receipts
are under baseline/. No compiled objects, global caches, tool binaries, large
outer archives, or raw service captures are bundled.

This is self-contained only with respect to CUSTOM runtime sources. External
Lean/Mathlib and official caches remain required. The full cost import closure
is intentionally absent: only its exact changed scalar obligation is replayed.

## Validate packaging only

Run from any directory:

    python3 /path/to/packet/replay.py --verify-only

This validates complete packet inventory, file hashes, the exact two mutation
derivations, and the reconstructed 162-module custom dependency closure. It
neither runs Lean nor claims a new proof result.

## Dependencies

Use the Linux x86_64 official Lean 4.19.0 release, whose lean executable SHA256 is
92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023.
Use a clean Mathlib git checkout at
c44e0c8ee63ca166450922a373c7409c5d26b00b with the eight revisions in
DEPENDENCY_PINS.json. Put this Lean bin directory first on PATH, and from that
Mathlib checkout use its official `lake exe cache get` flow. Set MATHLIB_CACHE_DIR
to a writable cache directory if needed. The official dependency caches are an
explicit trust boundary; they are not proof artifacts created by this packet.
The replay command verifies compiler bytes/version and all nine git revisions
and tracked-clean states. It does not download or modify dependencies.

## Reproduce the bounded work

Choose a new absent output directory outside the immutable extracted packet:

    python3 /path/to/packet/replay.py \
      --lean-bin /path/to/lean-4.19.0-linux/bin \
      --mathlib /path/to/mathlib4 \
      --out /path/to/new-followup-output --mode all

Use --mode cost for only the scalar checks, or --mode runtime for the exact
runtime positive closure, selected readbacks, and original runtime mutant.
Custom runtime sources compile fresh and sequentially into the new output.
No custom author objects are reused. No heartbeat flags are added. Each runtime
compile has a 180-second wall-clock ceiling; resource limits remain inconclusive.
The existing completed run used two independent compiler processes; its receipts
record that fact. The portable sequential entrypoint was structurally validated
but was not used to repeat proof runs during packaging.

Expected interpretation, not an instruction to force an outcome:

- Cost scalar positive: exit 0. Scalar negative: concrete type mismatch.
- Runtime positive: all 162 modules compile and three endpoint readbacks pass.
- Runtime mutant: the recorded completed run timed out at whnf. Any future
  non-resource outcome requires review; the driver never silently rewrites the
  two merged baseline INCONCLUSIVE statuses.

## Evidence projection

Logs and receipt command fields use symbolic roots instead of machine-specific
filesystem locations. PROJECTIONS.json binds each original hash to its public
projection. Receipt original_log_sha256 fields preserve the original log digest;
log_sha256 fields identify the bundled projected log. All .lean source bodies,
mutation bytes, and baseline public repository receipts remain exact.

No external human review or empirical/world-level validation is claimed.
