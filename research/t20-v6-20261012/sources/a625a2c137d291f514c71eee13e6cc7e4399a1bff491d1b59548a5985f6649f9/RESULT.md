# Constrained learning at a fixed finite prior

10 October 2026 UTC. Separate mathematical research packet. Written proofs and exact rational controls; no protected edit, integration, formal-kernel certification, actual-source validation, or programme closure. Root and worker are coauthors of the candidates and refinements; this packet is author verification, not independent review.

## 1. The constructive possibility boundary

Fix a current prior p in a convex set C of finite probability laws. An informative experiment whose every possible posterior stays in C exists mathematically **if and only if p is not an extreme point of C**. A binary channel strictly positive at every state already suffices. The exact set of individual posteriors attainable within such complete feasible experiments is the minimal face of C containing p; with strictly positive channels it is the part of that face having exactly p's support.

These are elementary consequences of the classical splitting lemma and finite convex geometry, not new general splitting or information-design theorems. Their useful role here is to complement the preceding **global** likelihood-invariance result: a family admitting only globally scalar channels can still allow informative experiments at its actual current prior. This gives a precise positive alternative to inferring universal impossibility from the stronger global test.

“Informative” here means that the posterior about the represented finite target X is not almost surely equal to p. It says nothing about learning concerning an unrepresented nuisance, a source, authority, or another target. A numerical prior and an abstract stochastic kernel are declared mathematical inputs; neither is thereby warranted as the actual world law or an available evidence source.

The theorem applies only when C is separately justified as a **convex probability feasible set**. It does not say that arbitrary noetic states, source records, authority judgements, or permissible actions form such a set. A prohibition on an action does not assign that action probability zero.

## 2. What is inherited and what is added

- `bayes-feasibility-compatibility-20261010/RESULT.md`, §§2–4, already proves the global finite-family classifier and affine incidence-component test. Its §4.2 already contains the exact fixed-mass positive channel reproduced in §6 below, including failure under a second unchanged observation. That example is reused and checked, not offered as a new discovery.
- `warranted-learning-20261009/RESULT.md`, §§6–8, already gives the posterior barycenter identity, model-relative score accounting, and source/provenance/permission boundaries. No score or warrant theorem is added here.
- `posterior-inquiry-value-20261010/RESULT.md` already shows why posterior answers alone do not preserve expected inquiry value. The proof-sensitive warranted-discrimination packet already supplies a finite permitted-test completion criterion and an optimum with acquisition and verification costs.
- The stochastic-exact-inquiry packet and its quotient-transport addendum already treat stronger exact-stopping objectives, hidden-state instruments, and lawful policy transfer. H-Continuation Theorem 2 already treats bounded adaptive branch-weighted values. The finite-tree observation in §7 does not replace or extend those results.
- The nearby measure-Bayes-face packet concerns universal preservation on infinite spaces. No infinite-dimensional or topological extension is claimed here.

The bounded inherited scan did not find the full fixed-prior/minimal-face formulation in these named reports. The increment is its explicit use at this constraint interface, including the positive-channel construction and exact reachability guard. This is not an exhaustive corpus or literature priority claim. Input identities and actual reading scopes are in `INPUT_BINDINGS.json`; external ancestry is in §9 and `SOURCES.json`.

## 3. Finite Bayes plausibility with a constraint

Let Δ_n={p∈R^n: p_i≥0, Σ_i p_i=1}, let C⊆Δ_n be convex, and fix p∈C. Put S=supp(p). A finite observation channel is a matrix K(y|i)≥0 with Σ_y K(y|i)=1 for every i. The target X is unchanged by observation. For each outcome with positive probability,

    α_y = Σ_i p_i K(y|i),       q_y(i) = p_i K(y|i)/α_y.

Call the experiment C-feasible at p when q_y∈C for every such outcome. Zero-probability outcomes have no posterior in this definition and are omitted. Labels may have identical posteriors.

**Proposition 1, classical finite splitting specialized to C.** A finite labelled list (α_y,q_y) is induced at p by some C-feasible channel if and only if

    α_y>0,   Σ_y α_y=1,   q_y∈C,   Σ_y α_y q_y=p.                 (1)

