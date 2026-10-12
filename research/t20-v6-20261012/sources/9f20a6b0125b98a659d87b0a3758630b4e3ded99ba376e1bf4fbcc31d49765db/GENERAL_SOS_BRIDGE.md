# Separate extension: SOS energies in the same controlled subspace

10 October 2026 UTC. This is an explicit extension of the quadratic result, not an application of its quadratic remainder estimate to higher-degree terms. The parent proposed the signed-projection route. The partial Gaussian bounds and compact Fourier/integrating-factor mechanism are inherited from the cumulative result; the present argument applies them to uniquely determined signed measures on the controlled space even when the joint representing law is indeterminate.

## G1. Exact statement

Write x=(z,y)∈R^r×R, r≥1. Let g_t(z) be real SOS polynomials that depend only on z, with coefficients continuous in t and a common finite degree bound on every compact time window. Assume that for every t>0,

    K_t(z)=∫₀ᵗg_u(z)du,
    K_t−c(t)|z|² is SOS for some c(t)>0.             (G)

Let L_t be a normalized full-square-positive polynomial hierarchy, with monomial coordinates C¹ through zero, satisfying L_t′(p)=−L_t(g_t p)+L_t(g_t)L_t(p).

Then all conclusions in RESULT.md hold: a whole-path lift exists; every positive-time representative deweights to a lift; representative fibres and lift fibres are in bijection; equality of one positive-time full moment record is equivalent to equality of all finite signed measures π_z*(y^jμ); and moment-coordinate continuation along a supplied continuing schedule in this same controlled subspace is unique. The conditional-determinacy sufficient criterion and ambiguous independent-hidden-law examples apply unchanged.

No instantaneous bound g_t≤C|z|² is asserted. A scalar shift depending only on time can be added or removed because it cancels from the normalized hierarchy; the SOS and cumulative certificate are imposed after that shift, on the shifted energy. This does not include a shift depending on y.

## G2. Algebraic bounds and existence before any law-level dynamics

Unnormalize as before:

    a(t)=exp(−∫₀ᵗL_u(g_u)du),  A_t=a(t)L_t,
    A_t′(p)=−A_t(g_t p),  0<a(t)≤1.                 (22)

The cumulative predecessor's finite backward Volterra identity and its nonnegative remainder use only SOS multiplication, finite-dimensional polynomial spaces at each expansion order, and coefficient continuity. They apply without a quadratic restriction. With R=|z|², condition (G) therefore gives

    ∑_(n=0)^N c(t)^n A_t(q²R^n)/n!≤A₀(q²)         (23)

for all q,N. The r controlled marginal Carleman conditions and the d−1-marginal existence theorem give a joint representative at every t>0. For any such finite representative ν_t of A_t, monotone convergence yields

    ∫q²e^(c(t)R)dν_t≤A₀(q²).                       (24)

As in the quadratic proof, A_t(q²R^n) decreases in t because q²R^ng_t is SOS. Consequently for each interior window J=[η,H] and c=c(η)>0,

    ∫q²e^(cR)dν_t≤A₀(q²),   t∈J,                 (25)

for every representative ν_t. This estimate precedes any identification of law-level dynamics.

## G3. Canonical signed projections despite noncanonical joint laws

For j≥0 and any representative ν_t, set

    σ_(t,j)=π_z*(y^jν_t).

This is a finite signed measure on R^r. The variation inequality for weighted pushforwards and |y|^j≤(1+y^(2j))/2 imply

    ∫e^(cR)d|σ_(t,j)|
      ≤∫|y|^j e^(cR)dν_t
      ≤M_j:=[A₀(1)+A₀(y^(2j))]/2,   t∈J.          (26)

Its z-polynomial moments are exactly A_t(z^αy^j), independent of the chosen joint representative. The Gaussian bound makes these signed moments determinate by the elementary Fourier Taylor argument in RESULT.md, Section 5. Thus σ_(t,j) itself is independent of the choice of ν_t. We have a canonical signed measure for each (t,j), without having to choose a measurable family of joint representatives.

For even j, σ_(t,j) is positive. In particular σ_(t,0) has total mass a(t). Equation (26) also implies, for every integer n≥0,

    ∫|z|^(2n)d|σ_(t,j)|≤M_j n!c^(−n),
    ∫|z|^n d|σ_(t,j)|≤M_j√(n!)c^(−n/2).           (27)

The second follows by Cauchy–Schwarz for the positive measure |σ|, using |σ|(R^r)≤M_j. If M_j=0 the measure is zero and all formulas remain valid.

## G4. Fourier identification is used only on the controlled space

Fix j and ξ∈R^r. Let

    P_N(z)=∑_(k=0)^N(iξ·z)^k/k!,
    F_(t,j)(ξ)=∫e^(iξ·z)dσ_(t,j),
    G_(t,j)(ξ)=∫g_t(z)e^(iξ·z)dσ_(t,j).

The full polynomial hierarchy gives

    dA_t(y^jP_N)/dt=−A_t(y^jg_tP_N).               (28)

On J, there are finite B and integer D with |g_t(z)|≤B(1+|z|^D). For n=N+1, the real Taylor remainder of e^(iv) is bounded by |v|^n/n!. Equation (27) therefore bounds the function-side error uniformly by

    M_j |ξ|^n√(n!)c^(−n/2)/n!,

and the derivative-side error uniformly by

    B M_j |ξ|^n/n! [√(n!)c^(−n/2)
                      +√((n+D)!)c^(−(n+D)/2)].    (29)

