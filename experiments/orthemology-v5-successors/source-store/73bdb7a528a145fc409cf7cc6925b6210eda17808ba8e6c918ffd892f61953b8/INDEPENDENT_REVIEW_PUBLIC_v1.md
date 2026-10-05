# Finitely additive concentration and a past-complete innovation law

4 October 2026 UTC. Independent ordinary-mathematics review. No code, simulations, Lean implementation, frozen-file modification, external contact, or actual metaphysical warrant is supplied. Mathematical existence below is nonconstructive where a free ultrafilter is used. This is a scoped programme application, not a theorem-priority claim.

## Verdict

**Accept the proposed Gaussian estimate**, with its real-valuedness, event-domain, and independence assumptions stated explicitly. Neither joint countable additivity nor tightness of the initial-position marginal is needed. The Gaussian increment marginal supplies the tail control. The resulting past-complete obstruction needs only tightness of the terminal-position marginal, a substantially weaker assumption than countable additivity of the entire joint law.

**Accept a matching finitely additive consistency construction.** A single ultralimit of uniform-anchor, two-sided-noise laws yields a real-valued finitely additive probability on the full Borel path-event domain. Every recurrence holds pointwise; the entire noise marginal remains the original countably additive iid product law; full past information is independent of future innovations. Its position marginals are translation-invariant and give every bounded interval probability zero. This demonstrates the exact failure of terminal-position tightness, without relaxing freshness.

**Do not infer a metaphysical realisability result or a general causal-finitism refutation.** These are probability specifications and mathematical controls. A causal or productive interpretation needs its own warrant.

## 1. Exact concentration statement

Let A be an algebra of subsets of a sample set Ω. Let μ:A→[0,1] be a real-valued, nonnegative, normalized finitely additive probability. Let Y,Z:Ω→R be pointwise real-valued maps, and fix n>0. It is sufficient to assume:

1. Preimages under Y of the bounded intervals used below, and their finite Boolean combinations, belong to A.
2. Preimages under Z of the translated closed intervals and two-sided tail events used below belong to A.
3. The event E={Y+Z∈I} belongs to A for the bounded interval I being assessed.
4. For those Y-cells C and Z-intervals D, μ({Y∈C}∩{Z∈D})=μ(Y∈C) μ(Z∈D).
5. The relevant Z-interval and tail probabilities equal those of N(0,n).

The cleaner, stronger formulation is that Y and Z have Borel preimages in A, are rectangle-independent for all Borel sets, and Z has exactly the ordinary N(0,n) Borel marginal. Exact Borel normality is sufficient, but more than the displayed proof needs. The sum event still needs to be in A: a mere algebra is not automatically closed under the countable operations that establish measurability of a sum on a σ-algebra.

For every bounded interval I,

μ(Y+Z∈I) ≤ length(I) / sqrt(2πn).

Empty intervals are immediate. A singleton has length zero and is covered by the argument, without assuming Y has no atoms.

### Proof

Write a=inf I, b=sup I, L=b−a, c=1/sqrt(2πn), and R=max(|a|,|b|). Thus I⊆[a,b]⊆[−R,R]. Fix M>R and δ>0.

Partition [−M,M] into finitely many disjoint cells C_j, each contained in a closed interval [u_j,v_j] of length at most δ. Use half-open cells and include the final right endpoint in the final cell. No endpoint is omitted or counted twice; Y may put arbitrary mass at partition boundaries.

If Y∈C_j and Y+Z∈I, then Z∈D_j=[a−v_j,b−u_j]. The interval D_j has length at most L+δ. Since the Gaussian density is everywhere at most c,

μ(E∩{Y∈C_j}) ≤ μ(Y∈C_j,Z∈D_j)
= μ(Y∈C_j) γ_n(D_j)
≤ c(L+δ) μ(Y∈C_j).

Finite additivity and disjointness give

μ(E∩{|Y|≤M}) ≤ c(L+δ) μ(|Y|≤M) ≤ c(L+δ).

