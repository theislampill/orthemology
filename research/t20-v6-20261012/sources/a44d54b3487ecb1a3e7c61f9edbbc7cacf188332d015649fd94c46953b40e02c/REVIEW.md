# Independent review: Gaussian induced correction geometry

## Status and scope

ACCEPTED within the mathematical scope below. Independent derivation and final frozen-author replay completed. Exact author-file and review-file binding is recorded in `review_receipt.json`. The reviewed author RESULT.md has SHA256 67577bc185c3190cbf131993fdfdd36aa67c605435fd225eb6f29b2cc6c21efa. This report concerns a mathematical probability-density model with unit-cost Euclidean transport and centered reaction. It does not identify this metric empirically with noetic phenomena, assert a global finite sufficient statistic for all laws, or grant project/audit closure.

The full-density induced Riemannian metric and its Gaussian quadratic-flow corollaries pass the mathematical review below. The accompanying independent script has 25 passing algebra checks. Fresh execution of the frozen author verifier also passed 166 exact/integrity assertions, including the nine original-input comparisons. Those checks supplement, and do not replace, the functional-domain proof.

## 1. Full-density tangent minimization

Fix the Gaussian probability density rho = N(m,v), v > 0, on the real line and write y = x-m. Work in the real Hilbert control space

H = L²(rho) × L²₀(rho),

with squared norm E_rho[u²+alpha²]. Here L²₀ means zero mean. Define the control operator distributionally by

A_rho(u,alpha) = -∂x(rho u) + rho alpha,

so its action against every smooth compactly supported test h is E_rho[u h′ + alpha h]. The induced squared norm of a prescribed signed density tangent sigma is the infimum over all controls in H with A_rho(u,alpha) = sigma in distributions.

A Gaussian parameter tangent (p,q) = (m-dot,v-dot) has the exact density ratio

sigma/rho = p y/v + q(y²-v)/(2v²).

Set

a = p/(1+v),   b = q/[2v(v+2)],
f = a y + b(y²-v).

Its centered control pair is (u*,alpha*) = (f′,f), since E_rho[f]=0. Direct differentiation gives

A_rho(f′,f)/rho = a(1+1/v)y + b(1+2/v)(y²-v),

which is exactly the specified Gaussian density tangent. This is density equality, not merely equality of two moments.

For any competing finite-action control pair, write its difference from (f′,f) as (U,B). Then A_rho(U,B)=0 distributionally. Choose smooth compact cutoffs chi_R equal to one on |y|≤R, zero on |y|≥2R, with derivative bounded by C/R. The tests h_R = chi_R f satisfy

h_R → f and h_R′ → f′ in L²(rho).

The cutoff-derivative term tends to zero because every polynomial has finite Gaussian moments; for example its square is bounded by C²R⁻² E[f² 1_{|y|>R}]. Distributional kernel equality tested against h_R and Cauchy–Schwarz therefore give

E_rho[U f′ + B f] = 0.

Consequently the exact Pythagorean identity is

E_rho[u²+alpha²] = E_rho[(f′)²+f²] + E_rho[U²+B²].

This proves attainment, uniqueness up to rho-null sets, and minimality against every finite-action decomposition of the full density tangent. No differentiability or pointwise flux-decay hypothesis on arbitrary competing controls is being smuggled into the proof. Distributional equality and L² control integrability suffice. Gaussian tails explicitly justify the noncompact test limit.

Gaussian moment evaluation yields

E_rho[(f′)²+f²] = a²(1+v)+2b²v(v+2),

hence the metric is

g = dm²/(1+v) + dv²/[2v(v+2)].

## 2. Channel separation and the inherited metric

The transport-only Gaussian metric is diag(1,1/(4v)), with cometric diag(1,4v). The centered-reaction-only metric is diag(1/v,1/(2v²)), with cometric diag(v,2v²). Both channels can move both Gaussian coordinates. Their cometrics add to diag(1+v,2v(v+2)); their metrics do not add.

In general an inversion of a matrix of moment responses would establish only a relaxed moment problem, or require further justification that restriction and minimization commute. Section 1 supplies that missing justification here: its quadratic potential produces the exact full Gaussian tangent and is orthogonal to the entire distributional control kernel, including non-Gaussian decompositions.

## 3. Energy gradient and exact Gaussian dynamics

For F(x)=x²/2, the energy is E(m,v)=(m²+v)/2. Its negative gradient under the metric above is

m′=-(1+v)m,   v′=-v(v+2).

Let D(t)=1+v0(1-e^(-2t))/2. The exact solution is

m(t)=m0 e^(-t)/D(t),   v(t)=v0 e^(-2t)/D(t).

The original transport characteristics are x(t)=e^(-t)x0. The unnormalized reaction weight along them is exp[-(1-e^(-2t))x0²/4]. Tilting the initial Gaussian by this weight and pushing forward by the characteristic gives precisely the displayed mean and variance. This provides an independent full-density realization; it is not an ansatz justified only by the first two moments.

For the general quadratic F(x)=k x²/2 + ell x + c, the exact tangent field is

m′=-(1+v)(k m+ell),   v′=-k v(v+2).

It is locally Gaussian-invariant while the positive-variance solution exists. For k>0 it exists at every forward finite time, including all nonnegative coercive quadratics. For k=0 it has constant variance and linearly moving mean. For k<0, the variance diverges at

T = log(1+2/v0)/(2|k|),

the same time at which the weighted Gaussian normalization loses integrability. Therefore a statement of unrestricted global invariance for every quadratic, including concave ones, would be false. Additive constants in F do not affect the normalized vector field.

