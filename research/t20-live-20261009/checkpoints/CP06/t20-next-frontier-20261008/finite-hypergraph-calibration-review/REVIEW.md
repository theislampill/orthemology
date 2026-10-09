# Independent review: finite hypergraph calibration

8 October 2026 UTC. This review concerns the new finite-panel sampled-calibration result. It preserves all earlier artifacts. Verdict: PASS for the three author proof artifacts bound in REVIEW_RECEIPT.json. The separate source binding also preserves the four inherited prerequisite digests. No integration, physical certification, owner acceptance or T20 closure is authorized.

## 1. Proof verdict and scope

The reviewed finite-fibre theorem, ordinary-incidence rank criterion, rootwise row-space criterion, pair-graph specialization, and positive-unary half-integer recovery argument are mathematically sound under their stated model and observation contracts. The finite-dimensional fibre is a fibre of sampled calibration values. The space of full calibration functions remains infinite-dimensional even when all sampled values are fixed.

Two qualifications are essential:

1. The preserved Cartesian grid consists only of the chosen interior commands and optional zero masks. It cannot silently include additional unit commands. Endpoint preservation prevents extending a nontrivial multiplicative gauge to the unit value.
2. A half-integer unary sign routine does not itself terminate when the unary count is zero, but known positive interaction products provide a different nonzero-gap test that does decide participating unary absence. Section 7 records that independently identified extension. A broad assertion that this anchored unary absence is undecidable would be false. A theorem restricted to promised positive unary counts is valid.

The supplied model is a fixed finite unguarded independent-route one-effect inventory, with one coordinatewise strictly increasing endpoint-preserving homeomorphism shared across every occurrence of each root. The complete positive-support pattern and the positive counts are known for the main fibre theorem. The theorem does not identify unlisted supports, latent mixtures, physical gate architecture or real-world calibration from assumptions alone.

## 2. Exact raw-panel fibre

Let V be the union of the known positive supports. Write a_i,l=r_i(x_i,l), with increasing interior commands, base u_i=a_i,1, and rho_i,l=a_i,l/u_i. Every raw masked probability used is positive because each nonzero coordinate command is interior.

For every positive support S, the alternating multiplicative mask contrast gives

    E_S = product_(T subset S) Q(x_T)^((-1)^(|S|-|T|))
        = (1-product_(i in S) a_i)^n_S.

This is valid with arbitrary known lower-order supports present: their logarithmic contributions have zero alternating coefficient. The known positive n_S gives the uniquely defined product

    P_S = 1-E_S^(1/n_S) = product_(i in S) a_i.

Observe P_S at base for each support. For every i and each additional level, choose any incident support S(i), vary only i from its base command, and take the ratio to its base product. The result is rho_i,l. Positivity makes the division legitimate. Overlapping supports must supply the same ratio because the model has common root calibration.

