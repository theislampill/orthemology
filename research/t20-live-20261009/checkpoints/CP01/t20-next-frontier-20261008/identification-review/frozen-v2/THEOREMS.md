# Conditional identification of direct productive routes

8 October 2026. Ordinary finite probability, unique factorisation and Boolean-lattice inversion are used below. No new general mathematical theorem or metaphysical possibility is claimed. The new result is the exact identification boundary for the declared causal interface.

## Declared model and observation law

There are two original-root indices A,B and a known nonempty finite created-effect catalogue E. They are different types. Each distinct productive route occurrence has:

- nonempty positive root support P;
- an absence guard N disjoint from P;
- nonempty output subset T of E.

P,N have exactly five possible types: (A,empty), (B,empty), (AB,empty), (A,B), (B,A). Write their multiplicities for each T as a(T), b(T), c(T), d(T), e(T). These nonnegative integers count distinct route occurrences in the supplied interpretation. They do not count original bearers, created births, intrinsic acts or representations of one occurrence. There are finitely many routes, with no known count bound needed for the exact theorem. There are no spontaneous, indirect or cyclic routes.

A route is enabled when all P are in the issued profile S and no N are in S. A trial first fixes S. Guards stay evaluated on this issued profile throughout that trial. Each positive incidence of each enabled route then independently survives: probability x=1/2 for an A incidence, y=1/3 for a B incidence. A route succeeds exactly when all its positive incidences survive and, if successful, emits every member of T together. The created endpoint is the union of successful output subsets. All gates of distinct actual occurrences are independent; aliases of one occurrence share its gates.

The readout exposes only that endpoint subset. It does not disclose route IDs, root support, guards or route count. The intervention law, catalogue, root indexing, rate calibration, trial comparability and independence assumptions are external premises. They do substantial semantic work and are not inferred from the readout. A zero incidence-survival rate still leaves the issued root present for guards. Changing S is a separate intervention.

For U a nonempty subset of E, let q_S(U) be the exact probability that no member of U occurs. This is a population probability, not an empirical frequency measured with finite precision.

## Theorem 1 Exact one-effect recovery

For one effect, at issued AB only the a,b,c routes are enabled. Route failure probabilities are respectively 1/2, 2/3 and 5/6. Independence gives

q_AB = (1/2)^a (2/3)^b (5/6)^c.

For a prime p let v_p(q) be its exponent in the nonzero rational q. Unique factorisation gives

c = v_5(q_AB),
b = -v_3(q_AB) - c,
a = b - c - v_2(q_AB).

The transformation is injective for all finite nonnegative integer counts. Empty route inventories yield q=1 and zero valuations, so they are included. No route-label observation or additive created-work measurement is used.

At issued A, q_A=(1/2)^(a+d), hence d=-v_2(q_A)-a. At issued B, q_B=(2/3)^(b+e), hence e=-v_3(q_B)-b. Thus three exact endpoint probabilities identify all five anonymous route multiplicities.

The decoder also checks nonnegative integer counts and reconstructs the probability, rejecting rationals with incompatible prime factors or signs. Such checks test membership in the assumed observation family. They do not independently certify that an observed world has that causal structure.

### Sharp profile requirement

Among probes made at one fixed issued profile at a time, all three nonempty profiles are necessary for identification over the full guarded class, even if arbitrary incidence rates may be used at every queried profile.

If A is omitted, add one A-with-absence-of-B route. It is never enabled at B or AB. If B is omitted, use the symmetric guarded route. If AB is omitted, add an AB route. It is never enabled at either solo profile. Each addition changes only the omitted profile's response. A common productive baseline can be present in both alternatives, so the witness does not depend on one alternative having no unattenuated output.

This is a lower bound on the permitted profile-query family. It does not rule out other kinds of measurement, pooled profile mixtures, direct observation of causal structure, or a narrower model class. The null profile supplies no information in this positive-root class. “Three probabilities” is not a universal information-theoretic lower bound on arbitrary encodings.

## Theorem 2 Recovery across multiple effects

For each root/guard type j define its hit count

h_j(U) = sum of n_j(T) over nonempty T intersecting U.

A route affects the no-U event exactly when its output subset intersects U. Thus the same product factorisation and the same three-profile decoding recover all five h_j(U) for every nonempty U. The route's shared survival event across all members of T is essential here.

Fix one j and put h(empty)=0. Let M=h(E), the total number of that type of route. Define

F(V) = M - h(E minus V).

The routes excluded by the hit count on E minus V are exactly those whose nonempty output subsets lie within V. Consequently F(V)=sum over T subset of V of n(T), with n(empty)=0. Boolean-lattice inversion gives

n(T) = sum over V subset of T of (-1)^(|T|-|V|) F(V).

To check the inversion, substitute the expression for F and exchange finite sums. The coefficient on n(W) is the alternating sum over W subset of V subset of T. It is 1 if W=T and 0 otherwise, by (1-1)^(|T minus W|).

Therefore three full endpoint distributions, one at each nonempty issued profile and the calibrated incidence rates, determine the complete anonymous histogram (P,N,T) of the declared direct routes. This identifies that histogram up to permutation of route-occurrence names. It does not identify numerical route IDs, temporal order, indirect lineage or original perfections.

The 2^|E|-1 joint-absence probabilities at one profile are coordinates computed from one joint endpoint law. They are not 2^|E|-1 separate actuator settings. Simultaneously observing which catalogue members occur can provide all those coordinates from the same trials. Separate marginal samples without within-trial pairing do not provide the joint law.

