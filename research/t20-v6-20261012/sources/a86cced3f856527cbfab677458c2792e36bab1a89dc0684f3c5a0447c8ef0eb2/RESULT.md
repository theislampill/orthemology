# Sharp corroboration bounds from pairwise-calibrated witnesses

11 October 2026 UTC. Additive T20 mathematical application of the supplied scriptural-recoverability connection. Ordinary proof and exact finite controls; no historical verdict, warranted-prior claim, formal-kernel claim, protected edit, integration, contact, T21, or T20 closure.

## Result

Knowing that three sources are individually better than chance and conditionally pairwise independent does **not** ensure that their unanimous report supports what they say. In a symmetric binary channel with common accuracy p in (1/2,1), the sharp lower Bayes factor of three unanimous reports is

    BF_min = p(2p−1)/(1−p)^2.

Consequently unanimity is guaranteed to be nonnegative evidence exactly when p ≥ (sqrt(5)−1)/2. With equal truth prior, the sharp identified posterior interval is

    [ p(2p−1)/(1−3p+3p²), 1 ].

At p=3/5 it is [3/7,1]. The fully mutually independent channel gives 27/35. A strictly positive, pairwise-independent channel instead gives 13/28, below the prior 1/2. Both channels have the same full unlabelled distribution of the three reports, as well as the same calibrated truth-and-one/two-report distributions. More strongly, **every proper marginal of the four-coordinate truth/report law agrees**. Additional unlabelled repetitions alone cannot identify which evidential interpretation is right.

The mechanism is inherited parity/missing-interaction mathematics. The bounded addition is its calibrated source-testimony realization, the complete sharp partial-identification interval, the exact accuracy threshold, and the distinction between learnable unlabelled agreement frequencies and the missing truth-sensitive calibration. This sharp result was not found in the inspected prior packets; no exhaustive project or literature novelty claim is made.

## 1. What was recovered, and what is not new

The three exact user-supplied Library files were already read completely and assessed in `scriptural-fibre-supplement-20261009`. Their recorded local projections rehash exactly to the retained bindings. Their source status remains independent research advice, including quoted earlier assistant claims, not independent primary evidence. This operation assigns **no new attachment-reading credit** and downloads no second copy.

The original supplement already separates raw observations from moments of laws, exact recovery from probabilistic warrant, target wording from commissioned content, and minimax error from a subject's error probability. Its two finite countercontrols remain intact. The completed communication-availability and commissioned-content-access operations already supply the source-owned explanatory-purpose condition, anti-empty-rescue test, and temporal-access countermodel. These results are recovered rather than redone.

The inspected Deep AX source explicitly requires joint architecture-conditioned likelihoods, allows products only under conditional independence, and warns that marginal multiplication may reverse evidence. The provenance-learning result already handles duplicate-root identity and conditional factorization. The tensor-likelihood closure result and inherited graded theorem already own parity collisions, all-proper-marginal insufficiency, and their likelihood-update consequences. Historical-source revision already transports parity to multiple retrospective revisions. None of those generic claims is new here.

The present question is more specific: **what exactly can one guarantee from source-by-source calibration and every pairwise independence check, even after the entire unlabelled report distribution is known?** It is motivated by the first attachment's request to use higher-order tensors and source-sensitive proof supports when apparently independent reports corroborate one another. No assumption of copying, a shared ancestor, selection, or failed authenticity is needed for this countercontrol. Conversely, the stipulated source labels do not authenticate any real source or prove causal independence.

## 2. A fully declared testimony channel

Let X in {0,1} be the truth value, with prior P(X=1)=alpha in (0,1). Let C=(C1,C2,C3) in {0,1}³ be a correctness vector, independent of X. Source i reports Yi=X when Ci=1 and Yi=1−X when Ci=0. Require

    P(Ci=1)=p,
    P(Ci=Cj=1)=p² for every i≠j,
    1/2 < p < 1.

These equations imply that each source has accuracy p under either truth value and that each pair of reports is conditionally independent given X. They do not require mutual conditional independence. Correctness independence from X makes the two truth-conditioned channels symmetric; it is a substantive model restriction, not a claim about all historical testimony.

