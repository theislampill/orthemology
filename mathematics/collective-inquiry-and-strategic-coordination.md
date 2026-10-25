# Collective inquiry: information, strategy and coordinated judgment

## Abstract

A community can possess the premises of a conclusion without any member being able to integrate them. A game can have an equilibrium while its agents violate a hard joint constraint. Two groups can produce exactly the same answers while using different members' evidence. These are different failures, and each requires a different mathematical account. This chapter develops a common framework for them: shared occurrences with local observations; heterogeneous evidence with explicit comparison rules; locally implementable strategies; scalar and vector equilibria; complete coordination records; temporal deployment; and observations that identify actual contribution. It supplies finite counterexamples and proofs, including an exact positive-weight characterization of finite vector equilibria, coordination and information bounds, and a Gaussian nonidentification result with positive discrimination and inquiry-value counterparts. Its temporal treatment also establishes sharp constrained-coupling bounds, a conditional restoration threshold, exact transfer through implementable information interfaces, and recovery conditions that distinguish finite departures from permanent failure. It also separates finite-memory accuracy from eventual correctness, distinguishes fixed hidden standards from a common observed objective, and gives the exact risk threshold for fresh switching innovations. For fixed finite models with positive controlled-observation laws, it gives an exact criterion for eventual correctness and a constructive history policy. The results consolidate conditional public research. They do not establish a cognitive anatomy, a fitted social model, or the completion of an unfinished general noetic-field theory.

## 1. Shared inquiry and distributed access

### 1.1 One occurrence, several observations and objectives

Let $`m`$ denote a concrete occurrence and $`\Omega_i(m)`$ the observation available to agent $`i`$. An occurrence includes the worldly facts needed for the inquiry: a game position can require the move history and the player to move, while a document assessment can require its actual edition. Different observations do not multiply the occurrence. In a card game, the actual deal is shared reality even though each player sees different cards. An information set describes what a player can distinguish; it is not an additional component of the world's identity. [1, §§1–3][r1]

An agent's analysis $`A_i`$ specifies a task, representation, boundary and assessment conditions. Its complete profile map $`O_i(m)`$ takes values in a profile space $`\Pi_i`$. This actual profile is distinct from the agent's inferred judgment, which must be formed from its available observation $`\Omega_i(m)`$ under the declared analysis. A repeatable state type such as “White checkmates Black” is also distinct from the objective “maximize my utility”: the objective selects appropriate outcomes; it is not itself one of their state types. A task can select a target set $`G_i\subseteq\Pi_i`$. The target, the transition rules and the policy have separate roles: the target says what counts as an appropriate outcome; the rules determine lawful successors; the policy chooses among available actions. A procedure for validating evidence is another object. Competitors can share standards for whether a position is terminal, an assessment is stale or an analysis is sufficient while aiming at opposed outcomes. Those standards govern how judgments are made and validated, not whose target wins. A task indexed to a player supplies no psychological or ethical finding of selfishness. None of these categories becomes another merely because each governs some part of a game.

Targets in different profile spaces cannot be compared by an untyped intersection. Pull them back to the same reachable-occurrence domain:

```math
\widetilde G_i(m)
=\{m'\in\mathrm{Reach}(m):O_i(m')\in G_i\}.
```

Two targets are jointly realizable precisely when $`\widetilde G_i(m)\cap\widetilde G_j(m)\ne\varnothing`$. The schema “win for the player in this role” can be invariant under a role exchange while the two instantiated win-targets are disjoint. Schema isomorphism is not target identity. Cooperation may use a shared analysis and target, or an explicit alignment between different profile spaces; partial joint realizability alone does not identify the objectives. Moreover, zero-sum payoffs allow a draw with payoffs $`(0,0)`$; opposed win-targets need not exhaust the terminal states. Actor-relative objectives also do not make every judgment actor-relative: whether an observed checksum matches a specified value can be the same question for every participant. [1, §§2–3][r1]

### 1.2 When component work forms one inquiry

A distributed investigation can be described as a directed graph of episode tokens. A handoff passes a scoped result or evidence item to a later episode; a revision changes an earlier assessment; a retry is a new attempt. Orient these edges from earlier tokens to later tokens. Repeated policies can cycle, but their successive episode tokens do not need backward edges.

The graph and an assessment of the collective are different levels of description. To represent the graph as one accountable inquiry episode, the public formal core requires compatible occurrence lineage and analysis, an identified collective boundary with rule precedence, and an explicit rule for combining profiles, evidential statuses and remaining obligations. Sharing a task label does not ensure compatible tolerances or representations. A fusion analysis is needed where the component analyses differ. [2, §5.2][r2]

Collective correctness is consequently not the conjunction of component correctness. A validator can catch a mistaken intermediate result and yield a correct collective output. Conversely, individually sound assessments can yield an unsound composite if a handoff drops a qualification or uses a result at a different edition. The final speaker's output is not automatically a complete account of what the collective established. These conditions define a proposed assessment model; they are not an empirical claim that every actual institution has such a boundary or fusion rule.

### 1.3 A complete five-state evidence example

Distributed availability, individual knowledge and operative integration can be separated without uncertain measurements. Consider five states with the following probability law and truth values. State 0 is actual. [3][r3]

| State | Probability | $`A`$ | $`B`$ | $`C`$ | $`H`$ |
|---:|---:|:---:|:---:|:---:|:---:|
| 0 | $`1/10`$ | true | true | true | true |
| 1 | $`2/10`$ | true | true | false | false |
| 2 | $`2/10`$ | true | false | true | false |
| 3 | $`2/10`$ | false | true | true | false |
| 4 | $`3/10`$ | false | false | false | true |

Member 1 observes the truth values of $`A,B`$; member 2 observes $`A,C`$; member 3 observes $`B,C`$. Their complete information partitions are respectively

```math
\{\{0,1\},\{2\},\{3\},\{4\}\},\qquad
\{\{0,2\},\{1\},\{3\},\{4\}\},\qquad
\{\{0,3\},\{1\},\{2\},\{4\}\}.
```

Use the idealized partition semantics: a member knows a proposition at a state when it holds throughout that member's information cell. At state 0, each of $`A,B,C`$ is known by two members, but no member knows the missing indicator, their conjunction, or $`H`$. Nevertheless

```math
A\cap B\cap C=\{0\}\subsetneq H=\{0,4\},
\qquad \Pr(H\mid A\cap B\cap C)=1.
```

Thus a componentwise inventory accepting propositions known by a relevant majority can contain premises that jointly entail $`H`$ while nobody has their joint information. The proper inclusion shows that $`H`$ was not merely defined as the conjunction. Each actual private cell has probability $`3/10`$ and contains $`H`$-mass $`1/10`$, so every member's posterior is $`1/3`$.

Even the description “the private evidence disconfirms $`H`$” depends on the baseline. Unconditionally $`\Pr(H)=2/5`$, so the posterior $`1/3`$ is lower. If the common background first includes $`D=\{0,1,2,3\}`$, then $`\Pr(H\mid D)=1/7`$. The same private cells are contained in $`D`$, so their posterior remains $`1/3`$ and now represents an increase. Joint entailment and private ignorance have not changed.

The model does not announce the actual inventory to its participants. Publicly announcing that all three indicators are true—or that each belongs to this factive majority-knowledge inventory—would change their information. The additional premise that no easy communication, memory or inferential route supplies the missing indicator is also substantive; ignorance alone does not establish it. Finally, posterior probability is not outright belief, and inventory membership is not group knowledge. Belief thresholds, integration processes and standards of access require their own interpretation. The example proves a separation among these relations rather than a finding about a real organization. [3][r3]

## 2. Evidence profiles and locally possible responses

### 2.1 What scalarization does and does not lose

A profile $`e\in E\subseteq\mathbb R^k`$ can record provenance, semantic coverage, resistance to defeat or other inquiry-specific dimensions. Their names do not make them raw measurements. Choosing a coordinate, its orientation, its units and the assessment that assigns its value can already involve evaluative assumptions. A tuple keeps these commitments visible; it does not certify them. The original epistemic-profile manuscript proposes functionally differentiated operations—perception, memory, source monitoring, defeater recognition and action guidance—whose responses can condition one another. This is an architectural proposal, not a demonstrated partition of a human mind. [4, §§1–4][r4]

For a partially ordered profile space $`(E,\preceq)`$, a real score $`f:E\to\mathbb R`$ can have four different properties:

| Property | Meaning |
|---|---|
| Injectivity | Different profiles have different scores. |
| Monotonicity | $`x\preceq y`$ implies $`f(x)\le f(y)`$. |
| Order reflection | $`f(x)\le f(y)`$ implies $`x\preceq y`$. |
| Sufficiency for $`g:E\to T`$ | There is a readout $`\widehat g:f(E)\to T`$ with $`g=\widehat g\circ f`$. |

**Proposition 1 — Order and target preservation.** A finite nonempty partially ordered set admits a monotone, order-reflecting real score exactly when it is a chain. A score is sufficient for a particular target exactly when that target is constant on every score fibre. [5, §1][r5]

**Proof.** Real numbers are totally ordered. Comparing the scores of any two profiles and reflecting that comparison makes the profiles comparable. Conversely, increasing integer ranks embed a finite chain. For target sufficiency, a readout must give the same answer at equal scores. If the target is constant on each fibre, define the readout at an attained score to be that common value. This defines it on $`f(E)`$; extending it to unattained scores needs an available default target value. ∎

For profiles $`(1,0),(0,1)`$ with coordinatewise order, the sum score collapses their identities but exactly preserves their sum. The score $`x_1+2x_2`$ is injective and monotone on that set, yet manufactures a numerical ordering between incomparable profiles. By contrast, the first coordinate faithfully orders $`(0,0),(1,1),(2,2)`$. An injective encoding of a finite set into the reals preserves every set-theoretic target; its numerical comparisons need not have an epistemic interpretation. Hence neither universal scalar information loss nor universal scalar adequacy follows from dimensionality alone.

A different measure of retained information also cannot replace the target test. For example, an observation with finite range and its finite scalar coarsening both carry their entire probability mass in atoms. That complete atomic-mass property does not distinguish a score that merges opposite target judgments from a sufficient one. An observation-law or measure-theoretic certificate must retain its own property rather than being relabelled as target preservation. [5, §1][r5]

**Proposition 2 — When positive weights reverse a ranking.** For $`x,y\in\mathbb R^k`$, freely variable normalized weights with every coordinate positive can give both strict rankings exactly when $`x-y`$ has at least one positive and one negative coordinate.

**Proof.** A sign-uniform difference cannot reverse under positive weights. When both signs occur, place almost all weight on a positive coordinate to obtain one sign and almost all on a negative coordinate to obtain the other, keeping sufficiently small positive weights elsewhere. ∎

The freely variable weight class matters. With two criteria, write $`d=x-y`$ and restrict $`\alpha\in[\ell,u]\subset(0,1)`$. The score difference is

```math
f(\alpha)=d_2+\alpha(d_1-d_2).
```

Its extrema occur at the endpoints. Opposite strict rankings occur precisely when $`\min(f(\ell),f(u))<0<\max(f(\ell),f(u))`$. Variation in the truth of “$`x`$ strictly outranks $`y`$” needs only $`\min\le0<\max`$: a tie and a strict preference already disagree about that target. For $`d=(1,-1)`$ and $`\alpha\in[3/4,7/8]`$, the ranking never reverses despite the crossing coordinates. These statements disclose dependence on an evaluation rule; they do not establish that every mathematically permitted weighting has normative authority. [5, §1][r5] [6, §§1–3][r6]

There are useful scalar positive cases. In a fixed binary-hypothesis model with positive likelihoods, a supplied prior $`\pi`$ gives

```math
\Pr(H_1\mid x)=
\frac{\pi\Lambda(x)}{\pi\Lambda(x)+1-\pi},
\qquad
\Lambda(x)=\frac{\Pr(x\mid H_1)}{\Pr(x\mid H_0)}.
```

The likelihood ratio is sufficient for every decision determined by that posterior, supplied losses and a supplied tie rule. It need not embed the order of an evidence-quality tuple. Its sufficiency is conditional on the observation model: one independent report of reliability $`.9`$ for a hypothesis and one against it have likelihood ratio $`9(1/9)=1`$; copying the first does not create a third independent report. Treating the copy as independent would falsely change the ratio to $`9`$. Known copying is a model error, not an alternative normative weighting. [6, §3][r6]

### 2.2 Common admission is not a common ranking or permission

A common inquiry can admit records only when schema, units, version and applicability match. Compatibility can preserve recorded source dependence without pretending that admitted records are independent. Two admitted profiles $`(1,0),(0,1)`$ can remain incomparable. They can also be available for analysis when the recipient has no permission to act, or support different repairs with no common safe action. Common admission therefore supplies neither a preferred ordering nor controllability. The bridges among those predicates need to be stated and justified. [5, §2][r5]

### 2.3 Local information determines implementability

Let $`Z`$ be global configurations, $`o_i:Z\to O_i`$ a local observation, $`S_i`$ a nonempty response set, and $`\pi_i:Z\to S_i`$ a prescribed response.

**Proposition 3 — Local implementability.** There is a local response function $`a_i:O_i\to S_i`$ realizing $`\pi_i=a_i\circ o_i`$ on all global configurations exactly when $`\pi_i`$ is constant on every fibre of $`o_i`$. The same statement holds for local histories and history-dependent responses. [5, §3][r5]

**Proof.** A function of a local view cannot distinguish two identical views. Conversely fibre constancy assigns a well-defined response to every attained view. Choose any fixed response for unattained views; nonemptiness of $`S_i`$ permits that extension. ∎

A source-monitoring component may know a bit $`b`$ while an action component sees the same signal at $`b=0`$ and $`b=1`$. If the safe action must be $`\mathrm{repair}_b`$, no local action rule can always succeed. A licensed channel that communicates $`b`$ makes it possible. A centralized description that simply lets the chooser inspect $`b`$ has changed the information architecture.

This does not prove that distributed cognition is formally irreducible. A finite architecture can be represented by a product-state transition system retaining every local state, channel, shared cause and local-policy restriction. Such a flattening preserves its traces. The error is to discard those restrictions or add an oracle. Multiple copies of the same bit also do not become independent evidence merely because they occupy different components. [5, §3][r5]

## 3. The finite strategic model and its limits

### 3.1 A game is additional structure

A strategic model specifies a nonempty finite set of players, nonempty finite strategy sets $`S_i`$, a full product $`S=\prod_iS_i`$ of jointly admissible profiles, and real payoffs $`u_i:S\to\mathbb R`$. The players can represent persons or functionally differentiated loci, but the assignment of strategies and preferences must be defensible. An evidence item or obligation is not a player merely because it appears in a representation. [4, §§4–8][r4] [7, §8][r7]

In a finite extensive-form situation, strategies can be complete contingent plans compatible with each player's information. That compilation must preserve the information structure; replacing contingent plans by bare action labels can give an agent information it does not have. Finite primitive action alphabets also do not make an unlimited temporal policy space finite. Coupled action constraints require separate treatment.

A mixed strategy $`p_i\in\Delta(S_i)`$ is a probability distribution on $`S_i`$. Under independent mixing,

```math
U_i(p)=\sum_{s\in S}u_i(s)\prod_jp_j(s_j).
```

Pure profiles form a Cartesian product. Once strategy bases are chosen, their embedding $`s\mapsto[s_1]\otimes\cdots\otimes[s_n]`$ and the probability tensor $`p_1\otimes\cdots\otimes p_n`$ express the multilinearity of expectation. A general joint law need not factor this way. Tensor notation does not itself supply a game, independence or a theory of cognition.

The interpretation of a probability vector must also be explicit. Repeated random choice, graded endorsement, unresolved competition and frequencies across episodes are different interpretations. The expectation formula and the sampling theorems below concern the declared probabilistic interpretation, not every use of a convex combination. [4, §5][r4]

### 3.2 Existence is conditional stability

**Theorem 4 — Finite mixed equilibrium.** Every game just specified has a nonempty compact set of mixed Nash equilibria. [5, §4][r5] [7, Theorem 8.3][r7] [13][nash] [14][kakutani]

**Proof.** The product $`P=\prod_i\Delta(S_i)`$ is nonempty, compact and convex. For fixed opponents, $`U_i`$ is affine in the player's mixture, so its maximizers form a nonempty compact convex set. Define the product best-response correspondence $`BR:P\rightrightarrows P`$. Its graph is closed: if opponent profiles and maximizing responses converge, continuity passes every maximizing inequality to the limit. Compactness of the codomain supplies upper hemicontinuity. Kakutani's fixed-point theorem gives $`p\in BR(p)`$, precisely the Nash inequalities. The fixed-point set is closed in compact $`P`$, hence compact. ∎

This is the classical Nash–Kakutani argument, not a new existence theorem. Empty values, nonconvex domains, lack of compactness or a discontinuous best-response graph can invalidate its premises. For example, $`F(x)=x/2`$ has no fixed point on $`(0,1)`$; the flip has none on $`\{0,1\}`$; and $`F(0)=1,F(x)=0`$ for $`x>0`$ has none on $`[0,1]`$. A correspondence equal to $`\{1\}`$ below $`1/2`$, $`\{0\}`$ above it and $`\{0,1\}`$ at it has closed graph and nonempty compact values but no fixed point: its value at the midpoint is not convex. [5, §4][r5]

Existence does not give a selection rule, uniqueness, an effective solver or convergence of play. The map $`F(x)=1-x`$ has a fixed point but its iterates from 0 alternate forever. A one-player payoff can even reward a false answer more highly than a true one. The unique equilibrium would then be false under the independently supplied truth predicate.

### 3.3 Changing inquiry can change incentives

Inquiry affects strategic possibilities as well as conclusions. Suppose a fixed analysis offers researchers two actions: independent pre-disclosure discovery $`D`$ and stopping $`S`$. Before public disclosure, both are available and $`D`$ pays 1 while $`S`$ pays 0. The unique equilibrium is $`(D,D)`$. Correct publication changes the public state and makes $`D`$ unavailable by its declared meaning; $`(S,S)`$ becomes the unique equilibrium. The analysis and feasibility rule remain fixed; the state to which they apply changed. If strategy or player sets change, compare equilibria through explicit transport maps or a common tagged space rather than subtracting differently typed sets. [7, Proposition 8.6][r7]

A different example separates correctness from inquiry value. Two researchers choose rapid disclosure $`F`$ or mechanism-rich exposition $`E`$:

| Player 1 / Player 2 | $`F`$ | $`E`$ |
|---|---|---|
| $`F`$ | $`(2,2)`$ | $`(5,0)`$ |
| $`E`$ | $`(0,5)`$ | $`(4,4)`$ |

The action $`F`$ strictly dominates $`E`$, so $`(F,F)`$ is the unique equilibrium, although $`(E,E)`$ benefits both more. Every outcome may disclose the same correct theorem while the fuller exposition supports more future inquiry. These are constructed payoffs, not measurements of researchers' motives. Truth, private incentives and prospective scientific value are different evaluations. [7, §8][r7]

## 4. Vector judgments, teams and representation changes

### 4.1 Two distinct improvement relations

Suppose player $`i`$ has a vector payoff $`V_i(s)\in\mathbb R^{k_i}`$, extended by coordinatewise expectation. Define two sets of equilibrium profiles:

```math
\begin{aligned}
E_{\mathrm{nd}}&=\{p:\text{no unilateral gain lies in }
\mathbb R_{\ge0}^{k_i}\setminus\{0\}\text{ for any }i\},\\
E_{\mathrm{all}}&=\{p:\text{no unilateral gain lies in }
\mathbb R_{>0}^{k_i}\text{ for any }i\}.
\end{aligned}
```

The first excludes improvement in some coordinate without deterioration in any; the second excludes improvement strictly in every coordinate. Thus $`E_{\mathrm{nd}}\subseteq E_{\mathrm{all}}`$. With one player choosing $`(0,0)`$ or $`(1,0)`$, every mixture belongs to the second set, while only the second pure outcome belongs to the first. The original manuscript used a nonzero nonnegative cone in one statement and every-coordinate-strict prose in another. The later analysis correctly separates them; neither interpretation should silently replace the other. [4, §7][r4] [5, §5][r5]

### 4.2 Exact positive-weight characterization

**Theorem 5 — Finite vector equilibria.** For a finite vector-payoff game with independently mixed strategies,

```math
E_{\mathrm{nd}}
=\bigcup_{w_i\in\mathbb R_{>0}^{k_i}}
\mathrm{NE}(w_1\cdot V_1,\ldots,w_n\cdot V_n).
```

In particular $`E_{\mathrm{nd}}`$ is nonempty. A scalar equilibrium with nonnegative nonzero weights guarantees membership in $`E_{\mathrm{all}}`$, but not generally in $`E_{\mathrm{nd}}`$. [5, Propositions on positive scalarization][r5]

**Proof.** A nonzero nonnegative vector has positive dot product with every strictly positive weight vector. Such a profitable vector deviation would contradict scalar equilibrium. Likewise every strictly positive gain has positive dot product with a nonnegative nonzero vector. Choosing strictly positive weights and applying Theorem 4 proves nonemptiness.

For the converse, fix $`p\in E_{\mathrm{nd}}`$ and one player. Against the fixed opponents, let $`d_j`$ be the expected vector gain of pure response $`j`$ relative to the current mixture. Let $`D`$ be the cone generated by these finitely many gains. If $`z=\sum_j a_jd_j`$ were nonzero and nonnegative with $`a_j\ge0`$, then $`A=\sum_j a_j>0`$ and the mixture with weights $`a_j/A`$ would realize gain $`z/A`$, contradicting efficiency. Hence $`D`$ is disjoint from the nonnegative simplex $`K=\{z\ge0:\sum z_j=1\}`$.

The finitely generated cone $`D`$ is closed and convex; $`K`$ is compact and convex. Strict separation provides $`w`$ with $`w\cdot d\le0`$ for all $`d\in D`$ and $`w\cdot z>0`$ on $`K`$. The first bound follows from conicity and $`0\in D`$; evaluating the second on the coordinate vectors shows every coordinate of $`w`$ is positive. Thus every pure deviation, and therefore every mixed deviation, has nonpositive scalar gain. Choose such weights separately for each player. The selected profile is scalar Nash. ∎

The weights can depend on both player and equilibrium. They are existence witnesses, not canonical epistemic trade-offs. The distinction between Pareto and weak Pareto criteria also appears in the weighted-game literature. Robust models that supply a set of possible weights solve a different optimization problem; their broader hypotheses do not replace this finite-polyhedral converse. [16][weighted] The zero-weight distinction is sharp: weights $`(0,1)`$ make both outcomes $`(0,0),(1,0)`$ optimal while the first is dominated.

Finite convexification matters. Among just the three pure outcomes $`(3,0),(1,1),(0,3)`$, the middle is Pareto efficient but maximizes no positive weighted sum. Once mixtures are allowed, the half-mixture of the extremes gives $`(1.5,1.5)`$ and dominates it. Even compact convex infinite payoff sets need not have the strictly positive support property. In

```math
C=\{(x,y):0\le y\le1,\ -1\le x\le-y^2\},
```

$`(0,0)`$ is efficient, but for any $`w_1,w_2>0`$, a sufficiently small $`t>0`$ gives $`w\cdot(-t^2,t)>0`$. Only a boundary weight such as $`(1,0)`$ supports the origin. The finite-polyhedral hypothesis cannot be replaced by compactness and convexity alone. [5, §5][r5]

