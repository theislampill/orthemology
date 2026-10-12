# Independent review of hierarchical marginal common-core closure

10 October 2026 UTC. Ordinary independent mathematical AI review of the frozen packet. The root and derivation worker jointly authored the target; this reviewer did not edit their result or checker. This is not a formal audit service, formal-kernel certificate, protected-source integration, field-wide novelty assessment, or T20/programme closure.

## Verdict

No blocking mathematical defect was found. The common-core stabilizer theorem, its full-prior probability-plus-posterior consequence, its normalized support-cylinder specialization, its global Fisher-objective consequence, and its least all-local-likelihood invariant enlargement are correct under the stated hypotheses.

The packet also states the necessary qualifications correctly: categorical alphabets are nontrivial; the face family is nonempty and downward closed; the prior domain is unrestricted rather than a graphical model; omitted coordinates remain latent; branch probability, posterior and feasibility are distinct outputs; and the enlargement is for every likelihood on the declared coordinate set, not an arbitrary single fixed channel.

The requested RESULT.md is 18,646 bytes and has SHA-256:

    a9b6bb1a955d0c90aea9b5b43a0f02889cc668ae0d23c35ba004bf906b33414d

All six manifest-listed target files and all five directly bound local input files match their declared identities. All 34 author assertion groups passed in an isolated copy; the regenerated CONTROL_RESULTS.json is byte-identical to the original. All 25 separately written independent control groups also passed. These include bounded enumerations of 19 categorical hierarchies and 167 binary hierarchies, and 1,322 posterior-likelihood grid cases. These counts describe test coverage, not the number of new theorems or an additive measure of proof strength.

## 1. General common-core proof

Write V_F as the orthogonal direct sum of the finite-product contrast spaces H_S for S in F. Its constant function is present because F is nonempty and downward closed. The finite maximal-face family is nonempty, even for F={∅}. Let C be the intersection of those maximal faces.

For sufficiency, every retained S lies in a maximal face T, and C is contained in T. Thus S∪C is retained. Multiplying a C-function by an S-function gives an (S∪C)-function in V_F. The retained functions span V_F, proving that every C-function stabilizes it.

For necessity, stabilization first implies L=L·1 lies in V_F. Suppose an ANOVA component L_S is nonzero and S is not contained in C. Choose S of maximal cardinality among precisely these offending components. Some maximal retained T omits an element of S. Put U=T\S. Then:

- U is disjoint from S and retained.
- U is nonempty: otherwise T would be strictly contained in retained S, contradicting maximality of T.
- S∪U=S∪T strictly contains T and therefore is not retained.

Choose a nonzero product of coordinate contrasts h_U. For a component L_R to contribute to the H_(S∪U) projection of Lh_U, it must have R\U=S. Outside U, multiplication changes no coordinate factor, so neither a missing contrast nor an extra contrast can be repaired there. Consequently R contains S. Such R is also offending. Maximality among offending components forces R=S. The forbidden projection is therefore exactly L_S⊗h_U and is nonzero.

This rules out all offending components. Several details are load-bearing and are handled correctly:

1. L_S need not be pure. Tensoring any nonzero vector with a nonzero h_U is injective over R. The proof does not factor L_S itself.
2. Overlapping categorical contrasts need not follow a binary symmetric-difference product rule. All cancellation exclusions occur using coordinates outside U and support maximality.
3. S need not have highest degree among all components. A higher-degree core component cannot contain the offending S and cannot contribute. Our independent control deliberately includes this situation.
4. Uncovered coordinates cannot enter L. The initial conclusion L∈V_F already excludes them.
5. Unequal-sized maximal faces require no extra hypothesis. “Hierarchical” does not mean pure, connected, decomposable, or graphical.

The result is an equality of real algebras, not merely of positive cones. A likelihood is then restricted separately to nonnegative values, or to [0,1] for one channel outcome. Requiring stability for every strictly positive probability-valued function on a coordinate set is sufficient to recover its entire real function algebra by linear span.

The q_i≥2 premise cannot simply be removed while retaining the nominal face core. For sizes (2,1) and maximal faces {0},{1}, the nominal core is empty, yet the retained space is the entire two-state effective function space. This independent negative control demonstrates why degenerate coordinates must be removed or the theorem's hypothesis retained.

## 2. Probability plus posterior, including impossible branches

Let M have independent retained-observable rows, including the all-ones mass row. If a decoder gives both branch probability α=Lᵀp and the complete retained posterior, it gives MD_Lp by multiplication whenever α>0. When α=0, nonnegativity implies D_Lp=0, so the unnormalized output is also determined.

