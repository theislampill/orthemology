# Sharp global calibration threshold for fixed pure counts

This is a separate mathematical continuation of the frozen `../calibration-design-frontier/ARBITRARY_RATE_COUNT_BOUND.md`. It leaves that result and all preceding stages unchanged. The result concerns fixed pure inventories in a conditional binary endpoint model. It does not certify a physical calibration model, solve arbitrary-mixture recovery, establish polynomial sampling efficiency at the new threshold, authorize protected integration, or close T20.

## 1. Model and the meaning of identifiability

Fix a positive integer k. The unknown count j is either k or k+1 and remains fixed throughout the experiment. A world consists of that count and one unknown static calibration function r:[0,1] -> [0,1]. The function is nondecreasing, preserves endpoints r(0)=0 and r(1)=1, and satisfies the uniform command-error bound

    sup_(x in [0,1]) |r(x)-x| <= eta.

At each trial a protocol chooses a nominal command x in [0,1], possibly from the complete previous transcript and its own randomness. Conditional on that history and command, its only new observation Y is a fresh Bernoulli no-hit indicator with

    P(Y=1 | history, x, j, r) = (1-r(x))^j.

Thus a count j consists of j independent copies of the same one-root route in this model. The conditional law, not just an unconditional one-trial marginal, is assumed. The protocol has no independent root-rate readout, labelled internal hits, known-count calibration specimen, or additional count-dependent channel. Commands and outcomes are retained. Competing worlds may have different fixed calibration functions, as usual for an unknown nuisance parameter; the calibration never changes during either experiment.

Below, uniform finite-sample identifiability means that for every prescribed delta in (0,1/2) there is a finite endpoint budget and a procedure whose probability of failing to return the correct count is at most delta for every admissible world. Abstention or nontermination counts as failure; alternatively one may restrict to procedures that return a count almost surely. Nonidentifiability is witnessed by two worlds with identical response curves at every command, which is stronger than failure of any particular finite design.

## 2. Sharp adjacent-count theorem

Put

    b = k/(k+1),
    t_* = b^(k+1),       s_* = b^k,
    Delta_k = s_* - t_* = b^k/(k+1),
    eta_k^* = Delta_k/2 = [1/(2(k+1))] [k/(k+1)]^k.

For every integer k>=1:

1. If eta>=eta_k^*, there are two admissible static calibration functions, one with count k and one with count k+1, whose complete command-response curves are identical. They can both be chosen continuous and strictly increasing. No endpoint-only adaptive, randomized, or stopped procedure can have error less than 1/2 in both worlds.
2. If 0<=eta<eta_k^*, a single command, repeated sufficiently often, uniformly distinguishes the two counts with any prescribed error delta>0. One valid command is

       x_* = 1 - (t_*+s_*)/2.

Consequently eta_k^* is the exact inclusive boundary of global nonidentifiability for this model. As k grows, eta_k^* is asymptotic to 1/(2e k). The result gives an order-1/k calibration threshold for identifiability, distinct from the order-1/k^2 uncertainty scale of the earlier efficiently tuned command x approximately 1/k.

### 2.1 Two static worlds that agree at every command

Parameterize the whole nominal command interval by u in [0,1]:

    x(u) = 1 - (u^(k+1)+u^k)/2,
    r_k(x(u)) = 1-u^(k+1),
    r_(k+1)(x(u)) = 1-u^k.

The function x(u) is a continuous strictly decreasing bijection from [0,1] onto [0,1]. Therefore these formulas define single-valued static functions of the nominal command. Both true-rate functions are continuous, strictly increasing in x, and preserve 0 and 1.

Their signed deviations from the command are opposite:

    r_k(x(u))-x(u) = u^k(1-u)/2,
    r_(k+1)(x(u))-x(u) = -u^k(1-u)/2.

The derivative of u^k(1-u) in the interior is u^(k-1)[k-(k+1)u]. Its maximum is attained at u=b and equals Delta_k. Both functions consequently have uniform error exactly eta_k^*.

For every u, their no-hit means agree:

    (1-r_k(x(u)))^k = u^[k(k+1)]
                            = (1-r_(k+1)(x(u)))^(k+1).