### 4.3 Team optimality and a restrictive concavity condition

When all players share a scalar payoff $`W`$, every global maximizer is Nash. The converse fails: if $`W(0,0)=2`$, $`W(1,1)=1`$ and the off-diagonal values are zero, both diagonal profiles are Nash. If a coupled constraint permits only these two profiles, each can also be stable because no unilateral feasible move exists. A constrained game is not the ordinary product-simplex problem.

**Theorem 6 — Joint concavity eliminates finite payoff interaction.** For the independent mixed extension of a finite common-payoff table on the full product of simplices, joint concavity, joint convexity, joint affinity and additive separability of the pure payoff table are equivalent. [5, team-concavity proposition][r5]

**Proof.** Fix two players, two responses each, and pure responses of all others. Write the four payoffs as $`a,b,c,d`$ in rectangular order. The midpoint obtained by mixing each player equally has value $`(a+b+c+d)/4`$. Concavity along each of the two diagonals implies both $`b+c\ge a+d`$ and $`a+d\ge b+c`$. Hence every conditional two-player mixed difference is zero. Relative to a fixed baseline $`r`$, the increment from changing one player's response is independent of the others' responses. Telescoping therefore gives

```math
w(s)=w(r)+\sum_i\bigl[w(r_{-i},s_i)-w(r)\bigr].
```

Its mixed extension is jointly affine, hence convex and concave. Convexity gives the same diagonal equality with the inequalities reversed, proving all implications. ∎

Affineness in a player's own mixture is automatic in finite games and is much weaker. Joint concavity is not a harmless way to preserve genuine team-payoff interaction while obtaining global optimality. The full-product hypothesis is essential: $`W(p,q)=1-p-q+3pq`$ restricted to $`p+q=1`$ becomes the concave function $`3p(1-p)`$. A joint-law simplex is another geometry, on which expected payoff is linear in the joint law. Without marginal or other restrictions, that change cannot improve the maximum common payoff: a maximizing pure joint profile was already available. Correlation becomes valuable when implementation constraints exclude that simple solution. [5, §5][r5]

A sequential pipeline can instead consist of transformations and a terminal criterion without any preferences or profitable deviations. Giving its components game-theoretic names adds no result unless the strategic interpretation is warranted.

### 4.4 Which re-encodings preserve which conclusions?

Coordinate permutations and coordinatewise strictly increasing bijections preserve deterministic coordinatewise order. Transporting schemas, units, admission rules and target readouts preserves their corresponding judgments. But applying a nonlinear transformation to pure payoffs before averaging need not preserve mixed equilibria. [5, §6][r5]

For example, give player 1 payoff matrix $`\left(\begin{smallmatrix}0&2\\1&0\end{smallmatrix}\right)`$ and player 2 payoff matrix $`\left(\begin{smallmatrix}1&0\\0&1\end{smallmatrix}\right)`$. At the unique fully mixed equilibrium, row-0 probability is $`1/2`$ and column-0 probability is $`2/3`$: player 2 is indifferent at equal row probabilities, and player 1 satisfies $`2(1-q)=q`$. Squaring player 1's nonnegative pure payoffs preserves their order but changes its equation to $`4(1-q)=q`$, hence $`q=4/5`$.

By contrast, strategy relabellings and positive affine scalar payoff changes preserve Nash equilibria: they biject unilateral deviations and multiply each gain by a positive constant. For vector games, an invertible affine change $`V_i'=A_iV_i+b_i`$ preserves either specified improvement relation when the cone is transported to $`A_iC_i`$. A change of units $`e'=De`$ preserves a scalar score only if its weights change to $`w'=D^{-T}w`$. Retaining old weights after changing units changes the comparison rule. [5, §6][r5] [7, Proposition 8.4][r7]

## 5. Strategically sufficient information and hard coordination

### 5.1 Retaining incentives rather than every payoff level

Suppose payoffs depend on a reference state $`x`$. For a pure profile $`s`$ and unilateral response $`b_i`$, define the gain observable

```math
g_{i,b_i,s}(x)=u_i(x,b_i,s_{-i})-u_i(x,s).
```

These differences, together with the relevant information branches and feasible strategies, determine the incentive comparisons. An offset depending only on the opponents' actions changes payoff levels without changing player $`i`$'s unilateral gains. A representation intended only to preserve Nash incentives can therefore need less information than one recovering every payoff. [8, Proposition 7][r8]

Define regret by

```math
\mathrm{Reg}_i^U(p)
=\max_{b_i\in S_i}U_i(b_i,p_{-i})-U_i(p).
```

It is nonnegative, and all regrets vanish exactly at Nash equilibria. Mixed deviations cannot exceed the best pure deviation because their payoffs are convex combinations.

**Proposition 7 — Incentive-error transport.** If a genuinely specified approximate game estimates every pure unilateral expected gain within $`\eta_i`$, then

```math
\mathrm{Reg}_i^{\mathrm{reference}}(p)
\le\mathrm{Reg}_i^{\mathrm{approximate}}(p)+\eta_i.
```

**Proof.** The mixed gain for each pure deviation is a probability-weighted average of its pure-profile gains. Its error is therefore at most $`\eta_i`$. Taking the maximum preserves that bound. ∎

If instead each payoff entry is known within $`\varepsilon_i`$, subtracting two entries gives $`\eta_i=2\varepsilon_i`$ and the familiar bound $`\delta_i+2\varepsilon_i`$ for a $`\delta_i`$-equilibrium of the approximation. Direct gain estimation can be more focused, but independently fitted gains need not come from a consistent payoff table. The existence theorem still needs an actual game. Likewise $`\lambda(x)\prod_i p_i(s_i)`$ requires independence between reference uncertainty and strategic randomization; state-dependent action belongs in contingent strategies or an explicit observation model. [7, Proposition 8.5][r7] [8, §6][r8]

### 5.2 A hidden interaction changes the equilibrium

Let $`x\in\{-1,1\}^n`$, $`n\ge2`$, and let $`\lambda_+,\lambda_-`$ be uniform on the two opposite parity classes. Every proper-subset marginal is the same: fixing fewer than all coordinates leaves an unobserved coordinate whose sign flip bijects the two parity classes. Permit the pairwise updates $`x_1\leftarrow x_1x_j`$ for $`j=2,\ldots,n`$. After these $`n-1`$ updates, $`x_1`$ equals the original full parity. Thus the binary target

```math
B=\frac{1-x_1^{\mathrm{final}}}{2}
```

is certainly 0 under $`\lambda_+`$ and certainly 1 under $`\lambda_-`$. Pairwise operations have made a previously hidden higher-order relation decisive for a unary question. [8, §4][r8]

Give two players actions 0 and 1 and payoffs

```math
u_i(x,s)=\mathbf1\{s_i=B(x)\}
+c\mathbf1\{s_1=s_2\},\qquad 0\lt{}c<1.
```

**Proposition 8 — Hidden reference games.** The reference games have unique equilibria $`(0,0)`$ and $`(1,1)`$. For any fixed independent mixed recommendation, each player has regret at least $`(1-c)/2`$ in at least one of the two games. [8, Proposition 6][r8]

**Proof.** The correct action gains at least $`1-c>0`$ against either opponent action, so it is strictly dominant. If player $`i`$ chooses 1 with probability $`p_i`$, its wrong-action probabilities in the two games are $`p_i`$ and $`1-p_i`$. Deviation to the correct action gains at least $`1-c`$ times that probability. Their maximum is at least $`(1-c)/2`$. ∎

A rule seeing only the shared proper-subset summary cannot distinguish the two games and identify both reference equilibria. The game witnessing the regret bound can differ by player. The conclusion does not exclude further observation or later conditioning; it identifies exactly what the retained representation failed to determine.

### 5.3 Independent feasibility is a support property

**Proposition 9 — Hard joint constraints.** For finite nonempty action sets, feasible set $`F\subseteq\prod_iS_i`$ and independent mixtures,

```math
\Pr_p(s\in F)=1
\quad\Longleftrightarrow\quad
\prod_i\mathrm{supp}(p_i)\subseteq F.
```

**Proof.** Every tuple in the product of the supports has positive probability. A forbidden such tuple produces positive violation probability; conversely no unsupported tuple can be sampled. ∎

Two actors who can each use an exclusive resource have locally admissible actions $`\{0,1\}`$ but joint feasible set $`\{(0,0),(1,0),(0,1)\}`$. Positive independent use probabilities violate the constraint. An allocator or a restricted product of strategies can repair this, but a finite penalty does not make the forbidden outcome impossible. [7, Counterexample 8.2][r7] [8, §7][r8]

For $`n\ge2`$, let $`u_i(s)=cs_i-M\prod_j s_j`$ with $`M>c>0`$, and forbid the all-one tuple. The pure equilibria are exactly profiles with $`n-1`$ active players: fewer allow an inactive player to gain $`c`$; all active makes deactivation profitable; at $`n-1`$, neither an active nor inactive player gains by switching. Yet the symmetric mixed equilibrium

```math
p_i=(c/M)^{1/(n-1)}
```

makes every player indifferent because its activation gain is $`c-M\prod_{j\ne i}p_j=0`$. Its violation probability is $`(c/M)^{n/(n-1)}>0`$. This refutes a guarantee that every finite-penalty equilibrium respects a hard constraint; it does not say that every penalized game is unsafe. [8, §7][r8]

### 5.4 The information needed for coordinated diversity

Let feasible sign outputs have even parity,

```math
F_+=\{z\in\{-1,1\}^n:\prod_i z_i=1\},\qquad n\ge2.
```

Under independent mixing with $`p_i=\Pr(z_i=-1)`$,

```math
\Pr(z\notin F_+)
=\frac{1-\prod_i(1-2p_i)}2.
```

Indeed the expectation of the product sign is both $`\prod_i(1-2p_i)`$ and the difference between even- and odd-parity probabilities. If $`p_i\in[\eta,1-\eta]`$, $`0<\eta\le1/2`$, then

```math
\Pr(z\notin F_+)\ge\frac{1-(1-2\eta)^n}{2},
```

with equality when all $`p_i=\eta`$. Unbiased independent marginals give failure probability $`1/2`$, while the uniform law on $`F_+`$ has the same unary marginals and never fails. [8, §7][r8]

**Proposition 10 — Exact shared-variable requirement.** If a finite shared variable $`Z`$ generates the uniform law on $`F_+`$ through outputs conditionally independent given $`Z`$, then

```math
|\mathrm{supp}(Z)|\ge2^{n-1},
\qquad H(Z)\ge n-1\text{ bits}.
```

**Proof.** Every nonempty Cartesian rectangle contained in $`F_+`$ is a singleton: varying any one coordinate while fixing the others flips parity. A positive mixture component cannot assign mass outside $`F_+`$, since nonnegative components cannot cancel forbidden mass. Each conditional product component therefore has singleton support. Every feasible tuple needs a positive component, and the output tuple is a deterministic function of $`Z`$. Its entropy is $`n-1`$ bits, so both bounds follow. Taking $`Z`$ itself uniformly distributed on the feasible tuples attains them. ∎

The bound concerns this shared-latent implementation. It is not a count of minds, persons or independent evidential sources. Interactive communication changes the resource model. Its practical content is that independent local diversity and a nonrectangular hard joint condition need a coordinating or restricting mechanism; an equilibrium certificate alone supplies none. [8, §7][r8]

## 6. Complete coordination records across a growing horizon

The finite parity example concerns one joint output law. A different coordination problem asks how much information a complete mediating record must carry as a horizon grows. Its probability and mediation hypotheses must be supplied independently; the following Gaussian results are not universal statements about memory, brains or physical resources. [9][r9]

### 6.1 Bounded capture forces information growth

For each positive integer $`n`$, let $`P_n`$ be a countably additive Borel law of real variables $`(Y_n,S_n)`$, with $`S_n\sim N(0,n)`$. Suppose $`X_0=Y_n+S_n`$ has the same terminal distribution at every horizon considered. Let $`Q_n`$ be the product of the two marginals. For an interval $`I`$ of length $`L>0`$, put

```math
p=P_n(Y_n+S_n\in I),
\qquad q_n=Q_n(Y_n+S_n\in I).
```

Here $`p`$ is independent of the horizon because the terminal law is fixed. The maximum probability that a centered normal of variance $`n`$ assigns to a length-$`L`$ interval is

```math
a_n(L)=2\Phi\!\left(\frac{L}{2\sqrt n}\right)-1
\le\frac{L}{\sqrt{2\pi n}}.
```

The centered interval is maximal because the normal density decreases away from zero; shifting an interval toward zero replaces lower-density mass by higher-density mass. Integrating this bound over the independent $`Y_n`$ marginal gives $`0<q_n\le a_n(L)<1`$.

Use natural logarithms and information in nats. Define mutual information by relative entropy,

```math
I(Y_n;S_n)=D(P_n\Vert Q_n)\in[0,\infty].
```

The value is infinite if $`P_n`$ is not absolutely continuous with respect to $`Q_n`$. Otherwise it is the integral of $`f\log f`$, $`f=dP_n/dQ_n`$, with $`0\log0=0`$. This definition needs no joint Lebesgue density or finite differential entropy.

**Theorem 11 — Gaussian coordination information.** Write $`h(p)=-p\log p-(1-p)\log(1-p)`$, with the usual zero conventions. Then

```math
I(Y_n;S_n)
\ge\frac p2\log n
-p\log\!\left(\frac L{\sqrt{2\pi}}\right)-h(p).
```

If the fixed terminal law is any Borel probability on the real line, then

```math
\liminf_{n\to\infty}\frac{I(Y_n;S_n)}{\log n}\ge\frac12.
```

**Proof.** For the sum event $`E`$, convexity of $`f\log f`$ applied separately on $`E`$ and its complement gives binary data processing:

```math
D(P_n\Vert Q_n)
\ge p\log\frac p{q_n}
+(1-p)\log\frac{1-p}{1-q_n}
\ge p\log\frac1{q_n}-h(p).
```

If absolute continuity fails, the infinite left side makes the inequality immediate. Insert the Gaussian bound for $`q_n`$ to obtain the first result. Every Borel probability on $`\mathbb R`$ is tight. For each $`\varepsilon>0`$, choose one bounded interval with terminal probability at least $`1-\varepsilon`$, before allowing $`n`$ to grow. Dividing the first bound by $`\log n`$ gives lower limit at least $`(1-\varepsilon)/2`$. Let $`\varepsilon\downarrow0`$. ∎

The finite-horizon right side can be negative, in which case nonnegativity supplies a better lower bound. Tightness alone gives no uniform additive constant or convergence rate. If a singleton terminal event has positive mass, its product-marginal benchmark probability is zero, so mutual information is infinite at that horizon; one must not substitute $`L=0`$ in the logarithmic expression. If $`S_n`$ is the measurable sum of a larger future block $`B_n`$, data processing also gives $`I(Y_n;B_n)\ge I(Y_n;S_n)`$. [9, §§1–2][r9]

### 6.2 A consistent sharp example

Let $`A\sim N(0,\tau^2)`$, $`0<\tau^2<\infty`$, independent of a two-sided sequence of ordinary independent standard normal increments. Define positions by finite forward and backward sums from $`X_0=A`$. At horizon $`n`$, set $`Y_n=A-S_n`$. This is one consistent anchored recurrence, with

```math
\mathrm{Var}(Y_n)=\tau^2+n,
\quad \mathrm{Var}(S_n)=n,
\quad \mathrm{Cov}(Y_n,S_n)=-n,
\quad \mathrm{Var}(Y_n\mid S_n)=\tau^2.
```

The log density ratio of $`Y_n\mid S_n`$ to $`Y_n`$ has expected value

```math
I(Y_n;S_n)
=\frac12\log\frac{\tau^2+n}{\tau^2}
=\frac12\log(1+n/\tau^2).
```

To see the cancellation, write the two normal log densities: their expected standardized quadratic terms are both one, leaving half the logarithm of the variance ratio. The asymptotic coefficient is exactly $`1/2`$. When $`\tau=0`$, the joint law lies on $`y=-s`$ and the product law gives that line zero mass, so information is infinite instead.

This anchored construction does not make the state independent of future increments. Even conditional on $`A`$, the relation $`Y_n=A-S_n`$ remains. A finite description of that formula is not a finite information channel mediating its dependence. Nor is this example a fresh forward-innovation law. [9, §3][r9]

### 6.3 The mediator must include every operative route

Suppose a discrete record $`R_n`$ mediates all dependence in the exact sense

```math
Y_n\perp S_n\mid R_n.
```

For standard Borel variables, the information chain rule gives

```math
I(Y_n;S_n)
\le I(Y_n,R_n;S_n)
=I(R_n;S_n)
\le H(R_n).
```

The first inequality follows by adding conditional mutual information, and conditional independence supplies the equality. Thus a uniformly bounded complete-record entropy cannot support fixed positive bounded capture at all horizons. If $`H(R_n)\le C`$, a necessary finite-horizon condition is

```math
n\le\frac{L^2}{2\pi}
\exp\!\left(\frac{2(C+h(p))}{p}\right),\qquad p>0.
```

This is necessary, not sufficient. It also applies to countably infinite records with bounded entropy. A bound on $`I(R_n;S_n)`$ can replace entropy even for a nondiscrete record; differential entropy is not itself a channel-capacity bound. [9, §4][r9]

With side information $`U_n`$, complete mediation instead requires conditional independence given $`(R_n,U_n)`$, and the corresponding bound is

```math
I(Y_n;S_n)
\le I(U_n;S_n)+H(R_n\mid U_n).
```

The record alone is insufficient when a prior resource carries uncontrolled dependence. A controller with finitely many instantaneous states can use an accumulating transcript, a clock or an external correlated resource. A quantized readout of a real state does not bound the information of the state itself. Program length, a law's description length and a complete mediating record are different quantities. The theorem applies only after the actual cut is established. [9, §4][r9]

### 6.4 Exact finite-alphabet capacity

**Theorem 12 — Sharp fixed-horizon capture.** Fix $`n>0`$, an interval $`I`$ of finite length $`L\ge0`$, and an integer $`N\ge1`$. Among countably additive joint laws with $`S\sim N(0,n)`$ admitting a mediator $`M`$ of at most $`N`$ values with $`Y\perp S\mid M`$,

```math
\Pr(Y+S\in I)
\le 2\Phi\!\left(\frac{NL}{2\sqrt n}\right)-1.
```

For $`L>0`$, optimizing the state marginal and encoder at this one horizon attains the bound. [9, §5][r9]

**Proof.** Discard zero-probability labels. For each remaining label let $`\nu_m`$ be the conditional law of $`Y`$, and let $`\lambda_m(B)=\Pr(M=m,S\in B)`$. These finite measures sum to the Gaussian law $`\gamma_n`$ and each is dominated by it, hence nonatomic. Conditional independence gives

```math
\Pr(Y+S\in I)
=\sum_m\int\lambda_m(I-y)\,d\nu_m(y)
\le\sum_m\sup_y\lambda_m(I-y).
```

For $`\varepsilon>0`$, choose for each label an interval translate $`J_m`$ within $`\varepsilon/N`$ of its supremum. Then

```math
\sum_m\lambda_m(J_m)
\le\sum_m\lambda_m\!\left(\bigcup_jJ_j\right)
=\gamma_n\!\left(\bigcup_jJ_j\right).
```

The union has length at most $`NL`$. A centered interval of that length maximizes Gaussian mass among Borel sets with that measure: density outside the interval is at most its boundary density, density on a missing interior portion is at least that value, and the exterior portion has no more measure than the missing portion. Therefore the last quantity is at most $`a_n(NL)`$. Let $`\varepsilon\downarrow0`$. No maximizing translate was presumed. For $`L=0`$, every translated singleton is null under each $`\lambda_m`$, giving zero directly.

For attainment when $`L>0`$, partition a centered interval $`J`$ of length $`NL`$ into $`N`$ adjacent length-$`L`$ cells $`J_m`$. Draw $`S`$ normally; assign it label $`m`$ in $`J_m`$ and label 1 outside $`J`$. Choose constants $`y_m`$ with $`I-y_m=J_m`$, and set $`Y=y_M`$. Conditional independence is automatic because $`Y`$ is constant given $`M`$. Capture occurs exactly on $`J`$ up to null endpoints; exterior points assigned label 1 add no capture. ∎

Thus capture probability at least $`0<p<1`$ with $`L>0`$ requires

```math
N\ge\left\lceil\frac{2\sqrt n}{L}
\Phi^{-1}\!\left(\frac{1+p}{2}\right)\right\rceil.
```

Probability-one bounded capture is impossible for finite $`N,L`$. This square-root growth is sharper than the alphabet bound obtained by combining Theorem 11 with $`H(M)\le\log N`$. The extremizer is a retrospective, single-horizon construction. It does not preserve an independently specified state marginal, fixed terminal law or one common history at every horizon, and it is not a forward-causal physical implementation.

### 6.5 A sharp approximation-error budget

The later correction separates an approximate law from the countably additive reference to which the Gaussian theorem applies. Let $`Q`$ meet Theorem 12 and put $`a=a_n(NL)`$. On the same event algebra let $`P`$ be a probability law, possibly only finitely additive, with

```math
\sup_A|P(A)-Q(A)|\le\eta,\qquad0\le\eta\le1.
```

**Theorem 13 — Robust finite mediation.** For $`E=\{Y+S\in I\}`$,

```math
P(E)\le\min(1,a+\eta).
```

The one-event inequality $`|P(E)-Q(E)|\le\eta`$ already suffices. For every nonempty target interval, the bound is sharp at one horizon, even when $`P`$ retains the same Gaussian $`S`$ marginal. [10][r10]

**Proof.** The upper bound follows from $`P(E)\le Q(E)+\eta\le a+\eta`$ and $`P(E)\le1`$. No entropy or conditional probability under $`P`$ is used.

For $`L>0`$, take the extremizing $`Q`$ above and let $`\delta=\min(\eta,1-a)`$. The Gaussian law is nonatomic, so choose a Borel set $`C\subseteq\mathbb R\setminus J`$ of mass $`\delta`$. Keep $`S`$ unchanged. On $`C`$, replace the state by $`Y'=c-S`$ for a fixed $`c\in I`$; elsewhere leave it alone. The new law $`P`$ has capture $`a+\delta`$. This coupling changes the pair only on a set of probability $`\delta`$, so event total variation is at most $`\delta`$. The capture event's probability changes by exactly $`\delta`$, proving equality and sharpness. For a nonempty singleton target, the same alteration on a Gaussian set of mass $`\eta`$ gives capture $`\eta`$ while every finite-mediator reference has capture zero. An empty target always has capture zero. ∎

The modified law generally loses the reference's finite complete mediator; that is what the error allowance permits. If $`P(E)\ge p`$, $`L>0`$ and $`0<p-\eta<1`$, then

```math
N\ge\left\lceil\frac{2\sqrt n}{L}
\Phi^{-1}\!\left(\frac{1+p-\eta}{2}\right)\right\rceil.
```

When $`p\le\eta`$ there is no positive alphabet-size conclusion; when $`L=0`$ one only obtains $`p\le\eta`$; and $`p-\eta=1`$ is impossible for finite $`N,L`$. The Gaussian marginal and complete-mediation assumptions belong to $`Q`$. Allowing finite additivity in the event-transport step does not transport Gaussian entropy or conditional independence to $`P`$. All attainment claims retain their fixed-horizon and retrospective scope. [10][r10]