If E holds and |Y|>M, then |Z|=|(Y+Z)−Y|≥|Y|−|Y+Z|>M−R. Therefore

μ(E∩{|Y|>M}) ≤ γ_n({|z|>M−R}).

Combining the two parts yields the finite inequality

μ(E) ≤ c(L+δ) + γ_n({|z|>M−R}).                         (1)

Given any ordinary ε>0, choose δ so that cδ<ε/2, and then M so that the Gaussian tail is below ε/2. Equation (1) gives μ(E)≤cL+ε. Since μ(E) and cL are real, μ(E)≤cL.

There has been no appeal to continuity of μ, no integration against the Y-law, no infinite partition, no interchange of a finitely additive integral with a countably additive integral, and no conditional probability given a null state. Gaussian tail convergence concerns the specified ordinary marginal γ_n only.

### Sharper available form

The same proof replaces c(L+δ) by q_n(L+δ), where

q_n(r)=sup_x γ_n([x,x+r])=2Φ(r/(2sqrt(n)))−1.

Hence μ(E)≤q_n(L). The density version requested is a simpler sufficient estimate. No sharp bound is needed for the later incompatibility.

## 2. Past-complete consequences and the exact probability boundary

Use the convention ξ_j takes X_j to X_(j+1). Suppose positions are real-valued and the recurrence holds pointwise, and for each positive integer n the finite future block (ξ_−n,…,ξ_−1) is fresh relative to X_−n. Require the block's sum S_n to have the stated ordinary N(0,n) law and the rectangle-independence needed in Section 1. Full Borel block independence and its usual Gaussian product marginal provide a transparent sufficient assumption.

Since X_0=X_−n+S_n, for every bounded interval I,

μ(X_0∈I) ≤ length(I)/sqrt(2πn) for every n,

so μ(X_0∈I)=0. This is entirely compatible with real-valued finite additivity. It contradicts terminal-position tightness: tightness would require some bounded interval to have positive, indeed arbitrarily near-unit, mass. In particular it contradicts countable additivity of the X_0 marginal, because the countable unit intervals cover R. Joint countable additivity is unnecessary for this final contradiction.

One can state the exact needed exhaustion condition even more weakly: if μ(|X_0|≤M) tends to 1 as ordinary M→∞, the zero-interval conclusion is impossible. Any hypothetical joint law may be finitely additive elsewhere; this one marginal property already excludes it.

The assumption about the normal block sum should not disappear into ambiguous terminology. Under finite additivity, one should not invoke the countably additive π–λ uniqueness theorem automatically. The full countably additive noise marginal in the construction below supplies every needed block and sum law directly. For the bound alone, interval and tail distribution facts plus the specified independence suffice; a proof of those facts from a weaker independence convention would be an additional step.

### Why iid increments alone are insufficient

Take a genuine countably additive two-sided iid noise law and define X_0=0 and all other X_t by finite forward/backward sums. Then every recurrence holds, and the increments remain iid. Nevertheless X_−1=−ξ_−1, so that state is not independent of its next innovation. This is a precise failure of freshness, not a contradiction in the recurrence or in bi-infinite indexing.

Also, in a finitely additive setting separate probability-one recurrence statements do not automatically have a probability-one countable intersection. Each fixed finite-block estimate only needs finitely many recurrences, so it survives that limitation. The construction below avoids it altogether: all recurrences hold literally for every sample point.

## 3. A complete real-valued finitely additive law with genuine freshness

### One fixed measurable sample space

Let E=R^Z with its product Borel σ-algebra, and let Q be the ordinary countably additive product law of iid N(0,1) coordinates ξ_j. Let Ω=R×E with its product Borel σ-algebra. Write a sample as (x,ξ), and define

S_0=0;
S_t=Σ_(j=0)^(t−1) ξ_j for t>0;
S_t=−Σ_(j=t)^(−1) ξ_j for t<0;
X_t=x+S_t.

