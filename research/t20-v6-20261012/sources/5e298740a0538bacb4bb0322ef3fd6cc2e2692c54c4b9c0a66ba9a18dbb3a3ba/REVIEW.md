# Independent review: complete-characteristic finite-rank lifting

Status: ACCEPTED as ordinary mathematical evidence, subject to the exact final-artifact bindings in ACCEPTED_BINDINGS.json. Both the complete two-sided theorem and the forward-complete/lower-killing-bound alternative were independently reviewed. No kernel-proof, integration, or closure approval is supplied.

## Independently checked proof obligations

The repair is mathematically valid under the expressly supplied full hierarchy, square positivity, local uniform finite full-Hankel rank, continuous locally degree-bounded polynomial coefficients, and unique complete two-sided characteristic flow on each finite interval. Completeness is a substantive added assumption, not a consequence of moment tails.

1. Finite GNS reconstruction. Cauchy–Schwarz for L(pq) makes the nullspace N={p:L(p²)=0} an ideal: L(pq)=0 for every q, hence L((xp)²)=L(p·x²p)=0. The finite-dimensional quotient has commuting self-adjoint coordinate multiplication operators. Joint diagonalization and cyclicity of [1] give distinct joint eigenvalues, one-dimensional joint eigenspaces, strictly positive weights, and exactly rank(H) atoms. This establishes actual laws from abstract records; no positivity on arbitrary nonnegative polynomials is silently assumed.

2. Local labels. On a constant-rank neighborhood choose a polynomial basis whose Gram matrix is positive definite. Coordinate multiplication matrices are G^{-1}H_j and are C1 because finitely many moments are C1. A fixed linear coordinate separating the atoms at the center has simple real spectrum throughout a smaller neighborhood. C1 spectral projections give C1 positions by tr(M_j P_i), and the weights are C1 by the invertible finite evaluation system. Coordinatewise C1 is enough; no infinite-dimensional norm differentiability is required.

3. Hermite tests. At a fixed time, let ell_i be a Lagrange polynomial obtained from a separating linear coordinate. The polynomial (x_j-x_ij)ell_i² has value zero at every atom and gradient e_j at atom i, zero gradients elsewhere. Comparing the differentiated atomic moment formula and hierarchy forces x_i'=b_t(x_i). The polynomial [1-2 grad ell_i(x_i)·(x-x_i)]ell_i² has the i-th cardinal value and zero gradients at all atoms; it forces w_i'=(L_t(k_t)-k_t(x_i))w_i. Tests are frozen at the time of comparison, so no derivative of a moving test is inserted into the supplied fixed-polynomial hierarchy.

4. Endpoint survival and noncollision. A finite collection of complete characteristics remains in a compact spatial set over a compact time interval. Polynomial coefficient regularity makes k bounded along these paths and L_t(k_t) continuous. Therefore every initial positive weight has a finite, strictly positive exponential factor at each finite endpoint. Backward uniqueness prohibits collision. Each atom and weight has a finite limit; every polynomial moment of this finite sum converges to that of the endpoint record by the supplied moment continuity. Endpoint rank is exactly the same number of distinct positive atoms.

5. Global rank. Local uniform finite rank gives a finite bound on each compact interval. The integer maximum R is attained. Rank lower semicontinuity follows from continuity of a nonzero finite Gram determinant; thus the rank-R set is relatively open. Any component of that set has no finite interior boundary: item 4 forces rank R at such a boundary, which then has a rank-R neighborhood. Connectedness makes rank constant on the compact interval. Exhaustion handles a connected open time interval. This is stronger than assuming local constancy without proving it and excludes hidden Cantor-time or accumulating rank changes.

6. Unique admitted path. After rank constancy, each atom and weight follows its characteristic/selection ODE from the initial reconstructed law. The explicit normalized weighted pushforward supplies existence, square positivity, and constant finite rank. Uniqueness concerns the admitted full positive finite-rank hierarchy class, not arbitrary infinite-rank distributional solutions or truncated records.

7. Lyapunov sufficiency. A proper C1 spatial V>=1 with |b_t·grad V|<=a(t)V and locally integrable a prevents escape in both time directions by Gronwall. Polynomial b with continuous locally degree-bounded coefficients is locally uniformly Lipschitz in space; bounded trajectories therefore extend. A one-sided inequality gives only its matching direction and must not be advertised as two-sided completeness. The cubic planar rotation b=(-y(x²+y²),x(x²+y²)) preserves V=1+x²+y² and has zero divergence. Affine b=A(t)x+a(t) with continuous coefficients is likewise complete on finite intervals. Polynomial killing can have either sign: along finitely many complete trajectories its finite-time integrals remain finite.

