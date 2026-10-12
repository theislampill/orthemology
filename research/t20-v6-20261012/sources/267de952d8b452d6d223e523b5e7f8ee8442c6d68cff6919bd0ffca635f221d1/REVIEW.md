# Independent review: one positive-time joint law under partial cumulative SOS damping

10 October 2026 UTC. Ordinary mathematical review, scoped to the frozen candidate below. No protected edit, integration, audit-governance disposition, proof-kernel certification, novelty determination, or closure claim is made.

## Result

**No mathematical gap found in the stated one-positive-time-representative implication, its fibre bijection, or its representable-segment continuation consequence.** The construction genuinely avoids assuming joint representing measures at all positive times. The controlled-space square-weighted functionals are the correct intermediate objects. The proof remains valid for every finite hidden dimension.

The verdict is bounded to the supplied hypotheses: a fixed controlled subspace, continuous polynomial coefficients and locally common finite degree bounds including time zero, SOS energies independent of the hidden variables, the cumulative radial SOS certificate at every positive time, and the full square-positive coordinatewise-C1 hierarchy. It does not establish automatic joint representability when at least two variables are hidden, does not establish a lift from initial representability alone, and does not cover a sole terminal-time certificate.

## Frozen bindings and evidence inspected

Primary object:

- `partial-cumulative-law-persistence-20261010/RESULT.md`
- SHA-256: `cf9b6626b24329f8dd27d2ff2d78027ea4e222f45a6b7621209aa4d39b840fe3`

Supporting proof dependencies inspected:

