# Independent review: coordinate-only dependent-gate transport

8 October 2026 UTC. Verdict: **PASS within the explicitly stated probability-model classes.** No substantive mathematical or attribution defect was found. This review does not authorize integration, T20 closure, or any physical, psychological or metaphysical interpretation.

The author packet is bound by MANIFEST.json SHA-256 `3ef066a690d014d22bfafb4cadb40e3506ead0c2f576b98345ab42da46af0661`. The later semantic guard is separately bound by ADDENDUM_MANIFEST.json SHA-256 `66a631d04cfe92964aaf8829f3668e362b589004d1c1c66dba287c4155513716`. All 10 original payloads and the one addendum payload were verified. Neither author files nor predecessors were modified. Exact file bindings and receipts accompany this review.

## Scoped verdicts

1. **PASS: direct joint-CDF theorem.** For every real 0<c<=1, F_c(a,b)=1-(1-ab)^c is a joint CDF on [0,1]^2 with margins H_c(z)=1-(1-z)^c. It is not itself a uniform-margin copula except at c=1.
2. **PASS: fixed-threshold realization.** A single command-independent pair (X,Y) with this CDF gives coordinate-only, nondecreasing gate sample paths 1{X<=a},1{Y<=b}. Taking mutually independent copies retains independence of route outcomes. Pairwise independence alone would not justify a product over more than two routes; the author constructs fully independent copies.
3. **PASS: full endpoint equivalence.** For every integer 1<=n<=m, c=n/m gives (1-F_c(a,b))^m=(1-ab)^n on the entire closed command square. Composition with baseline coordinate homeomorphisms preserves the declared calibration class.
4. **PASS: Joe identification.** Uniformization gives the established Joe copula with theta=1/c=m/n>=1. Primary software documentation, the constructor expression, and generator agree. This identifies a known formula; it is not a new copula discovery or an attribution of route semantics to those sources.
5. **PASS: homogeneous converse.** A common per-route joint-success law and endpoint-preserving coordinate marginals force J=H_(n/m)(ab) and both margins H_(n/m). For m<n a valid Bernoulli table is impossible near (1,1).
6. **PASS, separately: heterogeneous-joint/shared-marginal converse.** Joint laws may differ by route, but each root must retain one common marginal map across every route and all route outcomes must remain mutually independent. Under these restrictions the compatible counts are exactly m>=n. No occurrence-specific-marginal or route-dependent extension is certified.
7. **PASS: failure rectangles and semantic countercontrols.** The exact negative c=2 rectangles, distinction from inherited shared gates and cross-talk, and factorization-conditional interpretation of the four-value panel are correct.
8. **PASS: semantic addendum and attribution bounds.** Gate-outcome independence and original-source/whole-existence independence are explicitly distinct. The construction is a measurement-inference countermodel, not a model of harmonious plural Necessary Beings satisfying perfection premises. Targeted source inspection is distinguished from whole-paper reading.

## Independent mathematical derivation

### A. Joint CDF and fixed sample paths

Direct differentiation gives

    dF/da = c b (1-ab)^(c-1),
    d²F/(da db) = c (1-ab)^(c-2)(1-cab).

For 0<c<=1 the latter is strictly positive on the open square. Integrating on any compact interior rectangle gives a nonnegative rectangular increment. Approximate a boundary-touching rectangle by interior rectangles; continuity passes the inequality to its limit. The potential unbounded density at (1,1) causes no gap. Grounding, total mass one, continuity and 2-increasingness establish a probability law. Its continuous margins are H_c, so there is no ambiguity from atoms at thresholds.

As a genuinely different cross-check, expand H_c in powers of z. For 0<c<1, let w_1=c and

    w_(k+1)=w_k (k-c)/(k+1), k>=1.

The binomial series gives H_c(z)=sum_(k>=1) w_k z^k for 0<=z<1. Every weight is positive. Monotone convergence as z tends up to one shows sum w_k=1. At c=1 take w_1=1 and all subsequent weights zero. Draw an integer K with weights w_k and independent uniforms U,V, and set X=U^(1/K), Y=V^(1/K). Then

    P(X<=a,Y<=b | K=k)=a^k b^k,
    P(X<=a,Y<=b)=H_c(ab).

This supplies another full-square construction. K is a mixing index of a threshold law inside one route, not an inventory count. Choose independent (K,U,V) triples for distinct routes; the inventory stays fixed at m. Once each threshold pair is drawn, its A path refers only to a and its B path only to b.

