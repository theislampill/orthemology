# Independent adversarial review: bounded interaction detection

8 October 2026 UTC. Independent mathematical verdict on the supplied construction: **PASS**, with the scope and qualifications below. The final author-artifact and imported unary bindings are recorded in SOURCE_BINDINGS.json and REVIEW_RECEIPT.json. No preceding author or review file is modified.

## 1. Accepted claim and notation discipline

The inherited model has a known finite labeled root set R and a fixed, finite inventory of independent one-effect routes, with nonnegative integer multiplicities n_S for nonempty S⊆R. One static continuous strictly increasing endpoint-preserving coordinate calibration r_i is shared by every occurrence of root i. There are no guards, latent inventories, shared-gate substitutions, cross-talk, spontaneous routes, or within-route repeated root incidences. Thus

    Q(x)=∏_(nonempty S⊆R) (1−∏_(i∈S)r_i(x_i))^n_S.

Zero-count factors are omitted. In addition to an ordinary certified rational-accuracy pointwise population Cauchy oracle, the procedure receives an independently supplied integer M≥0 satisfying ∑_S n_S≤M. Correctness and termination are required for every valid oracle name. Under those premises, the construction finitely decides every positive support. The earlier positive-interaction half-integer procedure then finitely recovers all multi-root multiplicities. A small further half-integer procedure also finitely recovers unary multiplicities on interacting roots. The remaining count possibilities are exactly the finite positive-integer simplex described in §7.

For clarity this review writes A_min for the union of Boolean-minimal positive supports and I for the union of positive supports of size at least two. These are generally different sets. For example, with positive supports {a} and {a,b}, A_min={a}, whereas I={a,b}. With only a unary a route, a belongs to A_min but not I. Detection lower bounds on A_min are not claims that those calibration maps have been fully identified.

No count ceiling is inferred from the response function. M is a model promise, and the procedure does not certify that an arbitrary oracle satisfies it or the other model assumptions.

## 2. Boolean corners are finitely decidable

For X⊆R, query the command vector 1_X. Every present route has success probability either zero or one, so

    Q(1_X)=0  iff some positive support S is contained in X;
    Q(1_X)=1  otherwise.

One query of tolerance 1/8 separates the cases by a strict comparison with 1/2, even when the approximation center lies outside [0,1]. This relies on the discrete endpoint promise, not an illicit exact-real equality test. All finitely many corners determine the upward-closed family of X containing a positive support, hence its inclusion-minimal antichain C. An element T∈C is itself a positive support: if a smaller positive support existed inside it, T would not be minimal. Conversely every minimal positive support is detected.

If Q(1_R)=1, the inventory is empty. Return all counts zero before forming any expression involving 1/M or the minimum-support lower bounds. If M=0, the supplied promise already forces this branch; no probability query is needed. The empty root set also has only the empty inventory. It is permissible to use the corner query as a consistency check, but no assurance is made for invalid promises.

Set A_min=⋃C and B=R\A_min. Every positive support S contains an inclusion-minimal positive support T⊆S because the finite family of positive supports contained in S is nonempty. Therefore S∩A_min≠∅, and no positive route lies wholly in B. This hitting property, rather than any mistaken equality A_min=I, is the key fact.

## 3. Data-dependent rational rate lower bounds

Fix one common rational interior command vector b, for example b_i=1/2 for every root. Use exactly the same b_i in every minimum-support query and every later mixed-grid query. Put a_i=r_i(b_i)∈(0,1).

For T∈C, mask all coordinates outside T to zero. Since T contains no smaller positive support,

    Q_T=(1−p_T)^n_T,    p_T=∏_(i∈T)a_i∈(0,1),    1≤n_T≤M.

Consequently Q_T<1. Query at dyadic tolerances tending to zero and form a rational upper bound q_T^+ from each certified response interval, clipped to [0,1] if desired. Eventually q_T^+<1. This holds for every valid name: the upper endpoint is at most Q_T+2ε, so any ε<(1−Q_T)/2 suffices, though that unknown threshold need not be given to the algorithm.

Bernoulli's inequality gives

    1−Q_T = 1−(1−p_T)^n_T ≤ n_T p_T ≤ M p_T.

Since q_T^+≥Q_T,

    p_T ≥ (1−q_T^+)/M > 0.

Every a_i with i∈T is at least p_T, because all the other factors lie in (0,1]. Therefore the computable rational number

    λ_i=max_(T∈C, i∈T) (1−q_T^+)/M

satisfies 0<λ_i≤a_i for every i∈A_min. The maximum is over a nonempty finite family. The direction of both inequalities is correct; an upper probability bound, rather than a lower bound, belongs in 1−q_T^+.

