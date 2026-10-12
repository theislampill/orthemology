# Independent review: effective stationary selection and exact cap diameter

Status: PASS for final frozen author packet and fresh finite-control replay. No remaining blocking mathematical defect found. This review is ordinary mathematics, not Lean verification. Earlier reviews and protected sources remain unchanged.

## 1. Representation and operator computation

The stated ℓ1 representation is essential: outputs are fast Cauchy names of actual probability vectors, not exact finite rational vectors. Coordinatewise computability of a summable vector alone does not compute its total or its ℓ1 name. The supplied cap-tail modulus does both. Conversely, uniformly computable stochastic matrix entries do compute uniformly ℓ1-computable rows: for each row, search certified lower bounds on initial partial sums until they exceed 1−ε; row normalization guarantees termination. This search needs no zero tests or row-independent runtime bound. Finite rational input approximation, finitely many row names, and ||xP||1≤||x||1 then compute the induced linear operator.

The general positive lane assumes T(Kc)⊂Kc. The sharper cap contraction lane assumes every row lies in Kc. These are different premises. The identity operator on cap(3/4,3/4) preserves Kc but has many fixed points despite envelope diameter 1/2; it is correctly excluded from the row-domination contraction theorem.

The input is a supplied computable selected operator. No effective choice from arbitrary nonempty closed row correspondences is smuggled in. Different selections under one contracting cap may have different unique stationary laws. The inherited finite rational-polytope solver is a separate positive case with a stronger representation.

## 2. Residual laws, effective compactness, and unique-zero computation

The seed c/C is computable, normalized and cap-admissible because C≥1. Its Cesàro laws stay in Kc by convexity/invariance. Telescoping gives s_N P−s_N=(p0 P^N−p0)/N, hence residual ≤2/N. This proves uniform computable residual-ε laws, not finite exact rational cap points and not distance-ε approximations to the fixed set. The two-state small-transition example correctly separates residual from solution error.

Effective compactness is genuinely supplied rather than assumed. In Bc=∏[0,c_j] viewed in ℓ1, a cap-tail bound controls all omitted coordinates. Finite coordinate grids, clipped by computable min with c_j and extended by zero, give uniformly computable finite nets. Ordinary closedness/completeness and total boundedness prove compactness. Strict containment-margin tests against progressively fine nets semidecide finite open-ball covers; positive Lebesgue margins ensure completeness of that semidecision. Enumerated opens are handled by dovetailing finite subcovers. The sum functional is computable and 1-Lipschitz, so Kc=Bc∩{sum=1} is upper-effectively compact through the complement {sum≠1}. No decision of grid intersection with Kc and no computable dense sequence in an arbitrary effectively closed set is needed.

The residual r(x)=||xP−x||1 is computable and 2-Lipschitz. Its zero set Z inside Kc is upper-effectively compact: Z⊂U iff Kc⊂U∪{r>0}. Under the nonempty singleton promise, enumerate rational centers and semidecide containment in balls of radius 2^-k. Some ball contains the singleton; every accepted center is within that radius. This is a uniform exact stationary-law computation on the unique-law promise class. It does not decide uniqueness.

The additional computed Cesàro convergence modulus is valid: nested compact nonempty sets Z_n={r≤2^-n} intersect at π. A search for Z_n contained in a small rational ball terminates by compactness; residual ≤2/N then puts all sufficiently late Cesàro laws and π in that ball. This need not be an efficient or closed-form rate. Raw powers can still oscillate.

## 3. Exact cap-only contraction and universal uniqueness

For a fixed subset S, cap-admissible probabilities have maximal mass min(1,c(S)) and minimal mass max(0,1−c(S^c)) on S. Both bounds are feasible by proportional allocation within each cap group (zero-cap groups get zero mass). Discrete TV duality and interchange of suprema yield

D(c)=max_{p,q∈Kc} TV(p,q)
    =max_S [min(1,c(S))+min(1,c(S^c))−1]
    =max_S min(1,C−1,c(S),C−c(S)).

Attainment is justified: the subset-sum map on binary Cantor space is continuous by summable tails, hence has compact image. It follows exactly that D(c)=1 iff some capacity partition has both sides at least one.

