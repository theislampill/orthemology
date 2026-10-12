# CV-R — finite debt, infinite extinction, exact budget transport

These are ordinary proofs at actual measure scope. The original CV-R statement **already includes J**. The predecessor mixed countermodel and source status remain unchanged. Kernel and source status are separate in the formal coverage ledger.

## R2-01. Precise interface and decreasing events

Let `(Ω,𝔽,μ)` be a probability space. For every n≥0, let `Y_n:Ω→Q_n` be measurable, where Q_n has measurable singletons. Let measurable `h_n:Q_(n+1)→Q_n` satisfy `Y_n=h_n∘Y_(n+1)`. Let `ν_n=(Y_n)_*μ`, `S_n=S(ν_n)`, `A_n=Y_n⁻¹S_n`, `a_n=μ(A_n)` and `d_n=1-a_n`.

If coherence is only almost everywhere, remove the union of the countably many exceptional measurable null sets. All set inclusions/proofs below then hold on the common full set, and all laws and measure equalities are unchanged. A separate exceptional set for an uncountable time index would not be justified by this argument.

Define `Y_∞(ω)=(Y_n(ω))_n` into the countable product measurable space. Coordinate measurability gives product measurability. A product singleton is the countable intersection of coordinate-singleton inverse images, so it is measurable. Put `ν_∞=(Y_∞)_*μ` and `A_∞=Y_∞⁻¹S(ν_∞)`. Countability/measurability of each positive-singleton set follows from M2-01, not an unexplained assumption about support.

A fine positive singleton lies inside its coarse fibre, so `A_(n+1)⊆A_n`. A positive full-history fibre lies inside every finite fibre, so `A_∞⊆A_*:=⋂_n A_n`. All these sets are measurable. Set `D_n=A_n\A_(n+1)` and `J=μ(A_*\A_∞)`.

## R2-02. One-step and finite identities

For y∈S_n let `w_(n,y)=ν_n{y}` and let ρ_(n,y) be ν_(n+1) restricted to `h_n⁻¹{y}`, divided by w_(n,y). These are well-defined probabilities by M2-03. Its pushforward relation follows from coherence. Thus

`Δ_n:=Σ_{y∈S_n} w_(n,y)d(ρ_(n,y)) = d_(n+1)-d_n = μ(D_n)≥0`.

The final equality is finite measure additivity, since A_(n+1)⊆A_n. Induction on N gives

`d_N=d_0+Σ_(n<N)Δ_n`.

Base N=0 is the empty sum; adding the one-step equality proves the successor. This is the finite identity only, not a substitution for the limit theorem.

## R2-03. Infinite identity by disjoint decomposition

The D_n are pairwise disjoint: if n<m, then A_m⊆A_(n+1), so D_m is disjoint from D_n. Moreover

`A_0\A_* = ⋃_n D_n`.

For the nontrivial inclusion, a point initially in A_0 but not in all A_n has a least failing index k>0 and belongs to D_(k-1). The opposite inclusion follows from monotonicity. The three sets `A_0ᶜ`, `⋃D_n`, and `A_*\A_∞` are disjoint and their union is `A_∞ᶜ`. Countable additivity therefore proves the exact identity directly:

`d_∞=μ(A_∞ᶜ)=d_0+Σ_n Δ_n+J`.

This ENNReal disjoint-union proof can be formalized without an interchange of signed infinite sums or any martingale theorem. All summands are finite and their total is at most 1. It supplies a particularly small formal route against U05.

Continuity from above gives the equivalent limit formulation `μ(A_*)=lim_n μ(A_n)` (μ(A_0)≤1). Hence `L:=sup_n d_n=lim_n d_n=d_0+Σ_nΔ_n`, and `d_∞=L+J`. Nonnegative summability follows from bounded partial sums. This is the monotone/infinite identity; **L is not generally d_∞**.

## R2-04. Cell-mass characterization and exact extinction criterion

For ω∈Ω define `C_n(ω)={ω':Y_n(ω')=Y_n(ω)}` and `m_n(ω)=μ(C_n(ω))`. The cells decrease and their intersection is the full-history fibre. Continuity from above gives `m_n(ω)↓m_∞(ω)=ν_∞{Y_∞(ω)}`.

The function q↦ν_n{q} is measurable: outside the countable S_n it is zero, and on S_n it is the countable sum of weighted singleton indicators. Therefore each m_n is measurable, as is m_∞. We have `A_n={m_n>0}`, `A_∞={m_∞>0}`, and

`J=μ({ω:(∀n,m_n(ω)>0) ∧ inf_n m_n(ω)=0})`.

Consequently, each of the following is equivalent:

1. J=0;
2. `A_*=A_∞` up to a μ-null set;
3. for μ-almost every ω in A_*, `inf_n m_n(ω)>0`;
4. `d_∞=sup_n d_n`.

A pointwise lower bound may depend on ω; a single global positive lower bound is stronger than necessary. Equivalence follows immediately from the measurable set expression and R2-03, not from a numerical limit experiment.

## R2-05. Uniform small-cell criterion — necessary and sufficient

Define `H_n(ε)={0<m_n<ε}`. Then

`J=0  iff  lim_(ε↓0) sup_n μ(H_n(ε))=0`.

Proof of necessity: fix η>0. Since A_n↓A_*, choose N with μ(A_N\A_*)<η. On A_* and when J=0, m_∞>0 almost everywhere; choose ε small enough that μ(A_*∩{m_∞<ε})<η. For n≥N,

