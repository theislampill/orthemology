# Zero-support canonical causal sufficiency and physical error budgets

This is the preserved constructive checkpoint. The current full necessity/iff successor is documented in `ZERO_SUPPORT_EQUIVALENCE.md`; its separate receipts govern that stronger claim.

## Principal theorem

`Orthemology.Tranche3.recursive_certificate_canonical_policy_exists` in `lean/RecursiveCanonicalSufficiency.lean` proves the following statement for finite model/action/observation types, normalized nonnegative controlled-iid laws P, static target sets G, a public menu Γ(B) depending on the exact live support, a supplied initial support B₀, and the existing combinatorial `RecursiveWinning P G Γ B₀` certificate.

For any common private-seed probability law ρ, there is ONE measurable policy π(seed, acquired finite action/observation history) such that:

1. On every action-consistent history whose exact live support is nonempty, the next issued action belongs to Γ of that support. This includes every early target error.
2. For every θ in B₀, the expected total number of target-bad physical actions in the original `PolicyEmbedding.actionLaw π ρ (P θ)` is at most the explicit finite potential-exit-chain Hellinger budget Hθ(B₀).
3. Under that same action law, only finitely many target-bad actions occur almost surely.

The policy existential precedes the universal model quantifier. The policy ignores its seed; θ is absent from its definition. The theorem assumes neither a winning policy nor a policy representation, runner law equality, drift inequality, progress premise, likelihood convergence assertion, phase-rank premise, or physical-clock premise. These are constructed or proved internally. Zero observation probabilities, unequal/multi-action plans, support-dependent nonmonotone menus, and immediate first-exit interruption are retained.

## Exact semantic dependency map

### 1. Finite causal execution

`CausalActionTree.lean` defines a finite tree whose node contains an action chosen before the next observation, and whose Y-indexed children are selected only after that observation arrives. `stopTree` unfolds the existing `StopObs` protocol into this tree. `stopTree_value_eq_stopped_sum` proves that its sequential expected cost plus terminal value equals the sum under the original stopped-prefix mass. The exit-triggering action is included; the old unexecuted suffix is absent. `stopTree_value_le_planned` then bounds its actual-prefix charge by the prior whole-plan charge.

`replayObserved` folds acquired observations through the current residual tree, restarting with a fresh macro tree only at a leaf. The policy's next action is this reconstructed root action. Recorded past action fields are ignored by the replay, but the safety theorem explicitly requires `ActionCompatible`; this binds those fields to the action actually issued by the policy. No off-policy or empty-support licensing assertion is made.

### 2. Canonical law binding

`CanonicalHistoryPMF.lean` constructs the finite physical-time history PMF by starting at [] and repeatedly binding the selected action's normalized observation PMF. Its exact singleton formula is compatibility times the product of the acquired observation probabilities, with the correct history length.

`CanonicalHistoryBudget.lean` identifies that finite PMF with the ORIGINAL canonical fresh-row history marginal using the previously checked `history_marginal_formula`. It also proves that the finite physical action-prefix cost is exactly the cost of the acquired history. Therefore the finite PMF expectation is literally the corresponding original actionLaw expectation. An ENNReal monotone-series argument proves `canonical_total_cost_of_drift`; no limiting-law equality or independence assumption is supplied.

### 3. Finite-prefix normalization and the zero guard

For macro state (B,h), let mθ(B,h) be the killed-history likelihood under θ, Vθ(B,h) the prior weighted Hellinger potential, and Dθ(B) the Bellman continuation allowance. Define

Fθ(B,h) = Vθ(B,h) / mθ(B,h) + Dθ(B) when mθ(B,h)>0; otherwise 0.

This conditions only on an already acquired finite prefix. It does not condition observation laws on a future no-exit event.

`NormalizedResetPotential.normalizedResetPotential_step` derives

plannedBad(B,chosen) + Σw Kθ(w) Fθ(actualResetUpdate(w)) ≤ Fθ(B,h)

from the existing unnormalized drift and Bellman exit allowance. Continuing positive branches have new mass mθ·Kθ>0. Positive exit branches use the certified smaller support and empty likelihood history. Zero-probability branches contribute exactly zero and require no fictitious continuation invariant.