## 7. Temporal learning, coordinated restoration and model transfer

### 7.1 A mixed equilibrium need not restore a target

Suppose a finite joint response set $`S`$ carries a fixed law $`\mu`$, sampled independently at each time, and let $`T\subseteq S`$ be a separately supplied target.

**Theorem 14 — Repeated independent deployment.**

```math
\Pr(\text{eventually always in }T)=1
\quad\Longleftrightarrow\quad \mu(T)=1.
```

If $`\mu(T)<1`$, eventual target persistence has probability zero. [5, §7][r5]

**Proof.** A target-supported law remains in the target at every time with probability one. Otherwise the bad probability is some $`p>0`$. For any fixed time $`N`$, the probability of no bad draw in the next $`m`$ steps is $`(1-p)^m\to0`$. The probability of no bad draw after $`N`$ is zero. Eventual persistence is the countable union of these null events over $`N`$. ∎

In the two-player agreement game, both players independently mixing $`(1/2,1/2)`$ is Nash. Repeated independent deployment mismatches with probability $`1/2`$ each round and infinitely often almost surely. A shared fair bit choosing $`(0,0)`$ or $`(1,1)`$ has the same individual marginals and always agrees. It is a different joint law. Neither mechanism's agreement alone establishes truth, cognitive implementation or the authority of the common signal.

### 7.2 What does guarantee progress?

A separate temporal argument can establish entry and persistence. Suppose a licensed stochastic update process has a nonnegative integer rank $`R`$, an invariant target, no rank increase outside target, and conditional expected rank decrease at least $`\varepsilon>0`$ after every non-target history. Let $`\tau`$ be first target entry and $`R_0<\infty`$ the fixed initial rank. Then

```math
\mathbb E\tau\le R_0/\varepsilon,
\qquad\Pr(\tau<\infty)=1.
```

**Proof.** Stop the rank at target entry. Conditional expected decrease at step $`t`$ is at least $`\varepsilon\mathbf1\{\tau>t\}`$. Sum expectations through $`n-1`$ and use nonnegativity of the stopped rank:

```math
\varepsilon\sum_{t=0}^{n-1}\Pr(\tau>t)
=\varepsilon\mathbb E\min(\tau,n)\le R_0.
```

Monotone convergence yields the expectation bound and excludes positive probability of infinite entry time. Target invariance supplies persistence. If every non-target transition instead decreases the integer rank strictly, the stronger sure bound $`\tau\le R_0`$ follows. ∎

A geometric self-loop distinguishes the conclusions: it has positive expected progress and almost-sure entry but admits an infinite sequence of idle outcomes. An arbitrary controller switch can also reset a rank. The common progress certificate and its history-relative premises are additional scientific obligations, not consequences of the equilibrium label. [5, §7][r5]

For deterministic finite dynamics, a related result identifies the evaluation that progress tracks. Let $`X`$ be a nonempty finite set, $`G:X\to X`$ a transition and $`W:X\to\mathbb R`$ an independently supplied evaluation. Put $`M=\arg\max W`$. If $`W(Gx)>W(x)`$ outside $`M`$ and $`G(M)\subseteq M`$, every trajectory enters $`M`$ within $`|X\setminus M|`$ transitions and remains there. A pre-entry trajectory cannot repeat a state because $`W`$ strictly rises; there are only that many nonmaximum states. If maxima are additionally fixed pointwise, then $`\mathrm{Fix}(G)=M`$. [6, §4][r6]

Equality of fixed points and maxima alone is weaker. Take $`X=\{0,1,2\}`$, $`W=(1,0,0)`$ and $`G(0)=0,G(1)=2,G(2)=1`$. Its only fixed point is its unique maximum, but the other states cycle forever. Weak ascent permits a nonmaximal fixed point; dropping target closure permits later exit; dropping pointwise fixation can leave a cycle entirely inside the maximizing set. Distinguishing these conditions preserves the difference between convergence of states and satisfaction of a target.

Finally, a finite ordinal-potential game has no infinite strict-improvement path: each unilateral improvement strictly raises one common potential on a finite set. This is the classical finite-improvement property. It does not cover idle transitions, changing games or disturbances without further hypotheses. [15, Lemma 2.3][potential]

### 7.3 The exact cost of incompatible response marginals

The independent-deployment example leaves a constructive question: when can a coordinator retain the agents' specified marginal responses while making their joint response appropriate? Fix finite nonempty response sets $`A,B`$, probability laws $`\mu,\nu`$, and a supplied target relation $`R\subseteq A\times B`$. A coupling is a nonnegative joint table $`\kappa`$ with those two complete marginals. This section initially permits every pair in $`A\times B`$; hard exclusions are an additional constraint. For $`U\subseteq A`$, let

```math
R[U]=\{b\in B:\text{some }a\in U\text{ satisfies }(a,b)\in R\},
\qquad
\delta(\mu,\nu,R)=
\max_{U\subseteq A}\bigl(\mu(U)-\nu(R[U])\bigr).
```

The empty subset gives $`\delta\ge0`$, and $`\delta\le1`$. Zero-probability atoms are allowed in this mathematical statement. [17, §1][r13]

**Theorem (sharp marginal obstruction).** The minimum target-violation probability over all couplings is exactly $`\delta(\mu,\nu,R)`$. In particular, a coupling supported on $`R`$ exists if and only if

```math
\mu(U)\le\nu(R[U])
\quad\text{for every }U\subseteq A.
```

**Proof.** Under any coupling, mass starting in $`U`$ can stay within the relation only by arriving in $`R[U]`$. That arrival region has total capacity $`\nu(R[U])`$, so at least $`\mu(U)-\nu(R[U])`$ of the mass must violate the relation. Maximizing over $`U`$ proves the lower bound.

For attainment, form a finite transportation network. A source supplies row $`a`$ with capacity $`\mu(a)`$, a column $`b`$ drains to the sink with capacity $`\nu(b)`$, and every pair in $`R`$ has a row-to-column edge of capacity 2. A cut of capacity at most one exists. Thus a minimum cut cannot cross a relation edge. If $`U`$ is its source-side row set, its source-side column set must contain $`R[U]`$; among these choices, taking exactly $`R[U]`$ minimizes the cut. Its capacity is

```math
\sum_{a\notin U}\mu(a)+\sum_{b\in R[U]}\nu(b)
=1-\mu(U)+\nu(R[U]).
```

The max-flow/min-cut theorem therefore supplies an $`R`$-supported subcoupling of mass $`1-\delta`$. [22][flow] Its residual row masses $`r_a`$ and column masses $`s_b`$ are nonnegative and each total $`\delta`$. If $`\delta=0`$, the subcoupling is already complete. Otherwise add the table $`r_as_b/\delta`$. A positive residual row and positive residual column cannot be related: adding the smaller residual along that relation edge would augment the maximum flow. The added mass therefore lies entirely outside $`R`$, and its total is exactly $`\delta`$. Both full marginals are restored. ∎

For binary agreement, $`R=\{(0,0),(1,1)\}`$, the deficit is $`|\mu(0)-\nu(0)|`$. Marginals $`(4/5,1/5)`$ and $`(1/5,4/5)`$ force disagreement probability $`3/5`$. The joint table with masses $`1/5,3/5,0,1/5`$ in the order $`00,01,10,11`$ attains it. Equal fair marginals have zero deficit, even though independent sampling disagrees with probability $`1/2`$. The marginals do not determine the deployed coupling.

#### Licenses and incentives restrict the available couplings

If only pairs in a set $`L\subseteq A\times B`$ are licensed, the admissible joint law must be supported on $`L`$. The unrestricted deficit remains a lower bound but need not be attainable. With fair binary marginals and target $`R=\{(0,0)\}`$, the unrestricted optimum is $`1/2`$. If $`(1,1)`$ is forbidden, the marginal equations force both diagonal masses to zero. The only licensed law gives each off-diagonal pair mass $`1/2`$, and its target violation is one. An unavailable completion cannot be repaired by interpreting a probability constraint as permission.

Incentive compatibility is a further condition when the response loci are strategic players. For scalar payoffs $`u_1,u_2`$, a common recommendation law is a correlated equilibrium when obeying a received recommendation is at least as profitable as switching it. The first player's inequalities are

```math
\sum_{b\in B}\kappa(a,b)
\bigl(u_1(a,b)-u_1(a',b)\bigr)\ge0
\quad(a,a'\in A),
```

with the corresponding column inequalities for the second player. These are the unconditional form of recommendation-conditional comparisons; a recommendation of zero mass creates no additional obligation. Correlated equilibrium belongs to established game theory. [23][aumann] The information contract here gives each player its own recommendation and the declared game. Additional current private signals, sequential observation of other actions or a richer deviation menu require the appropriate conditional incentive constraints. These inequalities do not automatically cover that enlarged game. [17, §4][r13] [21, §C2][r17]

In matching pennies, let player 1 receive one for agreement and player 2 one for disagreement. A fair diagonal coupling implements agreement perfectly but gives player 2 a profitable deviation from each recommendation. With fixed fair marginals, write the four masses as $`t,1/2-t,1/2-t,t`$. Player 1's obedience requires $`t\ge1/4`$; player 2's requires $`t\le1/4`$. Hence the only compliant joint law is uniform and its agreement-target violation is $`1/2`$. If both players instead receive one for agreement, the diagonal law is an equilibrium. Feasibility of correlation does not determine its incentive properties.

For general binary marginals $`p=\mu(0)`$ and $`q=\nu(0)`$, every coupling is

```math
\kappa=
\begin{pmatrix}
t&p-t\\
q-t&1-p-q+t
\end{pmatrix},
\qquad
\max(0,p+q-1)\le t\le\min(p,q).
```

Each hard exclusion forces a cell to zero, and each recommendation inequality gives a linear bound on $`t`$. Their intersection is a closed interval or is empty. Target-violation mass is affine in $`t`$, so an endpoint minimizes it whenever the interval is nonempty. Requiring the inequalities under every member of a declared finite collection of payoff standards gives an exact robust version. Averaging standards instead requires its own justified probability interpretation. Neither calculation establishes the authority of the supplied standards.

More generally, let $`\mathcal C`$ be the nonempty compact polytope of couplings satisfying the supplied marginals, licenses and incentive inequalities. Then

```math
\delta^*=\min_{\kappa\in\mathcal C}\kappa(R^c)
```

exists and satisfies $`\delta\le\delta^*`$. An empty feasible polytope means that the response contract is not implementable; it is not assigned an artificial infinite violation probability. A selected joint table still needs a realizable sampler and the channels through which recommendations or coordinated actions are implemented.

Pairwise compatibility also falls short of global compatibility. For three binary loci with fair marginals, each pair has a perfectly anticorrelated coupling. No triple can make all three pairs different, since three binary values cannot be pairwise distinct. Every pairwise marginal test passes while the proposed global target is empty. Multiway coordination needs an actual joint law. A shared random source can supply correlation but does not multiply independent evidence or create new permission to coordinate. [17, §5][r13]

### 7.4 Restoration under dependent repeated responses

The stationary independent case in Theorem 14 has an exact extension to history-dependent responses. Let $`(\mathcal F_t)_{t\ge0}`$ be a filtration containing the decision history before the next response. At time $`t`$, the target $`R_t`$, response marginals $`\mu_t,\nu_t`$ and any admissible coupling polytope are measurable with respect to $`\mathcal F_t`$. The realized response pair is recorded by $`\mathcal F_{t+1}`$. In particular,

```math
V_t=\{(A_t,B_t)\notin R_t\}\in\mathcal F_{t+1},
\qquad
p_t=\Pr(V_t\mid\mathcal F_t).
```

The next pair must have the specified marginals **conditional on this decision history**. Unconditional one-time marginal statements are insufficient. Under this contract $`p_t\ge\delta_t=\delta(\mu_t,\nu_t,R_t)`$, or $`p_t\ge\delta_t^*`$ for the constrained problem. No independence across time is assumed. [17, §2][r13]

**Theorem (adapted-event restoration threshold).** Almost surely,

```math
\{V_t\text{ occurs only finitely often}\}
=
\left\{\sum_{t=0}^{\infty}p_t\lt{}\infty\right\}.
```

On paths where the compensator diverges, the accumulated violation count is asymptotic to that compensator. This is Lévy's conditional Borel–Cantelli theorem, with the adaptation premise made explicit. [24, Theorem 11][conditional-bc]

**Proof.** Put $`C_n=\sum_{t<n}\mathbf1_{V_t}`$ and $`H_n=\sum_{t<n}p_t`$. The differences $`D_{t+1}=\mathbf1_{V_t}-p_t`$ have conditional mean zero. Since $`H_{t+1}=H_t+p_t`$ is already $`\mathcal F_t`$-measurable,

```math
Z_n=\sum_{t\lt{}n}\frac{D_{t+1}}{1+H_{t+1}}
```

is a square-integrable martingale. Its conditional increment variance is at most $`p_t/(1+H_{t+1})^2`$. The decreasing function $`(1+x)^{-2}`$ gives the pathwise bound

```math
\sum_{t\lt{}n}\frac{p_t}{(1+H_{t+1})^2}
\le\sum_{t\lt{}n}\int_{H_t}^{H_{t+1}}\frac{dx}{(1+x)^2}
\le1.
```

Thus $`\sup_n\mathbb E Z_n^2\le1`$, and the square-integrable martingale convergence theorem gives convergence of $`Z_n`$ almost surely. Fix a path on that convergence event and write $`b_t=1+H_{t+1}`$, a positive nondecreasing sequence.

If $`H_\infty=\infty`$, summation by parts, or equivalently Kronecker's lemma applied to the convergent series $`\sum D_{t+1}/b_t`$, gives

```math
\frac{C_n-H_n}{1+H_n}\longrightarrow0,
\qquad
\frac{C_n}{H_n}\longrightarrow1.
```

For completeness, this summation argument separates finitely many initial terms from a tail whose partial sums have magnitude at most an arbitrary $`\varepsilon`$. The weighted tail, divided by its final nondecreasing weight, has magnitude at most $`2\varepsilon`$; the initial contribution tends to zero.

If $`H_\infty<\infty`$, the weights $`b_t`$ are bounded and their total variation is finite. The same summation-by-parts identity now shows that $`\sum D_{t+1}`$ converges: the convergent partial sums of $`D_{t+1}/b_t`$ are multiplied by bounded endpoint weights, and the remaining series is bounded by their supremum times the total variation of $`b_t`$. Therefore $`C_n=H_n+\sum_{t<n}D_{t+1}`$ has a finite limit. A nondecreasing integer-valued count with a finite limit can increase only finitely often. These two cases establish the event equality. ∎

In particular, a nonsummable deficit forces infinitely many target violations on the event $`\sum_t\delta_t=\infty`$. A fixed positive deficit is sufficient but unnecessary: $`\delta_t=1/(t+2)`$ also has a divergent sum. Conversely, an implementation with summable actual conditional violation probabilities eventually remains in the target almost surely.

For a deterministic schedule of marginals and targets, with every pair available and every selected finite coupling implementable, an eventually-target implementation exists **if and only if** $`\sum_t\delta_t<\infty`$. Necessity follows from the pointwise lower bound. For sufficiency, select a minimizing coupling at each time; its conditional violation probability is exactly $`\delta_t`$. The same equivalence holds with $`\delta_t^*`$ for deterministic nonempty licensed or incentive-constrained polytopes. The statement is about the specified schedule and sampler, not existence of a finite-memory realization. In an endogenous context, the current coupling can alter future marginals, polytopes and deficits. Minimizing today's violation does not prove dynamic optimality.

Two elementary schedules make the boundary explicit. Let the first response equal 0 with probability $`\delta_t`$ and the second always equal 1; the target is agreement. The conditional violation probability is necessarily $`\delta_t`$. With $`\delta_t=1/(t+2)^2`$, violations are finite almost surely, and

```math
\Pr(\text{some violation at or after }N)
\le\sum_{t=N}^{\infty}\frac1{(t+2)^2}
\le\frac1{N+1}.
```

Every fixed late time still has a positive violation probability, so there is no deterministic last-violation horizon. With $`\delta_t=1/(t+2)`$, the probability of no violation in a block starting at $`N`$ with length $`m`$ is

```math
\prod_{t=N}^{N+m-1}\left(1-\frac1{t+2}\right)
=\frac{N+1}{N+m+1}.
```

The product follows by conditional multiplication because the conditional hazards have the stated deterministic values. Its limit is zero, and violations recur infinitely often. Both deficits are positive and tend to zero; their summability separates the conclusions.

#### Public certification and physical restoration are different events

The filtration condition is essential. Suppose one unobserved bit $`Z`$ is fixed forever and is bad with probability $`1/2`$. Under a public filtration with no information about it, its conditional bad probability is always $`1/2`$. Yet infinitely many actual bad occurrences have probability $`1/2`$, not one. The repeated physical events are not measurable in the next public sigma-algebra, so the theorem does not apply there. Revealing $`Z`$ creates an adapted filtration but changes its conditional probabilities to zero or one. One cannot combine the enlarged filtration with the old half-probabilities. [17, §3][r13]

A finite plant also separates physical persistence from a demanding public certificate. Let the target states be $`\{0,2\}`$, start at 2, and give all states the same observation. State 0 remains at 0; state 1 moves to 0; state 2 stays at 2 with probability $`1/2`$ and moves to each of 0 and 1 with probability $`1/4`$. Every supported path has at most one bad visit, because its only bad state is 1 and that state immediately enters the absorbing good state. Physical eventual persistence is therefore sure, even on zero-probability supported infinite paths.

After one step the public support belief is $`\{0,1,2\}`$, and it remains that set forever. A certificate demanding that the next entire support belief lie inside the target consequently rejects the sole response at every time. Its certified target relation is empty and has Hall deficit one. This is correct evidence that the chosen public certificate is never met. It is not evidence that physical restoration is impossible. The actual bad-state probability at time $`t\ge1`$ is $`2^{-(t-1)}/4`$.

The same distinction applies when a previously proved finite-memory safety certificate permits only actions whose every observation successor stays in its certified winning region. A realizable joint law supported on those permitted actions preserves that certificate. Positive deficit obstructs the particular prescribed-marginal certificate implementation; it does not refute another bound, another winning policy, or actual target persistence. Establishing public knowledge of restoration is a stronger task than establishing restoration itself.
### 7.5 Transferring a restorative controller without a hidden-state oracle

A controller that succeeds in one stochastic model need not remain valid after its observations, action interface or disturbance law change. Preserving the list of possible transitions is insufficient for an almost-sure claim. Even exact transition couplings are insufficient if their proposed action translator consults hidden information. The following finite-model contract separates the probability proof, the information available to the implemented controller, and the destination's independent authorization. It consolidates the exact transfer result and its later private/public-memory refinement. [18, §§2–6][r14] [19, §1][r15]

#### Models, policies and information

Let the source have finite hidden state set $`X`$, finite actions $`A`$, observation map $`o_A:X\to O_A`$, initial law $`\mu_A`$, and finite nonempty disturbance menus $`D_A(x,a)`$. A disturbance $`d`$ selects a full transition distribution $`P_A^d(\,\cdot\mid x,a)`$. Define a destination with $`Y,B,o_B,\mu_B,D_B,P_B`$ in the same way. Each law includes every outcome, favorable or otherwise. Stochastic observations can be represented by adding the emitted observation to the plant state, provided the **joint** transition law is retained. This representation does not turn observations sharing one provenance root into independent copies.

A source behavioral policy $`\sigma`$ assigns a distribution on the next action to every finite source observation/action history. It may use the entire history. Its current action is sampled freshly after that history is fixed; it does not expose future action coins stored in advance. After the current action, the source adversary can use the complete source state/action history and choose a randomized member of the current disturbance menu. A guarantee against this full-history adversary class is a premise of the transfer theorem.

The destination interface has a finite controller-available mode set $`Q`$ and a projection $`\pi:Q\to P`$ onto its public mode. It specifies:

| Interface component | Information used |
|---|---|
| Initial mode $`q_0(o)`$ | Initial destination observation. |
| Reconstructed source observation $`\eta(q,o)`$ | Controller mode and current destination observation. |
| Admitted source-action menu $`M(q,o)\subseteq A`$ | The same controller information. |
| Executed action $`b=\tau(q,o,a)`$ | Controller mode, observation and its sampled virtual source action. |
| Next controller mode $`q'=u(q,o,a,b,o')`$ | Available controller information and the new observation. |
| Destination warrant $`J_B(\pi(q),o,b)`$ | The declared public mode, observation and actual destination action. |

The word “public” carries a mathematical obligation. There must be a function $`v`$ such that, on every used update,

```math
\pi\bigl(u(q,o,a,b,o')\bigr)
=v\bigl(\pi(q),o,b,o'\bigr).
```

Thus the public projection is reconstructible from the actual destination trace. Several virtual actions can translate to the same executed action; the controller may remember which one it sampled, but an external observer need not know it. If the entire mode is declared public, $`\pi`$ is the identity and the update cannot distinguish private virtual actions hidden by the same public trace. Publicly logging those actions would change the observation contract.

The source policy must put all its probability on $`M(q,o)`$ at every reachable interface history. This includes the histories under all permitted disturbances, not just the successful sampled examples. It is a policy-conformance premise, separate from verification of the finite plant tables.

The fibre criterion in Proposition 3 applies equally to action kernels: an implementation depending only on information $`I(h)`$ realizes a prescribed kernel $`K(h)`$ exactly when $`K`$ is constant on every fibre of $`I`$. A local hidden-state witness saying that **some** matching action exists for each hidden pair does not ensure a single available-information rule. Reconstructing the full source observation is a convenient sufficient condition here. A coarser reconstruction can suffice for a particular policy, but only after its action and memory updates are proved to factor through that coarser history.

#### A full probabilistic certificate

Supply a relation $`R\subseteq X\times Y\times Q`$. At every $`(x,y,q)\in R`$, with $`o=o_B(y)`$, require all of the following.

1. **Information:** $`\eta(q,o)=o_A(x)`$.
2. **Meaning and authority:** destination badness implies source badness; source safety implies destination safety. For every $`a\in M(q,o)`$, the source action is eligible at $`x`$, its translation $`b`$ is eligible at $`y`$, and the supplied public warrant $`J_B(\pi(q),o,b)`$ holds. Any additional task-readout preservation is another explicit relation, not an inference from the safe/bad labels.
3. **Every destination disturbance has a full match:** for every $`a\in M(q,o)`$ and $`d_B\in D_B(y,b)`$, there are $`d_A\in D_A(x,a)`$ and a coupling $`\kappa_{x,y,q,a,d_B}`$ satisfying

```math
\begin{aligned}
\sum_{y'}\kappa(x',y')&=P_A^{d_A}(x'\mid x,a),\\
\sum_{x'}\kappa(x',y')&=P_B^{d_B}(y'\mid y,b),\\
\kappa(x',y')>0
&\ \Longrightarrow
\bigl(x',y',u(q,o,a,b,o_B(y'))\bigr)\in R.
\end{aligned}
```

4. **Complete initial laws match:** a coupling $`\kappa_0`$ has marginals $`\mu_A,\mu_B`$ and positive mass only on pairs with $`(x,y,q_0(o_B(y)))\in R`$.

