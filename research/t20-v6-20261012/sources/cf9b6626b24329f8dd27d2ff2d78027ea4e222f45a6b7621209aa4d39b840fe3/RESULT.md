# One positive-time law controls the entire partially damped path

10 October 2026 UTC. Root-authored candidate ordinary proof. Independent review pending. No kernel, field-novelty, protected integration or T20 closure claim. This extends the active signed-projection argument to an arbitrary finite number of hidden variables; it does not assert automatic existence when two or more variables are hidden.

## Statement

Let z in R^r, y in R^k, with r>=1 and k>=0 finite. Let g_t(z) be a continuous, locally bounded-degree schedule of SOS polynomials, independent of y. Suppose K_t=integral_0^t g_u satisfies K_t-c(t)|z|^2 SOS for each t>0, with c(t)>0. Let L_t be normalized, square-positive on the full real polynomial algebra, coordinatewise C1 through zero, and satisfy

    L'_t(p)=-L_t(g_t p)+L_t(g_t)L_t(p).

Write a(t)=exp(-integral_0^t L_u(g_u)du), A_t=a(t)L_t.

If the full record L_s has any probability representative at one time s>0, then every such representative rho_s gives a single all-moments initial law mu=a(s)exp(K_s)rho_s lifting the entire path. Conversely every lift determines such a representative. Thus positive-time representability is an all-or-none property along this specified full path; the positive-time representative fibres are in bijection with its lift fibre.

For k<=1 the existing full/d-1 marginal existence theorem supplies the positive-time representative automatically. For k>=2 this theorem supplies no automatic existence. Strictly square-positive all-time nonmoment paths remain valid counterexamples.

## 1. Inherited algebraic estimate

The finite backward Volterra SOS argument applies before any joint measure is introduced. For every polynomial q(z,y), every N, and every t>0,

    sum_(n=0)^N c(t)^n A_t(q^2 R^n)/n! <= A_0(q^2),  R=|z|^2.

For every fixed q and n, A_t(q^2 R^n) decreases, because its derivative is -A_t(q^2 R^n g_t)<=0. Hence on each interior window [eta,H] the same finite partial-sum bound holds with c=c(eta)>0 at all times in that window. This estimate is inherited from the cumulative proof and requires no representability.

## 2. Canonical positive and signed measures on controlled space

Fix a polynomial b(y) and t>0. The functional on R[z]

    lambda_t^b(f)=A_t(f(z)b(y)^2)

is square-positive. Its mass is A_t(b^2)>=0. If this mass is zero, polynomial Cauchy-Schwarz shows lambda_t^b(f)=0 for every f, so it is represented uniquely by the zero measure. If its mass is positive, normalize it. The estimate in section1 gives factorial bounds in all r controlled marginals, so the classical full-marginal Nussbaum-Carleman theorem supplies a unique finite positive representing measure tau_t^b on R^r. This is a controlled-space representation, not a joint (z,y) law.

Monotone convergence in the same estimate gives

    integral exp(cR) d tau_t^b <= A_0(b^2)

uniformly on the chosen interior window. No joint measure has entered this argument.

For an arbitrary hidden polynomial h(y), define a finite signed measure

    sigma_t,h = (tau_t^(h+1)-tau_t^(h-1))/4.

Its controlled polynomial moments are A_t(f(z)h(y)), by the identity ((h+1)^2-(h-1)^2)/4=h. It has a uniform Gaussian total-variation bound inherited from the two tau measures. Signed measures with such a bound are determined by their polynomial moments: dominated Fourier Taylor expansion identifies the Fourier transform, and Fourier uniqueness identifies the measure.

Consequently h -> sigma_t,h is real linear, and sigma_t,b^2=tau_t^b is positive. These facts follow by comparing moments of finite signed measures with Gaussian variation control; they are not assumed as a jointly measurable conditional kernel. In particular sigma_t,1=tau_t^1 has mass a(t).

## 3. Canonical projected evolution without joint laws

For fixed h, the hierarchy gives

    d A_t(h(y) f(z))/dt = -A_t(h(y)g_t(z)f(z)).

The uniform Gaussian variation estimate for sigma_t,h and local polynomial-degree/coefficient bounds on g_t justify the same active-variable Fourier Taylor argument as GENERAL_SOS_BRIDGE.md, G4. Function and derivative approximants converge uniformly on compact frequency/time sets. Frequency-independent variation bounds then justify compact smooth Fourier tests. Thus

    d integral phi d sigma_t,h = - integral g_t phi d sigma_t,h

for every compact smooth phi(z). The time-dependent compact integrating factor proves

    sigma_u,h = exp(K_s-K_u) sigma_s,h,  s,u>0.

For reverse weighting, equality is first local on compacts; it identifies the resulting locally finite signed measure with the finite sigma_u,h and thereby establishes global finite variation. None of these operations needs a family of joint representing measures.

## 4. One joint law propagates

Suppose nu_s=a(s)rho_s represents A_s on the full algebra. Section1 and monotone convergence give weighted Gaussian bounds for every hidden square under nu_s. Therefore the signed projection pi_z*(h(y)nu_s) has Gaussian variation control and exactly the moments of sigma_s,h. Uniqueness yields equality of these signed measures.

For any u>0 define the positive Borel measure

    nu_u = exp(K_s-K_u) nu_s.

The identity with h=1 gives finite mass a(u). For each hidden multi-index beta and integer m>=0, positivity of sigma_t,y^(2beta) gives, first on bounded regions and then by monotone convergence,

    integral R^m y^(2beta) d nu_u
      = integral R^m d sigma_u,y^(2beta)
      = A_u(R^m y^(2beta)) < infinity.

Here y^(2beta) is the square of a hidden monomial. These estimates make every mixed polynomial absolutely and square integrable under nu_u. The signed identity for h=y^beta now recovers every mixed moment:

    integral z^alpha y^beta d nu_u = A_u(z^alpha y^beta).

So nu_u represents A_u for all positive u. Since g_t>=0, exp(K_s-K_u) increases to exp(K_s) as u decreases to zero. For each joint polynomial q, monotone convergence and continuity give

    integral q^2 exp(K_s) d nu_s = A_0(q^2).

Thus mu=exp(K_s)nu_s has mass1 and all absolute polynomial moments, and is the required initial lift. The scalar normalizer ODE proves the bijections.

## 5. Exact boundaries and information content

The argument works for every finite hidden dimension. It establishes a propagation theorem from one positive-time joint representative, not automatic representability of an arbitrary full PSD record. It does not infer positive-time representability merely from the existence of an initial representative. It supplies no unproved measurable selection of hidden conditional laws.

For two actual initial laws, equality of a positive-time full moment record is equivalent to equality of all finite signed measures pi_z*(y^beta mu), over hidden multi-indices beta. The proof is unchanged from the one-hidden theorem: partial Gaussian damping determines these signed measures at positive time, and multiplication by the known positive weight recovers the original ones. Thus any lifts of one specified path have identical moment continuations under any supplied SOS schedule that continues in the same controlled subspace with the cumulative condition. An admissible extension itself has a positive-time representative in its old interval, so the present theorem also shows that it must be lifted. This establishes uniqueness of moment-coordinate continuation in the full admissible class whenever the given path has a positive-time representative.

The proof uses classical full-marginal Nussbaum-Carleman existence in controlled dimension r, plus the inherited Volterra and signed-Fourier machinery. The new logical step is constructing canonical controlled-space weighted measures before a joint law is known, and using them to propagate a single joint representative. This is not a claim that every positive family of abstract conditional moments has a joint measure.
