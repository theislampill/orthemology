# CV-R — exact finite and infinite refinement debt

Status: PARTIAL obligation. This note is an ordinary mathematical derivation and a formalisation decomposition, not kernel evidence or adoption. It preserves the provisional source theorem, including its extinction residual. No other packet's new result is assumed.

## 1. Statement and hypotheses

Let (Ω,𝔽,μ) be a probability space. For n≥0 let Y_n:Ω→Q_n be measurable, with each Q_n having measurable singletons, and measurable h_n:Q_{n+1}→Q_n satisfying Y_n=h_n∘Y_{n+1}. With almost-everywhere coherence, all equalities below are interpreted outside the one common null set obtained from the countable family of exceptions; finite/full laws are unchanged. Coordinate spaces need not have identical carriers.

Let ν_n=(Y_n)_*μ, S_n its positive-singleton set, A_n=Y_n⁻¹S_n, a_n=μ(A_n), d_n=1−a_n. For each y∈S_n, define the probability law ρ_{n,y} of Y_{n+1} restricted to h_n⁻¹{y}, divided by w_{n,y}=ν_n({y}). Put

    Δ_n = Σ_{y∈S_n} w_{n,y} d(ρ_{n,y}) ≥ 0.

Let Y∞(ω)=(Y_n(ω))_n, into the countable product measurable space; its singletons are countable intersections of coordinate singleton inverse images. Let A∞ be the pullback of the positive-singleton set of its law. Set A*=⋂_n A_n and J=μ(A*\A∞).

The exact source target is

    d_N=d_0+Σ_{n<N}Δ_n,
    d∞=d_0+Σ_{n≥0}Δ_n+J.

The U05 measure instantiation is a shared formal predecessor, not an already compiled theorem in this run.

## 2. Ordinary proof decomposed into small formal targets

**P02-R01 (decreasing events).** A positive fine singleton is contained in its coarse fibre, so its coarse mass is at least its fine mass. Hence A_{n+1}⊆A_n. A positive full singleton is contained in every coordinate fibre, so A∞⊆A*.

**P02-R02 (one-step and finite telescope).** U05-M03 applied to h_n gives d_{n+1}−d_n=Δ_n, equivalently μ(A_n\A_{n+1})=Δ_n. Summing N equalities gives the finite formula. The partial sums increase and are bounded by 1−d_0, so their real infinite sum exists.

**P02-R03 (limit decomposition).** Continuity from above for the decreasing measurable A_n, with μ(A_0)≤1, gives μ(A*)=lim a_n. Since A∞⊆A*, μ(A∞)=μ(A*)−J. Substituting a_n=1−d_n and the finite telescope gives the infinite identity. This uses a separate measurable event A∞, not an unjustified assertion that A*=A∞.

**P02-R04 (cell masses).** For fixed ω let C_n(ω)={ω':Y_n(ω')=Y_n(ω)}. Coherence makes these sets decreasing. Their intersection is the full-history fibre of ω, hence

    m_n(ω)=ν_n({Y_n(ω)}) ↓ μ(⋂_n C_n(ω))=m∞(ω).

The function x↦ν_n({x}) is measurable because its positive set is countable and it is the countable sum of weighted singleton indicators. Thus the cell-mass events below are measurable. We have A_n={m_n>0}, A∞={m∞>0}, and

    J=μ({ω: every m_n(ω)>0, but lim_n m_n(ω)=0}).

For ε>0, the indicators of {0<m_n<ε} converge pointwise to the indicator of A*∩{m∞<ε}: a zero cell, once reached, persists; a decreasing positive sequence either stays at/above ε or eventually goes below ε. Dominated convergence and then continuity from above imply

    J = lim_{ε↓0} lim_{n→∞} μ({0<m_n<ε}).

The order is essential: at each fixed n the inner limit as ε↓0 is zero, so reversing the limits yields zero, even when J=1.

**P02-R05 (martingale distinction).** I_n=1_{A_n} is adapted to σ(Y_n), takes values in [0,1], and decreases pointwise, hence E[I_{n+1}|σ(Y_n)]≤I_n. It is a supermartingale, not generally a martingale. The actual martingale is M_n=E[1_{A∞}|σ(Y_n)]. Because A∞ belongs to σ(Y_0,Y_1,...) and the σ-fields increase, conditional-expectation convergence gives M_n→1_{A∞} almost surely and in L¹. The terminal gap I_n−M_n tends to 1_{A*\A∞} almost surely and in L¹, with limiting expectation J. This last standard convergence step is an ordinary dependency explicitly left for the pinned formal development; it is not needed for R03's elementary proof.

## 3. Retained negative and a new joint-debt witness

The source's fair-bit-prefix example has a_n=1 and Δ_n=0 at every finite stage but an atomless full law, so d∞=J=1. It already refutes dropping J. It is preserved as evidence, not presented as a new discovery.

**P02-R06, proposed mixed witness:** take a disjoint probability mixture of three tagged components, with weights 1/4, 1/3 and 5/12. The first has one fixed output. The second carries a uniform [0,1] value. The third carries a fair infinite bit stream. At stage zero observe only the tag. At stage n≥1 observe the tag, reveal the complete real value on the second component, and reveal the first n bits on the third. Coarsening discards the extra observations; all maps are measurable on the disjoint-sum/product spaces.

Then d_0=0, Δ_0=1/3, Δ_n=0 for n≥1, and d_n=1/3 for every n≥1. The full law retains only the first component's atomic mass 1/4, so d∞=3/4. The extinction residual is exactly 5/12, furnished by the third component. Thus a budget ε=1/2 is respected at every finite stage and exceeded by the full-history law. This example separates one-step diffuse exposure from positive-cell extinction; it does not replace the earlier counterexample or assert a physical application. Fraction arithmetic was checked; the infinite-law conclusion comes from the ordinary argument above, not those checks.

## 4. P02-R07: exact certificate transport

Suppose an initial semantic certificate states d_0≤ε with 0≤ε≤1, and write slack=ε−d_0. The finite transport condition is exactly Σ_{n<N}Δ_n≤slack. The full-history condition is exactly Σ_nΔ_n+J≤slack. Necessity for arbitrary almost-sure conjunction certificates additionally uses U05's rich-event premise; for restricted repertoires only the stated sufficient bound transfers unless richness is separately proved.

A certificate's semantic truth and its artifact/version validity are different. No source hash, checker identity, epoch or owner acceptance follows from the inequality. An engineering system may invalidate a stale certificate even when the semantic inequality is true; this note does not modify that policy.

## 5. Remaining formal boundary

The full CV-R Lean development is not supplied. R01–R04/R07 have precise ordinary proofs; R05 additionally requires the conditional-expectation convergence theorem with an exact pin and hypotheses. The formal plan lists restrictions, sums, product measurability, continuity from above, limit interchange and the rich-event application separately. No formal count, source-status promotion or historical criticism closure is granted.
