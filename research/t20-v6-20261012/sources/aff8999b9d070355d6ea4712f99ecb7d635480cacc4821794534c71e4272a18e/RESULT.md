# Effective search for a finite nonnegative-polynomial separator

10 October 2026 UTC. Separate optional addendum to the frozen valid-initial-partial-escape-20261010 theorem. Root proposed the effective-search question. This note supplies an ordinary proof of the bounded computability claim; it neither changes that frozen packet nor claims an implemented witness search, a computed separator, or kernel verification.

## 1. Bounded statement

Use exactly the explicit r=1, k=2, g_t(z)=z^2 construction in valid-initial-partial-escape-20261010/RESULT.md, with its dyadic-rational Schur functional Lambda, specified integer radii, finite signed blocks rho_n, positive hidden measure N, and continuous/discrete lognormal pair alpha,beta. Let

    F(u,v)=1+u^4v^2+u^2v^4-u^2v^2 >=3/4.

For every supplied rational t>0, there is a terminating algorithm that outputs a rational-coefficient polynomial q(z) and a rigorous strict-negative interval enclosure proving

    L_t(q(z)^2 F(u,v))<0.

The output polynomial is globally nonnegative. Every polynomial-square test still has strictly positive L_t value, by the separate ordinary theorem. This is a finite nonnegative-polynomial separator, not a failed square test.

The algorithm need not have a practical running time, modest degree, or modest coefficient size. No actual q or runtime bound is produced here. The computability and strict-sign semidecision principles are standard; the claim is their application to this explicitly constructed path, with every required tail modulus supplied.

## 2. Computable hidden moments with an explicit tail modulus

The base functional Lambda has a total exact rational moment algorithm from the inherited Schur recurrence. Hence each residual, integer radius R_n, finite signed block rho_n, and its positive/negative atomic parts can be computed exactly by finitely many rational operations and comparisons. Their finite supports have integer coordinates.

Write

    N_<=M = sum_(n=1)^M rho_n^-.

The frozen construction proves, for every 0<=d<n,

    integral |y|^d d|rho_n| <= 2^(-n).                            (2.1)

For any rational polynomial p(y)=sum_alpha p_alpha y^alpha, let D=deg p and B_p=sum_alpha |p_alpha|. For every M>=D,

    |N(p)-N_<=M(p)|
       <= sum_(n>M) integral |p| d rho_n^-
       <= B_p sum_(n>M)2^(-n)
       = B_p 2^(-M).                                             (2.2)

The constant term is covered by d=0. Every term in the finite approximant is rational. Thus the values N(p) are uniformly computable, with a known error bound rather than just a qualitative convergence assertion.

Because F>=0, its partial values increase. Its four coefficients have absolute sum 4 and degree 6, so for M>=6,

    N(F) belongs to [N_<=M(F), N_<=M(F)+4*2^(-M)].                (2.3)

Similarly n_0=N(1) and C=1+n_0 are computable. For the mass, one can use the sharper bound N(1)-N_<=M(1)<=2^(-M-1), since each zero-mass block has negative mass equal to half its total variation. Nothing here requires deciding a limiting real equality.

## 3. Computable active moments

Let X be standard Gaussian and put

    I_m(t) = integral z^m exp(-tz^2) d alpha(z)
           = E[exp(mX-t exp(2X))],

    J_m(t) = integral z^m exp(-tz^2) d beta(z)
           = S^(-1) sum_(j in Z) exp(-j^2/2+mj-t exp(2j)),
    S = sum_(j in Z) exp(-j^2/2).

For integers m>=0 and rational t>=0, these are uniformly computable real numbers. The following explicit tail bounds justify the claim without inferring unbounded integration from weak computability alone.

### Continuous lognormal integral

Because exp(-t exp(2X))<=1, for any real R>m,

    E[exp(mX-t exp(2X)) 1_(|X|>R)]
       <= E[exp(mX) 1_(|X|>R)]
       <= 2 exp(m^2/2) exp(-(R-m)^2/2).                           (3.1)

Completing the Gaussian square gives the shifted Gaussian tails. The standard Chernoff bound P(X>a)<=exp(-a^2/2), for a>=0, proves the last inequality; it follows directly from E exp(aX)=exp(a^2/2).

On [-R,R], the integrand with Gaussian density is an explicitly computable smooth function

    f(x)=(2pi)^(-1/2) exp(mx-t exp(2x)-x^2/2).

A computable upper bound on its derivative is

    |f'(x)| <= (m+2t exp(2R)+R) exp(mR).                         (3.2)

