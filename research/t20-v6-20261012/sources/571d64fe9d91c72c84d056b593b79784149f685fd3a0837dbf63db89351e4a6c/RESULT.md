# Bayesian likelihood updates and independently imposed probability constraints

10 October 2026 UTC. Scratch-only T20 mathematical continuation. Ordinary proofs and exact finite controls; no protected repository changes, empirical claim, formal-kernel certification, integration, or T20 closure.

## 1. Result, scope, and inherited difference

If a nonempty closed convex set of finite probability laws must remain feasible under **every strictly positive likelihood update**, it must be a simplex face: its only restrictions are fixed zero coordinates. This follows from the classical normalized-multiplication group action and elementary face geometry.

For an actual, specified likelihood, the condition is much weaker and can be decided exactly for an affine probability family. Homogenize its equalities, restrict to the family's actual support, and test preservation of the resulting kernel by the likelihood's diagonal matrix. Row reduction gives a particularly simple test: the likelihood must be constant on each component of a pivot/free-coordinate incidence graph. The graph and its matroid ancestry are classical; its role here is an exact implementation guard.

The decisive negative control is stronger than a failure of algebraic composition. With fixed block masses, “Bayes then KL reproject” satisfies composition and scalar/null neutrality, yet can erase all the genuine information in a declared positive observation channel. It is a different update operation. It can be legitimate Jeffrey-type marginal replacement when there is an independently justified replacement-evidence contract; it is not ordinary Bayes for the unchanged channel in the countermodel.

The inherited difference is bounded and specific:

- `warranted-learning-20261009/RESULT.md`, §§2–8, classifies multiply-then-repair with the **full simplex** as repair codomain and retains model, source, provenance, and authority premises. It does not authorize replacing that codomain by an arbitrary constraint slice while keeping its characterization unchanged.
- `nonseparable-bayes-repair-20261009/RESULT.md`, §§2–6, proves the perspective family and divergence decomposition. Those formulas imply the additional-constraint projection identity below; that input is inherited, not rediscovered.
- `noetic-gradient-transport-20261009/RESULT.md` distinguishes radial normalization, tangent objective correction, and transport of a separately specified metric. It supplies no identification of noetic hard constraints with affine probability equations.
- The pinned `SOUND-DESCENT-MODEL-COMPARISON.md` explicitly makes G1 feasibility-first and preserves provenance, uncertainty, hard constraints, and whole-state rereading. Its G1 remains a proposed candidate and G2 a conditional/future literal geometry. No theorem here upgrades that status.
- Deep AX V2 already supplies Bayesian source likelihoods, conditional factorization, duplicate invariance, and separately typed source/world obligations. H-Continuation and the retained audit-continuation packet already own instrument/observable invariant-subspace transport. This packet does not claim a new general Bayesian filtering or quotient theorem.

A bounded scan of those packets and nearby mathematical continuations found no statement of this particular feasible-family classifier, support-restricted affine test, or fixed-block composition countercontrol. This is a programme-local comparison, not an exhaustive field or repository priority search. Classical ancestry is recorded in §8.

**No normative identification is made.** The application begins only if an implementer separately represents a particular hard constraint by a probability feasible set. Source validity, normative authority, actual warrant, and permission to acquire or act on information remain distinct dimensions. A normative prohibition on an action does not imply that the prohibited action has probability zero.

## 2. The positive action and its complete support classification

Let n≥1 and

    Δ = {p∈R^n : p_i≥0, Σ_i p_i=1}.

For L∈R^n_{++}, define

    B_L(p) = D_L p / (1ᵀ D_L p),    D_L=diag(L).

The denominator is positive. These maps obey

    B_L B_M = B_(L⊙M),    B_1=id,    B_L^(-1)=B_(1/L),    B_(cL)=B_L (c>0).

“Preserved” initially means B_L(C)⊆C; when it holds for every positive L, the inverse law supplies equality. Arbitrary positive vectors are mathematical likelihood weights. Each can be rescaled into (0,1)^n without changing B_L and realized as one outcome of some positive binary channel. This does not make every such vector an available outcome of one **fixed** evidence model.

