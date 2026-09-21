# CV-R — Exact observation-refinement accounting

Status: ordinary mathematical proof, not kernel-checked; continuation of Q1-Q4.
No mathematical priority claim. See comparison/ADVERSARIAL_COMPARISON.md.

## 1. Objects and expressiveness
Let (Ω,F,μ) be a probability space. For each k, let Y_k:Ω→Q_k be measurable,
with measurable singletons, and ν_k=(Y_k)_*μ. Suppose measurable maps h_k satisfy
Y_{k-1}=h_k∘Y_k. Equalities can instead hold almost surely, after common null-set
adjustment for a countable tower. Set

    S_ν={y:ν({y})>0}, a(ν)=ν(S_ν), d(ν)=1−a(ν).

S_ν is countable: for each n≥1, at most n points have mass at least 1/n.
It is therefore measurable. "Atom" here means positive singleton; on general
measurable spaces it must not be conflated with every measure-theoretic atom.

For the FULL measurable event repertoire, among measurable intersections of
families of ν-conull sets, the least intersection mass is a(ν). Every conull set
contains S_ν. Conversely the intersection of Q\{y} over y∉S_ν is exactly S_ν.
Thus d is the exact largest universal failure probability for that repertoire.
A restricted repertoire need not attain the bound. Countably many actual conull
events always have conull intersection; countable source strings do not make the
instances of an impredicative quantifier countable.

## 2. Finite chain theorem
For y∈S_{ν_{k−1}}, write w_{k,y}=ν_{k−1}({y}) and

    ρ_{k,y}(B)=ν_k(B∩h_k^{-1}{y})/w_{k,y}.
    Δ_k=Σ_{y∈S_{ν_{k−1}}} w_{k,y} d(ρ_{k,y}).

Only positive fibres are used. No general disintegration is presupposed.
Every fine positive point maps to a coarse positive point. Partitioning its
countable support by h_k gives

    a(ν_k)=Σ_y w_{k,y}a(ρ_{k,y}),
    d(ν_k)−d(ν_{k−1})=Δ_k ≥0.

Consequently for every finite n,

    d(ν_n)=d(ν_0)+Σ_{k=1}^n Δ_k.                         (R-finite)

Each increment is zero iff every positive coarse fibre has zero conditional
defect. Strict positivity of every w_{k,y} proves the necessity: a sum of
nonnegative terms is zero only when each term is zero. This places no condition
on zero-probability coarse fibres.

For indices i<j put D(i,j)=d(ν_j)−d(ν_i). Then

    D(i,j)≥0, D(i,k)=D(i,j)+D(j,k), D(i,i)=0.

Applying Q1 directly to h_{i+1}∘...∘h_j yields the same D(i,j) as summing the
intermediate increments. Inserting, deleting or regrouping intermediate
observations therefore does not change endpoint debt, provided the endpoint
laws really are the same coherent laws. Two different observation paths with
different final laws need not agree. An invertible measurable relabelling
preserves positive singleton mass and has zero debt.

Coarsening reverses the inequality. A sequence with both refinements and
coarsenings still has telescoping SIGNED endpoint differences, but those are
not all nonnegative and cannot be called accumulated refinement losses.

If the finest outcome carrier is countable, its law is point-concentrated and
all coarser laws and all increments have defect zero. This remains true if the
countable carrier is an unchanged set of terminating program outputs.

## 3. Infinite chain: a necessary residual
For a countable tower take the full observation
Y_∞=(Y_0,Y_1,...) in the product measurable space and ν_∞=(Y_∞)_*μ. Countable
products of measurable singletons are measurable. Equivalently use a measurable
inverse-limit subspace containing this image. Let

    A_n={ω:Y_n(ω)∈S_{ν_n}},
    A_* = ⋂_n A_n,
    A_∞={ω:Y_∞(ω)∈S_{ν_∞}}.

A_{n+1}⊆A_n, and A_∞⊆A_*. Define

    J=μ(A_*\A_∞).

Continuity from above gives μ(A_*)=lim_n a(ν_n). The finite identity and bounded
monotonicity therefore give the completed exact chain rule

    d(ν_∞)=d(ν_0)+Σ_{k≥1}Δ_k+J.                       (R-infinite)

This is not obtained by silently exchanging infinite conjunction and almost
sure validity. J is precisely the defect missed by every finite level.

More explicitly put m_n(ω)=ν_n({Y_n(ω)}). The observation cells are decreasing
and their intersection is the complete-observation cell, hence

    m_n(ω) ↓ m_∞(ω)=ν_∞({Y_∞(ω)}).

