# Truth aim can constrain rationality without fixing a unique repair or its ultimate source

**Status:** scoped adversarial research, separate from sealed P15 and its rational-polytope successor. The results below are ordinary mathematical arguments and exact finite probes. They are standard accuracy-first ideas with an explicit robust-repair application; no global novelty, canonical adoption or proof-assistant credit is claimed.

## Result first

There is a genuine positive bridge stronger than an unstructured assertion that different norms give different answers:

> Given objective truth-value possibilities, positive weighted quadratic accuracy, access to the corresponding coherent projection, and a norm against uniformly accuracy-dominated credences, an agent's permissible credences must be probabilistically coherent.

The normative premise does not mention probabilistic coherence. The substantive added assumptions are the accuracy metric, the admissible alternatives, and the authority of the dominance norm. The conclusion is therefore a conditional derivation rather than a definition of coherence as rationality.

There is also a concrete obstruction to turning that classification into a common repair policy under uncertain standards. For b=(0.7,0.6) on A and ¬A, each positive quadratic weighting provides a coherent statewise-improving repair. Yet the two weights (1/4,3/4) and (3/4,1/4) have **no common coherent repair that is even weakly better at every possible truth state**. A smaller uncertainty interval does allow one, with a provable positive margin. This identifies a precise frontier: target classification, existence of a repair for each standard, and a single uniformly licensed repair are different claims.

## 1. An independently intelligible accuracy constraint

Let Ω be a finite nonempty set of allowed truth-value possibilities for propositions X₁,…,X_n. Write v(ω)∈{0,1}^n for the associated truth vector. Let C be the convex hull of these vectors. A vector c belongs to C exactly when it can be represented as the vector of proposition probabilities under some probability distribution on Ω. Thus C is the ordinary finite probabilistic-coherence region.

This descriptive/semantic input is not empty: the proposition identities and allowed valuations matter. Treating A and ¬A as independent Boolean coordinates would replace their two-state coherence segment by a square and erase the intended logical constraint. Mathematical modeling cannot silently supply correct truth conditions or an exhaustive space of metaphysically possible worlds.

For fixed positive weights w_i, define accuracy loss

`L_w(b,ω)=Σ_i w_i(b_i−v_i(ω))²`.

Positivity makes uniformly smaller coordinate errors better. The quadratic form additionally penalizes large errors and supplies a strictly convex aggregation. Both are intelligible candidate accuracy principles. Truth-directedness alone does not force the quadratic form; the deletion examples below make that limitation explicit.

The normative constraint D is:

`Do not retain b when an available alternative c has strictly lower accuracy loss at every allowed truth state, and no other relevant constraint defeats the comparison.`

This is a substantive norm, not a theorem of arithmetic or a hidden definition of “ought.” It can be motivated by the role of belief as truth-sensitive representation: a uniformly more accurate available alternative avoids a trade-off in truth-relative quality. Whether this norm is overriding, whether all relevant value is accuracy, and which changes count as available need separate defenses. We retain these as premises.

## 2. Positive theorem: weighted projection gives a coherent dominator

Let W=diag(w₁,…,w_n), and let c be the unique minimizer of ‖b−x‖²_W over C. Such a c exists because C is nonempty and compact, and is unique because W is positive definite.

**Theorem A1.** If b∉C, then for every ω,

`L_w(b,ω)−L_w(c,ω) ≥ ‖b−c‖²_W > 0`.

**Proof.** Optimality of the convex projection gives `(b−c)^T W(v−c)≤0` for every v∈C: differentiate the squared distance along the feasible segment from c to v at c. Expand

`‖b−v‖²_W−‖c−v‖²_W = ‖b−c‖²_W + 2(b−c)^T W(c−v)`.

The second term is nonnegative. If b∉C, positive definiteness makes the first term strictly positive. Apply this to each allowed truth vector. ∎

**Theorem A2.** No coherent c is weakly dominated at every state by a distinct d under the same loss.

**Proof.** Represent c=Σ_ω p_ω v(ω). Expanding expected losses gives

`Σ_ω p_ω[L_w(d,ω)−L_w(c,ω)] = ‖d−c‖²_W >0`.

If d were no worse at every state, the left side would be nonpositive, a contradiction. No positive probability at every state is required for this argument. ∎

Consequently, under a fixed w, the undominated region is exactly C. Add D and availability of the projection, and coherence follows. This argument does not put coherence into D. It does supply a specific geometry of accuracy and the truth-state input. It is a finite weighted-quadratic specialization of established accuracy-dominance results, not a new general proof of probabilism.

