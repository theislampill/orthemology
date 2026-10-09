# Independent adversarial review: interaction-calibration anchor

Review date: 8 October 2026 UTC.

## Verdict

The reviewed mathematical statement is correct in the expressly declared fixed,
finite, unguarded, one-effect, coordinatewise-common-calibration product model.
No mathematical blocking defect was found. The final file binding and author-
control replay are recorded below. This review does not authorize integration,
protected edits, physical interpretation or T20 closure.

The reviewer wrote and executed the independent control program before reading
the author's RESULT.md. It imports no author code and uses only exact integer and
Fraction arithmetic. The full theorem is accepted on the proof audit below, not
on the finite test enumeration.

## 1. Independent proof audit

### Support separation and the zero cases

For a mask T contained in S, rates outside T are exactly zero. A support U
contributes to log Q(x_T) precisely when U is contained in T. All active
coordinates remain strictly interior during inversion, so every individual Q is
positive and every log is finite. The coefficient of support U in the S contrast
is the finite Boolean-lattice sum

    sum_{U subset T subset S} (-1)^(|S|-|T|),

which equals one for U=S and zero for every proper U. Supports not contained in S
never contribute. The resulting isolated contrast is exactly

    L_S = n_S log(1 - product_{i in S} r_i(x_i)).

For every interior vector the log factor is strictly negative. Hence the exact
zero/nonzero contrast distinguishes absent from positive supports, including
non-minimal supports absorbed at the deterministic all-one endpoint. No lower
count bound or known finite upper bound is silently needed. Empty inventory,
unused roots and a root set with no positive interactions are all covered.
Exact zero testing is part of the supplied population-function contract.

### Interaction rigidity

For a positive S in two equal-response worlds, positivity gives n_S,n'_S>0.
Every calibration is an endpoint-fixing homeomorphism. Thus the independent
actual coordinate values range through the whole open cube, and

    product alpha_i(a_i) = H_c(product a_i),
    alpha_i = r'_i composed with r_i inverse,
    c = n_S/n'_S > 0,
    H_c(z) = 1-(1-z)^c.

Taking other coordinates to one is justified by continuity and fixed endpoints;
it forces each alpha_i=H_c. If |S|>=2, the remaining two-variable identity is
H_c(ab)=H_c(a)H_c(b). Only the explicit function H_c is differentiated in the
proof: H_c(a)/a tends to c>0. Dividing by a and letting a tend to zero gives
cb=c H_c(b), so H_c(b)=b. Its same right slope implies c=1. This argument makes no
differentiability assumption on any r_i, including at zero, and works for
interactions of every finite order. Each positive interaction independently
anchors all its coordinates; no connectedness assumption is missing.

### Necessity and sufficiency of the remaining fibres

Once an interacting coordinate is anchored, its unary log denominator is finite
and nonzero at every interior command, so the unary multiplicity is fixed too.
If a root is outside every positive interaction, its only possible contribution
is unary. For positive unary counts n and m, equality is equivalent to

    r'(x)=1-(1-r(x))^(n/m).

For every positive integer m this remains an allowed calibration homeomorphism.
A positive unary count cannot become zero, because the latter curve is constantly
one. For an unused root all allowed calibration maps are observationally equal.
Substituting these possibilities factor by factor proves sufficiency. Therefore
the list is an exact classification, rather than only a list of invariants.

## 2. Independent verification of the constructive inverse

The raw log-mask expression must not be used directly at unit-rate faces.
An unrelated lower-order route can force both numerator and denominator of a
multiplicative mask contrast to zero. The author's instruction to isolate first
and continuously extend the isolated function is essential and correct.

For a positive interaction containing i and j, the isolated extension is finite
for 0<u<1 and 0<=v<=1 after all its other coordinates are set to one:

    D_ij(u,v)=n_S log(1-r_i(u)r_j(v)).

The denominator D_ij(u,1) is strictly negative. Put p=r_i(u) and b=r_j(v). A
separate analytic verification of the recovery limit avoids unknown derivatives:
let f(z)=-log(1-z). Convexity and f(0)=0 give f(pb)<=b f(p), while integral
bounds give f(pb)>=pb and f(p)<=p/(1-p). Consequently

    b(1-p) <= f(pb)/f(p) <= b,      0<p<1, 0<=b<=1.

The interval width is bp and tends to zero solely by continuity of r_i at zero.
The ratio therefore converges to b even for calibrations with a kink or an
infinite one-sided slope. Its count multiplier cancels. At v=0 and v=1 the ratio
is exactly zero and one, respectively. Every coordinate of an interaction can be
paired with another, and once maps are recovered the stated log quotient gives
the interaction count and any anchored unary count.

This is an inverse using exact functions and limits. The review does not convert
it into a halting computation from approximations, a finite command panel, a
modulus uniform over calibrations, a statistical guarantee, or a physical
calibration procedure. The bound above is an analytic proof device only.

## 3. Adversarial boundary and failed-transport checks

1. **Singular raw logs.** An A unary route and two AB routes give Q(1,b)=0 for
   b<1; the A-only masked Q is also zero. Nevertheless the correctly isolated AB
   factor has the finite nonzero limit (1-b)^2. The exact control uses b=2/5,
   giving isolated limit 9/25. It never divides the two raw boundary zeros.
2. **Unary gauge.** Integer-power calibration pairs preserve the unary curve
   exactly. Thirty unequal count pairs that agree on all-but-one-coordinate
   boundary restrictions fail at a genuinely two-dimensional interior command.
   Boundary-only matching is insufficient to retain an interaction.