Every sum is finite. Every X_t is Borel measurable, and X_(j+1)=X_j+ξ_j holds pointwise for all integer j. The path map to R^Z is Borel measurable, so the eventual law can equally be pushed forward to the full Borel path-event σ-algebra.

For positive integer N, let U_N be normalized Lebesgue measure on [−N,N], and let P_N=U_N⊗Q. Thus the anchor X_0 is independent of the entire noise under each ordinary P_N. At negative times full freshness usually fails for P_N, which is why a limit argument must actually verify its restoration.

Fix one free ultrafilter U on the positive integers, and define for every Borel event A⊆Ω

μ(A)=lim_U P_N(A).

The scalar sequence lies in compact [0,1], so its ultralimit exists as an ordinary real. Positivity, normalization, and finite additivity pass through finite sums and ordinary real limits. This gives one finitely additive probability on the entire stated σ-algebra. The same fixed U is used for every event. No countable or uncountable diagonal selection is needed, and countable additivity is not claimed. The existence of a free ultrafilter uses the usual nonconstructive ultrafilter principle.

For every noise event C∈B(E), P_N({ξ∈C})=Q(C) at every N. Therefore the entire noise marginal of μ is exactly Q, not just a matching list of finite-dimensional distributions.

### Reanchoring comparison, with the normalization fixed

Fix t∈Z. Let R_(N,t) be the ordinary probability on the same Ω under which X_t is uniform on [−N,N] independently of the full noise ξ. In the original (x,ξ) coordinates this means x=u−S_t(ξ), where u∼U_N is independent of ξ∼Q.

Use total variation TV(P,R)=sup_A |P(A)−R(A)|. Two uniform probabilities on intervals of length 2N, displaced by s, have TV exactly min(1,|s|/(2N)). Conditional on ξ, the respective anchors in the (X_t,ξ) coordinates differ by S_t(ξ). Hence

TV(P_N,R_(N,t)) ≤ d_(N,t)
:= E_Q[min(1,|S_t|/(2N))] → 0.                         (2)

The convergence is ordinary dominated convergence under Q: S_t is finite Q-almost surely, and the integrand is bounded by 1. Gaussian moment estimates are unnecessary. Equation (2) holds uniformly over all Borel events on the common sample space, not merely finite-coordinate cylinder events.

### Full past–future innovation independence

Set

F_t=σ(X_s:s≤t; ξ_j:j<t),
G_t=σ(ξ_j:j≥t).

Under R_(N,t), each past position is X_t minus a finite sum of innovations with indices less than t. Thus F_t is contained in σ(u; ξ_j:j<t), which is independent of G_t under the ordinary product law. If A∈F_t and B∈G_t, and B corresponds to a noise event of Q-probability q, then

R_(N,t)(A∩B)=R_(N,t)(A)q.

By (2),

|P_N(A∩B)−P_N(A)q| ≤ 2d_(N,t) → 0.

Taking the fixed ultralimit gives μ(A∩B)=μ(A)μ(B). This proves full past–future σ-field independence in the rectangle sense. In particular it proves genuine finite-block innovation independence from the initial state, and not merely mutual independence among increments.

This statement is simultaneous for every integer t and every such pair of events: each equality follows from an ordinary vanishing error before taking the already fixed ultralimit. It does not rely on intersecting probability-one events or on a π–λ extension for μ.

There is an additional state-only property. Under R_(N,t), X_t is independent of the entire noise σ-field, including past innovations. The same uniform comparison shows

μ(X_t∈D, ξ∈C)=ν(D) Q(C),
ν(D):=lim_U U_N(D),

for every Borel D⊆R and C⊆E. This stronger statement concerns one position at a time, not the entire position process jointly independent of its own increments.

### Position means and lost tightness

The marginal ν is a normalized, real-valued finitely additive probability on Borel subsets of R. For every fixed a∈R, the uniform-shift TV bound gives ν(D+a)=ν(D). Thus ν is a translation-invariant position mean. Every bounded interval has ν-mass zero because U_N(I)≤length(I)/(2N)→0. The reanchoring argument gives this same marginal at every time.