8. Normalized inverse. For F=Phi(t,s) and E(x)=exp(-integral_s^t k_tau(Phi(tau,s)x) d tau), the forward law is F_#(E mu)/mu(E). Its inverse is normalized pullback weighted by 1/E(F^{-1}y). All weights are finite and positive on a finite support. Composition follows from the characteristic and exponential cocycles. This is injectivity of numerical finite laws/full moment records, not preservation of entropy, Fisher metric, conditioning, infinite-horizon recoverability, physical identity, or noetic bearer identity.

## Source convention and boundary contrast

For a non-divergence source equation partial_t mu=-b·grad mu+h mu, the dual reaction is h+div b. Hence killing k corresponds to h=-k-div b. The normalized non-divergence coefficient additionally contains L_t(k). Omitting div b changes the equation.

The damped escape construction in transport-rank-boundary-20261010/RESULT.md has b=x², k=x⁴ and a characteristic escaping at t=1 while its positive weight tends to zero. Its reverse has b=-x², k=-x⁴ and admits inflow from infinity. Neither has complete two-sided characteristics. Smooth full moments, uniform finite rank, tightness, fixed-moment uniform integrability, exponential tails, subcritical cubic-exponential tails, and snapshot determinacy all coexist with those failures. The repair does not reinterpret any of them as completeness.

## Independent exact controls and evidence tier

Run `python nonexplosive-transport-independent-review-20261010/check_independent.py`. The script checks 62 exact identities with SymPy: cubic flow, conserved radius and divergence; an affine flow and polynomial killing integral; the source-divergence correction; normalized inversion; Hermite cardinal/jet polynomials; normalized transport/selection monomials through degree 12; and the forward-only coercive gradient discriminator described below. It writes INDEPENDENT_EXACT_CHECKS.json. These finite tests supplement the general ordinary-mathematical proof obligations above. They do not kernel-check the lifting theorem, GNS argument, spectral regularity, global rank argument, ODE completeness, or inverse theorem. No formal/kernel evidence is asserted.

No original/protected artifact, integration decision, or audit closure is altered by this review.

## Additional sufficient repair: forward completeness plus lower killing bound

This alternative is independently valid on a forward horizon [0,T]: require b to be forward complete through every point at every starting time and k_t(x)>=-C_T globally on each compact horizon. It need not be backward complete.

Define the unnormalized functional A_t=exp(-integral_0^t L_u(k_u)du)L_t. Since the coefficients of k have a common finite degree bound and are continuous, L_t(k_t) is a finite sum of continuous functions and is continuous. The scalar multiplier is therefore strictly positive, bounded and bounded away from zero on [0,T]. Every A_t(p) is C1; A_t remains square-positive with the same finite rank, and A_t'=A_t(b·grad p-kp). In particular A_t(|x|²) is nonnegative, continuous and bounded on [0,T].

On a maximal-rank component take an interior time s and write its unnormalized atom masses c_j. For t<=s within the component,

    c_j(t)=c_j(s) exp(integral_t^s k_u(X_j(u))du)
           >= c_j(s) exp(-C_T(s-t)) > 0.

Thus c_j(t)|X_j(t)|²<=A_t(|x|²) gives a uniform bound on each atom position as the left component endpoint is approached. This is control of individual positions from a positive lower mass bound, not an inference from mere tightness. Uniformly bounded positions make b and k uniformly bounded along these curves. The bounded velocity gives a finite endpoint position. Local ODE extension applies there; finite integrated k yields a positive endpoint mass. Endpoint collisions would contradict local ODE uniqueness backwards and then uniqueness up to s. Moment continuity identifies exactly these distinct positive atoms at the endpoint, with the same maximal rank. At a right endpoint forward completeness supplies the identical continuation argument directly. Hence maximal rank fills [0,T], and the same actual-law formula and admitted-path uniqueness follow forward from time zero.

For an autonomous coercive polynomial F, b=-grad F is forward complete: dF(X)/dt=-|grad F(X)|²<=0 keeps every trajectory in a compact sublevel set. Coercivity also makes k=F bounded below. This does not assume time-varying coercive F automatically has the same energy inequality.

Unlike the two-sided theorem, this alternative gives injectivity and an inverse only on the propagated image. The flow need not be onto all spatial points, so its finite-law transform need not be onto all finite laws. For example F(x)=x⁴/4, b=-x³ gives Phi(t,0)x=x/sqrt(1+2tx²). For t>0 its image is the proper interval (-1/sqrt(2t),1/sqrt(2t)); a point mass outside cannot be reached. The killing integral is x²[1-(1+2tx²)^{-1}]/8. The independent script additionally checks four exact gradient-flow identities, raising the total to 62.

## Final author-text review

The complete final author theorem and its added §9 were read directly. The two-sided result uses local annihilating-polynomial root charts rather than the equivalent spectral chart route checked above; its positive definite projected Gram matrix guarantees r distinct projected nodes locally, so the construction is sound. The explicit signed radial-rotation example and time-dependent affine example were checked against the stated equations. No mathematical correction remains requested. Final acceptance is byte-specific and ordinary evidence only.
