# Reading the bounded operational correspondence

All theorem names below are exact source identifiers. The source files and
independent reviews, rather than this index, determine their complete statements.

## Common kernel and exact original specialisation

- `JoinModel.lean`: the parametric local admission/effect interface, full command
  memories, state, events and primitive transition functions. The interface asks
  only for admitted epoch/requester facts. It assumes no desired plant safety or
  goal conclusion.
- `JoinInvariant.lean`, `JoinSafety.lean`, `JoinTrace.lean`: authentic full-policy
  identity, arbitrary finite-history currentness, durable full-command
  cancellation and a separately discharged goal-preservation rule.
- `OriginalTranslation.lean`: exact original-state inverse maps and
  `trace_iff_lift_exists`. Every original event is covered; original timestamps
  are absent and introduced common annotations are erased. Damaged and otherwise
  unreachable states are covered by the local successor correspondence.

## Typed effects and the deliberately limited core relation

- `TypedInstantiation.lean`: the bounded subtype retains the entire ordered
  envelope, including its full successor and nonce. Path membership is projected
  to a finite set only after proving bounds and no duplicates. `root_gate_iff`
  and `successful_attempt_exact_effect` tie the generic gate/effect to exact
  imported runtime definitions. Malformed paths are outside this subtype;
  aggregate wrong-quorum paths retain their specified identity branch.
- The original `RuntimeRepresents` snapshot relation does not bind the runtime's
  effective policy or certificate history. Later lifecycle claims use the
  separate stronger `Aligned` relation; they are not silently inferred from this
  weaker core relation.
- `TypedHistoryProperties.lean` and `OffsetHistoryProperties.lean`: exact custody,
  four audit quantities and fixed-action exclusion over finite histories. A fresh
  valid installation can increment history even if the chosen rule is unchanged.

## Raw epochs, authentic lifecycle and exact aggregate effects

- `EpochOffset.lean`: the raw base is explicit. Raw command, grant and policy
  fields are never renumbered. Commands below the base remain in the universe
  and are rejected from honest stored-policy admission; a truncated natural-number
  index does not make them valid.
- `LifecycleModel.lean`: `Aligned` and complete sound/complete certificate
  provenance. `initial_aligned` covers the explicit post-boundary initial class,
  not an invented earlier history.
- `LifecycleCertification.lean`: actual `certifyTransition` requires the full
  next policy to equal the authoritative source value for simulation. Its
  numerical epoch-shape check alone does not establish authenticity.
- `LifecycleDelivery.lean`: recorded delivery preserves alignment, including
  repetition; unrecorded calls are exact identities. Primitive delivery events
  selected in the simulation respect the actual untainted-root update behaviour.
- `LifecyclePreparation.lean`: exact aggregate preparation and partial stored
  commitments. The shared `badSign` Boolean is retained.
- `LifecycleAttempt.lean`: successful attempt has the exact whole-world plant
  update; rejected attempt is an identity. The shared `badOpen` Boolean is retained.
- `RuntimeTrace.lean`: `runtime_trace_refines_history` and
  `reached_runtime_current_admission` cover the explicitly defined actual-call
  class. They do not claim whole runBatch refinement.

## Aggregate cancellation

- `LifecycleCancellation.lean`: `cancelWith_preserves_alignment` and
  `true_cancel_implies_certificate`. Reply counts in the current call differ from
  cumulative distinct common acknowledgements. A false reply can retain a good
  tombstone; repeated calls can duplicate actual list entries.
- `RuntimeCancellationTrace.lean`:
  `runtime_cancel_trace_refines_history` and
  `true_runtime_cancel_blocks_all_continuations`. The latter rejects the exact
  full envelope after every continuation in that enlarged actual-call class.
  Changing nonce, path order, lease or other command fields creates a different
  identity. Cancellation has no invented badSign/badOpen control parameter.

## New monotone reference-clock class

- `ReferenceClock.lean`: `setReferenceTime_aligned` is unrestricted structural
  preservation. `localStep_before_lease_end` follows from the exact installation
  and repair grant predicates. `expired_localStep_is_none` is a local exact-result
  theorem; `expired_aligned_attempt_rejected` transports it to aligned reachable
  runtime snapshots.
- `MonotoneReferenceTrace.lean`:
  `monotone_reference_trace_refines_history`,
  `reached_monotone_reference_current_admission`,
  `expired_envelope_stays_rejected`, and
  `true_cancel_blocks_monotone_reference_continuations` cover the separately
  named class with NEW reference time updates. This class permits stalling and
  unbounded forward jumps. Actor `observedTime` is never refreshed by those events.
- `ReferenceClockControls.lean` and the independent `ReferenceClockV6Challenges`
  demonstrate strict lease boundaries, legitimate fresh renewal, genuine aligned
  rollback resurrection outside the monotone class, persistent tombstones and
  partial dishonest preparation after expiry.

The approved source input and all portable proof materials are evidence of these
bounded mathematical statements. They supply no independent authority for real
permissions, physical clocks or foundational N2/T0/R5 conclusions.