This step uses only n_T≤M. A separately supplied valid upper bound on every minimal-support multiplicity would suffice for detection; a total ceiling is one way of providing it. A per-support ceiling must not later be substituted for the total budget used to restrict isolated unary gauges.

No lower bound on a_i is asserted for i∈B. None is needed, because those coordinates will be placed only at their known calibrated endpoints. Combining bounds obtained at different nominal commands without monotonic comparison would be invalid; the common b removes that problem.

## 4. The mixed grid and exact double inversion

For U⊆A_min and V⊆B, let x_(U,V) put b_i on U, one on V, and zero elsewhere, and write Q_(U,V)=Q(x_(U,V)). A present route S contributes nontrivially only when S∩A_min⊆U and S∩B⊆V. Every such route contains an A_min coordinate at a true interior rate, so its success probability is strictly below one. Every inactive route has success probability zero. There are finitely many routes, hence every raw Q_(U,V)>0. This remains true when all B coordinates are one.

Define a_S=∏_(i∈S)a_i for S⊆A_min. Then

    Q_(U,V)=∏_(∅≠T⊆U, H⊆V) (1−a_T)^n_(T∪H).

For every nonempty T⊆A_min and every H⊆B, INCLUDING H=∅, form

    Z_(T,H)=∏_(U⊆T, V⊆H) Q_(U,V)^[(-1)^(|T|−|U|+|H|−|V|)].

