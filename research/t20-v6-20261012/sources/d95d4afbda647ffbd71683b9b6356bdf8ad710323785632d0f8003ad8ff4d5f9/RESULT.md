# Uninformative observations can drive asymptotic concentration under weighted repair

9 October 2026. Conditional mathematical follow-through to the separately reviewed likelihood/repair interface. This is a model-level diagnostic, not a psychological manipulation capability or an empirical result. No earlier result is overwritten.

## Contract and inherited inputs

There are n>=2 hypotheses with a strictly positive coherent prior p. Let alpha_i>0 and F(x)=sum_i alpha_i x_i log x_i, continuously extended to the closed cube. P is the first-argument simplex projection argmin_q D_F(q,b). Its interior formula is P(b)_i=b_i exp(lambda/alpha_i), with lambda chosen to make the sum one. The preceding interface result establishes weak repair/multiplication composition for these coordinate-weighted generators; common weights alone implement ordinary Bayes.

At every step observe a fair coin, independent of the hypothesis and previous coins. BOTH outcomes have likelihood vector (1/2,...,1/2). The actual Bayesian posterior consequently remains p after every realised sequence. Consider instead the explicitly declared implementation q_0=p, q_(k+1)=P(q_k/2). Every finite q_k is interior. This is an implementation under examination, not an assertion that proper scoring theory prescribes it.

## 1 Exact path

Weak composition gives q_k=P(2^(-k)p). Introduce t=k log 2 and the continuous interpolation

q_i(t)=p_i exp(-t+lambda(t)/alpha_i),
sum_i p_i exp(-t+lambda(t)/alpha_i)=1.

The normalization equation has a unique smooth lambda, with lambda(0)=0. All finite-time coordinates are strictly positive. The discrete implementation samples this path. No stochastic averaging or rare repeated outcome is needed: EVERY coin sequence generates the same implemented forecast.

## 2 Concentration theorem

Put a=min_i alpha_i, M={i:alpha_i=a}, and P_M=sum_(i in M)p_i. Then

lambda(t)=a t-a log P_M+o(1),
q_i(t) -> p_i/P_M for i in M,
q_i(t) -> 0 for i not in M.

Proof. Write delta(t)=lambda(t)-a t. The normalization equation becomes

1=P_M exp(delta/a)+sum_(i not in M) p_i exp(-(1-a/alpha_i)t+delta/alpha_i).

For t>=0 its right side evaluated at delta=0 is <=1, while the first term forces delta<=-a log P_M at the solution. Thus delta lies in a fixed compact interval. Every non-minimal term tends uniformly to zero on that interval. Consequently P_M exp(delta/a)->1 and delta->-a log P_M. Substitution proves the coordinate limits.

With one minimum-weight hypothesis, the implementation tends to certainty in that hypothesis regardless of which hypothesis is true. With tied minimum weights, it retains their prior ratios. The actual posterior remains p throughout.

## 3 Expected regret is increasing and unbounded when weights differ

For the statewise Bregman score D_F(e_j,q), define actual expected risk using the fixed true prior p. Strict propriety gives risk(q)-risk(p)=D_F(p,q), since p is the categorical mean. Put A_p=sum_i alpha_i p_i and A_q(t)=sum_i alpha_i q_i(t). Direct substitution yields

D_F(p,q(t))=t A_p-lambda(t)-A_p+A_q(t).

Differentiating the normalization gives

lambda'(t)=1/(sum_i q_i(t)/alpha_i)=H_q(t),
A_q'(t)=H_q(t)-A_q(t)<=0.

The inequality is the weighted harmonic-arithmetic mean inequality. It is strict at every finite time when the alpha_i are not all equal, because q_i(t)>0. Therefore A_q(t)<A_p for t>0 and

d/dt D_F(p,q(t))=A_p-A_q(t)>0 for t>0.

Moreover,

D_F(p,q(t))=(A_p-a)t+a log P_M-A_p+a+o(1).

If the weights differ, positivity of the prior gives A_p>a. Hence expected regret diverges linearly, at rate (A_p-a) log 2 per coin observation. This is expected-score regret, not a classification error probability or a claim that human warrant is numerically this score.

## 4 Each repair stage nevertheless improves every statewise score

Let b=q_k/2 and q=q_(k+1)=P(b). Its interior projection condition makes grad F(q)-grad F(b)=lambda 1. For each categorical truth e_j, the Bregman three-point identity gives

D_F(e_j,b)-D_F(e_j,q)=D_F(q,b)>0.

Thus the final repair stage at EVERY step decreases EVERY truth-state loss relative to the unnormalised intermediate vector. Simultaneously, the full pipeline's expected risk relative to its unchanged stipulated true-prior baseline increases. The input transformation and the last-stage gain must not be conflated.

The counterexample preserves algebraic repair consistency and valid score geometry. What fails is the proposed likelihood-update interpretation. It supplies a concrete diagnostic for the source-required operation-realisation mapping, without claiming an actual deployed Orthemology or DAEE implementation has this defect.

## 5 Exact two-hypothesis family

For alpha=(1,2) and p=(1/2,1/2),

q_(k,2)=2/[1+sqrt(1+2^(k+3))],
q_(k,1)=1-q_(k,2).

At k=1 this is q=((9-sqrt(17))/8,(sqrt(17)-1)/8). As k grows, q_2 tends to zero, although every observation was an independent fair coin. Here A_p=3/2, a=1 and P_M=1/2, so

D_F(p,q_k)=(k log 2)/2-log 2-1/2+o(1).

## Scope and ancestry

The projection formula and weak composition are inherited from the immediately preceding T20 interface result. Softmax/log-sum-exp asymptotics, proper-score regret and the arithmetic-harmonic mean inequality are classical mechanisms. The local addition is the explicit repeated-null-channel trajectory, its limiting selection and monotone unbounded regret, alongside equal statewise repair gains. No exhaustive originality claim is made.

The mathematical domain, selected projection orientation, positive prior, fixed weights and stipulated independent coin channel are essential. It does not license choosing weights to steer real people, establish actual cognitive identifiability, or show that alternative proper scores cannot be used with an independently correct Bayesian update. Common weights remove this defect: the posterior stays p. A genuinely informative channel must be evaluated with its actual joint law and provenance.