`RecursiveMacroPotential.lean` discharges every abstract premise from P≥0, normalization, the recursive certificate, and the checked stopped Hellinger estimate. `recursiveMacroValid` explicitly means θ remains live AND mθ>0. `recursiveMacroValid_next` propagates it on every positive-probability stopped record. The root potential equals the explicit chain budget.

### 4. One physical observation at a time

`CausalTreeLaw.actionTreePolicy_total_cost` uses tree value as the physical-step potential. On a residual node, expected next-tree value is the recursive tree value. At a macro leaf, the new spawned tree value is bounded by Fθ at that leaf. Thus the one-step potential pays the literal current action cost. Its validity condition follows only positive observation branches. It invokes the proved canonical-history drift theorem.

`RecursiveCausalPolicy.lean` supplies the actual recursive macro update, MLE selector, stopped plan, weights and normalized potential. `recursiveHistoryPolicy_actionLaw_total_bad_budget` is the resulting quantitative canonical endpoint. Almost-sure eventual goodness follows from the finite expected total integer charge.

### 5. Exact dynamic menu safety

`RecursiveHistorySafety.lean` computes `historySupport` by actual sequential support filtering. `LicensedTree` tracks the support before EVERY physical action. Positive continuation observations preserve B; the first exit changes it to the actual filter and immediately resets. Completion preserves B. `recursiveHistoryPolicy_licensed` proves the licence contract on every feasible action-consistent finite history, uniformly in the seed and without waiting for eventual target correctness.

## Quantitative constant and its scope

For each certified support phase B and offered candidate σ, the local weight is

wθ(B,σ) = cθ(B,σ)/(1−rθ(B,σ))

when θ is live and the planned target-bad action count cθ(B,σ)>0, otherwise 0. The residual affinity r is computed on COMPLETING mass, retaining the full exit mass in the full experiment. Certificate lemmas prove the relevant denominator is strictly positive.

Let Lθ(B)=Σσwθ(B,σ). The finite directed graph has an edge B→C when some offered plan has a positive-probability first exit under θ to C. All actual exits are included. Some edges may be MLE-unreachable, so the graph is conservative. Its rank strictly decreases.

Hθ(B)=Lθ(B)+max(0,max over edges B→C of Hθ(C)).

`phaseChainBudget_le_supersolution` proves leastness ONLY among additive local-cost/edge supersolutions. It does not prove policy optimality, an exact expected cost, or leastness among all probabilistic estimates. `recursiveChainBudget_le_global` proves Hθ never exceeds the prior `(rank+1) × Σall-phases Lθ` constant.

The count tail bound is P(total bad actions≥k)≤Hθ/k. No expected last-error time, deadline, or stopping-time certificate is asserted. For example, exactly one error at time 2^K with P(K=k)=2^(-k), k≥1, has total count 1 but infinite expected error time.

## What is and is not closed

Closed here: a literal canonical finite-history policy for the zero-support support-menu model, all feasible-history licences, expected total physical bad-action cost, and almost-sure restoration. This strengthens the previously distinct recorded-runner constructive endpoint.

Still open here: general zero-support seeded-policy NECESSITY and a literal recursive iff. No equality between the recorded physical pushforward law and the new canonical law is asserted or needed by this proof. Both use the same offered-plan/first-exit mechanism, but the canonical result is proved directly through finite physical histories.

Classical real comparisons and certificate witness choice remain explicit. The exact rational experiments are controls, not a universal Python-to-Lean refinement. No moving plant, history-dependent resource/version menus, arbitrary source switch, normative/source authority, historical novelty, metaphysical ascent, canonical adoption or meniscus promotion follows.

## Frozen source boundary

`evidence/canonical-sufficiency-qualification-v2/SOURCE_MANIFEST.json` fixes the 72-module transitive closure. SHA256: `6774f8d2437528d3a02965ab0ea7a0d805cdc7c661ddb117834e88ef6ad835f2`.

The prior physical-cost and Bellman packets remain byte-identical and independently reviewed. The source-only canonical qualification and independent review results are recorded separately; no in-progress review is represented as a pass.

The preserved v1 author run failed closed at module 70 solely on an unused-section-variable linter warning; proof compilation succeeded. Version 2 inserts only `set_option linter.unusedSectionVars false` into the nine canonical-delta modules. No proof, theorem statement, or prior sealed source was changed for this correction.
