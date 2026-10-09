# Arbitrary two-face rates retain the fourth-power replay barrier

8 October 2026 UTC. New scratch sibling beyond the sixth checkpoint cutoff. Earlier frozen stages are unchanged. All conclusions concern the stated probability model and observation interface.

## 1. Result and observation contract

Fix an integer n>=1. Compare the same two worlds used in finite-replay-sampling-lower-bound:

- Reference: n mutually independent product AB routes with independent uniform coordinate thresholds.
- Alternative: m=n+1 mutually independent Joe threshold pairs, with c=n/(n+1), shared coordinate calibration H_c(z)=1-(1-z)^c, and per-route joint gate success H_c(ab).

They have identical fresh endpoint absence functions Q(a,b)=(1-ab)^n at every command. An informative replicate draws a new independent route-threshold vector, retains exactly that vector during the two face probes (a,1) and (1,b), and separately records both endpoint bits. The two rates are chosen before observing either bit. They can be any rates in [0,1], and can depend on all earlier completed replicates through a common randomized policy. Within a pair there is no redrawing, output carryover, state mutation, or adjustment of the second rate after the first bit. Distinct replicas are fresh and independent conditionally on the chosen rates and prior history. The true reference-rate coordinates must be selectable if this is interpreted operationally.

Let P0^(a,b), P1^(a,b) denote the two-bit laws. The following uniform bound holds, including literal boundary commands with the conventions below:

    KL(P1^(a,b) || P0^(a,b)) <= chi²(P1^(a,b) || P0^(a,b))
                              <= 32768 / n^4.                 (1)

The constant is deliberately loose. Consequently, for 0<alpha<1/2, any common adaptive design satisfying the above contract and deciding between these worlds with error at most alpha in each world requires

    E1[N_pair] >= (n^4/32768) kl(1-alpha,alpha),               (2)

under the unconditional terminal-correctness condition in section 6. A fixed pair budget N satisfies the same lower bound. Arbitrarily many permitted fresh single-endpoint observations add no information for this hard pair. The expectation in (2) is under the Joe alternative, in accordance with the KL orientation.

The all-rate chi-squared order is sharp. ASYMPTOTIC_DESIGN.md proves

    lim_(n->infinity) n^4 sup_(a,b in [0,1]) chi²(P1||P0)
       = [max_(u>0) u²/(exp(u)-1)]²
       = 0.4193990202... .                                   (3)

The same appendix combines the compact-uniform KL expansion with the all-rate escape bounds to prove

    lim_(n->infinity) n^4 sup_(a,b in [0,1]) KL(P1||P0)
       = (1/2)[max_(u>0) u²/(exp(u)-1)]²
       = 0.2096995101... .                                   (3a)

The unique positive scalar maximizer u* solves u*=2(1-exp(-u*)) and is approximately 1.5936242600. Choosing a=b=1-exp(-u*/n) attains both limiting suprema. This is an asymptotically optimal chi-squared and Joe-oriented KL design for this specific two-world, two-face experiment. It is not a finite-n global optimizer assertion, a sharp minimax sample constant, or an optimality statement for longer replay words or physical instruments.

## 2. Exact pair laws and boundary convention

For 0<a,b<1 set

    x=1-a, y=1-b, X=x^c, Y=y^c,
    A=x^n=X^m, B=y^n=Y^m,
    S=x^c+y^c-(x+y-xy)^c,
    g=S-XY, Delta=S^m-(XY)^m.

In outcome order (no/no, no/yes, yes/no, yes/yes),

    P0=(AB, A(1-B), (1-A)B, (1-A)(1-B)),
    P1=P0+(Delta,-Delta,-Delta,Delta).                         (4)

These laws are inherited from the fixed threshold construction, not independently selected contextwise tables. Their common margins are A,B. The concavity identity below gives g>0 in the interior. The positive threshold density also gives all four P1 cells positive there; P0 has full support directly. Summing the four chi-squared terms gives the exact identity

    chi²(P1||P0)=Delta²/[A(1-A)B(1-B)] = rho_n(a,b)².          (5)

Here rho_n is the normalized covariance of the two absence bits in the Joe world. The reference covariance is zero. This notation introduces no latent population correlation assumption beyond the declared pair law.

If any of a,b is 0 or 1, one face bit is deterministic and both worlds have exactly the same pair law. KL and chi-squared are then zero. Common zero-mass cells contribute zero; formula (5), with a zero denominator, is not used. The interior limit of chi-squared need not equal its value on a boundary. For example as a=b tends to 1 at fixed n,

    chi²(P1||P0) -> (2-2^c)^(2m)>0,

