# Exact initial-state characterization of the actual batch

This final scientific increment is additive to independently accepted actual-batch-v3. It changes no earlier proof, service function or actor interface. The earlier sufficient freshness results remain valid and unchanged.

## Exact theorem and hypotheses

`runBatch_survival_iff` characterizes the unchanged source `runBatch` with n=4 and q=3. Its explicit hypotheses are:

1. The actor's stored plant, full policy and stored time admit the fixed action to one predicted complete successor through the actual `localStep`.
2. The actual starting plant, full effective policy and actual annotation separately admit that same action to that same complete successor.
3. The requester is the action's actor. Every bounded good root has the full effective policy and has not revoked the action's epoch.

Under precisely these stable source-model obligations, the actual batch has exactly one landing **if and only if** at least one of its four predicted complete envelopes has:

- only actually good roots on its selected ordered path, and
- no preexisting tombstone for that exact complete envelope at any of those selected roots.

There is no fault-cardinality hypothesis in this characterization. For a world with too few intact roots, its right-hand side is false. There is also no global nonce high-water requirement, no demand that all four prospective envelopes remain uncancelled, and no requirement concerning a tombstone at an unselected root.

`runBatch_survival_effect_iff` includes equality of the entire final plant to the predicted successor. `runBatch_zero_iff_no_surviving_trial` characterizes zero landings by failure of the same initial-state condition. Unconditional source-specific at-most-once behavior from v1 supplies the exact count.

The predicate `HasSurvivingTrial` is proof-side mathematical information about the supplied initial world. It is not an Actor field, a proposal input, a path selector or an observation oracle. The real source still visits the same four paths in its fixed order and does not stop after a success receipt. None of these theorems tells an actor which roots are good, which tombstones exist, or how to obtain such information.

## Why necessity and sufficiency hold

Necessity uses the literal source's `badOpen=false`: every selected gate of an actually successful attempt must be good. Each of those live gates rejects its exact tombstones. Preparation never changes cancellation memory; attempts change only the plant; and cleanup can only add tombstones. Therefore absence at the successful trial implies absence in the original state at every selected root. The argument includes all prior failed-trial cleanup and does not infer a clean memory from a false reply.

For sufficiency, if an earlier trial lands, the desired positive outcome is already established while the actual fold continues. Otherwise the plant remains unchanged and the live admission/policy obligations persist. Cleanup of an earlier failed trial cannot cancel the chosen later complete envelope: the source generates distinct increasing nonces within this invocation. Thus a surviving later path remains intact and uncancelled until its turn; actual preparation then commits it at every selected root and the actual attempt lands. This is a proof about the literal service calls, not an assumed gate outcome or hypothetical early-stop implementation.

Actual selected-root memory is the relevant state, not a successful cancellation Boolean or common certificate alone. A false aggregate cancellation return can already have written a selected honest tombstone. Such a partial write makes that exact trial unavailable; this is fully retained by the characterization and independently challenged by source-generated false singleton-ack cancellation controls.

## Native and adversarial controls

The new source controls retain the exact native 3013-byte source.

- Cancelling the first prospective installation envelope on [0,1,2] in the bad-root-0 setup violates all-four freshness but does not prevent the actual batch from landing once on [1,2,3]. The iff now proves this directly.
- Cancelling the fourth prospective envelope eliminates the unique all-good source path and the actual batch has zero landings with the full original plant unchanged.
- The accepted delayed-delivery retry world has no surviving old trial; the fresh retry has one. These conclusions follow from the exact iff and the already checked concrete effects.
- Before root-policy delivery, an intact uncancelled repair trial exists, yet the actual batch stalls because the good-root policies are not synchronized. This proves the policy/admission hypotheses cannot simply be dropped from the iff.
- A tombstone placed only at an unselected good root does not veto the trial. This final test is expressly an arbitrary raw-World coordinate test, not a claim of lifecycle reachability: the unchanged `cancelWith` cannot create that unselected honest-root tombstone.

The independent reviewer separately supplies genuinely reachable partial-cancellation controls. Neither source flags nor cancellation receipts are treated as evidence that an actor knows the actual fault map.

## Final scope boundary

This closes the finite, stable, source-specific batch characterization. It does not turn the proof-side condition into an implementable observation procedure. Policy issuance, real identity authentication, authentic clocks/observations, external nonce allocation, service latency, asynchronous/interleaved or unbounded controller behavior, shared-alias lifecycle composition and physical/semantic warrant remain outside the theorem.

The all-good-path necessity is specific to the unchanged controller's withholding flag. It is not generalized to a controller that opens faulty execution gates. The separate full alignment/history safety theorem remains subject to its own authentic-source and fault-bound assumptions; this sharper source-semantics iff does not erase or replace those conditions.
