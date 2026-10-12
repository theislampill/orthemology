# Interface and quantifier ledger

Sources are cited as exact ZIP filenames followed by `::` and the verified member name. `SOURCE_IDENTITY_MAP.json` records archive/member SHA-256 values and declaration line anchors. The common and alias packets are separately accepted source objects, not one new composed implementation.

## 1. Shared exact source and complete command

`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::imports/Composition.lean`:75 defines `ComposedExecution.localStep (plant) (full policy) (now : Nat) (action) : Option Plant`. Both typed lanes retain that exact function. `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::TypedInstantiation.lean`:11–52 supplies `BoundedEnvelope n`, the complete duplicate-free in-range **ordered** raw path, finite-set path projection, raw-epoch typed interface, actor and entire successor. Its effect is the full envelope successor, not a target-only update. The common ZIP's `TypedInstantiation.lean` and `imports/Composition.lean` are byte-identical to `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/imports/common/TypedInstantiation.lean` and `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/imports/common/Composition.lean`, respectively. The accepted typed predecessor manifest is retained at `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/provenance/accepted-typed-history-v2/MANIFEST.json`. Memory-list membership representation does not quotient the envelope by nonce, path support or visible payload. `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasRuntime.lean` `rawRoot` preserves full-command membership.

## 2. Epoch and source quantifiers

Common offset interface `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::EpochOffset.lean`:13 uses proof indices `policy.epoch − base` and `action.epoch − base`; `Authority.raw_epoch` requires every authentic source policy's raw epoch to be `base + index`. Actual Policy, Grant, Action and Envelope fields are unchanged. A command below base remains in the universe but is rejected by the exact raw gate. The native example has raw base 2, then raw epoch 3; it does not certify pre-base history.

Alias typed code specializes `OperationalJoin.Typed.interface m`, not the offset interface. `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasModel.lean` `Environment.source_epoch` requires raw source epoch e; `initial` starts at 0. Its installation witness is raw epoch 0 using the compact three-byte source. The generic alias theorem is not restricted to that witness, but it does not import or prove raw2-to3 offset lifecycle transport.

## 3. Two different state relations

`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::LifecycleModel.lean` `Aligned` fixes n, budget, q, r, entire plant, full `effectivePolicy = source s.epoch`, taint at all bounded roots, exact root-policy and memory membership, idle macro boundary, and `CertificatesAligned`. The latter binds soundness/completeness and unique previous epochs of the full recorded runtime certificate list. `CertificateAt` retains the full source policy and original ordered distinct bounded acknowledger list, while its common set tracks membership. Equal policy epoch alone is insufficient.

`Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasRelation.lean` `Refines` equates epoch, pending, receipt sets, certificate and cancellation-receipt functions, entire plant, and derives abstract non-damage. At good labels `RootRefines` equates descriptors, masks commitments by that label's command selection, and requires **abstract veto sets ⊆ concrete veto sets**. Faulty stores are unconstrained. Concrete landing implies abstract landing; the converse need not hold. Literal shared-store copying can violate common selected-memory reachability.

## 4. Event and history quantifiers

Common `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::RuntimeTrace.lean` includes actual `prepare`, `attempt`, source-authentic well-shaped `certifyTransition`, and recorded/unrecorded `deliver`; `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::RuntimeCancellationTrace.lean` adds actual `cancelWith`, including false partial outcomes. Theorems quantify over every finite trace of the named language from an aligned world and reachable common state. They construct a valid common primitive trace and final full alignment. They are forward simulations, not all-service or converse refinements.

Alias `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasModel.lean` `Step` has ten explicit shared-model events, including fixed-bad-root corruption. `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasSimulation.lean` `step_simulation`, `trace_simulation` and `initial_trace_simulation` quantify over every lawful finite concrete trace. A step expands to a finite common list or stutters. The complete ordered landing list (full command, requester, numerical time) is equal. Preparation expands selected aliases, delivery the full fiber; neither expansion invents receipts. This is not equality of transcripts, hidden-map observations or event counts.

## 5. Map, faults and threshold quantifiers

Common `Authority` fixes one lifetime faulty subset of `Fin n`, cardinality ≤ B, with n+B < q+r, q+B ≤ n, r+B ≤ n and B<n. Native n=4, B=1, q=r=3 and intact [1,2,3] are an existence witness, not a discovery strategy.

Alias `Environment` fixes for the whole trace one nonempty class A and canonical `rootMap A`: labels in A map to `none`; other labels to `some i`. Actual faults are a fixed subset of the map image, of size ≤ B; B≥1 and B<m−|A|+1. The proved label bound is k=B+|A|−1, with m+k<q+r, q+k≤m, r+k≤m. The theorem is parameterized by every environment satisfying these fields, but constructs no controller uniform in an unknown map and no observation secrecy. The witness is m=7, A={0,1}, faulty actual singleton 6, B=1, k=2, q=r=5.

## 6. Gate snapshot and Boolean scope