**Robust classification.** Every positive w yields the same undominated region C, even though its nearest coherent projection can differ. Thus an application target can be invariant while the full enrichment and recommended intervention are not unique. This is a positive instance of the distinction established in P15.

## 3. The quantifier boundary: every score has a repair, but no common repair

For two exhaustive, mutually exclusive propositions, write b=(x,y), and w=(α,1−α), 0<α<1. The weighted projection is

`c_α=(t_α,1−t_α),  t_α=αx+(1−α)(1−y)`.

For b=(7/10,3/5), the projections at α=1/4,1/2,3/4 are respectively (19/40,21/40), (11/20,9/20), and (5/8,3/8). Each strictly improves both truth-state losses under its own weighting. The improvement is `α(1−α)(x+y−1)²` in each state.

Now require a single coherent c=(t,1−t) to be no worse under both α=1/4 and 3/4. Its loss at A-true is (1−t)², independent of α; its loss at A-false is t². The minimum original losses across the two standards are

`m₁=63/400=0.1575`, `m₀=97/400=0.2425`.

Therefore a common weak repair would require `(1−t)²≤63/400<4/25` and `t²≤97/400<1/4`. Since 0≤t≤1, the first implies t>3/5 and the second t<1/2. Impossible. This excludes even weak statewise improvement, not just one choice of strictness at a boundary.

The logical forms are:

`∀w ∃c∈C ∀ω: L_w(c,ω)<L_w(b,ω)` — proved for each positive w;

`∃c∈C ∀w ∀ω: L_w(c,ω)<L_w(b,ω)` — false in this example.

The known wide/narrow dominance concern is therefore not a merely verbal caution. It becomes a concrete admissibility-policy countermodel. An agent may know that b is dominated according to whichever score is correct, while a policy requiring one improvement licensed under all unresolved scores has no such coherent move. A conclusion that b should be coherent does not itself select an executable c.

### Randomization does not remove this obstruction

Suppose a common probability law μ selects coherent repairs, independently of the unresolved standard and truth state, and evaluate a random repair by its expected Brier loss. Its mean c̄ lies in C. Convexity gives `L_w(c̄,ω)≤E_μ L_w(c,ω)` for every w,ω. Any common randomized weak improvement would therefore supply a deterministic common weak improvement, which the counterexample excludes. This rules out randomization as a repair here under expected-loss semantics; it does not grant access to a law selected using hidden standard or truth information. For the complement segment the Jensen gap is exactly the variance of its first coordinate, since both statewise coherent losses have unit quadratic coefficient.

### Stronger unrestricted-weight observation

Suppose each represented proposition is true at some allowed state and false at some allowed state, and allow every strictly positive weight vector. If d differs from b in coordinate i, one of those states makes d's error in coordinate i strictly larger. By concentrating positive weight sufficiently near i, that state's total loss becomes larger. Thus no distinct d can weakly dominate b across all positive weights and all states.

Accordingly, the intersection of per-score undominated sets is C, whereas taking undominated points under the intersection of all score-specific dominance relations can leave the entire credence cube. These operations do not commute. The “every proposition varies” and rich-weight-class premises matter: tautological coordinates or tightly constrained weights can admit uniform repair.

## 4. Positive repair conditions under bounded uncertainty

For fixed x,y and weight interval α∈[a,b]⊂(0,1), define

`m₁ = min_{α∈{a,b}} [α(1−x)²+(1−α)y²]`,

`m₀ = min_{α∈{a,b}} [αx²+(1−α)(1−y)²]`.

**Theorem A3.** A common coherent repair strictly better at both truth states for every α in the interval exists exactly when `sqrt(m₁)+sqrt(m₀)>1`. A coherent replacement weakly no worse everywhere exists exactly when the sum is at least 1.

**Proof.** For c=(t,1−t), strict comparison requires `(1−t)²<m₁` and `t²<m₀`, equivalently `1−sqrt(m₁)<t<sqrt(m₀)`, with 0≤t≤1. Since each m is in [0,1], this interval is nonempty exactly under the stated condition. Replace strict inequalities by weak ones for the second claim. Endpoint evaluation is complete here because each original loss is affine in α for a fixed truth state; this does not license original-vertex checking for arbitrary Boolean ranking claims. ∎

