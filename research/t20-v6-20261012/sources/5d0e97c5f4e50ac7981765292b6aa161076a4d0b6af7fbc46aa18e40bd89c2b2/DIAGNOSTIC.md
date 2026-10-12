# Finite-degree detection of immediate nonrealizability

10 October 2026 UTC. Companion to the frozen RESULT.md. This observation was proposed and checked in participating root work; it is not independent review evidence.

Use the counterexample notation B_r(t)=∫x^r exp(−tx)dμ and w=η_K({0}). Write D(t)=B_0(t)−w>0 on the safe interval. Then

    m_0(t)=1,    m_r(t)=B_r(t)/D(t), r≥1.

For every degree N, the shifted Stieltjes Hankel matrix

    H_N^1(t)=(m_(i+j+1)(t))_(i,j=0)^N

is positive definite throughout the safe interval. Indeed, for a nonzero polynomial p of degree at most N,

    v^T H_N^1(t)v = D(t)^(-1) ∫x p(x)^2 exp(−tx)dμ(x)>0.

The strict inequality uses the strictly positive continuous lognormal density on (0,∞). Thus failure of Stieltjes realizability is entirely in the unshifted matrices

    H_N^0(t)=(m_(i+j)(t))_(i,j=0)^N.

At t=0, the unique initial representative ρ=(η_K−wδ_0)/(1−w) has infinite support, so every fixed finite H_N^0(0) is positive definite. Entrywise continuity and finite-dimensional eigenvalue continuity yield δ_N>0 such that H_N^0(t) remains positive definite for 0≤t<δ_N.

On the other hand, at every t>0 in the safe interval some finite H_N^0(t) fails positive semidefiniteness. Otherwise all unshifted and shifted Hankel matrices would be positive semidefinite, and the classical Stieltjes existence criterion would supply a representing positive measure, contradicting RESULT.md §4.

Consequently, if d(t) is the least degree of an unshifted matrix that is not positive semidefinite, then d(t) is finite for every positive safe time, but

    d(t)→∞ as t↓0.

To justify the limit, fix N. By the continuity argument H_N^0(t) is positive definite for sufficiently small t; all its lower-degree principal submatrices are then positive definite, so d(t)>N. This is an all-degree mathematical statement, not an empirical sampling claim.

There is also an exact finite-dimensional test. Let

    G_N(t)=(B_(i+j)(t))_(i,j=0)^N,
    e_0=(1,0,…,0)^T.

Since G_N(t) is positive definite,

    D(t)H_N^0(t)=G_N(t)−w e_0e_0^T

is positive semidefinite if and only if

    w ≤ [e_0^T G_N(t)^(-1)e_0]^(-1).

The right side is the finite Christoffel minimum at zero for the tilted lognormal measure. At t=0 it equals ∏_(j=1)^N(1−exp(−j)), strictly larger than w for every finite N (with value1 at N=0). Thus the initial full-atom threshold is approached only at unbounded degree, explaining why every fixed finite-degree test initially remains positive despite immediate exit from the moment image.

The only additional classical input here is the Stieltjes existence criterion: a sequence is representable on [0,∞) exactly when all its unshifted and one-step-shifted Hankel matrices are positive semidefinite. No numerical threshold, degree rate, or sampling-complexity result is asserted.
