# Coherence repair, likelihood semantics, and evidence-bearing correction

9 October 2026 UTC. Scratch-only T20 continuation. No protected source, implementation, release, or closure claim is changed. This packet gives written general proofs, exact finite controls, and an explicitly bounded source crosswalk. It does not identify actual noetic states, establish an actual prior or likelihood, or prove proper function, human uptake, revelation, or divine warrant.

## 1. Result and actual predecessor difference

A coherence repair can improve its input under every possible truth state and nevertheless make an evidence update strictly worse. The missing link is a representation-compatible action of the already specified Bayesian evidence channel across the Bregman coherence-repair interface. The project already has likelihood semantics; the issue here is whether this numerical repair can implement them faithfully.

Two distinct implementation contracts select two different classes of separable Bregman repairs:

1. **Order compatibility:** multiplying likelihood weights before or after repairing the input gives the same repaired result. Even the restricted test using subprobability inputs and attenuation of just one coordinate characterizes coordinatewise weighted negative entropy, f_i''(t)=α_i/t, with arbitrary α_i>0.
2. **Uninformative-evidence neutrality:** multiplying all coordinates by the same positive scalar does not change the repaired belief. This stronger semantic requirement characterizes a single common entropy weight, f_i''(t)=c/t, for every n≥2. It makes repair ordinary normalization and therefore realizes the ordinary finite Bayes action.

The binary case has no exceptional family for these contracts. The characterization is of the particular implementation “multiply likelihood weights, then apply this Bregman repair.” It does not say that other strictly proper scores are illegitimate, or that they cannot evaluate ordinary Bayesian learning.

The earlier Hessian repair supplied by the parent has dual-shift endpoint P_F and equal statewise loss reductions. That is the mathematical input. The present difference is an exact compositional and semantic condition on evidence intake, together with a valid finite experiment separating statewise repair improvement from epistemic learning. The general expected-learning and Bregman-regret identities used below are classical algebra, not novelty claims.

The pinned-source comparison is substantive:

- Deep AX V2, `PMR-007_DEEP_ROUND_AX_SOURCE_TESTIMONY_LIKELIHOOD_AND_WORLD_GATE_V2.md`, §§2–5, already supplies joint Bayesian likelihood updates, factorization only under conditional independence, exact-duplicate invariance, and an authority-separated source/world gate. Its §8 expressly separates posterior change from proper function and restoration. Those are inherited prerequisites, not missing project machinery or new results here. The new question is compatibility of that existing likelihood action with the separable Bregman-repair interface.

- Orthemology, `applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md`, leaves literal G2 geometry conditional. Its proposed G1 correction keeps hard constraints, provenance, uncertainty, and whole-state rereading separate from ranking. It supplies no probability law or likelihood action.
- `SEMANTIC-OPERATOR-CONTRACT.yaml` makes route, transition, and closure operators non-factive. Admissibility does not entail strict soundness. This packet adds a conditional numerical sub-operation; it does not reinterpret those runtime operators as physical gradients.
- DAEE, `docs/algebraic-notation-and-noetic-formalism.md`, bounds gradient/divergence/curl and keeps statistical signal properties separate from fiṭrah, revelation, and sound reason. `M2-prior-probability.md` treats a prior as requiring its own grounds. `sound-reason-epistemology.md` identifies proper function and truth-directed faculty/environment conditions, not a posterior normalization criterion.
- H-ICS v5 already proves observation/update congruence and distinguishes immediate access from reachable inquiry. It says reconstruction can enable new observations but does not generate warrant by self-endorsement. It does not contain this likelihood/Bregman classification.
- The current CP23 warranted-discrimination result already has typed authenticated evidence inventories, conditional proof soundness, and residual certificate frontiers. Its probabilities can remain identical while warrant-control inventories differ. This packet does not replace those certificate frontiers with entropy or rediscover that truth and warranted issuance differ.
- CP12's finite-geometric score is a calibrated testing construction for endpoint/skyline observations. Its score is not a Bregman belief-repair operator, and it has no repair–likelihood commutation law.

