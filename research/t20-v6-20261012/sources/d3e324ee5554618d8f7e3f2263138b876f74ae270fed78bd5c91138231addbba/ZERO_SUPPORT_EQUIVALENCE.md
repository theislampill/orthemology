# Exact zero-support restoration equivalence in one causal policy law

The separately sealed `AE_LICENSING_SCOPE.md` successor also admits almost-sure all-time licensing as the input safety contract; it preserves this87-module pointwise-licensing theorem unchanged.

Research successor, 2026-10-01. The separately frozen two-module extension `AE_LICENSING_SCOPE.md` also closes the weaker almost-sure observed-history licensing presentation, without changing the sources described here. Canonical files and all tranche-2 packets are preserved. This result extends the earlier full-support same-runner iff and the separate zero-support recorded-controller sufficiency.

## 1. Exact model and policy class

Let Θ, A, Y be finite types. The initial live family B₀⊆Θ is nonempty. For each θ and action a, Pθ,a is a nonnegative normalized distribution on Y. The hidden θ is fixed once, and feedback after each nonanticipating selected action is fresh with that action's declared kernel. Target-good sets Gθ⊆A are static. A public menu Γ(B)⊆A is supplied for every live support; menus can change arbitrarily when support changes and need not be monotone.

Histories are finite acquired action/observation records. The live support is exactly the result of successive filters

B[a,y]={λ∈B:Pλ,a(y)>0}.

Likelihood concentration does not delete a model. No hidden moving plant, private source version, consumed resource or unmodeled physical state is silently folded into B.

Fix an arbitrary measurable private-seed space R and a common probability law ρ. A policy π:R×History→A is measurable and receives no hidden θ. The experiment is the already existing `PolicyEmbedding.actionLaw`: it generates a fresh latent observation row at each physical step, reveals only the selected coordinate, and updates the acquired history. The unused row coordinates never become policy observations.

The licence contract on the policy is pointwise:

For every seed r and every finite history h consistent with π at r, if the exact live support B(h) is nonempty, π(r,h)∈Γ(B(h)).

This is a feasible-history contract. It does not demand a licensed action at an impossible empty-support history, or at an off-policy malformed action transcript. It covers every early target error as well as the eventual good actions. The same contract appears on both sides of every policy-existence statement below.

## 2. Original recursive support test

The criterion is the pre-existing `RecursiveWinning` relation and its checked equivalence with the maximal-support stage test. It is not redefined as policy existence.

For a nonempty B, first admit a∈Γ(B) only when every nonempty strict successor B[a,y] is recursively winning. Call the resulting set D(B). For each θ∈B:

- Progress: some a∈D(B) and θ-positive symbol y strictly shrink B; or
- Self-verification: there is a nonempty U⊆Gθ∩D(B) such that, whenever λ∈B has Pλ,a=Pθ,a for every a∈U, every a∈U also lies in Gλ

Equivalently, the greatest self-verifying support kernel for θ relative to B and D(B) is nonempty. The recursion only descends to proper finite subsets, so it is well founded. It treats every positive successor branch, not just successors possible under a favored model.

## 3. Principal theorems

`seeded_policy_exists_iff_recursiveWinning` proves:

There exists ONE shared measurable seeded history policy satisfying the licence contract and almost surely eventually using only Gθ actions for EVERY θ∈B₀, under the SAME canonical actionLaw,

if and only if

`RecursiveWinning P G Γ B₀`.

`seeded_policy_exists_iff_recursive_stage` substitutes the original greatest-support stage criterion without changing the policy law or quantifier order.

`finite_budget_policy_exists_iff_recursiveWinning` strengthens the existence statement: the criterion is also equivalent to existence of such a licensed shared policy with finite expected TOTAL number of target-bad physical actions in every initially live model. This is an equivalence of existence claims. It does not say that every almost-surely winning policy has finite expected error count.

The constructive policy has the explicit sharper potential-exit-chain Hellinger bound documented in `CANONICAL_SUFFICIENCY_SCOPE.md`. That bound yields deterministic physical-horizon bounds and P(total errors≥k)≤Cθ/k. It does not bound expected last-error time or give a restoration deadline.

## 4. Necessity: detailed ordinary proof and formal bindings

### 4.1 Fix one successful seed across all live models

Write the canonical action law as the image of ρ×νθ, where νθ is the actual fresh-feedback product law. This is proved by `actionLaw_raw_map`; it is not an abstract mixture hypothesis.

