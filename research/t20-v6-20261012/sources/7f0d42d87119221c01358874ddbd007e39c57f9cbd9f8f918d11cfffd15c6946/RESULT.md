# Fixed-model inquiry value is not branchwise robust Bellman value

11 October 2026 UTC. Additive T20 application, ordinary proof and exact rational controls. No protected changes, integration, actual-warrant claim, kernel certification, or programme closure.

## Result

The inherited finite inquiry/control results remain sound. **Their extension to the new coupled credal audit family must preserve one model through the entire policy tree.** Merely retaining the exact posterior family at every observed branch does not make scalar robust Bellman recursion an optimizer for fixed-model expected loss.

The existing strictly positive segment L supplies the countermodel without changing its numerical source/audit laws. A declared audit-contingent report plan has fixed-model worst loss **11/20**, while maximizing its two conditional losses independently gives **3/4**. With the explicit reporting/defer menu below, the deterministic ex ante optimum is 11/20 and the randomized optimum is **21/40**; conditional minimax chooses defer at both branches, costing **3/5**. An audit price of 1/40 reverses inquiry-versus-skip between those contracts.

A separate, parent-supplied strictly positive family removes the reporting-menu restriction altogether: with either target label and private randomization allowed before and after inquiry, fixed-model audit risk is **3/10**, whereas rectangular audit risk is **1/3**. At audit price 9/50, the fixed-model optimum audits for **12/25 < 1/2** and rectangular planning skips. Section 3A gives the complete unrestricted control.

The faithful constructive repair is a finite set of **model-indexed policy-loss vectors**, combined coordinatewise across chance branches and scalarized only at the root. Finite-polytope vertices suffice when uncertainty is in initial joint laws under a common instrument. This is not a theorem that vertices of an uncertain transition-kernel polytope suffice when the same unknown kernel is reused.

This is a new-to-this-inspected-interface application of classical nonrectangular robust decision theory, not a claim of mathematical priority. The coupled-credal report already explicitly warns against model reselection and declines robust Bellman optimality. The present note executes the previously unperformed control mapping rather than accusing that warning, conditioning theorem, or earlier controller of being false.

## 1. Actual inherited owners and overlap

Input byte identities are in INPUT_BINDINGS.json. DEDUP_SCAN.json records a bounded scan of 238 current top-level result/report/theorem/addendum/repair files, excluding preservation/replay/review names. The actual owners were then read; the scan is not an exhaustive literature or project-priority proof.

1. **Warranted completion with proof-sensitive memory and inquiry cost**, `constructive-t20-20261009/sources/research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-research-20261009/RESULT.md`, §4, Theorem 2. Its finite Bellman recurrence minimizes worst *realized path cost* over persistent, order-independent, one-use tests and their consistent scenarios. It expressly excludes worst expected cost under private randomization. Its scenario belief B shrinks to B(a,o); a complete feasible response path remains consistent with at least one fixed scenario. That pathwise maximum is not the fixed-model expectation considered here. Replacing its max over outcomes by a model expectation changes the objective and needs a new argument.
2. **H-ICS v5**, §§self-revision/observation congruence/sure finite decision. These concern deterministic initial possibilities and observation-based lawful controllers, not numerical minimax expectations over a credal family.
3. **H-Continuation**, Theorem 2(c), source lines 257–273 in the pinned local copy. Every bounded adaptive policy's value is a sum of the appropriate branch-weighted observables; randomized policies add their common convex combinations. This is exactly the pointwise foundation needed by the repair below. Its model is fixed, and all declared cost/readout observables must be retained.
4. **Supplied cross-front synthesis D3a–D3b**, `received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/documents/CROSS_FRONT_SYNTHESIS.md`, §§4–5, and `research/contracts.py::finite_values`. These transport finite-history laws and known-kernel Bellman values through a common joint outcome/block quotient. D3b explicitly requires a fully observed contract or a separately justified information state. Code charges terminal loss at a state with no enabled action. It does not introduce model ambiguity or a prior on model identity.
5. **Posterior-inquiry-value**, already shows that preserving conditional answers without event probabilities does not preserve expected inquiry value. The present obstruction persists even though *every model has the same audit probabilities*. It concerns coupling of model-dependent losses across branches, not another missing-frequency counterexample.
6. **Coupled-credal audit REPORT**, §§2–4, already owns L, elementwise conditioning, vertex propagation, unnormalized response pairing, and the express prohibition on inferring robust Bellman optimality. **Audit-continuation RESULT**, §§2–3, already owns the common instrument and predictive quotient. **Credal geometric REPAIR** already owns modelwise nonlinear coordinate conjugacy with original predictive readout. Those results are preserved.

