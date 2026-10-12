# U08 — a concrete finite-support correspondence, with separate effectivity

Status: PARTIAL obligation. An actual set-valued proposal and full ordinary hypothesis map are supplied. An appropriate **pinned Lean Kakutani development has not been identified or executed**. The general formal obligation is not closed by the following restricted family.

## 1. Preserved boundary

The source's solved singleton map on [0,1], p↦{(1−p²)/2}, and its separate contraction/sampling arguments remain intact. A solved singleton instance is not a general correspondence theorem. The source also preserves failure of unrestricted weakly closed safe-law domains. U05's finite-grid example still defeats compactness of {ν:d(ν)≤ε} for ε<1. Neither issue is repaired by renaming an unsafe domain.

## 2. P02-F01 — proposed actual domain and map

Choose m≥1 fixed outcome labels t_1,...,t_m in a measurable-singleton space (in particular, a finite discrete carrier) and the simplex

    K=Δ_m={p∈ℝ^m : p_i≥0 and Σ_i p_i=1}.

For each i fix a nonempty compact convex set R_i⊆Δ_m. Define

    F(p)={Σ_i p_i r_i : r_i∈R_i for every i}.

Its law interpretation is L(p)=Σ_i p_i δ_{t_i}. Every L(p) is supported on finitely many outcomes and has singleton defect zero. The labels need not be distinct for this assertion. If they are claimed to be certified programs, their typing/certificates are explicit **additional supplied premises**; this proposal neither produces them nor consumes an unreturned result of another packet.

This is a new proposed restricted safe envelope. It does not alter an accepted definition of all safe measures or claim to include every admissible semantic law.

## 3. Complete match to a stated existing fixed-point theorem

Primary reference: Y. Shmalo, *Combinatorial Proof of Kakutani's Fixed Point Theorem*, arXiv:1811.08454v1 (2018), Definition 2.4 and Theorem 2.5, inspected in HTML. Its theorem applies to an upper-semicontinuous map from a finite-dimensional simplex to nonempty compact convex subsets of that simplex. The present map meets those hypotheses as follows.

K is nonempty (any vertex), convex, closed and bounded in finite-dimensional Euclidean space, hence compact. It is affinely a simplex of dimension m−1; m=1 is the trivial singleton case. A tuple of rows in ∏_iR_i exists and produces an element of F(p), proving nonemptiness. Every such element is nonnegative with coordinate sum one, so F(p)⊆K. The finite product ∏R_i is compact, and the weighted-sum map is continuous, so F(p) is compact. Convexity follows by taking convex combinations row by row.

For upper semicontinuity, use the same witness rows at p and q. Since each row has ℓ¹-norm one,

    ||Σ_i p_i r_i − Σ_i q_i r_i||₁ ≤ Σ_i |p_i−q_i| = ||p−q||₁.

Thus the Hausdorff distance between F(p) and F(q) is at most ||p−q||₁. Finite-dimensional norm equivalence supplies the neighbourhood formulation of upper semicontinuity. All hypotheses of the cited simplex theorem are now discharged ordinarily, so some p*∈F(p*) exists. This is an application of an existing theorem; no fixed-point novelty is claimed.

There is also a direct check of existence for this particular family: choose one row r_i from each nonempty R_i, forming a stochastic matrix R. Starting from any law p, the Cesàro averages N⁻¹Σ_{k<N}pR^k have a convergent subsequence in K. Their difference after multiplication by R is (pR^N−p)/N, tending to zero, so the limit is stationary and belongs to F at itself. This is an ordinary finite-dimensional argument, not a replacement for the requested pinned proof evidence.

## 4. P02-F02 — a genuinely set-valued example

For two outcomes, write p as the probability of outcome 1. Let row 0 assign that outcome any probability in [1/4,1/2], and row 1 any probability in [1/2,3/4]. Then

    F(p)=[1/4+p/4, 1/2+p/4].

The fixed-point condition is equivalent to p∈[1/3,2/3]. In particular p=1/2 is stationary for rows of biases 1/4 and 3/4. Values are generally intervals, not singletons. This defines an actual correspondence rather than postulating that an unknown application satisfies Kakutani.

No convergence follows for arbitrary selections: another allowed row family, with row-0 bias 1 and row-1 bias 0, gives F(p)={1−p}. Its unique fixed point is 1/2, but iteration starting at 0 alternates 0,1 forever. The original contraction result is therefore preserved at its narrower scope.

## 5. P02-F03 — rational-polytope effectivity, separately proved

Add exact finite rational data for each row set:

    R_i={r∈Δ_m : A_i r≤b_i}, with R_i nonempty.

Introduce nonnegative flow variables f_ij and probabilities p_i, constrained by

    Σ_j f_ij=p_i,       Σ_i f_ij=p_j,       Σ_i p_i=1,
    A_i f_i≤b_i p_i.

This is a finite rational linear feasibility problem. A fixed point p with witness rows r gives f_ij=p_i r_ij and satisfies every constraint. Conversely, from a feasible (p,f), define r_ij=f_ij/p_i when p_i>0. For p_i=0, nonnegativity and the row-sum equation imply f_i=0; choose any row in the nonempty R_i. Dividing the inequalities for active rows proves r_i∈R_i, and the column sums yield p=Σ_i p_i r_i.

The feasible region is nonempty by F01, closed and bounded by the probability and flow constraints, and rational. A nonempty bounded rational polyhedron has a rational vertex: at a vertex choose a full-rank subsystem of active rational equations, then solve it by rational elimination. This also gives a finite algorithm: enumerate possible active constraint sets, solve full-rank systems, and test every constraint exactly. It is not claimed efficient. The algorithm and its formal proof are implementation proposals, not executed LP or Lean code in this checkpoint.

The resulting rational stationary law has an exact almost-surely terminating fair-bit sampler, for example the interval-comparison construction in the CV-C note. That sampler is not a claim that all samples halt under every infinite input stream.

## 6. P02-F04 — general semantic existence is not a sampler

Outside the rational-data contract, a singleton correspondence constantly equal to a noncomputable bias r has a semantic fixed point and satisfies the topological hypotheses, but no finite-description, oracle-free, almost-surely terminating fair-bit sampler for that Bernoulli law exists. Each terminal outcome probability of such a sampler is lower semicomputable by enumerating its accepting finite prefixes. Because the two probabilities sum to one, dovetailing their approximations computes r to any requested rational precision, a contradiction.

This obstruction concerns unrestricted real data; it does not deny effectivity of the rational-polytope family or the particular computable irrational bias in the source. A pinned general theorem, computable representation and sampler contract are separate dependencies.

## 7. Exact unresolved items

Read-only mathlib discovery returned Riesz–Markov–Kakutani representation material, not an identified fixed-point declaration at the requested pin. Search incompleteness is not proof that no such library exists. No replacement library version was adopted. The original 1941 paper's full text was not recovered through the tried route; the explicitly inspected primary restatement above is the theorem used.

Required later work: owner review of the proposed finite safe envelope; a verified exact-pin Kakutani dependency or a separately reviewed formal proof of this restricted family; formal compactness/convexity/continuity/flow equivalence; and, if requested, exact rational feasibility and sampling implementation. There is no repository change, policy adoption, generic effective selector or self-certification claim here.