For ∅≠S⊆{1,…,n}, put

    Δ_S = {p∈Δ : p_i=0 for i∉S},
    Δ_S° = {p∈Δ : supp(p)=S} = relint(Δ_S).

### Lemma 1: each orbit is exactly one support stratum

The orbit of p under all positive B_L is Δ_supp(p)°. Positivity preserves every zero and nonzero coordinate. Conversely, if p and q have the same support S, choose L_i=q_i/p_i on S and any positive values off S. Then D_Lp=q, its mass is 1, and B_L(p)=q. This also covers vertices and every lower-dimensional face. □

Consequently every invariant set, with no regularity assumption, is precisely

    C_F = ⋃_{S∈F} Δ_S°

for some family F of nonempty supports. For nonempty F:

1. C_F is convex iff F is closed under unions.
2. C_F is closed in Δ iff F is downward closed under nonempty subsets.

For (1), the support of a strict mixture of two laws is the union of their supports. Thus convexity requires union closure, and union closure makes every such mixture stay in an included stratum. For (2), closure of Δ_S° is Δ_S, so closedness requires every nonempty subset of S. Conversely, with downward closure, C_F is the finite union of the closed faces Δ_S for S∈F, hence closed. □

### Theorem 2: universal positive likelihood preservation selects faces

A nonempty closed convex C⊆Δ is preserved by every positive B_L iff C=Δ_S for a unique nonempty S.

One proof follows immediately from the preceding support-family description: union closure gives the maximal support S=⋃F as a member, and downward closure gives all its nonempty subsets and no others.

Equivalently, for each coordinate that is positive somewhere in C, select a witnessing point. Their finite average belongs to C and is positive on precisely S. Lemma 1 supplies all of Δ_S°, closedness supplies Δ_S, and the definition of S excludes any larger support. The converse is support preservation. □

Both hypotheses matter for this conclusion when only positive likelihoods are used. Δ_S° is convex and invariant but is not closed for |S|≥2. The union {e_1,e_2} is closed and invariant but not convex. There is no exceptional low-dimensional case; n=1 leaves the sole singleton face.

### Zero likelihoods and impossible branches

For L≥0, B_L(p) is defined only when Lᵀp>0. Its support is supp(p)∩supp(L). Invariance under all such **defined** updates forces downward closure of the support family: any nonempty subset is reached by zeroing the excluded coordinates. Thus convexity alone, with invariance under all defined nonnegative updates, already selects faces; topological closure then follows. Nonconvex downward-closed families remain possible.

An update with Lᵀp=0 is undefined conditioning, not a posterior to be “repaired.” If every coordinate supported by C receives likelihood zero, no law in C has a defined branch. Declaring an arbitrary replacement law changes the model and operation. Positive inverse-update statements below do not extend to singular diagonal likelihoods.

## 3. An exact test for a specified likelihood and affine family

Let

    C = {p∈Δ : Ap=b}

be nonempty, with any finite real matrix A and vector b. Redundant equations are allowed. Define the homogenized matrix and cone

    M = A − b1ᵀ,
    K = {x≥0 : Mx=0} = {tp : t≥0, p∈C}.

The equality follows by normalizing every nonzero x≥0: Mx=0 says Ax=b(1ᵀx). Let S=⋃_{p∈C}supp(p). All x∈K vanish outside S. Write M_S for its columns on S, D=diag(L_i:i∈S), and V=ker M_S.

### Support-generating fact

There exists p*∈C positive on every coordinate of S, by averaging finitely many coordinate witnesses. For v∈V, choose t≥0 large enough that v+t p*_S≥0. Then

    v=(v+t p*_S)−t p*_S

is a difference of two elements of K restricted to S. Therefore

    span(K restricted to S)=V.

No full-simplex interior or full-dimensional affine family is assumed.

### Theorem 3: equivalent exact preservation criteria

