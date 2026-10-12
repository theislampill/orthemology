# Epistemic tuples and equilibrium as a typed restoration test domain

## Research disposition and source identity

This is an isolated research return for P14-ET01–ET08, not a repository change or a canonical theorem admission. The supplied P14 packet is explicitly `SEALED_HANDOFF_ONLY`, with `research_executed=false`; its main basis is `03e2604dfcef278b01c60d19b05370fcec4194b6`. The 18-page source PDF has SHA-256 `d39f084222fe3b372b365a729b1cd3e4ab6c09c389efaeb18d7727d4b845aba5`.

**Substantive research verdict:** the PDF supplies a useful applied theorem and countermodel domain once several claims are repaired. Scalar information loss, order distortion, local implementability, equilibrium existence, and temporal restoration are distinct and can be tested in the same explicitly typed model. General mathematical novelty is not claimed. The empirical cognitive decomposition, normative correctness of any coordinate or utility, and any historical/religious conclusion remain unestablished.

The strongest result is a conditional integration, not a new Nash theorem: a finite multi-locus evidentiary architecture admits exact tests for which distinctions and licenses a representation preserves; its vector equilibria can be characterized without endorsing a unique weight vector; and deployment requires a separate joint-law and temporal-control contract.

The cone is written `C_order` or `C_i`, never the repository's trusted-calculus symbol `K`.

## 1. ET01 scalarisation has three independent questions

Let `(E,≤_E)` be a partially ordered evidence-profile space. Its coordinates, units, orientation and epistemic interpretation are supplied assumptions. A coordinate named “provenance quality” is already an evaluated coordinate unless its descriptive/normative construction is separately specified. Let `f:E→R` be a score, and let `g:E→T` be a particular target judgment.

- **Injectivity:** distinct profiles have distinct scores
- **Monotonicity:** `x≤_E y` implies `f(x)≤f(y)`
- **Order reflection:** `f(x)≤f(y)` implies `x≤_E y`
- **Target sufficiency:** some `ĝ:f(E)→T` satisfies `g=ĝ∘f`

These properties are not interchangeable.

### Proposition ET01-A finite order embedding

For a finite nonempty poset E, an order-preserving and order-reflecting map into R exists exactly when E is a chain.

**Proof.** If such a map exists, the real images of any x,y are comparable; reflection makes x,y comparable. Conversely, enumerate a finite chain in increasing order and assign increasing integer ranks. ∎

In fact reflection alone already forces comparability, and antisymmetry makes it injective. For infinite total orders, totality alone does not guarantee real embeddability; that extra representation issue is not discharged by this finite theorem.

### Proposition ET01-B exact target sufficiency

`g=ĝ∘f` for a function on `f(E)` exactly when g is constant on every f-fibre. If a fibre contains x,y with different target judgments, no decoder of that score can recover the target at both. Conversely assign each attained score its common target value. Extending the decoder to all real numbers additionally requires a value in T whenever there are unattained scores.

This is an application of the already inspected fibre-factorization core, not a newly originated theorem. It concerns one declared target. A likelihood-ratio score for a fixed binary question, for example, can be sufficient for that question without embedding a multidimensional evidence order.

### Countermodels and positive controls

1. `E={(1,0),(0,1)}`, Pareto order, `f(x)=x₁+x₂`: the score collapses two profiles. It loses the first-coordinate target, but perfectly retains the sum target
2. On the same E, `f(x)=x₁+2x₂` is injective and monotone, but fails order reflection. It creates a numerical comparison between incomparable profiles without losing their identities
3. On `E={(0,0),(1,1),(2,2)}`, the first coordinate is an order embedding. Not every scalar is lossy or normatively suspect
4. An arbitrary injective encoding of a finite profile set into R preserves every set-theoretic target, even when its numeric order is unrelated to the profile order. This is not a meaningful scalar utility until its comparison semantics are supplied

### Proposition ET01-C positive-weight ranking reversal

