# Effective stationary-law selection for the U08 cap envelope

10 October 2026. Separate ordinary mathematical research in ACTIVE T20.
No canonical change, closure claim, new axiom adoption, or fresh Lean/kernel claim.

## Result in brief

The U08 compact cap envelope supports three different effective conclusions, which must not be conflated.

1. A supplied computable Markov operator and a computable starting law give computable laws with arbitrarily small stationarity residual. Cesàro averaging supplies the explicit residual bound `2/N`.
2. A computable cap with an effective summable-tail modulus makes the cap envelope effectively compact. If the supplied operator has exactly one stationary law in this envelope, that law is uniformly computable on the promised input class. No mixing-rate input is needed.
3. Without uniqueness or other selection information, no uniform exact stationary-law selector exists, already for two-state rational-valued matrices presented by fast Cauchy names and the fixed cap `(1,1)`. This is a selection impossibility, not merely failure of power iteration.

There is also an exact cap-only contraction criterion for the original stronger **row-dominated** setting. The ℓ¹ diameter of its output envelope determines a computable sharp coefficient `D(c)`; `D(c)<1` supplies uniqueness, geometric computation, and a residual-to-solution error bound. The coarser test `C=Σc_j<2` implies `D(c)≤C−1<1`, and is sharp across cap profiles; at `C=2` exact uniform selection can fail. Some specific caps of total two still have `D(c)<1`. These are cap-only guarantees, not necessary conditions for uniqueness of a particular operator: caps may be loose.

The mathematical ingredients are classical. The project-relative contribution is the explicit U08 represented-input contract, the separation of residual approximation from exact selection, the sharp cap threshold, and matching countercontrols. Effective compactness and exact-zero/representation boundaries already have inherited T10/T18 ancestry; they are not restarted here.

## 1. Inheritance and source boundary

The exact local predecessor `inputs/U08_FIXED_POINTS.md`, F2-04–F2-07, proves ordinary Cesàro existence, countable cap compactness, and exact finite rational-polytope flow solving. Its countable correspondence allows arbitrary nonempty closed row sets `R_i⊂K_c`, chooses one member of each classically, and expressly does not supply effective names. F2-07's constant noncomputable Bernoulli law is a noncomputable-input control; it does not settle computable-input selection.

The retained repository pin is `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c` in `theislampill/orthemology`. The later actual P02 qualification descriptor lists `P02A2.Stationary.compact_convex_linear_fixed`, the approximate-point identities, and finite-simplex/flow targets. This inherited qualification must not be erased by repeating the earlier checkpoint's historical no-compilation statement. It supplies no represented-input algorithm for the countable cap theorem in this report. No descriptor is treated as a new replay.

The actual later T10 `MINIMAL_ADDENDUM.md` §1 already proves eventual inclusion of nested compact ranges in an open neighborhood and explicitly requires effective upper-compact presentations for its terminating search. Its §§2–3 separate a uniformly computable unique state from undecidable exact-zero queries. The actual T18 mathematical companion §11 already proves a Cauchy-name obstruction even for rational-valued stochastic entries, for the different problem of exact winner-existence decision. These are reused conceptual ancestors. The present exact selector problem asks for a stationary law, rather than a yes/no equality answer or a parity winner.

The 262-result retained local registry and targeted repository searches did not identify an already completed effective cap-stationary selector or cap-mass contraction interface. Searches are bounded discovery evidence, not a proof of global novelty or exhaustive absence. Source locations, copied actual texts, and search result paths are retained separately.

External primary ancestry:

- Stefano Galatolo, Mathieu Hoyrup and Cristóbal Rojas, *Dynamics and abstract computability: Computing invariant measures*, DCDS 29 (2011), 193–212, DOI https://doi.org/10.3934/dcds.2011.29.193. Theorem 2.9, Remark 5 and Corollary 3 give the isolated-zero/fixed-point effective-compactness method. Author-hosted text: https://members.loria.fr/MHoyrup/computinvmeas.pdf . We apply this general method in the stronger ℓ¹ topology and supply the cap representation below; we do not identify it with the paper's weak-measure application without a topology check.
- Stéphane Gaubert and Zheng Qu, *Dobrushin's ergodicity coefficient for Markov operators on cones*, arXiv:1307.4649v3, equations (1)–(2), https://arxiv.org/pdf/1307.4649 . These record the classical Doeblin–Dobrushin row-distance/overlap contraction characterization. Section 5 below proves the needed countable special case directly.