`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::imports/Composition.lean`:288 `attempt` checks valid path and all live local gates, then installs the complete successor or returns exact World identity. It does not read `effectivePolicy` or completed certificates. One shared `badOpen` Boolean controls all faulty gates.

`Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasRuntime.lean` `gateWorld` sets m labels, budget k, pulled-back taints/shared stores, actual concrete plant and supplied time, `effectivePolicy := E.source C.epoch`, and `completed := []`. `gateWorld_represents` proves only typed `RuntimeRepresents` against `literalSnapshot`, **not** offset `Aligned` and not reachability of that snapshot. `compiled_success_lands` works for either Boolean; `compiled_attempt_iff` is an iff only when that Boolean is true. False may additionally withhold. Reachable current-policy admission is obtained separately via the weak witness. No unchanged preparation, cancellation or certification storage macro is implemented by this snapshot construction.

## 7. Receipts and cancellation

Common source `cancelWith` (`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::imports/Composition.lean`:325) first checks path, distinct selected supplied addresses, then filters this call's responders by taint-or-requester-equality. Intact matching replies store the whole-envelope tombstone; bad replies need not. Its Boolean counts this call's distinct responders against B+1. `true_cancel_implies_certificate` (`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::LifecycleCancellation.lean`:174) embeds them into the accumulated common set. False can retain partial vetoes or coexist with a cumulative certificate; no converse follows. Repeated source tombstones can append even though abstract receipts deduplicate. `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::MonotoneReferenceTrace.lean` transports true-call exclusion for the exact same envelope over every allowed finite continuation, requester and shared Boolean.

Alias `acknowledge`/`cancelAck` update the shared veto store but insert only the actually addressed label receipt. `complete` requires exactly r accumulated distinct label receipts; `close` requires more than k. `cancellation_persists` starts from that cumulative k+1-label certificate and covers arbitrary lawful finite continuations, later times and requesters. The independent typed reviewer additionally derives false source attempts for either Boolean. The fixture receipts are exactly {0,2,3}; alias 1 shares a veto without becoming a reply. There is no alias aggregate-cancellation Boolean/certificate equivalence.

## 8. Clock scope and derived-only alias expiry

Common v4/v5 actual macro traces keep `World.now` constant. `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::ReferenceClock.lean` `setReferenceTime` is a **new reference operation** changing only that annotation. Structural `Aligned` is preserved even by rollback. `Eighth_Operational_Model_Checkpoint_v6_dist4.zip::MonotoneReferenceTrace.lean` adds advances with `w.now ≤ now`; the finite theorem derives numerical monotonicity. It allows stalling and unbounded forward jumps, does not refresh actor observations, and proves no physical clock or progress service.

Alias state contains no clock coordinate or clock-advance constructor. Numerical time is an argument to preparation/landing and the gate snapshot, with no cross-event monotonicity premise.

A valid ordinary logical consequence is nevertheless available. Fix any `E : Environment (Typed.interface m)`, any reachable shared state C, any bounded full envelope e, requester, time t and Boolean b. If the source attempt on `gateWorld E C t` returns true, `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasRuntime.lean` `compiled_success_exact_effect` gives:

`localStep C.plant (E.source C.epoch) t e.val.action = some e.val.successor`.

`Eighth_Operational_Model_Checkpoint_v6_dist4.zip::ReferenceClock.lean` `localStep_before_lease_end` quantifies over **arbitrary** plant, policy, time, action and successor, with no offset, alignment or reference-trace premise. Applying it to precisely those values yields `t < actionLeaseEnd e.val.action`. Hence `actionLeaseEnd e.val.action ≤ t` contradicts successful admission (and the Boolean is false). `Eighth_Shared_Root_Safety_Source_Only_v3.zip::Eighth_Shared_Root_Safety/science/AliasTyped.lean` `finite_history_admission` gives the same conclusion directly for concrete `Lands`.

This uses identical `localStep` source bytes. No new named theorem was compiled. It can be applied at each later reachable alias state when the separately supplied queried time satisfies the lease-end inequality; it does not make expiry irreversible under arbitrary decreasing query times or equip aliases with common-v6 monotone time.

## 9. Semantic decoder boundary

The accepted semantic `Semantic_Control_Independent_Review_20261002.zip::CORE_REVIEW.md`, `Semantic_Control_Independent_Review_20261002.zip::EXTRACTED_MUTANT_HEADER.txt` and `Semantic_Control_Independent_Review_20261002.zip::ExactStatementReview.lean` bind the refuted mixed statement. Its implementation certificate belongs to the executed old policy, while a separate computed-policy decoder reconstructs history from physical receipts. Positive measurable failure concerns that reconstruction. The same witness's old-program/old-decoder history satisfies parity on every tape; the computed/computed positive result remains intact. Neither physical old-controller failure nor a universal physical deployment theorem follows. These semantic results do not supply a missing common/alias runtime bridge.