Because the parameterization covers every command, this is an all-command identity, not an ambiguity at just one experimental setting. The t-parameterization in the candidate is equivalent: t=u^(k+1), t^(k/(k+1))=u^k.

To see why adaptation cannot help, couple the protocol's random seed in the two worlds. Whenever histories agree, the next command agrees, and the identical Bernoulli mean permits the same fresh uniform random number to generate both next outcomes. Inductively the transcripts agree pathwise. Any stopping decision and reported count determined by such a history and the common random seed also agree. Equivalently all finite-dimensional transcript laws, and hence the law on the generated infinite-sequence sigma-field, coincide. The probabilities of correctly reporting k and k+1 under a common output law sum to at most one, so at least one error is at least 1/2. Unlimited endpoint access does not resolve the two worlds. A stopping rule that fails to terminate does not acquire information by failing to return an answer.

### 2.2 Separation strictly below the threshold

Let m=(t_*+s_*)/2 and use x_*=1-m. For eta<eta_k^*, define

    A = m-eta,          B = m+eta.

Since eta_k^*=(s_*-t_*)/2,

    0 < t_* < A <= B < s_* < 1.

In particular, neither the success-rate uncertainty interval nor the survival-rate uncertainty interval is clipped at this command. Every admissible calibration gives survival 1-r(x_*) in [A,B]. The possible no-hit means under the two counts belong respectively to

    I_k = [A^k,B^k],
    I_(k+1) = [A^(k+1),B^(k+1)].

Their separating gap is strictly positive:

    g_k(eta) = A^k-B^(k+1) > t_*^k-s_*^(k+1) = 0.

The last equality is b^[k(k+1)] = b^[k(k+1)]. This argument uses only the pointwise error bound at x_*, so imposing monotonicity does not create a gap in the converse.

Write L=A^k, U=B^(k+1), and h=(L+U)/2. Repeat x_* for N fresh trials, take the empirical no-hit frequency q_hat, and report k if q_hat>=h, otherwise k+1. Under either hypothesis, an error requires a one-sided empirical deviation of at least g_k(eta)/2. Hoeffding's inequality gives the uniform bound

    maximum error <= exp[-N g_k(eta)^2/2].

Thus the finite budget

    N >= ceil[2 g_k(eta)^(-2) log(1/delta)]

suffices for binary testing. This is a safe bound, not a claim of a sharp constant or sharp variance-sensitive rate.

## 3. Exact extension to a whole fixed-count catalogue

Let M>=2 be a known maximum and let the unknown fixed count j range over 0,1,...,M. Define eta^*=eta_(M-1)^* and use the command x_* from the preceding theorem for the last pair M-1,M. For eta<eta^* let A=m-eta, B=m+eta as before. The possible means for count j lie in

    I_j=[A^j,B^j],         I_0={1}.

For j=0,...,M-1, the gap between consecutive intervals is

    g_j=A^j-B^(j+1).

The ratio A^j/B^(j+1) decreases in j because A/B<=1. Since g_(M-1)>0, all preceding g_j are positive too. In addition,

    g_(j+1)=A g_j-(B-A)B^(j+1)<g_j

whenever g_j>0. This includes eta=0 because A<1. Therefore the smallest adjacent interval gap is g=g_(M-1).

Place the decision threshold h_j halfway between B^(j+1) and A^j. These M ordered thresholds define a decoder for the one empirical no-hit frequency. If its error from the true mean is less than g/2, the decoded count is correct. One two-sided Hoeffding bound gives

    maximum error <= 2 exp[-N g^2/2],
    N >= ceil[2 g^(-2) log(2/delta)]  suffices.

There is only one empirical frequency, so no catalogue-size union bound is needed. The pair M-1,M supplies the matching nonidentifiability obstruction when eta>=eta_(M-1)^*. Hence eta_(M-1)^* is the exact threshold for uniform finite-sample identification of the entire fixed-count catalogue under this calibration class.

Count zero is defined by the absence of any root, so its no-hit probability is exactly one, including at x=1. If the catalogue is only {0,1}, the endpoint-preserving condition makes one trial at x=1 distinguish the counts deterministically for every eta. The positive-pair theorem deliberately starts at k=1; a formal 0^0 substitution would be inappropriate.