These inspected sources establish a bounded difference from the relevant retained work. They are not an exhaustive field-wide priority search or a claim of general mathematical originality. Exact source URLs, Git blob identifiers, and retained bytes are in `sources/SOURCE_BINDINGS.json`.

## 2. Mathematical contract

Fix n≥2. Let U=(0,1)^n, Δ={p∈[0,1]^n:Σ_i p_i=1}, and Δ° its strictly positive part. For each i let f_i be finite and continuous on [0,1], twice continuously differentiable on (0,1), with f_i''>0. Put F(b)=Σ_i f_i(b_i), and for b∈U, p∈Δ define

D_F(p,b)=F(p)−F(b)−∇F(b)·(p−b).

The repair is

P_F(b)=argmin_{p∈Δ}D_F(p,b).

Continuity on compact Δ gives existence; strict convexity gives uniqueness. For p∈Δ°, P_F(p)=p. We never assume every generic repair is interior. If a particular composite expression P_F(L⊙P_F(b)) is used, its second input must belong to U. Here ⊙ is componentwise multiplication, and N(b)=b/(Σ_i b_i).

### Lemma 1: subprobability repair is interior

If b∈U and Σ_i b_i<1, then P_F(b)_i>b_i for every i.

Proof. Write g_i(t)=f_i(t)−f_i'(b_i)t. Each g_i is strictly convex and minimized at b_i. Let p=P_F(b). If p_i≤b_i for some i, the sum constraint gives another j with p_j>b_j. Transfer a sufficiently small positive amount from coordinate j to coordinate i. For p_i<b_i, g_i decreases (including at zero, by convex secant inequalities). For p_i=b_i, its increase is o(ε), since b_i is interior and g_i'(b_i)=0. The decrease in g_j is bounded below by a positive multiple of ε. If p_j=1, the same bound follows from secants at a fixed interior point between b_j and 1, without assuming differentiability at 1. The total objective decreases, a contradiction. Thus p_i>b_i>0 for all i; n≥2 then implies p_i<1. □

Whenever p=P_F(b) is interior, its exact characterization is

f_i'(p_i)−f_i'(b_i)=λ for every i.                                             (1)

Sufficiency of (1) follows from strict convexity and the simplex constraint. This is a first-argument Bregman projection; reversing the divergence would change the problem.

## 3. Weak composition selects weighted entropy

For a coordinate k and 0<a<1, let L have L_k=a and L_i=1 for i≠k. Consider the restricted order-compatibility condition

P_F(L⊙P_F(b))=P_F(L⊙b)                                                      (W)

for every b∈U with Σ_i b_i<1, every k, and every such a. All three repair inputs in (W) are interior and all multiplied inputs are subprobabilities. No large or negative “likelihood” is used.

### Theorem 2

Condition (W) holds if and only if, for each coordinate i,

f_i(t)=α_i t log t+β_i t+γ_i,    α_i>0.                                      (2)

The α_i need not agree. For this class the same composition law holds for arbitrary positive L whenever its displayed arguments belong to U.

Proof of necessity. Fix a subprobability b and p=P_F(b). Because f_i''(b_i)>0, for t in a small interval around zero define a local curve by

f_i'(b_i(t))=f_i'(b_i)+t,    b_i(0)=b_i.

All b(t) remain in U with sum less than 1, and b_i'(0)=1/f_i''(b_i). Equation (1) shows P_F(b(t))=p: its common multiplier simply changes from λ to λ−t. With a fixed coordinate attenuation L, (W) now says q=P_F(L⊙b(t))=P_F(L⊙p) is independent of t. Lemma 1 makes q interior.

Subtract the two KKT equations for indices i,j at q, and differentiate at t=0. The terms at q are constant, so

L_i f_i''(L_i b_i)/f_i''(b_i)=L_j f_j''(L_j b_j)/f_j''(b_j).                  (3)

Choose i=k and j≠k. The right side is 1. Hence a f_k''(a b_k)=f_k''(b_k). Any x∈(0,1) can be b_k in a subprobability vector by making the other coordinates sufficiently small. For every 0<u<x<1, set a=u/x to conclude