Both tend to zero, also uniformly for ξ in any compact set. The ratio of consecutive terms in the second factorial sequence is (|ξ|/√c)√(n+D+1)/(n+1), which tends to zero. Polynomial coefficients and coordinates are continuous, so the finite approximants and their derivatives are continuous in t. Uniform convergence therefore proves

    ∂_tF_(t,j)(ξ)=−G_(t,j)(ξ),                    (30)

with both sides jointly continuous in t and ξ.

For the Fourier inversion step, use frequency-independent bounds rather than integrating the ξ-dependent Taylor estimate:

    |F_(t,j)(ξ)|≤M_j,
    |G_(t,j)(ξ)|≤B M_j[1+√(D!)c^(−D/2)].           (31)

For any φ∈C_c^∞(R^r), its Fourier transform is integrable. Fourier inversion, Fubini, and dominated differentiation using (30)–(31) give

    d/dt ∫φ dσ_(t,j)=−∫g_tφ dσ_(t,j).             (32)

The right side is continuous by the same Fourier formula and domination. This is a weak evolution equation for each canonical signed projection. No Fourier uniqueness or exponential integrability on the full (z,y) space is invoked.

## G5. Signed integrating factors

Fix 0<s<t<T. For φ∈C_c^∞(R^r), define

    ψ_u(z)=φ(z)exp(K_(s,u)(z)),   s≤u≤t.

Its spatial support is fixed and compact. Coefficient continuity makes it C¹ in u in the uniform norm, with ∂_uψ_u=g_uψ_u; all spatial functions involved are compact smooth tests. The difference-quotient product rule applied to (32) gives

    d/du∫ψ_u dσ_(u,j)
      =∫(∂_uψ_u−g_uψ_u)dσ_(u,j)=0.

For clarity, this product rule needs only the uniform total-variation bound (26), uniform differentiability of ψ, and continuity of σ_(u,j) against the frozen compact test ∂_uψ_u, already supplied by (32). It does not assume measure-valued differentiability.

Hence

    ∫φ e^(K_(s,t))dσ_(t,j)=∫φ dσ_(s,j).

Compact smooth tests determine locally finite signed measures, so

    σ_(s,j)=e^(K_(s,t))σ_(t,j),
    σ_(t,j)=e^(−K_(s,t))σ_(s,j).                  (33)

The inverse-weighted signed measure is initially locally finite. Equality on all compacts identifies it with the finite measure on the left and proves its global finite total variation. This finiteness is not inferred from a formal inverse moment transformation. For even j both measures are positive.

## G6. Reconstructing the joint lift from one representative

Fix s>0 and any positive finite representative ν_s of A_s. For any u>0 define the positive Borel measure

    ν_u=e^(K_s−K_u)ν_s.                            (34)

Equation (33) with j=0 shows its total mass is a(u)<∞. For every pair of nonnegative integers m,n, the positive even-j measure identity gives

    ∫R(z)^m y^(2n)dν_u
      =∫R(z)^m e^(K_s−K_u)dσ_(s,2n)
      =∫R(z)^m dσ_(u,2n)
      =A_u(R^m y^(2n))<∞.                         (35)

Equality follows first on bounded regions and then by monotone convergence. These squared-monomial integrals imply every polynomial has finite absolute and squared moments under ν_u. For example a monomial z^αy^j has square at most R^|α| y^(2j), and a finite sum is controlled by the sum of its squared monomials.

For signed mixed moments we may now use (33), with integrability already established by (35):

    ∫z^αy^j dν_u
      =∫z^α e^(K_s−K_u)dσ_(s,j)
      =∫z^α dσ_(u,j)
      =A_u(z^αy^j).                               (36)

Thus ν_u is a representative of A_u for every u>0. A single arbitrary joint representative has been propagated consistently across all positive times; arbitrary unrelated representatives were never identified with one another.

For u↓0, e^(K_s−K_u) increases pointwise to e^(K_s) because g_t≥0. Equations (35)–(36) give ∫q²dν_u=A_u(q²) for every polynomial q. Boundary continuity and monotone convergence therefore yield

    μ=e^(K_s)ν_s,  μ(1)=1,  ∫q²dμ=A₀(q²).

As before this is a P∞ law and ν_u=e^(−K_u)μ, giving the whole-path lift. The normalizer ODE gives the fibre bijection. The converse uses local coefficient bounds and e^(−K_t)≤1 to differentiate polynomially dominated moments.

The proof of the exact equivalence (E) in RESULT.md uses only K_s≥c(s)R and the fact that the energy depends on z alone, so it applies unchanged. The continuation and conditional uniqueness conclusions follow for the same reason. No claim for arbitrary hidden dimension without joint representability at all positive times is inferred here.

## G7. A higher-degree discriminator and the limit of the quadratic proof

In controlled dimension one, with one hidden coordinate, take

    g_t(z)=z⁴+t²z²,  t≥0.

This is SOS, and K_t=t z⁴+(t³/3)z² has K_t−(t³/3)z²=t z⁴ SOS for every t>0. No finite C can bound g_t≤Cz² on all z. Thus the quadratic geometric-remainder proof does not apply, while the signed-projection argument proves automatic whole-path lifting and the same exact identification relation.

This extension retains a fixed controlled subspace and an SOS energy independent of the hidden coordinate. It does not infer a theorem for cross-hidden terms, general generators that preserve squares, only-terminal cumulative coercivity, or finite moment truncations.
