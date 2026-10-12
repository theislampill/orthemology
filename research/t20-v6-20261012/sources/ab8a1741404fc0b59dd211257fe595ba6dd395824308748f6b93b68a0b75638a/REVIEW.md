# Independent supplementary review: exact forward admissibility

9 October 2026. This is a separate review of `hessian-general-admissibility-20261009/GENERAL_ADMISSIBILITY.md`. The completed original continuation review and its frozen checkpoint are unchanged. No author source file is edited by this reviewer.

## Verdict

The supplement passes independent mathematical review after three explicit scope clarifications: the general finite family has n≥1, the joint convex negative-Shannon classification has n≥3, and its coordinate-interiority claim is for t≥0. The terminology now correctly identifies the convex generator as negative Shannon entropy; the formula x log x/a was correct throughout. No substantive theorem defect was found.

The exact individual-start criterion, the n=2 and subcoherent corollaries, the n≥3 all-start classification, the joint scalar/safety classification, and the normalized-clock boundary distinction are all valid under the actual inherited Score assumptions. These are ordinary mathematical results, not kernel, deployed-runtime, noetic-authority, or closure certificates.

## 1. The dual interval and local regularity

For each coordinate, f_i' is C1 and strictly increasing, with interval image (ell_i,u_i). Its inverse phi_i is C1 with positive derivative 1/h_i(phi_i). For a finite nonempty coordinate family and an interior initial vector, the intersection of shifted intervals is exactly

    J=(L,R),
    L=max_i(ell_i−alpha_i), R=min_i(u_i−alpha_i),
    L<0<R.

The scalar Z=sum_i phi_i(alpha_i+lambda) is C1 and strictly increasing on J. The transformed equation lambda'=1−Z(lambda) consequently has a unique maximal solution. The inverse transformations in both directions justify transferring uniqueness to the original field despite its potentially non-Lipschitz reciprocal curvatures in the original coordinates.

The finite, nonempty family condition matters. An empty index family would invalidate the strict inequality Z'>0 and the displayed max/min definitions. The final report now states n≥1 explicitly.

## 2. Exact forward-lifetime criterion

Since Z is strictly increasing, an interior root exists exactly when its endpoint limits satisfy Z_L<1<Z_R. The root is unique. The forward solution either is stationary at it or moves monotonically toward it without crossing it. The interval between its initial shift and this interior root is compactly contained in J, and the corresponding coordinate rectangle is compactly contained in the cube. This proves forward global existence and interior convergence.

Near the root, C1 regularity and a finite positive Z' give linear first-order vanishing of |1−Z|. The reciprocal travel-time integral therefore diverges logarithmically. Thus no nonstationary solution reaches this interior equilibrium in finite time.

If the initial sum exceeds one and Z_L≥1, there is no root to the left. The solution moves toward L and has exact maximal interior lifetime

    T=integral_L^0 d lambda/(Z(lambda)−1).

The corresponding upper-directed formula is integral_0^R d lambda/(1−Z(lambda)). Separation of variables is legitimate throughout the open interval because the denominator has a fixed nonzero sign. The inverse travel-time map constructs the unique solution. A finite limiting shift strictly inside J with nonzero velocity could not be maximal, so the indicated endpoint and integral are exact.

A finite T is a loss of admissibility for the declared open cube even when a coordinatewise continuous completion exists. It does not license extending the same field through a degenerate or excluded boundary point. Infinite T makes every finite-time state admissible, but does not alone give an interior limit.

## 3. Sharp cube consequences

For n≥2 the upper endpoint always has Z_R>1. At a finite R, at least one coordinate tends to one, and each other coordinate stays above its strictly positive initial value. At infinite R, every coordinate tends to one, giving Z_R=n. Therefore every subcoherent interior initial point has an interior coherent root and is forward safe for every admissible Score family.

A lower-directed failure requires Z_L≥1. Its L must be finite: L=−infinity would mean all lower dual endpoints are −infinity and all coordinates tend to zero. A finite L has at least one coordinate tending to zero.