The existential source disturbance and coupling can depend on the related hidden triple and the selected destination disturbance. The implemented translator and mode update cannot inspect that hidden proof data. A populated source memory, learned history or migration memento also needs an initial-law/interface match; matching the current plant output alone does not authorize discarding it.

For rational finite tables, the matching problem for a fixed candidate source disturbance is exact transportation feasibility. The retained implementation searches over individual source disturbance kernels. Allowing a convex mixture of such kernels could give a weaker sufficient certificate against the randomized source adversary, but that additional search is not supplied by the checker. Neither successful transport nor its numerical feasibility certifies the truth or authority of the input labels.

#### The implemented controller and the path-law proof

Initialize $`q=q_0(o_B(y_0))`$ and the virtual source history with $`\eta(q,o_B(y_0))`$ and the explicitly matched initial source memory. At each step sample $`a`$ from $`\sigma`$ on that virtual history, execute $`b=\tau(q,o,a)`$, retain the virtual action $`a`$, receive $`o'`$, update $`q'`$, and append $`a,\eta(q',o')`$ to the virtual history. The implementation never observes or samples the proof's hidden source state.

**Theorem (exact restorative transfer).** Under the certificate, public-projection and policy-conformance premises, suppose the source policy has only finitely many bad visits almost surely against every permitted randomized full-source-history adversary. Then the implemented destination policy has only finitely many bad visits almost surely against every destination adversary. Source sure safety also transfers under the safety implication. Destination eligibility and public warrant are separately supplied at every reachable interface state.

Here “only finitely many bad visits” is a temporal property of the actual path. It does not assert a publicly recognized entry into an invariant core or a deterministic bound on the last bad time.

**Proof.** First suppose each plant has a single disturbance kernel for each state/action pair. Build a joint process from $`\kappa_0`$. At each related triple and joint finite past, draw $`a`$ from the source policy, translate it, and draw $`(x',y')`$ from the full coupling. The relation's observation identity proves inductively that the source observation/action history is exactly the destination controller's virtual history. Thus the action kernel in the construction is the actual implemented kernel on both sides; it is not secretly conditioned on hidden $`x`$ or later success.

The probability of a finite joint cylinder is the product of the initial mass, its successive policy probabilities and its coupling probabilities. All factors are nonnegative, and summing one-step extensions gives back the cylinder's mass. Summing each transition over $`y'`$ gives the complete source kernel. Because the action probability depends only on the source observation/action history, summing all destination histories leaves exactly the source controlled finite-history law. Summing instead over $`x'`$ gives the complete destination kernel. The controller mode and virtual action history are retained on the destination side, so this second marginal is the actual implemented destination law. No unfavorable branch is removed or renormalized.

These consistent finite-cylinder laws define a probability measure on infinite joint histories. All recorded states, actions and interface modes range over finite alphabets; unbounded behavioral memory is represented by finite histories rather than an additional arbitrary memory alphabet. To see the measure-extension condition directly, every finite union of cylinders is closed in the compact product of these finite discrete alphabets. A decreasing sequence of nonempty such sets has nonempty intersection. Consequently a decreasing sequence with empty intersection eventually has zero cylinder-algebra mass, supplying continuity at the empty set and the standard extension to the generated sigma-algebra. Cylinders determine that extension uniquely.

The relation holds initially and is preserved by every positive joint transition. A countable intersection therefore makes it hold at every time with probability one. On that event, every destination bad visit is a source bad visit, and

```math
\Pr_B(\text{bad infinitely often})
\le
\Pr_A(\text{bad infinitely often}).
```

The right side is zero by hypothesis.

Now fix an arbitrary nonanticipating destination adversary, allowing it to see the full destination state history and the controller's past/current virtual actions and available memory. In the joint construction it chooses $`d_B`$ first; the certificate then supplies $`d_A`$ and the coupling. The destination marginal is still exactly the selected adversary's process.

The chosen source disturbance can depend on the latent destination history. Condition on a positive-probability finite source state/action history $`h`$ and its already sampled current action $`a`$. Let $`\lambda_d(h,a)`$ be the conditional probability that the construction selected disturbance $`d`$. Then

```math
\Pr(X_{t+1}=x'\mid h,a)
=\sum_{d\in D_A(x_t,a)}
\lambda_d(h,a)P_A^d(x'\mid x_t,a).
```

This is an allowed randomized full-source-history adversary. At each finite time the conditioning is a ratio over finite sets; zero-probability histories can be assigned arbitrary legal choices. It does not condition on any future event. The source action kernel remains $`\sigma`$, since it was drawn freshly from the source observation/action history before either disturbance was selected. The source marginal is therefore a law covered by the robust source hypothesis, so the same event inclusion proves restoration.

For sure safety, a supported unsafe destination finite history would have positive probability under some legal disturbance choices. The exact joint lift would contain a supported source finite history ending in a related unsafe destination state. The safety implication forces that source state to be unsafe, contradicting source sure safety. The same lifting argument places every reachable destination history under the certificate's eligibility and warrant clauses. Their truth is an assumption supplied to the certificate, not established by the probabilistic argument. ∎

The randomized source-adversary class is necessary for this proof. If that adversary were restricted to public observations rather than full source histories, the induced conditional mixture might use information unavailable to it. A transfer theorem for that narrower adversary class needs an additional compatibility argument. It cannot inherit this conclusion by changing the word “adversary.”

#### Why support, information and authority remain separate

Several finite counterexamples isolate the independent hypotheses. [18, §6][r14]

* **A support simulation can lose all restoration probability.** Let source bad state $`b`$ stay at $`b`$ or enter an absorbing good state $`g`$, each with probability $`1/2`$. Let destination bad state $`B`$ remain there forever, with a separate absorbing good state $`G`$. The relation pairs $`b`$ with $`B`$ and $`g`$ with $`G`$. Every destination edge has a source support match, and badness reflects. The source restores almost surely; the destination fails surely. A relation-supported full coupling at $`(b,B)`$ is impossible because half the source mass must go to $`g`$ while all destination mass goes to $`B`$. Conditioning on the source self-loop would erase half the law at each step.
* **Matching actions can require unavailable information.** A fixed fair hidden bit $`h`$ is visible to the source and invisible to the destination. Each round guesses 0 or 1, and the state is bad exactly when the guess differs from $`h`$. Physical transitions under identical guesses can be coupled exactly. The source always guesses $`h`$; a destination with the same observation under both bits has the same action-sequence law under either. The disjoint events “eventually all guesses are 0” and “eventually all guesses are 1” cannot both have probability one. A hidden-pair-dependent choice of the matching guess is an oracle, not an implementation.
* **A coupling does not create destination permission.** In any valid finite certificate, deleting one required public warrant entry leaves the transition marginals untouched while invalidating the action's authority clause.
* **One matched initial pair does not match two initial laws.** If a source begins with probability one at $`b`$, a destination law assigning half its mass to an unrelated $`G`$ cannot be matched merely because $`(b,B)`$ is a valid pair.
* **A sufficient certificate need not exist whenever both systems restore.** One-action geometric-exit systems with exit probabilities $`1/2`$ and $`1/3`$ both restore almost surely, but their identity relation cannot couple their distinct one-step laws. A policy that never uses a source observation distinction can also transfer through a policy-specific coarsening even if full observation reconstruction fails.

These counterexamples preserve a constructive result: with a verified information interface and full laws, transfer is possible. Rejection of this particular certificate is not a general impossibility theorem for all controllers, relations or information-preserving translations.

#### Finite memory and the timing of randomization

If the source policy has an $`M`$-state realization with fixed initial memory, deterministic updates from its observation/action history and fresh current-action draws, the destination construction needs at most $`|Q|M`$ memory states, apart from the convention for storing the current observation. A history-dependent policy that uses an unbounded counter remains unbounded. A supplied external clock is memory, not a free finite-state implementation.

An arbitrary randomized-memory realization cannot be substituted under a changed memory-exposure contract. A finite prediction game shows why. Its plant has a prediction state $`P`$, locked-prediction states $`Q_0,Q_1`$ and an absorbing good state $`G`$; all other states are bad. Observations distinguish $`P,Q,G`$ but hide the subscript of $`Q_h`$. A controller samples a fair private bit $`r`$ before each prediction phase and waits. The disturbance then chooses $`h`$ and moves to $`Q_h`$. The controller responds $`r`$; a mismatch enters $`G`$, while a match returns to $`P`$ and refreshes the private bit. No disturbance choice after the response can revise the locked prediction.

For every nonanticipating full-plant/action-history adversary blind to the current bit, $`r`$ is conditionally fair when the prediction is made. Failure through $`n`$ rounds therefore has probability $`2^{-n}`$, and restoration is almost sure. An adversary allowed to inspect the pre-sampled bit instead chooses $`h=r`$ and keeps the system bad forever. Identical plant kernels and identity couplings do not fix that change of information.

Sampling the bit freshly at $`Q_h`$, after the prediction is locked, removes the exposed future randomness and restores the behavioral theorem's guarantee. The historical correction accordingly restricts the finite-memory product bound or requires a separate proof that the realization preserves the behavioral action kernel under the declared memory exposure. This counterexample concerns implementation equivalence; it does not refute the fresh-action transfer theorem. [21, §F1][r17]

Probabilistic simulation, full transition liftings and controller refinement have established mathematical ancestry. Haesaert, Soudjani and Abate's exact relation includes both transition and initial-law liftings; its interface may depend on both model states. The observation-restricted construction above adds a specific sufficient information contract and independently supplied destination authority. Their approximate finite-horizon theorem includes an accumulating probability error; it does not by itself assert exact infinite-horizon persistence. [25, Definition 6 and Theorem 3][refinement]
### 7.6 Composing transfers while keeping warrant public

Passing a controller through two valid interfaces creates a further information question. Something publicly visible at the intermediate plant may become a privately remembered virtual action at the final plant. It cannot automatically remain part of the final public warrant. The private/public split in §7.5 makes this distinction explicit and supports exact composition. [19, §§2–4][r15]

Consider a source $`A`$ whose state $`x\in\{0,1\}`$ is observed and whose action $`a`$ sets the next state to $`a`$. An intermediate plant $`B`$ has state $`y\in\{0,1\}`$ and the same state-setting actions, but only a constant observation. The first interface translates $`b=a`$ and tracks $`y`$ through a public mode updated from the actually executed action $`b`$. It reconstructs the source observation exactly. A final plant $`C`$ has one state, one observation and one action, tick. The second interface translates either $`B`$ action to tick and reconstructs $`B`$'s constant observation with a constant mode. Start $`A`$ and $`B`$ at 0; all states and actions in this structural example are supplied as good, safe and licensed.

Both individual interfaces have full deterministic couplings and all-public modes. In the composite, however, two different virtual actions produce the same actual $`C`$ trace while requiring different reconstructed $`A`$ observations. The mode tracking the original state is controller-private at $`C`$. Keeping it public would make the supplied two-action interface invalid. This is not an impossibility result for every particular constant policy; it is a failure of closure for the stated all-public interface class.

#### The composite interface

Let a valid split interface from $`A`$ to $`B`$ have private mode $`q\in Q_1`$, projection $`\pi_1`$, relation $`R_{AB}`$ and functions $`\eta_1,\tau_1,u_1`$. Let an interface from $`B`$ to $`C`$ have mode $`r\in Q_2`$, projection $`\pi_2`$, relation $`R_{BC}`$ and functions $`\eta_2,\tau_2,u_2`$. The middle plant is one and the same model, including observations, transition kernels, eligibility, safe/bad meanings and initial law. A correspondence between differently represented middle models would need a separately proved transport; the retained constructor requires exact equality.

Require menu compatibility: whenever the first interface permits a source action at a relevant composite information state, its translated $`B`$ action belongs to the second interface's menu. Silently deleting an incompatible source action would change the policy-conformance obligation.

Use the product private mode $`(q,r)`$ and the final public projection

```math
\pi(q,r)=\pi_2(r).
```

For current $`C`$ observation $`o`$ and source action $`a`$, define

```math
\begin{aligned}
o_B&=\eta_2(r,o),&
\eta((q,r),o)&=\eta_1(q,o_B),\\
b&=\tau_1(q,o_B,a),&
c&=\tau_2(r,o,b).
\end{aligned}
```

After receiving $`o'`$, the available update is

```math
r'=u_2(r,o,b,c,o'),\qquad
o_B'=\eta_2(r',o'),\qquad
q'=u_1(q,o_B,a,b,o_B').
```

The relation uses one common middle witness:

```math
R_{AC}=
\{(x,w,(q,r)):
\exists y,\ (x,y,q)\in R_{AB}
\text{ and }(y,w,r)\in R_{BC}\}.
```

Initialize $`r`$ from the actual $`C`$ observation, reconstruct the initial $`B`$ observation, and initialize $`q`$ from it. The original source controller retains the memory its policy requires.

**Theorem (composition with a private product mode).** These formulas define a valid source-to-final split interface. They preserve full probability laws, source-to-final badness and safety implications, and the final destination's independently supplied public warrant. The restorative-transfer theorem applies under its original robust policy premises.

**Proof.** Fix a related triple $`(x,w,(q,r))`$, choose a middle witness $`y`$, and fix an admitted source action and a final disturbance. The second certificate supplies a middle kernel $`P_B`$ and a coupling $`\kappa_{BC}`$ with the selected $`P_C`$. For that **same** middle kernel, the first certificate supplies a source kernel $`P_A`$ and a coupling $`\kappa_{AB}`$. Define

```math
\lambda(x',y',w')=
\begin{cases}
\displaystyle
\frac{\kappa_{AB}(x',y')\kappa_{BC}(y',w')}{P_B(y')},
&P_B(y')>0,\\[6pt]
0,&P_B(y')=0,
\end{cases}
\qquad
\kappa_{AC}(x',w')=\sum_{y'}\lambda(x',y',w').
```

At a zero middle mass, both couplings already have zero mass, so no probability is discarded. Summing gives

```math
\sum_{w'}\kappa_{AC}(x',w')
=\sum_{y'}\kappa_{AB}(x',y')=P_A(x'),
\qquad
\sum_{x'}\kappa_{AC}(x',w')=P_C(w').
```

Whenever a triple mass is positive, the second relation guarantees that the reconstructed next middle observation is the actual $`o_B(y')`$. The displayed $`q',r'`$ are therefore exactly the component updates at the same successor $`y'`$. Both component successor relations hold, proving support in $`R_{AC}`$. The middle state is a proof witness; the implementation computes its interface from $`q,r,a,o,o'`$ and never inspects that state.

Glue the initial couplings by the same formula, now using the common full middle initial marginal. Their observation identities ensure agreement of the prescribed initial modes. If those middle priors differed, this calculation would not provide both marginals.

Observation reconstruction composes through the common middle witness. The final public projection is reconstructible because the second interface's projection update depends only on its public mode and actual final trace; it is independent of any hidden identity of the virtual middle action. Pointwise,

```math
\mathrm{Bad}_C\Longrightarrow\mathrm{Bad}_B
\Longrightarrow\mathrm{Bad}_A,
\qquad
\mathrm{Safe}_A\Longrightarrow\mathrm{Safe}_B
\Longrightarrow\mathrm{Safe}_C.
```

Final action eligibility and warrant come from the second interface at $`\pi_2(r)`$. The intermediate warrant is not substituted for final authorization. All hypotheses of §7.5 are satisfied. ∎

With an $`M`$-state source realization having deterministic history updates and fresh action draws, the product implementation needs at most $`|Q_1||Q_2|M`$ controller-memory states. The random-memory exposure qualification remains unchanged. The finite relation certificate does not turn an unbounded source policy into a finite-memory one.

The theorem composes the supplied safe/bad meanings, not arbitrary task identity. If additional readout relations are to compose through the same middle witness, that claim needs its own statement and proof. Replacing such a claim by equality of coarse output labels can be a stronger and unjustified assertion. The composition of correct kernels likewise does not establish that real evidence has those kernels or that its final use is authorized.

### 7.7 Approximation needs an occupancy bound or a genuine return

Exact relatedness can be relaxed in more than one way, and the distinction matters for eventual persistence. A bound on leaving a relation concerns departures. Restoration concerns the amount of time spent in bad states. A single departure can occupy the entire remaining future. [20, §§1–3][r16]

#### One departure can destroy eventual persistence

Let a source consist of one always-good state. A destination begins at good state $`S`$. At time $`t`$, while at $`S`$, it enters an absorbing bad state $`F`$ with probability

```math
\delta_t=\frac1{(t+2)^2},
```

and otherwise remains at $`S`$. Relate the source state only to $`S`$. Every path has at most one departure, and its conditional departure hazard is bounded by a summable deterministic sequence. Nonetheless the no-departure probability after $`n`$ transitions is

```math
\prod_{k=2}^{n+1}\left(1-\frac1{k^2}\right)
=\prod_{k=2}^{n+1}\frac{(k-1)(k+1)}{k^2}
=\frac{n+2}{2(n+1)}
\longrightarrow\frac12.
```

Thus restoration succeeds with probability exactly $`1/2`$. On the remaining paths, the single departure produces infinitely many bad visits. Conditional Borel–Cantelli correctly guarantees finitely many departures; it does not guarantee finite bad occupancy. With any constant fault probability $`\delta>0`$, no-departure probability is $`(1-\delta)^n\to0`$, so arbitrarily small constant local error can destroy almost-sure restoration entirely.

#### An exact law can tolerate summably many occupancy defects

Sometimes only the target-preservation part of an interface is approximate. Let $`S`$ be an invariant relation on which the information reconstruction, full probability-law coupling and destination authority of §7.5 remain valid at every time. Let $`R\subseteq S`$ be the subrelation on which destination badness implies source badness. In the full joint proof filtration, let

```math
E_t=\{(X_t,Y_t,q_t)\notin R\}.
```

Suppose these events are adapted and

```math
\sum_{t=0}^{\infty}
\Pr(E_{t+1}\mid\mathcal F_t)\lt{}\infty
\quad\text{almost surely}.
```

**Proposition (finite occupancy defects).** If the source restores almost surely, the destination does also.

**Proof.** Exact gluing on $`S`$ supplies the actual source and destination marginals for all time. The adapted-event theorem implies only finitely many $`E_t`$. At every time,

```math
\mathrm{Bad}_B(Y_t)
\Longrightarrow
\mathrm{Bad}_A(X_t)\ \text{or}\ E_t.
```

Both exceptional time sets on the right are finite almost surely. ∎

No public detector for $`E_t`$ is needed in this particular theorem, since the implemented information interface and authority stay valid even during the mismatch. Its probabilities must nevertheless be conditioned on a filtration to which the physical events are adapted. A coarser public conditional probability cannot be substituted without that premise. If leaving the target-preserving relation also destroys observation reconstruction or invalidates controller memory, the invariant-interface premise fails and this proof is unavailable.

#### An executable regenerative repair

A genuinely broken interface requires a recovery policy and a legitimate restart. Retain discrete time, finite state/action/observation alphabets and controller memory determined by finite histories, possibly unbounded. Recovery may be history-dependent. This ensures countably many possible finite entry histories; a model with arbitrary continuous random recovery memory needs a corresponding regular-conditional-kernel formulation.

Assume the destination distinguishes running and recovery modes. A fault flag $`D_t`$ is generated after transition $`t`$, is observable by time $`t+1`$, and begins recovery. Conservative flags are permitted. The following four obligations are separate.

1. **Finite conditional fault budget.** For the full nonanticipating joint filtration, $`D_t\in\mathcal F_{t+1}`$ and predictable $`\delta_t\ge0`$ satisfy

```math
\Pr(D_t\mid\mathcal F_t)\le\delta_t,
\qquad
\sum_t\delta_t\lt{}\infty
\quad\text{almost surely}.
```

2. **Sound public detection while running.** Before a flag, the implementation uses the observation-compatible translated policy. Every running step has full source and destination marginals, including the actual flag/observation process. A no-flag successor remains in the relation and preserves the information interface, public projection and badness implication. A flagged successor may leave it. An existential hidden coupling does not itself implement a detector: the flag must be available through the declared destination interface.
3. **Almost-sure finite recovery.** From every reachable recovery entry and every allowed conditional law, a specified executable recovery policy reaches a public reentry point in finite time with conditional probability one. It may visit bad states during recovery. Any required sure safety and action authority must hold independently on all recovery actions and possible outcomes. If flags are suppressed during recovery, this recovery contract must already cover its disturbances; they cannot disappear from the obligations.
4. **Complete reentry law and memory.** At every reached controller-information reentry history $`h`$, the actual conditional destination law has a full initial coupling with a source law $`\mu_A^h`$ in a declared winning family. The policy $`\sigma^h`$, chosen from available information, restores almost surely for that family against the same full-source-history adversary class. Its reconstructed history, memory, mode and authority are reset or transferred through an explicit valid interface. If several hidden or environment-conditioned laws are compatible with $`h`$, the statement must hold for each induced law. Selecting one favorable initial pair is insufficient.

The initial state must have a valid running entry or an initial recovery satisfying the same almost-sure completion condition.

**Theorem (regenerative restoration).** Under these premises, the destination has only finitely many bad visits almost surely. The conclusion does not assert finite expected recovery duration or a deterministic cutoff time.

**Proof.** The conditional fault budget and §7.4 give only finitely many flags almost surely. Every recovery entry has conditional probability zero of never completing. Because entry times and finite histories form a countable population, the union of those noncompletion events is null. Thus, outside a null set, some final running episode begins at a finite time and receives no further flag.

It remains to justify that final episode without changing its law by conditioning on future success. Fix an episode index $`j`$ and a positive-probability reentry history $`h`$. Start the full source/destination coupling supplied by the reentry contract and use the running step couplings until the first flag. If a flag occurs, continue the **proof's source process only**, from its actual source state and memory, with its original source policy and any legal source disturbance. This auxiliary continuation is not an extra destination operation.

Before the flag, summing the full coupling gives the legal source marginal. After it, the autonomous continuation remains legal by construction. As in §7.5, marginalizing destination-dependent source-disturbance choices produces an allowed randomized full-source-history adversary. Consequently this unconditioned source continuation has probability zero of infinitely many bad visits.

On the event that the episode never flags, the auxiliary continuation is never used: relatedness and badness reflection hold throughout. Hence

```math
\Pr\bigl(
\text{episode }j\text{ never flags and the destination is bad infinitely often}
\mid h
\bigr)=0.
```

This is an event inclusion inside a process with the correct unconditioned marginal. It does not assert that conditioning the source process on no future flag preserves its original law. Sum these null events over the countably many episode indices and entry histories. Almost every path has one candidate final episode, so its destination cannot be bad infinitely often. The finite number of earlier finite-length running and recovery episodes contributes only finitely many visits. ∎

The last fault time is generally not a stopping time. The proof therefore does not invoke a restart or strong-Markov argument at that last time. Observable recovery entries and reentries can be stopping times, but the countable-episode argument is what identifies the final one without postselection. No independence between episodes is assumed.

#### Recovery distinguishes three temporal guarantees

First replace the absorbing failure state in the square-hazard example by an observed recovery state. From recovery return to $`S`$ with probability $`\rho=1/2`$ per step. With the stipulated safety and licenses, the fault budget remains summable, each recovery is geometric, and reentry restarts the always-good source. Regenerative restoration therefore has probability one.