For x,y∈R^k and the freely variable strictly positive normalized weights `w_j>0`, `Σw_j=1`, both strict score rankings `w·x>w·y` and `v·x<v·y` are possible exactly when x−y has at least one positive and one negative coordinate.

**Proof.** A sign-uniform difference cannot reverse against positive weights. If coordinates of both signs occur, put almost all mass on a positive coordinate for the first ranking and almost all mass on a negative coordinate for the second; sufficiently small positive mass on the remaining coordinates preserves strictness. ∎

A bounded or otherwise constrained weight class may prevent reversal. Its actual extrema, not the unrestricted theorem, decide that case. A positive weighted sum respects nonzero Pareto improvement; it does not in general reflect Pareto order or establish that compensations between dimensions are legitimate.

### Exact relationship to CV-R and T03

To instantiate observation factorization, supply a probability space, an evidence observation `Y:Ω→E`, and a measurable scalar `f`. Then `Y_score=f∘Y` is a **coarsening** of Y. Reversing the names does not make a score a refinement. CV-R additionally specifies pushforward laws, measurable singleton events, its full measurable event repertoire, and coherent factorization; its defect is positive-singleton mass loss, not discarded coordinates, ranking distortion, Shannon information, or target error.

In particular, on a finite evidence carrier both the full tuple and any finite score have CV-R defect zero, even when a score collapses the target. Therefore zero CV-R debt cannot certify P14 target sufficiency. The application may reuse the factorization interface while requiring a separate target/order certificate. T03/V4-Q1 retain their actual source scope and ordinary, non-kernel-checked status.

## 2. ET02 common admission does not provide a common ordering or license

Define an application context C by an inquiry identifier, coordinate schema and units, accepted versions, applicability conditions, and a declared joint-compatibility predicate. A record contains its context/schema/version, profile, and provenance information. Define

`Adm_C(e)` iff its schema, version, inquiry and applicability checks pass,

and

`Cong_C(e,f)` iff `Adm_C(e) ∧ Adm_C(f) ∧ Comp_C(e,f)`.

The checks must be stated for the intended application. For a minimal nonvacuous fixture, only records for inquiry q, schema `(provenance-resistance, semantic-coverage)` with the declared units, and version 1 are admitted; a record from another inquiry or schema is excluded. Compatibility permits both admissible profiles while retaining any recorded source dependence instead of treating it as independence.

Two admitted records with profiles `(1,0)` and `(0,1)` are distinct and incomparable. Nothing in admission chooses a compensating weight or a unique preferred response. To distinguish namespaces, the same records can be admitted to analysis while the operational action menu is empty because the recipient has no execution license. Similarly, two admitted model alternatives can require different repairs with no common safe action. Thus common comparison is compatible with failure of common controllability.

The positive bridge to an operational or analysis-relative context must explicitly map schema/version/inquiry checks and separately prove preservation of the relevant license or admissibility judgment. The repository's `Adm_Γ`, executable license record, and this application's `Adm_C` are not synonyms.

## 3. ET03 endogenous loci add information constraints rather than irreducible magic

A finite architecture consists of an evidence state e, local states `l_i∈L_i`, local observation maps `o_i`, response sets `A_i`, explicit communication/dependency channels, and a global transition relation on `(e,l₁,…,l_n,c)`. Each locus's response must factor through its available local history. Shared latent source variables and randomness are represented explicitly; absence of a direct message edge does not prove statistical independence.

### Proposition ET03-A local implementability

For a memoryless prescribed joint response π on global configurations Z, local response functions `α_i:O_i→A_i` with `π_i=α_i∘o_i` exist exactly when every `π_i` is constant on each `o_i`-fibre. The same criterion applies to local histories for history-dependent responses.

**Proof.** A local function cannot distinguish equal local views. Conversely its value on each attained view is well-defined by fibre constancy. ∎

