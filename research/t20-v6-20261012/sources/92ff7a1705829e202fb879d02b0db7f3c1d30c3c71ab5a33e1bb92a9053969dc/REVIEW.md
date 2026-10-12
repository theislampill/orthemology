# Adversarial review of two post-delivery T20 deductions

11 October 2026 UTC. Ordinary mathematical and source-scope review. Delivered T20 v2 and inherited owners remain inputs. No protected edit, external upload, formal-kernel claim, empirical validation, repository adoption, or programme closure is made.

## Verdict

PASS within the exact stated contracts, for the frozen reports identified below. No blocking mathematical defect found. The multi-partition gradient theorem and restricted-control continuation theorem have valid proofs. Their applications retain the structures actually needed to transport those proofs.

One nonblocking precision correction was requested and applied: the restricted-control lower-bound proof now says that the mass row lies in row(A), since 1ᵀA=1ᵀ. It was previously called a literal row of A. The corrected wording makes the tangent-kernel argument precise; the result and proof mechanism are unchanged. The exact difference and pre-correction report are retained separately.

Contribution scope matters: the cone common-refinement statement is a direct application of ET-23 via one tagged mixture instrument, not an additional general cone-rigidity theorem. This reviewer supplied that shorter proof before the audit author froze the report. The report now labels it Corollary C and credits the contribution. Accordingly, this review is not independent external corroboration of that particular proof. The original extreme-point and successive-conditioning proofs were reviewed independently and are also correct. The gradient and restricted-control proofs were not authored by this reviewer.

## Frozen targets

- audit_symmetries/RESULT.md: `123edeea72714cc9e1e7d4c830730e1fbee1c20aa8473219cfb56b10393d42c8`
- audit_symmetries/check_exact.py: `779a4d9ab9b50cf17d9ec49536023ef3db7e64b5d4c48fe9e3bef7af846edffd`
- audit_symmetries/SOURCE_BINDINGS.json: `dfc082cd0806b4b53482df56de45995bafc2173e9979788394b8aaa3db64020a`
- restricted_controls/RESULT.md: `cd25322628a1ec4997248286e8f05987ee1ed646ad97a59651e35f9960b1fd49`
- restricted_controls/verify.py: `d9430c2638404329fbc1709d872043804b3b6f6a36fc9e8a1eb9d8e86ca85574`

Paths above are relative to the enclosing reassessment directory. Byte-identical targets are retained in `author_snapshots/`; `REVIEW_TARGETS.json` gives full workspace-relative paths and sizes. Source bindings record what was actually read, distinguishing scope inspection from mere hash checking. The review does not silently convert an author’s recorded source inspection into its own.

## 1. Multi-partition gradient classification

The inherited fixed-partition theorem is the correct starting point. Its proof uses the actual metric decomposition into Fisher group masses and mass-weighted within-group metrics. The current inference is stronger than its action-generation guard, but does not contradict it.

For each partition, its inherited energy decomposition yields an additive decomposition of the canonical extension F(q,x)=S E(q/S,x), S=Σq. The extension is C² because normalization is smooth on the positive orthant and E is C² on the simplex manifold. It is positively one-homogeneous in the independent q variables. The constant C_l is legitimately absorbed into every block potential because block masses sum to one.

Lemma A1 correctly intersects additive decompositions. If two labels are separated by at least one partition, the differential in one label’s complete coordinates is independent of the other’s coordinates. The full product domain allows one outside factor to be changed at a time. The anchored restriction to a refinement cell is C² and has exactly the appropriate cell differential. The residual has zero differential on a connected domain and is therefore one constant. Non-simply-connected factors cause no problem; full product and connected factors are the relevant assumptions.

Lemma A2 repairs constants without losing a derivative. From F=c+Σf_A, Euler’s equation gives Σ(L_A f_A−f_A)=c. Independence of cell variables forces each bracket to be a constant k_A, with Σk_A=c. H_A=f_A+k_A retains C² and satisfies L_AH_A=H_A. Radial differentiation on the entire positive q_A orthant then gives the required homogeneity. Defining H_A directly as an Euler derivative would need an additional regularity argument; the report avoids that trap.

Restricting H_A to Q_A=1 produces the stated C² V_A on the positive conditional simplex and full within-cell position product. All three implications follow. One-block partitions impose no condition; repeated or nested partitions behave as expected; zero-dimensional position factors and singleton conditional simplexes are harmless. No boundary extension is needed or proved.

C² energy and the smooth positive metric give a C¹ field. Audit maps are diffeomorphisms of the full specified domain and have inverse audits. ODE uniqueness therefore establishes local-flow commutation and equality of maximal existence intervals. This proves no all-time completeness statement.

### Load-bearing guards

Connectedness and product structure cannot be dropped casually. For example, with disconnected position factors X₁=X₂=R\{0}, an energy that is one on equal-sign components and zero on unequal-sign components is smooth with zero gradient, hence audit-equivariant. It cannot globally equal w₁V₁(x₁)+w₂V₂(x₂)+C for all independent weights and sign choices. The report retains the assumptions excluding this example.

