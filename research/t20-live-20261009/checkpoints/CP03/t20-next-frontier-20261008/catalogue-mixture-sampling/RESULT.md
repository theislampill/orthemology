# Finite-catalogue grouped sampling with an explicit calibration floor

8 October 2026 UTC. Prospective mathematical continuation only. The frozen grouped-mixture stage is imported without alteration. No protected-repository integration, owner acceptance, T20 closure, empirical trial execution, new general statistical theorem, or Lean result is claimed.

## 1. Answer and assumptions

A **known finite catalogue** of eligible histogram labels permits a finite-sample support certificate. Polynomial inversion followed by ordinary bounded-variable concentration gives an explicit confidence radius; calibration contributes a nonvanishing error allowance. The guarantee is conditional on the catalogue, process and calibration promises. It does not discover that those promises hold.

Let the known catalogue be `H_1,...,H_N`, where each `H_j=(n_{j,e})` is a finite unguarded histogram in the imported independent-route class. Its nominal base4 code is

`z_j=q(H_j)=product_e (1−4^(−e))^(n_{j,e})`,

with port rates `x_l=4^(−2^l)`. The imported injection makes distinct eligible labels have distinct nominal codes. Equivalently, this stage only needs the catalogue's codes to be known and pairwise distinct in `[0,1]`.

Unknown weights obey `w_j>=0` and `sum_j w_j=1`. Zero weights are allowed; their locations are the support-recovery question. For the main experiment:

1. Draw one catalogue index `J_g` with probabilities `w` at the start of group `g`.
2. Keep that inventory fixed throughout the group.
3. Given `J_g=j`, the `R=N−1` no-effect indicators `Y_{g,1},...,Y_{g,R}` are independent **identically distributed** Bernoulli variables with one common actual propensity `theta_j`.
4. The full groups are independent, with the same weights and fixed actual propensities across groups. Equivalently `S_g=sum_t Y_{g,t}` are independent draws from the declared mixture of `Binomial(R,theta_j)` laws.

Nominal calibration means `theta_j=z_j`. With error, assume certified deterministic bounds `|theta_j−z_j|<=beta_j`, and put `beta=max_j beta_j`. The calibration error is in the component's propensity, not an unmodeled change of inventory or dependence of repetitions. See `PROCESS_AND_LABEL_BOUNDARIES.md` for exactly which assumptions drift would change.

**N=1:** `R=0`, the sole catalogue weight is already `w_1=1` and its support is known. No observations or concentration argument are needed. Set `L_1=1`, `b_1(0)=1`, `B_1=D_1=0`. All following sampled formulas concern `N>=2` and `n>=1`.

## 2. Count contrasts recover the nominal weights

For each known code, form its Lagrange polynomial

`L_i(z)=product_(j!=i)(z−z_j)/(z_i−z_j)=sum_(r=0)^R a_ir z^r`.

It has `L_i(z_j)=1{i=j}`. Define, for `s=0,...,R`,

`b_i(s)=sum_(r=0)^R a_ir (s)_r/(R)_r`,

where `(s)_r=s(s−1)...(s−r+1)`, `(s)_0=(R)_0=1`, and `(s)_r=0` for `r>s`. These are computable exact rationals for the base4 catalogue.

**Factorial identity.** Conditional on one common propensity `theta`, `(S)_r` counts ordered `r`-tuples of distinct successful repetitions. There are `(R)_r` tuples and conditional independence gives probability `theta^r` for each. Thus

`E[(S)_r/(R)_r | theta]=theta^r`,

including `r=0`. Consequently

`E[b_i(S)|J=j]=L_i(theta_j)`.

At nominal calibration,

`E b_i(S)=sum_j w_j L_i(z_j)=w_i`.

For `n` groups, use the raw contrast estimate

`hat_w_i=(1/n)sum_(g=1)^n b_i(S_g)`.

This is a signed linear estimate. Its entries need not lie in `[0,1]`: negative estimates and values above one do not invalidate the concentration calculation and must not be presented as genuine probability weights. Since `sum_i L_i=1`, polynomial coefficient comparison gives `sum_i b_i(s)=1` for every count, so `sum_i hat_w_i=1` exactly even when entries are signed. No projection or renormalization is required for the support test below.

## 3. Exact finite ranges and simultaneous confidence

Compute the exact range of each contrast on all possible counts:

`B_i=max_(0<=s<=R)b_i(s)−min_(0<=s<=R)b_i(s)`.

This is a finite enumeration, not a numerical maximization over an interval. It remains a valid bound if some counts have probability zero. Under independent groups, the two-sided Hoeffding inequality gives

`P(|hat_w_i−E hat_w_i|>=t)<=2 exp(−2 n t^2/B_i^2)`

