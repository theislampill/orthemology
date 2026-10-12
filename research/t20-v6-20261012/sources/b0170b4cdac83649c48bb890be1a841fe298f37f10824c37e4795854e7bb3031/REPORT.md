# Independent review: posterior-deterministic checker kernel

## Bound object and verdict

The review object is the immutable `PD_Checker_Restriction_Formal_Candidate_1_20261001.zip`, SHA-256 `a7bc903469a362de66fe8012a616b01d526386c92bf6d5a94e82736620749f2c`, 22,092 bytes. Its manifest SHA-256 is `11619edcc659151ab0aeb1738396b9e180f0e24b3675ef7bc180aed1f49e42d3`. `CheckerKernel.lean` has SHA-256 `074270a22703df806c0615cb6ed17ad90de60e37a9d7e6dcefdcd2695e5a696c`.

**ACCEPTED: local construction and posterior-deterministic restriction preservation.** The mathematical source review, fresh six-source replay and nine additional reviewer probes find no defect in the claimed scope. All 33 selected axiom footprints are subsets of `propext`, `Classical.choice` and `Quot.sound`. Acceptance is limited to those precise claims; the frozen ordinary reduction is a referenced dependency for context, not a newly re-proved complexity result here.

## Actual transition contract

The source constructs an actual Mathlib PMF on receipt/successor pairs. `kernel_posterior_deterministic` proves its per-old-state, per-action, per-receipt unique positive successor property from the definitions. It does not take posterior determinism as a premise. It does not say that a mixed hidden belief has only one possible hidden state.

A live state carries `(index, stored symbol, nonterminal control, head)`, with both index and head in `Fin m`. An action carries a claimed read symbol and a Boolean branch request. The machine table maps control, claimed symbol and chosen branch to a written symbol, destination control and signed integer shift. The constructor:

1. Rejects a false claim precisely when the checker index equals the current head
2. Computes the signed next head and rejects negative or ≥ m results
3. Checks the destination control only after that bounds check
4. On a valid nonterminal step, keeps the checker index, changes its symbol only if it was at the head, and updates the shared control and head
5. Maps accepting and rejecting outcomes to the unique corresponding sinks

The order matters. An accepting instruction cannot bypass an invalid head movement, and a checked false read rejects before any proposed instruction can rescue it. Conversely, a false read is not rejected by every checker: an unchecked cell can survive it. The author’s local invariant and the independent countercontrol correctly retain that distinction; the eventual first-false-claim argument is outside the formal packet.

At existential controls the action’s branch request selects a point mass. At universal controls the request is ignored and one exact normalized fair Boolean PMF is pushed through the transition. The reviewer proves the generic action-branch irrelevance statement, rather than relying only on a fixture. All actions have a normalized row; there is no separate availability predicate.

The PMF type supplies normalization. The explicit mass lemmas also show that every entry is 0, 1/2 or 1, with duplicate contributions summed. The five receipts are ordinary, universal-false, universal-true, accept and reject. Distinct live universal outcomes receive distinct branch receipts. If both branches emit the same terminal receipt, they both go to its single sink. Therefore terminal merging preserves the required uniqueness property. A separate reviewer fixture checks the case in which one fair branch accepts and the other rejects, each with mass 1/2.

The generic restriction proof permits arbitrary alphabet/control carriers with the necessary symbol decidable equality. Finiteness is separately supplied for the finite instance. The state-cardinality theorem is exactly `m² |Γ| |Q| + 2`. This is a cardinality theorem, not a bit-cost or construction-time theorem. Arbitrary signed shifts are allowed by the typed machine interface; the bounds check remains valid for shifts larger than one cell.

## Unseen-index initial mixing

`initialBelief` is the pushforward of the actual uniform PMF on `Fin m` through the injective map taking each index to its own initial checker. Its support is proved to be exactly that family; every checker has mass 1/m and strictly positive mass; the finite total is one. The `Nonempty (Fin m)` instance expresses the positive tape-size requirement. Supplying an initial head of type `Fin m` also rules out an actual zero-cell initialization.

No transition from a known boot state chooses the hidden checker. The mixed initial law is an input to the model, so the per-transition PD property is not asked to perform an impossible hidden selection under one common receipt. The author’s normalized bad-boot counterkernel proves that inserting exactly such a transition would fail PD. The independent rational oracle reproduces this failure.

In the state-labelled lift every initial checker receives the same ordinary label. Erasing the lift recovers the original mixed belief as a PMF equality. The common-label observation law is a point mass, so the initial observation does not expose the checker index. A reviewer lemma packages all three facts: positive mass at every index, exact erasure and the common label.

