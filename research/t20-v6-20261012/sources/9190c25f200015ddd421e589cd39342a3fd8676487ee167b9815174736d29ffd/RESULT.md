# Pointwise coercive changing gradients can escape in finite time

11 October 2026 UTC. Additive ordinary mathematical boundary control within ACTIVE T20. The parent proposed the potential and escaping characteristic; this note independently checks their algebra, gives the exact continuation obstruction, and corrects the external-work interpretation. No prior theorem is edited. This is not independent review of the packet, protected integration, formal-kernel verification, field-priority claim, empirical/noetic identification, or programme closure.

## 1. The counterexample and exact target

On the closed coefficient interval 0≤t≤1 put s=1−t and

    V_t(x)=x²/2−(3s+s²)x³/3+s³x⁴/4,
    b_t(x)=−∂_xV_t(x)=(3s+s²)x²−s³x³−x.             (1)

The coefficients are polynomials in t in one common finite spatial basis. Each frozen potential V_t is coercive, including the endpoint V_1(x)=x²/2. Nevertheless the nonautonomous gradient equation X'=b_t(X), X(0)=1, has the exact solution

    X(t)=(1−t)^(−2)=s^(−2),             0≤t<1,        (2)

which escapes to +∞ as t↑1. It has no finite continuation through t=1.

Thus smooth time coefficients, a bounded polynomial degree, and coercivity of every frozen potential do not replace a uniform continuation guard for nonautonomous gradients. The obstruction already occurs for an exactly represented rank-one moment path. It does not disprove initial-law representation on the interval where that path exists.

## 2. Verification and frozen autonomous completeness

For every t<1 the quartic leading coefficient s³/4 is strictly positive, so V_t(x)→+∞ as |x|→∞. At t=1 the potential is the coercive quadratic x²/2. The degree drops at that endpoint, but the coefficient family remains polynomial in t and belongs to the same degree-at-most-four basis throughout.

For any frozen time τ∈[0,1], the autonomous equation Y'=−∂_xV_τ(Y) is forward complete from every finite initial point. Indeed

    dV_τ(Y(r))/dr=−|∂_xV_τ(Y(r))|²≤0,

so the autonomous trajectory remains in one compact sublevel of the fixed coercive V_τ. Ordinary local ODE continuation then prevents finite-time escape. This standard argument is inherited from the complete-flow theorem; its inability to supply one common sublevel for changing V_t is exactly the boundary tested here.

For the genuinely nonautonomous curve (2),

    X'=2s^(−3),
    b_t(s^(−2))=(3s+s²)s^(−4)−s³s^(−6)−s^(−2)
                =2s^(−3).

Also X(0)=1. The polynomial vector field is locally Lipschitz in x and continuous in t, so local uniqueness makes this the trajectory from 1 up to its escape time. Any finite extension through t=1 would be continuous there, contradicting X(t)→+∞.

## 3. A positive rank-one hierarchy with no finite endpoint record

Define for 0≤t<1

    L_t(p)=p(X(t)),          ρ_t=δ_(X(t)).

This is a normalized linear functional on all real polynomials, with

    L_t(q²)=q(X(t))²≥0,
    m_n(t)=L_t(x^n)=s^(−2n).

Every moment is finite and C∞ at every time in the half-open domain, and on every compact subinterval of [0,1). The initial full record is that of δ_1. The full Hankel rank is exactly one at all these times.

For every polynomial p the reaction covariance vanishes on a Dirac law:

    −L_t(V_t p)+L_t(V_t)L_t(p)=0.

