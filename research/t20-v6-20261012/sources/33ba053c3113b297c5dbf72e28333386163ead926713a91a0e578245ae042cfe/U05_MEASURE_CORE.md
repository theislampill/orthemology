# U05 — completed ordinary measure core, attempt-0002

Status of the mathematics below: ORDINARY_PROOF. This is a proposed research extension, not a change to any accepted source theorem. Lean status is recorded independently in `formal/FORMAL_COVERAGE.json`. The exact original obligation and preimages are preserved in `provenance/ORIGINAL_OBLIGATIONS.json` and the predecessor ZIP.

## M2-01. Spaces, regimes and definitions

Unless stated otherwise, `(X,Σ,μ)` is a probability space with every singleton measurable. No topology, completion, effective enumeration or regular conditional probability is implicit. Define

`S(μ)={x:0<μ{x}}`, `a(μ)=μ(S(μ))`, `d(μ)=1-a(μ)`.

Here measure values used in subtraction are finite real values. An ENNReal implementation must establish finiteness before conversion. We call `d=0` **singleton-supported**, not just “atomic”, unless the terminology is explicitly fixed. It means support on a countable measurable set up to a null complement. It does not mean every point of X has positive probability.

“Finitely supported” means `μ(F)=1` for a finite F. “Countably supported” means the analogous statement for a countable F. An **atom as a measurable set** is a measurable A of positive mass with no measurable subset of intermediate mass. A measure is nonatomic if it has no such atom. These notions are not silently identified with singleton mass on arbitrary measurable spaces. “Computable” is always relative to a named effective presentation; “effectively presented” supplies an encoding of measurable generators, their operations, and a specified algorithm or oracle for the required probabilities. Neither is a consequence of the existence of μ.

### Proof of countability and regime separation

For j≥1, the set `E_j={x:μ{x}≥1/j}` has at most j elements. Otherwise choose j+1 distinct points and apply finite additivity to their disjoint measurable singletons, contradicting μ(X)=1. Each positive real mass is at least 1/j for some j, so `S=⋃_{j≥1}E_j` is countable and measurable. Enumerating its distinct points and applying countable additivity gives `a=Σ_{x∈S}μ{x}`. Thus `0≤a,d≤1`.

If μ is carried by countable F, each point of `F\S` has mass zero, and countable additivity gives μ(F\S)=0. Hence a=1. Conversely a=1 makes S a countable carrier. This proves

**countably supported iff singleton-supported iff d=0.**

Finite support implies these equivalent conditions. The converse fails for a geometric law on ℕ with every point positive. A nonatomic measure has zero singleton masses, since a positive singleton is an atom, and hence d=1. The converse requires additional separation structure.

For a countermodel to that converse, take an uncountable X with the countable/co-countable σ-algebra, and μ(A)=0 for countable A and 1 for co-countable A. This is a countably additive probability: a disjoint sequence has at most one co-countable member, and if none does its union is countable. Every singleton is measurable and null, so d=1. Yet X is an atom in the measurable-set sense because every measurable subset has mass 0 or 1.

On a space with a **countable measurable point-separating family** `(G_n)`, every measurable atom A is, modulo a null set, a positive singleton. For each n choose the side of G_n that contains all of A's mass. Remove from A the countable union of the discarded null parts. The remaining measurable set has μ(A)>0, so is nonempty. Its points have the same membership decisions in every G_n; separation makes it a singleton. Its mass is μ(A). Consequently, on such spaces (in particular standard Borel spaces), d=1 is equivalent to nonatomicity, and an atomic probability is countably supported. The countable separating-family premise, not merely measurable singletons, is what licenses this terminology.

## M2-02. Exact all-event lower bound

Let `(A_i)_{i∈I}` be any family of measurable events with μ(A_iᶜ)=0. A point x∈S cannot lie in A_iᶜ, by monotonicity `μ{x}≤μ(A_iᶜ)=0`. Therefore `S⊆⋂_i A_i` set-theoretically, without a measurability claim about the arbitrary intersection.