The general ancestry is established: Epstein–Schneider's author-hosted *Recursive Multiple-Priors* manuscript defines rectangularity by closure under combining branch marginals with independently selected conditional laws and links it to recursive evaluation. Its §4 discussion distinguishes the possible-model set from a rectangular enlargement used for preference recursion. Iyengar's publisher abstract states rectangularity as the premise for robust dynamic-programming counterparts. The exact primary-reading scope is recorded in SOURCES.md; no general rectangularity theorem is claimed here. [Epstein–Schneider](https://people.bu.edu/lepstein/files-research/rectang50.pdf), [Iyengar](https://pubsonline.informs.org/doi/10.1287/moor.1040.0129).

## 2. Three different contracts

Fix a finite horizon, lawful observation histories, common available actions at each such history, and a declared bounded loss. A policy uses its available history and permitted private randomness, never the unknown model identity.

**Fixed-model ex ante contract.** Nature chooses one complete model P in the stated family K, and it governs all branches and all times. For a policy π,

    J_K(π) = sup_{P in K} E_P[total loss under π],
    V_K = inf_{π in the declared policy class} J_K(π).

Choosing a single worst model after seeing the policy specification (including its randomization distribution) is allowed. Its private random realizations are not revealed before nature selects that fixed model. Choosing different models after seeing chance outcomes is a stronger operation unless those pasted laws already belong to K.

**Rectangular/adaptive contract.** Independent allowed conditional kernels can be selected at each history (and, when the contract permits it, after each selected action). Nested scalar worst-case recursion evaluates this historywise selection family. On a finite tree this also has a static description: each entire historywise selection determines one coherent path law. Its disadvantage for the present interpretation is not mathematical incoherence; it is that its path laws can lie outside the original family. Literal physical switching is not required for this enlarged-set interpretation.

**Conditioning-only contract.** After an actually observed history h, the family is updated elementwise to {P(·|h): P in K, P(h)>0}. This preserves conditional possibilities without assigning a distribution to model identities or prescribing an intertemporal preference rule. It does not answer whether to precommit to an ex ante optimal policy, to reoptimize conditional minimax at each history, or to change the allowed uncertainty set.

All three are well-defined. Confusing them changes the question being answered.

## 3. An exact control problem on the existing L segment

Use precisely the source report's cell order

    (P(Θ=1,A=1), P(Θ=0,A=1), P(Θ=1,A=0), P(Θ=0,A=0))

and its two vertices

    v0 = (1,9,9,21)/40,
    v1 = (9,1,21,9)/40,
    L = { (1−λ)v0 + λv1 : 0≤λ≤1 }.

Every joint cell is positive. Every model has P(A=1)=1/4 and P(A=0)=3/4. A reads one fixed audit bit; its projectors are idempotent and contradictory rereads are impossible. No repeated fresh source is invented.

### The decision/menu is an explicit new application premise

Before reading A, the available choices are:

- skip and defer, paying loss s=3/5;
- perform the audit, paying c=1/40, then use the following branch menu.

After A=1, choose between a risky report Θ=1, whose loss is its 0–1 error, and defer with constant loss s. After A=0, the risky report is Θ=0, with the same error loss, or defer. The risky label is prescribed by that branch's reporting option. The opposite label is **not** an additional available report in this contract. These are declared decision options, not assertions that such restrictions or prices are epistemically mandatory.

The restriction matters. Adding arbitrary free guesses would be a different optimization problem, and for this family its λ=1/2 law makes Θ independent of A and uniform. The present example does not claim valuable robust inquiry for that unrestricted symmetric guessing task. In particular, allowing both target reports and a private fair coin before the audit supplies a skip policy of worst loss 1/2, which beats this example's priced randomized inquiry loss 11/20. The executable controls verify that scope failure. Section 3A avoids this restriction in a separate family.

### Loss of the prescribed risky plan

The conditional risky-loss vectors, with coordinates (v0,v1), are

    A=1: (9/10, 1/10),
    A=0: (3/10, 7/10).

Choosing risky after either outcome has total expected-loss vector

    (1/4)(9/10,1/10) + (3/4)(3/10,7/10)
      = (9/20,11/20).

The expectation is affine in λ, so its maximum on L is 11/20. Branchwise maximization instead gives

    (1/4)(9/10) + (3/4)(7/10) = 3/4.

It uses v0's A=1 conditional and v1's A=0 conditional. The pasted joint law is

    v* = (1,9,21,9)/40.

This is positive and normalized, with the same audit frequencies. It is not in L: its first cell forces λ=0, whereas its third cell would require λ=1. Its risky-plan loss is exactly 3/4. Thus the scalar calculation is an exact evaluation over a strictly larger family, not a rounding or null-support effect.

### Deterministic optimum

Write R for risky and D for defer; order the pair by A=1 then A=0. The complete post-audit deterministic loss vectors are

    DD: (3/5, 3/5),
    RD: (27/40, 19/40),
    DR: (3/8, 27/40),
    RR: (9/20, 11/20).

The unique minimizing deterministic pair is RR, with maximum 11/20. In contrast, after either branch, the risky action's conditional maximum (9/10 or 7/10) exceeds 3/5, so conditional minimax selects D at both.

Including audit cost, fixed-model deterministic planning pays 23/40 by auditing, strictly below skip's 24/40. Rectangular planning prices audit-and-defer at 25/40, so skips at 24/40. This is a genuine inquiry-choice reversal under the declared menu.

### Randomization is a separate policy-class choice

Let x be the probability of risky at A=1 and y at A=0. Private coins are independent of the unknown model. The two expected losses are

    l0(x,y) = 3/5 + 3x/40 − 9y/40,
    l1(x,y) = 3/5 − x/8 + 3y/40,       0≤x,y≤1.

For every such policy,

    max(l0,l1) ≥ (l0+3l1)/4 = 3/5 − 3x/40 ≥ 21/40.

At x=1, y=2/3 both losses equal 21/40, proving the exact randomized optimum. This policy is also the ex ante mixture assigning weights 2/3 to RR and 1/3 to RD. Correlating branch coins cannot improve a one-audit problem: only the one realized branch's action marginal affects expected loss.

The rectangular post-audit criterion is

    3/5 + (3/40)x + (3/40)y,

whose minimum remains 3/5 at x=y=0. With audit cost, the randomized fixed-model root optimum is 22/40=11/20, still auditing, versus rectangular skip at 3/5. Mixing the skip plan with audit plans cannot improve 11/20: the same weighted-model lower bound is 11/20 on the optimal audit policy and 3/5 on skip, hence at least 11/20 on every mixture.

Randomization therefore strengthens rather than removes the separation. The inherited deterministic/pathwise optimizer should not be silently cited for this new randomized expected-loss optimum.

## 3A. A stronger control with both reports freely available

The parent supplied this second family after the L application was derived. It is a separate positive finite source/audit specification of the same interface, not a replacement of L's historical fixture:

    M = conv{ w0, w1 },
    w0 = (4,2,1,3)/10,       w1 = (3,1,2,4)/10.

Every cell is positive. Put wλ=(1−λ)w0+λw1. Every model has current target prior P(Θ=1)=1/2; audit masses range from 3/5 to 2/5. Both target reports are available before the audit and after either outcome; private randomization is allowed. Report loss is ordinary 0–1 error. No branch-report restriction or defer action is needed.

The conditional errors of the rule “report Θ=A” are

    e1(λ) = (2−λ)/(6−2λ),
    e0(λ) = (1+λ)/(4+2λ).

The first decreases from 1/3 to 1/4, while the second increases from 1/4 to 1/3. Both are strictly below 1/2, so the same classifier is individually Bayes optimal for every model, including against randomized classifiers. Its total error is

    wλ(Θ=0,A=1) + wλ(Θ=1,A=0) = 3/10.

Thus the ex ante robust audit risk is exactly 3/10 even with the full reporting menu and private randomization. Skipping has risk exactly 1/2, since the target marginal is uniformly 1/2 across the family.

At A=1 the worst conditional error is 1/3 at w0; at A=0 it is 1/3 at w1. Conditional minimax uses the same classifier but now values it at 1/3 on both branches, so rectangular audit risk is 1/3 independently of the chosen admissible audit marginal. Randomizing reports cannot improve these local minima because the recommended label has conditional probability greater than 1/2 throughout each branch family.

For an explicit coherent pasted witness use audit mass 1/2 and the two adverse conditionals:

    w* = (1/3,1/6,1/6,1/3).

It has target prior 1/2 and audit mass within the original range, but is outside M: every M-model has error 3/10, while w* has error 1/3. The failure therefore survives even a separate check of the current target prior and the audit-mass bounds. As before, the relevant problem is joint compatibility, not coherence of the enlarged law.

Any audit price c strictly between 1/6 and 1/5 gives a decision reversal. With c=9/50,

    fixed-model audit total = 3/10 + 9/50 = 12/25 < 1/2,
    rectangular audit total = 1/3 + 9/50 = 77/150 > 1/2.

The ex ante optimizer audits; rectangular planning skips using a private fair guess. The **full rectangular hull** has target priors ranging from 5/12 to 7/12; it does not preserve M's balanced target prior for every pasted law. A fair guess nevertheless has loss exactly 1/2 under every law, while the balanced pasted law w* lower-bounds every skip policy at 1/2 and every paid query policy at 77/150. These same lower bounds rule out an improving private mixture of skipping and querying. The fixed-model audit risks are all equal to 3/10, so a private query/skip mixture cannot improve the fixed-model minimum either. If private report randomization is disallowed, deterministic skipping under the full hull instead costs 7/12; the claimed rectangular skip value and inquiry-choice reversal in this unrestricted example explicitly use the permitted randomized policy class. This is a stronger unrestricted inquiry discriminator. It supplements, rather than obscures, the exact existing-L value calculation and its menu limit.

## 4. The exact one-split obstruction

For a compact model set, a fixed policy, common strictly positive branch probabilities p_o, and continuous conditional losses j_o(P),

    max_P Σ_o p_o j_o(P) ≤ Σ_o p_o max_P j_o(P).

**Equality holds if and only if all branch losses admit a common maximizing model.** Indeed, an attaining model gives nonnegative gaps max_Q j_o(Q)−j_o(P); their positively weighted sum is zero exactly when every gap is zero. Conversely a common maximizer attains equality.

For the risky plan on L, the maximizing parameter is λ=0 on A=1 and λ=1 on A=0. Their intersection is empty, so the inequality is strict. This criterion is for a fixed policy with common branch masses, not a necessary-and-sufficient rectangularity theorem for all instruments and all preferences. If masses vary with the model, masses and conditional responses must also remain paired.

It follows already that replacing each continuation vector by its scalar worst value is lossy. For example the A=1 conditional vectors for R and D are (9/10,1/10) and (3/5,3/5): neither componentwise dominates the other, although minimizing only their scalar maxima discards R. R is needed by the ex ante optimum.

## 5. Constructive faithful repair

### 5.1 What finite vertices cover

Let K=conv{v1,…,vm} be a finite polytope of initial nonnegative joint laws, with common finite nonnegative action/observation matrices M_(a,o), common lawful history-policy class, finite available terminal-decision menus, and declared state/history losses. All source versions and dependence required by the experiment are in those laws and operators. For every fixed finite policy π,

    E_(Σ_i λ_i vi)[L_π] = Σ_i λ_i E_vi[L_π].

For a deterministic tree this follows by summing its linear unnormalized branch losses; independent private randomization takes common convex combinations. Therefore

    J_K(π) = max_i J_i(π),       J_i(π)=E_vi[L_π].

An interior initial-law mixture needs no extra coordinate for this objective. No probability distribution on model identity is being inferred. The vector index records which complete initial model generated each component.

The statement also works for an explicitly finite list of complete models with their own kernels, by evaluating each coordinate under its own full model and using the same observation policy. But taking a convex hull of transition *matrices* and then reusing its selected matrix is a different parameterization: path expectations contain products of the same kernel parameter and need not be affine. No vertex reduction for that family follows.

### 5.2 An exact finite set-valued recursion

At a feasible public history h retain the entire indexed tuple

    r_i(h)=M_h vi,

without normalizing away each component's accumulated branch mass. Its next responses are r_i(hao)=M_(a,o)r_i(h). Let a terminal decision d have loss row ℓ_(h,d). Its loss vector is

    t^d(h) = ( ℓ_(h,d) r_i(h) )_(i=1,…,m).

Let an action's immediate cost row be c_(h,a); scalar action cost c means row c·1. Recursively define the finite attainable vector set S(h):

- include each permitted terminal vector t^d(h);
- for each permitted action a, and one choice z_o in S(hao) for each outcome o, include

      ( c_(h,a) r_i(h) + Σ_o (z_o)_i )_(i=1,…,m).

At the horizon only terminal vectors remain. If r_i(h)=0 for **every** model i, the history is globally impossible: define S(h) to be the singleton zero vector (equivalently omit that child from its parent's sum). Such an unreachable history need not supply a lawful terminal decision. If only some model components vanish, those components contribute zero while the live components still require a lawful continuation. No zero-mass branch is normalized. At a feasible history, if a terminal decision is required and no such decision is available, infeasibility must be represented explicitly; an empty set is not a free zero-cost stop. Actions and terminal decisions may not vary by hidden model index.

**Theorem.** S(h) is exactly the set of unnormalized future-loss vectors of deterministic lawful continuation policies from h. Consequently

    V_K^det = min_{z in S(empty)} max_i z_i.

**Proof.** Induct on remaining horizon. Terminal policies give exactly the displayed vectors. Every nonterminal deterministic policy chooses one common first action and one continuation for each observed outcome. Its expected unnormalized losses are the same-model sums in the formula, so its vector is generated. Conversely every generated vector supplies that first action and those child policies. No selection is made separately for different i. At the normalized initial laws the unnormalized loss is ordinary expected loss. The earlier affine identity proves the root maximum formula. ∎

Componentwise dominance is safe: a vector z with z_i≥w_i for every i can be replaced by the feasible w in any preceding nonnegative same-coordinate composition. Componentwise incomparable vectors cannot generally be removed by comparing scalar maxima, as §4 shows. Retaining all vectors is a constructive finite algorithm, not a polynomial complexity or minimum-memory claim.

If the contract permits a private random choice of a complete deterministic policy, with nature choosing the model before that choice is revealed, the attainable root set is conv S(empty). The exact robust program is the finite LP

    minimize t over α_π≥0, Σ_π α_π=1,
    subject to Σ_π α_π J_i(π) ≤ t for each i.

It can be implemented by selecting and retaining the sampled lawful policy. This formulation grants no ability to observe nature's index. Revealing the sampled whole policy before nature chooses a model is a different objective: in the L example, the displayed 2/3 RR plus 1/3 RD mixture would then cost (2/3)(11/20)+(1/3)(27/40)=71/120 before audit price, instead of 21/40. Private randomization timing is therefore material. The finite one-audit control explicitly realizes its optimum as an ordinary branch-randomized policy.

### 5.3 What is, and is not, cured

The construction solves the ex ante problem under its execution/commitment contract. It does not force a future decision maker who reoptimizes conditional minimax to follow the chosen continuation. In this very example conditional minimax after either audit value chooses defer. One must either retain the ex ante policy as the execution commitment, explicitly adopt a dynamically reoptimized objective, or justify a rectangular uncertainty specification. More state alone cannot make these different preferences identical.

A rectangular family is a legitimate alternative when its independently pasted conditionals belong to the declared uncertainty specification. Expanding L to obtain that property changes the source-model family and is not licensed by the original calibration bounds alone. Likewise, adding a prior over model identities gives a different Bayesian decision problem; no such prior has been supplied.

## 6. Transport through the existing cumulative and geometric interfaces

A common inherited predictive quotient E is sufficient if it preserves the actual branch masses, all relevant terminal/immediate loss rows, and lawful observation histories under every model, with the existing intertwining

    E M_(a,o) = T_(a,o) E.

Carry (E r_i(h)) with the same i through all branches. H-Continuation then preserves each J_i(π), and therefore preserves the entire policy-vector set, both root robust optima, and the lifted policy's value. Full two-way equality additionally requires the same lawful information-policy class; a one-way lift only gives the corresponding one-way guarantee. A target-only quotient does not automatically preserve unrelated costs or permission predicates.

The credal report's exact coupled-image construction supplies the appropriate representation rather than separate ranges. The additional demand for control is that different future branches still refer to compatible responses of the same initial model, and that each candidate *policy's* full loss profile is retained until aggregation. Tracking a posterior set correctly at each reached node does not authorize independently scalarizing hypothetical siblings.

The geometric REPAIR's invertible belief-coordinate map likewise transports each model's path law and loss readout when its inverse is used. For escort F(p), the predictive mass and loss are read from F^(-1)(q), not by interpreting q as the original law. This preserves the vector calculation; it does not remove the nonrectangularity or turn coordinate conjugacy into a new preference theorem. Our control checks use exponent 2 so both the encoded states and their exact rational inverse-ratio calculations can be checked without floating point.

## 7. Evidence and bounded consequence

Run, from the workspace parent:

    python3 coupled-credal-inquiry-transport-20261011/verify.py
    python3 -O coupled-credal-inquiry-transport-20261011/verify.py
    python3 coupled-credal-inquiry-transport-20261011/run_checks.py

The first two runs each execute 13,676 explicit checks that raise exceptions on failure. No correctness check uses Python assert. They verify the inherited fixture, all four deterministic policies, the exact rational LP and its dual lower bound, an inadmissible pasted law, the inquiry-choice reversal, a genuine 8-to-4-state predictive quotient, escort decoding and branch masses on every binary word through length 6, and set-valued recursion against separately enumerated loss-row evaluations of 669 fixed-depth policy trees whose stopping is permitted only at the horizon. That generic fixture has no globally zero-probability outcomes; zero branches are covered separately by the repeated-audit/escort controls. Small additional controls test the globally impossible-child singleton-zero rule, infeasible live histories with no terminal decision, and optional early stopping against direct policy enumeration. Twelve inherited inputs are rehashed unchanged. The additional unrestricted control checks its constant Bayes risk, branchwise extrema, a pasted law preserving the current target prior, all randomized two-label classifiers on an exact grid, and the priced inquiry reversal. Written proofs cover continuous mixture/randomization claims; finite grids corroborate them.

The runner also requires four deliberately false controls to fail: an active guard and the false fixed-equals-rectangular identity, each under ordinary and optimized Python. Successful controls and negative tests are author evidence, not independent review. A separate reviewer must bind the final bytes it actually checks.

The consequence for cumulative source revision is narrow and operational: an architecture that has correctly retained coupled source/audit models can also retain expected inquiry values, but must combine each fixed model's responses across the whole authorized policy. A scalar robust continuation value per branch silently adopts a different uncertainty/preference contract unless additional structure justifies it. This does not assess any actual source's calibration, choose human epistemic losses, establish cognitive basing or warrant, or require ordinary knowers to maintain a credal controller.

The L fixture and conditioning repair are inherited. The parent supplied a parallel two-model risky/safe discriminator, the vector-repair direction, and the stronger unrestricted M-family discriminator of §3A; this worker used the actual L segment, derived the exact deterministic/randomized menu application and one-split criterion, wrote the scoped recursion/transport proofs, and authored the controls. Parent and author overlap is collaborative development, not independent corroboration. No general novelty, sampling-complexity programme, protected change, integration, or closure is claimed.