For any nonconstant polynomial F of degree n with highest coefficient c_n, the ambient negative-gradient density ratio is

F″-(x-m)F′/v-F+E_rho F.

Its degree-n coefficient is -(1+n/v)c_n, which cannot vanish when v>0. The Gaussian tangent ratios are exactly the centered polynomials of degree at most two. Thus polynomial ambient negative gradients are Gaussian-tangent if and only if the polynomial has degree at most two (with constants giving zero). For higher-degree energies the restricted Gaussian gradient remains well-defined, but it is not the full ambient density vector field. Indeed Stein identities can make the first two instantaneous moments agree despite the extra higher-degree density components; this is why moment agreement alone is insufficient.

## 4. Optional Riemannian geometry

The change r = arcosh(v+1)/sqrt(2), with r>0, yields

g = dr² + sech(sqrt(2)r) dm².

Writing the warped coefficient as w(r)² with w=sech(sqrt(2)r)^(1/2), direct calculation gives Gaussian curvature

K = -w″/w = (3/2)sech²(sqrt(2)r)-1/2.

The metric is not a Hessian matrix in the fixed affine coordinates (m,v): a Hessian would require ∂v g_mm = ∂m g_mv, but the two sides are -(1+v)^(-2) and zero. This is only a coordinate/affine-structure statement. It does not prove nonexistence of another affine structure or another coordinate chart supporting a Hessian representation. The v=0 boundary is excluded throughout. For equal-mean endpoints, their intrinsic Gaussian distance equals |r(v2)-r(v1)|: every path has length at least its radial displacement, and the fixed-mean radial segment attains it. The sequence (m,v_j) with v_j tending to zero is therefore Cauchy without a limit in the manifold. This verifies the author’s added metric-incompleteness assertion. It does not identify unrestricted ambient endpoint distances.

## 5. Multivariate positive-definite covariance corollary

Let rho=N(m,Sigma) on Euclidean R^d, with Sigma positive definite, the same unit relative transport/reaction costs, and symmetric matrices paired by tr(AB). Write xi=x-m and take

f = a·xi + xiᵀA xi - tr(A Sigma),   A=Aᵀ.

Its controls (grad f,f) generate the exact Gaussian tangent

p=(I+Sigma)a,
B=L_Sigma(A)=2(A Sigma + Sigma A + Sigma A Sigma).

This follows either by direct Gaussian density-score differentiation or by matching coefficients of the centered quadratic polynomial density ratio. In particular, Sigma⁻¹ B Sigma⁻¹/2 = Sigma⁻¹A + A Sigma⁻¹ + A, and the constant score term is -2 tr(A)-tr(A Sigma), exactly as obtained from the control operator.

The same Gaussian W¹,² compact-cutoff argument gives full-control-kernel orthogonality in R^d, so the induced metric is

pᵀ(I+Sigma)^(-1)p + tr[B L_Sigma^(-1)(B)].

Indeed the optimal cost is

aᵀ(I+Sigma)a + 4tr(A²Sigma)+2tr(A Sigma A Sigma)
= aᵀ(I+Sigma)a + tr[A L_Sigma(A)].

The matrix map L_Sigma is Frobenius-self-adjoint and positive definite. In a Sigma eigenbasis its entrywise multiplier is 2(lambda_i+lambda_j+lambda_i lambda_j)>0. When converting the trace norm to independent coordinates on symmetric matrices, off-diagonal contributions are doubled. No commuting assumption between Sigma and an energy Hessian is needed.

For F(x)=xᵀQx/2+b·x+c with Q symmetric, the exact local Gaussian field is

m′=-(I+Sigma)(Qm+b),
Sigma′=-(Q Sigma+Sigma Q+Sigma Q Sigma).

For P=Sigma⁻¹, direct differentiation yields the linear precision equation

P′=P Q+Q P+Q.

Positive definiteness of P must be retained; this equation by itself is not an assertion of all-time existence for indefinite Q. For multivariate polynomials, diagonalize Sigma. Each highest-degree monomial xi^k is multiplied in the negative-gradient density ratio by -(1+sum_i k_i/lambda_i), a nonzero factor. Hence the same degree-at-most-two Gaussian tangency criterion holds.

## 6. Scope conclusion and replay

This is a genuine inherited full-density Gaussian Riemannian result for the stated model. Gaussian-family invariance for quadratic energies is a restricted-family theorem and does not contradict a no-go theorem about finite polynomial sufficient statistics valid for arbitrary probability laws. It also does not establish an empirical interpretation, coordinate-free Hessian obstruction, general geodesic distance formula, or any multivariate completeness theorem.

Run `python independent_checks.py` with SymPy installed. It writes no files and emits a JSON record of 25 checks. `independent_checks.json` records the reviewed run. Analytic claims are reviewed through the arguments above, not by treating these finite algebra tests as a formal proof of function-space or global-existence assertions.

## 7. Primary-source boundary check

The reviewer independently opened Kondratyev and Vorotnikov, [Spherical Hellinger-Kantorovich gradient flows](https://arxiv.org/html/1809.03430v2), Introduction and Remark 1.1. The displayed formal gradient matches the centered-reaction plus transport convention. The stated analytic setting uses bounded domains or a torus and a strictly negative fitness derivative with respect to density. A density-linear energy on the real line does not meet those assumptions. The author correctly uses the paper for ancestry and convention rather than importing its existence theorem as the Gaussian proof.