when `B_i>0`; if `B_i=0`, the contrast is constant and the sampling deviation is zero. For any `0<delta<1`, a union bound gives, with probability at least `1−delta`, simultaneously for every `i`,

`|hat_w_i−E hat_w_i|<=B_i sqrt(log(2N/delta)/(2n))`.

The estimates for different `i` are generally dependent because they use the same counts. A union bound does not require independence between coordinates. Independence is required across groups for this concentration step.

This is the classical Hoeffding bound, specialized to catalogue polynomial contrasts; it is not a new general theorem. For completeness, its standard exponential-moment argument can be stated in a few lines. If `X` lies in an interval of width `B`, let `h(lambda)=log E exp(lambda(X−EX))`. Then `h(0)=h'(0)=0`; `h''(lambda)` is the variance under exponential tilting. A variable supported in that same interval has variance at most `B^2/4`, because its variance is at most its mean squared distance from the interval midpoint. Integrating twice gives `h(lambda)<=lambda^2 B^2/8`. Independence, exponential Markov, and minimization at `lambda=4t/B^2` for the sample mean yield the displayed upper tail; applying it to `−X` gives the lower tail.

## 4. Certified calibration contribution

Let `D_i` be any certified upper bound for `sup_(z in [0,1]) |L_i'(z)|`. The mean value theorem gives

`|E hat_w_i−w_i| = |sum_j w_j (L_i(theta_j)−L_i(z_j))|`

`<=D_i sum_j w_j beta_j <=D_i beta`.

Thus, on the same simultaneous event,

`|hat_w_i−w_i|<=e_i(n,delta):=B_i sqrt(log(2N/delta)/(2n))+D_i beta`.

The weighted version `D_i sum_j w_j beta_j` can be used if that weighted quantity has an independently justified bound. Unknown weights must not simply be plugged into it as though known. The safe catalogue-wide `beta` is computable before observing weights.

`D_i beta` is a **calibration allowance/floor for this certificate**, not a claim that every calibration error creates exactly that bias, nor an information-theoretic lower bound. Increasing `n` only reduces the sampling term. If the allowance is already too large, this certificate cannot certify support; tighter certified calibration or a sharper valid bias calculation may help. Failure of a sufficient inequality alone proves no impossibility.

### An exact derivative certificate from the same contrasts

Write `B_(s,R)(z)=binom(R,s) z^s(1−z)^(R−s)`. The factorial identity, now for every scalar `z`, proves the polynomial identity

`L_i(z)=sum_(s=0)^R b_i(s) B_(s,R)(z)`.

For `R>=1`, differentiating and collecting adjacent terms gives

`L_i'(z)=R sum_(s=0)^(R−1)(b_i(s+1)−b_i(s)) B_(s,R−1)(z)`.

The Bernstein basis terms are nonnegative on `[0,1]` and sum to one. Therefore

`D_i:=R max_(0<=s<R)|b_i(s+1)−b_i(s)|`

is an exact rational certificate. It need not be the smallest possible derivative bound. Alternatively `sum_(r=1)^R r|a_ir|` is a valid monomial-coefficient certificate. A numerical grid maximum without a bound between grid points is not a certificate.

## 5. Exact support selection under a weight floor

Assume a declared `w_min>0` such that every weight is either zero or at least `w_min`. Define the estimated support by the raw contrasts:

`hat_A={i:hat_w_i>w_min/2}`.

If `max_i e_i(n,delta)<w_min/2`, then **on the simultaneous confidence event** `hat_A={i:w_i>0}`. Indeed, a zero weight has `hat_w_i<=e_i<w_min/2`; a positive one has `hat_w_i>=w_min−e_i>w_min/2`. Therefore the support is exactly recovered with probability at least `1−delta`. Weight values themselves are only estimated to the stated error; finite observations do not yield exact arbitrary real weights.

A sufficient sample-size condition is that every margin `m_i=w_min/2−D_i beta` be positive and

`n>max_i [B_i^2 log(2N/delta)/(2m_i^2)]`.

An integer strictly larger than that expression suffices. Equality of total error with the half-floor leaves no strict separation and is deliberately excluded.

Optional coordinatewise clipping `clip(x)=min(1,max(0,x))` cannot increase distance to any true `w_i in [0,1]`, and for a threshold in `(0,1)` it does not change whether `x` exceeds that threshold. Thus it is harmless for this support decision. It generally destroys the exact unit sum, and additional renormalization or other projections need separate analysis; none is used here.

## 6. Port-rate errors imply a code-error certificate

