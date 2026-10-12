# Independent review supplement: truth-asymmetric calibration boundary

11 October 2026 UTC. Reviewer-authored supplement to the ordinary independent review of `pairwise-corroboration-bound-20261011/RESULT.md`, SHA-256 `a86cced3f856527cbfab677458c2792e36bab1a89dc0684f3c5a0447c8ef0eb2`.

This is a separately marked mathematical extension identified during review. It does not amend the author's bytes, silently broaden the author's truth-symmetric theorem, authenticate any historical source, establish actual calibration or warrant, or close T20. The supplement has author-stage exact controls; it is not an additional independent review of itself. General parity, conditional likelihood, and missing-interaction mechanisms remain inherited.

## Result

Truth symmetry is unnecessary for the sharp unanimity Bayes-factor and posterior bounds if each truth-conditioned correctness law has the same common individual accuracy p and pairwise independence. It is necessary for the author's assertion that, at known unequal prior, the unlabelled report law identifies its single parameter t.

With two independently varying truth-conditioned interaction parameters, the full unlabelled report law identifies only one linear combination. Two distinct full-support models can have identical every proper truth/report marginal at an unequal prior and different posteriors after unanimous reports.

## 1. Declared model and sharp bounds

Let X be binary truth, alpha=P(X=1) in (0,1), and Y_i its three binary reports. Define C_i=1 exactly when Y_i=X. For each truth value x, require

    P(C_i=1 | X=x)=p,
    P(C_i=C_j=1 | X=x)=p² for i≠j,
    1/2<p<1.

Do not require C to be independent of X. Put t_x=P(C=111 | X=x), K=1−3p+3p², and L=p(2p−1). Conditional inclusion-exclusion independently yields, for x=0 and x=1,

    q_x(111)=t_x;
    q_x(c)=p²−t_x when c has two ones;
    q_x(c)=p−2p²+t_x when c has one one;
    q_x(000)=K−t_x.

Exactly the rectangle (t_0,t_1) in [L,K]² is feasible. Both conditional laws have full support exactly when both parameters lie strictly inside (L,K). Equal first/pair moments force the within-truth exchangeability here; no cross-truth symmetry is assumed.

For E={Y=111}, the true-state and false-state likelihoods are t_1 and K−t_0. Therefore

    BF(E)=t_1/(K−t_0),
    P(X=1 | E)=alpha*t_1/[alpha*t_1+(1−alpha)*(K−t_0)].

Both expressions are nondecreasing in each parameter and strictly increasing away from the relevant boundary. The minimum is attained at t_0=t_1=L; the Bayes factor becomes +infinity and the posterior becomes one when t_0=K. Since t_1≥L>0, E remains possible there. Thus the sharp ranges are unchanged:

    BF(E) in [p(2p−1)/(1−p)², +infinity],
    P(X=1 | E) in
      [alpha*L/(alpha*L+(1−alpha)*(1−p)²), 1].

Every intermediate value is already realized by the diagonal t_0=t_1. For full-support channels the ranges are open at both ends. The prior-independent threshold for uniformly nonnegative evidence remains p≥(sqrt(5)−1)/2. This extends the bound, not the author's single-parameter identification statement.

## 2. What the full unlabelled law identifies

Write q_t(c)=b(c)+d(c)*t, where d(c)=(-1)^(3−sum(c)). Since three is odd, d(complement(c))=−d(c). Marginalizing X gives

    P(Y=y)
      =alpha*q_(t_1)(y)+(1−alpha)*q_(t_0)(complement(y))
      =alpha*b(y)+(1−alpha)*b(complement(y))
       +d(y)*[alpha*t_1−(1−alpha)*t_0].

At fixed p and known alpha the entire eight-cell unlabelled distribution therefore depends on the pair only through

    beta=alpha*t_1−(1−alpha)*t_0.

It identifies beta, since P(Y=111)=(1−alpha)K+beta, but generally not both parameters. Each (X,Y_i,Y_j) distribution is fixed by the prior and pairwise calibration. Consequently equal beta means equal every proper marginal of (X,Y_1,Y_2,Y_3), while the unanimous posterior can differ.

The author's symmetric subclass sets t_0=t_1=t, so beta=(2alpha−1)t. At alpha=1/2 this is constant, giving the author's full unlabelled collision. At known unequal alpha it identifies t, exactly as the author states. The two-parameter extension does not contradict that result.

## 3. Exact unequal-prior collision

Take p=3/5, alpha=2/3, L=3/25, and K=7/25. Compare:

    Model A: t_0=t_1=1/5;
    Model B: t_0=11/50, t_1=21/100.

All four conditional parameter values lie in (3/25,7/25), so both joint laws have full support. Both have beta=1/15 and the same full unlabelled law:

    P(Y=111)=4/25;
    P(Y=000)=3/25;
    P(Y=y)=2/15 for each pattern with two ones;
    P(Y=y)=8/75 for each pattern with one one.

Every proper truth/report marginal also agrees. Nevertheless,

    Model A: P(X=1 | Y=111)=(2/15)/(4/25)=5/6;
    Model B: P(X=1 | Y=111)=(7/50)/(4/25)=7/8.

Thus known unequal prior alone does not repair unlabelled identification when the two truth-conditioned higher-order interactions are free. Both posteriors happen to favor truth in this control; the claim here is nonidentification of the posterior, not opposite evidential directions at that retained unlabelled law.

## Verification and limits

`python3 verify.py` is standalone and uses exact rational arithmetic to check the bound across truth-asymmetric grids, all conditional pair distributions, full support, the entire unequal-prior collision, every proper joint marginal, and both posterior values. It requires no Library projection, upstream source bytes, network, author import, or external package.

The general argument is the ordinary proof above. Finite controls are corroboration, not formal-kernel certification or a literature priority search. No acquisition procedure for t_0,t_1, empirical source calibration, historical sequence model, or philosophical warrant follows from this supplement.