Consequently

    L'_t(p)=p'(X(t))b_t(X(t))
           =L_t(b_t p')−L_t(V_t p)+L_t(V_t)L_t(p).    (3)

The path satisfies the full normalized transport/reaction hierarchy and every square test throughout 0≤t<1. Normalized reweighting cannot rescue the spatial escape because its covariance term is already identically zero.

The first moment m_1(t)=s^(−2) diverges, so there is no finite coordinatewise-continuous, hence no C¹, extension to a polynomial functional at t=1. There is also no weak probability limit on R: compactly supported continuous tests eventually vanish at X(t), giving vague limit zero, whereas the masses stay one. We do not reinterpret vague escape as a probability at infinity or silently reset the endpoint law.

## 4. Even decreasing instantaneous energy does not give a common barrier

Along the escaping characteristic,

    V_t(X(t))=(1/6)s^(−4)−(3/4)s^(−5)→−∞.           (4)

In fact its derivative is negative throughout 0≤t<1:

    d[V_t(X(t))]/dt=(2/3)s^(−5)−(15/4)s^(−6)<0,      (5)

because 0<s≤1. The gradient and explicit time derivative are

    ∂_xV_t(X(t))=−2s^(−3),
    |∂_xV_t(X(t))|²=4s^(−6),
    (∂_tV_t)(X(t))=(2/3)s^(−5)+(1/4)s^(−6)>0.        (6)

Thus the exact identity

    d[V_t(X(t))]/dt=(∂_tV_t)(X(t))−|∂_xV_t(X(t))|²

holds with a positive external-work term that partially offsets the larger negative gradient-square term. It would be inaccurate to attribute runaway simply to the sign of ∂_tV. The correct point is that even actual decreasing instantaneous energy controls no fixed compact set when the objective itself changes and its lower bounds are not uniform.

Equation (4) also proves that no finite scalar m satisfies V_t(x)≥m for every x and every 0≤t<1, despite a finite lower bound for each individual frozen potential. The coefficient family converges smoothly on every compact spatial set to V_1, while its relevant negative-energy regions move to infinity.

For completeness, the integrated original killing along this trajectory is

    J(t)=∫_0^t V_r(X(r))dr
        =19/144+(1/18)s^(−3)−(3/16)s^(−4),

with J(0)=0 and J(t)→−∞. The corresponding unnormalized Dirac mass exp(−J(t)) diverges. The normalized probability remains the valid δ_(X(t)) before escape. This is consistent with, rather than a remedy for, the failure of a uniform lower killing bound.

## 5. No uniform common coercive C¹ control exists

The obstruction is stronger than failure to find an SOS certificate. Suppose there were a fixed nonnegative coercive C¹ function H:R→[0,∞) and a finite constant C such that

    b_t(x)H'(x)≤CH(x)

for all x and all 0≤t<1. Along (2), Gronwall would imply

    H(X(t))≤e^(Ct)H(1),              0≤t<1.

The right side stays bounded through the finite endpoint, whereas coercivity and X(t)→∞ force H(X(t))→∞. This contradiction excludes every such common control, not just polynomial H or SOS-certified ones. The same contradiction works for a uniform integrable time-dependent coefficient C(t), because its integrated Gronwall factor is finite; the finite-constant statement is all that is needed to separate the theorem's hypotheses.

Likewise no finite D and nonnegative coercive H can satisfy V_t+D≥κH with κ>0 uniformly through t=1: already V_t(X(t))+D→−∞. In particular neither component of the common-energy theorem's uniform guard can be supplied for this endpoint window.

The result concerns the full approach to t=1. It does not deny ordinary local existence or uniform bounds on each fixed shorter interval [0,T] with T<1. Constants or control functions allowed to deteriorate as T↑1 do not furnish a continuation bound through the endpoint.

## 6. Ancestry and sharp nonclaims

The inspected `complete-flow-finite-rank-20261010/RESULT.md`, §9, explicitly confines its coercive gradient completeness argument to autonomous potentials and warns against importing a common-sublevel bound into arbitrary time dependence. The time-varying square-positivity theorem explicitly requires uniform SOS domination and does not substitute pointwise coercivity. The accepted nonautonomous common-energy theorem retains exactly such uniform finite-window guards.

The earlier damped-escape packet has autonomous non-gradient transport with smooth rank-changing moments. It is a different boundary mechanism: the present coefficients form a smooth family of gradients of individually coercive polynomials, the normalized rank remains one before the endpoint, and moments diverge there rather than gluing smoothly through escape.

A bounded scan of top-level result reports for this formula and the pointwise-coercivity warning located those antecedents but no prior explicit instance of (1)–(2). This is local deduplication, not a literature-priority survey. The parent supplied the candidate formula; the exact checks supplement the written argument.

This does not refute the nonautonomous theorem under its stated common-energy certificates, any of the autonomous coercive theorems, positive-time realizability of (3), or a claim that includes finite endpoint moment continuity as a premise. It shows that one cannot replace the uniform continuation assumptions by frozen-time coercivity and smooth polynomial coefficients. No finite-data detection algorithm, hidden-law nonuniqueness, cognitive interpretation, protected integration or T20 closure is asserted.
