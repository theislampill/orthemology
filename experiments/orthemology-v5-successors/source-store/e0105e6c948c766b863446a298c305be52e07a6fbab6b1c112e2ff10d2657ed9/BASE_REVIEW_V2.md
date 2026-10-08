# Independent dynamic-repair review: corrected checkpoint v2

Review date: 2026-10-02 UTC. Reviewer: `review_dynamic_repair_proofs`.
Target: `../../delivery/dynamic-repair-checkpoint-v2`.
Packet manifest SHA-256: `3d620e425f85b9f99681be5ba95ab48f11c4ff9ed706cf56696184e5a9593f67`.

## Disposition

**ACCEPTED AS A CONDITIONAL MATHEMATICAL CHECKPOINT AT THE DECLARED v2 INTERFACE.**

All three required v1 findings are resolved in the reviewed bytes. No unresolved mathematical or interface blocker was found within this review's scope. Acceptance does not certify physical interlocks, authenticated control ports, the reservation institution, the lifetime-union fault budget, or actual implementation timing. Those remain independent applicability premises. It is not acceptance of unrestricted mobile-fault tolerance, an exact physical-time bound, or an R5 defeat.

The immutable v1 remains a revision-required predecessor; v2 has a disclosed stronger control-access and cancellation interface. The correction must not be represented as proof that v1 already guaranteed termination.

## Required findings rechecked

### DYN-1: resolved by an explicitly stronger, root-charged cancellation mechanism

`MODEL_AND_PROOFS.md` lines 145–162 retain the correct-actor policy assumption, separate it from charged downstream dispatch, and explicitly add independently authenticated per-root control access even when another member of the serial data path is tainted. Shared active control dependencies are not silently exempted from the support map.

Lines 246–283 define bounded preparation, execution and cancellation phases. The actor advances to cancellation without waiting for a tainted execution acknowledgement. Each untainted cancelling root durably closes the full unique command/nonce/path before replying. Authentication and the original recipient's retained cleanup right are explicit; third-party cancellation is excluded. Fresh nonces remain available, and late preparation cannot reopen a cancelled command.

The counting argument is valid:

- `c>B` guarantees at least one lifetime-untainted acknowledger, whose continuing gate veto prevents any later landing of the cancelled command.
- `c≤q−B` guarantees enough selected-path correct responders under the stated independently bounded control service.
- The main feasibility inequalities imply `q≥2B+1`, so `c=B+1` satisfies both bounds.
- At minimum roots, `q=2B+1`, so cancellation's safe-and-available certificate threshold is uniquely `B+1`.
- A landing before cancellation completes is either already blocked or the same authorized idempotent repair; cancellation does not undo it.

The threshold is derived from the budget; the durable veto and bounded independent service are model hypotheses. The new Lean lemmas `charged_cancellation_blocks` and `cancellation_available` correctly prove that separation. The Python finite checks cover 4,459 selected-certificate/late-landing cases through `B=2`, a too-small certificate counterexample, nonce tombstones, lawful landing before closure, foreign-recipient rejection, and subsequent fresh-command availability.

The covering lower bound remains valid after adding labelled cancellation replies: `MODEL_AND_PROOFS.md` lines 238–243 and its Theorem 4, plus `COVERING_TRADEOFF.md` §1, expressly select admissible faulty behavior that matches intact preparation/cancellation replies and timing while withholding execution. Cancellation is therefore not silently a verified faulty-root oracle. The fixed-fault-set and randomized averaging arguments survive unchanged.

The model's logical synchronous phases are an explicit service interface. No physical clock mechanism or real-time duration is proved. Correct actor scheduling is required, and the model does not make a malicious or stalled actor execute the portfolio.

### DYN-2: resolved by horizon and cap-origin qualifications

`MODEL_AND_PROOFS.md` lines 293–301 require enough remaining permitted phase slots to finish the full batch within finite `H`. The union-fault premise is not extended by assertion beyond its declared horizon.

The bound counts newly initiated final-descriptor macro-attempts after stable delivery. Lines 424–432 explicitly charge any residual old in-flight attempt separately and start the `3N` phase upper bound at the next macro-attempt boundary. Delivery latency remains outside that bound. The end-to-end eventual result still assumes eventual certificate delivery, correct actor scheduling, final authorization and quiescence.

### DYN-3: resolved by preserving the exact fixed-R5 boundary

