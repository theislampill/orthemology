# Finite coupling quantifiers — complete criterion and effect theorem

## C01. Definitions and quantifier order

A finite rational probability μ on X is a finitely supported map into nonnegative rationals summing to one. A coupling κ of μ on X and ν on Y is a nonnegative matrix with row sums μ and column sums ν. “Supported by R” means `κ(x,y)>0 ⇒ R(x,y)`. For an indexed family (R_i), let E be its intersection. A common coupling is exactly a coupling supported by E:

    ∃κ∈Couplings(μ,ν), ∀i, supp κ⊆R_i.

This is not implied by `∀i,∃κ_i∈Couplings(μ,ν),supp κ_i⊆R_i`. The unchanged two-point equality/flip countermodel in attempt-0001 is the minimal nontrivial probability example: each relation supports a fair coupling, their intersection is empty. Fixed-support quantifier commutation remains valid and is not being refuted.

## C02. Exact common-coupling criterion

For S⊆X let N_E(S)={y:∃x∈S,E(x,y)}. Then

    a common coupling exists
    iff ∀S⊆X, μ(S)≤ν(N_E(S)).

**Necessity.** Sum a supported coupling over rows in S. All their nonzero mass lands in N_E(S), whose total column mass is ν(N_E(S)).

**Sufficiency, constructive for rational finite data.** Form a network source→x of capacity μ(x), x→y of capacity 1 for E-edges, and y→sink of capacity ν(y). Start at zero flow and augment along a residual source-to-sink path by its minimum residual capacity. Scale all capacities by a common denominator N. Each augmentation adds a positive integer at this scale, and total flow is at most N; hence the process terminates. Reverse residual edges permit cancelling previous assignments, so no greedy irreversible matching assumption is used.

If the terminal flow F<1, let S be the reachable left vertices. Every allowed neighbour of S is reachable: an E-edge has capacity 1, and no such edge can have carried a full unit when total flow F<1. Every reachable right vertex has its edge to the sink saturated, otherwise the sink would be reachable. Every left vertex outside S has its source edge saturated, and residual reachability excludes reverse-flow crossings from unreachable left vertices into reachable right vertices. Therefore the residual cut has capacity `μ(X\S)+ν(N_E(S))=F<1`. Rearrangement contradicts the assumed inequality for S. Consequently F=1, all source and sink edges are saturated, and the x→y flows give the desired coupling.

This proof also produces a specific Hall-deficiency witness if no coupling exists. `executable/coupling.py` implements this exact rational algorithm and checks its marginal or deficiency certificate before returning. Its finite census tests the implementation; it is not the proof of the quantified theorem.

## C03. When the diagonal suffices

For a law μ on one set, Δμ(x,y)=μ(x) if x=y and zero otherwise is a coupling of μ with itself. It is common for (R_i) **iff** every positive-mass x satisfies every R_i(x,x). This condition is necessary and sufficient for this diagonal construction. It is not a necessary condition for an arbitrary common coupling between distinct laws or with an off-diagonal support; C02 is the general criterion.

For an arbitrary indexed family of relations on finite X×Y, “every finite subfamily has a common coupling” implies a common coupling for the whole family. For each pair excluded by the full intersection, choose one relation excluding it. At most |X||Y| chosen relations have the same intersection as the entire family. A common coupling for that finite subfamily works for all. This is a finite combinatorial argument, not an unproved compactness assertion. It gives no algorithm to inspect an inaccessible infinite relation oracle.

## C04. Compositional constructions

A pair of related deterministic results has a Dirac coupling. If two left/right mixture pairs use the **same** weight p and have common branch couplings κ₀,κ₁, then `pκ₀+(1-p)κ₁` is a common coupling of the mixtures. Zero-weight branches contribute no positive support. For independently sampled application children, form the product of the function and argument couplings and push it forward by `((f,g),(x,y))↦(f x,g y)`. Its marginals are the specified independent application laws, and the arrow relation gives its support property. Both constructions preserve one previously supplied common witness; they never choose a different witness after seeing a relation index.

Matching weights is a sufficient structural rule, not a necessary condition for all possible expressions to be couplable. Unequal-weight expressions may still satisfy C02. Conversely a relation whose only allowed edge is equality cannot couple distinct laws. Thus forgetting the weight hypothesis is not harmless.

## C05. Strong finite-effect abstraction theorem

Consider the same finite effect syntax evaluated under two closing term valuations θ₀,θ₁. Its pure nodes are typed finite/contextual terms; weights are fixed rational constants **independent of type/relation environments**; application subtrees use independent sampling within each run. Give each syntactic random choice node its own finite random coordinate, with the indicated rational law, and take their finite product. Unused branch coordinates may be sampled too: integrating them out multiplies by one, so this does not change the specified mixture law.

Use the **same seed** for both runs. For each seed s, the two resulting pure terms are related by the finite/dependent fundamental theorem, by induction over the shared effect syntax and its typing derivation. At a mixture the chosen branch is the same; at application use the two child induction hypotheses; All introduction changes neither seed nor erased runtime expression. Type elimination selects the explicitly interpreted endpoint relation. This proves relatedness for every required relation environment with the same seed pairing.

Push the seed law forward to the pair of results. The resulting κ has the two execution laws as marginals. Since its construction contains θ₀,θ₁ and the fixed syntax/weights but **no relation index**, it is a common coupling across all environments for which those fixed valuations satisfy the input relation. The order is

    fixed syntax, weights, θ₀,θ₁
    → ∃κ
    → ∀admissible relation environments r, supp κ⊆Rel_A(r).

For an actual closed accepted EffectDerives expression, θ is empty and the same-run coupling is its diagonal after equal outcomes are aggregated. The predecessor's per-outcome theorem supplies the finite pure typing at every support point. This completes the distributional/coupling extension at the actual finite grammar; it does not quantify over general stochastic programs or value-dependent bind.

## C06. Observational consequence and its boundary

Let obs₀:X→O and obs₁:Y→O obey `R(x,y)⇒obs₀(x)=obs₁(y)`. A coupling supported by R pushes forward to a diagonal law on O×O. Therefore the two observed marginal laws are exactly equal, by finite summation. A common coupling gives this result for every such specified observation relation. Composing a well-typed finite context preserves relatedness by the abstraction theorem, so the result is contextual for these typed contexts and relation-respecting observations.

An observer that distinguishes the literal raw normal forms I and S K K is not respectful of a function PER equating them. No equality-of-observations claim is made for it. No empirical/physical observation, outside implementation, continuous measure or P02/P03 result is needed or presumed.
