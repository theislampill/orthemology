# Independent successor review: compiled criterion–interlock composition v2

Review date: 2026-10-02 UTC.

## Disposition

**Accepted as a conditional mathematical/reference-execution checkpoint at the declared typed interface.** The required actor-time correction CEX-1 is resolved in the exact reviewed successor. No unresolved source, proof, execution, or interface blocker was found within that scope.

This is technical research acceptance, not a governor lifecycle decision, repository adoption, external authorization, physical deployment, or whole-program closure. The source/authority, atomic observation, root independence, authentication, reservation, bounded service and compiler/runtime premises remain substantive external obligations. No all-input Python refinement, arbitrary-code updater, N2/T0 theorem, Candidate E adoption, or R5 defeat is established.

Frozen v1 retains the scope correction recorded in `REVIEW_V1.md`. V2 is a named, independently checked successor, not a reinterpretation of old bytes.

## Exact reviewed bytes

- V2 manifest: `a795122fa0d4c3d127371e22599bf23a65a9a546d2abdae8d0d96962682416ae` (132 bound files)
- V2 ZIP: `daa8af769210d2b0c8489b74a186399fc61286e5ca8da4f69595dd0af737f651` (235,625 bytes, 133 entries including manifest)
- V2 `Composition.lean`: `ca93c5a62515718c2de475e6102cff67b902f3021d297b68ce17e03694d2bee0`
- Dynamic-v2 predecessor manifest: `3d620e425f85b9f99681be5ba95ab48f11c4ff9ed706cf56696184e5a9593f67`
- Criterion-v3 predecessor manifest: `bd349c1c91950f2ed2f1616656a5a5334a22ccdeaad52d4810c9a1e1ccbbc75f`

Every manifest entry and every ZIP file was independently compared to copied bytes. The reviewer rebuilt and executed only in separate reviewer-owned trees. Original and copied v1/v2 packages and ZIPs were all rehashed unchanged after testing, together with all 63 original predecessor manifest records. None of the accepted source files was edited by this review.

## CEX-1 resolution

`Actor` now includes `observedTime`. `propose` takes the actor, action and path only; its imported transition call uses that stored observation. `runBatch` no longer supplies `World.now` to proposal construction. The actual root preparation/landing checks remain unchanged and continue to use warranted actual time.

The new definitional theorem `proposal_uses_actor_observation` accurately states the input boundary, without claiming that a stored number proves authenticity. The argument now separately requires a genuine actor observation sufficient for the proposal and an actually valid lease throughout the batch. It explicitly notes that policy delivery does not silently refresh the actor's clock. Thus stale observations are represented rather than suppressed with hidden global knowledge.

Independent source diff and native tests establish the distinction:

- Actor time 2 with actual time 100 still constructs the local proposal and performs exact-envelope cleanup, while live roots reject every expired landing.
- Actor time 100 with actual time 2 does not borrow the earlier world time to rescue its invalid proposal.
- The reviewer’s sixth runtime mutant restores the original hidden-time substitution by using `{ trialActor with observedTime := current.now }`. It compiles after deliberate theorem erasure, links, and exits 1 at `FAIL stale actor time still proposes without a current-time oracle`.

This proves detection of the corrected proposal-interface regression. It does not claim that v1 allowed an expired landing; v1’s live root checks already rejected that.

The artifact harness now predicts its installed successor by calling the imported transition on the actor's own observed plant, policy and time, then uses that guaranteed stable-batch successor for the second actor. It no longer fills the actor observation from `installed.plant`. The diagnostic output still correctly observes the actual resulting plant. The old “close nonce” test label now correctly says “close exact envelope.”

## Independent verification

Official toolchain: Lean 4.19.0, release commit `6caaee842e94`; compiler executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

The reviewer ran the portable replay from `freeze-v2/` into fresh `replay-v2/`. Every imported and new Lean module was compiled from source, C was freshly emitted and linked, and the native executable was run on the bound source. No author `.olean` or prebuilt native executable was accepted as replay evidence.

Verified results:

