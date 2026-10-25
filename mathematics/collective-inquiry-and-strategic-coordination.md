# Collective inquiry: information, strategy and coordinated judgment

## Abstract

A community can possess the premises of a conclusion without any member being able to integrate them. A game can have an equilibrium while its agents violate a hard joint constraint. Two groups can produce exactly the same answers while using different members' evidence. These are different failures, and each requires a different mathematical account. This chapter develops a common framework for them: shared occurrences with local observations; heterogeneous evidence with explicit comparison rules; locally implementable strategies; scalar and vector equilibria; complete coordination records; temporal deployment; and observations that identify actual contribution. It supplies finite counterexamples and proofs, including an exact positive-weight characterization of finite vector equilibria, coordination and information bounds, and a Gaussian nonidentification result with positive discrimination and inquiry-value counterparts. The results consolidate conditional public research. They do not establish a cognitive anatomy, a fitted social model, or the completion of an unfinished general noetic-field theory.

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
+c\mathbf1\{s_1=s_2\},\qquad 0<c<1.
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

## 7. Equilibrium and temporal learning

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

Temporal restoration introduces another obligation. An equilibrium of a stationary decision problem is not a convergence proof for repeated practice. Independent randomization can leave failures recurring forever. A valid progress argument supplies a target-preserving dynamic and a rank or potential suited to it. Conversely, an observed pattern of successful final answers may be insufficient to identify the evidence used to generate those answers. Identification requires a channel sensitive to the causal distinction, while a worthwhile inquiry further requires a declared decision problem and acceptable cost.

Several substantial questions remain open at the intended applied level. Which evidence coordinates and improvement relations are warranted for a particular scholarly task? Which cognitive or institutional operations can be defended as the strategic loci of a model? What actual records mediate coordination, and what dependencies bypass a proposed information cut? Which recording errors and intervention assumptions are empirically supported? These cannot be settled by declaring a tuple, invoking Nash's theorem, measuring an outcome curve or assigning a compression score.

A reproducible application must expose the conditions on which its result depends: coordinate orientation and units; source and extraction identity; inquiry and version; local views and permitted actions; payoffs or comparison cones; the strict-improvement convention; mixture and deployment semantics; and the kind of conclusion claimed. A certificate for one layer cannot certify another merely by changing its name. [5, §§8–9][r5]

The mathematical conclusions here are conditional statements with their proofs and counterexamples, not claims of general novelty, fitted psychological mechanisms or completed empirical validation. The epistemic-profile architecture remains a proposal with corrected mathematical consequences. The accepted Orthemology papers retain their own editions and authority. The unfinished objective of a general n-person noetic field, and any distinct constructive-correction companions, remain separate scientific work; this chapter neither substitutes for that objective nor imports private manuscript bodies.

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
