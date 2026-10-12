# Direct computable bounded-moment continuation does not require indexed recovery

Participating derivation, 10 October 2026; submitted to the author and independent reviewer. This is an effective consequence of the explicit compact-support exponential series already present in `measure-moment-continuation-boundary-20261009/RESULT.md` §3, not a new compact moment-determinacy theorem.

Let κ take values in the finite simplex Δ_m. Supply a uniform name of every tensor moment M_r=E[κ^⊗r]. The underlying law may have infinitely many labels, noncomputable individual label masses, or a general measurable carrier. No indexed cap is required in this paragraph. Supply a computable finite u∈R^m and a computable rational B≥||u||∞. Put Z=E[e^(−u·κ)]. Then Z≥e^(−B)>0.

For each requested output grade s, define tensor numerator A_s=E[κ^⊗s e^(−u·κ)]. It has the series

A_s = Σ_(r≥0) ((−1)^r/r!) contraction_(u^⊗r)(M_(s+r)).

The normalising scalar is A_0=Z, and the updated moment is A_s/Z. Every coordinate of κ^⊗s is in [0,1], including s=0. Taylor's remainder for exp at |u·κ|≤B therefore bounds the maximum-coordinate error after r≤R by

e^B B^(R+1)/(R+1)!.

This bound is uniform over all initial laws, all output coordinates, and s. It converges effectively to zero from the given finite B. Finite contraction sums are computable from the finite set of required moment names, and division by the supplied positive lower bound for Z is computable. Consequently all updated grades have a uniform computable name. No optimal truncation, stability under arbitrary unknown measurement error, finite-sample procedure or empirical model identification is claimed.

The same operation composes along the existing tilt group on bounded support. Computing a finite endpoint requires only the integrated control u; computable bounded controls and their computable integral supply such u. This does not assert that every abstract or merely measurable control has a computable integral.

## Why this matters for the new cap bridge

An effective cap enables recovery of the full *indexed* law in l1. That is a stronger output interface than the original bounded κ-moment continuation. It must not be presented as a prerequisite for the weaker task. The proposed no-effective-tail example can have computable all-order moments and computable bounded-moment continuations while retaining a noncomputable individual label mass. This separates two real computational tasks without denying the usefulness or faithfulness of the original moment representation.

Unbounded observables, such as an unrelated label cost or −log of a bounded coordinate approaching zero, do not satisfy this remainder argument. Recovering a computable indexed law would not alone make every such expectation computable either; suitable effective integrability is additional data.

A separate reviewer identified an especially sharp bounded-query distinction: in the no-tail example, the indexed observable 1_{j=0} is bounded and computable on N, yet its expectation p0 is noncomputable. It corresponds to a discontinuous observable at the accumulating support point κ0, so it is not a bounded continuous function of κ licensed by the moment continuation. Thus even the adjective 'bounded' must retain the declared observation interface. An l1-name of p plus a uniformly computable bounded indexed observable with a supplied bound would compute its expectation; the cap-free moment interface cannot claim this general indexed-query guarantee.
