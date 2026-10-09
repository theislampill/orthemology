# Process assumptions and the unknown-label obstruction

## 1. What the concentration statement needs

Three distinct independence claims must not be conflated:

1. Within an episode, the independent-route model gives the code product.
2. Within a group, conditional on its fixed histogram and common actual propensity, repeated endpoints are independent and identically distributed Bernoulli observations. This gives the factorial moment identity.
3. Across groups, the full group observations are independent under a fixed mixture law. This gives the stated Hoeffding concentration.

A stable histogram by itself implies none of the required probabilistic independence. Even independent but differently calibrated repeats inside a group have a factorial expectation that averages products of unequal propensities, not powers of one scalar. The theorem therefore explicitly assumes one common actual propensity for all repetitions of a given group. Per-repetition marginal calibration errors must not be substituted without a new argument.

Across-group calibration drift needs separate treatment. Deterministic varying propensities may preserve group independence; random shared drift can destroy it. The main theorem assumes fixed actual propensities and independent groups. An explicitly warranted extension is possible if groups remain independent, every group's index has the same weights `w`, each group has one common actual propensity `theta_(g,j)` for component `j`, and all deviations satisfy the same deterministic `beta_j` bound. Hoeffding for independent, not necessarily identically distributed, bounded variables then controls deviation around the average expectation, whose bias remains at most `D_i beta`. If the weights vary with groups, the target becomes their average law rather than an assumed fixed `w`.

A shared random nuisance sometimes permits a conditional concentration proof: one must independently establish the conditional independence and conditional weight/calibration promises and then integrate that proof. Merely naming the nuisance or stating marginal error bounds supplies no such warrant. No martingale, mixing-time, effective-sample-size, or drift guarantee is imported here.

### A transparent dependent-group adversary

Take the exact nominal two-label catalogue `(1,3/4)` and weights `(1/2,1/2)`. Draw the component once for the entire experiment and keep it forever. Conditional on that component, independently generate every endpoint, including across groups. Each individual group has the correct nominal mixture distribution, and every group internally satisfies its common-propensity Bernoulli model. Nevertheless groups are not marginally independent: endpoints in distinct groups have covariance `Var(z_J)=1/64`.

At `R=1`, the raw first weight estimate is `4 bar_Y−3`. As the number of groups grows, it converges to `1` or `0` according to the single sampled component, not to the population weight `1/2`. Its asymptotic variance is `16*(1/64)=1/4`. More repetitions of one realized inventory do not estimate the frequency of inventories in the population. This disproves an unconditional `n^(−1/2)` concentration claim under marginal group laws alone.

The predecessor's conditional-emission dependence, fresh within-group resampling, guard, infinite-route and persistence counterexamples remain in force. This finite-sample result does not repair them.

## 2. Calibration uncertainty can create a wrong population answer

For the known catalogue consisting of the empty histogram and one `{0}` route, nominal codes are `z_1=1`, `z_2=3/4`. With `R=1`,

`L_1(z)=4z−3`, `L_2(z)=4−4z`,

and the two contrasts at counts `0,1` are `(-3,1)` and `(4,0)`. Both ranges and derivative constants are `4`.

If the true inventory is always the route histogram but its actual port rate is `1/16`, then the no-effect propensity is `15/16`. The nominal estimator converges to `(3/4,1/4)`, although true catalogue weights are `(0,1)`. The code error is `3/16`, and the exact bias equals the stated allowance `D_i beta=3/4`. With a positive-weight floor of one, the threshold `1/2` selects only the wrong, empty-histogram label.

This example remains inside the independent-route and independent-repeat models. What fails is a small enough calibration premise for the support certificate. It does not say finite-catalogue estimation is always impossible under calibration uncertainty, or that this particular bias bound is minimax sharp in every catalogue.

## 3. Internal separation does not discretize unknown histogram labels

The finite catalogue is essential to this particular exact-label certificate. Knowing only that an unknown mixture has a bounded number of components, positive weights, and separated scalar nodes does not provide a uniform finite-sample exact histogram-label guarantee over the imported countable eligible class.

Here is a direct construction with all labels eligible and every weight unchanged. Start with any finite mixture

`Pi=sum_(a=1)^k w_a delta_(H_a)`

of distinct finite histograms, with `w_a>=w_min>0`. For `k>=2`, let its minimum internal code separation be