- 26 new named Lean theorems kernel-check. Inspected accepted source contains no `sorry`, custom axiom declaration, `native_decide`, or unsafe definition. Printed dependencies contain only ordinary `propext`, `Classical.choice` and `Quot.sound` as applicable; the new proposal-input theorem has no axioms.
- All 88 native assertions and seven wrapper boundary tests pass.
- The retained finite domains pass: 80 revocation cases, 60 cancellation cases, 20 exact open/withheld path pairs and five complete two-batch fault scenarios (40 macro-attempts).
- All five supplied runtime mutants are independently rebuilt and detected: ignored compiled successor, bypassed installed-rule gate, cached-only eligibility, omitted revocation memory, omitted cancellation memory.
- The independent sixth clock-substitution mutant is detected as described above.
- `extended-v2/IndependentTests.lean` passes 25 reviewer-authored assertions, including 140 exact open/withheld path cases across seven byte-source fixtures, twelve independently tampered complete-successor fields, malformed paths, wrong requester, grant/lease boundaries, delayed certificates, exact-envelope cancellation scope and three actor-clock cases.
- The three reviewer monotonicity/replay lemmas recompile against v2. They prove version/revision monotonicity and fixed-action rejection after further monotone progress. Their only dependencies are `propext` and `Quot.sound` as applicable. They supplement the review; they are not silently added to the frozen author proof inventory.

All five native state/byte artifact hashes are exactly equal to v1. Independent complete-record comparison confirms:

1. Installation changes `normalizedLF` to `exact`, rule version 3→4 and rule history `[]→[normalizedLF]`, while retaining the extra-LF defective draft, revision 8 and original draft history.
2. Separately authorized repair then restores the exact source draft, revision 8→9, appends the previous draft to history, and preserves installed rule/version/history.
3. Source identity/content/roots, destination, retained standard and unrelated custody are unchanged throughout.
4. Preserved source and repaired draft are the exact 3,013-byte input, both with SHA-256 `e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359`.

## Retained claim-level assessment

The eight detailed assessments in `REVIEW_V1.md` remain applicable, with CEX-1 resolved as above. In particular:

- The executable genuinely consumes the imported Lean source transition’s acceptance and full successor at proposal and live landing. Python is a build/evidence wrapper, not the policy or successor oracle.
- The installed two-constructor interpreter actually changes behavior on the source-plus-LF defect. Merely carrying the protocol string `C1-exact` cannot impersonate an installed exact rule.
- Rule version, draft revision and control epoch remain distinct coordinates, with independent install and data-repair grants. Complete successor binding prevents stale cross-component overwrites.
- Actual landing does not consult global effective policy. Current-policy refinement uses explicit authentic-serial-policy and stale-certificate coverage assumptions, plus the imported root-counting argument.
- Cancellation and revocation races retain correct scoped behavior: durable full-envelope tombstones, late-prepare exclusion, cleanup after action revocation, fresh envelopes available, no rollback of a lawful prior landing.
- Same-rule fresh installation can lawfully advance version/history. Literal state idempotence is false and is not inherited from the binary-table predecessor. Fixed-action exclusion and goal preservation are the correct replacement.
- The single-process atomic plant assignment is a reference transition boundary. It establishes no physical writer, independent root architecture, real authorization, clock fidelity or unbypassable veto. Common corruptible support cannot be treated as free.
- Four-path/two-batch progress is an ordinary bounded argument under the stated stable authorized windows, actor observations, whole-horizon taint bound, no competing plant write, independent bounded service and enough horizon. It is not a wall-clock bound or a complete arbitrary-history mechanization.

Two intentionally exposed nonclaims remain important. `receiveActor` validates certificate shape, not cryptographic authenticity; genuine serial delivery is still a premise. Cancellation is of the complete envelope, not a global ban on the numerical nonce across altered commands; fresh nonce discipline remains a correct-actor assumption. Neither boundary is concealed by the v2 claims.

## Reproducible evidence and stopping point

- `FREEZE_V2_VERIFICATION.json`
- `replay-v2/REPLAY_RECEIPT.json`, compiler/link/runtime logs and full artifacts
- `mutants-v2/MUTATION_RESULTS.json`; reproducer `run_v2_mutants.py`
- `extended-v2/IndependentTests.lean`, `runtime.log`
- `extended-v2/ReviewerMonotonicity.lean`, `monotonicity-compile.log`
- `verify_terminal.py`, `TERMINAL_VERIFICATION.log`
- `REVIEW_V2_RECEIPT.json`

The exact requested correction is implemented and independently rechecked. No additional correction is requested within this review’s bounded subject. Any later source or claim change requires a new digest-bound assessment. No external action, original denied action, or emulation of that action was performed.