The useful application is architectural: a centralized chooser cannot read variables merely because the analyst placed them in the global model.

### Exact two-locus fixture

A source-monitoring locus knows a hidden bit b. The action-guidance locus initially sees one constant signal. The task is to choose `repair_b`; the other repair is unsafe. A flat external chooser reading the whole configuration can choose correctly. The action-guidance locus cannot, because its two local views coincide. An authorized channel carrying b from source monitoring to action guidance in one step makes the task locally realizable. Removing that channel or its license restores the obstruction.

Both architectures can emit the same current display. The channel and retained information change future capability. Counting two local copies of b as two independent sources would be an additional error, not a consequence of the two-locus representation.

### Honest flattening control

A finite multi-locus architecture can always be represented by a single product-state transition system if that system retains all local states, channels, shared causes, and the local-factorization restriction on allowed policies. That faithful flattening preserves traces. The failure above arises from discarding information constraints or giving the flattened chooser a hidden-state oracle, not from a theorem that multiple faculties are formally irreducible. The model asserts no particular human cognitive anatomy.

## 4. ET04 the dependency-complete finite equilibrium theorem

Let the player/locus index set be finite and nonempty. Each response set `S_i` is finite and nonempty. Supply scalar pure-profile payoffs `u_i:∏S_j→R`. These S_i are one-shot options or already-compiled locally implementable plans for the declared information context. The ordinary game assumes their jointly feasible combinations form the full product. Finite primitive response alphabets do not make an unbounded temporal policy space finite, and observation-dependent or coupled action constraints need their own information-game/constrained model. The ordinary mixed extension uses independent player choices and expected payoffs

`U_i(σ)=Σ_s [∏_j σ_j(s_j)]u_i(s)`.

Every simplex `Δ(S_i)` is nonempty, compact and convex; their finite product Σ is likewise. Each U_i is continuous in the full mixed profile and affine in player i's mixture. Define

`BR_i(σ_-i)=argmax_{τ_i∈Δ(S_i)} U_i(τ_i,σ_-i)`.

For every opponent profile this is a nonempty compact convex face. Continuity gives a closed graph: any limit of maximizing choices remains maximizing against every alternative. With compact values/domain this supplies upper hemicontinuity. The product best-response correspondence therefore meets finite-dimensional Kakutani's hypotheses. A fixed point is precisely a mixed Nash equilibrium.

This is standard finite Nash, with the extra structure exhibited rather than hidden in the simplex notation. It uses no hypothetical P02/U08 or P12/Q1b checkpoint. It is not a new proof of general Kakutani, a Lean development, or a claim that the finite-support repository theorem realizes every real probability.

### Necessary distinctions and deletion witnesses

- Convex geometry without payoffs does not define a profitable deviation
- `F(x)=1−x` on `[0,1]` has the fixed point 1/2 but iterates from 0 alternate forever. Fixed-point existence does not imply iterative convergence
- A correspondence with empty values can have no fixed point
- On the nonconvex domain `{0,1}`, the flip has no fixed point despite nonempty singleton values
- On `(0,1)`, `F(x)=x/2` has no fixed point; compactness was removed
- `F(0)=1`, `F(x)=0` for x>0 has no fixed point; graph closure/continuity was removed
- The correspondence `{1}` below 1/2, `{0}` above 1/2, and `{0,1}` at 1/2 has a closed graph and nonempty compact values but no fixed point; convexity of values was removed
- A one-player model can give a false response higher utility than the true response. Its unique equilibrium is then false relative to the separately supplied truth predicate

The repository's V4-S2 separately proves contraction for one quadratic map after entry to an invariant interval. That cannot be promoted to convergence of all best-response correspondences. Finite-game existence also supplies neither an implemented solver nor a sampler/runtime contract; those require effective representations and their own verification.

## 5. ET05 strict-cone repair and vector equilibrium

