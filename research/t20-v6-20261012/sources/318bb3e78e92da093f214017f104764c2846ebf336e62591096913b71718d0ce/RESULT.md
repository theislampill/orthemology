# Independent review: positive instruments and finite cone transport

10 October 2026 UTC. Ordinary independent AI mathematical and semantic review. This is not a formal audit-assess result, Lean/kernel certificate, empirical validation, integration decision, or programme-closure receipt. The reviewer did not coauthor the candidate theorems. The candidate itself correctly identifies the root and author worker as joint authors.

## Verdict

**No blocking mathematical or semantic defect found in the frozen packet.** The proper-cone identity-interval theorem, canonical decomposition proof, identity-summing instrument classification, fixed-instrument stable-family transport, and displayed failure of unrestricted passive transport are supported by the written arguments.

All **16 author control groups reproduced exactly** in a separate snapshot. All **7 independently reconstructed exact control groups passed**. All **17 frozen author files** matched their recorded hashes, and the **9 inherited source inputs** matched their author-bound snapshots at review time. Finite checks corroborate the examples; the universal conclusions rest on the proofs.

Two minor precision changes were requested before freezing and verified afterward:

1. The compact-convex proof now explicitly chooses external approximants in aff(Q), keeps the limiting supporting vector in its direction space, and explains why the supporting face is proper.
2. The Barnum–Wilce links now specify arXiv v1, matching the verified Theorem 1 numbering.

Neither change alters a theorem or its hypotheses. No further correction is required for the reviewed claims.

## Exact review target

Author packet: `positive-instrument-cone-transport-20261010`.

- Frozen `RESULT.md` SHA-256: `5c74c7086c038dce1be0e9098b42fce9cc4c7aee8670fe0ba682b50d780af5c0`
- Frozen author `MANIFEST.json` SHA-256: `76724a4e3c578f7b61fe9892cd289d7b61ca87b77b3b26904af97833cb9ae35d`
- Author confirmed both final changes, no pending edits, and a freeze before the reviewer copied the packet.

`INPUT_BINDINGS.json` records every copied file, the isolated replay, and source-currentness checks. `author_snapshot/` retains the exact reviewed packet. The author verifier ran only inside that snapshot, so its result write did not modify the author directory. The replay reproduced the existing result bytes.

The full result and verifier were read. The inherited comparison was checked against the fixed-channel theorem and its convex-geometric proof, the fixed-prior splitting and feasible-mass example, the affine diagonal-preservation passages, H-Continuation's action–observation/Theorem 2 section, and the audit-continuation report's positive-cone/intertwining/normalization sections. This review does not claim a fresh exhaustive scan of the surrounding programme.

## 1. Proper cones and the geometric lemma

The definition retains every load-bearing hypothesis: nonzero finite-dimensional real space; nonzero closed convex cone; pointedness; and generation of the declared ambient space. Positivity is relative to that cone.

The construction of a strictly positive functional is correct. Pointedness excludes zero from the convex hull of the unit section. Compactness of that convex hull follows by finite-dimensional affine-dependence reduction. The nearest-point inequality gives a uniform positive lower bound on the unit section, hence boundedness of the normalized base. Closedness then gives compactness.

The revised induction for compact-convex extreme-point generation is complete. Working inside the affine hull is essential: otherwise a support vector perpendicular to the entire affine hull could expose the whole set. The revision excludes that possibility. Extreme points of the proper exposed face are extreme in the original set, and interior points are mixtures of endpoints of a compact line section. This gives finite convex combinations, without requiring a finite set of extreme points.

Normalization correctly identifies base extreme points with extreme rays. Generation of V then provides a vector-space basis selected from extreme rays. The packet explicitly avoids the false inference that this selected basis generates the whole cone as a positive hull.

The report appropriately distinguishes closedness as its sufficient extreme-generation hypothesis from the narrower algebraic assumptions needed later. The strict-quadrant countercontrol shows why simply deleting closedness is not justified.

