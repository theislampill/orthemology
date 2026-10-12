# An explicit rational obstruction to a fixed backward-heat certificate

10 October 2026 UTC. Root-authored additive mathematical diagnostic. It concerns polynomials in three variables of degree at most four. It is not an explicit construction of a square-positive functional on the entire polynomial algebra, a field-novelty claim, or a claim against the distinct pointwise heat-to-SOS statement in the inspected paper.

## 1. A strictly square-positive truncated functional without a measure

Define Λ on the 35 monomials of total degree at most four by

- Λ(1)=1;
- Λ(x_i²)=4;
- Λ(x_i⁴)=50;
- Λ(x_i²x_j²)=1 when i≠j;
- Λ(xyz)=3/2;
- every other nonconstant monomial in the domain has value zero.

For the quadratic-monomial basis

    (1,x²,y²,z²; x,yz; y,xz; z,xy),

the matrix M with entries Λ(m_i m_j) is block diagonal, with one block

    E = [[1,4,4,4],
         [4,50,1,1],
         [4,1,50,1],
         [4,1,1,50]]

and three copies of

    O = [[4,3/2],[3/2,1]].

The Schur complement of E's leading entry is 49I−15J, with eigenvalues 4,49,49. Each O is positive definite, with leading entry 4 and determinant 7/4. Hence M is positive definite. It follows that Λ(q²)>0 for every nonzero polynomial q of degree at most two, and Λ(S)>0 for every nonzero sum of squares S in its degree-four domain. This is strict square positivity at the full stated truncated scope.

But the Choi–Lam polynomial

    F=1−4xyz+x²y²+x²z²+y²z²

is globally nonnegative: AM–GM gives 1+x²y²+x²z²+y²z²≥4|xyz|. Its value under Λ is 1−6+3=−2. Therefore Λ admits no positive representing measure. No numerical semidefinite optimisation is used.

## 2. Exact heat evolution and any proposed fixed backward time

Let P_t=exp(tΔ) on the degree-four polynomial space. Its series terminates, and P_tP_(-t)=I on this space. Direct calculation gives

    P_tF=F+4t(x²+y²+z²)+12t²,
    Λ(P_tF)=−2+48t+12t².

For 0≤t≤1/100 this is at most −3797/2500<0. Positive heat time preserves sums of squares; the exact finite product identity in the accompanying heat comparison proves this algebraically. Moreover, P_t is injective on polynomials, so Λ∘P_t remains strictly square-positive on the stated domain.

For a>0 set Λ_a(p)=Λ(p(a·)) and F_a(x)=F(x/a). Dilation preserves strict square positivity. Heat covariance gives

    Λ_a(P_tF_a)=−2+48t/a²+12t²/a⁴.

Fix any proposed finite backward-heat time T≥0. Choose a>0 with a²≥100T. Then the functional

    L=Λ_a∘P_T

is nonrepresentable, since L(F_a)≤−3797/2500. Nevertheless,

    L∘P_(-T)=Λ_a

is strictly square-positive. Thus no single fixed backward-heat window yields a universal representation certificate of this form, even for the 35-dimensional ternary quartic problem.

A concrete entirely rational case is T=1,a=10. The nonnegative witness is

    F_10=1−xyz/250+(x²y²+x²z²+y²z²)/10000,

and L(F_10)=−3797/2500. EXACT_RESULTS.json gives all 35 rational values of this concrete L, permitting direct independent reconstruction.

## 3. Exact scope relative to the primary source

The inspected version is Curto–di Dio–Korda–Magron, arXiv:2211.04416v3, 26 August 2026, https://arxiv.org/pdf/2211.04416v3 . Its Corollary 3.22 on printed p.20 asserts a uniform finite heat-to-SOS time. The independently developed dilation obstruction in the accompanying comparison contradicts precisely that uniform assertion. Corollary 3.25 uses that parameter for a truncated representation criterion. The present calculation shows why replacing the nonexistent universal parameter by an arbitrary fixed time does not rescue that kind of certificate.

It does not refute the paper's separate pointwise statement that a time may depend on the polynomial. It does not invalidate the correct Choi–Lam threshold calculation in Theorem 3.12. It makes no assertion about all other claims or other versions of the paper.

The full-polynomial heat obstruction in the companion report uses a classical square-positive non-moment functional and establishes an arbitrarily long prescribed finite interval of nonrepresentation. This explicit truncated functional is a different object. No extension of the present 35 values to a full positive functional is assumed or proved.

## 4. Verification and limits

Run `python3 check_exact.py`. It reconstructs the 10×10 matrix from the 35-value definition, checks the exact block identities and positive principal minors, computes the witness and its scaled heat evolution, verifies inverse heat composition on every basis vector, and emits all concrete rational moments for T=1,a=10. A negative-mass matrix control is rejected. Arithmetic uses SymPy exact rationals and polynomial algebra, not floating-point signs. Universal nonnegativity and strict positivity are established by the written AM–GM and block-matrix arguments; finite controls supplement them.

This is not Lean verification, a measure-reconstruction algorithm, empirical evidence, protected repository integration, or T20 closure. The separate independent review is authoritative only at its recorded scope. Source PDFs are local reading intermediates; they are not included as a new redistribution.
