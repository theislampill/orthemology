# Arbitrary adaptive root rates cannot improve the bounded-count exponent

8 October 2026 UTC. New mathematical sibling; all earlier stages remain frozen. The result concerns one fixed anonymous route histogram, not an arbitrary trial-resampled mixture. No physical calibration, route architecture, empirical trial, original-agent identification, kernel theorem, integration, owner acceptance or T20 closure is established.

## Answer and scope

For a fixed known number r of roots and a known total-route bound L, the inherited endpoint instrument needs order L^(2r) log(1/delta) observations in the worst case, even when it may adaptively choose arbitrary root-specific survival rates and issued profiles. This statement is uniform for 0<delta<=1/4, at fixed r (and fixed effect-catalogue size when multiple effects are included). The exact lower bound below applies throughout 0<delta<1/2 and uses binary relative entropy, not a uniform logarithmic approximation near delta=1/2.

The new lower bound matches the count exponent and confidence dependence of the frozen K-aware mask upper bound **on the same fixed-histogram class**. It does not claim optimal constants or dependence on the number of roots/effects. It does not supply a mixture-recovery upper bound, an expected-stopping theorem, or a lower bound for route-addressable gating or additional internal observations.

The declared action menu assigns one survival rate to every incidence belonging to a given root. The vector may change arbitrarily at every trial, but cannot give different rates to separately addressed route occurrences of the same root. Root-wise rates, anonymous endpoint measurements, and the response-law assumptions are indispensable scope restrictions.

## 1. Model and hard pair

There are r>=2 known roots, a fixed nonempty known effect catalogue E, and a fixed finite histogram of direct routes (P,N,T), with nonempty positive support P, absence guard N disjoint from P, and nonempty output bundle T contained in E. The total number of distinct route occurrences is at most the known integer L. This is precisely the type used in the inherited bounded-count upper theorem; our hard pair uses no guards.

Each trial chooses an issued profile S contained in the root set, and exact known root-specific survival rates a_i in [0,1]. Issued roots and guards are fixed before attenuation. For an enabled route, its success probability is the product of its positive-support rates. Different route occurrences succeed independently within the trial. The observer receives only the resulting union of effect bundles, along with its own chosen action.

Sharing a calibrated numerical rate across incidences does **not** mean sharing one random root gate across every occurrence. Independent incidence gates are one implementation of the stipulated law; independent whole-route gates with the same support-product probabilities are another. A single global random gate per root would correlate duplicate routes, collapse multiplicity information and invalidate both this product formula and the inherited count upper. The endpoint model does not identify which physical implementation, if any, realizes its stated law.

Conditional on the past and chosen action, the next endpoint has exactly that response law for the same unknown fixed histogram. Internal protocol randomness is allowed, but supplies no information about the unknown histogram. This fresh conditional response-kernel premise excludes unmodeled cross-trial emission coupling. The policy may adapt both the profile and the entire rate vector to all earlier actions and endpoints.

Assume L>=r+1 and set

k=floor((L-1)/r)>=1.

Construct H0 with k copies of each of the r singleton supports. Construct H1 by adding one route whose support is the entire root set. Every route in both histograms emits the whole bundle E. The totals are rk and rk+1, respectively, both at most L. The distinction between per-root count k and total bound L must be retained.

Every root occurs in the common productive baseline, both inventories are nonempty, and the complete effect catalogue can occur. The construction does not depend on an empty inventory or an unrepresented root.

At a proper issued profile the added route is disabled, so the entire endpoint laws agree. At the full profile put

u_i=1-a_i, q0=product_i u_i^k, z=product_i a_i, q1=q0(1-z).

The endpoint is either empty or the whole bundle E, with no-effect probabilities q0 and q1. Thus even observing the full multi-effect endpoint gives exactly the binary information used in the lower bound.

## 2. Uniform information bound for every rate vector

Define

C(r,k) = [2/(k(k+3))] [4/(k+1)^2] [4/(k+2)^2]^(r-2).

We prove that the relative entropy KL(P0^action || P1^action) of a single endpoint law is at most C(r,k), for every profile and every rate vector.

Proper profiles already give zero. At a full profile, if some a_i=0 then z=0 and q0=q1. If some a_i=1 then the k>=1 singleton baseline at that root succeeds surely, q0=q1=0. Thus every boundary vector also gives zero. The latter conclusion would fail for an unbalanced baseline missing that root; see NEGATIVE_CONTROLS.md.

It remains to consider 0<a_i<1 for all i. The inequality log t<=t-1 gives the elementary Bernoulli chi-square bound

KL(Ber(q0)||Ber(q1)) <= (q0-q1)^2/[q1(1-q1)]
= q0 z^2 / [(1-z)(1-q1)].

Since z<=a_2 and q1<=q0<=u_1^k,

1-z >= u_2,
1-q1 >= 1-u_1^k = a_1 sum_(j=0)^(k-1) u_1^j.

Arithmetic-geometric mean gives sum_(j=0)^(k-1) u_1^j >= k u_1^((k-1)/2), including k=1. Substitution bounds the divergence by the separable product

[u_1^((k+1)/2) a_1/k] [u_2^(k-1) a_2^2] product_(i=3)^r [u_i^k a_i^2].

For alpha>=0 and b>0, the maximum of u^alpha(1-u)^b on [0,1] is attained at alpha/(alpha+b), with the alpha=0 endpoint interpreted directly. Dropping the factor [alpha/(alpha+b)]^alpha gives the convenient bound [b/(alpha+b)]^b. Applying it to the three displayed factor types gives, respectively,

2/[k(k+3)], 4/(k+1)^2, and 4/(k+2)^2.