When (1) holds, a realizing channel on the actual prior support is

    K(y|i)=α_y q_y(i)/p_i,      i∈S.                              (2)

For i∉S, any stochastic column can be used, for example K(y|i)=α_y.

**Proof.** Bayes' formula gives α_y q_y(i)=p_i K(y|i), so summing over y gives (1). Conversely, (1) and nonnegativity imply q_y(i)=0 whenever p_i=0. For i∈S, (2) is nonnegative and its column sum is p_i/p_i=1; hence its entries are at most 1. Off-support columns do not affect the joint law p_i K(y|i). Direct substitution recovers exactly α_y and q_y. □

The splitting statement itself needs no convexity if all the displayed q_y are in the prescribed set. Convexity enters the two-point and face conclusions below. No closedness, compactness, full support, or relative-interior assumption on C is needed.

This is existence among arbitrary mathematical channels. If an actual channel or permitted menu has already been specified, its posteriors must be computed and checked; (2) does not manufacture a source with those conditional probabilities. For example, a menu containing only state-independent channels supplies no information about X even at a nonextreme p.

## 4. Exactly which individual posteriors can occur

Define

    F_C(p) = {q∈C : p=λq+(1−λ)r for some r∈C and 0<λ<1}.       (3)

This includes p, by taking r=p. A face of C means a convex subset F such that whenever a strict mixture of two points of C belongs to F, both endpoints belong to F. No topological closedness is included in this definition.

**Proposition 2.** The set (3) is the smallest face of C containing p. It is also exactly the set of posteriors occurring with positive probability in some finite C-feasible experiment at p.

**Proof of the face description.** Suppose q_1,q_2 satisfy (3). Decrease their witnessing coefficients to a common λ∈(0,1): if λ≤λ_j, then

    p=λq_j+(1−λ)r'_j,
    r'_j=[(λ_j−λ)q_j+(1−λ_j)r_j]/(1−λ) ∈ C.

Mixing these two identities proves convexity of F_C(p). If q∈F_C(p) and q=ta+(1−t)b with a,b∈C and 0<t<1, substituting into (3) writes p as a strict convex combination of a and a point of C. Thus a∈F_C(p); likewise b∈F_C(p). Hence F_C(p) is a face. Every face containing p must contain every q in (3), by its defining segment property, so this is the minimal face. □

**Proof of reachability.** Given a complete feasible experiment and one branch q of weight λ<1, the normalized mixture of all other posteriors is a point r∈C and gives (3). A weight-one branch has q=p. Conversely, any witness (3) is a two-outcome experiment by Proposition 1. The case q=p can use two identical posterior labels. □

Thus every positive-probability posterior of a **complete C-feasible experiment** lies in F_C(p), which in turn lies in the simplex support face Δ_S. Membership in C or even having the same support as p is not enough. This statement does not restrict a single favourable branch of an otherwise infeasible experiment.

For example, in Δ_2 take C={q:q_1≥1/2} and p=(1/2,1/2). The positive binary channel with rows (3/4,1/4) and (1/4,3/4) yields those same two posterior vectors with equal probability. The first is in C and has p's support; the second is outside C. Since p is an extreme point of this C, F_C(p)={p}; no informative complete feasible experiment exists there.

**Proposition 3, strictly positive individual reachability.** A q occurs in a C-feasible channel strictly positive at every state and outcome if and only if

    q∈F_C(p) and supp(q)=S.                                      (4)

For sufficiency two outcomes suffice. Choose a witness p=λ_0q+(1−λ_0)r_0 with 0<λ_0<1. For any 0<λ<λ_0, the residual

    r_λ=(p−λq)/(1−λ)
       =[(λ_0−λ)q+(1−λ_0)r_0]/(1−λ)

lies in C. Because q is positive on S and λ_0−λ>0, r_λ is positive on S too. Formula (2) gives two positive entries in each column on S, and positive arbitrary columns complete the off-support states. Necessity follows from Proposition 2 and positivity of each factor p_i K(y|i) exactly when p_i>0. □