although at a=b=1 the laws coincide. This is a useful exact control against silently substituting into a 0/0 formula or assuming boundary continuity of chi-squared.

## 3. Rates a,b<=1/2: retain the endpoint decay

Write z=x+y-xy. The four arguments xy,x,y,z have the same endpoint sum. The double integral for a mixed finite difference gives

    g=c(1-c) integral_0^{xb} integral_0^{ya}
                         (xy+s+t)^(c-2) dt ds
      <=c(1-c) ab (xy)^(c-1).                                (6)

This is positive in the interior. Put h=g/(xy)^c. When a,b<=1/2, x,y>=1/2, so

    0<h<=[c/m] ab/(xy)<=1/m.

The difference of integer powers, together with (1+h)^(m-1)<=exp(mh)<=e, yields

    Delta=(xy)^n[(1+h)^m-1]
         <= e c [ab/(xy)] (xy)^n
         <=4e ab AB.                                         (7)

Set u=-n log x, v=-n log y. Then A=exp(-u), B=exp(-v), and a<=u/n, b<=v/n. Dividing (7) by the denominator of rho gives

    n^4 rho_n² <=16e² f(u)f(v),
    f(u)=u²/(exp(u)-1).                                      (8)

Since exp(u)-1>=u²/2 for u>=0, f(u)<=2. Thus throughout this region,

    chi²(P1||P0)<=64e²/n^4.                                  (9)

Using (6) alone outside this region would lose control near x=0 or y=0. The next argument preserves the factors needed there.

## 4. A positive-mixture identity and a uniform tail contraction

### 4.1 Direct derivation of the mixture bound

For 0<c<1 the binomial series has positive coefficients

    H_c(z)=1-(1-z)^c=sum_(k>=1) p_k z^k,
    p_k=(-1)^(k+1) binom(c,k)>0.