The source PDF contains a real mismatch on printed p.8: §7.1 uses `C_i\{0}`, while §7.2 says improvement in every dimension. Under the positive orthant, those are different notions. We retain both explicitly:

- **E_nd:** no unilateral expected vector gain lies in `R_+^{k_i}\{0}`; no weak-all/strict-some improvement
- **E_int:** no unilateral expected vector gain lies in `R_{>0}^{k_i}`; no every-coordinate-strict improvement

Then `E_nd⊆E_int`. The inclusion can be strict. With one player and two outcomes `(0,0)` and `(1,0)`, every mixture is in E_int because the second coordinate never rises; only the second pure action is in E_nd.

### Proposition ET05-A positive scalarization gives vector equilibria

In a finite vector-payoff game with coordinatewise expected mixed payoffs, choose for each player weights `w_i` with every coordinate strictly positive. Every Nash equilibrium of scalar payoffs `w_i·U_i` belongs to E_nd. Therefore E_nd is nonempty by finite Nash. Nonnegative, nonzero weights guarantee only membership in E_int in general.

**Proof.** A nonzero nonnegative gain has strictly positive dot product with a strictly positive weight vector, contradicting scalar equilibrium. A strictly positive gain has strictly positive dot product with any nonzero nonnegative vector. ∎

The strict-positivity hypothesis is sharp for the stronger conclusion. For the outcomes `(0,0)` and `(1,0)`, weights `(0,1)` make both actions scalar optimal, although the first fails E_nd. A weight outside the dual cone can even rank a dominated outcome above its improvement.

The weights here are mathematical existence witnesses. They do not specify which equilibrium or trade-off an epistemic agent ought to adopt.

### Proposition ET05-B exact finite mixed scalarization characterization

For the finite game and orthant order just specified,

`E_nd = ⋃_{w_i∈R_{>0}^{k_i}} NE(w₁·U₁,…,w_n·U_n)`.

Each equilibrium may require its own player-specific weight vectors. This is a union over allowed witnesses, not an assertion that one fixed weight vector captures every vector equilibrium.

**Proof of the converse.** Fix a profile in E_nd and player i. Let d_j be the expected vector gain from choosing pure response j against the fixed opponents, relative to the current mixture. The current mixture makes zero a convex combination of the d_j. Let D be their finitely generated cone. If D contained a nonzero nonnegative vector, positive rescaling and adding the feasible zero combination would produce a feasible mixed deviation with that sign, contradicting E_nd. Thus D and the simplex `{v≥0:Σv_j=1}` are disjoint. D is closed and convex because it is finitely generated; the simplex is compact and convex. Strict separation provides a vector w whose dot product is nonpositive on D and strictly positive on that simplex. In particular every coordinate of w is positive. It follows that every pure deviation, hence every mixed deviation, has nonpositive scalar gain under w. Choose such a w separately for each player. The profile is Nash in the resulting scalarized game. ∎

This finite convexification premise matters. Among only the three pure choices `(3,0),(1,1),(0,3)`, the middle point is Pareto efficient but maximizes no strictly positive weighted sum. Once mixtures are admitted, the half-mixture of the extremes yields `(1.5,1.5)` and dominates it. A sharper convex infinite-choice counterexample is the compact convex payoff set `{(x,y):0≤y≤1, −1≤x≤−y²}`. The point `(0,0)` is Pareto efficient, but for any strictly positive weights `(w₁,w₂)`, a sufficiently small t>0 gives `w·(−t²,t)>0`; no such weights support the origin. The boundary weight `(1,0)` does. The conic hull of feasible gains need not be closed here. Thus even compactness and convexity alone do not replace the finite-polyhedral premise for the strictly positive converse.

The weak version replaces strictly positive weights by nonnegative nonzero weights and uses weak separation against the open positive orthant. We use ET05-A and the fully supplied strong proof above for the executable interface; no unspecified general vector-existence theorem is being assumed.

### Team, constraints and pipeline are different branches

