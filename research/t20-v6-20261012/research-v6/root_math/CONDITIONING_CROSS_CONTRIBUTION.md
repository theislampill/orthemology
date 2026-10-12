# Joining the two Pro error contracts

11 October 2026. Candidate ordinary mathematical refinement for independent review. No Lean or field-wide novelty claim.

## Sources and why this is a substantive reconciliation

First Pro synthesis, CROSS_FRONT_SYNTHESIS.md, SHA256 8aad39f6fb030620059edd4e0639f58078537a10181836b64089f6d82dbe10f4, D4b, proves the safe bound min(1, 2 TV(p,q)/alpha) for a common likelihood in [0,1] and two positive event masses bounded below by alpha. It explicitly disclaims sharpness.

Second Pro synthesis, Cross_Front_Theorems.md, SHA256 c2ca691c70c953bd5e7af3f2e0d6a86f9ef72d7cf8996cb3b369bdd9afa1e1e1, Theorem D, proves the sharp relative-factor bound (sqrt(b)-sqrt(a))/(sqrt(b)+sqrt(a)). It changes likelihood factors while holding the origin law fixed. Its joined evidence/geometry result then uses posterior TV and endpoint coupling as distinct inputs.

These are different perturbations. Neither supersedes the other. Their combination gives a constructive qualification for a representation with both imperfect origin reconstruction and imperfect source factors.

## 1. Sharper common-likelihood bound

Let p and q be probability vectors on the same finite state space, let 0<=L<=1, and set A=sum Lp>0 and B=sum Lq>0. Let delta=TV(p,q), using half the l1 norm. Then

    TV(B_L p, B_L q) <= min(1, delta/max(A,B)).

Proof. Suppose A>=B, and let S be the coordinates where L_i p_i/A exceeds L_i q_i/B. The TV distance is the positive difference summed on S:

    TV = (1/A) sum_S L_i(p_i - (A/B)q_i)
       <= (1/A) sum_S L_i(p_i-q_i)
       <= (1/A) sum_i (p_i-q_i)_+
       = delta/A.

The middle inequality uses 0<=L_i<=1 and discards any negative differences. If B>A, exchange p and q. The trivial bound one completes the proof. The same argument works for probability measures by a dominating measure and the positive part of their density difference; no finite enumeration is needed for that extension.

Sharpness as a uniform alpha guarantee: for 0<alpha<=1 and 0<=delta<=alpha use

    p=(1-alpha, alpha-delta, delta, 0),
    q=(1-alpha, alpha-delta, 0, delta),
    L=(0,1,1,1).

Both event masses equal alpha, the prior TV is delta, and the posterior TV is delta/alpha. For delta>=alpha, disjoint accepted support can attain posterior TV one. Thus replacing the first Pro bound's factor 2 by 1 is justified, but the rare-event denominator cannot in general be removed.

## 2. Joint origin-and-factor error

Keep L as above. Let an approximate factor M have the same zero support as L, and suppose 0<a<=M_i/L_i<=b<infinity on the positive support of L. With A,B>0, all relevant posteriors exist. Inserting B_L q gives

    TV(B_L p, B_M q)
       <= min(1, delta/max(A,B) + (sqrt(b)-sqrt(a))/(sqrt(b)+sqrt(a))).

The first term follows from section1; the second is exactly Pro2 Theorem D applied to the probability vector B_L q and factor M/L. Unlike L, M need not be at most one for this normalised-posterior statement. No likelihood calibration or predictive-normaliser bound follows from the ratio oscillation alone.

This is an upper bound, not a claim that the sum is jointly sharp. Each component is sharp when the other perturbation vanishes. If zero supports differ, the bounded relative-factor hypothesis fails and this route must not be used. If B=0, the intermediate posterior is undefined; positive A alone does not repair that obstruction.

## 3. Consequence for the joined transport budget

For exact and approximate endpoint maps on these same origins with uniform displacement epsilon, and a bounded K-Lipschitz observable of range oscillation R, insert the resulting posterior bound into Pro2's already-proved coupling argument:

    absolute expectation error <= R * posterior_bound + K * epsilon.

This combines approximation of the retained law, approximation of evidence factors, and approximation of subsequent transport without identifying them. A fixed Markov postprocessing kernel contracts the posterior TV term. Source-dependent dynamics require the separately established replay or equivariance conditions; adaptive policy changes and discontinuous permission labels require their own contract.

The result is a scoped strengthening and joining of supplied ordinary proofs. It does not certify actual source likelihoods, truth-directed cognition, actual theological warrant, or any implementation's complete semantic model.

## Independent review disposition

The independent ordinary proof review in ../early_remaining/CONDITIONING_REVIEW.md accepted the main inequalities and identified the zero-alpha sharpness endpoint as undefined. The displayed fixture now explicitly requires alpha>0. For alpha<=delta<=1, the five-state fixture is p=(1-delta,delta-alpha,0,alpha,0), q=(1-delta,0,delta-alpha,0,alpha), L=(0,0,0,1,1): both event masses alpha, prior TV delta, posterior TV1. Independent exact controls are retained separately; neither review nor tests constitute Lean verification.
