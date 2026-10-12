# Positive-time smoothing does not guarantee finite initial Fisher–Rao length

11 October2026 UTC. Root ordinary mathematical candidate; independent review pending. This is a boundary for the same arbitrary-initial-law exponential-tilt class, not a new noetic or psychological assertion.

## Explicit supplied law

Take countable states {0,1,2,...}. Let p_0=1/2 and p_n=1/[2n(n+1)] for n≥1. The masses sum to one. Put V_0=0 and V_n=exp(n²) for n≥1. Every state has finite nonnegative loss, although the initial mean is infinite. Let

    p_n(t)=p_n exp(−tV_n)/B(t),
    B(t)=sum_j p_j exp(−tV_j).

For every t>0 all loss moments under p(t) are finite, since v^k exp(−tv) is bounded and B(t)≥1/2. The centered replicator derivative is defined, and its Fisher–Rao speed in the convention sum_j (dot p_j)^2/p_j is sqrt(Var_(p(t)) V). Also p(t)→p in total variation as t↓0 by dominated convergence and B(t)→1.

## Infinite length proof

For n≥1 use I_n=[1/V_n,2/V_n]. These intervals are disjoint since V_(n+1)/V_n=exp(2n+1)>2. On I_n,

    p_0(t)≥p_0=1/2,
    p_n(t)≥p_n exp(−2),

because B(t)≤1. The pairwise variance identity, applied to states0 andn alone, gives

    Var_(p(t)) V ≥ p_0(t)p_n(t)V_n²
                    ≥ p_0 p_n exp(−2)V_n².

Integrating speed across I_n of length1/V_n yields a contribution at least exp(−1)sqrt(p_0p_n)=1/[2e sqrt(n(n+1))]. The sum over every infinite tail of n diverges, since sqrt(n(n+1))≤n+1. Therefore every interval (0,ε] has infinite Fisher–Rao length, even though the curve converges in total variation to p and is smooth with finite speed at each positive time.

The same supplied law still falls inside the fixed-positive-endpoint, no-initial-moment reciprocal-Taylor approximation theorem. Thus high-order endpoint convergence and positive-time moment regularisation do not imply a rectifiable Fisher–Rao path starting at zero. Each fixed delayed interval [τ,T], τ>0, retains the ordinary smooth finite-length geometry.

## Finite initial energy is a sufficient repair

When E_p V<∞, the exact positive-time identity dE_(p(t))V/dt=−Var_(p(t))V and monotone-limit recovery of the initial mean imply

    integral_0^T Var_(p(t))V dt = E_p V−E_(p(T))V <∞.

Cauchy–Schwarz then bounds total Fisher–Rao length by sqrt(T(E_p V−E_(p(T))V)). Finite variance at exactly zero is stronger than this sufficient finite-length condition. No assertion that finite initial mean is necessary is made.

This separates three statements: finite initial tangent norm; finite initial path length; smooth positive-time geometry. It preserves the independently established endpoint convergence result rather than weakening it.

## Prescribed path length is not endpoint distance

The divergence concerns this particular exponential-tilt orbit. It does not imply infinite Fisher–Rao distance between its initial and later laws, or absence of another finite-length correction path. Under the square-root representation u_n=sqrt(p_n), v_n=sqrt(p_n(t)), both are unit vectors with positive inner product. Their nonnegative great-circle arc has finite length; with the stated Fisher convention the endpoint distance is2 arccos(sum_n sqrt(p_n p_n(t)))<π. Thus an endpoint may be close while the chosen orbit has infinite length near its initial time. This distinction is essential when transporting the result into a claim about path cost or adequacy.