If Z_L>1, the denominator stays between the positive constants Z_L−1 and Z(0)−1. The report's bounds

    (−L)/(Z(0)−1) ≤ T ≤ (−L)/(Z_L−1)

are correctly oriented, and give finite exit. If Z_L=1, the integral can be finite or infinite. Bounded Z' near L is sufficient for infinite arrival, since Z(lambda)−1≤M(lambda−L); unbounded Z' alone is not asserted sufficient for finite arrival.

For n=2, a lower boundary has one zero coordinate and the other strictly below its initial value, hence below one. Thus Z_L<1 and every initial interior point has an interior root. This is why the later n≥3 universal classification cannot be extended to n=2.

The n=1 exclusion also matters. There is no coherent point in its open cube. For example, f(x)=(1−x)^3/6 has h(x)=1−x and canonical field b'=1, reaching the coherent upper boundary in finite time. The report's general integral criterion allows this, while its n≥2 corollaries appropriately exclude it.

## 4. Coherent boundary reached at finite time

The author's exact mixed-family control is correct:

    f_1=x^3/6, h_1=x; f_2=f_3=x^2/2, h_2=h_3=1,
    b0=(1/2,5/8,5/8), alpha=(1/8,5/8,5/8), L=−1/8.

Putting u=lambda+1/8 and x=sqrt(2u) gives

    b=(x,1/2+x^2/2,1/2+x^2/2),
    z−1=x+x^2, x'=−1−x.

Therefore x(t)=(3/2)exp(−t)−1 and the first domain exit is exactly T=log(3/2), at (0,1/2,1/2). The travel-time substitution du=x dx correctly reduces the integral to integral_0^(1/2) dx/(1+x). The field's first component tends to −1 along this path, even though the residual tends to zero, because its curvature also vanishes. The endpoint is outside the positive-definite interior domain, so interior equilibrium uniqueness supplies no contradiction.

The comparison with the quadratic family is also correct: from (1/4,3/4,3/4), the trajectory is (x,1/2+x,1/2+x) with x=(1/4)exp(−3t). It has the same initial sum 7/4 and the same coherent boundary limit, but infinite arrival time. These are two different declared generator families. They show that limiting boundary coherence alone does not determine lifetime across the admissible Score class; they are not a same-fixed-field encoder lower-bound argument.

The root's earlier all-identical power-curvature candidate is valid as well, though it is not needed by the final proof. For f=4x^(5/2)/15, h=sqrt(x) and phi(y)=(3y/2)^(2/3). The boundary c=(0,9/25,16/25) has limiting dual coordinates (0,18/125,128/375). A small positive common shift u0 gives Z(u)−1≥(3u/2)^(2/3), hence T≤3(2/3)^(2/3)u0^(1/3)<infinity. This was independently checked without being substituted for the author's exact mixed-family example.

## 5. All-start safety iff every lower derivative diverges

For a fixed family and fixed n≥3, the three stated properties are equivalent: every interior initial point survives every finite forward time; every one converges to an interior coherent point; every lower derivative endpoint is −infinity.

Sufficiency is direct: all lower endpoints −infinity give L=−infinity and Z_L=0 for every initial vector; the upper-limit argument gives Z_R>1. Hence every dual orbit has an interior root.

Necessity is a genuine fixed-family construction. If ell_i is finite, choose the other initial coordinates r_j strictly between zero and one with sum greater than one. Such a choice exists because n−1≥2. Choose the ith coordinate close enough to zero that delta=f_i'(b_i0)−ell_i is small. At shift −delta the ith coordinate tends to zero; all others remain interior and approach their selected r_j as delta tends to zero. For sufficiently small delta their endpoint sum remains greater than one. Thus the first lower endpoint has Z_L>1 and is reached in finite time.

