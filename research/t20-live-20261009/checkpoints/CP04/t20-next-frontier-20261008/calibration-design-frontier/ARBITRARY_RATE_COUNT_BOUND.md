# A count lower bound that survives arbitrary adaptive calibration

This separate result concerns the pure-inventory subfamily of the finite catalogue H_0,...,H_K, where H_j has j independent copies of the same one-root route. The unknown inventory is fixed, not a mixture resampled during this experiment. It also lower-bounds any larger catalogue-support procedure required to handle these point masses. It does not give a complete mixture-recovery upper bound for that catalogue.

## Theorem

Let K>=2 be known. At each of N endpoint trials a protocol may choose any root success rate x in [0,1], adaptively from its past and internal randomness. Conditional on that past and chosen rate, H_j produces an independent new Bernoulli no-effect endpoint with parameter (1-x)^j. Calibration is exact in this theorem, and total budget N is fixed. If every count 0,...,K is identified with error at most delta, where 0<delta<1/2, then

N >= ((K-1)K/2) (1-2delta) log((1-delta)/delta).

For delta<=1/4 this is at least ((K-1)K/4)log(1/(2delta)). A single fixed rate x=1/K and at most ceil[18K^2 log(2/delta)] endpoints suffice. Thus the dependence is Theta(K^2 log(1/delta)) for this pure-count problem (uniformly away from confidence 1/2), even allowing adaptive arbitrary rates.

## Per-trial bound, uniform over every rate

Compare counts n=K-1 and n+1=K. Write t=1-x. At 0<t<1, put u=t^n,v=t^(n+1). The elementary log z<=z-1 bound gives

KL(Ber(u)||Ber(v)) <= (u-v)^2/[v(1-v)]
= t^(n-1)(1-t)/(1+t+...+t^n).

For n=1 this is (1-t)/(1+t)<=1=2/[n(n+1)]. For n>=2, arithmetic-geometric mean gives sum_(k=0)^n t^k >= (n+1)t^(n/2). The last display is therefore at most

t^((n-2)/2)(1-t)/(n+1) <= 2/[n(n+1)].

For n=2 the last numerator is 1-t<=1. For n>2 its maximum occurs at t=(n-2)/n and equals (2/n)((n-2)/n)^((n-2)/2)<=2/n. At x=0 or x=1 both positive-count laws coincide, so KL is zero and the bound also holds.

For an adaptive policy, conditioning on a common past leaves the same rate-selection kernel under both hypotheses. The conditional endpoint KL is bounded as above, regardless of that selected rate. Factorization of the transcript likelihood and expectation give total KL <=2N/[n(n+1)]. This is the ordinary adaptive chain-rule argument, not a finite-menu restriction on rates.

Let E be the final decision to report n. Correctness yields P_n(E)>=1-delta and P_(n+1)(E)<=delta. Grouping likelihood terms into E and its complement (the log-sum inequality) gives total KL >= kl(P_n(E),P_(n+1)(E)) >= kl(1-delta,delta). Here kl is binary relative entropy and the last inequality follows by differentiating in its two arguments on p>q. Since kl(1-delta,delta)=(1-2delta)log((1-delta)/delta), the stated bound follows. This proof avoids relying on an unproved extension to expected stopping times.

## Matching fixed-rate upper order

Choose t=1-1/K. Adjacent catalogue means differ by t^j/K, and their minimum for j=0,...,K-1 is t^(K-1)/K >1/(3K). Indeed (1+1/(K-1))^(K-1)<3: expand the binomial, bound each term by 1/r!, and use 1+1+sum_(r>=2)1/r!<3. Taking reciprocals proves the gap.

Estimate the one no-effect probability by its empirical frequency and select its nearest known mean t^j. Error less than 1/(6K) guarantees the right count. Hoeffding bounds failure by 2exp[-N/(18K^2)], giving the stated budget. There is only one empirical mean, so no catalogue-size union bound is needed. This is a pure-count upper bound; averaging unknown count components would change the target.

## Calibration floor for that fixed-rate construction

For this paragraph assume the actual success rate is unknown, fixed across repetitions, and differs from x=1/K by at most eta; each repetition still has the stated fresh conditional Bernoulli law at that actual rate. For every j<=K the mean then differs from its nominal value by at most K eta, by telescoping j factors in [0,1]. Consequently eta<=1/(12K^2), together with empirical error below 1/(12K), suffices; N>=ceil[72K^2 log(2/delta)] gives that sampling event. This conservative sufficient allowance has the correct K^-2 scale for this chosen command. No unproved random-drift concentration extension is intended.

For an exact obstruction at the same command, set t=1-1/K. Count K-1 at actual rate x=1/K has mean t^(K-1). Count K at actual rate

x'=1-t^((K-1)/K)

has the identical mean. Its deviation from the command is

d_K=t^((K-1)/K)-t.

No amount of repetition at this one command can distinguish these two worlds if eta>=d_K. Moreover

1/(2K^2) <= d_K <= 2/K^2.

To check the bounds, write L=-log t. Then d_K=t(exp(L/K)-1). The lower bound uses exp(v)-1>=v, L>=1/K and t>=1/2. The upper bound uses exp(v)-1<=v exp(v), t exp(L/K)=t^((K-1)/K)<=1, and L<=1/(K-1). Thus the uncertainty scale is genuinely K^-2 for this tuned fixed rate, not merely a loose decoder coefficient. Other commanded-rate panels could add information; the fixed-command ambiguity is not a theorem against all calibration-error models or all multi-rate procedures.

## Novelty and scope

The predecessor supplied a K^2 upper bound and matching lower count exponent for its prescribed one-root mask rate, while explicitly leaving arbitrary-rate alternatives outside its lower bound. The new ingredient here is a uniform per-observation KL inequality covering every success rate and hence every fixed-budget adaptive rate policy. The proof uses classical divergence and concentration tools. No field-wide priority claim, minimax constant, expected-stopping theorem, multi-root optimal exponent, mixture upper rate, or physical validation is asserted.