The mixture also gives rectangle mass

    sum_k w_k (a1^k-a0^k)(b1^k-b0^k),

and the four table cells as the sums of w_k times

    a^k b^k, a^k(1-b^k), (1-a^k)b^k, (1-a^k)(1-b^k).

All terms are nonnegative. The k=1 term makes every nondegenerate rectangle and every interior table cell strictly positive. This justifies the independently coded truncated-mixture lower-bound controls without mistaking a finite grid for a global proof.

### B. Endpoint equality and copula

With c=n/m, each route fails with probability (1-ab)^c. Mutual route independence gives the mth power, namely (1-ab)^n, including the boundary. The fixed maps H_c composed with the baseline maps are continuous strictly increasing endpoint-preserving maps, common to all occurrences.

Writing x=(1-u)^(1/c) and y=(1-v)^(1/c), the inverse margins give H_c^(-1)(u)=1-x and H_c^(-1)(v)=1-y. Therefore

    C(u,v)=1-[1-(1-x)(1-y)]^c
          =1-[x+y-xy]^c.

This is the Joe formula with theta=1/c. The generator is phi(u)=-log(1-(1-u)^theta)=-log H_c^(-1)(u), with inverse H_c(exp(-t)); their additive-generator composition recovers the same C. At theta=1 it is uv. For c<1 the mixture K is nondegenerate; the covariance of a^K and b^K is positive for interior a,b because both are strictly decreasing in K. Thus the two gates genuinely need not factorize.

### C. Homogeneous and heterogeneous converses

Homogeneous case: equality (1-J)^m=(1-ab)^n uniquely determines J because 1-J is nonnegative. On b=1 the B gate is almost surely one, so J(a,1)=alpha(a), forcing alpha=H_c; the other face forces beta=H_c. At a=b=1-epsilon, the 00 cell is epsilon^c[2-(2-epsilon)^c]. If c>1, any 0<epsilon<2-2^(1/c) makes it negative. No common threshold space is needed for this contradiction.

Heterogeneous case: even when J_k varies, b=1 gives product_k(1-J_k(a,1))=(1-alpha(a))^m=(1-a)^n because every occurrence shares alpha. Hence alpha=H_c; beta follows similarly. At a=b=1-epsilon the union bound gives each route failure at most 2 epsilon^c. Independence then yields

    Q' <= (2 epsilon^c)^m = 2^m epsilon^n,

whereas the required target is epsilon^n(2-epsilon)^n. For m<n the author's epsilon range 0<epsilon<2-2^(m/n) makes the target larger, a contradiction.

There is also one explicit rational choice valid simultaneously for every m<n at a given integer n>=2: epsilon=1/(2n). Bernoulli's inequality gives

    (1-1/(4n))^n >= 3/4 > 1/2,

and hence (2-epsilon)^n>2^(n-1)>=2^m. This is the independently implemented converse certificate. Existence for every m>=n is already provided by the homogeneous construction; together these give precisely {n,n+1,...} in the heterogeneous shared-marginal class.

The bound cannot be transported silently. With occurrence-specific maps the endpoint faces identify products of failures, not each marginal. With dependent route outcomes the probability of all failures is not their product. The independent controls include simple scalar examples of both broken inference steps; they do not purport to construct a complete all-command model outside the theorem's class.

### D. Exact failed CDF map

For c=2, F_2(a,b)=2ab-a²b². An independently factored rectangle identity is

    Delta F_2 = (a1-a0)(b1-b0)[2-(a0+a1)(b0+b1)].

It yields -17/256 on (3/4,1]², -41/4096 on (3/4,7/8]², and 7/16 on (0,1/2]². At a=b=3/4 the four cells are (207,33,33,-17)/256. Thus coordinatewise monotonicity, probability-valuedness and endpoint conditions do not make a joint CDF. For every real c>1 the mixed derivative is negative on the nonempty open region ab>1/c, furnishing an interior negative rectangle. Coordinatewise increasing changes of variables preserve rectangle increments and cannot repair this sign.

At c=1/2, a=b=1/2, the author's radical table is correct. Rational bounds 7/5<sqrt(2)<10/7 and 12/7<sqrt(3)<7/4 certify positivity and the strict covariance sqrt(2)-sqrt(3)/2-1/2>0 without floating-point evaluation. Two independent copies have absence probability 3/4.

## Inherited controls and observation semantics

The predecessor interaction anchor explicitly requires product-form within-route success and route-to-route independence. Its functional equation H_c(ab)=H_c(a)H_c(b) forces c=1. The new construction changes exactly the within-route product premise, so it does not refute that theorem.