Consequently ν is not countably additive: the countable unit intervals each have mass zero and together have mass one. Its failure is exactly at the position exhaustion step identified in Section 2. The entire innovation marginal, by contrast, is still countably additive.

Spatial translation invariance of the whole path law follows from the same fixed-shift TV estimate. Time stationarity follows by reanchoring at t and using shift invariance of Q; the discrepancy is bounded by d_(N,t), so it vanishes in the ultralimit. Stationarity is an additional property, not a premise needed for the concentration bound.

### Integer version

Replace R by Z, U_N by the uniform law on {−N,…,N}, and Q by the ordinary iid fair-sign product law. All definitions and arguments remain valid. For an integer shift s the uniform-shift distance is min(1,|s|/(2N+1)). The final position mean is translation-invariant on every subset of Z and gives every finite set mass zero. Full past–future freshness and the countably additive entire noise marginal remain intact.

### Exact scope of this construction

This is a coherent normalized, nonnegative, finitely additive path law with the stated independence identities. It does not assert countably additive position kernels, regular conditional distributions at null positions, countable conglomerability, stopping-time theorems, or a sampler for the final law. Such claims would require separate analysis. There is no assertion of uniqueness of the finitely additive extension.

## 4. Non-Archimedean values are a different statement

The requested theorem explicitly has real values, so its ε-removal is valid. If probability values instead lie in an ordered non-Archimedean extension, (1) still yields

μ(E)≤cL+ε for every positive ordinary real ε,

but that inference alone permits an infinitesimal excess above cL. Likewise an upper bound tending to zero through ordinary positive reals only gives a value that is zero or infinitesimal; it does not force exact zero.

A useful refinement prevents an overstatement of this caveat. For L>0 the maximal Gaussian interval mass q_n(L) is strictly below cL. Continuity permits δ>0 and a small ordinary tail bound such that q_n(L+δ)+tail<cL. The finite estimate then gives the advertised coarse bound even for ordered non-Archimedean values. For L=0 that strict-slack argument is unavailable. The sharp q_n(L) limit bound and the terminal zero-mass conclusion still require appropriate care. No non-Archimedean counterexample is claimed here; the scope of the proof's limit step is what is identified.

Nonstandard probability values, nonstandard state spaces, nonstandard time horizons, and standard-part operations are distinct choices. None is tacitly introduced into the real-valued theorem or the real-valued ultralimit construction.

## 5. Source-relative disposition

Primary inspected directly: Alexander Pruss, author post dated 2 September 2015, with the author-labelled reply dated 15 September 2015 at 10:37 AM, at https://alexanderpruss.blogspot.com/2015/09/from-past-infinite-causal-sequence-to.html .

The author's Gaussian follow-up says the earlier finite-additivity argument no longer works. A finite-partition and tail estimate repairs that particular route under explicit state–innovation independence. This is a qualification of the stated proof limitation, not a finding that the overall causal-finitism argument has been refuted.

## 6. Prior ownership and acceptance scope

P02 already owns careful separation of finite from countable additivity, measurable-singleton and support conditions, weak-limit failures, total-variation control, and existence-versus-effectivity distinctions. Tenth already owns the ordinary-mathematics representation/query boundary and compact inverse-system application. No credit is claimed for rediscovering those distinctions or for a new general probability theorem.

The scoped increment is the explicit use of those measure guards in this causal-history candidate: Gaussian finite-additive anti-concentration, the exact terminal-tightness contradiction, and a fully specified fresh-innovation finitely additive path law demonstrating the other side. The prior-owner search was targeted, not an exhaustive theorem-priority search. No frozen owner, report, canonical status, or accepted formal claim was changed.

Acceptance is limited to ordinary mathematical validity under the stated assumptions. It is not a new kernel-checked theorem, an empirical result, an externally reviewed publication, or an actual original-source participation finding.
