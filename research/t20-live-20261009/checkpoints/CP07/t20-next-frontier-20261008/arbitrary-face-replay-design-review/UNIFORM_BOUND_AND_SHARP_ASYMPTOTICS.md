# Uniform face-pair information bounds and the sharp asymptotic supremum

8 October 2026 UTC. Proof contribution in prospective scratch only. This note is not integration, audit closure, or an independent final review of the completed parent theorem. It records (i) an independently derived elementary three-region proof, (ii) a check of the parent's stronger tail argument, and (iii) a new sharp-asymptotic proof for final independent review.

## 1. Setup and conclusions

Let n>=1 be an integer, m=n+1, c=n/m. For commands a,b in [0,1], put x=1-a, y=1-b and

    A=x^n, B=y^n, T=(xy)^c,
    S=x^c+y^c-(x+y-xy)^c,
    J0=AB=T^m, J1=S^m, Delta=J1-J0.

The reference law is the product of Bernoulli absence margins A,B; the alternative has the same margins and joint absence J1. In the interior, its chi-squared divergence from the reference is exactly

    chi_n(x,y) = Delta^2 / [A(1-A)B(1-B)].                 (1)

The boundary laws agree whenever x or y is 0 or 1, so their divergence there is zero. Formula (1), with its vanishing denominator, is used only in the interior. Interior limits need not equal the boundary divergence.

The following statements hold.

1. The entirely elementary argument below gives chi_n<=65536/n^4, uniformly in both commands and every n>=1.
2. The checked parent argument improves this to chi_n<=32768/n^4.
3. The sharp asymptotic result is

       lim_(n->infinity) n^4 sup_(a,b in [0,1]) chi_n(a,b)
         = [u_*^2/(exp(u_*)-1)]^2,                         (2)

   where u_* is the unique positive solution of

       u_*=2(1-exp(-u_*)).

   Numerically, u_*=1.5936242600400400923 and the constant in (2) is 0.4193990202224225571. These decimals are optional numerical evaluations of an analytically specified constant, not evidence for the theorem.

Consequently the uniform per-pair chi-squared order is exactly Theta(n^-4). Rates a=b=1-exp(-u_*/n) attain the limiting supremum. The conclusions concern this specified two-face retained-threshold hard pair.

## 2. Exact concavity-gap identities

For 0<x,y<1 write g=S-T. The mixed second derivative of z^c gives

    g=c(1-c) integral_[0,x(1-y)] integral_[0,y(1-x)]
                          (xy+s+t)^(c-2) dt ds.           (3)

Indeed the rectangle corner values are x^c+y^c-(xy)^c-(x+y-xy)^c. All factors in (3) are positive. Since c-2<0,

    0<g<=c(1-c)ab(xy)^(c-1),
    g/T<=c(1-c)ab/(xy).                                  (4)

For any nonnegative S>=T and integer m,

    S^m-T^m <=m(S-T)S^(m-1).                             (5)

Also S<=min(x^c,y^c), because x+y-xy>=max(x,y).

## 3. Core region: x,y>=1/2

Set r=g/T. Here ab/(xy)<=1, so (4) gives mr<=c ab/(xy)<=1. Therefore

    Delta=AB[(1+r)^m-1]
         <=AB mr exp(mr)
         <=e ab AB/(xy)
         <=4e ab AB.                                     (6)

Define u=-n log x and v=-n log y. Since 1-exp(-u/n)<=u/n,

    a^2 A/(1-A) <=u^2/[n^2(exp(u)-1)].                   (7)

The elementary power-series inequality exp(u)-1>=u^2/2 yields

    chi_n <=64e^2/n^4.                                  (8)

Keep also the sharper functional envelope

    n^4 chi_n <=16e^2 f(u)f(v),
    f(z)=z^2/(exp(z)-1).                                (9)

This envelope is essential in section 7.

## 4. An independent three-region proof for all commands

By symmetry take x<=y. The core was handled above. Two regions remain.

### 4.1 A homogeneous concavity lemma

For arbitrary positive x<=y and 0<c<1, let

    H=x^c+y^c-(x+y)^c.

Then

    H<=2(1-c)(xy)^(c/2).                                (10)

To prove this, use the convergent improper integral

    H=c(1-c) integral_[0,x] integral_[0,y]
                              (s+t)^(c-2) dt ds.

Split the rectangle into [0,x]^2 and [0,x] times [x,y]. In the square, (s+t)^(c-2)<=max(s,t)^(c-2), hence its integral is at most 2x^c/c. In the second rectangle,

    (s+t)^(c-2)<=t^(c-2)<=x^(c-1)/t,

so its integral is at most x^c log(y/x). Consequently

    H <=(1-c)x^c[2+c log(y/x)].

After division by (xy)^(c/2), put z=c log(y/x)>=0. The remaining factor is (2+z)exp(-z/2)<=2, as its derivative is -z exp(-z/2)/2. This proves (10).

Subadditivity of the c-th power gives

    (x+y)^c-(x+y-xy)^c <=(xy)^c.

