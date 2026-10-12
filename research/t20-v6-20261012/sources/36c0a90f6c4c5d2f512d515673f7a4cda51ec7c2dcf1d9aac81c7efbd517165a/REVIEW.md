# Sixth inconclusive-control follow-up

## Scope and disposition

This is a bounded source/implementation-fidelity check against Orthemology main
`19de267cd41d2a5eeeb3eaf0b91562f706e2a916`. It is Sixth baseline revalidation,
not a Seventh theorem or a reopened positive endpoint. No repository files,
commits, pull requests, or remote states were changed.

The two original full-mutation execution outcomes remain **INCONCLUSIVE**.
There is an exact source-bound scalar obstruction for the cost mutation. The
runtime mutation still lacks an exact-subject counterexample or concrete
full-source rejection. A fresh 162-module positive closure passed, then the
unchanged runtime mutation again produced only a whnf heartbeat timeout. A
timeout is not counted as rejection.

## Source custody

The pinned successor overlay and its two component receipts were read through
the GitHub connector. The materialized overlay has Git blob SHA1
`523d2b57e052433d98fe1cb0cb6b6eed19a1a768`. Component receipts match the
overlay's SHA256 bindings:

- Cost: `6adcdf11f67f943677e23407a9c8f115e72583349affe8ebafd370c791275de3`
- Runtime: `752d00de10df73795daff7acf5de608c2290542dc9299d150aee76257d0d60ab`

The pinned SOURCE_MAP Git blob is
`0f565ab802d53fae8a3a929e65f291e3dade7242`. Both mutation members are explicitly
`CUSTODY_ONLY`; their bodies are not in the public source store. The exact files were recovered from the delivered predecessor archives:

- technicalpart1.zip, SHA256
  2a1791994b2965d9b2502886d6f836d49134d2b84bd0910359268fa674f0e9f8.
- Orthemology_v5_Sixth_Completion_Supplement_20261002.zip, SHA256
  70677d135cd8957f5b527d555001eb8e53b0cc19652297709eb110e94f2a39be.

Those large outer archives are not required for this packet's supported
replays: the exact custom runtime closure and the exact two mutants are
included. INPUT_MAP.json records their original nested custody identities.

Every inspected public Lean source matches its SOURCE_MAP SHA256, and both
mutation files match the exact hashes named in the baseline receipt.
`INPUT_MAP.json` records nested custody routes; the two `diffs/` files
are byte-bound diffs, each containing exactly one semantic replacement.

## Cost control 07: exact obstruction, limited credit

Target: `07-change_controller_tolerance-ActualExponentialMoments`, mutation
SHA256 `7b639a064e5d523827750a8a9e8527b4f172b45523ca2d32e565a10ba3348318`.

The mutation changes the call to
`actual_generated_badCount_exponential_cutoff_tail` from tolerance `ε` to
`ε/2`. It leaves its passed proof `hη` unchanged. The caller has
`hη : η ≤ ε`; the callee's source at GeneratedExponentialTail.lean:94 takes
`hη : η ≤ ε`. Instantiating the callee's ε with ε/2 therefore demands
`η ≤ ε/2`, which the caller does not supply. It likewise leaves the separator
proof and cost/controller terms at their original tolerance.

The exact missing implication is false already at ε = η = 1:
0 < 1 and 1 ≤ 1, but not 1 ≤ 1/2. The focused files check that same scalar
obligation over Mathlib real numbers. They do not replace the actual controller
with a toy controller and do not pretend to replay the large mutation module.
See evidence/cost/FOCUSED_CHECK_RESULT.json for their fresh execution status.

The original archive's byte-bound BUILD.log
`4a53ab0c59c6167b1e252b12559d0e83a608d18d7209a176f5fc95238bf26cde`
already contains this exact application-type mismatch at mutation line 92,
followed by a deterministic whnf timeout and a cascading unknown-constant
error. The concrete mismatch is useful supporting evidence. Its later timeout
is not an additional semantic rejection, and this inherited log is not a
fresh replay of the merged closure.