If `C=⋂_i A_i` is measurable, μ(C)≥a. This bound is attained: index by x∉S and use `A_x=X\{x}`. Every A_x is measurable and conull, and their intersection is precisely S. Hence the infimum of the masses of measurable intersections of arbitrary conull families is **exactly a**, with an attaining family.

For `0≤ε≤1`, every such intersection has mass at least `1-ε` iff d≤ε. For a possibly nonmeasurable intersection, the separately named safe conclusion is that it **contains the measurable set S of mass a**. We do not pretend its raw measure is defined as an event probability.

For any restricted event repertoire the lower bound remains sufficient. Attainment/necessity requires the repertoire to contain the singleton-complement family, or another family attaining S. A countable repertoire alone always has conull intersection, even for an atomless law. Thus countable syntactic expressibility does not establish the rich-event necessity direction.

## M2-03. Maps and positive restricted fibres

Let `h:X→Y` be measurable, with measurable singletons on Y; `ν=h_*μ`. For y∈S(ν), let `w_y=ν{y}>0` and define

`ρ_y(B)=μ(B∩h⁻¹{y})/w_y`, for B∈Σ.

The fibre is measurable and w_y is finite and positive; this is a probability on X. Zero-weight fibres are deliberately outside the index set. This is a normalized measurable restriction, not disintegration on arbitrary null fibres.

Map evaluation gives `ν{y}=μ(h⁻¹{y})`. For x∈S(μ), `{x}⊆h⁻¹{h(x)}`, so h(x)∈S(ν). Within a positive fibre, `ρ_y{x}=μ{x}/w_y`; outside it, the singleton mass is zero. Thus `S(ρ_y)=S(μ)∩h⁻¹{y}`. Partition the countable S(μ) by its h-images and sum its nonnegative singleton masses. This gives

`a(μ)=Σ_{y∈S(ν)} w_y a(ρ_y)`.

All series are bounded by 1. Since `a(ν)=Σ_y w_y`, subtraction of finite quantities yields

`d(μ)=d(ν)+Σ_{y∈S(ν)} w_y d(ρ_y)`.

In particular, d(ν)≤d(μ). Equality holds iff each positive fibre has zero defect: a sum of nonnegative terms is zero iff every term is zero, and every indexed w_y is strictly positive. A zero-mass fibre cannot create an additional equality requirement. The pushforward of the normalized restriction through a finer observable gives exactly the fibre law used by CV-R.

## M2-04. Countable mixture identity

Let I be finite or countable, μ_i probabilities on the same measurable-singleton space, and w_i≥0 with `Σ_i w_i=1`. Set `μ(B)=Σ_i w_i μ_i(B)`; nonnegative interchange proves countable additivity and normalization. Let `T=⋃_{i:w_i>0}S(μ_i)`.

For every x, the nonnegative sum `μ{x}` is positive iff some active component has positive singleton mass. Thus S(μ)=T, which is countable. For each active i, `T\S(μ_i)` is a countable union of μ_i-null singletons, so `μ_i(T)=a(μ_i)`. Consequently

`a(μ)=Σ_i w_i a(μ_i)` and `d(μ)=Σ_i w_i d(μ_i)`.

No pairwise disjointness of supports, no mutual singularity and no rationality are required. Finite-support laws can have countably infinite support after a countable mixture. Countably supported laws remain countably supported. An uncountable mixture need not preserve this: `∫_[0,1] δ_x dx` is Lebesgue probability, although each δ_x has defect zero. Therefore the unrestricted-mixture closure extension is **REFUTED**, while the countable-mixture replacement is proved. This does not relabel the original source, which already had the countable restriction.

## M2-05. Weak topology versus total variation

For these statements X is a Polish space with its Borel σ-algebra, and weak convergence is convergence of integrals of bounded continuous real functions.

The predecessor examples remain unchanged: uniform finite grids on [0,1] converge weakly to Lebesgue probability by the Riemann-sum theorem, with defects 0→1; uniform probabilities on [0,1/n] converge weakly to δ_0 by continuity at 0, with defects 1→0. Thus d is neither lower nor upper semicontinuous, and `d≤ε` is not weakly closed for any `0≤ε<1`. These are universal proofs using continuous test functions, not numerical approximations.