Combining it with (10), the normalized quantity R=S/(xy)^(c/2) obeys

    R<=(xy)^(c/2)+2(1-c).                               (11)

### 4.2 Region x<=1/2 and y<=3/4

For n>=15, c>=2/3 and 2(1-c)<=1/8. Since xy<=3/8,

    R <=(3/8)^(1/3)+1/8 <3/4+1/8=7/8.

The denominators satisfy (1-A)(1-B)>=1/8. Since Delta<=J1,

    chi_n <=J1^2/[AB(1-A)(1-B)]
          <=8 R^(2m)
          <=8(7/8)^(2m)
          <=8 exp(-n/4).                                (12)

Thus n^4 chi_n<=8(16/e)^4<=10368, using e>=8/3.

### 4.3 Region x<=1/2 and y>3/4

Here, with b=1-y<1/4,

    g=x^c(1-y^c)-[(x+y-xy)^c-y^c]
      <=x^c(1-y^c)<=b x^c.

Equations (5) and S<=x^c imply

    Delta <=m b x^n.

Since 1-A>=1/2 and 1-B>=b,

    chi_n <=2m^2 b(x/y)^n
          <=(m^2/2)(2/3)^n
          <=2n^2(2/3)^n.                                (13)

The elementary inequality log(3/2)>=2/5 gives

    n^4 chi_n<=2n^6 exp(-2n/5)
              <=2(15/e)^6
              <=2(45/8)^6<65536.                       (14)

For completeness, log z>=2(z-1)/(z+1) for z>=1 follows by differentiating their difference; its derivative is (z-1)^2/[z(z+1)^2]. The supremum of t^k exp(-lambda t) is (k/(e lambda))^k.

### 4.4 Small n and conclusion

For 1<=n<=14, (1) is the square of the Pearson correlation under the alternative, because that alternative has margins A,B. Hence chi_n<=1 and n^4 chi_n<=14^4<65536. Combine this with (8), (12), and (14). This establishes the first claim in section 1 without the power-series argument below.

## 5. Check of the parent's stronger tail argument

This section checks a proof supplied by the parent; it is not the origin of that argument. Set X=x^c and Y=y^c, so T=XY.

The series

    H_c(z)=1-(1-z)^c=sum_(k>=1) p_k z^k,
    p_k=(-1)^(k+1) binom(c,k)>0,
    sum p_k=1,

defines an integer-valued K. For 0<=a,b<=1,

    X=E[1-a^K], Y=E[1-b^K],
    S=E[(1-a^K)(1-b^K)].

Thus g=Cov(1-a^K,1-b^K). On the diagonal,

    Var(1-a^K)=X D_c(a),
    D_c(a)=2-(1+a)^c-(1-a)^c.

Concavity on [1,2] gives (1+a)^c>=1+(2^c-1)a; also (1-a)^c>=1-a. Therefore

    D_c(a)<=a(2-2^c)<=2(1-c)a.

The last inequality follows from 2^c>=2c on [0,1]. Cauchy-Schwarz now gives

    g<=2(1-c)sqrt(XYab).

By (5), m(1-c)=1, and 1-A>=a, 1-B>=b,

    Delta/sqrt[A(1-A)B(1-B)]
       <=2 sqrt[ab/((1-A)(1-B))] (S/sqrt(XY))^n
       <=2R^n.                                         (15)

The needed uniform bound on R in the tail is valid. Put r=1/c in [1,2], alpha=r/2, U=X^2, V=Y^2. The nonnegative concavity gap (3), now with exponent alpha, says

    U^alpha+V^alpha-(UV)^alpha >=(U+V-UV)^alpha.

It follows that

    (X^r+Y^r-X^rY^r)^(1/r)
       >=sqrt(X^2+Y^2-X^2Y^2),

and therefore

    S<=X+Y-sqrt(X^2+Y^2-X^2Y^2).

Rationalization and X+Y>=2sqrt(XY), X^2+Y^2>=2XY yield

    R <=(2+XY)/(2+sqrt(2-XY)).                           (16)

Outside the core, one of x,y is <=1/2, hence XY<=1/sqrt(2)<3/4. The numerator in (16) is at most 11/4, and the denominator is at least 3. Thus R<=11/12. Equation (15) gives the all-n tail estimate

    chi_n<=4(11/12)^(2n)<=4exp(-n/6).                   (17)

Consequently

    n^4 chi_n<=4(24/e)^4<=4*9^4=26244<32768.

Together with (8), this verifies the stronger uniform constant 32768 for every n>=1.

## 6. Uniform local asymptotics in the natural rate coordinates

For u,v>0 set x=exp(-u/n), y=exp(-v/n). Then A=exp(-u), B=exp(-v) exactly. Rescaling both integration variables in (3) gives the exact formula

    r_n:=g/T
       =c(1-c)[ab/(xy)] I_n(u,v),

    I_n(u,v)=integral_0^1 integral_0^1
      [1+(b/y)s+(a/x)t]^(c-2) dt ds.                    (18)

