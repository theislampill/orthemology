# Polynomial-sample recovery of primitive grouped-count support

8 October 2026 UTC. New mathematical sibling of the frozen grouped-calibration-invariants stage. The earlier population theorem explicitly did not provide this sampling guarantee. No physical experiment, actual calibration verification, efficient runtime, kernel result, protected integration, owner acceptance or T20 closure is claimed.

## 1. The conditional statistical result

Let M>=3 and C>=1 be known integers. Let w be a known rational number with 0<w<=1. An unknown one-root count mixture is supported on 0,...,M, has at most C distinct supported counts, and every nonzero component weight is at least w. This includes the weight of count zero if zero is present. A positive lower bound only for positive-count components would not certify the zero-presence flag.

At nominal command x0=1/M, the unknown actual route success probability a is fixed and satisfies

1/(2M) <= a <= 3/(2M).

Write t=1-a. The actual calibration is common to every count component. At the start of each group, independently draw one count J from the same fixed mixture. Retain it for R=2C repetitions, whose no-hit endpoints are conditionally independent Bernoulli variables with parameter t^J. The full groups are independent. Distinct route occurrences obey the inherited independent-copy response law; sharing a numerical calibration rate does not mean sharing one random gate across all copies.

The target is the increasing positive support divided by its gcd, together with the flag recording whether zero is present. For the zero-only mixture, the positive primitive vector is empty and the zero flag is true. Absolute counts are not the target.

Define

epsilon = 1/(32 M^2),
Delta = (w/2) epsilon^(2C) / 4^C,
tau = Delta/8,
Q = ceil(32C/Delta).

For 0<delta<=1/2, a finite rational-grid estimator described below recovers the target with probability at least 1-delta from any integer number of groups satisfying

n >= 32 Delta^(-2) log(4C/delta).

Total endpoint observations are 2C n. Since Delta=w/[2^(12C+1) M^(4C)], the sufficient group budget is

n >= [2^(24C+7)/w^2] M^(8C) log(4C/delta).

At fixed C,w this is O(M^(8C) log(1/delta)). The exponent and constants are not claimed optimal. The constants are very large; this is a mathematical sampling bound, not a proposed practical experiment. Polynomial in the numerical count bound M is not polynomial in its binary input length log M. No useful runtime or bit-complexity bound is claimed.

The rate interval corresponds to a pointwise absolute calibration tolerance 1/(2M) around the command. A global static calibration-error promise of that size would imply this pointwise condition, but the proof needs only the displayed common fixed rate. No derivative, global invertibility, or full command-response curve is used.

## 2. Uniform scalar geometry

Every component atom is q_j=t^j. The permitted survival interval is

T=[1-3/(2M), 1-1/(2M)],

which is contained in (0,1). We first prove q_j>=1/8 for every j<=M. Set lambda=3/M<=1. Concavity of log gives

log(1-lambda/2) >= lambda log(1/2),

because 1-lambda/2=(1-lambda)*1+lambda*(1/2). Multiplying by M shows (1-3/(2M))^M>=1/8. Since t>=1-3/(2M) and j<=M, q_j>=t^M>=1/8.

Distinct atoms in one world are separated by at least

gamma=1/(16M).

Indeed adjacent count means differ by t^j(1-t)>=t^M/(2M)>=1/(16M); nonadjacent gaps are no smaller. The zero-count atom is one, whereas every positive-count atom is at most t<=1-1/(2M).

### A separation lemma for different primitive targets

Let A={t^j:j in J} and B={s^ell:ell in L} be two eligible scalar supports, with both t,s in T and all counts in 0,...,M. Let h be their Hausdorff distance in the ordinary absolute-value metric. If

h < epsilon=1/(32M^2),

then they have the same primitive target and zero flag.

First, 2h<gamma. Every point has a unique nearby point in the other set; the map is injective in either direction because a collision would violate the within-world gap. Thus the correspondence is a bijection and preserves order. The atom one cannot be matched to a positive-count atom, whose distance from one is at least 1/(2M)>epsilon. Hence zero flags agree. If there are no positive counts, both supports are the zero-only support and the conclusion already holds.

