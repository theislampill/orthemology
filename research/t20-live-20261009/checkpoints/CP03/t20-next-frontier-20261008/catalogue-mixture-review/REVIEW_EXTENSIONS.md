# Two scoped robustness extensions

Independent reviewer derivation, 8 October 2026 UTC. This supplements, and does not edit, the author's narrower frozen result. These are elementary sensitivity/coupling arguments for the same count contrast. They are not claimed as new general probability theorems or physically warranted process assumptions.

Use the author's known distinct catalogue codes `z_j`, group length `R=N−1`, and count contrasts `b_i(s)`. Define

`c_i=max_(0<=s<R)|b_i(s+1)−b_i(s)|`, `D_i=R c_i`,

and `B_i=max_s b_i(s)−min_s b_i(s)`. For `R=0`, set `c_i=D_i=B_i=0`; the sole weight is known.

## 1. Independent unequal propensities within a group

Conditional on catalogue label `j` in group `g`, suppose repetitions are independent Bernoulli variables with possibly unequal propensities `theta_(g,j,t)`. Assume certified bounds

`|theta_(g,j,t)−z_j|<=beta_(g,j,t)`.

Let `F_i(theta_1,...,theta_R)=E[b_i(sum_t Y_t)]` under their product law. Hold every coordinate except `t` fixed. If `S_−t` is the count from the others, then

`F_i(theta)=theta_t E[b_i(S_−t+1)]+(1−theta_t)E[b_i(S_−t)]`.

Changing only `theta_t` therefore changes `F_i` by at most `c_i` times the propensity change. Telescoping from `(z_j,...,z_j)` to the actual vector gives

`|F_i(theta_(g,j,*))−1{i=j}|<=c_i sum_t beta_(g,j,t)`.

If every bound is at most a common `beta`, this is at most `D_i beta`, exactly the calibration allowance in the author's theorem. Thus the common-propensity restriction can be relaxed without worsening that allowance, provided conditional independence and individual propensity-error certificates remain warranted.

The power-moment identity itself need not survive: for two independent propensities `1/2` and `1`, the normalized second factorial moment is `1/2`, whereas `(3/4)^2=9/16`. The new proof controls the contrast's bias directly instead of incorrectly asserting a common latent power.

Assume full groups are independent and their latent catalogue probabilities are the same `w_j`. Even if the within-group propensities vary deterministically across groups, Hoeffding still controls the raw contrast average around its average expectation. A valid bias allowance is

`A_i >= (c_i/n) sum_g sum_j w_j sum_t beta_(g,j,t)`.

The safe uniform `D_i beta` avoids pretending the unknown weights are known. The confidence radius is `B_i sqrt(log(2N/delta)/(2n))+A_i`. The original strict half-weight-floor support test then applies verbatim. Group independence remains necessary for this concentration proof.

## 2. Independently certified joint-law deviation

Let the actual conditional endpoint-vector law in group `g`, given label `j`, be `Q_(g,j)`. It may have dependent repetitions. Suppose an independently justified certificate bounds its total variation distance from a declared product Bernoulli law `P_(g,j)` by `gamma_(g,j)`. That reference product may have the unequal propensities from Section 1.

For any bounded function with range width `B`, the difference of its expectations under two laws is at most `B` times their total variation. One proof couples the two laws maximally, subtracts the function's minimum, and bounds the contribution on the mismatch event. Equivalently, use the positive and negative parts of the signed measure. Applied to the count contrast this gives

`|E_Q b_i(S)−E_P b_i(S)|<=B_i gamma_(g,j)`.

Combining this with the calibration calculation yields the sufficient allowance

`A_i >= (1/n)sum_g sum_j w_j [c_i sum_t beta_(g,j,t)+B_i gamma_(g,j)]`.

With uniform bounds `beta` and `gamma`, take simply

`A_i=D_i beta+B_i gamma`.

Across-group independence still gives the same Hoeffding term because the statistic's exact range has not changed. The resulting support condition is

`max_i [B_i sqrt(log(2N/delta)/(2n))+D_i beta+B_i gamma] < w_min/2`.

Accurate conditional marginal propensities alone do not imply a small `gamma`: dependent repetitions can have exactly the nominal marginals and a substantially different joint law. Nor does a per-group TV certificate establish independence across groups. Those are separate assumptions; the existing copied-emission and shared-latent adversaries remain valid.

### Same disclosed budget with a small joint-law allowance

For the frozen three-label example, `delta=1/20`, `w_min=1/3`, `beta<=1/1000`, `n=40000`, `R=2`. If additionally every conditional group law is within `gamma<=1/20000` of a product law whose individual propensities satisfy that calibration bound, the same budget still suffices.

Using the worst constants `B=50/3`, `D=100/3`, the remaining sampling margin is

`1/6 − (100/3)/1000 − (50/3)/20000 = 53/400`.

The exact inequality `5/288 < (53/400)^2`, together with `log(120)<5`, proves strict separation. This is a sufficient design conditional on the new joint-law certificate, not a claim that such a certificate can be obtained from the same observations or from marginal calibration alone. It introduces no empirical execution or optimization claim.

## Exact controls

The independent script inverts complete binomial probability matrices rather than constructing the author's Lagrange polynomials. It checks 168 unequal-propensity groups by exact Poisson-binomial convolution, 56 conditional-law contamination instances, and the updated budget with rational arithmetic. The proofs above, rather than these finite controls, establish the general claims.
