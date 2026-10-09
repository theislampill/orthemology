# A matching-exponent lower bound for the fixed paired-face replay instrument

8 October 2026 UTC. New prospective scratch sibling, beyond the sixth checkpoint cutoff. All earlier packets remain unchanged. This is a probability-model sampling lower bound, not a physical experiment, practical sampling recommendation, global instrument-optimality claim, integration or T20 closure.

## 1. Result and exact experiment class

Fix an integer n>=1, and set

    m=n+1, c=n/(n+1), t=1/[3(n+1)], p=1-t.

The reference world has n independent AB route occurrences with independent uniform thresholds and identity marginal calibrations. The alternative has m independent route pairs, shared coordinate marginal calibrations H_c(x)=1-(1-x)^c, and the fixed Joe threshold law from dependent-gate-transport. Its per-route joint gate success at true-reference commands a,b is H_c(ab).

These worlds have the same entire fresh endpoint absence function

    Q(a,b)=(1-ab)^n,

and hence the same face marginals at every command. Their counts differ.

The allowed observations are:

1. An informative **paired-face replay replicate**: draw a fresh independent latent route-pair vector, retain that exact vector while probing (t,1) and (1,t), and observe both separately read binary endpoint outcomes. No output carryover, gate change or state mutation is allowed within this pair.
2. Optional fresh single-endpoint probes at any commands, with a separately redrawn latent vector for every probe. They can be selected adaptively but cannot share thresholds with another observation.

The pair instrument is fixed at the displayed t. No other retained-threshold commands, longer replay words, gate-level observations, cross-replicate threshold persistence or side information about which world is true are included. All replicas have the same fixed law within each world. Common policy randomness and adaptive allocation are allowed under the contracts below.

For 0<alpha<1/2, every test that correctly accepts the reference and rejects this Joe alternative, each with probability at least 1-alpha, requires

    N_replay >= [625/3136] (n+1)^4 kl(1-alpha,alpha)             (1)

when it uses a fixed number N_replay of informative replays. Here logarithms are natural and

    kl(x,y)=x log(x/y)+(1-x) log((1-x)/(1-y)).

The same lower bound holds for the **expected number of informative replays under the Joe alternative** with adaptive allocation and potentially unbounded stopping, under the unconditional terminal-correctness contract in section 5. Arbitrarily many allowed fresh single-endpoint observations do not change this bound.

The restriction alpha<1/2 is necessary for this nontrivial binary-testing statement. At alpha=1/2, a fair random decision with no observations is admissible; for alpha>1/2 it remains admissible and the positive expression kl(1-alpha,alpha) must not be used as a lower bound.

## 2. The exact hard pair of replay laws

Let A=p^n be either face's no-effect probability. Write replay outcomes in the order (no/no, no/yes, yes/no, yes/yes). The reference pair law is

    P0=(A^2, A(1-A), A(1-A), (1-A)^2).

For the Joe alternative, a single route's neither-gate probability is

    S=2p^c-(1-t^2)^c.

The joint no-effect probability for the whole retained-threshold pair is J1=S^m. Put

    Delta=J1-A^2.

Since the two face marginals still equal A, its pair law is exactly

    P1=P0+(Delta,-Delta,-Delta,Delta).                         (2)

These are genuine probability distributions, inherited from the fixed-threshold Joe construction; they are not chosen merely as four contextwise numbers. The following direct calculation shows that Delta is positive and small.

### 2.1 A concavity-gap bound

Define

    D=2-(1+t)^c-(1-t)^c.

Because 0<c<1 and t>0, strict concavity of x^c gives D>0. Taylor's integral remainder supplies the explicit upper bound

    D <= c(1-c)t^2 p^(c-2).                                  (3)

Indeed -d^2(x^c)/dx^2=c(1-c)x^(c-2), bounded above by c(1-c)p^(c-2) throughout [1-t,1+t]. The two one-sided integral remainders together have weight t^2.

Let B=p^(2c). Using 1-t^2=p(1+t),

    S-B=p^c D>0,
    B^m=p^(2n)=A^2.

Both S and B belong to [0,1]. The difference-of-powers identity therefore gives

    0<Delta=S^m-B^m <= m(S-B).

Combining this with (3) and m c(1-c)=c gives

    Delta <= c t^2 p^(2c-2)
           <= t^2 p^(-2)
           <= (36/25)t^2
           = 4/[25(n+1)^2].                                 (4)