This particular example gives more than the general theorem. If $`r_t`$ is its probability of occupying recovery at time $`t`$, then

```math
r_{t+1}=(1-r_t)\delta_t+(1-\rho)r_t
\le\delta_t+(1-\rho)r_t,\qquad r_0=0.
```

Unrolling and summing the nonnegative terms yields

```math
\sum_{t=0}^{\infty}r_t
\le\frac1{\rho}\sum_{t=0}^{\infty}\delta_t\lt{}\infty.
```

The expected total bad occupancy is finite here. The time-dependent hazard schedule needs its unbounded time index; this is not an automatically time-homogeneous finite-state implementation.

Second, almost-sure finite recovery need not have finite expectation. In recovery, let elapsed counter $`k`$ return on the next step with probability $`1/(k+2)`$ and otherwise increment. For its positive-integer duration $`T`$,

```math
\Pr(T>n)=
\prod_{k=0}^{n-1}\left(1-\frac1{k+2}\right)
=\frac1{n+1}\longrightarrow0,
\qquad
\mathbb ET=\sum_{n=0}^{\infty}\Pr(T>n)=\infty.
```

One such recovery followed by an always-good running mode satisfies eventual persistence while its expected bad occupancy is infinite. This policy uses unbounded elapsed-time memory; it is not a counterexample about a fixed finite homogeneous Markov chain.

Third, successful recovery after every fault does not guarantee that faults eventually cease. With fixed fault probability $`\delta>0`$ from $`S`$ and fixed return probability $`\rho>0`$ from recovery, the finite two-state chain is irreducible. Its stationary recovery mass solves $`r=(1-r)\delta+(1-\rho)r`$, giving

```math
r=\frac{\delta}{\delta+\rho}>0.
```

Recovery is visited infinitely often almost surely. Thus recovery can work each time while permanent correctness fails. Conversely, the finite-fault budget is sufficient rather than necessary for every architecture: infinitely many harmless flags need not create actual bad visits or destroy a winning interface. [20, §4][r16]

#### Mathematical and executable scope

The retained finite implementations check supplied coupling tables, private/public projections and compatible compositions using exact rational data. Their transportation witnesses expose both marginals; composition requires the same middle law; the independent tests preserve the hidden-information, missing-warrant and exposed-future-coin counterexamples. Finite-history and recurrence probes give bounded implementation evidence. They are not proofs of infinite-horizon measure statements, automatic synthesis of every interface or recovery controller, or validation of an actual cognitive system. The proofs above supply the stated infinite conclusions from their declared premises. [17][r13] [18][r14] [19][r15] [20][r16] [21][r17]

The remaining practical work is concrete: establish the actual joint kernels and provenance dependence, prove policy-menu conformance under all admitted disturbances, realize the sampler and information interface, supply destination warrant, and—for regenerative use—implement sound fault detection and a complete conditional reentry-law/memory contract. The ordinary research does not provide a general recovery synthesizer, an unrestricted migration decision procedure, a formal-kernel proof of these probability theorems, or permission to infer scientific truth from a finite checker. Preserving those distinctions makes the conditional results usable without overstating their reach.

### 7.8 Learning a hidden standard: memory, certainty and permission

A fixed hidden standard can be statistically learnable even though no finite observation certifies it. The memory and objective of the learner then matter independently of the size of the physical plant. Consider a standard $`h\in\{0,1\}`$ chosen initially and held fixed. Conditional on $`h`$, the acquisitions $`Y_1,Y_2,\ldots`$ are independent, with

```math
\Pr_h(Y_t=1)=
\begin{cases}
1/3,&h=0,\\
2/3,&h=1.
\end{cases}
```

After seeing the current acquisition, the learner issues a response $`a_t\in\{0,1\}`$. Both responses are, for now, stipulated safe and permitted under both standards. A response is correct exactly when $`a_t=h`$. The physical observation/response state is finite; the learner's accumulated information need not be.

Write $`\mathcal R_h`$ for eventual permanent correctness:

```math
\mathcal R_h
=\{\exists N\ \forall t\ge N:\ a_t=h\}.
```

The statistical dependence of acquisitions on $`h`$, the assignment of a target response to $`h`$, and permission to issue either response are three supplied assumptions. The model derives no norm from a frequency. [26][r18]

**Theorem (memory and certainty separate).** In this model:

1. No policy is sure to satisfy $`\mathcal R_h`$ under both standards.
2. One deterministic policy using unbounded memory satisfies $`\Pr_h(\mathcal R_h)=1`$ under both standards.
3. No finite, time-homogeneous controller satisfies that almost-sure guarantee under both standards.
4. For every $`\varepsilon>0`$, a finite controller achieves $`\Pr_h(\mathcal R_h)\ge1-\varepsilon`$ under both standards.
5. No rule can identify the standard with zero error under both models by a declaration that occurs after finitely many acquisitions almost surely.

Here a finite, time-homogeneous controller has a finite total internal state, a fixed initial law independent of the hidden standard, and fixed action and update kernels based on its available information. Randomized kernels are allowed. An unbounded clock, an externally changing transition table, or an increasing-precision register is additional memory. The physical state, any separately supplied current observation and any response needed to label correctness are included when compiling the controller into a finite chain.

**Proof of the sure impossibility.** Every finite bit word has positive probability under both standards. In particular, the infinite all-zero word is admitted by both support models: every one of its finite prefixes is possible. A deterministic policy has the same response sequence on that word in both models. The sequence cannot be eventually always zero and eventually always one. For a randomized policy, the same argument fixes a common supported sequence of its internal choices. Sure success quantifies over those choices and supported observations, including paths of probability zero. ∎

**Proof of almost-sure learning with unbounded memory.** After acquisitions $`1,\ldots,2m`$, choose their majority bit, resolving a tie as zero. Hold that response until the next even acquisition count. Let $`K_m`$ be the number of ones among the first $`2m`$ acquisitions. Under $`h=0`$, Markov's inequality gives

```math
\Pr_0(K_m\ge m)
\le \frac{\mathbb E_0[2^{K_m}]}{2^m}
=\frac{(4/3)^{2m}}{2^m}
=\left(\frac89\right)^m.
```

An incorrect response under $`h=0`$ actually requires $`K_m>m`$, so this bound is conservative. Under $`h=1`$, the number of zeros has the same law as $`K_m`$ under $`h=0`$. It also bounds the adverse tie and every incorrect majority response. Thus the error probabilities of the successive update blocks have finite sum, at most

```math
\sum_{m=1}^{\infty}\left(\frac89\right)^m=8.
```

The first Borel–Cantelli implication gives only finitely many incorrect update blocks almost surely. These events overlap in their acquired data, but that implication requires no independence between the events. Each selected response is held for only two response times; the finite initial prefix is immaterial. Hence there are only finitely many incorrect responses. The cumulative sample count and tally are unbounded. By summing the error indicators, eight also bounds the expected number of incorrect update blocks under the stipulated model; it is not a bound on the last incorrect time. ∎

**Proof of the finite-memory obstruction.** Fix one finite, time-homogeneous controller. Compile its total memory, available physical state and selected response into a finite Markov chain under each standard. Both acquisition probabilities are strictly positive. The two chains therefore have the same directed graph of positive transitions and the same reachable states from the common initial support, although their numerical transition probabilities differ.

Recall why the eventual-correctness test for a fixed finite chain is a graph test. Every reachable state has a path into a bottom strongly connected component. Finiteness gives a common finite path-length bound and a positive lower bound on the probability of following one such path. Repeated conditional trials in blocks of that length show that a bottom component is entered almost surely. Inside a bottom component, the same argument gives a positive uniform chance of reaching any prescribed state in a bounded number of steps. For each fixed time, the chance of avoiding that state forever afterward is zero. Taking the countable union over starting times shows that every state of the component is visited infinitely often almost surely. Conversely, every reachable bottom component has a positive probability of being entered along a finite path.

It follows that a finite chain is eventually always correct almost surely precisely when every reachable bottom component contains only correct-response states. Success under $`h=0`$ would require all states of each reachable bottom component to issue zero. Success under $`h=1`$ would require every state of those same nonempty components to issue one. The common graph makes the requirements incompatible. Randomized controller actions and updates merely contribute their positive edges to this graph; they do not remove the contradiction. ∎

This obstruction does **not** say that every finite controller has restoration probability zero. A controller can acquire four samples and then commit to their majority, with ties resolved as zero. Its restoration probabilities are

```math
\begin{aligned}
\Pr_1(\mathcal R_1)
&=\binom43\left(\frac23\right)^3\frac13
  +\left(\frac23\right)^4
 =\frac{16}{27},\\
\Pr_0(\mathcal R_0)
&=1-\binom43\left(\frac13\right)^3\frac23
     -\left(\frac13\right)^4
 =\frac89.
\end{aligned}
```

They are positive and below one. A finite machine may have different absorbing commitments, each reached with positive probability under both hypotheses. [21, §C3][r17]

**Proof of finite-memory approximation.** Given $`0<\varepsilon<1`$, choose $`m`$ with $`(8/9)^m\le\varepsilon`$. Acquire $`2m`$ samples, then commit forever to their majority. The same finite-sample bound makes the wrong-commitment probability at most $`\varepsilon`$ under either standard. One implementation stores a pair $`(n,k)`$, where $`0\le n\le2m`$ and $`0\le k\le n`$, and uses two terminal commitment states. Consequently

```math
\frac{(2m+1)(2m+2)}2+2
```

states suffice. This is an upper bound, not a memory-optimality theorem. The memory size changes when the requested error changes. Arbitrarily good finite-memory approximation and one almost-surely successful finite-memory policy have different quantifiers. ∎

**Proof of the finite-declaration obstruction.** Fix a finite sample count $`n`$ and a declaration $`d`$. For each word $`w\in\{0,1\}^n`$, let $`k_{n,d}(w)`$ be the probability, over the rule's own randomization, that it first stops at $`n`$ and declares $`d`$ on that word. The rule is the same under both standards, so this nonnegative factor is the same. The declaration probability under $`h`$ is

```math
\Pr_h(\tau=n,D=d)
=\sum_{w\in\{0,1\}^n}\Pr_h(Y_{1:n}=w)\,k_{n,d}(w).
```

Every word probability is positive under both models. A declaration event has positive probability under one precisely when it has positive probability under the other. Declaring zero must therefore have zero probability under both models if zero error under $`h=1`$ is required; declaring one likewise has zero probability under both if zero error under $`h=0`$ is required. The countable union over $`n`$ cannot have probability one. Continued revisability is compatible with almost-sure eventual correctness; it does not provide a finite zero-error certificate that revision can safely end. ∎

#### Acquisition roots and action authority

Two changes to the model remove the constructive conclusion for different reasons.

First, retain the biased one-time marginal law but draw only one bit $`Z`$ and report $`Y_t=Z`$ forever. Each of the two complete report words has positive probability under both standards. Conditional on either word, the learner has the same law of internal choices and responses in both models. Almost-sure correctness under both would require that common conditional response law to be concentrated both on eventual zero and on eventual one, which are disjoint events. It is impossible. Repeated reports of one acquisition do not supply the independent acquisitions used by the majority proof. One physical device can supply independent acquisitions if its actual stochastic and evidential model warrants them; the relevant quantity is independent acquisition events, not device count.

Second, retain fresh acquisitions but permit response $`a`$ only when $`a=h`$. Add a response “abstain” that is always permitted but never correct. Both standards remain possible after every finite public history. A menu requiring eligibility for every still-possible standard therefore contains neither binary guess. Only abstention remains, so no permitted policy achieves restoration. A small probability of error does not eliminate a positive-support possibility or supply permission to disregard it. A risk-tolerant permission rule would change the model's substantive authority premise.

The equal-support argument also has a precise limit. The two biased independent acquisition processes have the same one-step support, yet their different probabilities permit the unbounded-memory learner above. If the two biases are instead made equal while their targets remain opposite, their complete observation laws coincide. The induced response law of any common policy then cannot assign probability one to both disjoint eventual-response events. Thus unrestricted almost-sure learnability can change without any change of one-step support. The support test proved above applies to an already fixed finite homogeneous controller; it does not classify every unbounded strategy.

#### Hidden objectives and a legitimate common-objective specialization

The finite-memory obstruction is consistent with the theorem of Chatterjee, Doyen, Raskin and Sankur for multiple-environment Markov decision processes. Their model has a finite family of transition laws on a shared observed state space and **one common parity objective**. Their Theorem 4 establishes decidability of almost-sure winning and sufficiency of pure finite-memory strategies, with the stated exponential memory bound. [31, §§2–3][memdp]

Here correctness depends on the unobserved standard. The same observed response state can be correct under one model and incorrect under the other. No single priority labeling of that observed state represents both targets. Adding the hidden standard to the acceptance label does not make it observed. The common-objective theorem cannot be applied by silently removing this distinction.

A useful permitted specialization can nevertheless be stated exactly. Let $`x_t=(s_t,c_t)`$ be the complete finite observed state: $`s_t`$ records the physical state and $`c_t`$ the public evidence and permission state. Every additional public signal used by the policy or its eligibility test must be represented there. Let $`H_t`$ be the fixed environments still possible from the complete observed history, and write $`q_t=(x_t,H_t)`$. Require a known finite, time-homogeneous transition law $`K_h(x'\mid q,a)`$ for this complete observed successor under each fixed environment. This is a Markov premise about the entire compiled observation, not merely the physical marginal. If the public state has further history-dependent dynamics, they must admit the stipulated finite compilation before this specialization applies.

Initialize $`H_0`$ using the complete initial observation. For initial laws $`\mu_h`$ on the finite observed state and admitted environment set $`\mathcal E`$, the exact support updates are

```math
H_0=\{h\in\mathcal E:\mu_h(x_0)>0\},
\qquad
H_{t+1}
=\{h\in H_t:K_h(x_{t+1}\mid q_t,a_t)>0\}.
```

**Why the update is exact.** Fix a finite observed history and a common observation-based policy. The policy's action-selection factors are the same under each environment. Apart from those common factors, the history has likelihood

```math
\mu_h(x_0)
\prod_{r=0}^{t-1}K_h(x_{r+1}\mid q_r,a_r).
```

On a history the policy can generate, an environment is possible exactly when each factor in this finite product is positive. The initial rule and successive updates express that condition by induction. In particular, a possible transition cannot remove its actual environment. The pair consisting of this successor observation and the deterministic live-set update also defines the finite transition law on $`q`$. Rows with $`h\notin H`$ may be completed arbitrarily: they are unreachable under environment $`h`$ from the compatible initial state.

The physical marginal alone can lose a decisive observation. For example, take one physical state, one common action and two environments. The physical state stays fixed with probability one under both environments, while the next public state is $`c'=h`$. Observing $`c'=0`$ leaves only environment zero, and observing $`c'=1`$ leaves only environment one. A rule testing only the physical successor instead retains both. It produces a conservative superset, not the exact set needed by the stated compilation. A physical-only test is justified when the public update supplies no further support discrimination; a common deterministic update from the already observed physical transition is one sufficient restriction.

Require the permitted action set $`\Gamma(q)`$ to be determined by the observed compiled state, including any robust eligibility and warrant conditions. Require also one common parity objective on that state. The complete transition law then yields a finite multiple-environment model with common action menus: the law varies with the fixed environment, while state meanings, available actions and objective do not. A state with no permitted action is a losing analysis dead end; representing it by a losing sink does not authorize a physical action.

The cited common-objective theorem applies to this explicit model, starting from each observed initial state with its compatible environment set. Its complexity is measured on the compiled representation, not on an unspecified succinct permission language. Simultaneously satisfying all candidate targets can sometimes be expressed as a common objective. Satisfying only the actual hidden standard is a different requirement. Ongoing hidden physical state, switching environments, unbounded public memory or a target depending on the unknown environment removes the stated specialization.

#### A whole trace can be nonatomic and still identify a target

The acquisition example also separates a property of an entire observation law from success on one decision target. For a random observation $`V`$, let

```math
S_V=\{v:\Pr(V=v)>0\},
\qquad
d_{\mathrm{atom}}(V)=1-\Pr(V\in S_V).
```

All singletons here are measurable. The finite prefix $`Y_{1:n}`$ has a finite positive atomic law, so $`d_{\mathrm{atom}}(Y_{1:n})=0`$. For the complete trace and any fixed infinite word $`w`$,

```math
\Pr_h(Y=w)
\le\Pr_h(Y_{1:n}=w_{1:n})
\le\left(\frac23\right)^n
\longrightarrow0.
```

Thus no complete word has positive mass and $`d_{\mathrm{atom}}(Y)=1`$, under either model or any mixture of the two.

Nevertheless, the limiting empirical frequency identifies the standard almost surely. A short proof supplies the relevant convergence. Put $`T_n=\sum_{t=1}^nY_t`$ and let $`p=\Pr_h(Y_t=1)`$. At square sample sizes, Chebyshev's inequality gives, for every $`\delta>0`$,

```math
\Pr_h\!\left(\left|\frac{T_{k^2}}{k^2}-p\right|>\delta\right)
\le\frac{p(1-p)}{\delta^2k^2}.
```

The right sides are summable. Borel–Cantelli, applied to a countable sequence of positive $`\delta`$ tending to zero, yields $`T_{k^2}/k^2\to p`$ almost surely. For $`k^2\le n\le(k+1)^2`$, monotonicity of the counts gives

```math
\frac{T_{k^2}}{(k+1)^2}
\le\frac{T_n}{n}
\le\frac{T_{(k+1)^2}}{k^2}.
```

Both bounds converge to $`p`$. Define a decoder to return zero on traces with limiting frequency $`1/3`$, one on those with limit $`2/3`$, and any fixed value elsewhere. These are measurable limit conditions. Under any prior giving both standards positive mass, the decoder equals the actual standard almost surely. It is not correct on every support-admitted trace, and it cannot be replaced by a finite zero-error stopping declaration.

The atomic-mass defect of the complete trace therefore does not mean “no useful information” or “every decision target fails.” Its whole-observation property and this one-target identification claim have different quantifiers. Neither supplies the target's truth, empirical interpretation or action authority.

### 7.9 High average accuracy can coexist with perpetual errors

Finite-memory learning has several performance criteria. Let $`H_+`$ and $`H_-`$ give independent Bernoulli acquisitions with probabilities $`2/3`$ and $`1/3`$, respectively, with equal hypothesis priors. A time-average Bayes error is

```math
\overline e
=\lim_{n\to\infty}\frac1n\sum_{t=1}^n
\frac{\Pr_+(a_t=-)+\Pr_-(a_t=+)}2,
```

when the limit exists. Eventual correctness instead requires only finitely many errors on almost every path. The following exact family has arbitrarily small long-run average error as its memory grows, but restoration probability zero under each hypothesis. [27][r19]

#### An exactly solvable finite learner

Take $`S=L+1\ge2`$ memory states $`0,\ldots,L`$ and $`0<\varepsilon\le1`$. At an interior state, acquisition one moves right and acquisition zero moves left. At state zero, acquisition one moves to state one with additional probability $`\varepsilon`$; otherwise the learner stays at zero. At state $`L`$, acquisition zero moves left with additional probability $`\varepsilon`$; otherwise it stays at $`L`$. The extra randomization is fresh and independent of the acquisition.

For acquisition bias $`0<p<1`$, all adjacent moves have positive probability, and the endpoints have positive self-loops. The chain is irreducible and aperiodic. Set $`r=p/(1-p)`$. Its unnormalized stationary weights are

```math
w_0=1,\qquad
w_L=r^L,\qquad
w_i=\varepsilon r^i\quad(1\le i\le L-1).
```

For $`S\ge3`$, detailed balance on the first edge reads $`1\cdot\varepsilon p=(\varepsilon r)(1-p)`$. Each edge between interior states has ratio $`r`$, and the last edge reads $`(\varepsilon r^{L-1})p=r^L\varepsilon(1-p)`$. For $`S=2`$ there is only one edge: both directions carry the extra factor, with rates $`\varepsilon p`$ and $`\varepsilon(1-p)`$. Their ratio is again $`r`$, so the endpoint weights above remain correct without an interior-state argument. Normalizing the weights gives the stationary law. [21, §C3][r17]

For completeness, this law also describes the long-time distribution from any initial state. From any memory state $`i`$ to any $`j`$, there is a path through zero of length at most $`2L`$. Positive self-loops at zero pad it to exactly $`2L`$ steps. Consequently every entry of $`P^{2L}`$ is positive. If

```math
\alpha=\sum_j\min_i P^{2L}(i,j)>0,
```

each row contains the same subprobability vector of mass $`\alpha`$. Removing that common part leaves a stochastic residual of mass $`1-\alpha`$. The total-variation distance between two distributions contracts by at most $`1-\alpha`$ every such block. Thus the normalized stationary law is unique and every initial distribution converges to it. If $`\alpha=1`$, convergence after that block is immediate.

Under $`H_+`$ the ratio is two; the stationary law under $`H_-`$ is its reflection about $`L/2`$. With equal priors, choose minus below the midpoint and plus above it. At an integer midpoint either fixed response or a fair random tie has the same Bayes error. Define

```math
D_L=\sum_{i=1}^{L-1}2^i=2^L-2,
\qquad
C_L=\sum_{1\le i\lt{}L/2}2^i
 +\frac12\,2^{L/2}\mathbf1_{\{L\ {\rm even}\}}.
```

The posterior comparison follows directly from the stationary likelihood ratio $`2^{2i-L}`$. For any statewise decision, its equal-prior contribution to error is minimized by the more likely hypothesis. Equivalently, the minimum is half the sum of the smaller of the two stationary masses at each state. Reflection then gives

```math
E_S(\varepsilon)
=\frac{1+\varepsilon C_L}
       {1+2^L+\varepsilon D_L},
\qquad
\lim_{\varepsilon\downarrow0}E_S(\varepsilon)
=\frac1{1+2^{S-1}}.
```

Distributional convergence makes both the limiting instantaneous Bayes error and its time average equal to this stationary value. The formula does not replace the pathwise objective.

**Proposition (small average error, no restoration).** For every fixed $`S\ge2`$ and $`\varepsilon>0`$, the learner above has restoration probability zero under each hypothesis.

**Proof.** Under $`H_+`$, state zero issues an incorrect response; under $`H_-`$, state $`L`$ does. The finite irreducible chain visits each state infinitely often almost surely, by the bounded-path argument in §7.8. Hence each hypothesis produces infinitely many incorrect responses with probability one. ∎

For example, $`S=21`$ and $`\varepsilon=1/1000`$ give the exact stationary Bayes error

```math
E_{21}(1/1000)=\frac{1267}{524812787}
\approx2.41\times10^{-6},
```

while the probability of eventual permanent correctness remains zero. The statement concerns actual repeated incorrect responses, not merely a failure to certify an otherwise correct trajectory.

#### The zero-randomization limit changes the process

Let $`S=3`$ and start at state one. For positive $`\varepsilon`$,

```math
E_3(\varepsilon)=\frac{1+\varepsilon}{5+2\varepsilon}.
```

At $`\varepsilon=0`$, both endpoints become absorbing. The first acquisition moves from state one to an endpoint and determines the permanent response. The error probability is then $`1/3`$ under either hypothesis. At every fixed $`n\ge1`$, the finite-step law is a polynomial in the transition entries, so its error $`e_n(\varepsilon)`$ converges to $`e_n(0)=1/3`$ as $`\varepsilon\downarrow0`$. Therefore