For probabilities p,q, normalize the positive/negative parts of p−q to get p−q=t(a−b), t=||p−q||1/2. Under row domination, aP,bP lie in Kc; therefore ||pP−qP||1≤D(c)||p−q||1. Putting two maximizing cap-admissible rows at two input states shows the coefficient is cap-only optimal. This does not assert a computable maximizing partition or effective attainment for every cap.

For finite-prefix subset maxima D_N, f(s)=min(1,C−1,s,C−s) is 1-Lipschitz. Every subset loses at most the cap tail τ_N on truncation, giving D_N≤D(c)≤D_N+τ_N. Finite computable maxima and the supplied tail modulus compute D. The finite subset enumeration may be exponential. A strict D<1 promise lets certified upper approximations find rational D<ρ<1, giving ||pP^n−π||1≤2ρ^n and ||p−π||1≤||pP−p||1/(1−ρ).

The coarser bound D≤min(1,C−1) is sharp across cap profiles: c=(1,C−1) and rows (1,0),(2−C,C−1) attain it. But C=2 is not an exact failure criterion for a fixed cap: c=(.9,.9,.2) has D=.9. Pairwise overlap also does not imply one shared minorizing measure; the three half/half rows on three states have D=.5 and common coordinatewise minimum zero.

The stronger ordinary equivalence is correct: D<1 iff EVERY row-dominated stochastic kernel has a unique stationary law. When D=1, normalize c on the attained two capacity groups to p,q and define rows p on the first group, q on the other. Then pP=p and qP=q, so uniqueness fails. This quantifies over all mathematical kernels. Without effective partition data, it is not a computable-counterkernel construction for every computable critical cap. No iff uniqueness test for one particular supplied operator follows.

## 4. Uniform selection obstruction, not merely slow iteration

For P(a,b)=[[1−a,a],[b,1−b]], positive a-axis laws are forced to δ1 and positive b-axis laws to δ0, while the origin is identity. Thus no continuous extensional single-valued selector exists. That statement alone should not be used as a general theorem about name-dependent multivalued realizers; the author's stronger computability conclusion is justified by the independent diagonal construction below.