For h∈ker M and a strictly positive p, both small perturbations p±εh remain probability laws because the mass row makes h mass zero. Equal retained records then force MD_Lh=0. Hence MD_L factors linearly through M. Equivalently, every retained observable times L remains retained. Conversely that factorization supplies α and, when α>0, the retained posterior. The common-core theorem supplies the claimed iff.

This proves the implication even when the prospective decoder is nonlinear, discontinuous or otherwise unspecified, and even if the tested priors are only full support. No unnecessary regularity of the decoder is assumed. The all-zero likelihood descends as the zero unnormalized map and has no possible normalized branch.

For L=ℓ(x_C), every maximal retained T contains C. Thus its posterior is obtained by reweighting p_T(a) by ℓ(a_C) and dividing by Σ_cℓ(c)p_C(c). For a smaller retained S not containing C, the necessary S∪C marginal is retained. This is a direct calculation from the actual law. It neither reconstructs the joint law nor imposes conditional independence. Repeated use refers to declared fresh likelihood factors; the algebra provides no permission to count a known observation again.

At full order F=P(I), there is one maximal face I, so every likelihood stabilizes. If only the full marginal on A⊊I is retained, C=A and precisely A-functions stabilize, not arbitrary functions of the hidden coordinates. At F={∅}, only constants stabilize, although every possible normalized posterior has the same trivial mass record. The empty product I=∅ is a harmless one-state case, also independently checked.

## 3. Normalized-only descent and feasibility

The inherited support-rank argument can be reconstructed without a decoder regularity assumption. For h∈ker M, put a=MD_Lh, b=Lᵀh and q(p)=MD_Lp/(Lᵀp). Constancy of q along a positive fibre gives a=bq(p). If any b is nonzero, q is constant on the whole full-support simplex. Taking positive laws toward each supported atom forces all supported columns Me_x to be equal. If all b vanish, all a vanish and unnormalized descent holds.

In a downward-closed marginal family, equal columns are exactly equal assignments on covered coordinates A. Every covered coordinate has all of its unary observables retained, and no retained observable depends on an uncovered coordinate. Thus the second branch of the dichotomy is support inside one A-cylinder, exactly as stated.

This gives all the declared boundary cases:

- If A=I, the cylinder is a singleton.
- If A⊊I, a cylinder may contain several latent atoms; L may vary within it.
- If A=∅, all columns coincide and normalized-only sufficiency is automatic wherever a branch exists.
- If A is nonempty and L is strictly positive everywhere, its support cannot fit one A-cylinder. The positive normalized-only classification therefore reduces to the common-core class.
- L=0 is only vacuously posterior-only sufficient and is never assigned a defined normalized posterior.

Feasibility must retain the prior-domain distinction. Full-support priors make every nonzero nonnegative likelihood feasible, so a feasibility flag cannot exclude the support exception there. On the full simplex, a partial cylinder can have supported and unsupported atoms with identical retained records, immediately defeating feasibility descent.

A whole cylinder requires a further distinction. If F=P(A), its covered assignment mass p_A(a) is retained. A likelihood positive everywhere on that cylinder has α>0 exactly when this mass is positive. Posterior and feasibility can consequently descend while branch probability fails, because hidden-coordinate weights within the cylinder are unknown. Our independent (2,2,3) example has distinct likelihoods 1/4 and 1/2 at two observationally identical atoms.

If F is a proper hierarchy on A, retaining every covered unary does not imply retaining the whole A-marginal. Equal-record correlated priors can disagree on the cylinder's mass being zero. Our second control retains only the two covered unary marginals and compares diagonal versus antidiagonal binary covered assignments, with an omitted ternary coordinate. The likelihood is positive on the entire (0,0)-cylinder, yet the two priors disagree on feasibility.

The target's text correctly avoids the false blanket claim that feasibility always removes normalized-only exceptions. No correction or new broad feasibility theorem is required to use the packet as written.

## 4. Least enlargement for all declared local evidence

Use D for the evidence coordinate set, matching the target. Let A_D be all functions of x_D. Because it is a unital algebra,

    W = span{g v : g∈A_D, v∈V_F}

contains V_F and is A_D-invariant. Any linear observable space containing V_F and invariant under every g∈A_D must contain each displayed product. This proves minimality among all linear observable spaces, not just hierarchical ones.

For each retained T, products of T-functions and D-functions span every function on T∪D. Coordinate indicators give an explicit argument: a consistent pair of assignments yields the union indicator as their product; an inconsistent pair yields zero. Hence W is exactly the hierarchy with downward-closed faces contained in some T∪D. Its maximal faces all contain D, so its common core contains D. One multiplication layer already spans the closure because A_D is an algebra.

