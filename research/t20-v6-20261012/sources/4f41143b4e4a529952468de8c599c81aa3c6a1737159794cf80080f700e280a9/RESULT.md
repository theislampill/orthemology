# Polynomial-coordinate transport of represented moment continuation

10 October 2026 UTC. Additive T20 mathematical continuation. This is a conditional corollary of accepted Theorem V, extending the accepted affine-characteristic argument. The inherited fixed polynomial-coordinate transfer is credited rather than counted again. No field-priority or physical/noetic applicability claim is made.

## Question and increment

The existing affine result explicitly leaves general nonlinear transport open: an inverse characteristic map need not preserve polynomials and trajectories can escape. There is a genuine intermediate class where those obstructions can be discharged: supplied polynomial automorphism paths with controlled degrees. This note derives that class and gives a time-dependent triangular example outside the earlier affine theorem. It also proves that the resulting *joint* moment record can be determinate although a standard coordinatewise Carleman sufficient test fails. Failure of that test is not failure of representation or identity.

## Hypotheses

On each compact time window [0,H], let Phi_t and Psi_t be mutually inverse polynomial maps of R^d, with Phi_0=id. Their coefficients are C1 functions of t, and both maps have common finite degree bounds on the window. Set v_t=(partial_t Phi_t) composed with Psi_t. Let h_t be polynomials with continuous coefficients and a common finite degree bound. Assume the pulled-back polynomials k_t=h_t composed with Phi_t satisfy Theorem V: there are c>0 and C such that k_t+C-c|y|^2 is SOS throughout the window. The constants can depend on H. The complete path, not merely local existence of an arbitrary vector-field flow, is supplied.

Let L_t be normalized linear functionals on all real polynomials, square-positive at every t, coordinatewise C1 through t=0, satisfying

L_t'(p)=L_t(v_t dot grad p)-L_t(h_t p)+L_t(h_t)L_t(p).

These are strong hypotheses on an abstract full moment hierarchy; no initial representing law is assumed.

## Derivation

For a fixed polynomial q, define M_t(q)=L_t(q composed with Psi_t). Its argument has bounded degree and C1 coefficients, so differentiation is a finite sum of the known coordinate derivatives and coefficient derivatives. Differentiating Psi_t(Phi_t(y))=y gives

partial_t(q composed with Psi_t)+v_t dot grad(q composed with Psi_t)=0.

Consequently M_t is normalized, square-positive and satisfies the killing-only hierarchy with k_t. Theorem V yields one uniquely determined initial probability mu with all polynomial moments, and

L_t(p) = integral p(Phi_t(y)) exp(-integral_0^t k_s(y) ds) dmu(y)
         / integral exp(-integral_0^t k_s(y) ds) dmu(y).

The converse follows by differentiation under the integral. On every compact window the polynomial compositions, their time derivatives and the killing terms are bounded by a fixed polynomial in |y|, while the exponential is at most exp(CH). The initial law has every polynomial moment, providing an integrable dominating function. The denominator is strictly positive.

Every positive-time *joint* moment record is determinate. Indeed, any alternative probability representative of L_t pushes back by the polynomial Psi_t to a representative of M_t: every monomial after composition is still a polynomial, and its absolute integrability follows from the available even moments. V's determinacy identifies the pulled-back measures; pushing forward gives equality. This argument does not require Carleman growth in the original coordinates.

Thus initial representing laws parameterize the full paths, and positive-time continuation is unique along a supplied future (Phi,h) pair. This is a coordinate-covariant conditional representation result, not a theorem for all polynomial vector fields. A polynomial vector field may have a nonpolynomial inverse flow or finite-time escape.

## Explicit nonlinear time-dependent instance

In two dimensions take an integer m>=3 and

Phi_t(u,z)=(u,z+t*u^m),   Psi_t(x,y)=(x,y-t*x^m),
v_t(x,y)=(0,x^m),        h_t(x,y)=x^2+(y-t*x^m)^2.

Then k_t=u^2+z^2. The pulled-back radial certificate is exact. Each h_t is coercive, but at a fixed t>0, along y=t*x^m its ratio to x^2+y^2 tends to zero as |x| grows. Thus no h_t+C-c(x^2+y^2) SOS certificate with c>0 is possible: its value eventually becomes negative along that curve. The original-coordinate V hypothesis really fails; the new pathwise coordinate transfer supplies what is missing. The velocity is genuinely nonlinear and global, and the inverse is an explicit polynomial, not an assumed characteristic map.

## Determinacy despite failure of a coordinate Carleman test

Choose initial law with density pi^-1 exp(-u^2-z^2). At positive t the pulled-back tilted law has independent centred Gaussian U,Z of variance sigma_t^2=1/[2(1+t)]. The represented original coordinates are X=U, Y=Z+t U^m. Their joint law is determinate by the preceding proof.

For n>=1, expanding E[Y^(2n)] shows every nonzero summand is nonnegative: odd powers of centred Z vanish, and the remaining powers of U are even. Hence

E[Y^(2n)] >= t^(2n) E[U^(2mn)]
            = t^(2n) sigma_t^(2mn) (2mn-1)!!.

Since (2r-1)!! >= r! and r! >= (r/e)^r (the latter follows by comparing the sum of log j with its integral),

(E[Y^(2n)])^(-1/(2n)) <= t^-1 sigma_t^-m (e/(mn))^(m/2).

The Carleman sum for this coordinate therefore converges when m>2. This demonstrates failure of that *sufficient coordinate test*, not marginal indeterminacy. It neither asserts nor needs an indeterminate Y marginal. The full joint measure remains determinate because the invertible polynomial relationship exposes the Gaussian coordinates.

## Evidence and limits

The derivation is ordinary written mathematics, not Lean-checked. Exact symbolic controls supplement rather than establish the universal proof. The inherited V proof and fixed-coordinate result supply the stated dependencies. No measurement, human warrant, numerical oracle for infinite moments, or philosophical bearer identity is inferred. This is a modest extension of an existing transfer, not a replacement for the stronger autonomous coercive theorem G or a diffusion theorem.