Put t=P(C=111). Inclusion-exclusion forces every individual cell:

    111: t
    each of 110,101,011: p²−t
    each of 100,010,001: p−2p²+t
    000: 1−3p+3p²−t.

Conversely these cells, whenever nonnegative, sum to one and satisfy all the declared marginal constraints. This also proves exhaustiveness: exchangeability need not be added as an assumption; it follows from the specified equal first- and second-order marginals in this three-bit case.

Write K=1−3p+3p² and L=p(2p−1). Nonnegativity is equivalent to

    L ≤ t ≤ K.

Indeed the general lower bound is max(0,2p²−p)=L and the upper bound min(p²,K)=K for p>1/2. The interval has width K−L=(1−p)²>0. Its interior gives strictly positive mass to all eight correctness patterns.

These probabilities are a mathematical candidate class, not empirically measured accuracies. The law describes a simultaneous triple of reports about one binary target. It is not a historical sequence model, a theory of tawatur, or a definition of epistemic warrant.

## 3. Sharp posterior and evidence bounds

Observe E={Y1=Y2=Y3=1}. If X=1, this occurs exactly when C=111; if X=0, exactly when C=000. Hence

    P(E|X=1)=t,
    P(E|X=0)=K−t,
    P(X=1|E)=alpha*t / [alpha*t+(1−alpha)*(K−t)].

The event has positive probability throughout the admitted class, since alpha>0 and t≥L>0. The likelihood ratio is t/(K−t), with value +infinity at t=K. It is strictly increasing in t on [L,K), so the exact attainable Bayes-factor range is [L/(K−L),+infinity]. In particular

    BF_min=L/(1−p)²=p(2p−1)/(1−p)².

Every intermediate value is attained by its corresponding admissible t; the upper endpoint is an allowed boundary model. Restricting to full-support channels makes both endpoint posterior values limiting rather than attained. In that restriction the range is open, not closed.

The posterior rises above its prior exactly when BF>1. Thus the lower bound is at least one iff

    p(2p−1) ≥ (1−p)²,
    p²+p−1 ≥ 0,
    p ≥ (sqrt(5)−1)/2.

At the threshold, the boundary model is neutral evidence and every interior model gives strictly positive evidence. Below it, an open interval of strictly positive models reverses the unanimous claim's evidential direction. Above it, the direction is uniformly favorable in this class, though the posterior magnitude remains unidentified. These conclusions hold for every alpha in (0,1); the sharp posterior lower bound is obtained by substituting t=L in the displayed formula. No prior is claimed to be warranted by these equations.

At alpha=1/2, the denominator reduces to K/2, so P(X=1|E)=t/K. This proves the stated [L/K,1] interval without an approximation or a numerical optimization.

### Exact positive and negative controls

Take p=3/5 and alpha=1/2, so L=3/25 and K=7/25.

* The mutually independent model has t=p³=27/125 and posterior 27/35. Its Bayes factor is 27/8.
* The lower boundary has t=3/25 and posterior 3/7; its Bayes factor is 3/4.
* A fully interior model has t=13/100. Its masses are 13/100 at 111, 23/100 at each two-correct pattern, 1/100 at each one-correct pattern, and 15/100 at 000. Its posterior is 13/28 and Bayes factor 13/15. Every cell is positive, every source is 3/5-reliable, and every conditional pair is independent.
* Another fully interior model has t=1/5 and posterior 5/7. It supplies a strict opposite evidential direction within the very same retained calibration class.

This is not the claim that an actual trio with these summary statistics is unreliable. It shows that those particular summary statistics alone do not decide the sign of its unanimous evidence at this p.

## 4. Why full unlabelled report frequencies do not repair the gap

For alpha=1/2,

    P(Y=111)=P(Y=000)=K/2,
    P(Y=y)=p(1−p)/2 for every other report pattern y.

For each y, averaging over the two truth values pairs a correctness vector with its complement. The t terms cancel. Thus the **entire** eight-outcome law of Y is independent of t. The total is K+3p(1−p)=1, as required.