## 2. Exact effective input and output contracts

Use `ℓ¹(ℕ)` with its standard norm and dense ideal points consisting of finitely supported rational sequences. A name of `x∈ℓ¹` returns, on input `k`, such a sequence within `2^−k` in ℓ¹. A real name has the analogous rational error guarantee. 'Computable' below is in these representations, uniformly in every stated index.

The general invariant-cap input is:

- Nonnegative real coordinates `c_j`, uniformly computable in `j`.
- A computable function `m(k)` with `Σ_{j≥m(k)}c_j ≤ 2^−k`.
- The promise `C=Σ_jc_j≥1`. The preceding two items compute `c` as an ℓ¹ vector and compute `C` as a real.
- A stochastic matrix `P`, with `P_ij≥0` and `Σ_jP_ij=1`, supplied either by uniformly ℓ¹-computable rows or by uniformly computable entries plus the row-normalization promise. It induces `T(p)=pP`.
- The valid invariance premise `T(K_c)⊂K_c`, where `K_c={p:0≤p_j≤c_j, Σ_jp_j=1}`. For the original row-dominated special case, the stronger premise `P_ij≤c_j` gives this immediately.

The invariance premise can be a proved structural contract. It is not an oracle for testing real equality, deciding row support, or selecting elements of arbitrary closed row sets. All counterfamilies below have uniformly supplied elementary invariance proofs.

Uniform coordinate computability plus row normalization suffices for row ℓ¹ computability: to approximate row `i`, search for an initial partial sum certified greater than `1−η`; a strict lower approximation eventually witnesses this because the row sums to one. Approximate that finite initial block accurately and use the resulting tail bound. This is uniform in `i`, though it need not have a row-independent cost bound. Under common row domination the supplied cap modulus already bounds every row's tail.

The induced operator is a positive linear ℓ¹ contraction:

`||xP||₁ ≤ Σ_i |x_i| Σ_j P_ij = ||x||₁`.

It is computable: approximate `x` by a finite rational vector, apply the finitely many computable rows, and use the norm-one bound for the input truncation error. Thus `r(p)=||pP−p||₁` is a computable 2-Lipschitz real-valued function.

The effective theorem concerns **a supplied computable selected operator**. Bare nonempty closed sets `R_i` with negative descriptions do not provide such a selection. No algorithm for the full original set-valued correspondence is claimed. The inherited exact finite rational-polytope algorithm remains a separate positive case.

The selected matrix is fixed independently of the current law. A state-dependent choice `P(p)` is outside this contract: even setting every row of `P(p)` equal to `p∈K_c` satisfies pointwise row domination but gives `pP(p)=p` for every `p`, so the fixed-operator contraction conclusion would be false for that selection rule.

An exact output law means an algorithm producing arbitrarily accurate ℓ¹ approximations to one fixed stationary law. It does not mean a finite rational vector equal to that law. Likewise a residual-ε law below is a named actual probability in `K_c`; finite approximants to its name need not themselves satisfy the cap and normalization exactly. Such a finite-output promise would already fail for an irrational singleton envelope.

## 3. Computable residual-ε stationary laws

**Theorem E1.** Under the input contract above, uniformly in rational `ε>0`, one can compute a law `s∈K_c` with `||sP−s||₁≤ε`.

**Proof.** Compute `p₀=c/C`, which is a probability and is coordinatewise at most `c` because `C≥1`. For `N≥1` let

`s_N=(1/N)Σ_{k=0}^{N−1}p₀P^k`.

Every term belongs to `K_c` by invariance, and convexity puts `s_N` in `K_c`. It is computable uniformly in `N`. The telescoping identity gives

`s_NP−s_N=(p₀P^N−p₀)/N`, hence `r(s_N)≤2/N`.

Choose any integer `N≥2/ε`. This computes the desired law. ∎

