# Polynomial sampling and uniform calibration error

This separate appendix uses exactly the fixed-count and static-calibration model of `RESULT.md`. It does not modify that main theorem. It gives a global efficiency distinction sharper than comparing the main identifiability threshold with one earlier tuned command: at fixed confidence, the uniform calibration tolerance scale for the existence of some polynomial-budget procedure is log(M)/M^2 for a catalogue of counts 0,...,M. The constants and polynomial exponents below are deliberately conservative.

## 1. Exponential lower bound from clipped static maps

For the adjacent counts k,k+1, k>=1, let the boundary maps from the main theorem be written

    r_k^*(x)=x+d(x),       r_(k+1)^*(x)=x-d(x),

where d(x)>=0. In the integer-power parameterization,

    x=1-(u^(k+1)+u^k)/2,
    d=u^k(1-u)/2,          0<=u<=1.

Given any eta>=0, define the clipped maps

    r_k(x)=min{r_k^*(x),x+eta}=x+min{d(x),eta},
    r_(k+1)(x)=max{r_(k+1)^*(x),x-eta}=x-min{d(x),eta}.

Both maps are continuous and strictly increasing: the minimum of two strictly increasing continuous functions is strictly increasing and continuous, and so is their maximum. They preserve endpoints, have uniform error at most eta, and stay in [0,1]. For example x<=r_k(x)<=r_k^*(x)<=1 and 0<=r_(k+1)^*(x)<=r_(k+1)(x)<=x. They are one fixed map per world, independent of the protocol or its realized history.

### 1.1 Where the two worlds can differ

Where d(x)<=eta, clipping changes neither boundary map, so the two endpoint distributions agree exactly. Where d(x)>eta, the maps become x+eta and x-eta. The count-k no-hit probability increases from the common boundary value q_*, while the count-(k+1) probability decreases from q_*. Consequently

    0 <= q_k(x)-q_(k+1)(x) <= q_k(x)=(1-x-eta)^k.

No clipping of the rate range is hidden in this display. In this region x+eta<r_k^*(x)<=1 and x-eta>r_(k+1)^*(x)>=0.

The boundary error satisfies the useful inequality

    d(x) <= x/(2k+1).

Indeed, after substituting u, this is equivalent to

    u^k[(k+1)-ku] <= 1.

The left side is nondecreasing on [0,1], since its derivative is k(k+1)u^(k-1)(1-u)>=0, and equals one at u=1. Therefore d(x)>eta implies

    x>(2k+1)eta,        x+eta>2(k+1)eta.

Using 1-z<=exp(-z), the pointwise total-variation distance between the two Bernoulli endpoint laws is bounded by

    |q_k(x)-q_(k+1)(x)| <= exp[-2k(k+1)eta]

at every command. Where d(x)<=eta the left side is zero, so the same bound holds there too.

### 1.2 Adaptive transcript consequence

Couple an arbitrary randomized adaptive policy using the same internal randomness in both worlds. Until the first differing endpoint outcome, its histories and next commands agree. Conditional on such a common history, maximal coupling of the next Bernoulli draws disagrees with probability at most the preceding pointwise bound. A union bound over at most N endpoint trials gives

    TV(P_k,P_(k+1)) <= min{1,N exp[-2k(k+1)eta]}.

Uniform success probability at least 1-delta in both worlds, for delta<1/2, requires the event 'return k' to differ in probability by at least 1-2delta. Thus every such fixed-budget procedure satisfies

    N >= (1-2delta) exp[2k(k+1)eta].

As throughout the main theorem, failure to return the correct count includes abstention or nontermination. This is a fixed-budget bound, not an expected-stopping-time assertion. At eta>=eta_k^* the unclipped maps already agree everywhere and the main theorem gives the stronger conclusion of impossibility at every budget.

For a full fixed-count catalogue 0,...,M, M>=2, the last adjacent pair gives

    N >= (1-2delta) exp[2M(M-1)eta].