This mutation changes a proof application, not the positive theorem statement.
Therefore it would be wrong to seek a counterexample to the unchanged accepted
exponential-moment theorem, weaken its hypotheses, or claim that theorem fails.
The honest new credit is a verified local premise obstruction for the exact
changed application. The baseline full-run INCONCLUSIVE entry is preserved.

Minimal exact-module next test: once the pinned custom dependency closure is
freshly available, replay the unchanged hash-bound mutation or isolate the
unchanged failing application with the original theorem signature and imports.
Require a concrete mismatch diagnostic before any resource diagnostic; retain
the complete positive import control. Do not silently repair η or ε, add an
inequality hypothesis, or infer full rejection merely from elapsed resources.

## Runtime control 05: exact-subject blocker remains

Target: `05-run_unverified_old_tolerance-FullControllerCanonicalLaw`, mutation
SHA256 `89b9823fdbc8d4106fd8e8eb449dae8079cfe180c37859d95f23d222afded9eb`.

The only change is in the decoded-parity conclusion at line 64:

- Old program: `policyProgram c`
- Decoder policy, unchanged: `sourcePolicy (withComputedTolerance c)`

The original conclusion uses the computed-tolerance configuration for both.
The proof still obtains canonical-law equality and parity for the computed
program, and its final ae-map step still uses that computed program. In
CanonicalHistoryBinding.lean:166–168, decodedHistory obtains receipts from its
program argument and reconstructs action histories with its separate policy
argument. Thus this is a mixed executed-program/decoder claim. A witness about
running the old controller with its own old decoder would test another target.

The source contracts expose the gap precisely:

- `policy_program_implements c` certifies `policyProgram c` against
  `sourcePolicy c` (FullControllerSource.lean:462–469).
- `computed_policy_parity c` proves success for the computed policy.
- `withComputedTolerance` explicitly warns that it need not preserve arbitrary
  old policy decisions (ComputedToleranceSource.lean:10–12).
- The kernel fixture's receipt row depends on the actual action: the true
  receipt has probability 1/3 when action = model, and 2/3 otherwise
  (RuntimeRationalBinding.lean:16,58–71).

These facts demonstrate why an implementation/decoder compatibility bridge is
needed. They do not by themselves refute almost-sure parity for the exact mixed
decoder. A finite source difference, mismatched law, or one bad tape is not
enough to refute that almost-sure infinite-horizon assertion. A full-support
fixed fixture and the supplied-selector Certificate hypotheses must also be
respected. No such complete certificate and positive-measure parity failure was
constructed in the initial source-analysis pass. The supplied native execution
fixture explicitly disclaims a retained-selector certificate; the separately
accepted fixture uses zeroPriority, for which every path succeeds. Neither can
be relabeled a faithful negative witness.

The archive BUILD.log SHA256
`d0f2e7abc18aeb81d24adddd9a9484a502baf84a533ba61ec5b8760597e1dd8c`
contains only a whnf heartbeat timeout at the modified theorem. Its archived
RESULT.json labels it rejected, but that label is not semantic evidence. The
merged successor overlay correctly retains INCONCLUSIVE; so does this review.

The requested fresh focused replay was then performed. All 162 exact custom
modules passed, with FullControllerCanonicalLaw compiling in 5.033 seconds.
The unchanged hash-bound runtime mutant returned exit 1 after 20.934 seconds
and only a deterministic whnf heartbeat timeout at the modified theorem
(200,000 heartbeats). Log SHA256:
`1b8272ebf3ddfae764fede20756518234b8b76dc391bd2d05f1fe61c4d69db6b`.
There is no missing import, positive-control failure, fabricated fixture, or
wall-clock termination hiding behind that disposition. This remains a genuine
exact-source elaboration-resource blocker. No higher-heartbeat retry followed.

