# What final answers identify about collective evidence use

This is a guide to the complete written mathematical argument in the Fifteenth compendium, section **What final answers can identify about collective evidence use**. The exact document projection preserves the argument and its mathematical expressions. The results below are ordinary written mathematics. They are not a fitted participant model, kernel proof, verified numerical classifier, or identification of an actual contributor.

## The two mechanisms and the equal observation law

Fix finite parameters $v>0$, $k>1$, and $r_B,r_W\geq0$. For a fixed stimulus $x$, let

$$X_B=x+\sqrt v Z_B,\qquad X_W=x+\sqrt{kv}Z_W,$$

where the noises are independent standard normal variables. Put

$$\alpha=\frac{k-1}{k+1},\qquad\beta=\frac2{k+1}.$$

For announcer $a$, the one-input mechanism $L$ uses $T_L=X_B+\sqrt{r_a}Z_A$; the two-input mechanism $P$ uses $T_P=\alpha X_B+\beta X_W+\sqrt{r_a}Z_A$. Both return $Y=1\{T>0\}$. The equalities $\alpha+\beta=1$ and $\alpha^2+k\beta^2=1$ imply

$$T_L,T_P\sim N(x,v+r_a),\qquad
P_L(Y=1\mid x,a)=P_P(Y=1\mid x,a)=\Phi\!\left(\frac{x}{\sqrt{v+r_a}}\right).$$

Thus even observing the complete final score does not distinguish this matched pair. With fresh independent trial noises and the same complete stimulus/announcer design $D$, the full vector of final scores, and hence the full answer vector, has the same conditional law. A random design must have the same joint law and be exogenous to the trial noises. Matching stimulus marginals alone does not suffice: repeated and reversed joint designs can differ. The conclusion is equality in law, not equality of coupled answers on every sample path. At $k=3$, $P$ is the ordinary average. The excluded boundary $k=1$ has $\alpha=0$ and ceases to be a two-input mechanism. Zero output noise is allowed.

Within this pair, $do(X_W=w)$ leaves $L$ unchanged and strictly raises the response probability of $P$ as $w$ increases. The latter is

$$\Phi\!\left(\frac{\alpha x+\beta w}{\sqrt{\alpha^2v+r_a}}\right).$$

Both weights are positive, so the corresponding intervention on $X_B$ is also consequential in $P$. These are interventions on the stipulated model. They do not assert that private evidence can be manipulated passively or ethically in an actual human experiment.

## Linked passive observations separate the pair

Condition on the same fixed $(x,a)$. In $L$, $X_W$ is independent of $Y$. In $P$,

$$\operatorname{Cov}(X_W,Y\mid x,a)
=\frac{\beta kv}{\sqrt{v+r_a}}\,
\phi\!\left(\frac{x}{\sqrt{v+r_a}}\right)>0.$$

This is a same-trial link. Pooling over stimuli can produce association under $L$; observing unlinked marginal distributions is insufficient. Observation must leave the mechanism unchanged.

The single passive bit $Q=1\{X_W>0\}$ also suffices. Under $L$, its covariance with $Y$ is zero. Under $P$, the conditional success function of $Y$ is strictly increasing in $X_W$, giving strictly positive covariance with its threshold bit. All four joint cells have positive probability at the stipulated finite parameters, so this is statistical discrimination, not a finite observation that logically excludes one model.

For independently recorded bit error $E\sim\operatorname{Bernoulli}(\varepsilon)$, set $Q'=Q\oplus E$. Then