## 2. Identity interval, indecomposability, and canonical summands

For an extreme ray vector r, the decomposition r = Tr + (I−T)r forces both terms onto its ray. This uses domination by identity, not positivity of T alone. Its coefficient lies in [0,1].

Selecting an extreme-ray basis therefore diagonalizes every dominated map over the reals. Partitioning extreme rays by its distinct eigenvalues yields a direct cone decomposition because every cone element is a finite conical sum of such rays. Every eigenspace that appears contains a basis ray, so the corresponding cone summand is nonzero. Conversely, a nontrivial direct cone decomposition supplies a positive nonscalar projection dominated by identity. The equivalence with identity spanning an extreme ray of the positive-map cone follows directly from I = A + B. No self-duality or complete positivity is hidden in this argument.

The canonical graph proof is sound, including signed coordinates. Each extreme ray's nonzero coordinates belong to one connected component by definition. Coordinate projection therefore sends each extreme ray either to itself or to zero; extreme generation extends positivity to all K. Each resulting K_a is a proper cone in its own coordinate subspace.

Comparing the coefficients of Tr = t_r r forces equal diagonal values across every support edge, hence across each component. Conversely componentwise scalars in [0,1] give dominated maps. Applying this classification to idempotent summand projections forces their coefficients to be zero or one. Thus every other direct decomposition groups whole canonical components. This establishes indecomposability and uniqueness without assuming either in advance.

The wider classification of positive maps fixing every extreme ray individually is also correct, with nonnegative component scalars and no upper bound. The qualification excluding ray permutations is important and retained.

An independent square-cone-plus-ray control checks both a genuinely nonsimplicial component and a separate component. Its ray-eigenvector constraint system has nullity two, exactly the two component scalars. This supplements, rather than substitutes for, the graph proof.

## 3. Instruments and normalization

For a finite positive instrument summing to I, each branch is dominated by I because its complement is the sum of the other positive branches. Componentwise classification then gives a stochastic coefficient column for each canonical summand.

The component-mass formulas are correct. Strict positivity of u ensures zero component mass means zero component vector. Branch probabilities are nonnegative scalar sums, and their sum is one for a normalized input. A zero branch probability forces the whole positive branch vector to vanish; no normalized conditional state exists there.

On an indecomposable cone, each branch is c_y I. Hence an outcome likelihood is independent of which normalized input state was supplied, and every positive branch leaves that input state unchanged after normalization. An external prior over a parameter selecting those input states is consequently unchanged. This statement is correctly restricted to the represented input-state family.

On a decomposable cone, an outcome reweights only the uniquely defined summand masses. It retains the normalized state within every surviving summand. The packet correctly distinguishes that statement from the false assertion that a conditional mixed state must equal its prior. It also distinguishes identity of the average channel on the whole declared domain from trace preservation, one-state preservation, and preservation of selected observables.

Positivity is used as a mathematical operation class. Physical availability, ancillary-system behavior, and source warrant are not supplied by it.

## 4. Fixed-instrument stable families

Theorem 5's four-way equivalence is valid for nonempty closed convex C in the compact normalized base. The essential quantifiers are one fixed complete instrument and every defined outcome at every x in C.

At an extreme x, the identity-summing barycenter decomposition forces every defined conditional state to equal x. Zero-probability branches contribute zero vectors. Projection onto any occupied canonical summand then shows that all occupied summands have the same entire outcome column. Thus x lies in one equal-column group.

Compact-convex generation gives the convex-hull characterization. Uniqueness of the vector-space block decomposition then gives group conditioning, and the grouped Bayes formula proves the converse. This argument allows C to have smaller affine dimension and allows some group intersections to be empty.

The claimed smallest stable closed convex family is the finite convex hull of the nonzero group-conditionals of x. These points lie in independent subspaces, so their mixture weights are unique. If every coefficient of a particular outcome is positive, reciprocal group reweighting supplies an inverse inside C. The report correctly does not call those reciprocal weights physically available signals.