For a fixed L>0, the following are equivalent:

(a) B_L(C)⊆C.
(b) D_L K⊆K.
(c) D V⊆V.
(d) M_S D annihilates ker M_S.
(e) row(M_S D)⊆row(M_S).
(f) rank([M_S; M_S D])=rank(M_S), where the semicolon denotes vertical stacking.

Whenever these hold, in fact

    DV=V,    D_LK=K,    B_L(C)=C,

and B_(1/L) also preserves C.

**Proof.** Normalizing or unnormalizing a nonzero positive-mass vector proves (a)⇔(b). Positivity of D makes (c) imply (b); applying D to the span identity makes (b) imply (c). The definition of V gives (c)⇔(d), and the finite-dimensional identity (ker M_S)^⊥=row(M_S) gives (d)⇔(e)⇔(f). Since D is invertible, dim DV=dim V; inclusion then implies equality. Thus D^(-1)V=V as well. The inverse is again a positive diagonal map, hence preserves the nonnegative orthant and K. Both inclusions give equality of K and of its normalized base. □

Actual support cannot be omitted. For C={p∈Δ_3:p_2+p_3=0}={e_1}, take M=(0,1,1), L=(1,2,3). Every positive likelihood preserves C. Yet row(MD_L) is not contained in row(M). On the correct S={1}, M_S=0 and the test passes. A kernel containing signed directions that no feasible law can realize is the wrong test domain.

The converse from forward inclusion to equality is specific here to affine equality families with nonnegativity. For the closed convex inequality family C={p∈Δ_2:p_1≥1/2}, L=(2,1) maps C onto {p:p_1≥2/3}, a proper subset. Likewise a zero-likelihood update can map a full simplex onto a proper face on its defined domain.

### Corollary 4: all preserving likelihoods from one row reduction

Take a reduced row-echelon form R of M_S, removing zero rows. Let p_r be the pivot coordinate of row r, and J the free coordinates. Form an undirected graph on S with edge {p_r,j} whenever j∈J and R_rj≠0. Isolated coordinates count as components.

Then L>0 preserves C exactly when L is constant on each connected component of this graph. Coordinates outside S are unrestricted.

**Proof.** The standard nullspace basis has one vector v^(j) for each free j, with free coordinate j equal to 1, other free coordinates 0, and pivot coordinates v^(j)_(p_r)=−R_rj. Evaluating R D v^(j) gives, in row r,

    R_rj (L_j−L_(p_r)).

Thus D preserves the kernel iff every nonzero incidence forces equality of the two likelihood values. These pairwise equalities are exactly constancy on graph components. □

The graph is the fundamental-circuit incidence graph of the column matroid of M_S; the graph/components machinery is classical, not a field-new algorithm. The displayed proof does not require importing any matroid theorem. It also shows that changing a row basis or pivot choice does not change the resulting allowable positive diagonal maps: they are characterized intrinsically by Theorem 3. The admissible component partition is intrinsic, since distinct components can be assigned distinct positive values.

This makes fixed-model quantifiers operational. For a declared positive channel K(y|i), test only its actual L_y=(K(y|i))_i, and the relevant conditioned likelihoods after histories. To guarantee preservation for **all priors in C**, every permitted likelihood must pass Theorem 3. A finite family of passing likelihoods automatically preserves C under every finite product. No theorem grants permission to make any of those observations.

### Corollary 5: a preserving channel observes only the component label

For a fixed nonempty affine family C and its component map j(i), a finite strictly positive observation channel preserves C outcome by outcome for all priors in C iff, on S,

    K(y|i)=κ(y|j(i))

for a stochastic channel κ on component labels. Indeed, Corollary 4 applied to each likelihood row is exactly constancy of that row within each component; column normalization then gives Σ_yκ(y|a)=1. Thus the declared observation mechanism factors through the component label, and cannot distinguish states within one component.

