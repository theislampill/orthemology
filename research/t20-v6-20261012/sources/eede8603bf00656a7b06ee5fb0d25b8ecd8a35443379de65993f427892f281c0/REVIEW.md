# Independent review of universal Bayes preservation for probability classes

10 October 2026 UTC. Ordinary mathematical review of the exact author packet bound in INPUT_BINDINGS.json.

## Verdict and evidence level

**No required mathematical correction found.** The total-variation classification, Polish weak-closure classification, principal generated classes, and bounded-positive non-surjectivity example are correct with the author's explicit hypotheses and quantifiers. The proofs establish the infinite-space statements by ordinary mathematical arguments; finite examples or hash checks are not being substituted for those arguments.

This is an independent AI review within the same assistant workflow, not external peer review. The reviewer did not author or edit the target packet. The parent had supplied candidate proof ideas to the author; independence here means a separate proof and source check, not an independently originated research programme. No Lean or other formal-kernel verification was performed. This report gives no field-novelty, protected-integration, release, audit-closure, or T20-closure conclusion.

## Exact statement accepted

Let P be all countably additive probability measures on an arbitrary measurable space (X, Sigma), and let G be all measurable likelihoods with an everywhere positive lower bound and finite upper bound, both allowed to depend on the likelihood. For a nonempty convex TV-closed C contained in P, the following are equivalent:

- Every G-update of every member of C remains in C.
- C is a face of the full P.
- If p is in C and q is a probability with q absolutely continuous with respect to p, then q is in C.
- Every nonnegative measurable likelihood update remains in C whenever its normalizer at the current prior is finite and strictly positive.

For Borel probabilities on a Polish X, a nonempty weakly closed convex universally G-preserved class is exactly P(F), the probabilities carried by a unique nonempty closed F. The same classifications therefore hold when the universal likelihood family is enlarged to all bounded everywhere strictly positive likelihoods, or to all defined nonnegative integrable likelihoods.

Here TV is sup_A |p(A)-q(A)|. Weak convergence tests all bounded continuous real functions, and closure is relative to P(X). “Carried by F” means mass one on F, not support exactly F. Preservation initially means forward inclusion. The ambient space is the full countably additive probability simplex, not a moment-constrained or otherwise smaller ambient convex set.

## Total variation proof checks

### Normalization and measurable versions

Both admitted positive likelihood classes have strictly positive integrals at every probability: if a measurable function is positive everywhere, the union of the sets where it is at least 1/n is X. Its integral cannot be zero. Boundedness makes the integral finite. An arbitrary nonnegative likelihood is used only at priors with an explicitly finite positive normalizer.

For a strict decomposition p=tq+(1-t)r, q is absolutely continuous with respect to p and q(A) is at most p(A)/t for every measurable A. Finite-measure Radon–Nikodym applies on an arbitrary measurable space. A nonnegative measurable derivative can be clipped to [0,1/t] without changing its integrals: the set on which clipping changes it is itself measurable and p-null. This does not require completion or measurable singletons.

### Universal preservation forces the face condition

For the bounded derivative f=dq/dp, f+epsilon is in G for each epsilon>0, and its posterior is exactly (q+epsilon p)/(1+epsilon). Subtracting q gives epsilon(p-q)/(1+epsilon), so the stated TV distance and convergence are exact. TV closure gives q in C; the analogous derivative for r gives r in C. Arbitrary strict t is covered, not merely t=1/2. Convexity is supplied by the standing assumption.

### Closed faces admit arbitrary absolute continuity

For q absolutely continuous with respect to p, the author's f_n=min(f,n), a_n=integral f_n dp satisfy 0<a_n<=1 and a_n increasing to 1. In particular the formula q_n=(f_n/a_n)p never divides by zero. The coefficient t_n=a_n/(2n) lies in (0,1), and t_n q_n has density at most 1/2 relative to p. Consequently the residual r_n is a nonnegative countably additive probability, and the face property applies.

The L1 error bound is valid even when f is unbounded:

    integral |f_n/a_n-f| dp <= 2(1-a_n).

Thus q_n tends to q in TV, and closure gives q in C. This is the only extension from bounded density to arbitrary absolutely continuous probability in that implication. Every defined posterior is absolutely continuous with respect to its prior, which completes the remaining implications. The direct bounded-update decomposition with t=Z/(2M) is also valid, including constant likelihoods; it never degenerates to a coefficient of one.

### Principal classes and orbit closure

D(p)={q:q is absolutely continuous with respect to p} is TV closed because TV convergence preserves zero mass on each p-null measurable set. It is convex, and a positive convex component of a member of D(p) cannot charge a p-null set, proving its face property. The preceding implication establishes its minimality among TV-closed faces containing p.

The exact G-orbit has densities bounded above and bounded away from zero p-almost everywhere. Such a density admits an everywhere bounded positive measurable version; conversely normalizing a G-likelihood has those essential bounds. For any q in D(p), densities proportional to min(dq/dp,n)+1/n converge in L1 to dq/dp. This verifies the claimed orbit closure and both principal-class descriptions.

These are descriptions of classes generated by one prior. The author does not assert that every TV-closed face is D(p) for one p. The weaker “mutual absolute continuity alone gives a G-update” would be false: on (0,1], densities 1 and 2x are mutually absolutely continuous, but their ratio has no positive essential lower bound.

## Weak topology proof checks

TV convergence implies weak convergence since the bounded-test integral error is at most 2 times the test's supremum norm times TV. Therefore weakly closed C is TV closed, in the direction used by the proof. Theorem 1 is applicable without presupposing compactness of P(X).

The Dirac map x to delta_x is weakly continuous, so F={x:delta_x is in C} is closed. For a probability on a second-countable space, the complement of its support is the union of the countably many basic open sets of measure zero. This proves support measurability and conullness, and makes support nonempty. This step is not silently transported to arbitrary measurable spaces.

