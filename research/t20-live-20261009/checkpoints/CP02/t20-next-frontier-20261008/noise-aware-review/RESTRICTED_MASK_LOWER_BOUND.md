# Matching count exponent for the fixed-mask instrument

8 October 2026. A separate lower-bound consequence developed after the CRT freeze. It concerns the K-aware family with the fixed nonzero rate p=1/(2K), and does not claim a lower bound against arbitrary attenuation rates or additional measurements.

## Statement

Fix r>=1 known roots and an integer route-count bound K>=2. At each trial, a protocol may choose any root mask T, giving roots in T incidence survival p=1/(2K) and roots outside T survival zero. It observes only the endpoint. It may choose subsequent masks adaptively from all earlier masks and outcomes, and may use internal randomization. Trials follow the declared independent route-success law conditional on their chosen mask.

If a protocol using a fixed total budget N identifies every histogram in the K-bounded class with probability at least 2/3, then

    N >= (2K)^(2r) / 45.

The same bound applies to equal-prior discrimination of the particular two models below. It establishes the necessity of the K^(2r) exponent for this fixed-p mask family at fixed confidence and fixed r. It is not a universal experimental complexity bound.

## A hard two-model family

Choose one root A. Model 0 has K-1 distinct routes supported by {A}. Model 1 adds one route supported by the full root set R. All routes emit the same designated nonempty effect bundle. Both models satisfy the count bound and have no absence guards.

At any proper mask T, the added full-support route has zero success probability, so the entire endpoint laws agree. Only the full mask distinguishes the models. At that mask their no-effect probabilities are

    q0 = (1-p)^(K-1),
    q1 = q0 (1-p^r).

Thus Delta=q0-q1=q0 p^r<=p^r. This remains a binary endpoint law if the designated bundle is the entire known effect catalogue: outputs are either empty or that whole bundle. Access to the entire endpoint does not add distinguishing information beyond the Bernoulli outcome in this example.

## Uniform relative-entropy bound

Because p^r<=p,

    q1 >= (1-p)^K >= 1-Kp = 1/2.

For a natural m, (1-p)^(-m)>=1+mp follows from Bernoulli's inequality, so

    q0 <= 1/[1+(K-1)p] <= 4/5,

where the last step uses K>=2. Hence 1-q1>=1-q0>=1/5, and

    q1(1-q1) >= 1/10.

For Bernoulli parameters u,v in (0,1), applying log t<=t-1 to each term gives the standard bound

    KL(Ber(u) || Ber(v)) <= (u-v)^2/[v(1-v)].

Substituting q0,q1 yields KL<=10 p^(2r). All other masks have zero KL because their response laws coincide.

## Adaptive allocation and testing

For an adaptive protocol, condition on each past transcript. Its next-mask selection rule is the same under both models, so selecting a mask adds no conditional KL. The resulting observation contributes at most 10 p^(2r), and contributes zero for a proper mask. The chain rule therefore bounds full-transcript KL by 10N p^(2r), even when the allocation of masks is adaptive.

Pinsker's inequality gives total variation at most sqrt(5N p^(2r)). Equal-prior testing success is at most (1+TV)/2. Success at least 2/3 requires TV>=1/3; therefore 5N p^(2r)>=1/9, which is exactly the stated bound.

Relative entropy, its chain rule, Pinsker's inequality and the testing identity are standard tools. Their application here identifies a concrete hard family; they are not new general theorems.

## Comparison with the upper bound

The error tolerance epsilon=p^r/(16·2^r) gives a sufficient sample count of order K^(2r) per setting at fixed r and fixed confidence, under either the stated concentration bound or its variance/union-bound version. There are finitely many masks depending only on r. Thus the total upper and lower budgets match in their K exponent for this specific instrument family. Constants, dependence on r, confidence dependence and sample-optimal allocation have not been optimized.

This does not contradict the unbounded-count fixed-rate impossibility result: the instrument here chooses p using the known K. It also does not exclude better dependence from instruments allowed to choose other nonzero rates, observe more than endpoints, exploit a narrower model class, or use external causal information.

The current class does not require every root to occur in an active route. If that additional condition is imposed, assume K>=r+1 and distribute the K-1 singleton baseline routes with at least one at each root. The full-mask probability remains (1-p)^(K-1), all proper-mask endpoint laws still agree between the two models, and the same lower bound follows.

The theorem is about a fixed total budget, not an unproved statement about arbitrary expected stopping times. Unknown or invalid K, unmodeled calibration error, correlated trial generation and causal applicability remain separate premises. No protected edits, integration, historical research floor or field-wide priority claim is made.
