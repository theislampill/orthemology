# Independent narrow review: audit loss and quadratic tail repair

11 October 2026 UTC. Independent mathematical reading of the proposed application, not author/source edits, repository integration, formal verification, field-priority research, or programme closure.

## Verdict and essential qualification

The proposed coefficients and certificate are correct. The important effectivity qualification is that the restored prior has infinite first moment and therefore cannot itself furnish the full finite-moment input required by the effective-continuation predecessor. Construct a new full moment name at computable positive time before invoking that theorem. A mere existence assertion about moments would not suffice.

## Exact derivation

For n in N_0 let C0=sum_(n>=0)(n+1)^(-2), so 1<=C0<=2 (integral comparison), and μ(n)=1/[C0(n+1)^2]. The calibrated report factor L(n)=(n+1)^2/4^n lies in (0,1]. Its predictive normalizer is 4/(3C0) and its posterior is ν(n)=(3/4)4^(-n). The latter has an exponential moment exactly for exponents b<log 4; its moment at log 4 diverges. The positive audit factor 1/L restores μ, which has no positive ordinary exponential moment and no finite first moment.

Apply the independently retained objective F(x)=x²/2 to this restored supplied law, with the inherited unit transport/reaction convention. Then

- X_t(n)=e^(-t)n;
- K_t(n)=integral_0^t F(X_s(n)) ds=c_t n²;
- c_t=(1-e^(-2t))/4;
- Z_t=sum_n μ(n)e^(-c_t n²), with 1/C0<=Z_t<=1;
- μ_t=(X_t)_#[e^(-c_t n²)μ/Z_t].

For t>0 set a_t=c_t e^(2t)=(e^(2t)-1)/4. Direct cancellation gives

    integral exp(a_t x²) dμ_t = 1/Z_t <= C0 <= 2.

Completing the square gives b x <= a_t x²+b²/(4a_t), and hence for every finite real b,

    integral exp(bx) dμ_t <= 2 exp(b²/(4a_t)).

All positive ordinary exponential moments thus return at positive time. This does not give a bound uniform down to t=0: for any b>0, finite-sum limits and divergence of sum μ(n)e^(bn) show the exponential moment tends to infinity as t decreases to zero. On any delayed interval t>=τ>0, replacing a_t by a_τ does give a uniform certificate.

## Effective moment input: explicit terminating construction

For computable t>0 let

    S_r(t)=sum_(n>=0) n^r exp(-c_t n²)/(n+1)²,
    m_r(μ_t)=e^(-rt)S_r(t)/S_0(t),

with 0^0=1 for grade zero. We have S_0>=1, and C0 cancels. Choose a positive rational d<c_t and an integer N with N+1>=max(1,2/d). Since n^r<=r!e^n and n-dn²<=-dn²/2<=-dn/2 beyond N,

    sum_(n>N) n^r exp(-c_t n²)/(n+1)²
        <= r! exp[-d(N+1)/2]/(1-exp[-d/2]).

This tends effectively to zero, uniformly in the requested integer grade and accuracy. Finite computable sums plus the known lower denominator bound compute the full moment name. Rational strict majorants of the tail coefficients give purely rational error searches if desired. C0 is also computable by its elementary summation tail, so Z_t and the Gaussian certificate value are computable.

Choose any computable b>0 and supply a computable rational M>2 exp[b²/(4a_t)]. The exponential-tail-effectivity RESULT §2 input contract is now met. Its E2 applies for u>-b; an equality endpoint does not follow from E2 using only that certificate. In this particular stronger Gaussian class, any finite ordinary tilt u can instead be covered by choosing a larger ordinary exponent b>max(0,-u), so the operation becomes strictly interior relative to that stronger supplied certificate. This does not contradict either predecessor endpoint obstruction.

## Theorem L interpretation and edge conditions

The transfer inequality is correct under its stated budget condition η A_t+γ<=β. If A_t=0, the separate direct estimate integral exp(ηΩ) <= exp(ηB_t) holds for every finite η>=0, regardless of γ or β. The displayed C M/Z_R bound should not be extended outside its stated condition: C M/Z_R need not be >=1 when γ>β.

For A_t>0, β>γ guarantees a positive available exponent; equality permits only η=0 under this sufficient test. Budget failure is failure of this certificate, not a general impossibility theorem. The quadratic repair starts with a law having no initial exponential certificate, so it is a direct combined-weight estimate rather than a black-box invocation of L on that law. A damping bound of one alone would not show regeneration.

Theorem L's general integral proof and the countable example extend beyond the earlier finite-origin setup; make that countable domain explicit in the application. No substantive defect results because all relevant sums are nonnegative and the normalizers are positive and finite.

## Predecessor ownership and semantic ceiling

Inspected sources:

1. received-authorial-synthesis-20261011/extracted/Orthemology_T20_111min_Recovered_Authored_Work_20261010/Cross_Front_Theorems.md, §15: audit envelope lemma and the exact heavy-prior/geometric-posterior loss example.
2. full-law-gradient-action-tail-20261010/RESULT.md, §§1, 4, 5: supplied arbitrary-law characteristic formula, positive-time polynomial moments, and explicit quadratic characteristic/weight. Its finite-action conclusion is unconditional only after positive time; no length-from-zero claim is needed here.
3. exponential-tail-effectivity-20261010/RESULT.md, §§2–4, 6–7: represented full-moment inputs, effective strict-interior continuation, endpoint controls, and stronger-envelope restoration of interiority.
4. The bound ancestor nonconvex-atomic-limit-classification-20261010/RESULT.md, §5, equations (23)–(25), and quadratic control: positive-time regularization already proved for arbitrary supplied laws; quadratic X=ze^(-t), I=z²/4, R=X²/4 already explicit.

The addition is the constructive application joining source withdrawal to an inherited corrective law, including its explicit computable re-entry certificate. It is not a new general probability, regularization, or effective-continuation theorem. The retained objective, unit action convention, current law, and starting clock must be declared. Withdrawal/restarting does not recover an old evolved history or cover a changed objective without a new analysis. No empirical source reliability, noetic warrant, or ontological conclusion follows from the calculation.

The equations and estimates above were independently checked algebraically. No numerical experiment or finite enumeration is presented as a proof of their universal assertions.