A more general construction is available whenever ν is a nonatomic probability on a compact metric space. Cover X by finitely many balls of radius 1/n, disjointify the cover into Borel cells, choose one representative from each nonempty cell and give it the cell's ν-mass. The resulting finite law ν_n satisfies, for every continuous f,

`|∫f dν_n-∫f dν|≤sup_{dist(x,y)≤2/n}|f(x)-f(y)|→0`.

Each ν_n has d=0 and ν has d=1. Compactness supplies uniform continuity. On a noncompact Polish space one adds tight compact truncations; that extension is not needed to establish the stated failure.

**What does survive weak limits:** if every ν_n is supported on one fixed closed finite F, then any weak limit ν is supported on F by the closed-set Portmanteau inequality `1=limsup ν_n(F)≤ν(F)`. More generally, the set of probabilities with at most m support points is weakly closed on a Polish space. If a limit had m+1 distinct topological support points, choose pairwise disjoint open neighborhoods of them. Each has positive limiting mass, hence by the open-set Portmanteau inequality is positive for all sufficiently large n. A measure with at most m support points cannot charge all m+1 neighborhoods. A probability on a Polish space has a full-measure topological support (use a countable base), so failure to have at most m support points would indeed supply those m+1 points. The number m must be uniform; growing grid supports show why.

**Total variation replacement:** define `TV(μ,ν)=sup_{A∈Σ}|μ(A)-ν(A)|` (no factor-of-two ambiguity). Put `T=S(μ)∪S(ν)`, a countable measurable set. Null-singleton countability gives μ(T)=a(μ), ν(T)=a(ν). Therefore

`|a(μ)-a(ν)|=|μ(T)-ν(T)|≤TV(μ,ν)`, hence `|d(μ)-d(ν)|≤TV(μ,ν)`.

This proves both semicontinuities, and closure of every sublevel and superlevel of d, for total variation convergence. In particular countable-support and singleton-free probabilities are TV-closed. TV need not preserve finite support: truncations of a geometric law converge in TV to an infinite-support law. Finiteness, countable support and the topology of convergence must not be merged into one closure assertion.

## M2-06. Effective boundary and the separate Q8 compiler

Measure existence does not provide codes for its events, a name for its weights, an effective enumeration of its atoms, or a sampler. Even on {0,1}, a Bernoulli measure with a noncomputable bias exists. In an effective Cantor presentation, computability of all prefix-cylinder probabilities is a specific additional requirement; full atomic mass is still not thereby decidable (CV-C proves the exact index obstruction).

`code/prcodec.py::compile_q8` supplies an actual compiler for a finite two-counter machine into a P02-L1 synchronous observer. At output stage n it simulates the source for n transitions, detecting a halted instruction also at the initial/current configuration; then it returns the current fresh input bit iff halt has been reached, and zero otherwise. `pc` is snapshotted before each simulated step, so at most one original instruction executes per step. Both counters start at zero and are reset on each output-bit invocation.

For a machine that never halts, every output is zero and the law is δ_0∞. For a machine halting after T transitions, the outputs from T onward are distinct fresh independent input bits. Every singleton then fixes infinitely many independent bits and has probability at most 2^-k for every k, hence zero. Thus defect is 0 in the first case and 1 in the second. The source model's undecidability premise is a **computability premise**, not a measure axiom. The explicit arbitrary-PR normal-form reductions in CV-C independently establish undecidability without requiring this machine model to be used as the hierarchy's numbering.

The finite counter-machine tests check the implemented bounded simulator on specified instances. They neither decide nonhalting nor prove it for arbitrary machines. The universal simulation argument is structural and ordinary, in `CV_C_CODEC_AND_CORRESPONDENCE.md`.

## Original-claim disposition

The inherited U05 source already warns about atomless singleton complements and weak limits. It is **not refuted** by preserving those examples. Refuted statements in this extension are precisely: (i) singleton-free implies nonatomic on every measurable-singleton space; (ii) arbitrary mixtures preserve zero defect; (iii) weak limits preserve a fixed positive budget <1. Their hypothesis-correct replacements are M2-01, M2-04 and M2-05. No canonical theorem is weakened.