The `2/N` residual bound itself needs neither cap compactness nor uniqueness: any computable stochastic operator and computable starting probability suffice. The cap supplies a canonical computable admissible seed, keeps the averages within the specified domain, and is used for exact existence/selection below. This algorithm is not asserted efficient in `log(1/ε)`.

Residual smallness is not a distance-to-solution certificate. For

`P_t=((1−t,t),(0,1))`, `t>0`, and `q=(1/2,1/2)`,

the unique stationary probability is `(0,1)`, while `r(q)=t` and `||q−(0,1)||₁=1`. An arbitrarily small residual can coexist with fixed large solution error. Section 6 rules out a uniform algorithm for a prescribed coarse distance to a stationary law on the unrestricted represented-input class, even though residual approximation is uniform.

## 4. Effective compactness and uniqueness

**Lemma E2.** The set `K_c` has a uniform effective upper-compact presentation: for every effectively open set `U` in ℓ¹, inclusion `K_c⊂U` is semidecidable.

**Proof.** First consider `B_c={x:0≤x_j≤c_j}`. At mesh scale `η>0`, use `m` to choose `N≥1` with cap tail less than `η/4`. For each `j<N`, a finite rational grid of mesh at most `η/(4N)` extending strictly above `c_j` is computable. Clip grid values by the computable operation `u↦min(u,c_j)`. Products of these grids, extended by zero after `N`, give finitely many uniformly computable points of `B_c` that form an `η/2`-net. They can be approximated by rational ideal points with explicitly budgeted additional error.

To semidecide a finite open-ball cover of `B_c`, successively refine such nets and test strict containment margins for each net point, adding the certified covering radius to its distance from a proposed cover center. Every accepted certificate is sound. If the cover is genuine, compactness supplies a positive Lebesgue margin, so some sufficiently fine finite net passes. For a recursively enumerated open set, dovetail this test over its finite initial subfamilies. Thus `B_c` is effectively upper compact. Its ordinary compactness follows from completeness, coordinate closedness, and the same uniform tails.

The sum functional `S(x)=Σ_jx_j` is computable and 1-Lipschitz on ℓ¹. Therefore `{x:S(x)≠1}` is effectively open. Since

`K_c⊂U  iff  B_c⊂ U ∪ {x:S(x)≠1}`,

upper compactness of `B_c` gives the stated semidecision. No algorithm is presumed to decide which grid cells meet `K_c`, and no dense computable sequence in a general effectively closed set is assumed. ∎

**Theorem E3.** If additionally `Z={p∈K_c:pP=p}` is a singleton `{π}`, its element `π` is uniformly computable on this promised input class.

**Proof.** The zero set `Z` is upper compact because

`Z⊂U  iff  K_c⊂ U ∪ {p:r(p)>0}`,

and `r` is computable and nonnegative. For precision `2^−k`, enumerate finitely supported rational centers `q` and semidecide `Z⊂B(q,2^−k)`. If a certificate is found, output `q`. A rational center sufficiently close to the unique `π` exists, so the search terminates; every accepted output has the required error. This is the effective-compact singleton method. It uses the supplied representations and the uniqueness promise, not an attempted decision of uniqueness. ∎

The same argument computes an isolated stationary point if an effectively isolating compact restriction is supplied. We make no claim to decide that a stationary point is isolated or to discover an isolating region without further input.

There is even a computable Cesàro convergence modulus under the uniqueness promise, though it need not be a simple closed formula. Put `Z_n={p∈K_c:r(p)≤2^−n}`. These are uniformly upper compact, nested nonempty sets with intersection `{π}`. Given `k`, search jointly for `n` and rational `q` with

`Z_n⊂B(q,2^(−k−2))`.

The inclusion is semidecidable through `K_c⊂B(q,2^(−k−2))∪{r>2^−n}`. Compactness plus singleton intersection makes some such pair exist. For every `N≥2^(n+1)`, both `s_N` and `π` are in `Z_n`, so `||s_N−π||₁<2^(−k−1)`. Thus absence of an initially supplied mixing rate is not a noncomputability proof. Raw powers may still oscillate, as the inherited two-state swap demonstrates.

## 5. The sharp row-cap contraction threshold

This section assumes the stronger original row condition `P_ij≤c_j` for **all** `i,j`. General invariance of `K_c` alone does not imply the conclusion.