The metric is also indispensable. In Euclidean log-odds coordinates, E=θ²/2 has gradient θ(1,−1,−1), which is invariant under row/column translations while depending nontrivially on θ. This differs from the retained Fisher/transport metric. Thus the theorem is not a metric-free consequence of the audit group.

## 2. Generated actions versus gradient rigidity

The 2×2 row/column action group has a two-dimensional translation plane in three log-odds coordinates. Its invariant θ=u₁−u₂−u₃ is exact. The singleton multiplier (2,1,1,1) changes θ, so the generated subgroup is strictly smaller than all singleton audits.

Proposition B correctly classifies invariant C¹ coefficients as functions of (θ,x). Its smooth global section establishes factorization; the replicator formula correctly includes the common-fitness gauge. The explicit θ-dependent field has the stated all-time log-odds solution and fails singleton covariance.

The nongradient diagnosis is independently verified: the Fisher covector would have intrinsic components (−θ/α,0,0), whose mixed derivatives disagree. For the distinct energy E=ρ, scalar invariance does not yield metric-gradient covariance. The exact row-audit residual is (1/3,−1/3,1/3,−1/3) at the displayed point. The row-only interaction also fails the column test, while interaction inside a genuine common-refinement cell survives. These examples support the claimed boundary rather than erasing the group-action obstruction.

## 3. Cone stability and actual geometry transport

ET-23 supplies the exact finite proper-cone hypotheses, canonical indecomposable summands, dominated branch scalars, compact normalized base, and fixed-instrument stable-family theorem. They were checked at the bound owner bytes. Full outcome-column equality, not equality of one chosen outcome, is the required partition.

A positive tagged mixture S_(l,y)=β_l T_(l,y), with positive β summing to one, is a complete instrument. Its equal-column partition is exactly the common refinement, and its normalized positive branches equal the original branches. This proves Corollary C directly from the inherited theorem. It is a mathematical reduction; it does not assert physical availability of a tagged experiment.

The alternative extreme-point proof is valid because C is nonempty, closed and convex inside compact B. A stable extreme point must be supported in a block of every partition, hence a nonempty refinement cell. The conditional-mixture proof correctly handles empty intersections C∩B_H. The successive-conditioning proof also correctly observes that positive final-cell mass forces positive mass at every prefix. Strict positivity of u ensures that zero positive branch mass means zero vector, so no posterior is assigned there.

The proposed least stable hull contains z, is a finite compact convex hull, and is stable because branches rescale its conditional vertices. It is a hull statement, not finite-history reachability. In the positive orthant, positive branch words preserve support and odds ratio, while convexification need not preserve odds ratio and closure admits boundary vertices. In nonsimplicial summands, the internal conditionals remain retained and the hull need not be the whole base. Closedness is essential: the open simplex is convex and stable under strictly positive branches but omits the asserted pure conditionals.

Section 6 performs an actual structure-preserving construction. The coordinates z↔(w_a,x_a) are smooth and global on the normalized relative interior; their inverse uses positive component masses. Affine coordinates on each relative-interior base yield connected open Euclidean domains, including zero-dimensional points. The metric is explicitly additional data transported through this map, not inferred from cone order. Every positive grouped multiplier can be realized as one branch of some binary identity-summing positive instrument using sufficiently small ε. This does not turn one previously fixed finite instrument into the full continuous audit family. Order isomorphisms must transport the metric too. These distinctions are all retained.

## 4. Restricted controls and full-output equivalence

The dynamics are exactly MOM-01’s Fisher replicator dynamics on fixed simplex-valued support. Grouping by equality of the restricted fitness functional is correct. Within each group the same exponential factor multiplies every term; both its mass and unnormalized full-output barycentre are therefore sufficient. The record is BΔ_N°, not an unconstrained product of barycentres.

For a generic v in U, finitely many proper signature-difference kernels cannot cover U. Distinct signature values λ_a therefore exist whenever s>1. Equality of full q(t) supplies equality of v·q(t), which is −d log Z/dt. The initial normalization Z(0)=1 fixes the multiplicative constant. Equality of q then identifies each barycentre coefficient through independence of finite exponentials, equivalently a Vandermonde system of right derivatives at zero. This proves exact history equivalence, not finite-sample recoverability or numerical stability.

The full-output clause is necessary. A scalar v·q history identifies group masses, but can miss within-group output barycentres. The report’s six-state q-only pair even has the same signature masses, so its x-control scalar responses agree while its y output after the same tilt differs. Independent controls verify this stronger counterexample. The theorem correctly refrains from importing MOM-01’s scalar-response conclusion unchanged.

For s=1, all fitnesses are common, the dynamics vanish, B=A, and equality means equality of the full constant output. This covers U={0} and pure mass-gauge controls. Adding a common scalar to all fitnesses changes neither grouping nor dynamics. A one-dimensional nongauge control can distinguish all support points, so control-space dimension alone is not a memory bound. Duplicate original support columns may still represent distinct fine states; the quotient concerns the stated output/operation interface only.