### Why higher-order output information is needed

One AB route emitting {e1,e2} and two distinct AB routes emitting {e1} and {e2} have equal single-effect absence probabilities, each 5/6. Their joint absence probabilities are 5/6 and 25/36. Their unattenuated created catalogue is the same {e1,e2}. The difference concerns a shared operative route, not the number of created effect tokens.

There is a sharp coordinate result for the hit/absence representation. If an observer is supplied exclusively the retained coordinate values and any nonempty U0 coordinate is discarded at every issued profile, those values are insufficient over the unrestricted finite-count class. If the full raw joint endpoint law or paired trial records are also retained, the omitted coordinate is recomputable, so this obstruction does not apply. Set C=E minus U0 and define, for nonempty T,

delta(T) = (-1)^(|T|-|C|+1) if C is a subset of T, and 0 otherwise.

This is the inverse hit transform of a unit change at U0. Therefore sum over T intersecting U of delta(T) equals 1 when U=U0 and 0 otherwise. Split delta into its nonnegative positive and negative parts to obtain two one-root route inventories. Add the same singleton-output baseline to both if every effect must occur unattenuated. They agree on every retained hit coordinate and differ at U0. Since the failure base lies strictly between 0 and 1, their retained absence coordinates also agree and the omitted one differs.

This result concerns deleting that output coordinate family from all profile observations. It does not say every redundant scalar in the full five-type panel is individually necessary, nor that arbitrary alternative encodings require this coordinate format. More compact target-specific summaries may answer weaker questions.

## Gate semantics and exact failures of transport

1. Uniform independent thinning of whole routes with one probability z reveals only the number of enabled routes at each profile: q_S=(1-z)^N_S. In the one-effect class these counts are N_A=a+d, N_B=b+e, N_AB=a+b+c. Its entire fibre is the nonnegative integer set a<=N_A, b<=N_B, a+b<=N_AB, with d=N_A-a, e=N_B-b, c=N_AB-a-b. Coalescence and priority both give (1,1,1); uniform route thinning cannot distinguish them at any z. This is a full class-relative fibre description, not merely one equal-output example.
2. One gate per bearer with guards held fixed can separate coalescence from priority. It cannot reveal duplicate A routes or an AB route absorbed by an enabled A route: their Boolean success conditions remain A-gate in every case. The stronger theorem assumes the specified support-dependent route success probabilities and independence across distinct occurrences, supplied here by incidence gates. A single independent gate per route with the same product-dependent success probability has the identical endpoint law; the physical gate architecture itself is not identified. Under shared gates, the active monotone Boolean function depends only on its minimal enabling antichain; adding duplicate or larger absorbed supports leaves it unchanged.
3. A shared bearer gate interpreted instead as deleting the issued act forces guard reevaluation. The recovered coalescent, redundant and priority laws all then induce the same OR response over remaining roots. This operation is distinct from the preceding fixed-guard efficacy gate.
4. Unknown calibration defeats the simple recovery. One A route surviving with probability 3/4 and two independent A routes each surviving with probability 1/2 both have absence probability 1/4 at A and AB, and no output at B. The entire three-profile readout agrees. Calibration is not optional.
5. Repeating a representation of an occurrence does not create another independent gate. The executable record interface deduplicates equal records carrying one occurrence ID and rejects conflicting versions. Two distinct IDs count as two actual occurrences only under the explicitly supplied interpretation; numerical labels do not establish that fact metaphysically.

No theorem here turns one original bearer into many originals, identifies an intrinsic act with a created effect, or interprets computational gate records as created causal intermediates.

## Exact recovery versus finite samples

For the fixed calibrated instrument, unbounded route multiplicity precludes a uniform finite-sample guarantee. Compare k and k+1 A-only routes. Their absence probabilities are 2^(-k) and 2^(-k-1); their single-trial total variation distance is 2^(-k-1). For n independent trials, a product coupling gives total variation at most n times that distance. With equal prior weights, any discriminator's success is at most (1+n 2^(-k-1))/2. Achieving success at least 2/3 therefore requires n>=2^(k+1)/3. This lower bound concerns this fixed-rate instrument, not every adaptive choice of attenuation rate.

Even a bounded class containing two nondegenerate Bernoulli response laws cannot be identified with zero error from a fixed finite number of samples: every finite binary sample sequence has positive probability under both laws. A confidence statement is therefore essential.

A known total-route bound K gives a finite robustness guarantee. Every panel probability has denominator dividing 6^K. Since exact identification is injective, two admissible model panels differ in some coordinate by at least Delta=6^(-K). Let L=3(2^|E|-1). With n independent trials at each profile, each empirical absence frequency has variance at most 1/(4n). By the squared-deviation inequality and a union bound, the probability that any coordinate error reaches Delta/3 is at most 9L/(4n Delta^2). Thus n>=9L/(4 delta Delta^2) suffices for error probability at most delta under nearest-panel classification in the maximum-coordinate (ℓ∞) norm of the finite K-bounded class. Coordinate observations within one trial need not be independent for this union bound.

This deliberately loose upper bound is not an optimal sample complexity claim. Empirical frequencies should be compared with the finite catalogue of predicted panels; applying prime valuations directly to an approximate measured frequency is not justified. Exact factorisation is an ideal identification result, with an explicit and potentially severe statistical cost.