Their product is C(r,k). Empty products at r=2 equal one. The k=1 second factor is (1-u_2)^2<=1=4/(k+1)^2. No interior variance floor is assumed; small denominators are controlled by the corresponding rate factors.

## 3. Adaptive profiles and rates

Let a protocol use a fixed budget N of endpoint trials. Under H0 and H1, its conditional action-selection kernel is the same function of any common past transcript. Action selection itself therefore contributes zero conditional divergence. Given the selected action, the next endpoint contributes at most C(r,k), by the previous section. Factoring transcript likelihoods and taking expectations yields

KL(full transcript under H0 || full transcript under H1) <= N C(r,k).

This argument allows a continuum of rate vectors, randomized policies and arbitrary interleaving of issued profiles. It is a fixed-budget conditional-chain proof; no stopping-time interchange is needed or claimed.

Suppose every eligible histogram with at most L routes must be reported correctly with probability at least 1-delta, where 0<delta<1/2. Let A be the event that the report is H0. Then P0(A)>=1-delta and P1(A)<=delta. Grouping the transcript likelihood terms into A and its complement gives the log-sum/data-processing inequality

KL(transcript0||transcript1) >= kl(P0(A),P1(A)) >= kl(1-delta,delta),

where kl(p,q)=p log(p/q)+(1-p)log((1-p)/(1-q)). Monotonicity on p>q proves the second inequality. Therefore

N >= kl(1-delta,delta)/C(r,k)
= [k(k+3)(k+1)^2(k+2)^(2r-4)/(2*4^(r-1))] (1-2delta) log((1-delta)/delta).

This is the exact stated lower bound. In particular C(r,k)<=2*4^(r-1)/k^(2r), so for 0<delta<=1/4,

N >= [k^(2r)/(4*4^(r-1))] log(1/(2delta)).

At fixed r, k=floor((L-1)/r) is proportional to L. The conclusion is consequently Omega(L^(2r) log(1/delta)) in that confidence range. At r=1 the separately frozen one-root arbitrary-rate theorem supplies the corresponding exponent two. No constants uniform in growing r are claimed.

## 4. Same-class matching with the inherited upper bound

The frozen noise-aware-calibration/THEOREMS.md uses a known valid total count bound, named K there. Instantiate its K with **L**, not the hard pair's per-root k. It assumes the same known finite roots, direct-route response law, fixed inventory, exact calibrated root-wise rates, and endpoint observation. These assumptions include both H0 and H1.

Its menu is a subset of the current allowed menu: at each issued profile S, choose a nonempty mask V contained in S, set rates p=1/(2L) on V and zero on the remaining issued roots, and keep the issued profile/guard evaluation fixed. Independent route-success episodes give its logarithmic subset inversion, integer rounding and finite-confidence guarantee.

For the full guarded, m-effect class, with fixed m=|E|, that theorem uses

G=3^r-2^r actuator settings,
Q=G(2^m-1) retained event coordinates,
n_setting=ceil[128(16L^2)^r log(2Q/delta)].

One paired endpoint supplies every effect-query indicator at its chosen setting, so total endpoints are G*n_setting, not Q*n_setting. The theorem identifies every histogram in the stated L-bounded guarded/multi-effect class. Its arithmetic rounding and endpoint probability floor are part of that imported proof, not newly reproduced claims here.

For the narrower unguarded one-effect class, keep only the full issued profile with its nonempty masks: G0=Q0=2^r-1. The same positive-support inversion recovers all route-support counts, and the total budget is

(2^r-1) ceil[128(16L^2)^r log(2(2^r-1)/delta)].

The hard pair belongs to this narrower class already. It also belongs to the larger guarded/multi-effect class through the common-bundle embedding above, where full endpoint observation offers no further distinguishing information. Thus both upper/lower comparisons are genuinely on the same class and observation menu, not merely matching powers from unrelated experiments.

At fixed r>=2 and fixed m where relevant, for L>=r+1 and 0<delta<=1/4, the worst-case fixed-budget endpoint complexity in either declared class is Theta(L^(2r) log(1/delta)), with constants depending on r (and m for the larger class). Exact calibration and fresh conditional sampling are shared assumptions. The wider arbitrary-rate menu cannot improve that worst-case L exponent, although it may improve constants or performance on a narrower catalogue.

## 5. Limits and calibration

The upper is a fixed-histogram decoder. If a different latent histogram is independently drawn before every trial, the inherited all-rate mixture collision still applies. A lower bound on a point-mass subfamily also constrains a mixture-support procedure required to handle that subfamily, but it supplies no matching arbitrary-mixture upper bound or persistence theorem.

The rate calibration is exact in the matched theorem. The inherited noisy upper offers its separately justified endpoint-bias budget, eta<=epsilon/(2Lr) with epsilon=p^r/(16*2^r), and a fourfold sampling coefficient. That is a sufficient vanishing calibration allowance, not a proved necessary or optimal multiroot tolerance. Arbitrary unknown calibration drift or dependence is outside the matched theorem.

The root-wise common-rate and endpoint-only restrictions matter. A device that could address the added full-support route independently from every singleton could suppress the baseline and turn that route fully on, defeating this pair in one trial. That is a different measurement instrument with additional route-addressing information. Likewise, observing route successes or incidence traces can add information unavailable at the common endpoint. The theorem does not infer or validate any physical actuator architecture.

The raw number of roots or effects can grow, changing the constants and the number of settings; the fixed-dimension asymptotic is not a polynomial guarantee jointly in all parameters. No expected stopping-time result, minimax constant, metaphysical source count, source-admissibility bridge, empirical observation or integration authority follows.