Every finite sequence of such channels preserves within-component prior odds: for p_i,p_j>0 in the same component, the successive likelihood factors cancel in p_i/p_j. Zeros remain zero. This also holds for adaptive selection based on recorded past observations and independent randomization, provided that C, S, and the target remain fixed and every selected conditional channel satisfies the same criterion. Selection must not introduce an unmodelled state-dependent signal. This is a restriction on what information the globally preserving mechanism can acquire, not a claim about computational or statistical complexity, actual sources, or permissions.

For one actual current prior p∈C, the weaker necessary and sufficient test is simply

    M D_L p=0.

A likelihood can pass at that p while failing the family-wide test. A changing target, changing constraints, or history-dependent evidence model requires its own current test; preserving one step is not an all-time guarantee.

## 4. Positive controls: information can be compatible

### 4.1 An informative channel preserves a proper affine family globally

Let C={p∈Δ_3:p_1=p_2}. Its graph components are {1,2} and {3}, so all likelihoods (a,a,b) with a,b>0 preserve it. Consider the legitimate binary channel

    L_+=(3/4,3/4,1/4),    L_-=(1/4,1/4,3/4).

At p=(1/4,1/4,1/2), each outcome has probability 1/2, and the posteriors are

    Q_+=(3/8,3/8,1/4),    Q_-=(1/8,1/8,3/4).

Both stay in C and are informative about whether the state is in {1,2} or {3}. Under two conditionally independent repetitions, ++ gives (9/20,9/20,1/10), still in C. This does not contradict Theorem 2: this fixed channel supplies a restricted likelihood family, not every positive vector.

### 4.2 Preservation at one current prior is weaker and can still be legitimate

Let C={p∈Δ_3:p_1=1/2} and p=(1/2,1/4,1/4). Take

    L_+=(1/2,1/4,3/4),    L_-=(1/2,3/4,1/4).

Each outcome has probability 1/2 and gives

    Q_+=(1/2,1/8,3/8),    Q_-=(1/2,3/8,1/8).

These legitimate posteriors stay in C and change the within-block proportions. Neither likelihood preserves the whole family C, whose incidence graph is connected and therefore admits only scalar likelihoods globally. Indeed another independent + after Q_+ gives (4/9,1/18,1/2), outside C. An implementation scoped to the actual first-step pair must not reject that first update merely because a stronger universal-family contract fails.

## 5. What the inherited Bregman repair does with extra constraints

Use the inherited Bayes-compatible perspective family

    F(sp)=s f(p)+a(s)

with its first-argument Bregman convention. Its already proved identity is

    D_F(r,sp)=D_f(r,p)+D_a(1,s),    r∈Δ.

The boundary statement requires the inherited finite continuous extension of f and an interior second argument p. Therefore, for any independently imposed feasible C⊆Δ on which the objective is defined,

    argmin_(r∈C) D_F(r,b)
      = argmin_(r∈C) D_f(r,N(b)).

These are equal argmin sets; existence and uniqueness require their own hypotheses. Compact C with a finite continuous objective gives existence; strict convexity of the objective on C gives uniqueness. We do not infer strict convexity on every boundary face merely from strict convexity in the open simplex.

For b=L⊙p, the normalized point N(b) is the ordinary Bayesian posterior. Replacing the full-simplex codomain by C therefore inserts an additional **coherent-state constraint projection**. Bayes compatibility of the ambient extension eliminates normalization error, but cannot make an infeasible ordinary posterior belong to C. If a unique constraint projection is used, it equals that posterior iff the posterior is already in C. This is the precise connection to the inherited nonseparable repair, not a second normalization characterization.

## 6. Composition and null neutrality can coexist with lost evidence

Partition {1,…,n} into nonempty blocks I_1,…,I_k, and choose w_a>0 with Σ_aw_a=1. Let

    C_w={q∈Δ : Σ_(i∈I_a)q_i=w_a for every a}.

For a strictly positive law r, its first-argument KL projection onto C_w is

    P_C(r)_i = w_a r_i / r(I_a),    i∈I_a.