Shared-bearer gates make duplicate supports redundant and can absorb AB into A. Here distinct route pairs remain independent; a repeated route changes the endpoint law before compensating calibration/dependence changes. The inherited cross-talk model retains product-form gates but makes the A marginal depend on b. Here both the marginal and the realized A sample path depend only on a, while the pair is statistically dependent. These are distinct relaxations.

The inherited noise-aware result already says that accurate marginals do not establish a product joint law. The present result adds an explicit full-command cross-count equivalence and a bounded compatible-count classification, rather than claiming that general warning as new. The prior separability panel correctly returns n when its factorization premise is imposed. It does not certify that premise against these alternatives. Fresh conditionally independent trials allow ordinary adaptive endpoint transcript coupling; arbitrary temporal dependence and gate-level/multi-command joint observations are outside that statement.

The semantic guard matches the inherited source-admissibility cautions. A joint probability law does not establish admissible interventions, psychological manipulability, physical realization, productive-source independence, complete decisive willing, unchanged productive conditions, or metaphysical possibility. No closure or original-source theorem follows.

## Source audit and actual reading scope

The new RESULT.md, SOURCE_AUDIT.md, EXACT_CONTROLS.md, READ_FIRST.md, SOURCE_BINDINGS.json, source-read record, author script, and semantic guard were read. Predecessor inspection was targeted: the interaction anchor's declared product model, equivalence proof and controls; its panel's strict-sign proof; productive-identifiability's shared-gate, alias, implementation and admissibility discussion; and noise-aware-calibration's correlation/independence discussion. Exact local bindings appear in SOURCE_BINDINGS.json. Hash verification is provenance, not proof of reading every file in an inherited manifest.

External primary checks were targeted:

- [vinecopulas documentation, Table 1 Joe row](https://vinecopulas.readthedocs.io/en/stable/vinecopulas.html#fitting-a-vine-copula): complete CDF including outer 1/theta power and theta>=1, retrieved line 103.
- [CRAN copula R/joeCopula.R](https://raw.githubusercontent.com/cran/copula/master/R/joeCopula.R): constructor CDF builder at retrieved lines 27–31, parameter bounds 41–43, and independence branch 19–24. The two-dimensional product form expands to the reviewed formula. The mutable master URL was inspected, not executed or pinned to a package release.
- [CRAN acopula generator documentation](https://search.r-project.org/CRAN/refmans/acopula/html/generator.html): Joe generator and range, retrieved line 36, package 0.9.4. Direct algebra provides the parameter orientation.
- [CRAN copBasic help](https://search.r-project.org/CRAN/refmans/copBasic/html/JOcopB5.html): independently reproduced the retrieved main-formula omission of the outer exponent and its presence in the example. The location/cause of that defect is not established; it is not relied upon for the identification.
- [Publisher bibliographic result](https://www.sciencedirect.com/science/article/pii/S0047259X83710614) and [Joe's UBC publication list](https://www.stat.ubc.ca/~harry/pubs.html): metadata/abstract search retrieval corroborates title, 1993, volume 46, pages 262–282, DOI 10.1006/jmva.1993.1061. Direct DOI opening failed in this review; official search retrieval sufficed for bibliography. The full original paper, family numbering, historical priority and proofs were not read or certified.

The additional vinecopulib enum citation was not independently reread because the first three primary sources already directly establish formula, generator and range. That is a review coverage limit, not an assertion that the author's reported check did not occur. The author appropriately separates bibliographic attribution, targeted formula inspection, direct proof and bounded local synthesis. No whole-paper reading, exhaustive literature search, field-wide novelty, or source-level perfection is claimed by this review.

## Reproducible evidence

The independently written `independent_controls.py` passes 6,543 exact assertions across 35 named families. It uses rational positive-mixture lower bounds, a factored polynomial rectangle identity, independently selected endpoint witnesses, squared rational radical brackets, explicit rational converse witnesses, and distinct assumption-failure controls. These checks use no floating-point evidence, simulation or author imports.

The author script was copied byte-for-byte into this review's replay directory and executed there, so its relative output path could not modify the frozen packet. It passes 3,618 assertions across 30 families. Its output JSON and stdout exactly match the frozen author results. This replay is supplementary evidence, not the independent proof or independent controls.

No package was installed or run to certify the Joe implementation. Mathematical global claims rest on the derivations above, not on finite checks or software-documentation authority. Receipt hashes identify the reviewed inputs and evidence only; they do not broaden the theorem's scope.