Otherwise match the increasing positive counts as j_i and ell_i. Put u=-log t and v=-log s. Since all scalar atoms lie in [1/8,1], the mean value theorem gives

|j_i u-ell_i v| <= 8h,
u >= 1-t >= 1/(2M).

For any two matched indices i,k, cancellation of the unknown v gives

|(j_i ell_k-j_k ell_i)u|
<= (ell_k+ell_i)8h
<=16Mh < 1/(2M) <= u.

The determinant j_i ell_k-j_k ell_i is an integer, so it must be zero. All positive count ratios agree. By integer gcd normalization, the primitive positive vectors agree. For a single positive component the primitive vector is simply (1), consistently with this argument.

Consequently different primitive targets or zero flags force Hausdorff distance at least epsilon. This uses an integer determinant rather than division by a small logarithm; it supplies the stronger M^-2 node separation scale.

## 3. An explicit moment gap

The decoder below allows candidate weights at least w/2. Work temporarily in that larger class, still with at most C components and the same count/rate bounds. Let mu,nu be two scalar mixing laws in this class. If their support Hausdorff distance is at least epsilon, then

max_(1<=r<=2C) |m_r(mu)-m_r(nu)| >= Delta,

where m_r is the scalar r-th moment and Delta=(w/2)epsilon^(2C)/4^C.

To prove it, one of the two supports contains an atom a whose distance from every atom of the other support is at least epsilon. Swap mu,nu if necessary so that a belongs to mu. Write the other support as b_1,...,b_s, where 1<=s<=C, and form

p(z)=product_(i=1)^s (z-b_i)^2.

This polynomial has degree 2s<=2C, is nonnegative on the real line, and integrates to zero under nu. Under mu it integrates to at least (w/2)epsilon^(2s)>=(w/2)epsilon^(2C). There is no cancellation of this contribution because all weights and p are nonnegative.

Writing p(z)=sum c_r z^r, its coefficient absolute sum is at most product_i(1+b_i)^2<=4^C. Both zeroth moments equal one, so the constant term cancels. Therefore the positive polynomial expectation difference is at most 4^C times the largest moment discrepancy among orders 1,...,2C, proving the bound.

Combining this lemma with Section 2 separates every pair of different primitive targets by at least Delta in the moment panel. The stronger version, for any supports with Hausdorff distance at least epsilon, is also useful for the separate weight-estimation extension.

## 4. The finite rational-grid estimator

The promise w is an explicit rational lower bound. If an externally warranted weight floor is a larger real number, any supplied positive rational lower bound may be used instead. No representation of an unknown real weight is assumed.

Enumerate this finite candidate list:

1. Every nonempty count support J contained in {0,...,M} of size s<=C.
2. Every weight tuple (k_1/Q,...,k_s/Q), with nonnegative integer numerators summing to Q and every weight at least w/2.
3. Every survival value t_h=1-3/(2M)+h/(MQ), h=0,...,Q.

These are rational candidates. Each candidate moment is computed exactly as sum_i (k_i/Q)t_h^(r j_i), for r=1,...,2C. Given empirical moments, select a candidate with smallest maximum absolute coordinate discrepancy, breaking ties in a prescribed finite order. Return only its primitive positive support and zero flag for the main theorem. Its absolute counts and grid weights do not automatically have their own confidence guarantees.

An equivalent acceptance version scans the finite list until finding any candidate with discrepancy at most 2tau. If none exists it returns an inconclusive result, counted as a failure. On the statistical good event a candidate is guaranteed to exist, and every accepted candidate has the proved target. This version avoids computing a global minimum; it does not make the grid small.

### Why a sufficiently close candidate exists

Keep the true count support. Round the first s-1 true weights down to multiples of 1/Q, and set the last rounded weight to make the sum one. The first weights decrease by less than 1/Q, the last does not decrease, and the total absolute weight error is at most 2(s-1)/Q<=2C/Q. This includes zero error when s=1. Since 1/Q<=Delta/(32C)<=w/(64C), every rounded weight is at least w/2.

Round the true t downward to the survival grid. The error is at most 1/(MQ), while the rounded value stays in T. On [0,1], |d(t^(rj))/dt|<=rj<=2CM. Thus the survival perturbation contributes at most 2C/Q to any moment error, and the weight perturbation at most 2C/Q. The combined error is at most