If x is in the support of p, every radius-1/n open ball about x has positive p-mass. Its normalized restriction is an actual probability absolutely continuous with respect to p, hence is in C. For each bounded continuous h, continuity at x implies that the supremum of |h(y)-h(x)| on that ball tends to zero. Global uniform continuity and compactness are unnecessary. These restrictions converge weakly to delta_x, establishing support(p) contained in F and C contained in P(F).

For the reverse inclusion, a nonempty closed subspace F of a separable metric space has a countable dense sequence. Repetitions handle finite F. The disjointified balls are relative Borel cells, and the map choosing each cell's center is measurable because it has countable range and measurable fibres. A measure carried by F can be restricted to the Borel space F when taking this pushforward, then regarded again as a measure on X.

The countably supported pushforward is the TV limit of the displayed finite mixtures, with error at most the omitted tail mass. These finite mixtures lie in C. The subsequent pushforwards converge weakly to the original measure by pointwise convergence of the chosen centers and bounded convergence for each test. Both uses of weak closure are legitimate. No unproved compactness, Krein–Milman representation, or universal finite-support representation is needed.

The converse uses absolute continuity of posteriors and the nonnegative bounded continuous function min(1,d(x,F)). Its zero set is exactly F, and integral zero is equivalent to full mass on F. This proves weak closedness. Dirac membership identifies F uniquely. Minimality of P(support(p)) follows because any closed carrier of p contains support(p), while support(p) itself carries p. The stated Polish theorem is valid; the proof indeed uses only separable metric Borel hypotheses.

## Counterexamples and reciprocal boundary

For Lebesgue probability mu on [0,1], D(mu) is a proper TV-closed preserved face containing mu, which has full topological support. Every delta_x is excluded. Since every nonempty Borel carrier F contributes delta_x for x in F to P(F), this D(mu) cannot be a point-carrier class. The densities n times the indicator of [0,1/n] integrate to one, converge weakly to delta_0, and remain TV distance one from delta_0. The example tests exactly the topology distinction being claimed.

For G, products and reciprocals remain in G; direct normalization proves the composition and inverse identities. Universal forward G-preservation therefore gives equality for each G-map.

For a bounded everywhere positive L, an independent description of the full-simplex image is

    B_L(P) = {q in P : integral (1/L) dq is finite}.

Indeed an image q=B_L(p) satisfies that integral equal to 1/Z_L(p). Conversely, if its value is J<infinity, p=(1/(J L))q is a probability with posterior q. This directly verifies the author's example: for uniform q on (0,1] and L(x)=x, J is infinite. The failure is surjectivity and global availability of the inverse, not definedness of forward updating or preservation of P. The example does not contradict either classification.

## Ancestry and reuse check

The local comparisons were targeted. They support the author's reuse boundaries and do not establish an exhaustive repository search or priority claim.

- The concurrent finite packet's Section 2 establishes coordinate-face classification under every positive likelihood, together with same-support orbit transitivity. The measure packet transports that interface and explicitly drops finite ratio boundedness. This review does not certify the finite packet's separate affine, graph, or projection results.
- The preserved P02 U05 measure core, especially M2-01 through M2-05, already distinguishes singleton mass from topological support, countable from unrestricted mixtures, and weak from TV closure. Its shrinking-uniform example, full-measure support argument, and discrete approximations are correctly credited as inherited. The present arbitrary-measurable theorem avoids importing that source's measurable-singleton hypothesis where it is unnecessary.
- P03 U05 measure semantics Sections 1–6 retain the actual-measure and formalisation boundary. This packet supplies no missing kernel evidence for them.
- The moment packet Sections 1–5 and its addendum concern moment records, compact determinacy, one-sided exponential tilts, and future continuation. They do not state the universal feasible-class classifier. The moment state class and controls remain distinct from the full-simplex universal likelihood quantifier.
- The earlier archive's READ_FIRST and SOURCE_DEPENDENCIES were inspected only to check scope and provenance. Their transitive dependencies and entire archive were not recertified.

External sources were independently opened and checked. [Weis, Sections 4, 9 and 11](https://arxiv.org/html/2404.00832v2) supports the cited generated-face, absolute-continuity-face, bounded-ratio, and countable-simplex antecedents. Corollary 9.3 is explicitly labelled Dubins; the two-sided density description should not acquire a new authorship claim. Weis attributes the general generated-face formula to Alfsen. Neither original work was inspected here, so those credits remain secondary attribution. No earliest-priority claim is justified.

The [journal metadata](https://journalofconvexanalysis.com/articles/jca32046/) matches volume 32 (2025), issue 3, pages 901–919. [Van Gaans's author-hosted notes](https://pub.math.leidenuniv.nl/~gaansowvan/jancol1.pdf) contain the cited metric probability ingredients, including finite-discrete density in Proposition 4.4, and identify textbook antecedents. They are not cited as an exact source for the present weak-face theorem. The ordinary proof above, rather than that attribution, supports the theorem's precise formulation.

## Integrity and stopping boundary

INPUT_BINDINGS.json records the five author-packet files, including its manifest, and the seven directly named ancestry inputs. HASH_CHECK.json records exact byte-count and SHA-256 comparisons. A hash match establishes which bytes were reviewed; it does not establish mathematical truth, authorship priority, completeness of source discovery, or reproducible formal proof.

The useful result is the stated conditional classification and its topology and likelihood-class boundaries. Nothing in this review equates a normative prohibition with zero probability, establishes an actual evidence mechanism's available likelihoods, identifies a psychological realization, or supplies a theorem about noetic authority. No changes to the author or ancestor files were made. No correction cycle is required for the frozen statements reviewed here.