General nonnegative channels can reach support-boundary points of F_C(p); strictly positive channels cannot. This is a support distinction within the fixed-prior feasibility question, not the preceding global classifier.

## 5. When a feasible informative experiment exists

**Corollary 4.** For convex C and p∈C, the following are equivalent:

1. Some finite C-feasible experiment at p is informative about X.
2. p is not an extreme point of C.
3. Some C-feasible informative binary channel is strictly positive at every state.

**Proof.** If an experiment is informative, select a posterior q≠p. Its weight is in (0,1), and the complementary posterior mixture r∈C gives p=λq+(1−λ)r with q≠r. Thus p is nonextreme.

Conversely write p=λa+(1−λ)b for distinct a,b∈C and 0<λ<1. Nonnegativity forces both endpoints to vanish off S. For any 0<ε<1 define

    a_ε=(1−ε)p+εa,       b_ε=(1−ε)p+εb.

They lie in C, remain distinct, have support S, and satisfy λa_ε+(1−λ)b_ε=p. Formula (2) therefore gives an informative binary channel positive on S; choose any positive binary columns off S. Its two entries in every column are strictly between 0 and 1. This proves (2)⇒(3), and (3)⇒(1) is immediate. □

The witness can be made arbitrarily close to uninformative by decreasing ε, without becoming exactly uninformative. This is only an existence statement, with no lower bound on useful information gain, no source-availability claim, and no optimization conclusion. At an extreme p, observations may still concern other represented records or unrepresented targets; only informative change of this X-posterior under the fixed C contract is ruled out.

## 6. The inherited fixed-mass example and a finite adaptive continuation

Reuse exactly the preceding packet's §4.2 model:

    C={q∈Δ_3:q_1=1/2},           p=(1/2,1/4,1/4),
    K(+|·)=(1/2,1/4,3/4),       K(−|·)=(1/2,3/4,1/4).

Both outcomes have probability 1/2, and

    q_+=(1/2,1/8,3/8),          q_−=(1/2,3/8,1/8).

They stay in C and are distinct. The homogenized constraint matrix is proportional to (1,−1,−1), so its pivot connects to both free coordinates. The inherited global component test therefore permits only scalar likelihoods. Neither actual row is scalar. For example the same + row sends the other feasible prior (1/2,1/2,0) to (2/3,1/3,0), outside C.

As already proved in the inherited packet, an unchanged fresh + repetition after q_+ gives (4/9,1/18,1/2), outside C. Actual-prior first-step success is not uniform or repeatable validity.

A **changed, explicitly history-conditioned** second channel demonstrates the finite-tree distinction. After +, use rows

    (1/2,1/4,7/12),             (1/2,3/4,5/12);

after −, use rows

    (1/2,5/12,3/4),             (1/2,7/12,1/4).

Each is a positive binary stochastic channel and each receipt has conditional probability 1/2. In receipt order, the four terminal posteriors are

    (1/2,1/16,7/16), (1/2,3/16,5/16),
    (1/2,5/16,3/16), (1/2,7/16,1/16).

Every terminal vector belongs to C, each occurs with probability 1/4, and their mean is p. These kernels are mathematical witnesses, not observed or available sources. This merely executes a two-stage application of splitting; no new adaptive-learning theorem is claimed.

## 7. What adaptation does and does not add

Keep the target X and feasible set C fixed. Consider a finite history tree under one declared passive observation model. At each positive-probability history h, the current posterior p_h and conditional next-outcome weights satisfy

    p_h = Σ_y α_(y|h) p_(hy).                                   (5)

This is the posterior martingale identity. A fully specified finite C-valued tree satisfying (5) can conversely be realized node by node by (2), filling off-support columns arbitrarily. Thus all constraints are checked at the current nodes. The generated minimal faces can only shrink along a feasible branch, because any face containing p_h contains each child posterior.

Flattening the finite tree into its terminal transcript gives one finite channel and a C-valued terminal posterior distribution with barycenter p. Conversely every such terminal distribution is realizable in one step. Indeed, for any finite tree whose terminal posteriors are in convex C, each internal posterior is their conditional convex mixture and is also in C. **With arbitrary mathematical channels available and no timing restrictions, finite adaptation adds no extra terminal posterior possibilities beyond Proposition 1.**

