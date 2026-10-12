# High long-run accuracy can coexist with zero restoration probability

**Scope:** a quantitative successor to `hidden_standard_learning.md`, using the same synthetic fixed hidden standard and iid observation model. The statistical law, target assignment and permission to issue either response remain separate supplied premises. The result strengthens a dynamic counterexample; it does not determine which epistemic or normative objective ought to be chosen.

## 1. Two different criteria

Let observations be iid Bernoulli(2/3) under H₊ and iid Bernoulli(1/3) under H₋. A learner issues one of the two labels at each time. Compare:

- long-run average Bayes error, with equal hypothesis priors;
- restoration: eventually every issued label is correct for the fixed actual hypothesis.

The first scores the average frequency of mistakes. The second is a coBüchi condition: only finitely many mistakes. A small positive stationary mistake rate can be excellent by the first criterion and fail the second with probability one.

The existing HS1 proof already rules out a finite-memory time-homogeneous controller that restores almost surely under both hypotheses. Here is an explicit family showing how extreme the difference can be.

## 2. A finite sticky random walk

Fix S≥2 memory states {0,…,L}, where L=S−1, and a parameter 0<ε≤1. Under observation bias p:

- in an interior memory state i, observation 1 moves to i+1 and observation 0 to i−1;
- at state 0, observation 1 moves to 1 with additional probability ε; otherwise remain at 0;
- at state L, observation 0 moves to L−1 with additional probability ε; otherwise remain at L.

The extra randomization is fresh and independent of the acquisition. The policy is finite-state and time-homogeneous for each fixed ε. Both endpoint departures have positive probability, so the chain is irreducible. Endpoints have self-loops, so it is also aperiodic.

Let r=p/(1−p). Unnormalized stationary weights are

`w₀=1`, `w_L=r^L`, and `w_i=εr^i` for `1≤i≤L−1`.

For S=2 there are no interior weights. Adjacent detailed balance proves the formula: on the first edge the upward probability is εp and downward is 1−p; on interior edges their ratio is r; on the last edge the downward probability is ε(1−p), canceling the interior factor ε. Dividing by the sum gives the unique stationary law.

For p=2/3, r=2; for p=1/3 the stationary law is its reflection around L/2. With equal priors, the optimal state-based decision is H₋ below L/2 and H₊ above L/2. If L is even, the middle state is a tie and either label, or a fair tie randomization, has the same Bayes error.

Writing

`D_L = Σ_{i=1}^{L−1} 2^i = 2^L−2`

and

`C_L = Σ_{1≤i<L/2} 2^i + (1/2)·2^(L/2)·1_{L even}`,

the stationary average error is

`E_S(ε) = (1+εC_L)/(1+2^L+εD_L)`.

Consequently `lim_{ε↓0} E_S(ε)=1/(1+2^(S−1))`. Increasing S makes this limiting average error exponentially small.

### MA1. Every positive-ε machine nevertheless fails restoration surely

Under H₊, memory state 0 produces a wrong label. Under H₋, state L produces a wrong label. Each is recurrent in the respective finite irreducible chain and hence visited infinitely often with probability one. Therefore the probability of restoration is zero under **each** hypothesis, regardless of how small its stationary average error is.

For example, S=21 and ε=1/1000 gives exact stationary Bayes error

`1267/524812787 ≈ 2.4×10⁻⁶`,

but restoration probability remains zero. The wrong-response target is genuinely hidden-standard-relative, not merely a failure of a public certificate.

## 3. A singular zero-randomization limit

For S=3, start at state 1. The positive-ε stationary error reduces to

`E₃(ε)=(1+ε)/(5+2ε)`.

Thus taking the long-time limit first, and then ε↓0, yields error 1/5.

At ε=0, however, both endpoints become absorbing. Starting at state 1, the machine observes one bit, moves to an endpoint, and never changes its decision again. It errs with probability 1/3 under either hypothesis. For every fixed n≥1, the finite-time error converges to 1/3 as ε↓0. Therefore the two iterated limits differ:

`lim_{ε↓0} lim_{n→∞} error_n(ε)=1/5`,

`lim_{n→∞} lim_{ε↓0} error_n(ε)=1/3`.

There is a second reversal. For every ε>0, restoration probability is zero, while at ε=0 the one-sample commitment restores with probability 2/3. A better average score does not order these controllers the same way as eventual correctness. Nor does approaching a stationary-error infimum justify setting a transition probability to zero without rechecking the support and recurrent classes.

## 4. What the classical result does and does not say

Hellman and Cover's finite-memory learning work studied time-invariant randomized machines. Berg, Ordentlich and Shayevitz explicitly define an asymptotic average error and report the randomized infimum `1/(1+γ^((S−1)/2))`, with `γ=p(1−q)/(q(1−p))`. Here γ=4, matching the limit reached by the displayed symmetric construction. Their criterion is not eventual absence of errors. They also distinguish a time-varying transition rule from a genuinely finite time-invariant machine; an unbounded clock cannot be supplied for free. [Hellman–Cover, author-hosted paper](https://www-ee.stanford.edu/~hellman/publications/04.pdf), [Berg–Ordentlich–Shayevitz, definitions (4), (9) and related-work discussion](https://arxiv.org/pdf/2005.07445).

The universal optimality bound belongs to that literature; the present exact probe verifies the displayed family, not a new proof of optimality across all machines. No novelty claim is made for the sticky-boundary construction.

Even vanishing instantaneous error would not by itself prove restoration: independent mistake indicators with probabilities 1/(t+2) tend to zero in probability but occur infinitely often almost surely. The unbounded-memory majority construction in HS1 uses a summable exponential error bound, a materially stronger condition. Conversely, dependent mistakes can be finite almost surely without a finite expected total, as the heavy-tail recovery control in `regenerative_refinement.md` shows.

## 5. Reproducible evidence

`probe_memory_accuracy.py` checks 200 exact stationary laws, under both biases, for S=2,…,21 and ε∈{1,1/2,1/10,1/100,1/1000}. It verifies stationarity by direct matrix multiplication, computes the optimal equal-prior statewise Bayes error, compares the closed form at S=3, and independently classifies the wrong endpoint's reachable bad bottom component. It also checks the ε=0 one-sample absorbing law through 12 steps under each hypothesis. All checks pass; results are in `memory_accuracy_results.json`.

The infinite-visit conclusion uses the finite irreducible-chain proof, not a simulation that happened to make many errors. The model retains the iid provenance premise: reusing one acquisition as many apparent samples would define a different process and would invalidate the learning interpretation.
