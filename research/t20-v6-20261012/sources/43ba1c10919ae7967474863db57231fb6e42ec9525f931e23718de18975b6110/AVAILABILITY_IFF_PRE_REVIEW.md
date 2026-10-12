# Source-first criteria for the optional availability iff

This is an independent pre-proof specification for the separately authorized
iff increment. It changes no accepted v1/v3 source or review. No new iff proof
has been inspected at this point.

## Intended precise statement

Keep the literal unchanged four-path `runBatch`, with n=4 and q=3. Fix an action
and successor such that the actor's stored localStep and the actual initial
plant/full-effective-policy/time localStep both return that same successor.
Require the actor identity to equal the action actor and every bounded intact
root to hold the full effective policy and not revoke that action's epoch.

For each exact envelope predicted from action/successor/actor.nonce and the
ordered path position, availability is:

- Every selected root is actually untainted.
- That complete envelope is absent from every selected root's initial cancelled
  list.

Under those explicit stable conditions, positive actual landing count should
be equivalent to existence of one available predicted envelope. The right-hand
side must examine the original world, not an assumed successful intermediate
state. Selected-root freshness is enough; no global high-water bound, all-four
freshness premise, or fault-cardinality bound is appropriate for this iff.

This is a proof-side characterization. It must neither pass the available path
to the actor nor change the actor/propose/runBatch interfaces or portfolio.
The already accepted fixed-withholding uniqueness theorem then gives exactly
one landing, and the same-successor theorem gives full final plant equality.

## Necessary proof controls

Necessity must extract a real successful trial, use hard-coded badOpen=false
to show every selected gate is intact, and transport initial tombstones forward
through all earlier actual preparations/attempts/cancellations. An old selected
tombstone would still veto the successful live gate. The current recorded
envelope must be identified with its exact predicted value, including nonce
and ordered path.

Sufficiency may use an earlier actual landing to finish the logical existence
argument, but must not add early-stop behavior to the executable fold. If earlier
trials fail, their plant effects are identity while partial commitments and
cleanup still occur. Readiness and the chosen later envelope's availability
must survive these effects. Distinct generated nonces prevent the current
cancellation from cancelling that later complete envelope.

Do not replace tombstone absence by a true cancellation Boolean or abstract
certificate. Even a false singleton cancellation at an intact selected root
can veto an individual exact trial. Conversely, a tombstone stored at an
unselected root is irrelevant to that envelope's live path.

## Independent source controls queued

`BatchAvailabilityIffSourceChallenges.lean` starts from zero faults and performs
four genuine singleton-ack cancellations, one for each prospective envelope.
All four preliminary replies are false at B=1, but their actual selected-root
tombstones block every trial. The control separately derives aligned
reachability from the actual permitted cancellation history. This is an
admission/memory obstruction, not an expired grant or consumed version.

Existing independently compiled controls establish a cancelled faulty first
trial coexisting with successful intact fourth trial, a cancelled unique intact
fourth trial causing failure, no all-good path with two faults, and unrelated
higher-nonce tombstones coexisting with progress. New type-checked applications
will compare the exact iff predicate to those controls after freezing.

An unselected intact-root tombstone produced by raw World record update is a
valid semantics-only coordinate control, but is not thereby a reached actual
cancellation state: cancelWith explicitly restricts acknowledgers to the
envelope's own path. Any reachability claim for such a case needs a real history.

The iff remains conditional on stable actor/live admission, owner identity,
full root policy coherence and unrevoked epoch. It is not unconditional liveness,
physical availability, actor knowledge, arbitrary fault-strategy progress,
asynchronous service scheduling, or shared-alias lifecycle composition.
