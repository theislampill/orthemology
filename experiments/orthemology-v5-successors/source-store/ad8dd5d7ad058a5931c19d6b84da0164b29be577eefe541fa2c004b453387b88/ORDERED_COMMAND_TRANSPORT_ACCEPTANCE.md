# Ordered-command transport: independent acceptance

The frozen v1-r2 mathematical core passes independent review.

## Exact artifact

- Source archive: `Ordered_Command_Transport_Core_v1_r2.zip`
- Archive SHA-256: `661507cd937a349802b594facef78ed66d19f8301a2c75844d541c9868d69079`
- Manifest SHA-256: `6680fee2337761a74ea866416766b5454fa5d27c6243c6682c8eb4794eb15863`
- Core verification SHA-256: `0418add973d79e4e12c77ee449fbd180d194c2d39407cd0473a246c1055112b1`

The actual ZIP passes CRC and manifest checks. All eight frozen modules and their 26 custom transitive dependencies were compiled from cold source copies without reusing author objects. All 72 named declarations have only the standard transitive axioms propext, Classical.choice and Quot.sound; nine anonymous contract examples also compile. Twenty additional independently written definitions/theorems and their axiom audit pass.

## Accepted result

For each selected support, a coherent supplied nodup ordering is exchanged with the old ordering by an actual involution. Every other ordering and every other complete-command field is preserved. Identical old/new orders give identity. Distinct complete commands remain distinct even when their supports coincide. Independent controls demonstrate why normalizing all paths by sorting would instead be noninjective.

The map transports every commitment, tombstone and cancellation-receipt key, as well as the command memories in corrupt-event root payloads. Other root and state fields, including certificates, epoch, pending, acknowledgements and the full Plant, remain exact. The initial state is fixed.

Primitive operations are conjugated as complete state equalities. Step and ordered finite Trace hold if and only if they hold between the transported endpoints with pointwise transported events. Typed admission and effect are preserved. The source applied Boolean is exactly equal with the same badOpen value, including false.

Conditional counterexamples confirm that unchanged-state reuse of a nonfixed command key can fail for commitments, tombstones, close receipts and corrupt-event payloads. The conditions remain explicit; the controls do not claim those arbitrary snapshots are reachable.

## Trust and limits

Checks used pinned Lean 4.19.0, one sequential `-j1` lane, ordinary resource limits and a 180-second per-process ceiling. The supplied compiler and exact precompiled external dependency cache remain trusted. Their pins were checked read-only; five documented path-only cache-fetcher trace metadata differences were verified separately, with scientific dependency objects unchanged.

This acceptance concerns a proof-side whole-history isomorphism. It does not authorize an in-place physical-state conversion or old-key reuse; establish raw native-list equality or arbitrary-interface invariance; or certify reference-program composition, executable transport, signature reminting, sample authenticity, transcript opacity or wall-clock bounds.

Reference trial/run and public-program composition remain separate work. Any such result must preserve pointwise support/index/nonce correspondence and address service ordering. This acceptance is not a Ninth Tranche completion claim.