The penultimate step uses t<=1/6 and p>=5/6. No large-n approximation is used. Also S=p^c[2-(1+t)^c]<p^c, so J1<A and the two off-diagonal cells in P1 are strictly positive. The other two cells are positive by (2). Thus both pair laws have full support.

### 2.2 A uniform reference-cell floor

Integer Bernoulli's inequality gives A=(1-t)^n>=1-nt>=2/3. Conversely (1-t)^(-n)>=1+nt, while nt>=1/6, hence

    A <= 1/(1+nt) <= 6/7.

Every entry of P0 is therefore at least 1/49. These bounds are deliberately loose and uniform in n.

## 3. One replay supplies at most order n^(-4) relative entropy

Let d=KL(P1 || P0). The elementary inequality log z<=z-1 gives

    KL(P1 || P0)
      <= sum_i (P1(i)-P0(i))^2/P0(i).

This follows by expanding sum_i P1(i)[P1(i)/P0(i)-1] and using that each law sums to one. It is an upper bound by chi-squared divergence, not a quadratic approximation.

Use (2), the reference-cell floor, and (4):

    0<d <=196 Delta^2
          <=3136/[625(n+1)^4] =: d_bar_n.                    (5)

The strict positivity follows from Delta>0 and P1!=P0. Only the upper bound is needed for (1). The orientation is important: the denominator in the chi-squared bound is P0, and adaptive expected costs below are taken under P1.

For N independent replays, KL(P1^N || P0^N)=N d. Additional independent fresh endpoint observations have identical laws in both worlds and contribute zero relative entropy. Let E be the decision to reject the reference. The error requirements give P1(E)>=1-alpha and P0(E)<=alpha. Binary data processing, or the log-sum inequality applied to E and its complement, gives

    N d >= kl(P1(E),P0(E)) >= kl(1-alpha,alpha).

The final inequality uses alpha<1/2 and monotonicity of binary relative entropy when its first argument exceeds its second. Substitute (5) to obtain (1).

Randomized tests are included: adjoin their same-law random seed to the data, which contributes no relative entropy, then apply the same event inequality.

## 4. Fresh probes remain uninformative under adaptive allocation

It is not enough merely to note equality of unconditional fresh observations if a policy is adaptive. The relevant conditional statement is stronger and follows from the model:

At any common realized history, the same policy chooses the same conditional distribution over actions and commands in both worlds. Conditional on that history and a chosen fresh command (a,b), a new independent latent vector gives a Bernoulli absence outcome with the same Q(a,b) in both worlds. Thus that step's conditional likelihood ratio is one on its common support and its conditional KL contribution is zero.

The policy may nevertheless choose different marginal action frequencies across worlds because its past replay outcomes differ. This creates no extra information beyond that history: action choices use a common policy kernel, and their conditional KL contribution is zero. This distinction is why equal unconditional probe laws alone would not be a sufficient argument.

An informative pair action always supplies the fixed four-cell law P0 or P1, independently of previous replicas. Its conditional KL contribution is d. It is treated as one observation action that returns both bits; the protocol does not modify the second command after seeing the first. Fresh single endpoints cannot later be repurposed as retained-threshold observations.

## 5. Adaptive stopping, with nontermination accounted for

Consider a sequential policy indexed by observation slots. Before each slot it may choose an allowed fresh probe, the fixed informative pair, or stop and report accept/reject. Decisions and action kernels are measurable functions of the observed history and common randomization. After stopping, pad all later slots with a common dummy symbol. Let tau be the terminal time, possibly infinity, and let N_T count informative pairs observed by slot T before stopping. Put N_infinity=lim_T N_T, possibly infinity.

Require the **unconditional** terminal-correctness guarantees

    P0(tau<infinity and decision=accept) >= 1-alpha,
    P1(tau<infinity and decision=reject) >= 1-alpha.             (6)

Nontermination is neither an acceptance nor a rejection. It consumes the allowed failure probability in each world. Conditional-on-termination accuracy, with no control of termination probability, is not enough for this theorem.

For a finite prefix of T slots, the likelihood-ratio chain rule gives exactly

    KL(Law_1(history_T) || Law_0(history_T)) = d E1[N_T].        (7)

One direct verification writes the prefix log likelihood ratio as the sum of log(P1(O)/P0(O)) over its informative pair actions. Fresh outcomes, common action kernels, randomization and padding contribute zero. Each pair term has conditional expectation d under world 1. Finite T makes all these pair terms integrable because the fixed four-cell laws have positive entries. No optional-stopping theorem at an unbounded time is being assumed.

