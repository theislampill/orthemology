# Canonical Hessian correction: dual invariants, clock and domain

9 October 2026. Written mathematical investigation of an existing Orthemology field. This does not identify forecasts with human cognition or license a DAEE route. No repository mutation, integration or T20 closure.

## Exact inherited input

The directly read `SmoothScalar.Score` permits continuous generators on [0,1], with first and second derivatives on (0,1), continuous strictly positive second derivative. `SmoothRigidity.hessian` is the diagonal form with entries h_i(b_i)=f_i''(b_i). `NudgeRigidity.canonical_nudge_gain` supplies

    z(b)=sum_i b_i, r(b)=z(b)-1,
    V_i(b)=-r(b)/h_i(b_i),
    d D_F(e_j,b)[V(b)]=-r(b)^2 for every truth vertex e_j.

The inherited theorem is a directional statement. The following declares a continuous-time autonomous flow b'=V(b) on the open cube. Its time is a chosen model parameter, not measured cognitive, processor or research time. With smooth generators this is the negative Riemannian gradient of E(b)=r(b)^2/2 for the Hessian metric. At the inherited minimal regularity it is a continuous positive-definite Hessian-form gradient construction; no extra smoothness is silently claimed.

Sources were retrieved read-only at observed GitHub pin 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. That is a read snapshot, not a fresh CI or adoption assessment. Exact source bindings are retained in the adjacent recovery packet.

## 1. Dual coordinates give a genuine flow under the inherited regularity

Put y_i=f_i'(b_i). Since h_i is continuous and strictly positive, f_i' is a C1 increasing diffeomorphism from (0,1) onto its open image I_i; denote its C1 inverse by phi_i. The chain rule gives

    y_i'=h_i(b_i)b_i'=-r(b)=1-sum_k phi_k(y_k).

The right side is C1 in y, so it has unique local solutions. Transforming back establishes local existence and uniqueness of the original field even though mere continuity of h_i would not by itself justify an ordinary local-Lipschitz assertion about V in b-coordinates.

All differences y_i-y_j are conserved. For initial b^0, set alpha_i=f_i'(b_i^0). The trajectory has the representation

    b_i(t)=phi_i(alpha_i+lambda(t)),
    lambda'=1-sum_i phi_i(alpha_i+lambda), lambda(0)=0,

on the common interval where every alpha_i+lambda belongs to I_i. This is one scalar equation for a fixed initial parameter vector, not a one-number summary of all possible initial conditions. Discarding the alpha differences generally discards the curve itself.

These are the familiar Legendre/mirror-coordinate mechanisms specialised to the actual canonical field. They are not a new general construction of Hessian geometry.

## 2. What this correction conserves

For every pair of categorical truth vertices j,k,

    d/dt [D_F(e_j,b(t))-D_F(e_k,b(t))]=0.

This follows directly from the inherited equal directional-gain identity, now applied to a valid differentiable trajectory. Each statewise loss decreases by the same accumulated integral of r(t)^2. The correction removes a common incoherence penalty without changing the differences between those statewise losses.

This is a mathematical discriminator between coherence repair and changes in relative statewise scoring. It is not a theorem that all epistemic correction must conserve these differences, or that a human acquires no knowledge. Other evidence updates, routes, objectives or vector fields can change them. Nor does it identify a loss difference with actual warrant. The new credit is an explicit continuation consequence of the inherited directional identity.

## 3. A boundary counterexample inside the admissible generator class

Use n=3 and f_i(x)=x^2/2, so h_i=1. Start at b^0=(1/100,4/5,4/5), whose sum is 161/100. The exact unrestricted affine-space solution is

    r(t)=(61/100) exp(-3t),
    b_i(t)=b_i^0-(61/300)(1-exp(-3t)).

At t_*=(1/3) log(61/58), the first coordinate reaches zero while z(t_*)=79/50. Thus the open-cube forecast flow reaches its domain boundary before coherence. All inherited pointwise common-descent conclusions were true before that time.

The source did not claim global invariance of the open cube. This supplies an explicit control against importing that claim into an operational noetic interpretation. A boundary stop, a constrained/projection rule or a different metric requires its own declaration. It is not legitimate to silently run the same interior flow through a forbidden state and count the result as an admissible route.

## 4. Positive global result for the binary-log generator

Take f(x)=x log x+(1-x) log(1-x), continuously extended to endpoints, for every coordinate. Then

    h(x)=1/[x(1-x)], phi(y)=1/(1+exp(-y)),
    b_i'=-r b_i(1-b_i),
    b_i(t)=phi(alpha_i+lambda(t)), alpha_i=log(b_i^0/(1-b_i^0)).

