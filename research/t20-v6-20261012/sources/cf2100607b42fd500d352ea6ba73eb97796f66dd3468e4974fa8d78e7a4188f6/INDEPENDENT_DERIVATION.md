# Independent derivation before receipt of author result

2026-10-09 UTC. Ordinary mathematical review only. This derivation was written from the parent task and the known finite-support precursor, before the author's new RESULT.md was available. It confers no integration, release, or T20-closure authority.

## 1. Compact support preserves the positive determination result

Let K be a compact subset of R^d and let mu,nu be Borel probability measures supported on K. Equality of every tensor moment integral x^(tensor r), r >= 0, is precisely equality of every coordinate monomial integral and hence of every polynomial integral. The real polynomials restricted to K form a unital point-separating algebra. Stone-Weierstrass gives uniform density in C(K), and finite measures respect uniform limits. Uniqueness of finite Borel measures on compact metric spaces gives mu=nu.

For real u the integrand exp(-u dot x) is bounded above and strictly bounded below on K, so Z_mu(u) is finite and positive. Normalized tilt T_u mu is a probability on K. Equality of full moment records consequently preserves all these tilts and all mean outputs. The full record belongs to the graded product of symmetric tensor powers, not the algebraic direct sum unless only finitely many grades are nonzero. A compact simplex support is a special case; merely replacing finite channel support by continuous simplex support does not produce moment indeterminacy. Nothing here supplies finite-order closure on arbitrary infinite K, computable inversion, conditioning, or recovery from finite/noisy samples.

## 2. Exact Stieltjes class

Let f(x) = exp(-(log x)^2/2)/(sqrt(2*pi)*x) for x>0 and h(x)=sin(2*pi*log x). Put f_epsilon=f(1+epsilon*h), |epsilon|<1. Then (1-|epsilon|)f <= f_epsilon <= (1+|epsilon|)f, so f_epsilon is strictly positive and integrable. With Y standard normal,

I(s) := integral x^s f(x) h(x) dx
     = Im E exp((s+2*pi*i)Y)
     = exp(s^2/2-2*pi^2)*sin(2*pi*s), for real s.

In particular I(n)=0 for every integer n>=0. Thus all f_epsilon have mass one and moments m_n=exp(n^2/2). Distinct epsilons give distinct densities on a set of positive Lebesgue measure. This is a classical Stieltjes/lognormal construction, not a new general moment-problem theorem.

Every positive exponential moment diverges. For a>0, substituting y=log x reduces the lower bound to a positive constant times integral exp(a*exp(y)-y^2/2)dy. Its integrand eventually exceeds one, so the integral is infinite. In the tilt convention exp(-u*x), negative u are therefore inadmissible from these initial laws. The phrases 'negative exponential moment' and 'negative power moment' must not be conflated: all real power moments of the lognormal family are finite, although generally epsilon-dependent for noninteger orders.

## 3. One-sided normalized flow and its Fisher-type tangent calculation

For any probability mu on [0,infinity) with every polynomial moment finite, define L_mu(u)=integral exp(-u*x)dmu for u>=0 and T_u mu=exp(-u*x)mu/L_mu(u). Then 0<L_mu(u)<=1, every polynomial moment remains finite, and T_a T_b=T_(a+b) for a,b>=0. A locally finite piecewise-constant control lambda(t)>=0 gives u(t)=integral_0^t lambda(s)ds and a well-defined forward trajectory. This is a semigroup control repertoire. It is sufficient for the counterexample; arbitrary signed controls from u=0 cannot be imported from the compact case.

Write q=integral x dmu. In the completed score tangent space L^2_0(mu), the differential of J(mu)=integral x dmu is h -> integral x h dmu. Its Riesz representative is x-q because the variance is finite. Equivalently, the signed-density tangent G=(x-q)mu has Fisher norm squared integral (x-q)^2 dmu and pairs with h mu to give the mean differential. Bounded mean-zero scores provide actual small positive variations; the L^2 completion gives the Fisher-type tangent interpretation. No open positive-density Hilbert manifold or globally Lipschitz vector field has thereby been proved.

For the explicit tilt, d(mu_t)/dt=-lambda(t)(x-q_t)mu_t, away from control switches. Differentiation is valid in weighted total variation for each polynomial weight locally in u>=0, because x^r exp(-u*x)<=x^r and the required initial moments are finite; the endpoint derivative is from the right. Thus this is a concrete normalized replicator/Fisher-type trajectory and satisfies

m_r'=-lambda*(m_(r+1)-m_1*m_r), r>=0.

The mass equation r=0 is zero. In rank-one tensor notation M_r=m_r*e^(tensor r), contraction with lambda*e^* yields lambda*m_(r+1)*e^(tensor r), with no r+1 factor. The infinite system is coordinatewise defined on a graded product; it is nonlinear. It is not licensed as a well-posed ODE on an unnamed Banach space.

## 4. All right jets agree but analytic continuation differs