## 4. What happens near the threshold

The preceding upper bounds are finite for each fixed strict margin eta^*-eta>0. They do not remain bounded as the margin vanishes, and this is not merely a weakness of that decoder.

Fix k and let r_k^*, r_(k+1)^* be the indistinguishable maps constructed at eta_k^*. For eta<eta_k^*, put lambda=eta/eta_k^* and define

    r_(j,lambda)(x)=(1-lambda)x+lambda r_j^*(x),
    j in {k,k+1}.

These remain continuous strictly increasing endpoint-preserving maps, and their uniform errors are at most eta. Each is at most eta_k^*-eta from its corresponding boundary map. Since z -> (1-z)^j is j-Lipschitz on [0,1], the two no-hit probabilities obey, at every command,

    |q_(k,lambda)(x)-q_(k+1,lambda)(x)|
        <= (2k+1)(eta_k^*-eta).

Couple adaptive transcripts as before until their first differing outcome. At each common history, the next Bernoulli outcomes can be coupled to disagree with probability at most the displayed bound. For a protocol with at most N trials this yields

    TV(P_k,P_(k+1)) <= min{1,N(2k+1)(eta_k^*-eta)}.

If both errors are at most delta<1/2, the event 'report k' requires total variation at least 1-2delta. Therefore every such uniformly valid fixed-budget protocol must satisfy

    N >= (1-2delta)/[(2k+1)(eta_k^*-eta)].

This bound proves divergence for fixed k as eta approaches the threshold from below. It is not asserted to be the sharp divergence rate, an expected-stopping-time bound, or a rate uniform in growing k. The same obstruction applies to a full catalogue through its final adjacent pair.

At the boundary midpoint command,

    q_* = t_*^k = s_*^(k+1) = [k/(k+1)]^[k(k+1)],
    x_* -> 1-e^(-1),
    log(q_*) = -k + O(1).

Thus this robustness-optimal separation command has exponentially rare no-hit events in the large-k boundary regime. That fact and the explicit upper budget explain why the identifiability theorem must not be advertised as a polynomial-efficiency result. No theorem here rules out better sampling budgets at other commands and smaller error budgets.

## 5. Relation to the frozen result and boundaries

The frozen arbitrary-rate result assumes exact calibration and proves Theta(M^2 log(1/delta)) sampling for fixed counts 0,...,M, even allowing adaptive commands. Its efficient construction uses x=1/M and tolerates a conservative order-M^(-2) unknown fixed rate error; its fixed-command ambiguity establishes that this local uncertainty scale is real for that chosen command.

The new theorem changes the nuisance class: a whole unknown static monotone endpoint-preserving command map with a uniform absolute error bound. It proves an exact all-command ambiguity at order-M^(-1), and proves identifiability below it by a different command. There is no contradiction. The earlier order-M^(-2) example did not rule out other commands; the new identifiability threshold does not preserve the earlier sampling order.

Additional boundaries:

- The two worlds use different static nuisance maps. If the actual map is known or separately measured, the all-command equivalence no longer provides an obstruction to that enriched experiment.
- These are pure fixed counts. A fresh latent count mixture has response sum_j w_j(1-r(x))^j and requires a different inverse argument. The catalogue corollary is not a mixture-recovery theorem.
- Correlations or additional observations not determined by the specified conditional Bernoulli kernel can distinguish worlds that share one-trial means. The adaptive impossibility assumes the stated complete observation model.
- Endpoint preservation is explicit. It is important for the special zero-count case. The two positive-count ambiguity maps themselves satisfy it exactly.
- The construction already uses well-behaved continuous strictly monotone functions; it does not depend on jumps, nonmonotonicity, time-varying drift, or rate clipping.
- An independently observed actual calibration, a known-count control, an intervention restricted to a different command set, a relative-error bound, a prescribed parametric map, or extra derivative constraints would define another problem.
- This is conditional mathematics derived here from the frozen model. It provides no empirical calibration certification, source-admissibility warrant, physical causal identification, field-wide priority claim, protected write, or T20 closure.
