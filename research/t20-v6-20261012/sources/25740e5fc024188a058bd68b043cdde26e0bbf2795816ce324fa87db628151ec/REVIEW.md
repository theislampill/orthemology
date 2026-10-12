# Independent review: Hessian flow, scalar closure, and predictive memory

9 October 2026. Ordinary independent mathematical/source-interface review. No authored report or retained source was edited by this reviewer. No repository integration, protected edit, proof-assistant execution, or programme closure is part of this review.

## Verdict

The mathematical results pass independent review at their stated, corrected scopes:

1. The actual inherited canonical nudge has a unique local flow under the inherited C2 interior assumptions, by C1 dual-coordinate conjugacy.
2. Scalar projected velocity on the full open product domain is autonomous exactly for common-slope affine reciprocal curvatures, when n is at least two.
3. Projected scalar closure does not by itself preserve the maximal admissible lifetime or the boundary-stop event. The explicit quadratic same-sum separator below is essential to this distinction.
4. The binary-log field is globally defined on the open cube. For n at least two its forward trajectory converges to the stated unique interior Bregman projection; its backward trajectory is not confined to the same compact interval.
5. Exact prediction of the original-clock binary-log scalar trajectory on a positive time interval needs exactly n continuous real coordinates on the stated open ordered incoherent chambers. The proof allows an arbitrary decoder. Normalization changes this target to one requiring exactly one coordinate.

No blocking formula or theorem defect was found. Review corrections concern a forward-time quantifier, the exact inherited normalization source, the difference between scalar projectability and admissible lifetime, and consistent notation in the numerical/noetic interface. The final reviewed-byte manifest records the corrected versions separately from the initial input manifest.

## 1. Direct source-interface verification

All listed source-byte identities match the recovery packet's SHA-256 records. Matching bytes binds this review to the retained snapshot; it is not source authentication or a new Lean run.

- `SmoothScalar.lean`, lines 10–18: the record has continuity of f on the closed interval; derivative witnesses for f and df in the open interval; continuous positive ddf there. There is no C3 assumption, global lower curvature bound, or bounded endpoint derivative assumption. Lines 26–32 differentiate divergence with respect to its second argument for arbitrary first argument p.
- `SmoothRigidity.lean`, lines 110–119: the diagonal bilinear form is precisely the sum of ddf_i(b_i) u_i v_i. Lines 132–147 prove the actual Fréchet derivative of each Bregman loss in its forecast argument. Lines 273–288 establish interior positive definiteness.
- `NudgeRigidity.lean`, lines 149–165: `canonical_nudge_gain` is exactly the pointwise identity dD_F(e_j,b)[V]=−(sum b−1)^2. It is not an existence, invariance, convergence, or observability theorem. Its formula does not require the three-coordinate hypothesis of the separate universal rigidity classification in lines 177–209.
- `CoherentNudgeRigidity.lean`, lines 29–103: the positive reciprocal curvatures A and their sum S are used to construct c−base=S^−1 V at a prescribed sequence approaching an interior coherent point. The relation is explicit in lines 75–83. This is the actual ancestry of the normalized direction. The source does not claim that b+V/S is an interior endpoint at every arbitrary input, or already supply the global normalized ODE.
- `continuation_complete_orthing_full.md`, directly inspected lines 248–284 and 615–625: exact output separation, encoder injectivity, and invariance of domain already yield continuous-coordinate and fixed-summary augmentation bounds. The memory report correctly reuses that argument; it does not apply the older finite-law rank formula verbatim to this nonlinear flow. The retained file hash is `626504b64c2d7817b882e74992ba989d83c7ef8e67b1467b537101c2b804edb9`.

The historical `CORE_RECEIPT.json` reports a source-bound custom closure completed 2 October, and explicitly says original controls were not run. Its status remains historical evidence about the named old sources. It supplies no automatic kernel credit to the newly written ODE, functional-equation, or topological arguments.

## 2. Flow regularity and invariants

