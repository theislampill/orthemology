# Actual batch successor: native controller and precise freshness

This additive successor preserves all 68 bound files of actual-batch-v1 exactly. The frozen v1 argument remains a historical scope statement; the new results below resolve its pending native aggregate witness and sharpen its sufficient freshness assumption. No imported service, actor, policy, envelope or accepted proof is changed.

## Stronger aggregate safety endpoint

`BatchAdmission.runBatch_landing_admitted` needs only the accepted initial alignment/reachability, an arbitrary actor/action, and a positive actual batch landing count. It derives that the action's raw epoch is the original world's effective raw epoch, and constructs a successor such that the exact `localStep` admits the action from the original full plant, full effective policy and actual time; the entire final batch plant equals that successor. Thus success is not only safe at a hypothetical later query. The actual aggregate change itself is source-current and exact. This is a safety implication, not an existence claim.

The proof traces actual preparation to an aligned reachable intermediate world, applies the existing live-attempt admission theorem, and follows the literal fold. Before the first landing, the actual plant is unchanged; policy and time remain unchanged throughout the batch. Every proposed action is the same fixed action. No actor observation is promoted to trusted evidence.

## Cleanup classification

`serviceTrial_closes` proves that a proposed trial's actual `cancelWith` reply is true for the correct requester, a valid three-root path, and budget 1. The source's full-path cancellation gets all three modeled responses for its rightful owner. This is separate from effect progress: the stable completion theorem does not require world.budget=1, and a world with a larger cancellation threshold can land while failing the current-call cleanup threshold.

`runBatch_records_closed` then proves all four log records are closed for the correct owner at n=4, q=3, budget=1. Proposal rejection still creates a synthetic closed record with no cancellation call. The theorem does not reinterpret that record as a certificate. As before, converting a genuine true cleanup reply into durable exclusion uses the accepted aligned/reachable fault-bound premises.

## Sharper sufficient freshness

`trialEnvelopes` predicts the four complete envelope values using only the action, predicted successor, initial actor nonce and fixed ordered paths. The list is explicitly proved equal to nonce+1/[0,1,2], nonce+2/[0,1,3], nonce+3/[0,2,3], nonce+4/[1,2,3], preserving complete action/successor/path identity.

`ExactReady` retains v1's requester, actual full-policy admission, synchronized good-root full policies, and absence of action-epoch revocation. It replaces the conservative nonce high-water requirement with absence of precisely these four complete envelopes from bounded good-root cancellation memories. The actor-observed `localStep` obligation remains separate. `runBatch_exact_fresh_completion` proves exactly one actual landing and the entire predicted successor under these conditions and the same n=4, q=3, at-most-one-fault count.

This is strictly less restrictive than the v1 high-water premise. The kernel-checked exact-source control stores a prior tombstone with nonce 99 at every root while the actor starts at nonce 0. High-water is false. The four predicted envelopes are nevertheless absent, and the new theorem proves the actual batch completes once. No hidden memory is read by the actor; these remain explicit world-side premises. `ready_implies_exactReady` formally derives the sharper premise from the old sufficient one, so v1 is retained as a convenient conservative corollary.

Neither freshness predicate is claimed necessary or minimal. In particular, cancelling a prospective trial whose path includes the withholding faulty root may still permit a different, intact uncancelled trial to land. A condition sufficient for all four trials to remain eligible is stronger than a necessary condition for one landing.

## Exact native two-batch controller

`BatchNative` uses the same fixed actor and pure call sequence as the accepted native `BatchTests`: the full pinned 3013-byte source; installation at raw epoch 2; all four installation paths; the predicted installed observation and nonce 4; actual `certifyTransition` with ordered acknowledgers [0,1,2] and authentic source policy at raw epoch 3; actual `deliver`; actual `receiveActor`; and all four repair paths.

`native_certificate_exact` proves that the certificate was actually returned by source certification. `native_actor_receives_full_policy` proves the exact actor update. `native_full_batch_runtime_trace` constructs a finite accepted actual-operation history for both complete batches plus certification and delivery. `native_full_batch_common_history` derives the common primitive history and full final alignment. This is a theorem about those pure source operations and their actual composition, not the surrounding IO test runner, artifact writer, or an unimplemented observation service.

Both batches land exactly once, record exactly four closed trials, and the final entire plant equals the established `repaired` record. `native_full_plant_and_audits` retains the full original source and custody, exact rule, byte-for-byte draft, rule version 4, draft revision 9, rule history [.normalizedLF] and draft history [[88], sourceBytes ++ [10]]. The first batch's bounded cancellation high-water is derived and preserved by certification/delivery before the second batch; it is not recomputed by reading hidden root memories.

The accepted native setup has fixed bad root 0. The generic completion theorem handles every actual four-root taint function of cardinality at most one without passing the good-path witness to the controller. The concrete witness does not by itself prove an unknown-map or shared-alias strategy.

## Native boundary controls

At actual reference annotation 90, the same stored actor observation 2 still creates installation proposals but every actual landing is blocked; cleanup memory is nonempty and the whole plant stays unchanged. With actor observation 0 and actual annotation 2, proposals fail and the four closed records are synthetic, while root cancellation memory stays empty. These controls preserve the pinned complete source. They supplement the independent reviewer's direct-source and reached-history adversarial controls.

## Remaining boundaries

The complete four-trial function is now covered by common history refinement, actual aggregate admission, unconditional uniqueness and explicit stable-state completion. What remains open is not hidden inside the new theorem: physical or asynchronous service completion, authentic clocks and observation-refresh service, nonce allocation in an interfering environment, authority issuance, arbitrary interleavings or unbounded controller loops, shared-alias lifecycle composition, and deployment/semantic warrant. The numeric clock is unchanged inside each actual batch. No real elapsed-time deadline or fault-map/alias-map knowledge follows.