The functions are measurable: y↦ν_n({y}) is nonzero on at most countably
many level-n observations, and m_n is its composition with Y_n. Consequently

    J=μ({ω: (∀n,m_n(ω)>0) and lim_n m_n(ω)=0}).

The exact no-loss-at-infinity criterion is J=0. Sufficient conditions include
countability of the full observation carrier, or a positive path-dependent
lower bound inf_n m_n(ω)>0 for almost every ω∈A_*. Merely positive masses at every
finite stage are NOT sufficient.

Another quantitative expression, with the order of limits explicit, is

    J=lim_{ε↓0} lim_{n→∞} μ({0<m_n<ε}).

Indeed μ(0<m_n<ε)=μ(A_n)−μ(m_n≥ε), and {m_n≥ε} decreases to {m_∞≥ε}.
Take n→∞ and then ε↓0. No claim about swapping these limits is made.

Example: first-n-bit observations of a fair infinite stream have a(ν_n)=1 and
Δ_k=0, but a(ν_∞)=0 and J=1. Replacing the full outcome by a finite stopping output
changes the carrier and is a different problem. If stopping occurs almost
surely with countably many outputs, its defect is zero.

## 4. Correct filtration and cocycle language
Let F_n=σ(Y_n), I_n=1_{A_n}. Since I_{n+1}≤I_n, (I_n) is a bounded nonnegative
supermartingale, not generally a martingale. It converges to 1_{A_*}. Its expected
decrement is exactly Δ_{n+1}.

The conditional atomic probability inside a positive cell is
E[I_{n+1}|F_n]=a(ρ_{n+1,Y_n}) there; it is zero off A_n. This version is an explicit
conditional-expectation calculation on the countable positive cells.

An actual martingale is M_n=E[1_{A_∞}|F_n]. The event A_∞ belongs to
F_∞=σ(⋃F_n). By the upward conditional-expectation convergence theorem,
M_n→1_{A_∞} almost surely and in L1. Because A_∞⊆A_n, M_n≤I_n. The remaining gap
I_n−M_n converges to 1_{A_*\A_∞}, with expectation converging to J.
This uses the standard bounded martingale theorem; it is not formalised here.

D is an additive nonnegative cocycle on coherent refinement chains and is the
coboundary of the scalar potential d. This is a useful exact description, not
a new nontrivial cohomology class. It is not an entropy: splitting any finite
positive observation into finitely or countably many atoms has Δ=0 even though
information or Shannon entropy can increase. Consequently zero debt does not
mean equal information or observational equivalence.

## 5. Topological limits are a separate issue
Uniform finite grids on [0,1] have d=0 and converge weakly to uniform Lebesgue law
with d=1. Uniform laws on [0,1/n] have d=1 and converge weakly to δ_0 with d=0.
Thus d is neither generally upper nor lower semicontinuous for weak convergence.
A Kakutani/compactness argument does not automatically preserve a defect bound.
The coherent-tower theorem above is stronger structured data than arbitrary
weak convergence and must not be applied to arbitrary convergent sequences.

## 6. Exact certificate transport independent of software
Let ε∈[0,1] be a fixed allowed worst universal failure for the full event family,
and suppose stage 0 carries the semantic certificate d(ν_0)≤ε. Its slack is
s_0=ε−d(ν_0). Define accumulated revision debt D_n=Σ_{k=1}^nΔ_k.
Then

    the same ε-bound is true at stage n  iff  D_n≤s_0.

At the full infinite observation it holds iff ΣΔ_k+J≤s_0. Keeping every finite
prefix within budget does not establish the infinite certificate when J>0.
Proof: substitute R-finite or R-infinite. These are exact semantic equivalences.

The context Γ_k records the observation map/vocabulary, the declared law and the
event-family interpretation under dependency versions. K, the inference and
execution calculus, stays fixed. A certificate issued against Γ_0 is an artefact
bound to those versions. A relevant change invalidates that artefact even when
the transported semantic inequality happens to remain true. A NEW transport
certificate can combine the old bound with proved increments and bind itself
to Γ_n. If only upper bounds are supplied, adding them is sufficient but need
not be necessary; the displayed iff requires exact defects/increments.

This is not an estimator or a total decision algorithm for arbitrary laws. The
computability theorem CV-C explains why such an algorithm cannot exist for all
productive observers. The v4 engine verifies a restricted declared-law grammar.
