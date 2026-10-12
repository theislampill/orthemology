# Independent review: face-stratified finite exponential geometry

10 October 2026 UTC. Separate ordinary mathematical AI review of the frozen `face-stratified-noetic-geometry-20261010` packet. The reviewer is distinct from its author and from the root contributor to its proof strategy. This report grants no formal-kernel certification, protected-source integration, implementation-failure finding, empirical or cognitive warrant, historical novelty, or programme closure.

## Verdict and binding

**No blocking mathematical or attribution defect found within the stated finite, strictly-positive-reference, unrestricted-parameter scope.** The closure theorem, entropy completion and homeomorphism, reduced Fisher/Legendre geometry, same-reference zero-likelihood equivalence, and closed-model local-evidence corollary are correct. The packet correctly distinguishes support faces from feasibility zero faces, completion from the actual posterior, and closure membership from finite local hard-evidence reachability.

The frozen author manifest SHA-256 is:

`1a55afdd82a820d8006a23a3133a53e35737e1cae91b528f657ac227b04618b5`

The reviewed `RESULT.md` has 32,177 bytes and SHA-256:

`41d1343f00006d5e97d6a0b09264cc1d99ee2dd23a13ba5caaf2169afce63fa4`

All 15 manifest-bound author files and all six direct original-input bindings were verified. The unchanged author replay ran from an isolated copy and passed **35 exact assertion groups**, regenerating the author's control JSON and complete stdout byte-for-byte. A separate reviewer program passed **20 exact assertion groups** using independent Fraction linear algebra, prime-factor representations of rational logarithms, and explicit symbolic rational-function limits. It imports no author code. These are bounded executable controls supplementing the proof review, not an additive measure of theorem strength.

All original author-directory files, including its two unbound pre-existing cache files, were hashed before and after review. No author byte changed. The review writes only its separate review/research directories.

## 1. Facial necessity: the limiting-log argument is sufficient

Let a full-support exponential sequence converge to p and write S=supp p. Its retained functions f_n=log(p_n/r) converge finitely on S and to negative infinity off S. Since r is strictly positive on a finite set and p_n<=1, all f_n coordinates have one common finite upper bound. This upper bound prevents any positive divergence from canceling the negative divergence.

Take any probability a supported on S, and any b with the same retained mean. Retained mass and statistics give E_a f_n=E_b f_n. The first side has a finite limit. If b assigns positive mass to even one atom outside S, the second side tends to negative infinity. Therefore every probability representation of every point of conv phi(S) is S-supported.

The step from this fibre property to a saturated face can be reconstructed directly without importing an unverified inherited conclusion. Set F=conv phi(S). If t u+(1-t)v lies in F with u,v in P and 0<t<1, choose probability representations a,b for u,v. Their mixture represents a point in F, so has no mass outside S. Nonnegativity implies both a and b are S-supported; hence u,v belong to F. Thus F is a face. If phi(x) lies in F, the point mass at x is another representation of a point in F, so x must belong to S. This gives saturation, including every duplicate and nonvertex supplied column.

The restriction V|S is a closed finite-dimensional linear subspace. The finite limit of f_n|S therefore remains in it. This proves the required restricted affine-log form. There is no hidden bounded-parameter assumption, no invalid exchange of infinite sums, and no need to choose a convergent natural-parameter subsequence.

Conversely, a finite exposing normal exists for every polytope face. An affine face log density extends to the ambient affine span. Adding t times the exposing normal suppresses exactly the off-face atoms and leaves the requested normalized relative family on the face. The full face P uses the zero normal. Distinct saturated supports identify distinct faces, giving a disjoint union. Reapplying the same finite theorem on a face proves the claimed incidence relation.

The statement is limited to finite X, r_x>0, and all finite canonical parameters. Dropping any of these hypotheses calls for a different closure theorem.

## 2. Entropy completion, support, and continuity

For a feasible mean z in the relative interior of its minimal face F, every representing probability is supported on S_F. An exposing normal proves this: any mass off its maximizing set would lower the expectation strictly.