For each θ, almost-sure success of π under ρ×νθ implies by Fubini that, for ρ-almost every seed r, π with that seed succeeds νθ-almost surely. The live model family is finite, so the intersection of these full-measure seed sets still has measure one. Choose one r from it. The original pointwise licence contract remains valid at that r.

`common_seed_derandomization` binds this reasoning to the original actionLaw and proves that one seed works simultaneously in every live model. The necessity proof applies it to the finite subtype B₀. No seed is chosen after observing θ.

### 4.2 Every positive branch has one common winning continuation

For a fixed seed, the all-query evaluator ignores unused stacks and reads row n at physical time n. `actionLaw_dirac_eq_rowLaw` proves its exact law on iid rows alone.

`iid_cons_law` proves that an independently sampled head row followed by a fresh iid tail has exactly the original infinite iid row law. The proof derives the coordinate family independence and all marginals from the actual product measure.

Suppose the first action is a=π(r,[]) and a symbol y has Pθ,a(y)>0. The event that the first row's selected coordinate is y has exactly that positive probability. Fubini over the head-row/tail factorization gives a head row in this event with an almost-surely successful future fibre. On that fibre, the future action sequence is literally the policy with [(a,y)] hardcoded into its past, evaluated on the fresh tail. This equality is `rowHistory_cons_continuation`/`rowActions_cons_continuation`.

The hardcoded continuation is the SAME policy for every model still live after (a,y). The proof may select different unused row completions when analyzing different models, but those coordinates are not observed and do not enter the continuation policy. `deterministic_one_step_continuation` supplies this law-bound one-step result.

The exact support update and append identities preserve the licence contract. Inducting on finite history gives `fixedSeedWinning_at_history`: every feasible consistent public history yields one winning continuation for every model in its exact remaining support. This is the all-branch continuation obligation missing from a merely favorable-path argument.

### 4.3 Every same-support issued action is recursively admissible

Induct on the finite support B. Assume the necessity theorem for every proper subset. Let π at the fixed seed win from B.

At any feasible consistent history h with B(h)=B, the action a=π(r,h) is licensed by Γ(B). For any nonempty strict successor C=B[a,y], hardcoding h and then (a,y) gives a common winning policy from C by the preceding continuation result. The induction hypothesis gives RecursiveWinning(C). Thus a belongs to D(B).

The proof checks ALL nonempty strict successors of each issued action. It does not keep only the branch possible under the currently favored θ, nor infer recursive success from one eventual support. This step is internal to `fixedSeedWinning_recursive_necessity`.

### 4.4 Progress-capable candidates already pass

Fix θ∈B. If θ has a positive strict-support exit through an admitted action, the stage criterion's progress disjunct is satisfied. No positive probability of remaining forever at B is required in this case.

### 4.5 A non-progress θ remains at B and uses only D(B)

If θ has no progress witness, then every θ-positive observation after every action in D(B) preserves B exactly. This is `no_recursive_progress_preserves_support`.

Starting at B, induction on positive physical histories combines this support preservation with the all-branch admissibility of each issued action. Therefore the actual θ-action law stays in D(B) at every physical time. `fixedSeed_always_of_invariant` proves that actual-law assertion through the canonical finite-history experiment.

Consequently every θ-positive symbol of an admitted action is also positive under every live rival λ∈B. This is one-sided relative support inclusion on D(B), not global full support.

### 4.6 Relative-support finite information transfers to an actual rival

A winning finite-action path has a nonempty recurrent action set and eventually stays inside it. Partitioning by exact recurrent sets and then countably many tail cutoffs yields a positive-probability event with a fixed nonempty U⊆Gθ∩D(B), each U-action recurring infinitely, and no action outside U after some N. Intersecting with all-time membership in D(B) preserves positive probability.

For a live rival λ agreeing with θ on every action in U, all U-observations can use one common stack law. Only the finitely many actions outside U require model-specific feedback. Relative support inclusion on D(B) means every actual finite source-positive informative word remains rival-positive.

The formal chain makes this precise without claiming absolute continuity of infinite iid product measures:

- `absolutelyContinuous_of_atom_support`: relative atoms suffice on a countable finite-prefix alphabet
- `iidOracle_prefix_domination`: relative one-row support implies domination of every finite iid prefix
- `relative_finite_query_domination`: the existing finite-query factorization transfers that domination to observed traces with finitely many informative requests
- `canonical_event_eq_on_visited`: laws agreeing on D(B) give equal probabilities to measurable events whose action paths never leave D(B), proved through the zero-query restriction of the actual evaluator
- `canonical_positive_tail_on_safe_actions`: patch unused actions to the rival's law, retain equality on the source's all-D(B) event, and transfer its positive probability to the ORIGINAL rival actionLaw

