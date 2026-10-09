# Interaction supports remove the coordinate-calibration gauge

8 October 2026 UTC. This separate continuation preserves the productive-identifiability, global-calibration-ambiguity and grouped-calibration-invariants stages. It classifies exact population equivalence for a fixed finite unguarded, one-effect inventory. It does not solve the latent-mixture problem, certify physical calibration, claim finite-sample or computational efficiency, or authorize integration or T20 closure.

## 1. Model and answer

Let R be a known finite set of labeled root indices. For each nonempty S contained in R, let n_S be a nonnegative integer counting independent route occurrences with positive support exactly S. The inventory is fixed throughout the experiment and finite; every route produces the same one designated effect. There are no absence guards, spontaneous routes, latent inventory mixtures, within-route repeated root incidences, indirect or cyclic routes, or additional endpoint channels.

Each root i has one unknown static calibration homeomorphism r_i:[0,1] -> [0,1]: continuous, strictly increasing, r_i(0)=0 and r_i(1)=1. A route on S succeeds with probability product_(i in S) r_i(x_i), and distinct route occurrences succeed independently. The same r_i applies to every occurrence and support containing i. This specifies the endpoint law; independent incidence gates realize it, but that gate architecture is not inferred from it.

The supplied datum is the exact entire command-indexed probability of no effect,

    Q(x) = product_(nonempty S subset R) (1-product_(i in S) r_i(x_i))^n_S.

A zero-count factor is omitted, including at boundary points. Thus no undefined 0^0 convention is required. A positive-count factor can vanish on a boundary face. In this unguarded model, issuing only roots T gives the same endpoint law as setting coordinates outside T to zero; a single full issued profile with the full attenuation cube already suffices. This statement would need revision with absence guards.

Define the anchored root set

    A = union of S such that |S|>=2 and n_S>0.

Then Q determines:

- exactly which supports S have positive multiplicity, including supports absorbed by smaller supports in the deterministic Boolean endpoint;
- n_S for every |S|>=2;
- the complete calibration map r_i for every i in A;
- the unary multiplicity n_{i} for every i in A.

For an unanchored root i outside A with n_{i}>0, Q determines only its unary response curve (1-r_i(x))^n_{i}. Its multiplicity can be any positive integer m, provided its calibration becomes

    r'_i(x) = 1-(1-r_i(x))^(n_{i}/m).

An unused root, having no positive support containing it, has an entirely unobserved calibration. These are all remaining equivalences. In particular no connectivity between different interaction supports is needed: every support of size at least two anchors every one of its own roots, even in a disconnected support hypergraph.

The identification is of anonymous multiplicities indexed by known support labels. It does not identify route occurrence names, source ownership or metaphysical bearers.

## 2. Mask/log inversion isolates one support

For nonempty S and a vector x_S with 0<x_i<1 for i in S, let x_T denote the full command vector that agrees with x on T contained in S and is zero elsewhere. Every Q(x_T) is strictly positive: every nonzero route success probability is strictly below one. Set Q(x_empty)=1 and define

    L_S(x_S) = sum_(T subset S) (-1)^(|S|-|T|) log Q(x_T).

For a route support U, its log contribution is zero unless U is contained in T, since r_i(0)=0. In that case the contribution is the same n_U log(1-product_(i in U)r_i(x_i)) for every T containing U. Its coefficient in the alternating sum is

    sum_(U subset T subset S) (-1)^(|S|-|T|),

which is one for U=S and zero otherwise. Hence

    L_S(x_S) = n_S log(1-product_(i in S)r_i(x_i)).                 (1)

Every interior r_i is strictly between zero and one. Consequently L_S is identically zero exactly when n_S=0, and is strictly negative at every interior point exactly when n_S>0. One exact interior evaluation of each isolated contrast identifies support presence under the model promise. Exact zero testing is part of this population statement, not an operation supplied by arbitrary approximate data.

The equivalent multiplicative contrast

    E_S(x_S) = product_(T subset S) Q(x_T)^((-1)^(|S|-|T|))
             = (1-product_(i in S)r_i(x_i))^n_S

allows exact rational finite controls without numerical logarithms. It does not avoid the need for accurate data in applications.

### Boundary discipline

Do not substitute unit commands directly into the raw alternating log expression: individual Q(x_T) can vanish because a lower-order route succeeds certainly, creating undefined cancellation of infinities. Instead first isolate L_S on the open coordinate cube. Equation (1) supplies its unique finite continuous extension to every face on which product_(i in S)r_i(x_i)<1. In particular, all but one coordinate may approach one while the remaining coordinate stays interior. At the all-one corner a positive L_S diverges to minus infinity; that corner is never used as a finite log value below. Values of L_S at zero-product faces are zero.

