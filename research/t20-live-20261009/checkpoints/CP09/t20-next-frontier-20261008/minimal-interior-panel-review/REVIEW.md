# Independent review: minimal retained-interior panel

8 October 2026 UTC. Verdict: the proposed 2D combinatorial theorem and finite-depth statistical support consequence are correct with the qualifications below. This review independently derived the result from the threshold semantics before reading the author's new proof. It inspected `retained-interior-certificate/RetainedInterior.lean` and its `RESULT.md`. The existing Lean source proves the staircase witness injection, not the new minimum-panel theorem or absolute-continuity theorem. No new Lean/kernel assurance is claimed.

## 1. Exact combinatorial statement and derivation

A route with threshold (u,v) hits (x,y) iff u≤x and v≤y. The endpoint is the union of finitely many such upper rectangles, with the same thresholds retained across queries. Let P,N be finite positive and negative query sets. First reject inconsistency: p≤z coordinatewise for some p∈P,z∈N. Otherwise discard duplicate positives and every positive that dominates another positive. The remaining minimal positives can be uniquely ordered as

    p_i=(x_i,y_i),  x_1<...<x_k,  y_1>...>y_k.

The strict inequalities follow from minimality; equal-coordinate or duplicate input queries cause no exception after reduction. Covering these positives covers all discarded positives.

For each negative z=(a,b), define

    L(z)=max({i:x_i≤a}∪{0}),
    R(z)=min({i:y_i≤b}∪{k+1}).

Consistency gives L<R. A route covering the contiguous block p_s,...,p_t can be replaced by the most restrictive corner (x_s,y_t). This replacement still covers the block, and avoids z precisely unless s≤L and t≥R. Thus, if L≥1 and R≤k, z requires at least one cut in the nonempty integer interval

    I_z={L,L+1,...,R−1} ⊆ {1,...,k−1}.

Negatives with L=0 or R=k+1 impose no constraint. It is important to discard these negatives rather than introduce intervals containing fictitious cuts 0 or k.

Every threshold route covers a contiguous interval of the antichain indices (possibly empty). A cover by r such intervals admits a partition into at most r contiguous nonempty blocks, each contained in one covering interval: starting at the first uncovered index, choose an interval containing it with farthest right endpoint and finish that block at its endpoint. A selected interval cannot be selected again. Replacing each block by its corner preserves all positive labels and cannot create a negative hit, since its original covering route already avoided all negatives. Conversely, every set of cuts stabbing all I_z yields an admissible block-corner realization. Therefore, for k>0,

    minimum routes = 1 + minimum number of cuts stabbing all I_z.

The case P=∅ has minimum zero, not one. Inconsistent transcripts have no finite realization, so the formula is not a certificate theorem for arbitrary contradictory labels.

No probabilistic, independence, calibration, or physical-access premise enters this derivation. For unrestricted monotone coordinate-separable Boolean AND gates, finite restrictions are also suffixes in each coordinate, so the same finite rectangle reasoning applies; arbitrary monotone two-variable gates do not satisfy the required semantics.

## 2. Sharp query bound

Writing h for the minimum stabbing number, h≤k−1 and h≤|N|, because all cuts stab all intervals and one chosen point per interval is another cover. Consequently, for a nonempty consistent positive set,

    minimum routes ≤ min(k, |N|+1).

If a realizable transcript certifies at least m≥1 routes, it must have at least m positive queries and m−1 negative queries. Thus at least 2m−1 queries are necessary. Dominated positives, repeated queries, and irrelevant negatives cannot reduce this number. The m-point strict staircase with m−1 adjacent negative connectors attains it: every connector's interval is a singleton cut. All coordinates can be strictly inside (0,1).

The bound applies to individual finite transcripts, and hence to every branch of a binary adaptive policy. It does not identify a route count from every transcript, and it does not mean that every alternative produces the witness event.

## 3. Robust open realization and exact-count padding

The combinatorial statement is an at-most-route realization result. Moving to exactly n independent full-support routes requires a separate argument; this cannot be omitted.

For commands in [0,1]^2, suppose every positive has both coordinates >0, and no negative equals (1,1). For k>0, use block corners as above. For each negative and each block corner, at least one threshold coordinate exceeds the corresponding negative coordinate strictly. There are only finitely many such comparisons. Move both corner coordinates down by a sufficiently small positive amount: thresholds remain inside (0,1)^2, every covered positive is hit with strict margins, and every negative remains missed with a strict margin. Small open boxes around these moved corners retain all labels. Upper-face positives at coordinate 1 cause no problem. Equality in an original positive hit causes no problem either; no equality-null argument is needed.

Additional routes can be put in a sufficiently small neighborhood of an already constructed route: duplicating its positive/negative pattern changes no endpoint labels. Alternatively, place them near (1,1), avoiding every negative. With no positives, the near-(1,1) construction realizes all-negative transcripts with any prescribed positive number of routes. The excluded negative (1,1) is exactly the obstruction to that construction.

Thus every such transcript whose minimum is ≤n has a nonempty product-open realization with exactly n routes. If baseline route-pair laws independently give positive probability to every nonempty open rectangle in (0,1)^2, that transcript has positive baseline probability. Independence here is between occurrences; the two coordinates within a route need not be independent. Independent nonidentical route laws also work.

