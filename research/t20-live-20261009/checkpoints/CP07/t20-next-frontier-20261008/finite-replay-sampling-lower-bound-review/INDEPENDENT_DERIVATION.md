# Independent derivation, before reading the author packet

Recorded 2026-10-08. The reviewer received the candidate formulas from the parent and derived the following before reading any author result or controls. This is independent validation, not an independent priority claim for the proposed constants.

## Algebra and strict separation

Write m=n+1>=2, c=n/m in [1/2,1), t=1/(3m), p=1-t and A=p^n. Let S=2p^c-(1-t^2)^c and B=p^(2c). Then

S-B = p^c D,    D=2-(1+t)^c-(1-t)^c.

For f(x)=(1+x)^c,

D = c(1-c) integral[-t,t] (t-|x|)(1+x)^(c-2) dx.

The integrand is positive, giving D>0. Because c-2<0 and 1+x>=p,

D <= c(1-c)t^2 p^(c-2).

Furthermore 0<B<S<1: positivity follows from S>B, and S=p^c[2-(1+t)^c]<p^c<1. Thus

0<Delta=S^m-B^m <= m(S-B)
 <= m c(1-c)t^2 p^(2c-2)
 = c t^2 p^(2c-2)
 <= t^2 p^-2 <= (36/25)t^2 = 4/[25m^2].

Here m(1-c)=1 and p>=5/6. All inequalities hold at n=1; no asymptotic step is used.

## Baseline cell masses and KL

Bernoulli's inequality gives A=(1-t)^n >=1-nt>2/3. A useful independent upper bound stronger than the candidate's is

A^-1 = (1+t/p)^n >=1+nt/p
 =1+n/(3n+2)>=6/5,

so A<=5/6<6/7. Consequently both A and 1-A exceed or equal 1/7, and all four P0 cell masses exceed or equal 1/49.

For P1-P0=(Delta,-Delta,-Delta,Delta), the exact Pearson divergence is

chi^2(P1||P0)=Delta^2[1/A^2+2/(A(1-A))+1/(1-A)^2]
 =Delta^2/[A^2(1-A)^2]
 <=196 Delta^2 <=3136/[625m^4].

The elementary inequality log u<=u-1 gives KL(P1||P0)<=chi^2(P1||P0). Probability validity of P1 must still come from the stipulated Joe replay law, not from the loose Delta bound alone. Equivalently S<p^c implies S^m<A, giving positive off-diagonal cells A-S^m; the final cell is positive by P1,11=(1-A)^2+Delta.

## Common adaptive policies and potentially infinite stopping

Fix any policy whose conditional action, stopping, and terminal-randomization kernels are identical functions of the observed history under the two hypotheses. Each fresh single-endpoint action uses a new independent realization, with the same Bernoulli law at each chosen command under both hypotheses. Each informative action returns the same fixed-threshold two-face replay pair on a new realization. No query may reconnect to an earlier realization except within its one designated pair.

For finite T, pad the transcript after stopping with a common cemetery symbol. Include actions and terminal randomization in the transcript, or include a common independent random seed initially. The finite-prefix KL chain rule then gives exactly

KL(Law_1(H_T)||Law_0(H_T)) = d E_1[N_T],

d=KL(P1||P0), where N_T counts paired replay actions by round T. Common action kernels contribute zero conditional KL even when the chosen actions have different unconditional distributions under the two hypotheses. Arbitrary chosen fresh commands contribute zero conditional KL because the conditional observation laws at that same command agree. Their outcomes can change later allocation, but do not directly increase KL.

Let tau range over nonnegative integers and infinity, with terminal labels accept/reference or reject/Joe defined only on {tau<infinity}. Require unconditional correctness:

P0(tau<infinity, accept)>=1-alpha,
P1(tau<infinity, reject)>=1-alpha,  0<alpha<1/2.

For E_T={tau<=T,reject}, binary data processing gives

d E_1[N_T]>=kl(P1(E_T),P0(E_T)).

The event probabilities increase to r1>=1-alpha and r0<=alpha. Monotone convergence gives E_1[N_T] upward to E_1[N_tau], possibly infinity. Lower semicontinuity of binary KL gives

d E_1[N_tau]>=kl(r1,r0)>=kl(1-alpha,alpha),

where the last inequality follows from the monotonicity of kl(x,y) for x>y. Boundary probabilities use the extended-valued convention. Because d>0 and d<=3136/[625m^4],

E_1[N_tau]>=625/3136 * m^4 * kl(1-alpha,alpha).

If the protocol has at most N paired replay actions almost surely under Joe, the same lower bound applies to N. No almost-sure finite stopping assumption, optional-stopping identity, or error conditional on termination is needed. Infinite runs count against unconditional correctness and do not automatically receive a terminal label.

## Scope

The derivation controls only this fixed informative action plus arbitrarily many independent fresh single endpoints under the shared calibrated model. It does not control other held-threshold commands, longer replay words, reuse of realizations across actions, model-dependent policies, or globally optimal instruments. Comparison with an O(n^4 log(1/alpha)) upper test is order matching for this instrument/model and fixed reference n only. The lower bound counts paired replays under Joe; it does not by itself lower-bound the reference-expected count.