Under lambda=1, L_epsilon^(r)(0+) = (-1)^r exp(r^2/2). Domination by x^r and (for difference quotients) x^(r+1) proves continuous right derivatives of every order. L_epsilon(0)=1, so q_epsilon=-L_epsilon'/L_epsilon and every normalized moment m_r(t)=(-1)^r L_epsilon^(r)(t)/L_epsilon(t) is C-infinity from the right. Repeated quotient differentiation, or the hierarchy recursion, shows all their right jets at zero depend only on the initial moments and therefore agree for every epsilon.

This is not analytic uniqueness at zero. The Taylor coefficients of L have magnitude exp(r^2/2)/r! and hence zero radius of convergence. Smoothness from the right and equality of all right derivatives do not determine these functions.

For Re z>0, L_epsilon(z) is holomorphic: on Re z>=a>0 every derivative is dominated by bounded x^r exp(-a*x), integrated against a finite measure. Since L_epsilon(t)>0 for real t>0, each q_epsilon is real analytic on (0,infinity).

Suppose q_epsilon=q_delta on any nonempty open interval in (0,infinity). Then log L_epsilon-log L_delta is constant there, so L_epsilon=C L_delta. Holomorphic identity on the connected half-plane, or real-analytic identity on the positive half-line, extends that equation to all t>0. Taking t down to zero gives C=1. Laplace uniqueness then gives equality of the laws, contrary to epsilon!=delta.

For completeness, uniqueness can be proved without an inversion theorem: push both laws forward by y=exp(-x) into [0,1]. Equality of L at positive integers, together with mass one, gives equality of all moments of y. Polynomials are dense in C([0,1]), so the pushed-forward measures agree. The map x -> exp(-x) is a Borel isomorphism onto (0,1], and there is no pushforward mass at zero, so the original laws agree.

The precise conclusion is that two distinct epsilons have different mean-response functions and disagree somewhere in every nontrivial positive-time interval, including arbitrarily close to zero. It does not prove that their means differ at every single positive time. The difference is a nonzero real-analytic function on (0,infinity), so any coincidences there are isolated. Consequently the identical initial infinite moment record has multiple admissible coordinatewise hierarchy continuations. This refutes continuation sufficiency of that record in this separately defined unbounded class, without refuting uniqueness in the full measure state or finite-dimensional ODE uniqueness.

## 5. Exponential-integrability repair

For mu on [0,infinity), existence of integral exp(a*x)dmu<infinity for some a>0 makes the moment series absolutely convergent for |u|<a and equal to the Laplace transform there, by dominated summation. If nu has the same nonnegative integer moments, Tonelli first gives integral exp(a*x)dnu = sum a^n*m_n/n! = integral exp(a*x)dmu, so the same exponential bound transfers. Equality of transforms near zero and Laplace uniqueness give mu=nu. Thus even requiring the bound for just one of two moment-equivalent nonnegative laws suffices. The result is exact determinacy, not a finite moment record or an effective inversion theorem.

For every u>0, T_u mu automatically has some positive exponential moment, e.g. integral exp((u/2)*x)d(T_u mu)=L_mu(u/2)/L_mu(u)<infinity. Thus the specific indeterminacy obstruction sits at the initial one-sided boundary; at positive times the tilted laws are moment-determinate. This is consistent with their initially equal moment sequences diverging immediately as functions.

## 6. Source and novelty scope checked independently

The finite predecessor RESULT.md explicitly assumes known finite stochastic channel columns in a compact simplex, and its finite closure uses exact interpolation. Its unbounded extension is not implicit. The inherited H-formalisation source uses an algebraic tensor direct sum and requires declared updates and observables to factor through a future-safe quotient. The H-Continuation supplement already credits classical moment matching and proves finite action-observation instrument sufficiency. These are positive ancestry, not claims defeated by the unbounded example.

P02 U05_MEASURE_CORE.md distinguishes finite support, countable singleton support, nonatomicity, weak versus total variation limits, and effective presentation. P03 U05_MEASURE_SEMANTICS.md preserves that scope. P02 CV_C_HIERARCHY.md and inherited DEFECT_COMPUTABILITY.md classify point-concentration defect over declared total prefix-observer encodings. They do not identify existence, determinacy, computation, or sampling. All f_epsilon here are nonatomic Borel probabilities with singleton defect one; their distinct tilt futures neither refute nor improve those defect/computability classifications. No broad claim of source absence or novelty follows from the targeted inspection.

Primary external research inspected: Heyde, 'On a Property of the Lognormal Distribution', JRSS B 25(2), 1963, pp.392-393, publisher abstract (https://doi.org/10.1111/j.2517-6161.1963.tb00521.x); Kleiber, 'The generalized lognormal distribution and the Stieltjes moment problem', introduction and Section 3 (https://arxiv.org/pdf/1301.1277). These explicitly identify classical lognormal moment indeterminacy, lack of positive exponential moments, and compact-support / exponential-integrability determinacy. The displayed proofs above are independent ordinary derivations, not numerical evidence or a kernel-checked certificate.
