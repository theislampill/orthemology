# A known route ceiling makes support detection constructive

8 October 2026 UTC. New sibling; all earlier stages remain unchanged. In the same fixed-inventory endpoint model, an independently supplied finite route ceiling changes the Cauchy-oracle absence problem. The result is conditional mathematics, not a way to infer or justify the ceiling, certify a physical calibration model, or close T20.

## 1. Contract and result

There is a known finite set R of labeled root indices. For every nonempty S contained in R, n_S is a nonnegative integer route multiplicity, fixed throughout the experiment. Distinct route occurrences succeed independently, each with success probability product_(i in S) r_i(x_i). There is one effect, no guards or latent mixtures, and one static coordinatewise calibration r_i shared across all supports and occurrences containing i. Every r_i is continuous, strictly increasing and endpoint preserving on [0,1].

The probability of no effect is

    Q(x)=product_(nonempty S subset R) (1-product_(i in S)r_i(x_i))^n_S,

with zero-count factors omitted. An independently warranted integer M>=0 is supplied, and every admissible world satisfies the TOTAL ceiling

    sum_(nonempty S subset R) n_S <= M.                         (1)

The input oracle accepts a rational command vector x in the closed cube and a positive rational tolerance epsilon, returning a rational center within epsilon of the exact population Q(x). Every correctness and termination assertion holds for every valid fixed oracle name. Exact endpoint commands are permitted. No calibration modulus, calibration-error band, exact-value flag or exact-real equality test is supplied.

There is a terminating finite-query procedure that:

1. determines exactly which supports S have n_S>0;
2. recovers every positive multi-root multiplicity;
3. recovers every unary multiplicity on a root participating in a positive multi-root support;
4. returns the exact remaining finite multiplicity ambiguity allowed by (1).

Let C be the union of positive supports of size at least two, let I be the set of positive-unary roots outside C, and let N_fixed be the sum of all already identified multi-root counts and unary counts on C. Then the remaining possible counts are exactly the tuples

    m_i>=1 for i in I,   sum_(i in I) m_i <= M-N_fixed.          (2)

Each m_i is an integer. If I is empty all counts are identified. If I is nonempty and M-N_fixed=|I|, every remaining count is one. If M-N_fixed>|I|, the remaining gauge is genuine; every isolated unary root has at least two compatible counts among the allowed tuples. The ceiling couples those choices, so they cannot be chosen independently without checking the sum.

This is a constructive discrete-structure theorem from certified population approximation access. It does not recover an entire calibration function from finitely many values, promise a uniform required precision/runtime/sample budget, or turn empirical frequencies into a Cauchy population oracle.

## 2. Boolean corners identify minimal supports

For every U contained in R, query the corner 1_U that is one on U and zero elsewhere. Endpoint preservation makes every enabled route succeed with probability one. Therefore

    Q(1_U)=0 exactly when some positive support S is contained in U;
    Q(1_U)=1 otherwise.

These are exact model-implied alternatives even though the oracle returns approximate centers. One query with epsilon=1/4 distinguishes them by threshold 1/2. The empty corner is one because no empty/spontaneous support is allowed.

Let F be the antichain of inclusion-minimal U for which Q(1_U)=0. Its members are exactly the inclusion-minimal positive route supports. To verify this, a minimal U with a route S contained in it cannot have S properly smaller, while a minimal positive support has no smaller positive corner.

If F is empty, the inventory is empty and every count is zero. This includes M=0 and R empty; no division by M is performed. In every remaining admissible case M>=1.

Define

    A=union of T in F,   B=R\A.

Every positive support contains some inclusion-minimal positive support, since the finite family of its positive subsets has a minimal member. Consequently every positive support intersects A, and no route lies wholly in B.

**A is not the interaction-anchored set C in section 1.** For example, one A-only route plus one AB route has minimal-support union {A}, while both roots belong to C. A root in B may participate in a nonminimal interaction; its interior calibration need not be known or bounded below at this stage.

## 3. The ceiling supplies interior rate lower bounds on A

Choose once and for all a rational interior base vector b_i, for instance b_i=1/2 for every root. The same nominal b_i is used whenever root i occurs in any minimal support or later mixed-grid query.

For a minimal support T in F, set coordinates in T to their base commands and every other coordinate to zero. No proper positive support lies inside T, so

    q_T=Q(b_T,0_else)=(1-p_T)^n_T,
    p_T=product_(i in T)r_i(b_i),  0<p_T<1,  1<=n_T<=M.         (3)

Refine the Cauchy oracle until its certified rational upper bound q_T^+ is strictly less than one. This terminates because q_T<1. No modulus or exact zero/equality test is needed: upper endpoints converge to a strictly smaller number.

Bernoulli's inequality gives

    1-q_T=1-(1-p_T)^n_T <= n_T p_T <= M p_T.

Hence the rational number

    ell_T=(1-q_T^+)/M >0

satisfies ell_T<=p_T. Since each factor in p_T belongs to (0,1), p_T<=r_i(b_i) for every i in T. Thus set

    lambda_i=max_(T in F, i in T) ell_T,  i in A.               (4)

