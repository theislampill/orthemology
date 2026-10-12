# Independent review: dynamic V2 finite-history safety kernel

Review date: 2026-10-02 UTC. Disposition: **PASS, at the conditional finite-history claim ceiling below.**

This is a new independent review of the extension, not acceptance inherited from the old base. Candidate input: `../REVIEW_SNAPSHOT_V1.json`, SHA-256 `9b2bafffd7b45f84db7ce6ca8f8e86e6027f8dd573f6e302d392fb5615d48c94`, containing 33 files. The accepted V2 source and old review serve as the controlling interface and premises, not as evidence that these new proofs work.

No material mathematical, source-correspondence, circularity, or verification blocker was found. No candidate correction is required for this disposition. The positive result certifies the displayed Lean transition system; it does not certify physical deployment or external consent.

## Independent verification

- Verified the supplied manifest digest and all 33 file sizes/hashes before and after review.
- Ran `./verify.sh ./independent-review-v1/replay` using the candidate's script, with an independent output/build directory. All five modules and both public/non-vacuity fixtures compiled, all seven false-claim controls were rejected for the intended false-proposition reason, and all seven accepted-Python-source scenarios passed.
- Candidate and all 11 frozen source/review bindings remained unchanged. No canonical source or predecessor was edited; only this review directory was written.
- Used Lean 4.19.0, release commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The independent build directory precedes the supplied Mathlib/package caches in `LEAN_PATH`; development `.olean` files beside candidate sources were not imported.
- The supplied Mathlib archive hashes to `9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425`; its root names commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. Independently compared all 6,816 archive source files to the supplied source directory, with no mismatch. Consumed the supplied compiled cache read-only, without reinstalling, changing, or rebuilding dependencies. This is not an independent cache-reproducibility audit.
- Printed principal theorem dependencies contain only `propext`, `Classical.choice`, and `Quot.sound`. The candidate replay rejects proof holes/custom axioms, `unsafe`, `native_decide`, and warnings/errors in positive proof compilation.

The authoritative replay output is `verify-console.log`, with detailed logs under `replay/`. `RECEIPT.json` binds this report and verification artifacts. Earlier diagnostic logs concern only reviewer-authored fixture binder names, not candidate failures; the final `review-challenges.log` is the reviewer-fixture result.

## Adversarial assessment

### 1. Source fidelity and authentic history: pass

Compared the actual accepted `base-v2/MODEL_AND_PROOFS.md`, `dynamic_interlock.py`, and `review/BASE_REVIEW_V2.md` against all new modules and scope documentation. Descriptor, whole two-entry table, authenticated requester, full command/nonce/path commitment, close-before-acknowledge, durable revocation/cancellation, and post-admission damage classification are retained.

The Python atomic `World.revoke` is split into request, individual acknowledgements, and completion. Interleavings are more permissive but cannot install the next good-root descriptor early. A fixed arbitrary `source : Nat → Descriptor` encodes the authoritative serial choices, with the unique pending next descriptor implicit. This is a safety model of source choices, not a protocol for selecting authority or predicting future proposals. Per-root delayed/reordered delivery is permitted by the ordinary source even though Python offers a bulk-good-root delivery operation.

`Step.deliver` uses `0 < e ∧ e ≤ s.epoch`, rather than carrying a certificate object. This compression is sound on reachable histories: `past_certificates (e-1)` supplies the stored size-r completed certificate and its durable good acknowledger records. The reviewer independently compiled that implication. The delivery restriction is a semantic authenticity premise, not a global input to an honest gate. Arbitrary non-reachable states are not silently covered.

There is no mechanized Python-to-Lean refinement theorem. The documented ordinary correspondence and bounded source replay are correctly identified as such.

### 2. Induction and proof-side fault accounting: pass

`Consistent` (`HistoryModel.lean:177–184`) contains structural authenticity, not-future, completed/pending revocation evidence, and selected durable cancellation evidence. It does not contain the desired landing-safety conclusion. `HistoryInvariant.lean` establishes it from `Initial` by checking each concrete constructor and then actual finite-trace induction. Its auxiliary `consistent_setRoot` is a proved lemma with explicit conditions, not an unrestricted invariant-preserving transition axiom.

Good-root revocation/tombstone monotonicity, global epoch monotonicity, and cancellation-evidence persistence are separately proved from actual steps. Faulty-root arbitrary replacement cannot clear another root's stores.

`Config.faulty` is a proof-side fixed superset F of the entire trace's lifetime-union faults. Treating every root in F as arbitrary even before its first real failure is a conservative safety overapproximation. No actor discovers F, no apparent recovery resets the budget, and the result is not instantaneous/mobile-fault tolerance.

### 3. Admission and causal veto: pass, under the explicit mechanism premise

`Envelope`/`Permits` (`HistoryModel.lean:48–53`) read only the actual local descriptor, full-command commitment, revocation/cancellation stores, command, and authenticated requester. They do not read effective epoch, `source`, F, or the final safety theorem. F in `Lands` is semantic adversary classification, not a deployed permission oracle.