For identical scalar payoffs W, every global maximizer of W is Nash; the converse fails. In the two-player coordination table `W(0,0)=2`, `W(1,1)=1`, and the off-diagonal values 0, both diagonal profiles are Nash, but only `(0,0)` is globally optimal.

If a joint feasibility constraint permits only `(0,0)` and `(1,1)`, unilateral feasible deviations may be impossible at either point. A generalized Nash criterion can then accept a suboptimal point even with a common objective. The feasible set is not a product of independent simplices, so ordinary finite Nash's best-response argument cannot be imported unchanged.

A pipeline instead supplies ordered transformations and a terminal/readout condition; it need not contain preferences or profitable deviations at all. Its correctness belongs to composition, local information and permitted transitions. Calling it a game adds no theorem unless the response and payoff interpretation is defensible.


### Proposition ET05-C a joint-concavity repair removes finite team-payoff interaction

For the ordinary independent mixed extension W of a finite common-payoff table on the **full product** of mixed simplices, joint concavity, joint convexity, joint affinity, and additive separability of the pure payoff table are equivalent. Consequently one cannot impose joint concavity as a harmless way to turn unilateral stability into global team optimality while retaining genuine interactions in that scalar payoff.

**Proof.** Fix any two players, two responses for each, and pure responses of all others. Both opposite pairs of corners have the same mixed midpoint, whose value is the mean of all four corner values. Concavity on one diagonal and then the other forces equality of the diagonal sums. Every conditional two-player rectangle therefore has zero mixed difference. Relative to a pure baseline r, the payoff increment from changing one player's response is independent of all other responses. Telescoping gives `w(s)=w(r)+Σ_i[w(r_-i,s_i)−w(r)]`. Its mixed extension is jointly affine, hence both concave and convex. Convexity gives the same diagonal equality with inequalities reversed. ∎

This is stronger than each payoff being affine in its **own** mixture, which every finite game already satisfies. Additive payoff separability need not remove every causal or informational interaction in the architecture. Nor does the result apply to a proper coupled feasible subset: the coordination payoff `W(p,q)=1−p−q+3pq`, restricted to `p+q=1`, becomes the concave function `3p(1−p)`.

A joint-law simplex also changes the geometry: `Σ_s μ(s)w(s)` is linear in μ even for an interacting payoff. Without further constraints this does not raise the maximal common expected payoff, because a payoff-maximizing pure joint profile is already a product of pure marginals. Fixed marginals or other implementation constraints are what make correlation improve the feasible value in the deployment counterexample below.

## 6. ET07 representation invariance has a typed boundary

### Proposition ET07-A evidence-order invariance

Coordinate permutations and coordinatewise strictly increasing bijections preserve and reflect coordinatewise order, hence preserve dominance and incomparability of deterministic profiles. If records' schema, units and admission predicates are transported with the transformation, common admission is preserved as well. A bijective observation re-encoding also preserves target sufficiency after the target/readout is transported.

This claim does not automatically preserve **expected-payoff mixed games** when nonlinear functions are applied to pure outcomes before averaging.

### Proposition ET07-B game invariance

