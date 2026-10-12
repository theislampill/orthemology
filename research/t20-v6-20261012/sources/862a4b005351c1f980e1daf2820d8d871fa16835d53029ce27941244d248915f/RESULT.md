# Computability and terminating negative certificates

10 October 2026 UTC. Separate bounded continuation of the frozen determinate-initial counterexample. No changes to that packet, no sampling-complexity or rate-optimization claim, and no formal-kernel certificate.

## 1. Computational status of this particular counterexample

Let Z be standard normal, μ the law of exp(Z), and

    B_r(t)=E[exp(rZ−t exp(Z))], t≥0.

The counterexample's zero-atom mass is

    w=∏_(j≥1)(1−exp(−j)),

with the explicit product tail bound supplied in the preceding packet. Set

    D(t)=B_0(t)−w,
    T_0=(1−w)/(2 exp(1/2)).

On 0≤t<T_0, D(t)>(1−w)/2>0. The counterexample hierarchy has

    m_0(t)=1,    m_r(t)=B_r(t)/D(t), r≥1.

These coordinates are uniformly computable in the integer grade r and a named nonnegative time in the safe interval. The statement is not merely that the formulas are explicit.

### Effective integral bounds

For M>r, drop the damping exp(−t exp(Z))≤1 outside [−M,M]. Completing the Gaussian square gives the absolute tail bound

    ∫_(|z|>M) exp(rz−t exp(z)) φ(z) dz
      ≤ exp(r²/2)[Q(M−r)+Q(M+r)],

where Q(u)=∫_u^∞ φ(v)dv. For u>0 the elementary Mills bound is

    Q(u)≤exp(−u²/2)/(sqrt(2π)u).

The resulting computable bound tends to zero effectively as M increases. On [−M,M], the integrand is an explicitly computable smooth function. For example its derivative is

    (r−t exp(z)−z) exp(rz−t exp(z)−z²/2)/sqrt(2π),

which has an elementary computable uniform bound on a named compact time interval. Uniform subdivision with outward function-range enclosures therefore gives compact integral enclosures of arbitrarily small width. This is a terminating uniform algorithm for B_r(t). The same argument handles time input approximation with an explicit bound on the time derivative, or directly with interval-named time.

Combining that algorithm with the convergent product and positive denominator bound computes all m_r. In particular, this invalid coordinate-positive solution is itself computable; the failure is not an inability to evaluate it. The unique positive initial law and its genuine tilt remain different objects, recovered under the retained realizable-solution result.

## 2. A sound terminating certificate search at positive safe rational times

Fix a rational t with 0<t<T_0. For a finite rational vector v=(v_0,…,v_N), let p_v(x)=Σv_i x^i and define

    Q_t(v)=Σ_(i,j=0)^N v_i v_j B_(i+j)(t)−w v_0².

Since D(t)>0,

    v^T H_N^0(t)v = Q_t(v)/D(t).

Every Q_t(v) is a computable real with certified error bounds from §1. The reviewed finite-Hankel diagnostic guarantees some finite N and some real v with Q_t(v)<0. Continuity in this finite-dimensional vector gives a rational vector with the same strict sign. By homogeneous scaling, an integer vector also suffices.

A simple dovetailed search therefore terminates:

1. At stage k enumerate every degree N≤k and every integer vector with |v_i|≤k.
2. Compute an enclosing interval for each Q_t(v) to absolute width at most 2^(−k).
3. Stop and output t, v, and its interval as soon as the interval's upper endpoint is negative.

A strict negative witness has finite degree and finite coefficients, so is revisited at every sufficiently large stage. Its enclosing interval eventually lies below zero. The algorithm is sound because it returns only a strictly negative upper bound. Its termination depends on the proven nonrealizability and Stieltjes/Hankel existence criterion, not on guessing a degree.

This search is specified and proved here; a general search implementation has NOT been executed or claimed. No computable bound on its running time or detecting degree is asserted. The absence of a fixed detecting degree as t↓0 is compatible with termination at each specified positive time.

## 3. One executed rigorous interval witness

The file certify_degree_one.py implements one fixed witness, using mpmath 1.3.0 interval arithmetic at 50 decimal digits:

    t=1/10,     p(x)=1−17x/50.

It integrates the nonnegative function

    exp(−t exp(z)−z²/2) [1−17 exp(z)/50]² / sqrt(2π)

over [−10,10] with 4,096 uniform interval rectangles. Each rectangle uses a full interval range of the integrand, not a point sample. Outside the compact interval the inequality

    (1−17 exp(z)/50)²≤2[1+(17/50)²exp(2z)]

and the Mills bounds in §1 supply an explicit tail upper bound. Forty factors and the analytic remainder bound enclose the infinite product w. Thus every component of the final enclosure has an identified rounding or truncation bound.

Executed enclosures, rounded outward here for readability:

- Infinite-product mass w lies in [0.5044286547259664021, 0.5044286547259664046].
- The safe-time check 1−w−2t exp(1/2) is greater than 0.16582709.
- Absolute tail contribution is less than 1.079×10^(−15).
- Compact integral lies in [0.46635274528, 0.47185582507].
- The quadratic-form numerator lies in [−0.038075910, −0.032572829].

The strict negative upper bound certifies failure of the degree-one unshifted Hankel condition at this time. It is consistent with the theorem that the required degree diverges near zero; t=1/10 is one fixed positive time.

Reproduce with:

    python computable-positive-hierarchy-20261010/certify_degree_one.py

The exact output is saved in certify_degree_one.log. The script exits by assertion failure if either the safe-time margin or the strict negative sign is not certified. Ordinary mpmath interval arithmetic, its elementary function implementation, and Python are trusted computing components; no verified-kernel arithmetic claim is made. The separate explore_candidate.py used unverified high-precision quadrature to propose a witness and is not counted as certification evidence.

## 4. Boundaries

This packet proves coordinatewise computability and a terminating mathematical certificate-search algorithm, and executes one fixed interval witness. It does not implement the generic search, compute the complete Krein support, optimize certificate degree, establish complexity bounds, or modify earlier results.