To prove this, write q_i=w_a q(i|I_a). Then

    KL(q||r) = Σ_a w_a log(w_a/r(I_a))
               + Σ_a w_a KL(q(·|I_a)||r(·|I_a)).

The first sum is fixed; each second term is uniquely minimized by preserving the conditional distribution in its block. This is the standard Jeffrey marginal-replacement formula and relative-entropy projection, stated here with its orientation and positive-domain hypotheses.

For p∈C_w with strictly positive coordinates, define U_L(p)=P_C(B_L(p)). Then

    U_L(p)_i = w_a L_i p_i / Σ_(j∈I_a)L_jp_j,    i∈I_a.

Direct cancellation gives

    U_L U_M = U_(L⊙M),    U_1(p)=p,    U_(cL)=U_L,    U_(1/L)U_L(p)=p.

Thus this constrained update has a perfectly consistent normalized multiplicative action within each block. Yet it is not in general B_L. In particular, **every likelihood constant within each block acts as the identity under U**, even when its constants differ between blocks and supply genuine evidence about block identity.

Equivalently, the operation divides the original likelihood by its current conditional mean within each block. That generally state-dependent adjustment removes the relative evidence affecting the prescribed block masses. Algebraic composition and null neutrality on the smaller codomain do not imply ordinary posterior fidelity. The full-simplex codomain in the older characterization was an essential hypothesis.

### A fully specified positive channel with exact repeated-update loss

Let X∈{1,2,3} have prior

    p=(1/2,1/4,1/4),    C={q∈Δ_3:q_1=1/2}.

For Y∈{+,-}, declare the genuinely stochastic, strictly positive channel

    L_+=(3/4,1/4,1/4),    L_-=(1/4,3/4,3/4).

Each coordinate's two likelihoods sum to 1. Both outcomes have probability 1/2. Ordinary Bayes gives

    Q_+=(3/4,1/8,1/8),    Q_-=(1/4,3/8,3/8).

Both are outside C, and the fixed-block KL repair sends both back to p. Theorem 3 fails, as it should: M=(1/2,−1/2,−1/2) has a connected incidence graph, so only scalar positive likelihoods preserve the entire affine family.

For two **fresh, conditionally independent** repetitions of this experiment, ordinary Bayes after ++ is

    B_(L_+⊙L_+)(p)=(9/10,1/20,1/20).

Repeated constrained updating U_(L_+)U_(L_+)(p) is still p. It also equals U_(L_+⊙L_+)(p): the composition test passes while all block information is discarded. These are independent modelled experiments, not two copies of one source report. Their product likelihood is justified by the declared conditional independence.

For an exact proper-score diagnostic, use half-Brier loss ℓ(j,q)=||e_j−q||²/2, whose posterior regret is ||Q−q||²/2. This is a scoring diagnostic; the constraint projection above remains KL. Each outcome's regret from reporting p instead of Q_± is

    (1/2)||Q_±−p||² = 3/64.

The prior Bayes risk is 5/16. The correct expected posterior risk is 17/64. The constrained procedure's expected risk remains 5/16. Its posterior implementation regret 3/64 exactly cancels the ordinary model-relative information gain 3/64. It does not worsen expected risk relative to this prior; it forfeits the available gain. No psychological, source-authentication, proper-function, or actual-warrant conclusion follows from that score.

This countermodel does **not** refute Jeffrey conditioning or feasibility-first governance. If independent replacement evidence warrants the fixed marginal w after the observation, P_C has the familiar Jeffrey interpretation. The operation then incorporates that extra replacement contract. Nor is a family of allowable **priors** automatically a family in which every posterior is obliged to remain. Whether C constrains priors, posterior reports, actions, or a revisable model must be specified rather than supplied by this mathematics.

## 7. The resulting implementation guard, and its exact boundary

For a separately justified probability representation, the check is:

