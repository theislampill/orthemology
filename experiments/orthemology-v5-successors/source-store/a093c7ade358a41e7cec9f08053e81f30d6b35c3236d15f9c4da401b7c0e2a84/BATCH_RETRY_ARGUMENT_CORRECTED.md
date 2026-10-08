# Delayed delivery, retries, and the actual controller projection

This additive note records the final increment after actual-batch-v2. No earlier scientific source or frozen argument is rewritten.

## A failed batch can consume the proposed envelopes

The native actor receives the authentic raw-epoch-3 repair certificate before the honest roots receive it. Its stored proposal admission succeeds, but the live roots still hold their old installation policies. The actual `runBatch` therefore lands zero times. Nevertheless, its unconditional `cancelWith` calls record durable full-envelope tombstones for the generated repair trials (nonces 5 through 8 in this two-batch sequence).

Delivering the authentic certificate then restores live local policy admission but leaves those cancellation memories intact. Calling `runBatch` again with the same actor and same repair action regenerates the same complete envelopes. The kernel-checked `same_actor_retry_still_zero` result shows that this retry also lands zero times and leaves the installed plant unchanged.

The operational distinction is exact: `runBatch` returns a World and records, not an updated Actor. Its within-batch nonce increments do not change the actor supplied by the caller to a later invocation. A caller retry must supply genuinely fresh complete envelopes relative to the durable memories; successful policy delivery is insufficient by itself.

## Fresh envelope identity, not a global nonce law

The source-only recovery control supplies an actor whose nonce is 8, so the four new trials use 9 through 12. The sufficient high-water premise used by the conservative recovery proof is derived from the preceding exact batches and preserved through delivery. `fresh_retry_completes_once` proves one landing and the exact repaired plant.

A second control keeps the old actor nonce 4 and changes the admitted complete repair command's leaseEnd from 90 to 91, still inside the same source grant's endpoint 100 and at the same actual annotation 2. The predicted envelopes have the old nonce values 5 through 8 but differ in the complete action. `renewed_repair_exact_ready` verifies their absence from cancellation memory, and `same_nonce_changed_command_completes` proves one landing and the exact repaired plant. The old conservative high-water predicate remains false.

This is a mathematical alternate-command control using the unchanged source functions, not an implemented renewal service or permission to alter a real authorization. It proves why global nonce increase is not a necessary condition. The theorem's actual boundary is the explicitly stated absence of the new complete action/successor/nonce/path envelopes. Even absence of all four is only sufficient, not necessary: a blocked trial on a withholding-faulty path can coexist with successful completion on another intact path.

## Exact source-controller provenance

`provenance/BatchTests.lean` is a byte-for-byte copy of the accepted composition test source, SHA256 `12b365143d21b350d99048b06225bb64bc527990e302854dc3c901d224a89bcd`. `CONTROLLER_SOURCE_BINDING.json` binds its accepted location and the imported Composition/Fixtures/source identities.

`BatchControllerProjection.batchTestsPureProjection` reproduces the source's let-bound sequence: original actor and world, actual installation batch, predicted installed actor observation with nonce 4, authentic repair transition, certificate `getD` fallback, actor receipt, delivery and actual repair batch. It excludes only the IO assertions and the outer loop over test fault sets. The theorem `native_is_exact_controller_projection` proves equality to the new native witness for the pinned complete source and bad root 0 by definitional proof. `exact_source_projection_completes` transports the actual repaired-plant/one-landing result to that projection.

This binds the concrete witness to the cited source controller without claiming a theorem about the entire IO test runner, source-file interpretation, physical message delivery, global nonce allocation, actor knowledge, or asynchronous progress.