A representation positive at every atom of S_F really does exist, even with repeated/nonvertex columns. Take the uniform barycentre b of all S_F columns. Since z is relatively interior, y=z+epsilon(z-b) stays in F for sufficiently small positive epsilon. Expressing z as a positive mixture of b and y yields such a representation. The case z=b, including zero-dimensional F, uses b directly.

The continuous strictly convex relative-entropy functional has a unique minimizer on the nonempty compact fibre. If the minimizer has an avoidable zero, mixing it with the strictly positive feasible law produces a t log t term with strictly positive coefficient. All originally positive-coordinate changes are O(t). Hence the objective decreases for small t, which is a contradiction. This is the necessary boundary-positivity argument; strict convexity alone would not establish full minimal-face support.

At this positive minimizer, both signs of every kernel perturbation are feasible for sufficiently small magnitude. First-order optimality and row/kernel duality put log(q/r) in V|S_F. It is therefore a finite relative-parameter family member, and the closure theorem applies. The entropy Pythagorean identity holds for every law in the same fibre because all such laws are supported where q is positive.

One elementary point implicit in the uniqueness argument is worth making explicit: any law positive on every supplied column of a face G has mean in relint G. Otherwise a proper supporting face containing its mean would force all its positive mass into that proper face, a contradiction. Consequently an arbitrary closure member with mean z must have G=F(z). The entropy identity then gives uniqueness across the entire closure, not only within a preselected stratum.

The compact-to-Hausdorff argument is sound and noncircular: existence and uniqueness are proved first; then the continuous mean map from the compact simplex closure onto P is a bijection and therefore a homeomorphism. This establishes continuity across faces without assuming continuity of an entropy argmin under changing constraints.

The global convex conjugate formula also checks. KL nonnegativity gives one inequality. Along an exposing ray, the common normal contribution cancels against the face mean and gives the entropy value in the limit. A proper-face value cannot be attained at finite ambient parameter, because equality would require a full-support law to equal a proper-face law. Normalizing r adds only a constant to entropy. The independent controls verify this identity at a nonzero boundary tilt with duplicate and nonvertex atoms.

## 3. Relative geometry and the limits of smoothness

Affine coordinates on aff F remove exactly the directions whose statistics are constant on F. Their evaluations, together with mass, form a basis of V|S_F. With positive mass at every S_F atom, zero variance of a linear coordinate combination means that combination is constant on F; minimality then makes the coefficient zero. The reduced covariance is therefore positive definite in positive-dimensional strata. The zero-dimensional case has only its zero tangent space and no invented positive-dimensional metric.

Differentiating the face exponential family gives dq=q(psi-E psi)·deta. Direct Fisher pairing produces covariance in natural coordinates and inverse covariance in mean coordinates. The inherited interior coercivity and inverse-function argument applies after this reduction, establishing a finite relative parameter and the Legendre Hessian. The fine Fisher gradient of a retained objective is tangent to the face family, so the displayed gradient dynamics are the exact within-support dynamics.

In the ambient statistic space, the covariance kernel is D_F perpendicular and its image is D_F. Positivity of the relative covariance proves both assertions. Continuity of q_r(z) gives a continuous positive-semidefinite ambient covariance field. It does not give a continuous finite inverse in disappearing normal directions. The edge example's coefficient 1/(1-z_x^2) diverges as asserted.

The conclusion is stratum-wise geometry. It supplies no nonsingular global Fisher metric, automatic stratum crossing, global dynamical uniqueness, or unrestricted global-time ODE result. It also need not be read as denying every possible topological smoothing or manifold-with-corners description of a polytope; those are different claims. No correction to the frozen wording is required.

## 4. Zero-likelihood equivalence and zero-domain intersections

For a nonzero nonnegative L and any finite full-support prior, the posterior has support exactly S=supp L and positive branch mass. Subtracting its prior affine log density from the posterior affine log density shows that the posterior can lie in the fixed-r closure precisely when S is saturated facial and log L|S is retained. This argument has no parameter-dependent remainder. Thus membership at one finite parameter is equivalent to membership at every finite parameter.