## 3. Complete observational-equivalence theorem

Compare two admissible worlds (n,r) and (n',r'). If Q=Q' on the entire cube, their L_S agree, so they have the same positive supports. For a positive support S write c=n_S/n'_S>0 and define the coordinate homeomorphism

    alpha_i = r'_i composed with r_i^(-1).

Its domain is all [0,1], its endpoints are fixed, and it is continuous. Because the actual coordinate values a_i=r_i(x_i) range independently over (0,1), equality of (1) gives

    product_(i in S) alpha_i(a_i) = H_c(product_(i in S)a_i),
    H_c(z) = 1-(1-z)^c.                                        (2)

Let all coordinates except i tend to one in (2). Endpoint preservation and continuity give alpha_i(a)=H_c(a). If |S|>=2, retain distinct i,j and let every other coordinate tend to one. Thus

    H_c(ab) = H_c(a)H_c(b),  0<a,b<1.                          (3)

The known elementary function H_c has right slope c at zero: H_c(a)/a -> c. Divide (3) by a and take a down to zero, obtaining cb=c H_c(b), and therefore H_c(b)=b. Taking the same right limit at zero gives c=1. No derivative or modulus of continuity of an unknown calibration map was assumed. It follows that n_S=n'_S and alpha_i is the identity for each i in S, so r_i=r'_i on the whole interval.

Taking the union over every positive interaction support identifies all calibration maps on A. For a unary support on an anchored i, equality reads

    n_{i} log(1-r_i(x)) = n'_{i} log(1-r_i(x)).

The logarithm is finite and nonzero for an interior x, so the unary multiplicities agree, including the already-detected zero case.