Write h_i=f_i'' and q_i=1/h_i. The map f_i' is C1 with strictly positive derivative on (0,1). It is strictly increasing, has an open interval image I_i, and has a C1 inverse phi_i. Therefore the transformed equation

    y_i' = 1 − sum_k phi_k(y_k)

has a C1 vector field on the product of the I_i. Standard local ODE uniqueness applies there, and conjugating back proves uniqueness of the original continuous field V. It would be incorrect to justify this by asserting that all the original reciprocal curvatures are locally Lipschitz.

This regularity distinction is real. For example, f(x)=x^2/2+(4/15)|x−1/2|^(5/2) has h(x)=1+sqrt(|x−1/2|). It satisfies the inherited interior regularity, but q is not locally Lipschitz at 1/2. At an incoherent input having that coordinate, neither is the corresponding component of V in general. The dual-coordinate proof still applies.

Each dual derivative is equal to the same scalar, so all y_i−y_j are constant. The parameterized expression b_i=phi_i(alpha_i+lambda) is correct only while all alpha_i+lambda remain in their respective images. The alpha differences are fixed initial-state parameters; their presence prevents treating this one-dimensional equation along one orbit as a one-real-number encoding of the whole family of orbits.

The loss identity gives, on every admissible time interval,

    D_F(e_j,b(t)) = D_F(e_j,b(0)) − integral_0^t r(u)^2 du.

Consequently all statewise loss differences are conserved. This remains a statement about the declared loss family and field, rather than a preservation theorem for evidence, warrant, source authority, or all possible update rules.

## 3. Scalar iff and the boundary guard

The scalar report's three mathematical conditions are equivalent: projected velocity depends only on z; S=sum q_i depends only on z; and q_i(x)=a x+c_i with a common slope. The proof needs no derivative of q_i.

The step at the zero factor z=1 is legitimate: shift the same coordinate of two equal-sum points by the same sufficiently small nonzero increment, use the noncoherent equality of S, and pass to the limit by continuity. Thereafter, transferring a small increment between distinct coordinates gives a common continuous increment function. Local additivity forces linear increments, and subdivision extends the common slope across each interval. This works for n=2. It does not work for n=1, where z is the full state and every admissible q closes.

Once the affine form is obtained, the scalar equation is

    z' = −(z−1)(a z+sum c_i).

This locally Lipschitz scalar equation justifies projected output agreement for equal initial sums while the original solutions exist in the domain. It does not determine their domain of existence.

### Same scalar trajectory, different admissible lifetime

For q_i=1 and n=3, put

    a=(1/100,4/5,4/5),
    b=(161/300,161/300,161/300).

Both have initial sum 161/100. Their unrestricted scalar solution is the same:

    z(t)=1+(61/100)exp(−3t).

The first trajectory reaches (0,79/100,79/100) at t=log(61/58)/3, so its open-cube maximal forward interval is finite. The second has coordinates 1/3+(61/300)exp(−3t) and remains interior for every forward time. Thus even exact scalar projectability cannot recover a boundary-STOP event from z alone.

The root's added quadratic guard (z,m), where m=min_i b_i, is correct. Equal coordinate velocities preserve ordering; m(t)=m(0)−r0(1−exp(−nt))/n. For positive r0, a finite exit occurs exactly when r0>n m(0), with time −log(1−n m(0)/r0)/n. Equality gives a boundary limit only at infinite time. For r0≤0 and n≥2, coordinates increase, their sum stays at most one, and the other coordinates remain strictly positive, excluding an upper-boundary hit. Some additional information beyond z is necessary for this output-plus-stop target; the minimum is one sufficient choice, not the uniquely required statistic.

These controls also show why full-product, clock, domain, and output quantifiers must remain separate. On the coherent simplex alone, V=0 for every generator, so arbitrary nonaffine q satisfy trivial scalar stationarity. On a restricted one-dimensional family, z may also suffice without satisfying the full-product classification.

## 4. Binary-log global solution and endpoint