```math
\lim_{\varepsilon\downarrow0}\lim_{n\to\infty}e_n(\varepsilon)
=\frac15,
\qquad
\lim_{n\to\infty}\lim_{\varepsilon\downarrow0}e_n(\varepsilon)
=\frac13.
```

The restoration probability changes as well: it is zero for every positive $`\varepsilon`$, but $`2/3`$ at zero. Removing a positive transition changes recurrent classes. Approaching an error infimum therefore does not justify setting a parameter to zero while retaining the old qualitative conclusion.

The classical finite-memory learning criterion is an asymptotic average error. For equal-prior, time-invariant randomized $`S`$-state tests of Bernoulli parameters $`0<q<p<1`$, the Hellman–Cover infimum is expressed using $`\gamma=p(1-q)/(q(1-p))`$ as $`(1+\gamma^{(S-1)/2})^{-1}`$. Berg, Ordentlich and Shayevitz state that criterion and the randomized infimum explicitly while studying deterministic machines. Here $`\gamma=4`$, matching the limit of the displayed family. The universal optimality assertion belongs to that literature; the calculation above proves this family's law and temporal behavior. [29][memory-origin]; [30, §I][memory-learning].

A vanishing instantaneous error is also insufficient by itself: the harmonic error example in §7.4 has errors tending to zero but infinitely many errors almost surely. The majority construction instead has summable update errors. Conversely, the recovery example in §7.7 shows that finitely many bad visits almost surely need not have finite expected total. Average accuracy, convergence in probability, eventual correctness, expected error count and a finite zero-error declaration must therefore retain their separate definitions.

### 7.10 Fresh switching innovations impose an irreducible conditional risk

An unbounded tally can learn a fixed source frequency. It cannot predict a fresh, unobserved change after its current action has been selected. Let a binary standard evolve by

```math
h_t=h_{t-1}\mathbin{\oplus}B_t,
\qquad t\ge0,
```

where $`\oplus`$ denotes exclusive-or and $`h_{-1}`$ is known. Before issuing $`a_t`$, the controller sees $`h_{t-1}`$ exactly but not $`B_t`$. Correctness means $`a_t=h_t`$. Both responses are initially stipulated safe and permitted under either next standard. [28][r20]

Let $`\mathcal F_t`$ include the entire past, the selected action $`a_t`$, and all randomness used to select it. The innovation is not yet observed. Assume

```math
\Pr(B_t=1\mid\mathcal F_t)=p_t,
\qquad
0\le p_t\le\frac12,
```

for a prescribed deterministic schedule. The next sigma-algebra contains the realized innovation and standard as well as the next selected action. Thus $`E_t=\{a_t\ne h_t\}`$ belongs to $`\mathcal F_{t+1}`$. Conditioning after action selection prevents a shared current random source from secretly predicting an innovation still described as fresh.

**Theorem (switching threshold).** There exists a nonanticipating policy with only finitely many mistakes almost surely under this model if and only if

```math
\sum_{t=0}^{\infty}p_t\lt{}\infty.
```

**Proof.** Conditional on $`\mathcal F_t`$, both the last standard and the selected response are known. Therefore

```math
\Pr(E_t\mid\mathcal F_t)=
\begin{cases}
p_t,&a_t=h_{t-1},\\
1-p_t,&a_t\ne h_{t-1},
\end{cases}
\qquad
\Pr(E_t\mid\mathcal F_t)\ge p_t.
```

If the prescribed sum diverges, the adapted conditional theorem of §7.4 gives infinitely many mistakes almost surely for every admitted policy, including randomized policies with unbounded memory. If the sum converges, choose $`a_t=h_{t-1}`$. A mistake then occurs exactly when $`B_t=1`$. Its probabilities have finite sum, so the first Borel–Cantelli implication gives only finitely many mistakes. The policy needs only the last observed standard; it need not store the schedule or know the current value of $`p_t`$. The environment's potentially time-dependent hazard law remains an explicit premise. ∎

If the risks are instead endogenous or policy-dependent, the conditional lower-bound argument still applies on paths with divergent cumulative conditional risk. The deterministic-schedule existence equivalence does not prove that a greedy current predictor minimizes future endogenous risk.

Several sharp changes of assumption locate this theorem's scope.

**Persistent support uncertainty.** If $`0<p_t\le1/2`$ at every time, both next standards remain possible at every decision. No single response keeps every supported successor in the target. Thus there is no nonempty support-invariant target core for this response model and information timing. A summable positive schedule nonetheless permits eventual correctness almost surely. The support adversary can choose a contrary innovation at every step; almost-sure success is not sure success.

**Earlier observation.** If the current $`h_t`$ is revealed before selection, $`a_t=h_t`$ is always correct. That conclusion belongs to an enlarged information channel.

**Copied rather than fresh innovations.** Draw one bit $`Z\sim{\rm Bernoulli}(\varepsilon)`$, with $`0<\varepsilon<1/2`$, and put $`B_t=Z`$ for every time. Each unconditional flip marginal is still $`\varepsilon`$. After the first transition, the controller learns $`Z=h_0\oplus h_{-1}`$ and selects

```math
a_t=h_{t-1}\mathbin{\oplus}Z
\qquad(t\ge1).
```

Every later response is correct. The conditional **flip probability** is now the known value $`\Pr(B_t=1\mid\mathcal F_t)=Z`$, whereas the chosen policy's conditional **error probability** is zero. These are different quantities. Summing the unchanged unconditional flip marginals would falsely invoke the fresh-innovation theorem.

**Eligibility tied to the new standard.** If response $`a`$ is permitted only when $`a=h_t`$, both alternatives remain possible whenever $`0<p_t<1`$. Neither binary response is then eligible under every supported standard. A statistical predictor is not an authorized restoration policy merely because its expected errors are small. If such uncertainty persists and only an always-permitted, nontarget abstention is available, permitted eventual correctness fails. If uncertainty ceases, that separate eventual situation must be analyzed under its actual menu.

The hypotheses about standards, acquisition laws, target meanings and permissions are not observations established by these calculations. The results identify which memory and information contracts can support the specified objective, while leaving empirical identification and substantive cognitive or normative authority to their own evidence.

### 7.11 Controlled observations and eventual correctness

In §7.8, observations arrive without requiring an incorrect response. An inquiry can have a different structure: an action determines which observation is acquired, and the informative action may itself violate the target. Identifiability under unlimited experimentation then need not yield eventual permanent correctness. The following finite model characterizes when the available good actions can sustain the necessary discrimination. [32]

#### Fixed models, acquired histories and good action sets

Let $`\Theta,A,Y`$ be nonempty finite sets of fixed hidden models, actions and observations. For each $`\theta\in\Theta`$ and $`a\in A`$, a supplied probability vector satisfies

```math
P_{\theta,a}(y)>0,\qquad
\sum_{y\in Y}P_{\theta,a}(y)=1.
```

The true model is chosen once. An action is issued before its observation. Conditional on the complete acquired history, the controller's private seed and the chosen action $`a_t`$, the next observation has law $`P_{\theta,a_t}`$. This is a condition on fresh acquisitions. Equal one-time marginals of copied observations do not satisfy it.

A controller has one common probability space $`(Z,\rho)`$ for its private seed and one measurable policy

```math
\pi:Z\times(A\times Y)^*\longrightarrow A.
```

At time $`t`$ it issues $`a_t=\pi(z,h_t)`$, where $`h_t=((a_0,y_0),\ldots,(a_{t-1},y_{t-1}))`$. The seed is independent of the fresh feedback sources, and neither its law nor the policy depends on the true model. Memory is unrestricted. The length of the history supplies the time index, so no time-homogeneity assumption is imposed.

Each model supplies a fixed target set $`G_\theta\subseteq A`$. Initially every action is stipulated safe and commonly permitted; an explicit additional permission restriction is treated below. Write $`\Pr_\theta^\pi`$ for the law generated by the policy and the controlled observations. Restoration means

```math
\Pr_\theta^\pi
 \bigl(\exists N\ \forall t\ge N:\ a_t\in G_\theta\bigr)=1
\quad\text{for every }\theta\in\Theta.
```

The existential policy quantifier precedes the universal model quantifier. A separate constant successful action for each model does not establish this common-policy requirement. An empty target set makes restoration impossible; allowing that degenerate case will be useful when permissions are imposed. The target sets, observation laws and permission judgments remain separate supplied premises.

For $`U\subseteq A`$, define

```math
E_\theta(U)=
 \{\lambda\in\Theta:
       P_{\lambda,a}=P_{\theta,a}\text{ for every }a\in U\}.
```

A nonempty set $`U`$ is **self-verifying for the target at $`\theta`$** when

```math
U\subseteq G_\theta,
\qquad
U\subseteq G_\lambda\quad
       \text{for every }\lambda\in E_\theta(U).
```

Thus a rival that rejects any action in $`U`$ must differ observationally on some action in $`U`$. The rival need not be identifiable if it accepts the whole set. Here “self-verifying” describes a property of the supplied finite model; it does not mean that the controller issues a finite certificate that its current actions are correct.

**Theorem (controlled-observation restoration).** One common seeded history policy restores almost surely under every model if and only if each model has a nonempty self-verifying target set. Whenever the condition holds, a deterministic history policy suffices. [32–33]

#### Necessity: transferring a recurrent set without stopping at its last exit

Suppose a common policy restores. Under a fixed true model $`\theta`$, let $`U_\infty`$ be the actions used infinitely often. Finiteness of $`A`$ makes $`U_\infty`$ nonempty on every infinite action sequence. Restoration implies $`U_\infty\subseteq G_\theta`$ almost surely. There are only finitely many possible recurrent sets, so some nonempty $`U\subseteq G_\theta`$ occurs with positive probability. On that event, each action outside $`U`$ occurs only finitely often. Consequently, for some deterministic $`N`$,

```math
F(U,N)=\{a_t\in U\text{ for all }t\ge N,
          \text{ and every }a\in U\text{ recurs infinitely often}\}
```

has positive $`\Pr_\theta^\pi`$ probability. No last-exit time is assumed to be a stopping time.

Fix $`\lambda\in E_\theta(U)`$. Include the private seed in the length-$`N`$ prefix. For a finite history $`h=((a_s,y_s))_{s<N}`$, its joint law with the seed has the explicit form

```math
\rho(dz)
\prod_{s<N}
 \mathbf 1\{a_s=\pi(z,h_s)\}
 P_{\theta,a_s}(y_s).
```

The indicator factors are identical under the two models, and every observation factor is strictly positive. Hence their seed-and-prefix laws are mutually absolutely continuous. On the part associated with a compatible history $`h`$, the density ratio is the positive finite number

```math
\prod_{s<N}
 \frac{P_{\theta,a_s}(y_s)}{P_{\lambda,a_s}(y_s)}.
```

After a seed and prefix have been fixed, send the process to a common absorbing cemetery state at its first subsequent action outside $`U`$. The continuation kernels of these killed processes coincide: their policy is the same, and all observation laws for actions in $`U`$ agree. Equality on finite cylinders gives equality of their continuation laws. In particular, they assign the same conditional continuation probability to staying in $`U`$ forever and visiting each member infinitely often.

Integrating that common nonnegative continuation probability against the two equivalent prefix measures transfers positivity of $`F(U,N)`$ to model $`\lambda`$. If some $`a\in U`$ were outside $`G_\lambda`$, this event would contain infinitely many errors under $`\lambda`$, contradicting restoration. Thus $`U\subseteq G_\lambda`$ for every $`\lambda\in E_\theta(U)`$. This proves necessity for the fixed $`\theta`$, and then for every model. Keeping the common seed in the prefix also proves the claim for seeded randomization without presuming a general policy-realization theorem. $`\square`$

#### A constructive policy with the correct physical clock

Choose one nonempty self-verifying set $`U_\lambda`$ for each candidate $`\lambda`$, and fix an ordering of its elements. Its ordered list is a plan. At a completed-plan boundary, compute the acquired likelihood

```math
L_t(\lambda)=\prod_{s<t}P_{\lambda,a_s}(y_s),
```

choose a maximizing candidate using a fixed tie rule, and load its plan. Execute one action at a time until that plan is empty, acquiring and recording fresh feedback after every action. Then choose a new maximizing candidate from the enlarged history. A change of likelihood ranking during a plan does not cancel its remaining actions. [33]

This is a history policy, including on histories it would not itself generate. Start its queue at the plan chosen from the empty likelihood record. Upon appending any action/observation pair, remove one queue element; if the queue becomes empty, refill it using the likelihood of the enlarged record. On actual histories, the recorded action is the queue head. On arbitrary histories, the same recursion still defines a nonempty queue. Every plan is nonempty and finite, so the policy always has an action and never needs an arbitrary empty-queue default.

For the probability argument, fix $`\theta`$ and take independent stacks $`(Y_{a,k})_{k\ge1}`$ with law $`P_{\theta,a}`$, one stack for each action. On its $`k`$th use, action $`a`$ consumes $`Y_{a,k}`$. The controller accesses no unused coordinate. Induction on acquired histories shows that each consistent finite history has exactly the product probability prescribed by the controlled-observation model: each new coordinate is independent of those already acquired and has the required action law. Thus this stack construction generates the actual policy law, rather than a different law whose good behavior is merely assumed to transfer. The general probability-law comparison in §§7.5–7.6 retains its broader scope.

Let $`N_a(t)`$ count uses of action $`a`$ before time $`t`$. The acquired likelihood satisfies the exact identity

```math
\log\frac{L_t(\theta)}{L_t(\lambda)}
 =\sum_{a\in A}\sum_{k=1}^{N_a(t)}
     \log\frac{P_{\theta,a}(Y_{a,k})}
                    {P_{\lambda,a}(Y_{a,k})}.
```

Multiplicity and actual acquisition counts matter in this equation. Replacing repeated uses by set membership, reusing a stack's first observation, or counting plans instead of actions changes the experiment.

For each action, the strong law gives the limiting average of its log ratio as

```math
D_{\theta,\lambda}(a)
 =\sum_{y\in Y}P_{\theta,a}(y)
       \log\frac{P_{\theta,a}(y)}{P_{\lambda,a}(y)}.
```

This finite-alphabet strong law follows by applying the indicator argument in §7.8 to each symbol. All log increments are bounded because the alphabets are finite and the probabilities are positive. Jensen's inequality for the strictly concave logarithm gives $`D_{\theta,\lambda}(a)\ge0`$, with equality exactly when the two probability vectors agree: apply it to $`P_{\lambda,a}(y)/P_{\theta,a}(y)`$, whose $`P_{\theta,a}`$-weighted mean is one.

Work on the probability-one intersection of these finitely many strong-law events. For every informative action, a sufficiently long stack-prefix sum is at least half its positive mean times its length. An action sampled finitely often contributes an eventually fixed finite amount; a noninformative action contributes zero. It follows that the total log ratio tends to positive infinity whenever at least one distinguishing action is sampled infinitely often. This reasoning uses complete stack-prefix limits and then evaluates them at the actual counts; it does not assume that adaptively selected observations form an unconditioned random subsequence.

Call a candidate $`\lambda`$ harmful under $`\theta`$ if $`U_\lambda\nsubseteq G_\theta`$. Self-verification of $`U_\lambda`$ implies that some $`b\in U_\lambda`$ distinguishes $`\lambda`$ from $`\theta`$: otherwise $`\theta\in E_\lambda(U_\lambda)`$ would require $`U_\lambda\subseteq G_\theta`$. If this harmful candidate were selected at infinitely many plan boundaries, every action in its plan, including $`b`$, would be executed infinitely often. The log ratio above would then tend to positive infinity. Eventually $`L_t(\theta)>L_t(\lambda)`$, so $`\lambda`$ could no longer maximize likelihood at a boundary. This is a contradiction.

Only finitely many harmful candidates exist, and each is chosen for finitely many plans almost surely. If $`T_j`$ is the start of plan $`j`$, then

```math
T_0=0,\qquad
T_{j+1}=T_j+|U_{\lambda_j}|,
\qquad 1\le |U_{\lambda_j}|\le |A|.
```

These intervals cover physical time and their endpoints tend to infinity. After the finitely many harmful plans have finished, every actual action belongs to $`G_\theta`$. The physical cutoff is the sum of the preceding plan lengths, not the number of plans. The same deterministic queue policy works under every true model, completing the sufficiency proof. $`\square`$

The earlier construction selects a likelihood maximizer after every action and keeps a separate persistent cyclic pointer through each candidate's set. It is another valid policy: infinitely many selections of a harmful candidate again force every member of its cycle to be used infinitely often, and the same likelihood contradiction applies. Its persistent pointers must not be replaced by restarting the chosen plan at each action. The block policy just proved is the one realized by the later physical-history construction; the two algorithms are not claimed to have identical action laws. [32–33]

#### The greatest good set and a finite decision procedure

The union of two self-verifying sets for $`\theta`$ is self-verifying. A rival agreeing on the union agrees on each set and therefore accepts both. There is consequently a unique greatest such set, with the empty set used when none exists. It can be found without enumerating all subsets.

Start with $`U_0=G_\theta`$ and iterate

```math
U_{k+1}
 =U_k\cap\bigcap_{\lambda\in E_\theta(U_k)}G_\lambda.
```

The operation is contracting and monotone. If $`V\subseteq U`$, then $`E_\theta(U)\subseteq E_\theta(V)`$; hence every member surviving the intersection for $`V`$ also survives it for $`U`$. Any self-verifying $`V\subseteq G_\theta`$ remains in every iterate: a rival agreeing on $`U_k`$ agrees on $`V`$ and accepts all its actions. After at most $`|G_\theta|`$ strict deletions, the sequence stabilizes at a set $`K_\theta`$. A nonempty fixed point satisfies precisely the self-verification condition, and the preceding inclusion shows that it contains every other self-verifying set. Therefore

```math
\text{common almost-sure restoration exists}
\quad\Longleftrightarrow\quad
K_\theta\ne\varnothing\text{ for every }\theta.
```

Each deletion has a finite witness: a rival that agrees on every currently retained action but rejects the deleted action. The witnesses must be checked at their actual elimination stages. For $`n=|\Theta|`$, $`m=|A|`$ and $`d=|Y|`$, direct repeated rational-vector comparison takes $`O(n^2m^2d)`$ rational comparisons over all models. This counts comparisons of supplied exact probabilities, not bit operations, acquisition costs or authentication work. For arbitrary real inputs, exact equality and likelihood comparison remain mathematical operations; no general effective procedure for presenting such reals is assumed.

Two rounds can be essential. In the following table, entries are the probabilities of observing one, with $`Y=\{0,1\}`$:

| Model | $`G_\theta`$ | Action $`a`$ | Action $`b`$ |
|---|---|---:|---:|
| $`0`$ | $`\{a,b\}`$ | $`1/2`$ | $`1/2`$ |
| $`1`$ | $`\{a\}`$ | $`1/2`$ | $`1/2`$ |
| $`2`$ | $`\{b\}`$ | $`1/2`$ | $`2/3`$ |

For model zero, the first step removes $`b`$ because model one agrees on both actions and rejects $`b`$. Once only $`a`$ remains, model two also becomes indistinguishable and removes $`a`$. Thus $`U_0=\{a,b\}`$, $`U_1=\{a\}`$, $`U_2=\varnothing`$. A single filtering pass would return a false positive.

Three monotonicity statements follow directly from valid-set inclusion. Adding rival models can only shrink an old model's greatest set. Enlarging all target sets can only enlarge these sets. Applying a common observation garbling at each action preserves old equalities of observation laws and can add new equalities, so it can only shrink the greatest sets. The restoration interpretation of the last statement requires the garbled model to retain the theorem's stated observation hypotheses. None of these order statements selects the true target or establishes its authority. [32]

#### A fixed permission menu

Let $`\Gamma\subseteq A`$ be a supplied common static menu. Require $`\pi(z,h)\in\Gamma`$ for every seed and every finite history, including histories the policy never generates. Such a policy with almost-sure restoration under every model exists exactly when the greatest-set calculation for the restricted targets

```math
G_\theta^{\Gamma}=G_\theta\cap\Gamma
```

is nonempty for every model. [33]

For necessity, all-time menu membership and eventual target membership imply eventual membership in $`G_\theta^\Gamma`$, so the theorem applies. For sufficiency, use its nonempty greatest sets as the queue plans. Every initial plan and every replacement plan lies in $`\Gamma`$, and every residual queue is a nonempty suffix of such a plan. Induction on arbitrary finite histories proves that every issued action is in $`\Gamma`$. This includes malformed histories containing earlier actions outside the menu. The queue never empties at a decision, so an out-of-menu fallback value cannot be used. Eventual membership in the restricted target implies eventual membership in the original target.

If $`\Gamma`$ is empty or some target misses it, no such policy exists. Early target errors may still be permitted; eventual correctness alone does not establish all-time permission. The result concerns a fixed common menu. History-dependent or model-dependent permissions require another analysis, and no statistical concentration result authenticates the menu's authority.

#### Positive and negative cases

**Information available only through bad actions.** Take two models, actions $`r_0,r_1,q`$, and $`G_0=\{r_0\}`$, $`G_1=\{r_1\}`$. Both repair actions emit a fair bit under either model. The probe $`q`$ emits a Bernoulli bit of parameter $`1/3`$ under zero and $`2/3`$ under one. All actions are permitted, but $`q`$ is target-bad under both models. Neither singleton target is self-verifying, so no common almost-surely restorative policy exists, even with unrestricted memory and adaptive probing.

Nevertheless, for any $`\delta>0`$, take $`2m`$ probe samples and commit to their majority, with $`m`$ chosen so that $`(8/9)^m\le\delta`$. The already proved calculation in §7.8 gives restoration probability at least $`1-\delta`$ under both models. Only finitely many probe actions occur, but a wrong commitment makes infinitely many subsequent errors. Arbitrarily high finite-confidence success is different from one probability-one guarantee. Infinite probing identifies the model almost surely and fails restoration because the probes remain bad. [32]

**Good actions that sustain discrimination.** If both $`r_0`$ and $`r_1`$ instead have different positive observation laws under the two models, each singleton target becomes self-verifying. The constructive policy restores while continuing to acquire information through its eventual good actions. If only $`r_0`$ is informative while $`r_1`$ remains indistinguishable, only the first target has a valid set; there is still no policy restoring under both. The quantifier over every possible true model is essential.

**Correct decisions without exact identification.** If two models have identical observation laws at every action but both accept $`c`$, the constant policy $`c`$ restores under both. Their disagreement about other actions and their unidentified model labels do not obstruct this decision. Conversely, identical complete observation laws and disjoint target sets give empty greatest sets, even though each model individually admits a successful constant action.

**Why a plan cannot be restarted after every observation.** Let $`G_0=\{a,b\}`$ and $`G_1=\{c\}`$. At $`a`$ both models emit a fair bit; at each of $`b,c`$ they emit Bernoulli bits with respective parameters $`1/3,2/3`$. Both target sets are self-verifying. Choose model zero in a likelihood tie and order its plan as $`(a,b)`$. A rule that recomputes a maximizer after every action and always restarts its plan chooses $`a`$ forever: those observations never break the tie. It therefore fails under model one. The queue executes $`b`$ before replanning, and the persistent-pointer alternative also eventually reaches $`b`$. Their proofs rely on those actual actions, not just the existence of an informative member in an unexecuted plan.