4C/Q <= Delta/8=tau.

This is an existence proof inside the enumerated finite list. The algorithm never needs to know the true weights or t to perform the enumeration, and never tests an exact equality involving an unknown real parameter.

## 5. Estimating all required moments from the same groups

For group g, let S_g be its number of no-hit endpoints among R=2C repetitions. For r=1,...,R define

U_(g,r)=(S_g)_r/(R)_r,

using falling factorials. These statistics lie in [0,1]. Conditional on one retained count and its common no-hit propensity q, the numerator counts ordered successful r-tuples, so E[U_(g,r)|q]=q^r. Hence their empirical averages hat_m_r estimate m_r without requiring the latent label.

Hoeffding's inequality and a union bound over R=2C coordinates give

P(max_r |hat_m_r-m_r| >= tau) <=4C exp(-2n tau^2).

The coordinates from one group need not be independent. Independence of the full groups is required here. Taking the stated n makes this failure probability at most delta.

On the good event, the nearby grid candidate has discrepancy at most 2tau from the empirical panel. The minimizing candidate therefore has discrepancy at most 2tau too, and is within 3tau=3Delta/8<Delta of the true moment panel. Both laws belong to the weight-floor-w/2 class. The moment-separation lemma implies their supports have Hausdorff distance less than epsilon; Section 2 then forces the correct primitive target and zero flag.

This is a finite-sample confidence theorem derived from quantitative separation. It does not infer exact support by a noisy rank or Hankel zero-test.

### Completely rational budget selection

For rational delta, let B be the least nonnegative integer such that 2^B>=4C/delta. It is found by integer/rational comparisons. Since log(4C/delta)<=B log 2<B, choosing

n=ceil[32 Delta^(-2) B]

is a fully rational sufficient budget with the same stated asymptotic order. The analytic ceiling of a transcendental logarithm need not be evaluated exactly. Q and all empirical/candidate moments likewise use rational arithmetic. The resulting finite list can be enormous; no practical exhaustive-grid run is asserted.

## 6. Why this does not identify absolute counts

The unknown rate window permits calibration error of order 1/M. The frozen global-calibration theorem already gives pure counts M-1 and M identical full response curves under static monotone calibration maps with error

eta*=[1/(2M)] [(M-1)/M]^(M-1) <1/(2M).

Both maps therefore obey the present pointwise rate window at x0=1/M. Absolute count recovery can be impossible even with unlimited command access, while their primitive positive target (1) is the same. The present theorem does not contradict that ambiguity or the earlier much smaller calibration tolerance required for polynomial absolute-count recovery.

For arbitrary mixtures the target can be nontrivial, containing several relative counts and the zero flag. The common calibration and quantitative promises stabilize those invariants. No gcd-one assumption is made, and no absolute unit count is recovered by convention.

## 7. Boundaries and evidence

The theorem requires known C,M,w, a genuinely common fixed actual calibration in the specified rate window, held latent counts with conditionally independent repetitions, and independent identically distributed groups. Arbitrary shared drift, component-specific calibration, fresh resampling within a group, or a shared random gate across route copies can invalidate the moment or geometry premises.

The calibration window keeps all scalar atoms away from zero and gives an M-dependent within-world gap. Mere interiority without such control did not supply the frozen stage's missing uniform sample guarantee. Without the weight floor, an arbitrarily rare component or zero atom remains hard to detect. Without any valid count ceiling, fixed rates can also saturate as counts grow: the separate equal-weight {n,n+1} versus pure {n} countercontrol in NEGATIVE_CONTROLS.md preserves a fixed rate and differs in primitive target. The frozen approximation countermodel is another obstruction but changes the rate as well as the counts; it is not imported under the present quantitative window. These stronger premises are doing the statistical work.

WEIGHT_ESTIMATION.md gives a separate accuracy-dependent extension for the matched weights; it is not automatically supplied by the main support budget. Exact rational controls check the geometry, polynomial coefficients, quantization and arithmetic contracts. They are deterministic tests, not collected endpoint data. The full-grid estimator and its confidence result are established by the written proof; no claim of an executed large empirical search or physical architecture follows.