`Delta_0=min_(a!=b)|z_a−z_b|>gamma>0`.

The strict slack above a proposed separation requirement `gamma` is explicit. Choose a port index `l` absent from every route in the finitely many `H_a`. Such indices exist arbitrarily far out. Put `E=2^l`, `eta=4^(−E)`, and add one route of support `{l}` to **every** component:

`H'_a=H_a+delta_E`, `z'_a=(1−eta)z_a`.

All new labels are different from all old labels, because their multiplicity at the fresh support code `E` is one, whereas every old label has zero there. The new labels remain mutually distinct. All weights retain the same positive floor. Their internal node separation is

`min_(a!=b)|z'_a−z'_b|=(1−eta)Delta_0`.

For sufficiently large `l`, this is still at least `gamma`. Thus the obstruction does not depend on collapsing mixture nodes or allowing tiny mixture weights. For `k=1`, the separation condition is vacuous and the same label obstruction holds.

### Full grouped laws approach one another

Compare one length-`R` group under the original and shifted mixtures. Couple the component index using the same probabilities `w`. Given component `a`, couple each pair of Bernoulli endpoints using the same fresh uniform variable. Its mismatch probability is `|z_a−z'_a|=eta z_a<=eta`. The conditional endpoint sequences on each side have the required independent Bernoulli law. A union bound therefore makes the probability of any group mismatch at most `R eta`; consequently

`TV(T_R,T'_R)<=R eta`.

This applies to the full ordered endpoint vectors, and hence also to their counts by deterministic data processing. For `n` independent groups the same coupling gives

`TV(T_R^n,(T'_R)^n)<=min(1,nR eta)`.

More generally a fixed finite collection of groups with total `M` endpoints has bound `min(1,M eta)`. Its grouped moment differences also satisfy `|m_r−m'_r|<=r eta`, since `m'_r=(1−eta)^r m_r` and `0<=m_r<=1`.

The actual base4 calibration is exact in both models. This obstruction is therefore separate from the calibration error in the finite-catalogue certificate.

### Elementary testing consequence

Let any estimator output an exact set of histogram labels from these `n` groups, allowing its own independent randomness. Let `A` be the event that it returns the original support. Under the original model, the probability of error is `1−P(A)`. Under the shifted model, whose true support is disjoint, its error probability is at least `P'(A)`. Their sum is at least

`1−P(A)+P'(A)>=1−TV(P,P')`.

Thus at least one of the two models has error probability at least `(1−nR eta)/2`. Letting the fresh port index grow makes `eta` arbitrarily small while preserving `gamma`, the component count and all weights. For every fixed finite sampling budget, the supremum exact-support error over any model class containing this baseline and all its sufficiently rare-route perturbations is at least `1/2`. In particular no uniform finite budget guarantees confidence `1−delta` for `delta<1/2` from internal mixture separation and a positive weight floor alone.

This is a standard two-point testing/coupling argument, specialized to the imported route code, not a new general impossibility theorem. It does not preclude pointwise consistency, approximate scalar-node estimation, stronger interventions, or algorithms under an independently justified isolation promise. It also does not contradict exact-moment identifiability: different laws may be uniquely identifiable from exact probabilities while arbitrarily close under every finite grouped observation budget.

## 4. What extra isolation would need to mean

An internal separation condition compares components that are present in the same mixture. It says nothing about the distance from a component's code to codes of alternative histogram labels outside that mixture. A valid code-isolation promise would have to bound that latter distance over the allowed hypothesis class, at a scale exceeding all calibrated and sampling uncertainty relevant to its decoder. The finite catalogue supplies a discrete, explicitly known set of alternatives for the present Lagrange construction.

A claimed isolation radius over **all** finite eligible histograms is false: adding a fresh sufficiently high-index route supplies a different eligible code arbitrarily close to any fixed finite histogram. Restricting supports, multiplicities, total route count, or the hypothesis class may justify a finite catalogue, but such restrictions must be separately supplied and checked. This note does not prove a new general recovery theorem for every possible isolation promise.

## 5. Interpretive scope

Recovered support consists of anonymous histogram labels in the declared catalogue. It does not identify physical bearers, establish finitude from observation alone, count underived productive originals, prove actual independent route mechanisms, or supply an original-efficacy or theological source bridge. A probability certificate quantifies sampling uncertainty conditional on its premises; it does not create the premises.