To extend preservation to a boundary prior on S_G, intersect supports. Under the global criterion, S_F intersect S_G equals S_(F intersect G). On a positive branch this is a nonempty saturated face support; restricted prior log density and restricted log L are both affine there. The closure criterion applies again. Conversely, preservation of the whole closure includes preservation from any full-support member. All four stated clauses are equivalent.

For a criterion from an already specified boundary face, only T=S_G intersect supp L matters. A globally nonfacial likelihood may still give a valid facial posterior from that particular boundary prior. The independent triangle control demonstrates this explicitly. Conversely, splitting two duplicate atoms can fail even when the resulting mean remains a vertex. The review also checks an empty support intersection: the branch has zero mass, normalization raises an explicit error, and no empty-face probability is introduced.

The local-evidence corollary is valid. Retaining every function on scope D retains both the support indicator and a finite extension of log ell from the positive cells. The indicator exposes the exact support face; the log extension supplies the second condition. This includes constant likelihoods and full support. Induction proves finite sequences of positive branches remain in the same closed fixed-reference model. A nonproduct reference does not alter this reasoning.

The all-prior common-core theorem has different quantifiers. Arbitrary joint laws sharing the same retained mean need not share a reference class, so even unary hard evidence can produce different retained posteriors. The packet's explicit comparison and the independent correlated-square test preserve this distinction. Exact model-based reconstruction is not an efficiency theorem or a universal marginal-only update formula.

## 5. Completion, actual support, and no free compression

The diagonal square controls are correct: each conditional law has mean zero in the global interior, rank-one actual covariance, and nonfacial support. The unique uniform-reference entropy completion at zero is the uniform product law with identity covariance. Replacing one by the other changes the law and metric.

The independent review adds a stricter diagnostic guard: the uniform law on three of the four square vertices has mean (-1/3,-1/3), which is interior, and positive-definite covariance with determinant 16/27. Nevertheless it fails the product closure identity. The product law with the same mean has weights (4,2,2,1)/9. Thus full-rank covariance, as well as a globally interior mean, cannot certify membership in the chosen closed model.

Facial support is not sufficient either: the packet's cube face likelihood produces a yz odds ratio of nine rather than one. Duplicate and nonvertex examples similarly show that a face's vertex hull does not replace its full supplied-atom support, and agreeing at duplicate columns alone does not force the remaining log values to be affine.

For arbitrary L, rL on its nonempty support is a valid positive reference for a conditional-support family. Removing affine redundancies there is legitimate even if the support is not a global face. If the old and new same-support reference classes had a common law, subtraction of their affine log densities would put log L in V restricted to that support. This verifies the claimed disjointness when that condition fails. If support is nonfacial, closure membership is already impossible.

A declared support and reference class plus the relative mean determine the selected conditional-family member. The mean alone does not establish either the support or residual log-density class. This is a conditional model representation, not free compression of arbitrary unknown laws or authentication of the likelihood.

## 6. Pairwise facet: regular relative geometry versus hard reachability

The six non-all-equal cube atoms form the retained pairwise facet. Its augmented columns have rank six, so its relative affine dimension is five and its restricted family contains every positive law on those six atoms. The displayed relation xy+xz+yz=-1 removes one genuine global affine redundancy. The reduced covariance blocks and eigenvalues are correct. An independent Fraction computation gives positive leading principal minors

1, 8/9, 16/27, 128/243, 256/729,

while the full six-statistic covariance kills exactly the lost normal (0,0,0,1,1,1).

The finite-hard-factor obstruction does not follow merely from low-order terminology; it follows from full support projection. Each pair assignment appears in the six target atoms. Any nonnegative pair-local factor in a finite product that is positive on all six must therefore be positive on every pair assignment. Every factor is then positive on all eight atoms, so their product cannot have exactly the desired six-atom support. The independent checks record an explicit witness atom for each of the twelve pair assignments. This is a support argument, not massive enumeration.

The equal-rate soft-factor path has positive branch probability at every finite time, tends to zero branch probability, and has the claimed normalized six-atom limit. The hard limit demands three simultaneous pairwise anti-alignments and has no atom. The normalized limit is not conditioning on that impossible event. The nonlocal indicator of the six-atom set does condition directly with probability 3/4.

