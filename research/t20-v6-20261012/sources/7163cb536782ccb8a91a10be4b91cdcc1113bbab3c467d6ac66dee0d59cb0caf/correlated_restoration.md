# Correlated response policies and the exact limit of marginal restoration

This extends the completed P14 research return without altering that sealed packet. It addresses a concrete gap between mixed-policy geometry and a continually deployed restorative mechanism. All profiles, marginals, target relations, payoffs and licenses below are declared model objects. Their epistemic correctness and actual implementation remain separate burdens.

## 1. One-step coordination has a sharp finite obstruction

Two loci choose responses in finite nonempty sets A and B. Their prescribed marginals are probability distributions μ and ν. A coordinator may choose any coupling κ with those marginals. Let `R⊆A×B` be a supplied target relation; write `R[U]={b:∃a∈U,(a,b)∈R}`.

Define the maximal weighted Hall deficit

`δ(μ,ν,R)=max_{U⊆A} [μ(U)−ν(R[U])]`.

The empty set makes δ nonnegative. It lies in [0,1].

### Theorem CR1 exact unavoidable violation mass

When every joint profile in A×B is available, the minimum probability of violating R over all couplings of μ and ν is exactly δ. Consequently a target-supported coupling exists exactly when all weighted Hall inequalities `μ(U)≤ν(R[U])` hold.

**Lower bound.** For any U, mass from U that lands inside R can reach only R[U], whose total column capacity is ν(R[U]). At least `μ(U)−ν(R[U])` mass must fall outside R. Take the maximum.

**Attainment.** Form a transportation flow network: source-to-row capacities μ(a), row-to-column edges only for pairs in R with capacity larger than one, and column-to-sink capacities ν(b). A finite cut corresponding to row subset U has capacity `1−μ(U)+ν(R[U])`. The max-flow/min-cut theorem therefore gives a maximal R-supported subcoupling of total mass `1−δ`.

Complete the residual row/column masses to a full coupling. If δ>0, their product divided by δ is one completion. No residual positive row/column pair lies in R, because it would augment the supposedly maximal flow. The completed law has precisely δ mass outside R. ∎