The pairwise calibration constraints fix every joint marginal on (X,Yi,Yj); their marginals fix all smaller sets involving X. The just-derived law fixes the remaining proper three-coordinate subset (Y1,Y2,Y3). Hence all proper marginals of (X,Y1,Y2,Y3) agree across t, while the posterior of X after Y=111 varies.

If unlabelled triples from independent fresh target instances are sampled under this same equal-prior stationary model, every finite sample has the same product distribution for every t. No estimator using only those samples can identify t uniformly across the class. This is a direct finite-law identifiability statement, not a bound on a particular learning algorithm. It does not cover nonstationary truth priors, labelled calibration, truth-related extra observations, or an independently justified causal factorization, which change the experiment.

The equal-prior qualification matters. For general alpha,

    P(Y=111)=(1−alpha)K+(2alpha−1)t.

If alpha is known and alpha≠1/2, this one frequency identifies t in the population limit. The posterior interval in section 3 still holds before that additional frequency information is supplied. We do not silently transport the unlabelled nonidentifiability claim to unequal priors.

## 5. Exact tensor transport and the positive repair

Use sign variables S=2X−1 and Zi=2Yi−1, with Wi=2Ci−1. Then Zi=S*Wi. At equal prior E[S]=0. The retained proper moments include

    E[S*Zi]=2p−1,
    E[Zi*Zj]=(2p−1)²,

with all other odd-S-dependent proper moments zero or fixed by the same constraints. The missing full interaction is

    tau=E[S*Z1*Z2*Z3]
       =E[W1*W2*W3]
       =8t−12p²+6p−1.

Its coefficient of t is nonzero. One supplied truth-sensitive third-correctness interaction t, or equivalently the four-coordinate sign moment tau, restores the entire joint law within this calibrated class and therefore every posterior after an admitted report. This is a positive one-scalar augmentation of the stipulated family; it is not an acquisition procedure or a promise that historical calibration is obtainable.

This distinction of grades is important. There are three correctness coordinates, but four semantic truth/report coordinates. Calling the missing object simply a third-order report moment would be false: the complete unlabelled three-report moment is already fixed. What is missing is its relation to truth. Tensor slot identity matters as much as order.

The inherited full-simplex parity result explains why this fibre exists. The present sharp identified interval solves the further nonnegativity/calibration restriction on that fibre and gives its evidential boundary. It does not alter the inherited generic continuation, graded-tensor, Gaussian geometry, or finite-polynomial no-go results.

## 6. Consequence for the supplied philosophical connection

The result offers a specific admissibility test for a proposed probabilistic corroboration argument: if its justification establishes only individual reliability and conditional pairwise independence, joint likelihood multiplication is unlicensed. Even learning all unlabelled agreement frequencies can leave the target-sensitive interaction undecided in a balanced model. The necessary repair is a justified full joint model, the relevant higher-order calibration, or a defensible restricted model that fixes or bounds it tightly enough for the desired conclusion.

This does not replace the first supplement's historical obligations. An actual scripture comparison still requires a named target, justified histories and evidence, source/meaning attribution, actual causal or probabilistic calibration, and the relevant warrant and mission premises. No finite accuracy number here is attributed to any tradition. Neither a posterior below one nor a nonzero minimax defect establishes absence of all warrant. No comparison of biblical autographs, Qur'anic rasm, recitations, or theological coherence is inferred.

The affirmative productive-ground, intrinsic-necessity, common-source, and recognition appraisals are unchanged. The packet adds a calibrated mathematical transport useful for evaluating the specific claim that pairwise-checked witness plurality supplies a sufficient joint evidence model.

## Verification and credit

`python3 verify.py` performs exact-rational checks of the cell law, all conditional pairs, all proper truth/report marginals, opposite posterior directions with full support, the independent control, all event probabilities, the missing tensor coordinate, endpoint sharpness over a rational grid, and the unequal-prior countercontrol. These finite checks corroborate the ordinary proof; they are not universal formal-kernel certification. The file manifest and input bindings record custody. Root-coordinated independent review is pending.
