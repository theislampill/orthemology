# Prose corrigendum: conservative nonce high-water premise

The current reader-facing retry note is `BATCH_RETRY_ARGUMENT_CORRECTED.md`. It differs from the frozen v3 retry note in exactly one sentence: the nonce high-water property is a **sufficient premise used by the conservative recovery proof**, not a necessary condition for recovery or progress.

The same accepted source model permits recovery with reused nonce values when the admitted complete command differs. The exact source counterexample, all Lean proofs, frozen v3 source bytes, v3 manifest, and sealed independent review remain unchanged.

This is an explicit prose projection, not a new scientific theorem or a reissued proof snapshot. `PROJECTION_MAP.json` binds both versions and the exact replacement. A distribution should retain the immutable v3 source note for manifest/review verification and direct readers to this corrected note.