This is standard finite transportation/max-flow mathematics, with a restorative application. The original max-flow/min-cut source is Ford and Fulkerson, [*Maximal Flow Through a Network*](https://doi.org/10.4153/CJM-1956-045-5), 1956.

### Exact binary example

If R requires the two binary responses to agree, the deficit is `|μ(0)−ν(0)|`. Marginals `(4/5,1/5)` and `(1/5,4/5)` therefore force disagreement probability at least 3/5. The bound is attained by joint masses `κ(0,0)=1/5`, `κ(0,1)=3/5`, `κ(1,1)=1/5`.

For equal half-half marginals, independent mixing disagrees with probability 1/2, while a diagonal coupling has zero disagreement. Marginal summaries alone do not identify which mechanism is deployed.

### Hard authorization exclusions change the optimization

If only profiles in `L⊊A×B` are licensed, first require a coupling supported in L. To minimize violation of R, solve the constrained transportation problem; CR1's unrestricted deficit need not be attained by an L-supported law.

For half-half binary marginals, `R={(0,0)}` has unrestricted deficit 1/2. If `(1,1)` is forbidden while the other three profiles are permitted, the only coupling has mass 1/2 on each off-diagonal. Its R-violation probability is one. The unrestricted optimal completion used an unavailable profile. This is an authorization/feasibility constraint, not a defect of the max-flow theorem.

## 2. A repeated-use threshold with the filtration stated

Let `(F_t)` be a filtration containing all past publicly recorded joint response profiles and the current context used to choose the next joint law. At step t, the target relation R_t and prescribed marginals μ_t,ν_t are F_t-measurable. The sampled pair `(A_t,B_t)` is included in F_{t+1}; thus

`V_t = {(A_t,B_t)∉R_t}` belongs to F_{t+1}.

The contract says that **conditional on every admitted decision history**, the next pair has marginals μ_t and ν_t. It is stronger than prescribing only unconditional one-time marginals. Put

`p_t=P(V_t | F_t)`, `δ_t=δ(μ_t,ν_t,R_t)`.

CR1 gives `p_t≥δ_t` almost surely. No independence between successive draws is assumed.

### Theorem CR2 exact adapted-event threshold

For any such implemented process,

`{V_t occurs only finitely often} = {Σ_t p_t<∞}` almost surely.

In particular:

1. On paths where `Σδ_t=∞`, infinitely many target violations occur almost surely
2. If a selected implementation has `Σp_t<∞` almost surely, it eventually always meets the target almost surely
3. A uniform lower bound `δ_t≥ε>0` is a sufficient obstruction, but not a necessary one; nonsummable deficits tending to zero also obstruct
4. Merely positive deficits tending to zero do not by themselves obstruct eventual persistence

This is Lévy's conditional Borel–Cantelli principle applied to the explicitly adapted violation event, not a new probability theorem. A precise statement and proof appear as Theorem 11 in Chandra Nair's [martingale notes](https://chandra.ie.cuhk.edu.hk/courses/Probability/ln6.pdf).

**Proof mechanism.** Let `S_n=Σ_{t<n}1_{V_t}` and `A_n=Σ_{t<n}p_t`. The compensated count is a martingale. The normalized martingale

`Z_n=Σ_{t<n}(1_{V_t}−p_t)/(1+A_{t+1})`

is square-integrable with bounded total expected quadratic variation: conditionally its next variance is at most `p_t/(1+A_{t+1})²`, and the pathwise sum is bounded by `∫₀^∞(1+x)^{−2}dx=1`. It converges almost surely. On `A_∞=∞`, Kronecker's lemma gives `(S_n−A_n)/(1+A_n)→0`, hence infinitely many violations. On `A_∞<∞`, summation by parts with the bounded increasing denominators makes the compensated count converge; S_n then has a finite limit. This gives the claimed event equivalence. ∎

### Corollary CR2-S deterministic marginal schedules

Suppose μ_t,ν_t,R_t are a fixed deterministic sequence, every joint profile is available, and every selected finite coupling can be implemented under the declared sampler/channel contract. There exists a history-based coupling scheme with almost-sure eventual target persistence **if and only if** `Σδ_t<∞`.

For sufficiency choose a minimizing coupling at each t, so `p_t=δ_t`; for necessity every coupling scheme has `p_t≥δ_t`. The explicit schedule need not be stationary or implementable by a finite-memory controller. No finite-arena bound is inferred.

For context-dependent future marginals, a greedy minimizing coupling may change which future contexts occur. The corollary is not a general dynamic-programming shortcut: one must analyze the resulting deficit process under the selected policy.

### Sharp positive and negative schedules

Let the first binary marginal assign probability δ_t to response 0, while the second always chooses 1, and let target mean agreement. Then the violation probability is forced to be exactly δ_t.

- For `δ_t=1/(t+2)²`, violations are finite almost surely. A union bound gives probability of any violation at or after N at most `1/(N+1)`. There remains a positive chance of a violation at every fixed late time, so no deterministic last-violation horizon is supplied
- For `δ_t=1/(t+2)`, violations are infinite almost surely. The probability of no violation over a block starting at N of length m is `(N+1)/(N+m+1)`, tending to zero

Both schedules have positive deficits at every step, and both tend to zero. Summability is the relevant boundary at this exact scope.


### Corollary CR2-P licensed and incentive-compatible coupling polytopes

Let `C_t` be a nonempty compact set of couplings satisfying the prescribed marginals, current hard action licenses, and any explicitly chosen correlated-equilibrium inequalities. Define

`δ*_t=min_{κ∈C_t} κ(R_t^c)`.

The minimum exists by finite-dimensional compactness. Every compliant implementation has `p_t≥δ*_t`, while a selected minimizer attains equality. Consequently the same adapted-event theorem applies with δ* in place of the plain Hall deficit. For deterministic sequences of nonempty feasible polytopes and targets, a compliant almost-sure eventually-target implementation exists exactly when `Σδ*_t<∞`, under the stated sampler/channel realizability premise.

Plain Hall is only a lower bound `δ_t≤δ*_t` in this constrained problem. An empty feasible polytope is a different obstruction: the marginal/license/incentive contract cannot be implemented at that step. It is not assigned an arbitrary infinite “probability.” In endogenous contexts, choosing a current minimizer can alter future polytopes and deficits; this corollary does not prove greedy dynamic optimality.

## 3. The information guard cannot be omitted

Conditional Borel–Cantelli requires the violation events to be adapted to the filtration used for their conditional probabilities. Conditioning an unobserved physical predicate on public history does not satisfy that condition automatically.

### Countermodel CR-hidden-public-certificate

Take safe states 0,1,2 with target `{0,2}` and one joint response. State 0 stays at 0; state 1 moves to 0; state 2 moves to 2 with probability 1/2 and to each of 0 and 1 with probability 1/4. Initially the plant is at 2. Every state emits the same observation.

Every support path has at most one actual bad visit, so physical co-Büchi restoration is **sure**, stronger than almost sure. Nevertheless the public belief after one step is always `{0,1,2}`. A rule requiring the next belief to be wholly target has no certified action; its publicly computed target-action relation is empty. For the sole joint response its Hall deficit is one, and that public certificate fails forever.

The Hall conclusion is correct about the chosen **public certificate** and false if relabeled as a physical-restoration impossibility theorem. Here the actual probability of a bad state at time t≥1 is `2^{−(t−1)}/4`, and the bad state is not observed in the public filtration.

The even smaller filtration warning is a hidden bit Z that is bad with probability 1/2 and never changes. With no public observations, `P(Z is bad | F_t)=1/2` for every t, yet infinitely many actual bad occurrences have probability 1/2, not one. The alleged repeated bad events are not F_{t+1}-measurable. Enlarging the filtration to reveal Z changes their conditional probabilities to zero or one; one may not keep the old half probabilities after that enlargement.

### Consequence for the disturbance synthesis result

At a counter-game state `(c,f)` in S_k, define

`Good_k(c,f)={a∈Γ(c,supp f): every observation successor stays in S_k}`.

A joint-action coupling supported in Good_k, with an observable action record and a faithful sampler/channel implementation, is a sufficient way to realize the already certified bounded-visit controller. All random support choices remain in the winning safety game.

A positive Hall deficit for Good_k obstructs **that prescribed-marginal, fixed-k certificate implementation**. It does not establish that no other bound, other strategy, or actual co-Büchi restoration is possible. Public certificate failure and physical failure remain separate.

## 4. Coupling feasibility is not incentive compatibility

If loci are obedient parts of an authorized joint controller, the question is implementability. If they are modeled as strategic players, a proposed recommendation law also needs an incentive condition.

For scalar payoffs u₁,u₂, a correlated equilibrium law κ must satisfy, for every response a and alternative a′,

`Σ_b κ(a,b)[u₁(a,b)−u₁(a′,b)]≥0`,

and the analogous inequalities for the second player. These are additional linear constraints. With uncertain supplied payoff standards, requiring them under every live standard is a robust incentive contract; averaging standards instead requires its own warranted probability interpretation.

### Countermodel CR-incentive

In matching pennies, player 1 receives one for agreement and player 2 one for disagreement. The unique Nash marginals are half-half. A diagonal coupling with those marginals exists and satisfies the agreement target perfectly, so its Hall deficit is zero. But the second player gains by deviating from every diagonal recommendation. There is no correlated equilibrium supported on the diagonal. Under the fixed half marginals, the incentive inequalities force the uniform joint law, with agreement-target violation probability 1/2.

In the common-interest coordination game where both receive one for agreement, the diagonal law **is** a correlated equilibrium. Same marginal feasibility does not determine the incentive conclusion; the payoff bridge matters.

### Exact binary implementation surface

With first-response probabilities p and q, every binary coupling has the form

`κ₀₀=t`, `κ₀₁=p−t`, `κ₁₀=q−t`, `κ₁₁=1−p−q+t`,

where `max(0,p+q−1)≤t≤min(p,q)`. Hard exclusions and all correlated-equilibrium inequalities are linear bounds on t. The attached exact rational solver intersects these bounds and minimizes the remaining target-violation mass at an endpoint. It reports infeasibility when the lower and upper bounds conflict. This does not certify that the utilities, permitted profiles, or prescribed marginals are epistemically authoritative.

## 5. Pairwise root or channel compatibility does not solve global coordination

For three binary loci with half-half marginals, each pair admits a perfectly anticorrelated coupling. But no joint triple satisfies all three pairwise anticorrelation requirements: three binary values cannot be pairwise different. Every pairwise Hall test passes while the global relation is empty.

Thus a many-locus implementation needs the actual joint law and global compatibility constraints. Independent-looking channel names, pairwise consistency, or several marginal certificates do not establish a realizable multiway coupling. Likewise, copying one common random source can create correlation but does not create independent evidential roots or new permission to coordinate.

## 6. Verification and claim ceiling

The standard-library scripts use exact rational arithmetic:

- `maximize_relation_mass` constructs a maximal supported subcoupling, completes it, and checks both marginals and attained violation mass
- 3,000 seeded transport instances match independent exhaustive Hall-deficit calculations with zero discrepancies
- 4,000 constrained/robust-incentive binary instances match an independent exact vertex grid; 1,170 are feasible, with zero feasibility or optimal-value discrepancies
- 500 adaptive finite-history trees satisfy the conditional geometric tail bound; 152 harmonic products match the exact telescoping expression
- The hidden physical/public-certificate separation and impossible three-way anticorrelation are explicit regression fixtures
- At the Hall/incentive checkpoint the combined unit suite passed 20 tests; the consolidated 34-test replay is recorded in `README.md` and `verification_report.json`

The infinite adapted-event threshold is proved mathematically and inherits a stated standard martingale theorem; finite probes do not establish infinite-time measure claims. No hypothetical coupling, payoff, observer, or provenance label is being asserted to describe a real person, source, or cognitive system.