This addresses the essential boundary caveat: an empty inventory realizes a negative at (1,1), but a positive inventory with thresholds in the square does not. Minimum zero alone is not enough to justify padding. Similarly a positive on x=0 or y=0 is realizable by boundary thresholds but not by thresholds confined to the open square.

## 4. Measurable adaptive policies and absolute continuity

A clean sufficient formulation is:

- n≥1, commands lie in [0,1]^2, and outputs are noiseless retained-threshold endpoint bits;
- baseline has exactly n independent route pairs, each with full support on (0,1)^2;
- alternative has a nonempty finite inventory of route pairs lying in (0,1]^2 almost surely (its count and dependence are immaterial for this direction);
- the same measurable policy is used in both worlds, with the same law for all its external random seeds, independent of the latent thresholds;
- each branch makes at most 2n queries.

Package all external policy randomness in a seed S. For each fixed seed and each binary word w, the policy specifies finitely many fixed query values along that word. A realizable alternative word has the needed boundary conditions: positive axes are impossible, and a negative at (1,1) is impossible. Its minimum route count is ≤floor((length(w)+1)/2)≤n, including the separate all-negative case. The open-realization argument therefore makes that word baseline-positive whenever it is alternative-positive.

For fixed s this proves absolute continuity of the finite bit-word law. Integrating over the common seed law proves absolute continuity of the joint (S,w) law: if a measurable event has baseline integral zero, its baseline conditional probability is zero for almost every s, and its alternative conditional probability is then zero for those same s. Any recorded transcript, including real-valued query coordinates, seed disclosure, policy stopping information, or a measurable postprocessing, is a measurable function of (S,w), so its alternative law is absolutely continuous with respect to its baseline law.

Variable stopping is handled by encoding stopped words separately (a finite alphabet) or by a deterministic padding convention. Padding must not accidentally count as additional probes beyond the depth bound. Continuous query values do not create an uncountable set of output branches once the seed is fixed. A proof that only compares unconditional probabilities of individual real-valued transcript atoms would be invalid; all such atoms can have probability zero in both models.

At 2n+1 probes the fixed interior staircase supplies a baseline-zero event. It is alternative-positive when the alternative route pairs are independent with full support on the open square. This additional support/independence assumption is used for the separating direction, not the ≤2n domination direction. Under the full stated independent, full-support, continuous-threshold assumptions both directions follow. This is a sharp support-separation depth, not a claim that laws below the threshold are equal or that their KL is finite.

A common seed must not secretly encode latent thresholds. Matching its marginal law alone is insufficient: conditioning on a correlated seed need not preserve route full support, and observing such a seed can already distinguish worlds. The policy must also be genuinely common, with no model-dependent side information or query choices.

“Continuous” should mean atomless coordinate marginals, or, more generally, simply state strictly positive threshold coordinates in the unit square almost surely. An atomless joint measure alone is insufficient: a mixture of open-square uniform mass and uniform mass on x=0 is atomless as a measure on pairs and has full support, yet a positive at (0,1) is possible under that alternative and impossible under a uniform baseline after only one query. Full support of occurrence marginals without between-occurrence independence likewise does not ensure the product-open realization has positive probability.

## 5. The genuinely two-dimensional boundary

In three dimensions take positives

    (3/4,1/4,1/4), (1/4,3/4,1/4), (1/4,1/4,3/4)

and the single negative (1/4,1/4,1/4). A route hitting any two positives must hit their coordinatewise minimum, which is the negative. Thus four queries require three routes, contradicting the putative universal five-query lower bound. There is a robust three-route realization by lowering the positive corners slightly, so this is not an equality-only pathology. The 2D interval ordering is essential.

## 6. Actual independent checks and assurance

`independent_checks.py` compares the interval answer against a separate exhaustive subset-corner/set-cover search, not against another implementation of the interval construction. It passed:

- all 19,683 absent/positive/negative panels on a 3×3 grid;
- 1,500 seeded random panels on a 4×4 grid;
- sharp staircases for m=1 through 8;
- the three-dimensional four-query/three-route counterexample.

The initial checker run exposed only an implementation sentinel bug: an impossible subproblem returned 100 and adding a route returned 101; replacing the sentinel with infinity fixed it. The complete rerun passed and is retained in `CHECKS.log`. These finite controls corroborate, but do not replace, the mathematical proof, and do not verify the measure-theoretic theorem computationally. No source/package/repository files outside this reviewer sibling were changed. No physical count, favorable sample complexity, philosophical conclusion, or T20 closure follows from this review.

## 7. Final author reconciliation and freeze

At 20:43 UTC, the completed author proof in `minimal-interior-panel/RESULT.md` was read and reconciled against this independent derivation. Its stronger arbitrary nonempty finite source-inventory theorem, (0,1]^2 boundary scope, exact-count open padding, interval duality, joint seed/leaf integration, reverse absolute-continuity remark, and explicit non-KL scope are accepted. Two wording fixes were requested and verified: the zero-boundary counterexample explicitly uses a target law supported in the open square, and ambiguous wording about singular measures was removed. Neither changed the theorem.

Accepted author RESULT.md SHA256: `c35abf8d96720c8ee9c611fc554db647990c0f0233e630dee0792939a75b0dc7`. Author-reported larger finite control counts are not represented as independently rerun here; this reviewer's own executed checks are listed in section 6. This reviewer packet is frozen after this reconciliation.