**Theorem E4.** If `1≤C<2`, then for any probabilities `p,q`,

`||pP−qP||₁ ≤ (C−1)||p−q||₁`.

Consequently there is exactly one stationary probability `π`, it belongs to `K_c`, and `||pP^n−π||₁≤2(C−1)^n` for every starting probability `p` and `n≥1`.

**Proof.** Any probabilities `u,v` dominated by `c` satisfy

`Σ_j max(u_j,v_j)≤C`,
`Σ_j min(u_j,v_j)=2−Σ_j max(u_j,v_j)≥2−C`,
`||u−v||₁=2−2Σ_j min(u_j,v_j)≤2(C−1)`.

Write `p−q=t(a−b)`, where `t=||p−q||₁/2` and `a,b` are the normalized positive and negative parts; if `t=0`, the result is immediate. Row domination ensures that both probabilities `aP` and `bP` are dominated by `c`. Thus

`||pP−qP||₁=t||aP−bP||₁≤2t(C−1)`.

The complete probability simplex is invariant under `P`, so the contraction principle supplies its unique fixed point. Alternatively use U08 existence and the displayed contraction. Every one-step output is in `K_c`, hence the fixed point is too. Iterating the contraction and using the diameter bound two gives the claimed error. ∎

**Effective rate.** Compute a rational `r` with `C−1<r<1` by searching certified strict inequalities; the promise `C<2` makes this terminate, including when `C=1`. To approximate `π` within `2^−k`, choose `n` with `2r^n≤2^(−k−1)` and approximate the computable vector `p₀P^n` within `2^(−k−1)`. No exact test of `C=1` is needed. In fact this contraction computation only needs a certified rational row-cap total bound `<2`, a computable operator and a computable probability seed; a cap-tail modulus is not independently needed once such a contraction bound is available.

**Optimal factor.** For every real `C∈[1,2]`, take

`P_C=((1,0),(2−C,C−1))`, `c_C=(1,C−1)`.

Both rows are dominated by `c_C`, whose total is `C`. For `p=δ₀,q=δ₁` the norm ratio is exactly `C−1`. For `C<2` the unique stationary law is `δ₀`; for `C=2` the matrix is the identity. Thus the coefficient and strict threshold cannot be improved using the cap total alone. At or above two, particular kernels can nevertheless have unique computable stationary laws; this is a loss of the cap-only guarantee.

This is the explicit cap consequence of classical Doeblin–Dobrushin overlap contraction, not a proposed new general contraction theorem.

### 5.1 Exact cap-only coefficient, beyond the total-mass test

The following refinement was developed jointly during this investigation; the participating derivation is retained at `inputs/ENVELOPE_DIAMETER.md`.

**Theorem E4b.** Put `TV(p,q)=||p−q||₁/2` and

`D(c)=max_{p,q∈K_c} TV(p,q)`.

Then

`D(c)=max_{S⊂ℕ} [min(1,c(S))+min(1,c(Sᶜ))−1]`,

where `c(S)=Σ_{j∈S}c_j`. Equivalently the expression maximized is

`f(c(S))`, where `f(s)=min(1,C−1,s,C−s)` for `0≤s≤C`.

For every row-dominated stochastic operator and all probabilities `p,q`,

`||pP−qP||₁≤D(c)||p−q||₁`.

No smaller uniform coefficient follows from the cap alone. Moreover, `D(c)=1` exactly when a subset partitions the cap into two parts each having total capacity at least one.

**Proof.** For a fixed subset `S`, the largest feasible value of `p(S)` is `min(1,c(S))`; the smallest is `max(0,1−c(Sᶜ))`. Both are attained: distribute the selected mass proportionally to the cap within each group, and assign zero to a zero-cap group. The group capacities and `C≥1` make the assignments feasible. The discrete total-variation identity gives

`sup_{p,q∈K_c}TV(p,q)=sup_S sup_{p,q∈K_c}(p(S)−q(S))`,

which is the formula. The subset-sum map `{0,1}^ℕ→[0,C]`, `z↦Σ_j c_jz_j`, is continuous by the uniform cap-tail bound; its domain is compact. Thus the displayed supremum is a maximum. The expression equals one exactly when both group capacities are at least one.

