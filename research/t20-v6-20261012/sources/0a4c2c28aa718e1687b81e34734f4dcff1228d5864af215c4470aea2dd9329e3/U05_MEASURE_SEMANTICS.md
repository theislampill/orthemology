# U05 — actual measure semantics and formalisation boundary

Status: PARTIAL obligation; ordinary derivations and pinned implementation plan supplied. New kernel evidence: NONE. This note does not change any accepted source status. Exact inherited statements, predecessor IDs and preimage hashes are in `OBLIGATION_RESULTS.json`; the whole received packet is preserved under `inputs/packet/`.

## 1. Negative evidence governs the interface

The accepted logical `AlmostSureBoundary` development is retained at its mapped-native scope. Its abstract `Full` and `CompleteFull` predicates are not measures. Neither its compilation nor a finite Python census supplies the instantiation below. The original strict-wrapper compilation failure is independently preserved in the input A8R replay; it is not reinterpreted as a missing compiler. In this run, by contrast, no Lean executable is available and no new compilation was attempted successfully.

Use positive **singleton** mass, not topological support and not an arbitrary indivisible measurable set. Every result below assumes a probability measure μ on (X,Σ) with measurable singletons. Where a new map or event is used, its measurability is stated. Complete σ-algebras and standard Borel structure are not silently assumed.

## 2. P02-M01: countability and the mass definition

Put Sμ = {x : μ({x}) > 0}, a(μ)=μ(Sμ), d(μ)=1−a(μ). These are proposed actual-measure definitions of the already discussed quantities, not new replacements for the logical source.

For j≥1 the set E_j={x: μ({x})≥1/j} has at most j elements: any j+1 distinct singletons are disjoint measurable sets of total mass at least (j+1)/j>1. Every positive real singleton mass exceeds 1/j for some j, hence Sμ=⋃_{j≥1}E_j is countable. It is measurable by countable union of measurable singletons. Countable additivity gives a(μ)=Σ_{x∈Sμ} μ({x}). All terms are nonnegative and a,d belong to [0,1]. No assertion is made that the complement is empty when d=0.

In Lean, retain ENNReal values while defining restrictions, maps and countable sums; establish finiteness before converting a and d to ℝ for subtraction identities. Using truncated ENNReal subtraction without the necessary order hypotheses must not replace real subtraction arguments.

## 3. P02-M02: the all-event criterion, with the intersection issue exposed

Let (A_i) be any family of measurable conull sets. Every x∈Sμ lies in every A_i: otherwise μ({x})≤μ(A_iᶜ)=0. Thus Sμ⊆⋂_i A_i as a set, without asserting that an arbitrary intersection is measurable. For a family whose intersection I is measurable, μ(I)≥a(μ).

This lower bound is attained by the family A_x=X\{x}, indexed by all x∉Sμ. Every A_x is measurable and conull, and their intersection is exactly Sμ, which is measurable. Consequently, among all such families with measurable intersection, the least possible intersection probability is a(μ). In particular, all eligible conull intersections have probability one iff d(μ)=0; all have probability at least 1−ε iff d(μ)≤ε, for 0≤ε≤1.

An alternative formulation for arbitrary, possibly nonmeasurable conjunctions is that the conjunction contains a measurable set of mass at least 1−ε. The preceding proof supplies Sμ. Keep this formulation separately named; do not write μ(I) as though measurability had been established. When a=1, containing the measurable conull set Sμ also gives a conull-set interpretation without completing the σ-algebra.

**Restricted repertoires:** the bound remains valid, but attaining it requires the singleton-complement family to be permitted. For a merely countable family, the intersection is conull by countable subadditivity of the union of null complements, even for atomless μ. Thus neither countable syntax nor a restricted semantic repertoire licenses the rich all-event necessity direction. This accounts for Q7 rather than erasing it.

## 4. P02-M03: exact pushforward and fibre formula

Let h:X→Y be measurable, with measurable singletons on both spaces. Put ν=h_*μ. For each y∈Sν let w_y=ν({y})>0 and

    ρ_y(B)=μ(B∩h⁻¹{y})/w_y.