`MODEL_AND_PROOFS.md` lines 594–604 no longer claim that the already checked R5 architecture realizes every new mechanism. They retain the warranted conclusions: the operational proof does not consume an integrative sourcehood/unity bridge, and no R5 defeat has been established. Newly supplied interlocks, certificates, reservation rules and warrants are not retroactively admitted R5 resources.

## Retained mathematical assessment

The detailed v1 cold review remains applicable to unchanged arguments and witnesses; see `REVIEW_V1.md`'s twelve scoped conclusions. In particular:

- Safety plus repair/revocation availability is exactly `q+r>n+B`, `q,r≤n−B` for the frozen symmetric q/r gate interface.
- The minimum is `n=3B+1`, uniquely `q=r=2B+1` there.
- Under the opaque-failure interface, the minimal-root optimum is `choose(3B+1,B)` macro-attempts, including `B=0`.
- In general the optimum is the covering number `C(n,n−q,B)`. For fixed feasible `n,B`, the minimum attempt objective is attained at `q=2B+1,r=n−B`.
- The supplied exact small frontier remains correct: `B=1,n=4,5,6` gives `4,3,2`; `B=2,n=7,8,9,10` gives `21,11,8,6`.
- The complete `C(9,4,2)=8` lower argument is an ordinary proof. Its four-edge sublemma is additionally kernel-checked. No solver status is substituted for the missing incidence/repetition formalization.
- Lifetime-union taint, actual certificate-effective reservation semantics, full future mediation, actor-local descriptor custody and final quiescence remain essential premises.

The macro-attempt bound is exact for the declared search objective. `3M` unit phases, or `M(Dp+De+Dc)` logical service units, is the construction's upper bound; the packet does not prove optimality of primitive rounds or wall-clock latency.

## Independent replay and byte binding

All 30 packet-manifest files matched size and SHA-256 before copying. The reviewer replayed the portable verifier from `freeze-v2-replay/` into `replay-v2-logs/`, not in the author packet or canonical repository:

    python freeze-v2-replay/verify_all.py \
      --lean <LEAN_EXECUTABLE> \
      --output-dir <review-directory>/replay-v2-logs

All four stages exited zero: finite dynamic checks, finite covering checks, `DynamicInterlock.lean`, and `CoveringCore.lean`. The three JSON result/trace files and four per-stage logs are byte-identical to the author replay. The whole frozen payload and its manifest were rehashed afterward and remained unchanged.

Official compiler: Lean 4.19.0, release commit `6caaee842e94`.
Executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

No `sorry`, custom axiom declaration, `native_decide`, or unsafe definition occurs in either Lean source. Printed theorem dependencies are only ordinary Lean logical axioms (`propext`, `Classical.choice`, `Quot.sound` as applicable). This establishes kernel acceptance of those formal propositions, not full temporal-protocol mechanization.

Replay counts include:

- 347,489 quorum-pair enumerations and 2,025 threshold parameter cases through `n=9`
- 12,870 stale-landing executions through `B=2`
- 211 quiescent fault sets through `B=3`, with 43,500 repair/persistence attempt slots
- 861 unique-good-path cases through `B=4`, plus all 96 `B=1` search-order prefixes
- 4,459 cancellation late-landing cases through `B=2`
- 145 maximal fault sets across covering witnesses, 1,350 portfolio executions, and 15 four-edge graph cases

The reviewer additionally wrote `independent_set_checks.py`, importing no candidate function. Its bounded checks pass:

- 686,829 cancellation-certificate/fault-set pairs through `n=9`
- 1,155 cancellation-availability parameter cases
- 2,025 cross-overlap parameter cases
- 186 fault sets of every size at most `B` across the explicit portfolios

Those are finite corroboration only. The general conclusions rely on the ordinary proofs and listed Lean propositions.

## Remaining obligations and handoff

No requested correction remains open. External realization of the premises remains unestablished. In particular, this review does not infer authenticated channels from identity strings, a physical veto from a set-membership assertion, actual consent from a certificate definition, bounded service from a synchronous Python call, or unbounded lifetime security from a finite regression suite.

The frozen README and author replay retain their historical “independent review pending” labels. This independent report and `INDEPENDENT_REVIEW_RECEIPT.json` are the acceptance sidecars for the exact manifest above. They do not alter those frozen bytes. Any later source change requires a new digest-bound review of the changed material.