Thus the positive exact-recurrence event transfers to λ. Almost-sure success under λ forces every recurrent action in U to lie in Gλ. Hence U is live self-verifying, and the greatest-support stage kernel is nonempty. This is `stable_model_self_verifying_necessity`.

Every candidate therefore passes progress or self-verification, completing the strong support-subset induction. The final seeded necessity and iff merely assemble these proved parts with the independently separated constructive policy.

## 5. Essential controls and limitations

- Initial B₀ is explicitly nonempty. Empty-support feasibility cannot silently witness a successful problem.
- The hidden θ is fixed; no step replaces it by a history-wise adversary.
- All positive strict successors are checked, even when a particular favored true model cannot take a bad branch.
- A source-positive prefix transfers only to rivals for which it remains possible. Observation zeros are not treated as positive.
- Private seed is common and model independent; its successful value is fixed once across the finite family.
- The policy never sees future feedback, and the first support-changing observation interrupts the old menu immediately.
- Dynamic safety is proved on every feasible action-consistent public history. An unrestricted behavioral-kernel realization theorem is not claimed. This exact 87-module checkpoint uses the pointwise premise; the separate 89-module AE extension proves an existence iff for almost-sure observed-history licensing.
- Arbitrary real comparisons and certificate selection are classical. Rational tests do not amount to universal Python refinement.
- Menus depend on B alone, and targets/kernels remain fixed. Richer moving-state, resource, source-version and history-dependent permission models require those variables in the state and a new theorem.
- Expected total errors is not expected last-error time. Statistical discriminability does not authenticate an observation source or confer normative authority.
- No canonical adoption, historical novelty, metaphysical ascent or meniscus promotion is inferred.

## 6. Existing source crosswalk

This directly discharges the two exclusions in tranche 2's `crosswalk/DELIVERY_INDEX.md`: the zero-support same-history-runner necessity/iff, and physical quantitative budget transfer. It combines exact observation support, target sets, public licences, causal acquired-history implementation, actual probability laws and quantitative resource accounting in one declared controlled-observation model.

The source-facing interpretation follows `tranche2/crosswalk/FRONTIER_CROSSWALK_MAP.md`: this advances the finite controlled-observation portions of M4/M6/M8/M9 and operational source/norm-class integration with P15, while preserving the separate world/source adequacy and authority/ascent burdens. The original canonical commit remains `03e2604dfcef278b01c60d19b05370fcec4194b6` and is not edited.

The residual Hellinger mechanism retains the previously recorded Dzhaparidze–Spreij–Valkeila/structured-bandit ancestry; Bellman path composition is standard dynamic programming. The contribution claimed here is the exact scope integration, policy-law closure, relative-support proof, quantitative transfer and mechanization. No historical general-mechanism novelty claim is made.

## 7. Verification state

Frozen full iff closure: `evidence/recursive-equivalence-qualification-v1/SOURCE_MANIFEST.json`, 87 modules, SHA256 `e645050892ad3e9b3f98f4735d3e62f38c5d96663411c9982f96efbabaa95eda`.

The physical-budget and Bellman predecessors have separate independent scoped passes. Canonical sufficiency v2 has an author source-only PASS across 72 modules/46 selected readbacks; its earlier v1 lint-only fail-closed receipt is retained. The full iff's fresh author and independent replay results must be read from their own receipts and are not presumed here while in progress.

Root's independent bounded-controller challenge is `tranche3/control-challenge/FINITE_MEMORY_RESULT.json`: 262,144 exact specifications and 477,738 controller/support-pattern analyses found no bounded winning controller rejected by the criterion. The 512 criterion-positive cases without a ≤3-memory-state witness are compatible with the theorem's unrestricted history memory. This search is finite evidence, not the necessity proof.

## Completed verification update

Full iff author PASS: `evidence/recursive-equivalence-qualification-v1/RESULT.json`, SHA256 `b8d9e56c9d492702e7f4b7de569ed39527ea08e7c9a4b7ca6c50c8dc11ceec31`. Independent `PASS_SCOPED`: `../independent-audit/recursive-equivalence/Independent_recursive_equivalence_Review_20261001.zip`, SHA256 `76cbb500de653620197759956b18ad0ad0d51150b9c8fa67e896595d5208e8b0`; actual archive bytes rehashed at 04:25 UTC.
