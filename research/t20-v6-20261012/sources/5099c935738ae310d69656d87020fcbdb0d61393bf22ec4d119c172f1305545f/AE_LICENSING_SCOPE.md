# Almost-sure licensing: same recursive iff, weaker input contract

## Principal result

`ae_licensed_policy_exists_iff_recursiveWinning` in `lean/AELicensedEquivalence.lean` removes the pointwise all-seeds licence premise from the INPUT existence statement. For the same finite fixed controlled-iid models, nonnegative normalized kernels, nonempty initial support B, support-only public menus, and common private-seed probability law:

There exists one measurable shared policy π such that, for every θ∈B,

- the actual observed-history experiment is almost surely licensed at every physical step; and
- its same canonical actionLaw is almost surely eventually target-good

if and only if the original `RecursiveWinning P G Γ B` criterion holds.

`ae_licensed_finite_budget_exists_iff_recursiveWinning` gives the analogous existence iff with a finite expected total physical error budget. All 87 sources of the prior pointwise-licensing iff are preserved byte for byte; this is a separately frozen two-module extension.

## Why the licence event lives on histories

`LicensedHistoryPath P Γ B d H` means, at each n,

`historyAction d H n ∈ Γ(historySupport P B (H n))`.

The action is read from the next history head, and the menu is computed from the current acquired history before the next observation. This event is proved measurable. It is stated under the original canonical `observedTraceLaw`; the action-only pushforward discards the observations needed to recover the current support, so it would be the wrong interface for this safety assertion.

## Necessity: existence conversion, not relabelling the old policy

1. `common_seed_success_and_history_event` writes both safety and target success on the actual seed×feedback product experiment. Fubini and a finite intersection select ONE seed with both properties in every initially live model.
2. `rowHistory_marginal_formula` computes the probability of each fixed-seed acquired history from the original canonical cylinder formula. For a compatible history with θ still live, every observation factor is positive. Its compatible fixed-seed factor is one. `feasible_rowHistory_positive` therefore proves that the history has strictly positive probability in every one of its live models.
3. If the fixed-seed policy issued an illegal next action at any feasible compatible history, all paths in that positive cylinder would violate all-time safety at that very step. This contradicts the selected seed's almost-sure safety. `fixed_seed_ae_license_is_pointwise` consequently supplies the pointwise licence premise required by the prior deterministic necessity theorem.
4. The existing all-branch induction and relative-support recurrence argument imply the recursive criterion.

No claim is made that the ORIGINAL randomized policy is pointwise safe on its null seeds. For example, a seed law concentrated on seed0 can permit arbitrary illegal behavior on seed1 without affecting almost-sure safety. The proof selects a seed and proves an existence consequence; the constructive direction may then return the separately defined shared seed-independent certified controller.

## Sufficiency and true-model retention

The already constructed controller is pointwise safe on every feasible action-consistent history. To obtain an almost-sure statement in the actual history law, the extension also proves true-model retention instead of presuming that all abstract histories are possible:

- `rowHistory_marginal_eq_historyPMF` binds the fixed-seed fresh-row history distribution to the explicit micro-step PMF
- `rowHistory_true_live_ae` propagates θ membership using only positive-probability observation branches and normalized finite kernels
- `rowHistory_actionCompatible` proves generated histories are consistent with the actual policy
- `pointwise_license_implies_ae_license` lifts the resulting safety statement through the unused-stack and common-seed product factors into the canonical observed-history law

This proof applies to arbitrary measurable policies satisfying the pointwise premise, not only to the constructed controller.

## Preserved boundaries

The models, targets and observation/source laws remain fixed; Γ depends only on the exact live support. The family and action/observation types are finite. The common private seed is model independent. No arbitrary abstract behavioral-kernel realization theorem is supplied. No richer hidden plant/resource/version process, source authentication, normative authority, metaphysical ascent, historical novelty or canonical adoption follows.

The AE licence requirement is ALL-TIME safety, not eventual licensing and not a finite expected number of unauthorized actions. Early target errors must still respect the current menu. The quantitative result concerns total target-error count, not the date of the last error.

## Frozen sources and verification

`evidence/ae-equivalence-qualification-v1/SOURCE_MANIFEST.json` fixes 89 source modules. SHA256: `5a02afe216e00d5777ad0b422869bad421b73df70ef13f9695a02d8a35276a22`.

New files:

- `ObservedHistoryLicensing.lean`: `5605feee1725b4a45d47e9d481495de9b69f7bbec83834d77741e7a02c425420`
- `AELicensedEquivalence.lean`: `1a4efc42a9a182af53edc3a25b96efef555df58d2f97db486ff59acf22f00810`

The fresh author result and independent review are separate receipts. No in-progress review is represented as a pass.

## Completed verification update

Author PASS: `evidence/ae-equivalence-qualification-v1/RESULT.json`, SHA256 `c1a5d697bf16a64353a57ff3ed8a2c8a14f69ff741afe838319e52eb9450b96f` (89 source modules,82 selected readbacks, standard axioms only). Independent `PASS_SCOPED`: `../independent-audit/ae-licensing/Independent_ae_licensing_Review_20261001.zip`, SHA256 `45ad0b22e3c1f2b31fb60491a82e9ec502eb85183de62857ff1dd2511883fb36`; the archive bytes were rehashed at 04:25 UTC.