Each factor associated with support T'∪H' has exponent coefficient

    [∑_(T'⊆U⊆T)(−1)^(|T|−|U|)]
    ×[∑_(H'⊆V⊆H)(−1)^(|H|−|V|)],

which is one precisely when T'=T and H'=H, and zero otherwise. Supports not contained in T∪H never enter the grid products. Thus

    Z_(T,H)=(1−a_T)^n_(T∪H).

All divisions are by strictly positive raw probabilities. No zero-valued endpoint probability is divided out, no raw log at a zero is taken, and no cancellation of infinities occurs. When U is empty every grid probability is one, because no route lies wholly in B; retaining those factors is harmless.

The H=∅ case is indispensable: if it were omitted, a positive nonminimal support contained entirely in A_min would be missed. For example, positive supports {a}, {b}, and {a,b} give A_min={a,b}, B=∅; restricting H to nonempty subsets would test nothing at all.

## 5. Certified support decisions terminate for every name

Let

    δ_T=∏_(i∈T)λ_i>0.

If n_(T∪H)=0, the isolated value is exactly one. If n_(T∪H)≥1, then a_T≥δ_T and

    Z_(T,H)=(1−a_T)^n_(T∪H)≤1−a_T≤1−δ_T.

Use the rational threshold τ_T=1−δ_T/2. The true value lies strictly above τ_T in the absent case and strictly below τ_T in the present case. It is never equal to the threshold.

Here is an explicit interval procedure with no hidden equality oracle or calibration modulus. Requery the finitely many raw Q_(U,V) values involved at tolerance ε_j=2^(−j). Intersect each returned interval with [0,1]. Once every denominator lower endpoint is positive, interval multiplication and reciprocal operations provide a rational enclosing interval [L_j,U_j] for Z_(T,H). If U_j<τ_T, return present. If L_j>τ_T, return absent. Otherwise increase j.

For each fixed true positive denominator q, every valid name's lower endpoint is at least q−2ε_j. Hence it is eventually positive. On a finite neighborhood of the actual vector of positive raw probabilities, the finite rational product/quotient map is continuous, and the intervals shrink to the actual vector. Consequently U_j−L_j→0. This elementary convergence statement is sufficient: the algorithm tests its actual rational bounds, rather than asking for an unknown rate of convergence. Since the true isolated value has distance at least δ_T/2 from τ_T, one of the strict stopping tests eventually holds. Nonnested intervals and arbitrary valid rounding choices do not affect this conclusion.

The construction never treats failure to detect Z<1 as proof of absence. It decides absence only after a computed interval has crossed the explicitly separated rational threshold. The gap is learned from the supplied ceiling and coarse-to-fine minimum-support observations.

There are only finitely many T,H and all purely-B supports are already known absent, so every support decision terminates after finitely many certified pointwise population queries. The support stage uses finitely many distinct rational command vectors: corners, minimum-support masks at b, and the mixed grid. Repeated precision queries remain necessary. There is no uniform accuracy, sample, or runtime claim.

## 6. Recovery of all anchored multiplicities

### 6.1 Multi-root supports

Support detection supplies exactly the positivity promise required by the earlier finite-panel appendix. For each detected S with |S|≥2, choose two roots, two strictly ordered rational interior commands on each, and fixed rational interior commands on the others. Masking outside S and Boolean-lattice inversion yield four isolated values

    Z_pq=(1−K a_p b_q)^n_S.

All raw values are positive. The previously proved strict determinant sign is sign(m−n_S) for candidate m>0. At half-integer m no integer n_S can equal m, so certified rational-root and determinant intervals eventually exclude zero. Binary search on [1,M] recovers n_S, or the earlier doubling routine may be used. No absent support is passed to the nonzero-sign procedure.

### 6.2 Anchored unary extension: corroboration of the separate lemma

The separately authored and reviewed `finite-hypergraph-calibration` stage owns the general two-level unary sign lemma. The proof below is independent corroboration, not a competing primary derivation. The final unary file and its scoped superseding review receipt are bound by exact digests in SOURCE_BINDINGS.json. The final revision only clarifies that this particular sign loop stalls at zero; it makes no broader absence-impossibility claim.

Let i∈I have a present unary support with multiplicity m>0. Choose any detected positive interaction S containing i. Its multiplicity n is now known. Fix every other command in S at an interior rational value, and choose two rational commands u_1<u_2 for i. Put a_k=r_i(u_k), so 0<a_1<a_2<1, and let K be the positive product of the other fixed true rates. Interior mask inversion gives

    Z_k=(1−K a_k)^n,    U_k=(1−a_k)^m.

The quantities P_k=1−Z_k^(1/n)=K a_k are Cauchy computable by certified positive integer-root bisection. For a positive candidate h, put R_k(h)=1−U_k^(1/h). With c=m/h and H_c(z)=1−(1−z)^c,

    D(h)=R_2(h)P_1−R_1(h)P_2
        =K a_1a_2 [H_c(a_2)/a_2−H_c(a_1)/a_1].

The explicit known function H_c has H_c(0)=0 and

    H_c''(z)=−c(c−1)(1−z)^(c−2).

For c>1 it is strictly concave, so H_c(z)/z is strictly decreasing for z>0. For 0<c<1 it is strictly convex, so the quotient is strictly increasing. For c=1 the quotient is one. Therefore

    sign D(h)=sign(h−m),

with zero only at h=m. The determinant orientation is correct. Strict concavity/convexity follows directly from the displayed derivative or the chord inequality; no unknown calibration is differentiated.

At h=k+1/2, 1/h=2/(2k+1), so only rational powers computed by rational root brackets are needed. The isolated raw values are positive, their intervals shrink, and the true D(h) is nonzero. Thus its sign is eventually certified for every valid name. Binary search on the finite interval [1,M] recovers m. Absent unary supports were already set to zero and are not subjected to this positive-count search.

This extension identifies each anchored unary count without reconstructing an entire calibration map or taking an uncertified boundary limit. It uses only finitely many extra rational command vectors and arbitrary-precision queries to their population values.

## 7. Exact residual count fibre under the total ceiling

Let J={i∉I:n_{ {i} }>0} and k=|J|. The support decisions identify J. Let N_fixed be the sum of all recovered multi-root counts and all recovered unary counts for roots in I. Set L=M−N_fixed. The true-world promise guarantees L≥k.

The full set of multiplicity vectors observationally equivalent to the true law, while retaining the same total ceiling M, is obtained by retaining all recovered/zero counts and choosing

    (m_i)_(i∈J) ∈ Z_(≥1)^k,    ∑_(i∈J)m_i≤L.

Necessity follows from the inherited full-law equivalence theorem: positive supports and all interaction-anchored counts are fixed, isolated positive-unary counts remain positive, and the total cannot exceed M.

Sufficiency is explicit. If the actual isolated unary count is n_i, replace its calibration by

    r_i'(x)=1−(1−r_i(x))^(n_i/m_i).

This is another continuous strictly increasing endpoint-preserving homeomorphism and preserves that root's entire unary factor. Isolated means the root occurs in no interaction, so the replacement changes no other factor. Apply the replacements independently for all i∈J. Their only coupling is the total-count inequality. Unused roots retain zero counts and have arbitrary allowed calibration maps. Hence there is no further hidden compatibility restriction on the displayed count simplex.

If k=0, every count is fixed regardless of unused budget. If k>0, the count fibre is a singleton exactly when L=k, in which case all isolated positive-unary counts equal one. If L>k, each isolated root individually can take any integer from 1 through L−k+1, with choices jointly constrained by the sum. Thus it is false to describe every isolated unary count as always ambiguous under a total ceiling, and false to give every such root an independent unrestricted range up to M.

The simplest collapse example has a single positive unary support and M=1. An ambiguity example has its response Q(x)=(1−x)^2 and M=2: count two with r(x)=x and count one with r'(x)=2x−x^2 obey the same ceiling and give the same entire law. With two isolated roots and residual budget three, the feasible pairs are (1,1), (1,2), and (2,1); (2,2) is excluded by the total ceiling.

The count-fibre statement does not say that finitely many query values reconstruct arbitrary complete continuous calibration maps. Unused-root calibration freedom remains even when the count fibre is a singleton.

## 8. Independent controls and preservation

`independent_controls.py` was written independently in this review directory. The support algorithm receives only certified rational approximation intervals for raw Q values. It does not receive exact isolated values, true support labels, calibration rates, or equality flags. Hidden fixture values are used to generate valid names and validate the final output.

The controls exercise four fixed total oracle-name styles: centers at Q+ε, centers at Q−ε, a deterministic alternating choice, and dyadic downward rounding. Replies need not be nested and may require clipping to the population-probability range. Every selected query has a fixed reply determined by the world, command, tolerance, and style, rather than an adaptive world choice.

Observed results in `INDEPENDENT_CONTROLS.json`:

- 1,216 world/name runs and 9,740 support decisions, all correct.
- Exhaustive count inventories for selected root sizes through four, plus stress fixtures.
- Empty inventory, M=0, empty root set, H=∅, overlapping minimal supports, absorbed higher-order supports, entirely unused B roots, very small A rates, and very small raw denominators.
- 32 complete anchored-unary recoveries and 168 strictly nonzero half-integer sign certifications, with lower-order nuisance routes present.
- 20 finite simplex controls covering empty, collapsed, and ambiguous isolated-unary fibres.
- 631,925 raw-oracle queries and a largest requested precision of 94 bits in these particular tests. These are diagnostic observations, not theorem bounds.
- SHA-256 checks confirm that all 91 bound files from the preceding anchor, anchor-review, absence-obstruction, and absence-review directories remain byte-identical.

The author’s `exact_controls.py` was copied into `author_replay` and executed there. All 18,101 assertions pass, and the replay JSON is byte-identical to the author’s JSON. The original author file was never executed in place or modified.

Finite controls do not establish all-name correctness, arbitrary-count correctness, or arbitrary-homeomorphism termination. Those conclusions rest on the proofs above and the inherited multi-root sign theorem.

## 9. Conditional known-count cover: the same gap without a target ceiling

This corollary is the same lower-bound/gap mechanism under a different supplied premise. It was proposed in the finite-hypergraph-calibration review and assigned to this detection stage; it is not a separately credited rediscovery of the gap argument.

Let G be a finite supplied family of positive supports, each with a known positive integer count n_S, and let T be a nonempty target support with T⊆⋃G. The target count may be zero or any finite positive integer, and no target-count ceiling is supplied. Counts on G may, for example, have been recovered using the earlier interaction procedure after their positivity was independently established. Neither positivity of G nor knowledge of its counts is inferred merely by calling it a cover.

At one common rational interior base b for every involved root, form the ordinary interior masked contrast Z_S for each S∈G. All raw probabilities are positive. Known n_S makes

    P_S=1−Z_S^(1/n_S)=∏_(i∈S)r_i(b_i)>0

Cauchy computable using rational-root bisection and positive-denominator operations. Refine its rational interval until the lower endpoint ell_S is strictly positive. That search terminates for every valid name, and 0<ell_S≤P_S≤r_i(b_i) for every i∈S. For each covered root set λ_i=max_(S∈G, i∈S)ell_S. Every target root has a positive such bound.

The ordinary interior target contrast obeys

    E_T=(1−∏_(i∈T)r_i(b_i))^n_T.

Set δ=∏_(i∈T)λ_i>0. Then E_T=1 when n_T=0, and E_T≤1−δ for every n_T≥1. The same strict interval comparison at 1−δ/2 therefore decides target presence and absence after finitely many refinements. No target-count upper bound is used in this argument. This includes unary targets and targets whose roots are covered by different known supports; those known supports may contain additional roots outside T.

No full-rank support-incidence condition is required: a known positive support product bounds each of its factors from below even when those factors are not individually identified by the finite panel.

This conclusion is limited to entirely covered targets and the common-base/shared-map contract. It supplies no unconditional discovery of initial positive supports or counts, no information about an uncovered target, and no escape from the unbounded absence obstruction. If G covers all known roots, the corollary conditionally decides all supports, but the supplied known-count cover is then a substantial additional premise.

Independent `conditional_cover_controls.py` checks 104 covered target/world/name combinations, including zero and positive target counts, unary and higher-order targets, and roots outside the cover. All pass. Four targets containing an uncovered root are rejected without querying or claiming absence. These controls use 3,949 raw-oracle queries and at most 42 requested bits in the tested fixtures; again, these are observations rather than theorem bounds.

## 10. Discovering an interaction cover without a total ceiling

A second sufficient contract is valid: R is finite and known, no total count ceiling is supplied, and **every root in R** is promised to belong to some positive multi-root support. This is stronger than saying every used root is covered. It also specifically requires multi-root supports: unknown isolated unary counts cannot be recovered merely from their positivity.

Choose one common rational interior base. For each of the finitely many candidate supports S⊆R with |S|≥2, its ordinary interior masked contrast satisfies E_S=1 when absent and E_S<1 when present. All raw Q values used in these masks are positive, even before any cover is known, because every nonzero command is interior.

Use fair rounds. In round j, request finitely accurate intervals for each unresolved candidate's raw values, attempt one finite interval product/quotient evaluation, and certify positivity only if its upper contrast endpoint is strictly below one. If a denominator is not yet bounded positively or a contrast interval still touches one, leave that candidate unresolved and advance to the next candidate/round. Never wait indefinitely inside the positivity test for a particular candidate.

Each genuinely positive support is eventually certified: its positive raw denominators are eventually separated from zero, its contrast interval shrinks to E_S<1, and its test is revisited at arbitrarily fine tolerances. An absent support never receives a false certificate. Each newly certified support can be sent to the inherited positive-interaction count routine, using unbounded doubling followed by half-integer binary search. That subroutine terminates on the certificate's guaranteed positive finite integer count. It is safe to finish these count searches sequentially: there are finitely many candidate supports and each such inserted computation is finite. Alternatively they may be dovetailed.

Maintain the union of supports whose positivity and counts have both been established. Stop this stage only when that union equals R. Under the stated promise, a finite family of genuine positive interactions covers R. Each member has a finite certification round and a finite count-recovery computation. Taking the maximum of the finitely many certification rounds and including the finite inserted computations proves that the stopping condition is eventually reached. This proof needs no computable bound on the unknown rounds, determinants, rates, or counts.

Now apply §9 to this actually certified known-count cover. It decides every support because every target root is covered. Recover every remaining positive multi-root count with the same unbounded half-integer searches. For every positive unary support, use an incident known-count interaction and the imported unary sign lemma, again with unbounded doubling/cuts. All roots are interaction-anchored, so no isolated positive-unary count gauge remains. The output is the entire discrete support/count inventory, not whole calibration functions.

If R is empty, the empty inventory is returned immediately. A nonempty singleton R cannot satisfy the multi-root-cover promise. Without the coverage promise, the same scheme is a sound partial procedure: it completes only when an actual known-count cover is certified, and on such a completion its output is correct. It may run forever in a world with an uncovered root. Finite waiting, a finite collection of failed positivity tests, or nontermination supplies no negative support inference. No arbitrary timeout is part of the theorem's stopping condition.

Independent `cover_discovery_controls.py` executes the actual positivity-round discovery, interaction count recovery, covered-root gap decisions, and anchored unary searches with no total-ceiling argument. The replay passes 18 complete world/name runs, 52 positive-count searches, and 168 certified half-integer signs; eight bounded partial-run checks produce no spurious cover. It uses 46,972 raw queries and at most 34 precision bits in these fixtures, not as a uniform guarantee. Finite partial-run harness checks are explicitly time/round-limited tests of non-spurious certification; they do not prove nontermination or turn an unresolved run into an absence decision.

## 11. Scope and non-transports

The known total ceiling excludes the nuisance-count sequence used in the unrestricted absence obstruction; there is no contradiction. The new result distinguishes the supplied ceiling promise from a response-function continuity modulus and never claims to infer that ceiling from data. It uses calibrated endpoints for B, not an unavailable interior lower bound or an assumed identity calibration on B.

This is a certified population Cauchy-oracle result. Empirical frequencies, confidence intervals with nonzero failure probability, or a finite Bernoulli sample do not meet that oracle contract. No uniform precision/sample/runtime theorem follows. The argument does not physically establish independent routes, homeomorphic calibration, warranted intervention access, bearer identity, metaphysical existence/nonexistence, source-level productive sufficiency, integration authorization, owner acceptance, or T20 closure.

No mathematical blocker was found in the construction when H includes the empty set, the common-base discipline is retained, the M=0/empty branch precedes division, and the total-ceiling count fibre is stated jointly as above.