Fix 0<epsilon<M<infinity and let (u,v) vary in K=[epsilon,M]^2. Uniformly on K,

    a/x=exp(u/n)-1=O(1/n),
    b/y=exp(v/n)-1=O(1/n),
    I_n(u,v)=1+O(1/n),
    n^2 ab/(xy)=uv+O(1/n),
    c=1+O(1/n).

Since m(1-c)=1, (18) implies, uniformly on K,

    n^2 m r_n=uv+O(1/n),
    r_n=O(n^-3), m r_n=O(n^-2).                         (19)

For z=m r_n>=0, Bernoulli's inequality and 1+r_n<=exp(r_n) give

    0<=(1+r_n)^m-1-mr_n<=exp(z)-1-z=O(z^2).

Thus (19) yields the uniform expansion

    n^2 Delta/(AB)
       =n^2[(1+r_n)^m-1]
       =uv+O(1/n).                                     (20)

Substitute this into (1). Since exp(u)-1 and exp(v)-1 are bounded away from zero on K,

    F_n(u,v):=n^4 chi_n(exp(-u/n),exp(-v/n))
      -> f(u)f(v)                                     (21)

uniformly on every such K, with f defined in (9).

## 7. Why local convergence controls the unrestricted supremum

The issue is moving rates that approach either boundary faster or slower than 1/n; pointwise convergence alone would not settle it.

First, f is continuous and positive on (0,infinity), with f(z)->0 as z decreases to zero or increases to infinity. It has a finite maximum L. For every eta>0, choose epsilon,M so that

    sup_[z outside [epsilon,M]] f(z)
       < eta / [(16e^2+1)L].                            (22)

For points in the core x,y>=1/2 but outside K=[epsilon,M]^2, one coordinate is outside [epsilon,M], so (9) and (22) give

    |F_n(u,v)-f(u)f(v)|
       <=F_n(u,v)+f(u)f(v)<eta.                         (23)

For points outside the core, (17) gives F_n<=4n^4 exp(-n/6), uniformly. At least one of u,v exceeds n log 2; hence

    f(u)f(v)<=L sup_[z>=n log 2] f(z)->0.

Therefore the left side of (23) tends uniformly to zero outside the core as well.

Finally, K is eventually inside the core and uniform convergence on K was proved in (21). Since eta was arbitrary,

    sup_(u,v>0) |F_n(u,v)-f(u)f(v)| ->0.                (24)

This is a full uniform convergence statement in the rescaled coordinates. In particular, the difference between the two suprema tends to zero. Boundary commands have divergence zero and do not change the supremum. This proves (2).

The alternate tail estimates (12)-(13) also suffice for the truncation proof: after multiplication by n^4 they vanish uniformly. Thus the sharp-asymptotic conclusion does not depend on using the parent's stronger constant.

## 8. Maximizing the limiting function

Differentiate f:

    sign f'(u) = sign h(u),
    h(u)=2(1-exp(-u))-u.

We have h(0)=0, h'(u)=2exp(-u)-1, and h''(u)=-2exp(-u)<0. The derivative is positive before log 2 and negative afterward. Since h(log 2)=1-log 2>0 and h(2)=-2exp(-2)<0, there is exactly one positive root u_* in (log 2,2), with f increasing before it and decreasing after it. Thus the unique maximizer of f(u)f(v) is (u_*,u_*), proving the characterization in section 1.

For numerical verification only, mpmath at 50 decimal digits evaluated the root and displayed constant. No grid or numerical optimizer is needed for the theorem.

## 9. Unreviewed future note, excluded from the main contract

The parent theorem fixes both commands before each pair. The following one-step adaptation observation is only a future proof note; it is unreviewed and is not part of the present theorem or its authorized design-class enlargement.

Suppose a first-face command a is selected, and the second-face rate is b_0 or b_1 according to the first bit, using the same retained latent vector. The first marginal is identical in both worlds. Consequently the chi-squared divergence of the resulting two-bit adaptive experiment equals the sum over first-bit branches of their common branch probability times their conditional chi-squared divergence.

For branch i this contribution is one nonnegative summand of the fixed-pair chi-squared divergence at (a,b_i). Therefore the adaptive two-bit divergence is at most

    chi_n(a,b_0)+chi_n(a,b_1)
       <=2 sup_(a,b) chi_n(a,b).

Common randomization is covered by conditioning and then data processing if the seed is hidden. This observation preserves the n^-4 order while introducing a factor two in this simple bound. It does not establish the sharp asymptotic constant for within-pair adaptation, nor cover more than two observations sharing the latent vector.

## 10. Evidence and limitations

The proof uses only exact identities, elementary inequalities, convergent positive series, and calculus. The correlation bound assumes the specified genuine equal-margin alternative, which is supplied by the Joe construction in the parent task. The proof does not identify actual experimental hardware or productive route counts from arbitrary side information. It does not extend to longer retained-threshold transcripts by treating their individual pairs as independent. This is a mathematical design-class statement about the given hard pair.

Sections 4 and 6-8 are proof contributions. Section 5 independently checks the parent's specified tail derivation but does not constitute final independent review of the combined result. A fresh reviewer should assess the integrated theorem and asymptotic claim.