Here (2pi)^(-1/2)<1, exp(-t exp(2x))<=1 and exp(-x^2/2)<=1 were only used to enlarge the bound. Rational upper approximations to the right side, an ordinary uniform Riemann mesh, and interval evaluation of the elementary functions give a rigorous finite integral enclosure of any requested width. Choosing R by (3.1) and then refining the mesh therefore computes I_m(t). No numerical black-box quadrature assumption is needed.

### Discrete lognormal sum

For |j|>=4m,

    exp(-j^2/2+mj-t exp(2j)) <= exp(-j^2/4).

Consequently, if J+1>=max(1,4m), the two-sided omitted numerator tail obeys

    sum_(|j|>J) exp(-j^2/2+mj-t exp(2j))
       <= 2 exp(-(J+1)^2/4) / [1-exp(-(2J+3)/4)].                (3.3)

The bound is a geometric comparison of successive exp(-j^2/4) terms. It is uniform for t>=0. The same kind of bound at m=0 computes S; also S>=1, so division is computable without a zero-denominator issue. The finite numerator sum contains only computable elementary values. Thus J_m(t) has arbitrarily narrow rigorous interval enclosures.

For a rational polynomial q, expand q^2 into finitely many monomials. The integrals I_t(q^2) and J_t(q^2) are computable finite linear combinations of these active moments. Coefficient cancellation does not affect computability because the error budget can be divided among the finitely many terms.

## 4. The path coordinates are themselves computable

For a mixed monomial z^m u^a v^b, the normalizing factor C cancels, giving

    L_t(z^m u^a v^b)
       = [Lambda(u^a v^b) I_m(t) + N(u^a v^b) J_m(t)]
          / [I_0(t)+n_0 J_0(t)].                                (4.1)

Every numerator quantity is uniformly computable by Sections 2-3. The denominator is positive. More explicitly, both active laws have second moment exp(2), so Jensen's inequality gives

    I_0(t)>=exp(-t exp(2)),  J_0(t)>=exp(-t exp(2)),
    I_0(t)+n_0J_0(t)>=(1+n_0)exp(-t exp(2))>0.                   (4.2)

One may compute a positive rational lower bound from (4.2) and budget division error directly. Thus all path coordinates are computable uniformly in rational t>=0 and the finite multi-index. This is not a general claim about arbitrary unknown square-positive hierarchies or arbitrary non-effective supplied schedules.

## 5. Guaranteed finite separator search

Set B=N(F), a computable nonnegative real. For each rational polynomial q define the computable real

    W_t(q) = -I_t(q^2) + B J_t(q^2).                              (5.1)

The frozen construction gives

    A_t(q^2 F)=W_t(q)/C,
    L_t(q^2 F)=W_t(q)/[I_0(t)+n_0J_0(t)].                         (5.2)

Therefore its sign is exactly the sign of W_t(q). Neither C nor the normalizer needs to be approximated to find the separator.

The density argument in the frozen theorem proves that some real-coefficient polynomial q has W_t(q)<0. Its degree is finite. On that fixed finite-dimensional coefficient space, W_t is a quadratic form with finite entries, hence continuous in the coefficients. Rational coefficient vectors are dense, so some rational polynomial also has strictly negative W_t value.

Enumerate every rational-coefficient polynomial, and dovetail this enumeration with increasingly accurate interval enclosures for W_t(q). Accept as soon as the upper endpoint of one enclosure is strictly negative. The accepted q is sound by (5.2). A strictly negative rational q exists, so its enclosure eventually has negative upper endpoint and the entire search terminates.

Dovetailing is essential: one must not wait for a sign decision for an earlier zero-valued candidate. Strict negativity of a computable real is semidecidable; equality is not being decided. The output's everywhere-nonnegative property follows symbolically from q^2>=0 and F>=3/4, not from sampling polynomial values.

This proves a terminating finite witness-search guarantee for each rational t>0. It does not give a uniform degree bound, a cost estimate, a low-degree diagnostic, an algorithm deciding arbitrary moment representability, or an executed interval certificate.

## 6. Prior mechanisms and evidence limits

The project already uses effective tails, computable strict inequalities and dovetailed searches, for example in determinate-moment-effectivity-20261010/RESULT.md. Its compact-fibre recovery theorem is not used here: this initial record is indeterminate, and the search is over an explicit computable negative polynomial evaluation, not over possible representing laws. This note claims no new general semidecision principle.

The exact rational computability of Lambda is supplied by the ordinary full-polynomial Schur recurrence; that computational claim is distinct from the later noncomputable Lean definition of its algebraic counterpart. Sections 2-5 are ordinary arguments. No code implementing the active integral enclosures or separator enumeration was run, and no particular q was computed. The frozen predecessor's existence and nonrepresentability proof remains independent of this optional effectivity result.
