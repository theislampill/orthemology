# Independent V2 recheck: finite-history interlock safety

2026-10-02 UTC. **PASS at the conditional original-interface claim ceiling below.** No material issue remains. V1's non-blocking Reservation-domain precision issue is resolved.

## Inputs and independence

Reviewed `REVIEW_SNAPSHOT_V2.json`, SHA-256 `e253a2b1a537826094db7ede00768b561360ce25e3a6907354592a320a2de278`, binding 34 files. Verified every file before and after the review. Also verified all 33 frozen V1 input files against manifest `9b2bafffd7b45f84db7ce6ca8f8e86e6027f8dd573f6e302d392fb5615d48c94` and confirmed the V1 review receipt plus all 44 bound review artifacts were untouched.

This is a narrow independent delta review with a fresh full replay. It retains the substantive V1 independent assessment because the relevant sources are byte-identical, not because the old accepted V2 base automatically accepts new formalization. The detailed V1 report is preserved in `../independent-review-v1/REVIEW.md`, SHA-256 `d87ee8e19ad0b91a38c761c8905855f12b8af91b035cc4f45bce81cb574f1665`.

## Exact correction

The only Lean changes are:

1. `Reservation` explicitly requires `ValidPath c k` before concluding external permission.
2. `admitted_externally_authorized` supplies that premise using `admitted.1`.

The source statement adds the matching valid-q-root-path qualification. Author verification metadata/replay evidence are refreshed and `V2_CHANGELOG.md` records the correction. The model, gates, states, transitions, thresholds, invariants, central admission/safety/cancellation/persistence results, negative controls, public fixtures, and verifier are unchanged. `candidate-diff.patch` and `diff-audit.json` record the comparison; an additional exact-text assertion verifies the two-line proof delta.

The correction weakens an unnecessarily broad external hypothesis without weakening any internal theorem or operational contract. Reservation remains an independently supplied external premise; it is neither a gate input nor consent inferred from a certificate. The proof now consumes precisely the valid-path fact already available from the actual admitted landing.

A reviewer-only `ReservationDomain.lean` check proves both that the revised predicate can preserve the valid-path domain and that the copied V1 predicate unnecessarily required permission for a concrete descriptor-authorized invalid-path command. This validates the intended change, rather than merely observing that two lines changed.

## Fresh verification

Ran the unchanged `verify.sh` with independent output `independent-review-v2/replay`:

- Five modules and both candidate fixtures compiled.
- All seven false claims failed for the expected kernel-reduced false-proposition reason.
- All seven accepted-source scenarios passed.
- Candidate hashes, all 11 frozen source/review bindings, and compiler binding stayed unchanged.
- Recompiled the entire V1 reviewer challenge suite against V2. Its sole source adaptation supplies the new valid-path premise in the external-consent counterexample. All checks passed.
- The additional Reservation-domain checks passed. Positive logs contain no warnings, errors, or proof holes; reported theorem dependencies are only `propext`, `Classical.choice`, and `Quot.sound`.

Used Lean 4.19.0, release commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, and the same supplied Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` read-only. Freshly compared all 6,816 Mathlib source files to archive SHA-256 `9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425`, with no mismatch. No dependency was changed or rebuilt; compiled-cache reproducibility is not separately certified. All reviewer writes were confined to `independent-review-v2`.

## Retained exact ceiling

The result is conditional kernel-checked safety for arbitrary finite allowed histories of the original dynamic V2 finite-root/whole-binary-table interface: every admitted write is current, internally authorized, recipient-bound, and exact; completed cancellation excludes that same full command/nonce/path after every finite continuation; an admitted repair restores the whole table; and an already restored whole-table goal persists across a stable-effective-epoch continuation.

The proof requires authentic authoritative serial descriptors, one continuing lifetime-union fault superset/budget, coherent root-wide close-before-acknowledge and durable live veto across all owned gate copies, and same-command non-bypassable atomic physical mediation. Correlation alone does not establish root-wide closure. F is proof-side lifetime accounting, not actor knowledge or instantaneous/mobile-fault protection. Actual external authorization additionally requires the corrected valid-path Reservation premise.

Honest actor policy, fresh nonces, all-good path addressability, and independently bounded authenticated per-root control service remain separate progress premises. No complete liveness, phase-time bound, covering/randomized optimality, infinite-horizon extension, real consent, cryptographic or physical implementation assurance, R5 defeat, or automatic transport to typed compiled composition/unknown-label interfaces is established. Python-to-Lean correspondence remains an explicit ordinary argument plus bounded corroboration, not a mechanized refinement proof. Negative controls remain concrete witnesses, not exhaustive mutation tests or physical experiments.

No correction remains open for this V2 digest. Source-preserving packaging may retain this disposition only with the exact reviewed bytes and this receipt; changed source requires a newly bound review.
