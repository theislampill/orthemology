# A four-probability replay panel identifies the finite route count

8 October 2026 UTC. Prospective mathematical scratch work. This sibling preserves all predecessor files. It proves an exact conditional probability-model certificate; it does not assert a physical experiment, finite-sample identification, an effective equality test, protected integration, global gate independence, or T20 closure.

## 1. Main result and the command-coordinate qualification

Fix a positive integer n and the reference model of n mutually independent AB route occurrences, with independent A/B gates of respective true success rates a,b. Its fresh-trial absence and same-threshold paired-face absence laws are

    Q_n(a,b) = (1-ab)^n,
    J_n(a,b) = ((1-a)(1-b))^n.

Put

    t = 1/[3(n+1)].

Consider an alternative with an arbitrary positive integer m of mutually independent route occurrences. All occurrences share the same coordinate-only endpoint-preserving A marginal map alpha and B marginal map beta. Each occurrence can have a different valid A/B joint distribution. In a paired replay, the probes (t,1) and (1,t) must reuse each occurrence's same A-at-t and B-at-t gate realization, with no gate-state mutation or resampling between probes. A fixed threshold-pair realization supplies this semantics, but the proof requires only the resulting valid joint Bernoulli tables at this t.

If the alternative exactly matches the following four scalar probabilities, then m=n:

    Q(t,1) = (1-t)^n,
    Q(1,t) = (1-t)^n,
    Q(t,t) = (1-t^2)^n,
    J(t,t) = (1-t)^(2n).

Thus three command settings, together with one extra joint observation across the two face probes, suffice. There is no upper bound on m. Heterogeneous within-route joint laws are allowed. The same certificate additionally forces

    alpha(t)=beta(t)=t,
    P(A_j(t)=1, B_j(t)=1)=t^2   for every route j.

These are statements at the one tested rate, not global factorization statements.

**Qualification about selecting the panel.** Here a,b are the reference model's true gate-rate coordinates. The finite design is operationally specified only when those rates are known/selectable, for example when the reference calibration is the identity or commands realizing a=b=t are supplied. If arbitrary unknown nominal-to-true homeomorphisms are retained, the theorem instead supplies an existential finite panel in true coordinates. It does not identify known nominal commands depending only on n, recover unknown inverse calibrations, or establish an algorithm that finds the required commands from finitely many exact comparisons. The all-command change-of-coordinates argument in the predecessor does not remove this finite-design qualification.

## 2. Reduction to a single collection of valid tables

Write

    c = n/m,
    p = (1-t)^c,
    u = 1-p.

At (t,1), endpoint preservation makes the B gate certain, so route independence and the common A marginal give

    Q(t,1) = (1-alpha(t))^m.

The first face equality therefore forces alpha(t)=u. The other face similarly forces beta(t)=u. No equality of the routes' joint laws follows or is assumed.

Let

    x_j = P(A_j(t)=1, B_j(t)=1),
    y_j = 1-x_j,
    z_j = 1-2u+x_j.

Validity of the j-th Bernoulli table gives x_j,y_j,z_j>=0, and

    y_j+z_j = 2p.

The fresh diagonal and paired replay observations respectively mean

    product_j y_j = q := (1-t^2)^n,
    product_j z_j = r := (1-t)^(2n) = p^(2m).

The second identity specifically uses replay with the same gate realization: neither face probe produces a hit exactly when both A_j(t) and B_j(t) fail, for every route j. Merely retaining the route inventory while independently redrawing its thresholds would not give this z_j product.

## 3. All smaller counts are excluded at the same point

For nonnegative y_j,z_j, generalized Holder's inequality gives

    (product_j y_j)^(1/m) + (product_j z_j)^(1/m)
        <= product_j(y_j+z_j)^(1/m) = 2p.

If m<n, then c>1. The target probabilities would require

    (1-t^2)^c + ((1-t)^2)^c <= 2(1-t)^c.

But the two distinct positive numbers 1-t^2 and (1-t)^2 have arithmetic mean 1-t. Strict convexity of s -> s^c gives the reverse strict inequality. This is a contradiction. No high-command corner or bound over the finitely many smaller integers is necessary.

This smaller-count argument works at any 0<t<1 and also handles m=1. If zero routes were allowed, the face probability would be one and already disagree with the target.

## 4. All larger counts are excluded uniformly

Suppose m>n. Integrality yields

    0<c<=n/(n+1)<1.

Because p=(1-t)^c>=1-t, we have u<=t. In particular

    s := 1-2u >= 1-2t > 0.

Put w=1-q. The elementary union/product bound gives

    sum_j x_j >= 1-product_j(1-x_j) = w.

Expanding the product with nonnegative x_j and s then gives

    J = product_j(s+x_j)
      >= s^m [1+(sum_j x_j)/s]
      >= s^m(1+w/s).

Define d=u/p. The exact identity s=p^2-u^2 gives

    J/r >= (1-d^2)^m(1+w/s)
         >= (1-d^2)^m(1+w),

where s<=1 was used in the second line.

### Uniform control of the first factor