Quantification over all mathematically allowed identity-summing instruments is handled by a binary instrument with distinct summand columns. The resulting class consists of convex hulls of arbitrary closed convex within-summand families. Indecomposability makes all defined updates identity, so every such C is stable. The orthant's stronger coordinate-face conclusion depends on its one-dimensional summands and cannot be exported verbatim.

The independent grouped-channel control checks 35 rational mixtures in a family with unequal constraints inside two identical-column groups, reciprocal inversion, and a cross-group extreme singleton that fails stability. The proof, not this finite sample, establishes the general claim.

The stable hull is properly separated from finite-history reachability, actual repetition, and perfect disclosure. No fresh-source or stopping assumption has been smuggled into the geometric argument.

## 5. Feasible-cone versus ambient passive transport

The three-state discriminator is exact. In the two-dimensional span of K_C = {(a+b,a,b): a,b ≥ 0}, the two displayed projections are positive, complementary, and sum to identity. Their normalized outputs are the two fixed-mass endpoints, with probabilities 2p_2 and 2p_3.

A fixed ambient diagonal map cannot equal the first projection on this span: its first diagonal entry would have to be both one and zero on the two generating rays. More generally, cone preservation by an ambient diagonal map forces equality of all three diagonal coefficients. This correctly reproduces the inherited affine-incidence restriction while demonstrating that the intrinsic positive-map class is larger.

At a single prior the displayed likelihood row (p_2/p_1, 1, 0), with its complement, realizes the same two raw branch vectors. Because p_1 = 1/2, it is a valid stochastic pair even at the endpoints. Its first entry varies with the prior, so this is not one fixed passive channel over C. Independent endpoint checks verify that a vanished branch remains undefined after normalization.

The semantic conclusion is warranted: an abstract summand coordinate does not automatically have the same meaning as an original target atom. Retaining only the feasible cone while replacing the operation class loses the original passive evidence contract. This is a failure of that proposed transport, not a contradiction of either theorem.

## 6. PSD and nonclosed controls

The qubit proof is valid for real-linear maps on Herm_2(C). If 0 ≤ T(P) ≤ P for a rank-one projector, positivity and the zero quadratic form on its orthogonal complement force T(P) to be a scalar multiple of P. Comparing the z and x decompositions of I makes their four coefficients equal; comparing y supplies the remaining basis direction. Thus T is scalar on the four-dimensional real Hermitian space.

The six-ray linear constraint system independently has rank 21 with 22 unknowns, so its nullspace is exactly the scalar solution. The domination hypothesis supplies the scalar bounds [0,1]; linear equations alone are not asserted to supply them.

The dephasing example preserves trace and fixes diagonal states but not every state. Its displayed residual (I−J_0)(P_x,+) has determinant −1/4, independently recomputed directly as a Hermitian matrix. Hence J_0 is not dominated by identity. The example does not evade the theorem through complete positivity; it simply lacks average identity on the full PSD cone.

The strict positive quadrant plus zero is convex, pointed, and generating, with no extreme rays. In dimension two a nontrivial direct-sum decomposition would provide two one-dimensional ray summands and hence extreme rays, which is impossible. Both nonscalar diagonal branches preserve this nonclosed cone. Its open normalized base exposes the missing compact extreme generation. The counterexample is correct.

## 7. Representation and semantic scope

Order-isomorphic transport is valid when the cone, mass functional, and admissible instruments all travel together. Conjugation preserves identity sums, branch probabilities, normalized positive states, and canonical summands.

The more general surjective compression claim explicitly assumes intertwining. F(K) = K′ then implies positivity of each descended branch; u′F = u gives probabilities and normalized images; surjectivity transfers the identity sum. No claim that every positive coarse map admits such a descent is made. An independent exact control supplies a quotient merging two fine states: unequal fine likelihoods cannot descend, while equal ones do descend and preserve the stated quantities.