This proves necessity even for the weaker all-start finite-time-safety property, so it also proves the equivalence with universal interior convergence. It does not say that every state is unsafe when one lower endpoint is finite: all subcoherent starts remain safe.

No upper derivative barrier is required. The conclusion concerns this particular objective and canonical field, rather than geodesic completeness of the metric or safety for arbitrary gradient objectives.

## 6. Joint original-clock scalar closure and all-start safety

The previously reviewed scalar theorem gives q_i(x)=a x+c_i with a common slope on the full product for n≥2. For n≥3, combine this with the just-proved all-start criterion.

Positivity on (0,1) forces c_i≥0. If c_i>0, h_i=1/(a x+c_i) is bounded near zero, so integrating h_i shows that f_i' has a finite lower limit. Therefore all-start safety forces every c_i=0, and positivity then forces the common a>0. Conversely q_i=a x gives f_i'=(log x)/a plus a coordinate constant, so each lower limit is −infinity.

Integration yields precisely

    f_i(x)=x log x/a + beta_i x + gamma_i

on the source interval, continuously extended at zero. These coordinate-affine terms do not alter the Hessian or field.

The explicit solution formulas are correct:

    z'=a z(1−z),
    z(t)=z0/[z0+(1−z0)exp(−a t)],
    b_i(t)/z(t)=b_i0/z0.

For t≥0, the denominator stays positive; all coordinates move monotonically between their initial values and b_i0/z0, with the latter strictly between zero and one for n≥2. This is the unique joint class under the fixed-selector, fixed-clock, full-product and n≥3 quantifiers. It is not a classification of every safe geometry: binary-log curvature gives safety without original-clock scalar projectability.

Forward time is essential. For q_i=a x and b0=(1/2,1/2,1/2), the same solution reaches the upper boundary (1,1,1) at the finite negative time −log(2)/a. Thus the binary-log family's earlier two-sided completeness cannot be transferred to the entire new safe class. The final author's wording explicitly restricts its claim to t≥0.

## 7. The normalized clock does not preserve STOP timing

In a lower-directed boundary case r>0, r'=−r S yields

    tau(t)=integral_0^t S ds=log(r0/r(t)).

For a coherent boundary, r(t) tends to zero, so tau tends to infinity even when the original T is finite. For the exact mixed example S=1/x+2 and x'=−1−x; differentiating log[(3/4)/(x+x^2)] gives exactly S. Thus the normalized trajectory is interior at every finite normalized time while approaching the same excluded endpoint asymptotically.

For a strict-residual boundary, tau_exit=log[r0/(Z_L−1)] is finite. The boundary point and path are preserved but arrival times are not. These statements are explicitly about the declared numerical model clock, not physical research time or permission to execute an owner operation.

## 8. Source and evidence ceiling

The supplement uses the same directly checked Score, Hessian, canonical-nudge and normalized-direction interfaces as the original review. Its new byte bindings were checked against those retained source files. The older source theorems remain pointwise/local geometric inputs, not already-proved global ODE statements. The all-start and joint-class results are newly written consequences at this field-specific scope.

Classical analysis supplies the inverse-function, local ODE, phase-line, integration, and barrier arguments. No general novelty claim follows from this review. The criterion specifies an exact mathematical guard test using the initial state's dual orbit; it does not assert a cheap algorithm, a smaller universal memory representation, or a completed semantic-control adapter.

Fresh independent symbolic verification passed 13 named identities, covering both finite coherent-boundary constructions, the exact mixed-family lifetime, its normalized clock, convex negative-Shannon curvature, and the singleton exception. A byte-identical copy of the author's control script also passed all four fixture groups: 32 finite-boundary points, 32 infinite-boundary points, one strict-residual boundary, and 288 entropy-flow points. Its emitted result bytes match the author's retained result file. These are bounded finite controls, not proofs of the analytic universal statements; those were checked by the written arguments above.

The final receipt binds the exact reviewed report, author controls, source bindings, and this supplementary review. The earlier frozen review remains a separate unmodified evidence event.
