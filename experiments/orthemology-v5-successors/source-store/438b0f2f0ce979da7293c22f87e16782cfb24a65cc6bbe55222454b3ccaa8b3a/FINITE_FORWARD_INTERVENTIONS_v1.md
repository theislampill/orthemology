# Exact finite forward intervention semantics

4 October 2026 UTC. Correction-driven ordinary mathematical supplement. Existing accepted files are unchanged. This supplements the fixed sample space and finitely additive Gaussian path law in the independent review; no code, new general programme, or physical realisability result is supplied.

## 1. Baseline and one replacement

Use Ω=R×R^Z with coordinates (x,ξ), X_0=x, and

X_t=x+Σ_(k=0)^(t−1) ξ_k for t>0,
X_t=x−Σ_(k=t)^(−1) ξ_k for t<0.

Thus ξ_j takes X_j to X_(j+1). The baseline probability μ is the accepted real-valued finitely additive law on Borel Ω. Every recurrence holds pointwise. Its noise marginal is the ordinary countably additive iid Gaussian product Q, and its full past state/noise sigma-field F_t is rectangle-independent of its future noise sigma-field G_t.

Fix one integer j and one real replacement value a. Put Δ=a−ξ_j and define T_(j,a):Ω→Ω by

ξ′_j=a;  ξ′_k=ξ_k for k≠j;
x′=x+Δ if j<0, and x′=x if j≥0.

This map is Borel: only one noise coordinate and the anchor change, by Borel coordinate operations. Substituting into the finite sums gives, for every integer t and every sample,

X′_t=X_t for t≤j,
X′_t=X_t+Δ for t>j.                                    (1)

For j<0 the anchor adjustment is essential. Without it, overwriting ξ_j in an anchored parametrisation would change earlier states instead of preserving them. Including it gives exactly the stated forward intervention.

Equation (1) preserves the entire prehistory through X_j. At the selected step,

X′_(j+1)−X′_j=ξ_j+Δ=a=ξ′_j.

At every other step both adjacent states have the same displacement, so their difference remains ξ′_k=ξ_k. Therefore all recurrences hold pointwise after the intervention.

## 2. A finite family and composition

Fix a finite set J⊆Z and prescribed real values a_j for j∈J. Put Δ_j=a_j−ξ_j, computed from the original sample. Define T_(J,a) by

ξ′_j=a_j for j∈J, and ξ′_j=ξ_j otherwise;
x′=x+Σ_(j∈J,j<0) Δ_j.

All sums are finite, so this is Borel. Direct substitution gives

X′_t=X_t+Σ_(j∈J,j<t) Δ_j.                              (2)

For nonempty J, every state with t≤min J is unchanged. At every step k the displacement difference in (2) is exactly Δ_k when k∈J and zero otherwise, proving X′_(k+1)=X′_k+ξ′_k for all k. The empty set gives the identity map.

Single-coordinate replacements at distinct times commute: each displacement uses a noise coordinate untouched by the other operation, and negative-time anchor corrections add. Consequently any order of the finitely many distinct replacements produces T_(J,a).

A repeated replacement at the same coordinate by the same value is idempotent. Two replacements at the same coordinate by different values do not commute; the last replacement wins. More generally, finite maps with overlapping target sets commute when their prescribed values agree on overlaps. These qualifications are part of the composition statement.

## 3. Pushforward laws and the properties actually preserved

Define the intervened law by

μ^(J,a)(A)=μ(T_(J,a)^−1(A))

for every Borel event A⊆Ω. Borel preimages preserve finite unions, disjointness and the whole space, so this is again a normalized, nonnegative, real-valued finitely additive probability. Its paths satisfy every recurrence pointwise. The construction is an overwrite/pushforward, not conditioning on the Gaussian-null event ξ_j=a_j.

The entire noise marginal is exactly Q pushed through the coordinate replacements. It is an ordinary countably additive product law: coordinates in J are point masses at their prescribed a_j, and all other coordinates remain independent N(0,1). Thus the targeted innovations no longer have their original Gaussian marginal, as intended; the unmodified coordinates retain their joint product law.

Full past–future factorisation also survives in the appropriate intervened variables. For a fixed time t, equation (2) shows that every transformed past state X′_s, s≤t, is measurable with respect to the original F_t: its added terms only use ξ_j with j<s≤t. Transformed past noise also belongs to F_t. Every transformed future noise variable, indexed j≥t, is either its unchanged original coordinate or a constant, and so is measurable with respect to the original G_t. Original rectangle independence of F_t and G_t therefore proves independence of the intervened full past state/noise sigma-field from the intervened future noise sigma-field.

The accepted baseline law is spatially translation-invariant. These finite maps commute with a common spatial translation of the anchor and all states. Their pushforwards are therefore spatially translation-invariant as well. In particular every bounded position interval still has probability zero: arbitrarily many disjoint translates of such an interval have equal mass, and finite normalization forces that mass to vanish. No bounded-capture guarantee is created by these fixed finite replacements. Fixed selected times can break time stationarity; no time-stationarity preservation is asserted.

## 4. Exact positive grant and its limit

The model admits explicit, composable finite forward intervention semantics that hold its prehistory fixed and change the selected innovation and subsequent states. Anchored coordinates do not obstruct that positive mathematical construction. This is more than merely checking a statistical independence identity: the maps are supplied additional structure with exact counterfactual trajectory effects.

The family is for finitely many prescribed target times and fixed replacement values. No arbitrary infinite-past replacement operation is asserted. With infinitely many negative target times the required anchor-displacement sum may diverge, and defining a Borel path map or a pushforward law would require additional hypotheses. No claim about state-dependent, adaptive, or future-dependent replacement policies is silently included either.

This mathematically specified intervention family does not by itself establish actual manipulability, physical implementation, productive causal direction in the world, or metaphysical realisability. Those are separate interpretation and warrant questions. Conversely, the use of an anchor in the original parametrisation is not a valid mathematical reason to deny this finite forward-intervention family.