- `partial-cumulative-one-hidden-lift-20261010/GENERAL_SOS_BRIDGE.md`, SHA-256 `9f20a6b0125b98a659d87b0a3758630b4e3ded99ba376e1bf4fbcc31d49765db`. In particular, G4's explicit function/derivative Taylor bounds and G5's compact-test product rule.
- `cumulative-square-positivity-20261010/RESULT.md`, SHA-256 `a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f`. In particular, the finite backward Volterra identity, sign of its remainder, and radial SOS comparison.
- `partial-cumulative-one-hidden-lift-20261010/RESULT.md`, SHA-256 `047ec278a738cdc018b7118113afa93a8fa6d0aa1a315d33440f2aa0586a53ea`. Sections 5–6 supply the normalized-record comparison and continuation pattern checked below.
- `partial-quadratic-rank-classification-20261010/RESULT.md`, SHA-256 `d940d080eea86c0486e81219898c343c4e4c025f86e00cda209df3a3266a3288`. Inspected for the already known one-time-law implication and distinction between nonmoment records and nonunique laws; no independent certification of its imported infinite nonmoment functional is claimed here.
- The version-specific [Putinar–Schmüdgen primary source, Theorem 25 and following paragraph, printed page 24](https://arxiv.org/pdf/0810.0840v1), checked against the local PDF SHA-256 `9e551b5856cdf1065f1170641bed91a1d0f40c1d19368c9187f0c3d16661ac94` and its retained page text. It applies directly to a positive semidefinite multisequence, with no prior multivariate representing law. All marginal Carleman conditions give existence and determinacy. In one controlled dimension, use Hamburger existence followed by scalar Carleman determinacy.

The candidate was hash-checked before inspection and again by the executed controls. Any modification requires a fresh currentness check and review of the change.

## Claim-by-claim adversarial checks

### 1. The inherited partial estimate does not presuppose a law

For a fixed finite expansion order, local degree bounds put every integrand in a finite-dimensional polynomial space. Coefficient continuity and coordinate continuity therefore justify repeated integration and Fubini. The backward remainder is nonnegative on q² because it applies A at the latest simplex time to q² times a product of SOS polynomials. The factor 1/n! comes from commuting scalar polynomial factors and simplex symmetrization, not from any matrix commutativity.

The assumption K_t−cR SOS implies K_t SOS and makes K_t^n−c^nR^n SOS by factorization. This proves the finite partial-sum inequality algebraically. Since q²R^n g_t is SOS, each A_t(q²R^n) is nonincreasing. Hence the same coefficient c=c(eta) and bound A_0(q²) work throughout [eta,H]. No regularity of the chosen c(t) or of SOS decompositions is needed.

### 2. Zero-mass and normalized controlled-space moment problems

Fix b and write m=A_t(b²). The controlled functional lambda(f)=A_t(f b²) is positive on squares because lambda(f²)=A_t((fb)²). If m=0, its own Cauchy–Schwarz inequality gives

    |lambda(f)|² <= lambda(1) lambda(f²) = 0.

Thus it is the zero functional, and its only positive representative is the zero measure. There is no normalization by zero.

If m>0, write M=A_0(b²), necessarily M>=m>0. The normalized i-th even controlled moment is at most

    (M/m) n! c^(-n).

For a nonzero such moment, its inverse 2n-th root is at least

    (m/M)^(1/(2n)) sqrt(c)/sqrt(n)
      >= sqrt(m/M) sqrt(c)/sqrt(n).

The divergent series proves every controlled Carleman condition after normalization. Zero moments contribute infinity. The classical theorem therefore supplies tau_t^b without constructing any joint law. Scaling its normalized representative back by m preserves all identities. Applying monotone convergence to the *whole partial-sum bound*, rather than only separate factorial estimates, gives the claimed bound at the full exponent c:

    integral exp(cR) d tau_t^b <= A_0(b²).

The distinction matters: separate factorial estimates alone would not justify this bound at the endpoint exponent. The candidate uses the stronger partial-sum estimate correctly.

### 3. Polarization, uniqueness, linearity, and hidden-square positivity

The signed measure obtained from tau^(h+1) and tau^(h−1) has the required moments. More explicitly, its uniform variation bound is

    integral exp(cR) d|sigma_t,h|
      <= [A_0((h+1)²)+A_0((h−1)²)]/4
      = [A_0(h²)+1]/2 =: M_h.

For any finite signed measure with this bound, every exp(a|z|) is variation-integrable, since a|z| <= c|z|² + a²/(4c). Fourier Taylor series may therefore be integrated termwise. Equal polynomial moments imply equal Fourier transforms, then equal finite signed measures.

Finite linear combinations of these measures retain a Gaussian variation bound. Comparing moments therefore proves sigma_(lambda h+mu j)=lambda sigma_h+mu sigma_j. Comparing sigma_(b²) to tau^b proves equality and positivity. This does not require, imply, or secretly select hidden conditional measures. In particular, it is not an attempted solution of a multivariate hidden moment problem.

### 4. Derivative control genuinely survives arbitrary hidden degree

For fixed h, the bound M_h is finite and uniform in time on the interior window. It gives, for every integer n>=0,

    integral |z|^n d|sigma_t,h| <= M_h sqrt(n!) c^(-n/2).

Local coefficient and degree bounds give |g_t(z)|<=B(1+|z|^D). If n=N+1, the controlled Fourier derivative-approximation error is at most

    B M_h |xi|^n/n!
      [sqrt(n!) c^(-n/2) + sqrt((n+D)!) c^(-(n+D)/2)].

The second sequence has successive ratio (|xi|/sqrt(c)) sqrt(n+D+1)/(n+1), tending to zero. The first is the same argument with D=0. This proves convergence uniformly on compact time/frequency sets, even for arbitrarily high but locally bounded polynomial degree D. It does not use the invalid higher-degree estimate g_t<=CR.

The finite approximants are C1 in t by the given hierarchy; their derivatives are continuous using only coefficients of g and moment coordinates. No time derivative of g is taken. Uniform derivative convergence establishes the Fourier evolution. For Fourier inversion, the correct independent-of-frequency bound is

    |G_t,h(xi)| <= B M_h [1+sqrt(D!) c^(-D/2)].

Together with integrability of the Fourier transform of a compact smooth test, this justifies differentiation under Fourier inversion. There is no requirement to integrate the frequency-dependent Taylor estimate over all frequencies, and no prior measurability assumption on a family of joint laws.

### 5. Compact integrating factors and global variation after inverse weighting

The time-dependent compact test phi exp(K_u−K_s) is uniformly C1 on its fixed support. The product rule follows by splitting the difference quotient, using uniform total variation and continuity against the frozen compact test. Thus local signed-measure equality is established first.

Let W=exp(K_s−K_u), a strictly positive continuous function. Even if W is unbounded, W sigma_s,h initially makes sense as a locally finite signed Radon measure. On every compact set its variation is W|sigma_s,h|. Equality on compact smooth tests identifies that local measure with sigma_u,h. Therefore, on an increasing compact exhaustion C_j,

    integral_C_j W d|sigma_s,h| = |sigma_u,h|(C_j).

Monotone convergence proves integral W d|sigma_s,h|=|sigma_u,h|(R^r)<infinity. This closes the potential global-variation gap; it is not a formal inverse of a moment transformation. Both time orderings are covered.

### 6. One joint law: integrability precedes signed mixed integration

The starting law nu_s has weighted Gaussian moments for h² and for 1 from the algebraic partial-sum bound. The pushforward of h nu_s consequently has Gaussian variation control by |h|<=(1+h²)/2. Its moments agree with sigma_s,h, so signed uniqueness identifies them.

Define the positive measure nu_u=W nu_s. The h=1 identity proves its finite mass. For each hidden multi-index beta, the positive projected measure for y^(2 beta) is sigma_s,y^(2 beta). Positive weighted pushforward and monotone convergence give

    integral R^m y^(2 beta) d nu_u
      = integral R^m d sigma_u,y^(2 beta) < infinity.

No cancellation is used here. Since |z^alpha|²<=R^|alpha|, these even mixed moments imply absolute and squared integrability of every joint polynomial. Only then is it legitimate to weight the signed pushforward for y^beta and recover the signed mixed moments. This order is essential and is observed by the candidate.

A finite signed projection can be zero despite nonzero hidden absolute moments, so signed-projection finiteness alone would be insufficient. The candidate avoids exactly that error by retaining the positive hidden-square projections.

### 7. Time zero and exact representative/lift bijections

For u decreasing to zero below s, W increases pointwise to exp(K_s) because g is pointwise nonnegative. The established identities for q² and continuity through zero give

    integral q² exp(K_s) d nu_s = A_0(q²).

The case q=1 fixes mass one, and |p|<=(1+p²)/2 supplies all absolute moments. Polarization supplies the signed initial moments. This excludes mass loss, an infinite initial law, and an omitted zero-time coordinate.

For any whole-path lift mu, its normalizer Z solves Z'=-L_t(g_t)Z with Z(0)=1, hence Z=a. Consequently tilting at s and deweighting by a(s) exp(K_s) are exact inverses. Every positive-time representative is covered, not only a selected one. A representative at one positive time therefore implies representatives at all positive times; absence at any one positive time excludes all of them along this specified path.

### 8. Equality of normalized records and the precise continuation claim

For two actual all-moments probability laws, equality of their normalized full records at s>0 determines the Gaussian-controlled signed projections of every hidden monomial at s. Removing the common positive weight gives the original signed projections divided by their respective normalizers. The beta=0 identity, followed by taking total masses, proves the two normalizers equal. Thus the unnormalized original signed projections coincide exactly. Conversely, equality of all original signed projections determines every mixed polynomial moment after any supplied controlled-variable SOS weighting.

For a path on [0,T) having a positive-time representative, each lift supplies an extension along a specified continuing SOS schedule in the same controlled variables. Polynomial domination gives its C1 regularity through all finite times. All lifts have the same signed projections, hence the same extended coordinates. Any competing admissible extension contains a positive-time representative in the original interval, so the theorem now under review applies to that entire extended path. Its lift restricts to a lift of the original path and must give the same extension. This proves uniqueness in the full admissible extension class, even when the hidden dimension is at least two.

This argument does not classify continuations of a nonmoment initial segment, choose an unspecified future schedule, or justify changing the controlled subspace. Those stronger claims would not follow and are not made.

## Supporting exact controls

Executed `python review-joint-law-persistence-20261010/check_controls.py` with SymPy 1.14.0: **24 controls passed, 0 failed**. The machine-readable names and frozen source bindings are in `CONTROL_RESULTS.json`.

The controls cover source currentness, the polarization and variation constants, a genuinely higher-degree cumulative schedule and its integrating factor, the exact factorial-error ratio, an explicit three-atom two-hidden-variable normalized hierarchy, the fibre inverse, a zero-mass hidden-square case, a signed-cancellation discriminator, and a mixed-monomial radial majorant. They are finite symbolic controls of relevant identities and failure modes. They do not establish Carleman existence, Fourier uniqueness, or the universal theorem by sampling. Those are addressed by the ordinary arguments above and the precisely scoped classical input.

## Optional editorial hardening

No theorem-changing repair is required. For a standalone statement, explicitly declare the time domain [0,T), define "continuous schedule" as coefficient continuity with common degree bounds on every [0,H], and mention Hamburger plus scalar Carleman for r=1. Displaying M_h and the compact-exhaustion variation equality would make the two least-obvious bridges easier to audit without consulting G4–G5. These are clarification opportunities, not identified mathematical defects.