1. State what C means and whether it is a current-report restriction or a model-wide invariant; keep action feasibility in its own type.
2. Retain the target/version, justified prior, source and acquisition records, joint or conditional channel, and applicable evidence-use permission. These are inherited obligations.
3. Compute the ordinary posterior for a defined positive-mass branch. At the current prior, check membership directly. For a claimed affine-family invariant, use Theorem 3 or its incidence-graph test on actual support.
4. If the posterior violates C, do not label a repaired output “the ordinary posterior under the unchanged channel.” Report a constraint/model incompatibility, or use a separately justified model revision, additional evidence operation, report restriction, or action-only constraint. The theorem does not choose among these responses.
5. Preserve what the numerical test cannot settle: source validity, normative authority, actual warrant, and action permission. Continue the governed whole-state reread without using numerical feasibility or score gain as a closure certificate.

Theorems 2–4 describe conditional numerical mechanisms. They do not show that noetic hard constraints are linear, probabilistic, time-invariant, or even representable inside one finite simplex. They do not imply that hard norms must be weakened, that evidence intake is always permissible, or that observed probability changes establish truth or restoration. This is a guarded mathematical interface, with the representation bridge itself still explicit.

## 8. Classical ancestry, provenance, and verification scope

- Normalized multiplicative changes are the familiar compositional perturbation operation. Aitchison and Ng, [*The role of perturbation in compositional data analysis* (2005)](https://journals.sagepub.com/doi/10.1191/1471082X05st091oa), identifies this operation and its group-structure setting. Reading scope here: publisher abstract, keywords, bibliographic references; no claim to have inspected its paywalled full text. Our orbit and face statements are proved directly.
- The pivot/free graph is the standard fundamental dependence graph of a represented matroid. Krogdahl, [*The dependence graph for bases in matroids* (1977)](https://www.sciencedirect.com/science/article/pii/0012365X77901182), explicitly studies that graph and extraction of matroid connected components. Reading scope: publisher-indexed abstract and bibliographic data; a direct page open failed. The diagonal-invariance proof is elementary and written in full above; neither it nor the graph is marketed as a field-new theorem.
- Jeffrey updating and minimum-relative-entropy updating predate this packet. Grünwald and Halpern, [*Updating Probabilities*, §§5.1–5.2](https://arxiv.org/pdf/cs/0306124), explicitly give the partition-weight replacement rule and its minimum-relative-entropy interpretation, with observation-protocol conditions kept separate. Reading scope: abstract, introduction, and those specified passages, not a full review of all their theorems. Their work already warns that a numerical update rule and an appropriate observation model are different requirements. Our fixed-channel countercontrol makes that familiar distinction concrete at this inherited repair interface.
- The original I-projection ancestry includes Csiszár, *I-Divergence Geometry of Probability Distributions and Minimization Problems* (1975), as cited in Grünwald–Halpern. The original full article was not inspected here; no exact theorem from it is imported as an unverified premise.

The principal questions, face-conjecture proof idea, affine criterion, and fixed-block channel countermodel were jointly developed with the parent during this task. This worker supplied the detailed proof, hypothesis checks, actual-support and current-prior controls, row-reduction construction, source comparison, and executable controls. These are author verification, **not independent review**; any independent review is a separate artifact.

`verify.py` records 10 exact control groups: a lower-support orbit and inverse; all 32,767 nonempty support families on four labels; rank/graph/vertex/inverse agreement for 756 likelihood instances across 28 feasible affine presentations; actual-support omission; a globally preserved informative model; symbolic block composition and scalar neutrality; the positive-channel information-erasure countermodel; single-prior versus family quantifiers; the legitimate first-step-only model; and zero-likelihood/inequality boundaries. Rational and symbolic checks supplement the written proofs; the finite enumeration does not prove the universal statements. `CHECK_RESULTS.json` and `verification.txt` contain the executed output.

Deliverables are confined to the separate scratch directory; protected inputs are unchanged. Input hashes and exact source paths are retained in `INPUT_BINDINGS.json`. No repository integration, source doctrine revision, independent-review label, or T20 closure is asserted.