**Freshness and permissions remain separate.** Copying one biased root bit forever retains the same one-time marginals but violates the conditional fresh-observation premise; the common positive-probability report words give the impossibility proved in §7.8. Likewise, if only a universally licensed abstention survives the common menu and it belongs to neither target, restricting the targets to that menu yields empty greatest sets. Neither many repeated reports nor a high likelihood supplies a missing acquisition or permission.

**Zero probabilities change the criterion.** Keep the opposing singleton targets and uninformative repair actions in the first example, but make $`q`$ reveal the true model exactly. One probe followed by the corresponding repair restores surely. The singleton good sets still fail the equality-based condition, because their own observation laws agree. The finite-prefix absolute-continuity premise has now failed: the probe has disjoint outcome supports. This is a counterexample to extending the stated necessity beyond its full-support domain; separate constructive results with zero probabilities do not establish the same unrestricted equivalence.

#### A general obstruction after informative probing ends

The deterministic-prefix argument has a useful extension beyond finite action spaces. Fix two models on common standard Borel action, observation and controller-record spaces. Fix one common measurable causal policy, including its randomization, and the corresponding regular continuation kernels. The record contains the acquired history and all private state needed for future policy behavior; its update rule and future randomization kernels are common. Let $`R`$ be a measurable class of nonprobe actions. Assume that the controlled observation kernels agree under both models whenever an action in $`R`$ is chosen at a common record. Assume also that their complete finite-prefix laws are mutually absolutely continuous. Finally, let $`B_\theta,B_\lambda`$ be disjoint measurable successful-tail events, each of which entails that only finitely many actions fall outside $`R`$. Then no common policy has probability-one success under both models. [32, §4]

To prove this, suppose $`\Pr_\theta^\pi(B_\theta)=1`$. For some deterministic $`N`$,

```math
\Pr_\theta^\pi
 \bigl(B_\theta\cap\{a_t\in R\text{ for all }t\ge N\}\bigr)>0.
```

Let $`\mu_\theta^N,\mu_\lambda^N`$ be the prefix laws. Kill the future process on leaving $`R`$. Equality of the common policy and nonprobe kernels gives one measurable subprobability continuation kernel $`Q_N`$ under both models. For the indicated full-path event, including its prefix-dependent success condition, its probabilities are

```math
\int Q_N(h,B_\theta)\,\mu_\theta^N(dh)
\quad\text{and}\quad
\int Q_N(h,B_\theta)\,\mu_\lambda^N(dh).
```

The first is positive, and $`\mu_\theta^N\ll\mu_\lambda^N`$ makes the second positive. The transferred paths lie outside $`B_\lambda`$, contradicting probability-one success there. Standard Borel spaces and the specified common continuation kernels make the disintegration and measurable-kernel statement meaningful; equivalent finite prefixes by themselves do not make arbitrary infinite-tail laws equivalent. No conditioning on the final probe is used. $`\square`$

An independently proved fact that increasingly accurate repair sequences encode the hidden norm can supply the disjoint success events in this proposition. The proposition does not establish that geometric encoding or authenticate the norm-to-observation relation. It also does not exclude a finite-confidence rule, a singular revealing probe, or continued informative target-good behavior, all of which alter its premises.

Controlled testing and robust policies have substantial antecedents. Bovy and collaborators study one policy under a fixed but unknown member of a finite family of partially observed models, with finite-horizon and discounted reward criteria and linear-program constructions. [34] Kaufmann, Cappé and Garivier give an adaptive bandit change-of-measure inequality at an almost-surely finite stopping time. [35, Lemma 1] Those settings help locate the present comparison; the last informative probe is not automatically a stopping time to which that lemma applies. The qualitative target-dependent criterion here also retains the distinction from the common observed-state parity objective discussed in §7.8. No historical priority claim follows.

The finite greatest-set test and the infinite-time policy theorem answer different computational questions. The policy uses growing acquired likelihoods; it supplies no general finite-memory bound, deterministic last-error time, finite zero-error declaration, expected physical error budget or arbitrary-real implementation. In particular, the historical finite enumeration and formal implementation evidence retain their own source and execution boundaries. The mathematical result concerns the stated observation laws, targets and permissions; empirical truth, normative warrant and the unfinished broader account of collective inquiry require their own arguments.

## 8. What final judgments identify about evidence use

The previous sections ask what information a strategy or coordination mechanism needs. The converse question is different: what does a successful collective answer reveal about how the answer was produced? A group can produce informative, accurate answers without the available observations identifying each member's causal contribution. The following construction proves this limitation while preserving both a real two-input mechanism and a real one-input alternative. [11][r11]

### 8.1 Two mechanisms with the same complete answer law

Fix a stimulus $`x\in\mathbb R`$, a variance $`v>0`$, a variance ratio $`k>1`$ and an announcer $`a\in\{B,W\}`$ with output-noise variance $`r_a\ge0`$. On each trial let $`Z_B,Z_W,Z_A`$ be independent standard normal variables, with fresh independent triples across trials. Define the two private observations

```math
X_B=x+\sqrt v\,Z_B,\qquad
X_W=x+\sqrt{kv}\,Z_W,
```

and put

```math
\alpha=\frac{k-1}{k+1}>0,\qquad
\beta=\frac{2}{k+1}>0.
```

Compare two mechanisms:

| Mechanism | Latent score | Announced answer |
|---|---|---|
| Single-input mechanism $`L`$ | $`T_L=X_B+\sqrt{r_a}\,Z_A`$ | $`Y_L=\mathbf1\{T_L>0\}`$ |
| Two-input mechanism $`P`$ | $`T_P=\alpha X_B+\beta X_W+\sqrt{r_a}\,Z_A`$ | $`Y_P=\mathbf1\{T_P>0\}`$ |

The hypothetical unaided threshold readouts of $`X_B`$ and $`X_W`$ have maximum response-curve slopes $`1/\sqrt{2\pi v}`$ and $`1/\sqrt{2\pi kv}`$. These are model quantities, not an assertion that participants formed or reported private decisions, or that human capacities remain stable across experimental conditions.

The two-input weights are deliberately chosen to preserve the observable variance:

```math
\alpha+\beta=1,\qquad \alpha^2+k\beta^2=1.
```

**Theorem 15 (answer-law nonidentification).** For every permitted parameter choice,

```math
T_L\sim T_P\sim N(x,v+r_a),\qquad
\Pr(Y_L=1)=\Pr(Y_P=1)
=\Phi\!\left(\frac{x}{\sqrt{v+r_a}}\right).
```

For any fixed finite schedule of stimuli and announcers, the entire answer-vector law is the same under the two mechanisms. This remains true for any common exogenous joint distribution of that complete schedule, independent of the trial noises.

**Proof.** The single-input score has the stated normal mean and variance. The two-input score has mean $`(\alpha+\beta)x=x`$ and variance $`(\alpha^2+k\beta^2)v+r_a=v+r_a`$. Normality follows from linear combination of independent normal variables. The threshold probabilities therefore agree. Conditional on a fixed schedule $`D=((x_t,a_t))_{t=1}^n`$, fresh noises make both answer laws the identical product of Bernoulli laws with parameters $`\Phi(x_t/\sqrt{v+r_{a_t}})`$. Integrating against the same joint law of $`D`$ proves the final claim. ∎

Thus both mechanisms have the same psychometric curve, the same maximum slope $`1/\sqrt{2\pi(v+r_a)}`$, and, for nonzero stimulus with correct answer determined by its sign, the same accuracy $`\Phi(|x|/\sqrt{v+r_a})`$. Announcer-specific output noise may change these values while preserving the equivalence.

This is not an algebraic disguise of the same causal rule. In $`P`$ both coefficients are strictly positive; changing either input while holding the other fixed changes its score. When $`k=3`$, the two-input mechanism is the ordinary mean of the two observations. The restriction $`k>1`$ matters: at $`k=1`$, $`\alpha=0`$, so the purported two-input mechanism ceases to use both inputs. Zero output noise is permitted and does not break Theorem 15.

The schedule's **joint** law also matters. Equality of individual stimulus marginals does not suffice. Take a fixed announcer, a positive $`c`$ and let $`p=\Phi(c/\sqrt{v+r_a})>1/2`$. A schedule that repeats a common random sign, $`(c,c)`$ or $`(-c,-c)`$ with equal probabilities, has the same marginal stimulus distribution at each time as a schedule that reverses that sign, $`(c,-c)`$ or $`(-c,c)`$. Yet the first produces answer agreement with probability $`p^2+(1-p)^2`$ and the second with probability $`2p(1-p)`$. The theorem compares complete specified designs, not isolated marginals.

### 8.2 Causal influence is compatible with observational equivalence

An intervention replaces an input equation while retaining the other independent noises. Under $`\mathrm{do}(X_W=w)`$,

```math
\Pr_L(Y=1\mid\mathrm{do}(X_W=w))
=\Phi\!\left(\frac{x}{\sqrt{v+r_a}}\right),
```

whereas

```math
\Pr_P(Y=1\mid\mathrm{do}(X_W=w))
=\Phi\!\left(
\frac{\alpha x+\beta w}{\sqrt{\alpha^2v+r_a}}
\right).
```

The first is constant in $`w`$ and the second is strictly increasing. Likewise,

```math
\Pr_P(Y=1\mid\mathrm{do}(X_B=b))
=\Phi\!\left(
\frac{\alpha b+\beta x}{\sqrt{\beta^2kv+r_a}}
\right)
```

is strictly increasing in $`b`$. Under $`L`$, replacing $`X_B`$ changes the answer directly; if $`r_a=0`$ it becomes the deterministic threshold $`\mathbf1\{b>0\}`$. Hence the models differ about genuine causal use even when the entire answer-only record has the same distribution.

A passive record of $`(X_B,X_W,Y)`$ also separates them. With positive output noise, the conditional response under $`L`$ depends only on $`X_B`$, whereas under $`P`$ it depends strictly on both inputs. With zero output noise, the separating lines $`X_B=0`$ and $`\alpha X_B+\beta X_W=0`$ still differ on sets with positive Gaussian probability. Enlarging the observable record changes the identification problem; it does not contradict the answer-only theorem.

### 8.3 Adaptation cannot manufacture a missing channel

The fixed-design result does not, by itself, assert equality for every adaptive experiment. A later extension supplies explicit conditions under which that equality does persist. [12, §§1–2][r12]

**Theorem 16 (adaptive answer-only equivalence).** At each stage let a common nonanticipating policy choose the next stimulus, announcer or stopping decision from the past recorded designs and answers and a common independent random seed. Keep the model parameters fixed. Conditional on that history and the chosen next design, draw a fresh independent normal noise triple with the law specified above. The policy has no access to hidden observations, model-specific refusal channels or interventions on the input mechanisms. Then the two models give the same law to the entire adaptive recorded experiment, including eventual stopping and the reported result.

**Proof.** Include the common policy randomization in the history. At the initial stage its distribution is the same under both models. Whenever the recorded histories agree in distribution, applying the same policy kernel gives the same distribution for the next design or stop. On continuing, Theorem 15 applied conditionally to the chosen design gives the same next-answer law, because the fresh noise triple is independent of the history. Induction therefore gives equality of every finite transcript. Pad a stopped transcript by an absorbing stop symbol. Equality on all finite cylinder events determines the same probability law on the countable sequence space, so every measurable stopping event and reported-result event has the same probability. ∎

This result allows genuine new answer trials: their conditional likelihood ratios are still one. It is not restricted to reusing the same answer record. But endogenous human designs, interventions, hidden-variable access, model-dependent missingness and retained internal records require a new argument; the conditional-freshness and common-policy assumptions cannot be inferred from the word “adaptive.”

The same reasoning has a simpler static form. If the answer record has common law $`\mu`$ and an analysis or audit uses a common kernel $`K`$, its output law is

```math
\Pr(\text{analysis output}\in A)=\int K(d,A)\,\mu(dd)
```

under both models. Randomized reanalysis, a summary statistic or an answer-only adjudication cannot distinguish them. An audit that actually receives an additional informative record changes the premise.

For two fully specified candidate models with positive prior probabilities, identical answer likelihoods leave their posterior odds equal to their prior odds. They do not make unequal priors equal. Nor do they make these two models equally warranted in every other respect, prevent evidence from favoring both over a third model, or prove that causal explanation is impossible. For composite models, the same conclusion requires equality of their induced observable laws after integrating their parameter priors; a convenient pairing of parameters is insufficient. The limitation is a precisely identified observational one.

## 9. Linked evidence and the limits of statistical discrimination

The following positive and negative results use the same received collective-evidence construction, including its later finite and sequential arguments. [11][r11]

### 9.1 One additional linked observation can be informative

The observational equivalence can be broken by retaining a within-trial link between an input and the final answer.

The readout is passive: recording $`X_W`$ or its binary threshold is assumed not to change the structural equations. All covariance comparisons below condition on the declared stimulus $`x`$ and announcer $`a`$. Pooling trials with varying stimuli can create summary–answer or linked-bit–answer association even in $`L`$: although conditional covariance vanishes there, both conditional means can vary with the common stimulus. Such pooled association alone therefore cannot identify a member's causal contribution. The construction does not establish feasible passive access to an actual person's private state. [11, linked-record analysis][r11] [12, §3.1][r12]

Set $`\sigma^2=v+r_a`$ and let $`\phi`$ be the standard normal density.

**Proposition 17 (a linked real-valued record).**

```math
\mathrm{Cov}_L(X_W,Y)=0,\qquad
\mathrm{Cov}_P(X_W,Y)
=\frac{\beta kv}{\sigma}\,
\phi\!\left(\frac{x}{\sigma}\right)>0.
```

**Proof.** In $`L`$, $`X_W`$ is independent of $`T_L`$ and hence of its threshold. In $`P`$ the pair $`(X_W,T_P)`$ is jointly normal, with covariance $`\beta kv`$. Its conditional mean is

```math
\mathbb E[X_W-x\mid T_P]
=\frac{\beta kv}{\sigma^2}(T_P-x).
```

Therefore the covariance with $`\mathbf1\{T_P>0\}`$ equals $`(\beta kv/\sigma^2)\mathbb E[(T_P-x)\mathbf1\{T_P>0\}]`$. Standardizing $`T_P=x+\sigma Z`$, the latter expectation is
$`\sigma\int_{-x/\sigma}^{\infty}z\phi(z)\,dz=\sigma\phi(x/\sigma)`$, proving the formula. ∎

Even a binary linked record can suffice. Let

```math
Q=\mathbf1\{X_W>0\}.
```

Under $`L`$, $`Q`$ and $`Y`$ are independent. Under $`P`$,

```math
g(w)=\Pr_P(Y=1\mid X_W=w)
=\Phi\!\left(
\frac{\alpha x+\beta w}{\sqrt{\alpha^2v+r_a}}
\right)
```

is strictly increasing and lies strictly between zero and one. Write $`\pi=\Pr(X_W>0)\in(0,1)`$ and $`\mu_+=\mathbb E[g(X_W)\mid X_W>0]`$, $`\mu_-=\mathbb E[g(X_W)\mid X_W\le0]`$. The positive Gaussian density and strict monotonicity give $`\mu_+>g(0)>\mu_-`$. Consequently,

```math
\mathrm{Cov}_P(Q,Y)
=\pi(1-\pi)(\mu_+-\mu_-)>0.
```

The conclusion is separation in distribution, not perfect classification of one observed pair. Every one of the four binary pairs has positive probability under both mechanisms, including when output noise is zero. Every finite paired data string is therefore possible under both. The linked record supplies evidence, not a finite error-free selector.

Now let a recording error independently flip $`Q`$ with probability $`\varepsilon`$. With an independent Bernoulli error $`E`$,

```math
Q'=Q+E-2QE,\qquad
\mathrm{Cov}(Q',Y)=(1-2\varepsilon)\mathrm{Cov}(Q,Y).
```

For $`0\le\varepsilon<1/2`$ the separation remains positive. At $`\varepsilon=1/2`$, $`Q'`$ is a fair bit independent of every pre-error variable; with fresh independent recording errors across trials the entire paired record again has the same law under both models. For $`\varepsilon>1/2`$, reversing the recorded bit restores a positive separation if the error regime is known. Dependent, adversarial or unmodelled errors are not covered by this formula.

The link itself is part of the information. At zero stimulus the unary bit marginals are fair in both models. Authentic observations of $`Q'`$ and $`Y`$ taken from disjoint independent trials therefore give the same independent pair law under both models. A within-trial link is needed for the covariance witness. This is not a blanket claim that every shuffle of a finite data array destroys all dependence; different observation procedures must be modelled as such.

### 9.2 A finite guarantee requires a declared separation

Fix one design and independent identically distributed paired trials. Let $`p=\mathbb E Q'`$ and $`q=\mathbb E Y`$, which are common to the paired models, and let

```math
\delta=\mathbb E_P[Q'Y]-pq>0.
```

Under $`L`$ the corresponding covariance is zero. Suppose first that the baseline $`pq`$ and a positive lower bound $`\delta_0\le\delta`$ are known. Select $`P`$ when

```math
\frac1n\sum_{t=1}^n Q'_tY_t
\ \ge\ pq+\frac{\delta_0}{2},
```

and otherwise select $`L`$.

**Proposition 18 (finite separated test).** Each error probability is at most

```math
\exp(-n\delta_0^2/2).
```

Thus $`n\ge2\log(1/\eta)/\delta_0^2`$ suffices for each error to be at most $`\eta\in(0,1)`$.

**Proof.** If $`Z`$ is Bernoulli with mean $`m`$, put $`\psi(\lambda)=\log\mathbb E e^{\lambda(Z-m)}`$. Then $`\psi(0)=\psi'(0)=0`$ and $`\psi''(\lambda)`$ is the variance of a tilted Bernoulli variable, hence at most $`1/4`$. Integrating twice gives $`\psi(\lambda)\le\lambda^2/8`$ for every real $`\lambda`$. Independence, Markov's inequality and the choice $`\lambda=4t`$ give

```math
\Pr\!\left(\overline Z-m\ge t\right)
\le\exp(-2nt^2).
```

Using $`\lambda=-4t`$ proves the same lower-tail bound. Under $`L`$ the upper-tail distance is $`\delta_0/2`$; under $`P`$ the lower-tail distance to the threshold is at least $`\delta_0/2`$. These give the asserted bounds. Assigning equality to $`P`$ does not invalidate either bound. ∎

The source supplies a concrete exact case. Set $`x=0,v=1,k=3,r_a=0,\varepsilon=0`$. For independent standard normals $`U,V`$,

```math
Q=\mathbf1\{V>0\},\qquad
Y_P=\mathbf1\{U+\sqrt3V>0\}.
```

Rotational symmetry makes the angle of $`(U,V)`$ uniform. The two positive half-planes intersect in a sector of angle $`5\pi/6`$: in polar coordinates the conditions are $`0<\theta<\pi`$ and $`\cos(\theta-\pi/3)>0`$, so their intersection is $`0<\theta<5\pi/6`$. Hence

```math
\Pr_P(Q=1,Y=1)=\frac5{12},\qquad
\Pr_L(Q=1,Y=1)=\frac14,\qquad
\delta=\frac16.
```

With $`n=216`$, choose $`P`$ when the joint-positive count is at least $`72`$. Each error is at most $`e^{-3}<1/20`$. These are parameters and guarantees of an exact illustrative model, not a report of performed trials or a recommendation for a particular empirical study.

There is no comparable uniform finite guarantee over all positive separations. For binary variables with the same unary marginals, a covariance difference $`\delta`$ changes the four cells by $`(+\delta,-\delta,-\delta,+\delta)`$. The one-pair total variation distance is exactly $`2\delta`$. For $`n`$ independent pairs, the product-law telescoping identity and the triangle inequality give total variation at most $`2n\delta`$. For any possibly randomized test, the sum of its two errors is therefore at least

```math
1-2n\delta.
```

Indeed, writing the probability of selecting $`P`$ as a test function $`f\in[0,1]`$, the sum is $`1-(\mathbb E_Pf-\mathbb E_Lf)`$, and that expectation difference is at most total variation. In the concrete model above, independent recording error gives $`\delta=(1-2\varepsilon)/6`$, arbitrarily close to zero as $`\varepsilon\uparrow1/2`$. Large stimulus magnitude also shrinks the separation. Strictly positive identifiability alone supplies no uniform finite sample size.

### 9.3 A sequential positive witness without a promised effect size

The known baseline and lower separation bound can be removed if the procedure is allowed to continue indefinitely under the null. Retain fixed-design independent identically distributed paired trials and a strictly positive separation under $`P`$. Define

```math
\widehat p_n=\frac1n\sum_{t=1}^n Q'_t,\qquad
\widehat q_n=\frac1n\sum_{t=1}^n Y_t,\qquad
\widehat b_n=\frac1n\sum_{t=1}^n Q'_tY_t,\qquad
\widehat c_n=\widehat b_n-\widehat p_n\widehat q_n.
```

For $`\gamma\in(0,1)`$ put

```math
e_n=\sqrt{\frac{\log(6n(n+1)/\gamma)}{2n}},
\qquad
\tau=\inf\{n\ge1:\widehat c_n>3e_n\}.
```

On stopping, declare a positive contribution witness, namely $`P`$ within this specified pair of models. The procedure never declares $`L`$.

**Theorem 19 (time-uniform positive detection).** Under $`L`$, the probability of ever stopping is at most $`\gamma`$. Under every fixed $`P`$ with $`\delta>0`$, $`\tau<\infty`$ almost surely.

**Proof.** Apply the two-sided bound proved above to each of the three Bernoulli means. At each time, each failure probability at tolerance $`e_n`$ is at most $`\gamma/(3n(n+1))`$. A union bound over the three means and all $`n`$, using $`\sum_{n\ge1}1/(n(n+1))=1`$, gives an event $`G`$ of probability at least $`1-\gamma`$ on which all three mean errors are at most $`e_n`$ at every time. Since all means lie in $`[0,1]`$,

```math
|\widehat p_n\widehat q_n-pq|
\le|\widehat p_n-p|+|\widehat q_n-q|
\le2e_n.
```

Thus $`|\widehat c_n-\delta|\le3e_n`$ throughout $`G`$. Under the null $`\delta=0`$, the strict stopping inequality cannot occur on $`G`$, proving the false-positive bound.

Almost-sure detection requires a separate argument: $`G`$ itself has only probability at least $`1-\gamma`$. For every positive rational tolerance, the fixed-tolerance concentration probabilities are summable in $`n`$. The Borel–Cantelli argument, applied to the three means and countably many such tolerances, shows their almost-sure convergence to $`p,q,b`$. Hence $`\widehat c_n\to\delta>0`$ almost surely, while $`e_n\to0`$. Eventually the strict stopping inequality holds. ∎

This is an exact-real mathematical stopping rule. A numerical implementation needs a certified comparison whose approximation error tends to zero: for example, a certified lower bound for $`\widehat c_n`$ and upper bound for $`3e_n`$. An arbitrarily loose conservative threshold can protect the false-positive bound while destroying eventual detection. No finite uniform detection time follows, and failure to stop is not a negative contribution certificate.

### 9.4 Why a uniformly reliable two-answer procedure cannot always stop

The inability to declare the null after a uniformly bounded amount of ambiguous evidence is structural.