For f(x)=x log x+(1−x)log(1−x), the formulas h=1/[x(1−x)] and phi=logistic are correct. The shifted sum Z(lambda) is strictly increasing from zero to n. For n≥2, one lies strictly inside that range, giving a unique finite lambda-star. The equation lambda'=1−Z(lambda) is globally Lipschitz and bounded. For forward time it remains between zero and lambda-star and converges to lambda-star. This compact interval claim is not true in backward time unless the solution is stationary.

The resulting forward orbit is contained in a compact interior set, so S has a positive trajectory-dependent minimum and |r| decays exponentially. There is no uniform lower bound on S over all interior states: interior points can approach a truth vertex. The n≥2 hypothesis is essential to a finite dual endpoint. For n=1, the original flow is b'=b(1−b)^2 and approaches b=1 on the boundary; it has no finite lambda-star.

The Bregman three-point calculation has the correct sign:

    D_F(p,b0)−D_F(c,b0)=D_F(p,c)+<grad F(c)−grad F(b0),p−c>.

The inner product is lambda-star times sum(p−c)=0 on the categorical simplex. Strict convexity and continuity at its boundary give a unique minimizer c, including comparison against boundary points p. No undefined gradient at p is used. A useful exact consequence is that the full accumulated common loss decrease is D_F(c,b0), but this does not identify c with a truth vertex or an epistemic warrant.

## 5. Exact binary-log predictive-memory proof

The memory report's global existence argument is sound for every n≥1: finite-time logit growth is bounded while in the cube, preventing a boundary hit; a polynomial vector field confined to that bounded region cannot blow up. Coordinate order and the sign of r are preserved. Hence one common fixed observation horizon T>0 is legitimate.

Direct differentiation yields p_k'=k r(p_{k+1}−p_k). The recursive output-jet polynomial Q_j has leading term j!r^j p_{j+1}; only differentiating that highest moment creates p_{j+2} at the next step. Differentiating its coefficient and the lower-moment remainder creates no higher moment. This proves the arbitrary-order induction, not merely the finitely checked instances.

At r≠0 the first n output-jet entries therefore recover p_1 through p_n. Newton identities determine the characteristic polynomial and its root multiset, including multiplicities. On a fixed strictly ordered chamber, that multiset determines the initial vector. The determinant

    det DJ = (product_{k=1}^n k!)(z−1)^[n(n−1)/2] product_{i<j}(b_j−b_i)

has the correct coefficient and sign with the report's row and coordinate order. The rectangular Vandermonde rank argument also correctly makes consecutive derivative order n−1 sharp on the stated open domain.

If an exact continuous encoder assigned the same record to two chamber states, the decoder's identical output would give identical jets and hence identical states. Thus the encoder is injective. Zero-padding an encoder into fewer than n real coordinates would produce a continuous injection from an open subset of R^n into R^n with image inside a proper coordinate plane, contradicting invariance of domain. Decoder continuity is unnecessary. The n-coordinate identity or moment encoder attains the bound.

The following exceptions are correctly preserved:

- Permutations are output-indistinguishable; labels are not recovered on the full cube.
- Repeated coordinates do not spoil Newton multiset recovery, though they invalidate the displayed nonsingular chamber determinant at that point.
- All coherent inputs have the same constant output and require zero coordinates when considered as the entire restricted domain.
- If z(0) is free side information, exactly n−1 additional coordinates suffice and are necessary on fixed-sum incoherent open pieces.
- A single future scalar value is a different target and can itself be used as a one-coordinate continuous encoder. The theorem concerns the whole local time function.
- Approximation, noise robustness, discontinuous infinite-precision encodings, finite bits, runtime, interventions, unknown n, and uncharged state-dependent side information are outside this contract.

The explicit three-coordinate pair a=(1/10,1/2,3/5), b=(1/5,3/10,7/10) has the same z=6/5, S=29/50, and z'=−29/250, but z'' equals 853/12500 and 889/12500 respectively. This was checked independently from z''=r S^2+r^2 sum_i b_i(1−b_i)(1−2b_i), rather than by relying only on the author's expanded jet polynomial.