The review adds a path-dependence check within probability-valued local factors. Let the equality weights on the three pairs be c_i s and the inequality weights one, with 0<s<=1/3. For c=(1,1,1), the limit is uniform on six atoms. For c=(1,2,3), the limit in lexicographic cube order is

(0, 1/12, 1/6, 1/4, 1/4, 1/6, 1/12, 0).

Both product likelihoods tend pointwise to the same identically-zero hard product, and both branch probabilities tend to zero. Their distinct normalized limits reinforce the packet's refusal to infer a unique conditional on the impossible limit.

## 7. Source reading and inherited credit

Primary-source checking used the existing local acquired PDFs and extracted texts, with their hashes independently verified against the author's notes. This was **fresh reading of local source content, not a fresh web retrieval**. No claim is made to have checked ResearchGate uploader metadata, current URL availability, or the full cited papers. The separate source receipt states exact page boundaries.

- Csiszár–Matúš, *Information Projections Revisited* (2003), PDF pp. 4–6 and 11–12, printed pp. 1477–1479 and 1484–1485: the reviewed passages define face components, give the unique moment-fibre intersection and Pythagorean characterization, and explicitly equate the finite extension with ordinary Euclidean closure. The inverse-image restriction includes duplicate statistic values, supporting saturation. Formula pages 5, 6, 11, and 12 were visually inspected; page 12 was additionally rendered independently from the verified PDF.
- Csiszár–Matúš, *Closures of exponential families* (2005), reprint pp. 1, 3, 5–6, 10–11, and 13: the broader closure theorem uses accessible faces and projected canonical domains. With finite support and unrestricted parameters, it specializes as stated. Theorem 2 on p. 10 was also freshly rendered and visually inspected. The source itself identifies the electronic reprint's pagination difference.
- Wainwright–Jordan, PDF pp. 70–71 and 73–74, printed pp. 63–64 and 66–67: inspected extracted text supports minimal interior parametrization and entropy duality/boundary dual limits. This review does not credit these loci with the exact facial-union theorem. No full-paper reading or additional appendix verification is claimed.
- Barndorff-Nielsen is an indirect historical pointer only. The book was not read here and receives no direct-reading credit.

The cited sources support classical finite exponential-family geometry. They do not support a historical novelty claim or the packet's external cognitive interpretation; the packet does not claim either.

The direct inherited passages also support the author's stated boundaries. The leafwise input §§6–10 already supplies the positive full-support geometry and positive-likelihood criterion, explicitly excluding support changes. Event-feasibility §§2–6 supplies the saturated zero-set face lemma and the pairwise global-facet/local-positivity obstruction. The inherited event review was inspected as provenance, not borrowed as review of this extension. Hierarchical §§1–4 supplies the all-prior common-core comparison. Source-audit opening and §§2–4, 8 distinguishes supported conditioning, inverse-factor loss, and null-event revision. No transitive verifier replay or fresh review of the entirety of those packets is claimed.

## 8. Reproduction and precise limits

`author-replay/REPLAY_RECEIPT.json` records the isolated exact author replay. `INDEPENDENT_RESULTS.json` and `independent-verification.txt` record the separate 20-group run. `PRESERVATION_RECEIPT.json` binds unchanged original bytes; `SOURCE_CHECK_RECEIPT.json` binds the inspected local source versions and reading scope. `MANIFEST.json` binds all compact review files except itself and its detached seal.

To verify and replay the compact review without modifying it:

    python3 replay_review.py private-locator:2766b44f9e596a08fcda

The output directory must not already exist and must be outside the review packet. This checks review integrity, replays the copied author verifier in a new copied tree, and replays the independent checks in another copied directory. Optional `--verify-original-inputs WORKSPACE` additionally verifies the six direct original bindings. Source re-reading, transitive inherited replays, and mathematical reasoning are not automated by that command.

The universal claims have ordinary finite proofs; the executable examples are not kernel certificates. No numerical face-finding tolerance, approximate-data robustness, statistical estimation guarantee, general reconstruction complexity bound, globally smooth change-of-support metric, semantic authentication, or actual implementation allegation has been established. No author correction is requested, and no author/protected file was changed.