$$\operatorname{Cov}(Q',Y)=(1-2\varepsilon)\operatorname{Cov}(Q,Y).$$

The positive separation remains for $\varepsilon<1/2$. At $\varepsilon=1/2$, the recorded bit is independent of the answer under both mechanisms; with fresh mutually independent errors across trials, the full recorded-pair sequence laws coincide. For $\varepsilon>1/2$, reversing the recorded bit restores the direction. Dependent recording errors are outside this argument.

## Fixed sample guarantees require a known gap

Let $p'=P(Q'=1)$ and $q=P(Y=1)$, and let $\delta=\operatorname{Cov}(Q',Y)>0$ under $P$. For independent repetitions at fixed design, a known baseline $p'q$ and a known lower bound $\delta\geq\delta_0>0$ give the rule

$$\text{select }P\quad\text{if}\quad
\frac1n\sum_{i=1}^n Q'_iY_i\geq p'q+\frac{\delta_0}{2}.$$

Hoeffding's bound makes each error probability at most $e^{-n\delta_0^2/2}$. Therefore $n\geq2\log(1/\eta)/\delta_0^2$ suffices for each error to be at most $\eta$. This is a guaranteed error bound under the assumptions, not finite certainty. In the mathematical illustration $x=0,v=1,k=3,r_a=0,\varepsilon=0$, the joint success probabilities are $1/4$ under $L$ and $5/12$ under $P$; $\delta=1/6$. With $n=216$, select $P$ at a joint count of at least 72, giving each error at most $e^{-3}<1/20$. No study of 216 participants or trials was run here.

For one binary pair, the total variation distance is $2\delta$, and for $n$ independent pairs it is at most $2n\delta$. Consequently the sum of errors is at least $1-2n\delta$. Since the model class permits arbitrarily small positive gaps, no one finite sample size has a uniform nontrivial error guarantee over the whole unseparated class. A known gap is a substantive premise.

## A one-sided sequential service

For iid binary pairs with unknown marginals, write

$$\widehat c_n=\widehat b_n-\widehat p_n\widehat q_n,
\qquad
\epsilon_n=\sqrt{\frac{\log(6n(n+1)/\gamma)}{2n}}.$$

The exact-real rule stops and selects $P$ the first time $\widehat c_n>3\epsilon_n$. A union bound over the three empirical means and all times controls the probability of ever selecting $P$ under the independence null by $\gamma$. For every fixed positive covariance alternative, concentration and the vanishing threshold imply almost-sure finite detection. The procedure returns no $L$ answer and has no uniform finite time bound.

This limitation cannot in general be repaired by adding a reliable terminating $L$ branch. Fix the uniform independent-pair null at $x=0,v=1,k=3,r_a=0$ and approach it with the alternatives $\delta=(1-2\varepsilon)/6\downarrow0$. A nonanticipating two-answer procedure that terminates almost surely under that null cannot also maintain uniform null/alternative error bounds whose sum is less than one over all these alternatives. The argument needs neither alternative-side almost-sure termination nor finite expected stopping time. Near-null alternatives can approximate any finite stopping prefix closely enough to inherit the null decision's probability.

The compendium proves an exact-real rule. It does not supply a certified floating-point implementation. A conservative implementation would need validated statistical errors and thresholds that still tend to zero to preserve its eventual-detection claim.

## The scientific limit

For this parameter-matched pair, final-answer-only likelihood ratios equal one. Such answers leave prior odds unchanged; they do not establish equal overall plausibility or erase other evidence. Composite-model priors would need matching induced observation laws. Linked observations, a changed observation design, or suitable interventions can discriminate the stipulated mechanisms. None of these mathematical results determines which mechanism generated the published participants' responses.

<!-- SOURCE_NAVIGATION -->
## Inspectable sources

- [Complete Fifteenth mathematical compendium](../../source-store/34393b10d6a7447b0d802cb2aa65f6ec93d3f20446d0de97a9c4e292e59081f2/Orthemology_Fifteenth_Mathematical_Compendium_v1_20261005.md) — `T15-COMPENDIUM-DERIVED-MARKDOWN`.
- [Fifteenth main report](../../source-store/69051582e889b364891ee1e6b59782fe025c0334eaa423e9fd822e5f256f08ee/Orthemology_Fifteenth_Research_Final_v1_20261005.md) — `T15-REPORT-DERIVED-MARKDOWN`.
- [Original review and verification scope](../../source-store/9e799d654bbf71e75b70e70d622b8b7e4d7e86719d738146409e80a06aff9d27/T15-RECEIPT) — `T15-RECEIPT-SOURCE`.