Let A have a row 1_S for every positive support, plus a unit row for every independently supplied actual base anchor. A known positive unary support already supplies a unit row, so it need not be duplicated. With y_i=log u_i the base record is Ay=b. For a candidate sampled vector with the same record, put v_i=log(u'_i/u_i). Equality of the base products and actual anchors is exactly Av=0. Equality of the one-coordinate ratios forces

    a'_i,l = exp(v_i) a_i,l.

The only additional pointwise feasibility condition is

    exp(v_i) max_l a_i,l < 1  for every i.

There is no extra positivity or strict-order obstruction: exp(v_i)>0, and common multiplication preserves the strictly positive ordering. Connect (0,0), the finitely many nominal/actual knots, and (1,1) by linear segments. Every segment has strictly positive slope, giving a continuous strictly increasing bijection of [0,1] and hence a homeomorphism. This extension argument constructs maps from sampled knots; it does not multiply a whole original map by exp(v_i), which would violate the unit endpoint.

Conversely, any such v and any homeomorphic interpolants preserve every support product at every combination of the chosen levels:

    product_(i in S) a'_i,l_i
      = exp(sum_(i in S) v_i) product_(i in S) a_i,l_i
      = product_(i in S) a_i,l_i.

At zero masks the relevant product remains zero. Hence every factor, and therefore every full raw Q value on that finite interior/zero grid, is preserved. This proves equality of the compact raw masked panel has exactly the stated sampled-value fibre; raw background observations do not impose additional constraints beyond A because all known positive supports occur as rows.

Completeness of the known support pattern matters in that last step. If an additional unrecorded positive support is allowed, its product need not be gauge-invariant.

## 3. Dimension, partial identification and the probability-mass distinction

The feasible log-fibre is the affine space y+ker A intersected with finitely many strict upper coordinate inequalities. It contains y as a relatively open point because all sampled true values lie strictly below one. Thus every kernel direction permits a sufficiently small positive and negative displacement. Its local dimension is exactly

    |V| - rank A.

All sampled values are identified if and only if A has full column rank. For an individual root i, all its sampled values are identified if and only if v_i=0 for every v in ker A. Finite-dimensional orthogonality makes this equivalent to e_i belonging to row(A). If e_i is outside that row space, some kernel direction has nonzero i-coordinate; a small feasible displacement changes u_i and all its sampled values.

No sum-to-one or mass-zero restriction applies. These y_i are log rates, not probabilities over mutually exclusive catalogue states. The historical signed-law criterion includes a mass-zero restriction because probability-law differences have total mass zero. Its full-support or mass-retaining hypotheses are unnecessary and inappropriate here. The star with rows AB, AC, AD has kernel vector (1,-1,-1,-1), whose coordinate sum is -2; discarding that direction would give an incorrect calibration conclusion.

Unused roots outside V have no raw observations of their calibration. They must be kept outside this matrix theorem or treated separately. Independent actual measurements of unused roots are additional data, not consequences of the inventory law.

## 4. Exact graph and hypergraph controls

For pair supports, an edge ij imposes v_i+v_j=0. Propagation from one vertex alternates signs along paths. In a connected bipartite component, this yields one free scalar, with opposite signs on the two color classes. An odd cycle forces that scalar to equal its own negative, hence zero. A unary or actual anchor v_i=0 kills the scalar of the entire connected bipartite component. These conclusions concern ordinary unsigned incidence, not oriented incidence.

Exact examples:

- AB, AC, BC has rank three and no gauge. At base products 1/20, 1/15, 1/12, the roots are 1/5, 1/4, 1/3; the squared reconstruction identities are checked exactly.
- AB, BC, CD, DA has rank three and alternating gauge (1,-1,1,-1).
- AB, AC, AD has rank three and gauge (1,-1,-1,-1).
- AB and ABC have rank two. C alone is identified because log u_C=log P_ABC-log P_AB. A and B retain reciprocal scaling.
- Adding an actual anchor or known positive unary support at one vertex makes a connected bipartite pair component full rank.

The independent script also uses the even cycle together with the higher-order support ABCD and unequal counts. Scaling A,C by 6/5 and B,D by 5/6 preserves all 81 raw Q values on a three-level-per-coordinate grid (zero plus two positive levels). This includes masks with lower-order background. At an added unit command the same two homeomorphic worlds differ, confirming the grid qualification rather than assuming it.

## 5. Observation and computability contracts

The algebraic identification theorem treats exact population values as mathematical data. It must not be read as a finite Bernoulli-sample guarantee.

For certified population Cauchy access, all raw probabilities in the chosen interior mask panel are positive. Refining an interval eventually certifies each divisor has a positive rational lower bound. Finite multiplication, division and positive rational powers then compute P_S and rho_i,l to arbitrary requested precision. An independent actual anchor must itself be supplied with the stated precision access if used computationally.

When A has full column rank, choose |V| independent rows, giving an invertible integer square matrix B. Its inverse is rational. If the corresponding positive product/anchor data are p_j, then

    u_i = product_j p_j^((B^(-1))_ij),
    a_i,l = rho_i,l u_i.

Negative rational exponents are permissible because p_j>0. Rational root bisection and positive-denominator division yield effective arbitrary-precision access. Logs are useful in the proof but are unnecessary as oracle operations. Arbitrary input real numbers are not thereby returned as finite exact strings. If exact rational raw data are expressly supplied instead, equality and support-presence questions can have stronger algorithms; rational nominal commands alone do not supply that contract.

Full rank does not impose a uniform conditioning, precision, runtime or sample bound. Near-zero products and narrowly separated levels can make computations expensive. Nor does it determine any entire homeomorphism between the finite knots.

## 6. Positive unary multiplicity recovery

Assume a participating root has two true levels 0<a_1<a_2<1, and known-count interaction products supply rho=a_2/a_1. The isolated solo data are Z_l=(1-a_l)^n for a positive integer n. For candidate real m>0, with c=n/m,

    D(m) = 1-Z_2^(1/m) - rho (1-Z_1^(1/m))
         = a_2 [H_c(a_2)/a_2-H_c(a_1)/a_1].

Here H_c(z)=1-(1-z)^c. If c>1, H_c is strictly concave with H_c(0)=0, so H_c(z)/z strictly decreases. If 0<c<1 it is strictly convex, so the quotient strictly increases. Consequently sign D(m)=sign(m-n), with equality exactly at m=n. The explicit derivative H''_c(z)=-c(c-1)(1-z)^(c-2) verifies the curvature; no unknown calibration is differentiated.

At m=k+1/2, exponent 1/m=2/(2k+1) is rational and m cannot equal the integer n. Compute a certified interval for D, refining all raw-data, ratio and root uncertainties until it excludes zero. This terminates for each cut. Positive sign means n<=k; negative sign means n>=k+1. Doubling k=1,2,4,... gives an upper bound and integer binary search returns n. No equality test is used. The finite raw command set is fixed, but precision requests may increase without a world-independent bound.

The independent recovery script receives certified intervals for raw probabilities, including unknown unary A, unary B background and a known-count AB support. It obtains the ratio by mask contrast and interval root operations; it is not handed the exact ratio. Both oracle interval styles recover n=1,...,12, for 24 recoveries and 204 terminating sign decisions. Twelve zero-count controls correctly keep zero in D's enclosure. Exact rational controls confirm the sign orientation and the pure-unary count/calibration ambiguity in the absence of an independent ratio.

## 7. Independent extension: anchored absence has a nonzero gap

The following observation is independent of whether it is incorporated into the author artifact.

A known-count positive support S containing i gives a base product p=P_S>0. Each other true rate lies at most one, so a_i>=p. If the unknown unary count is zero, Z_i=1. If it is any positive integer, then

    1-Z_i = 1-(1-a_i)^n_i >= a_i >= p.

Therefore

    (1-Z_i)-p/2

is strictly negative in the absent case and strictly positive in the present case. This is a terminating certified-Cauchy sign test for unary presence under the known-interaction-product premise, requiring no zero test. It can precede the positive-unary half-integer search to recover an arbitrary nonnegative participating unary count. Twenty-six raw-oracle cases, including zero and positive counts under both interval styles, verify this supplementary control.

More generally, suppose every i in a target support T has a known positive base-rate lower bound b_i, obtained for example as the product of a known-count positive incident support. Put beta=product_(i in T)b_i>0. The isolated target contrast satisfies

    1-E_T = 0                       if n_T=0,
    1-E_T >= product_(i in T)a_i >= beta  if n_T>=1.

The sign of (1-E_T)-beta/2 decides target presence. This applies only to covered roots with supplied positive lower bounds; it does not decide arbitrary support absence involving uncovered coordinates. It therefore does not contradict the unrestricted absence obstruction or turn raw Cauchy equality into a decidable operation. Independent raw-Cauchy controls check all seven nonempty supports on three roots under two interval-name styles, using one known positive ABC count as the covering seed; the 14 decisions include both genuinely absent and positive lower-order supports.

## 8. Additional audit: finite boundary-point reconstruction

The author also supplies BOUNDARY_POINT_RECONSTRUCTION.md. Its stronger observation instrument is valid and is separate from the interior gauge theorem. At the i-only unit command, the raw Q is exactly zero for a positive unary count and exactly one for an absent unary support. The midpoint decision has a promised gap and is therefore available to a certified Cauchy oracle. This particular corner probe is not available to an interior-only panel, although Section 7 gives a different interior presence test when an interaction product is known.

If the unary support is present, the recovered interaction ratio and solo observations give its count by Section 6 and then the desired calibration values. If it is absent, fix r_i(1)=1. Every remaining raw masked probability is strictly positive because a surely successful route would have to have been the absent unary i route. Removing i from supports therefore gives another valid fixed independent-route law, with

    tilde_n_T = n_T + n_(T union {i})

for each nonempty reduced support T, and no empty/spontaneous route. For T=S without i, positivity follows from the promised original S. A reduced interaction count is recovered by the inherited four-value procedure. If T is a singleton j, S is exactly ij; the reduced count is n_j+n_S, and n_j is first decided and recovered from the original interaction ratio. There are no omitted extra supports that coalesce to that singleton.

After inverting the reduced contrast, its true product P_T is positive. Dividing the original P_S by P_T returns r_i at the desired sampled command. No raw log infinity or boundary-limit subtraction is introduced. Additional roots outside the chosen support are masked to zero, so an unknown inventory background does not spoil support isolation. This supplies arbitrary precision at finitely many requested points with finitely many distinct command vectors and potentially unbounded precision refinement, not a whole-function finite representation or finite-sample guarantee.

Independent exact controls verify 27 complete reduced-field grid values with multiple lower-order and higher-order routes, additive support coalescence, both deterministic unary corner outcomes, and the original/reduced product quotient. They explicitly use original ABC count 3 and reduced BC count 7, preventing the erroneous substitution of the original count for the reduced aggregate.

## 9. Verification summary

The independent standard-library script is separately authored and imports no author implementation. It uses exact rational fixtures for controls and to construct genuine certified interval names; its recovery routines receive only those names. The replay reports 305 assertions, 81 interior raw-grid equalities, 27 reduced-boundary grid equalities, 24 unary recoveries, 204 certified sign decisions, 12 zero-D interval controls 26 anchored unary presence decisions and 14 general covered-support presence decisions, all passing. Its diagnostic maximum of 32 precision bits is an observed fixture cost, not a theorem bound.

These finite tests support the preceding mathematical proof audit. They do not substitute for the general proofs or expand any permission boundary.
