> Retained incoming research text. Verification claims below describe the original packet. See the [current evidence status](../RESULT_STATUS.json) and [original-to-public source map](../SOURCE_MAP.json). Packet navigation is rendered as text; spaced path separators denote original packet locators.

# Independent review: almost-sure observed-history licensing

**PASS_SCOPED.** This separate successor binds the author's 89-module manifest SHA256 `5a02afe216e00d5777ad0b422869bad421b73df70ef13f9695a02d8a35276a22`. The 87 predecessor source/object pairs were verified against this reviewer's recursive-equivalence replay and subsequently sealed audit, SHA256 `76cbb500de653620197759956b18ad0ad0d51150b9c8fa67e896595d5208e8b0`. Only the two new files were freshly compiled here. Every custom object originates in the independent copied-source audit chain; author custom objects are excluded. Official dependency objects remain the pinned trusted cache. The full direct-import closure and current author source hashes were checked again.

The two main endpoints are `ae_licensed_policy_exists_iff_recursiveWinning` and `ae_licensed_finite_budget_exists_iff_recursiveWinning`. They preserve the finite-model, finite-action, finite-observation controlled-iid, common-seed, nonempty-initial-support, and support-menu scope of their predecessor. They replace the pointwise licensing premise with an almost-sure all-time event in the **observed-history law**. The eventual target-success event remains in the original action law.

## Semantic review

`LicensedHistoryPath` reads the selected action at time n from the head of H(n+1), and licenses it against the live support computed from H(n). This is the before-action support. The countable finite-history space makes its predicate measurable; the infinite event is a countable intersection. An arbitrary action-only path generally loses the observations needed to recover those supports, so the different observable law is necessary.

`common_seed_success_and_history_event` pulls both safety and goodness back to the same raw seed/feedback product, intersects them, and then uses Fubini and the finite model intersection. Its witness is one seed jointly safe and successful for every initially live model. It does not separately select a safe seed and a successful seed, and does not change the seed after conditioning on data.

For that fixed seed, `rowHistory_marginal_formula` is an actual canonical-law cylinder formula: the history has the specified length, the seed satisfies action compatibility, and its mass is the product of selected observation probabilities. Membership of a model in the computed support gives strict positivity of every factor. Thus every feasible action-consistent history has positive cylinder mass in **each** of its surviving models. Almost-sure all-time safety then supplies a safe path inside this cylinder, whose action is exactly the policy's action at that history. This recovers pointwise feasible-history safety for the chosen seed and permits the previously audited necessity induction.

The reverse implication proves that the true model remains live at every actual finite history almost surely under arbitrary measurable policies. It uses the exact finite history PMF and its positive transitions; impossible symbols are not assumed absent on every raw input. Action compatibility is deterministic on generated histories. Pointwise feasible-history licensing therefore implies the actual observed-history licensing event almost surely.

## Boundaries and controls

The original randomized policy can still violate a license on a null seed. No theorem upgrades all its seeds or impossible histories. Nine independent Lean controls include a literal Dirac-seed observed-history law that is almost surely licensed, while another null seed of the same policy chooses an unlicensed action. Other controls prove positive feasible history mass, incompatible forged action records, distinct live supports behind identical action projections, and the exact before-action support convention.

Exact rational enumeration verifies 10,044 fixed-seed cylinder masses and 5,022 live-support histories, including zeros. A changing-menu example rejects checking a just-issued action retroactively against its post-observation support. Five source mutations fail: using post-action support, dropping action consistency, replacing surviving-model membership by initial membership for positivity, discarding history safety during joint seed selection, and reading the action before it is recorded.

Every public declaration in both new files has exact type/body/axiom readback, with only standard Lean axioms. The first independent control attempt had reviewer-only namespace/type annotation failures, retained in `CONTROL_ATTEMPT1.log`; the corrected controls compile without warnings. Neither authors' source nor earlier audit seals were changed.

The finite-budget endpoint remains an existence equivalence; it does not establish finite expected errors for every almost-sure winner. It also does not assert finite informative observation use, a last-error time bound, source-code implementation, or authority for the supplied licensing menu. Finite executable controls are corroboration, not universal Python-to-Lean refinement.