Minimal next semantic test requires one full `Config`, menu, priority, initial
state/support and `Certificate`, and a proof of positive-probability failure for
the computed-policy decoder fed receipts from the old executed program. A
faithful certificate must bind all 16 cycle cells, 16 conditional target cells,
and four stage-action cells to the retained choices. Alternatively, an
independent proof of the exact mixed target could establish that the proposed
negative control is semantically valid and needs reclassification. Mere
source/program inequality would not decide that question.
Do not substitute old/old decoding, a missing certificate, a changed kernel,
or a finite-prefix law discrepancy for that parity counterexample.

## Dependency and verification boundary

Lean 4.19.0 binary SHA256 matches the Sixth pin
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Official Mathlib source was acquired at the exact pinned revision
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. Its toolchain, manifest, and Real.Basic
files match pinned GitHub blob identities; all eight official dependency git
HEADs match the manifest. A minimal official cache request first covered the
focused scalar checks; the subsequent exact runtime replay required the full
official cache (6,641 objects unpacked successfully). Dependency cache objects
remain explicitly trusted.
No custom Sixth object has been imported from an author build or silently
reused as a fresh result. No unbounded heartbeat retry was run.

A further exact-source feasibility pass extracted the runtime-v8 candidate
archive (SHA256 b5be7775f6d0b1d5628f8d100f4d0db3c3d44827472e3965c7bbd4cb04423b34),
verified its entire frozen manifest/inventory, and identified a 162-module
custom import closure for FullControllerCanonicalLaw. Seven modules import
all Mathlib. INPUT_MAP.json records the graph. The completed run used a
fresh, isolated, two-process focused driver. The portable replay.py entrypoint
uses sequential compilation with no heartbeat changes or custom-object reuse.
The completed run's result is
evidence/runtime/RESULT.json; the scalar check receipt is separate.
Selected canonical-law, decoded-parity, and output-parity types/axioms were
read back successfully against this fresh closure; all three use only
propext, Classical.choice, and Quot.sound. That readback is recorded separately
in evidence/runtime/READBACK_RESULT.json. This is not a rerun of the
original aggregate driver or its complete theorem readback census.

## Verified source links

- [Merged control overlay](https://github.com/theislampill/orthemology/blob/19de267cd41d2a5eeeb3eaf0b91562f706e2a916/docs/provenance/v5-research-continuations/SIXTH_FINAL_OVERLAY.json)
- [Cost callee](https://github.com/theislampill/orthemology/blob/19de267cd41d2a5eeeb3eaf0b91562f706e2a916/experiments/orthemology-v5-continuations/source-store/4904e5827d4b972c32fb182f40707c96b46b7d309f0cd75d63c54c42615df22c.lean#L90-L107)
- [Runtime original](https://github.com/theislampill/orthemology/blob/19de267cd41d2a5eeeb3eaf0b91562f706e2a916/experiments/orthemology-v5-continuations/source-store/47df70da9ffde6c5c8f4e7e443e7d4d7389b36001ebd60d15d5c9cb60b2ff1b3.lean#L56-L74)
- [Computed-tolerance contract](https://github.com/theislampill/orthemology/blob/19de267cd41d2a5eeeb3eaf0b91562f706e2a916/experiments/orthemology-v5-continuations/source-store/5c9c68b419c7c4249c166f545257414a8f500f3aef126482b091439f6f7cd54c.lean#L10-L16)

## Public packet projection

Evidence logs and command fields use symbolic filesystem roots. PROJECTIONS.json
retains the original byte hashes and the public file hashes. The original hashes
in the discussion above refer to the completed run before path normalization.
All Lean source and mutation files are byte-exact. The portable driver was
packaging-validated without rerunning any proofs; completed proof evidence is
retained separately. This packet supports full fresh runtime-target closure and
mutant replay plus the limited scalar cost checks. It does not contain the full
cost theorem import closure or claim full cost-mutant replay.