For contraction, repeat the normalized positive/negative-part proof in E4 and bound `TV(aP,bP)` by the envelope diameter `D(c)`. Conversely, choose two cap-admissible rows attaining the diameter, place them at two different input indices of an otherwise row-dominated operator, and use the two corresponding Dirac input laws. Its full-simplex Lipschitz constant is at least `D(c)`. This is optimality of the cap-only coefficient on all probability inputs; it does not assert every particular row family attains it. ∎

**Effective computation.** For `J_N={0,…,N−1}` define

`D_N=max_{S⊂J_N} f(c(S))`, `τ_N=Σ_{j≥N}c_j`.

The function `f` is 1-Lipschitz in `s`. Removing the tail of any subset changes its cap mass by at most `τ_N`. Therefore

`D_N≤D(c)≤D_N+τ_N`.

Each finite maximum is computable from the coordinate names and the computable total `C`, and the supplied tail modulus bounds `τ_N`. This computes `D(c)` uniformly. The finite subset enumeration is exponential; there is no efficiency or optimization claim.

Under the promise `D(c)<1`, strict-inequality search finds a certified rational `ρ` with `D(c)<ρ<1`. The selected operator's unique stationary probability then obeys

`||pP^n−π||₁≤2ρ^n`,
`||p−π||₁≤||pP−p||₁/(1−ρ)`.

The second bound follows by inserting `pP` and using contraction. It is the missing quantitative upgrade from E1's residual to a solution-error certificate when a cap contraction gap is supplied or found. Merely knowing `D(c)≤1` gives no decision procedure for equality to one.

**Controls.** For `c=(9/10,9/10,1/5)`, total mass is two, but the subset masses are `0,1/5,9/10,11/10,9/5,2`. The formula gives `D(c)=9/10<1`. Therefore the total-two obstruction is not a claim that every total-two cap fails. For `c=(1/2,1/2,1/2)`, `D(c)=1/2`, but the three admissible rows `(1/2,1/2,0)`, `(1/2,0,1/2)`, `(0,1/2,1/2)` have zero coordinatewise common minorant. The proof uses pairwise overlap/envelope diameter and must not be replaced by an assertion of one common Doeblin minorizing measure.

Finally, uniqueness remains specific to the fixed selected operator. The inherited interval correspondence in which every `R_i` consists of Bernoulli laws with parameter in `[1/3,2/3]` has cap `(2/3,2/3)` and total `4/3`, yet its correspondence-level fixed-point set is the whole interval. Different computable selections can have different unique fixed points. This is an inherited scope control, not a new countermodel.

**Corollary E4c: exact universal cap criterion.** The inequality `D(c)<1` holds if and only if every stochastic kernel whose rows belong to `K_c` has a unique stationary probability. The forward direction is E4b's contraction. For the reverse, if `D(c)=1`, take the attained partition `S` with `c(S),c(Sᶜ)≥1`, and choose probabilities `u,v∈K_c` supported respectively on the two groups. Define row `i` to be `u` when `i∈S` and `v` otherwise. Then `uP=u` and `vP=v`, so uniqueness fails. This equivalence quantifies over all mathematical stochastic kernels. It does not assert that a suitable partition or the counterkernel can be chosen computably from every computable cap.

The distinction between row domination and envelope invariance is essential even in two dimensions. The identity operator preserves the envelope with `c=(3/4,3/4)`, whose diameter coefficient is `D(c)=1/2`, but every law in that envelope is stationary. Its Dirac rows do not belong to the envelope. Thus E4b–E4c cannot be applied from `T(K_c)⊂K_c` alone.

## 6. Exact selection is not uniform at cap mass two

Define

`P(a,b)=((1−a,a),(b,1−b))`, with `0≤a,b≤1`,
`c=(1,1)`, `K_c=Δ₂`.

Normalization and row domination are immediate and uniform. If `a+b>0`, the unique stationary law is

`π(a,b)=(b/(a+b),a/(a+b))`.

Indeed stationarity is the single balance equation `π₀a=π₁b` plus normalization. If `a=b=0`, every probability is stationary.

### 6.1 Topological obstruction