For b=(0.7,0.6) and α∈[0.45,0.55], c=(0.55,0.45) improves every allowed score and state by at least 3/500. For a symmetric uncertainty interval [1/2−h,1/2+h], 0≤h<1/2, the strict-repair criterion reduces exactly to

`h²+330h−25<0`, or `h<5 sqrt(1090)−165` (approximately 0.07574).

At equality a weak common replacement exists but no all-state-strict common replacement. At h=1/4 even weak repair is impossible. The strict/weak distinction is explicit; no ambiguous “Pareto improvement” is used.

**General local robustness lemma.** Suppose a fixed c₀ improves b under w₀ with minimum statewise gain δ>0. Set `r_ω,i=(b_i−v_i(ω))²−(c₀_i−v_i(ω))²` and `R=max_ω ‖r_ω‖_∞`. If `‖w−w₀‖₁<δ/R`, then c₀ still improves b in every state, because the change in each gain is bounded by `‖w−w₀‖₁R`. This provides a sufficient, sometimes conservative common-repair neighborhood. It neither chooses the correct weights nor claims every uncertainty set admits repair.

## 5. Deletion and rival models

**A. Truth-directedness without strict propriety.** Take equal-weight absolute error instead of squared error. On A/¬A, every b=(x,y) in the unit square has the two losses 1−x+y and x+1−y, whose sum is 2. Hence no vector can lower both, or weakly lower both with one strict improvement. Incoherent vectors remain undominated. Absolute error is continuous, symmetric and truth-directed, so those properties alone do not establish the positive coherence theorem.

**B. A zero-weight coordinate.** With w=(1,0), b=(0.7,0.6) cannot be strictly improved at both truth states by changing the first coordinate; changing only the second leaves all measured loss unchanged. Positivity in A1 cannot simply be omitted.

**C. Available alternatives can exclude the repair.** Suppose an independent evidential side constraint fixes the first coordinate at 0.7. Among alternatives (0.7,z), reducing the second coordinate improves loss at A-true but worsens it at A-false, and increasing it reverses that trade-off. The incoherent b=(0.7,0.6) is undominated within this available set. The coherent alternative (0.7,0.3) improves one state and worsens the other. This is a nontrivial continuous alternative set, not a singleton manufactured to block change. Whether that evidential constraint is justified remains a separate issue.

**D. Calibration does not uniquely fix truth accuracy.** Let Y be equally likely 0 or 1. A constant forecast 0.5 is calibrated. The informative forecast 0.6 when Y=1 and 0.4 when Y=0 has squared error 0.16 in either state, improving on 0.25, yet is uncalibrated within its two report groups. Calibration and pointwise closeness to truth can disagree; a calibration-only source constraint does not supply the entire accuracy ordering. A perfect report Y is both calibrated and more accurate, so this does not argue against calibration as one desideratum.

**E. Strictly proper does not mean objectively true.** A proper scoring mechanism elicits a supplied belief p by maximizing expected score under p. If the forecaster's belief differs from the actual data-generating law, honest reporting can still be systematically inaccurate. The subjective and objective expectation measures must not be silently identified.

**F. Report-dependent outcomes.** The usual propriety comparison keeps the outcome distribution fixed as the report varies. If reporting q changes Y to Bernoulli(q), expected squared error becomes q(1−q), minimized at 0 or 1. It does not generally select an earlier belief p. This is a causal act–state dependence issue, not a failure of the fixed-distribution propriety theorem.

## 6. Strict propriety fixes honest reporting but not the ranking of imperfect reports

For a differentiable strictly convex G:[0,1]→R, define the score

`S_G(q,y)=G(q)+G′(q)(y−q)`.

Under a fixed Bernoulli(p) law, expected score is `G(q)+G′(q)(p−q)`, uniquely maximized at q=p by strict convexity. The expected regret is the Bregman quantity `D_G(p,q)=G(p)−G(q)−G′(q)(p−q)`.

Take p=1/10, q_A=1/100 and q_B=1/5. For G₂(q)=q², regrets are 81/10000 and 1/100, so q_A is better. For G₄(q)=(1−q)^4, regrets are 4481163/100000000 and 417/10000, so q_B is better. Both generators are strictly convex and produce strictly proper scores. The second is asymmetric, but that feature is not needed for the failure. Use instead the symmetric generators H₂(q)=q²+(1−q)² and H₄(q)=q⁴+(1−q)⁴. Their regrets at the same reports are respectively (81/5000,1/50) and (2245563/50000000,217/5000), preserving the opposite rankings. Both generators, and their resulting outcome/report comparisons, respect complement symmetry. Thus adding this symmetry does not force a unique full ranking.

