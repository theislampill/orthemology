# Actual four-trial batch refinement and bounded completion

## What genuinely closes

The accepted common-v6 report explicitly excluded the actual `runBatch`. This extension connects that exact imported function, without changing it, to the already accepted lifecycle model. `BatchSource.runBatch_eq_fold` is definitional equality to the imported fold body. `BatchExtraction.runBatch_runtime_trace` constructs a finite `RuntimeWithCancellationTrace` for the actual aggregate output, for every actor and action. It retains preparation's partial effects, skips the attempt exactly when preparation returns false, and performs actual cleanup even after failure. Proposal rejection is a zero-service-event branch.

`BatchSafety.runBatch_refines_history` therefore proves a genuine common primitive history and complete final `Aligned` relation for the aggregate function from an aligned reachable four-root world. This includes full plant, full current policy, roots and durable memories, thresholds, fixed taint and authentic completed-certificate provenance. It is not a renamed abstract trace assumption. Existing current-policy admission and durable exact-envelope cancellation transport across the aggregate output.

The aggregate's records have exactly four entries. Their ordered paths are the source's fixed `fourPaths`; nonces are actor.nonce+1 through actor.nonce+4. No effect receipt makes the controller stop early. A proposal-none record has `closed=true` without any cancellation call, so this Boolean alone is never promoted to a cancellation certificate.

## Unconditional uniqueness

`runBatch_at_most_one_landing` requires no alignment, authenticity, synchronization, or fault-budget hypothesis. It follows from the exact source choice `badOpen=false`: any landing on a nonempty path supplies an intact live gate and hence a real local transition. The imported fixed-action theorem uses the changed version/history state to exclude the same action from every later policy/time. Every batch trial retains the fixed action. Zero landings leave the full plant unchanged; one landing makes that action permanently non-admitting from the resulting plant, for this fixed source local-step semantics.

This does not prove that a landing exists. Withholding at every faulty gate is a restriction of this concrete controller, not a theorem about arbitrary Byzantine behavior.

## Separate bounded stable completion

`runBatch_stable_completion` proves exactly one actual landing and equality of the entire final plant to the predicted successor. Its premises are explicit:

- The actor's stored plant, full policy and stored observedTime admit the action to that successor under the actual `localStep`.
- The actual world's current plant, full effective policy and World.now separately admit the same action to the same successor.
- The requester is the action's actor. Every bounded good root holds that full current policy and has not revoked the action's epoch.
- The actual world has n=4 and q=3; `ChargedInterlock.card 4 tainted ≤ 1`.
- `FreshAbove w actor.nonce`: every preexisting cancelled complete envelope at bounded good roots has nonce at most the actor's initial nonce.

The last premise is a conservative sufficient high-water condition, stronger than absence of only the four prospective envelopes. It is not necessary. A higher-nonce unrelated tombstone can violate it without blocking the batch. Finite root memories have a mathematical maximum, but no theorem says an actor can discover that value or access hidden root memory. External nonce initialization/allocation remains a premise; unchanged `runBatch` does not establish global freshness.

`fourPaths_has_intact` derives a good portfolio member from the fault-cardinality bound. The actual controller always visits all four paths in the same order and never receives this witness or a fault-map input. If a prior trial did not land, preparation and cancellation preserve the remaining readiness obligations at the incremented high-water mark. When the intact path is visited, its actual preparation and live attempt succeed. All successful proposals share the same full predicted successor; the final plant equality retains exact rule/draft versions and audit histories.

The completion result is about one total, finite Lean function evaluation under a stable state. It is not a physical latency bound, evidence of real external service completion, an unbounded controller loop or general liveness theorem. `World.now` remains constant throughout the actual batch; authentic clock readings and elapsed time are not supplied.

## Source actor and authority boundaries

The actor's proposal still receives only its stored policy, observed plant, identity, observed time and nonce plus an action and path. It never receives the world, taint set, alias map or newer service clock. Separate proposal and live-admission premises permit an old observation that remains valid, but do not certify observation authenticity or give an observation-refresh operation.

No new policy is issued by a batch. A subsequent raw2-to3 installation/repair controller must still use authentic externally supplied policy issuance and source-bound certification/delivery. `receiveActor` checks certificate shape and increasing epoch, but cannot authenticate an arbitrary shape-correct certificate by itself. The predicted observation update in the accepted native fixture remains an explicit external assignment.

## Frozen core and remaining work

This scientific core compiles against Lean 4.19.0 and the exact accepted source dependencies. Its new theorem axiom closures use only standard Lean axioms. The core leaves the new full aggregate native raw2-to3 witness and additional controller/cleanup controls to the next reviewed increment; the accepted 3013-byte primitive witness remains copied without change. Independent direct-source reviewer challenges already exercise synthetic closure, partial mutation, stale observations, prior cancellation, fault-budget failure and high-water non-necessity.

Still outside this result: alias-runtime lifecycle composition, observation secrecy or knowledge, physical deployment warrant, authentic clocks, general progress under interruptions/policy change, unknown-map adaptation and unbounded controller convergence. These are not inferred by adjoining the batch and shared-root results.