For a route support `S_e={l: the l-th binary bit of e is 1}`, its success probability under port rates `x` is `p_e(x)=product_(l in S_e)x_l`. Assume all nominal and actual rates are in `[0,1]`, `|x_l−x'_l|<=epsilon_l`, and the actual route model retains both this route-success product and independence of route-success events. Then

`q_H(x)=product_e(1−p_e(x))^(n_e)`.

For numbers `a_t,b_t in [0,1]`, telescoping their products gives

`|product_t a_t−product_t b_t|<=sum_t |a_t−b_t|`,

because every remaining product multiplier is at most one in absolute value. First apply this within one route to get `|p_e(x)−p_e(x')|<=sum_(l in S_e)epsilon_l`. Apply it again to the list of all route occurrences, including multiplicities, to obtain

`|q_H(x)−q_H(x')|<=sum_e n_e sum_(l in S_e)epsilon_l`.

Since both propensities lie in `[0,1]`, a certified bound is

`beta_H=min(1, sum_e n_e sum_(l in S_e)epsilon_l)`.

Only finitely many terms occur for each catalogue histogram. Overlap between route supports does not license independence of their successes; that is an explicit model premise here. Marginal port-error bounds alone do not justify the product law when routes share randomness or have hidden guards.

## 7. Concrete exact controls and a disclosed sufficient budget

All computations below are finite exact rational controls, with no generated empirical samples. The script additionally reconstructs the entire Bernstein polynomial and derivative polynomial exactly; finite checks do not replace the general proofs.

For the actual one-port catalogue with zero, one, or two copies of support `{0}`, nominal codes are `(1,3/4,9/16)` and `R=2`. In catalogue order, the count contrast values at `s=0,1,2` are

- `b_1=(27/7,−15/7,1)`, `B_1=6`, `D_1=12`;
- `b_2=(−12,14/3,0)`, `B_2=50/3`, `D_2=100/3`;
- `b_3=(64/7,−32/21,0)`, `B_3=32/3`, `D_3=64/3`.

For a conservative scale example, take `delta=1/20`, `w_min=1/3`, `beta<=1/1000`, and `n=40,000` independent two-repeat groups, hence `80,000` endpoint observations. A port-rate error at port zero of at most `1/2000` certifies this `beta`, since the maximum route multiplicity is two. The largest calibration allowance is `1/30`, and the remaining half-floor margin is `2/15`. Since `log(120)<5` and

`(50/3)^2 * 5/(2*40,000)=5/288 < (2/15)^2`,

every total error is strictly below `1/6`. The support certificate therefore has confidence at least `0.95`. The logarithm comparison can be certified from a finite positive Taylor sum for `exp(5)`. This is an illustrative sufficient design, not an optimal sample complexity or a report of an executed experiment.

An additional two-label control takes codes `(1,3/4)`, true weights `(0,1)`, actual port rate `7/32`, and `beta=1/32`. Its contrast expectations are `(1/8,7/8)`. With `delta=1/10`, `n=256`, and `log(40)<4`, the bound is strictly below the half-floor `1/2`. At actual rate `1/8`, however, expectations are `(1/2,1/2)`: applying the strict threshold to that population-limit vector selects neither label. Finite-sample decisions at this boundary can fluctuate; convergence to a tie does not imply eventual selection of neither label. At actual rate `1/16`, the expectations are `(3/4,1/4)` and the threshold selects the wrong label, with a strict margin. Independent groups converge to these biased expectations, so the latter wrong support is eventually selected almost surely. These examples show why the strict floor condition matters and exhibit a genuine failure beyond the floor, rather than merely a loose bound.

Controls also cover one through five catalogue labels, mixed two-port supports, capped port-error sums, an exact finite-sample tail calculation, a dependent-group adversary, and separated unknown-label perturbations. See `results/exact_controls.json` for full rational output and `results/exact_controls.log` for execution status.

## 8. Limited comparison with separate moment confidence intervals

One alternative estimates each normalized factorial moment by its group average. Every such count statistic lies in `[0,1]`; the order-zero moment is exactly one. A union bound over orders `1,...,R` gives moment error at most `sqrt(log(2R/delta)/(2n))`. Applying the polynomial coefficients yields weight sampling error

`C_i sqrt(log(2R/delta)/(2n))`, where `C_i=sum_(r=1)^R |a_ir|`.

Because every normalized factorial count lies in `[0,1]`, `B_i<=C_i`. This explains the benefit of applying concentration directly to the combined contrast before taking a union bound. The two displayed bounds have different logarithmic factors, so no universal dominance claim is made without comparison.

For the three-label example, `C=(148/7,164/3,704/21)`, substantially larger than its exact ranges. There is no broad optimization claim over group lengths, other estimators, calibration designs, or sparse-model methods.
