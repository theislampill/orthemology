# The global asymptotic chi-squared and KL optima

This appendix concerns precisely the hard pair and the atomic two-face instrument in RESULT.md. Rates can depend on n. The result is stronger than pointwise asymptotics because the supremum is over the whole command square.

## 1. Compact-uniform local limit

For u,v>0 put

    x=exp(-u/n), y=exp(-v/n), a=1-x, b=1-y,
    c=n/(n+1), m=n+1, h=[S-(xy)^c]/(xy)^c.

The exact integral after rescaling the rectangle in RESULT.md is

    h=c(1-c) [ab/(xy)] I_n(u,v),
    I_n=integral_0^1 integral_0^1
          [1+(b/y)s+(a/x)t]^(c-2) dt ds.                     (A1)

Fix any compact box [epsilon,L]^2 contained in (0,infinity)^2. Uniformly on it, na->u, nb->v, xy->1, I_n->1, c->1, and m(1-c)=1. In particular

    n² m h -> uv,
    m h=O(n^-2),
    n²[(1+h)^m-1] ->uv.                                    (A2)

For the last step, the integer power lies between 1+mh and exp(mh), so the difference from mh is O((mh)²), uniformly on the box. As (xy)^n=exp(-u-v) exactly,

    n² Delta -> uv exp(-u-v)

uniformly on that box. The four reference cells are bounded away from zero there. Therefore

    n^4 chi²(P1||P0) -> f(u)f(v),
    f(u)=u²/(exp(u)-1),                                     (A3)

uniformly on every such compact box. Fixed positive u,v already give a positive lower limit, hence show the all-rate O(n^-4) chi-squared order cannot be improved to o(n^-4).

For these fixed-rate families, the four-cell Taylor expansion also gives

    KL(P1||P0)=chi²(P1||P0)/2+o(n^-4).                       (A4)

This local KL expansion is uniform on every such box, justified by a positive reference-cell floor there and Delta=O(n^-2). It alone would not justify a global supremum statement; the escape control below is also needed.

## 2. Why no escaping rate regime improves the supremum

Let K_n=sup_(a,b in [0,1]) n^4 chi²(P1||P0). Literal boundary rates have value zero. In the region a>1/2 or b>1/2, RESULT.md gives

    n^4 chi² <=4n^4(11/12)^(2n) ->0.                        (A5)

In the other region the change of variables u=-n log(1-a), v=-n log(1-b) is valid, and the sharper bound there is

    n^4 chi² <=16e² f(u)f(v).                               (A6)

The nonnegative continuous function f tends to zero both at u down to zero and at u tending to infinity, and is bounded. Given any eta>0, choose epsilon>0 small and L large enough that the right side of (A6) is below eta whenever (u,v) lies outside [epsilon,L]^2. This uses the boundedness of the other f factor, so it handles asymmetric escapes too. On the compact box apply the uniform convergence (A3). Equation (A5) handles the remaining region. Hence

    limsup K_n <=sup_(u,v>0) f(u)f(v).

Conversely every fixed u,v design is allowed, so (A3) gives the reverse liminf inequality. Thus

    lim K_n=[max_(u>0) f(u)]².                              (A7)

No interchange of supremum and a merely pointwise limit is used. Both the near-zero and infinite-u regimes are explicitly controlled, including n-dependent and asymmetric designs.

Exactly the same truncation argument applies to L_n=n^4 KL(P1||P0). On a compact box (A4) gives uniform convergence to f(u)f(v)/2. Outside it, nonnegativity and KL<=chi-squared give the same vanishing envelope used in (A5),(A6). Fixed positive u,v supply the matching liminf. Consequently

    lim_(n->infinity) n^4 sup_(a,b in [0,1]) KL(P1||P0)
       =(1/2)[max_(u>0) f(u)]².                            (A8)

The orientation remains P1 relative to P0. No conclusion about the reverse KL optimum or a sharp sequential-testing sample constant is needed or claimed.

## 3. Unique positive maximizing rate and its meaning

Differentiation gives, for u>0,

    sign f'(u)=sign[2(1-exp(-u))-u].

The bracket G has G(0)=0, G'(u)=2exp(-u)-1 and G''(u)=-2exp(-u)<0. It increases initially, reaches its only turning point at log 2, and then decreases to minus infinity. It has exactly one positive zero u*. Therefore f has one positive maximizer. At that point

    u*=2(1-exp(-u*)),
    u*=1.5936242600400400923...,
    [f(u*)]²=0.4193990202224225571... .

The decimals are numerical evaluations of the proved characterization, not the basis of the optimization theorem. The KL limiting constant is half the displayed chi-squared constant, approximately 0.2096995101112112785. The design a=b=1-exp(-u*/n), equivalently a,b~u*/n, is asymptotically optimal for both chi-squared and Joe-oriented KL. Any sequence whose scaled information converges to the appropriate supremum must have u,v->u*, by the same compactness argument and uniqueness of the maximizer. This statement refers to interior near-optimal sequences; boundary choices cannot be near-optimal for large n.

The earlier fixed design t=1/[3(n+1)] has u=-n log(1-t)->1/3, and hence limiting n^4 chi-squared constant

    [f(1/3)]²=0.0788814953469059027... .

The ratio is approximately 5.3168239063, the same for the local KL constants because both are halved. It is a constant improvement in this particular hard pair's one-replay information, while the exponent remains four. It is not a proved factor reduction of the conservative broad wrong-count test's sample bound, and it does not move that test's all-alternative certificate to the new rate automatically.

The parent requested the all-rate question and supplied the concavity-gap identity. The author developed the Sibuya covariance/tail bound. The independent proof worker separately found a three-region bound, checked the covariance proof, and proposed the global chi-squared supremum extension. The parent then proposed transporting the same escape control to the global KL supremum. This appendix supplies the explicit compact-uniform and escape-control proofs. A fresh final review is required separately from the contributing worker's checks.