Every lambda_i is a known positive rational lower bound for the actual rate r_i(b_i). Each is strictly less than one. No such lower bound is asserted for B, and none is needed in the detection phase.

The bound M is a premise used in the inequality; it is not estimated from q_T or the corners. The unary count/calibration gauge prevents reading a count ceiling off that curve. An incorrect ceiling can invalidate (4) and the later gap test.

## 4. A positive mixed grid separates every support

For U contained in A and V contained in B, define x(U,V) to use base commands on U, unit commands on V and zero elsewhere. Write

    q(U,V)=Q(x(U,V)).

Every one of these finitely many raw probabilities is positive. Indeed every route meets A. If it is active at this mixed command it has at least one factor r_i(b_i)<1, so its success probability is strictly less than one. If it is inactive its failure factor is one. A finite product of these positive route-failure factors is positive. In particular q(empty,V)=1 for all V.

For nonempty T contained in A and any H contained in B, **including H empty**, form the multiplicative double mask contrast

    Z_(T,H)=product_(U subset T, V subset H)
             q(U,V)^((-1)^(|T|-|U|+|H|-|V|)).                  (5)

All divisions in this expression are by strictly positive numbers. For derivation only, take finite logarithms. If a route has support P union J, with nonempty P contained in A and J contained in B, it contributes to log q(U,V) exactly when P is contained in U and J is contained in V. In that case its contribution is

    n_(P union J) log(1-product_(i in P)r_i(b_i)),

independent of U,V. The two finite alternating subset sums cancel every term except P=T,J=H. Therefore

    Z_(T,H)=(1-p_T)^n_(T union H),
    p_T=product_(i in T)r_i(b_i).                              (6)

Equation (6) is valid for every nonempty T, not just minimal T. There are no missing supports wholly in B: their counts were already proved zero from the minimal antichain. H empty is essential to cover supports wholly inside A.

Define the known rational gap

    d_T=product_(i in T)lambda_i >0.

By (4), p_T>=d_T. Under the model promise there are only two separated possibilities:

    n_(T union H)=0  implies Z_(T,H)=1;
    n_(T union H)>0 implies Z_(T,H)<=(1-p_T)<=1-d_T.             (7)

Compute a certified approximation to Z_(T,H) with error less than d_T/4 and compare it with 1-d_T/2. This decides presence without testing equality to one. Repeating over all T,H recovers the complete positive-support family.

### Why the required quotient precision is obtainable

Every q(U,V)>0. Refine each needed input interval until its lower endpoint is positive, then propagate rational product and quotient intervals through (5). The input intervals shrink to their positive true values, and the finite rational operations are continuous there. Refinement therefore eventually gives an interval of width less than any specified positive tolerance, including the gap required in (7).

This is a termination proof, not a uniform conditioning bound. Some q values and some d_T can be arbitrarily small across admissible homeomorphisms. No lower bound on them is silently inferred from nominal commands.

The corners used in section 2 can have Q=0, but no logarithm or reciprocal of those corner values is used. The mixed grid is a different family of command vectors and has positive raw Q by the preceding argument. This separation prevents any log(0) cancellation or division-by-zero issue.

## 5. Constructive multiplicity recovery after detection

### Positive multi-root supports

For every detected S with |S|>=2, apply the separately reviewed finite-panel procedure in `../interaction-calibration-anchor/FINITE_PANEL_APPENDIX.md`. Choose two strictly ordered interior commands on two of its roots and fixed interior commands on all other roots in S. Form its four isolated support values Z_pq from ordinary zero/interior masks. They have the form

    Z_pq=(1-K a_p b_q)^n_S,  0<K<=1.

For candidate h>0 the determinant of [1-Z_pq^(1/h)] has strict sign(h-n_S), and is zero only at h=n_S. At half-integer cuts h=k+1/2 it is nonzero. Certified Cauchy intervals eventually determine each sign. Binary search in the supplied integer interval 1,...,M recovers n_S in finitely many such sign decisions. No exact-real equality test is used.

This support is known positive from section 4, so the predecessor's essential promise has now been supplied constructively. Root membership in B does not obstruct this phase: strict monotonicity supplies strictly ordered interior actual values even when their separation is not quantitatively known. Nonzero half-integer determinant signs still eventually separate.

### Unary counts on interaction-anchored roots

Detection already gives every absent unary count as zero. For a positive unary support on a root i participating in a positive interaction S, the now-known count n_S lets two isolated interaction values supply the rate ratio r_i(x_2)/r_i(x_1) at any two ordered interior commands.

Import `../finite-hypergraph-calibration/ANCHORED_UNARY_COUNT.md`, the separately owned and reviewed positive-unary sign lemma. With solo values U_k=(1-a_k)^m and the interaction ratio rho=a_2/a_1, it proves that

    D(h)=1-U_2^(1/h)-rho[1-U_1^(1/h)]

has strict sign(h-m). Positive half-integer cuts therefore give terminating Cauchy sign decisions without an equality test. Binary search in 1,...,M recovers the unary count; if M=1, positivity already forces count one. Its hypotheses hold here because positivity was decided in section 4, the incident interaction count has been recovered, and the same coordinate calibration is shared across unary and interaction supports.