## 6. Normalized clock and source/application boundary

For W=V/S, the time transformation is d tau/dt=S, not its reciprocal. It gives dz/dtau=1−z and changes each statewise loss derivative to −r^2/S. The reversed factor is dt/dtau=1/S. Both reports use the correct orientation. The normalized binary-log flow is forward global, including n=1 where it is simply b'=1−b. One continuous coordinate suffices for its scalar trajectory and zero cannot suffice on a nonempty open domain with varying initial z.

For an arbitrary score family, time-reparameterization preserves oriented interior curves but is not a theorem about equal maximal time intervals. The quadratic boundary control already prevents that inference. Likewise, common positive scaling of the generator rescales the original field's clock; the normalized field cancels that scaling.

The noetic interface report preserves the needed distinction between (i) a numerical theorem, (ii) a licensed-operation realization map, and (iii) an actual execution witness. A numerical summary sufficient for one output cannot by itself establish eligibility, authority, a source-basis update, or closure. This review checks the mathematical consistency of that boundary; it does not independently audit the entire noetic source corpus or instantiate the missing map. The author's checked notation repair now uses b for forecast coordinates, leaving q_i for reciprocal curvatures in the mathematical reports.

The root's combined result also gives a valid tensor formulation: with a declared aligned basis, the covariant diagonal sum_i e_i* tensor ... tensor e_i* contracts b tensor ... tensor b to p_k. This is an ordinary multilinear identity. Tagged copies and the shared coordinate alignment are explicit; arbitrary basis invariance is not claimed. The text correctly says that degree-one full-coordinate storage also suffices, so the moment hierarchy is not misreported as a universal requirement for high tensor order. The combined summary's final checked revision now retains n≥2 for the scalar affine iff and for the binary-log interior coherent endpoint.

## 7. Attribution and verification ceiling

Inherited contributions are the score signature, actual Bregman derivative, positive Hessian form, canonical gain, pointwise normalized direction, fixed-generator universal rigidity, and the separation/invariance-of-domain proof method. The older universal classification concerns two fixed families and at least three truth states; the new scalar projectability theorem concerns one field on a full product with at least two coordinates. Neither replaces the other.

Classical ingredients include inverse-function and ODE theory, dual/Legendre coordinates, continuous Pexider equations, time changes, Bregman optimality, Newton identities, observability via output derivatives, and invariance of domain. The author-hosted Alvarez–Bolte–Brahic paper was independently opened; its introduction and displayed Hessian-gradient/Bregman discussion support the broad ancestry claim. No general global theorem from that paper is imported into this proof. See [the author-hosted paper](https://www.math.tecnico.ulisboa.pt/~brahic/Legendre10.pdf).

The model-specific additions are the declared continuation analysis, precise boundary and clock separators, the common-slope scalar classification applied to this canonical field, and the explicit binary-log jet/reconstruction/memory calculation. This is a bounded contribution assessment, not an exhaustive novelty search.

Independent controls: `independent_controls.py` freshly passed 29 named exact rational/symbolic checks. They cover the numerical flow/clock controls, the stronger lifetime separator, direct moment recurrences, and direct low-dimensional state-coordinate jet determinants. All three author control scripts were also freshly replayed from byte-identical copies inside this review's own directory, so no authored result file was overwritten. The flow's 46 assertions and memory's 66 checks passed, with generated result bytes exactly matching their retained author results; the scalar controls also passed. `AUTHOR_CONTROL_REPLAYS.json` binds those copied scripts and outcomes. Analytic global existence, the arbitrary-order induction, and topology were checked by written proof; no finite test is credited as proving them.

The review reaches mathematical acceptance at the explicit corrected scope. It supplies no new kernel, deployed-runtime, empirical-cognitive, source-authentication, integration, or programme-closure status.
