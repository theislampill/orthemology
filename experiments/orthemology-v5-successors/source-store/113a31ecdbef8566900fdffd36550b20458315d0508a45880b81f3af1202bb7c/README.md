# Portable independent-review wrapper

The original independent-review archive and all accepted proof sources/receipts remain unchanged. This wrapper binds that exact archive and supplies portable compiler, Mathlib, archive and output paths.

It also corrects one replay-only compatibility issue: the cleaned core runner emits PASS_INDEPENDENT_REVIEW_CHECKS, while the original literal continuation expected PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS from the completed staged run. Both successful statuses are accepted, followed by the unchanged closure, source and object checks. The literal runner's embedded Mathlib archive location becomes the explicit CLI argument. No proof source, proof loop, heartbeat setting or prior scientific disposition changes.

Required review archive:

- Semantic_Control_Independent_Review_20261002.zip
- SHA256 a7dac7ac8fe8e867b4581ebcd2757067371985eb728a66fc83720e33389c8f9b
- REVIEW_MANIFEST.json SHA256 94b983318333e8bd79f08ba2e43f72add2f561629b3b54b05a37faed42d70abf

Validate all 737 archive entries and both driver derivations without running proofs:

    python3 replay_review_portable.py --review-zip /path/to/review.zip --verify-only

Run a clean independent reproduction into a new absent output directory:

    python3 replay_review_portable.py --review-zip /path/to/review.zip \
      --lean-bin /path/to/lean-4.19.0-linux/bin \
      --mathlib /path/to/mathlib4 \
      --mathlib-archive /path/to/pinned-mathlib.tar.gz \
      --out /path/to/new-absent-output

For an exact clean Git checkout of Mathlib, omit --mathlib-archive. The unchanged source helper verifies compiler bytes, package revisions, dependency source identities and the official-cache trust boundary. No downloads or dependency edits occur.

The archive already contains the complete custom source snapshots. The wrapper extracts them only into its newly created output and produces a separately hash-bound literal-driver derivation and diff. The core compiles 167 runtime and 146 cost modules from source, then the literal route uses only those newly rebuilt verified core objects. It checks all 80 core declarations and 56 literal declarations, exact target correspondence, measurable failure, old/old positive behavior, cost mutation, encoded policies and 340 finite native cases.

The complete portable route passed on 2 October 2026 at 21:27:12 UTC. COMPLETED_PORTABLE_REPLAY.json and evidence/full-replay/WRAPPER_RESULT.json record the new execution; FULL_REPLAY_PROJECTIONS.json maps every delivered receipt/log to its original digest. All 167 runtime, 146 cost and three literal modules, all 80/56 declaration audits, exact statement/measure controls, four policy encodings and 340 finite native cases passed. The concrete cost rejection retains its additional resource diagnostic; the old runtime mutant was not rerun.

WRAPPER_SPEC.json and VALIDATION.json are preserved pre-run specification/guard records. Their pending or guard-only fields describe that earlier stage, and do not override the completed execution receipt. The original reviewed scripts, sources and staged receipts remain unchanged. The generated literal driver under evidence/ is retained only to inspect the exact derivation; invoke replay_review_portable.py as the entrypoint. This is a portable reproduction of the already independently reviewed route, not a new external-human review.