Let A={e:φ_e(e)=0}, B={e:φ_e(e)=1}, which admit no total computable binary separator (diagonalizing the separator's own index). Use rate 2^(-t-2) when the corresponding outcome first appears at stage t, and zero otherwise. Fast Cauchy names are uniformly computable by finite simulation, every rate is rational-valued, and at most one is positive. A uniform algorithm returning any stationary law, even one depending on the input name, would approximate its second coordinate within 1/4 and threshold at 1/2 to separate A and B. The origin's freedom and exact threshold ties do not help. The same argument rules out a fixed coarse ℓ1 approximation within 1/4 of SOME stationary law on the full family.

Every individual matrix in that family has a computable stationary point; the obstruction is uniform selection across the class, including nonunique origin cases. It does not contradict uniform computation on the unique-law promise class or solving finite matrices supplied as exact rational fractions. The countable geometric product lift preserves the forced two-state marginal and supplies an explicit cap tail. Each stationary lifted law has infinite support, and bounded linear marginalization computes the obstructed two-state answer.

## 5. No-effective-tail boundary

The Specker birth-death construction is valid in the general invariant-cap lane. A computable increasing rational sequence with noncomputable limit α yields w0=1 and w_n=2^-n+α_n−α_(n−1), with noncomputable total W=2+α. Conductances h_n=min(w_n,w_(n+1))/4 produce uniformly rational stochastic tridiagonal rows, diagonals≥1/2, and detailed balance wP=w. Positivity proves T(Kw)⊂Kw.

Stationary currents satisfy J0=0 and J_n=J_(n−1), so every stationary law is proportional to w; normalization uniquely gives π=w/W. Since π0=1/W, the law is noncomputable. There is still a computable admissible seed δ0 and computable residual averages. No computable tail modulus of w can exist, since it would compute W. This demonstrates why classical compactness cannot replace the effective presentation in the general unique-zero theorem.

It is not a counterexample in the stronger summable row-domination regime: diagonals≥1/2 at arbitrarily high states rule out any common summable row cap. The report does not infer that every computable countable kernel with an effective cap has a computable stationary point without uniqueness/selection information.

## 6. Classical ancestry and scope

The effective singleton method matches Theorem2.9, Remark5 and Corollary3 of [Galatolo–Hoyrup–Rojas](https://members.loria.fr/MHoyrup/computinvmeas.pdf); their uniformity statement is directly relevant. The cap supplies an ℓ1 effective compact presentation, so the proof does not silently transfer a weaker measure topology. Classical row-distance/overlap ancestry is correctly identified in equations(1)–(2) of [Gaubert–Qu](https://arxiv.org/pdf/1307.4649); the report supplies its countable specialized proof. Only those relevant passages were inspected, not both entire papers. No world-novel theorem or priority claim is approved.

The retained U08 F2-04–07 already owns the classical cap/Cesàro existence and finite rational-flow results; T10 already distinguishes effective compact containment from classical compactness; T18 §11 already distinguishes rational-valued Cauchy inputs from exact fractions. These actual excerpts were checked without duplicating repository discovery searches or baseline rebuilds.

Two draft presentation issues were raised before freeze: separate the extensional topological observation from the stronger realizer/index impossibility proof, and qualify the disclaimer about uniqueness criteria to individual operators rather than denying the proved universal cap criterion. Final resolution and exact author binding will be recorded below.

## 7. Final freeze, addressed findings, and evidence

Both requested presentation corrections are present in the frozen report. Section6.1 now restricts the axis argument to continuous extensional single-valued selectors and explicitly relies on Section6.2 for arbitrary name-dependent/index computability impossibility. The final disclaimer now concerns an iff uniqueness test for an individual operator, preserving the proved universal cap criterion E4c.

Final author RESULT.md SHA256: ec03a2d42894f7e16c109631d884fec6023ab85e4c149bc6639d01e399f91f9c.
Final author MANIFEST.json SHA256: dbc337f0600e67326889be3341020b60100bb58cd21b4cded6326fec4c67b15a.

A separate fresh sibling snapshot effective-stationary-review-replay-20261010 was used to execute check_controls.py. All 5,081 exact rational checks pass, including independent finite vertex-versus-subset diameter checks, telescope identities, product-lift formulas, birth-death local balance, and negative scope controls. Every one of the 13 author file bindings matches both final original and replay snapshot. No baseline/kernel rebuild was performed.

Reviewer-written controls independently pass 3,375 three-state row-cap checks (2,007 with C<2), sharp-rate examples from C=1 through C=2, periodic Cesàro residual checks, axis/small-residual examples and finite detailed balance. A second independent script passes 709 cap profiles, 2,130 actual stationary capacity-split witnesses, and 32 exact dyadic-prefix tail-error checks. These are finite corroboration only; the ordinary proofs above carry the universal/effectivity/noncomputability claims.

REPLAY_RECEIPT.json binds final author hashes, fresh replay command and results. INDEPENDENT_CHECKS.json and DIAMETER_CHECKS.json record separate controls. Source-acquisition searches were not duplicated; only supplied primary-source URLs and retained relevant excerpts were inspected. The source DOI resolver could not be opened by the web tool, but the author-hosted GHR text and exact theorem passages were available and checked. No unverified DOI resolution is claimed.

The reviewed contribution is a project-relative effective boundary and sharp cap-envelope refinement, with classical ancestry retained. It is not an empirical/warrant conclusion, new general computability priority claim, universal row-correspondence selector, or full Weihrauch classification.

## 8. Final state-dependent scope guard

The final author delta adds the requirement that the selected matrix be fixed independently of the current law. Independently checked: with c=(3/4,3/4), D(c)=1/2 and Kc the Bernoulli interval [1/4,3/4], let every row of P(p) equal p. Each frozen matrix has unique stationary law p, while the adaptive update pP(p)=p fixes the whole interval. Thus pointwise row domination does not transfer the fixed-linear-operator contraction theorem to a state-dependent selection. The explicit nonsingleton example also clarifies the author's generic example. No defect in the fixed-operator theorem results.

Separate participating root STATE_DEPENDENT_SCOPE.md and SOURCE_NOTE.md are preserved under sources/. The former's algebra was independently checked; the latter records the root's limited introductory ancestry inspection. Our independent source checks are recorded separately in PRIMARY_SOURCE_CHECKS.json and do not claim to verify the root's acquisition event. Neither note supplies empirical identification, warrant, truth, or implementation evidence.