For n>=2, Z(lambda)=sum_i phi(alpha_i+lambda) is strictly increasing from 0 to n. There is a unique finite lambda_* with Z(lambda_*)=1. The scalar field lambda'=1-Z(lambda) has a unique global solution; it stays between 0 and lambda_*, is monotone unless already stationary, and converges to lambda_*. These claims follow from the sign on either side of the unique equilibrium and the bounded, globally Lipschitz right side. A finite limit different from lambda_* would have a nonzero derivative of fixed sign in a neighbourhood and hence cannot be the limit.

Consequently the full trajectory stays in a compact subset of the open cube and converges to the coherent interior point c_i=phi(alpha_i+lambda_*). Its coordinate log-odds differences remain unchanged. Along its compact scalar interval, S=sum_i b_i(1-b_i) has a positive minimum, and r'=-Sr gives exponential decay with that trajectory-dependent lower bound. No uniform rate across all initial states near the boundary is claimed.

The endpoint is exactly the unique Bregman projection minimising D_F(c,b^0) over the closed categorical simplex. Indeed grad F(c)-grad F(b^0)=lambda_* 1, and for every simplex point p,

    D_F(p,b^0)-D_F(c,b^0)=D_F(p,c)+lambda_* sum_i(p_i-c_i)=D_F(p,c)>=0.

Strict convexity gives uniqueness. Endpoints of p cause no difficulty because c and b^0 are interior and F is continuous on the closed cube. Existing Bregman projection results supply ancestry; this argument identifies the endpoint of the declared canonical dynamics in this explicit score family. It does not infer one correct truth vertex or actual cognitive warrant from convergence to a coherent forecast.

## 5. Clock preservation is part of the continuation contract

Let S(b)=sum_i 1/h_i(b_i)>0. The inherited coherent-directed construction also uses the normalised direction W=V/S. If it is declared as a vector field with its own parameter tau, then

    dz/dtau=-(z-1), z(tau)=1+(z(0)-1) exp(-tau).

Thus the scalar coherence sum predicts its own entire trajectory in that normalised clock for every generator family, for as long as the trajectory remains in the domain. V and W have the same oriented paths. To retain V's original parameter one needs d tau/dt=S(b(t)), equivalently dt/dtau=1/S(b(tau)). This clock generally contains information absent from z.

The normalisation also changes each statewise loss derivative from -r^2 to -r^2/S. It is not a semantics-free substitution if the target includes time, checking cost, route duration or score decrease per declared unit. None of those real-world quantities has been empirically identified here.

Exact three-coordinate control for binary-log scores:

    a=(1/5,2/5,4/5), b=(3/10,1/2,3/5).
    z(a)=z(b)=7/5; r^2=4/25 in both.
    S(a)=14/25; S(b)=7/10.
    z'_V(a)=-28/125; z'_V(b)=-7/25.
    z'_W=-2/5 in both.
    statewise loss derivatives under W are -2/7 and -8/35 respectively.

This separates present common gain, original-clock continuation, and normalised-clock continuation using the actual inherited separable scoring signature. It does not claim the full forecast vectors or full current losses are equal.

## 6. Attribution and evidence level

- Inherited: score signature, Hessian form, all-state canonical-nudge gain, pointwise normalisation, Bregman projection machinery, fibre/continuation principles.
- Ordinary classical mechanisms: inverse-function/ODE theory, Legendre coordinates, time reparametrisation, convex Bregman optimality.
- Local additions: explicit flow-level invariants and boundary control, binary-log global trajectory/endpoint calculation, and clock-sensitive information distinction. The companion investigations determine the scalar-projectability class and exact predictive-memory boundary.
- Not claimed: a new general mirror-flow theorem, a fresh kernel replay of inherited modules, a newly kernel-checked ODE theorem, empirical cognitive dynamics, source authentication, DAEE route admission, or universal mathematical novelty.

For classical ancestry, Alvarez, Bolte and Brahic, *Hessian Riemannian gradient flows in convex programming* (2004), author-hosted manuscript https://www.math.tecnico.ulisboa.pt/~brahic/Legendre10.pdf, introduction and §§3.1–3.2/5.2–5.4, presents Hessian metrics, Bregman relations and Legendre-coordinate flow methods. The present elementary specialisation is proved above rather than borrowing an unchecked global theorem. Only the specified portions were inspected; no full-paper verification is claimed.