The closed barycentre ODE follows by direct summation and preserves its admissible image through the positive exponential solution. No full-state recovery follows when B is noninjective. The six-state h pair explicitly preserves every permitted output while remaining different laws.

## 5. Continuous augmentation and composed controls

Since A factors through B, rank subtraction on ker A is valid. The corrected mass-row statement makes every vector in ker A a simplex tangent. Independent B-images of k such vectors give a small open k-box inside a fixed-q positive fibre. Any sufficient continuous sidecar must inject that box into its own real-coordinate space. Invariance of domain rules out fewer than k coordinates even if the decoder is discontinuous or nonlinear. A linear basis extension attains k=rank(B)−rank(A), so the continuous and smooth minima agree. The k=0 case is immediate.

This is a full-law, exact, continuous-coordinate statement. A finite or countable-valued sidecar cannot distinguish an uncountable fixed-q box when k>0; a pathological exact real encoding is excluded by continuity. None of these facts is a bit complexity, approximate storage, noise, sample, or acquisition bound. ET-09’s finite sidecar theorem remains a different result.

For several permitted subspaces, arbitrary finite concatenations realize every integrated parameter in their sum. Equality of all allowed histories therefore supplies all endpoint q(u), including u=tv for a generic v in the sum even when that v is not one allowed instantaneous control. This justifies the new §6 necessity argument. Amplitude, ordering, menu, or duration restrictions would need a new reachable-set argument, as the report states.

The nine-point composition example is exact. Both isolated barycentre records annihilate h=(1,−2,1)⊗(1,−2,1)/100; their stacked rank is eight. Composed x/y signatures distinguish all nine columns. Literal successive half-power tilts separate the full outputs by

    (−56700,−56700,113400)/24009919.

The two x/y components agree by symmetry and their total mass difference is zero. This is a valid current-law Fisher-control realization of the already inherited missing-interaction mechanism. ET-05 already has complete isolated source-revision profiles that fail to compose, and the report gives it explicit credit.

## 6. Source ownership and depth assessment

The exact grouped owner explicitly left multi-partition gradients unclassified while proving the row/column action-generation obstruction. Theorem A fills that bounded gap under the original metric and domain. Its cone-gradient application is conditional on added geometric data and a continuous audit quantifier. Corollary C itself is a direct ET-23 reuse.

MOM-01 already supplies the exponential solution, generic-control argument, and rich-control qualification. H-Continuation already supplies observable closure and the continuous augmentation lower bound. The present restricted-control theorem computes the exact intermediate quotient: retain every output-coordinate function restricted to each fitness-signature group. Equivalently, row(B) is the smallest row space containing row(A) and invariant under the diagonal fitness operators. A separating fitness and its interpolation polynomials generate the group indicators. This explains why the construction is a specialization of established observable-span machinery rather than a new general observability theorem.

GEO-06’s mean/leaf coordinates reconstruct the entire positive law; the smaller B record is sufficient for a restricted output contract and does not preserve every leaf invariant or every future source operation. Its adjacent stabilizer-block theorem concerns which objectives descend on a fixed observed space, a related but distinct quantifier. ET-09 counts finite labels per retained fibre, while the present theorem counts continuous real coordinates. These comparisons preserve the actual source structures rather than equating results by title or vocabulary.

The scoped deductions provide concrete additional mathematical synthesis. They do not establish exhaustive intellectual exploration, field novelty, source authentication, normative permission, noetic realization, or truth. No broad literature campaign was performed or inferred.

## 7. Executed evidence and preservation

Fresh independent controls in `check_independent.py` passed normally and under Python optimization: 62 named checks, including exact symbolic/rational controls and one exhaustive five-label partition-support calculation. Normal and optimized outputs are byte-identical. Large internal finite-case counts do not prove the C² theorem.

The frozen audit author suite reproduced 14 control groups / 3054 counted checks and fixtures in both modes. Of these, 2959 are finite partition-pair support cases. The frozen restricted author suite reproduced 31 exact controls in both modes. The mathematical universal quantifiers are established by the reviewed proofs, not those counts.

Author files were copied before replay. The audit checker’s read-only fixture ROOT variable was rebound to the workspace because the snapshot is nested more deeply; its source code was not changed. HERE and every generated author-result write remain inside the review snapshot. The restricted checker was executed directly from its byte-identical snapshot. This relocation is documented in `replay_authors.py`.

`SOURCE_BINDINGS.json` records 17 matching inherited files and exact reading scopes. `FINAL_CURRENTNESS.json` checks the final report/checker/bindings against their snapshots and verifies those inherited file hashes again. `MANIFEST.json` binds the review artifacts. The review authored files only in its own directory and made no changes to delivered v2 or inherited source files. No broader repository integrity claim is inferred from these bounded hash checks.