u f_k''(u)=x f_k''(x).

Thus t f_k''(t)=α_k>0 on the entire interval. Twice integrating proves (2); continuity supplies the endpoint values with 0 log 0=0.

Proof of sufficiency. Affine terms cancel from the divergence. For (2) the minimizer is interior and uniquely given by

P_F(b)_i=b_i exp(λ(b)/α_i),

where Σ_i b_i exp(λ/α_i)=1. The left side is strictly increasing from 0 to infinity, so λ exists uniquely. If p=P_F(b), then

f_i'(L_i p_i)−f_i'(L_i b_i)=λ(b)

for all i. The inputs L⊙p and L⊙b therefore lie on the same dual-shift fibre and have the same simplex projection. Equivalently, their two successive normalizing multipliers add. This proves (W) wherever the products are in U. □

The result uses C² regularity only in the open interval. It neither assumes C³ regularity nor differentiates f_i''.

### Why the weak contract is genuinely weaker

Take α=(1,2), coherent p=(1/2,1/2), and common attenuation c=1/2. Formula (2) gives

P_F(c p)=((9−√17)/8,(√17−1)/8),

which differs from p. Yet the weak composition law holds for every admissible positive L. The repair can compose its own weight action perfectly while interpreting an uninformative observation incorrectly.

## 4. Neutral evidence selects common entropy and ordinary Bayes

Require only the scalar-neutrality condition

P_F(c b)=P_F(b),    b∈U, 0<c≤1.                                           (N)

The restricted values c≤1 already include genuine possible likelihoods of an observation independent of the state.

### Theorem 3

The following are equivalent:

(a) Scalar neutrality (N).
(b) P_F(b)=N(b) for every b∈U.
(c) f_i(t)=c₀ t log t+β_i t+γ_i with one common c₀>0.
(d) Strong likelihood equivariance:

P_F(L⊙b)=B_L(P_F(b)),    B_L(p)=N(L⊙p),                                   (B)

for all b∈U and positive L with L⊙b∈U.

Proof. (a)⇒(b): put z=Σ_i b_i and p=N(b)∈Δ°. If z≥1, scale b down by 1/z. If z<1, scale p down by z. In both cases (N) and P_F(p)=p give P_F(b)=p. Consequently every such projection is interior; this is derived, not assumed.

(b)⇒(c): fix any b∈U, and let p=N(b). For s in an open interval around 1 with sb∈U, property (b) gives P_F(sb)=p. Subtract the i,j KKT equations for this fixed p and differentiate in s at 1:

b_i f_i''(b_i)=b_j f_j''(b_j).                                            (4)

The coordinates b_i and b_j vary independently through (0,1). Because n≥2, equation (4) forces every function t f_i''(t) to equal the same positive constant c₀. Integrate as above.

(c)⇒(b) is the common-weight case of the projection formula in Theorem 2. (b)⇒(d) is N(L⊙b)=N(L⊙N(b)). Finally, (d)⇒(a) uses L=c·1 and B_L(p)=p. □

There is also an elementary, metric-independent reason (d) forces normalization: any retraction P from U onto Δ° satisfying (B), applied to coherent p and L_i=b_i/p_i, obeys P(b)=N(b). The separable curvature theorem then determines which Bregman generators can realize that retraction.

No claim here invalidates quadratic or other proper scoring rules. For any such score one can first calculate the ordinary Bayesian posterior from a justified channel and evaluate it with that score. The characterization restricts using that score's Bregman projection itself as the implementation of likelihood normalization.

### Corollary 4: null observations on coherent beliefs already suffice

The apparently weaker requirement P_F(c p)=p for every p∈Δ° and 0<c<1 is also equivalent to common entropy. Thus the characterization can be motivated entirely by genuine uninformative observations on already coherent priors.

Proof. For fixed p, differentiate the KKT pair differences along c p. It follows that x f_i''(x)=y f_j''(y) for arbitrary different i,j and x,y>0 with x+y<1: choose a subprobability vector with those coordinates and represent it as c p. To compare any two values x,x' of the same coordinate function, choose y>0 smaller than both 1−x and 1−x', and use another coordinate j. Both values then equal y f_j''(y). This makes each coordinate function constant and makes the constants agree. The argument works for n=2; for n>2 choose the remaining coordinates small enough. The converse follows from normalization. □