`admitted_current_authorized` first finds a good path member, obtains authentic local authorization and a not-future bound, and then excludes an old epoch using the actual completed revocation certificate's good overlap. Only afterward does it conclude current global authorization. The `land` function's global authorization check classifies an already admitted effect as repair or damage; it does not veto an unsafe effect.

One `RootState` supplies every gate occurrence owned by that root. Thus root-wide close-before-acknowledge, durable lookup across all owned copies, and same-command non-bypassable atomic mediation are operational premises. Shared failure correlation alone would not imply any of them. The documentation states this distinction explicitly and does not elevate a displayed certificate or an uncharged common writer into a physical enforcer.

### 4. Actual writes, cancellation, and persistence: pass

`finite_history_safety` and `finite_history_admission` quantify over arbitrary finite allowed histories and reached pre-states. Every admitted write has the current epoch, exact recipient, target ID/version, scope, and both table entries. Exact commitment membership additionally binds nonce and actual path. Event determinism prevents `AuthorizedTrace` from selecting a different safer execution.

`no_landing_after_cancellation` allows arbitrary further requests, transitions, deliveries, preparations, holds, and bad-root changes. Its conclusion is for the same full command/nonce/path and every requester. The reviewer also proved absence of that landing event at every position in any continuation, rather than merely checking one endpoint.

`admitted_repair_restores` establishes whole-table restoration on an admitted repair. `stable_trace_preserves_goal` preserves an already restored table under arbitrary continuation whose endpoint epoch is unchanged; proved monotonicity rules out an intervening change-and-rewind. Neither statement asserts that a landing eventually occurs.

### 5. External premises remain separate: pass, with one precision note

`Reservation` and `admitted_externally_authorized` make actual external permission a separate explicit premise. They do not derive consent from certified currentness. In particular, a pending request before root closure can still admit the old current command, which the reviewer checked. Immediate external revocation needs the independently warranted reservation/earlier-closure bridge.

Non-blocking precision note: `Reservation` (`HistoryTrace.lean:131–134`) is sufficient rather than minimal. It quantifies over every descriptor-authorized `Command`, including commands with invalid path cardinality; the admission corollary only needs the valid-path instances. Preserve this exact quantifier when citing that corollary. Do not represent it as a proved equivalence to every external permission model. A future tighter external refinement could restrict its domain, but internal history safety does not depend on this predicate.

Correct actor policy, fresh nonces, direct all-good path addressability, and independently bounded authenticated per-root control service remain distinct progress premises. None is manufactured by safety induction or by root correlation. No phase scheduler, eventual certificate delivery, bounded-time attempt termination, or liveness proof is supplied here.

## Controls and non-vacuity

The seven negative claims genuinely fail by kernel reduction, not missing imports or syntactic errors. Positive witnesses include concrete preparation, revocation, delivery, and cancellation prefixes. The selective revocation omission leaves local authorization/requester/commitment/cancellation checks intact; target-only authorization intentionally removes more of the live envelope, which is correctly disclosed. The B-only cancellation example still uses the original good-gate contract. Substitution and bypass witnesses correctly mark the same-command/mediation assumption boundary.

These controls are concrete countermodels and false-claim rejection checks. They are not an exhaustive mutation campaign, a theorem that every syntactic check is individually necessary, or a hardware fault-injection experiment. The bypass function directly models an unsafe bypass effect; its witness cannot independently establish that a particular real writer has such power. The source replay corroborates seven scenarios, not all language-level behaviors.

The supplied `MultiEpoch` fixture has a real reachable repair after two transitions, partial and reordered certificate delivery, a lagging non-path good root, and stale exclusion. This rules out an all-hold-only interpretation, but is one concrete configuration rather than evidence for generality; generality comes from the quantified proofs.

Reviewer-only `ReviewChallenges.lean` additionally compiles: certificate existence for deliveries; event-wise cancellation exclusion; positive thresholds from Config; pending-request/early-close distinctions; copied-requester rejection; reachability of the B-only cancellation state; bad-root store erasure plus late reprepare with the honest veto retained; rejection of good-root cancelled reprepare and foreign cancellation; successful fresh-nonce repair after cancellation; a successful B=0 trace; arbitrarily long hold traces; and failure to infer external consent without its premise.

## Exact claim ceiling and disposition

PASS supports conditional kernel-checked safety of arbitrary finite histories in the original accepted dynamic V2 finite-root/whole-binary-table interface, with authenticated authoritative serial descriptors, a continuing lifetime-union budget, coherent durable root-wide vetoes, and exact non-bypassable physical mediation as model premises. It supports current/exact internally authorized admitted writes, permanent exclusion of a cancelled full command, and stable-epoch whole-table persistence. External authorization additionally requires the displayed `Reservation` premise.

It does not establish external realization, real consent, hardware or cryptographic correctness, unrestricted mobile faults, a new horizon or infinite-liveness result, full search/liveness/covering/randomized optimality, R5 defeat, or transport to the separately typed compiled composition or unknown-label interface. Such claims need their own premises and proofs.

No material issue remains open for this digest. Any change to the reviewed candidate inputs requires a newly bound review; archive/extraction replay may preserve this review only when the exact bytes are retained.