`H_n(ε)⊆(A_N\A_*) ∪ (A_*∩{0<m_∞<ε}) ∪ (A_*\A_∞)`.

Indeed H_n⊂A_n⊂A_N, and m_∞≤m_n<ε. The last set is null. Thus all n≥N have mass <2η. For the finitely many n<N, `H_n(ε)↓∅` as ε↓0, so reduce ε further to make their masses <η. This proves the uniform limit.

Proof of sufficiency: on `A_*\A_∞`, every m_n is positive and tends to zero, so for every ε>0 the points in that residual eventually lie in H_n(ε). Fatou's inequality for indicators implies `J≤liminf_n μ(H_n(ε))≤sup_n μ(H_n(ε))`. Let ε decrease to zero.

This criterion is strictly stronger than saying each fixed n has no mass in arbitrarily small positive cells. The latter is always true by continuity from above and cannot exclude extinction.

Useful sufficient conditions now have proofs rather than merely names:

- If every ν_n has at most M positive singleton values, uniformly in n, then `μ(H_n(ε))≤Mε`, so J=0. Any remaining diffuse part of ν_n is outside A_n and does not invalidate this bound.
- More generally any uniform modulus `μ(H_n(ε))≤g(ε)` with g(ε)→0 proves J=0.
- If every ω∈A_* outside a null set has a positive path-dependent lower cell-mass bound, R2-04 gives J=0 directly.
- If the full law is countably supported, then d_∞=0; R2-03 forces d_0=ΣΔ=J=0. This last condition is much stronger than merely having J=0 when diffuse mass was exposed at a finite stage.

The reverse-ordered limits always give zero: for each fixed n, `lim_(ε↓0)μ(H_n(ε))=0`. The fair-prefix example has J=1, so these limits cannot be interchanged without an additional hypothesis. The predecessor iterated-limit formula is retained; no change to its strict-inequality convention is needed.

## R2-06. Exact budgets and finite-to-infinite transport

For `0≤ε≤1`, a finite-stage semantic certificate `d_0≤ε` has slack `s=ε-d_0`. At stage N,

`d_N≤ε iff Σ_(n<N)Δ_n≤s`.

At full history,

`d_∞≤ε iff Σ_nΔ_n+J≤s`.

Suppose instead one knows all finite stages satisfy d_n≤ε. Then L≤ε, and the **exact remaining condition** is `J≤ε-L`. In particular J=0 is sufficient, and the uniform small-cell criterion is a checkable mathematical condition implying it. J=0 is necessary for equality `d_∞=L`, but it is not necessary for preserving a budget with unused slack: J may be positive and still fit below ε. We do not turn a sufficient zero-residual condition into a false necessary condition for every budget.

If ε=1, the probability budget is automatic regardless of J. Any claim that finite-stage bounds alone imply the same infinite bound for every ε<1 is refuted by the fair-prefix example (L=0,J=1). The mixed predecessor example additionally separates mechanisms: d_0=0, total finite debt 1/3, J=5/12, L=1/3, d_∞=3/4. Every finite stage respects ε=1/2 but full history does not. These exact values and their ordinary proof are inherited, not rerun as a new census.

The all-event interpretation of a d≤ε certificate additionally uses M2-02's rich-event conditions for necessity. Restricted/countable repertoires can have better conjunction behavior; we supply only the sufficient singleton-support guarantee absent richness. Artifact validity, source hashes, registry state and owner acceptance are not consequences of any of these probability inequalities.

## R2-07. Optional martingale statement, kept out of the core dependency

Let 𝔽_n=σ(Y_n) and Z=1_(A_∞). Under coherent increasing observation σ-fields, `I_n=1_(A_n)` is an adapted decreasing bounded supermartingale. It need not be a martingale. `M_n=E[Z|𝔽_n]` is the bounded martingale. Since A_∞ is measurable with respect to `σ(⋃𝔽_n)`, the upward conditional-expectation convergence theorem gives M_n→Z almost surely and in L¹. Dominated convergence gives I_n→1_(A_*) in L¹. Thus I_n-M_n→1_(A_*\A_∞) in L¹, with limiting expectation J.

This optional interpretation requires conditional-expectation convergence in addition to the elementary core. R2-01 through R2-06, all budget results and the P03 consumer interface do **not** depend on it. It is not a hidden substitute for the missing finite-to-infinite equality.

## Explicit U05 → CV-R map

| CV-R result | U05 result | Additional assumptions / theorem | Extinction |
|---|---|---|---|
| R2-01 measurable A_n,A_∞ | M2-01 | measurable Y_n; countable product singleton measurability | retained |
| R2-02 one-step fibre identity | M2-03 | measurable h_n, coherence, positive-weight restrictions | finite |
| R2-03 exact infinite decomposition | M2-01/M2-03 | measurable antitone A_n, B=A_∞⊂intersection; countable disjoint additivity | explicitly J |
| R2-03 limit alternative | M2-01 | continuity from above for finite μ(A_0) | explicitly J |
| R2-04 cell characterization | M2-01 | countable weighted singleton indicators; continuity from above | explicitly J |
| R2-05 uniform criterion | M2-01 | continuity from above; Fatou for nonnegative indicators | excludes iff modulus vanishes |
| R2-06 budgets | M2-02 for rich-event interpretation | real arithmetic and R2-03 | exact residual slack |
| R2-07 optional martingale | M2-01 | upward conditional-expectation convergence | terminal gap J |

No Q1c, U08 fixed-point theorem, other packet result, or finite-machine computation is required to prove the core CV-R identities.
