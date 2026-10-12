# Independent review: actual empirical rows

## Verdict and exact source

**Accepted at the stated empirical-row and phase-test interface.** No material proof defect was found. The four new modules establish actual-law strong laws, literal acquired-history/count transfer, all-future deviation bounds, and the stated qualitative true/false row tests. They do not construct the complete hidden-parity controller.

This review binds author manifest `141cb587588f054f26b52908c3ac4b3a66f187d35bcb1b8ecfcbc17b03b0cef8` and author archive SHA-256 `d8de897ce9c1ef5a62d4423e2baef465383f13faae2a0060ec23afad772d9559`. The [retained scope](../../PUBLIC_BOUNDARIES.md#recovered-reference-072), [source identities](../../PUBLIC_BOUNDARIES.md#recovered-reference-071), and [21-module independent cold receipt](../../PUBLIC_BOUNDARIES.md#recovered-reference-070) identify the exact candidate. This is separate from the phase-stabilization manifest and from any global-controller synthesis.

## Proof audit

1. **Actual law and row means.** `RawEmpiricalRows` uses the inherited probability measure `rho.prod (stackMeasure P hP hN)` and the real seeded coordinates. Singleton indicators are measurable and integrable. Their actual integrals are the supplied row entries by the coordinate pushforward and singleton-mass theorems. Restriction to deterministic indices of a fixed row preserves the proved coordinate independence; composing with indicators supplies the hypotheses of Mathlib's `strong_law_ae_real`. This includes zero-mass symbols and deterministic rows. Convergence is not a new hypothesis or axiom.
2. **Simultaneity.** The finite pair and symbol intersections are taken before the policy transfer. The resulting probability-one raw-tape event supports the pointwise argument for every policy. There is no uncountable intersection of policy-dependent almost-sure events. Product independence of the seed and tapes supports the retained controlled-process interpretation; equal marginal laws alone do not replace it. Bare raw-coordinate convergence can hold under weaker joint assumptions, so this review does not claim seed independence is logically necessary for every isolated SLLN statement.
3. **Literal observed statistics.** `historySymbolMass_eq_raw_sum` follows actual sequential consumption and newest-first acquired histories. Each selected pair reads its next previously unused tape cell. `historyFrequency_eq_rawFrequency` holds pathwise at the consumed count. Recurrence implies the count tends to infinity, and deterministic composition transfers the raw limit. Nothing asserts that a random-count sample is conditionally iid or unbiased. An unused pair is correctly excluded from the recurrent-pair conclusion.
4. **All-future probability bounds.** `RawTailDeviation` quantifies over every deterministic count after the threshold. Its events are measurable and decrease; actual SLLN makes their intersection null. Continuity from above gives vanishing masses. The finite-model maximum produces one deterministic existential schedule before the universal model quantifier. It is chosen from the entire supplied model family, without access to the realized true model. The schedule satisfies the lower count gate and the summable geometric budgets; the theorem does not claim it is computable, monotone, or rate-optimal.
5. **Adaptive tests and phase endpoints.** Set containment transfers raw all-future bounds to observed adaptive-count deviations. For arbitrary policies the measure inequality can be read as an outer-measure inequality; actual event probabilities additionally use the proved measurability premise and retained canonical-law adapter. `seeded_true_phase_rejections_bounded` gives a finite random count threshold uniform over policies on one raw-good event. The false-row endpoint requires a recurrent pair and a coordinate gap strictly greater than the fixed tolerance. It then eventually rejects beyond every fixed phase gate. The model and proposed row appear in the theorem's analysis, not as hidden information supplied to the observed-history policy.

## Verification and independent controls

The independent cold replay completed on 2026-10-01 at 18:43:22 UTC: **21 fresh custom objects and 249 exact declaration/axiom readbacks** under Lean 4.19.0 and the pinned Mathlib revision. Source hashes, transitive fingerprints, compiler identity, and official-source ownership are recorded in the receipt. Official dependency object caches remain trusted; this is not a rebuild of Mathlib itself.

The [eight independent Lean probes](../a8d067d153a55d57c7d025b1f5d0107f4bf8d40530f66c983ff26fdded3db533/IndependentEmpiricalProbe.lean) are separately compiled against those fresh objects, with exact type and axiom readbacks. They check real observed counts, deterministic observed frequencies, actual zero/one row means, zero-probability-symbol convergence, the zero-tolerance failure, and the strict-gap boundary. All readback axiom sets remain within the recorded standard Lean axioms.

The [independent exact finite controls](../../PUBLIC_BOUNDARIES.md#recovered-reference-069) pass **83,489 assertions**. They construct the complete finite independent seed/tape law before evaluating causal policies, rather than assigning fresh laws at selected counts. They compare literal acquired histories with raw prefixes, test event containment and probability inequalities, and include deterministic and zero entries. The author's separate 2,750,008-assertion control output also replays identically. These finite computations corroborate definitions and counterexamples; the infinite convergence and tail limits are justified by the checked Lean proofs.

Rejected shortcuts have explicit witnesses:

- A fair tape stopped at its first one or after two draws has final-symbol mean 3/4 and stopped empirical mean 5/8
- Correlating the policy seed with a tape cell changes the selected receipt law despite unchanged separate marginals
- A statistic can match exactly at one count and deviate later; an all-future tail event is essential
- A coordinate gap equal to tolerance need not trigger a strict rejection
- A zero tolerance makes the raw-tail event the whole space in the nonempty control
- An unvisited pair need not have the raw limiting frequency as its observed statistic
- An unconditional error budget need not remain valid after conditioning on a rare phase-entry event

## Composition boundaries

The integration still needs a lawful controller, a common positive tolerance below the relevant finite nonzero row gaps, actual phase-transition identities, support-change handoffs, and a proof that a permanently wrong candidate either reaches a suitable mode or exposes a mismatching recurrent pair. A deterministic burn-in probability bound under the original experiment is not automatically a conditional bound at every adaptive restart. No explicit sample rate, effective schedule, finite expected phase duration, global winning theorem, or controller-memory bound is added by this review.

The earlier cold attempt was interrupted during host contention and is preserved as an interruption, not a failure of the candidate or a successful closure. Targeted development checks against 17 already qualified dependency objects preceded the independent full cold run. Reviewer-only probe/readback formatting corrections are recorded in the review history; no author source was changed. The final claim is based on the completed fresh run and final probe receipt.

## Replay

From the extracted review directory, run the bundled author driver with `--root source-snapshot`, explicit pinned `--lean-bin` and `--mathlib` paths, a fresh absent `--out`, and `--suites empirical_rows --no-reuse`. Then run `python -B replay_probes.py --cold <that output> --environment <pinned environment directory> --out <fresh probe output>`. Run each Python control with `python -B` and compare its JSON with the bound evidence. The environment paths are external prerequisites, not embedded custom objects.