Strictly positive probability-valued likelihoods suffice. The functions 1/4+(1/2)1_(x_D=d), for example, have values strictly between zero and one and span the D-function space. Invariance is linear in the multiplier. Requiring independent use of all local functions on several coordinate sets generates all functions on their union, since products of local coordinate indicators generate union assignments. In particular, allowing all coordinate-local evidence separately forces full-law observables.

This is a universal-in-the-evidence-set conclusion. A single fixed likelihood generates only functions constant on its likelihood-value blocks. On ternary×binary×binary unary records, our control finds:

- Initial retained dimension: 5.
- One ternary likelihood with values (1/4,1/4,3/4), alone or with its complementary channel outcome: least closure dimension 7.
- A ternary likelihood with three distinct values: least closure dimension 9.
- Every ternary-coordinate likelihood: least closure dimension 9.

The unequal dimensions directly protect against applying the all-D formula to an unspecified single categorical channel. For a nonconstant binary-coordinate likelihood, two distinct values already generate all binary-coordinate functions. The inherited six-dimensional three-bit star repair is recovered in that special case; it earns no new-result credit here. A larger channel with other outcomes needs its actual whole likelihood algebra specified.

## 5. Global Fisher-objective classification

At a retained moment z=Mp, let g represent dJ_z and f=Mᵀg. The actual negative fine Fisher gradient is

    X(p)=−diag(p)f+(g·z)p.

For two positive laws in the same retained fibre, its projected difference is −MD_f(p−q). The same local kernel perturbation argument gives fibre constancy iff fV_F⊆V_F. The common-core theorem therefore says that the fitness must be a C-function at every z.

This differential condition integrates globally. If two moment points have the same C-marginal, the entire line segment between them remains in the convex relative-interior moment domain and has zero C-marginal tangent. Pairing that tangent with the C-function fitness gives zero, so J is constant along the segment. A global smooth section is obtained by fixing a strictly positive conditional law within each C-cylinder and mixing them with weights w=p_C. Consequently J=Φ(w) with the claimed C² regularity. Conversely such an objective has C-dependent fitness and descends.

This independent reconstruction confirms there is no disconnected-fibre or local-to-global gap. The mass-coordinate gauge adds a constant to f and changes neither membership in the stabilizer nor the fine field. When C is empty, the marginal simplex has one point and only constant intrinsic objectives qualify. At full order every smooth objective qualifies.

For maximal T, summing the fine field gives exactly

    ṗ_T(a)=−p_T(a)(b_(a_C)−Σ_cw(c)b_c),

and summing again gives the C-marginal replicator equation. Signed b is unrestricted as a differential; it is not being misidentified with a nonnegative likelihood. Our nonlinear core objective Φ(w)=w₀²+(3/2)w₁²−2w₂ on a correlated ternary-centered star gives core velocity (−1/4,−1/6,5/12) from w=(1/2,1/3,1/6), identically for two distinct full-support laws with the same retained record. A leaf objective instead detects their omitted conditional interaction.

The claim is about the projection of the fine evolving-Fisher field, not a substitute metric chosen on the coarse space. The maximal-positive-existence-interval restriction is correctly retained; arbitrary C² objectives need not have bounded boundary derivatives or all-time interior solutions.

## 6. Crosswalk to finite interaction grade and conditional noetic geometry

### What is inherited and what is computed here

The tensor-likelihood packet already supplies the arbitrary-decoder multiplier criterion, the complete proper interaction-cutoff constant stabilizer, the normalized support-rank dichotomy, and the specific three-bit star repair. The leafwise packet already supplies the one-objective stabilizer criterion and the general stabilizer-block objective factorization. None of those results becomes newly established work of the hierarchical packet merely by being specialized again.

The bounded new-to-the-inspected-passages deduction is the explicit stabilizer computation for every nonempty downward-closed marginal family and the resulting all-local-evidence enlargement formula for such a family. The global Fisher corollary applies the inherited block theorem after identifying its blocks as C-cylinders. Our targeted reading found no conflict with those inspected passages; this is not an exhaustive priority search.

### Finite interaction grade is not semantic word degree

For the complete cutoff F={S:|S|≤k}, 0≤k<|I|, the maximal-face intersection is empty. The new formula therefore recovers the inherited constant algebra. At k=|I|, C=I and the full algebra returns. A nonuniform hierarchy with a nonempty common core is outside the uniform proper-cutoff obstruction even when it omits some high-order interactions. Connectedness or a junction tree is not the relevant test; the intersection of all maximal retained coordinate sets is.