3. **Anchored unary counts.** Preserving a unary response by changing its count
   and recalibrating A changes a common-calibration AB response. If the unary
   routes are allowed a support-specific A map, the count ambiguity returns.
   Thus map sharing is specifically needed to transfer the interaction anchor
   to the unary factor.
4. **Shared root gates.** With one shared random gate per root, one A route and
   the inventory A,A,AB have the same no-effect law 1-a. The independent-route
   product law instead gives (1-a)^2(1-ab). Both duplicate and absorbed route
   invisibility are genuine countercontrols to changing gate semantics.
5. **Coordinate cross-talk.** Count two on AB with identity maps equals count
   one using A'=a(2-ab)/(2-b), B'=b(2-b). Their product is ab(2-ab), so the equality
   holds as a polynomial/rational identity on the full square. The denominator
   is at least one; both maps have their own endpoints and are continuous.
   For every fixed b, dA'/da=2(1-ab)/(2-b)>0 on 0<a<1; dB'/db=2(1-b)>0 on
   0<b<1. Thus own-coordinate strict monotonicity does not rescue the theorem
   when cross-talk is allowed. The more general H_c formula in the author's
   result also satisfies joint continuity at b=0 because H_c(z)/z tends to c
   uniformly over 0<=z<=b. No broader cross-talk classification is asserted.
6. **Insufficient map regularity.** Endpoint-preserving binary monotone step
   maps make all positive powers of an active factor identical. They can even
   hide an absorbed AB support behind A. This is outside the homeomorphism
   class; the theorem does not claim its regularity assumptions are minimal.
7. **Latent inventories.** A fresh half-mixture of one A route and one B route
   has no AB route in either component, but at a=b=1/2 its isolated multiplicative
   AB contrast is 8/9, not one. Thus taking the log of a mixture cannot be used
   as the claimed fixed-inventory support decomposition. No fixed/held/fresh
   mixture equivalence theorem is implied.
8. **Guards.** At a fixed full issued profile an absence-of-B guard disables its
   A route even when the attenuation on B is zero. Such a route is invisible in
   the current full-profile cube. Issued-profile variation and attenuation
   masking cannot be conflated.
9. **Observation process.** The response curve alone describes one-trial binary
   laws. Its extension to adaptive or stopped transcripts needs the specified
   fresh conditional Bernoulli kernel. Arbitrary temporal dependence or an extra
   observation channel need not be determined by Q. The author states this
   qualification explicitly.
10. **Semantic reach.** The result identifies anonymous support-indexed route
    multiplicities in a stipulated law, not route names, physical architecture,
    source ownership, admissible interventions or complete productive adequacy.

## 4. Independent exact controls

Command, run inside this review directory:

    python independent_controls.py --output INDEPENDENT_CONTROLS.json

Observed result: PASS.

- 2,281 fixed inventories; 16,865 exact support-isolation and support-presence
  checks. This exhausts counts 0,1,2 on every support for one, two and three
  roots, then checks deterministic higher-root inventories through five roots.
- 180 exact unary equivalence evaluations over counts 1 through 6.
- 30 unequal interaction-count comparisons after matching all-but-one boundary
  restrictions.
- An anchored-unary recalibration separation: 5/24 versus 3/16.
- Unused-coordinate invariance and empty inventory including boundary commands.
- A raw-boundary-log failure control with isolated factor limit 9/25.
- Twenty shrinking exact analytic envelopes along r(u)=sqrt(u), u=4^(-k),
  whose derivative at zero is not finite.
- Shared-gate and latent-mixture countercontrols, support-specific calibration,
  81 rational cross-talk evaluations, and 25 step-map evaluations.

All program comparisons are exact Fraction equalities or inequalities. The
analytic inequalities and general classification are justified above rather
than being extrapolated from these finite controls. No numerical log evaluation
or floating-point near-equality is used.

## 5. Author replay, source audit and packet binding

The author's exact_controls.py was copied into author_replay and executed there.
It passes 36,604 assertions; its result JSON and printed log are byte-identical
to the author outputs. This replay is distinct from the independent controls.
The separately added FINITE_PANEL_APPENDIX.md is reviewed and receipted in
FINITE_PANEL_REVIEW.md and APPENDIX_REVIEW_RECEIPT.json; it does not alter this
main theorem's population-equivalence classification.

The following predecessor texts were read without changing them:
productive-identifiability/THEOREMS.md,
productive-identifiability/general-roots/RESULT.md,
global-calibration-ambiguity/RESULT.md, and
grouped-calibration-invariants/RESULT.md. The original H fibre-criterion excerpt,
the parent's finite-panel candidate, and the author's SOURCE_AUDIT.md were also
inspected. The source audit distinguishes actual subset-inversion transport from
semantic analogy and identifies the scope failures rather than claiming that
inheritance authenticates a physical model or an external novelty claim.

All 50 predecessor payload hashes in the three frozen manifests, the manifest
identities themselves, and all 12 individually listed source identities were
independently rechecked. Byte verification does not imply that all those payload
texts were reread or that the entire original source manuscript was refetched.
The cited excerpt supports the bounded fibre-preservation statement attributed
to it. No hidden external theorem is needed for the elementary proof reviewed.

AUTHOR_BINDING.json lists the exact reviewed author files and their SHA-256
identities, with matching immutable review-local copies in author_snapshot.
MAIN_REVIEW_RECEIPT.json binds this report, its independent controls and output,
and the core author theorem/control/source-audit identities. REVIEW_MANIFEST.json
binds the review package; verify_review.py rechecks these identities, frozen
source payloads and deterministic control replays without editing predecessors
or author files. Administrative files added later by the author are outside the
listed binding unless explicitly reviewed and receipted again.