The fibre h⁻¹{y} is measurable, so ρ_y is a probability measure. No division at a zero-mass fibre and no general regular conditional probability are needed. If x∈Sμ then μ({x})≤ν({h(x)}), so h(x)∈Sν. On a positive fibre, ρ_y({x})=μ({x})/w_y; off it the singleton mass is zero. Partition the countable set Sμ by h and sum nonnegative terms:

    a(μ) = Σ_{y∈Sν} w_y a(ρ_y).

Since a(ν)=Σ_y w_y, subtracting finite quantities gives

    d(μ) = d(ν) + Σ_{y∈Sν} w_y d(ρ_y).

This proves the monotonicity d(ν)≤d(μ) and equality iff every positive fibre has zero defect. The iff uses w_y>0 and nonnegativity. A zero-mass fibre cannot impose such an equality condition. These are the actual-measure prerequisites reused by CV-R; a future CV-R kernel proof must import checked versions, not assume this note was compiled.

## 5. P02-M04: countable mixtures and finite carriers

For a finite or countable family of probability measures μ_i and nonnegative weights w_i summing to one, put μ=Σ_i w_i μ_i and S=⋃_{i:w_i>0}S_{μ_i}. The set S is countable. A singleton has positive μ-mass exactly when it is in S. For every active i, the set S\S_{μ_i} is a countable set of μ_i-null singletons, so μ_i(S)=a(μ_i). Therefore

    a(Σ_i w_i μ_i)=Σ_i w_i a(μ_i),
    d(Σ_i w_i μ_i)=Σ_i w_i d(μ_i).

Overlapping supports are allowed; mutual singularity is unnecessary. This is NOT an uncountable-mixture identity. Lebesgue measure is an uncountable barycentre of zero-defect Dirac laws and has defect one.

Any law on a finite or countable measurable-singleton carrier has d=0: its zero-mass singleton points form a countable null set. Probability parameters may be irrational or vary continuously; the carrier need not vary with them. This is the safe finite-support premise used in the separate U08 proposal.

## 6. P02-M05: both weak-limit obstructions, retained not newly discovered

On [0,1] with its Borel σ-algebra, the uniform measures on finer finite grids converge weakly to Lebesgue measure, by Riemann sums against continuous test functions. Their defects are zero, whereas the limit defect is one. Thus d is not lower semicontinuous, and {μ:d(μ)≤ε} is not weakly closed for any ε<1.

Conversely, uniform probability on [0,1/n] converges weakly to δ_0 by uniform continuity of each test function. Its defect is one at each stage and zero at the limit; d is not upper semicontinuous. These are preserved source obstructions to an unqualified compact safe-law domain, not a request to rerun a numerical grid experiment.

## 7. P02-M06: Q8 stays separate from measure and finite experiments

Given a machine index e, output zero at stage n unless the machine has halted within n steps; after that condition holds, output the n-th fresh fair input bit. Bounded simulation is primitive recursive, and the observer outputs a bit at every stage regardless of whether e halts. If e never halts, its law is δ_{0∞}, with d=0. If it halts, only a finite prefix is forced; the infinite independent random tail gives every singleton mass zero, so d=1. A total decision procedure for zero defect would decide nonhalting. This restricted family realises the source Π₁-type boundary; it is not by itself the full CV-C Π₃ classification.

## 8. Exact formal work remaining

The new `P02/MeasureCore.lean` candidate contains only four theorem declarations: countability, measurability, positive-point membership in a null-complement event, and the set-theoretic intersection inclusion. All are UNEXECUTED. The actual APIs for disjoint positive-measure countability were inspected at the exact mathlib commit; this is source inspection, not a declaration/type/axiom readback.

The full target sequence is: M01 support/sum identity → M02 rich and restricted event interfaces → M03 restriction/map formula → M04 countable mixtures → M05 weak convergence instances → M06 bounded-simulation reduction. Source definition compatibility, real/ENNReal conversion, countable index handling, the two weak-limit constructions and the Q8 reduction remain uncompiled. No omitted hypothesis may be discharged by changing the statement. See `PINNED_FORMAL_PLAN.md` and the fail-closed later verification commands.