In particular, a calibration budget eta=c/M with any fixed c>0 is exponentially expensive in M whenever uniform identification is possible at all. If that budget is at or beyond the exact main threshold, identification is impossible instead. The earlier exact-calibration order-M^2 lower bound also remains applicable because the nuisance class always contains the identity map; the exponential lower bound is not intended to replace it at eta=0.

## 2. A polynomial-budget sufficient construction

Fix M>=2, and assume

    0<=eta<=1/(16M).

Choose the single nominal command

    x=max{1/M,8M eta}.

Then 1/M<=x<=1/2 and eta<=x/(8M). Put

    A=1-x-eta,       B=1-x+eta.

These obey 0<A<=B<1 and B>=1/2, so there is no rate clipping. As in the main catalogue proof, it suffices to bound the gap between the final adjacent pair:

    g=A^(M-1)-B^M.

Since A/B=1-2eta/B lies in [0,1], Bernoulli's inequality gives

    g = B^(M-1)[(1-2eta/B)^(M-1)-B]
      >= B^(M-1)[x-eta-2(M-1)eta/B]
      >= B^(M-1)[x-(4M-3)eta]
      >= (x/2) B^(M-1).

The final inequality uses eta<=x/(8M), since (4M-3)/(8M)<1/2. Also B>=1-x, and log(1-x)>=-2x for 0<=x<=1/2. Therefore

    g >= (x/2) exp[-2(M-1)x] > 0.

All preceding adjacent intervals separate as well, and their gaps are larger, by the ordering argument in the main theorem. One empirical-frequency decoder with midpoint thresholds and the two-sided Hoeffding bound thus succeeds with any target error 0<delta<1/2 using

    N=ceil[8 x^(-2) exp[4(M-1)x] log(2/delta)]

trials. This is a sufficient budget, not the minimal budget. Since x>=1/M and x<=1/M+8M eta, a simpler, looser sufficient bound is

    N=ceil[8 e^4 M^2 exp[32M(M-1)eta] log(2/delta)].

The construction uses only the known error bound eta and maximum count M. It does not require knowing the actual calibration map, and it is valid uniformly over the monotone static maps in the stated class. In fact, its positive result uses only the pointwise calibration bound and the fresh endpoint law at this chosen command.

## 3. Exact polynomial-versus-superpolynomial tolerance scale

Fix delta in (0,1/2), independent of M. Let eta_M>=0 be a known sequence of allowed uniform errors. Say that the sequence admits polynomial-budget uniform identification if some constants C,p<infinity and some procedures identify every fixed count 0,...,M with error at most delta, uniformly over every allowed calibration map, using at most C M^p endpoints for all sufficiently large M.

Then this property holds if and only if

    eta_M = O(log(M)/M^2).

Necessity: the clipped-map lower bound forces

    eta_M <= [p log(M)+log(C)-log(1-2delta)]/[2M(M-1)].

If eta_M reaches the main nonidentifiability threshold, no finite-budget method exists, which is stronger. Otherwise the displayed inequality already gives the stated order requirement.

Sufficiency: if eta_M<=c log(M)/M^2 eventually, then eta_M<=1/(16M) eventually and the sufficient construction applies. Its simpler budget is at most

    ceil[8e^4 M^(32c+2) log(2/delta)]

for all sufficiently large M. This is polynomial in M for each fixed c. No optimal exponent, sharp constants, or optimal dependence on confidence are asserted.

## 4. Three distinct regimes and exclusions

The distinctions are now explicit:

1. Exact calibration, or the earlier small order-M^(-2) tolerance at x approximately 1/M, supports the familiar order-M^2 sampling scale up to confidence and constant factors.
2. Allowing some polynomial sample budget permits uniform error as large as a constant times log(M)/M^2; the polynomial exponent may grow with that constant.
3. Bare identifiability persists up to the sharp order-M^(-1) threshold in the main theorem. At error c/M it is either exponentially expensive or impossible, depending on c and the exact threshold.

This appendix does not identify the sharp minimax exponent between those scales, claim that its Hoeffding budget is optimal, extend to expected stopping times, address arbitrary count mixtures, or certify any physical calibration or causal model. It does not authorize integration or T20 closure. Its review must be bound separately from the main theorem's review.
