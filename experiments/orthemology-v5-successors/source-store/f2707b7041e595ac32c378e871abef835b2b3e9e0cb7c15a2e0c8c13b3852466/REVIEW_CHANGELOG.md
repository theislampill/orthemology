# v1 review and v2 corrective scope

The immutable author v1 snapshot has manifest SHA-256
`7c60a02b75ded4f90f50d526e184da02ab43f98758faf43319d4459cc2a8cfc0`.
It remains preserved separately. This portable v2 checkpoint contains the
following corrections and awaits independent v2 replay/review.

1. A withheld tainted path was not guaranteed to terminate merely because an
   intact path finishes. v2 adds a charged B+1 selected-root cancellation
   certificate, independently reachable authenticated per-root control ports,
   lasting full-command tombstones, and preparation/execution/cancellation
   phases. The same q>=2B+1 inequality supplies cancellation availability.
   This is a disclosed stronger mechanism/interface premise, not a claim that
   the original v1 liveness argument had already proved termination.
2. Cancellation must bind the exact command/recipient/path/unique nonce. The
   original recipient's cleanup right and authenticated request are explicit.
   Foreign actors cannot cancel or execute its command. Landing before close
   remains a valid idempotent repair; after close that nonce cannot land, while
   a fresh nonce stays usable. Corrupt roots can mimic intact cancellation
   acknowledgements, preserving the opaque-search lower-bound transcript.
3. The finite horizon must contain enough remaining authorized phase slots.
   N counts newly initiated final-descriptor macro-attempts after stable
   certificate delivery; old in-flight work may need to finish cancellation
   first. 3N logical phases do not claim physical wall-clock time or erase that
   residual delay.
4. A v1 sentence overstated fixed R5 as already realizing every new mechanism.
   v2 says only that no defeat is established and no unification bridge is
   consumed; stronger interlocks and reservation premises are not retroactively
   admitted R5 resources.
5. Before the v1 freeze, parent review removed an implicit global-descriptor
   feed to the actor. Actor-local certificate custody and identity now govern
   its commands; stale knowledge safely fails, and current knowledge does not
   rename one recipient into another.

No general quorum arithmetic or covering-number error has been reported in
the review messages so far. That observation is not a final review acceptance.