Consequently, if F is outside the common-entropy class, there are coherent p and 0<c<1 for which P_F(c p)≠p. A two-outcome channel independent of X with probabilities c and 1−c then produces strictly positive expected posterior regret:

c D_F(p,P_F(c p))+(1−c)D_F(p,P_F((1−c)p))>0.

Both output reports are interior by Lemma 1, so their losses are well-defined under the stated hypotheses. The first term is strictly positive. This is a general adversarial null-experiment diagnostic for the specified multiply-then-repair implementation, not an empirical claim.

## 5. A real finite channel defeats the naive composition

Use n=2, F(b)=(b₁²+b₂²)/2, and coherent prior p=(3/4,1/4). Let X have this declared law. Observe Y∈{0,1}, independent of X with P(Y=0)=P(Y=1)=1/2. Each outcome therefore has a genuine likelihood vector L_y=(1/2,1/2). The ordinary posterior remains p after either outcome.

The naive rule “multiply, then use quadratic repair” instead yields

b=L_y⊙p=(3/8,1/8),    q=P_F(b)=(5/8,3/8).

With loss D_F(e_j,q)=||e_j−q||²/2, exact arithmetic gives

E_p D_F(e_X,p)=3/16,
E_p D_F(e_X,q)=13/64,
excess expected loss=1/64.

At the same time, for each j∈{1,2},

D_F(e_j,b)−D_F(e_j,q)=1/16=D_F(q,b).

Thus the repair is a uniform statewise improvement relative to the raw vector b, while the whole evidence operation worsens expected predictive performance relative to the prior. Repair changed the object being scored: the raw likelihood-weighted vector had already been introduced by an incompatible evidence implementation. This is the precise gap between all-state coherence safety and evidence-acquiring correction.

This is a synthetic, completely specified two-state experiment. It makes no empirical or psychological claim.

## 6. Exact accounting of repair, learning, and implementation error

The following identities are standard Bregman/proper-scoring algebra. They make the new compatibility requirement operationally discriminating.

Define R_F(r,s)=Σ_j r_j D_F(e_j,s), and H_F(r)=R_F(r,r). For r,s∈Δ°,

R_F(r,s)=H_F(r)+D_F(r,s).                                                  (5)

Now declare a finite evidence channel K(y|j), a coherent prior p∈Δ°, and restrict attention to positive-probability outcomes with interior posterior Q_y. Let m_y=Σ_j p_j K(y|j), Q_yj=p_j K(y|j)/m_y. These are model commitments whose application must be established separately. They imply Σ_y m_y Q_y=p and

H_F(p)−Σ_y m_y H_F(Q_y)=Σ_y m_y D_F(Q_y,p).                               (6)

For an implementation producing any interior report q_y, combine (5)–(6):

R_F(p,p)−Σ_y m_y R_F(Q_y,q_y)
 = Σ_y m_y D_F(Q_y,p)−Σ_y m_y D_F(Q_y,q_y).                                (7)

The first term is genuine model-relative information gain. The second is posterior implementation regret. An uninformative experiment has the first term zero, so any changed report strictly worsens expected score under strict convexity. Entropy repair removes this implementation regret for the ordinary likelihood-multiplication mechanism; it does not verify the channel.

Finally let p=P_F(b) be interior and suppose p is also the independently declared prior for X. The three-point Bregman identity and (1) give, for every truth state j,

D_F(e_j,b)=D_F(e_j,p)+D_F(p,b).

Hence the complete expected difference from the raw report b is

R_F(p,b)−Σ_y m_y R_F(Q_y,q_y)
 = D_F(p,b)+Σ_y m_y D_F(Q_y,p)−Σ_y m_y D_F(Q_y,q_y).                        (8)

Equation (8) prevents crediting a large coherence repair as evidence gain. It also explicitly exposes the required bridge premise: the repaired numerical vector is being used as the declared prior. The geometry does not establish that premise. Under misspecified priors or channels, the model-relative gain is not automatically improvement under the actual world law.

