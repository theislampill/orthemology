# Four isolated interaction values identify a positive multiplicity

8 October 2026 UTC. Separately scoped strengthening of RESULT.md. The fixed-inventory, independent-route, shared coordinatewise homeomorphism model is unchanged. This appendix concerns the multiplicity of a **promised positive support S with |S|>=2**. It does not identify whole calibration maps from a finite panel, silently decide absent supports from approximate data, or supply a uniform precision, runtime or sample bound.

## 1. A finite panel and its rank test

Choose distinct i,j in S. Pick two strictly ordered interior nominal commands u_1<u_2 for i and v_1<v_2 for j. Hold every other coordinate in S at any fixed interior command w_k. Coordinates outside S are zero. For each pair (p,q), form the isolated multiplicative contrast from its masked endpoint probabilities:

    Z_pq = product_(T subset S) Q(x_T^(p,q))^((-1)^(|S|-|T|))
         = (1-K a_p b_q)^n,

where n=n_S>0, a_p=r_i(u_p), b_q=r_j(v_q), and K=product_(k in S\{i,j}) r_k(w_k). The empty product gives K=1 if |S|=2. Strict monotonicity gives 0<a_1<a_2<1 and 0<b_1<b_2<1, while 0<K<=1.

All Q values in this finite masked panel are positive, since every nonzero command is interior. The panel uses at most 4 times 2^|S| endpoint-probability values; repetitions can be merged and Q(0)=1 is known. Thus these are four **isolated** values, not necessarily four raw endpoint evaluations.

For any real m>0 define a two-by-two matrix

    P_m(p,q) = 1-Z_pq^(1/m) = H_(n/m)(K a_p b_q),
    H_c(z)=1-(1-z)^c,

and let Delta(m)=P_m(1,1)P_m(2,2)-P_m(1,2)P_m(2,1). Then

    sign Delta(m) = sign(m-n),

with equality zero exactly when m=n. At m=n the matrix is K times the outer product (a_1,a_2) times (b_1,b_2), so its determinant is zero. The strict-sign theorem proves that no other positive multiplicity, even a noninteger one, fits these isolated data under separability.

This is stronger than merely saying that an exact all-command curve identifies n. It does not remove the integer/equality-oracle issue from a naive search for a zero determinant; the constructive replacement appears below.

## 2. Strict determinant sign

For c>0, let

    e_c(z)=z H'_c(z)/H_c(z),   0<z<1.

Set t=-log(1-z)>0. Direct substitution yields

    e_c(z)=c (exp(t)-1)/(exp(c t)-1).

The derivative of log e_c with respect to t is

    [f(t)-f(c t)]/t,   f(s)=s/(1-exp(-s)).

For s>0,

    f'(s)=[1-(1+s)exp(-s)]/[1-exp(-s)]^2 >0,

because exp(s)>1+s. Consequently e_c strictly decreases with z if c>1, strictly increases if 0<c<1, and is constant one if c=1.

Let g_c(h)=log H_c(exp(h)) for h<0. Then g'_c(h)=e_c(exp(h)), so g''_c has strict sign 1-c when c differs from one. Apply this to

    F(s,t)=log H_c(K exp(s+t))

on the rectangle with s=log a_1,log a_2 and t=log b_1,log b_2. Its mixed second derivative has strict sign 1-c. Integration over the nondegenerate rectangle shows that

    log H_c(K a_1 b_1)+log H_c(K a_2 b_2)
      -log H_c(K a_1 b_2)-log H_c(K a_2 b_1)

has strict sign 1-c. Exponentiation preserves the comparison of the two positive diagonal products, establishing sign Delta(m)=sign(1-n/m)=sign(m-n).

This differentiates the explicit known function H_c, not any unknown r_i. Strictly ordered true values are enough; no calibration differentiability assumption is introduced.

## 3. Integer recovery from a population Cauchy oracle

Assume each probability in the chosen finite panel is available through an oracle that, for any requested accuracy, returns a rational approximation with a certified error bound tending effectively to zero. The oracle concerns the exact population probability. An empirical frequency with a probabilistic confidence interval is a different contract.

Finite products and quotients of these positive probability values are computable to any prescribed accuracy. For division, refine a denominator's interval until a strictly positive rational lower bound is certified, which terminates because the true denominator is positive. Thus the masked product gives Cauchy access to each Z_pq in (0,1), without logarithms.

Evaluate determinants only at positive half-integers

    m=k+1/2,   k=0,1,2,... .

Here 1/m=2/(2k+1), so Z_pq^(1/m) is the unique nonnegative (2k+1)-st root of Z_pq^2. Certified rational interval bisection computes that root. The resulting determinant can be approximated with a certified shrinking interval. Since n is an integer, Delta(k+1/2) is nonzero. Refine until its interval excludes zero; this sign search always terminates under the positive-integer support promise.

A sign at k+1/2 answers the integer cut exactly:

- positive means n<=k;
- negative means n>=k+1.

To recover n without a known ceiling, try k=1,2,4,8,... until the sign is positive. This terminates because n is finite. Then binary search the integers between one and that upper bound using half-integer cuts. Finitely many sign searches return n; each sign search takes finitely many precision refinements. No exact-real equality test or transcendental-function oracle is required by this construction.

The protocol uses finitely many **distinct command vectors**, fixed before the search. It may query the corresponding probability oracles repeatedly at increasingly fine precision. This does not mean finitely many Bernoulli samples identify n exactly, nor that the amount of requested precision is uniformly bounded. Counts can be large, calibrations can make all relevant true rates very small or nearly coalesce, and each determinant can be arbitrarily close to zero.

An exact-rational input contract would be different again: if every relevant population probability is supplied as an exact rational number, finite rational arithmetic decides Z=1 and hence absence at an interior contrast. Rational nominal commands do not imply rational Q under arbitrary real calibration. That stronger contract must not be attributed to ordinary Cauchy access.

## 4. Presence and calibration remain separately scoped

If n_S=0, every Z_pq is one and every determinant is exactly zero. The half-integer sign routine then has no certified termination condition. A negative isolated log contrast, or equivalently Z<1, can eventually certify positivity through approximation, but failure to certify it does not certify absence. This appendix assumes positivity; it does not claim a general impossibility theorem for every richer experimental design or additional prior that could detect absence.

Once n is recovered, P_n has rank one. These four entries identify ratios a_2/a_1 and b_2/b_1 (and the corresponding products with K), but they generally do not identify the absolute a and b values separately. Even for K=1, sufficiently small reciprocal rescalings a_p -> lambda a_p and b_q -> b_q/lambda preserve all four products and maintain interior ordering; they can be extended to endpoint-preserving homeomorphisms through the sampled nominal points. No finite panel fixes the rest of either calibration function between unsampled commands. Other independently warranted measurements might remove this finite-panel freedom, but that is not furnished by these four isolated values.

The main result's complete calibration-map reconstruction remains a population-limit construction from the full command-indexed law. The present appendix adds a finite-panel positive-multiplicity theorem and a terminating Cauchy-oracle sign-search procedure under its explicit promise. It supplies no computability claim for exact support absence from arbitrary approximation data, uniform finite-sample bound, numerical conditioning guarantee, physical calibration certification, protected integration or T20 closure.

## Attribution and proof scope

The parent proposed the four-value determinant test and the half-integer-cut construction. Author development verified the strict elasticity argument, included fixed interior K for higher-order supports, and made the finite-panel/Cauchy-oracle contracts explicit. The elementary convexity/elasticity identity is derived here; no field-wide novelty claim or separate discovery credit for equivalent proofs is asserted. Independent review is bound separately from the main theorem.