For i outside A, all supports containing i other than {i} are absent. If n_{i}>0, unary equivalence is exactly

    (1-r_i(x))^n_{i} = (1-r'_i(x))^n'_{i},

and solves to the displayed power recalibration with m=n'_{i}>0. Every positive m gives another allowed homeomorphism. Zero cannot be substituted for a positive multiplicity, since its response would be identically one. If n_{i}=0, Q is independent of x_i, and any allowed r'_i is equivalent.

Conversely, retain every interacting support count and anchored map, retain anchored unary counts, apply arbitrary permitted unary power replacements to the isolated positive-unary roots, and choose arbitrary maps for unused roots. Every factor in Q is then preserved, proving sufficiency and the completeness of the classification.

### Observation process qualification

Q supplies the full one-trial binary endpoint law. If repeated trials use fresh endpoints with conditional Bernoulli no-effect probability Q(x), even after adaptive commands, equality of Q gives equality of every adaptive/stopped transcript law by coupling a common protocol seed and common fresh uniform variables. No arbitrary temporal joint law is claimed to be determined by its one-trial marginals. Inventory persistence, common coordinate calibration and conditional trial independence are separate premises when that process extension is used.

## 4. Constructive population reconstruction

There is an explicit inverse in terms of exact function operations and limits. It is not advertised as a halting algorithm from Cauchy approximations, a finite-query reconstruction procedure or a finite-sample estimator.

1. Form all L_S on the open cube, and detect their positive-support pattern using (1).
2. For a positive support S with |S|>=2 and distinct i,j in S, use the continuous extension described above to define

       D_ij(u,v) = L_S(x_i=u,x_j=v,x_k=1 for k in S\{i,j})
                  = n_S log(1-r_i(u)r_j(v)).

   The notation at unit coordinates denotes the isolated-function limit, not a raw log-mask calculation. For 0<u<1 and 0<=v<=1 this is finite, including D_ij(u,1)=n_S log(1-r_i(u))<0.
3. Recover every participating r_j by

       r_j(v) = limit_(u down to 0) D_ij(u,v)/D_ij(u,1).          (4)

   Indeed a=r_i(u) tends to zero, and log(1-a b)/log(1-a) tends to b for each b in [0,1]. The multiplier n_S cancels. For v=0 and v=1 the ratios are exactly zero and one. Swapping i,j recovers r_i; each other root in S can be paired with any distinct root of S. No calibration differentiability is needed.
4. For any positive interaction support, evaluate at any interior x_S and recover

       n_S = L_S(x_S) / log(1-product_(i in S)r_i(x_i)).

   The denominator is finite and nonzero. An anchored unary count follows from its analogous unary quotient; absent counts are zero.

For an isolated positive-unary root no canonical actual count or calibration is selected. A convenient representative of its observational equivalence class has count one and calibration 1-exp(L_{i}(x)); calling this representative the true count or calibration would add an unsupported assumption.

In promised exact-population data the recovered counts are integers and every overlapping support yields the same recovered root map. Such consistency conditions are necessary model checks. No finite set of tests here certifies that arbitrary observed functions or a physical experiment satisfy all model assumptions.

## 5. Exact countercontrols and failed transports

### 5.1 The unary gauge really remains

Count two with identity calibration has no-effect curve (1-x)^2. Count one with calibration H_2(x)=2x-x^2 has exactly the same entire curve. Both maps are allowed homeomorphisms. Apply this independently to isolated unary coordinates. Adding other unrelated interaction components does not anchor those isolated roots.

### 5.2 An actual interaction defeats that unary recalibration

For one positive AB support, transforming both rates by H_2 cannot compensate a count change from two to one: H_2(ab)-H_2(a)H_2(b)=-2ab(1-a)(1-b), which is nonzero for interior a,b. At a=b=1/2, the two-route identity-calibrated no-effect probability is 9/16, while the one-route H_2-calibrated probability is 7/16. Solo-edge restrictions agree, but the joint response separates them. The proof covers all positive count ratios, not merely this control.

### 5.3 Boolean absorption is not absorption under independent routes

An A route and an added AB route have the same unattenuated monotone Boolean endpoint as A alone when all occurrences use one shared A gate and one shared B gate. Under the stipulated independent route law their absence probabilities are respectively (1-a)(1-ab) and 1-a, differing at interior a,b. Thus the theorem identifies the absorbed support only because the declared stochastic endpoint channel retains it. It does not recover an AB support under the shared-gate channel, where duplicate and absorbed routes stay invisible at all commands.

### 5.4 Sharing calibration across supports is essential to transfer an anchor

Take an AB route with identity calibrations plus two unary A routes with identity calibration. An alternative retains the AB route and replaces the unary A pair by one unary A route with calibration H_2. The complete Q is unchanged. Its unary A map differs from the A map used in the AB route, so it violates precisely the cross-support common-calibration premise. An AB observation cannot identify the unary count if a support-specific hidden calibration is allowed.

### 5.5 Coordinatewise calibration is essential even with own-input endpoint preservation

For a pure AB inventory with count n versus m, put c=n/m. Starting from identity maps, define an alternative context-dependent calibration by

    r'_B(a,b)=H_c(b),
    r'_A(a,b)=H_c(ab)/H_c(b) for b>0,
    r'_A(a,0)=a.

For each fixed other coordinate, each root map is continuous, strictly increasing in its own input and preserves its own zero and one endpoints. Joint continuity at b=0 follows from H_c(z)/z -> c uniformly for 0<=z<=b as b down to zero; at all other points the denominator is positive. Yet r'_A depends on b. Their product is H_c(ab), so

    (1-r'_A(a,b)r'_B(a,b))^m=(1-ab)^n

on the entire square. This is an all-command cross-talk counterexample, not a relabeling.

The exact rational instance n=2,m=1 is

    r'_B=b(2-b), r'_A=a(2-ab)/(2-b).

The denominator stays at least one; r'_A(a,b)-a=ab(1-a)/(2-b). This explicitly verifies the own-input endpoints, continuity, nontrivial cross-talk and identical endpoint law.

### 5.6 Non-homeomorphic endpoint maps can erase multiplicities

If every calibration instead takes only values zero and one through an endpoint-preserving monotone step, a positive interaction factor is either zero or one. Any positive multiplicity on that support then gives the same response. Continuity/strict monotonicity are sufficient premises here; the theorem does not claim a minimal regularity characterization. An allowed class that lacks any genuine interior true rate defeats the stated inference.

### 5.7 Guards, latent mixtures and physical interpretations are different models

At a fixed issued full profile, A-with-absence-of-B routes are disabled regardless of attenuation. They cannot be recovered from Q on that one profile. Equating attenuation masks with issued-profile changes would reevaluate the guard and invalidate the mask derivation. With all issued profiles a guarded extension might be studied separately; none is proved here.

For a fresh latent inventory mixture, Q is an average of inventory-specific products. Logarithms no longer turn it into a sum of fixed-support contributions, so (1) need not hold. For example, an equal fresh mixture of one A route and one B route has Q(a,b)=1-(a+b)/2 and isolated multiplicative contrast E_AB=[1-(a+b)/2]/[(1-a/2)(1-b/2)]<1 at interior a,b, although neither inventory contains an AB route. Calling that contrast evidence for a fixed AB route would confuse latent mixture dependence with the stipulated fixed-inventory factor. Held-inventory grouped laws are a further, distinct observation model; no grouped-mixture classification is transferred here.

The current synthesis transports an explicit Boolean-lattice inverse and uses the cross-coordinate interaction equation to break a nuisance equivalence. It does not infer physical gate architecture, warranted interventions, actual causal independence, original-agent perfections or complete productive adequacy. No finite-sample/runtime/physical calibration guarantee, external priority claim, protected write, final integration or T20 closure follows.