Bijections of each player's action names, with payoff and feasibility tables pulled back accordingly, transport mixed equilibria by pushforward of distributions. For scalar mixed games, transformations `u_i'=a_i u_i+b_i` with `a_i>0` preserve exactly the Nash set, because every unilateral expected gain is multiplied by a_i. For vector expected-payoff games, invertible affine transformations `U_i'=A_iU_i+b_i`, together with cone transport `C_i'=A_iC_i`, preserve both explicitly chosen improvement relations and their equilibrium sets.

### Countermodel ET07-NL monotone utility re-encoding changes mixed equilibrium

Player 1's payoff table is `[[0,2],[1,0]]`; player 2's is `[[1,0],[0,1]]`. Their unique fully mixed equilibrium has row-0 probability p=1/2 and column-0 probability q=2/3. Squaring player 1's nonnegative pure payoffs preserves all its pure outcome rankings but changes its indifference equation and yields q=4/5. Thus arbitrary monotone transformation of pure payoffs is not harmless for expected-utility mixing.

Units also matter. Profiles `(1,0)` and `(0,2)` with weights `(1,1)` reverse score order if only the first coordinate's unit is multiplied by three and the old weights are retained. Transporting the weights contravariantly, by `w'=D^{-T}w` under `e'=De`, preserves the score. A re-encoding that changes the bridge as well as the representation is not a pure representation test.

## 7. The new dynamic connection equilibrium deployment is not restoration

The PDF itself distinguishes interpretations of a mixed vector. The following exact theorem concerns only one explicitly declared interpretation: independent identical resampling of joint response profiles over time.

### Proposition ET-D1 repeated mixed deployment

Let a finite joint profile set S carry a fixed sampling law μ, drawn independently at every time, and let `Target⊆Safe⊆S` be independently supplied. Then

`Pr(eventually always Target)=1` iff `μ(Target)=1`.

If `μ(Target)<1`, the probability of eventual target persistence is zero.

**Proof.** Target-supported sampling stays target on every support path. Otherwise let bad probability be p>0. For any fixed N, the probability of no bad draw after N is the limit of `(1−p)^m`, namely zero. The event of only finitely many bad draws is the countable union of those zero-probability events over N. ∎

No generic independence assertion is needed outside that explicitly declared deployment. Changing temporal dependence changes the model.

### Same marginals, opposite temporal results

In the two-player coordination game with payoff one for agreement and zero otherwise, both players mixing `(1/2,1/2)` is Nash. Under independent resampling, mismatches occur with probability 1/2 each round and infinitely often almost surely. If the target is agreement, that Nash policy is not almost-sure restorative.

A shared random bit that produces `(0,0)` or `(1,1)` with equal probability has the same individual marginals but always meets the agreement target. It is a correlated coordination law, not the same independently mixed profile. Neither mechanism establishes truth, the authority of a shared random source, or real cognitive implementation. Their exact joint dependence, rather than marginal weight vectors, controls restoration.

### A sufficient dynamic bridge, separate from Nash

Suppose a selected licensed finite update process has an integer rank R≥0, target is invariant, and outside target

- R never increases on any admitted transition
- conditional on every history, expected rank decrease is at least ε>0

Then target entry is almost sure and its expected time is at most `R₀/ε`. Stopping the rank at target and telescoping conditional expectations gives `ε E[min(τ,n)]≤R₀`; monotone convergence yields the bound and almost-sure finiteness. If every allowed non-target step strictly decreases R, the stronger sure bound is `τ≤R₀`. A geometric self-loop shows that positive expected progress alone does not give sure entry.

A finite ordinal-potential game's strict improvement steps supply a separate finite-progress mechanism, but arbitrary idle steps, disturbances, or switching potentials can destroy it. The disturbance lane's countermodels and common bad-visit ranks explain exactly what additional temporal contract is needed. An equilibrium label by itself supplies none of these assumptions.

## 8. ET06 assumption DAG and evidence ceiling

`assumption_dag.json` accompanies this report. L5 scalar, L6 vector, and L7 team/constrained formulations are sibling branches. The common graph distinguishes:

- typed profile representation
- an explicitly supplied comparison order
- local state/information architecture
- finite response sets and licensed joint implementation
- geometric mixed simplices
- an actual deployment interpretation/joint law
- scalar, vector, and common-objective evaluation branches
- fixed-point existence
- effective realization and temporal restoration
- separately warranted truth and normative authority

Lower-level data cannot discharge a missing premise by relabeling it. In particular, source tuples do not alone select utilities; geometric mixtures do not select a sampling law; Nash existence does not select a convergent dynamic; explicit bridge provenance does not make the bridge correct.

## 9. ET08 implementation interface and exact credit

Proposed isolated application names use the `EpistemicProfile` namespace; they do not allocate canonical T-identifiers:

- `ProfileSchema`, `ContextAdmission`, `ProfileOrder`, `ScoreTargetCertificate`
- `LocalViewArchitecture`, `LocalPolicyFactorization`
- `FiniteScalarGame`, `FiniteVectorGame`, `ImprovementKind`
- `PositiveWeightWitness`, `EquilibriumReencoding`
- `DeploymentKernel`, `TemporalTargetContract`

An implementation must preserve explicit fields for coordinate orientation/units, source/extraction identity, inquiry/version, local views, permitted actions, payoff or cone identity, strict-improvement convention, mixture semantics, and output claim type. A result about one layer must not be accepted as a certificate for another.

Recommended implementation order is: schema/order checks; fibre/target counterexamples; local-view architecture; exact finite rational equilibrium fixtures; vector witness checks; re-encoding tests; independent temporal kernels; then optional formal theorems. Integrate with `observations.py` only through a declared observation-law/factorization adapter, and with the operational engine only through separately issued current licenses. No new authority is created by importing this application.

Required negative controls are the score collision, injective order manufacture, nonmonotone utility transform, zero-weight Pareto failure, nonconvex pure-choice scalarization failure, hidden local repair bit, unauthorized channel, mixed/correlated same-marginal separation, unsafe equilibrium, and progress-resetting controller switch. Positive controls include chain embedding, target-sufficient compression, lawful local message transfer, scalar/vector equilibria with explicit weights, affine invariance, and target-supported or rank-certified deployment.

The outcome is **mixed but substantive**: accepted conditional applied mathematics and test cases; repaired scalar-loss and strict-cone claims; rejected automatic bridges from cognitive vocabulary, equilibrium, or current output to truth, convergence or authorization. Canonical adoption, empirical validation, global novelty and publication remain open. P15 may consume the finalized, hash-bound `p15_interface.json` research checkpoint; it must preserve these accepted/repaired/rejected distinctions rather than treating the original PDF as uniformly established.

## Primary mathematical sources

- Nash, [*Equilibrium points in n-person games*](https://doi.org/10.1073/pnas.36.1.48), 1950: finite mixed equilibrium with expected scalar payoffs. This is the existence ancestry, not a convergence or epistemic-truth result
- Monderer and Shapley, [*Potential Games*](https://people.csail.mit.edu/jrennie/trg/papers/monderer-potential-96.pdf), 1996, Lemma 2.3: strict improvement paths in finite ordinal-potential games are finite. Idle transitions and mode changes need separate hypotheses
- Qu, Ji and Goh, [*The Robust Weighted Multi-Objective Game*](https://pmc.ncbi.nlm.nih.gov/articles/PMC4583224/), 2015: explicitly distinguishes Pareto and weak Pareto and studies supplied sets of weights. Its broader nonlinear/robust hypotheses are not silently substituted for our finite mixed polytope proof

The proofs above supply the exact application-specific claims. The general scalarization/separation methods are standard; no priority claim is made.


## Reproducible verification record

`python -m unittest -v` passes seven focused tests. `python probe_epistemic.py` checks 242 labeled posets through four elements against 5,377 injective rank maps; 1,530 score/target pairs against all finite decoders; 10,935 three-response/two-coordinate mixtures against independent exact segment-gain analysis; and 1,200 seeded two-player vector profiles plus affine invariance checks. There are zero reported mismatches. The strong and weak vector criteria accept 2,739 and 5,835 cases respectively, preserving the PDF's strictness distinction rather than erasing it.

The companion `team_concavity_check.py`, independently replayed for this packet, checks all 81 two-player and 6,561 three-player binary-response payoff tables with entries −1,0,1. Exactly 19 and 33 respectively are additive; every other table has midpoint witnesses against both joint concavity and joint convexity. These are exact finite checks and ordinary proofs, not a kernel-checked general P14 development.