Monotone convergence as z increases to 1 gives sum p_k=1. Thus K with masses p_k is a legitimate positive-integer random variable. This is the classical Sibuya(c) distribution; the probability mass formula and transform are documented in the [CRAN copula Sibuya reference](https://search.r-project.org/CRAN/refmans/copula/html/Sibuya.html). The following bounded-variable calculation is supplied directly; no finite moment of K is assumed or needed.

Let F=1-a^K and G=1-b^K. Expanding their expectations gives

    E F=X, E G=Y, E(FG)=S, g=Cov(F,G).

In particular

    Var(F)=X[2-(1+a)^c-(1-a)^c].

The concave chord on [1,2] gives (1+a)^c>=1+(2^c-1)a, and (1-a)^c>=1-a. Also 2-2^c<=2(1-c), by the mean value theorem and log 2<1. Hence

    Var(F)<=2(1-c)Xa,   Var(G)<=2(1-c)Yb,
    g<=2(1-c)sqrt(XYab).                                    (10)

Cauchy-Schwarz is applied to bounded F,G, not to K. The difference-of-powers bound Delta<=m g S^(m-1), and m(1-c)=1, now imply

    rho_n <= 2 sqrt{ab/[(1-A)(1-B)]} [S/sqrt(XY)]^n
           <=2 [S/sqrt(XY)]^n,                               (11)

because 1-A=1-(1-a)^n>=a, and likewise for b. The vanishing factors in (10) are essential when one rate tends to zero.

### 4.2 Comparing with the c=1/2 law

Let r=1/c in [1,2], alpha=r/2 in [1/2,1]. The same concavity-gap inequality used in (6), now at U=X²,V=Y², gives

    U^alpha+V^alpha-(UV)^alpha >=(U+V-UV)^alpha.

Taking the power 1/r shows

    (X^r+Y^r-X^rY^r)^(1/r)
       >=sqrt(X²+Y²-X²Y²).

Consequently

    S<=X+Y-sqrt(X²+Y²-X²Y²).

Rationalizing and using X+Y>=2sqrt(XY) and X²+Y²>=2XY yields

    S/sqrt(XY) <= (2+XY)/(2+sqrt(2-XY)).                       (12)

If a>1/2 or b>1/2, then one of X,Y is at most 2^(-c)<=1/sqrt(2)<3/4; therefore XY<3/4. Bounding the numerator in (12) by 11/4 and its denominator below by 3 gives

    S/sqrt(XY)<=11/12,
    chi²(P1||P0)<=4(11/12)^(2n).                             (13)

This includes every interior approach to all the problematic boundaries, however the rates depend on n. It does not assume comparable x,y or a lower bound on either rate.

## 5. Combining the regions

Since log(12/11)>=1/12, the right side of (13) is at most 4exp(-n/6). The maximum of z^4 exp(-z/6) over z>=0 occurs at z=24. Using e>=8/3,

    n^4 chi² <=4(24/e)^4 <=4*9^4=26244<32768

in the tail region. The central bound (9) is also below 32768/n^4 (for example e<3 suffices). Literal boundary commands were dealt with in section 2. This proves the all-rate chi-squared bound. The elementary log inequality gives KL(P1||P0)<=chi²(P1||P0), completing (1).

The proof also gives the more useful split envelope (8),(13). That envelope, rather than the coarse constant 32768, is what justifies the global supremum limit in ASYMPTOTIC_DESIGN.md.

## 6. Adaptive rate selection and stopping

At every completed-history value, a common policy chooses the next action and its rates using the same conditional kernel in both worlds. A replay action returns the entire ordered pair; a fresh action uses a separate new threshold vector and returns one endpoint bit. The pair's conditional KL is at most 32768/n^4, independently of its selected rates. A fresh endpoint's conditional laws agree exactly, so its KL contribution is zero. Common policy randomness and action choices add zero conditional KL.

After termination pad the transcript with a common dummy symbol. Let N_T be the number of pairs by slot T, and N_infinity its increasing limit. The finite-prefix chain rule gives

    KL(Law_1(history_T)||Law_0(history_T))
       <=(32768/n^4) E1[N_T].                                (14)

This is the same conditional-information argument as in the frozen fixed-rate predecessor, with a uniform bound replacing its fixed one-pair divergence. Continuous choices of rates cause no exceptional equality test. Literal boundary laws are identical on their common support. At interior choices all reference cells are positive. The uniform KL bound makes finite-prefix conditional contributions integrable; the negative part of a finite-alphabet log likelihood ratio is integrable as well, since p log(q/p)<=q on p<q. Thus no uniform lower cell floor across all rates is being silently required.

Require unconditional terminal correctness:

    P0(stop finitely and accept reference)>=1-alpha,
    P1(stop finitely and reject reference)>=1-alpha.           (15)

For E_T={stop by T and reject}, binary data processing bounds the left side of (14) below by kl(P1(E_T),P0(E_T)). Let T increase to infinity, using monotone convergence for costs and lower semicontinuity of binary KL for the event probabilities. The limiting rejection event E has P1(E)>=1-alpha and P0(E)<=alpha. For alpha<1/2 this implies kl(P1(E),P0(E))>=kl(1-alpha,alpha), proving (2). Infinite expected cost satisfies the result trivially. Conditional correctness only among terminating paths would not suffice.

The cost is pairs; each pair comprises two endpoint probes. The conclusion does not cover retaining one latent vector across different replicates, longer replay words, gate-level observations, or changing the second command after seeing the first bit. Equality of fresh unconditional laws would not suffice without the stipulated fresh conditional response law.

## 7. Comparison, ancestry, and exact limitations

The frozen finite-replay-sampling-lower-bound packet proved this exponent only at a=b=1/[3(n+1)]. Its fixed-rate inequality was not an all-rate theorem. The frozen finite-panel-replay-robustness packet supplies a reference test, with N>=ceil[200000000(n+1)^4 log(8/alpha)] pairs at that fixed rate and N independent fresh diagonal trials, against every wrong positive count in its declared common-marginal independent-route class. Our Joe alternative belongs to that class. The old design remains available inside the enlarged all-rate instrument, so its imported upper bound and the present lower bound agree in the n^4 exponent. For 0<alpha<=1/4 they also agree in small-error logarithmic order. This comparison imports the upper theorem and its separate review; it does not re-prove a new all-alternative certificate at the asymptotically optimal hard-pair rate.

The Sibuya law, Joe family, binomial series, covariance inequality, power comparison, KL bound, and change-of-measure method are inherited mathematics. The new bounded synthesis is the all-rate information envelope, its adaptive transport for this interface, and the global asymptotic design calculation. SOURCE_AUDIT.md records the precise local and external inspection scope, and NEGATIVE_CONTROLS.md preserves failed bounds and numerical limitations.

No probability-model result here validates selectable true rates, threshold retention, route independence, common calibration, actual productive occurrences, physical architecture, or psychological interventions. Count labels are labels of the stipulated route model. There is no physical experiment, empirical sampling, protected integration, or T20 closure.
