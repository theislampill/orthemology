# Restricted correction controls and the exact information they require

11 October 2026. A source-bound cross-front deduction prepared during the owner's synthesis-depth reassessment. This is post-cutoff research, kept outside the unchanged delivered v2. Ordinary mathematics; no field-level novelty, kernel verification, psychological interpretation or repository adoption claimed.

## 1. Question and inherited starting points

The current field guide connects operation-relative finite sidecars (ET-09), tensor continuation (MOM-01) and missing geometric context (GEO-06). Their quantifiers differ. ET-09 is a finite-state contract; MOM-01's recovery of every aggregate weight permits every coarse linear control; GEO-06 supplies a smooth mean/leaf reconstruction of an entire positive law.

What if the permitted correction objectives occupy only a declared linear subspace? Does the inherited full-control requirement still force every aggregate weight to be retained?

No. The exact sufficient record can be smaller, and can be computed by grouping support points according to the controls' actual distinctions. The construction below uses the actual MOM-01 dynamics and H-Continuation's established observable-span and augmentation principles. The explicit restricted-control classification is a deduction from them, not a new general observability theory. Restriction to a chosen control subspace is mathematical input, not proof that a noetic permission system supplies that subspace.

Source owners:
- MOM-01: `tensor-moment-continuation-20261009/RESULT.md`, SHA-256 `03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11`, especially §§2–5 and the rich-control qualification following Theorem 2.
- H-Continuation: `continuation_complete_orthing.md`, SHA-256 `626504b64c2d7817b882e74992ba989d83c7ef8e67b1467b537101c2b804edb9`, observable closure and Proposition 9's continuous augmentation bound.
- GEO-06: `leafwise-noetic-geometry-20261010/RESULT.md`, SHA-256 `6d5c3c38f6e89c8f74f3b5d58cabcace7b9cae0eb2d6f8bf3a2f6ef4f4aef724`, §§6–8. Its full mean/leaf record remains sufficient; minimality depends on the operation/output contract.

## 2. Declared domain and record

Let fixed support columns κ₁,…,κ_N lie in the probability simplex in R^m. We may first aggregate identical columns as in MOM-01. Let w be any strictly positive normalised law on these columns; q=Σ_j w_j κ_j is the retained output. Controls g(t) belong to a fixed linear subspace U of R^m and are piecewise constant with finitely many switches on bounded intervals. The actual dynamics are

    ẇ_j = −w_j(g·κ_j − g·q).

Define j~ℓ iff g·κ_j=g·κ_ℓ for every g∈U. Write the equivalence classes G₁,…,G_s. The fitness signature of G_a is the common functional α_a∈U*, α_a(g)=g·κ_j. Retain its unnormalised full-output barycentre

    b_a(w)=Σ_{j∈G_a} w_j κ_j.

Its mass is m_a=1ᵀb_a, since every κ_j has coordinate sum one. Thus q=Σ_a b_a. B is the linear map w↦(b₁,…,b_s), and A is w↦q. The admissible B-domain is BΔ_N°, rather than an arbitrary product of independently chosen barycentres.

## 3. Exact restricted-control continuation theorem

For positive laws w,w′, the following are equivalent:

1. Bw=Bw′.
2. Full q-output histories agree for all common permitted piecewise-constant U-controls.
3. Full q-output histories agree under every constant U-control.
4. Full q-output histories agree on [0,ε], for any ε>0, under one fixed v∈U separating the distinct signatures α_a.

For s=1, any v∈U is suitable; all fitnesses are equal and the dynamics are stationary. Equality in item 4 then means equality of the constant full q-output.

### Proof

For integrated control u(t)=∫g, the inherited exponential solution groups exactly as

    Z_w(u)=Σ_a m_a exp(−α_a(u)),
    q_w(u)=[Σ_a b_a exp(−α_a(u))]/Z_w(u).

Therefore (1) implies (2), and (2) implies (3) implies (4). If s>1, a separating v exists because U is not the union of the finitely many proper kernels of α_a−α_b. Set λ_a=α_a(v), which are distinct. If s=1 the reverse implication is immediate, as B=A.

For s>1, equality of full q(t) implies equality of its scalar projection v·q(t). The latter equals −d log Z_w(tv)/dt. Both initial normalisers equal one. Integration gives equality of Z throughout the interval. Equality of q then gives

    Σ_a (b_a(w)−b_a(w′)) exp(−tλ_a)=0

throughout that interval. Componentwise differentiation at zero to orders 0,…,s−1 gives an invertible Vandermonde system, so each b_a(w)=b_a(w′). This proves (4)⇒(1). The derivative argument concerns exact continuous observations, not finite samples or a numerical identification algorithm. □

The grouped record also has exact closed dynamics:

    ḃ_a=−(α_a(g)−g·Σ_c b_c)b_a.

It preserves its actual admissible image because it is the grouped image of the positive exponential solution. It makes no claim about arbitrary states outside that image.

## 4. Exact continuous augmentation cost

If q remains available and the sidecar must be a continuous real-vector function of w, then the minimum additional number of coordinates needed for exact continuation is

    k = rank(B) − rank(A).

### Proof

A factors through B by summing its blocks. Extend a basis of row(A) to row(B) with k rows; their expectations give a linear sufficient sidecar. This proves attainability.