The reset-channel comparison in §9 is correct. A convex decomposition at one chosen state gives positive preparation branches whose average resets all normalized inputs to that state. Their outcome weights are input-independent. Conditional output change therefore does not by itself establish information about the supplied input.

The discussion of finite adaptive selections retains the same cone and checks admitted identity-summing instruments at each node. It expressly excludes unmodeled state-dependent selection. No general-history, asymptotic, approximate-disturbance, tensor-composition, or information-geometry theorem follows merely from the established classification.

The packet makes no inference from cone indecomposability to psychological unity, noetic objects, metaphysical bearer simplicity, absence of intrinsic attributes, or a creator. It also preserves the distinction between numerical possibility and epistemic, normative, source, and permission warrant.

## 8. Independently checked primary ancestry

The primary sources were opened independently on 10 October 2026, and the cited numbering was checked at the following versions:

- Loewy and Schneider, *Indecomposable Cones*, LAA 11 (1975), pp. 235–245: Definition 3.1 and Lemma 3.2 are on pp. 237–238; Theorem 3.3 and its proof are on pp. 238–239. Under reproducingness and extreme generation, its equivalences include indecomposability and identity extremality. Theorem 2.3 supplies a broader extreme-generation result. This is an exact antecedent, not merely a thematic citation. [Primary PDF](https://people.math.wisc.edu/hans/loew_s75.pdf)
- Barnum and Wilce, *Information processing in convex operational theories*, arXiv:0908.2352v1: §2, p. 4 gives the finite ordered-state setup; §4, p. 6 labels the componentwise nondisturbing-map statement **Theorem 1**. Adjacent discussion and its footnote distinguish average nondisturbance from selective change of mixed states. The final candidate now links this actual version. [Version-specific primary PDF](https://arxiv.org/pdf/0908.2352v1)
- Heinosaari, Leppäjärvi and Plávala, *No-free-information principle in general probabilistic theories*, Quantum 3, 157 (2019): §5, Lemma 2 and Proposition 4 start on p. 10, Theorem 1 on p. 12, and Corollary 2 plus Remark 1 on p. 13. These support the extreme-point, direct-sum, and operation-class ancestry claimed. [Publisher PDF](https://quantum-journal.org/papers/q-2019-07-08-157/pdf/)
- D'Ariano, Perinotti and Tosini, *Information and disturbance in operational probabilistic theories*, Quantum 4, 363 (2020): the publisher abstract explicitly distinguishes local-state preservation from preservation of correlations and states the identity-atomicity connection. Only that abstract and bibliographic entry were used, matching the author's limited claim. No full-proof inspection is claimed. [Publisher record](https://quantum-journal.org/papers/q-2020-11-16-363/)

These sources justify the explicit rejection of field-level novelty. The review confirms the named antecedents; it does not establish exhaustive priority, exhaustively compare the literature, or import those papers' additional operational conclusions.

## 9. Verification artifacts and residual limits

- `author-replay.txt`: all 16 author control groups passed in `author_snapshot/`.
- `independent_checks.py`: independent rational arithmetic for seven additional control groups.
- `INDEPENDENT_CHECK_RESULTS.json` and `independent-verification.txt`: executed independent results.
- `INPUT_BINDINGS.json`: frozen author identities and inherited-source currentness at capture.
- `FINAL_CURRENTNESS.json`: final recheck of the frozen author and inherited inputs.
- `MANIFEST.json`: hashes of this review packet, excluding the manifest itself.

The verifier is not an arbitrary-cone decomposition algorithm. Graphs defined using all extreme rays need not be effectively enumerable from an arbitrary cone description. No untested algorithmic complexity or physical-realizability claim is validated.

The review's authority is limited to this ordinary AI proof and semantic assessment of the exact frozen mathematical packet. No author-directory edits were made by the reviewer, and no protected source, integration state, or closure status was changed.