For 0<c<=1, concavity of h -> h^c gives the tangent bound h^c<=1+c(h-1) at h=1. Taking h=(1-t)^(-1) yields

    d = (1-t)^(-c)-1 <= c t/(1-t).

Consequently

    m d^2 <= A := n c t^2/(1-t)^2
                    <= n t^2/(1-t)^2
                     = n/(3n+2)^2 < 1.

Integer Bernoulli's inequality therefore yields

    (1-d^2)^m >= 1-m d^2 >= 1-A > 0.

No constant in this bound depends on an upper bound for m.

### Uniform control of the second factor

For 0<z<1 and positive integer n,

    (1-z)^(-n) = (1+z/(1-z))^n >= 1+nz.

Taking z=t^2 gives

    w = 1-(1-t^2)^n >= W := n t^2/(1+n t^2).

Combining the last inequalities, all with positive factors, gives

    J/r >= (1-A)(1+W).

The right side is strictly larger than one whenever

    A < W/(1+W) = n t^2/(1+2n t^2).

It suffices that

    (1-t)^2 > [n/(n+1)](1+2n t^2).

For the stated rational choice t=1/[3(n+1)], the difference is exactly

    (1-t)^2 - [n/(n+1)](1+2n t^2)
        = (n^2+7n+4)/[9(n+1)^3] > 0.

Hence J>r, contradicting the fourth observed probability. This excludes every larger positive integer count at once, without an asymptotic expansion, a differentiability assumption on the unknown marginals, or any exchange of limits over m.

In fact the proof gives the explicit conditional separation

    J >= (1+delta_n) (1-t)^(2n),

where

    delta_n = n(n^2+7n+4)
              / [(n+1)(9(n+1)^2+n)(3n+2)^2] > 0.

This lower bound assumes the other three probabilities match exactly. It is not by itself a robustness theorem when those three probabilities also have estimation errors, and it is not a finite-sample statistical guarantee.

## 5. Equality identifies the local gate table when m=n

The two count exclusions force m=n and hence c=1, p=1-t, and u=t. The Holder bound in section 3 is now an equality because

    q^(1/n) + r^(1/n)
      = 1-t^2 + (1-t)^2 = 2(1-t).

For n>=2, equality with positive y_j,z_j requires y_j/z_j to be the same for every j. Together with y_j+z_j=2p, this forces all y_j to be equal. Their product fixes

    y_j=q^(1/n)=1-t^2,
    x_j=t^2.

For n=1, the fresh diagonal probability directly fixes x_1=t^2. Thus every tested pair A_j(t),B_j(t) has the independent Bernoulli(t) table. This does not determine its behavior at another command.

## 6. Global copula independence is still not certified

A direct fixed-threshold countermodel shows the remaining freedom even after the count is correctly identified. Use identity marginal calibrations and put

    f(x)=x(1-x)(x-t),
    C_epsilon(a,b)=ab+epsilon f(a)f(b),
    epsilon=1/100.

The function is grounded and has uniform margins because f(0)=f(1)=0. Its mixed density is

    1+epsilon f'(a)f'(b).

On [0,1],

    f'(x)=-3x^2+2(1+t)x-t,
    |f'(x)|<=5+3t<=11/2<8.

The density is therefore at least 1-64/100>0. Integration of this density establishes nonnegative rectangle masses and C_epsilon is a genuine copula. It is not the product copula, since epsilon is nonzero and f is not identically zero.

Yet f(t)=0, so C_epsilon agrees with ab at all three panel points, and at the face replay cell determined by them. Take n independent route threshold pairs with this copula. All four panel probabilities agree with the reference model, while every route has a nonproduct copula away from the panel.

More generally, for any fixed finite set of evaluated coordinate levels, a nonzero polynomial vanishing at those levels and at both endpoints, with sufficiently small coefficient in the same density construction, preserves the entire finite grid while changing dependence elsewhere. Thus finite count certification and all-command certification of arbitrary within-route independence are different claims.

## 7. Exact scope and attribution

The parent proposed the finite-panel question, the anticipated small-t uniform-separation route, and the true-coordinate qualification. The frozen dependent-gate-transport/RESULT.md supplies the underlying widened gate model and the predecessor count ambiguity. This work replaces the proposed asymptotic control with elementary exact inequalities, supplies the rational t, eliminates the need for a high-corner panel, and exhibits an explicit positive conditional gap. The same-threshold-replay sibling develops the separate all-command theorem and includes a high-command finite-panel alias; its author also emphasized mutual route independence and the calibrated-command qualification.

The result assumes a fixed finite integer route count, common coordinatewise marginal maps, mutually independent route pairs, endpoint saturation, exact probabilities, and genuine same-gate replay. It does not cover route-specific marginal maps, dependence across routes, state-mutating probes, random inventories, unknown selection of nominal commands, or a fresh-redraw replacement for replay. It does not infer physical productive occurrences, admissible psychological interventions, causal ontology, metaphysical identification, empirical validation, protected integration, or T20 closure.

This is a mathematical scratch result and a prospective discriminator. No elapsed research duration is asserted. There is no claim that the finite panel is minimal or optimally placed.