Thus strict propriety supplies a genuine invariant optimum given p, but does not supply a unique full ranking. It is a substantial constraint, not an automatic canonical norm-fixing theorem. Additional constraints can matter. Any stronger uniqueness argument must state its domain, invariances, locality, regularity, units and admissible transformations; it cannot call these details consequences of “truth aim” without argument.

## 7. Consequences for the one-bearer R5 rival and the source question

The positive theorem can narrow the epistemic competence demanded by the programme: a truth-aiming rational system with the stated accuracy and availability conditions should not remain incoherent. It does not infer that the system consciously computes a score, that its causal mechanism represents this theorem, or that the ultimate ground hosts the relevant thought token.

An enriched R5 can include a single impersonal fundamental structure, local agents that genuinely host thoughts, environmental regularities, and error-correcting feedback that tracks truth-sensitive outcomes. Such a rival can implement or approximate accuracy-improving transitions. This is a substantive functional architecture rather than setting a personal-source predicate to false. But the architecture alone still owes its account of original content and the authority of accuracy norms. We neither discharge those debts by simulation nor treat them as an automatic contradiction.

The positive source position can fairly insist that correctness is more than stable causal output, and that genuine understanding involves content-sensitive reasons. To reach an ultimate personal source, however, it must add a defended relation connecting the relevant norm or representational particular to the ultimate bearer: constitutive hosting, norm-authoring or another precise relation. Being the ultimate causal or metaphysical ground of a local accuracy-sensitive process does not by itself instantiate that relation. The constitutive-locality argument already investigated applies to the locus that bears the attribute; it does not reverse the inference from grounding an attributed thing to bearing its attribute.

The refined frontier is therefore twofold:

1. Can the truth-role and relevant evidence independently justify enough structure to fix a normative target or a common permitted repair?
2. If so, why must the source of that norm be an intentional host at the fundamental locus, rather than a norm recognized and instantiated by local thinkers under an impersonal ground?

A1–A3 make real progress on the first conditional. They do not answer the second by definitional transfer. School-neutral accuracy mathematics and Athari-conditional bearer/locality premises retain separate scopes.

## 8. Primary-literature scope

Predd and collaborators give a broader coherence/dominance theorem under their regularity conditions. Their paper uses “proper” as an abbreviation for strictly proper and explicitly assumes additive penalties over a finite list of events. Our argument above proves its finite positive-weight quadratic specialization directly; it does not attribute the robust uncertainty threshold or every later nonadditive extension to that paper. [Predd et al., 2009, §§II–IV](https://www.princeton.edu/~kulkarni/Papers/Journals/j071_2009_PreSeirLieOshKulPoo_TransIT.pdf)

Joyce distinguishes the normative warrant of dominance from its mathematical consequences and discusses the wide/narrow quantifier issue: score-relative dominators need not be a common dominator. His discussion also considers whether a context has one correct score. This motivates careful typing of the issue; our finite examples do not settle that philosophical dispute. [Joyce, Accuracy and Coherence, §§10–12](https://websites.umich.edu/~jjoyce/papers/aac.pdf)

Gneiting and Raftery distinguish proper scoring, honest elicitation, calibration and sharpness, and connect strict propriety with convex generators. These are mathematical/evaluative constraints with many instances. They do not by themselves establish an ultimate normative authority or a unique metaphysical source of truth. [Gneiting–Raftery, 2007, §§1–3](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf)


## 9. Verification and limitations

Seven unit tests were written before their respective implementations: six for the initial exact formulas and one exposing the need for the symmetric-generator extension. Red and green logs are retained. Exact arithmetic probes checked 2,299 weighted projections with 4,598 statewise gain identities, 50 rational uncertainty-width threshold instances, 484 strict-propriety pairs across four generators, 121 absolute-error constant-sum cases and 1,452 randomized Jensen identities. All passed, with no mismatches. These are finite implementation checks accompanying the proofs, not new mathematical novelty or empirical validation.

The small arithmetic helpers accept exact mathematical inputs in their stated domains; they are not a hardened external-data parser. No code or theorem has been integrated into the canonical repository. The examples identify premise sensitivity and a real conditional normative bridge. They do not determine which scoring regime is correct, whether all relevant epistemic value is captured by accuracy, or whether the positive normative premises require an ultimate intentional bearer.