On the positive `a`-axis, every exact selector is forced to return `δ₁`. On the positive `b`-axis it is forced to return `δ₀`. Both axes approach the same identity matrix. Whichever stationary law is selected at the identity, continuity along both axes is impossible. Thus no continuous extensional single-valued selector exists on this matrix family. Identity's freedom is explicitly included in the argument; choosing its midpoint, endpoint, or any other stationary value cannot satisfy both forced limits. This topological statement alone is not our exclusion of arbitrary name-dependent realizers of the multivalued selection problem; that stronger algorithmic impossibility is proved in §6.2.

### 6.2 Explicit computable-family diagonal obstruction

The following proof does not rely only on continuity and handles both Type-2 realizers whose choices may depend on the input name and algorithms acting on program indices. In either case the uniformly computable family of names below turns a putative solver into one uniform computable output family.

Fix an effective enumeration `φ_e` of partial computable natural-valued functions. Let

`A={e:φ_e(e) halts with output 0}`,
`B={e:φ_e(e) halts with output 1}`.

These disjoint c.e. sets have no total computable binary separator `d` satisfying `d=1` on `A` and `d=0` on `B`: if `φ_k=d`, then `d(k)=0` puts `k` in `A` and forces `d(k)=1`, while `d(k)=1` puts `k` in `B` and forces `d(k)=0`.

If `φ_e(e)` first halts at stage `t` with output 0, put `a_e=2^(−t−2)`; otherwise put `a_e=0`. Define `b_e` similarly for output 1. Both sequences are uniformly computable real numbers. At precision `2^−k`, simulate through stage `k`; if the relevant halt has appeared, output its exact dyadic rate; otherwise output zero. Any future rate is smaller than `2^−k`. At most one rate is positive. Every individual rate is a rational number, but no uniform exact-fraction representation is thereby supplied.

Suppose one uniform algorithm returns a Cauchy name of some exact stationary law `π_e` for every `P(a_e,b_e)`. Compute a rational `z_e` approximating its second coordinate within `1/4`, and set `d(e)=1` when `z_e>1/2`, otherwise zero. This is a total computable binary function. On `A`, stationarity forces `π_e=δ₁`, so `d(e)=1`. On `B`, it forces `π_e=δ₀`, so `d(e)=0`. This contradicts the preceding diagonal argument.

There is no ambiguity at `z_e=1/2`: the algorithm makes an exact rational comparison and picks zero; that value can occur only in the unconstrained part of the separator problem. An arbitrary stationary choice at the identity therefore cannot evade the contradiction.

**Theorem E5.** Uniform exact selection fails even when all entries are rational-valued, rows and cap have effective tail bounds, every input has a stationary law, and every individual input has a computable stationary law. It fails already at the fixed coarse task of returning a rational approximation within `1/4` in ℓ¹ of some exact stationary law: such an approximation also determines the separator on the two forced branches.

This does not refute the inherited finite exact-rational solver. A pair of integers encoding a rational value supplies decidable zero/equality information that an arbitrary Cauchy name of a rational number does not provide. Nor does it refute E3: E3 is partial outside the unique-stationary input promise, while the selector above must also handle the identity cases.

### 6.3 Genuinely countably supported lift

Let `g_n=2^(−n−1)` and identify `(j,n)∈{0,1}×ℕ` with `2n+j`. Define

`Q((i,n),(j,m))=P(a,b)_(i,j) g_m`,
`c_(j,m)=g_m`.

All rows are uniformly computable and are dominated by the same computable cap of total two. Beyond index `2N` the cap tail is `2^(1−N)`, so an explicit modulus is available. For any law `p`, write its two-state marginal as `h_i=Σ_np_(i,n)`. Then

`(pQ)_(j,m)=(hP)j g_m`.

Hence the stationary laws of `Q` are exactly `p_(j,m)=π_jg_m` for stationary two-state laws `π`. Each such law has infinitely many positive coordinates. An ℓ¹ name of a stationary `p` computes the marginal `π`, since summing over one fiber is a bounded computable linear functional. A selector for this countably infinite family would therefore contradict E5. The obstruction is not an artifact of finite support.

## 7. Why effective tightness cannot just be omitted

The following separate control is for the **general invariant-cap** regime, not the stronger all-rows-dominated regime of E4–E5.

