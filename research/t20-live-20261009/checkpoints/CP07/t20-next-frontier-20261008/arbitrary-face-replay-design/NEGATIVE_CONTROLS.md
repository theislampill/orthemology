# Boundaries, failed shortcuts, and exploratory history

## The old lower bound cannot simply be renamed

The fixed-rate predecessor explicitly restricts its informative pair to t=1/[3(n+1)]. Its cell floor and Delta estimate depend on that choice. They do not establish an all-rate lower bound. The new proof must control rates depending on n, asymmetric rates, and approaches to all four boundaries. The central inequality alone is insufficient.

In particular the exact concavity-gap bound g<=c(1-c)ab(xy)^(c-1) becomes poorly conditioned as xy decreases to zero. Dropping S^(m-1) from the difference-of-powers inequality loses the endpoint decay as well. Neither shortcut proves the advertised uniform theorem. The positive-mixture covariance bound and the c=1/2 comparison supply the missing tail control.

The contributing worker's independently derived three-region argument is retained separately in ../arbitrary-face-replay-design-review/UNIFORM_BOUND_AND_SHARP_ASYMPTOTICS.md. It is a valid alternate route with a looser constant; it is not the final independent review. Its future note about choosing a second command after the first bit is excluded from the present theorem and review scope.

## Literal boundaries and noncontinuous chi-squared limits

At a=0 or a=1, the first face endpoint is deterministic. At b=0 or b=1 the second is deterministic. Both worlds have the same remaining margin, hence the entire pair laws coincide. The chi-squared convention removes common zero cells and gives zero; the ratio with zero denominator is not evaluated.

There is nevertheless a positive interior limit at a=b tending to one, for each fixed n. Write x=y decreasing to zero. Then

    S=x^c[2-(2-x)^c],
    J1/x^n ->(2-2^c)^m,
    Delta/x^n ->(2-2^c)^m.

The denominator in chi-squared divided by x^(2n) tends to one, giving the limit (2-2^c)^(2m). This does not contradict equality at the exact corner. The global proof handles such limits through an exponential-in-n tail bound. A continuity-based compact maximum argument would have been invalid without this distinction.

## Preserved initial scan and cancellation failure

The first exploratory calculation used 65 decimal digits and direct subtraction for S. It scanned u=-n log(1-a), v=-n log(1-b) at decimal-quarter powers from 10^-4 to 10^4. Reported largest grid n^4 chi-squared values were approximately:

    n=1: .117749006091 at u=v=316.22777
    n=2: .192399577703 at u=v=1.7782794
    n=5: .294732628091 at u=v=1.7782794
    n=10: .344572229936 at u=v=1.7782794
    n=20: .375733948878 at u=v=1.7782794
    n=50: .397305699514 at u=v=1.7782794
    n=100: .405076349293 at u=v=1.7782794
    n=300: .410435204074 at u=v=1.7782794.

That initial exploratory script skipped nonpositive computed S values. It was not a certified search, did not exclude missed regimes, and did not establish the maximizing rate. Its approximately 1.78 grid location is superseded by the analytic positive root approximately 1.5936. The scan was useful only as a regime suggestion.

There is an explicit failure of direct high-precision subtraction: n=1,u=1000,v=1 at 80 decimal digits gives S=0 when evaluated as x^c+y^c-(x+y-xy)^c, although the true value is positive. The stable calculation instead gives positive chi-squared approximately 8.72192793566424 times 10^-435. Thus merely using many digits does not fix every unbalanced subtraction.

The final controls first order x<=y and evaluate

    S=x^c-y^c expm1(c log1p(x(1-y)/y)).

They work in logarithms thereafter and use expm1 for the small excess in J1/J0. Independent 80/160-digit agreement is checked over a bounded logarithmic grid and selected extreme regimes. This is numerical consistency evidence, not a universal certificate. The rational algebraic enclosures and universal written proof supply separate evidence.

## What the asymptotic comparison does not transfer

The 5.3168 information ratio compares the asymptotic one-pair chi-squared values of this particular hard pair at two designs. It is not a factor improvement of the predecessor's conservative all-wrong-count sample upper bound. That broader certificate used four coordinates including a fresh diagonal and was proved at its specified rate. A new broad certificate at u*/n would require its own proof.

The local KL expansion alone would apply only on compact scaled-rate families. The global KL supremum theorem additionally uses the proved all-rate escape envelopes and KL<=chi-squared; dropping that extra step would be an invalid transfer. No sharp minimax sample constant is claimed. The simpler all-rate KL upper bound sufficient for the n^4 sample lower bound also follows directly from chi-squared.

The command policy fixes both rates before each pair. Conditional-on-first-output command selection, longer replay words, gate observations, latent reuse across pairs, actual architecture certification, and unknown nominal-to-true-rate inversion remain outside this task. None is resolved by the present two-face theorem.