For necessity, the theorem forces any sufficient combined representation (Aw,h(w)) to distinguish different B-values. Restrict B to ker A. Its rank is k by rank subtraction. Choose k tangent vectors in ker A with independent B-images. Their coordinate sums vanish because mass is a row of A. A sufficiently small open k-box around any positive w remains positive and has constant Aw and distinct B-values. The continuous sidecar must inject this box into R^r. By the same invariance-of-domain dimension obstruction used in inherited H-Continuation Proposition 9, r≥k. For r<k, compose with the coordinate inclusion R^r→R^k; an injective continuous image would have to be open in R^k but lies in a proper subspace. □

If k>0, no finite or countably valued sidecar, even discontinuous, suffices, because the same box contains uncountably many B-values. Conversely arbitrary pathological real-valued encodings are excluded from the dimension theorem by continuity. This is not a finite-bit lower bound for approximate/noisy operation, nor an acquisition or sample-complexity claim.

When all support points are U-distinguished, B has rank N and k=N−rank(A), recovering the familiar need to distinguish every aggregate weight. If U={0}, there is one group, B=A and k=0. Between those cases, U can be low-dimensional yet distinguish all columns, so control dimension alone is not a memory bound.

## 5. Six-state exact control: a genuinely smaller sufficient record

Take six simplex columns κ(x,y)=(x,y,1−x−y), with x∈{0,1/2}, y∈{0,1/4,1/2}. Let U=span{(1,0,0)}, so only the x-coordinate supplies fitness. The two signature groups have fixed x; each group's barycentre is determined by its mass and y-total. Hence rank(A)=3, rank(B)=4, and one additional continuous coordinate beyond q is necessary and sufficient.

The whole law has five degrees of freedom. The full-control contract needs three extra coordinates beyond q, whereas the restricted-control contract needs one. Both minima refer to the same laws, same output and same metric; the admissible controls differ.

In column order (0,0),(0,1/4),(0,1/2),(1/2,0),(1/2,1/4),(1/2,1/2), take the uniform law w and

    h=(1,−2,1,0,0,0)/24.

The positive laws w+h and w−h have identical B-records and therefore identical complete permitted q-histories. They are not the same law. An additional y-fitness control distinguishes their projected y-velocities, so expanding the allowed operation family invalidates this particular quotient.

For a contrasting q-only failure, use

    k=(1,0,−1,−1,0,1)/24.

The laws w+k and w−k have the same q, but different b_a. Under an x-tilt that weights the second group by 1/2, their resulting y-means differ. The omitted coordinate is genuinely needed.

The reference controls use exact rational arithmetic and symbolically arbitrary positive group multipliers. They do not estimate a real population or validate noetic calibration.

## 6. Several permitted control families: separate profiles need not compose

Let U₁,…,U_r be finitely many linear control subspaces. Permit finite concatenations of controls chosen from their union, with arbitrary real amplitudes. Their integrated endpoint parameters span U=U₁+…+U_r, because each summand may be applied over its own positive-duration stage. Conversely every such history has its integrated parameter in U. The exact continuation theorem therefore applies to U. Its signature groups are the common refinement of the individual signature groups.

Necessity does not require the one generic U-control itself to be an admitted instantaneous control: each desired endpoint u∈U can be realised by a finite concatenation. Equality of all such histories gives equality of q(u) for every u∈U, including u=tv for a separating v, and the earlier proof then applies. A fixed duration is harmless because each subspace permits arbitrary finite amplitudes. If amplitudes, order, duration or menus are restricted, this argument needs their actual reachable parameter set instead.

However, retaining the sufficient grouped barycentre profile for each U_l separately is not always sufficient for their composed repertoire. Linear spans of the individual records need not be invariant under the other allowed operations. An explicit exact control makes that failure concrete.

Take the nine simplex support points κ(x,y)=(x,y,1−x−y), x,y∈{0,1/4,1/2}, in row-major order. Start with the uniform law w, put v=(1,−2,1), and let h_(ij)=v_i v_j/100. Both w+h and w−h are strictly positive. With U_x=span{(1,0,0)}, each row's mass and y-total agree because Σ_j v_j=Σ_j y_j v_j=0. Thus their complete full-q histories agree under every x-only control. By the same argument their complete histories agree under every y-only control. Even the combined list of those two isolated response profiles is identical.

An x-correction followed by a y-correction is different. Use integrated covectors (4 log 2,0,0) and (0,4 log 2,0); the total factor at (i,j) is 2^(−i−j), with i,j=0,1,2. The exact rational controls verify that the final q-values differ. The full x/y-composed repertoire distinguishes all nine support weights, because its two-dimensional signatures are distinct. The concatenated isolated-profile matrix has rank eight; the faithful composed record has rank nine. The missing one-dimensional tensor is precisely v⊗v.

This is a structure-preserving reuse of inherited higher-order interaction and continuation machinery, and parallels ET-05's failure of separate historical revision profiles. It is not a claim that tensor order alone determines memory, or that the older profile counterexample was absent. Here the operations are actual controlled Fisher corrections on the same current law, and the domain and exact missing direction are explicit.

## 7. Contribution and boundaries

This is a meaningful synthesis clarification of a conditional quantifier: the full-control minimum must not be carried into a restricted-control application unchanged. It provides an explicit quotient and exact augmentation dimension for that intermediate regime. The general machinery and its dimensional principle are inherited; any novelty claim is limited to this written specialisation relative to the directly inspected sources, pending wider source-overlap review.

It does not identify permitted intellectual investigation with an arbitrary selected U, reduce actual epistemic grounds to numerical means, identify equal numerical columns with equal sources, or authenticate a target/metric. Named-source withdrawal, recalibration, additional observations and boundary support restoration are absent from this contract. Adding them requires recomputing the faithful representation. Finite-state D1 sidecar bits and the present continuous-coordinate minimum remain different results.