Let E_T={tau<=T and decision=reject}. Binary data processing applied to the finite prefix yields

    d E1[N_T] >= kl(P1(E_T),P0(E_T)).                           (8)

The events E_T increase to the actual terminal-rejection event E. Monotone convergence gives E1[N_T] increasing to E1[N_infinity]. Continuity of binary relative entropy at interior limits, and lower semicontinuity at possible boundary limits, then give

    d E1[N_infinity] >= kl(P1(E),P0(E)).

By (6), P1(E)>=1-alpha, while P0(E)<=alpha because E is disjoint from terminal acceptance. Consequently

    E1[N_infinity] >= [625/3136](n+1)^4 kl(1-alpha,alpha).      (9)

If the expectation is infinite, the inequality is true without further argument. If tau is almost surely finite in both worlds, N_infinity is just the ordinary stopped replay count, so this specializes to the standard expected-sample bound. The more general formulation does not grant free success on nonterminating paths.

The standard change-of-measure perspective is illustrated by [Kaufmann, Cappe and Garivier, JMLR 17 (2016), Lemma 1 and Appendix A.1](https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf). Those targeted passages state an almost-surely-finite stopping version. The finite-prefix proof above supplies the exact experiment and terminal-correctness scope used here, including the permitted nontermination budget; no whole-paper reading or unexamined extension is claimed.

## 6. Matching the robust certificate, only within this instrument class

The separately developed finite-panel-replay-robustness theorem uses the same t and accepts a specified reference against all wrong-count alternatives in the shared-marginal, independent-route, stable-replay class. Its sufficient design takes

    N >= ceil[200000000 (n+1)^4 log(8/alpha)]

independent informative pairs, plus N independent fresh diagonal trials. It uses 3N endpoint evaluations in total. The fresh diagonal observations help the broad wrong-count test, even though they carry no information for this particular lower-bound pair.

Our alternative belongs to that wrong-count class. Thus no such reference test using only the allowed fixed pair instrument and fresh independent endpoints can uniformly improve the n^4 replay-count exponent. For fixed alpha in (0,1/2), (1) is an order-n^4 lower bound. Also

    kl(1-alpha,alpha)=(1-2alpha) log((1-alpha)/alpha)

is asymptotic to log(1/alpha) as alpha decreases to zero. For the explicit range 0<alpha<=1/4 it is at least (1/4)log(1/alpha). Hence the upper and lower orders agree in n and in small-error logarithmic dependence, within this restricted observation class. The lower cost is a fixed replay budget or expectation under the Joe alternative, not a lower bound on every model's individual expected cost. Constants are very far apart.

This is not global experimental optimality. A design allowed other retained-threshold rates, longer replay words, additional joint channels, or genuinely different measurements is outside the lower bound. It is also not a practical guarantee that even one replay can be implemented. The target-rate coordinate must be known/selectable if an operational design is intended.

The lower bound stands independently of the upper theorem's review status. SOURCE_AUDIT.md records the exact upper artifact inspected and its status at freeze; any final combined order comparison should retain both independent reviews rather than infer one from the other.

## 7. Negative evidence and attribution

- Full fresh endpoint equality makes every independently redrawn single-command observation information-free for the hard pair. It does not imply equality of retained-threshold joint laws.
- Measuring the complete two-bit pair is already allowed. Keeping only J or any other summary cannot defeat the bound, by data processing, but is not assumed in deriving it.
- The pair must be fixed at t. The one-replay bound is not a uniform KL bound over every possible rate or longer shared-threshold transcript.
- Fresh samples must use independent new latent vectors. Sharing a latent vector with earlier observations changes the experiment and can make conditional fresh outcomes informative.
- An expected-cost conclusion concerns the Joe world, matching KL(P1||P0). It is not silently transferred to expectation under the reference world.
- The nontrivial error range is alpha<1/2. A no-data fair decision at alpha>=1/2 is an exact negative control against dropping that condition.
- Unconditional terminal correctness is essential; nontermination is not silently converted into a correct answer.
- Probability-model sample lower bounds do not validate common calibration, mutual route independence, actual productive occurrences, no-mutation replay, physical availability, psychological control, or source-level original independence.

The parent proposed the Joe hard pair, explicit Delta and KL constants, and fixed-reference comparison. Author work checks the inequalities, corrects the error-range qualification, and develops the finite-prefix adaptive/stopping proof with an explicit terminal contract. Joe copulas, Taylor remainder, KL/chi-squared comparison, binary data processing and change-of-measure inequalities are inherited mathematics, not new general discoveries.