**Theorem 20 (null-termination obstruction).** Fix $`x=0,v=1,k=3,r_a=0`$ and allow independent recording errors $`0\le\varepsilon<1/2`$. There is no single nonanticipating sequential procedure whose terminal decision is either $`L`$ or $`P`$, with common independent auxiliary randomization, satisfying all three conditions:

1. It terminates almost surely under the single-input model.
2. Its probability of declaring $`P`$ under that model is at most $`\gamma`$.
3. Under every two-input model in this family, its probability of declaring $`L`$ is at most $`\zeta`$, where $`\gamma+\zeta<1`$.

**Proof.** Under the single-input model, each paired observation is uniform on the four cells, independently of $`\varepsilon`$; call this common null law $`L_0`$. The alternative has the same fair marginals and covariance $`\delta=(1-2\varepsilon)/6\downarrow0`$.

Let $`A_N`$ be the event that the procedure declares $`L`$ by time $`N`$. Null almost-sure termination and condition 2 give $`\Pr_{L_0}(\bigcup_N A_N)\ge1-\gamma`$. Choose $`\eta>0`$ with $`\gamma+\zeta+2\eta<1`$ and then a finite $`N`$ with $`\Pr_{L_0}(A_N)>1-\gamma-\eta`$. Choose an alternative with $`2N\delta<\eta`$. Its first $`N`$ pairs have total variation distance at most $`2N\delta`$ from the null. Appending the common independent seed and applying the common procedure cannot increase that distance. Consequently,

```math
\Pr_P(A_N)>1-\gamma-2\eta>\zeta,
```

contradicting condition 3. ∎

The argument needs neither almost-sure termination under the alternatives nor a finite expected running time. It rules out this uniform combination of guarantees, not every useful sequential method. A lower bound on effect size, a weaker error demand, an additional measurement channel or permission to withhold a negative answer changes the problem.

## 10. Choosing an informative inquiry and revising its calibration

Identifiability asks whether laws differ. An inquiry decision also needs a loss function, a prior and the cost and availability of obtaining the proposed observation. The source's exact linked-bit example permits these ingredients to be calculated transparently. This calculation concerns the specified two-model decision problem, not an empirical valuation of cognition. [12, §3][r12]

### 10.1 The distinguishing information is an interaction

Continue with $`x=0,v=1,k=3,r_a=0`$ and independent bit error $`0\le\varepsilon\le1/2`$. The linked pair $`(Q',Y)`$ has fair unary marginals in both models. Write $`\delta=(1-2\varepsilon)/6`$. In the cell order $`(0,0),(0,1),(1,0),(1,1)`$, the laws are

```math
P_L=
\begin{pmatrix}
1/4&1/4\\
1/4&1/4
\end{pmatrix},
\qquad
P_P=
\begin{pmatrix}
1/4+\delta&1/4-\delta\\
1/4-\delta&1/4+\delta
\end{pmatrix}.
```

Their difference is the interaction $`\delta(1,-1)\otimes(1,-1)`$. It has rank one when $`\delta\ne0`$ and rank zero at $`\varepsilon=1/2`$, where $`\delta=0`$. Summing either index gives zero. Keeping both unary distributions therefore loses exactly the distinction at issue. Preserving the within-trial interaction retains it.

### 10.2 An exact value of information

Give the two models equal prior probability and evaluate an estimate $`a\in[0,1]`$ of the indicator of model $`P`$ by squared loss $`(a-\mathbf1_P)^2`$. At posterior probability $`q`$ the expected loss is

```math
q(a-1)^2+(1-q)a^2=(a-q)^2+q(1-q).
```

Thus the optimal estimate is the posterior itself, with risk $`q(1-q)`$. Before the query the risk is $`1/4`$.

A concordant pair, $`Q'=Y`$, gives posterior

```math
q_{\mathrm{same}}=\frac{1/4+\delta}{1/2+\delta},
```

and a discordant pair gives

```math
q_{\mathrm{different}}=\frac{1/4-\delta}{1/2-\delta}.
```

The predictive probabilities of these events are respectively $`1/2+\delta`$ and $`1/2-\delta`$. Since the expected posterior is its prior $`1/2`$, the reduction in optimal expected squared loss is the posterior variance:

```math
V=\frac14-\mathbb E[q(1-q)]
=\mathbb E[(q-1/2)^2].
```

Substitution gives the exact value

```math
V=
\left(\frac12+\delta\right)
\frac{\delta^2}{4(1/2+\delta)^2}
+
\left(\frac12-\delta\right)
\frac{\delta^2}{4(1/2-\delta)^2}
=\frac{\delta^2}{1-4\delta^2}.
```

| Independent bit-error probability | $`\delta`$ | Posterior after concordance | Posterior after discordance | Value $`V`$ |
|---:|---:|---:|---:|---:|
| $`0`$ | $`1/6`$ | $`5/8`$ | $`1/4`$ | $`1/32`$ |
| $`1/4`$ | $`1/12`$ | $`4/7`$ | $`2/5`$ | $`1/140`$ |
| $`1/2`$ | $`0`$ | $`1/2`$ | $`1/2`$ | $`0`$ |

At zero recording error the posterior expected risk is $`7/32`$, improving on $`1/4`$ by $`1/32`$. If the query costs $`c=1/64`$ in the same loss units, it is beneficial at zero error and not beneficial at error $`1/4`$. An answer-only query has value zero for discriminating this pair under the common observation contract, even if it is an authentic new trial. It can still be valuable for a different target, such as learning the stimulus.

The calculation assumes that the linked record is available at the stated cost and that the two-model prior and loss are appropriate for the decision. It does not establish either assumption, exclude additional candidate mechanisms, or choose the ethically or epistemically correct loss. Positive value in this model is not a global ranking of research programmes.

### 10.3 Calibration repair replaces the old contribution

Suppose one concordant paired observation was initially evaluated with $`\varepsilon=0`$. Its likelihood ratio for $`P`$ over $`L`$ is

```math
\frac{1/4+1/6}{1/4}=\frac53,
```

which changes prior odds one to posterior probability $`5/8`$. If justified calibration later changes the same recording channel to $`\varepsilon=1/4`$, the correct likelihood ratio for this **same observation** becomes

```math
\frac{1/4+1/12}{1/4}=\frac43,
```

and its corrected posterior is $`4/7`$. Multiplying both ratios would give odds $`20/9`$ and probability $`20/29`$, falsely treating one record under two calibrations as two independent observations.

The product can be appropriate for two genuinely independent records, one from each specified channel. It is inappropriate merely because a different copy, report or analysis presents the original observation. A root-aware record of what was observed must be joined to a scientific model of dependence; identity alone supplies no likelihood factorization.

Uncertain calibration must also remain coupled to the model and record whose likelihood it changes. A Bayesian treatment can integrate a common calibration model with a declared prior. A robust treatment can retain an admissible set of common calibrations. Choosing a convenient endpoint separately for each hypothesis or multiplying an audit result as independent when it depends on the same observation changes the model. If a calibration audit supplies new information, its appropriate contribution is the joint law of the observation and audit, or a justified conditional factorization of that law.

These corrections preserve the earlier statistical limits. An informative linked channel admits a positive contribution witness under its hypotheses. It does not supply an effect-size lower bound, a finite uniform decision time, or certainty that a persistent lack of evidence establishes absence of contribution.

## 11. Scientific interpretation and remaining questions

The results distinguish four objects often conflated in discussion of collective intelligence: the evidence available somewhere in a group; the information available to each response; the joint mechanism producing an outcome; and the observations from which an investigator tries to identify that mechanism.

The five-state example separates distributed possession from individual or collective integration. The local-policy criterion then identifies the exact informational condition for a proposed response. Finite game theory adds preferences and unilateral incentives, while vector equilibrium makes the adopted improvement relation explicit. A stable profile has neither truth nor hard feasibility built into it: those require specified targets, joint-law constraints and an appropriate mechanism. The parity and Gaussian bounds quantify two different coordination tasks without collapsing either into a general physical law.

Temporal restoration introduces another obligation. An equilibrium of a stationary decision problem is not a convergence proof for repeated practice. Independent randomization can leave failures recurring forever. A valid progress argument supplies a target-preserving dynamic and a rank or potential suited to it. More general dependent deployment requires the actual conditional violation law and a filtration that observes the relevant events. Transferring a restorative policy requires complete probability marginals, implementable information and destination authority; approximation additionally needs control of bad occupancy or a genuine recovery and reentry mechanism. Conversely, an observed pattern of successful final answers may be insufficient to identify the evidence used to generate those answers. Identification requires a channel sensitive to the causal distinction, while a worthwhile inquiry further requires a declared decision problem and acceptable cost.

Finite memory adds a further distinction between repeatedly being accurate and eventually making no more mistakes. Fixed hidden standards can be learned almost surely by an unbounded tally even when every finite homogeneous controller falls short of that guarantee. Fresh, unobserved switching innovations instead impose an irreducible current risk. In both settings the acquisition law and permitted response remain separate from the statistical inference.

Several substantial questions remain open at the intended applied level. Which evidence coordinates and improvement relations are warranted for a particular scholarly task? Which cognitive or institutional operations can be defended as the strategic loci of a model? What actual records mediate coordination, and what dependencies bypass a proposed information cut? Which recording errors and intervention assumptions are empirically supported? These cannot be settled by declaring a tuple, invoking Nash's theorem, measuring an outcome curve or assigning a compression score.

A reproducible application must expose the conditions on which its result depends: coordinate orientation and units; source and extraction identity; inquiry and version; local views and permitted actions; payoffs or comparison cones; the strict-improvement convention; mixture and deployment semantics; and the kind of conclusion claimed. A certificate for one layer cannot certify another merely by changing its name. [5, §§8–9][r5]

The mathematical conclusions here are conditional statements with their proofs and counterexamples, not claims of general novelty, fitted psychological mechanisms or completed empirical validation. The epistemic-profile architecture remains a proposal with corrected mathematical consequences. The accepted Orthemology papers retain their own editions and authority. The unfinished objective of a general n-person noetic field, and any distinct constructive-correction companions, remain separate scientific work; this chapter neither substitutes for that objective nor imports private manuscript bodies.

The stochastic-transfer and recovery sections are ordinary mathematical consolidations of public research and its explicit correction for adversarial exposure of pre-sampled random memory. They preserve the supplied model and authority assumptions. Their finite implementations and historical probe results remain separate evidence; this exposition neither repeats those executions nor upgrades their formal or empirical status.

The learning sections likewise preserve the exact memory, observation, objective and permission hypotheses of their public sources. The common-objective specialization invokes the cited theorem within its stated model; it is not a newly implemented general synthesis procedure. The finite probes remain inspectable historical evidence, while the complete ordinary proofs above establish the stated mathematical conclusions.

## References and source editions

The numbered project sources below identify public research editions. They establish attribution and allow comparison of the inherited statements and corrections. The arguments required for this chapter are given above; ordinary reading does not require reconstructing those historical files. Source extraction is distinguished from the unretrieved original PDF, and a section citation does not claim incorporation of an entire larger work.

1. Orthemology project. *Multi-Actor / Zero-Sum Orthemic Note: stress test, corrections, and formal residue*. Public revised analytic note, 20 July 2026. [Exact public edition][r1].
2. Orthemology project. *Orthemic Core Formalization: Orthing, Episodes, Metaorthemes, Pathway Adequacy*, §§5.2–5.3. Public revised formal core, 20 July 2026. [Exact public edition][r2].
3. Orthemology project. *Five state evidence control*. Ordinary mathematical construction. [Exact public edition][r3].
4. *Epistemic Tuples and Intra-Agential Equilibrium: A formal thesis on evidentiary profiles, cognitive faculties, mixed epistemic policies, and equilibrium*. Public text extraction of the manuscript. The original PDF is a distinct edition and is not newly authenticated or reproduced here. [Exact public extraction][r4].
5. Orthemology public research. *Epistemic tuples and equilibrium as a typed restoration test domain*, especially the corrected scalarization, local-information, finite-game, vector-equilibrium, team-concavity and temporal arguments. [Exact public edition][r5].
6. Orthemology public research. *Relative normative-gap disclosure with an exact continuous-weight checker*, §§1–4. The later definability and checker sections remain outside this chapter's incorporation claim. [Exact public edition][r6].
7. Orthemology public research. *Graded Representations, Witnessed Revision, and Inquiry Landscapes: A conditional mathematical extension of Orthemology*, §8 and reference appendix. Research draft, 8 September 2026. [Exact public edition][r7].
8. Orthemology public research. *Continuation-Complete Orthings: Sharp information loss, minimal predictive memory, and safe strategic composition*, the pairwise-parity and strategic-composition sections. Research supplement, 8 September 2026. [Exact public edition][r8].
9. Orthemology public research. *A bounded information consequence for coordination explanations*. Ordinary-mathematics result, 4 October 2026. [Exact public edition][r9].
10. Orthemology public research. *A sharp error budget for finite coordination modes*. Ordinary-mathematics corollary. [Exact public edition][r10].
11. Orthemology public research. *What final answers can identify about collective evidence use*. Complete constituent of the public mathematical compendium, 5 October 2026, including its finite and sequential discrimination results. The other constituent works are separate. [Exact public edition][r11].
12. Orthemology public research. *Collective diagnosis and committed continuation*, §§1–3 on answer-only adaptation, linked information, inquiry value and recalibration, 11 October 2026. The independent computability branch is separate. [Exact public edition][r12].
13. John F. Nash, Jr. “Equilibrium Points in N-Person Games.” *Proceedings of the National Academy of Sciences* 36, no. 1 (1950): 48–49. [doi:10.1073/pnas.36.1.48][nash].
14. Shizuo Kakutani. “A Generalization of Brouwer's Fixed Point Theorem.” *Duke Mathematical Journal* 8, no. 3 (1941): 457–459. [doi:10.1215/S0012-7094-41-00838-4][kakutani].
15. Dov Monderer and Lloyd S. Shapley. “Potential Games.” *Games and Economic Behavior* 14 (1996): 124–143. The ordinal-potential definition and finite-improvement result used here are in §2, especially Lemma 2.3. [Primary paper][potential].
16. Shaojian Qu, Ying Ji and Mark Goh. “The Robust Weighted Multi-Objective Game.” *PLOS ONE* 10, no. 9 (2015): e0138970. [doi:10.1371/journal.pone.0138970][weighted].

17. Orthemology public research. *Correlated response policies and the exact limit of marginal restoration*. Ordinary proofs of the sharp coupling obstruction, adapted-event threshold and constrained-response qualifications. [Exact public edition][r13].
18. Orthemology public research. *Causal stochastic migration with an implementable information interface*. Corrected exact-coupling and controller-information treatment, including its finite-memory qualification. [Exact public edition][r14].
19. Orthemology public research. *Composing migration interfaces without turning private memory into public warrant*. Split public/private mode and exact same-middle-law composition. [Exact public edition][r15].
20. Orthemology public research. *Approximate migration: finite departures need an actual return mechanism*. Occupancy-defect and regenerative restoration results with their complete conditional reentry obligations. [Exact public edition][r16].
21. Orthemology public research. *Cross-lane adversarial synthesis review*, §F1 and §§C2–C4, 30 September 2026. The exposed-future-coin counterexample, relevant stochastic proof qualifications, hidden-standard learning boundaries and the two-state stationary-law correction are incorporated here; the review's other mathematical and philosophical assessments remain separate. [Exact public review][r17].
22. L. R. Ford, Jr., and D. R. Fulkerson. “Maximal Flow Through a Network.” *Canadian Journal of Mathematics* 8 (1956): 399–404. [doi:10.4153/CJM-1956-045-5][flow].
23. Robert J. Aumann. “Subjectivity and Correlation in Randomized Strategies.” *Journal of Mathematical Economics* 1, no. 1 (1974): 67–96. [doi:10.1016/0304-4068(74)90037-8][aumann]. [Author-hosted reprint][aumann-reprint].
24. Chandra Nair. *Probability Theory: Lecture Notes 6*. 18 December 2019. Theorem 11 states Lévy's extension of the Borel–Cantelli lemmas; its preceding martingale result and Lemma 5 support the convergence argument. [Author's notes][conditional-bc].
25. Sofie Haesaert, S. Esmaeil Zadeh Soudjani and Alessandro Abate. *Verification of General Markov Decision Processes by Approximate Similarity Relations and Policy Refinement*. Author preprint, arXiv:1605.09557v1, 2016. Definition 6 and §§3.3–4.2 distinguish exact law lifting, state-dependent interfaces and finite-horizon approximate refinement. [Primary preprint][refinement].

26. Orthemology public research. *Hidden target standards can require infinite memory under ongoing observations*. Complete fixed-standard learning, memory, authority, common-objective and whole-trace distinctions. [Exact public edition][r18].
27. Orthemology public research. *High long-run accuracy can coexist with zero restoration probability*. Exact stationary-error family and singular-limit counterexample; the two-state edge derivation is made explicit in §7.9. [Exact public edition][r19].
28. Orthemology public research. *Fresh hidden switching: an exact conditional-error threshold*. Conditional innovation and observation/permission boundaries. [Exact public edition][r20].
29. Martin E. Hellman and Thomas M. Cover. “Learning with Finite Memory.” *The Annals of Mathematical Statistics* 41, no. 3 (1970): 765–782. [doi:10.1214/aoms/1177696958][memory-origin].
30. Tomer Berg, Or Ordentlich and Ofer Shayevitz. *Binary Hypothesis Testing with Deterministic Finite-Memory Decision Rules*. arXiv:2005.07445v1, 2020. §I, especially equations (4) and (9), specifies the average-error criterion and the classical randomized-machine comparison. [Primary preprint][memory-learning].
31. Krishnendu Chatterjee, Laurent Doyen, Jean-François Raskin and Ocan Sankur. “The Value Problem for Multiple-Environment MDPs with Parity Objective.” *52nd International Colloquium on Automata, Languages, and Programming*, LIPIcs 334, article 150 (2025). The common observed-state objective and almost-sure finite-memory result used here are in §§2–3 and Theorem 4. [doi:10.4230/LIPIcs.ICALP.2025.150][memdp].

32. Orthemology public research. *Controlled information and eventual restoration*. Complete bounded public mathematical note. Exact Git object: `13cd55f631f3335b7c5c164947fb88ebe56e8f72`. The source's original finite enumeration remains separate execution evidence.
33. Orthemology public research. *One causal history-policy law: finite full-support restoration iff* and *Explicit common static licence*. Exact public review objects: `8cfcd82cce15b5df64f964f81b2424c97fc1bb7c` and `dd8f4908d7a733aa8f08481da568318d458fc584`. Exact formal endpoint objects: `5d0d5d9a1cb0d9f6d3fdf1a12c113c7e22bda696` and `08be7df023329ae8e83b269433c48e55548c6570`. The historical source closures and incremental verification receipts retain their distinct scope; no fresh kernel build is claimed here.
34. Eline M. Bovy, Caleb Probine, Marnix Suilen, Ufuk Topcu and Nils Jansen. *Multi-Environment POMDPs: Discrete Model Uncertainty Under Partial Observability*. arXiv:2510.23744v1, 2025, §§3–5, especially Theorem 5 and Appendix A.4. [Primary preprint](https://arxiv.org/html/2510.23744v1).
35. Emilie Kaufmann, Olivier Cappé and Aurélien Garivier. “On the Complexity of Best-Arm Identification in Multi-Armed Bandit Models.” *Journal of Machine Learning Research* 17(1) (2016): 1–42, Lemma 1. [Published primary article](https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf).

[r1]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/theory/orthemic-multi-actor-conflict-note.md
[r2]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/theory/orthemic-core-formalization.md
[r3]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/experiments/orthemology-v5-successors/source-store/a73f2cac6cb027d65c46ce6923e80bfed72a3591789779b57cc5578cdb359f84/FIVE_STATE_MODEL.md
[r4]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/a81201d5cb53b8c6d3d5eaf47abc704286f879cf78579421d6db6e0800fc5255/Epistemic_Tuples_and_Intra_Agential_Equilibrium.txt
[r5]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/c67c2fa0a538875a2bbbc0df51ad7877a6a701d11cb1567af4f250ff7c2724ad/research.md
[r6]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/f23c356f01dda091aa6195b15ff87b6c906dea579ec6a7283e4dd0dda1879147/research.md
[r7]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/theory/lineages/h-formalisation/orthing_formalisation_v1.md
[r8]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/theory/lineages/h-continuation/continuation_complete_orthing.md
[r9]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md
[r10]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/research-v6/type_collective/ROBUST_FINITE_MEDIATOR_BOUND.md
[r11]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/experiments/orthemology-v5-successors/source-store/34393b10d6a7447b0d802cb2aa65f6ec93d3f20446d0de97a9c4e292e59081f2/Orthemology_Fifteenth_Mathematical_Compendium_v1_20261005.md#what-final-answers-can-identify-about-collective-evidence-use
[r12]: https://github.com/theislampill/orthemology/blob/44734e836f9d74905cfdab745ef7d1d6abe30a38/research/t20-v6-20261012/sources/93ce02f68f9c20543e8790a4180bd6f5c72520b101456b5b8f50c69f24a92f16/RESULT.md
[nash]: https://www.pnas.org/doi/10.1073/pnas.36.1.48
[kakutani]: https://doi.org/10.1215/S0012-7094-41-00838-4
[potential]: https://people.csail.mit.edu/jrennie/trg/papers/monderer-potential-96.pdf
[weighted]: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0138970
[r13]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/7163cb536782ccb8a91a10be4b91cdcc1113bbab3c467d6ac66dee0d59cb0caf/correlated_restoration.md
[r14]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/e3a1087fae58f515c03ac1cb6f7420302abfde06e53d38f1a44ea2519bd3b157/stochastic_refinement.md
[r15]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/c363575fa62fd4ffead857b0ab9c8e1d7b0b81320721b8cf7389cea84417eea1/private_interface_composition.md
[r16]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/38fe5921cd3415625ad5e4de4084b6f81bc6658455aa51f1972fb2456ce69da7/regenerative_refinement.md
[r17]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/66a75aa4aff97954421c969818b167cb369344cc5bb4e2b63587c193f66d07ab/REPORT.md
[flow]: https://doi.org/10.4153/CJM-1956-045-5
[aumann]: https://doi.org/10.1016/0304-4068(74)90037-8
[aumann-reprint]: https://ma.huji.ac.il/raumann/pdf/Subjectivity%20and%20Correlation.pdf
[conditional-bc]: https://chandra.ie.cuhk.edu.hk/courses/Probability/ln6.pdf
[refinement]: https://arxiv.org/pdf/1605.09557v1

[r18]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/8ca78e5825fbe7233842871910254dba6fd12da0293c71a7a569060e010564c0/hidden_standard_learning.md
[r19]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/cb062c429d7d4cdd3a80d3250bceaa10dc47dc8743905ec15a1869f954809fd6/memory_accuracy_boundary.md
[r20]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/research/t20-v6-20261012/sources/7336cfa637b26bd82370c43e00601d3362291b6f4cb51b8563b49f66163799fb/switching_innovation_threshold.md
[memory-origin]: https://doi.org/10.1214/aoms/1177696958
[memory-learning]: https://arxiv.org/pdf/2005.07445v1
[memdp]: https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.150/LIPIcs.ICALP.2025.150.html
