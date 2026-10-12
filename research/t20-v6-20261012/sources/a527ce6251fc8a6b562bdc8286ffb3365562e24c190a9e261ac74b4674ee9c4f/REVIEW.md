# Independent mathematical review: fixed semantic predicates along constrained Gaussian correction

11 October 2026 UTC. Ordinary mathematical review by a separately tasked reviewer. This is not external peer review, kernel verification, new general Gaussian theory, philosophical warrant, publication, integration, owner acceptance, or T20 closure.

## Verdict and binding

**QUALIFIED within the report's stated mathematical scope; no unresolved mathematical blocker found.** The principal counterexample is valid. The report is a useful application/interface qualification of inherited results, with no established field-level novelty claim. A minor precision defect in the represented-real proof was reported to the author and corrected before final qualification. The independent checks below were rerun against the corrected bytes.

`INPUT_DIGESTS.json` binds the exact reviewed RESULT, author checker, source-binding manifest, and four directly read ancestor reports. This review applies only to those bytes. The source reports were inspected as ordinary written mathematics; their upstream files, historical literature, kernel proofs, and external provenance were not freshly replayed. The independently derived controls do not import or execute the author's checker.

## 1. Independent derivation of the specialised full-law example

Substituting beta=0, tau=1, b=0 into the source's two polynomial equations gives b'=0 and s'=2-s-s². Polynomial ODE uniqueness preserves b=0. Separating the scalar equation gives

    d/dt log((s+2)/(1-s)) = 3,
    (s+2)/(1-s) = 2 exp(3t),
    s = 2(exp(3t)-1)/(2exp(3t)+1).

This derives the corrected denominator independently of the author checker. It gives s(0)=0, s'(0)=2 and 0<s(t)<1 for t>0. The formerly used denominator exp(3t)+2 does not solve the scalar equation and is explicitly rejected by the independent regression control. That was a corrected development error, not an outstanding finding.