This imports the general lemma rather than claiming it again. `CORROBORATING_UNARY_CHECK.md` preserves this lane's equivalent determinant calculation as a corroborating check only. The final source binding and review receipt identify the exact imported artifact. The resulting finite count recovery does not require reconstructing the entire calibration map or an effective rate for a boundary limit.

## 6. Exact residual count fibre under the ceiling

Let I and N_fixed be as defined in section 1. A root i in I appears only in its unary support. Its full response factor is (1-r_i(x))^n_i. Replacing its count by any positive integer m_i and its calibration by

    r'_i(x)=1-(1-r_i(x))^(n_i/m_i)

preserves that factor at every command and remains an allowed homeomorphism. Since the root appears nowhere else, this replacement changes no other factor. Apply it simultaneously to all i in I. Exactly those tuples satisfying (2) obey the supplied total ceiling.

Conversely, the frozen exact full-response equivalence classification forces agreement of all multi-root counts and every anchored unary count, and preserves every support's positivity. It leaves only these isolated-unary replacements and unused-root maps. Thus (2) is the complete multiplicity fibre of the full response function inside the class (1), not merely a list of candidates from a weak finite design.

The actual world's existence guarantees M-N_fixed>=|I|. If equality holds, every m_i is forced to one. If the residual budget is larger, the all-one tuple and a tuple adding one to any selected isolated root are both admissible. An upper bound is not a promise that the total equals M; replacing (2) by equality would impose a different prior.

Unused-root calibrations remain unobserved. Calibration maps of interaction-anchored roots are determined by the full response law according to the earlier theorem, but this finite-query procedure outputs discrete structure and counts, not entire infinite-dimensional maps.

## 7. Conditional covered-root detection without a total ceiling

The same gap mechanism has another sufficient premise. Suppose a finite family F_known of positive supports has known positive integer counts, and let D be their root union. Choose one common interior base vector for every support in this family. For each S in F_known, its isolated value gives the Cauchy-computable positive product

    P_S=1-Z_S^(1/n_S)=product_(i in S) r_i(b_i)>0.

Refine until a positive rational lower bound ell_S<=P_S is certified. Since P_S<=r_i(b_i) for each i in S, choose lambda_i as the maximum available ell_S over known supports containing i. These are effective positive rootwise lower bounds on D.

For any nonempty target T contained in D, the ordinary zero/interior mask contrast E_T is one if n_T=0, and is at most 1-product_(i in T)lambda_i if n_T>0. The same separated midpoint test therefore decides that target's presence. No upper bound on its multiplicity, or on the total inventory, is needed for this conditional conclusion. It includes unary targets, although endpoint access can also decide unary presence directly.

Known positive interactions can supply the needed counts through the prior promised-positive procedure. The known-positive support family is a premise or an already certified result; this corollary does not infer it by circularly assuming the target's presence. It makes no claim for uncovered roots, and shared base commands and common calibration remain essential. It is compatible with the unbounded absence witness, whose absent base world has no known-count positive support covering its unused B root.

This is an application of the already proved positive-gap mechanism, proposed by the finite-hypergraph-calibration reviewer and assigned to this detection stage. It is not credited as a second independent discovery of that mechanism.

`COVER_DISCOVERY.md` separately proves that, when every root in a known finite universe is promised to lie in a positive multi-root support, fair positivity searches and count recovery discover such a cover and terminate with all support statuses and counts, without a total ceiling. Without that promise the same discovery process is partial and makes no negative inference from nontermination.

## 8. Limits and comparison with the unbounded obstruction

The frozen unbounded absence family has N unary A routes plus one AB route. Its minimal support is {A}, and N grows without bound. No fixed total M contains that sequence. The lower-bound step (3)-(4) pinpoints why the new prior changes the problem: an interior minimal-support failure curve can no longer be attributed to arbitrarily many arbitrarily weak routes. This is a genuine change of admissible worlds, not a contradiction of the earlier negative result.

For the support-detection phase alone, the proof only needs known upper bounds on the multiplicities of the detected minimal supports. A common per-support ceiling would suffice for that phase as well. It is not the same as a total ceiling: applying the final fibre constraint (2) requires the actual total bound, not silently relabeling a per-support bound as M. We make no minimal-assumptions characterization or separate theorem for all weaker prior classes.

Endpoint preservation and endpoint command access do substantial work. They give the binary corners and make every B factor equal one when enabled in the mixed grid. A model without those endpoints, with guards reevaluated under masks, with a fresh inventory mixture, correlated/shared-route gates, or support/context-dependent calibration has not been covered by this proof.

The algorithm can use a finite number of distinct rational command vectors and finitely many precision requests for each admissible input/name. The counts of refinements, required digits and numerical conditioning need not be uniform over the calibration class. No uniform sample, precision or runtime guarantee is asserted. The exact population Cauchy oracle is not supplied by a finite collection of random Bernoulli outcomes.

All conclusions presume the externally given ceiling and the generative/observation contract. They do not infer that ceiling from data, authenticate route occurrences, identify physical bearers, validate an intervention, settle productive adequacy, authorize protected integration or close T20.