## 7. Inherited provenance condition: a necessary sanity control

Deep AX V2 §§2–5 already proves the joint-likelihood, conditional-independence, and duplicate-invariance claims in this section. They are repeated here only as an inherited sanity control on the new interface. The numerical compatibility theorem does not supersede that constraint. Entropy normalization can implement a badly specified likelihood perfectly.

Take equal prior on two states and a single root signal Z with

P(Z=+|X=1)=4/5,    P(Z=+|X=2)=1/5.

Observe two exact copies Y₁=Z, Y₂=Z. On the positive result the true joint likelihood is (4/5,1/5), and the correct posterior is (4/5,1/5). After Y₁=+, the second copy has conditional likelihood (1,1): it provides no further information. Multiplying the same marginal vector twice instead yields (16/17,1/17). The second multiplication fabricates discrimination even though normalization and the algebraic composition law both hold.

For passive observations of a fixed X, use either an independently justified joint channel or sequential conditional likelihoods

K(y₁,y₂|j)=K(y₁|j)K(y₂|j,y₁).

The chain rule does not require independence. Replacing the second conditional factor with its marginal requires the appropriate conditional-independence premise. For observations that can be reordered without changing their meaning or acquisition mechanism, the two chain factorizations of the same joint channel agree. For interventions that change the target or available measurement, this passive-channel model cannot simply be imposed; a justified transition/instrument model is required, as the inherited operative-access results already warn.

A practical source-faithful admissibility gate therefore asks for the target/version, evidence content and acquisition event, origin or shared-root links, scope and authentication status, the channel or conditional-likelihood model, and authority to acquire/use the evidence. Those obligations remain separate from the posterior vector. A copied item is not treated as independent merely because it has a distinct record ID. Conversely, distinct origins alone do not prove conditional independence; shared causes may remain.

This is a precise probabilistic reason why the retained source/provenance inventory cannot be discarded when numerical beliefs happen to agree. It is not a numerical tawātur threshold and not a warrant verdict.

## 8. Operative-warrant boundary and useful next operation

The source-faithful operation is:

1. Retain the actual finite target alternatives and their meaning/version; do not identify them with a person's hidden noetic state by stipulation.
2. Establish whether a probability model and source-conditioned observation channel are justified for this task. If they are not, hold that numerical update rather than invent a prior or likelihood.
3. Check the action's access, authority, provenance, and relevant source commitments using the existing episode and evidence records.
4. If the implementation multiplies likelihood weights then repairs, test the repair's scalar-neutrality and composition contracts. Common entropy implements ordinary Bayes in the declared finite model; weighted entropy alone provides only algebraic order compatibility.
5. Compute and distinguish coherence credit, information gain, and implementation regret using the appropriate conditional model. Preserve the evidence records and unresolved obligations.
6. Carry the result into the governed whole-state reread. No numerical score gain discharges unproved source reliability, semantic bridges, proper-function premises, or claim-relative truth linkage.

This is a conditional constructive bridge between the established Hessian geometry and an evidence-bearing correction. Its concrete achievement is a testable implementation contract with a sharp classification and a countermodel. It does not establish actual noetic restoration, theorem-to-runtime completeness, or T20 closure.

## 9. Verification and attribution

- The parent supplied the strong-neutrality characterization and the independent-channel quadratic countermodel.
- This worker developed the restricted weak-composition classification, the interiority lemma, the source comparison, and the explicit information-minus-regret interface crosswalk; the provenance/Bayes conditions are inherited from Deep AX V2; the parent independently supplied a related differential-kernel proof of the weak classification.
- The independent reviewer checked the proof sketches, including the endpoint-safe interiority lemma and the n=2 case; the final document is to receive a separate document-level read.
- `verify.py` checks exact rational finite examples and identities; numerical weighted-entropy checks are diagnostics only. No finite test proves the universal classification.
- No formal proof-assistant/kernel certification, empirical experiment, protected integration, or field-wide originality is claimed.