Take a computable increasing rational sequence `α_n↑α∈[0,1/3]`, with `α₀=0` and noncomputable limit. One explicit choice enumerates the diagonal halting set `H` and takes partial sums of `Σ_{e∈H}4^(−e−1)`. This sum is noncomputable: after earlier digits are determined, absence of the `e`th term leaves a tail at most one third of that term, whereas its presence contributes at least the entire term, so a computable real approximation would decide membership in `H` successively.

Put `w₀=1` and, for `n≥1`,

`w_n=2^−n+α_n−α_(n−1)`.

Every `w_n` is a uniformly computable positive rational, but `W=Σ_nw_n=2+α` is not computable, so no computable cap-tail modulus exists. Define conductances

`h_n=min(w_n,w_(n+1))/4`,
`P(n,n+1)=h_n/w_n`,
`P(n+1,n)=h_n/w_(n+1)`,

and fill each diagonal with the remaining row mass. Each off-diagonal term is positive and at most `1/4`, so diagonal probabilities are at least `1/2`. Every row has at most three rational entries and is uniformly computable. Detailed balance gives `wP=w`. For any `p∈K_w`, positivity gives `pP≤wP=w`; mass preservation gives `pP∈K_w`. Thus the operator and its invariance have effective descriptions, while the cap is classically summable but not effectively tight.

The probability `π_n=w_n/W` is stationary and belongs to `K_w`. It is the unique stationary probability: for any stationary `q`, let `J_n=q_nP(n,n+1)−q_(n+1)P(n+1,n)`. The stationarity equation at zero gives `J₀=0`; the equation at `n≥1` gives `J_n=J_(n−1)`, hence every current vanishes. Positivity of `h_n` then yields `q_n/w_n=q_(n+1)/w_(n+1)` for all `n`; normalization fixes the constant to `1/W`.

But `π₀=1/W` is noncomputable, since a computable positive `π₀` would compute `W` and then `α`. Therefore computable coordinate caps, classical summability, a computable operator, effective structural invariance, and uniqueness alone do not imply a computable stationary law. The effective compactness assumption in E3 cannot be replaced by classical compactness on this input class.

This control also has the computable admissible seed `δ₀`, so computable Cesàro residual approximations exist even though the unique limit is noncomputable. Its rows cannot satisfy one common summable coordinate cap: every row's diagonal is at least one half. Consequently it must not be represented as a counterexample within the stronger original all-rows-dominated class.

## 8. Exact scope, evidence and stopping point

- The new claims are ordinary proved theorems E1–E5, including refinement E4b, plus the no-effective-tail counterexample; no new Lean candidate or kernel result is attached.
- The executed `check_controls.py` performs 5,081 exact-rational checks, including 125 cap instances comparing the subset formula with independent finite-polytope vertex diameters, and checks of identities, row domination, optimal contraction examples, the residual/distance separation, and infinite-lift formulas with explicit tail accounting. These finite controls do not prove noncomputability, arbitrary computable compactness, or a universal algorithm refinement.
- The uniqueness search is a genuine terminating computability proof on promised inputs, not an efficiency estimate. It is allowed to run indefinitely when its promise fails.
- The obstruction is to uniform selection. It does not say every computable Markov chain here lacks a computable stationary point. The two-state obstruction family has a computable point in every instance.
- No full Weihrauch-degree classification, general computable selection from row correspondences, or necessary-and-sufficient uniqueness test for an individual operator is asserted. E4c is instead a universal criterion for all mathematical kernels admitted by one cap.
- Existing U08 rational-flow results, T10 compact-warrant/equality boundaries, T18 Cauchy-name decision boundary, and all protected framework/pinned states remain unchanged. The U08 classically chosen row operator is not silently promoted to an effective selection.

The useful new operation is explicit: from effective cap/selected-operator input, compute residual laws; upgrade to exact laws on the uniqueness promise; and, under original row domination, compute the exact cap-only coefficient `D(c)`. A verified `D(c)<1` replaces the uniqueness promise with a geometric bound and a residual-to-solution certificate. The total-mass test `C<2` is a sharp simpler sufficient test. At the cap `(1,1)`, a general uniform exact selector is impossible even for rational-valued named rows, and the obstruction lifts to infinitely supported outputs.
