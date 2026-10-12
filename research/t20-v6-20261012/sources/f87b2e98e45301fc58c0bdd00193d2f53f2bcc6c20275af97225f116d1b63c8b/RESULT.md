# Nonnegative SOS loss tending to zero does not ensure continuation

11 October 2026 UTC. Additive T20 mathematical counterexample, proposed and developed by root. Written proof and exact algebraic controls; independent review is pending. The earlier signed-energy example and all accepted positive theorems remain unchanged.

## Stronger question

The earlier pointwise-coercive counterexample allows its instantaneous energy to become arbitrarily negative across time. Could the failure therefore disappear if every objective were a nonnegative polynomial square, with the actual observed loss strictly decreasing to zero and normalized reweighting well behaved?

**No.** The following predetermined smooth schedule has all these stronger properties while a single finite initial state escapes to infinity in finite time. This does not refute the retained uniform common-energy theorem: its common control is precisely absent.

## Predetermined schedule and potential

For 0≤s≤1/2 define

    t(s)=integral_s^(1/2) du/(1−5u^5),
    T=t(0).

On this closed interval 27/32≤1−5s^5≤1. Thus

    1/2≤T≤16/27.

The derivative t′(s)=−1/(1−5s^5) is nonzero. The integrand is smooth on a neighborhood of this compact interval, so its inverse s(t) is smooth on a neighborhood of [0,T], including t=T. It satisfies

    s(0)=1/2,   s(T)=0,   ds/dt=−(1−5s^5).

This schedule is defined independently of the state trajectory. Put

    a(t)=s(t)−s(t)^6,
    V_t(x)=1/2 [x^4−a(t)x^5]^2,
    b_t(x)=−∂_x V_t(x).

Every coefficient is smooth on [0,T]. For t<T, a=s(1−s^5)>0, so V_t is a degree-ten coercive polynomial square. At t=T, a=0 and V_T=x^8/2 is also coercive. All V_t are nonnegative, with a common lower bound zero; all have minimum zero at x=0. Their individual autonomous gradient flows are forward complete by their own compact sublevels.

## Exact escaping solution with decreasing loss

Define X(t)=1/s(t), 0≤t<T. Then X(0)=2 and

    X′(t)=(1−5s^5)/s².

Writing r=a/s=1−s^5, direct differentiation gives

    b_t(1/s)
      =−s^(−7)(1−r)(4−5r)
      =(1−5s^5)/s²=X′(t).

Hence X is the actual solution of the smooth, time-dependent gradient equation starting at 2. It goes to positive infinity as t approaches finite T.

Nevertheless,

    V_t(X(t))=s²/2,
    d[V_t(X(t))]/dt=−s(1−5s^5)<0   for t<T.

The loss decreases from 1/8 to the global minimum value zero, but there is no finite limiting state. At the endpoint the objective is still coercive and its only zero is x=0. The trajectory does not converge to that minimizer. The two limits, following the escaping state versus fixing the endpoint objective, cannot be exchanged.

For clarity, the external-time and spatial contributions are

    |∂_xV_t(X(t))|²=(1−5s^5)²/s^4,
    ∂_tV_t(X(t))=(1−5s^5)(1−6s^5)/s^4>0.

Their difference is the displayed negative total energy derivative. The external-time term partially offsets spatial dissipation. No claim that its sign alone causes the escape is needed.

## Actual probability and full hierarchy control

Let L_t(p)=p(X(t)). This is a rank-one Dirac probability functional, with every polynomial moment finite and smoothly varying for t<T. It satisfies every square test and

    L′_t(p)=L_t(b_t p′)−L_t(V_t p)+L_t(V_t)L_t(p),

because the covariance terms vanish on a Dirac law. This is an actually represented solution, not a spurious positive hierarchy.

The unnormalized weight

    w(t)=exp(−integral_0^t V_r(X(r))dr)

has a strictly positive finite endpoint limit, since

    0≤integral_0^T V_r(X(r))dr
      =integral_0^(1/2) u²/[2(1−5u^5)]du≤T/8.

Consequently exp(−T/8)≤w(t)≤1. The obstruction is neither negative killing nor normalization collapse: a positive surviving mass escapes. The normalized first moment L_t(x)=1/s diverges, so there is no coordinatewise continuous full-moment continuation through T. The Dirac probabilities are not tight and have no weak probability limit on the original real line. Changing to a compactified carrier would change the claim.

## No fixed common coercive control

Suppose a fixed nonnegative coercive C¹ function H and finite constant C supplied

    b_t(x)H′(x)≤C H(x)

for all relevant x and 0≤t<T. Along X, Gronwall yields H(X(t))≤exp(CT)H(2). Coercivity instead forces H(X(t))→∞. This contradiction excludes such a uniform control, whether or not H is polynomial or has an SOS certificate.

The moving sublevels are not uniformly compact: X(t) lies in {x:V_t(x)≤1/8} but is unbounded as t approaches T. Pointwise coercivity of a smooth coefficient family supplies no common compact barrier. This is exactly the uniformity distinction the positive common-energy theorem protects.

## Scope and evidence

The coefficient family is smooth, not asserted polynomial in time. The potential is polynomial in x, on a common finite basis, throughout the closed coefficient interval [0,T]. The solution and its moment hierarchy exist only on [0,T), and that open/closed distinction is essential.

The result disproves a guarantee of finite-time continuation or minimizer attainment based solely on frozen-time coercivity, nonnegative SOS objectives, and an actual decreasing loss tending to the minimum value. It does not prove that every changing-objective flow fails, or that the retained sufficient common-control certificate is necessary for every successful flow. It supplies no psychological identification, empirical cognitive claim, or metaphysical defeater.

`check.py` verifies the exact polynomial and rational identities. The finite-time schedule, coercivity, Gronwall contradiction and probability-limit conclusions are written universal arguments, not established by finite sampling. Predecessor hashes are recorded separately. No field-priority claim or T20 closure is made.