The bound semantic tensor manuscript defines a free tensor algebra graded by ordered semantic words, with concatenation multiplication. The present construction evaluates a finite tensor product of coordinate function spaces and decomposes it by contrast support. Its multiplication is pointwise. Repeating a coordinate in a product may produce both constant and contrast parts; on binary coordinates x_i²=1 already prevents identification with additive word degree. Labeled coordinates are not silently symmetrized, semantic workflows are not identified with diagonal likelihood multiplication, and an ANOVA support family is not automatically a family of admissible semantic words.

### Conditional geometry is a different domain contract

A fixed-reference exponential leaf stores a log-density class as model data. Positive likelihood preservation of that same leaf requires log L∈V_F. Whole-simplex exact retained updating instead requires LV_F⊆V_F. These are different conditions.

For example, positive evidence on one retained leaf coordinate of a star has log L in the retained space and preserves its declared exponential leaf, yet generally fails all-prior closure because that coordinate is outside the common core. The independent odds-ratio and posterior controls confirm both sides in the same example. Fixing the leaf selects one law per interior retained moment; it does not make the unrestricted fibre disappear without carrying the model class.

Similarly, on a specified exponential leaf, all smooth retained-moment objectives have the exact leaf covariance cometric. Across arbitrary priors, only the common-core objectives have one shared projected fine field. An arbitrary-prior implementation cannot infer the missing class from retained marginals. The pair (moment, log-density class) from the inherited geometry recovers the complete positive law, so it is not a universal information reduction.

These mathematical conditions establish no empirical noetic mechanism, truth test, actual warrant, intervention permission, sampling advantage or restoration of a named philosophical conclusion. They do not close T20.

### Classical stabilizer ancestry

The cited primary source defines componentwise stabilizing algebras and their decomposition into disjoint-support blocks over arbitrary fields in its first sections. Since V_F contains 1, it has full support, so the source's distinction between proper and extended stabilizers collapses here. This supports the target's ancestry statement, not a field-novelty claim or an assertion that the source states this marginal-family theorem. [Randriambololona, Definition 2.6 and Proposition 2.11](https://arxiv.org/pdf/1312.0022).

## 7. Independent execution and artifact boundaries

The author replay was run from author_replay/hierarchical-marginal-core-20261010, with all five required sibling-source paths reproduced from exact checked bytes. The original target directory was not executed or edited. The author checker verifies its direct inputs and then runs its controls. It does not re-run the older transitive cone dependency gate, whose historical drift is explicitly discussed in the inherited tensor review. Our successful replay does not erase or recertify that qualification.

The independent script does not import the author checker. It constructs orthogonal integer coordinate contrasts, the retained space and its orthogonal complement, and exact multiplier constraints from their products. It also uses independent repeated multiplication closure, exact posterior polynomial identities, explicit same-record priors, and signed Fisher fields. Its highlights are:

- All 19 nonempty downward-closed families on a 2×3×2 product, tested by exact ambient linear constraints.
- All 167 nonempty downward-closed families on four binary coordinates, tested through exact character support shifts.
- Unequal-dimensional maximal faces, omitted coordinates, the empty product, and a deliberately violated singleton-alphabet hypothesis.
- A rank-two H_{0,3} categorical component below a degree-three core component. For an event likelihood strictly inside (0,1), the constructed full-support priors share every retained observable and branch probability 1/2 but yield tested posterior means ±5/512.
- Strictly positive generators, an all-linear-space product-span certificate, and smaller repeated-value fixed-channel closures.
- 1,322 exact finite likelihood cases of the posterior polynomial criterion, including zero likelihood as a vacuous case.
- Whole/partial cylinder, full/proper covered hierarchy, full-simplex/full-support feasibility distinctions.
- A nonlinear core objective, mass gauge invariance, a non-core obstruction, and a fixed-leaf versus all-prior contrast.

To replay from this review directory:

    python3 author_replay/hierarchical-marginal-core-20261010/verify.py
    python3 independent_controls.py
    python3 verify_bindings.py

The first command writes only its isolated copy's results. The second writes only this review's independent results. The third verifies frozen target, direct inputs, replay identities and review-manifest identities without changing them. Logs and JSON results are included. MANIFEST.json binds the delivered review files; ORIGINAL_PACKET_BEFORE.json and ORIGINAL_PACKET_AFTER.json prove that every originally present target-directory file, including the existing compiled cache, remained unchanged during this review.

No source correction is requested. Preserve the stated hypotheses, inherited-credit boundary and output-contract distinctions whenever the result is reused.