## Joint-kernel to deterministic-state-observation lift

The lift has three possible last receipts on live states, and one accepting and one rejecting sink. Its cardinality is exactly `3m² |Γ| |Q| + 2`, and the stated at-most-fivefold bound follows. The previous last-receipt field does not influence the next transition; the reviewer proves this directly.

`copyOutcome` is deliberately total on inconsistent receipt/state pairs, but `kernel_support_valid` proves that every positive-mass actual outcome is consistent. The proof of `observe_copy` requires that validity hypothesis. It is then applied only on the support to derive the exact PMF identity

    map (next label, erased next state) (lifted row) = original joint row.

The fallback is therefore unreachable from every actual source row, including rows from arbitrary old states. It is not used as an unrestricted observation-preservation axiom. The reviewer proves a concrete inconsistent accepting/live pair whose fallback changes the receipt, so removing the support-validity condition is explicitly falsified.

`lifted_kernel_posterior_deterministic` derives state-labelled uniqueness from the constructed source row and the support-validity/erasure identities. It has no PD premise supplied by a caller. Acceptance is globally visible: the accepting observation occurs exactly at the unique top state, and that state is absorbing under every action. The reviewer additionally verifies the corresponding visibility and absorption properties for the rejecting sink.

The exact *one-step row identity* is proved. A complete path-law, belief-update or strategy-transport theorem is not present and is not credited implicitly by this review. The initial-lift equalities and row identity are appropriate ingredients for such a future theorem, but they are not themselves that theorem.

## Honest-step invariants

`honest_running_step` has the appropriate local hypotheses: the claimed symbol is the actual tape symbol at the head, the selected machine transition has a valid checked head, and its next control is nonterminal. Under those conditions, each checker becomes the same coordinate of the updated complete tape, with the same next control and head. This is a direct one-step statement, not an assumed global simulation relation.

`honest_branch_receipt` and `honest_receipt_law` prove equality of actual public receipt PMFs across checker indices for a truthful step. They include both invalid bounds and terminal merging; no live branch identifier is needed once a terminal state has been reached. These lemmas do not yet establish equal posteriors after an arbitrary policy history, or a first-false-claim impossibility argument.

## Independent evidence and countercontrols

The author archive is digest-checked, extracted to a separate source-reference tree, and its six sources are replayed into a newly absent output directory using the exact pinned Lean 4.19.0 binary, Mathlib revision, official package revisions and official object search paths. No author custom `.olean` is used in the independent cold replay. The restored official upstream objects remain trusted; this is not a complete fresh upstream bootstrap.

Shared-host contention delayed the cold replay, which was left running and completed successfully. The reviewer probes were then compiled against only the objects from that successful independent fresh build. No redundant second whole replay was launched under the high load, and no author development object was substituted. The source-only portable verifier supports a future complete replay with `--lean`.

`CheckerContractProbe.lean` adds nine selected theorem footprints: universal-branch request irrelevance, old-copy label irrelevance, rejecting visibility, rejecting absorption, pointwise joint-row readback, hidden initial mixing, invalid-copy countercontrol, split terminal half-masses and survival of an unchecked false read. It also checks large positive and negative out-of-bounds accepting moves.

The independent Python oracle imports no author routines. It compares two separately structured transition evaluators and checks normalized rational rows, allowed probabilities, PD, preserved checker indices, exact lifted row reconstruction and state-labelled PD. It covers 100,800 complete local rows and 28,800 truthful checker-index pairs, with 931,318 exact assertions. Six negative controls cover a hidden boot choice, suppressed branch receipts, invalid copy pairs, revealed initial labels, out-of-bounds acceptance and the distinction between checked and unchecked false reads.

These finite checks are controls on local formulas. The generic restriction theorem is established by the Lean proof, not by enumeration. Neither these checks nor the kernel theorem receive credit for alternating-machine language equivalence or complexity hardness.

## Scope boundary

Accepted coverage is restricted to the actual typed constructor, PMF normalization and masses, exact initial mixing, posterior-deterministic restriction, label-consistent one-step lift, finite cardinalities and local honest-step invariants, as supported by the replay evidence.

The package does not formalize a clock transformation, an alternating-machine language, global honest histories, positive-probability first-error soundness, policy extraction, a complete path-law correspondence, a file parser, a validated model builder, bit encoding, a solver or an EXPTIME reduction. The README correctly excludes those claims. This review does not re-open or extend the separate ordinary complexity acceptance or historical-priority assessment.