The full-density claim is consistent with actual fields, not merely matching a covariance ODE. Put k=1/s-1, v=(0,kz), and alpha=k(z²-s)/2. For the product Gaussian density rho_s,

    -div(rho_s v)/rho_s + alpha
      = k(1/s+1/2)(z²-s)
      = (s'/(2s²))(z²-s)
      = partial_t log rho_s.

At each y, the conditional expectation of alpha is zero and v_y=0, so the whole y-marginal is preserved. Gaussian second/fourth moments give

    integral (|v|²+alpha²) dmu = k²s+k²s²/2
      = (s+2)(1-s)²/(2s) = D.

Differentiating E=(s-1-log s)/2 gives E'=-D. Full tangent minimality and general constrained-flow identification remain inherited from the exact source contract; this specialised calculation corroborates their use without purporting to prove a fresh full PDE uniqueness theorem.

## 2. Time, action and topology

The independent expansion is

    s(t)=2t-t²-t³+O(t⁴),
    D(t)=1/(2t)-5/4+(3/8)t+O(t²).

Thus original-time action diverges, while length is finite. On r in [0,1], the changed fields multiply by 2 epsilon r, and their action density is

    4 epsilon² r² D(epsilon r²)
      = 2 epsilon - 5 epsilon² r² + (3/2) epsilon³ r⁴
        + O(epsilon⁴ r⁶).

The remainder is uniform for 0<=r<=1 and small epsilon because tD(t) has a removable analytic extension at zero. Integration yields the stronger control

    A_epsilon = 2 epsilon - (5/3)epsilon² + (3/10)epsilon³
                + O(epsilon⁴).

The report's 2 epsilon+O(epsilon²) is therefore correct. Its wording properly concerns a feasible unit-interval endpoint competitor, not finite original-time action, shortest action, noncompact attainment, or an unchanged gradient equation. The author checker alone tests a boundary action-density limit rather than the full integrated remainder; the written inherited proof and the independent uniform expansion close that evidential distinction.

The W2 equality is exact: every coupling pays second-coordinate cost s, and coupling the same Y attains it. H={z=0} separates the endpoints completely, so TV=1 with the report's sup-event convention. There is no contradiction between small W2/action and maximal TV. Endpoint proximity is supported by the explicit competitor; no equality with another unconstrained metric is inferred.

## 3. Fixed repertoire and defect audit

The same carrier R², the same index set R minus {0}, and the same Borel sets A_a={z!=a} are used at all times. No outcome-dependent, time-dependent, or shrinking repertoire has been substituted. Their set-theoretic intersection is exactly the Borel line H. Initial and positive-time measures each give every A_a mass one, but H has masses one and zero. The measurable universal intersection is exhibited directly, so there is no illicit arbitrary-intersection closure assumption. Every countable subfamily remains conull by countable subadditivity.

The inherited CV-R theorem concerns the full measurable repertoire and its maximum failure probability. The continuous Y marginal makes every singleton of R² null even initially, so its defect is already saturated at one. The report correctly declines to identify that envelope with this restricted repertoire's failure. A saturated invariant envelope cannot certify preservation of the chosen H.

For the explicitly supplied disintegration, Z|Y=y is delta_0 initially and N(0,s) later. Its defects are zero and one. These regular conditional versions are available for all y here, although arbitrary versions are only almost-everywhere unique. Because every singleton Y fibre has zero marginal mass, the positive-coarse-atom increment formula in CV-R cannot be used as an accounting identity for this disintegration. The report makes this distinction explicitly. The flow is also not silently treated as a coherent observation-refinement tower.

## 4. Moment and computability audit

All mixed moments have the stated Gaussian product form and continuous endpoint limits. Ordinary Gaussian moment determinacy, including the endpoint supported on z=0, is compatible with the argument. More strongly, the variance coordinate already identifies this promised family. Consequently the obstruction is discontinuity of the specified event query, not nonuniqueness of the represented probability law.

The event-mass function is the zero-test on [0,1]. With ordinary real approximation names, run any alleged uniformly accurate evaluator on the all-zero name. It reads finitely many precision requests. A sufficiently small positive s has a valid name giving the same answers on those requests, forcing the same output, although the event masses differ by one. Error strictly below 1/3 is impossible. Uniform computability from complete moment names is also impossible because s uniformly computes the product sequence of Gaussian moments. This argument does not deny computability at an explicitly supplied symbolic endpoint or within a promised strictly-positive domain.

The initial draft's phrase about *any* compatible finite zero transcript was too broad when approximation conventions allow boundary answers. The revised proof uses the all-zero name and no longer makes that unnecessary assertion. This is resolved in the final bound bytes.

The capped tensor theorem assumes indexed countable laws on a known support in a compact simplex, effective cap tails, and the stronger l1 output contract. None applies to the diffuse Gaussian law as an indexed atomic law. Its cap-free moment continuation does not compute arbitrary measurable events, and the present example does not refute it. The report is careful about the supplied effectiveness requirements for bounded discrete queries. Its negative result is an interface distinction, not a claimed noncomputable Gaussian parameter inverse.

## 5. Repairs, inherited scope, and application ceiling

The equivalence between preserving every initial measurable conull set and nu<<mu follows immediately by complements, and the direction is correct. Finite normalised positive reweightings satisfy it; weak limits need not. TV controls each event query with constant one under the stated convention. The restricted-query pseudometric is accurately labelled a present-query device, without a fabricated future-operation closure theorem. Adding H preservation really excludes the nondegenerate members of this family rather than making them available through a finer numerical step.

CV-R supplies the full/restricted-repertoire distinction and topology caveats; the singular entrance supplies the specified correction geometry and endpoint qualifications; capped recovery supplies the representation contract; U08 supplies the pre-existing all-safe noncompactness warning and effective/existence distinction. I found no contradictory borrowing among these four source reports. U08 is background ownership evidence rather than a necessary premise of the concrete example.

No logical bridge from this mathematical model to human beliefs or theological warrant has been established. The report expressly says so, does not assign actual historical or philosophical premises these Gaussian semantics, and does not claim an uncountable human belief repertoire. Its philosophical use is a conditional warning about a proposed interface. A substantive application still needs its own carrier, predicate, probability, and admissible-update interpretation. The evidence ceiling is honest at that level.

## 6. Final scope amendments

The final author revision makes two additional limitations explicit; both are supported and leave the mathematical verdict unchanged.

1. The example starts at a singular, infinite-KL law. It therefore does not refute a theorem whose hypotheses require a positive-density, finite-initial-energy initial law. In this particular Gaussian family, any two strictly positive variances give equivalent measures with respect to Lebesgue measure, so the displayed conull-event loss cannot occur between two such states. Small positive times do not silently turn the singular endpoint counterexample into an example satisfying finite initial KL.
2. Finite strings over a countable alphabet form a countable set. Separate finite program or formula occurrences cannot enumerate all distinct A_a in this uncountable repertoire, and countably many conull events stay conull. A quantified formula can nevertheless quantify over an uncountable semantic domain. Its interpretation must be supplied separately; neither the example nor the CV-R source provides an automatic compiler-to-predicate transport. The revised report now states this explicitly.

The refreshed INPUT_DIGESTS.json binds these final amendments. All other six bound inputs were checked to be unchanged before the refresh.

## 7. Independent execution evidence

`independent_controls.py` ran successfully both normally and with Python -O: 37 checks in each mode, byte-identical JSON outputs. RuntimeError-based guards remain live under optimisation. Controls cover source specialisation, separated solution derivation, rejection of the old denominator, full density tangent, conditional mass conservation, field-norm action, dissipation, three boundary coefficients, integrated action coefficients, thirteen positive-degree Gaussian moment traces plus normalisation, and all seven input digests.

These are finite algebraic and digest controls. The arbitrary-intersection argument, Type-2 impossibility, domination equivalence, endpoint continuity justification, and philosophical scope are reviewed written arguments, not consequences of finite test enumeration. No new kernel run or external review is implied.