This is not equivalence of physical inquiry options: a flattened channel may not be available as a single action, and a restricted menu, changing access or permissions, acquisition costs, or timing can distinguish procedures. Any selection information must be included in the observed history and joint model. Selection depending only on recorded history and independent private randomization is harmless when modelled; an unmodelled state-dependent choice is an extra signal. The theorem does not justify multiplying copied evidence or replacing conditional likelihoods by marginal ones.

No infinite-horizon convergence, stopping-time, consistency, sampling-complexity or optimum result is asserted. If the target evolves under intervention, its current-state distributions are not automatically a martingale for one fixed X; use the separately justified instrument model, and preserve the initial target if that is the question.

## 8. The limited implementation consequence

If a separately warranted probability representation supplies convex C and current p, the useful checks are:

1. Distinguish a model-wide invariant from an all-outcome constraint at this p and from a favourable single posterior branch.
2. For an actual channel, compute every positive-probability posterior and test its membership in C. The global incidence test is stronger and should not reject an actually feasible local experiment merely because uniform preservation fails.
3. For abstract numerical possibility, use a convex decomposition of p in C. Nonextremality supplies a positive binary witness; the minimal-face criterion determines which proposed endpoint can participate.
4. Separately establish whether a matching channel exists, its likelihood model and provenance are warranted, and acquisition/use/reporting are permitted. A proposed stochastic matrix supplies none of these facts.

This helps distinguish a genuine numerical obstruction from an unresolved source or action question. It does not weaken hard norms, certify correct belief or noetic restoration, or optimize inquiry. Existing authority, evidence, proof, and whole-state rereading obligations remain in force.

## 9. Classical ancestry and verification

Kamenica and Gentzkow's [*Bayesian Persuasion* (2011)](https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf), §I.B, Proposition 1 and its Appendix proof, explicitly give the posterior-mean condition and the construction π(s|ω)=μ_s(ω)τ(μ_s)/μ_0(ω). Their setup assumes a full-support prior; restricting to S handles the zero-prior coordinates here. Their introduction, p. 2593, credits earlier use of the expectation restriction and identifies Aumann and Maschler's repeated-games work. The mathematical construction is classical; the present direct proof specializes it to this fixed-prior constraint contract.

Arieli, Babichenko, Sandomirskiy and Tamuz's [*Feasible Joint Posterior Beliefs* (2020)](https://tamuz.caltech.edu/papers/feasible.pdf), introduction and §2, names the one-agent result the Splitting Lemma and attributes its ancestry to Blackwell (1951) and Aumann–Maschler (1995). Only those passages and front matter were inspected; their multi-agent theorems are not imported. The [MIT Press record](https://mitpress.mit.edu/9780262526265/repeated-games-with-incomplete-information/) confirms *Repeated Games with Incomplete Information* (1995). The original book's lemma text was not inspected, so no unverified original theorem number or quotation is claimed.

Posterior constraints themselves are also established literature. Babichenko, Talgam-Cohen and Zabarnyi's [*Bayesian Persuasion under Ex Ante and Ex Post Constraints* (2021 version)](https://arxiv.org/pdf/2012.03272v2), §§2.1–2.2, combines Bayes plausibility with constraints imposed on each admissible posterior. The present note imports no optimization, approximation, strategic-persuasion or complexity result from that paper. Its scope is the elementary fixed-prior possibility boundary and its application to the preceding global rigidity result.

`verify.py` uses exact `fractions.Fraction` arithmetic for twelve control groups: inherited local feasibility; global/repetition failure; two-stage adaptive flattening; asymmetric shrinking and off-support filling; strict individual reachability; single-branch versus complete-experiment feasibility; support-boundary reachability; nineteen open-segment priors; noninformative signals at an extreme prior; the need for convexity in the two-point reduction; an uninformative available-menu control; and unchanged input hashes. `CHECK_RESULTS.json` and `verification.txt` contain the executed results. The checks corroborate the displayed proofs and are not enumeration-based proofs of universal claims.

All writes are confined to this separate packet. No review authority, protected edit, release or closure is claimed.
