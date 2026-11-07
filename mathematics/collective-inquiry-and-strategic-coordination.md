# Collective inquiry: information, strategy and coordinated judgment

## Abstract

A community can possess the premises of a conclusion without any member being able to integrate them. A game can have an equilibrium while its agents violate a hard joint constraint. Two groups can produce exactly the same answers while using different members' evidence. These are different failures, and each requires a different mathematical account. This chapter develops a common framework for them: shared occurrences with local observations; heterogeneous evidence with explicit comparison rules; locally implementable strategies; scalar and vector equilibria; complete coordination records; temporal deployment; and observations that identify actual contribution. It supplies finite counterexamples and proofs, including an exact positive-weight characterization of finite vector equilibria, coordination and information bounds, and a Gaussian nonidentification result with positive discrimination and inquiry-value counterparts. Its temporal treatment also establishes sharp constrained-coupling bounds, a conditional restoration threshold, exact transfer through implementable information interfaces, and recovery conditions that distinguish finite departures from permanent failure. It also separates finite-memory accuracy from eventual correctness, distinguishes fixed hidden standards from a common observed objective, and gives the exact risk threshold for fresh switching innovations. For fixed finite models with positive controlled-observation laws, it gives an exact criterion for eventual correctness and a constructive history policy. Allowing zero observation probabilities, a recursive certificate yields a lawful physical-action policy with finite expected total target errors. The converse identifies the same recursive certificate from any successful common policy, preserving positive-branch continuations and the guard on every earlier action. Stateful revealing observations admit a safe region recursion, and hidden parity requires recurrent fairness and exact full-row matching. A posterior-deterministic joint kernel can be transformed into that visible-state model while preserving the acquired history, hidden objective and physical action clock. The results consolidate conditional public research. They do not establish a cognitive anatomy, a fitted social model, or the completion of an unfinished general noetic-field theory.

## 1. Shared inquiry and distributed access

### 1.1 One occurrence, several observations and objectives

Let *m* denote a concrete occurrence and $`\Omega_i(m)`$ the observation available to agent *i*. An occurrence includes the worldly facts needed for the inquiry: a game position can require the move history and the player to move, while a document assessment can require its actual edition. Different observations do not multiply the occurrence. In a card game, the actual deal is shared reality even though each player sees different cards. An information set describes what a player can distinguish; it is not an additional component of the world's identity. [1, §§1–3][r1]

An agent's analysis *A*<sub>*i*</sub> specifies a task, representation, boundary and assessment conditions. Its complete profile map $`O_i(m)`$ takes values in a profile space Π<sub>i</sub>. This actual profile is distinct from the agent's inferred judgment, which must be formed from its available observation $`\Omega_i(m)`$ under the declared analysis. A repeatable state type such as “White checkmates Black” is also distinct from the objective “maximize my utility”: the objective selects appropriate outcomes; it is not itself one of their state types. A task can select a target set $`G_i\subseteq\Pi_i`$. The target, the transition rules and the policy have separate roles: the target says what counts as an appropriate outcome; the rules determine lawful successors; the policy chooses among available actions. A procedure for validating evidence is another object. Competitors can share standards for whether a position is terminal, an assessment is stale or an analysis is sufficient while aiming at opposed outcomes. Those standards govern how judgments are made and validated, not whose target wins. A task indexed to a player supplies no psychological or ethical finding of selfishness. None of these categories becomes another merely because each governs some part of a game.

Targets in different profile spaces cannot be compared by an untyped intersection. Pull them back to the same reachable-occurrence domain:

```math
\widetilde G_i(m)
=\{m'\in\mathrm{Reach}(m):O_i(m')\in G_i\}.
```

Two targets are jointly realizable precisely when $`\widetilde G_i(m)\cap\widetilde G_j(m)\ne\varnothing`$. The schema “win for the player in this role” can be invariant under a role exchange while the two instantiated win-targets are disjoint. Schema isomorphism is not target identity. Cooperation may use a shared analysis and target, or an explicit alignment between different profile spaces; partial joint realizability alone does not identify the objectives. Moreover, zero-sum payoffs allow a draw with payoffs (0,0); opposed win-targets need not exhaust the terminal states. Actor-relative objectives also do not make every judgment actor-relative: whether an observed checksum matches a specified value can be the same question for every participant. [1, §§2–3][r1]

#### A byte-bound occurrence is not a certified sense

An exact textual pilot gives a concrete instance of the occurrence/observation distinction. The occurrence `quran:61:5:4` is bound to a specified Fusha revision and one projection represented at four appearances. Those appearances are not four independent observations of the underlying source. The pilot separately distinguishes occurrence assertions, an entry certificate, candidate segmentation/function assignments, a candidate-entry relation and a root-family relation. A certified entry does not settle which candidate sense governs this occurrence; an unresolved governor is deliberately omitted from the rendered answer. Its five certified facts comprise four occurrence facts and one rootless entry fact, not five independent sources or a completed linguistic interpretation. The legacy `review_required` records and their certified v2 successors must likewise be distinguished rather than merged into an undated status. [Q250A-012]

The corresponding verifier's evidence is narrower and reproducible in principle: it requires exactly 70 locked files, rejects duplicate or unsafe relative paths, checks byte length, SHA-256 and Git blob identity, and performs twelve occurrence checks on the same already checked in-memory bytes. Its historical total of 82 assertions is 70 byte bindings plus twelve occurrence assertions. The separate sense-source verifier checks nine additional files' identities but parses no linguistic content and contributes zero occurrence or sense tests. Neither program fetches absent inputs. The historical runs, selected source-lock files and external pinned bytes remain dependencies; static inspection of the programs establishes no new successful run, whole-application verification, live deployment or truth of a candidate sense. This is positive byte-and-occurrence evidence precisely because its claim is kept narrower than those conclusions. [Q250A-013] [Q250A-014]

### 1.2 When component work forms one inquiry

A distributed investigation can be described as a directed graph of episode tokens. A handoff passes a scoped result or evidence item to a later episode; a revision changes an earlier assessment; a retry is a new attempt. Orient these edges from earlier tokens to later tokens. Repeated policies can cycle, but their successive episode tokens do not need backward edges.

The graph and an assessment of the collective are different levels of description. To represent the graph as one accountable inquiry episode, the public formal core requires compatible occurrence lineage and analysis, an identified collective boundary with rule precedence, and an explicit rule for combining profiles, evidential statuses and remaining obligations. Sharing a task label does not ensure compatible tolerances or representations. A fusion analysis is needed where the component analyses differ. [2, §5.2][r2]

Collective correctness is consequently not the conjunction of component correctness. A validator can catch a mistaken intermediate result and yield a correct collective output. Conversely, individually sound assessments can yield an unsound composite if a handoff drops a qualification or uses a result at a different edition. The final speaker's output is not automatically a complete account of what the collective established. These conditions define a proposed assessment model; they are not an empirical claim that every actual institution has such a boundary or fusion rule.

### 1.3 A complete five-state evidence example

Distributed availability, individual knowledge and operative integration can be separated without uncertain measurements. Consider five states with the following probability law and truth values. State 0 is actual. [3][r3]

| State | Probability | *A* | *B* | *C* | *H* |
|---:|---:|:---:|:---:|:---:|:---:|
| 0 | 1/10 | true | true | true | true |
| 1 | 2/10 | true | true | false | false |
| 2 | 2/10 | true | false | true | false |
| 3 | 2/10 | false | true | true | false |
| 4 | 3/10 | false | false | false | true |

Member 1 observes the truth values of A,B; member 2 observes A,C; member 3 observes B,C. Their complete information partitions are respectively

```math
\{\{0,1\},\{2\},\{3\},\{4\}\},\qquad
\{\{0,2\},\{1\},\{3\},\{4\}\},\qquad
\{\{0,3\},\{1\},\{2\},\{4\}\}.
```

Use the idealized partition semantics: a member knows a proposition at a state when it holds throughout that member's information cell. At state 0, each of A,B,C is known by two members, but no member knows the missing indicator, their conjunction, or *H*. Nevertheless

```math
A\cap B\cap C=\{0\}\subsetneq H=\{0,4\},
\qquad \Pr(H\mid A\cap B\cap C)=1.
```

Thus a componentwise inventory accepting propositions known by a relevant majority can contain premises that jointly entail *H* while nobody has their joint information. The proper inclusion shows that *H* was not merely defined as the conjunction. Each actual private cell has probability 3/10 and contains *H*-mass 1/10, so every member's posterior is 1/3.

Even the description “the private evidence disconfirms *H*” depends on the baseline. Unconditionally $`\Pr(H)=2/5`$, so the posterior 1/3 is lower. If the common background first includes $`D=\{0,1,2,3\}`$, then $`\Pr(H\mid D)=1/7`$. The same private cells are contained in *D*, so their posterior remains 1/3 and now represents an increase. Joint entailment and private ignorance have not changed.

The model does not announce the actual inventory to its participants. Publicly announcing that all three indicators are true—or that each belongs to this factive majority-knowledge inventory—would change their information. The additional premise that no easy communication, memory or inferential route supplies the missing indicator is also substantive; ignorance alone does not establish it. Finally, posterior probability is not outright belief, and inventory membership is not group knowledge. Belief thresholds, integration processes and standards of access require their own interpretation. The example proves a separation among these relations rather than a finding about a real organization. [3][r3]

The model and probability law are shared background, not announcements of the actual state, private observations or actual inventory. The no-easy-route premise is assessed at state 0 on the relevant timescale, not asserted in every state; the displayed nonactual singleton cells remain. The partitions assume accurate observations, so noisy indicators require a different information and factivity model. Applying this control to an actual organisation requires evidence for its bearers, observations, access routes, probabilities and support standard. This is an ordinary written control, not a measured organisational model, an implementation or a Lean-certified theorem. [Q250A-005]

The source's prospective specialist questions preserve this model's relational distinctions: an available inventory, a warranted group judgment and an operative integration are different proposed review targets. The same review request asks for a positive bridge from target-directed cognition to the asserted same-bearer integrity, allowing a properly justified basic or abductive reason rather than requiring an endless certificate regress. These are specified questions for possible expert assessment, not an actual invitation, completed consultation or expert endorsement. The five-state calculation above is already the substantive retained counterexample. [Q250A-005] [Q250A-009]

### 1.4 Copying, synchronisation and the acquisition of evidence

Making evidence available to another participant can improve that participant's inquiry without creating another independent source. Synchronisation can also discard distinctions that the participants previously retained. Two complementary models make these effects exact: a lineage graph records which acquisitions an episode descends from, while a linear signature records which declared root directions remain visible. Neither model makes the authenticity, relevance or independence of its inputs true by definition. The following account incorporates the public lineage-root and synchronisation studies, including the latter's repair of a missing old-information term. [51–52]

#### Acquisitions and inherited roots

Let a finite directed acyclic graph represent episode tokens. Process its nodes in any order in which each predecessor occurs before its successor. Each node has a declared type and a set of authenticated root identifiers. An initial acquisition introduces a fresh root. More generally, if $`\mathrm{Pred}(v)`$ is the predecessor set, define

```math
H(v)=
\begin{cases}
\displaystyle\bigcup_{u\in\mathrm{Pred}(v)}H(u),
 &v\text{ is a copy, transformation or synchronisation};\\[4pt]
\displaystyle\left(\bigcup_{u\in\mathrm{Pred}(v)}H(u)\right)\cup\{r_v\},
 &v\text{ is an authenticated acquisition}.
\end{cases}
```

The identifier r<sub>v</sub> in the second line must be absent from the previously introduced root set. That is a condition of this model, to be justified when it is applied. A purported acquisition that merely supplies another name for an old source belongs to a different operation or needs alias resolution. A source-free transformation has an empty inherited set.

**Proposition (root accounting).** After any initial segment of the construction, the union of the root sets of all constructed nodes is exactly the set of authenticated roots introduced by acquisitions in that segment. Appending a copy, transformation or synchronisation leaves this global set unchanged. Appending an acquisition adds exactly its fresh root.

**Proof.** The empty construction has both sets empty. At a nonacquisition node, every inherited root already belongs to a predecessor and hence to the previous global set. Taking a union with the new node's set adds nothing. At an acquisition, the same reasoning applies to inherited roots and freshness adds exactly r<sub>v</sub>. Induction proves the claim. ∎

This global statement differs from availability at a particular recipient. If two predecessors have root sets $`\{a\}`$ and $`\{b\}`$, their synchronised successor has $`\{a,b\}`$, although neither predecessor had both. The global union remains $`\{a,b\}`$. If earlier nodes are subsequently discarded from the *accessible* collection, the accessible union can decrease; that pruning operation is not the append-only construction in the proposition. A transformation's inherited roots record its ancestry even when its output omits or cancels the information they once supplied.

One acquisition followed by one hundred copies gives 101 episode tokens and one root. Equal root sets do not make the tokens, carriers or paths identical: two copies can occupy distinct devices and follow different intermediate routes. Conversely, different authenticated acquisition events need not be probabilistically independent. Two measurements may both read the same hidden bit Z, so their outcomes agree surely even when the events and their lineages are distinct. A common upstream cause can remain absent from the declared root graph. Authentication of events and adequacy of the causal model are separate requirements. A transformation can also expose an already implied conclusion or make old evidence usable; that cognitive improvement need not introduce another acquisition root.

#### Linear signatures and information lost in synchronisation

Fix a field F and a finite-dimensional root space V. A warranted application must first say what its coordinates mean, how aliases have been identified, and which distinctions matter to the claim. One construction starts with the free vector space on authenticated root identifiers and takes a fixed quotient by declared alias and claim-irrelevance relations. The algebra below assumes that choice; it does not certify it.

Let the rows of a matrix A be the retained linear signatures in V. Write $`E=\mathrm{row}(A)`$. A linear synchronisation acts by left multiplication with a matrix B of compatible dimensions. Put

```math
S=\mathrm{row}(BA),\qquad
\rho_{\mathrm{before}}=\dim E,\qquad
\rho_{\mathrm{sync}}=\dim S,\qquad
\delta=\dim E-\dim S.
```

Every row of $`BA`$ is a linear combination of rows of A, so $`S\subseteq E`$. Consequently $`\delta\geq0`$, with equality exactly when $`S=E`$. Appending duplicate rows preserves the span. More generally, a copying matrix preserves the full span if its selected rows span E; copying only one selected row can discard the others. A nonempty collection of copies of a nonzero row has rank one, whereas any number of copies of the zero row has rank zero. The unqualified rank-one wording of the earlier examples requires this nonzero hypothesis. [51]

The lineage and linear models can coexist under an explicit compatibility condition. Suppose a node's raw signature is supported on the roots in $`H(v)`$, and the same fixed linear quotient sends every raw signature to V. For an accessible collection D of nodes,

```math
\dim\mathrm{span}\{a_v:v\in D\}
\leq
\dim q\!\left(\mathrm{span}\{e_r:r\in\bigcup_{v\in D}H(v)\}\right)
\leq\left|\bigcup_{v\in D}H(v)\right|.
```

Indeed, each a<sub>v</sub> belongs to the middle subspace, and a linear image cannot have larger dimension than its generating set. Equality is not required. Combining signatures e<sub>1</sub>,e<sub>2</sub> into the single row $`e_1+e_2`$ retains both lineage roots but only one visible direction. Cancellation can even produce a zero row while ancestry remains nonempty. The set-valued invariant therefore does not contradict a loss of linear rank.

#### Old recovery and fresh innovation

Let W be a separately authenticated finite-dimensional fresh-root space. Embed the synchronised span as $`S_0=S\oplus\{0\}\subseteq V\oplus W`$. Here an acquisition into the visible collection means a newly accessible signature; it need not be a root-introducing acquisition node in the lineage graph. Retrieving an earlier authenticated record can restore an old direction in V without introducing a new lineage root. Distinct authenticated events can also have signatures in the same old direction under the fixed alias or claim-relevance quotient. The application must declare that map: W records separately admitted fresh directions, not every newly available record or new event identifier. Later received signatures have row span

```math
Q=\mathrm{row}\,[C_{\mathrm{old}}\mid C_{\mathrm{fresh}}],
\qquad U=S_0+Q.
```

The block notation refers to fixed bases of V and W. Define

```math
\begin{aligned}
\rho_{\mathrm{after}}&=\dim U,\\
\gamma_{\mathrm{total}}&=\dim U-\dim S_0,\\
\gamma_{\mathrm{fresh}}&=\dim\pi_W(U)=\mathrm{rank}(C_{\mathrm{fresh}}),\\
\gamma_{\mathrm{old}}&=\dim\bigl(U\cap(V\oplus\{0\})\bigr)-\dim S_0.
\end{aligned}
```

Here π<sub>W</sub> is projection onto the fresh coordinates. The old term counts independently available *pure old-coordinate* directions beyond the synchronised span. It can include directions previously erased and old directions that were never present in E. A mixed acquisition need not reveal its old component separately.

**Proposition (exact synchronisation and acquisition balance).** There is a short exact sequence

```math
0\longrightarrow
\frac{U\cap(V\oplus\{0\})}{S_0}
\longrightarrow
\frac{U}{S_0}
\overset{\overline\pi_W}{\longrightarrow}
\pi_W(U)
\longrightarrow0.
```

Therefore

```math
\gamma_{\mathrm{total}}
=\gamma_{\mathrm{old}}+\gamma_{\mathrm{fresh}},
\qquad
\rho_{\mathrm{after}}
=\rho_{\mathrm{before}}-\delta
 +\gamma_{\mathrm{old}}+\gamma_{\mathrm{fresh}}.
```

**Proof.** Projection on U has kernel $`U\cap(V\oplus\{0\})`$ and image $`\pi_W(U)`$. Because S<sub>0</sub> lies in that kernel, $`\overline\pi_W(u+S_0)=\pi_W(u)`$ is well-defined. It is surjective, and its kernel is exactly the image of the first quotient under the inclusion map. That inclusion is injective. Rank-nullity on $`U/S_0`$ gives the first identity; substituting $`\dim S_0=\rho_{\mathrm{before}}-\delta`$ gives the second. ∎

These are finite-dimensional identities, not new general linear-algebra theorems. They show positively how a synchronisation deficit can be repaired. The final rank reaches or exceeds the original rank precisely when $`\gamma_{\mathrm{old}}+\gamma_{\mathrm{fresh}}\geq\delta`$. Fresh contribution alone is sufficient when it reaches δ, but it is not necessary: recovered old information can supply the difference.

There is a sharper distinction between restoring a dimension and restoring the old span. Let $`E_0=E\oplus\{0\}`$ and set

```math
\gamma_{\mathrm{recovered}}=\dim(U\cap E_0)-\dim S_0,
\qquad
\gamma_{\mathrm{previously\ absent}}
=\dim\bigl(U\cap(V\oplus\{0\})\bigr)-\dim(U\cap E_0).
```

Both are nonnegative, their sum is γ<sub>old</sub>, and $`0\leq\gamma_{\mathrm{recovered}}\leq\delta`$. Moreover,

```math
E_0\subseteq U
\quad\Longleftrightarrow\quad
\gamma_{\mathrm{recovered}}=\delta.
```

The proof is the chain $`S_0\subseteq U\cap E_0\subseteq E_0`$ and equality of finite-dimensional nested spaces at equal dimension. This is a composed consequence of the balance model, not an additional source of empirical warrant. If $`V=E`$, every pure old innovation is recovery and $`\gamma_{\mathrm{old}}\leq\delta`$. If E is a proper subspace of V, newly accessed old directions can increase γ<sub>old</sub> beyond the original deficit without recovering every lost direction.

#### Controls that distinguish the quantities

**Recovery with no fresh root.** Take A to have rows e<sub>1</sub>,e<sub>2</sub> and let synchronisation retain only e<sub>1</sub>. Retrieving the old e<sub>2</sub> record again gives $`\delta=1`$, $`\gamma_{\mathrm{old}}=1`$, $`\gamma_{\mathrm{fresh}}=0`$, and final rank two. A formula counting only fresh-root rank would wrongly predict one. This is the material repair of the predecessor's earlier formulation. [51]

**Mixed rows do not split automatically.** With the same old span and synchronised row, acquire only $`e_2+f_1`$, where $`f_1\in W`$ is nonzero. Then $`U=\mathrm{span}\{e_1,e_2+f_1\}`$, so the old innovation is zero and the fresh innovation is one. Adding the separate row f<sub>1</sub> permits subtraction and exposes e<sub>2</sub>: both innovations then equal one. In the first case, adding the separate ranks of the old and fresh blocks would count one mixed direction twice.

**Equal rank without restoration.** Instead acquire only f<sub>1</sub>. The final rank again equals two, but $`e_2\notin U`$ and $`\gamma_{\mathrm{recovered}}=0`$. A dimension certificate is weaker than preservation of the original subspace and, without a further model connecting signatures to a target, weaker still than restored diagnostic or corrective capacity.

**Aliases and relevance.** For a fixed linear root-identification map $`R:V\to V'`$, the transformed span is $`R(E)`$ and

```math
\mathrm{rank}(AR)=\dim R(E)\leq\dim E.
```

Two displayed basis rows can collapse to one when $`R(e_1)=R(e_2)`$. Conversely, a raw new coordinate can increase rank while being irrelevant to the claim and disappearing in its declared quotient. These examples explain why root authentication and relevance must precede the intended interpretation of rank. Changing the quotient during a comparison changes the question.

**Equal outputs from different roots.** The functional $`(x_1,x_2)\mapsto x_1+x_2`$ maps e<sub>1</sub> and e<sub>2</sub> to the same value although their root signatures span two dimensions. Equality of registered output is compatible with independent origins, just as many copies of one nonzero row are compatible with rank one. A synchronisation that makes every recipient retain only $`e_1+e_2`$ can increase widespread availability while lowering a previously visible rank-two collection to rank one.

These controls separate episode count, accessible ancestry, visible root span, output agreement and claim-relative support. They apply equally to replicated testimony, repeated artifacts and copied theorem expositions. A separately authenticated proof or acquisition may add a genuine direction; an additional presentation alone does not establish that it has done so. In probabilistic applications the actual conditional law decides how informative an acquisition is. The repeated-one-bit counterexample in §7.8 and the sample-count argument in [Information and Inquiry](information-and-inquiry.md) make this distinction at the level of learnability and statistical evidence. Neither device count nor linear rank can be substituted for their independence hypotheses.

The lineage predecessor reports a historical finite checker over 23,369 valid operation sequences of at most five nodes, 92,740 node checks, and seven rejected mutants. Its stated controls include invented roots under copying or synchronisation, root/carrier-count confusion, an inference from distinct roots to independence, an inference from equal root sets to numerical identity, and a collapse of capability, permission and warrant. Those are the source's execution declarations; no new run or independent receipt of its checker is asserted here. The induction and linear proofs above do not rely on the reported counts. They establish the stated accounting properties, while truth, competent testimony, warranted collective belief, common knowledge, personal identity and actual repair capacity require the appropriate additional premises. [51–52]


#### The rejected fresh-only balance and its finite evidence

The missing old-information term was a formal defect, not a change of terminology. The [primary record][receipt-au-06] reports 375 failures of the first version's fresh-only equation within 1,024 acquisition cases. A minimal mechanism has a zero visible old span and a later nonzero old-coordinate row, with no fresh coordinate at all: the visible rank increases while the proposed fresh term remains zero. The [cold audit][receipt-au-02] therefore required preserving the rejected formula and replacing it by the quotient/intersection decomposition. The [repair log][receipt-au-04] records that correction. Its other eight findings distinguish a linear root span from evidential independence, require an independently fixed relevance contract, restrict synchronization to a deterministic linear operation, separate algebraic loss from future repair capacity, require actual-root authentication before interpreting labels, type left aggregation and right root contraction separately, and retain the ancestry, novelty and identity limits.

The historical finite evidence has two different methods and domains. Over the declared binary field, the [primary record][receipt-au-06] reports 262,144 synchronization cases with 112,672 strict losses, 1,024 acquisition cases with no failure of the repaired decomposition or fresh-rank lower bound, 256 root-contraction cases and 1,536 duplicate-row cases. Its result is explicitly `PASS_WITH_V1_COUNTEREXAMPLE`; the 375 rejected-equation failures have not disappeared. The [distinct rereview][receipt-au-03] used direct span sets over the three-element field instead of binary Gaussian elimination. Its [result record][receipt-au-05] reports 20,000 sampled synchronization systems with 6,380 strict losses; 15,000 old-plus-fresh acquisition systems; 15,000 contractions; 5,000 duplicate-row cases; and 10,000 relevance projections. All six frozen files matched, and each corresponding failure count was zero. These are separate recorded populations, not newly executed checks or an exhaustive assertion about arbitrary fields and dimensions.

Both records preserve the diagnostic controls: many copies of one nonzero direction can have rank one; synchronization can reduce two directions to one; an old direction can be recovered without a fresh component; two displayed labels can contract to one actual root; and different root directions can produce the same observed output. The work's more explicit distinctions remain necessary. A zero row does not acquire rank one through copying. A mixed old/fresh row need not expose its old part separately. The old innovation term can include previously inaccessible directions as well as recovered ones; recovering the numerical rank does not by itself recover the original span. The historical counts establish none of these premises for an actual acquisition system merely by being attached to it.

The [scoped admission][receipt-au-01] records finite-dimensional linear balance and rank monotonicity, while leaving root authentication, claim relevance, testimonial and causal independence, truth, tawātur warrant, common knowledge and authorization to their own evidence. Rank does not decide numerical, carrier, episode or lineage identity, and it does not restore the earlier TAC/SAC terminology or establish operational future repair capacity. Nonlinear, stochastic and adaptive synchronization require a further model. The mathematical ancestry is standard linear algebra; the earlier synchronization, provenance and authenticated-access studies are related sources or interfaces, not recovered historical theorem identities. External review remains open and owner adoption pending. The algebraic component can inform those wider inquiries without completing them.


### 1.5 Finite mutual knowledge and common knowledge

The evidence-accounting results above leave a different question open: how many levels of mutual knowledge are needed for common knowledge in a declared finite model? Fix a nonempty finite set of worlds *W*, two agents *A* and *B*, equivalence accessibility relations $`R_A,R_B`$, and a fixed proposition valuation. Write $`K_i\psi(w)`$ when $`\psi`$ holds at every world accessible to agent *i* from *w*, and put $`E\psi=K_A\psi\land K_B\psi`$. Define $`E^0\varphi=\varphi`$ and $`E^{k+1}\varphi=E(E^k\varphi)`$. Common knowledge $`C\varphi`$ at *w* means that $`\varphi`$ holds throughout the reflexive-transitive closure of $`R_A\cup R_B`$ from *w*. These are model-relative information conditions, not conclusions about an actual communication channel. [Finite common-knowledge radius, frozen model][specialist-a-radius]

Let $`d(w)`$ be the greatest shortest-path distance from *w* to a world in its union-accessibility component. Then

```math
C\varphi(w)\quad\Longleftrightarrow\quad E^{d(w)}\varphi(w),
\qquad d(w)\leq |W|-1.
```

**Proof.** Induction on *k* identifies $`E^k\varphi(w)`$ with truth of $`\varphi`$ at every endpoint of a length-*k* path whose edges each belong to one of the two relations. Reflexivity lets a shorter path be padded by repeated visits to its last world. Thus the same condition says that $`\varphi`$ holds at every world at distance at most *k*. At $`k=d(w)`$ this set is the entire reachable component, which is exactly the definition of common knowledge. Each shortest path can be chosen without repeated vertices, giving the stated bound. For an isolated world, $`d(w)=0`$ and the convention $`E^0\varphi=\varphi`$ covers the same result. A particular valuation may settle earlier; the radius guarantees closure throughout the component. ∎ [Finite common-knowledge radius, result][specialist-a-radius]

The distinction from one round is already visible in three worlds. Let *A*'s information partition be $`\{0,1\}\mid\{2\}`$ and *B*'s be $`\{0\}\mid\{1,2\}`$. Let $`\varphi`$ be true at 0 and 1 and false at 2. At world 0, both agents individually know $`\varphi`$, so $`E\varphi(0)`$ holds. But the alternating path $`0\mathrel{R_A}1\mathrel{R_B}2`$ reaches a false world. In particular *A* cannot know that everybody knows: at its accessible world 1, *B* considers world 2 possible. Hence $`E^2\varphi(0)`$ and $`C\varphi(0)`$ both fail, and $`d(0)=2`$. [Finite common-knowledge radius, countermodel][specialist-a-radius]

The radius is a depth in this fixed accessibility structure, not a count of messages, acknowledgements or successful actions. The theorem does not establish that messages were delivered, that acknowledgements are reliable, that agents share clocks, that the stipulated valuation is actually true, or that a source is warranted or independent. A communication process that changes the model must justify its own update rules. Copying and synchronization can be assessed by §1.4's ancestry and rank results while these further epistemic conditions remain unestablished; the finite theorem identifies the additional condition rather than supplying it by analogy. [Finite common-knowledge radius, conclusion ceiling][specialist-a-radius]

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

Its extrema occur at the endpoints. Opposite strict rankings occur precisely when $`\min(f(\ell),f(u))<0<\max(f(\ell),f(u))`$. Variation in the truth of “*x* strictly outranks *y*” needs only $`\min\le0<\max`$: a tie and a strict preference already disagree about that target. For $`d=(1,-1)`$ and $`\alpha\in[3/4,7/8]`$, the ranking never reverses despite the crossing coordinates. These statements disclose dependence on an evaluation rule; they do not establish that every mathematically permitted weighting has normative authority. [5, §1][r5] [6, §§1–3][r6]

There are useful scalar positive cases. In a fixed binary-hypothesis model with positive likelihoods, a supplied prior π gives

```math
\Pr(H_1\mid x)=
\frac{\pi\Lambda(x)}{\pi\Lambda(x)+1-\pi},
\qquad
\Lambda(x)=\frac{\Pr(x\mid H_1)}{\Pr(x\mid H_0)}.
```

The likelihood ratio is sufficient for every decision determined by that posterior, supplied losses and a supplied tie rule. It need not embed the order of an evidence-quality tuple. Its sufficiency is conditional on the observation model: one independent report of reliability $`.9`$ for a hypothesis and one against it have likelihood ratio $`9(1/9)=1`$; copying the first does not create a third independent report. Treating the copy as independent would falsely change the ratio to 9. Known copying is a model error, not an alternative normative weighting. [6, §3][r6]

### 2.2 Common admission is not a common ranking or permission

A common inquiry can admit records only when schema, units, version and applicability match. Compatibility can preserve recorded source dependence without pretending that admitted records are independent. Two admitted profiles $`(1,0),(0,1)`$ can remain incomparable. They can also be available for analysis when the recipient has no permission to act, or support different repairs with no common safe action. Common admission therefore supplies neither a preferred ordering nor controllability. The bridges among those predicates need to be stated and justified. [5, §2][r5]

### 2.3 Local information determines implementability

Let *Z* be global configurations, $`o_i:Z\to O_i`$ a local observation, *S*<sub>*i*</sub> a nonempty response set, and $`\pi_i:Z\to S_i`$ a prescribed response.

**Proposition 3 — Local implementability.** There is a local response function $`a_i:O_i\to S_i`$ realizing $`\pi_i=a_i\circ o_i`$ on all global configurations exactly when π<sub>i</sub> is constant on every fibre of *o*<sub>*i*</sub>. The same statement holds for local histories and history-dependent responses. [5, §3][r5]

**Proof.** A function of a local view cannot distinguish two identical views. Conversely fibre constancy assigns a well-defined response to every attained view. Choose any fixed response for unattained views; nonemptiness of *S*<sub>*i*</sub> permits that extension. ∎

**One policy for an initial belief.** The same factorization becomes a joint control requirement in a finite deterministic system with common actions $`A=\{0,1\}`$, fixed observation $`o:S\to O`$, transition law and nonempty initial belief $`B\subseteq S`$. Restrict attention to stationary strategies and a co-Büchi condition: eventually the trajectory stays in a declared good set. In a finite deterministic system under a stationary policy, this is equivalent to requiring that the eventual cycle be entirely good.

An observation policy $`\tau:O\to A`$ wins from every state in $`B`$ exactly when there is **one** state policy $`\sigma:S\to A`$, constant on every observation fibre, that wins from every state in $`B`$. Forward, use $`\sigma=\tau\circ o`$. Backward, fibre constancy defines $`\tau`$ on attained observations; choose action zero on unattained observations. The two policies then induce the same trajectory from every initial state. The quantifier is one shared witness for all states, not a separate winning witness for each. [specialist-a-uniform]

The distinction has an explicit four-state counterexample. Let $`s_0,s_1`$ have the same observation, with a good absorbing sink $`g`$ and a bad absorbing sink $`b`$. At $`s_0`$, actions zero and one lead to $`g`$ and $`b`$ respectively; at $`s_1`$ reverse them. Each initial state is individually perfect-information winning, and a nonuniform state policy can win from both. No observation-based stationary policy wins from belief $`\{s_0,s_1\}`$: its common first action sends one possible initial state to the permanently bad sink.

This is a specialization of local implementability, not a new fixed-point method. The source separately reports **204,504** two/three-state enumeration cases, **8,234** statewise-false-sufficiency countermodels and six mutant rejections. The displayed four-state proof is not asserted to belong to that enumerated population. Those counts remain historical reports, and the reported source-only Lean factorization draft is not a verified project-level co-Büchi result. No randomized, adversarial-nondeterministic, history-dependent, infinite-state, asynchronous-protocol or metaphysical conclusion is imported. [specialist-a-uniform]

A source-monitoring component may know a bit *b* while an action component sees the same signal at $`b=0`$ and $`b=1`$. If the safe action must be $`\mathrm{repair}_b`$, no local action rule can always succeed. A licensed channel that communicates *b* makes it possible. A centralized description that simply lets the chooser inspect *b* has changed the information architecture.

This does not prove that distributed cognition is formally irreducible. A finite architecture can be represented by a product-state transition system retaining every local state, channel, shared cause and local-policy restriction. Such a flattening preserves its traces. The error is to discard those restrictions or add an oracle. Multiple copies of the same bit also do not become independent evidence merely because they occupy different components. [5, §3][r5]

### 2.4 Exact comparison across a continuum of evaluation weights

The endpoint test in §2.1 decides how one affine score comparison varies over an interval. A compound question can require more. One alternative may have to outrank a second while remaining below a third; a decision may depend on a tie or a disjunction of several comparisons. Such a Boolean target can be false at both endpoints and true between them. The following treatment gives the full finite procedure and its proof, then separates the resulting determination from the justification of the evaluation rule. [6, §§1–8][r6]

#### What a declared class determines

Let a base structure D interpret a language of alternatives, criteria, measurements, provenance and feasible consequences. An enriched structure N additionally interprets the evaluation and comparison symbols needed by a target sentence φ. A specified admissibility condition B determines the class

```math
\mathcal E_B(D)=\{N:\mathrm{red}(N)=D\text{ and }B(D,N)\}.
```

Here equality of reducts means the same carriers and interpretations of all base symbols. An alternative formulation using isomorphic bases must transport the relevant alternatives and target. D alone does not interpret a sentence containing the added symbols. The well-typed relative claim is

```math
D\models_B\varphi
\quad\Longleftrightarrow\quad
N\models\varphi\text{ for every }N\in\mathcal E_B(D).
```

If two admissible expansions give opposite truth values to φ, one refutes each of the two universal claims for φ and its negation. Conversely, in classical bivalent semantics, failure of both universal claims supplies those two witnesses. This converse concerns truth throughout the specified class. Failure to find a proof, or agreement in an incomplete sample, does not establish it. [6, §2][r6]

| Admissible expansions over the same base | What is determined |
|---|---|
| None | Both universal statements are vacuous; the substantive finding is that this regime admits no extension over D. It is not a verdict that both opposite judgments hold in the actual case. |
| Exactly one | Every closed target has a fixed truth value within that class. Stipulating one extension supplies no independent authority for it. |
| Several, agreeing on φ | The target is determined although the whole enrichment need not be unique. |
| Several, disagreeing on φ | Neither φ nor its negation follows throughout the class; the opposing expansions witness the dependence. |

A stronger independently warranted condition can restrict the class. If B′ implies B, its extensions form a subset of the old extensions. Every conclusion holding throughout the old class therefore holds throughout the new one. The new class must still be checked for nonemptiness, and previous disagreement can disappear. There is no inference that all restrictions are arbitrary or that a well-supported theory could never determine the evaluation. [6, §2][r6]

The interpretation of the base also matters. A citation count may be recorded descriptively, while interpreting it as provenance quality or justificatory strength requires calibration. Selecting criteria, choosing their orientation and classifying defeaters can already involve evaluation. Such disclosed mixed assumptions can legitimately support a relative comparison; they cannot simultaneously be treated as evidence that purely descriptive premises have failed to determine a normative conclusion. A declaration that a column is descriptive does not settle its meaning. [6, §1][r6]

#### A positive trade-off class and its strategic effect

Fix rational two-coordinate profiles e(a) for the alternatives used by a finite target formula, orientations o₁ and o₂ each equal to 1 or −1, and rational bounds with $`0\lt{}\ell\le u\lt{}1`$. For this comparison the admissible weights are **every real α in the entire closed interval** $`I=[\ell,u]`$, with no additional unexpressed restriction. Define

```math
s_\alpha(a)=\alpha o_1e_1(a)+(1-\alpha)o_2e_2(a).
```

Each score induces a complete weak order and its strict part. Because both weights are strictly positive, a weak improvement in both oriented coordinates with a strict improvement in at least one gives a strictly higher score: the score difference is a sum of two nonnegative weighted differences with at least one positive term. Thus the class imposes a substantive comparison restriction; it is not a collection of completely unconstrained truth assignments. Its linearity, orientation and particular priority bounds nevertheless require their own justification. Nonlinear evaluation, lexicographic priority or a more tightly justified bridge defines a different class. [6, §1][r6]

The effect can reach an equilibrium without any change of physical consequences. Take two players choosing 0 or 1. A player's own action 0 yields the profile (1,0), and action 1 yields (0,1), regardless of the opponent. Both maximize the same positively oriented α score. If α exceeds 1/2, action 0 is each player's unique best response against every opponent mixture, so (0,0) is the unique equilibrium. Below 1/2, (1,1) is uniquely selected. At 1/2 both actions have equal payoff against every opponent, so every mixed profile is Nash. The game skeleton is unchanged; the evaluation differs. This proves dependence in the specified example, not that evaluation is arbitrary, nonnatural or incapable of independent warrant. [6, §4][r6]

An exclusion from the feasible set is a different operation from a low payoff for a feasible move. Likewise, a transition's stability is different from its maximizing an independently supplied evaluation. Section 7.2 supplies the positive finite-ascent result, its entry bound and the separate closure and pointwise-fixation requirements; a fixed-point label alone supplies none of those premises.

#### The complete finite calculation

The target grammar consists of Boolean constants, negation, finite conjunction and finite disjunction, applied to strict or weak comparisons of the scores. After subtracting scores, each atomic occurrence has the form $`a_j\alpha+b_j>0`$ or $`a_j\alpha+b_j\ge0`$, with rational coefficients. For example, with the orientations absorbed into a profile difference d, its comparison function is $`d_2+\alpha(d_1-d_2)`$. Let k be the number of atomic occurrences; repeated atoms may be counted again. [6, §6][r6]

Collect the endpoints and all in-range roots of the nonconstant affine expressions:

```math
R=\{\ell,u\}\cup
\left\{-\frac{b_j}{a_j}:
a_j\ne0,\quad
\ell\le-\frac{b_j}{a_j}\le u\right\}.
```

Deduplicate and order these rational points as $`r_1\lt{}\cdots\lt{}r_m`$. Let S contain every point in R and the rational midpoint of every adjacent open interval $`(r_i,r_{i+1})`$. If the original interval is a singleton, R and S each consist of that one point.

**Theorem 3A — Exact sign-cell comparison.** For every target in the stated grammar, its truth values on S are exactly its truth values over the full real interval I. There are at most $`2k+3`$ representatives. Consequently the procedure decides whether the target is always true, always false, or takes both truth values in this declared class. In the last case it supplies rational witnesses for both values. [6, §6][r6]

**Proof.** Consider an open interval between adjacent points of R. Every nonconstant affine expression has no root in this interval. Its strict sign is constant there: a change between positive and negative, or between zero and nonzero, would require its unique root in the interval. A constant expression also has constant truth value; in particular, the identically zero expression makes a strict comparison false and a weak comparison true. Thus every atomic comparison is constant on the open interval.

Boolean constants are constant as well. Negation preserves constancy, and conjunction and disjunction of formulas constant on that same interval remain constant. Structural induction on the finite target formula therefore proves that its value throughout each open interval equals its value at the chosen midpoint. Evaluating every point of R separately retains the distinction between equality and strict preference, including roots at the original endpoints.

Every point of I lies either in R or in one of these open intervals. Hence every realized truth value is observed at a representative. Conversely every representative belongs to I, so the procedure introduces no unrealized value. All roots included in R and all chosen midpoints are rational. Each nonconstant atomic occurrence contributes at most one root, so $`m\le k+2`$. There are m point representatives and $`m-1`$ open-interval representatives, giving $`2m-1\le2k+3`$. For a singleton interval m is one and the same count gives one representative. ∎

This proof covers zero slopes, repeated roots, roots equal to either endpoint, strict and weak atoms, constant targets and degenerate intervals. It assumes exact rational input arithmetic and the specified grammar. It does not assume that a sufficiently dense grid eventually becomes a proof, and its representative bound is not a claim about optimal query complexity or unrestricted implementation running time. The nonempty interval is a theorem hypothesis; the empty-extension case above is a separate question about the regime being used.

#### Why endpoints and open intervals alone are insufficient

One realization of the source's narrow-interior control uses three actual profiles with both orientations positive:

```math
e(x)=(1,0),\qquad
e(a)=(49/100,49/100),\qquad
e(b)=(51/100,51/100).
```

On $`I=[1/4,3/4]`$, the target “x strictly outranks a and b strictly outranks x” holds exactly when $`49/100\lt{}\alpha\lt{}51/100`$. It is false at both original endpoints and true at α = 1/2. The two roots produce four distinct cut points and seven representatives, including the middle interval. Endpoint-only inspection would give the wrong invariance verdict. The three-profile realization makes explicit how this Boolean target belongs to the score-comparison grammar; it is an expository construction of the source's control, not a reported empirical example. [6, §6][r6]

Root points have an independent role. For profiles (1,0) and (0,1), the target that neither strictly outranks the other holds exactly at α = 1/2. In the same interval it is false on both open cells and true at the separating root. Checking only open-interval representatives would miss it. At a root, replacing a weak comparison with a strict one can therefore change the entire target. The proof's separate treatment of points is necessary for this grammar.

The procedure's positive conclusion is exact at its declared scope. If every representative makes the target true, the proof extends that value to every admitted real weight; it is not merely an estimate of frequent agreement. If two representatives disagree, their explicit parameter values exhibit the failure of determination. Neither outcome establishes that the chosen class exhausts every substantively admissible evaluation.

#### Canonical choice is a separate question

A unique expansion, a unique truth value for one target, a choice respecting the base's symmetries, and explicit definability in the base language are different requirements. Multiple weights can give the same dominance verdict without fixing the weights themselves. A singleton bridge can fix every target while leaving the bridge's substantive justification open. Parameter-free definability requires invariance under the base's automorphisms, but that necessary condition is not asserted to be sufficient in arbitrary structures. [6, §5][r6]

For a concrete symmetry control, take alternatives a and b and two otherwise indistinguishable criteria with profiles (1,0) and (0,1). In this example a, b, 1 and 2 are metalanguage labels, not distinguished constants that the base's automorphisms must fix. Simultaneously swapping the alternatives and criteria preserves the base, and the interval [1/4,3/4] is closed under the corresponding weight change $`\alpha\mapsto1-\alpha`$. A covariant rule choosing a single alternative at this base would have to choose a point fixed by that swap. Neither alternative is fixed. Such a single-winner rule is impossible under those premises.

The failure does not extend to every canonical output. Equal weights are fixed by the swap, produce a weak ordering with a tie, and permit the invariant chosen set {a,b}. Naming a preferred alternative or adding an independently warranted priority changes the relevant structure or admissibility condition. A target formula that explicitly asks about one named alternative is also a different object from an unnamed canonical selection rule. The general fixed-point account of natural selectors is given in [Objective Normativity, §8.10](../foundations/objective-normativity-and-corrective-cognition.md#810-structural-covariance-content-recoding-and-semantic-identification); the present example specifies its distinct selection target.

There is also a positive uniqueness result. For a positive integer q, a normalized weight vector fixed by every permutation of q indistinguishable criteria must give all coordinates the same weight: the transposition of any two coordinates forces their equality. Since the weights sum to one, each equals $`1/q`$. This proves uniqueness under the symmetry condition. It does not establish that the criteria are actually exchangeable or that equal importance is substantively correct. [6, §5][r6]

The source's comparison with Beth definability concerns a first-order theory across its models, where the relevant implicit determination supports explicit definability. A unique enrichment over one selected D, or a unique target in this finite application, does not by itself satisfy that global hypothesis. The cited Buss discussion's standard-versus-nonstandard-model warning belongs to that inherited comparison. Neither an arbitrary-structure converse from automorphism invariance nor a new proof of a definability theorem is claimed here. [6, §5][r6]

#### What the result establishes about an application

The target-factorization criterion in Proposition 1 has a positive general use: equal recorded profiles need agree only on the target to be recovered, not on every omitted feature. A readout is defined first on attained profiles; extending it to an unattained input requires a permissible default target value. The present theorem supplies an effective decision for a restricted family because its syntax and arithmetic allow the complete finite partition. Set-theoretic determination in an arbitrary family does not by itself supply such a procedure. [6, §7][r6]

The relevant family must be specified separately for each application. The interval ranking problem and the constructed game above give exact instances of dependence on evaluation. Prediction under a model family or threshold is a conditional instance whose admissible models need their own rationale; its uncertainty need not be moral uncertainty. Hidden-provenance inference likewise needs a fixed observation map and genuinely admissible acquisition histories. Once copying is known, the false independent-source model is excluded rather than retained as a rival normative judgment. The likelihood-ratio positive case in §2.1 instead supplies a sufficient statistic for a fixed model, prior, loss and tie rule. None of these cases gives a complete class of morally possible worlds or a theory of original intentional sourcehood. [6, §7][r6]

Syntactically permitted expansions, epistemically live models and metaphysically possible structures are not interchangeable. A pair of formally different predicate assignments is a counterexample within a class that admits them. It is not thereby a metaphysically adequate impersonal rival to a richer source argument. Conversely, an independently justified naturalist account may constrain evaluative interpretation more strongly than this interval class does. Showing disagreement in the weaker class does not refute that stronger account; its additional premises must be assessed at their own scope.

The source's philosophical comparisons retain those distinctions. Its Hume discussion concerns making a transition to an ought-relation explicit, not deriving an unrestricted new-word prohibition. In classical logic p entails $`p\lor O`$, whatever ethical vocabulary occurs in O, and $`O\lor\neg O`$ is true in every bivalent interpretation. These simple controls defeat a purely syntactic test while leaving substantive questions about justified moral inference open. Moore's question about the analysis of goodness is different from variation of α in this model; the latter proves no indefinability of good. Jackson and Pettit's moral functionalism is a positive example of a proposal for stronger determining constraints, cited in the source through a publication record and authored abstract rather than a complete adjudication. No global anti-naturalist or non-supervenience conclusion follows. These are attributed comparisons from the public study, not fresh full readings of the primary works. [6, §8][r6]

Finally, a reported research implementation is evidence at its own scope. The public source describes exact-fraction evaluation, a restricted syntax, recomputation and a sequence of finite checks, including a later repair of Boolean/integer certificate equality. Those historical observations are not rerun here and are not kernel or empirical validation of the philosophical application. Binding input content by a digest does not authenticate its author or justify its normative interpretation. The ordinary sign-cell proof establishes the continuous-domain claim under its hypotheses. A higher-dimensional polytope procedure, an unrestricted input parser, global metaphysical supervenience and machine-certified normative authority remain outside it. [6, §§6–9][r6]


<a id="receipt68-correct-view-agreement"></a>

### 2.5 One-step agreement when correct membership can vary

The fibre criterion in §2.3 asks whether a prescribed response can be implemented from a local view. A related synthesis problem permits several valid outputs and allows the set of correct participants to differ between scenarios. The output must be chosen by the actual local rules, rather than by a central chooser who knows which scenario occurred. The finite equality-constraint form of this problem has an exact component criterion. [R68-S020]

Let $`\Sigma`$ be a finite scenario family, $`K`$ a finite nonempty set of complete output objects, and $`A_s\subseteq K`$ the objects admitted in scenario $`s`$. Each scenario has a nonempty correct-participant set $`C_s`$ and supplies a complete local view $`v_i(s)`$ to each $`i\in C_s`$. A deterministic one-step protocol chooses an output through a function $`a_i`$ of participant $`i`$'s view. Success requires the correct participants in $`s`$ to agree on an element of $`A_s`$. Faulty participants' outputs are not required to agree; any fault-generated observations relevant to correct behavior must already be represented in the correct participants' views.

Construct a graph whose vertices are the appearing **participant-view tokens** $`(i,v_i(s))`$ with $`i\in C_s`$. For every scenario, join all its correct tokens into a clique. A single-token scenario contributes an isolated vertex unless that token occurs elsewhere. Token identity includes participant identity: two different participants seeing the same symbol do not thereby share one local response function. Since $`C_s`$ is nonempty, all the tokens of $`s`$ belong to one well-defined component, denoted $`\gamma(s)`$.

**Component criterion.** A successful deterministic protocol exists exactly when

```math
\bigcap_{s:\,\gamma(s)=D} A_s\ne\varnothing
\qquad\text{for every graph component }D.
```

**Proof.** Agreement in one scenario makes the protocol output equal along every edge of its clique. Repeated occurrence of the same participant-view token reuses the same function value. Equality therefore propagates along paths, making the output constant on each connected component. That constant must be admitted by every scenario assigned to the component, proving necessity. Conversely, choose one object $`k_D`$ from each displayed intersection and assign it to every token in $`D`$. The assignment defines consistent local functions on all appearing correct views. Extend those functions to unused views using any fixed object of the nonempty set $`K`$. Each scenario's correct tokens then return $`k_{\gamma(s)}\in A_s`$, proving sufficiency. The empty scenario family imposes no conditions. [R68-S020] [R68-S021]

This is stronger than checking whether each scenario separately admits a common choice. Consider two scenarios with correct sets $`\{1,2\}`$ and $`\{2,3\}`$. Let participant two have the same view in both, while the required outputs are respectively the distinct singletons $`\{a\}`$ and $`\{b\}`$. Each scenario alone is solvable. Together, the repeated token of participant two joins their cliques, and the component's required intersection is empty. A central observer could select the scenario's output; the local protocol cannot give two values to that unchanged token. This is an information obstruction, not a shortage of candidate actions.

A truthful public bit distinguishing the two scenarios can repair the example if it is incorporated into every correct participant's protocol view, is commonly available at the relevant step, and has the required source, version and admissibility conditions. It splits the formerly repeated token. A private bit available only elsewhere, an untrusted message, or a bit omitted from the actual decision state does not supply the same repair. Refining views changes the information contract. By contrast, adding more scenarios while keeping the old views and requirements fixed cannot make an infeasible family feasible: any protocol for the larger family would restrict to one for the original family. [R68-S020]

The output type matters equally. Suppose two incompatible action-certificate objects project to the same visible action. Agreement after that projection does not make their full admissible-object intersection nonempty. The certificates may differ in reason, root, source version, authority or applicability even though the actuator receives the same instruction. The component theorem is applied to the complete declared objects; it does not infer that their supplied admissibility sets are truthful or independently warranted. This is the relation-selection distinction developed in Information Retained by Inquiry §9.4, now with equality obligations generated by changing correct membership. [R68-S021] [R68-S022]

The historical primary check reports **3,155** one-, two- and sampled three-scenario families and **4,632** supersets of infeasible pairs. The distinct review replaced the sampled three-scenario part with all **76,076** families in its stated small class: three participants, two views per participant, nonempty correct sets and nonempty subsets of two typed outputs. Its result file records no criterion mismatch and explicitly retains the action-only projection control. These are different historical finite populations, not new executions or a pooled experiment. [R68-S020] [R68-S021] [R68-S022]

The mathematics is an equality-constraint specialization of local factorization. It is not a general Byzantine-agreement or asynchronous-liveness theorem. Repeated interaction, randomized protocols, changing information states, causal restoration and stable reach-and-stay need additional arguments. The scenario family must contain every fault, message, membership, source and snapshot pattern claimed by the application. Nor does operational agreement on a root or source label establish one metaphysical bearer, source truth or recipient authority. The criterion identifies exactly which one-step common choices the stipulated local information permits.

## 3. The finite strategic model and its limits

### 3.1 A game is additional structure

A strategic model specifies a nonempty finite set of players, nonempty finite strategy sets *S*<sub>*i*</sub>, a full product $`S=\prod_iS_i`$ of jointly admissible profiles, and real payoffs $`u_i:S\to\mathbb R`$. The players can represent persons or functionally differentiated loci, but the assignment of strategies and preferences must be defensible. An evidence item or obligation is not a player merely because it appears in a representation. [4, §§4–8][r4] [7, §8][r7]

In a finite extensive-form situation, strategies can be complete contingent plans compatible with each player's information. That compilation must preserve the information structure; replacing contingent plans by bare action labels can give an agent information it does not have. Finite primitive action alphabets also do not make an unlimited temporal policy space finite. Coupled action constraints require separate treatment.

A mixed strategy $`p_i\in\Delta(S_i)`$ is a probability distribution on *S*<sub>*i*</sub>. Under independent mixing,

```math
U_i(p)=\sum_{s\in S}u_i(s)\prod_jp_j(s_j).
```

Pure profiles form a Cartesian product. Once strategy bases are chosen, their embedding $`s\mapsto[s_1]\otimes\cdots\otimes[s_n]`$ and the probability tensor $`p_1\otimes\cdots\otimes p_n`$ express the multilinearity of expectation. A general joint law need not factor this way. Tensor notation does not itself supply a game, independence or a theory of cognition.

The interpretation of a probability vector must also be explicit. Repeated random choice, graded endorsement, unresolved competition and frequencies across episodes are different interpretations. The expectation formula and the sampling theorems below concern the declared probabilistic interpretation, not every use of a convex combination. [4, §5][r4]

### 3.2 Existence is conditional stability

**Theorem 4 — Finite mixed equilibrium.** Every game just specified has a nonempty compact set of mixed Nash equilibria. [5, §4][r5] [7, Theorem 8.3][r7] [13][nash] [14][kakutani]

**Proof.** The product $`P=\prod_i\Delta(S_i)`$ is nonempty, compact and convex. For fixed opponents, *U*<sub>*i*</sub> is affine in the player's mixture, so its maximizers form a nonempty compact convex set. Define the product best-response correspondence $`BR:P\rightrightarrows P`$. Its graph is closed: if opponent profiles and maximizing responses converge, continuity passes every maximizing inequality to the limit. Compactness of the codomain supplies upper hemicontinuity. Kakutani's fixed-point theorem gives $`p\in BR(p)`$, precisely the Nash inequalities. The fixed-point set is closed in compact *P*, hence compact. ∎

This is the classical Nash–Kakutani argument, not a new existence theorem. Empty values, nonconvex domains, lack of compactness or a discontinuous best-response graph can invalidate its premises. For example, $`F(x)=x/2`$ has no fixed point on (0,1); the flip has none on $`\{0,1\}`$; and $`F(0)=1,F(x)=0`$ for $`x>0`$ has none on $`[0,1]`$. A correspondence equal to $`\{1\}`$ below 1/2, $`\{0\}`$ above it and $`\{0,1\}`$ at it has closed graph and nonempty compact values but no fixed point: its value at the midpoint is not convex. [5, §4][r5]

Existence does not give a selection rule, uniqueness, an effective solver or convergence of play. The map $`F(x)=1-x`$ has a fixed point but its iterates from 0 alternate forever. A one-player payoff can even reward a false answer more highly than a true one. The unique equilibrium would then be false under the independently supplied truth predicate.

### 3.3 Changing inquiry can change incentives

Inquiry affects strategic possibilities as well as conclusions. Suppose a fixed analysis offers researchers two actions: independent pre-disclosure discovery *D* and stopping *S*. Before public disclosure, both are available and *D* pays 1 while *S* pays 0. The unique equilibrium is (D,D). Correct publication changes the public state and makes *D* unavailable by its declared meaning; (S,S) becomes the unique equilibrium. The analysis and feasibility rule remain fixed; the state to which they apply changed. If strategy or player sets change, compare equilibria through explicit transport maps or a common tagged space rather than subtracting differently typed sets. [7, Proposition 8.6][r7]

A different example separates correctness from inquiry value. Two researchers choose rapid disclosure *F* or mechanism-rich exposition *E*:

| Player 1 / Player 2 | *F* | *E* |
|---|---|---|
| *F* | (2,2) | (5,0) |
| *E* | (0,5) | (4,4) |

The action *F* strictly dominates *E*, so (F,F) is the unique equilibrium, although (E,E) benefits both more. Every outcome may disclose the same correct theorem while the fuller exposition supports more future inquiry. These are constructed payoffs, not measurements of researchers' motives. Truth, private incentives and prospective scientific value are different evaluations. [7, §8][r7]

## 4. Vector judgments, teams and representation changes

### 4.1 Two distinct improvement relations

Suppose player *i* has a vector payoff $`V_i(s)\in\mathbb R^{k_i}`$, extended by coordinatewise expectation. Define two sets of equilibrium profiles:

```math
\begin{aligned}
E_{\mathrm{nd}}&=\{p:\text{no unilateral gain lies in }
\mathbb R_{\ge0}^{k_i}\setminus\{0\}\text{ for any }i\},\\
E_{\mathrm{all}}&=\{p:\text{no unilateral gain lies in }
\mathbb R_{>0}^{k_i}\text{ for any }i\}.
\end{aligned}
```

The first excludes improvement in some coordinate without deterioration in any; the second excludes improvement strictly in every coordinate. Thus $`E_{\mathrm{nd}}\subseteq E_{\mathrm{all}}`$. With one player choosing (0,0) or (1,0), every mixture belongs to the second set, while only the second pure outcome belongs to the first. The original manuscript used a nonzero nonnegative cone in one statement and every-coordinate-strict prose in another. The later analysis correctly separates them; neither interpretation should silently replace the other. [4, §7][r4] [5, §5][r5]

### 4.2 Exact positive-weight characterization

**Theorem 5 — Finite vector equilibria.** For a finite vector-payoff game with independently mixed strategies,

```math
E_{\mathrm{nd}}
=\bigcup_{w_i\in\mathbb R_{>0}^{k_i}}
\mathrm{NE}(w_1\cdot V_1,\ldots,w_n\cdot V_n).
```

In particular E<sub>nd</sub> is nonempty. A scalar equilibrium with nonnegative nonzero weights guarantees membership in E<sub>all</sub>, but not generally in E<sub>nd</sub>. [5, Propositions on positive scalarization][r5]

**Proof.** A nonzero nonnegative vector has positive dot product with every strictly positive weight vector. Such a profitable vector deviation would contradict scalar equilibrium. Likewise every strictly positive gain has positive dot product with a nonnegative nonzero vector. Choosing strictly positive weights and applying Theorem 4 proves nonemptiness.

For the converse, fix $`p\in E_{\mathrm{nd}}`$ and one player. Against the fixed opponents, let *d*<sub>*j*</sub> be the expected vector gain of pure response *j* relative to the current mixture. Let *D* be the cone generated by these finitely many gains. If $`z=\sum_j a_jd_j`$ were nonzero and nonnegative with $`a_j\ge0`$, then $`A=\sum_j a_j>0`$ and the mixture with weights $`a_j/A`$ would realize gain $`z/A`$, contradicting efficiency. Hence *D* is disjoint from the nonnegative simplex $`K=\{z\ge0:\sum z_j=1\}`$.

The finitely generated cone *D* is closed and convex; *K* is compact and convex. Strict separation provides *w* with $`w\cdot d\le0`$ for all $`d\in D`$ and $`w\cdot z>0`$ on *K*. The first bound follows from conicity and $`0\in D`$; evaluating the second on the coordinate vectors shows every coordinate of *w* is positive. Thus every pure deviation, and therefore every mixed deviation, has nonpositive scalar gain. Choose such weights separately for each player. The selected profile is scalar Nash. ∎

The weights can depend on both player and equilibrium. They are existence witnesses, not canonical epistemic trade-offs. The distinction between Pareto and weak Pareto criteria also appears in the weighted-game literature. Robust models that supply a set of possible weights solve a different optimization problem; their broader hypotheses do not replace this finite-polyhedral converse. [16][weighted] The zero-weight distinction is sharp: weights (0,1) make both outcomes $`(0,0),(1,0)`$ optimal while the first is dominated.

Finite convexification matters. Among just the three pure outcomes $`(3,0),(1,1),(0,3)`$, the middle is Pareto efficient but maximizes no positive weighted sum. Once mixtures are allowed, the half-mixture of the extremes gives (1.5,1.5) and dominates it. Even compact convex infinite payoff sets need not have the strictly positive support property. In

```math
C=\{(x,y):0\le y\le1,\ -1\le x\le-y^2\},
```

(0,0) is efficient, but for any $`w_1,w_2>0`$, a sufficiently small $`t>0`$ gives $`w\cdot(-t^2,t)>0`$. Only a boundary weight such as (1,0) supports the origin. The finite-polyhedral hypothesis cannot be replaced by compactness and convexity alone. [5, §5][r5]

### 4.3 Team optimality and a restrictive concavity condition

When all players share a scalar payoff *W*, every global maximizer is Nash. The converse fails: if $`W(0,0)=2`$, $`W(1,1)=1`$ and the off-diagonal values are zero, both diagonal profiles are Nash. If a coupled constraint permits only these two profiles, each can also be stable because no unilateral feasible move exists. A constrained game is not the ordinary product-simplex problem.

**Theorem 6 — Joint concavity eliminates finite payoff interaction.** For the independent mixed extension of a finite common-payoff table on the full product of simplices, joint concavity, joint convexity, joint affinity and additive separability of the pure payoff table are equivalent. [5, team-concavity proposition][r5]

**Proof.** Fix two players, two responses each, and pure responses of all others. Write the four payoffs as a,b,c,d in rectangular order. The midpoint obtained by mixing each player equally has value $`(a+b+c+d)/4`$. Concavity along each of the two diagonals implies both $`b+c\ge a+d`$ and $`a+d\ge b+c`$. Hence every conditional two-player mixed difference is zero. Relative to a fixed baseline *r*, the increment from changing one player's response is independent of the others' responses. Telescoping therefore gives

```math
w(s)=w(r)+\sum_i\bigl[w(r_{-i},s_i)-w(r)\bigr].
```

Its mixed extension is jointly affine, hence convex and concave. Convexity gives the same diagonal equality with the inequalities reversed, proving all implications. ∎

Affineness in a player's own mixture is automatic in finite games and is much weaker. Joint concavity is not a harmless way to preserve genuine team-payoff interaction while obtaining global optimality. The full-product hypothesis is essential: $`W(p,q)=1-p-q+3pq`$ restricted to $`p+q=1`$ becomes the concave function $`3p(1-p)`$. A joint-law simplex is another geometry, on which expected payoff is linear in the joint law. Without marginal or other restrictions, that change cannot improve the maximum common payoff: a maximizing pure joint profile was already available. Correlation becomes valuable when implementation constraints exclude that simple solution. [5, §5][r5]

A sequential pipeline can instead consist of transformations and a terminal criterion without any preferences or profitable deviations. Giving its components game-theoretic names adds no result unless the strategic interpretation is warranted.

### 4.4 Which re-encodings preserve which conclusions?

Coordinate permutations and coordinatewise strictly increasing bijections preserve deterministic coordinatewise order. Transporting schemas, units, admission rules and target readouts preserves their corresponding judgments. But applying a nonlinear transformation to pure payoffs before averaging need not preserve mixed equilibria. [5, §6][r5]

For example, give player 1 payoff matrix $`\left(\begin{smallmatrix}0&2\\1&0\end{smallmatrix}\right)`$ and player 2 payoff matrix $`\left(\begin{smallmatrix}1&0\\0&1\end{smallmatrix}\right)`$. At the unique fully mixed equilibrium, row-0 probability is 1/2 and column-0 probability is 2/3: player 2 is indifferent at equal row probabilities, and player 1 satisfies $`2(1-q)=q`$. Squaring player 1's nonnegative pure payoffs preserves their order but changes its equation to $`4(1-q)=q`$, hence $`q=4/5`$.

By contrast, strategy relabellings and positive affine scalar payoff changes preserve Nash equilibria: they biject unilateral deviations and multiply each gain by a positive constant. For vector games, an invertible affine change $`V_i'=A_iV_i+b_i`$ preserves either specified improvement relation when the cone is transported to $`A_iC_i`$. A change of units $`e'=De`$ preserves a scalar score only if its weights change to $`w'=D^{-T}w`$. Retaining old weights after changing units changes the comparison rule. [5, §6][r5] [7, Proposition 8.4][r7]

## 5. Strategically sufficient information and hard coordination

### 5.1 Retaining incentives rather than every payoff level

Suppose payoffs depend on a reference state *x*. For a pure profile *s* and unilateral response *b*<sub>*i*</sub>, define the gain observable

```math
g_{i,b_i,s}(x)=u_i(x,b_i,s_{-i})-u_i(x,s).
```

These differences, together with the relevant information branches and feasible strategies, determine the incentive comparisons. An offset depending only on the opponents' actions changes payoff levels without changing player *i*'s unilateral gains. A representation intended only to preserve Nash incentives can therefore need less information than one recovering every payoff. [8, Proposition 7][r8]

Define regret by

```math
\mathrm{Reg}_i^U(p)
=\max_{b_i\in S_i}U_i(b_i,p_{-i})-U_i(p).
```

It is nonnegative, and all regrets vanish exactly at Nash equilibria. Mixed deviations cannot exceed the best pure deviation because their payoffs are convex combinations.

**Proposition 7 — Incentive-error transport.** If a genuinely specified approximate game estimates every pure unilateral expected gain within η<sub>i</sub>, then

```math
\mathrm{Reg}_i^{\mathrm{reference}}(p)
\le\mathrm{Reg}_i^{\mathrm{approximate}}(p)+\eta_i.
```

**Proof.** The mixed gain for each pure deviation is a probability-weighted average of its pure-profile gains. Its error is therefore at most η<sub>i</sub>. Taking the maximum preserves that bound. ∎

If instead each payoff entry is known within ε<sub>i</sub>, subtracting two entries gives $`\eta_i=2\varepsilon_i`$ and the familiar bound $`\delta_i+2\varepsilon_i`$ for a δ<sub>i</sub>-equilibrium of the approximation. Direct gain estimation can be more focused, but independently fitted gains need not come from a consistent payoff table. The existence theorem still needs an actual game. Likewise $`\lambda(x)\prod_i p_i(s_i)`$ requires independence between reference uncertainty and strategic randomization; state-dependent action belongs in contingent strategies or an explicit observation model. [7, Proposition 8.5][r7] [8, §6][r8]

### 5.2 A hidden interaction changes the equilibrium

Let $`x\in\{-1,1\}^n`$, $`n\ge2`$, and let λ<sub>+</sub>,λ<sub>−</sub> be uniform on the two opposite parity classes. Every proper-subset marginal is the same: fixing fewer than all coordinates leaves an unobserved coordinate whose sign flip bijects the two parity classes. Permit the pairwise updates $`x_1\leftarrow x_1x_j`$ for $`j=2,\ldots,n`$. After these $`n-1`$ updates, *x*<sub>1</sub> equals the original full parity. Thus the binary target

```math
B=\frac{1-x_1^{\mathrm{final}}}{2}
```

is certainly 0 under λ<sub>+</sub> and certainly 1 under λ<sub>−</sub>. Pairwise operations have made a previously hidden higher-order relation decisive for a unary question. [8, §4][r8]

Give two players actions 0 and 1 and payoffs

```math
u_i(x,s)=\mathbf1\{s_i=B(x)\}
+c\mathbf1\{s_1=s_2\},\qquad 0\lt{}c<1.
```

**Proposition 8 — Hidden reference games.** The reference games have unique equilibria (0,0) and (1,1). For any fixed independent mixed recommendation, each player has regret at least $`(1-c)/2`$ in at least one of the two games. [8, Proposition 6][r8]

**Proof.** The correct action gains at least $`1-c>0`$ against either opponent action, so it is strictly dominant. If player *i* chooses 1 with probability *p*<sub>*i*</sub>, its wrong-action probabilities in the two games are *p*<sub>*i*</sub> and $`1-p_i`$. Deviation to the correct action gains at least $`1-c`$ times that probability. Their maximum is at least $`(1-c)/2`$. ∎

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

For $`n\ge2`$, let $`u_i(s)=cs_i-M\prod_j s_j`$ with $`M>c>0`$, and forbid the all-one tuple. The pure equilibria are exactly profiles with $`n-1`$ active players: fewer allow an inactive player to gain *c*; all active makes deactivation profitable; at $`n-1`$, neither an active nor inactive player gains by switching. Yet the symmetric mixed equilibrium

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

with equality when all $`p_i=\eta`$. Unbiased independent marginals give failure probability 1/2, while the uniform law on F<sub>+</sub> has the same unary marginals and never fails. [8, §7][r8]

**Proposition 10 — Exact shared-variable requirement.** If a finite shared variable *Z* generates the uniform law on F<sub>+</sub> through outputs conditionally independent given *Z*, then

```math
|\mathrm{supp}(Z)|\ge2^{n-1},
\qquad H(Z)\ge n-1\text{ bits}.
```

**Proof.** Every nonempty Cartesian rectangle contained in F<sub>+</sub> is a singleton: varying any one coordinate while fixing the others flips parity. A positive mixture component cannot assign mass outside F<sub>+</sub>, since nonnegative components cannot cancel forbidden mass. Each conditional product component therefore has singleton support. Every feasible tuple needs a positive component, and the output tuple is a deterministic function of *Z*. Its entropy is $`n-1`$ bits, so both bounds follow. Taking *Z* itself uniformly distributed on the feasible tuples attains them. ∎

The bound concerns this shared-latent implementation. It is not a count of minds, persons or independent evidential sources. Interactive communication changes the resource model. Its practical content is that independent local diversity and a nonrectangular hard joint condition need a coordinating or restricting mechanism; an equilibrium certificate alone supplies none. [8, §7][r8]

## 6. Complete coordination records across a growing horizon

The finite parity example concerns one joint output law. A different coordination problem asks how much information a complete mediating record must carry as a horizon grows. Its probability and mediation hypotheses must be supplied independently; the following Gaussian results are not universal statements about memory, brains or physical resources. [9][r9]

### 6.1 Bounded capture forces information growth

For each positive integer *n*, let *P*<sub>*n*</sub> be a countably additive Borel law of real variables (Y<sub>n</sub>,S<sub>n</sub>), with $`S_n\sim N(0,n)`$. Suppose $`X_0=Y_n+S_n`$ has the same terminal distribution at every horizon considered. Let *Q*<sub>*n*</sub> be the product of the two marginals. For an interval *I* of length $`L>0`$, put

```math
p=P_n(Y_n+S_n\in I),
\qquad q_n=Q_n(Y_n+S_n\in I).
```

Here *p* is independent of the horizon because the terminal law is fixed. The maximum probability that a centered normal of variance *n* assigns to a length-*L* interval is

```math
a_n(L)=2\Phi\!\left(\frac{L}{2\sqrt n}\right)-1
\le\frac{L}{\sqrt{2\pi n}}.
```

The centered interval is maximal because the normal density decreases away from zero; shifting an interval toward zero replaces lower-density mass by higher-density mass. Integrating this bound over the independent *Y*<sub>*n*</sub> marginal gives $`0<q_n\le a_n(L)<1`$.

Use natural logarithms and information in nats. Define mutual information by relative entropy,

```math
I(Y_n;S_n)=D(P_n\Vert Q_n)\in[0,\infty].
```

The value is infinite if *P*<sub>*n*</sub> is not absolutely continuous with respect to *Q*<sub>*n*</sub>. Otherwise it is the integral of $`f\log f`$, $`f=dP_n/dQ_n`$, with $`0\log0=0`$. This definition needs no joint Lebesgue density or finite differential entropy.

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

**Proof.** For the sum event *E*, convexity of $`f\log f`$ applied separately on *E* and its complement gives binary data processing:

```math
D(P_n\Vert Q_n)
\ge p\log\frac p{q_n}
+(1-p)\log\frac{1-p}{1-q_n}
\ge p\log\frac1{q_n}-h(p).
```

If absolute continuity fails, the infinite left side makes the inequality immediate. Insert the Gaussian bound for *q*<sub>*n*</sub> to obtain the first result. Every Borel probability on $`\mathbb R`$ is tight. For each $`\varepsilon>0`$, choose one bounded interval with terminal probability at least $`1-\varepsilon`$, before allowing *n* to grow. Dividing the first bound by $`\log n`$ gives lower limit at least $`(1-\varepsilon)/2`$. Let $`\varepsilon\downarrow0`$. ∎

The finite-horizon right side can be negative, in which case nonnegativity supplies a better lower bound. Tightness alone gives no uniform additive constant or convergence rate. If a singleton terminal event has positive mass, its product-marginal benchmark probability is zero, so mutual information is infinite at that horizon; one must not substitute $`L=0`$ in the logarithmic expression. If *S*<sub>*n*</sub> is the measurable sum of a larger future block *B*<sub>*n*</sub>, data processing also gives $`I(Y_n;B_n)\ge I(Y_n;S_n)`$. [9, §§1–2][r9]

### 6.2 A consistent sharp example

Let $`A\sim N(0,\tau^2)`$, $`0<\tau^2<\infty`$, independent of a two-sided sequence of ordinary independent standard normal increments. Define positions by finite forward and backward sums from $`X_0=A`$. At horizon *n*, set $`Y_n=A-S_n`$. This is one consistent anchored recurrence, with

```math
\mathrm{Var}(Y_n)=\tau^2+n,
\quad \mathrm{Var}(S_n)=n,
\quad \mathrm{Cov}(Y_n,S_n)=-n,
\quad \mathrm{Var}(Y_n\mid S_n)=\tau^2.
```

The log density ratio of $`Y_n\mid S_n`$ to *Y*<sub>*n*</sub> has expected value

```math
I(Y_n;S_n)
=\frac12\log\frac{\tau^2+n}{\tau^2}
=\frac12\log(1+n/\tau^2).
```

To see the cancellation, write the two normal log densities: their expected standardized quadratic terms are both one, leaving half the logarithm of the variance ratio. The asymptotic coefficient is exactly 1/2. When $`\tau=0`$, the joint law lies on $`y=-s`$ and the product law gives that line zero mass, so information is infinite instead.

This anchored construction does not make the state independent of future increments. Even conditional on *A*, the relation $`Y_n=A-S_n`$ remains. A finite description of that formula is not a finite information channel mediating its dependence. Nor is this example a fresh forward-innovation law. [9, §3][r9]

### 6.3 The mediator must include every operative route

Suppose a discrete record *R*<sub>*n*</sub> mediates all dependence in the exact sense

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

With side information *U*<sub>*n*</sub>, complete mediation instead requires conditional independence given (R<sub>n</sub>,U<sub>n</sub>), and the corresponding bound is

```math
I(Y_n;S_n)
\le I(U_n;S_n)+H(R_n\mid U_n).
```

The record alone is insufficient when a prior resource carries uncontrolled dependence. A controller with finitely many instantaneous states can use an accumulating transcript, a clock or an external correlated resource. A quantized readout of a real state does not bound the information of the state itself. Program length, a law's description length and a complete mediating record are different quantities. The theorem applies only after the actual cut is established. [9, §4][r9]

### 6.4 Exact finite-alphabet capacity

**Theorem 12 — Sharp fixed-horizon capture.** Fix $`n>0`$, an interval *I* of finite length $`L\ge0`$, and an integer $`N\ge1`$. Among countably additive joint laws with $`S\sim N(0,n)`$ admitting a mediator *M* of at most *N* values with $`Y\perp S\mid M`$,

```math
\Pr(Y+S\in I)
\le 2\Phi\!\left(\frac{NL}{2\sqrt n}\right)-1.
```

For $`L>0`$, optimizing the state marginal and encoder at this one horizon attains the bound. [9, §5][r9]

**Proof.** Discard zero-probability labels. For each remaining label let ν<sub>m</sub> be the conditional law of *Y*, and let $`\lambda_m(B)=\Pr(M=m,S\in B)`$. These finite measures sum to the Gaussian law γ<sub>n</sub> and each is dominated by it, hence nonatomic. Conditional independence gives

```math
\Pr(Y+S\in I)
=\sum_m\int\lambda_m(I-y)\,d\nu_m(y)
\le\sum_m\sup_y\lambda_m(I-y).
```

For $`\varepsilon>0`$, choose for each label an interval translate *J*<sub>*m*</sub> within $`\varepsilon/N`$ of its supremum. Then

```math
\sum_m\lambda_m(J_m)
\le\sum_m\lambda_m\!\left(\bigcup_jJ_j\right)
=\gamma_n\!\left(\bigcup_jJ_j\right).
```

The union has length at most $`NL`$. A centered interval of that length maximizes Gaussian mass among Borel sets with that measure: density outside the interval is at most its boundary density, density on a missing interior portion is at least that value, and the exterior portion has no more measure than the missing portion. Therefore the last quantity is at most $`a_n(NL)`$. Let $`\varepsilon\downarrow0`$. No maximizing translate was presumed. For $`L=0`$, every translated singleton is null under each λ<sub>m</sub>, giving zero directly.

For attainment when $`L>0`$, partition a centered interval *J* of length $`NL`$ into *N* adjacent length-*L* cells *J*<sub>*m*</sub>. Draw *S* normally; assign it label *m* in *J*<sub>*m*</sub> and label 1 outside *J*. Choose constants *y*<sub>*m*</sub> with $`I-y_m=J_m`$, and set $`Y=y_M`$. Conditional independence is automatic because *Y* is constant given *M*. Capture occurs exactly on *J* up to null endpoints; exterior points assigned label 1 add no capture. ∎

Thus capture probability at least $`0<p<1`$ with $`L>0`$ requires

```math
N\ge\left\lceil\frac{2\sqrt n}{L}
\Phi^{-1}\!\left(\frac{1+p}{2}\right)\right\rceil.
```

Probability-one bounded capture is impossible for finite N,L. This square-root growth is sharper than the alphabet bound obtained by combining Theorem 11 with $`H(M)\le\log N`$. The extremizer is a retrospective, single-horizon construction. It does not preserve an independently specified state marginal, fixed terminal law or one common history at every horizon, and it is not a forward-causal physical implementation.

The retained information bounds in §§6.1–6.4 have the exact scope of the bounded-coordination supplement: countably additive joint laws, a complete mediator rather than a selected message, side information charged separately, and retrospective one-horizon quantizer attainability rather than an online controller for every horizon. Tightness of a fixed terminal law supplies the $`\liminf I/\log n\ge1/2`$ rate; zero-width capture is a separate case. The supplement credits the complete-cut, measure-guard and action-disclosure sources for those interfaces. [Q250A-001]

### 6.5 A sharp approximation-error budget

The later correction separates an approximate law from the countably additive reference to which the Gaussian theorem applies. Let *Q* meet Theorem 12 and put $`a=a_n(NL)`$. On the same event algebra let *P* be a probability law, possibly only finitely additive, with

```math
\sup_A|P(A)-Q(A)|\le\eta,\qquad0\le\eta\le1.
```

**Theorem 13 — Robust finite mediation.** For $`E=\{Y+S\in I\}`$,

```math
P(E)\le\min(1,a+\eta).
```

The one-event inequality $`|P(E)-Q(E)|\le\eta`$ already suffices. For every nonempty target interval, the bound is sharp at one horizon, even when *P* retains the same Gaussian *S* marginal. [10][r10]

**Proof.** The upper bound follows from $`P(E)\le Q(E)+\eta\le a+\eta`$ and $`P(E)\le1`$. No entropy or conditional probability under *P* is used.

For $`L>0`$, take the extremizing *Q* above and let $`\delta=\min(\eta,1-a)`$. The Gaussian law is nonatomic, so choose a Borel set $`C\subseteq\mathbb R\setminus J`$ of mass δ. Keep *S* unchanged. On *C*, replace the state by $`Y'=c-S`$ for a fixed $`c\in I`$; elsewhere leave it alone. The new law *P* has capture $`a+\delta`$. This coupling changes the pair only on a set of probability δ, so event total variation is at most δ. The capture event's probability changes by exactly δ, proving equality and sharpness. For a nonempty singleton target, the same alteration on a Gaussian set of mass η gives capture η while every finite-mediator reference has capture zero. An empty target always has capture zero. ∎

The modified law generally loses the reference's finite complete mediator; that is what the error allowance permits. If $`P(E)\ge p`$, $`L>0`$ and $`0<p-\eta<1`$, then

```math
N\ge\left\lceil\frac{2\sqrt n}{L}
\Phi^{-1}\!\left(\frac{1+p-\eta}{2}\right)\right\rceil.
```

When $`p\le\eta`$ there is no positive alphabet-size conclusion; when $`L=0`$ one only obtains $`p\le\eta`$; and $`p-\eta=1`$ is impossible for finite N,L. The Gaussian marginal and complete-mediation assumptions belong to *Q*. Allowing finite additivity in the event-transport step does not transport Gaussian entropy or conditional independence to *P*. All attainment claims retain their fixed-horizon and retrospective scope. [10][r10]

### 6.6 Finite-additive concentration and the weakest capture contradiction

The earlier information lower bound has stronger probability assumptions than are needed for a concentration obstruction. Let P be an ordinary real-valued, nonnegative, normalized, finitely additive probability. Require measurability of the interval, tail, rectangle and sum events used. Suppose Y and Z have interval-rectangle independence and Z has the interval and tail probabilities of an ordinary centered Gaussian with variance v>0. Mutual independence among noise increments is insufficient: an earlier state may encode its future increments. [N250A-246]

For a bounded interval I of length L contained in [−R,R], fix δ>0 and M>R. Partition [−M,M] into finitely many interval cells C_j of length at most δ, treating endpoints so they form a disjoint finite partition. On Y∈C_j and Y+Z∈I, Z lies in an interval of length at most L+δ. Since the Gaussian density is bounded by c_v=1/√(2πv), independence and positivity give

P(Y∈C_j, Y+Z∈I) ≤ P(Y∈C_j)c_v(L+δ).

Finite summation bounds the contribution with |Y|≤M by c_v(L+δ). On the remaining part of the sum event, |Z|>M−R. Therefore

P(Y+Z∈I) ≤ c_v(L+δ)+P(|Z|>M−R).

The Gaussian marginal's tight tail makes the second term arbitrarily small, and δ can then be arbitrarily small. Ordinary real-order comparison yields

P(Y+Z∈I) ≤ L/√(2πv).

No countable sum under P, countable additivity of the joint law or tightness of Y is used. The tail of Z controls large compensating Y on the particular sum event. [N250A-246]

Now fix one terminal law and suppose X₀=X₋ₙ+Z_n for every positive integer n, with Z_n∼N(0,n) independent of X₋ₙ in the stated sense. For every bounded I,

P(X₀∈I) ≤ |I|/√(2πn) for all n,

so P(X₀∈I)=0. A single independently warranted capture P(X₀∈I)>0 contradicts this package. Full terminal tightness and countable additivity of the terminal marginal are convenient stronger sufficient premises, not the weakest ones. All horizons must concern the same terminal law. A realized finite value or one successful reading does not itself warrant positive prospective capture; conditioning on a terminal observation can also destroy historical independence. Innovation, capture and interpretation must remain in the same probability and information state. [N250A-246] [N250A-249]

The supplied review checks the concentration argument at its actual finite-additive boundary: finite partitions and a tail estimate replace a countable interchange, full noise-law hypotheses cannot be obtained merely by invoking a countably additive extension theorem, and the sharp real-valued inequality must not be exported unchanged to a non-Archimedean probability. There an arbitrarily small standard error may leave an infinitesimal remainder; a strict-slack positive-width estimate survives where the exact singleton conclusion need not. These are scope qualifications on the retained proof, not a new review of its underlying primary sources or of every later reporting protocol. [Q250A-003]

### 6.7 Quantitative separation from independence

Let P_n be an actual pair law with the block recurrence, Gaussian block marginal and the same terminal law at every horizon. Let Q_n be a lawful independent benchmark on the same measurable pair-event domain. Define event total variation by

d_TV(P_n,Q_n)=sup_E |P_n(E)−Q_n(E)|,

whose maximum for probability laws is one, including under finite additivity. For E_I={(y,z):y+z∈I}, write p_I=P(X₀∈I). Concentration under Q_n gives

d_TV(P_n,Q_n) ≥ max(0,p_I−|I|/√(2πn)).

This is a separating-event proof, not an invocation of coupling or Radon–Nikodym characterizations. One fixed capture p_I>0 gives liminf d_TV≥p_I. If the one terminal law is tight, choose I_ε with mass at least 1−ε first, hold that interval fixed as n increases, then let ε decrease. The result is d_TV(P_n,Q_n)→1. Tightness alone gives no rate uniform over all terminal laws. None of this says the noise increments cease to be mutually iid; the dependence measured is between state and future block. [N250A-246] [N250A-249]

Benchmark existence must not be hidden in notation. For a countably additive state marginal ν_n, its usual product with γ_n=N(0,n) is canonical. For a real-valued finitely additive ν_n on the full Borel σ-algebra of R, at least one benchmark on B(R²) is

Q_n(E)=∫_fa γ_n({z:(y,z)∈E}) dν_n(y).

The inner section probability is bounded Borel. Uniform approximation by Borel simple functions defines the outer positive normalized integral; pointwise addition of disjoint sections proves finite additivity. Rectangles have value ν_n(A)γ_n(B), giving both marginals and independence. The construction fixes an integration order. It neither proves uniqueness among all finitely additive extensions nor lets rectangle values determine every Borel value by countably additive uniqueness. On a smaller event algebra, retain benchmark existence as a premise unless the required domain and integration hypotheses have been established. [N250A-249]

### 6.8 A coherent diffuse history and positive controls

The missing bounded-capture premise is real, not a technical omission that pointwise finiteness repairs. On Ω=R×R^Z, give the noise coordinates their ordinary countably additive iid Gaussian law Q, put X₀=x, and define every X_t by the finite signed innovation sum from zero. All positions are finite and every recurrence holds pointwise. For positive integers R, let P_R make x uniform on [−R,R] independently of the noise. A fixed nonprincipal-ultrafilter limit of P_R on every Borel event defines one ordinary real-valued normalized finitely additive μ with the same entire noise marginal Q. [N250A-246]

To obtain full past/future independence, fix t and compare P_R with the law reanchored uniformly at X_t. The event-total-variation difference is bounded by

E_Q[min(1,|S_t|/(2R))]→0,

using the distance between translated uniform intervals and ordinary dominated convergence under Q. Under the reanchored law, past states and noise depend on X_t and earlier noise and are independent of future noise. The error bound is uniform over all Borel events, so factorization passes to μ for the full past state/noise and future-innovation σ-fields at every fixed t. Reanchoring also gives stationarity and translation-invariant position marginals. Every bounded position interval has μ-probability zero although every position is finite. The position law is not countably additive; the noise law remains so. No countable intersection is used to obtain the pointwise recurrences, and no effective sampler follows from the nonconstructive ultrafilter. This constructs one coherent zero-capture law, not all non-tight entrance laws or a concrete metaphysical realization. [N250A-246]

The anchored notation is not a barrier to finite forward interventions. Replacing ξ_j by a with δ=a−ξ_j while shifting x by δ for j<0 and by zero otherwise leaves X_t unchanged for t≤j and adds δ for t>j. For finite replacement set J, the anchor shift is Σ_{j∈J,j<0}(a_j−ξ_j), and the state shift at t is Σ_{j∈J,j<t}(a_j−ξ_j). Distinct replacements commute. These are Borel pushforwards, not conditioning on null Gaussian events. Unchanged innovations retain their joint Gaussian law, and past/future factorization survives because transformed past and future use their corresponding original information. This supplies abstract finite-intervention semantics; it does not establish physical manipulability, and divergent infinite anchor shifts block an automatic extension to arbitrary infinite recombination. [N250A-246]

The finite-intervention algebra also distinguishes commuting replacements from overwriting one coordinate. Replacing the same coordinate twice by the same value is idempotent; two different values obey last-write-wins. Two finite replacement maps commute exactly when they agree on their overlap. Their pushforwards retain spatial translation invariance, hence null probability for every bounded state interval, while intervention at selected times may destroy time stationarity. Thus preservation of the unmodified innovation law and the past/future factorization is not preservation of every symmetry of the original process. These claims concern finite, fixed interventions, not adaptive state-dependent choices or an infinite past whose anchor correction may fail to converge. [Q250A-002]

Three controls prevent overgeneralization. First, ordinary iid Gaussian increments anchored at X₀=0 obey every recurrence but make X₋ₙ depend on its future block. Equations and mutually iid noise do not supply freshness. Second, for 0<|a|<1 the two-sided Gaussian autoregression

X_t=Σ_{j≥0}a^j ξ_{t−1−j}

converges in L² and almost surely, and countable additivity supplies one common probability-one set for every integer t. It has tight stationary variance 1/(1−a²), fresh future innovations and infinitely many nonzero coefficients. Its n-block innovation variance (1−a^{2n})/(1−a²) stays bounded, so it fails the accumulating-variance premise rather than refuting concentration. Nonzero coefficients are not automatically concrete productive contributions. Third, X_t=t with deterministic innovation one is a nonstationary countably additive bi-infinite entrance law for translation even though Z admits no countably additive invariant probability. It fails the spreading-noise premise; absence of a stationary law alone is insufficient. [N250A-246] [N250A-249]

Searching successively for |X₀|≤m terminates at a finite stage on every sample, but μ(success by m)=0 for every fixed m. The eventual-termination event has probability one. The difference is the absent continuity-from-below principle, not a contradiction, an implemented search algorithm or a finite-expected-runtime result. [N250A-246] [N250A-249]

### 6.9 Operational capture and a law-specific diachronic test

#### Positive capture from an actual access contract

A same-law operational premise can supply precisely the capture that M1 requires. If a valid capture C has prospective chance at least s>0 and C⊆{X₀∈I} for a bounded operating range, then P(X₀∈I)≥s. This requires a warranted chance of delivery, not merely conditional soundness of delivered reports, a direction to try, or one actual successful episode. [N250A-247]

The budget need not be fixed in advance. Let T≥0 be resource use and require a finite b(m) for each finite m such that

C∩{T≤m}⊆{|X₀|≤b(m)}.

Finite subadditivity gives

P(C)≤P(|X₀|≤b(m))+P(T>m).

If P(C)≥s>0, one tail bound P(T>m)<s already implies positive bounded mass. A tight T marginal suffices; independence between T and X₀ is unnecessary. Under the diffuse μ, any such magnitude-sensitive acquisition with tight resource marginal therefore has zero success probability. Randomizing the budget with a countably additive finite-valued law does not restore the guarantee. This rejects μ as a model of that justified task, not as a possible law under every task. [N250A-247]

The actual correction does not yet identify this magnitude-sensitive task. A sign query has just two faithful outputs and a positive-half-line probability of 1/2 under μ, while both output inverse images are unbounded. Finite semantic output therefore need not be bounded magnitude capture. A bounded encoding of the corrected sentence does not automatically retain Gaussian additive dynamics. Actual target/evidence/subject fidelity, conditional safety, positive opportunity, prior chance and posterior knowledge must remain distinct. If μ is an objective history law rather than the agent's operative previsions, the bridge to those previsions is also a substantive premise. [N250A-247]

#### Positive-mass reports with zero conditional chance in every cell

The diffuse law itself supports a concrete nonconglomerability test. Put N=1+floor(|X₀|), so each {N=n} is μ-null, and A={ξ₀≥0}, with μ(A)=1/2. From independent Gaussian coordinate ξ₁ construct an integer K with q_n=2^(−n), independent of A in the ordinary noise marginal. Report R=N on A and R=K on Aᶜ. The Borel cells H_n={R=n} form a countable exhaustive partition, with

μ(H_n)=q_n/2>0,  μ(A∩H_n)=0,  μ(A|H_n)=0 for all n.

These are ordinary positive-denominator ratios, not arbitrary choices on null reports. No independence between N and A is needed. The sum of the cell masses is 1/2 even though their union is the full space, a permitted failure of countable additivity. [N250A-247]

Suppose μ supplies the agent's operative valuations, R is eventually disclosed without extra information about A, an A-ticket remains transferable until that disclosure and can later settle, small stakes have additive state-independent value, costs and delay do not alter the comparison, and the agent accepts each contemporaneously favorable offer or precommits to that policy. For 0<ε<1/4, buy the unit A-ticket for 1/2−ε and sell after any exact report for ε. Each transaction has expected gain ε at its own information state. Their combined payoff is the fixed loss −1/2+2ε<0. There are two bounded transactions on each history, not an infinite portfolio. The second trade has negative prior expectation; the example does not contradict static finite-bet coherence. [N250A-247]

The action opportunities matter. The report may require arbitrarily long but pointwise finite acquisition; formula measurability is not an algorithm, and exact floor identification from approximate real names has a boundary problem. Memory, counterparty, transferability and settlement must persist across that duration. Timing or other revealed information can change the posterior. A defender may reject this access contract, reject compulsory acceptance of every local favorable offer, or choose a dynamically sophisticated policy that rejects the dominated composite. Those responses restrict the operational policy without making μ's static event probabilities inconsistent. [N250A-247]

#### A total integer reporter separates computation from maintained resources

The integer analogue removes a specific computational objection without supplying a sampler for the finitely additive law. Its anchor $`X_0`$ is an actual finite integer in every sample, while every finite set of anchor values has probability zero. Supply its sign privately and its magnitude on a finite unary tape $`1^{|X_0|}0`$; put $`N=1+|X_0|`$. The input is supplied, not sampled by the reporter. Let $`A=\{\xi_0=+1\}`$ and let $`K_\infty`$ be the first head in the later fair-bit tape. Each round reads one magnitude-tape cell and one later bit in the same padded phase. Set $`K^*=\min(K_\infty,N)`$, with the cap also applying to an all-tails tape, and emit the pulse at $`R=N`$ on $`A`$ and at $`R=K^*`$ otherwise. The controller finishes on every finite supplied input and every bit tape, not merely almost surely: $`R\le N`$. A finite-state controller is sufficient for this pulse protocol. [Q250A-000]

Although $`K^*`$ uses the anchor cap and therefore is not causally a noise-only variable, its entire marginal is the ordinary geometric law $`q_n=2^{-n}`$. For fixed $`n`$, its difference from the first-head event is confined to the null event $`\{N\le n\}`$. The same observation gives the joint probabilities with $`A`$; the geometric tail bound supplies tightness rather than an illicit countable sum under the ambient finitely additive law. With $`H_n=\{R=n\}`$, this gives $`\mu(H_n)=q_n/2>0`$, $`\mu(A\cap H_n)=0`$ and $`\mu(A\mid H_n)=0`$, whereas $`\mu(A)=1/2`$. The cap repairs exceptional-tape termination without changing the exact-report calculation. [Q250A-000]

The information contract matters as much as the program. The trader sees only a common start, the round clock, prior silence and the pulse, not the branch bit, input sign, input length, private cells or state-dependent loading time. A transaction before the branch bit is read and one in the designated post-pulse phase, before the branch is revealed, can implement the two prices $`1/2-\varepsilon`$ and $`\varepsilon`$. Each trade has conditional expected gain $`\varepsilon`$ at its information state; their combined payoff is identically $`-1/2+2\varepsilon`$ for $`0<\varepsilon<1/4`$. Selling the retained ticket or cancelling it with its issuer locks that loss at the reporting time; an additional later executed settlement is not required, although the ticket's warranted retained value remains part of the contract. Following these conditional-price recommendations is a further normative premise, not a consequence of computational termination. [Q250A-000] [Q250A-004]

The full anchor input length misses every fixed finite bound with probability one, but the report runtime does not. Writing $`Q_m=1-2^{-m}`$, one has $`\mu(R\le m)=Q_m/2`$ and $`\mu(R>m)=1-Q_m/2\to1/2`$. Thus runtime is pointwise finite and non-tight, while its bounded-runtime events have positive probability. On $`A`$, runtime equals $`N`$ and misses each fixed deadline with conditional probability one. The silence posterior remains $`1/(2-Q_m)`$, exactly the residual branch used below. The protocol needs an unbounded repertoire of supplied finite inputs, indefinitely maintained service and opportunities, and an unbounded timestamp repertoire if exact timestamps are stored; it does not need infinite working memory during a run merely to emit a pulse. This is a total abstract integer protocol, not an exact-real Gaussian acquisition algorithm, a physical sampler, or an actual realization of the complete support contract. [Q250A-000]

#### Finite deadlines restore the omitted residual branch

Schedule report R at stage R. At deadline m put Q_m=Σ_{n≤m}q_n=1−2^(−m) and D_m={R>m}. Then

μ(R≤m)=Q_m/2,  μ(D_m)=1−Q_m/2,

μ(A∩D_m)=1/2,  μ(A|D_m)=1/(2−Q_m)>1/2.

Ordinary finite-partition averaging holds. Trading only on reports received by m no longer produces uniform loss: retaining the ticket is profitable when A holds on D_m. Trading also on D_m requires its higher correct valuation, not ε. Eventual arrival itself is the whole space and leaves μ(A|eventual arrival)=1/2, despite all exact-report conditionals being zero. The issue is admissibility of the completed non-tight information schedule, not the number of transactions. [N250A-247]

For a purely forecasting version, quadratic loss is L(p,A)=(p−1_A)². Retaining p=1/2 loses 1/4 everywhere. Updating to each exact-report posterior gives p=0 and prior expected loss μ(A)=1/2, although every report assigns the update conditional expected loss zero rather than 1/4. Thus this completed update policy loses the usual prior averaging justification for value of information. Ignoring the report remains an option; no universal scoring-based epistemology is assumed. At finite deadline the conditional forecasts are zero on H₁,…,H_m and 1/(2−Q_m) on D_m, with prior expected loss

(1−Q_m)/[2(2−Q_m)]≤1/4.

These finite-stage forecasts converge pointwise to zero and their expected losses tend to zero, while the limiting forecast's expected loss is 1/2. This is failure of bounded convergence under μ, pinpointing the extra continuity or operational warrant required to pass to the completed protocol. [N250A-247]

Two weaker proposals should not be conflated with this argument. Positivity and finite linearity exclude uniform sure loss from a static finite set of bounded bets at μ-fair prices. But g=1/(N+1) is positive at every sample and has expectation zero because g≤1_{N≤m}+1/(m+1); selling it for zero gives everywhere-strict loss with no uniform positive lower bound. Rejecting that trade uses a stronger strict-dominance norm and may require arbitrarily fine physical payoff precision. Likewise, “my value is finite” has μ-probability one but does not select a positive-mass bounded cell. Comparative or reflection principles across all cells require their own warrant; any finite check leaves an unbounded residual. [N250A-247]

Null actual capture does not admit ratio conditioning under μ alone, though a separately assessed full conditional model or revision could specify an update. If a rival task law Q gives capture C positive probability and a two-model mixture gives both laws positive prior weights, observing C sets the μ-component's posterior weight to zero by ordinary mixture conditioning. This is a valid bounded calculation, not metaphysical impossibility. When Q gives positive probability to every bounded reporting cell, the same elimination at every exact report reproduces nonconglomerability at the model-label level; it does not independently validate the whole acquisition/update policy. A tight posterior also cannot be combined silently with an unconditional freshness law. [N250A-247]

These weaker-additivity concentration and access results do not extend the entropy or finite-mediator theorems of §§6.1–6.4 beyond their countably additive hypotheses. The source research assessment and its quantitative review retain distinct historical scopes; no new execution, primary inspection, general priority or kernel validation is claimed. Effective witness search and budget refusal remain separately treated in [Measure, computability and finite warrant](measure-computability-and-finite-warrant.md#51-the-effective-search-and-its-premises). [N250A-246] [N250A-247] [N250A-249]

## 7. Temporal learning, coordinated restoration and model transfer

### 7.1 A mixed equilibrium need not restore a target

Suppose a finite joint response set *S* carries a fixed law μ, sampled independently at each time, and let $`T\subseteq S`$ be a separately supplied target.

**Theorem 14 — Repeated independent deployment.**

```math
\Pr(\text{eventually always in }T)=1
\quad\Longleftrightarrow\quad \mu(T)=1.
```

If $`\mu(T)<1`$, eventual target persistence has probability zero. [5, §7][r5]

**Proof.** A target-supported law remains in the target at every time with probability one. Otherwise the bad probability is some $`p>0`$. For any fixed time *N*, the probability of no bad draw in the next *m* steps is $`(1-p)^m\to0`$. The probability of no bad draw after *N* is zero. Eventual persistence is the countable union of these null events over *N*. ∎

In the two-player agreement game, both players independently mixing $`(1/2,1/2)`$ is Nash. Repeated independent deployment mismatches with probability 1/2 each round and infinitely often almost surely. A shared fair bit choosing (0,0) or (1,1) has the same individual marginals and always agrees. It is a different joint law. Neither mechanism's agreement alone establishes truth, cognitive implementation or the authority of the common signal.

### 7.2 What does guarantee progress?

A separate temporal argument can establish entry and persistence. Suppose a licensed stochastic update process has a nonnegative integer rank *R*, an invariant target, no rank increase outside target, and conditional expected rank decrease at least $`\varepsilon>0`$ after every non-target history. Let τ be first target entry and $`R_0<\infty`$ the fixed initial rank. Then

```math
\mathbb E\tau\le R_0/\varepsilon,
\qquad\Pr(\tau<\infty)=1.
```

**Proof.** Stop the rank at target entry. Conditional expected decrease at step *t* is at least $`\varepsilon\mathbf1\{\tau>t\}`$. Sum expectations through $`n-1`$ and use nonnegativity of the stopped rank:

```math
\varepsilon\sum_{t=0}^{n-1}\Pr(\tau>t)
=\varepsilon\mathbb E\min(\tau,n)\le R_0.
```

Monotone convergence yields the expectation bound and excludes positive probability of infinite entry time. Target invariance supplies persistence. If every non-target transition instead decreases the integer rank strictly, the stronger sure bound $`\tau\le R_0`$ follows. ∎

A geometric self-loop distinguishes the conclusions: it has positive expected progress and almost-sure entry but admits an infinite sequence of idle outcomes. An arbitrary controller switch can also reset a rank. The common progress certificate and its history-relative premises are additional scientific obligations, not consequences of the equilibrium label. [5, §7][r5]

For deterministic finite dynamics, a related result identifies the evaluation that progress tracks. Let *X* be a nonempty finite set, $`G:X\to X`$ a transition and $`W:X\to\mathbb R`$ an independently supplied evaluation. Put $`M=\arg\max W`$. If $`W(Gx)>W(x)`$ outside *M* and $`G(M)\subseteq M`$, every trajectory enters *M* within $`|X\setminus M|`$ transitions and remains there. A pre-entry trajectory cannot repeat a state because *W* strictly rises; there are only that many nonmaximum states. If maxima are additionally fixed pointwise, then $`\mathrm{Fix}(G)=M`$. [6, §4][r6]

Equality of fixed points and maxima alone is weaker. Take $`X=\{0,1,2\}`$, $`W=(1,0,0)`$ and $`G(0)=0,G(1)=2,G(2)=1`$. Its only fixed point is its unique maximum, but the other states cycle forever. Weak ascent permits a nonmaximal fixed point; dropping target closure permits later exit; dropping pointwise fixation can leave a cycle entirely inside the maximizing set. Distinguishing these conditions preserves the difference between convergence of states and satisfaction of a target.

Finally, a finite ordinal-potential game has no infinite strict-improvement path: each unilateral improvement strictly raises one common potential on a finite set. This is the classical finite-improvement property. It does not cover idle transitions, changing games or disturbances without further hypotheses. [15, Lemma 2.3][potential]

### 7.3 The exact cost of incompatible response marginals

The independent-deployment example leaves a constructive question: when can a coordinator retain the agents' specified marginal responses while making their joint response appropriate? Fix finite nonempty response sets A,B, probability laws μ,ν, and a supplied target relation $`R\subseteq A\times B`$. A coupling is a nonnegative joint table κ with those two complete marginals. This section initially permits every pair in $`A\times B`$; hard exclusions are an additional constraint. For $`U\subseteq A`$, let

```math
R[U]=\{b\in B:\text{some }a\in U\text{ satisfies }(a,b)\in R\},
\qquad
\delta(\mu,\nu,R)=
\max_{U\subseteq A}\bigl(\mu(U)-\nu(R[U])\bigr).
```

The empty subset gives $`\delta\ge0`$, and $`\delta\le1`$. Zero-probability atoms are allowed in this mathematical statement. [17, §1][r13]

**Theorem (sharp marginal obstruction).** The minimum target-violation probability over all couplings is exactly $`\delta(\mu,\nu,R)`$. In particular, a coupling supported on *R* exists if and only if

```math
\mu(U)\le\nu(R[U])
\quad\text{for every }U\subseteq A.
```

**Proof.** Under any coupling, mass starting in *U* can stay within the relation only by arriving in $`R[U]`$. That arrival region has total capacity $`\nu(R[U])`$, so at least $`\mu(U)-\nu(R[U])`$ of the mass must violate the relation. Maximizing over *U* proves the lower bound.

For attainment, form a finite transportation network. A source supplies row *a* with capacity $`\mu(a)`$, a column *b* drains to the sink with capacity $`\nu(b)`$, and every pair in *R* has a row-to-column edge of capacity 2. A cut of capacity at most one exists. Thus a minimum cut cannot cross a relation edge. If *U* is its source-side row set, its source-side column set must contain $`R[U]`$; among these choices, taking exactly $`R[U]`$ minimizes the cut. Its capacity is

```math
\sum_{a\notin U}\mu(a)+\sum_{b\in R[U]}\nu(b)
=1-\mu(U)+\nu(R[U]).
```

The max-flow/min-cut theorem therefore supplies an *R*-supported subcoupling of mass $`1-\delta`$. [22][flow] Its residual row masses *r*<sub>*a*</sub> and column masses *s*<sub>*b*</sub> are nonnegative and each total δ. If $`\delta=0`$, the subcoupling is already complete. Otherwise add the table $`r_as_b/\delta`$. A positive residual row and positive residual column cannot be related: adding the smaller residual along that relation edge would augment the maximum flow. The added mass therefore lies entirely outside *R*, and its total is exactly δ. Both full marginals are restored. ∎

For binary agreement, $`R=\{(0,0),(1,1)\}`$, the deficit is $`|\mu(0)-\nu(0)|`$. Marginals $`(4/5,1/5)`$ and $`(1/5,4/5)`$ force disagreement probability 3/5. The joint table with masses $`1/5,3/5,0,1/5`$ in the order 00,01,10,11 attains it. Equal fair marginals have zero deficit, even though independent sampling disagrees with probability 1/2. The marginals do not determine the deployed coupling.

#### Licenses and incentives restrict the available couplings

If only pairs in a set $`L\subseteq A\times B`$ are licensed, the admissible joint law must be supported on *L*. The unrestricted deficit remains a lower bound but need not be attainable. With fair binary marginals and target $`R=\{(0,0)\}`$, the unrestricted optimum is 1/2. If (1,1) is forbidden, the marginal equations force both diagonal masses to zero. The only licensed law gives each off-diagonal pair mass 1/2, and its target violation is one. An unavailable completion cannot be repaired by interpreting a probability constraint as permission.

Incentive compatibility is a further condition when the response loci are strategic players. For scalar payoffs u<sub>1</sub>,u<sub>2</sub>, a common recommendation law is a correlated equilibrium when obeying a received recommendation is at least as profitable as switching it. The first player's inequalities are

```math
\sum_{b\in B}\kappa(a,b)
\bigl(u_1(a,b)-u_1(a',b)\bigr)\ge0
\quad(a,a'\in A),
```

with the corresponding column inequalities for the second player. These are the unconditional form of recommendation-conditional comparisons; a recommendation of zero mass creates no additional obligation. Correlated equilibrium belongs to established game theory. [23][aumann] The information contract here gives each player its own recommendation and the declared game. Additional current private signals, sequential observation of other actions or a richer deviation menu require the appropriate conditional incentive constraints. These inequalities do not automatically cover that enlarged game. [17, §4][r13] [21, §C2][r17]

In matching pennies, let player 1 receive one for agreement and player 2 one for disagreement. A fair diagonal coupling implements agreement perfectly but gives player 2 a profitable deviation from each recommendation. With fixed fair marginals, write the four masses as $`t,1/2-t,1/2-t,t`$. Player 1's obedience requires $`t\ge1/4`$; player 2's requires $`t\le1/4`$. Hence the only compliant joint law is uniform and its agreement-target violation is 1/2. If both players instead receive one for agreement, the diagonal law is an equilibrium. Feasibility of correlation does not determine its incentive properties.

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

Each hard exclusion forces a cell to zero, and each recommendation inequality gives a linear bound on *t*. Their intersection is a closed interval or is empty. Target-violation mass is affine in *t*, so an endpoint minimizes it whenever the interval is nonempty. Requiring the inequalities under every member of a declared finite collection of payoff standards gives an exact robust version. Averaging standards instead requires its own justified probability interpretation. Neither calculation establishes the authority of the supplied standards.

More generally, let $`\mathcal C`$ be the nonempty compact polytope of couplings satisfying the supplied marginals, licenses and incentive inequalities. Then

```math
\delta^*=\min_{\kappa\in\mathcal C}\kappa(R^c)
```

exists and satisfies $`\delta\le\delta^*`$. An empty feasible polytope means that the response contract is not implementable; it is not assigned an artificial infinite violation probability. A selected joint table still needs a realizable sampler and the channels through which recommendations or coordinated actions are implemented.

Pairwise compatibility also falls short of global compatibility. For three binary loci with fair marginals, each pair has a perfectly anticorrelated coupling. No triple can make all three pairs different, since three binary values cannot be pairwise distinct. Every pairwise marginal test passes while the proposed global target is empty. Multiway coordination needs an actual joint law. A shared random source can supply correlation but does not multiply independent evidence or create new permission to coordinate. [17, §5][r13]

### 7.4 Restoration under dependent repeated responses

The stationary independent case in Theorem 14 has an exact extension to history-dependent responses. Let $`(\mathcal F_t)_{t\ge0}`$ be a filtration containing the decision history before the next response. At time *t*, the target *R*<sub>*t*</sub>, response marginals μ<sub>t</sub>,ν<sub>t</sub> and any admissible coupling polytope are measurable with respect to $`\mathcal F_t`$. The realized response pair is recorded by $`\mathcal F_{t+1}`$. In particular,

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

Thus $`\sup_n\mathbb E Z_n^2\le1`$, and the square-integrable martingale convergence theorem gives convergence of *Z*<sub>*n*</sub> almost surely. Fix a path on that convergence event and write $`b_t=1+H_{t+1}`$, a positive nondecreasing sequence.

If $`H_\infty=\infty`$, summation by parts, or equivalently Kronecker's lemma applied to the convergent series $`\sum D_{t+1}/b_t`$, gives

```math
\frac{C_n-H_n}{1+H_n}\longrightarrow0,
\qquad
\frac{C_n}{H_n}\longrightarrow1.
```

For completeness, this summation argument separates finitely many initial terms from a tail whose partial sums have magnitude at most an arbitrary ε. The weighted tail, divided by its final nondecreasing weight, has magnitude at most $`2\varepsilon`$; the initial contribution tends to zero.

If $`H_\infty<\infty`$, the weights *b*<sub>*t*</sub> are bounded and their total variation is finite. The same summation-by-parts identity now shows that $`\sum D_{t+1}`$ converges: the convergent partial sums of $`D_{t+1}/b_t`$ are multiplied by bounded endpoint weights, and the remaining series is bounded by their supremum times the total variation of *b*<sub>*t*</sub>. Therefore $`C_n=H_n+\sum_{t<n}D_{t+1}`$ has a finite limit. A nondecreasing integer-valued count with a finite limit can increase only finitely often. These two cases establish the event equality. ∎

In particular, a nonsummable deficit forces infinitely many target violations on the event $`\sum_t\delta_t=\infty`$. A fixed positive deficit is sufficient but unnecessary: $`\delta_t=1/(t+2)`$ also has a divergent sum. Conversely, an implementation with summable actual conditional violation probabilities eventually remains in the target almost surely.

For a deterministic schedule of marginals and targets, with every pair available and every selected finite coupling implementable, an eventually-target implementation exists **if and only if** $`\sum_t\delta_t<\infty`$. Necessity follows from the pointwise lower bound. For sufficiency, select a minimizing coupling at each time; its conditional violation probability is exactly δ<sub>t</sub>. The same equivalence holds with $`\delta_t^*`$ for deterministic nonempty licensed or incentive-constrained polytopes. The statement is about the specified schedule and sampler, not existence of a finite-memory realization. In an endogenous context, the current coupling can alter future marginals, polytopes and deficits. Minimizing today's violation does not prove dynamic optimality.

Two elementary schedules make the boundary explicit. Let the first response equal 0 with probability δ<sub>t</sub> and the second always equal 1; the target is agreement. The conditional violation probability is necessarily δ<sub>t</sub>. With $`\delta_t=1/(t+2)^2`$, violations are finite almost surely, and

```math
\Pr(\text{some violation at or after }N)
\le\sum_{t=N}^{\infty}\frac1{(t+2)^2}
\le\frac1{N+1}.
```

Every fixed late time still has a positive violation probability, so there is no deterministic last-violation horizon. With $`\delta_t=1/(t+2)`$, the probability of no violation in a block starting at *N* with length *m* is

```math
\prod_{t=N}^{N+m-1}\left(1-\frac1{t+2}\right)
=\frac{N+1}{N+m+1}.
```

The product follows by conditional multiplication because the conditional hazards have the stated deterministic values. Its limit is zero, and violations recur infinitely often. Both deficits are positive and tend to zero; their summability separates the conclusions.

#### Public certification and physical restoration are different events

The filtration condition is essential. Suppose one unobserved bit *Z* is fixed forever and is bad with probability 1/2. Under a public filtration with no information about it, its conditional bad probability is always 1/2. Yet infinitely many actual bad occurrences have probability 1/2, not one. The repeated physical events are not measurable in the next public sigma-algebra, so the theorem does not apply there. Revealing *Z* creates an adapted filtration but changes its conditional probabilities to zero or one. One cannot combine the enlarged filtration with the old half-probabilities. [17, §3][r13]

A finite plant also separates physical persistence from a demanding public certificate. Let the target states be $`\{0,2\}`$, start at 2, and give all states the same observation. State 0 remains at 0; state 1 moves to 0; state 2 stays at 2 with probability 1/2 and moves to each of 0 and 1 with probability 1/4. Every supported path has at most one bad visit, because its only bad state is 1 and that state immediately enters the absorbing good state. Physical eventual persistence is therefore sure, even on zero-probability supported infinite paths.

After one step the public support belief is $`\{0,1,2\}`$, and it remains that set forever. A certificate demanding that the next entire support belief lie inside the target consequently rejects the sole response at every time. Its certified target relation is empty and has Hall deficit one. This is correct evidence that the chosen public certificate is never met. It is not evidence that physical restoration is impossible. The actual bad-state probability at time $`t\ge1`$ is $`2^{-(t-1)}/4`$.

The same distinction applies when a previously proved finite-memory safety certificate permits only actions whose every observation successor stays in its certified winning region. A realizable joint law supported on those permitted actions preserves that certificate. Positive deficit obstructs the particular prescribed-marginal certificate implementation; it does not refute another bound, another winning policy, or actual target persistence. Establishing public knowledge of restoration is a stronger task than establishing restoration itself.
### 7.5 Transferring a restorative controller without a hidden-state oracle

A controller that succeeds in one stochastic model need not remain valid after its observations, action interface or disturbance law change. Preserving the list of possible transitions is insufficient for an almost-sure claim. Even exact transition couplings are insufficient if their proposed action translator consults hidden information. The following finite-model contract separates the probability proof, the information available to the implemented controller, and the destination's independent authorization. It consolidates the exact transfer result and its later private/public-memory refinement. [18, §§2–6][r14] [19, §1][r15]

#### Models, policies and information

Let the source have finite hidden state set *X*, finite actions *A*, observation map $`o_A:X\to O_A`$, initial law μ<sub>A</sub>, and finite nonempty disturbance menus $`D_A(x,a)`$. A disturbance *d* selects a full transition distribution $`P_A^d(\,\cdot\mid x,a)`$. Define a destination with Y,B,o<sub>B</sub>,μ<sub>B</sub>,D<sub>B</sub>,P<sub>B</sub> in the same way. Each law includes every outcome, favorable or otherwise. Stochastic observations can be represented by adding the emitted observation to the plant state, provided the **joint** transition law is retained. This representation does not turn observations sharing one provenance root into independent copies.

A source behavioral policy σ assigns a distribution on the next action to every finite source observation/action history. It may use the entire history. Its current action is sampled freshly after that history is fixed; it does not expose future action coins stored in advance. After the current action, the source adversary can use the complete source state/action history and choose a randomized member of the current disturbance menu. A guarantee against this full-history adversary class is a premise of the transfer theorem.

The destination interface has a finite controller-available mode set *Q* and a projection $`\pi:Q\to P`$ onto its public mode. It specifies:

| Interface component | Information used |
|---|---|
| Initial mode $`q_0(o)`$ | Initial destination observation. |
| Reconstructed source observation $`\eta(q,o)`$ | Controller mode and current destination observation. |
| Admitted source-action menu $`M(q,o)\subseteq A`$ | The same controller information. |
| Executed action $`b=\tau(q,o,a)`$ | Controller mode, observation and its sampled virtual source action. |
| Next controller mode $`q'=u(q,o,a,b,o')`$ | Available controller information and the new observation. |
| Destination warrant $`J_B(\pi(q),o,b)`$ | The declared public mode, observation and actual destination action. |

The word “public” carries a mathematical obligation. There must be a function *v* such that, on every used update,

```math
\pi\bigl(u(q,o,a,b,o')\bigr)
=v\bigl(\pi(q),o,b,o'\bigr).
```

Thus the public projection is reconstructible from the actual destination trace. Several virtual actions can translate to the same executed action; the controller may remember which one it sampled, but an external observer need not know it. If the entire mode is declared public, π is the identity and the update cannot distinguish private virtual actions hidden by the same public trace. Publicly logging those actions would change the observation contract.

The source policy must put all its probability on $`M(q,o)`$ at every reachable interface history. This includes the histories under all permitted disturbances, not just the successful sampled examples. It is a policy-conformance premise, separate from verification of the finite plant tables.

The fibre criterion in Proposition 3 applies equally to action kernels: an implementation depending only on information $`I(h)`$ realizes a prescribed kernel $`K(h)`$ exactly when *K* is constant on every fibre of *I*. A local hidden-state witness saying that **some** matching action exists for each hidden pair does not ensure a single available-information rule. Reconstructing the full source observation is a convenient sufficient condition here. A coarser reconstruction can suffice for a particular policy, but only after its action and memory updates are proved to factor through that coarser history.

#### A full probabilistic certificate

Supply a relation $`R\subseteq X\times Y\times Q`$. At every $`(x,y,q)\in R`$, with $`o=o_B(y)`$, require all of the following.

1. **Information:** $`\eta(q,o)=o_A(x)`$.
2. **Meaning and authority:** destination badness implies source badness; source safety implies destination safety. For every $`a\in M(q,o)`$, the source action is eligible at *x*, its translation *b* is eligible at *y*, and the supplied public warrant $`J_B(\pi(q),o,b)`$ holds. Any additional task-readout preservation is another explicit relation, not an inference from the safe/bad labels.
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

4. **Complete initial laws match:** a coupling κ<sub>0</sub> has marginals μ<sub>A</sub>,μ<sub>B</sub> and positive mass only on pairs with $`(x,y,q_0(o_B(y)))\in R`$.

The existential source disturbance and coupling can depend on the related hidden triple and the selected destination disturbance. The implemented translator and mode update cannot inspect that hidden proof data. A populated source memory, learned history or migration memento also needs an initial-law/interface match; matching the current plant output alone does not authorize discarding it.

For rational finite tables, the matching problem for a fixed candidate source disturbance is exact transportation feasibility. The retained implementation searches over individual source disturbance kernels. Allowing a convex mixture of such kernels could give a weaker sufficient certificate against the randomized source adversary, but that additional search is not supplied by the checker. Neither successful transport nor its numerical feasibility certifies the truth or authority of the input labels.

#### The implemented controller and the path-law proof

Initialize $`q=q_0(o_B(y_0))`$ and the virtual source history with $`\eta(q,o_B(y_0))`$ and the explicitly matched initial source memory. At each step sample *a* from σ on that virtual history, execute $`b=\tau(q,o,a)`$, retain the virtual action *a*, receive o′, update q′, and append $`a,\eta(q',o')`$ to the virtual history. The implementation never observes or samples the proof's hidden source state.

**Theorem (exact restorative transfer).** Under the certificate, public-projection and policy-conformance premises, suppose the source policy has only finitely many bad visits almost surely against every permitted randomized full-source-history adversary. Then the implemented destination policy has only finitely many bad visits almost surely against every destination adversary. Source sure safety also transfers under the safety implication. Destination eligibility and public warrant are separately supplied at every reachable interface state.

Here “only finitely many bad visits” is a temporal property of the actual path. It does not assert a publicly recognized entry into an invariant core or a deterministic bound on the last bad time.

**Proof.** First suppose each plant has a single disturbance kernel for each state/action pair. Build a joint process from κ<sub>0</sub>. At each related triple and joint finite past, draw *a* from the source policy, translate it, and draw (x′,y′) from the full coupling. The relation's observation identity proves inductively that the source observation/action history is exactly the destination controller's virtual history. Thus the action kernel in the construction is the actual implemented kernel on both sides; it is not secretly conditioned on hidden *x* or later success.

The probability of a finite joint cylinder is the product of the initial mass, its successive policy probabilities and its coupling probabilities. All factors are nonnegative, and summing one-step extensions gives back the cylinder's mass. Summing each transition over y′ gives the complete source kernel. Because the action probability depends only on the source observation/action history, summing all destination histories leaves exactly the source controlled finite-history law. Summing instead over x′ gives the complete destination kernel. The controller mode and virtual action history are retained on the destination side, so this second marginal is the actual implemented destination law. No unfavorable branch is removed or renormalized.

These consistent finite-cylinder laws define a probability measure on infinite joint histories. All recorded states, actions and interface modes range over finite alphabets; unbounded behavioral memory is represented by finite histories rather than an additional arbitrary memory alphabet. To see the measure-extension condition directly, every finite union of cylinders is closed in the compact product of these finite discrete alphabets. A decreasing sequence of nonempty such sets has nonempty intersection. Consequently a decreasing sequence with empty intersection eventually has zero cylinder-algebra mass, supplying continuity at the empty set and the standard extension to the generated sigma-algebra. Cylinders determine that extension uniquely.

The relation holds initially and is preserved by every positive joint transition. A countable intersection therefore makes it hold at every time with probability one. On that event, every destination bad visit is a source bad visit, and

```math
\Pr_B(\text{bad infinitely often})
\le
\Pr_A(\text{bad infinitely often}).
```

The right side is zero by hypothesis.

Now fix an arbitrary nonanticipating destination adversary, allowing it to see the full destination state history and the controller's past/current virtual actions and available memory. In the joint construction it chooses *d*<sub>*B*</sub> first; the certificate then supplies *d*<sub>*A*</sub> and the coupling. The destination marginal is still exactly the selected adversary's process.

The chosen source disturbance can depend on the latent destination history. Condition on a positive-probability finite source state/action history *h* and its already sampled current action *a*. Let $`\lambda_d(h,a)`$ be the conditional probability that the construction selected disturbance *d*. Then

```math
\Pr(X_{t+1}=x'\mid h,a)
=\sum_{d\in D_A(x_t,a)}
\lambda_d(h,a)P_A^d(x'\mid x_t,a).
```

This is an allowed randomized full-source-history adversary. At each finite time the conditioning is a ratio over finite sets; zero-probability histories can be assigned arbitrary legal choices. It does not condition on any future event. The source action kernel remains σ, since it was drawn freshly from the source observation/action history before either disturbance was selected. The source marginal is therefore a law covered by the robust source hypothesis, so the same event inclusion proves restoration.

For sure safety, a supported unsafe destination finite history would have positive probability under some legal disturbance choices. The exact joint lift would contain a supported source finite history ending in a related unsafe destination state. The safety implication forces that source state to be unsafe, contradicting source sure safety. The same lifting argument places every reachable destination history under the certificate's eligibility and warrant clauses. Their truth is an assumption supplied to the certificate, not established by the probabilistic argument. ∎

The randomized source-adversary class is necessary for this proof. If that adversary were restricted to public observations rather than full source histories, the induced conditional mixture might use information unavailable to it. A transfer theorem for that narrower adversary class needs an additional compatibility argument. It cannot inherit this conclusion by changing the word “adversary.”

#### Why support, information and authority remain separate

Several finite counterexamples isolate the independent hypotheses. [18, §6][r14]

* **A support simulation can lose all restoration probability.** Let source bad state *b* stay at *b* or enter an absorbing good state *g*, each with probability 1/2. Let destination bad state *B* remain there forever, with a separate absorbing good state *G*. The relation pairs *b* with *B* and *g* with *G*. Every destination edge has a source support match, and badness reflects. The source restores almost surely; the destination fails surely. A relation-supported full coupling at (b,B) is impossible because half the source mass must go to *g* while all destination mass goes to *B*. Conditioning on the source self-loop would erase half the law at each step.
* **Matching actions can require unavailable information.** A fixed fair hidden bit *h* is visible to the source and invisible to the destination. Each round guesses 0 or 1, and the state is bad exactly when the guess differs from *h*. Physical transitions under identical guesses can be coupled exactly. The source always guesses *h*; a destination with the same observation under both bits has the same action-sequence law under either. The disjoint events “eventually all guesses are 0” and “eventually all guesses are 1” cannot both have probability one. A hidden-pair-dependent choice of the matching guess is an oracle, not an implementation.
* **A coupling does not create destination permission.** In any valid finite certificate, deleting one required public warrant entry leaves the transition marginals untouched while invalidating the action's authority clause.
* **One matched initial pair does not match two initial laws.** If a source begins with probability one at *b*, a destination law assigning half its mass to an unrelated *G* cannot be matched merely because (b,B) is a valid pair.
* **A sufficient certificate need not exist whenever both systems restore.** One-action geometric-exit systems with exit probabilities 1/2 and 1/3 both restore almost surely, but their identity relation cannot couple their distinct one-step laws. A policy that never uses a source observation distinction can also transfer through a policy-specific coarsening even if full observation reconstruction fails.

These counterexamples preserve a constructive result: with a verified information interface and full laws, transfer is possible. Rejection of this particular certificate is not a general impossibility theorem for all controllers, relations or information-preserving translations.

#### Finite memory and the timing of randomization

If the source policy has an *M*-state realization with fixed initial memory, deterministic updates from its observation/action history and fresh current-action draws, the destination construction needs at most $`|Q|M`$ memory states, apart from the convention for storing the current observation. A history-dependent policy that uses an unbounded counter remains unbounded. A supplied external clock is memory, not a free finite-state implementation.

An arbitrary randomized-memory realization cannot be substituted under a changed memory-exposure contract. A finite prediction game shows why. Its plant has a prediction state *P*, locked-prediction states Q<sub>0</sub>,Q<sub>1</sub> and an absorbing good state *G*; all other states are bad. Observations distinguish P,Q,G but hide the subscript of *Q*<sub>*h*</sub>. A controller samples a fair private bit *r* before each prediction phase and waits. The disturbance then chooses *h* and moves to *Q*<sub>*h*</sub>. The controller responds *r*; a mismatch enters *G*, while a match returns to *P* and refreshes the private bit. No disturbance choice after the response can revise the locked prediction.

For every nonanticipating full-plant/action-history adversary blind to the current bit, *r* is conditionally fair when the prediction is made. Failure through *n* rounds therefore has probability $`2^{-n}`$, and restoration is almost sure. An adversary allowed to inspect the pre-sampled bit instead chooses $`h=r`$ and keeps the system bad forever. Identical plant kernels and identity couplings do not fix that change of information.

Sampling the bit freshly at *Q*<sub>*h*</sub>, after the prediction is locked, removes the exposed future randomness and restores the behavioral theorem's guarantee. The historical correction accordingly restricts the finite-memory product bound or requires a separate proof that the realization preserves the behavioral action kernel under the declared memory exposure. This counterexample concerns implementation equivalence; it does not refute the fresh-action transfer theorem. [21, §F1][r17]

Probabilistic simulation, full transition liftings and controller refinement have established mathematical ancestry. Haesaert, Soudjani and Abate's exact relation includes both transition and initial-law liftings; its interface may depend on both model states. The observation-restricted construction above adds a specific sufficient information contract and independently supplied destination authority. Their approximate finite-horizon theorem includes an accumulating probability error; it does not by itself assert exact infinite-horizon persistence. [25, Definition 6 and Theorem 3][refinement]
### 7.6 Composing transfers while keeping warrant public

Passing a controller through two valid interfaces creates a further information question. Something publicly visible at the intermediate plant may become a privately remembered virtual action at the final plant. It cannot automatically remain part of the final public warrant. The private/public split in §7.5 makes this distinction explicit and supports exact composition. [19, §§2–4][r15]

Consider a source *A* whose state $`x\in\{0,1\}`$ is observed and whose action *a* sets the next state to *a*. An intermediate plant *B* has state $`y\in\{0,1\}`$ and the same state-setting actions, but only a constant observation. The first interface translates $`b=a`$ and tracks *y* through a public mode updated from the actually executed action *b*. It reconstructs the source observation exactly. A final plant *C* has one state, one observation and one action, tick. The second interface translates either *B* action to tick and reconstructs *B*'s constant observation with a constant mode. Start *A* and *B* at 0; all states and actions in this structural example are supplied as good, safe and licensed.

Both individual interfaces have full deterministic couplings and all-public modes. In the composite, however, two different virtual actions produce the same actual *C* trace while requiring different reconstructed *A* observations. The mode tracking the original state is controller-private at *C*. Keeping it public would make the supplied two-action interface invalid. This is not an impossibility result for every particular constant policy; it is a failure of closure for the stated all-public interface class.

#### The composite interface

Let a valid split interface from *A* to *B* have private mode $`q\in Q_1`$, projection π<sub>1</sub>, relation R<sub>AB</sub> and functions η<sub>1</sub>,τ<sub>1</sub>,u<sub>1</sub>. Let an interface from *B* to *C* have mode $`r\in Q_2`$, projection π<sub>2</sub>, relation R<sub>BC</sub> and functions η<sub>2</sub>,τ<sub>2</sub>,u<sub>2</sub>. The middle plant is one and the same model, including observations, transition kernels, eligibility, safe/bad meanings and initial law. A correspondence between differently represented middle models would need a separately proved transport; the retained constructor requires exact equality.

Require menu compatibility: whenever the first interface permits a source action at a relevant composite information state, its translated *B* action belongs to the second interface's menu. Silently deleting an incompatible source action would change the policy-conformance obligation.

Use the product private mode (q,r) and the final public projection

```math
\pi(q,r)=\pi_2(r).
```

For current *C* observation *o* and source action *a*, define

```math
\begin{aligned}
o_B&=\eta_2(r,o),&
\eta((q,r),o)&=\eta_1(q,o_B),\\
b&=\tau_1(q,o_B,a),&
c&=\tau_2(r,o,b).
\end{aligned}
```

After receiving o′, the available update is

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

Initialize *r* from the actual *C* observation, reconstruct the initial *B* observation, and initialize *q* from it. The original source controller retains the memory its policy requires.

**Theorem (composition with a private product mode).** These formulas define a valid source-to-final split interface. They preserve full probability laws, source-to-final badness and safety implications, and the final destination's independently supplied public warrant. The restorative-transfer theorem applies under its original robust policy premises.

**Proof.** Fix a related triple $`(x,w,(q,r))`$, choose a middle witness *y*, and fix an admitted source action and a final disturbance. The second certificate supplies a middle kernel *P*<sub>*B*</sub> and a coupling κ<sub>BC</sub> with the selected *P*<sub>*C*</sub>. For that **same** middle kernel, the first certificate supplies a source kernel *P*<sub>*A*</sub> and a coupling κ<sub>AB</sub>. Define

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

Whenever a triple mass is positive, the second relation guarantees that the reconstructed next middle observation is the actual $`o_B(y')`$. The displayed q′,r′ are therefore exactly the component updates at the same successor y′. Both component successor relations hold, proving support in R<sub>AC</sub>. The middle state is a proof witness; the implementation computes its interface from q,r,a,o,o′ and never inspects that state.

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

With an *M*-state source realization having deterministic history updates and fresh action draws, the product implementation needs at most $`|Q_1||Q_2|M`$ controller-memory states. The random-memory exposure qualification remains unchanged. The finite relation certificate does not turn an unbounded source policy into a finite-memory one.

The theorem composes the supplied safe/bad meanings, not arbitrary task identity. If additional readout relations are to compose through the same middle witness, that claim needs its own statement and proof. Replacing such a claim by equality of coarse output labels can be a stronger and unjustified assertion. The composition of correct kernels likewise does not establish that real evidence has those kernels or that its final use is authorized.

### 7.7 Approximation needs an occupancy bound or a genuine return

Exact relatedness can be relaxed in more than one way, and the distinction matters for eventual persistence. A bound on leaving a relation concerns departures. Restoration concerns the amount of time spent in bad states. A single departure can occupy the entire remaining future. [20, §§1–3][r16]

#### One departure can destroy eventual persistence

Let a source consist of one always-good state. A destination begins at good state *S*. At time *t*, while at *S*, it enters an absorbing bad state *F* with probability

```math
\delta_t=\frac1{(t+2)^2},
```

and otherwise remains at *S*. Relate the source state only to *S*. Every path has at most one departure, and its conditional departure hazard is bounded by a summable deterministic sequence. Nonetheless the no-departure probability after *n* transitions is

```math
\prod_{k=2}^{n+1}\left(1-\frac1{k^2}\right)
=\prod_{k=2}^{n+1}\frac{(k-1)(k+1)}{k^2}
=\frac{n+2}{2(n+1)}
\longrightarrow\frac12.
```

Thus restoration succeeds with probability exactly 1/2. On the remaining paths, the single departure produces infinitely many bad visits. Conditional Borel–Cantelli correctly guarantees finitely many departures; it does not guarantee finite bad occupancy. With any constant fault probability $`\delta>0`$, no-departure probability is $`(1-\delta)^n\to0`$, so arbitrarily small constant local error can destroy almost-sure restoration entirely.

#### An exact law can tolerate summably many occupancy defects

Sometimes only the target-preservation part of an interface is approximate. Let *S* be an invariant relation on which the information reconstruction, full probability-law coupling and destination authority of §7.5 remain valid at every time. Let $`R\subseteq S`$ be the subrelation on which destination badness implies source badness. In the full joint proof filtration, let

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

**Proof.** Exact gluing on *S* supplies the actual source and destination marginals for all time. The adapted-event theorem implies only finitely many *E*<sub>*t*</sub>. At every time,

```math
\mathrm{Bad}_B(Y_t)
\Longrightarrow
\mathrm{Bad}_A(X_t)\ \text{or}\ E_t.
```

Both exceptional time sets on the right are finite almost surely. ∎

No public detector for *E*<sub>*t*</sub> is needed in this particular theorem, since the implemented information interface and authority stay valid even during the mismatch. Its probabilities must nevertheless be conditioned on a filtration to which the physical events are adapted. A coarser public conditional probability cannot be substituted without that premise. If leaving the target-preserving relation also destroys observation reconstruction or invalidates controller memory, the invariant-interface premise fails and this proof is unavailable.

#### An executable regenerative repair

A genuinely broken interface requires a recovery policy and a legitimate restart. Retain discrete time, finite state/action/observation alphabets and controller memory determined by finite histories, possibly unbounded. Recovery may be history-dependent. This ensures countably many possible finite entry histories; a model with arbitrary continuous random recovery memory needs a corresponding regular-conditional-kernel formulation.

Assume the destination distinguishes running and recovery modes. A fault flag *D*<sub>*t*</sub> is generated after transition *t*, is observable by time $`t+1`$, and begins recovery. Conservative flags are permitted. The following four obligations are separate.

1. **Finite conditional fault budget.** For the full nonanticipating joint filtration, $`D_t\in\mathcal F_{t+1}`$ and predictable $`\delta_t\ge0`$ satisfy

```math
\Pr(D_t\mid\mathcal F_t)\le\delta_t,
\qquad
\sum_t\delta_t\lt{}\infty
\quad\text{almost surely}.
```

2. **Sound public detection while running.** Before a flag, the implementation uses the observation-compatible translated policy. Every running step has full source and destination marginals, including the actual flag/observation process. A no-flag successor remains in the relation and preserves the information interface, public projection and badness implication. A flagged successor may leave it. An existential hidden coupling does not itself implement a detector: the flag must be available through the declared destination interface.
3. **Almost-sure finite recovery.** From every reachable recovery entry and every allowed conditional law, a specified executable recovery policy reaches a public reentry point in finite time with conditional probability one. It may visit bad states during recovery. Any required sure safety and action authority must hold independently on all recovery actions and possible outcomes. If flags are suppressed during recovery, this recovery contract must already cover its disturbances; they cannot disappear from the obligations.
4. **Complete reentry law and memory.** At every reached controller-information reentry history *h*, the actual conditional destination law has a full initial coupling with a source law $`\mu_A^h`$ in a declared winning family. The policy $`\sigma^h`$, chosen from available information, restores almost surely for that family against the same full-source-history adversary class. Its reconstructed history, memory, mode and authority are reset or transferred through an explicit valid interface. If several hidden or environment-conditioned laws are compatible with *h*, the statement must hold for each induced law. Selecting one favorable initial pair is insufficient.

The initial state must have a valid running entry or an initial recovery satisfying the same almost-sure completion condition.

**Theorem (regenerative restoration).** Under these premises, the destination has only finitely many bad visits almost surely. The conclusion does not assert finite expected recovery duration or a deterministic cutoff time.

**Proof.** The conditional fault budget and §7.4 give only finitely many flags almost surely. Every recovery entry has conditional probability zero of never completing. Because entry times and finite histories form a countable population, the union of those noncompletion events is null. Thus, outside a null set, some final running episode begins at a finite time and receives no further flag.

It remains to justify that final episode without changing its law by conditioning on future success. Fix an episode index *j* and a positive-probability reentry history *h*. Start the full source/destination coupling supplied by the reentry contract and use the running step couplings until the first flag. If a flag occurs, continue the **proof's source process only**, from its actual source state and memory, with its original source policy and any legal source disturbance. This auxiliary continuation is not an extra destination operation.

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

First replace the absorbing failure state in the square-hazard example by an observed recovery state. From recovery return to *S* with probability $`\rho=1/2`$ per step. With the stipulated safety and licenses, the fault budget remains summable, each recovery is geometric, and reentry restarts the always-good source. Regenerative restoration therefore has probability one.

This particular example gives more than the general theorem. If *r*<sub>*t*</sub> is its probability of occupying recovery at time *t*, then

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

Second, almost-sure finite recovery need not have finite expectation. In recovery, let elapsed counter *k* return on the next step with probability $`1/(k+2)`$ and otherwise increment. For its positive-integer duration *T*,

```math
\Pr(T>n)=
\prod_{k=0}^{n-1}\left(1-\frac1{k+2}\right)
=\frac1{n+1}\longrightarrow0,
\qquad
\mathbb ET=\sum_{n=0}^{\infty}\Pr(T>n)=\infty.
```

One such recovery followed by an always-good running mode satisfies eventual persistence while its expected bad occupancy is infinite. This policy uses unbounded elapsed-time memory; it is not a counterexample about a fixed finite homogeneous Markov chain.

Third, successful recovery after every fault does not guarantee that faults eventually cease. With fixed fault probability $`\delta>0`$ from *S* and fixed return probability $`\rho>0`$ from recovery, the finite two-state chain is irreducible. Its stationary recovery mass solves $`r=(1-r)\delta+(1-\rho)r`$, giving

```math
r=\frac{\delta}{\delta+\rho}>0.
```

Recovery is visited infinitely often almost surely. Thus recovery can work each time while permanent correctness fails. Conversely, the finite-fault budget is sufficient rather than necessary for every architecture: infinitely many harmless flags need not create actual bad visits or destroy a winning interface. [20, §4][r16]

#### Mathematical and executable scope

The retained finite implementations check supplied coupling tables, private/public projections and compatible compositions using exact rational data. Their transportation witnesses expose both marginals; composition requires the same middle law; the independent tests preserve the hidden-information, missing-warrant and exposed-future-coin counterexamples. Finite-history and recurrence probes give bounded implementation evidence. They are not proofs of infinite-horizon measure statements, automatic synthesis of every interface or recovery controller, or validation of an actual cognitive system. The proofs above supply the stated infinite conclusions from their declared premises. [17][r13] [18][r14] [19][r15] [20][r16] [21][r17]

The remaining practical work is concrete: establish the actual joint kernels and provenance dependence, prove policy-menu conformance under all admitted disturbances, realize the sampler and information interface, supply destination warrant, and—for regenerative use—implement sound fault detection and a complete conditional reentry-law/memory contract. The ordinary research does not provide a general recovery synthesizer, an unrestricted migration decision procedure, a formal-kernel proof of these probability theorems, or permission to infer scientific truth from a finite checker. Preserving those distinctions makes the conditional results usable without overstating their reach.

### 7.8 Learning a hidden standard: memory, certainty and permission

A fixed hidden standard can be statistically learnable even though no finite observation certifies it. The memory and objective of the learner then matter independently of the size of the physical plant. Consider a standard $`h\in\{0,1\}`$ chosen initially and held fixed. Conditional on *h*, the acquisitions $`Y_1,Y_2,\ldots`$ are independent, with

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

The statistical dependence of acquisitions on *h*, the assignment of a target response to *h*, and permission to issue either response are three supplied assumptions. The model derives no norm from a frequency. [26][r18]

**Theorem (memory and certainty separate).** In this model:

1. No policy is sure to satisfy $`\mathcal R_h`$ under both standards.
2. One deterministic policy using unbounded memory satisfies $`\Pr_h(\mathcal R_h)=1`$ under both standards.
3. No finite, time-homogeneous controller satisfies that almost-sure guarantee under both standards.
4. For every $`\varepsilon>0`$, a finite controller achieves $`\Pr_h(\mathcal R_h)\ge1-\varepsilon`$ under both standards.
5. No rule can identify the standard with zero error under both models by a declaration that occurs after finitely many acquisitions almost surely.

Here a finite, time-homogeneous controller has a finite total internal state, a fixed initial law independent of the hidden standard, and fixed action and update kernels based on its available information. Randomized kernels are allowed. An unbounded clock, an externally changing transition table, or an increasing-precision register is additional memory. The physical state, any separately supplied current observation and any response needed to label correctness are included when compiling the controller into a finite chain.

**Proof of the sure impossibility.** Every finite bit word has positive probability under both standards. In particular, the infinite all-zero word is admitted by both support models: every one of its finite prefixes is possible. A deterministic policy has the same response sequence on that word in both models. The sequence cannot be eventually always zero and eventually always one. For a randomized policy, the same argument fixes a common supported sequence of its internal choices. Sure success quantifies over those choices and supported observations, including paths of probability zero. ∎

**Proof of almost-sure learning with unbounded memory.** After acquisitions $`1,\ldots,2m`$, choose their majority bit, resolving a tie as zero. Hold that response until the next even acquisition count. Let *K*<sub>*m*</sub> be the number of ones among the first $`2m`$ acquisitions. Under $`h=0`$, Markov's inequality gives

```math
\Pr_0(K_m\ge m)
\le \frac{\mathbb E_0[2^{K_m}]}{2^m}
=\frac{(4/3)^{2m}}{2^m}
=\left(\frac89\right)^m.
```

An incorrect response under $`h=0`$ actually requires $`K_m>m`$, so this bound is conservative. Under $`h=1`$, the number of zeros has the same law as *K*<sub>*m*</sub> under $`h=0`$. It also bounds the adverse tie and every incorrect majority response. Thus the error probabilities of the successive update blocks have finite sum, at most

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

**Proof of finite-memory approximation.** Given $`0<\varepsilon<1`$, choose *m* with $`(8/9)^m\le\varepsilon`$. Acquire $`2m`$ samples, then commit forever to their majority. The same finite-sample bound makes the wrong-commitment probability at most ε under either standard. One implementation stores a pair (n,k), where $`0\le n\le2m`$ and $`0\le k\le n`$, and uses two terminal commitment states. Consequently

```math
\frac{(2m+1)(2m+2)}2+2
```

states suffice. This is an upper bound, not a memory-optimality theorem. The memory size changes when the requested error changes. Arbitrarily good finite-memory approximation and one almost-surely successful finite-memory policy have different quantifiers. ∎

**Proof of the finite-declaration obstruction.** Fix a finite sample count *n* and a declaration *d*. For each word $`w\in\{0,1\}^n`$, let $`k_{n,d}(w)`$ be the probability, over the rule's own randomization, that it first stops at *n* and declares *d* on that word. The rule is the same under both standards, so this nonnegative factor is the same. The declaration probability under *h* is

```math
\Pr_h(\tau=n,D=d)
=\sum_{w\in\{0,1\}^n}\Pr_h(Y_{1:n}=w)\,k_{n,d}(w).
```

Every word probability is positive under both models. A declaration event has positive probability under one precisely when it has positive probability under the other. Declaring zero must therefore have zero probability under both models if zero error under $`h=1`$ is required; declaring one likewise has zero probability under both if zero error under $`h=0`$ is required. The countable union over *n* cannot have probability one. Continued revisability is compatible with almost-sure eventual correctness; it does not provide a finite zero-error certificate that revision can safely end. ∎

#### Acquisition roots and action authority

Two changes to the model remove the constructive conclusion for different reasons.

First, retain the biased one-time marginal law but draw only one bit *Z* and report $`Y_t=Z`$ forever. Each of the two complete report words has positive probability under both standards. Conditional on either word, the learner has the same law of internal choices and responses in both models. Almost-sure correctness under both would require that common conditional response law to be concentrated both on eventual zero and on eventual one, which are disjoint events. It is impossible. Repeated reports of one acquisition do not supply the independent acquisitions used by the majority proof. One physical device can supply independent acquisitions if its actual stochastic and evidential model warrants them; the relevant quantity is independent acquisition events, not device count.

Second, retain fresh acquisitions but permit response *a* only when $`a=h`$. Add a response “abstain” that is always permitted but never correct. Both standards remain possible after every finite public history. A menu requiring eligibility for every still-possible standard therefore contains neither binary guess. Only abstention remains, so no permitted policy achieves restoration. A small probability of error does not eliminate a positive-support possibility or supply permission to disregard it. A risk-tolerant permission rule would change the model's substantive authority premise.

The equal-support argument also has a precise limit. The two biased independent acquisition processes have the same one-step support, yet their different probabilities permit the unbounded-memory learner above. If the two biases are instead made equal while their targets remain opposite, their complete observation laws coincide. The induced response law of any common policy then cannot assign probability one to both disjoint eventual-response events. Thus unrestricted almost-sure learnability can change without any change of one-step support. The support test proved above applies to an already fixed finite homogeneous controller; it does not classify every unbounded strategy.

#### Hidden objectives and a legitimate common-objective specialization

The finite-memory obstruction is consistent with the theorem of Chatterjee, Doyen, Raskin and Sankur for multiple-environment Markov decision processes. Their model has a finite family of transition laws on a shared observed state space and **one common parity objective**. Their Theorem 4 establishes decidability of almost-sure winning and sufficiency of pure finite-memory strategies, with the stated exponential memory bound. [31, §§2–3][memdp]

Here correctness depends on the unobserved standard. The same observed response state can be correct under one model and incorrect under the other. No single priority labeling of that observed state represents both targets. Adding the hidden standard to the acceptance label does not make it observed. The common-objective theorem cannot be applied by silently removing this distinction.

A useful permitted specialization can nevertheless be stated exactly. Let $`x_t=(s_t,c_t)`$ be the complete finite observed state: *s*<sub>*t*</sub> records the physical state and *c*<sub>*t*</sub> the public evidence and permission state. Every additional public signal used by the policy or its eligibility test must be represented there. Let *H*<sub>*t*</sub> be the fixed environments still possible from the complete observed history, and write $`q_t=(x_t,H_t)`$. Require a known finite, time-homogeneous transition law $`K_h(x'\mid q,a)`$ for this complete observed successor under each fixed environment. This is a Markov premise about the entire compiled observation, not merely the physical marginal. If the public state has further history-dependent dynamics, they must admit the stipulated finite compilation before this specialization applies.

Initialize *H*<sub>0</sub> using the complete initial observation. For initial laws μ<sub>h</sub> on the finite observed state and admitted environment set $`\mathcal E`$, the exact support updates are

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

On a history the policy can generate, an environment is possible exactly when each factor in this finite product is positive. The initial rule and successive updates express that condition by induction. In particular, a possible transition cannot remove its actual environment. The pair consisting of this successor observation and the deterministic live-set update also defines the finite transition law on *q*. Rows with $`h\notin H`$ may be completed arbitrarily: they are unreachable under environment *h* from the compatible initial state.

The physical marginal alone can lose a decisive observation. For example, take one physical state, one common action and two environments. The physical state stays fixed with probability one under both environments, while the next public state is $`c'=h`$. Observing $`c'=0`$ leaves only environment zero, and observing $`c'=1`$ leaves only environment one. A rule testing only the physical successor instead retains both. It produces a conservative superset, not the exact set needed by the stated compilation. A physical-only test is justified when the public update supplies no further support discrimination; a common deterministic update from the already observed physical transition is one sufficient restriction.

Require the permitted action set $`\Gamma(q)`$ to be determined by the observed compiled state, including any robust eligibility and warrant conditions. Require also one common parity objective on that state. The complete transition law then yields a finite multiple-environment model with common action menus: the law varies with the fixed environment, while state meanings, available actions and objective do not. A state with no permitted action is a losing analysis dead end; representing it by a losing sink does not authorize a physical action.

The cited common-objective theorem applies to this explicit model, starting from each observed initial state with its compatible environment set. Its complexity is measured on the compiled representation, not on an unspecified succinct permission language. Simultaneously satisfying all candidate targets can sometimes be expressed as a common objective. Satisfying only the actual hidden standard is a different requirement. Ongoing hidden physical state, switching environments, unbounded public memory or a target depending on the unknown environment removes the stated specialization.

#### A whole trace can be nonatomic and still identify a target

The acquisition example also separates a property of an entire observation law from success on one decision target. For a random observation *V*, let

```math
S_V=\{v:\Pr(V=v)>0\},
\qquad
d_{\mathrm{atom}}(V)=1-\Pr(V\in S_V).
```

All singletons here are measurable. The finite prefix $`Y_{1:n}`$ has a finite positive atomic law, so $`d_{\mathrm{atom}}(Y_{1:n})=0`$. For the complete trace and any fixed infinite word *w*,

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

The right sides are summable. Borel–Cantelli, applied to a countable sequence of positive δ tending to zero, yields $`T_{k^2}/k^2\to p`$ almost surely. For $`k^2\le n\le(k+1)^2`$, monotonicity of the counts gives

```math
\frac{T_{k^2}}{(k+1)^2}
\le\frac{T_n}{n}
\le\frac{T_{(k+1)^2}}{k^2}.
```

Both bounds converge to *p*. Define a decoder to return zero on traces with limiting frequency 1/3, one on those with limit 2/3, and any fixed value elsewhere. These are measurable limit conditions. Under any prior giving both standards positive mass, the decoder equals the actual standard almost surely. It is not correct on every support-admitted trace, and it cannot be replaced by a finite zero-error stopping declaration.

The atomic-mass defect of the complete trace therefore does not mean “no useful information” or “every decision target fails.” Its whole-observation property and this one-target identification claim have different quantifiers. Neither supplies the target's truth, empirical interpretation or action authority.

### 7.9 High average accuracy can coexist with perpetual errors

Finite-memory learning has several performance criteria. Let H<sub>+</sub> and H<sub>−</sub> give independent Bernoulli acquisitions with probabilities 2/3 and 1/3, respectively, with equal hypothesis priors. A time-average Bayes error is

```math
\overline e
=\lim_{n\to\infty}\frac1n\sum_{t=1}^n
\frac{\Pr_+(a_t=-)+\Pr_-(a_t=+)}2,
```

when the limit exists. Eventual correctness instead requires only finitely many errors on almost every path. The following exact family has arbitrarily small long-run average error as its memory grows, but restoration probability zero under each hypothesis. [27][r19]

#### An exactly solvable finite learner

Take $`S=L+1\ge2`$ memory states $`0,\ldots,L`$ and $`0<\varepsilon\le1`$. At an interior state, acquisition one moves right and acquisition zero moves left. At state zero, acquisition one moves to state one with additional probability ε; otherwise the learner stays at zero. At state *L*, acquisition zero moves left with additional probability ε; otherwise it stays at *L*. The extra randomization is fresh and independent of the acquisition.

For acquisition bias $`0<p<1`$, all adjacent moves have positive probability, and the endpoints have positive self-loops. The chain is irreducible and aperiodic. Set $`r=p/(1-p)`$. Its unnormalized stationary weights are

```math
w_0=1,\qquad
w_L=r^L,\qquad
w_i=\varepsilon r^i\quad(1\le i\le L-1).
```

For $`S\ge3`$, detailed balance on the first edge reads $`1\cdot\varepsilon p=(\varepsilon r)(1-p)`$. Each edge between interior states has ratio *r*, and the last edge reads $`(\varepsilon r^{L-1})p=r^L\varepsilon(1-p)`$. For $`S=2`$ there is only one edge: both directions carry the extra factor, with rates $`\varepsilon p`$ and $`\varepsilon(1-p)`$. Their ratio is again *r*, so the endpoint weights above remain correct without an interior-state argument. Normalizing the weights gives the stationary law. [21, §C3][r17]

For completeness, this law also describes the long-time distribution from any initial state. From any memory state *i* to any *j*, there is a path through zero of length at most $`2L`$. Positive self-loops at zero pad it to exactly $`2L`$ steps. Consequently every entry of $`P^{2L}`$ is positive. If

```math
\alpha=\sum_j\min_i P^{2L}(i,j)>0,
```

each row contains the same subprobability vector of mass α. Removing that common part leaves a stochastic residual of mass $`1-\alpha`$. The total-variation distance between two distributions contracts by at most $`1-\alpha`$ every such block. Thus the normalized stationary law is unique and every initial distribution converges to it. If $`\alpha=1`$, convergence after that block is immediate.

Under H<sub>+</sub> the ratio is two; the stationary law under H<sub>−</sub> is its reflection about $`L/2`$. With equal priors, choose minus below the midpoint and plus above it. At an integer midpoint either fixed response or a fair random tie has the same Bayes error. Define

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

**Proof.** Under H<sub>+</sub>, state zero issues an incorrect response; under H<sub>−</sub>, state *L* does. The finite irreducible chain visits each state infinitely often almost surely, by the bounded-path argument in §7.8. Hence each hypothesis produces infinitely many incorrect responses with probability one. ∎

For example, $`S=21`$ and $`\varepsilon=1/1000`$ give the exact stationary Bayes error

```math
E_{21}(1/1000)=\frac{1267}{524812787}
\approx2.41\times10^{-6},
```

while the probability of eventual permanent correctness remains zero. The statement concerns actual repeated incorrect responses, not merely a failure to certify an otherwise correct trajectory.

#### The zero-randomization limit changes the process

Let $`S=3`$ and start at state one. For positive ε,

```math
E_3(\varepsilon)=\frac{1+\varepsilon}{5+2\varepsilon}.
```

At $`\varepsilon=0`$, both endpoints become absorbing. The first acquisition moves from state one to an endpoint and determines the permanent response. The error probability is then 1/3 under either hypothesis. At every fixed $`n\ge1`$, the finite-step law is a polynomial in the transition entries, so its error $`e_n(\varepsilon)`$ converges to $`e_n(0)=1/3`$ as $`\varepsilon\downarrow0`$. Therefore

```math
\lim_{\varepsilon\downarrow0}\lim_{n\to\infty}e_n(\varepsilon)
=\frac15,
\qquad
\lim_{n\to\infty}\lim_{\varepsilon\downarrow0}e_n(\varepsilon)
=\frac13.
```

The restoration probability changes as well: it is zero for every positive ε, but 2/3 at zero. Removing a positive transition changes recurrent classes. Approaching an error infimum therefore does not justify setting a parameter to zero while retaining the old qualitative conclusion.

The classical finite-memory learning criterion is an asymptotic average error. For equal-prior, time-invariant randomized *S*-state tests of Bernoulli parameters $`0<q<p<1`$, the Hellman–Cover infimum is expressed using $`\gamma=p(1-q)/(q(1-p))`$ as $`(1+\gamma^{(S-1)/2})^{-1}`$. Berg, Ordentlich and Shayevitz state that criterion and the randomized infimum explicitly while studying deterministic machines. Here $`\gamma=4`$, matching the limit of the displayed family. The universal optimality assertion belongs to that literature; the calculation above proves this family's law and temporal behavior. [29][memory-origin]; [30, §I][memory-learning].

A vanishing instantaneous error is also insufficient by itself: the harmonic error example in §7.4 has errors tending to zero but infinitely many errors almost surely. The majority construction instead has summable update errors. Conversely, the recovery example in §7.7 shows that finitely many bad visits almost surely need not have finite expected total. Average accuracy, convergence in probability, eventual correctness, expected error count and a finite zero-error declaration must therefore retain their separate definitions.

### 7.10 Fresh switching innovations impose an irreducible conditional risk

An unbounded tally can learn a fixed source frequency. It cannot predict a fresh, unobserved change after its current action has been selected. Let a binary standard evolve by

```math
h_t=h_{t-1}\mathbin{\oplus}B_t,
\qquad t\ge0,
```

where $`\oplus`$ denotes exclusive-or and h<sub>−1</sub> is known. Before issuing *a*<sub>*t*</sub>, the controller sees h<sub>t−1</sub> exactly but not *B*<sub>*t*</sub>. Correctness means $`a_t=h_t`$. Both responses are initially stipulated safe and permitted under either next standard. [28][r20]

Let $`\mathcal F_t`$ include the entire past, the selected action *a*<sub>*t*</sub>, and all randomness used to select it. The innovation is not yet observed. Assume

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

If the prescribed sum diverges, the adapted conditional theorem of §7.4 gives infinitely many mistakes almost surely for every admitted policy, including randomized policies with unbounded memory. If the sum converges, choose $`a_t=h_{t-1}`$. A mistake then occurs exactly when $`B_t=1`$. Its probabilities have finite sum, so the first Borel–Cantelli implication gives only finitely many mistakes. The policy needs only the last observed standard; it need not store the schedule or know the current value of *p*<sub>*t*</sub>. The environment's potentially time-dependent hazard law remains an explicit premise. ∎

If the risks are instead endogenous or policy-dependent, the conditional lower-bound argument still applies on paths with divergent cumulative conditional risk. The deterministic-schedule existence equivalence does not prove that a greedy current predictor minimizes future endogenous risk.

Several sharp changes of assumption locate this theorem's scope.

**Persistent support uncertainty.** If $`0<p_t\le1/2`$ at every time, both next standards remain possible at every decision. No single response keeps every supported successor in the target. Thus there is no nonempty support-invariant target core for this response model and information timing. A summable positive schedule nonetheless permits eventual correctness almost surely. The support adversary can choose a contrary innovation at every step; almost-sure success is not sure success.

**Earlier observation.** If the current *h*<sub>*t*</sub> is revealed before selection, $`a_t=h_t`$ is always correct. That conclusion belongs to an enlarged information channel.

**Copied rather than fresh innovations.** Draw one bit $`Z\sim{\rm Bernoulli}(\varepsilon)`$, with $`0<\varepsilon<1/2`$, and put $`B_t=Z`$ for every time. Each unconditional flip marginal is still ε. After the first transition, the controller learns $`Z=h_0\oplus h_{-1}`$ and selects

```math
a_t=h_{t-1}\mathbin{\oplus}Z
\qquad(t\ge1).
```

Every later response is correct. The conditional **flip probability** is now the known value $`\Pr(B_t=1\mid\mathcal F_t)=Z`$, whereas the chosen policy's conditional **error probability** is zero. These are different quantities. Summing the unchanged unconditional flip marginals would falsely invoke the fresh-innovation theorem.

**Eligibility tied to the new standard.** If response *a* is permitted only when $`a=h_t`$, both alternatives remain possible whenever $`0<p_t<1`$. Neither binary response is then eligible under every supported standard. A statistical predictor is not an authorized restoration policy merely because its expected errors are small. If such uncertainty persists and only an always-permitted, nontarget abstention is available, permitted eventual correctness fails. If uncertainty ceases, that separate eventual situation must be analyzed under its actual menu.

The hypotheses about standards, acquisition laws, target meanings and permissions are not observations established by these calculations. The results identify which memory and information contracts can support the specified objective, while leaving empirical identification and substantive cognitive or normative authority to their own evidence.

### 7.11 Controlled observations and eventual correctness

In §7.8, observations arrive without requiring an incorrect response. An inquiry can have a different structure: an action determines which observation is acquired, and the informative action may itself violate the target. Identifiability under unlimited experimentation then need not yield eventual permanent correctness. The following finite model characterizes when the available good actions can sustain the necessary discrimination. [32]

#### Fixed models, acquired histories and good action sets

Let Θ,A,Y be nonempty finite sets of fixed hidden models, actions and observations. For each $`\theta\in\Theta`$ and $`a\in A`$, a supplied probability vector satisfies

```math
P_{\theta,a}(y)>0,\qquad
\sum_{y\in Y}P_{\theta,a}(y)=1.
```

The true model is chosen once. An action is issued before its observation. Conditional on the complete acquired history, the controller's private seed and the chosen action *a*<sub>*t*</sub>, the next observation has law $`P_{\theta,a_t}`$. This is a condition on fresh acquisitions. Equal one-time marginals of copied observations do not satisfy it.

A controller has one common probability space (Z,ρ) for its private seed and one measurable policy

```math
\pi:Z\times(A\times Y)^*\longrightarrow A.
```

At time *t* it issues $`a_t=\pi(z,h_t)`$, where $`h_t=((a_0,y_0),\ldots,(a_{t-1},y_{t-1}))`$. The seed is independent of the fresh feedback sources, and neither its law nor the policy depends on the true model. Memory is unrestricted. The length of the history supplies the time index, so no time-homogeneity assumption is imposed.

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

A nonempty set *U* is **self-verifying for the target at θ** when

```math
U\subseteq G_\theta,
\qquad
U\subseteq G_\lambda\quad
       \text{for every }\lambda\in E_\theta(U).
```

Thus a rival that rejects any action in *U* must differ observationally on some action in *U*. The rival need not be identifiable if it accepts the whole set. Here “self-verifying” describes a property of the supplied finite model; it does not mean that the controller issues a finite certificate that its current actions are correct.

**Theorem (controlled-observation restoration).** One common seeded history policy restores almost surely under every model if and only if each model has a nonempty self-verifying target set. Whenever the condition holds, a deterministic history policy suffices. [32–33]

#### Necessity: transferring a recurrent set without stopping at its last exit

Suppose a common policy restores. Under a fixed true model θ, let U<sub>∞</sub> be the actions used infinitely often. Finiteness of *A* makes U<sub>∞</sub> nonempty on every infinite action sequence. Restoration implies $`U_\infty\subseteq G_\theta`$ almost surely. There are only finitely many possible recurrent sets, so some nonempty $`U\subseteq G_\theta`$ occurs with positive probability. On that event, each action outside *U* occurs only finitely often. Consequently, for some deterministic *N*,

```math
F(U,N)=\{a_t\in U\text{ for all }t\ge N,
          \text{ and every }a\in U\text{ recurs infinitely often}\}
```

has positive $`\Pr_\theta^\pi`$ probability. No last-exit time is assumed to be a stopping time.

Fix $`\lambda\in E_\theta(U)`$. Include the private seed in the length-*N* prefix. For a finite history $`h=((a_s,y_s))_{s<N}`$, its joint law with the seed has the explicit form

```math
\rho(dz)
\prod_{s\lt{}N}
 \mathbf 1\{a_s=\pi(z,h_s)\}
 P_{\theta,a_s}(y_s).
```

The indicator factors are identical under the two models, and every observation factor is strictly positive. Hence their seed-and-prefix laws are mutually absolutely continuous. On the part associated with a compatible history *h*, the density ratio is the positive finite number

```math
\prod_{s\lt{}N}
 \frac{P_{\theta,a_s}(y_s)}{P_{\lambda,a_s}(y_s)}.
```

After a seed and prefix have been fixed, send the process to a common absorbing cemetery state at its first subsequent action outside *U*. The continuation kernels of these killed processes coincide: their policy is the same, and all observation laws for actions in *U* agree. Equality on finite cylinders gives equality of their continuation laws. In particular, they assign the same conditional continuation probability to staying in *U* forever and visiting each member infinitely often.

Integrating that common nonnegative continuation probability against the two equivalent prefix measures transfers positivity of $`F(U,N)`$ to model λ. If some $`a\in U`$ were outside G<sub>λ</sub>, this event would contain infinitely many errors under λ, contradicting restoration. Thus $`U\subseteq G_\lambda`$ for every $`\lambda\in E_\theta(U)`$. This proves necessity for the fixed θ, and then for every model. Keeping the common seed in the prefix also proves the claim for seeded randomization without presuming a general policy-realization theorem. $`\square`$

**Why the private-seed rule has a common behavioral form.** The ordinary
source review [53] also describes the reduction from a common private seed
to a common distribution of next actions at each fully observed history.
In this finite, full-support model the reduction can be proved directly,
without a general disintegration theorem.

For a finite history $`h=((a_s,y_s))_{s\lt{}N}`$, let

```math
C_h=\{z:\pi(z,h_s)=a_s\text{ for every }s\lt{}N\},
\qquad
\ell_\theta(h)=\prod_{s\lt{}N}P_{\theta,a_s}(y_s).
```

The joint-prefix formula just used says
$`\Pr_\theta(z\in D,h)=\rho(D\cap C_h)\ell_\theta(h)`$
for every measurable seed set $`D`$. The likelihood factor is constant
over the compatible seeds. If $`\rho(C_h)>0`$, it is positive under every
model, and cancellation gives

```math
\Pr_\theta(z\in D\mid h)
 =\frac{\rho(D\cap C_h)}{\rho(C_h)},\qquad
\kappa(a\mid h)
 =\frac{\rho(C_h\cap\{z:\pi(z,h)=a\})}{\rho(C_h)}.
```

Neither expression depends on the true model. For
$`\rho(C_h)=0`$, the history has probability zero under every model;
choose any fixed distribution $`\kappa(\,\cdot\,\mid h)`$ there. The
action alphabet is finite, so these expressions give a probability
vector at every history. Induction on history length shows that
sampling each next action from this vector, followed by its stipulated
fresh observation, reproduces all finite action/observation-history
laws of the seeded policy. The equality extends to their generated
infinite-history laws.

The result concerns the law of the observed interaction, not identity
of private seeds or internal state. It uses the full remembered history
including the controller's own actions, a parameter-independent seed
law and the stated conditional observation law. A parameter-correlated
seed or omitted private feedback would invalidate the factorization.
The construction gives neither a bounded-memory implementation nor
advance access to the current action's observation. The broader
continuous-space obstruction below keeps its own explicit common
measurable policy and continuation-kernel assumptions.

<a id="conditional-seed-feedback-product"></a>

The product-source refinement separates two facts about restarting a seeded policy. For a fixed positive acquired history h, its input event is the rectangle C_h×F_h of compatible private seeds and compatible feedback. Normalized restriction of the original independent product therefore factors as

```math
(\rho\otimes\nu)(\,\cdot\mid C_h\times F_h)
 =\rho(\,\cdot\mid C_h)\otimes\nu(\,\cdot\mid F_h).
```

The identity follows by evaluating measurable rectangles and cancelling the two positive finite normalizing masses. The seed factor is the common residual seed already derived above; positivity of each compared prefix suffices for this cancellation even if unrelated rows contain zeros. This observation does not remove the full-support premise from the restoration necessity theorem. In the source's normalized-restriction convention an impossible prefix gives the zero measure, not a probability posterior. [Q250E-153] [Q250E-141]

Every measurable function of the feedback, including the shifted unused row-oracle tail, consequently remains independent of the residual seed under that conditional input law. Its marginal in `posterior_seed_unused_tail_product` is explicitly the pushforward of **conditioned feedback**. The theorem does not itself identify that marginal with a fresh iid oracle. Fresh-tail identification and equality with the restarted policy's original history law are further distributional steps; conditional product structure alone cannot replace them. This is a distinction between two probability identities, not an additional independence assumption imposed on the observed action count. [Q250E-141]

[Q250E-153]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9608772a6948c3dfb69d95659d27b5f6b961aece08ccc09afc594b63cd264ba6/ResidualSeedPosterior.lean
[Q250E-141]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0f37e47723087f1ad72667012a3abac927ae29162a14625cc58dfae754346115/PosteriorFeedbackProduct.lean

#### A constructive policy with the correct physical clock

Choose one nonempty self-verifying set U<sub>λ</sub> for each candidate λ, and fix an ordering of its elements. Its ordered list is a plan. At a completed-plan boundary, compute the acquired likelihood

```math
L_t(\lambda)=\prod_{s\lt{}t}P_{\lambda,a_s}(y_s),
```

choose a maximizing candidate using a fixed tie rule, and load its plan. Execute one action at a time until that plan is empty, acquiring and recording fresh feedback after every action. Then choose a new maximizing candidate from the enlarged history. A change of likelihood ranking during a plan does not cancel its remaining actions. [33]

This is a history policy, including on histories it would not itself generate. Start its queue at the plan chosen from the empty likelihood record. Upon appending any action/observation pair, remove one queue element; if the queue becomes empty, refill it using the likelihood of the enlarged record. On actual histories, the recorded action is the queue head. On arbitrary histories, the same recursion still defines a nonempty queue. Every plan is nonempty and finite, so the policy always has an action and never needs an arbitrary empty-queue default.

For the probability argument, fix θ and take independent stacks $`(Y_{a,k})_{k\ge1}`$ with law P<sub>θ,a</sub>, one stack for each action. On its *k*th use, action *a* consumes Y<sub>a,k</sub>. The controller accesses no unused coordinate. Induction on acquired histories shows that each consistent finite history has exactly the product probability prescribed by the controlled-observation model: each new coordinate is independent of those already acquired and has the required action law. Thus this stack construction generates the actual policy law, rather than a different law whose good behavior is merely assumed to transfer. The general probability-law comparison in §§7.5–7.6 retains its broader scope.

Let $`N_a(t)`$ count uses of action *a* before time *t*. The acquired likelihood satisfies the exact identity

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

This finite-alphabet strong law follows by applying the indicator argument in §7.8 to each symbol. All log increments are bounded because the alphabets are finite and the probabilities are positive. Jensen's inequality for the strictly concave logarithm gives $`D_{\theta,\lambda}(a)\ge0`$, with equality exactly when the two probability vectors agree: apply it to $`P_{\lambda,a}(y)/P_{\theta,a}(y)`$, whose P<sub>θ,a</sub>-weighted mean is one.

Work on the probability-one intersection of these finitely many strong-law events. For every informative action, a sufficiently long stack-prefix sum is at least half its positive mean times its length. An action sampled finitely often contributes an eventually fixed finite amount; a noninformative action contributes zero. It follows that the total log ratio tends to positive infinity whenever at least one distinguishing action is sampled infinitely often. This reasoning uses complete stack-prefix limits and then evaluates them at the actual counts; it does not assume that adaptively selected observations form an unconditioned random subsequence.

Call a candidate λ harmful under θ if $`U_\lambda\nsubseteq G_\theta`$. Self-verification of U<sub>λ</sub> implies that some $`b\in U_\lambda`$ distinguishes λ from θ: otherwise $`\theta\in E_\lambda(U_\lambda)`$ would require $`U_\lambda\subseteq G_\theta`$. If this harmful candidate were selected at infinitely many plan boundaries, every action in its plan, including *b*, would be executed infinitely often. The log ratio above would then tend to positive infinity. Eventually $`L_t(\theta)>L_t(\lambda)`$, so λ could no longer maximize likelihood at a boundary. This is a contradiction.

Only finitely many harmful candidates exist, and each is chosen for finitely many plans almost surely. If *T*<sub>*j*</sub> is the start of plan *j*, then

```math
T_0=0,\qquad
T_{j+1}=T_j+|U_{\lambda_j}|,
\qquad 1\le |U_{\lambda_j}|\le |A|.
```

These intervals cover physical time and their endpoints tend to infinity. After the finitely many harmful plans have finished, every actual action belongs to G<sub>θ</sub>. The physical cutoff is the sum of the preceding plan lengths, not the number of plans. The same deterministic queue policy works under every true model, completing the sufficiency proof. $`\square`$

The earlier construction selects a likelihood maximizer after every action and keeps a separate persistent cyclic pointer through each candidate's set. It is another valid policy: infinitely many selections of a harmful candidate again force every member of its cycle to be used infinitely often, and the same likelihood contradiction applies. Its persistent pointers must not be replaced by restarting the chosen plan at each action. The block policy just proved is the one realized by the later physical-history construction; the two algorithms are not claimed to have identical action laws. [32–33]

#### The greatest good set and a finite decision procedure

The union of two self-verifying sets for θ is self-verifying. A rival agreeing on the union agrees on each set and therefore accepts both. There is consequently a unique greatest such set, with the empty set used when none exists. It can be found without enumerating all subsets.

Start with $`U_0=G_\theta`$ and iterate

```math
U_{k+1}
 =U_k\cap\bigcap_{\lambda\in E_\theta(U_k)}G_\lambda.
```

The operation is contracting and monotone. If $`V\subseteq U`$, then $`E_\theta(U)\subseteq E_\theta(V)`$; hence every member surviving the intersection for *V* also survives it for *U*. Any self-verifying $`V\subseteq G_\theta`$ remains in every iterate: a rival agreeing on *U*<sub>*k*</sub> agrees on *V* and accepts all its actions. After at most $`|G_\theta|`$ strict deletions, the sequence stabilizes at a set K<sub>θ</sub>. A nonempty fixed point satisfies precisely the self-verification condition, and the preceding inclusion shows that it contains every other self-verifying set. Therefore

```math
\text{common almost-sure restoration exists}
\quad\Longleftrightarrow\quad
K_\theta\ne\varnothing\text{ for every }\theta.
```

Each deletion has a finite witness: a rival that agrees on every currently retained action but rejects the deleted action. The witnesses must be checked at their actual elimination stages. For $`n=|\Theta|`$, $`m=|A|`$ and $`d=|Y|`$, direct repeated rational-vector comparison takes $`O(n^2m^2d)`$ rational comparisons over all models. This counts comparisons of supplied exact probabilities, not bit operations, acquisition costs or authentication work. For arbitrary real inputs, exact equality and likelihood comparison remain mathematical operations; no general effective procedure for presenting such reals is assumed.

Two rounds can be essential. In the following table, entries are the probabilities of observing one, with $`Y=\{0,1\}`$:

| Model | G<sub>θ</sub> | Action *a* | Action *b* |
|---|---|---:|---:|
| 0 | $`\{a,b\}`$ | 1/2 | 1/2 |
| 1 | $`\{a\}`$ | 1/2 | 1/2 |
| 2 | $`\{b\}`$ | 1/2 | 2/3 |

For model zero, the first step removes *b* because model one agrees on both actions and rejects *b*. Once only *a* remains, model two also becomes indistinguishable and removes *a*. Thus $`U_0=\{a,b\}`$, $`U_1=\{a\}`$, $`U_2=\varnothing`$. A single filtering pass would return a false positive.

Three monotonicity statements follow directly from valid-set inclusion. Adding rival models can only shrink an old model's greatest set. Enlarging all target sets can only enlarge these sets. Applying a common observation garbling at each action preserves old equalities of observation laws and can add new equalities, so it can only shrink the greatest sets. The restoration interpretation of the last statement requires the garbled model to retain the theorem's stated observation hypotheses. None of these order statements selects the true target or establishes its authority. [32]

#### A fixed permission menu

Let $`\Gamma\subseteq A`$ be a supplied common static menu. Require $`\pi(z,h)\in\Gamma`$ for every seed and every finite history, including histories the policy never generates. Such a policy with almost-sure restoration under every model exists exactly when the greatest-set calculation for the restricted targets

```math
G_\theta^{\Gamma}=G_\theta\cap\Gamma
```

is nonempty for every model. [33]

For necessity, all-time menu membership and eventual target membership imply eventual membership in $`G_\theta^\Gamma`$, so the theorem applies. For sufficiency, use its nonempty greatest sets as the queue plans. Every initial plan and every replacement plan lies in Γ, and every residual queue is a nonempty suffix of such a plan. Induction on arbitrary finite histories proves that every issued action is in Γ. This includes malformed histories containing earlier actions outside the menu. The queue never empties at a decision, so an out-of-menu fallback value cannot be used. Eventual membership in the restricted target implies eventual membership in the original target.

If Γ is empty or some target misses it, no such policy exists. Early target errors may still be permitted; eventual correctness alone does not establish all-time permission. The result concerns a fixed common menu. History-dependent or model-dependent permissions require another analysis, and no statistical concentration result authenticates the menu's authority.

#### Positive and negative cases

**Information available only through bad actions.** Take two models, actions r<sub>0</sub>,r<sub>1</sub>,q, and $`G_0=\{r_0\}`$, $`G_1=\{r_1\}`$. Both repair actions emit a fair bit under either model. The probe *q* emits a Bernoulli bit of parameter 1/3 under zero and 2/3 under one. All actions are permitted, but *q* is target-bad under both models. Neither singleton target is self-verifying, so no common almost-surely restorative policy exists, even with unrestricted memory and adaptive probing.

Nevertheless, for any $`\delta>0`$, take $`2m`$ probe samples and commit to their majority, with *m* chosen so that $`(8/9)^m\le\delta`$. The already proved calculation in §7.8 gives restoration probability at least $`1-\delta`$ under both models. Only finitely many probe actions occur, but a wrong commitment makes infinitely many subsequent errors. Arbitrarily high finite-confidence success is different from one probability-one guarantee. Infinite probing identifies the model almost surely and fails restoration because the probes remain bad. [32]

**Good actions that sustain discrimination.** If both *r*<sub>0</sub> and *r*<sub>1</sub> instead have different positive observation laws under the two models, each singleton target becomes self-verifying. The constructive policy restores while continuing to acquire information through its eventual good actions. If only *r*<sub>0</sub> is informative while *r*<sub>1</sub> remains indistinguishable, only the first target has a valid set; there is still no policy restoring under both. The quantifier over every possible true model is essential.

**Correct decisions without exact identification.** If two models have identical observation laws at every action but both accept *c*, the constant policy *c* restores under both. Their disagreement about other actions and their unidentified model labels do not obstruct this decision. Conversely, identical complete observation laws and disjoint target sets give empty greatest sets, even though each model individually admits a successful constant action.

**Why a plan cannot be restarted after every observation.** Let $`G_0=\{a,b\}`$ and $`G_1=\{c\}`$. At *a* both models emit a fair bit; at each of b,c they emit Bernoulli bits with respective parameters $`1/3,2/3`$. Both target sets are self-verifying. Choose model zero in a likelihood tie and order its plan as (a,b). A rule that recomputes a maximizer after every action and always restarts its plan chooses *a* forever: those observations never break the tie. It therefore fails under model one. The queue executes *b* before replanning, and the persistent-pointer alternative also eventually reaches *b*. Their proofs rely on those actual actions, not just the existence of an informative member in an unexecuted plan.

**Freshness and permissions remain separate.** Copying one biased root bit forever retains the same one-time marginals but violates the conditional fresh-observation premise; the common positive-probability report words give the impossibility proved in §7.8. Likewise, if only a universally licensed abstention survives the common menu and it belongs to neither target, restricting the targets to that menu yields empty greatest sets. Neither many repeated reports nor a high likelihood supplies a missing acquisition or permission.

**Zero probabilities change the criterion.** Keep the opposing singleton targets and uninformative repair actions in the first example, but make *q* reveal the true model exactly. One probe followed by the corresponding repair restores surely. The singleton good sets still fail the equality-based condition, because their own observation laws agree. The finite-prefix absolute-continuity premise has now failed: the probe has disjoint outcome supports. This is a counterexample to extending the stated necessity beyond its full-support domain; separate constructive results with zero probabilities do not establish the same unrestricted equivalence.

#### A general obstruction after informative probing ends

The deterministic-prefix argument has a useful extension beyond finite action spaces. Fix two models on common standard Borel action, observation and controller-record spaces. Fix one common measurable causal policy, including its randomization, and the corresponding regular continuation kernels. The record contains the acquired history and all private state needed for future policy behavior; its update rule and future randomization kernels are common. Let *R* be a measurable class of nonprobe actions. Assume that the controlled observation kernels agree under both models whenever an action in *R* is chosen at a common record. Assume also that their complete finite-prefix laws are mutually absolutely continuous. Finally, let B<sub>θ</sub>,B<sub>λ</sub> be disjoint measurable successful-tail events, each of which entails that only finitely many actions fall outside *R*. Then no common policy has probability-one success under both models. [32, §4]

To prove this, suppose $`\Pr_\theta^\pi(B_\theta)=1`$. For some deterministic *N*,

```math
\Pr_\theta^\pi
 \bigl(B_\theta\cap\{a_t\in R\text{ for all }t\ge N\}\bigr)>0.
```

Let $`\mu_\theta^N,\mu_\lambda^N`$ be the prefix laws. Kill the future process on leaving *R*. Equality of the common policy and nonprobe kernels gives one measurable subprobability continuation kernel *Q*<sub>*N*</sub> under both models. For the indicated full-path event, including its prefix-dependent success condition, its probabilities are

```math
\int Q_N(h,B_\theta)\,\mu_\theta^N(dh)
\quad\text{and}\quad
\int Q_N(h,B_\theta)\,\mu_\lambda^N(dh).
```

The first is positive, and $`\mu_\theta^N\ll\mu_\lambda^N`$ makes the second positive. The transferred paths lie outside B<sub>λ</sub>, contradicting probability-one success there. Standard Borel spaces and the specified common continuation kernels make the disintegration and measurable-kernel statement meaningful; equivalent finite prefixes by themselves do not make arbitrary infinite-tail laws equivalent. No conditioning on the final probe is used. $`\square`$

An independently proved fact that increasingly accurate repair sequences encode the hidden norm can supply the disjoint success events in this proposition. The proposition does not establish that geometric encoding or authenticate the norm-to-observation relation. It also does not exclude a finite-confidence rule, a singular revealing probe, or continued informative target-good behavior, all of which alter its premises.

Controlled testing and robust policies have substantial antecedents. Bovy and collaborators study one policy under a fixed but unknown member of a finite family of partially observed models, with finite-horizon and discounted reward criteria and linear-program constructions. [34] Kaufmann, Cappé and Garivier give an adaptive bandit change-of-measure inequality at an almost-surely finite stopping time. [35, Lemma 1] Those settings help locate the present comparison; the last informative probe is not automatically a stopping time to which that lemma applies. The qualitative target-dependent criterion here also retains the distinction from the common observed-state parity objective discussed in §7.8. No historical priority claim follows.

The finite greatest-set test and the infinite-time policy theorem answer different computational questions. The policy uses growing acquired likelihoods; it supplies no general finite-memory bound, deterministic last-error time, finite zero-error declaration, expected physical error budget or arbitrary-real implementation. In particular, the historical finite enumeration and formal implementation evidence retain their own source and execution boundaries. The mathematical result concerns the stated observation laws, targets and permissions; empirical truth, normative warrant and the unfinished broader account of collective inquiry require their own arguments.

### 7.12 Recursive restoration with zero observation probabilities

An observation of zero probability under a candidate can remove that candidate altogether. The actions permitted after this elimination may differ from those permitted before it. A useful controller must therefore preserve the observation that caused the change, interrupt an obsolete plan immediately, and account for the action that produced that observation. A recursive certificate supplies these obligations and a finite expected error budget. Its constructive proof uses the original probabilities of continuing observations; conditioning on continued survival would remove part of the information. [36–38]

#### The model and the recursive certificate

Let Θ,A,Y be nonempty finite sets of fixed hidden models, actions and observations. For every θ,a, the supplied law satisfies

```math
P_{\theta,a}(y)\ge0,\qquad
\sum_{y\in Y}P_{\theta,a}(y)=1.
```

An action is chosen before its observation. Conditional on the entire acquired history, the controller's private seed and the current action, the next observation has this fixed law. Thus the observations are fresh controlled acquisitions. Their laws may have zeros. Targets $`G_\theta\subseteq A`$ are fixed. A public menu $`\Gamma(B)\subseteq A`$ is supplied for each live model support $`B\subseteq\Theta`$; it may change nonmonotonically as the support shrinks. These probability, target and permission premises remain distinct.

For an action and its observed symbol, put

```math
B[a,y]=\{\eta\in B:P_{\eta,a}(y)>0\}.
```

Starting from a nonempty *B*<sub>0</sub>, a finite history determines its support by these successive updates. Call the history **feasible** when its resulting support is nonempty. It is **action-consistent** with a policy when every recorded action equals the policy's action at the preceding record. Legality will be required at every feasible action-consistent history, for every seed. It is not a claim about invented action fields or histories impossible under every initially live model.

Define a recursive certificate $`W(B)`$ by induction on $`|B|`$. The empty support is not certified. For nonempty *B*, each candidate $`\sigma\in B`$ must have a nonempty finite ordered action list v<sub>B,σ</sub> satisfying three requirements:

1. Every action in the list belongs to $`\Gamma(B)`$.
2. For every listed action *a* and every symbol *y*, if $`B[a,y]`$ is nonempty and strictly smaller than *B*, then $`W(B[a,y])`$ holds.
3. Either the list has a **progress witness**—some listed *a* and *y* with $`P_{\sigma,a}(y)>0`$ and $`B[a,y]\ne B`$—or it is **self-verifying among the live models**:

```math
\{a:a\text{ occurs in }v_{B,\sigma}\}\subseteq G_\sigma,
```

and every $`\eta\in B`$ whose full observation vectors agree with σ at every listed action accepts every action in the list.

The recursion refers only to smaller nonempty supports. A symbol impossible under every live model produces the empty set and does not require a certificate. The definition contains no successful-policy premise. Its universal continuation condition is stronger than finding one favorable exit. Action order and repeated occurrences will matter to the controller and its cost, even though acceptance and licensing depend only on which actions occur. [36]

There is also a finite bottom-up test for this definition. After deciding smaller supports, retain precisely those actions in $`\Gamma(B)`$ for which every nonempty strict successor is certified. For each $`\sigma\in B`$, require either an available progress witness or a nonempty available action set that is self-verifying among *B*. This is equivalent to the list definition: a progress witness gives a singleton list; a self-verifying set can be listed in any fixed order. Conversely, each certified list supplies its progress witness or its underlying self-verifying set, and all its actions survive the continuation test. This is a combinatorial equivalence, without a policy-necessity conclusion. Equality and positivity of supplied exact probabilities are required operations; no general algorithm for comparing arbitrary represented real numbers follows. [36]

For the self-verifying branch of this bottom-up test, let $`A_B`$
be the retained licensed actions after checking all strict successors.
Apply the greatest-set deletion calculation of §7.11 with rival
family $`B`$ and starting set $`G_\sigma\cap A_B`$. Its proof is
combinatorial: every self-verifying subset survives each contracting
iterate, and the final fixed point is itself self-verifying when
nonempty. It uses equality of supplied observation vectors, not
positivity of every symbol. Thus zero probabilities do not invalidate
this greatest-kernel subroutine. They do change the stochastic
necessity argument, which additionally needs the recursive exits
treated in §7.13. This is the explicit greatest-kernel step requested
by the support-elimination review [53].

#### One policy, with immediate interruption

Choose one witnessing list for every certified support and every live candidate, with a fixed tie rule. This is a finite collection of finite choices. At entry to a support *B*, reset the within-phase likelihoods to one. At each completed-plan boundary, choose a live candidate maximizing the likelihood of the observations acquired since this phase began, and load its list. During a plan, retain the remaining suffix rather than recomputing the plan after each observation.

After issuing each action *a* and acquiring *y*, perform the exact support update. If the support remains *B*, retain the acquired observation and continue the suffix. If it changes, preserve the action and observation in the public history, abandon the entire remaining suffix, enter $`B[a,y]`$, and reset the within-phase likelihoods there. A completed plan with unchanged support is followed by a new likelihood choice. Resetting a likelihood calculation does not erase the public record used to establish the new support or count physical actions.

The rule uses the supplied laws and acquired observations; it does not take the hidden true model as an input. It defines a deterministic history policy. It can ignore an arbitrary common private seed, so its existence holds for every common seed distribution. To make the policy total, give a fixed default response at infeasible or action-inconsistent records. The legality theorem does not cover those records; this choice of totalization need not match a source implementation's particular behavior there.

On every feasible consistent history, induction shows that the current support is certified. Continuing observations preserve the support and its licensed suffix; a strict nonempty successor is certified by requirement 2 and receives a new licensed plan. Every issued action therefore belongs to the current menu. Under a true $`\theta\in B_0`$, the next symbol has positive P<sub>θ,a</sub> probability almost surely, so the support retains θ at every time outside a single null event. Every strict change then lowers $`|B|-1`$, allowing at most $`|B_0|-1`$ changes.

This is a policy in the stated physical experiment. The probability of any consistent finite acquired history under θ is the product of its selected-action observation probabilities, obtained by induction from the conditional acquisition law. On an exit, that product includes the exit-triggering symbol; it is neither discarded nor renormalized. Finite-history probabilities determine the law on infinite histories. No extra law-equality or independent policy-realization premise is supplied. [37–38]

There are two invariants in this argument. A decreasing analysis rank
bounds how often phases can change; it does not alone prevent a removed
model from reappearing. For example, ranks $`2,1,0`$ and live sets
$`\{\theta,\lambda\},\{\theta,\eta\},\{\theta,\lambda\}`$ preserve the
true model and strictly decrease rank while reintroducing
$`\lambda`$. The actual update $`B[a,y]\subseteq B`$ rules this out:
induction makes every later support a subset of every earlier one.
Together with positive-probability retention of $`\theta`$, it gives
the support persistence used by the recursive proof. This is the
additional premise identified by the earlier generic-controller review
[53]. It says nothing about inclusion between permission menus:
$`\Gamma(B[a,y])`$ may differ nonmonotonically from $`\Gamma(B)`$,
which is why an exit must interrupt the old plan.

#### A survival-affinity estimate

Fix a certified support *B* and a live true model θ. For an action *a*, let

```math
S_B(a)=\{y:B[a,y]=B\},\qquad
\alpha_{B;\theta,\sigma}(a)=
 \sum_{y\in S_B(a)}
   \sqrt{P_{\theta,a}(y)P_{\sigma,a}(y)}.
```

For an ordered list $`v=(a_1,\ldots,a_\ell)`$, put

```math
c_{B;\theta,\sigma}(v)
 =\prod_{i=1}^{\ell}\alpha_{B;\theta,\sigma}(a_i).
```

This is the affinity of the two subprobability laws for completing the whole list without changing support. Each factor lies in $`[0,1]`$ by Cauchy–Schwarz and normalization. The full-row affinity equals one only when the two probability vectors agree: equality in Cauchy–Schwarz makes their square-root vectors proportional, and their unit norms make them equal.

Let $`b_{B,\theta}(\sigma)`$ be the number of occurrences in v<sub>B,σ</sub> that are outside G<sub>θ</sub>, counting multiplicity. If this number is positive, then

```math
c_{B;\theta,\sigma}(v_{B,\sigma})\lt{}1.
```

Indeed, suppose the certificate uses a progress witness at a listed action. Some positive σ probability lies outside $`S_B(a)`$, so the mass of its restricted row is strictly less than one. Cauchy–Schwarz then makes that action's affinity strictly less than one, and the entire product is strictly less than one. If the certificate instead uses self-verification, a plan containing an action bad under the live θ cannot have identical observation vectors under σ and θ at every listed action. At a differing action the full-row affinity is strictly less than one, hence so is the restricted affinity and the product.

The argument retains both possible sources of a strict deficit: distinguishable continuing laws and positive probability of leaving the support. It remains valid when some probabilities vanish. [37]

#### Finite expected error count in one phase

Until the first strict support change, let $`L_j(\eta)`$ denote the likelihood under a live model η of the acquired history at the start of plan *j*. Only completed continuing plans precede such a boundary. Their symbols have positive probability under every live model, so all these likelihoods are strictly positive.

For a fixed candidate σ, define

```math
R_j^\sigma=
 \mathbf 1\{\text{the phase is still active at boundary }j\}
 \sqrt{\frac{L_j(\sigma)}{L_j(\theta)}}.
```

After the phase exits, set this potential to zero forever. At its initial boundary it equals one. Given an active boundary and the chosen list *v*, summing over all complete continuing symbol strings gives the exact conditional identity

```math
\mathbb E_\theta[R_{j+1}^\sigma\mid\mathcal F_j]
 =R_j^\sigma\,c_{B;\theta,\sigma}(v).
```

For an exiting observation string the next potential is zero. For a continuing string, its true-model probability multiplies the square root of the likelihood ratio, producing the product of the square-root probability factors. Summing over its symbols yields the displayed product affinity. This calculation uses the unnormalized continuing mass. It does not condition the experiment on future survival.

For the candidate's own plan, abbreviate $`c_\sigma=c_{B;\theta,\sigma}(v_{B,\sigma})`$. If $`b_{B,\theta}(\sigma)>0`$, set $`\delta_\sigma=1-c_\sigma>0`$. Every other chosen plan has affinity at most one. When the chosen candidate is σ, likelihood maximization gives $`L_j(\sigma)\ge L_j(\theta)`$ and hence $`R_j^\sigma\ge1`$. Therefore

```math
\mathbb E_\theta R_{j+1}^\sigma
 \le \mathbb E_\theta R_j^\sigma
  -\delta_\sigma
      \Pr_\theta(\text{candidate }\sigma
                     \text{ is selected at boundary }j).
```

Telescope this inequality from the initial value one, retain the nonnegative terminal potential, and let the finite horizon grow. The expected number of selections of this candidate during the phase is at most $`1/\delta_\sigma`$.

A stopped execution of a plan incurs at most its full planned number of bad occurrences, including the action that triggered exit. Consequently the expected number of actual bad actions before the phase ends is bounded by

```math
C_{B,\theta}
 =\sum_{\substack{\sigma\in B\\ b_{B,\theta}(\sigma)>0}}
   \frac{b_{B,\theta}(\sigma)}
        {1-c_{B;\theta,\sigma}(v_{B,\sigma})}
 \lt{}\infty.
```

The direction of this charge comparison matters [53]. Saying that a
positive charge implies a bad planned block would still permit assigning
zero charge to every block. It would give no bound on executed errors.
Here the charge is instead the number of bad occurrences in the complete
plan. If the executed prefix has length $`e\le\ell`$, its count is

```math
\sum_{i=1}^{e}\mathbf 1\{a_i\notin G_\theta\}
 \le
\sum_{i=1}^{\ell}\mathbf 1\{a_i\notin G_\theta\}.
```

All discarded summands are nonnegative. The exit-producing action lies
in the executed prefix and is included on the left; repeated actions
are counted at each occurrence. Thus the charge actually dominates the
physical bad-action count. Positivity of a charge, correct candidate
selection and count domination are separate statements.

The conclusion also covers a phase that never exits. The proof neither assumes phase termination nor requires all candidates to be identified. It bounds precisely the actions that violate the true target. [37–38]

The finite transcript-tree form keeps the terminal affinity visible for nonnegative normalized rows K. Let $`m_\eta(h)`$ be the product of the actual selected-row probabilities along h, let $`A(h)=\sqrt{m_\theta(h)m_\sigma(h)}`$, and let $`F_n(h)`$ be the sum of these affinities at the leaves n selections later. Let $`C_n(h)`$ be the corresponding unnormalised true-model mass-weighted count of selections of σ. If the same causal selector is used in both trees and selecting σ implies $`m_\theta(h)\le m_\sigma(h)`$, then

```math
(1-\operatorname{aff}(K_{\theta,\sigma},K_{\sigma,\sigma}))C_n(h)
 +F_n(h)\le A(h).
```

The branch identity is $`\sum_y A((a,y)::h)=A(h)\operatorname{aff}(K_{\theta,a},K_{\sigma,a})`$. Induction uses this identity and the selector inequality only where σ is selected; it does not assume a conditional-expectation decrement. At the empty history, a strictly positive affinity deficit bounds every finite selection count by its reciprocal. For normalized rows, unequal rows give that deficit by the squared square-root-distance identity. The supremum bound on finite expected counts still needs the actual-law and monotone-count identification before it becomes an infinite-expectation statement. [Q250C-114]

The dependent-alphabet version permits each experiment a to have its own finite outcome type and each row to have mass at most one. It proves the same budget without normalising surviving rows. Its reciprocal conclusion explicitly assumes affinity less than one; normalization and mere row inequality are not silently imported into the subprobability statement. This is the relevant finite-tree interface for support-killed continuation mass, rather than a replacement law conditioned on survival. [Q250C-091]

#### Resetting likelihoods while retaining the probability of an exit

The phase proof above bounds actual errors directly. A complementary
identity explains the earlier source's generated-process calculation
[53]. It distinguishes an unnormalized history calculation from an
expectation under the actual probability law.

Write a controller state as $`x=(s,h)`$, with one of the finitely many public phases $`s`$ and
its within-phase acquired history $`h`$. A selected finite plan produces
a stopped observation record $`r`$ with probability
$`p_\theta(r\mid x)`$. These probabilities sum to one over all
continuing and exiting records. The shared update $`T(x,r)`$ either
extends the same phase history or enters a successor phase with empty
within-phase history. It retains the exit record when counting actual
actions, even though it resets the likelihood memory. The true
$`\theta`$ indexes the observation law used in the analysis, not the
selector or public update.

The transition kernel is

```math
K_\theta(x,x')
 =\sum_{\{r:T(x,r)=x'\}}p_\theta(r\mid x).
```

It is normalized on the countable state space of finite histories.
The generated trajectory law has finite-cylinder probabilities given
by products of these kernel entries from the declared initial state.
For a nonnegative finite current-state charge $`c_\theta(x)`$, put
$`V_0(x)=0`$ and

```math
V_{n+1}(x)
 =c_\theta(x)+\sum_r p_\theta(r\mid x)V_n(T(x,r)).
```

Backward integration, or induction on $`n`$ using those cylinder
probabilities, gives
$`V_n(x)=\mathbb E_{\theta,x}\sum_{j=0}^{n-1}c_\theta(X_j)`$.
Because the observation alphabet and each selected plan are finite, a
fixed finite horizon from one state has only finitely many possible
record sequences. With finite current-state charges, every $`V_n(x)`$
is therefore finite; no uniform bound over all states is needed for
this finite-horizon identity. [Q250C-124]

The convention charges states zero through $`n-1`$ for $`n`$
selections; it does not silently omit the initial selection or add a
terminal one.

Let $`m_\theta(s,h)`$ be the true-model mass of the within-phase
history under its actually selected actions, with
$`m_\theta(s,\varnothing)=1`$. For a continuing record,
$`m_\theta(T(x,r))=m_\theta(x)p_\theta(r\mid x)`$.
For a reset record the successor's new local empty-history mass is
one. Define $`U_n(x)=m_\theta(x)V_n(x)`$. Multiplying the recurrence
therefore gives exactly

```math
\begin{aligned}
U_{n+1}(x)
={}&m_\theta(x)c_\theta(x)
 +\sum_{\text{continuing }r}U_n(T(x,r))\\
 &+\sum_{\text{reset }r}
       m_\theta(x)p_\theta(r\mid x)U_n(T(x,r)).
\end{aligned}
```

This is the unnormalized reset recurrence. It weights each
successor's reset-at-empty-history cost by the full exit mass.
There is no division by $`m_\theta(x)`$. If that mass is zero, every
continuing extension also has zero mass and every reset term carries
a zero prefactor, so the identity still holds. The equality is an
inductive relation between the two calculations, not an inference
from calling both of them a process.

On an actually continuing prefix, every observed symbol preserves the
current support. All survival indicators are therefore one, so the killed
and full likelihoods agree on that prefix; the killed calculation is zero
on an excluded continuation.

Conditioning a continuing observation on survival would replace
its original probability by a normalized value and would change this
recurrence. The partially revealing probe below displays the lost
information. With the actual generated law, a uniform finite bound
on the finite-prefix expected charges passes to the total charge by
monotone convergence. If charges are nonnegative integers, finite
total expectation implies finitely many positive charges almost
surely. A physical-action conclusion additionally needs the
stopped-prefix domination just proved, true-model retention along
positive exits, and the nonempty-block clock argument below.
This generic identity does not equate every historical implementation
with the particular policy of this section or supply a new kernel
execution receipt.

<a id="reset-budget-rank-and-full-exit-mass"></a>

The generic reset budget makes its hypotheses explicit. Let m(p,h) be the unnormalized continuing-history mass, r(p) a natural phase rank, and V(p,h)≥0 a local potential with V(p,∅)≤C for one C≥0. Suppose the current charge times m, plus the sum of V over continuing children, is at most V(p,h). Suppose also that every **positive true-model exit** strictly decreases r; no rank condition is needed on zero-mass branches. For the full-mass reset recurrence above, finite-horizon induction yields

```math
U_n(p,h)\le V(p,h)+r(p)C\,m(p,h),
\qquad
U_n(p,\varnothing)\le(r(p)+1)C.
```

At an exit the successor root bound is at most r(p)C and is multiplied by m(p,h)K_θ(p,a,y). At a continuing child the same rank term is multiplied by its continuing-history mass. Summing both kinds of branch uses the **full** normalized row, while the local-potential inequality pays the current charge. Thus no conditioning on the ultimately surviving phase enters the bound. The rank controls resets, not live-model exclusion or physical-action domination; those remain the separate invariants already stated. [Q250E-150]

`ResetLaw` proves that the full finite tree has total leaf mass m(p,h), and that leaf-weighted accumulated cost equals U_n(p,h) plus the pre-existing accumulated charge times m(p,h). `ResetTrajectory` separately constructs a normalized reset kernel and an infinite Ionescu–Tulcea trajectory with the prescribed finite causal compositions. These are the finite-tree and law-construction providers for the expectation argument above, rather than an assumption that two objects called a process have identical laws. [Q250E-151] [Q250E-152]

[Q250E-150]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d482ed24b70fa4501eefcd7878a7889af7b8f3fbf31f8c6de60b77ebffa758b1/ResetBudget.lean
[Q250E-151]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f76f752f31565baa5262aa4aafcf21a7f3722d1f74c9681fe6d8a2a50bb02d12/ResetLaw.lean
[Q250E-152]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c1bae278764e20b67382204474b62e8bba769463f812d5adfc2086b85b303f68/ResetTrajectory.lean

#### The complete physical-time guarantee

Define a finite bound by induction on support size:

```math
D_{B,\theta}
 =C_{B,\theta}
  +\max\Bigl(
      \{0\}\cup
      \{D_{B',\theta}:
          \theta\in B'\subsetneq B,\ W(B')\}
    \Bigr).
```

The maximum ranges over finitely many smaller certified supports. The bound is attached to the chosen witnesses; it is not an optimal cost claim.

**Theorem (recursive constructive restoration).** If $`W(B_0)`$ holds, the single policy just constructed is licensed on every feasible action-consistent finite history, for every seed. Under each $`\theta\in B_0`$, its total number N<sub>bad</sub> of physical actions outside G<sub>θ</sub> satisfies

```math
\mathbb E_\theta N_{\mathrm{bad}}\le D_{B_0,\theta}\lt{}\infty,
\qquad
\Pr_\theta(N_{\mathrm{bad}}\ge k)
 \le \frac{D_{B_0,\theta}}{k}
 \quad(k\ge1).
```

In particular, almost surely all sufficiently late physical actions belong to G<sub>θ</sub>.

**Proof.** The phase estimate holds conditionally after every actual finite entry history: future acquisitions have the stipulated conditional laws, and within-phase likelihoods restart at one. At a first support exit, the new nonempty support contains the true model and is certified. Induction on support size bounds the conditional future cost by its $`D_{B',\theta}`$. Summing over the countably many possible finite exit records, and adding the current phase's bound, proves the stated D<sub>B,θ</sub> inequality. A phase with no exit contributes no later phase. This argument conditions at actual observed entries and exits, not at the unobservable last error or on never exiting again.

For clarity, let *e*<sub>*j*</sub> be the number of actions actually executed in stopped plan *j*. Every loaded plan is nonempty, and an immediate exit still executes one action. Thus

```math
1\le e_j\le |v_j|,\qquad
T_0=0,\qquad T_{j+1}=T_j+e_j.
```

These intervals cover the physical action clock and *T*<sub>*j*</sub> tends to infinity. The old suffix contributes no executed actions. The initial controller state has no completed-action record and is not counted as a block. Every later block contains its actual exit action when present. Summing block charges therefore counts all physical bad actions exactly; domination by the full planned charge supplies the bound already proved.

Markov's inequality gives the count tail. Finite expectation of this nonnegative extended integer count implies that it is finite almost surely. A finite set of bad physical times has a finite maximum, which proves eventual target goodness. The controller continues to issue actions; no finite zero-error stopping declaration or observable final-error certificate follows. $`\square`$

The source's canonical policy theorem has this finite expected physical-cost interface. The ordinary proof above supplies a direct phase calculation and the displayed support-chain bound; it is not a fresh execution of the source's formal development or a claim that two historical implementations have identical whole-state laws. [38]

#### Completed episode records and the information available at an action

The last step has two different obligations: reconstruct the physical
action stream correctly, and show that its decisions use only information
available at their physical times. The staged source review [53]
separates them.

A recorded transition must retain the old phase, selected candidate
and stopped observation record. Reconstructing the executed block
from the new phase after a reset can select a different plan and
discard the action that caused the exit. With the old record, the
block is exactly the executed prefix, including that exit action and
excluding the abandoned suffix. The initial placeholder has no
completed action. Every later recorded block is nonempty on the
specified probability-one event, so concatenation covers the physical
clock; a total decoder's fallback outside that event affects none of
these almost-sure conclusions. These are the record and clock
properties used in the preceding count argument.

Measurability in finitely many completed episode records alone is
weaker than action-time nonanticipation. If one episode contains two
actions, its completed record also contains the observation after the
second action. A measurable function of that record can inspect this
later observation when choosing a purported first action. It is still
episode-record measurable. Thus a result that the first $`t+1`$
completed records determine physical action $`t`$ does not by itself
prove that only the first $`t`$ acquired physical observations are
used.

The policy constructed here supplies the additional invariant
directly. Start with its fixed initial support, empty likelihood
history and nonempty chosen queue. Given the same finite sequence
of acquired physical action/observation pairs, induction reconstructs
the same current support, within-phase likelihoods and residual queue.
The fixed tie rule chooses the same replacement plan whenever a
boundary is reached. Hence the next action is the same queue head
before its observation is received. After that observation, the
support update either retains the suffix or discards it immediately
and loads the new plan. Changing observations beyond this acquired
physical prefix cannot affect the action being issued. This proves
the physical-clock information property for this history policy,
in addition to the measurable decoding and eventual-goodness
argument.

The earlier decoder review correctly left that stronger inference
open for the endpoint it actually inspected. The acquired-history
construction in this section provides an ordinary proof of the
needed property for its own policy; it does not retrospectively add
a causality theorem to the earlier formal decoder's statement.

#### Positive cases and necessary boundaries

**Revealing evidence and a newly forbidden suffix.** Take two models and actions q,r<sub>0</sub>,r<sub>1</sub>. The probe *q* returns the model label with certainty; the repair actions always emit label zero under both models. Let $`G_i=\{r_i\}`$, let the initial menu be $`\{q,r_0\}`$, and let the singleton menus be $`\{r_0\}`$ and $`\{r_1\}`$. For both initial candidates, the list (q,r<sub>0</sub>) has progress and certified singleton successors. At a singleton, its correct repair is a self-verifying one-action list.

The policy executes *q*, updates the support and then issues the corresponding repair forever. Exactly one bad action occurs. Under model one, executing the abandoned suffix *r*<sub>0</sub> would violate the new menu. Dropping the exit record would instead erase the one real bad action from the count. The support must use strict positivity: retaining a model whose label had zero probability would lose the inference that makes the new action licensed.

**A partially revealing probe.** Let *q* emit an eliminating symbol *e* with probability 1/2 under model zero and with probability zero under model one; otherwise it emits *s*. Take $`G_0=\{r_0\}`$, $`G_1=\{q\}`$, initial menu $`\{q\}`$ and menu $`\{r_0\}`$ after eliminating model one. Let the repair always emit the symbol s, and use the initial probe menu also at singleton model one. Both initial candidates can use the one-action plan *q*: candidate zero has progress, while candidate one has a live self-verifying plan because the full observation vectors differ. Under zero, the number of probes is geometric with mean two; under one, every action is already good.

Conditional on observing only the continuing symbol, the normalized observation law is the same point mass under both models. Replacing the raw probabilities by these normalized rows would erase the survival information and the positive exit mass. The full stopped law and the affinity deficit keep both.

**Every possible strict successor matters.** Consider three models. A sole initially permitted probe separates model zero from the pair $`\{1,2\}`$. The singleton zero has a permitted good action. At the pair $`\{1,2\}`$, suppose the only permitted action is bad for both models and has the same deterministic observation under each. The favorable singleton branch does not certify the initial support: the other nonempty successor cannot progress or self-verify. Under models one and two, any lawful policy remains bad forever. Requiring one successful branch would therefore give a false positive.

**Impossible and forged histories.** An empty menu at a nonempty support cannot supply a nonempty licensed plan. An empty initial support cannot supply the theorem's certified starting point. Impossible observations need no continuation certificate, and a fabricated off-policy action can give a different inferred support from the controller's actual replay. The legality conclusion consequently retains both feasibility and action consistency. Legality for a fixed common menu can be stated without this support reconstruction; it is a different contract. [38]

**Counting errors is different from locating the last error.** Section 7.7 already supplies almost-sure finite recovery with infinite expected bad occupancy. Conversely, finite expected bad count need not bound the expected time of the last bad action. In a one-model system with a permitted good action *g* and bad action *b*, draw $`K\ge1`$ with $`\Pr(K=k)=2^{-k}`$, issue *g* for $`2^K`$ times, issue *b* once, and then issue *g* forever. The bad count is one, while the expected last-error time is infinite because each summand $`2^{-k}2^k`$ in its expectation equals one. This does not contradict the theorem's count bound.

The certificate and constructed policy concern finite fixed controlled laws, exact support updates and support-dependent menus. They do not handle arbitrary moving plants, general history-dependent resource constraints, copied observations, empirical validation of a sensor or authentication of a normative target. They use exact probability comparison and finite classical witness choice, without claiming a general executable procedure for arbitrary real inputs.

A later source separately establishes necessity and an existence equivalence in the same finite seeded-policy interface. It also equates existence of an almost-surely restoring lawful policy with existence of a possibly different policy having finite expected bad count. That converse belongs to its own all-branch continuation and transfer argument; it is not derived here from the positive-probability criterion or from this constructive proof. Its existence statement does not upgrade every almost-surely successful policy to finite expected cost. [39]

### 7.13 When recursive restoration is necessary

The recursive certificate in §7.12 is also necessary for the same finite controlled-observation problem. Its necessity is a distinct result: zero-probability observations prevent the unrestricted finite-prefix transfer available under full support. The argument instead follows every feasible support-changing branch and transfers probability only on actions whose positive observations remain possible in the rival model. [39–40]

Retain the nonempty finite sets Θ,A,Y, fixed normalized nonnegative laws P<sub>θ,a</sub>, targets G<sub>θ</sub>, nonempty initial support *B*<sub>0</sub>, exact support update and support-dependent menus Γ of §7.12. Fix any common private-seed probability space (Z,ρ). A measurable policy $`\pi(z,h)`$ chooses an action from the seed and acquired finite history; the next observation, conditional on this entire information and the chosen action, has law P<sub>θ,a</sub>. The seed law is the same under every hidden model. Legality means

```math
\pi(z,h)\in\Gamma(B(h))
```

for every seed and every feasible action-consistent history. The model parameter is not an input to this policy or seed selection.

**Theorem (recursive characterization).** The following conditions are equivalent:

1. The initial support has the recursive certificate $`W(B_0)`$.
2. One common legal measurable policy has almost-sure eventual target goodness under every $`\theta\in B_0`$.
3. One common legal measurable policy has finite expected total number of target-bad physical actions under every $`\theta\in B_0`$.

The existential policy precedes the universal model quantifier in both policy statements. The policies in conditions 2 and 3 need not be the same. A deterministic common policy suffices whenever these conditions hold. The constructive implication from 1 to 3 and the implication from 3 to 2 are established in §7.12; the proof below establishes 2 to 1. [39–40]

#### Fixing one common seed

For a fixed seed *z*, let $`\Pr_\theta^{\pi_z}`$ be the law generated by $`\pi_z(h)=\pi(z,h)`$ and the fresh controlled observations. The common experiment is the explicit mixture

```math
\Pr_\theta^\pi(E)
 =\int_Z \Pr_\theta^{\pi_z}(E)\,\rho(dz)
```

for measurable path events *E*. This follows from the common-seed construction and the finite-history product probabilities, then from extension to the generated path sigma algebra. It is not an arbitrary representation assumption about a separately supplied behavioral process.

If eventual goodness has probability one under θ, its fixed-seed probability is one for ρ-almost every seed. Intersect these full-measure seed sets over the finitely many initially live models. Their intersection still has measure one and is nonempty. Choose a single z<sub>*</sub> there. The resulting deterministic policy succeeds in every live model. Its pointwise legality follows from the original contract, which held for every seed. The seed is now fixed once, before any continuation or support induction. A model-dependent posterior over seeds is not used. [41]

#### What a positive acquired prefix permits

Use chronological histories in this proof. For a deterministic policy *f*, let $`h=((a_0,y_0),\ldots,(a_{n-1},y_{n-1}))`$ be action-consistent. Its probability under a model θ is

```math
p_\theta(h)=\prod_{s\lt{}n}P_{\theta,a_s}(y_s).
```

Induction over the acquisitions proves this formula. Exact support updating consequently gives

```math
B(h)=\{\theta\in B_0:p_\theta(h)\gt{}0\}.
```

Define the continuation by $`f_h(v)=f(h\frown v)`$, where $`\frown`$ appends a future acquired record. Its conditional future finite-history probabilities, given *h* under any $`\theta\in B(h)`$, are precisely the products generated by *f*<sub>*h*</sub> and P<sub>θ</sub>. Each action is chosen before its next observation. Cylinder equality therefore identifies the entire continuation law.

If *f* succeeds almost surely, its conditional failure probability after a positive-probability prefix is zero. Thus the **same** continuation *f*<sub>*h*</sub> succeeds for every model remaining in $`B(h)`$. It is legal there as well: every feasible consistent future record *v* yields a feasible consistent full record $`h\frown v`$, and

```math
B_{B_0}(h\frown v)=B_{B(h)}(v).
```

The public menu and original legality contract apply to that same support. No unobserved coordinate or hidden model selects the continuation. The source's newest-first storage convention writes the future before the retained older record; the acquired chronological order above expresses the identical causal continuation. [41,43]

#### Transfer with a guard on the entire earlier path

The needed replacement for full-support transfer is one-sided and restricted. Consider two fixed observation families P,Q under one common seeded policy. Let $`U\subseteq D\subseteq A`$. Assume

```math
P_a(y)\gt{}0\ \Longrightarrow\ Q_a(y)\gt{}0
 \quad(a\in D,\ y\in Y),
\qquad
P_a=Q_a\quad(a\in U).
```

Let *C* be a common measurable action-path event on which every action lies in *D* and every action after a deterministic time *N* lies in *U*. Then

```math
\Pr_P^\pi(C)\gt{}0\quad\Longrightarrow\quad
\Pr_Q^\pi(C)\gt{}0.
```

To prove this, split at the deterministic length *N*. Only prefixes whose recorded actions lie in *D* can contribute. For such a prefix *h*, let $`I_h(z)`$ indicate that its actions are consistent with the seeded policy, and put $`p_P(h)=\prod_{s\lt{}N}P_{a_s}(y_s)`$; define *p*<sub>*Q*</sub> similarly. The implication on positive atoms gives

```math
p_P(h)\gt{}0\quad\Longrightarrow\quad p_Q(h)\gt{}0.
```

For a fixed seed and prefix, kill the future process before executing its first action outside *U*. Its kernels coincide under *P* and *Q*. Hence there is one common measurable nonnegative continuation probability $`q_h(z)`$ for the section of *C* after this prefix. Its measurability follows from the finite-cylinder construction and extension to measurable events. The event's probabilities are

```math
\Pr_P^\pi(C)
 =\sum_{h:\,a_s\in D}
    p_P(h)\int_Z I_h(z)q_h(z)\,\rho(dz),
\qquad
\Pr_Q^\pi(C)
 =\sum_{h:\,a_s\in D}
    p_Q(h)\int_Z I_h(z)q_h(z)\,\rho(dz).
```

The sum has finitely many prefixes. A positive term in the first expression gives a positive term in the second. This proves the implication. The proof keeps the entire common seed and acquired prefix; it neither treats the last exceptional action as a stopping time nor asserts absolute continuity of different infinite observation products. [42]

The all-time restriction to *D* is essential. Agreement or one-sided support on *D* says nothing about a singular action outside *D* in the earlier prefix. It cannot be replaced merely by eventual membership in *D*.

The source also expresses this restriction by changing unused rows. Laws agreeing on *D* give identical probabilities to every measurable action event restricted to staying in *D* forever: kill at the first action outside *D*, compare the identical finite-cylinder kernels and then extend to their path laws. Thus replacing *P*<sub>*a*</sub> by *Q*<sub>*a*</sub> outside *D* leaves such guarded events unchanged. The patched family is globally dominated at the level of one-step atoms, while the original unused rows may be singular. This explains the guard's role without asserting equality of the unrestricted path laws or domination of the original infinite row arrays. [42]

#### A stable support supplies a self-verifying set

Suppose the same policy succeeds under every model in a nonempty support *B*. Fix a true model $`\theta\in B`$ and an action set *D* such that, under θ, all actions lie in *D* almost surely. Suppose also that

```math
P_{\theta,a}(y)\gt{}0
 \ \Longrightarrow\
P_{\eta,a}(y)\gt{}0
\quad(\eta\in B,\ a\in D,\ y\in Y).
```

There is then a nonempty self-verifying set $`U\subseteq D\cap G_\theta`$ among the live models.

Indeed, on every infinite action sequence over finite *A*, some nonempty set of actions recurs infinitely often. Almost-sure eventual goodness under θ puts this recurrent set inside G<sub>θ</sub>, and all-time membership in *D* puts it inside *D*. Some exact recurrent set *U* has positive probability. On that event, only finitely many actions fall outside *U*. For some deterministic *N*, the event

```math
C(U,N)=
 \{a_t\in D\text{ for every }t;\
   a_t\in U\text{ for every }t\ge N;\
   \text{each }a\in U\text{ occurs infinitely often}\}
```

has positive probability under θ.

Fix a rival $`\eta\in B`$ agreeing with θ on every action in *U*. The guarded transfer just proved makes $`C(U,N)`$ positive under η as well. If any member of *U* were outside G<sub>η</sub>, this event would contain infinitely many errors under η, contradicting its almost-sure success. Therefore every such rival accepts all of *U*, proving live self-verification. Exact recurrence matters: transferring only eventual membership in a larger set could silently drop the particular action rejected by the rival. [40,42]

#### Necessity by induction over live supports

Prove the claim simultaneously for every deterministic successful legal policy by strong induction on the size of its nonempty initial support *B*. The induction hypothesis therefore applies to each continuation policy on every smaller support. Fix such a policy for the current induction step. Let $`D(B)`$ be the set of actions in $`\Gamma(B)`$ whose every nonempty strict observation successor has a recursive certificate. This is exactly the bottom-up admissible-action set of §7.12.

First, every action that this policy issues after a feasible consistent history with unchanged support *B* belongs to $`D(B)`$. It belongs to $`\Gamma(B)`$ by legality. For every symbol *y* whose successor $`B[a,y]`$ is nonempty and strict, the acquired-prefix argument supplies a common successful legal continuation on that successor. Its cardinality is smaller, so the induction hypothesis supplies $`W(B[a,y])`$. This argument examines **every** such symbol at **every** feasible same-support history, not one favorable realized path. Thus the action is in $`D(B)`$. [40,43]

Now fix a candidate $`\sigma\in B`$. If some action in $`D(B)`$ has a progress witness under σ, this candidate satisfies the progress alternative in the stage certificate.

Otherwise, for every $`a\in D(B)`$ and every *y* with $`P_{\sigma,a}(y)\gt{}0`$, the support update must equal *B*: a strict change would itself be a progress witness. Starting at the empty history, induction over actual positive-probability acquisitions therefore preserves support *B*. At each stage, the policy's action is in $`D(B)`$ by the preceding paragraph. Taking the countable intersection over physical times shows that under σ all actions remain in $`D(B)`$ almost surely. This derives the invariant from positive branches; it is not an assumed permanent-safety property.

Furthermore, support preservation means that every live rival remains possible on each such positive symbol:

```math
P_{\sigma,a}(y)\gt{}0
 \ \Longrightarrow\
P_{\eta,a}(y)\gt{}0
 \quad(\eta\in B,\ a\in D(B)).
```

The stable-support argument now supplies a nonempty self-verifying set within $`D(B)\cap G_\sigma`$. Thus this candidate satisfies the other stage alternative. Every candidate has either progress or such a self-verifying set, so the combinatorial equivalence in §7.12 gives $`W(B)`$. The singleton case is included: no nonempty strict successor exists, and the same stable argument supplies its certified actions. This completes the induction and the necessity proof. Together with the already proved construction, it establishes all three conditions of the theorem. $`\square`$

**Positive observation laws as a special case.** If every observation probability is strictly positive, every support update preserves the entire live support. There are no progress witnesses or strict successors, and the recursive admissible menu is exactly $`\Gamma(B_0)`$. The certificate therefore reduces to the self-verifying-set criterion of §7.11, restricted to that common menu. The additional affinity argument in §7.12 supplies a policy with finite expected bad count also in this special case. Choosing an off-policy default inside the nonempty menu extends its legality to arbitrary histories. This budget is supplied by the additional argument; it is not an assertion that every almost-surely restoring policy has finite expected cost.

#### Controls that distinguish the hypotheses

**One-sided support can be enough.** Let $`D=\{a,b\}`$ and $`U=\{b\}`$. Under *P*, action *a* emits zero surely; under *Q*, it emits zero or one with probability 1/2 each. Action *b* emits zero under both. A policy first issues *a*, then uses *b* forever after zero and an action $`c\notin D`$ forever after one. The guarded event of staying in *D* and using *b* after time one has probability one under *P* and 1/2 under *Q*. The needed implication holds, although the positive supports of the first-action laws are not equal.

**An earlier singular action defeats an unguarded tail claim.** Keep identical laws at $`b\in D`$, but let the initial action $`a\notin D`$ reveal the model perfectly. After one outcome choose *b* forever, and after the other choose $`c\notin D`$ forever. Eventual membership in $`\{b\}`$ has probability one in the first model and zero in the second, despite complete agreement on *D*. The all-time guard excludes precisely this earlier unsupported acquisition.

**Unused singular rows do not obstruct a guarded event.** Let the policy always issue *b*, with identical laws there, while an unused action *u* emits zero surely under one model and one surely under the other. The complete arrays of potential observations for *u* are singular. The policy's actual action laws are nevertheless the same constant sequence. Requiring domination of the original unused row laws would add an unnecessary hypothesis.

**The seed cannot contain the hidden answer.** With identical observation laws under two models and disjoint singleton targets, give each model a different deterministic seed and let the policy choose the corresponding target action. This creates model-specific successful experiments but no common-seed solution. Their success does not contradict the theorem: the common seed distribution premise has been violated. The identical-law, disjoint-target obstruction remains the one already explained in §7.11.

**Feasibility does not replace action consistency.** In a one-model system, let both actions g,b be permitted, let every observation be zero, and let only *g* be good. A policy chooses *g* at the empty record and at every record containing only *g*, but chooses *b* forever after any record containing *b*. Its actual behavior is always good. The fabricated prefix $`((b,0))`$ is feasible in the observation model but inconsistent with the policy; its continuation is bad forever. Thus the continuation lemma cannot be extended to arbitrary feasible records.

A zero-mass observation branch likewise cannot inherit a success statement by conditioning on it. The exact support restriction removes that branch from every model for which it is impossible. Finally, nonempty *B*<sub>0</sub> is necessary: with no live models the policy's universal success and feasible-history legality conditions are vacuous, whereas $`W(\varnothing)`$ is false.

This characterization concerns the stated finite fixed controlled laws, exact support menus and common causal history policy. It establishes neither a finite-memory bound nor a finite zero-error declaration, and it does not convert every successful policy into a finite-expectation one. The public menu and target assignments remain application premises. The source's formal closure and original reviewer controls retain their separate execution scope; the ordinary proof here does not claim a fresh kernel build or an unrestricted policy-realization theorem.

### 7.14 Stateful learning with revealing observations

The controlled-observation results extend to a visible state that changes with the selected action. Two obligations then interact: every revealing transition must enter a winning continuation for the models that survive, and navigation within an unchanged support must remain viable. A finite recursion over model supports, with a greatest fixed point over physical states at each level, characterizes eventual correctness. A deterministic scheduling refinement also supplies a computable policy with finite expected total errors. The stateful argument and its scheduling refinement are distinct from the controlled independent-observation proofs in §§7.12–7.13. [44–46]

#### The experiment and the state-region criterion

Let Θ, S and A be finite nonempty sets of hidden models, visible states and actions. The fixed unknown model θ determines supplied rational transition probabilities $`P_\theta(s,a,y)`$, normalized over y in S. Conditional on the complete acquired history, the current action and any common independent private seed, the next state has this row law. The controller observes states and its own actions, but neither θ nor the acceptance bit. The accepted pairs form a supplied set $`G_\theta\subseteq S\times A`$.

The nonempty live support B is updated after the transition from s through action a to y by

```math
C(B,s,a,y)=\{\eta\in B:P_\eta(s,a,y)>0\}.
```

The true model remains live almost surely. A supplied hard menu $`\Gamma(B,s)\subseteq A`$ may depend arbitrarily on the live support and visible state; it need not vary monotonically with B. An empty menu cannot sustain an infinite lawful continuation. As in §7.13, legality applies at every feasible action-consistent history from the declared initial condition. The policy has no extra information correlated with θ. Define its total number of errors by

```math
\mathrm{Bad}_\theta
 =\sum_{t\ge0}\mathbf 1\{(S_t,A_t)\notin G_\theta\}.
```

Compute winning regions $`W_B\subseteq S`$ in increasing order of the cardinality of nonempty B. When processing B, the regions for its proper nonempty subsets are already fixed. For any proposed region W, let $`\mathcal A_{B,W}(s)`$ consist of the actions in Γ(B,s) such that every possible nonempty successor satisfies

```math
\begin{aligned}
C(B,s,a,y)\subsetneq B&\ \Longrightarrow\ y\in W_{C(B,s,a,y)},\\
C(B,s,a,y)=B&\ \Longrightarrow\ y\in W.
\end{aligned}
```

These tests cover outcomes possible under any live model. Checking only a favored candidate's outcomes would permit an irreversible failure in another model.

Call an edge **internal** when it leaves the support equal to B, and put

```math
I_B(s,a)=\{y:C(B,s,a,y)=B\},\qquad
q_\theta(s,a)=\sum_{\varnothing\ne C(B,s,a,y)\subsetneq B}P_\theta(s,a,y).
```

Every internal edge is positive under every model in B. For a candidate θ, a qualifying component consists of a nonempty set D of states in W and nonempty action sets $`U(s)\subseteq\mathcal A_{B,W}(s)`$ on D with the following properties. Every internal successor of a used pair stays in D, and the graph of these internal edges is strongly connected. Every used pair is θ-accepted and has zero θ-exit probability. Finally, every live model σ agreeing with θ on the **full transition row** of every used pair accepts every used pair. This last condition is self-verification. The zero-exit condition makes the θ-rows on the component genuine normalized internal transition rows. Other models can have revealing exits. Equality after conditioning on no revelation would discard relevant probability mass and is not the criterion.

Let $`T_\theta(W)`$ be the union of qualifying component states, and let $`E_\theta(W)`$ contain the states having an allowed action with positive θ-exit probability. Define $`R_B(W)`$ to contain the states in W from which, for every θ in B, an internal path of allowed actions reaches $`T_\theta(W)\cup E_\theta(W)`$. Paths of length zero count. Start with S and iterate $`W_{j+1}=R_B(W_j)`$. All component, action and reachability conditions are monotone in W, and $`R_B(W)\subseteq W`$. There are at most |S| strict decreases. The stable set is *W*<sub>*B*</sub>, the greatest fixed point for this support. [44]

**Theorem (stateful restoration).** For any nonempty initial support B and state s, the following conditions are equivalent:

1. The state s belongs to *W*<sub>*B*</sub>.
2. One common lawful history policy has finite $`\mathrm{Bad}_\theta`$ almost surely for every θ in B.
3. One common lawful history policy has finite $`\mathbb E_\theta\mathrm{Bad}_\theta`$ for every θ in B.
4. A computable deterministic common history policy has the property in 3.

The policy is chosen before the universal model quantifier. Condition 4 uses the exact finite rational input. Its policy may ignore any prescribed common seed, including a constant seed. The original construction for 1 implies 3 uses fresh independent private action choices; the deterministic refinement below removes that additional resource requirement. The theorem supplies existence of a suitable finite-expectation policy, not finite expectation for every almost-surely winning policy. It does not require a finite observed certificate that no more errors will occur. [44–46]

#### Necessity: safe prefixes and recurrent components

Let *V*<sub>*B*</sub> be the states admitting a common almost-surely winning policy. Induct on |B|, assuming the theorem for every proper nonempty support. For necessity, the common-seed selection argument of §7.13 applies to the present Markov acquisition law as well: intersect the finitely many full-measure successful seed sets and fix one common seed. This gives a deterministic history policy whose successful continuation can be examined after any positive acquired prefix. Equivalently, a common behavioral policy has model-independent action factors in its finite-history probabilities.

Every surviving model assigns positive probability to such a prefix. Its residual policy must win under all survivors, since positive conditional failure would give positive unconditional failure in that model. Consequently every action used at a history with live support B has its same-support successors in *V*<sub>*B*</sub> and each proper-support successor y in $`V_C=W_C`$. It belongs to $`\mathcal A_{B,V_B}`$.

Fix an actual θ. A positive-probability proper support exit supplies a finite internal path to $`E_\theta(V_B)`$. If there is no positive exit event, or if a positive event remains at B forever, consider the state-action pairs used infinitely often on a no-exit run. Almost surely, an infinitely repeated pair cannot have a positive θ-exit probability: each repetition would give a fixed positive conditional chance of exit. The same repeated-trial bound makes every positive internal successor recur. After the finitely occurring pairs disappear, the run supplies paths between the recurrent states. Its recurrent pairs therefore form an internally closed strongly connected component, with zero θ-exit probability and only θ-accepted pairs. [Q250C-085]

There are finitely many recurrent pair sets. Some fixed component D occurs on a positive-probability no-exit event. If a live σ agrees with θ on all full rows used by D, choose a finite positive prefix after which the run uses only these pairs and each recurs. Such a prefix exists by a countable-union argument; it is not a stopping time defined as the last bad action. Kill the residual process at its first pair outside D or first support change. Its θ- and σ-laws have identical transition rows and action kernels before killing. Equality of finite cylinders gives equality of the measurable event of staying in D and visiting all its pairs infinitely often. The prefix has positive probability under σ, and full-row equality also gives zero σ-exit probability on D. If σ rejected any recurrent pair, the transferred event would contradict σ's almost-sure success.

Thus D is a qualifying θ-component. It is reached by an internal path from the initial state. For every θ, either the exit argument or the recurrent-component argument supplies the required path. Hence $`V_B\subseteq R_B(V_B)`$, and monotonicity gives $`V_B\subseteq W_B`$. This uses the original process throughout; conditioning on no exit does not turn its physical trajectory into an independent sequence. [44]

#### Navigation when a predicted exit never occurs

For sufficiency, fix a nonempty winning support region W and a candidate φ. First use a baseline navigation policy that chooses uniformly from $`\mathcal A_{B,W}(s)`$ until a candidate target is reached, the candidate is rejected, or the support changes. Every state of W has a nonempty allowed menu: a path to a target or exit supplies an action, and a target has component actions.

Write N=|S|, a=|A| and M=Na. Let p be the least positive transition probability in the supplied finite system. Use the conservative constants

```math
q=(p/a)^N,\qquad L=N/q.
```

For a fixed actual θ, let H contain the allowed state-action pairs whose full rows differ under θ and φ, and put d=|H|. H is an analysis device; the controller tests every sampled row and does not know θ or H.

From every active state the fixed-point condition supplies a simple internal path of length at most N−1 to a φ-target or a φ-positive exit pair. Its internal edges are all θ-positive. At a target, navigation ends. At an exit pair, either the full row differs, completing an H-row sample, or the rows agree and a revealing outcome is also θ-positive. Thus within N physical actions the conditional probability of target entry, a support exit, a completed H-row sample, or earlier rejection is at least q. The conditional mean wait for the next such event is at most L. A candidate's exit that is impossible in the actual model still provides a sample of a differing row; it cannot justify waiting indefinitely for revelation. [44]

To test rows, let Δ be the least positive coordinate difference between supplied model rows at the same pair; if none differ, take Δ=1. Put $`c=\Delta^2/2`$ and $`r=(1+c)^{-1}<1`$. Choose a rational allowance $`0<\varepsilon<1`$ and an integer $`n_0\ge1`$ satisfying

```math
\frac{2MN r^{n_0}}{1-r}\le\frac{\varepsilon}{2}.
```

After each completed k-th sample of a pair, for $`k\ge n_0`$, reject the candidate if any empirical coordinate differs from its candidate probability by at least Δ/2. At each new stage, the Markov experiment can be realized by fresh independent next-state tapes, one for every pair, consuming its next entry when that pair is selected. Conditional on the stage's starting history, each tape has its actual row law. Physical state trajectories need not be independent. Hoeffding's bound at a fixed tape count is at most $`2\exp(-ck)\le2r^k`$. Union over the M pairs, N coordinates and all deterministic counts from *n*<sub>0</sub> onward bounds a matching stage's false-rejection probability by ε/2.

Call a completed navigation event either an H-row sample or termination; a transition satisfying both ends the stage. Let J count completed events through termination, with J=0 if the stage starts in its target. Before termination, all completed events are H-row samples. If d>0 and $`j\ge dn_0`$, survival after j events forces one differing row to have at least $`\lceil j/d\rceil`$ samples without rejection. Fix a differing coordinate for each row of H. Survival at that count forces a deviation of at least Δ/2 from its actual probability. Since both the row and its count are selected by the data, take a union over every H-row and every deterministic count $`k\ge\lceil j/d\rceil`$ on the preallocated tapes:

```math
\Pr(J>j\mid\text{stage start})
 \le \frac{2d r^{\lceil j/d\rceil}}{1-r}.
```

No fixed-count concentration inequality is applied after conditioning on a selected count. Summation gives an upper bound $`dn_0+2d^2r^{n_0}/(1-r)^2`$ on the mean event count. If d=0, the next event is terminal. A bound valid in every case is

```math
J_{\rm nav}=1+Mn_0+\frac{2M^2r^{n_0}}{(1-r)^2}.
```

Let τ<sub>j</sub> denote successive completed-event times, extending them by the terminal time after termination. Whether J is at least j is known at τ<sub>j−1</sub>. The bounded-block argument bounds the conditional mean wait for the next required event by L. Conditional expectation and monotone convergence therefore give

```math
\mathbb E\tau_J
 =\sum_{j\ge1}\mathbb E\left[
    \mathbf1_{\{J\ge j\}}(\tau_j-\tau_{j-1})\right]
 \le L\mathbb E J\le L J_{\rm nav}.
```

Each required next event is almost surely finite by the block bound, and the event-count tail makes J finite almost surely, justifying the stopped sum. This bounds all navigation actions, without independence between event counts and waiting times. [44]

#### Operation, candidate cycles and the physical error budget

Cycle through the candidates in B. Start fresh counters for each navigation stage. On rejection, begin the next candidate at the current state. On target entry, choose a qualifying component containing that state, reset the statistical counters once, and choose uniformly among its U-actions. Test after each completed row sample as before. A revealing transition immediately invokes the already constructed policy for its winning lower-support state, taking precedence over simultaneous rejection. The action producing that transition is counted at the old support; the continuation begins afterward.

<a id="stationary-operating-pair-kernel"></a>

When the actual rows are normalized and all their positive successors remain in the component, the uninterrupted stationary operating policy has the following pair-chain construction. Give every retained pair f a strictly positive weight w(f), with the weights at each used source state summing to one. Its transition from e to f is P_θ(e,source(f))w(f). Grouping the sum over f by source state, using those local normalizations and closure of all positive P_θ-successors, gives total mass one. Its positive edges are exactly the positive physical successor edges followed by a retained choice. A state-graph path therefore lifts to a pair-chain path; the nonempty-successor clause supplies its initial step. Strong connectivity of the component yields irreducibility of this pair chain. Uniform weights are obtained from the reciprocal of each nonempty source fiber's cardinality. This construction concerns the uninterrupted stationary policy; it neither makes the rotor's physical projection Markov nor conditions on future nonrejection. [Q250E-168]

[Q250E-168]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5b7e23bf7aca12b0529cb77362bf1cb93d54fc1567fe5db7e9d8d000b5d50d99/StationaryPairChain.lean

For actual θ and an operated φ-component, three cases exhaust the possibilities.

* If all full rows match, self-verification makes every used pair θ-good and gives zero θ-exit probability. The stage may last forever with no bad cost; its false-rejection probability is at most ε/2.
* If some used pair has a θ-positive exit, the strongly connected internal graph and uniform action choice give a conditional exit probability at least q within N actions. The expected time to exit is at most L, and statistical rejection can only end the attempt earlier.
* If there is no θ-exit but some full row differs, the uninterrupted uniform component policy is a finite irreducible θ-chain. Ignore other rejection tests for analysis and let K be the first tape count at which one fixed differing coordinate would reject. Then $`\Pr(K>k)\le2r^k`$ for $`k\ge n_0`$, so

```math
\mathbb E K\le J_{\rm op}
 :=n_0+\frac{2r^{n_0}}{1-r}.
```

The conditional mean wait to the next completed sample of this row is at most L. Survival to its next sample is determined after the previous sample, so the same stopped-sum calculation bounds mean rejection time by $`LJ_{\rm op}`$. Other tests can reject sooner. Since $`J_{\rm op}\ge1`$, this is a common conditional bound on harmful operating cost in the last two cases.

For the true candidate, navigation falsely rejects with probability at most ε/2. Given target entry, fresh operation falsely rejects with probability at most ε/2. Except on their union, the attempt either hands off to a winning smaller support or remains permanently in an actually good component. Every completed candidate cycle includes a true-candidate attempt. Iterated conditioning bounds the expected number of attempts begun at support B by $`|B|/(1-\varepsilon)`$. Thus its local expected bad cost is at most

```math
C_B=\frac{|B|L(J_{\rm nav}+J_{\rm op})}{1-\varepsilon}.
```

Only one proper-support handoff ends this level. If *H*<sub>*C*</sub> bounds the lower-support continuation from every state in its winning region, set

```math
H_B=C_B+max_{\varnothing\ne C\subsetneq B,\ W_C\ne\varnothing}H_C,
```

where an empty maximum is zero. Induction gives a finite bound, with the simpler global estimate

```math
H_B\le
\frac{|B|(|B|+1)L(J_{\rm nav}+J_{\rm op})}{2(1-\varepsilon)}.
```

No exit-triggering action is lost or counted twice. Finite expected nonnegative bad count implies almost-sure finiteness. Together with necessity this proves equivalence of conditions 1–3 under the stated randomization resource. [44]

#### Deterministic scheduling without resetting away progress

The action coins can be removed by retaining a local round-robin counter at every state. Fix an order on each allowed navigation menu, or each selected operating menu. On a visit to s, select its next action and advance its counter modulo its menu size; leave other counters unchanged. Reset the counter vector only at a new navigation or operating stage. In particular, tests, returns to an anchor and the analysis-only H-row milestones do not reset it. [45]

For a fixed stage, augment the physical state with the whole counter vector. With at most a actions per state, this finite chain has at most $`Z=Na^N`$ states. Every positive augmented transition has probability at least p. Consider a closed strongly connected class of the augmented chain and its physical projection D. A positive cycle through an augmented vertex over s returns to the same counter vector. Its positive number of departures from s must be a multiple of the menu size. Consequently every prescribed action at s occurs on the cycle. Closure includes every supported successor of each such action. Thus D is closed under all prescribed actions at all of its states. The physical process alone need not be Markov, and the augmented chain need not be irreducible.

For navigation, kill this auxiliary chain on an H-row sample, target entry or support exit. A closed nonterminal class would project to states avoiding the target and using every allowed action. Avoiding H makes all their θ- and φ-rows agree. Avoiding exits makes their θ-exit probabilities zero and therefore their φ-exit probabilities zero. Their internal successors stay in the projection, contradicting the fixed-point path to a φ-target or φ-exit. Thus every active augmented state has a path to a terminal event.

A shortest such path uses at most Z transitions, each of probability at least p. The conditional probability of an event within Z steps is at least $`p^Z`$, uniformly over **every** counter vector. Therefore the conditional mean wait is at most

```math
L_{\rm rr}=Z/p^Z.
```

For operation, a closed augmented class avoiding a possible exit would project to a nonempty set closed under every internal U-edge. Strong connectivity forces that projection to be the entire component, including its exit-bearing pair, a contradiction. If no exit is possible, kill at the next sample of any specified used pair; the same projection argument rules out a closed class avoiding that pair. Both waiting times are bounded by L<sub>rr</sub>.

Per-row tapes remain independent with their actual row laws under this deterministic action schedule. The deterministic-count concentration, selected-count union, completed-event stopping argument and candidate-cycle proof therefore remain valid with L replaced by L<sub>rr</sub>. The resulting policy has

```math
\mathbb E_\theta\mathrm{Bad}_\theta
 \le\frac{|B|(|B|+1)L_{\rm rr}(J_{\rm nav}+J_{\rm op})}
               {2(1-\varepsilon)}.
```

Take ε=1/2 so each stage receives allowance 1/4. All threshold searches then compare exact rational expressions and terminate; no noncomputable real testing parameter enters the effective construction. Its expectation is over the random transitions, not private action coins. The policy needs only local counters and empirical counts; the augmented graph is a proof device, not a structure it must construct during execution. The rotor has finite memory, but the full learner retains unbounded sample counts. Condition 4 is proved without asserting a stationary finite-state implementation or a practical learning-time bound. [45–46]

Resetting at every action would always select the first action. Resetting at every first return to an anchor similarly starves later actions there. For a state whose first action is an uninformative self-loop and whose second is informative, retained round-robin uses the second on the next visit; repeated reset never does. The proof's uniformity over accumulated counter vectors is therefore substantive, not an initialization convention.

#### Exact computation and reduction to the earlier models

The component calculation has a finite pruning algorithm. For fixed B,W,θ, retain the allowed θ-good pairs with zero θ-exit probability. Compute their maximal end components. Within each, remove any pair rejected by a model agreeing with θ on every full row of that component, then recompute. Every valid self-verifying subcomponent survives: it lies in a current maximal end component, and a model matching that larger component also matches the subcomponent and accepts all its pairs. Pairs outside every end component cannot belong to a valid one. At termination the surviving maximal end components are good and self-verifying. The invariant places every originally valid component inside a returned one, and any larger valid extension would contradict maximality. Their outputs are exactly the maximal qualifying components. Intersecting valid components have a valid union, so maximal qualifying components have disjoint state sets. Target entry therefore admits a definite component choice. [44–45]

At most M pairs can be deleted in one such computation. Exit positivity is a finite rational sum; internal reachability is a graph search. At most N strict region decreases occur for each of at most $`2^{|\Theta|}-1`$ nonempty supports. Region decision takes $`2^{|\Theta|}`$ times a polynomial in the explicit finite state, action, model and rational input. With a fully listed support-indexed menu table the operations are polynomial per table entry, with the stated graph work. A succinct menu representation requires its own analysis. This bound excludes the threshold search, rational-expression sizes, statistical running time and controller memory; none is asserted small.

If all live models have common transition supports on every lawful pair, no proper support update occurs. All exit sets are empty, the support recursion is unused, and the criterion becomes the greatest fixed point of common-support safe reachability to self-verifying components. Replacing graph reachability by per-model almost-sure target reachability gives the same greatest fixed point: the latter operator is contained in the former, while at a graph fixed point uniform navigation, or the retained round-robin proof, reaches the required target with a geometric bound. Intermediate iterates can differ. A state forced to branch to a target or a bad trap has a target path but lacks almost-sure target reachability until viability removes the trap and its unsafe predecessors.

If the row, acceptance and menu depend only on the action and live support, regard the current state as the last observation. Inductively each *W*<sub>*C*</sub> is either all of S or empty, and $`\mathcal A_{B,S}`$ is exactly the set of actions with winning proper observation successors in §7.12. A progress action makes $`E_\theta(S)=S`$. Without progress, a qualifying component supplies a self-verifying action set by taking its used labels. Conversely, for any nonempty self-verifying action set with no θ-progress, take D to be the union of its θ-observation supports and use every action at every state of D. Every row stays in D, the union graph reaches each state of D from each other state in one step, and any initial state can enter D. Hence $`R_B(S)=S`$ exactly when every live model has progress or a self-verifying action set; otherwise it is empty. This is the recursive criterion already established in §§7.12–7.13. Their formal endpoint evidence does not by itself kernel-check this stateful theorem. [36–44]

#### Examples, boundaries and antecedents

A revealing initial action can send two models deterministically to different terminal states, each with an accepted singleton continuation. The initial state wins even when the whole-family self-verification condition at either terminal would fail. If one revealed singleton instead has no accepted continuation, the child-region test prohibits that action. Learning the model does not repair an irreversible losing successor. Support- and state-dependent menus must change to Γ(C,y) on the actual observed successor, not retain the old menu or consult an unindexed union of winning states.

A second example isolates navigation cost. At state 0 let candidate φ, under either action a or b, return to 0 with probability 1−η and reveal itself at state 1 with probability η, for rational η>0. Under θ both actions always return to 0. State 1 has a φ-good continuation; at 0 only b is θ-good. Then φ can win by revelation, and b supplies a θ-self-verifying component. A false φ-navigation attempt under θ never reveals φ or reaches its target, but every observed row differs. Once either action has *n*<sub>0</sub> samples the test rejects, which occurs within $`2n_0-1`$ actions for two actions. Untested uniform navigation would use the bad action a infinitely often. At η=0 the row distinction and revelation disappear; choosing incompatible acceptance requirements then makes the initial state losing. Exact zero versus positive probability cannot be replaced by a numerical tolerance.

Full rows are also essential. With one action, let θ₀ remain at 0 and accept there, while θ₁ stays at 0 with probability 1/2 and moves to its revealed state 1 with probability 1/2, accepting only at 1. Both terminal rows self-loop. Repetition succeeds, with zero bad count under θ₀ and mean bad count 2 under θ₁. The full rows at 0 differ, so its component is θ₀-self-verifying. Conditional no-exit rows coincide; substituting them would wrongly eliminate that target. Irreversible traps and identical transition laws with incompatible targets remain obstructions, and a single reachability pass cannot replace the state fixed point.

The model and tools have established antecedents. Chadès and collaborators' hidden-model MDP includes visible states and model-dependent transition and reward functions; its finite-horizon value-threshold result has a different objective and quantifier structure. [47] Support refinement, belief-restricted winning regions and common components occur in work on multi-environment MDPs, including Suilen, van der Vegt and Junges and the common observed-state parity formulation cited in reference 31. Those results retain their own objective hypotheses. [31,48] POMDP-lite likewise represents a family of visible-state MDPs indexed by a hidden parameter and studies Bayesian planning guarantees. [49] Duan and collaborators synthesize policies for asymptotically detecting a fixed MDP from its state-action history. Correct eventual action need not identify the model, while identification through infinitely many rejected probes need not give finite bad count. [50]

The concentration estimate is classical; the completed-event and augmented-state arguments supply the required physical-cost obligations here. The source's separate common-support regenerative and bounded-regret comparisons remain distinct evidence, as does its comparison with the later journal edition of the detection work. A later corrigendum alone establishes no mathematical correction to the result used here. These bounded comparisons neither establish priority nor prove absence of a published equivalent theorem. This section supplies ordinary proofs of the stated conditional claims, not a new kernel execution, recovered historical review seal, empirical validation or inference of understanding or normative authority from successful control.


#### Hidden priorities and recurrent fairness

The same finite model can attach an integer priority $`d_\theta(s,a)`$ to each state/action pair. The objective is that the minimum priority seen infinitely often is even. The model is fixed but hidden, and its priority values are not extra observation feedback. A policy is selected before the actual-model quantifier and must attain probability one under every initially live model. A supremum of success probabilities equal to one is a different statement. [56]

There is a direct parity version of the state-region criterion above. Preserve the support recursion, safe actions, internal edges and candidate exit sets. In a candidate φ-component, retain zero φ-exit probability, internal closure and strong connectivity. Replace the requirement that every matching model accepts every pair by

```math
\min\{d_\sigma(s,a):s\in D,\ a\in U(s)\}\text{ is even}
```

for every live σ whose full rows agree with φ on all used pairs. This includes φ itself. Let the target be the union of these components and take the same greatest reachability fixed point inside each support. Membership is equivalent to existence of a common lawful almost-sure parity policy. The statement permits arbitrary history memory; it supplies neither a finite expected odd-visit count nor a memory bound.

For necessity, parity is unchanged by deleting a finite prefix. The positive-history continuation argument therefore puts each used action inside the same safe region conditions. On a positive no-exit tail, the exact recurrent pair set is a zero-exit end component. Choose a finite positive prefix and kill at the first outside pair or support change, as in the preceding proof. Equality of full rows transfers the measurable event on which exactly those retained pairs recur. Each matching model must have an even minimum on that same set, or its transferred event would be a positive-probability failure. This supplies the parity target and the post-fixed-point inclusion.

The exact fixed-model continuation interface makes the restart in this necessity argument explicit. Histories in the provider are newest first: a future record t extends an old record h as t++h. Condition the original observed-history law on $`H_{|h|}=h`$ and read $`(H_{|h|+n}).\mathrm{take}(n)`$. For a positive-probability h, this whole infinite continuation law equals the canonical law of the policy that appends h, started at its latest observed state and using the common posterior private-seed law. The proof first establishes the actual extended-prefix probabilities, reconstructs every finite path prefix from its last history, and then uses uniqueness of the sequence measure. Equality of isolated time marginals without that reconstruction would not suffice. [Q250C-088] [Q250C-090] [Q250C-115] [Q250C-126]

With the same policy and seed law, two models whose full rows agree on E have identical complete killed-history laws: the first outside action's receipt and all later receipts are erased, while alive/dead flags retain the killing time. Consequently their original laws restricted to never leaving E agree on every measurable observed-history event. After h the same conclusion holds provided h has positive probability in both models; their old prefix rows may differ. The event used for parity is the intersection of never leaving E with **exactly** E as recurrent set, not mere containment in E. Restriction preserves original almost-sure properties, and finite-shift invariance identifies the continuation's action parity, so conditional success is derived rather than supplied as an additional assumption. This supplies an even attained minimum for a matching rival whenever that exact surviving recurrence event has positive mass. It neither normalises the never-leaving event to probability one nor assumes a conditioned process is iid or Markov. [Q250C-087] [Q250C-089] [Q250C-119] [Q250C-120] [Q250C-121] [Q250C-125] [Q250C-132]

For arbitrary private-seed policies, the formal lawfulness quantifier is: for each finite history with nonempty live support, almost every seed chooses a menu action whenever that history is action-compatible. It is equivalent to zero probability, under every initially live model, of each history followed by an illegal next selection; no receipt of that next action is conditioned on. A positive history has a positive row-likelihood factor, so cancellation recovers the seed-level condition, while a null history contributes zero. Compatibility, live-support concatenation and restriction to the common posterior prove lawful restart. This seed-almost-everywhere contract must not be strengthened to legality of every individual null-seed branch, nor weakened to a single chosen-model simulation. The deterministic constructed policies separately prove their all-compatible-history invariant. [Q250C-122] [Q250C-123]

For sufficiency, the navigation, empirical-row testing and conditional milestone estimates use transition rows and candidate target/exit reachability, not binary acceptance labels. They remain valid. In a matching operating component, uniform choice of its actions gives an uninterrupted finite irreducible chain in which every retained pair recurs almost surely. Intersect this full-measure recurrence event with the event of no later rejection; it is unnecessary to claim that the process conditioned on no rejection stays Markov. The actual recurrent minimum is then the even component minimum. A positive actual exit or a differing row terminates the phase almost surely by the inherited waiting and rejection bounds; a matching phase that later rejects contributes only a finite prefix. Each completed candidate cycle includes the true candidate, whose conditional chance of continuing to another cycle is at most the fixed allowance ε<1. Only finitely many attempts occur almost surely. Support can shrink only finitely many times, so a final matching operating phase persists and wins parity. Merely remaining somewhere in a valid component would not prove this: full-pair recurrence is required. [56] [Q250C-097] [Q250C-101] [Q250C-102] [Q250C-118]

The target computation also has an explicit finite pruning proof. For fixed B,W,φ start with all allowed pairs having zero φ-exit probability and compute maximal end components. In a current component D, if a row-matching model σ has odd minimum priority d, delete **all pairs at that attained minimum**, then recompute components, matching models and minima. Any valid subcomponent E⊆D still matches σ. No σ-priority in D is below d, so if E retained a priority-d pair its own minimum would be the same odd d. Such a pair cannot belong to a valid E. Every valid subcomponent therefore survives each deletion and remains inside some current maximal component. At stability each returned component satisfies every matching model's parity condition. Preservation and maximality make the outputs exactly the maximal valid components. Intersecting valid components have a valid union: a model matching the union matches each part, and the minimum of their two even minima is even.

<a id="pruning-across-intersecting-maximal-components"></a>

For a round that deletes bad pairs globally across all current maximal components, preservation needs one more containment step. If a protected valid component E meets a current maximal component D in a pair, the graph-component union property makes E∪D a component inside the retained universe. Maximality of D then forces E⊆D. Hence **every** maximal component capable of deleting a pair of E contains all of E, and the odd-minimum argument applies to that deletion as well. Choosing only one maximal envelope for E would leave this global-deletion case unproved. The exact `PruningKernel` uses this graph-union fact, finite cardinal maximization and the independently defined validity predicate; its powerset selector is an exhaustive reference, not the polynomial SCC implementation. [Q250E-143]

[Q250E-143]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d16d51d77c59f0538952e1401e105e699fd6d2648df3aa3db8dbf3c09888a253/PruningKernel.lean

The outer region reference has a different fuel bound. Its state-set descent stabilizes within the finite state count. Its support recursion is independent of excess fuel once the fuel is at least |B|: the allowed-pair test consults lower regions only for proper child supports, whose cardinalities are smaller. Strong induction on B therefore equates those child regions for any two sufficient fuel values, equates the stage operators, and identifies the bounded result with a fixed point using the canonical child regions. This is the support-recursion argument, not a bound on statistical running time. [Q250E-148]

[Q250E-148]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ca456e211d02a994192809bac318ae3a75684f163daf2f9037346b84517b347a/RegionAlgorithm.lean

Recomputation matters because removing one layer can reveal another odd minimum or a newly matching rival. Deleting all odd-priority pairs at once would be stronger and incorrect. The number of deletion rounds is bounded by the number of pairs, not by the largest numerical priority. Together with the outer region iteration and support recursion, this gives an exponential-in-model-count, polynomial-in-explicit-state/action/rational/priority-bit decision upper bound. It is a mathematical algorithm bound, not qualification of a production solver API or of its learning time. [56]

A forced cycle of priorities 2 and 3 wins while visiting priority 3 infinitely often. Thus general parity has no finite odd-visit guarantee. The exact eventual-good special case assigns 1 to bad pairs and 2 to good pairs. Assigning 0 to good and 1 to bad would allow infinitely many bad visits when good visits also recur. These distinctions are retained by the literal signed service in §§7.15–7.18; its separately proved compiled policy is not silently identified with the stage-local construction here.

One narrow obstruction explains why a hidden objective cannot simply be replaced by an arbitrary finite observable monitor. With a constant action and two full-support coin laws, a fixed finite deterministic monitor driven only by observed receipts has the same positive transition graph in both models and the same monitor priority labels. Its reachable bottom classes therefore cannot yield success probability one in one model and zero in the other. This does not rule out every reduction or an infinite-memory monitor. It is a boundary example, not a novelty argument. [56]

The original generated-policy providers distinguish a semantic witness from a law-preserving transformation. Necessity derives safe actions until a support exit from positive-history restarts, proves that the semantic region is postfixed, and uses strict support-cardinality induction together with finite descending state iteration to place it in the computed region. Sufficiency constructs one deterministic history policy with Unit seed, one finite-family separating tolerance and shared finite choices before the actual model is quantified. Thus an arbitrary measurable-private-seed winning policy entails existence of this deterministic witness; it does **not** entail equality of their action or history laws. Empty support has no computed winner. These are the original generated-region endpoints, not the later literal-body compiler's executable identity theorem. [Q250C-112] [Q250C-113] [Q250C-116]

In that generated controller, the all-compatible-history safety invariant holds for **every** Boolean rejection test, including arbitrary false positives. Statistical accuracy is needed for convergence, not for hard-menu licensing. The actual-run equations reconstruct the source labels from observed receipts, keep the global departure count, test the newly completed history, and clear retained components on support change or rejection. Once support is fixed, the index changes by zero or one; equal index preserves the retained component. The true-candidate non-rejection argument and the cyclic barrier then supply eventual phase constancy, after which an option-valued retained mode either stays empty or keeps one component. The latter arithmetic fact needs no finiteness assumption on the type of retained objects. Fair closed-set navigation and recurrent-row matching exclude the permanently empty mode and yield the stated parity result. [Q250C-095] [Q250C-098] [Q250C-104] [Q250C-105] [Q250C-106] [Q250C-107] [Q250C-108] [Q250C-128] [Q250C-130] [Q250C-133]

#### Posterior determinism as a law-preserving visible-state construction

A finite hidden-state system can meet the observed-state hypothesis through an exact information-preserving construction, provided its **actual joint kernel** is posterior-deterministic. Let Q be a finite hidden-state set, O an observation alphabet and A the actions. The supplied rational probability row is $`T(o,q'\mid q,a)`$, summing to one over (o,q′). Posterior determinism means that for each (q,a,o) at most one q′ has positive mass. Define

```math
p_o(q,a)=\sum_{q'}T(o,q'\mid q,a),
\qquad
\delta(q,a,o)=\text{the unique positive successor when }p_o(q,a)>0.
```

The successor is undefined at zero observation probability. Independent observation and next-state marginals cannot replace this joint kernel: two correlated positive pairs can determine a unique state after each observation even though their product marginals would not. The controller is not given q or the hidden initial state. [57]

Let Θ be the positive support of the initial distribution on Q, with k=|Θ|≤|Q|. Treat the initial state θ as a fixed hidden tag. A visible descriptor is a partial function f:Θ⇀Q, together with the last observation $`\ell\in O\cup\{\bot\}`$. Initially f(θ)=θ for each tag and ℓ=⊥. Given action a and new observation o, define the next descriptor by

```math
\operatorname{dom}f'
=\{\eta\in\operatorname{dom}f:p_o(f(\eta),a)>0\},
\qquad
f'(\eta)=\delta(f(\eta),a,o),\qquad \ell'=o.
```

For a defined tag θ, its visible transition row assigns mass $`p_o(f(\theta),a)`$ to (f′,o). Different observations yield distinct visible successors because the last-observation field is retained. This remains necessary when two observations happen to produce the same f′ but different likelihood evidence. The row is normalized and each positive entry is one original joint-kernel entry under posterior determinism. For an undefined tag, choose any normalized completion; that row will never govern an actual reachable history for that tag.

Induction on acquired histories proves the invariant

```math
B=\operatorname{dom}f,\qquad q=f(\theta)
\quad\text{for the actual live tag }\theta.
```

Initially it is immediate. After an observation, the actual tag has positive observation likelihood and remains, its unique next hidden state is the updated coordinate, and every other tag is retained exactly when its likelihood is positive. The live-support update is therefore precisely coordinate deletion. Distinct tags whose current coordinates merge remain distinct possible initial models; replacing the tag set by the image of f would be wrong. Menus may permit the original actions when the nonempty live support equals dom f and reject inconsistent pairs (B,f). From the designated start this guard neither removes an available action nor reveals hidden information. Arbitrary definitions on impossible histories and off-domain rows do not affect the reachable law. [57]

The complete acquired action/observation history computes the descriptor sequence. Conversely, the last-observation field recovers each original receipt from a consistent visible history. These history maps are inverse on reachable histories. Pulling a causal policy through either map preserves the same independent private seed and the same available information; one does not replace a history policy by a policy using only its current descriptor. For every fixed initial tag and seed, induction gives the same selected action and the same next observation mass at every finite history. Finite cylinder equality extends to the full path laws. Equivalently, coupling the receipts path by path makes posterior determinism recover the hidden trajectory from the fixed tag and shared history.

In particular, if the original bad indicator at action index n is $`b(q_n,a_n)`$, assign the lifted indicator $`b(f_n(\theta),a_n)`$. They agree **before** receipt n+1. Initial action n=0 is included with no dummy-action shift. The entire indicator stream, all finite sums, total count, extended expectation and eventual-acceptance event are preserved. Model-dependent priorities are transported in the same way, preserving the full hidden priority stream and its min-even parity event without revealing those priorities to the policy. [56–57]

For a prior with finite positive tag weights wθ, the same policy has prior-almost-sure success exactly when it succeeds almost surely under every positive tag. It has finite prior expected count exactly when every corresponding conditional expected count is finite. Writing $`w_{\min}=\min_\theta w_\theta>0`$, the quantitative relation is

```math
\sum_\theta w_\theta C_\theta
\leq\max_\theta C_\theta
\leq\frac1{w_{\min}}\sum_\theta w_\theta C_\theta.
```

Zero-prior states are not added as adversarial environments. If an initial observation is genuinely supplied before the first action, condition on each of its positive-probability branches and use the corresponding posterior initial tags; this does not shift the action clock. It supplies no authority to invent an initial receipt or expose the hidden tag when the original interface does not do so.

For n=|Q| and m=|O|, there are at most $`(n+1)^k(m+1)`$ visible descriptors: each tag has n defined images or is absent, and the last observation has m+1 possibilities. Dense transition rows and explicit consistency menus have polynomial size in this descriptor count, times an exponential-in-k factor. Nonzero probabilities retain the original rational bit size. Substituting into the finite observed-state procedure yields a singly exponential upper bound in the original explicit input encoding: attained almost-sure hidden co-Büchi winning, and the parity extension, lie in EXPTIME for this finite rational posterior-deterministic class. This is an upper bound, not a matching lower bound or an efficient learning-time theorem. In the co-Büchi instance the criterion also supplies existence of a finite expected bad-count witness. The separately proved deterministic scheduler can be transferred through the same history maps, with its unbounded empirical memory. General parity carries no odd-visit cost conclusion. [56–57]

Attainment remains essential. Consider two fixed full-support coin models with distinct parameters, for example 1/3 and 2/3. A policy can wait for a sufficiently long finite sample and then make an irreversible commitment to one model, with error probability as small as desired. Assign priority 1 to waiting and an incorrect committed sink, and priority 2 to a correct committed sink. Almost-sure success would require a finite correct commitment. Some finite commitment event then has positive probability in one model, and full support together with the common seed/history transfers positive probability of that same commitment to the other. There it is wrong forever. No common almost-sure policy exists although the supremum of success probabilities is one. Moreover, any positive probability of an infinitely bad sink makes expected bad count infinite. High-probability commitment is therefore not a finite-expectation witness. [57]

The reviewed descriptor idea credits earlier initial-tag and state-tuple constructions. Its cited observation-compatible parity and reachability-value approximation results retain their own objective and normalization hypotheses; they are not automatically the hidden co-Büchi statement proved through this crosswalk. The full-law, hidden-priority and clock arguments above make the necessary distinctions explicit. They establish ordinary mathematical consequences at the stated finite-model scope, without restoring vanished formal closures, qualifying compiled runtime behavior, establishing field-wide priority, or deriving understanding or normative authority from a controller.


### 7.15 A finite signed service for common lawful parity policies

Section 7.14 characterises eventual restoration in a finite class with a fixed hidden model and fully observed states. A related finite service supplies both positive policy certificates and complete negative evidence for a more general parity objective. The *Mathematical Companion*, entries 12–13, separates two additions to the inherited positive-certificate theorem: exhaustive finite syntax with checkable refutations, and an executable controller compiled from the **literal accepted body**. The theorem about the returned controller concerns its actual observation-history law. It is not obtained by replacing that controller with a previously known successful policy. [Finite signed certification and direct compilation][signed-companion]

#### 7.15.1 The exact finite input and the semantic question

Fix positive integers q,n,k. Models are $`M=\mathrm{Fin}(q)`$, observed states $`S=\mathrm{Fin}(n)`$ and actions $`A=\mathrm{Fin}(k)`$. The actual model σ is fixed but hidden. A valid input supplies exact rational rows

```math
p_\sigma((s,a),y)\geq0,\qquad
\sum_{y\in S}p_\sigma((s,a),y)=1,
```

natural priorities $`d_\sigma(s,a)`$ and sparse menus $`\mathrm{menu}(B,s)`$ for surviving model sets B. Validity includes the positive dimensions, all array shapes, in-range and distinct sparse keys and members, and every row's normalisation. Absent menu entries are not filled in by guesswork. The full interpretation and coding data are part of the input's structured identity.

For an observed action pair $`e=(s,a)`$ and receipt y, define

```math
L_B(e,y)=\{\sigma\in B:p_\sigma(e,y)>0\}.
```

The observed history determines the current state and live support by retaining exactly the initially possible models that give every acquired transition positive probability. A nonempty $`L_B(e,y)`$ equal to B is an internal receipt; any nonempty proper subset is an information-bearing support reduction. The policy knows the history and supplied rows, but has no actual-model argument.

The question is whether **one common lawful policy**, selected before quantifying over $`\sigma\in B_0`$, achieves parity almost surely for every initially possible model. Lawfulness means menu compliance on every feasible, policy-compatible finite history with nonempty live support. Parity means that the minimum model-dependent priority among the state/action pairs occurring infinitely often is even. The probability law is the original Markov observation-history law induced by that policy and the actual row family.

This differs from a hidden-state partially observed process: the physical state is fully observed. It also differs from a changing hidden model, adversarial sure-winning play, and an objective that demands success by a fixed finite deadline. Empty initial support and invalid input are separately rejected admissions, not negative certificates of the same well-posed policy question. The source supplies typed finite starts; it does not thereby supply an external wire parser.

#### 7.15.2 What the positive syntax actually certifies

An accepted body is a finite list of nodes with distinct nonempty support keys. A node for B contains a retained state set W, an allowed pair set D, and exactly one obligation for each $`(s,\theta)\in W\times B`$. Every pair in D starts in W and uses an original permitted action. Its closure obligation covers **every** receipt with nonempty $`L_B(e,y)`$:

- if the support remains B, the next state belongs to W;
- if it shrinks, the body contains a child node with exactly that smaller support and containing that next state.

A rare adverse receipt cannot be omitted merely because an existential exit witness names a more favourable one. Every listed node, including a node not reached from the requested start, remains subject to the body's validity checks.

An obligation at (s,θ) supplies an internal, action-witnessed path to one of two targets. The first is an allowed pair with a θ-positive receipt that strictly reduces support. The second is an entry state of a submitted component $`E\subseteq D`$. The path checks every stored edge and its declared endpoints. It certifies possible internal reachability, not a power to command a stochastic receipt or a bound on the time taken by a policy to reach the endpoint.

A component is a nonempty end component for the common internal-successor relation, with explicit root and linking paths proving closure and strong connectivity. It has nonempty internal successors. For its selected candidate θ, every positive successor of a pair in E is internal, so that candidate has no support exit there. Finally, for every rival $`\sigma\in B`$ whose **full numerical transition rows** match θ on all pairs of E, the attained minimum of d<sub>σ</sub> on E is even.

That last condition permits a candidate to be globally wrong while operationally adequate on the retained component. Equality of positive supports alone would be insufficient: persistent frequencies can distinguish rows with the same support, and the controller uses those frequencies. Nor is it enough that the component is good only for the candidate; an observationally indistinguishable actual rival must satisfy the same parity condition.

The inherited positive theorem states that acceptance of some body is equivalent, for this exact valid input class and initial query, to common lawful almost-sure parity-policy existence. Its policy-to-certificate direction also covers the source's arbitrary measurable private-seed policies. The new signed service uses that theorem at this declared scope; it neither reproves a different game semantics nor infers a finite-body certificate from a finite simulation trace.

The bounded-path provider earns the syntax bound without substituting a reachability oracle for local checks. It first extracts an action witness from each edge of a reachable walk. On extending a simple witnessed walk, a repeated endpoint is handled by retaining the already witnessed prefix ending there; a fresh endpoint is appended with its actual action/receipt edge. The visited-state list stays duplicate-free, so its length is at most the number of states, and the edge count is at most one less. Equal endpoints use the empty path. This is proof-side completeness for the locally checked start, end and every literal edge, not an online stochastic travel-time bound. [F939A-793]

`PathEdgesMutant` retains the start, endpoint and length tests but replaces the edge-validity conjunct by `True`. With at least two states it can then admit a one-step jump in an empty allowed graph. The retained local `Edges` definition does not help if the actual acceptance predicate omits it. The mutant is a rejection target, not another accepted reachability provider; no compiler rejection was newly obtained here. [F939A-766]

[F939A-766]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d222268e08b6a8960dd349b9b20dd00c2ed53ec1805061b10ddfe915860da41e/PathEdgesMutant.lean
[F939A-793]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d8e26f21fa37cd8ddf250ab9b440a1b25da481d201e66f3913ce822620e799f8/CertificatePath.lean

#### 7.15.3 Exhaustive finite syntax without replacing the submitted body

Finite semantic state alone does not justify a finite search over arbitrary proof syntax. The source derives explicit syntax bounds from the unchanged positive checker. An accepted path has at most $`n-1`$ edges. Component link lists have no repeated state keys and length at most n. Node obligation lists have no repeated state/model keys and length at most $`nq`$. Distinct nonempty support keys bound the body length by $`2^q-1`$. These bounds apply to the actual admitted syntax, including unused nodes.

For a finite alphabet X and bound b, enumerate all lists of length at most b by the recursion that includes the empty list and extends every shorter list by every element of X. This enumeration retains arbitrary orders and repeated elements. Enumerating all sublists of a fixed finite list gives every finite subset without a choice operation. Assemble the domain in syntax order: paths, links, components, exit or component witnesses, obligations, nodes, then bodies. The checker filters the many malformed or redundant candidates.

Every accepted literal body occurs in this domain. The coverage argument uses its own checked bounds and membership facts; it does not first sort it, shorten its paths, discard unused nodes, identify isomorphic components, or replace it with a semantically equivalent body. This literal coverage is what later lets a negative certificate exclude an arbitrary accepted positive body.

The size can be made explicit. Put $`S(m,b)=\sum_{i=0}^{b}m^i`$ and define the following elementary enumeration-scale expressions:

```math
\begin{aligned}
P&=nS(kn,n-1),&L&=nP^2,\\
C&=2^{nk}nS(L,n),&H&=P(n^2k+nC),\\
Z&=nqH,&N&=2^q2^n2^{nk}S(Z,nq),\\
M&=S(N,2^q-1).
\end{aligned}
```

They expose the growth of nested list and subset enumeration; the source does not present them as a separately formalised tight cardinality theorem. In its one-state, one-model, one-action finite example, the successive enumerated lengths are 1,1,4,5,5,48,49. These are source-reported historical counts. The general positive result is finiteness and literal coverage, with potentially enormous cost.

#### 7.15.4 Refuting a reconstructed finite formula

For each exact input, query and body, reconstruct a Boolean formula from constants, signed atomic tests, conjunction and disjunction. A bounded universal is a conjunction with empty value true; a bounded existential is a disjunction with empty value false. Negation is pushed to literals by exchanging conjunction and disjunction and flipping signs.

The atoms are closed finite tests: exact rational and natural comparisons, finite membership, order and the declared structural conditions. They do not include the aggregate positive checker, a body-validity oracle or the semantic winning predicate as a black box. The formula explicitly expands dimension and array checks, sparse-key validity, row conditions, layout, all node obligations, all positive-receipt closure, strict child support, paths, component row matching, attained even minima and the requested start. Conditionals are represented by the appropriate two implications, so both branches are accounted for. The reflection theorem is

```math
\mathrm{eval}(\mathrm{positiveFormula}(I,c,B,s))
=\mathrm{check}(I,c,B,s)
```

for **all** inputs, not merely valid ones.

A refutation is a finite syntax tree dual to this formula. A false constant or false literal has a leaf. A false conjunction has a refutation of a designated false child. A false disjunction requires refutations of both children. The checker rejects mismatched formula and refutation shapes. Induction proves soundness: an accepted refutation entails that its formula evaluates to false. A structural recursive procedure gives the converse, returning a refutation exactly when the formula is false. No excluded infinite search occurs in this construction.

The receiver reconstructs the formula from the bound input and body. Accepting a submitted list of convenient atomic truth values would not establish the same theorem: those values could describe a different problem. This is why the finite refutation mechanism and the exact source-input binding are both required.

#### 7.15.5 A complete negative certificate and a terminating solver

A negative certificate binds the entire original input, initial support and state, including interpretation and authority-bearing data already present in that input. Reconstruct the complete ordered body domain $`c_0,\ldots,c_{m-1}`$. The negative packet must supply exactly

```math
(0,r_0),(1,r_1),\ldots,(m-1,r_{m-1}),
```

where r<sub>i</sub> refutes the reconstructed formula for c<sub>i</sub>. Validation advances through the expected indices and requires both lists to end together. Omission, duplication, reordering, an extra entry, or a refutation for a different formula is rejected.

**Signed correctness.** An accepted negative packet excludes every accepted positive body. If no positive body is accepted, a negative packet exists and can be constructed.

**Proof.** If a positive body were accepted, literal coverage would place it at some index in the reconstructed domain. Reflection makes its formula true, while the accepted indexed refutation makes that same formula false. Conversely, if all domain bodies fail, reflection makes every reconstructed formula false. The finite refutation procedure supplies its refutation; collect them in the prescribed index order. $`\square`$

Combining this exact finite result with the inherited semantic equivalence gives a negative answer precisely when no common lawful almost-sure parity policy exists, for the valid nonempty query. The inherited reduction from arbitrary measurable private-seed winning policies to positive certificates makes the negative result exclude those policies too. It does not assert that an adversary can force failure on every run, that failure must occur within a fixed horizon, or that the negative certificate is compact.

The solver first checks the declared input and query admissions. It then searches the finite domain in order, returns the first accepted positive body if one occurs, and otherwise constructs the full negative packet. It mathematically terminates. The nested enumeration scale provides no practical deadline or claim that a large negative packet can be produced with available resources.

On the positive branch, the compiled service returns that literal accepted body together with the direct controller described next. Its correctness includes equality to the policy constructed from the actual body and the original actual-history-law theorem for that policy. Returning some extensionally related successful policy without this binding would be a weaker result.

<a id="third-cohort-b-literal-certificate-controls"></a>

The exact-index obligation has a particularly small mutation test. `SkippedIndexMutant` replaces each submitted index by its position in the received list before calling `indexedCheck`. With two submitted entries both numbered zero, this laundering fabricates indices zero and one. Its final guard demands rejection, contrary to what the mutated preprocessing permits. The unmodified index check must consume the supplied indices, not reconstruct a compliant declaration in their place. This is a source-specified failing mutation, not a newly observed test failure. [T750B623]

The path and enumeration controls distinguish literal evidence from its target relation. An overlong cyclic walk can genuinely reach the endpoint and still fail the admitted path-length bound, even when another short witness exists. Changing the stored start, endpoint or a used edge invalidates that particular witness; enlarging the allowed set preserves it. At the smallest dimensions, a valid unused node remains in the enumeration, whereas an invalid unused node rejects the whole body. These facts support the literal-coverage argument above rather than an algorithm that silently repairs or discards inconvenient submitted evidence. [T750B584] [T750B598]

[T750B584]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9bfe96341b130524ee86c4706bc2e996396ff471f3c03e183928d0c2e74825c5/PathControls.lean
[T750B598]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a1c782816cd0c906fc191e7b29d0777c67a4a18432520b63ad08b8183c6ffe78/EnumerationControls.lean
[T750B623]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a988f2558354481f0e13d920d78e3f19cb7de2ee728e72d4d2e3d67bc94a2470/SkippedIndexMutant.lean

### 7.16 Compiling the literal certificate into a common controller

#### 7.16.1 The local stage family

From the submitted body c, form $`W_c(B)`$ and $`D_c(B)`$ by finite unions over nodes with key B. This definition is total even for malformed lists with no matching node or several matches. Acceptance supplies the unique-key fact, so on an accepted body these projections are exactly the stored sets.

For candidate θ, let $`\mathrm{Pool}_c(B,\theta)`$ be the list of components literally occurring in its target obligations, retaining submission order. Let $`T_c(B,\theta)`$ be the union of their used states, and let $`Q_c(B,\theta,s)`$ select the first listed component containing s, with an empty default when none exists. These are terminating list operations. They do not call the old winning-region algorithm or search all mathematically qualifying components.

The derived stage interface contains only local facts: available actions at retained states, original-menu inclusion, closure under all positive live receipts, qualification and current-state containment of selected components, and target-or-exit reachability. It contains no field that assumes policy success, lawfulness, fairness or convergence.

Availability follows directly from an obligation at (s,θ), choosing any $`\theta\in B`$ for this proof. A nonempty path supplies its first allowed action. If the path is empty, its exit endpoint supplies an allowed pair at s, or its component endpoint is a used state of a nonempty component contained in $`D_c(B)`$. This proof-side choice is not an actual-model input to the program. Likewise the obligation itself supplies either a reachable candidate-positive proper exit or a path to an entry in the **submitted** target pool. No larger solver-generated target set is substituted.

#### 7.16.2 The actual history recursion

The compiled policy is deterministic, with a singleton seed space and its Dirac measure. Its arguments are the valid input, initial support and state, and literal body. Validity supplies dimension evidence and a normalised kernel; it supplies no policy-success assumption. The policy reconstructs from its finite history:

- the current observed state and surviving support B;
- a natural phase index r;
- either no retained component or a retained pair set E;
- global source-departure, pair-use and pair/receipt counts.

All recursions on a finite supplied history terminate. Histories and natural counters may grow without a fixed memory bound. Explicit index-zero fallbacks make the program total when a projected action set is empty; the accepted-body safety proof shows that those fallbacks are not used on admitted compatible histories.

The current candidate is the rth cyclic element of the finite ordered support B. Before choosing an action, retain the existing component if there is one. Otherwise, if the current state belongs to $`T_c(B,\theta)`$, select $`Q_c(B,\theta,s)`$; if not, remain in navigation mode. In navigation, cycle through the actions of $`D_c(B)`$ departing from the current state. In operation, cycle through the corresponding actions of E. For a nonempty ordered action set F, the selected position is the global departure count from that state modulo $`|F|`$.

These departure counters are **never reset** at a phase change, support change or component selection. After action a and receipt y, compute $`C=L_B((s,a),y)`$ and update in this order:

1. If $`C\ne B`$, reset the phase to zero and clear the component.
2. Otherwise, if the empirical test rejects the old candidate at the old phase index, increment r by one and clear the component.
3. Otherwise, if a retained component was exited, increment r by one and clear it.
4. Otherwise retain the memory.

Normalisation at the new observed state occurs before the next action. Giving support change priority prevents reuse of a stale component or candidate after the information state changes. The source implements a pure history recursion; this ordering is its mathematical case distinction and does not assume stateful side effects in the empirical test.

#### 7.16.3 An exact rational test without true-model knowledge

Collect all strictly positive coordinate differences

```math
|p_\sigma(e,y)-p_\theta(e,y)|,
\qquad \sigma,\theta\in B_0, e\in S\times A, y\in S.
```

If this finite set is nonempty, set ε to half its minimum; otherwise set $`\varepsilon=1`$. It is positive and strictly below every nonzero row-coordinate gap. Identical rows require no artificial separation.

For the acquired source-labelled history h, let $`N_e(h)`$ count uses of pair e and $`N_{e,y}(h)`$ count its receipts y. Define the exact rational frequency $`f_{e,y}=N_{e,y}/N_e`$, with zero-denominator value zero. Reject candidate θ at phase r exactly when

```math
\exists e,y\quad r\lt{}N_e(h)
\quad\text{and}\quad
|f_{e,y}(h)-p_\theta(e,y)|\geq\varepsilon.
```

The count gate matters. A pair sampled only finitely many times may retain a misleading early frequency forever; at sufficiently late phase indices its bounded count no longer triggers rejection. For infinitely sampled pairs, the row law makes frequencies converge to their actual values. The tolerance is derived from the finite supplied model family and uses no hidden knowledge of the actual model.

The implementation counts with natural numbers and computes rational frequencies. The proof identifies their real casts exactly with the inherited history-symbol masses and the real-valued test. It does not replace the executable rational comparison with an idealised asymptotic test.

#### 7.16.4 Lawfulness is a finite-history invariant

On every compatible feasible finite history with nonempty support, the current state remains in $`W_c(B)`$. A retained component is a qualifying component for the current candidate and contains the current state. These claims are proved by induction on history length. The submitted menu inclusion makes the chosen action lawful. All-receipt closure sends a same-support receipt to a retained state and a support-reducing receipt to its exact submitted child. The update order clears memory before applying the new support's normalisation. Qualification and containment justify component actions; availability justifies navigation actions. Therefore the total program's empty-set fallbacks are unreachable on these admitted histories.

This safety proof does not require that the empirical test is already accurate. A temporarily mistaken candidate still chooses only permitted actions and remains within the submitted closure conditions. Exact history erasure and reconstruction identify the executable counts with the actual departure, pair and receipt counts. The resulting history policy is measurable and lawful for the original finite-history definition, rather than merely lawful on one probability-one set under a chosen model.

#### 7.16.5 Stabilisation and parity under the actual law

Fix any actual $`\sigma\in B_0`$. Work on the full-measure event supplied by the inherited probability theory: acquired receipts have positive actual probability; every repeatedly used pair sees each actual positive successor repeatedly; and empirical rows converge whenever the pair is sampled infinitely often. These statements apply to adaptively selected actions under sequential consumption of the primitive random inputs. No independence of the random sample count is assumed.

The actual model remains in every live support, which can strictly shrink only finitely many times. Thus the support eventually stabilises at some nonempty B containing σ. Global departure cycling is fair whenever a state is visited infinitely often in a fixed final mode: after an arbitrary initial offset its count traverses every residue modulo the fixed action-set size infinitely often.

A useful stronger quantifier behind the row test is available without conditioning on an adaptive sample count. For positive ε, simultaneous convergence of the finitely many primitive row tapes gives one probability-one event on which a finite random K makes every acquired estimate accurate at every physical time and for every policy whenever that pair has consumed at least K entries. The history frequency equals the raw frequency at the actual consumed count pathwise. Accordingly every adaptive deviation beyond a deterministic count N is contained in the all-pair, all-symbol raw-tail deviation event. Its probability decreases to zero. For any finite model family there is one deterministic schedule $`N_k\ge k+1`$ whose raw-tail errors are at most $`2^{-k}`$ under each model, with total at most 2. This schedule is existential: this provider proves neither a computable nor a logarithmic burn-in rate. The literal controller instead uses its fixed separating ε and the gate count>phase; a recurrent mismatching row is eventually rejected at every fixed phase index. [Q250C-092] [Q250C-093] [Q250C-129] [Q250C-131]

There is a finite threshold K after which the true model cannot be rejected at any phase $`r\geq K`$. For every infinitely sampled pair, convergence puts all frequencies strictly within ε of the actual row after a finite point. For every finitely sampled pair, choose K above its final count. Finiteness of the pair and receipt sets lets one choose a single threshold and time for all of them. In a true-model component, the candidate's no-exit condition also prevents component exit once support is fixed.

After the last support reduction, the phase is nondecreasing and changes only by one. Choose a sufficiently late cyclic index $`j\geq K`$ whose candidate is the actual model. If the phase reaches j, neither rejection nor component exit can increase it. It cannot jump over j. Thus the phase is bounded and eventually constant. This barrier argument proves stabilisation without assuming that the eventual candidate must be the actual model.

Let R be the nonempty set of state/action pairs occurring infinitely often after the support and phase have stabilised. If a recurrent pair had a candidate row differing from the actual row, a differing coordinate would have a gap at least $`2\varepsilon`$. Its empirical frequency converges to the actual coordinate, and its count tends to infinity, so the fixed-phase rejection test would eventually fire. This contradicts phase stability. Therefore candidate and actual rows agree in full on every pair of R.

Suppose navigation persisted forever. Cycling makes all allowed actions at each recurrent state recurrent. Positive-successor recurrence then propagates recurrent membership along each internal submitted path starting there. The target-or-exit obligation yields either a candidate-positive proper exit or a submitted target state. In the first case row agreement on the recurrent exit pair makes that receipt actual-positive; it must occur, contradicting stable support. In the second case the target state recurs and normalisation selects a component, contradicting permanent navigation. Hence operation is eventually entered.

In stable operation, recurrent pairs lie in the retained component E. Fair cycling includes all component actions at recurrent states. Closure and positive-successor recurrence propagate recurrent states along the internal links; strong connectivity therefore makes every used state recurrent and every pair of E recurrent. Thus $`R=E`$. The full-row agreement already proved now holds on all of E. Its rival-robust parity clause applies to the actual model and makes the attained minimum of d<sub>σ</sub> on R even. This proves almost-sure parity for this σ, and the same compiled policy works for each $`\sigma\in B_0`$.

The formal chain transports the primitive random-input argument to the pair law and then, by the actual history pushforward identity, to the original observation-history law of the returned policy. It does not merely exhibit another policy with the same informal description. No finite-memory, expected-time, finite-error-count or deployment theorem is added by this proof.

### 7.17 How the signed service meets the earlier restoration theorem

The common finite-model setting does not make the objectives identical. General parity permits infinitely many visits to some undesirable pairs: priorities 0 and 1 recurring together still have even minimum. To express the earlier eventual-good objective exactly, assign priority 1 to a bad pair and priority 2 to a good pair, separately for each model. In a finite pair space, the minimum recurrent priority is even exactly when bad pairs occur only finitely often. This provides the precise co-Büchi instance of the parity service. Assigning priority 0 to good pairs and 1 to bad pairs would instead allow recurring bad pairs whenever a good pair also recurs.

When the input class, menus and bad-pair interpretation are identical, the signed service consequently decides the same **existence** question in this instance. Section 7.14's stronger existence equivalence also supplies a policy with finite expected bad count. It does not follow that the particular direct policy of section 7.16 has that expectation bound. Its proof establishes the actual returned policy's almost-sure parity, and the source explicitly transports no cost theorem. Likewise the earlier stage-local fresh-count implementation and this global-count implementation need their own fairness and convergence arguments; neither is declared correct merely by renaming the other.

The negative renewal results in [Measure, computability and finite warrant](measure-computability-and-finite-warrant.md#91-finite-success-and-an-indefinitely-continuing-policy) use an unbounded effective history tree and a different service. They coexist with the present finite syntax, exact rational input and finite exhaustive decision procedure. Finite local success is not generally enough for indefinite policy existence; a valid positive body here supplies much stronger closure, reachability, discrimination and recurrent-objective premises. The complete negative branch comes from the exact finite syntax bounds and reflection, not from a generic assertion that all infinite behaviour is finitely decidable.

### 7.18 Formal evidence and remaining implementation boundaries

The single public companion body reports separate author and independent acceptance for fourteen direct-controller modules and seven signed-search modules. Its historical fresh replays compiled 95 inherited modules and these 21 additions, for 116 production modules, without reusing project objects while reusing pinned external dependency objects. The reported 172 Lean invocations consist of 160 positive and 12 rejection invocations. The safe-declaration audit reports 1,309 declarations, the computational dependency audit 1,467 entries, and the separate external-object inventory 6,646 identity-checked reused objects. These figures describe the source's recorded replay; none is a fresh execution in this composition.

The source's historical mutation controls test distinct parts of the negative certificate. They include removing required indices, duplicating or skipping indices, reversing their order, supplying out-of-range or additional indices, forging a refutation of a true atom, and substituting an unjustified aggregate leaf. Other controls alter input, source or query bindings. Larger direct formulas exercise missing-child, complete-row-agreement and attained-even-minimum failures. Deliberately weakened coverage or index implementations are themselves subjected to the rejection controls. These named checks preserve the separate obligations of exhaustive coverage, local refutation and exact request binding; none has been newly executed or reconstructed here.

That development is separate from the companion's 111-module core. Adding the numbers does not produce one newly built 132-module library, and project-object rebuilding is not a cold rebuild of dependencies. The direct controller's original default-heartbeat compilation and finite controls support their reported interface, not a verified wire parser, machine-code correctness, a physical controller or a resource-bound guarantee. The positive calculus's semantic equivalence and general probability lemmas remain inherited results; the new source contribution is exhaustive signed certification and the theorem about the literal body's actual compiled policy.

#### Exact-archive acceptance and dependency identity

The detached signed-service description adds an exact-archive distinction to the theorem scopes above. It binds candidate-v2, an unchanged 127-file Ninth predecessor plus the separate extension and its wrapper evidence. Its author and independent runs are reported to have used fresh paths containing spaces, unrelated working directories, poisoned caller search paths and absent isolated outputs. The recorded wrapper suites distinguish 23 unit tests from nine author and eleven independent actual-archive boundary cases; 191 copy-custody rows retain their own source-inclusion and exclusion roles. These are historical reported checks of that particular archive, not additional mathematical modules or fresh executions of this chapter. [Q250B-081] [Q250B-083]

The preserved candidate-v1 attempt is more specific than either success or theorem failure: disconnection interrupted it after the 120-call Ninth stage and 43 successful extension calls, leaving its original RUNNING receipt unchanged. The accepted v2 restart changed custody entries, the package manifest and its embedded digest, but the description reports no mathematical or control-source change. A later accepted exact replay can resolve the deliverable's verification status without rewriting the earlier incomplete attempt as a success. [Q250B-081]

For the signed replay, the sealed dependency-object census is environment-specific: 6,641 official cached objects plus five locally built cache-client objects, with source revisions and the official Lean executable pinned. Clean checkouts, absence of unexpected Lean sources and project-name object collisions, and before/after object identities are separate gates. The exact package-registration boundary permits resolved dependency symlinks while protecting their targets from output writes; this does not relax the source package's refusal of symlinks. An independently source-built dependency object with different bytes needs its own justified environment receipt rather than silent relaxation of that sealed gate. [Q250B-082] [Q250B-083]

The recovered core's targeted dependency cache is not the signed package's complete sealed closure, and the later source-build assurance for the required core subset does not extend automatically to signed116. Its fresh project builds continue to rely on identity-checked cached dependencies and the declared compiler/runtime/native primitive trust. Conversely, source-only verification of the signed package checks census and hashes, not the full positive/negative controls, proof audits or code generation. The archive digest supplied separately binds the manifest and entry point; a manifest distributed with the same bytes is not an independent authenticity authority. No partial replay, embedded success string or C-generation record supplies linked-binary execution or actual authority. [Q250B-057] [Q250B-058] [Q250B-082] [Q250B-083]

[Q250B-057]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6d02ceae10a28d68cc138a4793dbd87c2147b8ac786745a6602a023fc751ed5b/README.md
[Q250B-058]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9fbe1d74a790020862fb39a37cb2951131d63f09779e60c9dd57b1c77188408/VERIFICATION_GUIDE.md
[Q250B-081]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/581e4add3d991511f2a1f5b8372a109dd40a548754c518fc80edc6315bc25e83/SIGNED_SERVICE_VERIFICATION_v1.md
[Q250B-082]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f6f9db7e95689421981d0aa834fbd40802f29640f2d83172e3cd3a0fe0ae3edd/DEPENDENCY_TRUST.md
[Q250B-083]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9366801f890e9c14f1b97d2456fa664b3ccd92dbf585c89443adb0ae111fe4ff/README.md

<a id="signed-service-replay-and-probe-scope"></a>

The frozen-source review and full package replay support different receipts. `SOURCE_REVIEW_SUMMARY` reports that its 21-module review reused 96 individually identified predecessor objects; it expressly does not claim the fresh 95+21 source replay. It also separates 1,309 safe declarations from 1,856 compiler/elaborator unsafe artifacts and preserves a corrected audit-harness diagnostic without counting it as a successful proof attempt. The reported source review does not automatically validate the top-level wrapper, package census or corruption controls. [Q250E-172]

The retained `replay.py` specifies the additional full-replay contract: exact file census and hashes, refusal of optimized Python, exclusion of project objects from dependency libraries, a fresh predecessor run, and unchanged package and dependency identities afterward. Its `--verify-only` branch explicitly stops after package checks. A rejected mutant counts only when exit code1 accompanies exactly the intended native-guard diagnostic, not an unknown import, type error or timeout. These are conditions imposed by the wrapper's source, not newly observed execution results. [Q250E-171]

The mutation derivation preserves the original acceptance gate while replacing the compiled submitted family by an empty family; another mutation replaces the actual history departure count by zero. Their guards therefore distinguish literal-witness use and fair cycling from mere checker acceptance. The rational-test mutations separately replace the strict count gate by a nonstrict one and truncate only the frequency history while retaining full counts. Unique source anchors and recorded derived digests identify these particular probes; the presence of a derivation script is not evidence that its probes ran or failed as intended. [Q250E-173]

The six small `Red` files are declaration-interface requests for enumeration bounds, indexed coverage, formula reflection, refutation, the signed solver and the compiled solver. Despite their names, they contain no negative example whose rejection was observed. `SignedAxioms` likewise requests axiom reports for named bounds and endpoints without containing the reports. Retaining these commands preserves inspection targets, not additional proofs, successful audits or independent replays. [Q250E-174] [Q250E-175] [Q250E-176] [Q250E-177] [Q250E-178] [Q250E-179] [Q250E-180]

[Q250E-171]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2935baf06457e5c12ed127be50417c3a0bb3088754b4fd6df8c551635b0bab26/replay.py
[Q250E-172]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9f57394de9d67856fa2e9424c0fa320d90d6c80fdd65989443dc55f393e8c629/SOURCE_REVIEW_SUMMARY.md
[Q250E-173]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/64b0e67aeee09bbb27dffac097523d6425caf0a72e8cab141f5b84f188bc57fe/derive_mutations.py
[Q250E-174]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/800d4898e11890458ae553af2fba3459e08375c5d4651b8e9d0d62b22463af15/EnumerationRed.lean
[Q250E-175]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e1ace3cbe65ba1398963557a60f136f11e5ddaa1d389e660070be7bd4e866ed4/IndexedCoverageRed.lean
[Q250E-176]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1df069295afc84a23adc98ae7193dabbbdb798b36ea3bb1f3d4603332d6ccb6e/PositiveFormulaRed.lean
[Q250E-177]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/578400fab2b49c0704ea010d2a34923c941417d5483c40022c2089523a59d476/RefutationRed.lean
[Q250E-178]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ef4a13492e491c64d0688978a786f340406c7ae6d390d165268958f938938dc9/SignedAxioms.lean
[Q250E-179]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f44f5fbe2d570209edf225964fd22cf84d3a3bca73f7f382c17d2c11e0d0e49a/SignedControllerRed.lean
[Q250E-180]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4cb50594280758198066ac8dfe89cc6358a3c7c4bfa62bbd93e81fe92105dc71/SignedServiceRed.lean

#### Exact solver, controller and audit interfaces

The finite signed service has four outcomes, not two on arbitrary input: invalid input, empty support, a literal positive body, or a bound negative transcript. Its positive-or-negative semantic dichotomy retains the valid-input, nonempty-support and dimension hypotheses. The finite list controls deliberately preserve order and duplicate occurrences in the enumeration rather than silently replacing submitted syntax by a canonical representative. Refutation correctness is relative to the supplied finite formula and atom evaluator. Indexed coverage establishes one local reason for every member of the reconstructed list; it does not, by itself, establish that an arbitrarily supplied list exhausts an external semantic domain. The literal-domain coverage argument of §7.15.3 supplies that additional premise. [Signed service][fc250-0] [Finite enumeration controls][fc250-62] [Refutation construction][fc250-115] [Indexed coverage][fc250-114]

The direct-controller proof likewise has distinct interfaces. `DirectRun` reconstructs the generated history, current support and memory and uses the global source-departure count for cycling. `DirectSafety` maintains region and memory validity and menu lawfulness even when the rejection test has false positives. `DirectStability` takes eventual true-row nonrejection as an explicit regularity input; it does not establish that probabilistic premise by declaring the phase stable. `DirectParity` proves the generated run's parity on the stated common regularity event. `DirectEndpoint` discharges the actual-law endpoint for the literal submitted body and valid rational input. These steps preserve the difference between a pathwise implication, its probability-one premise, and the policy actually returned. A file containing only named certificate-soundness checks remains an interface-presence probe, not another proof or a fresh kernel result. [Run equations][fc250-50] [Safety invariant][fc250-142] [Stability][fc250-61] [Pathwise parity][fc250-218] [Actual-law endpoint][fc250-109] [Soundness interface requests][fc250-209]

The negative controls preserve concrete failure distinctions. The signed fixture uses 49 domain entries and rejects missing, additional, duplicated, shifted or reversed entries as well as stale input, support and start bindings. That number belongs to its finite fixture, not the general search complexity. Formula-branch controls distinguish full numerical row equality, missing live-support children, even-minimum failure and a forged refutation of a true atom; one convenient leaf cannot replace the aggregate formula. The empirical-history mutation keeps full-history counts while computing frequency from only the first history element. Its unchanged comment about using the full history does not describe the mutant's actual computation. These are controls for the specified implementation boundaries, not accepted alternative controllers; their replay status must be reported separately from reading their source. [Signed controls][fc250-180] [Formula-branch controls][fc250-175] [Truncated-history mutation][fc250-176]

Finally, the compiled-service dependency audit follows computational definitions, opaque bodies and native-replacement redirects, and reports inherited trusted primitive leaves. It is designed to exclude classical selection, the old solver and success or fairness oracles from the compiled service. An audit command identifies that dependency obligation; its presence is not a new successful audit or a proof of compiler, foreign-function or machine-code correctness. The mathematical actual-law theorem and the implementation's trusted computational boundary must both remain visible. [Compiled-service dependencies][fc250-9]

#### Literal certificate binding and the controls behind the semantic bridge

A transport envelope contains the actual structured input and a literal body; it does not carry a trusted acceptance bit or proof that a renamed input is the same. Its bound checker accepts exactly when the actual input equals the packaged input and the checker accepts the body against that actual input. Equal labels, hashes or a previously accepted status cannot replace the required structured equality. Interpretation and authority fields participate in input identity. Invalid dimensions, array lengths, rational rows, sparse menu keys and repeated or out-of-range members reject; the huge malformed-dimension controls require this rejection before expensive finite-universe enumeration. [F250-107] [F250-170]

The small fixtures distinguish several claims that are easy to conflate. There are revealing-action inputs with proper-support children, latent Bernoulli inputs, an equal-row variant and inputs with more than one admissible literal choice. A whole body can be invalid even if one queried node appears useful. An unused invalid extra node is not ignored; an admissible empty-state extra node is a different case. A child that passes its own checks under a different support is not the exact support child required by the parent's receipt. Two distinct direct and detour witnesses can both be accepted without being the same body. An empty body, or a node with nonempty support but an empty state set, can validate while answering no query. Empty support, duplicate support nodes or obligations, an omitted live candidate, missing menu permission and an omitted same-support successor reject. A distinct odd rival with matching full rows rejects, whereas unequal full rows with the same positive support can pass. A freshly rebound revision can pass even though the old envelope fails literal input identity. These are distinct acceptance conditions, not interchangeable malformed cases. Full numerical row equality is stronger than equality of positive supports and matters for an indistinguishable rival's parity condition. The fixture definitions and guard commands specify these comparisons; no new checker execution is inferred from reading them. [F250-11] [F250-25]

Support ordering also has a limited job. Its key records cardinality and sorted model indices, giving an injective key and deterministic duplicate-free order of the **supplied** finite support collection. It does not enumerate every mathematically possible support or certify that an external collection was complete. Likewise, the path-edge mutation controls test direct and detour routes, exact reconstructed source, length, start and endpoint, used-edge removal and the empty/nonempty singleton boundary. They import the selected mutant, so their textual guard requests cannot be promoted to observed successful rejection results. [F250-64] [F250-126]

The positive semantic bridge supplies what neither ordering nor local checks can supply alone. Submitted component links and paths yield actual qualifying Markov components; witness validity yields the stated reachability alternative. Strict induction over live supports then relates body nodes to the winning region, with an explicit finite fuel/descent argument from postfixedness to the greatest region. It does not infer greatest-fixed-point inclusion from an unsupported claim that a candidate is fixed. Thus accepted checking yields the inherited existence of a common lawful almost-sure parity policy. Serialization and compilation of the literal policy are not established by this checker; they require separate direct-controller evidence. [F250-195]

Finally, the hidden-change files containing `#print axioms`, universe and endpoint readback requests are inventories of declarations to inspect. They contain no outputs certifying their own clean execution. Their scientific role is retained alongside the exact positive/negative finite-region and semantic endpoint statements, without adding another axiom-audit pass merely because an inventory was preserved. [F250-10] [F250-15]

<a id="finite-targets-and-probability-interfaces"></a>

The direct certificate sources distinguish executable witness checking from proof-side existence. `CertificateCompleteness` constructs actual root paths, components, keyed obligations and support-ordered body syntax from the inherited winning regions, using finite classical choice. `region_has_certificate`, `policy_has_certificate` and `semantic_iff_certificate` therefore do not merely assume a certificate. Those powerset/choice constructions are outside the executable checker's dependency closure. [R750A-554]

`FiniteEnumeration` is specifically the **Signed** variant: accepted path length is at most n−1, component links at most n, node obligations at most n·q and body nodes at most2^q−1. Its ordered finite domains deliberately over-enumerate malformed and unused nodes; list order is not discarded. Accepted syntax belongs to that domain, but the domain can be huge. `IndependentControls` makes this boundary concrete with a49-entry tiny domain, malformed rows/menus, missing or duplicate entries, all seven interpretation coordinates, reconstructed nonconstant physical histories, and two accepted obligation orders giving different literal first actions. `EndpointFixtures` supplies positive/negative input and body records, not observed checker outcomes. The four-line `OrderedCycleRED` file merely requests cycle declarations after a Finset-sort import; it contains no positive availability theorem or successful readback. [R750A-552] [R750A-512] [R750A-537] [R750A-506]

The ordinary `COST_SCOPE` argument charges verification to the explicit input and submitted AST, with shape/positivity short-circuiting **before** carrier enumeration. Valid dense dimensions are paid for by actual array lengths, sparse menus and supports are scanned rather than expanded into all subsets, rational numerator/denominator growth is charged, and priorities are compared and reduced modulo2 rather than used as numeric loop bounds. This is an ordinary polynomial bit-cost argument, not a Lean cost theorem, polynomial certificate-size result or feasible exhaustive synthesis bound. The bound envelope compares complete structured inputs rather than trusting digests. [R750A-561]

`PROOF_OWNERSHIP` limits its own earlier submitted-syntax interface to the exact inherited87-module cost-variant closure and its independent checking/completeness/binding increment. That packet excludes autonomous finite-state-controller extraction and negative-complete certification, as well as parser, deployment, authority and physical-safety claims. These exclusions describe **that packet**, not a repeal of the later signed service or hidden-change endpoint in their separate sections. The identical-support Bernoulli fixture also retains full-row rival matching: making an odd rival's numerical rows equal changes component acceptance. Basename similarity is not a license to combine these different namespaces or claim scopes. [R750A-569]

[R750A-506]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/87237cd1e186077fb22e45c6a7963b41359d809c7df088467bc5c021d3bda768/OrderedCycleRED.lean
[R750A-512]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/885f6d059cadc896fd844a470cd7455ca081dabe13ce6698d90a1d4806950ff1/IndependentControls.lean
[R750A-537]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8fe2870c40af338155f589c009eb6d4deab649bc5983a20e8df215f80c01c0e5/EndpointFixtures.lean
[R750A-552]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/93debf0cf880bd635c1a74df660f2edfafcfb7f33100691b120946c0f7f3a2ab/FiniteEnumeration.lean
[R750A-554]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/94ad1e2f7d6e7ef106b108a79459a4b5103b15867711bebb7daea76005934953/CertificateCompleteness.lean
[R750A-561]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/96b8f65fc920311e045f2b9145483d3ad432ac7adc48d01b0fa4df70152ebc51/COST_SCOPE.md
[R750A-569]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/98afc319cb575a4fe03a52b815a76f5ab8ed22b4cd0f75535dec20c93a724266/PROOF_OWNERSHIP.md

The selected dependency and endpoint readbacks preserve narrower reproducibility roles. `ControllerDependencies` follows definition, opaque and implemented-by dependencies, reports external implementations and rejects its designated forbidden names. `TraceApiProbe` requests the specific list, last-element and chain interfaces used by hidden-change traces. `SemanticEndpointAxioms` requests axiom and full-signature readbacks for labelled/all-history lawfulness, compiled positive semantics, private-seed necessity and bound/signed equivalences. Reading those commands does not supply their returned closure, declaration inventory or compiler output, and none was executed for this incorporation. [T750-C671] [T750-C681] [T750-C684]

[T750-C671]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b52a407efc7796c1dc5ff22b1672e5ade1ce38b029cab4ea37468a522fac2f23/ControllerDependencies.lean
[T750-C681]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b7c3458d30a6d3acc7c926874eabb75ab40037bf32f6c56e9d66d7bf6c670b9e/TraceApiProbe.lean
[T750-C684]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b87465b9413af8edededf57336d8d7f21a1a4a004af96fb7d08f396cef9e2198/SemanticEndpointAxioms.lean

### 7.19 Exact targets and the probability interface

The hidden-parity target-pruning review guide concerns an exact finite target construction, including an executable exhaustive reference and a normalized rational-kernel adapter. It explicitly separates this construction from hard-menu/support recursion, the stochastic policy-existence equivalence and a polynomial strongly-connected-component or maximal-end-component implementation. Those further obligations cannot be discharged merely by retaining the target table. The broader ordinary arguments in §§7.11–7.17 keep their own source support and are not recounted as new consequences of this guide. [GUIDE105-G092]

The distinction between execution and proof is equally concrete. A finite comparison run tests the cases it evaluates. A kernel-checked refinement or an ordinary decision proposition has its own formal statement and dependency assumptions. The guide reports both types of historical evidence, using a trusted installed object cache, but supplies neither its module closure nor a fresh replay here. Its finite comparison counts are not an exhaustive quantification over arbitrary controller implementations. [GUIDE105-G092]

The executable exhaustive reference has two separate finite-fuel arguments. Forward reachability grows the current set by its one-step successors; each nonstable round increases cardinality, so $`|S|`$ rounds from a singleton suffice and agree with ordinary reflexive-transitive reachability. End-component checking uses that bounded relation. Maximal components are then selected by enumerating subsets of the current pair set, and pruning is iterated for the initial pair-set cardinality, recomputing components and row-matching rivals. The resulting target equals the existential target over **all** qualifying components, including nonmaximal ones. This source implementation is an exponential powerset reference, not the polynomial MEC implementation discussed in the ordinary algorithm bound above. [Q250C-094] [Q250C-096] [Q250C-103]

The normalized rational-row adapter proves that no candidate-positive support exit is equivalent to total internal mass one, and, for a live candidate, identifies the internal-successor graph with its actual positive-support graph. Full-row matching transfers this equality without renormalization. A computed target state therefore supplies a concrete component and an actual uniform or deterministic round-robin operating law that wins for every **matching** live model; every retained pair recurs, including higher odd priorities. A common lawful policy for all of B follows locally only with matching for every live model and menu inclusion, automatically reducing to the singleton-target case. Navigation from other region states remains a separate obligation. [Q250C-084] [Q250C-086] [Q250C-127]

The rational actual-source bridge guide isolates another boundary: its source theorem is deterministic for explicit seeds. Probability and finite-history transport require separately stated external finite-law conditions; that bridge does not itself provide a new formal probability theorem. A deterministic function can be placed under many seed distributions. Identifying its output law requires the distribution and its relation to the acquired history, not only correctness of the function on each seed. The actual-law constructions already given in this chapter supply their own declared probabilistic premises. [GUIDE105-G064]

The same guide preserves historical kernel logs and the non-object dependency collection without claiming a new compilation. Environment-bound verification harnesses remain historical evidence rather than portable promises. Assertion-based reviewer controls receive their stated normal-mode credit; optimized execution is supplemental where it removes those assertions. Participating diagnostics do not become independent review by appearing beside the review files. These distinctions preserve the positive finite target and deterministic-source results while keeping their probability, implementation and execution limits explicit. [GUIDE105-G064]


<a id="common-exponential-cost-range"></a>

#### A common exponential cost range for the original generated policy

Finite expected bad count is not the strongest conclusion available for every particular construction. The original generated hidden-parity policy has a separate, stronger co-Büchi cost theorem: on a fixed finite input, one policy admits a positive exponential-moment range common to all initially live models. The reason is a bound on products of chronologically stopped interval factors, not an inference from the finite expectation in §7.14. This result concerns the source's `generatedPhasePolicy` with its original empirical row test and constant Unit seed. Neither the stage-local fresh-count scheduler of §7.14 nor the literal certificate body's separately compiled policy in §7.16 is identified with it merely because each addresses the same existence question. [EXP-common][EXP-actual]

**Statement and quantifiers.** Let S and A be finite nonempty state and action sets, let B₀ be a finite nonempty set of models, and supply normalized rational transition rows, support-indexed hard menus, an initial state s₀ and the source construction's fallback values. For each model σ, let badσ be a predicate on state/action pairs. Assign priority 1 to bad pairs and 2 to good pairs, as in §7.17, and assume s₀ lies in the generated construction's hidden-parity winning region. Its lawful navigation, target selection and retained-action scheduling retain that construction's hypotheses; the cost statement is not a replacement specification for those components.

Choose a positive row-test tolerance ε such that

```math
\forall\sigma,\tau\in B_0\;\forall e\in S\times A,
\quad P_\tau(e,\cdot)\ne P_\sigma(e,\cdot)
\ \Longrightarrow\
\exists y\in S:\ |P_\sigma(e,y)-P_\tau(e,y)|>\varepsilon.
```

This is inequality of the full original rows and separation in **some** coordinate, not every coordinate and not the rows conditioned on no support change. Here ε is a probability-coordinate tolerance, not §7.14's bound on a stage's false-rejection probability. The empirical test at candidate index k rejects if some pair has acquired count greater than k and some empirical coordinate differs from the candidate row by at least ε. It uses the acquired global pair counts. The policy is fixed with this same ε throughout the theorem; the analysis must not quietly replace its test by one at ε/2. [EXP-test]

Let π<sub>ε</sub> denote that original generated policy, chosen before the actual model. Under its canonical Markov history law for model σ and the constant seed, put

```math
C_\sigma=\sum_{t\ge0}\mathbf1\{\mathrm{bad}_\sigma(S_t,A_t)\}
\quad\text{in }[0,\infty].
```

The first executed action is t=0. There is no synthetic initial charge or omitted first action. There exists r>0 such that, for every σ∈B₀, Cσ is finite almost surely, and

```math
\forall\theta\in[0,r)\quad\exists K_\theta<\infty\quad
\forall\sigma\in B_0,\qquad
\mathbb E_{\sigma,\pi_\varepsilon}
       \exp(\theta C_\sigma)\le K_\theta.
```

The ordinary exponential is evaluated on the almost-sure finite value. The source states almost-sure finiteness separately from its integral using the extended-nonnegative count's real conversion: that conversion sends infinity to zero and cannot itself exclude infinitely bad runs. The order is one ε, one policy and one positive r for the whole fixed input, then θ, then a common finite Kθ, then all actual models. Kθ may depend on θ. Neither the rate nor the bound is claimed independent of the input, effectively extracted, or practically small. [EXP-common]

**Finite separation supplies the analysis constants without changing the policy.** There are finitely many coordinate differences between the rows of models in B₀. If any are positive, half their positive minimum is a permitted common ε; if all are zero, the separation implication is vacuous and one may take ε=1. This choice precedes the actual-model quantifier. For an already chosen permissible ε and a fixed actual σ, the positive gaps above ε form a finite set. Half the minimum of ε and those positive gaps gives an analysis margin η with 0<η<ε and a witnessing coordinate difference greater than ε+η for every unequal rival row. If there are no unequal rival rows, take η=ε/2. This is slack for the proof, not a retuning of π<sub>ε</sub>. Likewise the finite actual transition table supplies p∈(0,1] below every positive entry. [EXP-test][EXP-margin][EXP-moments]

**Why the stopped factors can be multiplied.** Work first with independent next-state tapes for each pair, consumed according to the generated policy. This is a representation of the acquisition law, not a claim that the selected physical trajectory or its selected counts are independent. Write q=|S×A|, m=|B₀|, and let D=|S|·|A|<sup>|S|</sup>>0 be the finite augmented rotor-state bound used by the source's navigation argument. [EXP-rotor] For a deterministic count cutoff N≥1, the event that any row coordinate deviates by at least η at any tape prefix of length n≥N has probability at most

```math
A\exp(-cN),\qquad
c=\frac{(\min\{\eta,1\})^2}{2},\qquad
A=\frac{2q|S|}{1-\exp(-c)}.
```

This unions over all deterministic tape counts before consulting the selected acquired count. Off that event every acquired history is accurate whenever its relevant pair count is at least N. On a supported accurate finite prefix, the generated index remains below N+m. Each nonterminal mismatching execution consumes a distinct global pair-count position below that barrier, contributing at most q(N+m−1) endpoints. Segment-terminal transitions contribute at most 2m(N+m); the final detecting transition is included once, not dropped because its newly completed history might be inaccurate. Thus the chronological progress-slot budget is

```math
J_N=q(N+m-1)+2m(N+m)=\alpha N+\beta,
\quad\alpha=q+2m,\quad\beta=q(m-1)+2m^2.
```

This census is specific to the generated policy's retained global counts and phase/support bookkeeping. Resetting the pair counts at each phase would destroy the cross-phase count budget. The index and segment invariants are inherited controller obligations, not consequences of a generic concentration inequality. [EXP-charge][EXP-cutoff]

A dangerous slot is an actual chronological interval whose actions may incur bad cost; a matching good operating interval can have infinite elapsed duration but no bad cost. The source retains the zero-cost gaps on the original physical path. For a deterministic horizon T, let L<sub>j,T</sub> be the number of dangerous actions in its j-th progress slot, with zero for absent slots. The accurate-prefix census bounds the bad prefix by the sum of the first JN such lengths. At a dangerous slot's complete finite starting history, the augmented navigation argument gives a chance at least pᴰ of progress within D steps. Iterating this conditional bound gives

```math
\Pr(L_{j,T}>kD\mid\text{the complete starting history})
 \le\rho^k,\qquad \rho=1-p^D<1.
```

No conditional law is required on a null starting-history cylinder; its integral contribution is zero. With a=2/(1+ρ)>1, the geometric-tail summation for the rounded count R=⌈L<sub>j,T</sub>/D⌉ yields

```math
\mathbb E(a^R\mid\text{start})
 \le 1+(a-1)\sum_{k\ge0}a^k\rho^k
 =1+\frac{a-1}{1-a\rho}=2.
```

Here aρ<1, including the case ρ=0. The bound does **not** make different slots independent. For a fixed slot index, its possible finite starting histories form disjoint cylinders. On each cylinder all earlier slot lengths, and hence the product of their factors, are already determined by that complete history. Multiply the conditional integral bound by this known earlier product and sum over the cylinders. On the complement, the slot never starts and its factor is 1. Induction therefore gives the unconditional estimate

```math
\mathbb E\prod_{j<J}a^{\lceil L_{j,T}/D\rceil}\le2^J.
```

The no-start complement, chronological indexing and knowledge of the entire past are necessary: multiplying marginal moment bounds or conditioning on an analysis-selected last error would not prove this inequality. [EXP-slot][EXP-product][EXP-tower]

**From the product to an affine confidence tail.** Put λ=log a>0. On the accurate event, the bad prefix count is at most the slot-length sum, and rounding gives

```math
\exp\!\left(\frac{\lambda}{D}\,C_{\sigma,T}\right)
 \le\prod_{j<J_N}a^{\lceil L_{j,T}/D\rceil}.
```

Markov's inequality and the product bound control the accurate-event contribution; the preceding deterministic-count union controls its complement. The full count is the increasing supremum of its literal prefix counts. Continuity from below therefore gives, for t≥0,

```math
\Pr(C_\sigma>t)
 \le A e^{-cN}
       +\exp\!\left((\alpha N+\beta)\log2-\frac{\lambda t}{D}\right).
```

This passage permits Cσ=∞ and does not presuppose the almost-sure finiteness to be proved. It improves the alternative union-over-long-slots estimate, whose threshold is a product of the number of slots and their length cutoff; finite moments obtained from that weaker estimate do not by themselves establish an exponential moment. [EXP-cutoff][EXP-exp-tail]

For u≥0 choose N=⌈(log(2A)+u)/c⌉. Since A≥1, this is at least 1 and is bounded above by (log(2A)+u)/c+1. Define

```math
b=\frac D\lambda
  \left[\left(\alpha\left(1+\frac{\log(2A)}c\right)+\beta\right)
          \log2+\log2\right],
\qquad
v=\frac D\lambda\left(\frac{\alpha\log2}c+1\right)>0.
```

At t=b+vu the first tail term is at most e<sup>−u</sup>/2 by the lower bound on N; the second is at most e<sup>−u</sup>/2 by its upper bound. Hence

```math
\Pr(C_\sigma>b+vu)\le e^{-u}.
```

This explicit algebraic optimization explains the positive range; it is not an assertion that the source exports certified executable rate constants. [EXP-affine]

**Moments and the actual history law.** The affine tail implies, for every integer n≥0,

```math
\Pr(C_\sigma>n)\le\widetilde A\,r_0^n,
\qquad \widetilde A=e^{b/v},\quad r_0=e^{-1/v}<1.
```

For n≥b substitute u=(n−b)/v; for n<b the right side is at least 1. Summing the integer tails bounds the extended expectation and therefore proves almost-sure finiteness. A weighted tail sum then gives the finite bound

```math
\mathbb E e^{\theta C_\sigma}
 \le 1+\frac{e^\theta\widetilde A}{1-e^\theta r_0}
 <\infty\qquad(0\le\theta<1/v).
```

Thus finiteness is established before the real conversion is relied upon. All natural moments also follow, since for θ>0 and x≥0,

```math
x^k\le\frac{k!}{\theta^k}e^{\theta x}.
```

The tape calculation must then be transported to the **whole action-path law**. The generated source's stack-action trajectory law equals its canonical Markov action law, and the map from histories to executed actions preserves action 0. Applying this equality to the measurable exponential-of-count function transports its nonnegative integral, including possible infinite values. Applying the corresponding first-moment identity supplies almost-sure finiteness on the actual history law as well. Equality of a parity event alone would not transport these integrals. This is the same kind of full-law obligation distinguished from deterministic seed correctness earlier in §7.19. [EXP-tail-moments][EXP-cost-law][EXP-actual]

**One range for every live model.** For each σ∈B₀, the preceding proof supplies a positive rate rσ and actual-law finiteness for the *same* π<sub>ε</sub>. Take

```math
r=\min_{\sigma\in B_0}r_\sigma>0.
```

If 0≤θ<r, every model's exponential integral is finite. Their finite maximum is a valid Kθ. The minimum belongs to the rate argument; the maximum belongs to the bound argument. Replacing the minimum by a maximum can enter a model's unsupported rate range; replacing the maximum integral by a minimum need not bound all models. Nor can the all-model separation premise be checked only at the fallback model. The source's finite-set induction also treats B₀=∅ vacuously, choosing a positive rate and zero supremum, but that empty branch does not describe an actual model or a winning physical experiment. [EXP-common]

The common range is open. For example, a geometric count with 0<ρ<1 and probability (1−ρ)ρⁿ at n has finite exponential moment exactly when e<sup>θ</sup>ρ<1; it diverges at θ=−logρ. No endpoint assertion follows from the positive-range proof. Finiteness of B₀ is equally substantive: a sequence of geometric models with positive rates tending to zero need not have a common positive rate. More basically, a count with probabilities proportional to (n+1)<sup>−3</sup> has finite mean but no positive exponential moment. These boundary examples explain why the result strengthens the earlier cost conclusion without licensing a closed endpoint, an infinite-family extension or a rate uniform across inputs.

There is one useful connection to §7.14's posterior-deterministic visible-state construction. That construction preserves the entire bad-indicator stream, not just the event of eventual goodness. If the present generated policy is applied to a qualifying lifted finite model and pulled back through those exact causal history maps, the equality of count laws preserves its exponential moments too. This is a consequence of the already established full-law transport, conditional on the lifted input satisfying the present theorem's premises; it is not a new cost theorem for an arbitrary posterior-deterministic controller. Neither this connection nor the moment bound turns bad-action count into physical elapsed time, bounds the memory of the full learner, or extends a co-Büchi cost result to general parity with recurring odd visits.

The source editions below preserve the exact theorem and proof dependencies used here. Their text supports this ordinary reconstruction; no new Lean execution, recovered historical acceptance seal, mutation rejection run or source-closure qualification is asserted. In particular, the six supplied mutations of the common-range module isolate minimum/maximum, open-endpoint, all-model and fixed-policy obligations, but their existence is not evidence that the exact mutated builds have freshly failed.


The exact `FullControllerCanonicalLaw` provider identifies the canonical Markov history law and then the Boolean source's output law through their common measurable decoder. Its computed-tolerance parity consequence retains the accepted certificate, exact finite selector bindings, fixed fixture kernel, false initial state, support condition and winning-region membership. The parity objective is evaluated on the **decoded history**, not on a raw Boolean bit stream, and no nonatomic-output consequence is supplied. [R750A-520]

`LiteralCodeReadback` is the separate utility for printing four literal policy byte arrays: old/computed tolerance under both Boolean configurations. It records how those exact runtime bindings would be obtained, not the arrays themselves or an executed equality check. This preserves the reproducibility interface without treating an uninvoked exporter as proof of compiler/native correspondence. [R750A-527]

[R750A-520]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/89b9823fdbc8d4106fd8e8eb449dae8079cfe180c37859d95f23d222afded9eb/FullControllerCanonicalLaw.lean
[R750A-527]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8c1819835ab2fc00f6d98c49b5e08db1f211af70b08e3bd5596911e05fd8c2cc/LiteralCodeReadback.lean

### 7.20 One irreversible hidden change: finite regions and a lawful common controller

The preceding fixed-model results do not license replacing a fixed hidden law by an arbitrarily changing one. A more specific extension permits **at most one irreversible change**, from mode0 to mode1, with the switch itself unobserved. The extension has its own two-layer region criterion and actual-law proof. It must not be conflated with the repeated switching innovations of §7.10, or inherit the exponential-cost theorem just stated for a different generated policy. Its finite criterion characterizes existence of any lawful measurable private-seed winner and yields a literal deterministic winning controller from accepted positive evidence. The arbitrary-policy necessity proof and signed semantic endpoint complete this characterization. Statistical regularity, fixed-index reduction, all-history lawfulness and input binding retain their separate roles; fresh formal execution and runtime-representation correspondence remain distinct qualification questions. [HC184] [HC202] [HC208] [HC313] [HC331] [HC387]

#### 7.20.1 The input and the two layers

There are finite state and action sets, two normalized nonnegative rational transition-row families P₀(e,·) and P₁(e,·), and mode-owned natural-number priorities p₀(e),p₁(e) on state/action pairs e=(s,a). The structured input also supplies the declared menu and interpretation. Both layers use **the same common menu**, the input's full-support menu evaluated at the two-mode set; admissibility requires validity of the input and a nonempty common menu at every state. Discovering mode1 does not itself enlarge permission to act. The controller observes public state/action history, not hidden governing tags. At a fixed switch index N, mode0 governs rounds t<N and mode1 governs rounds t≥N. The never-switch case stays in mode0. Priorities belong to the mode governing the **departure pair**, not to an inferred label on its arrival state. [HC184] [HC208] [HC244]

Write Succθ(e) for the positive-probability successors under modeθ. Internal successors are those supported both by modeθ and mode0. A pair set E is **known-good** when it is an end component under mode1 and the minimum mode1 priority attained on E is even. It is **uncertain-good for θ** when it is an end component under θ, every θ-supported successor at its pairs is also supported under mode0, and every rival modeσ whose *complete numerical rows match θ on E* has an even minimum priority on E. Nonemptiness, closure and connectivity are supplied by the end-component predicate; “even minimum” means some member attains that even priority and no member has a smaller one. These are finite predicates, not empirical claims that an actual process is in such a component. [HC184]

Matching is numerical, not mere agreement of positive supports. For example, rows (1/3,2/3) and (2/3,1/3) have the same support but are not equal. Conversely, demanding the rival's parity without the matching condition imposes a different, stronger criterion: statistically distinguishable rivals need not be treated as permanently indistinguishable. The support-implies-matching and unconditional-rival-parity mutation files preserve these two distinct invalid strengthenings. They are negative controls, not positive source theorems or freshly observed compiler failures. [HC119] [HC67]

For proposed regions K (known mode1) and W (still uncertain), define the allowed pair sets as follows.

- D₁(K) contains pairs whose state is in K, whose action is in the common menu, and all of whose mode1 successors lie in K.
- D(K,W) contains pairs whose state is in W, whose action is in the common menu, all of whose mode0 successors lie in W, and whose mode1 successors unsupported by mode0 lie in K.

The last condition represents a **revealing transition**: observing a successor with zero mode0 probability rules out still being in mode0, under the supplied exact row model. It does not make arbitrary rare events revealing. A mode1 successor still supported by mode0 must also lie in W, because it satisfies the mode0-closure condition. [HC184]

Known progress from s means that a path through D₁(K), using mode1 support, reaches a state of a known-good component contained in D₁(K). Uncertain progress from s, for each possible actual modeθ, means either an internal-support path through D(K,W) reaches a θ-uncertain-good component contained there, or it reaches a permitted pair having a θ-positive, mode0-zero exit into K. Define F₁(K) by retaining in K precisely the states with known progress, and F(K,W) by retaining in W precisely those with uncertain progress for **both** modes. Thus reachability and a terminal recurrent target are separate requirements; simply keeping transitions inside a safe set does not establish parity. [HC184]

Both operators are monotone in their region arguments and shrinking. Enlarging a region preserves a permitted pair, a previously available finite path and a component witness, which proves the monotonicity claims. Starting from all n states, n descending iterations of F₁ produce its greatest postfixed region K*. With K* fixed, n descending iterations of F(K*,·) produce its greatest postfixed region W*. A strict descent removes at least one state, so after at most n strict decreases the process stabilizes. The source proves fixedness and the greatest-postfixed inclusion for both regions. This finite calculation contains **no stochastic-law or winning-policy predicate by itself**. Its semantic force requires the bridges below; it is not a standalone theorem that every graph-defined target is executable. [HC184]

#### 7.20.2 Why arbitrary one-change timing reduces to fixed indices

Fix one public-history policy π and one probability law for its private seed. Against an adaptive one-change adversary, the mode sequence can depend on acquired history and on the adversary's independent private seed, but cannot return from1 to0. On each complete input consisting of both seeds and the iid transition stacks, define κ to be the first round governed by mode1, or “never” if none occurs. Irreversibility makes that sequence exactly the deterministic schedule selected by κ. [HC202]

The crucial step is stronger than observing that such an index exists. Induction on the actual evaluator recursion proves that the **entire adaptive trajectory equals the fixed-κ trajectory on the same complete input**. At each round the public histories agree, hence π selects the same physical action; the first-one identity supplies the same governing tag, so the same stack entry supplies the same successor. The construction also proves that adjoining and forgetting the independent adversary seed preserves the original joint controller-seed/transition-tape law. This is a proved law-preserving projection, not permission to change the controller's seed distribution after observing the adversary. [HC202]

There are only countably many κ, including never. If each fixed-index trajectory satisfies parity almost surely, the union of their exceptional sets is null on that common space. Outside that union, the trajectory chosen by the possibly path-dependent κ is also good. Conversely, a fixed schedule is a legal particular adversary. Therefore, **for the same measurable π and same seed law**, almost-sure success against every legal measurable one-change adversary is equivalent to almost-sure success at each deterministic switch index, including never. The result is not an uncountable intersection over all adversaries and is not obtained merely from one successful policy separately for each index. The policy is fixed before this quantification. [HC202]

Newest-first history storage must not reverse this chronology. The receipt at list position j in a history of length ℓ belongs to round ℓ−1−j. In the prefix-reversal mutation, the likelihood instead uses j while the mode-lifting operation retains ℓ−1−j. A deterministic example shows the loss: mode0 returns state0, mode1 returns state1, and switching at round1 produces chronological observations0 then1, stored newest-first as1 then0. Assigning round0 to the newest observation gives an impossible mode0 factor for1 instead of the correct probability1. At the switch round itself, t=N, mode1 already governs. The strict-post-switch mutation changes that boundary incorrectly. The long prefix-reversal file includes copied lifting, marginal and restart declarations, but its deliberately inconsistent likelihood cannot be counted as another accepted proof of those declarations. [HC17] [HC244]

Conditioning after a positive observed prefix must likewise retain its actual schedule. A prefix possible before a late switch need not be possible under mode1 from the beginning. The stationary-prefix control targets exactly that retroactive replacement. A restart may shift a schedule and retain the acquired seed posterior; it cannot erase the history's evidential constraints by assuming it was stationary all along. No fresh evaluation of the imported late-switch fixture is asserted here. [HC135]

The exact switch-timing mutation makes the boundary error visible at its smallest input: it defines fixed mode0 for t≤N while retaining the assertion that `fixedMode (some 0) 0 = 1`. At t=N=0 its changed definition yields 0. Its copied likelihood and stochastic declarations are not additional positive proof credit. The no-change-only mutation separately attempts a positive body for the singleton input whose priorities are0 before change and1 after it; the no-change winner cannot meet the omitted fixed-index obligations. These are precisely scoped mutation targets, not newly executed compiler failures or a withdrawal of the full one-change theorem. [F939-C885] [F939-C899]

[F939-C885]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f28864e1da49295980017ac16fef033f44118ca3891133c085db8ef33565992e/MutationSwitchTiming.lean
[F939-C899]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f6209a5b043bda64d8e6a0c2d89c656b2791f3accaad219a0cd42ef61e2ee26d/MutationNoChangeOnly.lean

#### 7.20.3 Finite contamination and the strict empirical gate

After a fixed finite switch, observations generated under the old mode are finite in number. This does **not** mean that every empirical row converges. For a physical pair e, its cumulative visit count is monotone and either remains bounded or diverges. Only in the divergent case does adding finitely many old-mode numerator and denominator terms preserve the final-mode limit. In elementary notation, if a(t)/b(t)→p and b(t)→∞, then (a(t)+A)/(b(t)+B)→p for fixed finite offsets. The actual-stack construction identifies those offsets with the old-tag observations; the tag-separated history used to prove this equality is never a controller input. [HC192]

For example, one old outcome1 mixed with t final-mode outcomes0 gives frequency1/(t+1), tending to0 as t grows. If the pair is visited only once after the switch, the frequency remains1/2 instead. The latter case supplies no consistent row estimate. It is handled by the test's **strict count gate**, not by pretending that convergence occurred. [HC192]

At phase r, a row can trigger rejection only if its acquired count exceeds r and some empirical coordinate differs from the candidate row by at least the positive tolerance. For a bounded row count B, every phase r≥B makes that row inactive. For a divergent row, choose a time T after which every coordinate is within tolerance of the true final row. Earlier times have count at most their history length, so choosing r≥T prevents an earlier time from satisfying count>r. A finite maximum over all pairs supplies a path-dependent K such that, for every r≥K and **every time t**, the final-mode row test does not reject. This all-time quantifier follows from the bounded/divergent split and early-time gate; it is stronger than saying only that a test eventually stops rejecting at one fixed phase. It supplies no known convergence deadline or expected stopping-time bound. [HC192]

Under the constructed actual fixed-index law, every recurrent physical pair has divergent count and its empirical coordinates converge to the final-mode numerical row. If a candidate differs numerically on such a recurrent pair, a separating coordinate eventually makes the literal test reject at any fixed phase. The finite input's rational tolerance provides the executable rational-test corollaries. The same stack law proves that each positive final-row successor of a recurrent pair occurs infinitely often. These are almost-sure facts under the declared law, not adversarial guarantees over every supported infinite path. An odd state that stays with probability1/2 and reaches an absorbing even state with probability1/2 reaches the latter almost surely, while a support adversary could choose the stay edge forever. [HC192]


<a id="final189-b01-strict-count-controls"></a>

The exact count-boundary controls distinguish strict acquisition from a nonstrict substitute. With one stale receipt, count1 is inactive at phase1 but active at phase0; two identical receipts are inactive at phase2 and active at phase1. Discrepancy equal to tolerance1 still rejects. The separate nonstrict-count mutant uses phase≤count and asks an empty phase-zero history not to reject, exposing the changed boundary rather than proving a new gate theorem. [F189B-813](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dbd8599528a4b659e245a4cb2d9fd26515b739b416e700dad0e187f6a53b40a8/NonStrictCountGuard.lean) [F189B-816](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dc3285a64fac115de96afeb74acb985a2bc47d0b6b26391dd67dec367c7d0ba9/ContaminationControls.lean)

The stale-data counterexample keeps one wrong observation of pair(0,0) and appends arbitrarily many accurate receipts for another pair. Its first pair's count and wrong frequency stay1 forever. Deleting the count conjunct therefore yields rejection at every history length and no all-time phase barrier, although total data grow without bound. The source proves this failure; the mutation file's contrary rejection assertion is deliberately false. Finite contamination remains harmless only for a pair whose own count diverges, exactly as required above. These static controls have not been executed anew. [F189B-816](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dc3285a64fac115de96afeb74acb985a2bc47d0b6b26391dd67dec367c7d0ba9/ContaminationControls.lean) [F189B-832](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e1ad4ed82be77786cb99b0a6dfd48c31082c070d44ccc3ba7a7afc860f4cf04c/MutationDropsCountGate.lean)

#### 7.20.4 From regular paths to the literal controller's actual parity

The source compiler is a particular deterministic policy built from a positively checked body and an initial state. It retains a layer flag, phase and possible component, cycles the retained legal actions, and updates from actual acquired receipts. Memory starts in the unknown layer at phase0 with no retained component. Candidate choice alternates by phase modulo2 rather than deleting mode1 when earlier observations contradict it. Component selection follows the submitted obligation order before choosing an action. Revelation takes priority over statistical rejection and component exit; in the known layer, rejection is ignored and an exit clears the retained component. Ordinary uncertain-layer rejection or component exit increments the phase by1 and clears the component. Intersecting candidate actions with the common menu and using a permitted fallback preserve lawfulness even on malformed or off-policy histories, while the proved invariant makes that intersection redundant on the certified run. The Lean data-only body is not identified with the separate Python representation. The pathwise parity theorem assumes: a valid body and its initial-region membership; a history following that controller; actual supported steps; irreversible and eventually fixed mode; the all-time true-row gate; eventual rejection of recurrent unequal rows; and recurrence of positive final-row successors. Those are explicit premises of the **pathwise** result, not conclusions supplied by an arbitrary execution trace. The copied common definitions in the mutation sources retain the menu, initialization and update-role specifications just described; their deliberately changed branch is not a positive controller proof. [HC155] [HC33] [HC177]

The proof first obtains stabilization of the layer, phase and retained-component choice. If the uncertain phase stabilizes at r, every recurrent pair must have the same numerical row under the phase's candidate and the actual final mode: otherwise eventual wrong-row rejection would contradict stable nonrejection. Positive-successor recurrence makes the physical recurrent set closed under the actual final row. If no component is retained, cycling and finite progress would force a component target, a revelation or a numerical mismatch; each contradicts the proposed stabilized navigation case. If a component is retained, cycling and recurrent closure identify the required recurrent behavior. In the known layer the final mode is1 and the known-good component supplies even minimum. In the uncertain layer numerical matching triggers the uncertain-good component's rival-parity clause for the actual final mode. [HC155]

Two update controls are essential. Testing rejection against the old prefix rather than the history including the **new receipt** discards precisely the acquired evidence that must inform the next memory state. Advancing the phase by2 rather than1 defeats the intended alternation/barrier argument; this is not an interchangeable implementation optimization. The new-receipt mutation supplies a two-state, one-action full-support example: on its one-receipt history the mutated memory stays at phase0, while the deliberately failing assertion asks for phase1. The double-phase mutation starts at phase7 with rejection true and no revelation: its rule gives9 while the control asks for8. These mutation sources preserve the failing semantic alterations, without supplying fresh compiler diagnostics or new positive controller theorems. [HC33] [HC177]

The final compiler endpoint discharges the pathwise theorem's support, gate and recurrence premises from the constructed `fixedLaw`; it does **not** ask its caller to assume fairness, stabilization, convergence, recurrence or success. It identifies each hidden departure tag with the actual governing mode almost surely, proves that an eventually constant tag has the same parity as the physical pair path labeled by the final mode, and obtains parity for the literal compiled policy at every fixed index. The countable reduction then yields success against every legal measurable private-seed one-change adversary for that **same** policy. For the finite nonempty state/action input and admissibility conditions, this is genuine constructive controller sufficiency from an accepted positive body. This is a mathematical literal-policy construction, not an executable procedure for selecting a positive body, nor a parser or runtime-correspondence result. The endpoint depends on the imported actual-law, compiler-invariant and stability providers; this prose does not replace their formal dependency closure or claim a fresh Lean execution. [HC208] [HC202]

The separate Python reference has a narrower **representation contract** than an unqualified claim of totality on arbitrary objects. Its raw model admits plain integer dimensions, indices and priorities, excluding booleans, and exact integer or canonical rational-string probabilities. It validates even unavailable-action rows. The normalized model instead stores immutable tuples of exact fractions. Its submitted certificate checker examines the supplied components and routes; it does not obtain acceptance by asking the solver for another body. These facts identify the checked data boundary, not an established Python/Lean parser correspondence. [Q250D2-218] [Q250D2-219] [Q250D2-222] [Q250D2-225] [Q250D2-228]

The history interface first checks the positive body and the complete history syntax: an odd nonempty alternating state/action sequence, in-range nonboolean indices and lawful recorded actions. Malformed syntax raises an error. On such well-formed public histories, a different initial state, an off-policy action, an impossible observation or a broken region invariant sends the replay to persistent first-menu-action fallback. Before revelation, an observation is impossible only when both rows assign it zero probability; after known1, a mode1-zero observation is impossible even if mode0 permits it. Thus a mode1-zero receipt before revelation neither announces mode1 nor permanently removes that candidate. These branches preserve the distinction between all-history lawfulness and success on the supported certified run. The incremental `choose`/`observe` interface trusts memory reached from its initializer with the same checked model and body; it does not certify arbitrary caller-constructed memory. The bounded controls compare that incremental path with history replay and poison runtime priority access, but supply no new general runtime-refinement theorem. [Q250D2-218] [Q250D2-220] [Q250D2-226] [Q250D2-242]

[Q250D2-218]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5d9f384c23ee6995eb963da6bb10b3073bcc4dd856d666f4c639e1aca71288c5/API.md
[Q250D2-219]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a75e325dd879bab3ab392b4a467e12b93716ee33eebec61d30ba668fbdd1e41c/certificates.py
[Q250D2-220]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/777a95bf89caa09b4c0c4c9274e4b5aa3b7371d63ea9a92c313e7bffba8be003/controller.py
[Q250D2-222]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/81e01e552e6ebb455f381a81f2568aa08d5b233522bda53d23c8b930d023c823/model.py
[Q250D2-225]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7b5282bc84c2637c44481799c9f28334114189854878a28bcf6ad9eb67cf36ca/test_certificates.py
[Q250D2-226]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9711497756f6a0962dae8f6795c87c7cf8415945dfa7cdf903b512d7461b4eb/test_controller.py
[Q250D2-228]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4eadeb5229787a92545139ebaff231c74ccb674a259773efcbc7ffdc4a28bf06/test_model.py
[Q250D2-242]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/33e9e65f19f696211583e81330751a42017869f6faf723efe45f313c52018db3/test_reference_independent.py

#### 7.20.5 Necessity from arbitrary private seeds and the signed semantic endpoint

The known-region argument above is only one part of the converse. The positive-prefix, killed-tail and uncertain-progress sources complete the finite rational one-change characterization. They must be read together: success at every fixed index concerns **one fixed measurable policy and its fixed probability seed law**, while lawfulness concerns every public history, including histories of probability zero. The resulting theorem is not restricted to finite memory or to policies already generated by the certificate compiler. [HC313] [HC331, §§6–9] [HC387]

Fix a finite public history h of length n. Let C_h be the measurable set of private seeds that select its recorded actions, and L_κ(h) the product of its actual scheduled row probabilities. The actual joint seed/prefix law factors as

\[
\Pr_κ(r\in D,H_n=h)=\rho(D\cap C_h)L_κ(h).
\]

When h has positive probability, both factors are positive and the residual seed law is ρ_h(D)=ρ(D∩C_h)/ρ(C_h). The numerical prefix likelihood cancels. Thus two deterministic schedules assigning h positive probability give the **same residual private-seed law**, even when their likelihoods differ. The restarted policy concatenates the entire old public history before its new suffix; it does not reset private memory. After n rounds, a finite switch index j becomes max(j−n,0), while “never” stays “never”. Conditioning a zero-probability prefix instead gives the zero measure, not a probability restart. These statements are derived for the original constructed law and its physical marginal, not obtained by declaring a posterior independent of the history. [HC403] [HC265]

The time convention is particularly consequential. An old prefix generated before a late switch need not be possible under stationary mode1. A comparison of no change with a switch *at n* keeps the entire old prefix under mode0 and changes only the subsequent law. The forward tail-transport theorem proves equality of the joint prefix-and-tail masses in this case when the two complete tail rows agree on the selected pair set E. It applies to the measurable event that the tail never leaves E and its exact recurring pair set is E. [HC476]

**Why complete confined-tail laws agree.** Kill a record immediately before its policy selects a pair outside E, then emit a cemetery symbol forever. Couple two equal-on-E row families using the same private seed and transition uniforms, with identical samplers on equal rows. At each live shared history they select the same action; either both are killed or both obtain the same next receipt. Induction equates the whole killed record. Hence its pushforward laws agree for all measurable infinite-record events, not only individual finite coordinates. If schedules have different but positive prefixes h, the joint prefix-and-confined-tail probabilities differ by the strictly positive finite ratio L_κ′(h)/L_κ(h). No absolute continuity of unrestricted infinite laws is asserted. [HC331, §6]

For an arbitrary lawful fixed-index winner define K by states witnessed at positive original post-switch prefixes, and W by states witnessed at positive original no-change prefixes. The policy-relative definitions retain the original seed law, history and schedule. Positive next-action seed mass, multiplied by a positive governing transition, supplies a positive extended prefix. Every positively selected pair is in the common menu. Consequently all mode0-positive successors remain in W, and every revealing mode1-positive/mode0-zero successor belongs to K; these are precisely the uncertain safety conditions. Before revelation, any positive compatible prefix under another fixed schedule is also positive under no change with the same compatible-seed factor. Thus the same uncertain safety applies to actual unrevealed mode1 histories. Countably many finite-history exceptional sets are removed together on the actual law. [HC412] [HC497]

Actual-law support and positive-successor recurrence then make the exact recurrent pair set an end component of the final mode. A finite prechange prefix is allowed to use edges unsupported by the final mode: the deterministic graph argument requires final-mode support only after a finite index. Recurrent closure follows because each positive final-row successor of an infinitely used pair recurs; strong connectivity follows from supported finite segments sufficiently late that all their pairs belong to the recurrent set. This derives the component instead of assuming a stationary or fair arbitrary-policy tail. [HC400]

For uncertain progress at a positive compatible prefix, separate two cases. If never-revealing continuation has positive probability, partition it among the finitely many possible recurrent pair sets and select one with positive mass. Its component lies in the uncertain safe pairs and has no candidate-positive revealing edge. A late enough actual finite segment reaches it. If never revelation has probability zero, a positive supported finite history reaches a first revealing exit into K. Cycle deletion gives the finite internal route in either case. [HC313]

The component's rival-parity clause requires a further argument. Select a **deterministic** confinement time and a positive finite prefix from the positive recurrent-E event, using its countable union over possible confinement times. This does not treat the random last exit as a stopping time. For candidate0, compare no change with a switch at that selected time; the prefix laws agree and equal E-rows give the same positive confined-tail mass. An odd rival minimum contradicts winning under that late switch. For candidate1, select the prefix inside a never-revealing immediate-change run. It is mode0-compatible, so replace its finite likelihood and tail law by the no-change law using the positive ratio above. An odd mode0 minimum would contradict no-change winning. Each candidate's own parity follows directly from its winning law. [HC331, §§6–7] [HC476]

Therefore W is postfixed under F(K,·) for both candidates. The Lean `policyUncertainRegion_postfixed` explicitly uses no change for candidate0 and the switch at the witnessing prefix length for candidate1. Together with the known-region inclusion K⊆K*, monotonicity places W inside W*. Its initial state belongs to W, so every such arbitrary-private-seed winner supplies finite positive evidence. Conversely an accepted body drives the literal deterministic public-history compiler, whose actual-law sufficiency was established in §7.20.4. [HC313] [HC387]

For a finite nonempty state/action input with normalized nonnegative rational rows and nonempty common menus, the earned equivalences are thus:

- an arbitrary lawful measurable private-seed winner exists;
- the initial state belongs to W*;
- an accepted positive body exists;
- a literal deterministic compiled winner exists.

A submitted signed record also binds the **whole structured input and initial state**. Accepted positive records carry the deterministic winner. Accepted complete negative records exclude every lawful measurable policy separately on any supplied probability seed space, not merely the deterministic compiler; exactly one sign has accepted evidence. The winner predicate retains measurability, all-history common-menu lawfulness and parity against every permitted adversary. Parity alone does not imply either of the other two conditions. [HC387]

The complete negative evidence contains both descending region traces, with initial universe, each exact update and the required terminal repetition. Earlier §7.20.1 supplies the shrinking/greatest-region proof. Merely producing a smaller postfixed region does not prove exclusion. The explicit malformed-input and binding controls reject missing or nonstochastic rows, missing priorities, invalid or duplicate menu data, wrong initial states, stale revisions and altered raw rows. Even reordering irrelevant menu data can preserve interpreted body acceptance while fail exact submitted-input equality. This distinction prevents a body proof from being reused as a receipt for a different raw input. [HC280] [HC365] [HC462]

The ordinary complete proof is supplied in [HC331]; the formal endpoint [HC387] calls the imported controller and necessity providers rather than hiding them in a new assumption. Inspection of these source derivations is not a fresh Lean build, clean-axiom verdict, parser theorem, Python/Lean representation equivalence or scientific adoption. The mathematical converse is now present; those separate execution and representation obligations should not be misstated as an absent converse.

The earlier known-progress component remains part of this argument: stationary mode1 recurrence, permitted-pair containment and parity for an arbitrary measurable seeded policy yield a reachable known-good component from a positive-measure recurrent-support class. Positive original post-switch prefixes and the restarted posterior then make the policy-relative known region postfixed under F₁, placing it inside K*. This does not require recognition of a last exit time. The added uncertain-region providers complete, rather than replace, this result. [HC171] [HC184]

The finite binding alternatives also retain their separate content. Under admissibility, a bound accepted positive record exists exactly for s∈W*, and a bound accepted negative record exactly for s∉W*. Dropping initial-state equality from the positive wrapper permits a body accepted at the requested state to carry another submitted initial label; the negative wrapper retains its own equality check. These finite facts are not a parser theorem, byte-encoding theorem or external attestation of the input. [HC178] [HC134]

The earlier paired-trace controls retain the exact n+2 length boundary. With both traces carrying the stated list, they assert acceptance of the one-state odd input with [universe,empty,empty], rejection of an empty-start trace, rejection of an invalid descending trace for an even input, rejection of a two-entry trace, acceptance of the canonical separator trace, and rejection of an extra repeated empty round. Adding repeated terminal states cannot evade the boundary. These are source check assertions, not newly run tests here. [HC183]

#### 7.20.6 Lawfulness and evidence limits are substantive

Strategic success does not supply authority. A one-state two-action input with self-loop rows gives the permitted action odd priority1 and an excluded action even priority0 in both modes. The constant excluded-action policy has parity success under every fixed schedule, and hence all legal one-change schedules by the reduction, yet fails lawfulness already at the empty history. The finite uncertain region is empty and there is no accepted positive body. Thus parity, measurability and even universal timing success do not turn the policy into a lawful semantic winner. Conversely, replacing the parity conjunct of a winner by `True` discards the objective even if measurability and lawfulness remain. The corresponding one-state odd-priority fixture has a measurable permitted constant policy satisfying that weakened predicate, contrary to the mutation file's intended no-winner assertion. Its helper equates the source-labeled lawful-policy contract with all-history public-menu lawfulness; that equivalence does not repair the omitted parity conjunct. [HC92] [HC186]

This separation is especially important when the mathematics is used as a realization of noetic structures: formal policy success is not, without further premises, warranted cognition, genuine source authority or knowledge transmission. The model supplies precise conditional relations among evidence, permitted control and eventual parity. It does not establish that the chosen rows describe the actual world, that an observation source is truthful, or that the menu embodies legitimate authority. Those source-grounding obligations retain their own arguments elsewhere in this work.

Finally, the endpoint-interface and axiom-review files preserve declaration checks and intended axiom-inspection surfaces. Naming a theorem is neither its proof nor observed execution. The additional proof bodies and companion incorporated in §7.20.5 now supply the uncertain-region and arbitrary-private-seed converse. Audit commands themselves still provide no fresh clean-kernel verdict, parser/runtime correspondence, dependency reproduction or scientific adoption. Preserve this distinction without demoting the earned mathematical converse or promoting deliberate mutations into established theorems. [HC130] [HC198] [HC313] [HC331] [HC387]


#### 7.20.7 Polynomial decision, complete evidence and its exact scope

The ordinary rational-input theorem in [HC331, §10] strengthens finite decidability to deterministic polynomial decision, and supplies a self-contained P-completeness proof. It is an **offline existence/evidence** result, not a polynomial learning-time bound for the online controller.

Write R_eq for pairs where every coordinate of the two numerical transition rows agrees. For candidate θ, remove every pair with a candidate-positive/mode0-zero successor. A remaining end component qualifies in exactly two cases: it contains a pair outside R_eq and its θ-priority minimum is even; or every pair lies in R_eq and both mode-priority minima are even. This exhausts the two-mode rival clause without replacing equality by common support.

For each attained even candidate priority v, restrict to pairs of priority at least v, compute maximal end components, and retain those that attain v and contain a pair outside R_eq. For equal-row components, enumerate pairs of attained even minima (v₀,v₁), restrict to R_eq and to both lower thresholds, and retain maximal components attaining both. Each qualifying component is contained in a maximal component of its own threshold restriction; the witnesses attaining its minima and distinguishing row remain. Conversely every retained component qualifies. Hence the procedure preserves exactly the **union of target source states**, which is what the progress predicate and descending region iteration consume. It need not reproduce an exhaustive list of every qualifying component.

The maximal-component routine filters whole actions whose positive successors all remain in the candidate state set, then decomposes the positive-edge graph into strongly connected components and recurses on proper components. An original end component survives inside one child. No-action singletons are discarded; a terminal strongly connected set with an action at every source returns all retained pairs. Disjoint returned source sets and coverage establish maximality. The recursion has at most n leaves and 2n−1 nodes. Filtering removes an entire action, never only its adverse receipt edges.

If m=|S×A|, each candidate needs at most m single and m² double thresholds, taken from values actually occurring rather than all numbers below a binary-encoded priority. At most n strict decreases occur in each region chain. Graph searches, rational sign/equality tests and binary priority comparisons have polynomial bit complexity; a loose O(n³m³) incidence-work bound suffices. The decision does not depend on an inverse minimum probability or separation. Finite witness extraction gives positive evidence; recomputed complete descending traces give negative evidence.

**P-hardness.** A polynomial-time machine computation has a polynomial-size acyclic monotone circuit, constructible in logarithmic space: use one-hot tape-cell/label indicators over a polynomial time-space window, fixed local three-cell transition templates, explicit blank ghost cells at the boundary, and persistent halting configurations. Each next indicator is the OR of the finite valid predecessor-label triple conjunctions. A constant number of logarithmic counters emits topologically numbered gates without storing a whole layer. The acceptance indicator is the circuit output.

Make one stochastic state per circuit gate plus absorbing true/false states. Both actions are lawful. An OR-state lets the action choose its child; an AND-state sends either action to its two children with probabilities 1/2,1/2, combining equal children into probability1. Both hidden modes use this same kernel. Give priority0 everywhere except the false absorbing state, whose priority is1. Every nonterminal step moves backwards in circuit order, so parity equals eventual arrival at true. The value recursion is max at OR and arithmetic mean at AND. Backward induction bounds every history-dependent policy, pointwise in its private seed and then after integration; a memoryless maximizing OR choice attains it. The value is1 exactly when the circuit is true. A logspace transducer emits the explicit dense normalized rows and priorities. Thus the existence language is P-complete under logspace many-one reductions even with identical kernels, common state priorities0/1, two lawful actions and entries0,1/2,1. This does not identify stochastic AND with adversarial sure choice on cyclic graphs, imply an optimal polynomial degree, or prove an unconditional parallel lower bound.

Thresholding must precede maximality. At one state with self-loop priorities2 and1, the full maximal component has odd minimum although the priority2 action alone wins. With two priorities and action-priority pairs (2,3),(3,2),(1,1), the first two together attain even minima(2,2); neither alone does, and the third spoils them. The double-threshold method retains the two required, possibly distinct minimum witnesses. [HC331, §§10,13]

The exact Python sources realize the threshold argument without substituting the exhaustive reference search in production. The iterative SCC routine filters whole positive-successor actions inside each work item; a nonterminal item splits into proper disjoint state components. The efficient solver enumerates attained even priority values and reverse-reachable targets, while preserving numerical row equality in the equal-row case. Its body can differ from the exhaustive reference's list while retaining the same target-state union and certificate interface. The helper adapter verifies all five reference-module hashes before importing and exports the shortest-route helper rather than the exhaustive solver. Loading definitions is not executing their exhaustive paths. [Q250D-206] [Q250D-207] [Q250D-208]

A negative body is checked from the full carrier through every stated transition: all nonterminal steps must strictly descend and the final step must repeat exactly. Extra repetitions, omitted prefixes and merely matching the final region are rejected. Invalid models and resource failures propagate as execution errors rather than negative mathematical answers. The structural controls check the 2n−1 SCC-work-item bound and m+m² threshold calls, including large binary priorities; timing is only illustrative. The source argument above carries the general complexity claim. The retained fixture, dependency-tampering, threshold and solver tests state bounded implementation checks; none was newly executed by this consolidation. Their import closures and exact pins remain live reproducibility dependencies. [Q250D-209] [Q250D-210] [Q250D-211] [Q250D-212] [Q250D-213] [Q250D-214] [Q250D-215] [Q250D-216] [Q250D-217]

[Q250D-206]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/80a239405e103d780c8328acd03347f84b9f6af26e795ae0cc562e090bff600f/dependencies.py
[Q250D-207]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/eaf319dd0909271ea757ec14b88efa0ad45f325ba3b652aa6a6f88f3230a157f/efficient.py
[Q250D-208]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/22a119d827635d18fd47bccfded1fcf2735f177a5534830525a026c9dc2e40f4/mec.py
[Q250D-209]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/41658548a65dc6aa6bffdae1f11a692bb4d58ccec6056a6a95bd55a5817ea4a0/negative.py
[Q250D-210]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d05f7b01d3c85cb7b873ccc0fa93e0bfef3260a119a50b49a82ca9d2e57f4d53/fixtures.py
[Q250D-211]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/587a53b4330851962e34b896c9479addf917bc5b2ce28a1bcbfeaa35302ecef8/operation_counts.py
[Q250D-212]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8ec609b981f3176589a31c0907ce9e0bd02dbadec2d5568e0606630f616f4b58/support.py
[Q250D-213]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e8ddcc7f0c691cfdc31c7f2da1eba91de7ae2e67782dd1e5aa648a683bc5de50/test_dependencies.py
[Q250D-214]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/197c3ddc6295de759436a1a5b14dc39aa48e501b0178333aba5177ad319e0a01/test_mec.py
[Q250D-215]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a4837ad3e57c780866d14ee332c952b5695369180395e98dfd89f8d0d0146253/test_solver.py
[Q250D-216]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b0d04c12037b0ff4e7ada426efbb23033339127de78b78f44f9af0b026c29cdd/test_structure.py
[Q250D-217]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/add193071ffbf84dcddae379692c2e37e9383a07da794a0b4d4f16df3671c331/test_thresholds.py

The independent finite oracle offers a different characterization of the same greatest regions. Instead of repeating descending iteration, it enumerates every candidate region satisfying the positive progress clauses and takes their union, first for K and then for W with that K fixed. This is justified by the monotonicity and contraction already proved in §7.20.1: if F(Xᵢ)=Xᵢ and U=⋃ᵢXᵢ, then each Xᵢ⊆F(U), so U⊆F(U)⊆U. The union is therefore itself feasible and contains every feasible region. Boolean transitive closure computes finite reachability, independently of the solver's route search. This comparison checks the finite existential criterion without presupposing that the solver's particular descent or selected witnesses are correct. It remains an exponential reference calculation, not a replacement for the polynomial construction. [Q250D2-239]

For the **one-action subclass**, a second oracle avoids certificate predicates altogether. Let Gθ be the states from which every reachable bottom strongly connected component of the modeθ chain has even minimum departure priority, and let Reach₀(s) include s itself. Then K*=G₁ and W*={s∈G₀ : Reach₀(s)⊆G₁}. The finite-chain recurrence argument makes Gθ exactly stationary almost-sure parity success. Necessity of the W* condition follows from no-change success and from changing at the endpoint of any positive mode0 finite path: an endpoint outside G₁ gives a positive probability of subsequently entering an odd bottom component. Conversely, if every such endpoint belongs to G₁, each deterministic finite switch has a mode1-winning continuation after its finite prefix, while never switching wins from s∈G₀. The countable fixed-index reduction of §7.20.2 supplies the same conclusion for the allowed adaptive one-change adversaries. This derives a semantic check independent of the region/body predicates and explains the two-state separator; checking only immediate change and no change would omit the intermediate reachable endpoints. [Q250D2-239]

The control programs keep their independence and finite scope explicit. One family independently enumerates end components and all allowed-pair subsets, checks exact maximal components and disjoint source sets, and compares the union of qualifying target states rather than requiring identical witness lists. Another compares every K and W argument, the returned final regions and the submitted signed bodies against the independent feasible-region oracle. The declared complete families contain 13,122 two-state/one-action inputs, 500 one-state inputs with up to three actions, and 6,561 state-homogeneous two-state/two-action inputs. The additional 343 three-state support graphs and 160 fixed-seed sparse inputs first have a component-only campaign and separately an end-to-end campaign. None exhausts arbitrary three-state numerical models. [Q250D2-230] [Q250D2-231] [Q250D2-233] [Q250D2-234] [Q250D2-235] [Q250D2-240] [Q250D2-241]

Other controls answer narrower questions: substituted efficient entry points replay earlier adversarial tests; forged traces compare two negative checkers; patched aliases plus code-entry profiling test that bounded production calls avoid exhaustive routines; and large binary priorities exercise structural call bounds without enumerating every smaller integer priority. These are inspectable test specifications, not new observed passing runs, general probabilistic proofs, or a derivation of complexity from timings. Assertion-based campaigns require an assertion-enabled execution to warrant their checks. Their independent oracle definitions, reference checker and import closures remain reproducibility dependencies, including where a missing-module helper deliberately fails rather than silently skipping a test. [Q250D2-224] [Q250D2-232] [Q250D2-236] [Q250D2-237] [Q250D2-238]

[Q250D2-239]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/093b6530adab6b9c1cd022a3f3c82208088534717a9bc412673ad9a1857cbe33/oracle.py
[Q250D2-230]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c9f1f091a125fc6d197772ff5b870ab10dd11317d13e3ca29edb5e39bf2a64a9/component_checks.py
[Q250D2-231]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/57d0f7be02946ac8723cfaaac9d8e0cda0a6743ff7f382c7a26db1129121b1e2/oracle.py
[Q250D2-233]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/dfad96bc36c2d0f75fd737cf46ff0295254bfacf9f207795f060321e2707b727/run_campaign.py
[Q250D2-234]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6f1428055f2db50eb8e43a3ba7e17ed1f149b999bbeb63597b386f47ce224393/run_extra_campaign.py
[Q250D2-235]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/04e6462783fa751eb968178f6090dca06fe981ec2b8512f22a9365d58851c7f0/run_extra_end_to_end.py
[Q250D2-240]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a6011a82aeabb2d82b45fb753996af1f77a2e6a343faf412c4a1cdbeb8a6421d/run_census.py
[Q250D2-241]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6a85124dc106a6387108b323375630b77b1c2aa9e06cc293a7320d4fc5dc0d54/run_extended_census.py
[Q250D2-224]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d6e3287baf9864f397f962658bcd5af43c96e1b347c8aacd8e93b3d39ac25879/support.py
[Q250D2-232]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a74ef658c1e8d530b2d15bed2411e8a59f20cc2ecdc688031663a0a4514d8c04/replay_previous_adversarial.py
[Q250D2-236]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/75d30ef82def50fa8e2dacc7cd60b4de2268f38cfb9f35b4794f6ec8b13d7211/run_negative_campaign.py
[Q250D2-237]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d6d18bd003ad11dee04c506b4a2e56c3d965285cb1ec2b62700dffc1be9d95af/test_efficient_independent.py
[Q250D2-238]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8ca7779e47f8241b587ba4fc2b8fc37f5880513b787bdf2e1751c67b64d7ac10/test_production_paths.py

#### 7.20.8 Real-number representations and a uniform support-only positive theorem

The probability/component proof applies mathematically to real stochastic kernels on the same finite carriers. For **each individual real instance**, a positive certificate can be implemented by a finite deterministic effective history program. Hard-code its finite certificate, exact support and equality masks, and rational comparison centers. If Δ is the least positive numerical coordinate difference, choose rational τ>0 with 4τ<Δ and rational centers within τ/4 of each true coordinate. Use rejection distance τ around these centers. True empirical coordinates eventually lie within τ/2 of the actual row, hence within3τ/4 of the correct center; a wrong recurrent coordinate differs from the wrong center by more than15τ/4 and is eventually rejected. Revelation uses the exact support mask, not an approximate zero test. These finitely many rational choices exist even for noncomputable coefficients; they are **nonuniform advice**, not a uniform extraction algorithm. If all rows agree, finite fair navigation and cycling suffice without a learner. General finite programs may need unbounded counters. [HC331, §11]

Exact signed decision from arbitrary fast-Cauchy names is impossible, even when the named values happen to be rational. Let receipts be Bernoulli, independent of source/action, with p₀=1/3 and p₁=1/3+ε_M, where ε_M=0 if machine M never halts and ε_M=2^{−(T+3)} if its first halt is at step T. Simulating k steps supplies a uniform fast-Cauchy name: if no halt is yet observed, a later contribution is smaller than the requested error. Mode i rewards eventual exclusive action i. Equal parameters give identical observable laws requiring disjoint eventual actions and hence no winner; a positive gap admits an empirical-threshold winner. Exact existence would decide halting. This is a representation obstruction, consistent with polynomial decision from explicit rational fractions and with nonuniform effectivity for each instance.

There is nevertheless an important **uniform positive subclass**. If the two modes have the same priority map, exact supports, menus and priorities suffice to compute one certificate and one deterministic effective policy **before** choosing any compatible numerical realization. For every such realization and every legal one-change adversary, that same policy wins almost surely under the resulting law. This quantifier order is stronger than one different policy for each realization, but does not assert a common conull event across uncountably many laws. Component qualification now uses only candidate support and the common even priority minimum; the rival clause adds nothing. Uniform rational rows on the supplied supports therefore decide the same finite criterion.

The controller retains the same navigation, phase and revelation structure, replacing numerical discrepancy by the one-sided test

\[
N_e>r,\quad y\in H_\theta(e),\quad (r+1)N_{e,y}<N_e.
\]

Candidate-zero coordinates are not tested. For any fixed realization, its smallest positive row entry p* is positive, but is used only in the proof. Finite contamination and the strict gate eventually put true gated frequencies above p*/2, while1/(r+1)≤p*/2. Thus sufficiently large true phases cannot be rejected. A stable phase cannot have a candidate-positive, actual-zero coordinate at a recurrent pair, or its frequency tends to zero and forces rejection. The conclusion is H_θ(e)⊆H_σ(e) on recurrent pairs, **not equality**. Inclusion transfers candidate reachability into actual recurrent closure. It forces a component entry or revelation during navigation and every candidate-component pair to recur after retention. Extra actual exits would advance the phase and so cannot persist in a stable phase. The common even priority then supplies success. Trusted exact supports remain an input assumption, not something recovered from finite observations. [HC331, §12]

For general mode-owned priorities, even the support/equality skeleton does not select a common winning policy. Compare two positive Bernoulli instances with parameter pairs(1/3,2/3) and(2/3,1/3), identical supports, empty within-instance equality mask and opposing eventual-action objectives. The first with no change and second with immediate change have the same Bernoulli1/3 observation law, but require eventual exclusive actions0 and1. Their success events are disjoint under the common law, even with private randomization. Numerical calibration therefore matters for **policy selection** although the skeleton decides existence. A common lower bound1/3 does not remove this obstruction.

Nor is a finite program the same as finite memory. A time-homogeneous finite-memory randomized controller on the unequal full-support Bernoulli example produces two finite product chains with the same reachable bottom components. Winning in mode0 requires every vertex of every reachable bottom component to choose0; winning in mode1 requires the same components to choose1. Both are impossible. An empirical learner with unbounded counters wins. This memory separation needs at least two actions and two physical states for the stated example and is not a lower bound for the common-priority subclass. [HC331, §§12–13]

#### 7.20.9 Discriminating controls and formal interfaces

The two-state one-action separator is stronger than an unsupported warning about switching. Mode0 alternates q,r and mode1 fixes the current state; common priorities are0 at q and1 at r. From q, no change and immediate change win, but a switch after the first action remains at r forever and loses. The known region is{q}, the uncertain region is empty. With one observed state a common winner of both fixed modes cannot give this gap: intersect the two conull seed events and note that a finite change alters only a finite priority prefix. The source controls exhibit the separator both on the actual evaluator and through bound negative evidence. [HC284] [HC409] [HC365] [HC331, §13]

Controller refinements matter independently. `Follows` in the dynamics source records only structural recursion; it assumes no fairness or success. The invariant and modulo-two barrier prove phase stabilization using eventual final-mode support and the all-time true-row gate, leaving the finite old history inside the test. [HC430] The rejection-before-revelation mutant requires both a mode0-zero receipt and rejection=false before setting known1; its concrete control presents revelation and rejection together and so exposes the loss of precedence. The clears-known mutant resets known1 on its next known-layer step, contrary to irreversibility. The strict-discrepancy mutant uses ε<distance rather than distance≥ε and has a zero-tolerance exact-equality countercontrol. Two deliberately false timing equalities target dropping modulo-two alternation and treating2<2 as true. They are negative controls, not new positive proofs or fresh observed compiler failures. [HC287] [HC443] [HC378] [HC461]

A separate coherent stale-data path retains exactly one old observation of a transient pair. Without the phase-dependent gate it rejects the true row at every time, so no all-time phase barrier exists. The ordinary companion strengthens this into a positive three-state plant whose frozen transient count makes every true odd phase reject after at most one action; action0 then recurs under final mode1 and the weakened learner fails almost surely. The original count>phase gate excludes the frozen count1 in every odd phase. This refutes that specific natural weakening, not every conceivable forgetting or ungated algorithm. A control also distinguishes a policy's initial action from the restart after a remembered prefix. [HC265] [HC331, §13]

The parity bridge separately proves that an eventually constant governing tag leaves the same recurring physical pairs and final-mode priorities, and transports positive post-final-mode prefixes to stationary restarts. This prevents a finite-prefix tag from being mistaken for an extra infinitely recurring priority. [HC250] The ControllerAxioms, EndpointAxioms and expanded ReviewAllAxioms files specify declaration/axiom readback surfaces for the controller, law, restart, recurrence and stability chain. They are requests to inspect these declarations, not observed clean-axiom output. Their interfaces remain necessary for reproducibility; no new compiler, kernel or audit execution is claimed by the present integration. [HC262] [HC358] [HC396]

The direct rational and dynamic providers make the implemented gate precise. `RationalTest` computes from the **whole** acquired history, requires actionCount>phase and rejects at deviation≥epsilon. Epsilon is half the minimum positive live-support coordinate gap, or1 if no positive gap exists; the source proves positivity, separation and rational/real test correspondence even on zero-count or malformed histories. `DirectDynamics` then proves active-pair membership from certified stage invariants and supported feedback, phase increments of0 or1 under stable support, and retained-component persistence when phase and rejection remain unchanged. A true candidate with a negative test cannot exit its certified component through supported feedback. These conditional pathwise facts do not replace the probabilistic regularity argument. [R750A-510] [R750A-547]

The exact controller controls pin down sorted cycling with global offsets, alternating candidates, retained known components, unreset empirical history, a single phase increment for combined reject/exit, and mode0-zero revelation priority. In contrast, `MutationDeletesCandidateOne` tests **mode1** row zero before setting known1. That branch is the opposite of the positive control, despite inherited prose about not deleting candidate1. The independent odd-residue source also deliberately asks a mode1 arithmetic residue to equal mode0. Finite region controls distinguish numerical row equality from common support, even from odd minima, connected from disconnected loops, and action permission from merely staying inside the region. These source controls specify their mathematical and rejection targets without being counted as fresh executions. [R750A-536] [R750A-504] [R750A-508] [R750A-535]

`HiddenChangeTaggedLaw` defines the tag erasure used in the law bridge: the policy chooses its action before the adversary chooses the next tag, and the physical state/action pair depends only on the erased history, not hidden tags or the adversary seed. Irreversibility and the actual selected-row cylinder factors remain explicit. Its fixed/adaptive whole-law equations instantiate the inherited stack machinery; they do not claim a new generic iid theorem. [R750A-551]

The rival-parity provider uses a positive **original** recurrent event with P0 compatibility only on that event. A countable deterministic prefix fibre retains positive mass and the acquired posterior; matching complete final-mode rows gives the surviving-tail comparison, from which universal fixed-index winning forces an even rival minimum. It does not substitute global no-exit, global compatibility or fairness. `PrefixTransportControls` exhibits the reason: a late legitimate prefix has probability1 under no change but0 under stationary mode1. Comparing continuations at that same prefix and switch time is valid; conditioning on the impossible stationary prefix is not. Its shifted index saturates at zero. [R750A-534] [R750A-572]

Finally, `ReviewEndpointControls` separates measurable policy, lawfulness on every history and almost-sure parity. A null-seed violation, an off-policy violation, a nonmeasurable choice under a coarse seed sigma-algebra and a parity-winning forbidden action each omit a different duty. Literal input labels, menu order and initial state remain bound. Compilation of malformed evidence retains its lawful fallback, not a winning guarantee; measurable lawful randomized existence and the derived deterministic-existence endpoint retain the full stated premises. [R750A-573]

[R750A-504]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/86ad158a1fbd6a30a2fa9e64c0fb632f03aef6f9621c848d55bbe9d2b4e2c67b/MutationDeletesCandidateOne.lean
[R750A-508]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/87492a1bb30d9ec5e906289fbac128b005a6defbef99a8c79ea1a666690211fa/PhaseArithmeticExpectedFailure.lean
[R750A-510]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/87cfb72769c42a459d47eb0c7e3468882ba196abcb709f79fd5febbc34b8d2dc/RationalTest.lean
[R750A-534]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8ee817790b80b391e4c57cbec91295214dbc3ba3de4e7dc04f66fc683397638c/HiddenChangeRivalParity.lean
[R750A-535]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8f16386b7799d3428ecd928ed9a365ce23021df0521371266000979097a3f274/FiniteControls.lean
[R750A-536]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8f16b47f50f573c74395fc042eb60b53bdf6494e8861d2e262e30e8fbe76e162/ControllerControls.lean
[R750A-547]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9292534e7bad1c144b5ae374c8de7e768268cbd865a56a1eb277d0e68fef3525/DirectDynamics.lean
[R750A-551]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/93af2d6a58792060dc2cd7a8bd2723f2d5f3b59c8313926666ffbb20f79fe0b2/HiddenChangeTaggedLaw.lean
[R750A-572]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/99ed6e991f7a1e96bced15fcf85adb43106052390802ed140d2fd37fd18a500c/PrefixTransportControls.lean
[R750A-573]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9a0ac8c22cf75b51e02a5b4e0b4bb2bc89fced80e39c35d7f59fd2ae82350c3f/ReviewEndpointControls.lean

The additional direct controller and stability sources make explicit where the preceding positive guarantee is earned. Phase and retained memory are computed solely from observed action/state history. Normalization chooses a certified target component when one is available and otherwise uses the stage menu; support changes and rejection clear stale memory. These invariant proofs are parametric in the supplied observed-history rejection test. In the known-model layer, revelation persists, so the known1 state eventually stabilizes. For histories following the controller on an admissible input and valid body, region validity, positive known-model transitions and **eventual phase stabilization** imply that the retained mode eventually remains absent or equals one fixed component. That last stabilization premise is not proved merely by naming this layer. [T750-C731] [T750-C743]

The arithmetic stopping lemma explains one such premise precisely: unit increments or stays, together with stopping at the prescribed residue beyond a threshold, force eventual constancy without restricting the initial finite prefix. Dropping the stop condition permits p(t)=t; allowing jumps of two permits p(t)=2t to skip odd stops. The necessity controls likewise distinguish no-change winning from all fixed-index change laws, positive past mass from an unselected branch's mass, and an old positive prefix from support under stationary post-change dynamics. These are specific counterexamples to stronger hypotheses, not denials of the common-controller theorem. [T750-C713] [T750-C669]

The lawfulness bridge proves source-labelled policy lawfulness equivalent to the original common-menu condition on **all public histories**, with the necessity wrapper retaining measurability, admissibility and WinsAll. Erased-history controls give identical visible histories across hidden mode tags, so an adaptive policy cannot branch on those tags. Action-first adversary choice, irreversible change and a fixed switching schedule remain distinct interfaces. `MutationTagPersistence` removes persistence of the previous mode while retaining an irreversibility assertion; a constantly false adversary defeats that assertion. `MutationParityGivesLawfulness` attempts membership of an excluded action. Those two mutation files receive no positive theorem credit, and their expected rejection was not rerun. [T750-C707] [T750-C746] [T750-C676] [T750-C720]

[T750-C669]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b43c7809e91b99904102d0d82dbcc85703a232d84d8b8ddaefef69fdc6620ebe/NecessityControls.lean
[T750-C676]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b687a7cb8d4f0af9ed457ebaa2d5f7f211a15cca2f7da8683452d579f95c5dac/MutationTagPersistence.lean
[T750-C707]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bf366a159a49dbaf5ae4986812b1302a955403fa20663d74d3343206e373309b/ContractLawfulnessControls.lean
[T750-C713]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c1101224054d587b115631a9dd2c17020430497cded524334360d6bb5e39a743/PhaseArithmeticControls.lean
[T750-C720]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c27cfc7f57669f88fca7abc18f3c8a3fe89e44469e307ee141b39e1299ecddb1/MutationParityGivesLawfulness.lean
[T750-C731]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c68605b22b1c74bdacaec0c586e35f19e80a7154d3d31b3c2edac05feda0f5a5/DirectController.lean
[T750-C743]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c9c82b598c3df411010cb4677544efd5c49694f21754ffb356389b7b7b0ffc7a/HiddenChangeControllerStability.lean
[T750-C746]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cb3d94187d641c366a32c5c6e6097c4b4e660446ac74d3066e10efc46aabc22e/TaggedLawControls.lean

The further finite controls distinguish three semantic duties that a successful-looking receipt cannot discharge. In the branching two-state example, one positive receipt stays in W={0}, but another positive successor leaves it; consequently (0,0) is not uncertain-allowed. The `MutationChosenReceiptClosure` file asks for exactly that rejected membership. Another model has equal supports but rows (1/2,1/2) and (1/3,2/3), so the candidate can be uncertain-good while its numerically unequal rival has odd minimum. Most decisively, an excluded-action policy actually wins every fixed-index parity law, yet is unlawful and no positive lawful body exists. Objective success cannot supply the common-menu premise. [F939-C916] [F939-C906]

The certificate controls make admissible shape more precise: the consistently empty known region K, empty D1 and empty known-obligation list can be accepted, and K/W overlap is also permitted. Keeping old obligations when K is emptied, omitting either mode's uncertain obligation, duplicating known or uncertain keys, altering routes or revelation endpoints, or using an empty common menu is rejected by the specified checks. Candidate 0 cannot justify a mode0-zero revealing transition. Both layers use the full-support common menu even when a singleton-mode menu is absent. The basic controller fixtures supply one-state/two-action, revealing and unequal-row inputs; they are data and source assertions, not an additional general compiler theorem. [F939-C898] [F939-C913]

A two-state/one-action separator with the same priorities in both modes has knownRegion={0} but uncertainRegion=∅. Equality of priority labels therefore does not erase the information-regime distinction. A separate contracting operator removes 0, then 1, then remains empty: stabilization can genuinely require two strict removals. Neither fixture licenses replacing the n-step finite descent by one application. All outcomes here are the exact source statements and interpretations; this consolidation runs none of their `decide` or audit commands. [F939-C936]

[F939-C898]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f5c7559218224928217a470ffd10d27b1fcb091e063eb3d8e037d2982b24d03b/CertificateControls.lean
[F939-C906]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f936ca1a2e3d6fff6e59aca60e60152762f48abc4d867f534e402ea229986c46/MutationChosenReceiptClosure.lean
[F939-C913]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fb4fd31e67bfe4c88fc78b6713ef9d03a6e3261d2f509cef757501c46182f9b4/ControllerFixtures.lean
[F939-C916]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fbe81e88a1cdbc82cdbd0d9d74d176db2f0c6c9d75b65275ada0e8bcab919d85/ReviewSemanticControls.lean
[F939-C936]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ffb2a7a3acd1c3495a6b7c53c1bf402b0f3bcb3d4173efab691ce974551bcf37/GreatestRegionControls.lean

#### Implementation evidence, restoration of replay and later environment qualification

The four-state supplement provides a discriminating finite control that the smaller fixtures cannot express: threshold removal of low-odd bridge actions exposes two simultaneous nontrivial two-state maximal components. In the equal-row anchor, the blocks attain their two mode-owned even minima at different pairs. Removing one rival-even witness invalidates only its block; removing the forward bridge prevents the surviving block's witness from rescuing an isolated bad block. Equal support with unequal probabilities, and matched versus revealing exiting successors, distinguish numerical evidence from whole-action closure. Its eight labelled templates at four initial states give 32 complete inputs, not 32 graph structures or an exhaustive four-state census. The guide reports 30 positive and two negative checked bodies under one capped campaign; the source explicitly treats timeout and incomplete coverage as execution failures. No new campaign was run here. [Q250D-200] [Q250D-243] [Q250D-244]

Historical component acceptance and package replay have separate scopes. The Eighteenth summary records a full author custom-source replay but an independently accepted recovered composite: 187 retained hidden-change units were checked, two missing controls completed, and the full HasE lane rerun. Interrupted original receipts remained nonterminal. The runner now requires every declared source and control, fresh successful objects, qualified expected-failure diagnostics and exact axiom-audit counts. A missing import, timeout or unrelated elaboration failure is not credited as a mathematical negative. These are the source-reported historical results and the inspected runner contract, not a fresh kernel run in this refactor. [Q250D-201] [Q250D-202] [Q250D-205]

The earlier prepared-environment limitation is not the last word on acquisition. A separately qualified hidden-change recipe reports restoring the exact 6,646-object inventory: 6,641 official-cache outputs plus five newly compiled Cache-tool objects, with source, toolchain and fresh Mathlib-import checks. This supplies a narrower acquisition route without rewriting the base package's historical statement. It is neither a dependency-theorem cold build, a clean-new-host installation nor a second full hidden-change proof replay. The HasE 1,369-object environment remains distinct; fourteen of its same-named Mathlib objects differ from the broader cache inventory, and common source revisions alone do not authorize substituting one inventory for the other. The recipe preserves failed/started receipts and refuses to overwrite them; that custody property must survive migration of its consumers. [Q250D-203] [Q250D-245] [Q250D-246] [Q250D-247] [Q250D-248]

Finally the HasE endpoint transport and its ordinary normal-form diagnostic must not be conflated. The diagnostic reads exact exported SKI syntax, uses capture-avoiding de Bruijn beta/eta contraction with explicit fuel and seven self-tests, and compares two displayed normal forms. It is a finite ordinary calculation, not a kernel theorem of general nonconvertibility or compiler-image membership. The source summary retains the literal frozen compiler x/x+0 question as unresolved and records a positive inhabitant of the reflexive endpoint target, preventing a rejected cast from being promoted into universal noninhabitation. [Q250D-202] [Q250D-204]

[Q250D-200]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0a3d9345f1ca6fced6c69af1db53b34deab96bf71987668b279e10914664c0a9/README.md
[Q250D-201]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/26c5929222fdfe39073848892dc2b5e512c0292e923749107c11898fedc45f34/README.md
[Q250D-202]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/164789fddd3ade86d576d6c1c3a6b06cd31c62328657b3f2f7ce9e4e323e8978/VERIFICATION_SUMMARY.md
[Q250D-203]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cae78b6cc70bb3a5f1592f03ac9442e189e2b96c5d31422c16eea1f925decc20/ORIGINS_AND_AVAILABILITY.md
[Q250D-204]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/093857b23dac06e14ec7da11a3be91cc356af1a498c93fed51a6e5ab32d99504/check_lambda_normal_forms.py
[Q250D-205]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4b1522dbe651ac97bece149b2fd21c8fc0688a87ac7bbd10e1f761bcf80d9adc/replay.py
[Q250D-243]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/89a3add9be4b25912e773341b47066ac4e2815fadfda1d90ae5d32bfa35f558e/README.md
[Q250D-244]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/54d3331b984636eb15aaa4dd783995fed6147a527be15d1c6afa99bb5a993fe1/run_control.py
[Q250D-245]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6cb3686f8225216646c469db8e15f29aa9b9c87994aefe0ade57b4dfaa12cded/README.md
[Q250D-246]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9a4255223c8c149ffb0c6dd267c8721725106e046040652a89035b3052839abe/QUALIFICATION_PLAN.md
[Q250D-247]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c34a8b5c5105e4308abf7b888b9b3fce57c0906d13d93c3fdf36e4633590c8e5/provision.py
[Q250D-248]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7b0eef9674097a729fc5e1b55cadcbac13948c4baafcc9ef6f552f044b9976df/test_refusal_custody.py

#### Exact sources for the one-change extension

[HC17]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/04a7cfa782f9cb6b50a7b8b7a7b1fc3d56e903871286934c6222b5af6c883d50/MutationPrefixReversal.lean
[HC33]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0843f7c2f1bfe6f835ab5a0ff28f6ef0560961149110cc534a29af13e85fa38f/MutationDropsNewReceipt.lean
[HC67]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/12a83f613cea2de432415a9628c79bd245bab092e58231d9f7e021058f57a5ca/MutationUnconditionalRivalParity.lean
[HC92]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1da85dc06dd0002214643fec081dcfc9392e00dc96c4e095448824b3aa59f76b/EndpointLawfulnessControls.lean
[HC119]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/23b268c2e96015781fbb2cbfe7a25457004d3846ab207ced577dd06f1c595bfc/MutationSupportImpliesMatching.lean
[HC130]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/274a039f6dbe1a31341394423bd61a606ee979422197d8fb23db2612ce62ae32/EndpointInterfaces.lean
[HC134]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2988efa498c9cd33d09a3ec4728965316d4d69a97db526676bb1433e2d62df12/MutationPositiveDropsInitial.lean
[HC135]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2991a4dd8faafbd6b0da6c159a9f5487e50f794c11a46d13fc8ab86ded643762/MutationStationaryPrefix.lean
[HC155]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2fec13712488b3fc671d7edb0ee9f3776b6f2941ee38672c6514de308e0d0f6e/HiddenChangeControllerParity.lean
[HC171]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/345c6c01770f9e5169679f738183f7f5e79a4dad29ea9eb0c4216375af046fd2/HiddenChangeKnownProgress.lean
[HC177]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/358e0581b17182bc7e42fafa2bf5b0ee5b5843d23a8d33153b86b2390d5ce083/MutationDoublePhase.lean
[HC178]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/35963bfdab6f60e730e76711921b358ecd0e136293c1fb98233b49155e18c428/HiddenChangeBinding.lean
[HC183]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/36f0e653ad31e4a4e7c7dd9716f66c709478a4aa2095670e9992a911228ef23e/NegativeTraceControls.lean
[HC184]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/37211b5ded947f0b48f46b39c2f9ee81b353e24fafd8bc0944118ea74de94394/HiddenChangeFinite.lean
[HC186]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/37ccc58c3b6aba817ff922e7e5c5782ff5a7735f8d208fca7c285c2320465c03/MutationWinnerDropsParity.lean
[HC192]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/395ab119cd2e4eb25902492cafad8153563a126ae81cad8a4d0bf88bb97ef6d4/HiddenChangeContamination.lean
[HC198]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3a65d9812276aed807382f1a7b165864a2d5ed53075313a7c32e132b455324c0/ReviewAllAxioms.lean
[HC202]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3b218331b2d9f040763097702b15bac7488a2939930a7039e0682afdeedace49/HiddenChangeFixedIndex.lean
[HC208]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3d88b8221dfb58a4d8c35f2b2cd9ccb05405845296ea90870fa9d22578c723c9/HiddenChangeControllerEndpoint.lean
[HC244]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/44c0f751657993ffc655b9362f854abd77c4cf45fce1a3adc5692b5d4852d604/MutationStrictPostSwitch.lean

These links retain the exact public source edition. Native blob, SHA-256 and source-role checks were made against the admitted source identities; no original program or Lean kernel was executed for this integration.


<a id="third-cohort-b-hidden-change-provider-scopes"></a>

The intermediate providers have narrower endpoints than the completed parity theorem. For a submitted body satisfying `BodyValid`, `HiddenChangeControllerSafety` constructs memory/component validity on every public history; its active and safe-action consequences additionally require `RegionValid`. `HiddenChangeControllerActualLaw` supplies causal recursion and governing-row support under the actual fixed-change law, then obtains almost-sure region invariance and eventual phase stabilization for the literal accepted compiler, under input admissibility and a successful positive check. That module explicitly stops before full component recurrence or parity. The later endpoint in §7.20.4 supplies the remaining recurrence and probability bridges, so acknowledging this modular limit neither removes the completed theorem nor credits it to an earlier provider alone. [T750B588] [T750B602]

Two mutations isolate separate uses of counting. `CounterReset` always calls the generated phase policy with cycle counter zero; retaining the same menus and phase-memory types cannot then supply repeated-visit cycling. `MutationLiteralCandidate` instead fixes candidate(r)=0, while its final test demands candidate(1)=1. Losing action cycling and losing candidate alternation are different changes. Neither mutated body is a second positive controller proof. [T750B616] [T750B639]

The positive review controls permit an empty known-mode region when no revealing receipt can occur and exhibit a stable candidate that is globally wrong while every retained row matches the actual mode. They also retain old pair/receipt counts after revelation and preserve an already retained component even if another comes first in list order. For the same measurable policy winning at every fixed switch index, rival parity is earned on a positive recurrent event with zero-compatible prefixes and full numerical row matching; this does not require global zero compatibility or license replacement by support equality. These are source-bound invariants and controls, not a fresh execution or an extra fairness assumption on the final theorem's caller. [T750B597] [T750B605]

[T750B588]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/9cd9993d4c5a1087282c28a82d1fe2fa52414bebfc3aceaa207382686121b423/HiddenChangeControllerSafety.lean
[T750B597]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a04e27e0f5734b446bcd607c761aae91ea91f0cbbf70d3faa99db376c8d67d9c/RivalParityControls.lean
[T750B602]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a23216ba3eb1eb6ded572ce7068d246065bb375a260e41e3f952bb7088e17c42/HiddenChangeControllerActualLaw.lean
[T750B605]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a343e82d8cf336b4e059545f43e76b17269cf943dfdac686a365f0c58f9411b3/ReviewControllerControls.lean
[T750B616]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a770f7c822785c7243dc5f7c39e693c80af8fde51ca23b68d17fc3826b41e467/CounterReset.lean
[T750B639]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ad6a7aea0a9d7e5ce528c89ae695fa8cb5e3ef6dc42c649072d75c6a62298716/MutationLiteralCandidate.lean

### 7.21 Exact criteria, opaque search and the operational meaning of a repair

The preceding constructions distinguish a winning policy from justified cognition. A complementary group of results makes the interfaces between evidence, criteria and mediated action explicit. Their positive conclusions are conditional mathematical results: no predicate certifies its own source authenticity, real-world adequacy, institutional legitimacy or physical implementation. The exact cardinality and search statements below have different scopes from the temporal interlock; neither silently supplies the other's premises.

#### Defeat and transport require coverage of the relevant witnesses

Let eligible, defeated and authoritative be predicates on candidate grounds W. Token sufficiency means that some eligible witness is authoritative. If every eligible witness is defeated and defeat excludes authority for each witness, token sufficiency is impossible: take the alleged sufficient witness and apply those two premises to it. Defeating one designated whole is weaker. On Bool let only true be defeated and only false authoritative, with both eligible. The whole true is defeated while a sufficient proper-subset witness false remains. An alternative route is explicit upward sufficiency: if any eligible authoritative witness would make the whole authoritative, insufficiency of the whole excludes all such witnesses. Neither closure premise follows merely from naming a basis complete. [T07F034]

The source-bound cold assessment makes the intended quantifier explicit: defeat must apply to **every eligible sufficient witness wholly supported by the full token basis, for the same judgment and respect**. Its countermodel to defeating only the whole records an acknowledged formalization obligation, not a newly discovered refutation of that stronger intended meaning. Upward sufficiency is one possible repair, but it is substantive where adding defeaters can undermine authority; witness-relative defeat states the intended condition without making all normative reasoning monotone. Calling existential token sufficiency “exclusive closure” would add a further claim: existence of one token-supported sufficient witness does not say that every possible authority is token-supported. [N250A-011]

The concrete exact-byte correction below leaves its recovery standard, source identification, inferential resources and scoped permissions intact. It therefore witnesses retained-standard correction, not the existence of an objectively justified correction whose entire authority basis is defeated. Shrinking that basis after the correction to include only the failed first-order checker would manufacture radicality. The assessment's five responses are an overlapping dialectical taxonomy: a retained meta-standard denies full-basis radicality; a trans-state standard supplies a different kind of authority; a holistic fixed point still needs a constitution and selection warrant; a primitive normative fact remains a logical option; and relativization or error theory rejects or weakens the robust correction premise. Holistic and primitive accounts can also be trans-state accounts. Bare unconstrained predicates do not prove that these responses exhaust all cases without an authority-existence/classification premise. The report preserves the historical unadopted status of that assessment and derives no proper-function theory, source necessity, Wisdom or common metaphysical bearer from the local checker. [N250A-011] [N250A-015] [N250A-016]

An exact criterion for target t accepts x precisely when x=t. Two criteria adequate for that same target have the same extension, though they may use different implementations. A representation f preserves this exact criterion at t precisely when the fibre of f(t) is the singleton {t}. To preserve exactness at every target is precisely to make f injective. The proofs substitute the equality criterion in each direction; a wrong x with f(x)=f(t) is the explicit false acceptance when singleton-fibre adequacy fails. A useful normalization can therefore preserve one declared standard without preserving an exact-byte standard. The representation and the standard must be specified together. [T07F034]

For source evidence class E_U, recipient class E_V, relation R and claims p,q, define robust validity by truth at every admitted evidence-world. Suppose each v in E_V is related to some u in E_U, and related admitted pairs carry p(u) to q(v). Source robust validity then gives recipient robust validity by selecting that covering u. The backward coverage premise is necessary for this transport schema **uniformly over all predicates**: use p=True and q(v)=“some admitted source u relates to v.” It is not necessary for every fixed independently warranted q. A Unit source related only to false in a Bool recipient class preserves the claim v=false on related pairs while failing at true. The same missing coverage does not prevent the independently true constant claim. Actual truth additionally requires that the actual world belongs to the evidence class. This robust model is not a definition of all ordinary epistemic warrant. [T07F034]

Likewise, at one fixed observation o, a policy on observations can choose a good action in every admitted world with that observation iff there is one action good in all those worlds. Forward evaluate the policy at o; backward choose that action constantly. The fact that each Bool world w has its own good action a=w does not supply a common action. A guarded compound action can change the answer only by being included as a distinct available action, with its guard and execution semantics exposed. It cannot be silently counted as an unobserved-world choice. [T07F034]

#### Guarded correction is stronger than rejection and narrower than an oracle

A minimal draft state records source, draft, revision and history. An accepted step requires an allowed contextual guard and a payload equal to the source. It replaces the draft by the source, increments the revision once and appends the old draft to history, while retaining the source. A rejected step leaves everything unchanged. Every step preserves the source; if draft=source already holds, every step preserves that equality, and induction gives persistence under any finite list of mediated steps. Rejection alone does not repair an initially wrong draft. The Boolean guard is an input premise, not a truth or permission generated by this program. These conclusions separate effective restoration, preservation and refusal. [T07F034]

A further logical control concerns infinite explanations. Both the constantly true and constantly false sequences satisfy P_i↔P_(i+1) for every i. An infinite recurrence by itself fixes no truth value and supplies no normative authority. This does not refute a productive or source-grounding argument with additional substantive premises. [T07F034]

#### Actual roots, interface labels and the fixed-family threshold

The attribution results count actual independent roots rather than merely labels. In the stated one-collapsed-class model there are m labels, a class A of size c≥1 identified with one root, and singleton roots outside A. Thus the number of actual roots is m−c+1. For label sets P,R, the common-root count has two contributions: labels in P∩R outside A, and one bridge root if both P and R meet A. The bridge can exist without a shared label in A. For a nonempty intersection I, minimizing over c-subsets gives the natural-number expression |I|−c+1, equivalent to max(1, integer(|I|)−c+1); the empty-intersection case requires its separate analysis. Under B≥1, c≥1 and c≤m, robustness of P,R against all admitted maps is exactly B+c≤|P∩R|. Source212 states this theorem's parameter-complete interface. The B=0 corner has a distinct forced-bridge condition, so dropping B≥1 is not licensed. [T07F106] [T07F212]

An actual fault set of size at most B taints at most B+c−1 labels. Conversely every maximal k-set of labels, k=B+c−1≤m, is realized by a c-class and B actual faulty roots with exactly that pullback. Hence universal real-root availability of a fixed family is equivalent to avoiding every k-set of labels. Source199 records the exact interface, including B≥1, c≥1, c≤m and k≤m. The central fixed-family theorem uses the stronger B<m−c+1 and therefore k<m. [T07F106] [T07F199]

For two families F,G chosen once outside all map/fault quantifiers, the safety-and-availability contract is feasible exactly at the threshold m≥3k+1 under the stated parameter restrictions. The lower bound does not assume uniform families: choose a k-set T and P avoiding it, so |P|≤m−k; choose min(k,|P|) labels of P, extend to a k-set and obtain R avoiding them. Then |P∩R|≤|P|−min(k,|P|), incompatible with the required overlap >k below the threshold. All (m−k)-subsets attain the upper bound. These are fixed families, not families updated after learning the hidden map. [T07F106]

The Option-valued canonical root map is a representation, not another physical assumption. Any map whose equality fibres are exactly A and the singleton outside labels has the same counts. The source map reports cardinality-preserving fault transport in both directions, restricted to actual image roots, and correspondence to the earlier representative-index and Bool/Nat interfaces. Its audit file requests axiom and signature readbacks for these count, image, availability, fixed-family and correspondence statements. Those commands are not their outputs. The theorem map's historical acceptance statements are not a new compilation or a proof that a physical service satisfies the premises; its A–C packet explicitly does not establish the dynamic cancellation story or covering-search optimum. The latter requires the separate argument next. [T07F106] [T07F035]

The complete attribution review and target specification now supply the more precise warrant for that historical formalization claim. They report all-parameter acceptance of the root-image equivalence, actual-root availability and arbitrary fixed-family threshold, together with representation transport and separately bound actual-root corollaries. They do not count covering/search closure, physical cancellation or temporal applicability as part of those A–C targets. In particular, “every fault set of at most B actual roots leaves an untainted shared root” is equivalent to the shared **actual image** having more than B members: if its size is at most B, the whole shared image is an admissible fault set. Combining the fixed-family threshold with n=m−c+1 gives the sharp actual-root minimum n=3B+2c−1, an excess 2(c−1) over the known-attribution comparison 3B+1. The comparison does not itself establish either design's operational applicability. [N250A-000] [N250A-001]

Two admitted Python checkers retain different finite representations of this interface. One constructs explicit partitions and images for 2≤m≤7; the other represents labels and root images by bit masks for 3≤m≤7 and separately checks selected minimum constructions. Both expose alias bridges, maximal-taint realizations and the failure of counting two aliased cancellation labels as two actual roots. Their finite domains do not replace the generic proof. The review reports fresh Lean compilation and a transitive standard-axiom audit against its pinned dependencies, while disclosing reused dependency libraries and a wrapper needed to run the regression/supplement stages absent from the central entry point alone. Reading those reports and checker bodies here is neither a new kernel replay nor an inspection of the unadmitted dependencies they cite. [N250A-000] [N250A-029] [N250A-030]

The direct deletion and regression witnesses retain all these parameter restrictions. For B=1,c=2, the fixed-family threshold is m=7 rather than6; for B=1,c=3 it is m=10 rather than9. Aliased labels count as one root, while disjoint label sets can meet through the same collapsed class. The controls separately remove positive B, positive c, realizable class size, realizable taint size, family availability and pair safety. Impossible class/fault sizes can make universal clauses vacuous. Transport of faults under a root renaming is restricted to the actual image; arbitrary unused codomain labels are not faults of the original system. These are the concrete discriminators for the theorem above, not new thresholds obtained by counting fixtures. [R750A-501] [R750A-502]

The named `count_labels_as_roots` mutation makes the precise forbidden replacement: `rootImage A P` becomes `P.image some`, ignoring A, while the retained proof text still claims membership of `none` exactly when A meets P. A `some`-only image cannot satisfy that claim for a nonempty intersection. The subsequent copied `robust_iff` text is therefore not independent positive evidence for the accepted root theorem. This exact definition-level mismatch is retained as a mutation boundary; no fresh compiler failure is asserted. [R750A-532]

[R750A-501]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/865e2cc5857e5fac8993d4b4998fe78dcc62aee76e469b244edd6a99726df0bd/DeletionControls.lean
[R750A-502]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8685cb09f2b0a9613076846451bbaf12b653143bff31e07f9820c3c1d39a63f1/Regression.lean
[R750A-532]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8dc2354a610673aaa0418dd47dcb61e9648f347d0f12027bcb26b9b21cad188b/count_labels_as_roots.lean

The arbitrary fixed-family result supplies more than a symmetric-threshold calculation. For k≤m bad labels in an m-label universe, let F and G remain available against every k-set and require every P∈F and R∈G to intersect in more than k labels. Choose an available P avoiding a k-set, so |P|≤m−k; then choose R avoiding up to k labels of P. Their required intersection gives |P|≥2k+1 and hence m≥3k+1. Conversely, all (m−k)-subsets attain the contract whenever m≥3k+1. Thus the lower bound covers arbitrary fixed families, not only equal-cardinality quorums. The k≤m premise prevents availability against nonexistent k-sets from becoming vacuous. [T750-C741]

For one hidden alias class of c labels and B faulty actual roots, the pullback has at most k=B+c−1 bad labels, and maximal taint sets are realized by a class root plus singleton roots. With B,c≥1, c≤m and B<m−c+1, the actual-root fixed-family contract is equivalent to that label contract. Feasibility is therefore exactly m≥3(B+c−1)+1, corresponding to m−c+1≥3B+2c−1 actual roots at the minimum. The threshold argument and the arbitrary-family theorem use this same correlation accounting; neither grants a hidden-root oracle or supplies live permission. [T750-C748] [T750-C741]

[T750-C741]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c9aaf517e6a33002e0525f8cf4f9a381ad12ed9d1d3f12d67c1b75950401724e/FixedFamilies.lean
[T750-C748]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cbf291fec343e9b9e9eb62cacf9dbef810541f8b0d729a7c077b1ef62cd03b7b/UnknownRootAttribution.lean

Two three-label interpretations isolate the fixed-family theorem's essential quantifiers. At k=1, the family of all two-label subsets is available. Pairing it only with the singleton family containing the whole three-label universe gives intersection size2, yet that second family is not available and m=3 remains below3k+1. Likewise the two-label family has safe self-intersections, but {0,1} and {1,2} intersect in only one label. Diagonal safety does not supply safety for **every cross-family pair**. These are explicit premise-deletion witnesses, not contradictions of the jointly available cross-pair theorem. [F939-C933]

[F939-C933]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff3f5ac1046b9744f6bcb4d55424520c8ba57994b66c8f6c069e7971caca1c83/FamilyDeletionControls.lean

#### Full-history adaptation cannot beat an opaque failure spine

Fix a finite prepared family F of q-label paths. A deterministic policy sees its entire selected-path/reply history, and each attempt has a fresh ordinal. A maximal bad-label world T has k labels. Physical success is exactly disjointness of the selected path from T. Opacity means that whenever a selected path fails, its entire macro reply equals a world-independent failed reply, which may depend on the attempt and path. Preparation, cancellation, timings and nonce can all be represented inside that reply; success replies are unrestricted. [T07F147]

Run the policy against that failed-reply oracle to obtain its failure spine, and let F_N be the distinct paths it selects during the first N attempts. Until the first success in any world, induction identifies actual history with the spine history. One can prove this induction either from failure of all earlier spine paths or from failure of all earlier actual paths. Consequently success before N in T is equivalent to some path in F_N avoiding T. A universal N-attempt cap is equivalent to availability of F_N. The family remains q-uniform and |F_N|≤N, even when the policy repeats paths. Complementing paths turns availability into a covering problem, giving

```math
C(m,m-q,k)\le N.
```

Here C(m,b,k) is the minimum number of b-subsets covering every k-subset. This lower bound permits full-history adaptation; it relies on opaque failures, a fixed prepared family and the stated physical success predicate. It is not a lower bound for an interface that leaks additional world information. [T07F147]

The bound is attained when q≤m and k≤m−q. A minimal available portfolio is nonempty because maximal k-worlds exist. Enumerate each member once using history length, then repeat an arbitrary member if needed. This nonadaptive policy succeeds within the portfolio's cardinality for every observation function, since every maximal world has an avoiding member. The formal enumeration uses a noncomputable finite ordering/choice, so the theorem supplies a policy-existence construction, not a newly implemented search optimizer. At q=m−k, each complementary block has size k and covers only itself; the exact cap is binomial(m,k). In particular m=3k+1, q=2k+1 gives binomial(3k+1,k). [T07F147]

The exact-cap interface quantifies over a prepared uniform family and its history policy and uses canonical homogeneous control replies **with a truthful physical-effect receipt**. A failed receipt is uniformly false, so it does not distinguish failed worlds. Under q≤m and k≤m−q, such a cap exists iff C(m,m−q,k)≤N. The same minimum-label specialization follows. Receipts therefore do not refute the lower bound: their precise information on failure is already included. [T07F145]

A more concrete action packages path, fresh nonce and one fixed repair body. The enumerating full-command policy sets nonce to history length, hence nonce n on attempt n for every reply history, and retains the same body on every history. For B≥1,c≥1,c≤m,q≤m and B+c−1≤m−q, it attains C(m,m−q,B+c−1) attempts against every actual root-fault set of size at most B. The proof transports availability to tainted labels and invokes the same avoiding member; it does not infer authorization or physical efficacy from bytes. A canonical macro observation may include a control payload depending on the **complete command and complete history**, together with an optional truthful disjointness receipt. On failure the receipt is false, preserving opacity. Authentication and authorization remain retained premises. [T07F238]

The small `RepairStateBridge` supplies the target-state interpretation needed by a disjointness-hit argument. After N rounds its Boolean target is true exactly when it was initially true or some earlier hit occurred. Thus defective initial states equate repair with a hit, whereas already-correct states need no intervention. This is neither a full physical protocol nor an unconditional lower bound on achievement from every initial state. The separate `Check` file requests the covering-number, opaque-action and repair-state declaration/axiom surfaces; it is not another derivation or received audit output. [R750A-509] [R750A-571]

[R750A-509]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8774d23d1435947d7986ad6e996384c0c195868eb0de900e9b689fc2a0bcd72e/RepairStateBridge.lean
[R750A-571]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/99ddf11ec3fc32e1cadd91b6281652df4b90bec6605c5b6eb1e62ce8985e5dca/Check.lean

The numerical covering notation is justified by a genuine transport theorem. A bijection of finite label types maps every block and preserves its cardinality, transports each k-subset back through the inverse, and hence preserves both uniformity and coverage. Mapping a finite portfolio is injective as well, so its number of blocks is unchanged. Applying this argument in both directions makes the attainable portfolio sizes, and therefore the minimum covering number, identical; the standard notation C(m,b,k) can use `Fin m` without depending on label names. A many-to-one alias map lacks this inverse and need not preserve either block or portfolio cardinality. This theorem must not be used to erase the actual-root correlation costs just derived. [F939A-791]

[F939A-791]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/d8b5e2ed9564e17ea3d2352286e5c9e78ac55cb495e907b4720d6b152b56ce12/LabelTransport.lean

The randomized boundary keeps the world outside the coin outcome. Under a probability seed law, if every maximal bad-label world succeeds almost surely within the same cap N, the finite intersection of those almost-sure events contains a seed. That seed selects an ordinary deterministic policy, so the same covering-number lower bound applies. Contraposition supplies **one fixed** bad-label world with a non-null failure set; the source-correspondence theorem realizes it by one fixed alias class of size c and exactly B faulty actual roots. The map and fault set are not chosen after seeing the coins. The positive portfolio construction separately covers every actual fault set of size at most B, including smaller taint sets. [F939-C901] [F939-C878]

The full-action independent check makes the failure quantitative. Put m=|α| and k=B+c−1. Assume B,c≥1, k≤m, a probability seed measure, all action supports in one q-uniform finite family, and opacity for every seed on compatible failed prefixes. If N<C(m,m−q,k), then one fixed actual-root world has failure **outer measure** at least 1/binomial(m,k). Finite subadditivity over the maximal-world failure sets yields that inverse-cardinality bound; no measurability of each seed-policy event is silently added. Opacity need not constrain reachable post-success histories, and the source supplies such a richer post-success example. The result covers adaptive full-action policies, not just a fixed query order. [F939-C910]

The corner cases are substantive: feasible covers are positive even at k=0 (the empty universe has one empty world and cover number1); there is no zero-attempt hit; oversized nonexistent worlds and zero measures can make universal or almost-everywhere promises vacuous. Smaller fault sets are handled by extension to a maximal set. Translating the hit bound into actual restoration still uses the defective initial target, as in the repair-state bridge above. These source theorems add no physical authentication, new execution or seed-dependent choice of the adverse world. [F939-C910]

[F939-C878]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/eef155e9c645c1bdfdb87ffd57d3f58531929a020d017fbdba77aa01e824d925/SourceCorrespondence.lean
[F939-C901]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f6e89ecca07f5b16f4200ce6673dfa1a96db3a5ce4379f6c73cb9eac85010efe/RandomizedSearch.lean
[F939-C910]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fab177fbbf567d5e7d5b99ef627d7d33ba7f863b8a9c8d4c1f5ad84476f52b7c/IndependentChecks.lean

#### Trading additional roots for fewer opaque attempts

The known-root instance makes the resource tradeoff explicit. With n actual roots, lifetime fault budget B, repair-path size q and revocation size r, retain q+r>n+B and q,r≤n−B. Complementing each repair path gives a block of size n−q, so the exact opaque macro-attempt cap is C(n,n−q,B). For fixed n,B,r, the smallest safe path has q=n+B−r+1. Feasibility forces r≥2B+1. Across feasible thresholds, r=n−B and q=2B+1 maximize the complement size and minimize the attempt count:

```math
M_{\mathrm{opt}}(n,B)=C(n,n-2B-1,B).
```

To justify the minimization, extend each smaller covering block to the larger permitted size. Coverage survives and the number of distinct blocks cannot increase. The improvement buys more revocation witnesses and actual root modules; it does not minimize every resource at once. A portfolio of M prebuilt q-gate branches uses qM gate occurrences but only n independently failing roots. Selection, shared writers and independently reachable control ports remain charged supports. [N250A-024]

For B=1 and n≥4, the blocks must cover n singleton faults and each has n−3 points. Counting gives M≥ceil(n/(n−3)); partitioning the points into groups of at most n−3 and extending the groups to blocks attains it. Thus n=4,5,6 require respectively 4,3,2 attempts, and every n≥6 still requires two. One cannot suffice because its nonempty path contains a potentially faulty root. For B=2 the reported frontier at n=7,8,9,10 is respectively 21,11,8,6 attempts, with q=5 and r=n−2. The corresponding gate-occurrence counts are 105,55,40,30. The upper sides depend on the separately supplied covering witnesses; the admitted checker shows how those witnesses are validated, but those witness files were not opened or rerun here. [N250A-024] [N250A-027]

The pair-incidence lower argument is elementary. Every point of a (v,b,2)-cover must occur in at least ceil((v−1)/(b−1)) blocks; counting incidences then gives M≥ceil(v ceil((v−1)/(b−1))/b). This supplies the frontier's lower bounds except at (v,b)=(9,4), where it gives only seven. The extra obstruction is worth retaining rather than replacing it by a solver label. Suppose seven four-point blocks covered all pairs of nine points. Every point occurs at least three times, and the 28 incidences force one point x to occur four times and the other eight to occur three times. Each other point has nine companion slots for eight companions, so it has exactly one repeated companion. [N250A-024]

Among the four x-blocks, four of the other points occur twice and four once. A twice-occurring point uses its entire repetition allowance on x and lies in exactly one non-x block. Represent each such point by the pair of x-blocks containing it. The four pairs are distinct edges of a four-vertex graph: duplicate edges would make two such points meet twice. Four distinct edges have a disjoint pair, because a pairwise-intersecting edge family has at most three edges, either a star or a triangle. The corresponding two points must meet in a non-x block. No third twice-occurring point can fill that block, since its pair of x-blocks meets one of their disjoint pairs and would repeat a companion. No once-occurring point can fill it either: its one x-block likewise repeats a companion. The two required remaining places cannot be filled. This contradiction excludes seven, and the source's eight-block witness supplies the upper side. The general incidence reduction remains an ordinary proof; only the small four-edge fact is separately reported as a finite kernel check. [N250A-024] [N250A-027]

The full-action covering review preserves two distinctions that these numbers could conceal. Its opacity condition applies only on failed prefixes still compatible with the fixed bad world; it need not identify observations after success or on unreachable histories. The defective-start bridge equates achievement with an intervention only when the target initially fails; an initially correct target needs zero attempts. The accepted v2 review reports that this bridge corrected an objective-correspondence gap and that a malformed opacity-deletion test was replaced by a well-typed loss-of-information mutation. A failure at syntax or binder inference is not thereby credited as testing the intended premise. The current source statements and explicit mutation drivers preserve those distinctions without a fresh compiler run. [N250A-005] [N250A-006] [N250A-008] [N250A-009]

The finite semantic controls also distinguish an almost-sure cap from an expectation. Uniformly permuting the four minimum paths gives mean first success 5/2 in every fixed one-fault world, while the almost-sure cap remains four and the probability of failing by three is 1/4. A reliable failed-root identity permits a two-attempt strategy on the same four roots: after failure, avoid the disclosed root. This changes the observation contract. The reviewer's controls additionally use complete prior commands and replies, fresh nonordinal history-dependent nonces and one fixed repair body, so their adaptive examples do not depend on identifying arbitrary nonce policies with ordinal renamings. All reported counts remain bounded corroboration; the fixed-world probability quantifier and general cap retain the independent proofs above. [N250A-005] [N250A-007] [N250A-010]

#### Temporal interlocks need all of their independent duties

The negative controls use four roots, fault budget B=1, faulty root0, and path/revocation thresholds q=r=3. They prepare a command on roots0,1,2, then request a transition, acknowledge at1,2,3 and complete it. The source retains the same target bytes/version/recipient but changes its control epoch and permission. Removing only durable epoch revocation admits the old command even while commitment, requester, local authorization and cancellation checks remain. The correct gate blocks it; applying the unguarded landing operation nevertheless damages the state. Thus the landing state transformer must not be mistaken for proof that its transition is enabled. [T07F029]

A second mutation retains only command commitment and target fields. After later descriptors are delivered, the unchanged payload still passes that target-only check while the original authorization envelope fails. This mutation drops more than epoch equality: retaining a correct revoked-epoch guard would block the permission-only example. Target identity is not current permission. A third mutation deletes the cancellation tombstone while retaining commitment, authorization, requester and epoch checks. An actual B+1 cancellation certificate, here acknowledgments from one faulty and one honest selected root, closes the command; removing its tombstone admits a landing afterward. Exactly B acknowledgments, all potentially faulty, do not close it, and the full correct gate can still land it. Late preparation of that same command cannot reopen a retained tombstone. [T07F029]

Two further controls isolate physical mediation and command identity. The already charged faulty root0 can bypass honest vetoes if unmediated damage is admitted; this does not introduce an extra uncharged adversary. An approved command and a substituted command with different table bytes are not interchangeable: the original lands, the substitution is rejected, and physically applying the substituted bytes damages the state. Source75 deliberately asks `by decide` to prove that the too-small cancellation state cannot land; source143 similarly asks it to prove the substituted landing is undamaged. Both requests contradict the explicit positive controls in source29. Their role is expected **negative** fixtures, not additional positive theorems. No compiler failure is newly reported here. Their testing role must remain available wherever the corresponding validation contract is retained. [T07F029] [T07F075] [T07F143]

The multi-epoch fixture advances twice, with source target version equal to epoch and table alternating by epoch parity. Root1 receives epoch2 directly while root2 first receives epoch1. Repeated delivery of stale epoch1 cannot rewind root1; after root2 receives epoch2, both have epoch2 while root3 can still have epoch0. Preparation on0,1,2 and a legal epoch2 landing restore the current target. The trace is built from actual request, acknowledgment, completion, delivery, preparation and landing transitions; its reachability is not merely a desired final valuation. Commands from epochs0 and1 remain blocked in that restored reachable state. This is a concrete two-transition control, not an unrestricted dynamic correctness proof generated by the fixture. [T07F189]

The dynamic-model argument also names the physical conditions under which its count can be used. Its contract is q+r>n+B with q,r≤n−B; hence n≥3B+1, with q=r=2B+1 at equality. A cancellation receipt threshold c must satisfy B+1≤c≤q−B. At the minimum, opaque sequential failure has exact worst-case binomial(3B+1,B) attempts **after stable descriptor delivery**, under the stated trial contract. This is a conditional bounded-port model result. [T750-C721]

Its faults are charged over their lifetime union, including common writers and selector/control ports; rotating a bounded instantaneous fault set does not preserve that budget. Progress additionally requires quiescence, complete live mediation, exact payload binding and an actual reservation or coupling of external authorization. An immediate external revocation cannot be bridged just by an internally current certificate or an earlier observation. The source's counterexamples remove these duties one at a time. Their force is to specify what a faithful implementation must establish, not to claim a generic distributed impossibility or a deployment certificate. [T750-C721]

[T750-C721]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c33e271b68f0ab941bab29cf8ca679ea53d1d26c108071e2d7a313ae222022ab/MODEL_AND_PROOFS.md


<a id="final189-b16-charged-batch-persistence"></a>

The direct charged-interlock development separates its local positive mechanisms from the ordinary counting argument. Honest-overlap counting gives a good root shared by repair and revocation when q+r>n+b; a selected cancellation set with more than b acknowledgers similarly supplies a good veto on that same path. Local binding gives only a locally authorized command until a genuine stale-revocation witness and the independently warranted reservation institution yield current authorization. The finite three-state batch then proves a different positive fact: a safe trial preserves safety, repaired is absorbing under every later trial, and any finite batch containing a success ends repaired when started safe. No recognition of which trial succeeded is needed for this idempotent persistence. The source's untested-candidate lemma is an abstract finite counting fact; the explicit low-overlap adversary and binomial enumeration remain in the ordinary proof rather than being newly kernel-proved by this file. [F189B-874](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/edfd448348d352d6e31a16c776216632bcf344643382661aaf01b65402984195/DynamicInterlock.lean)

#### Executable evidence interfaces are not replaced by prose

The criterion-installation replay program reads the pinned source bytes and12-field CSV fixtures. Its decoder binds actor/destination, target identity, source bytes, permission epoch, rule/version, operation, grant and time; fields distinguish normalized-LF from exact criteria and install from replacement operations. Its output records whether application occurred, resulting exactness/rule version, preservation of draft/source/unrelated state, rule-history length and acceptance of source, source-plus-LF and a wrong-byte variant. Wrong row length raises an error. The source uses permissive numeral conversion/array access conventions, so this program alone is not a proof of a hardened arbitrary-input parser. It replays an installation operation, not a permission to mutate a repository or an equivalence proof for every fixture source. [T07F071]

The artifact writer exercises a different composed scenario: install a criterion, certify a policy transition, deliver it, receive a repair actor and issue the repair. It exports before/installed/repaired JSON with source target/content/roots, destination, standard, draft revision/history, rule version/history and unrelated state, plus preserved-source and repaired-draft binaries. Its local prediction and certificate use explicit default values when optional results are absent. Therefore an output filename or available fallback is not itself evidence that installation, certification or repair succeeded; the actual values and transition outcomes must be checked. If an active reproducibility consumer still requires either IO implementation, its role must be retained or equivalently migrated. If the programs serve only historical reproduction and their exact bodies are recoverable in the approved archive, this prose does not impose an additional active-file requirement. Scientific incorporation alone does not determine that consumer disposition. [T07F116] [T07F071]


### 7.22 A positive-probability opposite-tail failure

The literal runtime comparison supplies a sharper separation than a single unlucky input tape. In its Boolean fixture, the objective has parity success exactly when the action coordinate is eventually permanently equal to the model θ. A history decoder obtained from the source policy with computed tolerance is literally the retained controller policy; its measurability follows from its countable domain. Under the fixture kernel for either θ, that same decoder wins almost surely for every initial state-action pair. These claims keep the given old-configuration winning and tolerance certificates; they are not a theorem about arbitrary decoders. [R250-X154]

An eventual opposite-action tail cannot satisfy the true model's objective: eventual action θ and eventual action ¬θ would have a common late index, contradicting Boolean inequality. More consequentially, let Q be a rational comparison kernel with **strictly positive every row entry**, and suppose Q at true model θ agrees with the fixture kernel at model ¬θ on every state-action pair whose action is ¬θ. Q may differ before that tail. Under Q, the same computed decoder has a strictly positive probability of failure. [R250-X154]

The argument starts from almost-sure eventual opposite action under the fixture's opposite model. It selects a positive-probability recurrent support U within those good pairs, then a finite tail index N with a positive-probability complete event that remains in U thereafter. Row equality on U and strict positivity of the comparison transitions transfer positive mass for this **event**, not merely for a distinguished infinite path, to Q. Every path in the transferred tail event eventually takes action ¬θ, so monotonicity of probability gives a positive failure event under the true model. Agreement on recurrent rows is used with finite-prefix positivity, not silently strengthened to agreement everywhere; the decoder is unchanged across laws. This is a conditional counterexample mechanism and does not infer a numerical lower probability bound absent one in the hypotheses. [R250-X154]

The separate SelectorNumeralReadback file only requests printing `(literalConfig false).selectors` and `(literalConfig true).selectors`, under the labels SELECTORS_FALSE and SELECTORS_TRUE. It supplies no captured numeral output or new execution of the literal counterexample. Its inspection interface is preserved without crediting an unobserved run. [R250-X188]

[R250-X154]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2fd8b8bed21278e6b3f005325f4980b44619d7f2074b800e6c7300fe65b68f74/OppositeTailTransfer.lean
[R250-X188]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/37d53080341b25b5f98dff79325cc21e5e0649dab055fd1012780e557ed601b4/SelectorNumeralReadback.lean

### 7.23 Finite world bounds, exact selector records and bound certificates

The fixed-family search result in §7.21 has a probabilistic extension that preserves the order of its quantifiers. Let W be a finite family of problem instances and let one probability law on complete random tapes be used independently of which instance is chosen. If each fixed instance succeeds almost surely, the intersection of their finitely many conull success sets is conull and contains a tape on which all succeed. Thus a deterministic lower bound that every tape violates on some member of W also bounds a per-instance almost-sure randomized cap. This does not give an adversary access to the realized tape. If failure events cover the tape space, the finite union bound yields one **fixed** instance whose failure has outer measure at least 1/|W|, with nonempty W; ordinary failure probability is obtained when those events are measurable. Arbitrary-event outer measure is not silently described as an independently proved measurability result. [R500-317](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/54ef55ed2558f042c7abe3d577d728ade06f323eb4f9ea3434465f1c58d431ef/RandomizedFinite.lean)

The covering-source statement map uses this finite-family argument with maximal bad-label worlds and transports a violating label set to one compatible actual-root map and fault set. The map and faults are chosen outside the almost-everywhere quantifier. Its covering optimum retains q≤m and k≤m−q for attainment, B,c≥1 for the root-world correspondence, a fixed prepared family and opaque full failure observations. Target achievement needs a defective initial target coordinate: an initially correct coordinate already satisfies the target with zero attempts. A symbolic truthful effect receipt does not prove that a physical implementation emits truthful receipts. The source's complete observation formulation includes full commands and histories; the smaller path-only adapter is not its sole premise. [R500-359](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5f27e799d13f0c30ff04445813062135111648742c44f08fff1d75ed67a39a81/THEOREM_MAP.md) [R500-305](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/506e4a8b8a049f8ad294395c3fd47bfb4005c3369f3fd2bb1f4314c80806452d/CoveringPortfolio.lean) [R500-376](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/61d7a12bde7d60e783598d2833a2225b4f25ad69ca0b90fb97a1dd031517cd45/TargetSearch.lean)

The smaller Boolean-label kernel proves the complement/portfolio equivalence directly, bounds union cardinality by the sum of block sizes and derives the singleton-cover incidence lower bound. Its finite four-vertex edge enumeration supplies the stated disjoint-edge obstruction. The separate target module exposes the covering-number and portfolio-size declarations through checks; it is not another proof or an observed compiler execution. [R500-291](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4eeac9fa4b3d3cc66b9a43bcbb30284ee50e70c67dfc110169d05639224a1049/CoveringCore.lean) [R500-445](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7748198d3466c435d79442ea70ab2e213b7a74363111c257c8a57574e6fa11c7/TargetCovering.lean)

The root-image proofs support exactly this interface. One class A of c labels has one actual root; the other labels have singleton roots, yielding m−c+1 actual roots. B faulty actual roots taint at most B+c−1 labels, and every maximal taint set is realized by a suitable class and B actual faulty roots. Hence fixed-family availability is equivalent to avoiding every maximal taint set under the stated nonsaturation conditions. Root-name transport is bijective on **actual images**, not necessarily on an ambient type of unused names; the Boolean/Nat and representative-index encodings preserve those actual images and budgets. For a nonempty path intersection, the minimum shared-root count is the natural-number expression |P∩R|−c+1. The disjoint-path and B=0 cases need their separate forced-bridge condition: every c-class bridges the paths exactly when m<c+min(|P|,|R|). None of these cardinality facts provides a live authorization or service schedule. [R500-252](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4656044198075f7a55933dbcc08a7b55e58e5b469a57f02748e3c6fb4ddd1182/Availability.lean) [R500-353](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5e459fff98878c78f50f4c0314f777f138815f5d575646af1348e246f3bf7fdf/RootImage.lean) [R500-361](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5f76ef32a3635ad7dce7e711e9e3b2d74d2f731db320af6e5aaecd21654889ab/Correspondence.lean) [R500-290](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4eb87e8ea6edcfcdab9b1de4e09ed4dd1f14503d62f0939b76e122731a723e7c/IndependentChecks.lean) [R500-469](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7d249b5ccf13bdefe4a3b06fd6cad95a3514b3f19a3e333755409d933b5f087e/ImageMinima.lean)

#### Exact cells determine a bounded record, not every raw execution

The selector normal-form account in [Physical realisation, §2.5](physical-realisation-and-continuation.md#25-certified-representation-changes-do-not-repair-a-mismatched-decoder) includes two different semantic boundaries. In the earlier permissive fixture, a full-support retained cycle is fallback-independent, but an off-path singleton-support/opposite-candidate cell can admit more than one qualifying retained target. That target specification alone therefore need not determine one selector record. The later sparse-menu fixture removes that ambiguity by giving each singleton its single good pair, including off-path candidates. It checks all four Boolean support cases and makes a literal certificate equivalent to equality of its orientation with the retained initial candidate. A two-case disjunction proves that one literal record is certified; it does not evaluate the opaque classical choice to name that record. [R500-354](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5e7146fe77b2e68c2f879e442f0e61116d5ae0c21537eb1ec4d3f5fc9f02bf05/LiteralSelectorObstruction.lean) [R500-459](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7b6463aef59aebd51c26e5f81734217de144bc3a80c3d1f257824dc0efdb96c6/LiteralSelectorFamily.lean)

The exact sparse literals have cycle numerals 24332 or 44812, target numeral 428783445879334172098560 and stage numeral 64080. Their table classification preserves raw cell numerals, including the distinction between absent target 0 and present empty target 1. Moduli 2^16,2^80,2^16 remove only unused high digits. Every certified record has one bounded normal form; distinct unbounded encodings can remain certified. For supplied certified data, cycle bit 12 recovers the orientation. A malformed support code 4 reads a discarded bit, so equal legitimate cells do not imply equality on every natural-number argument. These are the exact representation claims already used in §2.5, now tied to the finite classification source rather than promoted to an arbitrary-environment extraction theorem. [R500-275](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4b9e5ff926ea23b1c715d4f1340ac4c2b26ee537945c0dbf568cba9efdffacc0/SelectorTableNormalForm.lean)

The literal old-program/new-decoder counterexample retains the executed and interpreted configurations as separate arguments. Its exact-statement review identifies the mixed claim, proves the failure event measurable under the fair-Cantor input law and retains the matching old/old positive control. In its fixture a gap 1/3 gives computed tolerance 1/6. The matched computed/computed control in the counterpart source remains positive. Normalization or equality of an eventual action set cannot supply equality of decoded finite histories or the actual output law. Historical resource-limited probes are not retroactively credited as observed rejections. [R500-324](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/559a1c37b6db9899fc1bdb46e5b7d2136fc9ddb56004df3616e668398da7d1b0/ExactRuntimeCounterexample.lean) [R500-407](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6a838d5188fd4441ebb71f4452865b7d0f8a21bc5f09e53eef19f90fd620660e/LiteralEndpointReview.lean) [R500-453](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/792a683d9997b7d573110afae9be66b00362213a2a2c527b330f7e79288a25bd/ExactStatementReview.lean)

#### A certificate composition preserves its submitted children and declaration

The certificate-body merge and parent-link operations concern finite submitted evidence, not a new search for a winning body. At each support key, merge unions the submitted state and pair sets and left-biases the literal obligations at equal state/candidate keys. Thus it retains chosen submitted witnesses, not an unchanged whole node. Two bodies accepted for the identical structured input yield an accepted merged body; successful queries from each accepted input are preserved. The selected witnesses need not be commutative. Linking a new parent requires its support to be absent and its actual child/path obligations to be valid against the existing body; the checked API returns only when these premises are checked. A valid merge is not an arbitrary union of conflicting evidence, and a parent cannot be admitted merely because its conclusion is desired. Source path controls retain start, endpoint and singleton/length conditions; changing a literal path can invalidate the supplied witness. [R500-475](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ef0cb1db2fffa67642c361520560fffc53cc0d8b39530bec92f56070a999c0e/CertificateComposition.lean) [R500-348](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5c663b6dc75b23c6937570766a1913b5c1d40b563fc63928e5239048cb9ec8e6/CompositionControls.lean) [R500-444](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/76e3fa078a75460c6a347dcae9646c9c96cbc32a48cd55bcfbc6ce52ad99b849/PathLengthMutationControl.lean)

The raw body checker and the declaration-bound checker are also different. Altering the interpretation's authority can leave raw mathematical body acceptance unchanged while making the old bound packet fail; rebinding produces a new syntactically matching packet. That operation does not authenticate the external declaration or establish its normative authority. Audit-source inventories inspect the intended declaration/dependency boundary, including definitions, opaque values and redirected implementations where specified, but their presence supplies no newly observed axiom/dependency audit. [R500-470](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7d936210bd47f72130de3b1caf24deb797d522b3dc55f74c140a876f5b2228c4/BindingControls.lean) [R500-328](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/572a8c8aab47e5d0407f3b3134fac6291ca3fffe8be6a67770693123474003a3/PathDependencies.lean) [R500-343](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5b6019d2b8bf5089a93931246de0b77836e3e4a52441eef28de1329df546f640/ReviewerFullDependencies.lean) [R500-448](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/77ca711bbc0287368381fbc845df4652b35af3cc6d18521e962e9edd34b51648/ReviewerPathReadback.lean)

Finally, the generated co-Büchi controller's positive exponential-moment range in §7.19 is an actual-law theorem for that fixed construction: actual model in initial support, a winning-region start, positive tolerance and strict row separation. It transports the complete action law, including the first action, and accompanies the real-valued bad-count bound by almost-sure finiteness. It is not a cost bound for every private-seed policy or general parity, and not a physical-clock estimate. Its exact-source endpoint is [R500-458](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7b639a064e5d523827750a8a9e8527b4f172b45523ca2d32e565a10ba3348318/ActualExponentialMoments.lean). The separate expression-stack correspondence scope [R500-489](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/81d31db2010d1e16f0f0f95fc8eefa264d7fd69dbf439908a61a27de43015339/P1_SCOPE.md) retains only finite well-formed decoded expressions, exact built-in natural integers, input-dependent resource bounds and the stated source-shaped stack/meter semantics. Parser, statement evaluator, CPython primitive correctness and host allocation/time failure remain outside that proof; the ideal existence of adequate bounds is not a cheap or host-safe budget estimator.

#### Submitted evidence and the accepted certificate language

The composition controls validate a submitted body **before** canonicalizing it: otherwise normalization can delete a malformed duplicate and make an invalid input appear valid. They require complete child coverage, reject an invalid unrelated node, retain each obligation's original connected component, and bind the input revision so that a structurally valid stale envelope is still rejected. The structural controls also check all nodes and obligations, exact support keys, child identities and ordering. Freshly rechecked extra grants or a changed declared source can pass the structural checker while `sameInput` becomes false; input equality is a separate contract. [T750-C686] [T750-C702]

`IndexedCoverageControls` admits complete two-position evidence but rejects omission, duplicates, skipped/out-of-range positions, extra entries and reversal. Perfect indexing does not make a false local refutation sound. This strict indexed syntax should not be imported into the different mask certificate interface, which permits redundant/reordered rows with complete semantic coverage. The accepted language is part of each theorem. [T750-C693]

Two source variants illustrate the distinction between semantic correctness and representation policy. `PathLengthMutant` leaves local edges and endpoint reconstruction but literally replaces the final length-bound conjunct by `True`; it supplies no path-size bound, despite its inherited comments. `RepresentationControls` records that Lean's checker accepts a bounded nonsimple stored path rejected by Python's `valid_route`, and admits redundant fixed repetitions within its n+2 bound; its negative trace can repeat empty sets. These are exact syntax differences, not a newly found failure of the semantic theorem. The single-state fixtures separately fix even/odd priority, empty and one-step paths, a singleton body and tags invalid/empty/positive/negative as 0/1/2/3. Fixture data and deliberately weakened variants are not additional general theorems or fresh test results. [T750-C742] [T750-C744] [T750-C749]

[T750-C686]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/b90f0bdfb1ac808add221823f315d5ed141ef0ce8ae737a0bc05663693fda03c/ReviewerCompositionControls.lean
[T750-C693]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/bda4ff0bd21d51d1b44e1394c7a310c38e2c8be4e1d5999c0bc948313592fa7c/IndexedCoverageControls.lean
[T750-C702]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/be7154c4dad2daa1dc2ab93b88788358adc0d2c9dd6dab949dec1a8300f534ba/CertificateControls.lean
[T750-C742]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c9c64640c7210adee2c9345d48ee225b41957350ebfcde6414886e874450b0da/PathLengthMutant.lean
[T750-C744]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ca56c7b81b8730cb0a602fea3d63ebd80e114b29b60b7f5a95fcf546f26c8cdf/RepresentationControls.lean
[T750-C749]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cbfde605e09d1c7eb86c7f54c5a388b48653b15b087d9a8844fae58186a74129/SmallFixtures.lean


<a id="final189-b05-shape-and-evidence-contract"></a>

The direct finite-input definition adds an operationally significant validation order. It first checks positive q,n,k and literal lengths q·n·k·n for rows, q·n·k for priorities, and q,n,k for the coding lists. A failed shape gate returns false before enumerating the claimed finite carriers or performing row arithmetic. Sparse-menu validation rejects repeated support/state keys, repeated support or action members, and out-of-range entries; absent menu records mean the empty menu. Exact sameInput compares every structured field, including interpretation strings, rather than only the induced probabilities. The language supplies data and validation, not a solver or a winning-policy witness. [F189B-828](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e05d663571ba1cdf8e2ad04f19442721d4f03ee5bca46c0ad185e5d2c2f0e0c6/CertificateData.lean)

The certificate grammar gives each used component state exactly one link record, containing paths to and from a chosen root; the no-duplicates condition applies to the records' state keys. It checks full candidate-row closure and requires each numerically matching rival to attain an even minimum on the component. Node obligations have exactly the state×candidate keys, with no duplicates; every nonempty proper live-support update must reference a submitted child containing the successor. Layout checks the submitted supports, not an enumeration of all unlisted supports, while body validation checks every submitted node before query lookup. These are positive finite certificate interfaces under their precise syntax. The positive-input-binding mutant drops sameInput only on the positive branch: its changed input still accepts the body, contradicting its retained false assertion. That demonstrates the necessity of the omitted binding check for the submitted-record contract, not unsoundness of the structural theorem. No test has been rerun here. [F189B-842](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e41f1506d7b17c76bdc11929d6f31c73512549f55c7281f9ea85d37f597b372a/CertificateSyntax.lean) [F189B-870](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ed99c3cbd5253c1fa6412801136653d1b94675c23afb003f80c02187cb5d5b5c/MutationPositiveDropsInput.lean)

#### The earlier existence interface and its exact execution evidence

The independent existence-calculus review confirms the inherited positive endpoint used in §7.15: for a valid fixed finite rational input and query, **there exists an accepted finite body if and only if a common lawful almost-sure parity policy exists**. It is not the claim that every submitted body passes on a winning query. Its arbitrary measurable-seed premise also yields a finite body, while the submitted syntax's finite size does not establish autonomous finite-state policy sufficiency. The cited Bernoulli control uses good priority 2 and bad priority 1 under minimum-even parity; changing good priority to 0 would change that particular co-Büchi comparison. These are properties of the earlier existence interface, not limits withdrawing the later signed service or direct controller. [N250C-127] [N250C-132]

The same review fixes two operational qualifications beyond the structural argument. A polynomial verification-cost argument charges explicit materialized input and AST bit length, including rational numerators/denominators; it promises neither polynomial certificate size nor a verified bit-cost counter. And independence from the synthesizer holds at the finite typed-data interface. It does not authorize executing arbitrary Lean or Python from an untrusted producer. A trusted constructor/decoder enforcing finite indices and syntax remains necessary; the scientific replay runner is not a wire-format parser or upload service. [N250C-127] [N250C-128]

The historical full portable execution was of v2, while v4 retains identical scientific/control sources. The v3→v4 diff changes a result-metadata literal to distinguish **no added invocation heartbeat override** from two preserved inherited source settings of 800000 in FiniteChainTrajectory and GeneratedParitySuccess. It changes no command, order, control or resource budget. The review qualifies that exact bridge; it does not claim a fresh full execution of the different wrapper bytes. All eight new modules use defaults. The author's portable runner rebuilds its 87-module inherited closure and eight new production modules, while the independent runner can instead qualify 95 existing production source/object bindings and explicitly record reuse. [N250C-129] [N250C-130] [N250C-131] [N250C-133]

Both runners refuse optimized Python and distinguish the intended concrete mutation rejection from an unrelated error. The independent five mutations remove all-receipt closure, rival parity, full numerical row matching, used-menu licensing or exact state/candidate keys. Their control logic tests changed executable predicates rather than reasserting the original soundness theorem. The acceptance reports successful checks at its historical boundary; this incorporation only reads that code and report. Official external objects remain trusted, C generation is not linked standalone execution, and none of these results authenticates the declared worldly model, grant authority or occurrence. [N250C-127] [N250C-130] [N250C-131]

## 8. What final judgments identify about evidence use

The previous sections ask what information a strategy or coordination mechanism needs. The converse question is different: what does a successful collective answer reveal about how the answer was produced? A group can produce informative, accurate answers without the available observations identifying each member's causal contribution. The following construction proves this limitation while preserving both a real two-input mechanism and a real one-input alternative. [11][r11]

### 8.1 Two mechanisms with the same complete answer law

Fix a stimulus $`x\in\mathbb R`$, a variance $`v>0`$, a variance ratio $`k>1`$ and an announcer $`a\in\{B,W\}`$ with output-noise variance $`r_a\ge0`$. On each trial let Z<sub>B</sub>,Z<sub>W</sub>,Z<sub>A</sub> be independent standard normal variables, with fresh independent triples across trials. Define the two private observations

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
| Single-input mechanism *L* | $`T_L=X_B+\sqrt{r_a}\,Z_A`$ | $`Y_L=\mathbf1\{T_L>0\}`$ |
| Two-input mechanism *P* | $`T_P=\alpha X_B+\beta X_W+\sqrt{r_a}\,Z_A`$ | $`Y_P=\mathbf1\{T_P>0\}`$ |

The hypothetical unaided threshold readouts of *X*<sub>*B*</sub> and *X*<sub>*W*</sub> have maximum response-curve slopes $`1/\sqrt{2\pi v}`$ and $`1/\sqrt{2\pi kv}`$. These are model quantities, not an assertion that participants formed or reported private decisions, or that human capacities remain stable across experimental conditions.

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

**Proof.** The single-input score has the stated normal mean and variance. The two-input score has mean $`(\alpha+\beta)x=x`$ and variance $`(\alpha^2+k\beta^2)v+r_a=v+r_a`$. Normality follows from linear combination of independent normal variables. The threshold probabilities therefore agree. Conditional on a fixed schedule $`D=((x_t,a_t))_{t=1}^n`$, fresh noises make both answer laws the identical product of Bernoulli laws with parameters $`\Phi(x_t/\sqrt{v+r_{a_t}})`$. Integrating against the same joint law of *D* proves the final claim. ∎

Thus both mechanisms have the same psychometric curve, the same maximum slope $`1/\sqrt{2\pi(v+r_a)}`$, and, for nonzero stimulus with correct answer determined by its sign, the same accuracy $`\Phi(|x|/\sqrt{v+r_a})`$. Announcer-specific output noise may change these values while preserving the equivalence.

This is not an algebraic disguise of the same causal rule. In *P* both coefficients are strictly positive; changing either input while holding the other fixed changes its score. When $`k=3`$, the two-input mechanism is the ordinary mean of the two observations. The restriction $`k>1`$ matters: at $`k=1`$, $`\alpha=0`$, so the purported two-input mechanism ceases to use both inputs. Zero output noise is permitted and does not break Theorem 15.

The schedule's **joint** law also matters. Equality of individual stimulus marginals does not suffice. Take a fixed announcer, a positive *c* and let $`p=\Phi(c/\sqrt{v+r_a})>1/2`$. A schedule that repeats a common random sign, (c,c) or $`(-c,-c)`$ with equal probabilities, has the same marginal stimulus distribution at each time as a schedule that reverses that sign, $`(c,-c)`$ or $`(-c,c)`$. Yet the first produces answer agreement with probability $`p^2+(1-p)^2`$ and the second with probability $`2p(1-p)`$. The theorem compares complete specified designs, not isolated marginals.

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

The first is constant in *w* and the second is strictly increasing. Likewise,

```math
\Pr_P(Y=1\mid\mathrm{do}(X_B=b))
=\Phi\!\left(
\frac{\alpha b+\beta x}{\sqrt{\beta^2kv+r_a}}
\right)
```

is strictly increasing in *b*. Under *L*, replacing *X*<sub>*B*</sub> changes the answer directly; if $`r_a=0`$ it becomes the deterministic threshold $`\mathbf1\{b>0\}`$. Hence the models differ about genuine causal use even when the entire answer-only record has the same distribution.

A passive record of (X<sub>B</sub>,X<sub>W</sub>,Y) also separates them. With positive output noise, the conditional response under *L* depends only on *X*<sub>*B*</sub>, whereas under *P* it depends strictly on both inputs. With zero output noise, the separating lines $`X_B=0`$ and $`\alpha X_B+\beta X_W=0`$ still differ on sets with positive Gaussian probability. Enlarging the observable record changes the identification problem; it does not contradict the answer-only theorem.

### 8.3 Adaptation cannot manufacture a missing channel

The fixed-design result does not, by itself, assert equality for every adaptive experiment. A later extension supplies explicit conditions under which that equality does persist. [12, §§1–2][r12]

**Theorem 16 (adaptive answer-only equivalence).** At each stage let a common nonanticipating policy choose the next stimulus, announcer or stopping decision from the past recorded designs and answers and a common independent random seed. Keep the model parameters fixed. Conditional on that history and the chosen next design, draw a fresh independent normal noise triple with the law specified above. The policy has no access to hidden observations, model-specific refusal channels or interventions on the input mechanisms. Then the two models give the same law to the entire adaptive recorded experiment, including eventual stopping and the reported result.

**Proof.** Include the common policy randomization in the history. At the initial stage its distribution is the same under both models. Whenever the recorded histories agree in distribution, applying the same policy kernel gives the same distribution for the next design or stop. On continuing, Theorem 15 applied conditionally to the chosen design gives the same next-answer law, because the fresh noise triple is independent of the history. Induction therefore gives equality of every finite transcript. Pad a stopped transcript by an absorbing stop symbol. Equality on all finite cylinder events determines the same probability law on the countable sequence space, so every measurable stopping event and reported-result event has the same probability. ∎

This result allows genuine new answer trials: their conditional likelihood ratios are still one. It is not restricted to reusing the same answer record. But endogenous human designs, interventions, hidden-variable access, model-dependent missingness and retained internal records require a new argument; the conditional-freshness and common-policy assumptions cannot be inferred from the word “adaptive.”

The same reasoning has a simpler static form. If the answer record has common law μ and an analysis or audit uses a common kernel *K*, its output law is

```math
\Pr(\text{analysis output}\in A)=\int K(d,A)\,\mu(dd)
```

under both models. Randomized reanalysis, a summary statistic or an answer-only adjudication cannot distinguish them. An audit that actually receives an additional informative record changes the premise.

For two fully specified candidate models with positive prior probabilities, identical answer likelihoods leave their posterior odds equal to their prior odds. They do not make unequal priors equal. Nor do they make these two models equally warranted in every other respect, prevent evidence from favoring both over a third model, or prove that causal explanation is impossible. For composite models, the same conclusion requires equality of their induced observable laws after integrating their parameter priors; a convenient pairing of parameters is insufficient. The limitation is a precisely identified observational one.

## 9. Linked evidence and the limits of statistical discrimination

The following positive and negative results use the same received collective-evidence construction, including its later finite and sequential arguments. [11][r11]

### 9.1 One additional linked observation can be informative

The observational equivalence can be broken by retaining a within-trial link between an input and the final answer.

The readout is passive: recording *X*<sub>*W*</sub> or its binary threshold is assumed not to change the structural equations. All covariance comparisons below condition on the declared stimulus *x* and announcer *a*. Pooling trials with varying stimuli can create summary–answer or linked-bit–answer association even in *L*: although conditional covariance vanishes there, both conditional means can vary with the common stimulus. Such pooled association alone therefore cannot identify a member's causal contribution. The construction does not establish feasible passive access to an actual person's private state. [11, linked-record analysis][r11] [12, §3.1][r12]

Set $`\sigma^2=v+r_a`$ and let ϕ be the standard normal density.

**Proposition 17 (a linked real-valued record).**

```math
\mathrm{Cov}_L(X_W,Y)=0,\qquad
\mathrm{Cov}_P(X_W,Y)
=\frac{\beta kv}{\sigma}\,
\phi\!\left(\frac{x}{\sigma}\right)>0.
```

**Proof.** In *L*, *X*<sub>*W*</sub> is independent of *T*<sub>*L*</sub> and hence of its threshold. In *P* the pair (X<sub>W</sub>,T<sub>P</sub>) is jointly normal, with covariance $`\beta kv`$. Its conditional mean is

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

Under *L*, *Q* and *Y* are independent. Under *P*,

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

Now let a recording error independently flip *Q* with probability ε. With an independent Bernoulli error *E*,

```math
Q'=Q+E-2QE,\qquad
\mathrm{Cov}(Q',Y)=(1-2\varepsilon)\mathrm{Cov}(Q,Y).
```

For $`0\le\varepsilon<1/2`$ the separation remains positive. At $`\varepsilon=1/2`$, Q′ is a fair bit independent of every pre-error variable; with fresh independent recording errors across trials the entire paired record again has the same law under both models. For $`\varepsilon>1/2`$, reversing the recorded bit restores a positive separation if the error regime is known. Dependent, adversarial or unmodelled errors are not covered by this formula.

The link itself is part of the information. At zero stimulus the unary bit marginals are fair in both models. Authentic observations of Q′ and *Y* taken from disjoint independent trials therefore give the same independent pair law under both models. A within-trial link is needed for the covariance witness. This is not a blanket claim that every shuffle of a finite data array destroys all dependence; different observation procedures must be modelled as such.

### 9.2 A finite guarantee requires a declared separation

Fix one design and independent identically distributed paired trials. Let $`p=\mathbb E Q'`$ and $`q=\mathbb E Y`$, which are common to the paired models, and let

```math
\delta=\mathbb E_P[Q'Y]-pq>0.
```

Under *L* the corresponding covariance is zero. Suppose first that the baseline $`pq`$ and a positive lower bound $`\delta_0\le\delta`$ are known. Select *P* when

```math
\frac1n\sum_{t=1}^n Q'_tY_t
\ \ge\ pq+\frac{\delta_0}{2},
```

and otherwise select *L*.

**Proposition 18 (finite separated test).** Each error probability is at most

```math
\exp(-n\delta_0^2/2).
```

Thus $`n\ge2\log(1/\eta)/\delta_0^2`$ suffices for each error to be at most $`\eta\in(0,1)`$.

**Proof.** If *Z* is Bernoulli with mean *m*, put $`\psi(\lambda)=\log\mathbb E e^{\lambda(Z-m)}`$. Then $`\psi(0)=\psi'(0)=0`$ and $`\psi''(\lambda)`$ is the variance of a tilted Bernoulli variable, hence at most 1/4. Integrating twice gives $`\psi(\lambda)\le\lambda^2/8`$ for every real λ. Independence, Markov's inequality and the choice $`\lambda=4t`$ give

```math
\Pr\!\left(\overline Z-m\ge t\right)
\le\exp(-2nt^2).
```

Using $`\lambda=-4t`$ proves the same lower-tail bound. Under *L* the upper-tail distance is $`\delta_0/2`$; under *P* the lower-tail distance to the threshold is at least $`\delta_0/2`$. These give the asserted bounds. Assigning equality to *P* does not invalidate either bound. ∎

The source supplies a concrete exact case. Set $`x=0,v=1,k=3,r_a=0,\varepsilon=0`$. For independent standard normals U,V,

```math
Q=\mathbf1\{V>0\},\qquad
Y_P=\mathbf1\{U+\sqrt3V>0\}.
```

Rotational symmetry makes the angle of (U,V) uniform. The two positive half-planes intersect in a sector of angle $`5\pi/6`$: in polar coordinates the conditions are $`0<\theta<\pi`$ and $`\cos(\theta-\pi/3)>0`$, so their intersection is $`0<\theta<5\pi/6`$. Hence

```math
\Pr_P(Q=1,Y=1)=\frac5{12},\qquad
\Pr_L(Q=1,Y=1)=\frac14,\qquad
\delta=\frac16.
```

With $`n=216`$, choose *P* when the joint-positive count is at least 72. Each error is at most $`e^{-3}<1/20`$. These are parameters and guarantees of an exact illustrative model, not a report of performed trials or a recommendation for a particular empirical study.

There is no comparable uniform finite guarantee over all positive separations. For binary variables with the same unary marginals, a covariance difference δ changes the four cells by $`(+\delta,-\delta,-\delta,+\delta)`$. The one-pair total variation distance is exactly $`2\delta`$. For *n* independent pairs, the product-law telescoping identity and the triangle inequality give total variation at most $`2n\delta`$. For any possibly randomized test, the sum of its two errors is therefore at least

```math
1-2n\delta.
```

Indeed, writing the probability of selecting *P* as a test function $`f\in[0,1]`$, the sum is $`1-(\mathbb E_Pf-\mathbb E_Lf)`$, and that expectation difference is at most total variation. In the concrete model above, independent recording error gives $`\delta=(1-2\varepsilon)/6`$, arbitrarily close to zero as $`\varepsilon\uparrow1/2`$. Large stimulus magnitude also shrinks the separation. Strictly positive identifiability alone supplies no uniform finite sample size.

### 9.3 A sequential positive witness without a promised effect size

The known baseline and lower separation bound can be removed if the procedure is allowed to continue indefinitely under the null. Retain fixed-design independent identically distributed paired trials and a strictly positive separation under *P*. Define

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

On stopping, declare a positive contribution witness, namely *P* within this specified pair of models. The procedure never declares *L*.

**Theorem 19 (time-uniform positive detection).** Under *L*, the probability of ever stopping is at most γ. Under every fixed *P* with $`\delta>0`$, $`\tau<\infty`$ almost surely.

**Proof.** Apply the two-sided bound proved above to each of the three Bernoulli means. At each time, each failure probability at tolerance *e*<sub>*n*</sub> is at most $`\gamma/(3n(n+1))`$. A union bound over the three means and all *n*, using $`\sum_{n\ge1}1/(n(n+1))=1`$, gives an event *G* of probability at least $`1-\gamma`$ on which all three mean errors are at most *e*<sub>*n*</sub> at every time. Since all means lie in $`[0,1]`$,

```math
|\widehat p_n\widehat q_n-pq|
\le|\widehat p_n-p|+|\widehat q_n-q|
\le2e_n.
```

Thus $`|\widehat c_n-\delta|\le3e_n`$ throughout *G*. Under the null $`\delta=0`$, the strict stopping inequality cannot occur on *G*, proving the false-positive bound.

Almost-sure detection requires a separate argument: *G* itself has only probability at least $`1-\gamma`$. For every positive rational tolerance, the fixed-tolerance concentration probabilities are summable in *n*. The Borel–Cantelli argument, applied to the three means and countably many such tolerances, shows their almost-sure convergence to p,q,b. Hence $`\widehat c_n\to\delta>0`$ almost surely, while $`e_n\to0`$. Eventually the strict stopping inequality holds. ∎

This is an exact-real mathematical stopping rule. A numerical implementation needs a certified comparison whose approximation error tends to zero: for example, a certified lower bound for $`\widehat c_n`$ and upper bound for $`3e_n`$. An arbitrarily loose conservative threshold can protect the false-positive bound while destroying eventual detection. No finite uniform detection time follows, and failure to stop is not a negative contribution certificate.

### 9.4 Why a uniformly reliable two-answer procedure cannot always stop

The inability to declare the null after a uniformly bounded amount of ambiguous evidence is structural.

**Theorem 20 (null-termination obstruction).** Fix $`x=0,v=1,k=3,r_a=0`$ and allow independent recording errors $`0\le\varepsilon<1/2`$. There is no single nonanticipating sequential procedure whose terminal decision is either *L* or *P*, with common independent auxiliary randomization, satisfying all three conditions:

1. It terminates almost surely under the single-input model.
2. Its probability of declaring *P* under that model is at most γ.
3. Under every two-input model in this family, its probability of declaring *L* is at most ζ, where $`\gamma+\zeta<1`$.

**Proof.** Under the single-input model, each paired observation is uniform on the four cells, independently of ε; call this common null law *L*<sub>0</sub>. The alternative has the same fair marginals and covariance $`\delta=(1-2\varepsilon)/6\downarrow0`$.

Let *A*<sub>*N*</sub> be the event that the procedure declares *L* by time *N*. Null almost-sure termination and condition 2 give $`\Pr_{L_0}(\bigcup_N A_N)\ge1-\gamma`$. Choose $`\eta>0`$ with $`\gamma+\zeta+2\eta<1`$ and then a finite *N* with $`\Pr_{L_0}(A_N)>1-\gamma-\eta`$. Choose an alternative with $`2N\delta<\eta`$. Its first *N* pairs have total variation distance at most $`2N\delta`$ from the null. Appending the common independent seed and applying the common procedure cannot increase that distance. Consequently,

```math
\Pr_P(A_N)>1-\gamma-2\eta>\zeta,
```

contradicting condition 3. ∎

The argument needs neither almost-sure termination under the alternatives nor a finite expected running time. It rules out this uniform combination of guarantees, not every useful sequential method. A lower bound on effect size, a weaker error demand, an additional measurement channel or permission to withhold a negative answer changes the problem.

## 10. Choosing an informative inquiry and revising its calibration

Identifiability asks whether laws differ. An inquiry decision also needs a loss function, a prior and the cost and availability of obtaining the proposed observation. The source's exact linked-bit example permits these ingredients to be calculated transparently. This calculation concerns the specified two-model decision problem, not an empirical valuation of cognition. [12, §3][r12]

### 10.1 The distinguishing information is an interaction

Continue with $`x=0,v=1,k=3,r_a=0`$ and independent bit error $`0\le\varepsilon\le1/2`$. The linked pair (Q′,Y) has fair unary marginals in both models. Write $`\delta=(1-2\varepsilon)/6`$. In the cell order $`(0,0),(0,1),(1,0),(1,1)`$, the laws are

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

Give the two models equal prior probability and evaluate an estimate $`a\in[0,1]`$ of the indicator of model *P* by squared loss $`(a-\mathbf1_P)^2`$. At posterior probability *q* the expected loss is

```math
q(a-1)^2+(1-q)a^2=(a-q)^2+q(1-q).
```

Thus the optimal estimate is the posterior itself, with risk $`q(1-q)`$. Before the query the risk is 1/4.

A concordant pair, $`Q'=Y`$, gives posterior

```math
q_{\mathrm{same}}=\frac{1/4+\delta}{1/2+\delta},
```

and a discordant pair gives

```math
q_{\mathrm{different}}=\frac{1/4-\delta}{1/2-\delta}.
```

The predictive probabilities of these events are respectively $`1/2+\delta`$ and $`1/2-\delta`$. Since the expected posterior is its prior 1/2, the reduction in optimal expected squared loss is the posterior variance:

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

| Independent bit-error probability | δ | Posterior after concordance | Posterior after discordance | Value *V* |
|---:|---:|---:|---:|---:|
| 0 | 1/6 | 5/8 | 1/4 | 1/32 |
| 1/4 | 1/12 | 4/7 | 2/5 | 1/140 |
| 1/2 | 0 | 1/2 | 1/2 | 0 |

At zero recording error the posterior expected risk is 7/32, improving on 1/4 by 1/32. If the query costs $`c=1/64`$ in the same loss units, it is beneficial at zero error and not beneficial at error 1/4. An answer-only query has value zero for discriminating this pair under the common observation contract, even if it is an authentic new trial. It can still be valuable for a different target, such as learning the stimulus.

The calculation assumes that the linked record is available at the stated cost and that the two-model prior and loss are appropriate for the decision. It does not establish either assumption, exclude additional candidate mechanisms, or choose the ethically or epistemically correct loss. Positive value in this model is not a global ranking of research programmes.

### 10.3 Calibration repair replaces the old contribution

Suppose one concordant paired observation was initially evaluated with $`\varepsilon=0`$. Its likelihood ratio for *P* over *L* is

```math
\frac{1/4+1/6}{1/4}=\frac53,
```

which changes prior odds one to posterior probability 5/8. If justified calibration later changes the same recording channel to $`\varepsilon=1/4`$, the correct likelihood ratio for this **same observation** becomes

```math
\frac{1/4+1/12}{1/4}=\frac43,
```

and its corrected posterior is 4/7. Multiplying both ratios would give odds 20/9 and probability 20/29, falsely treating one record under two calibrations as two independent observations.

The product can be appropriate for two genuinely independent records, one from each specified channel. It is inappropriate merely because a different copy, report or analysis presents the original observation. A root-aware record of what was observed must be joined to a scientific model of dependence; identity alone supplies no likelihood factorization.

Uncertain calibration must also remain coupled to the model and record whose likelihood it changes. A Bayesian treatment can integrate a common calibration model with a declared prior. A robust treatment can retain an admissible set of common calibrations. Choosing a convenient endpoint separately for each hypothesis or multiplying an audit result as independent when it depends on the same observation changes the model. If a calibration audit supplies new information, its appropriate contribution is the joint law of the observation and audit, or a justified conditional factorization of that law.

These corrections preserve the earlier statistical limits. An informative linked channel admits a positive contribution witness under its hypotheses. It does not supply an effect-size lower bound, a finite uniform decision time, or certainty that a persistent lack of evidence establishes absence of contribution.

### 10.4 Recorded scores, active majorities and the scope of an empirical reanalysis

The exact-law examples above separate observable accuracy from the mechanism that produced it. A reported reanalysis of an empirical group-judgment study makes the choice of outcome and weighting similarly consequential. Pescetelli, Rutherford, Rahwan and Kao's 2025 article, *Collective incentives improve group accuracy by reducing reliance on shared news sources*, studies 232 participants making forecasts after receiving both a more accurate shared source and a less accurate independent source on every round. Round-level source preference was inferred from agreement between the participant's binary forecast choice and a source's evidence on rounds when the two sources disagreed; it was not a directly observed round-level source-selection response. The publisher's account attributes improved group accuracy to collective incentives and reduced reliance on shared news. Those are the publication's empirical claims, not conclusions established by the mathematical models in this chapter. [Published study][empirical-pescetelli]

The public derived *Sixteenth Report* describes a reanalysis of the author-linked 2019/2020 archive with 232 people and 75 games. Its scope is that archived dataset and its reconstructed variables; it does not establish identity with the exact analysis files or supplementary information used for the 2025 publication. No participant data have been newly analysed for this composition. The following numerical results retain their status as source-reported historical calculations. [Public report, empirical validation][signed-report]

The report distinguishes the roster, recorded forecasts and correctness flags. Every positive recorded group score corresponds to a correct majority among score-supported responses, but 130 negative scores also have such a correct majority. A further 185 scores are missing at roster-count ties. Thus recorded score and correctness of the active, score-supported majority are different outcomes. A reanalysis must define which one it estimates before comparing incentive conditions.

For its rescoring, the report assigns half-credit to a nonempty tie and zero to empty score support. Across 47 multiplayer games, its prespecified equal-size incentive contrast is **+1.62 percentage points**, with a marginal 95% game-bootstrap interval of **−1.66 to 5.00 percentage points**. Equal-size weighting assigns one third of the total weight to only five fifteen-person games. The contrast therefore answers a particular size-balanced question; it is not numerically interchangeable with a participant-weighted, observation-weighted or equally weighted game contrast.

Dependence also changes the apparent precision. The report's paper-like interaction has standard error 0.077 under one calculation and 0.241 when clustering by game is used. A separate post hoc comparison finds a positive seven-person recorded-score advantage in all six matched batches. This sign pattern is a different, selected comparison, not a replacement confidence interval for the prespecified rescored estimand. The report leaves the source-use and error-dependence contrasts uncertain.

The public report also records author and independent complete replays of that reanalysis with hash-verified inputs and pinned dependency versions, producing byte-identical generated reports. It says that reversing the previously approved narrative metadata changes reproduced the retained historical report hashes while leaving all computed statistical fields unchanged. These are reported reproducibility observations about the archived analysis, not fresh executions here, a new experiment under a matching protocol, or human-specialist validation.

These distinctions support concrete limits on interpretation. The reanalysis does not establish causal mediation by source choice, equivalence of individual performance across incentives, behaviour under a new scoring rule, or exact identity with the publication's analysis and supplementary materials. Its uncertainty interval crosses zero for the stated marginal contrast; that does not prove equality, just as the post hoc sign pattern does not establish every proposed mechanism. Connecting an incentive to a source-choice mechanism would require the corresponding intervention, measurement and dependence assumptions, not accuracy differences alone.

The connection with sections 8–10 is therefore about the evidence needed for a claim. Identical final-judgment laws can conceal different evidence-use mechanisms in the mathematical countermodels; distinct empirical outcome definitions and cluster structures can also change what a numerical comparison supports. Neither observation invalidates the original study as a whole, and neither supplies a new empirical validation of the chapter's exact-law theorems. The useful positive result is an explicit separation of outcome, estimand, weighting, dependence and mechanism so that each inference can be assessed on its own evidence.

#### The scoring rule determines which support is being compared

The retained independently authored analysis makes the support distinction in §10.4 executable. For one game-round let n be assigned capacity, m the observed roster, e the number of nonmissing stored correctness flags, and c the number of those flags that are correct. The declared domain has n ≥ m ≥ e and m > 0. Its reconstruction of the recorded score is

```math
R^*=\begin{cases}1,&c>m/2,\\0,&c<m/2,\\\text{missing},&c=m/2.\end{cases}
```

Three comparison scores use different denominators:

```math
A_{E0}=\begin{cases}1,&c>e/2,\\0,&c<e/2,\\1/2,&e>0\text{ and }c=e/2,\\0,&e=0,\end{cases}
\qquad B_{E0}=\mathbf1\{c>m/2\},\qquad Q_{E0}=\mathbf1\{c>n/2\}.
```

Thus active correctness, roster majority and assigned-capacity majority are not synonymous. With stored flags [true, missing] and capacity three, the reconstruction is missing, active correctness is one and both strict-majority scores are zero. With [true, true, false] and capacity seven, active and roster scores are one while the assigned-capacity score is zero. Empty flag support receives active completion score zero, not tie half-credit. These are the exact synthetic cases specified in the retained tests, not newly executed study observations. [Q250B-061] [Q250B-068]

The estimation program joins the flag reconstruction one-to-one to game-round records and refuses continuation unless it agrees with recorded R on every round, including matching missing values. It separately computes active-minus-roster, roster-minus-assigned and final-forecast-minus-flag-support contrasts; its matched active-minus-recorded comparison restricts both terms to the rounds on which R is available. Replacing missing R by one half or by one is an explicitly separate sensitivity outcome. Final forecasts also have their own vote-based active and quorum calculations, which do not silently replace stored correctness flags. A successful reconstruction would identify a relation among archive variables, not prove the participants' decision rule or the meaning of eligibility. Changing a retrospectively computed score is not an intervention on their behaviour. [Q250B-061] [Q250B-063]

The input gate preserves the observations to which those claims refer. It checks two fixed input digests, unique game/player/round/stage keys, three stage records per response key and agreement of duplicated stage fields. It then checks an exact one-to-one join to the author response export on the key and seven named projected fields, including forecast, stored correctness, group score, size, both cue flags and incentive. Game-round truth/cue/score fields and game-level treatment and batch fields must be internally consistent. Event extraction accepts only literal Boolean values for the two relevant fields and never evaluates an unrelated expression in the event dictionary. These checks make an archive-specific comparison possible; they do not establish identity with the later publication's analysis files. [Q250B-067] [Q250B-061]

#### Game uncertainty and paired-batch sensitivity answer different questions

For metric Y, the primary descriptive estimate in the retained program is

```math
\widehat\Delta_Y={1\over3}\sum_{s\in\{3,7,15\}}
\left(\overline Y_{s,\mathrm{collective}}-
      \overline Y_{s,\mathrm{individual}}\right).
```

It first averages available rounds within each game and gives available games equal weight within each size/treatment cell. The bootstrap resamples games independently within these six cells and recomputes the equal-size contrast, using 20,000 replicates and a fixed seed. An empty cell produces an explicit unavailable result. Size-specific intervals and leave-one-game-out ranges retain their own denominators. These uncertainty calculations condition on the realised task items and scoring support; repeated rounds do not become independent experimental units. A fixed seed makes an algorithm reproducible, not its model assumptions true. [Q250B-061] [Q250B-063]

The logistic diagnostic also exposes the dependence adjustment. For design rows x_i, fitted means p_i and outcomes y_i, write

```math
H=\sum_i p_i(1-p_i)x_ix_i^\mathsf T,
\qquad S_g=\sum_{i\in g}x_i(y_i-p_i).
```

Its game-cluster covariance is H⁻¹(Σ_g S_gS_gᵀ)H⁻¹, multiplied for CR1 by G/(G−1) times (N−1)/(N−k), when those factors are defined. It uses t critical values with G−1 degrees of freedom, while also retaining the ordinary inverse-Hessian diagnostic. Half-credit active outcomes are fractional-logit sensitivities, not Bernoulli-outcome likelihood observations. The program checks design rank, finite input and the fitted score gradient; none of these checks turns a fitted interaction into causal mediation. The synthetic duplication control repeats observations within each existing game and requires the coefficient and CR0 covariance to remain unchanged, directly testing that copies are not treated as new independent clusters. [Q250B-061] [Q250B-063] [Q250B-068]

The explicitly post hoc matched-batch analysis changes the resampling unit and target. Its treatment-metadata gate requires six mixed batches containing paired three- and seven-person arms, and two paired fifteen-person batches. It declares 46 matched games and excludes the unpaired fifteen-person collective game. For each mixed batch it retains the vector of its size-three and size-seven treatment differences; resampling these vectors together preserves their cross-size covariance. Fifteen-person batch differences are resampled separately, and the three resulting size means receive equal weight. The source additionally reports size-specific and overall leave-one-block-out ranges, the two fifteen-person differences, missing contributing games, a design-count-weighted batch contrast and an available-game-equal contrast. Those latter weightings can differ when outcome availability differs. The small paired-batch support is not certified randomisation inference and does not replace the primary game-bootstrap estimand. [Q250B-062] [Q250B-061]

#### Cue dependence, finite tests and complete replay retain their own scope

The pair-correlation calculation requires at least twelve jointly observed rounds and nonconstant correctness vectors. Short-overlap and constant-vector pairs are counted separately rather than assigned correlation zero. It averages eligible pairs within each game before taking the game-level contrast; local/shared cue correlations on the same selected overlap are different from the separate full-vector manipulation checks. The latter inspect all 48 recorded cue positions, shared-cue identity within each game-round, correct-cue counts and both pair-weighted and game-equal cue correlations. They tabulate response correctness for the four local/shared cue-correctness combinations and for cue agreement versus conflict, separately on stored-score and final-forecast support. These are finite-vector descriptive checks. Neither exact recorded sharedness nor a small empirical local correlation proves stochastic independence, causal mediation or a learning trajectory. [Q250B-063] [Q250B-064]

The replay entry point requires both explicit local input files and a new or empty output directory, then runs reconstruction, primary estimation, post hoc batch sensitivity and cue checks in that order. It downloads nothing. The package requests Python 3.12 with NumPy 2.3.5, pandas 2.2.3 and SciPy 1.17.0. Its synthetic test source specifies wrong-digest refusal before estimation, preservation of a nonempty destination, Boolean/capacity guards, selected-overlap rules and covariance/paired-bootstrap identities. Reading those tests is not running them. The source-only package and the pinned libraries remain necessary to reproduce this implementation, and its local intermediate participant records are not redistributed by this exposition. [Q250B-060] [Q250B-065] [Q250B-066] [Q250B-068] [Q250B-069]

The later public empirical status explicitly reports completed author and independent replays after an earlier acquisition blockage was resolved. Its accepted comparison reverses approved narrative metadata substitutions without changing any numerical field. The public terminal records are status-and-digest projections, not the underlying numerical reports. Their completion claim must therefore neither be downgraded to “synthetic tests only” nor promoted into a fresh execution here or a new independent experiment. The original exact data and result bodies have not been acquired for this static source reconciliation. [Q250B-059] [Q250B-058]

[Q250B-058]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a9fbe1d74a790020862fb39a37cb2951131d63f09779e60c9dd57b1c77188408/VERIFICATION_GUIDE.md
[Q250B-059]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/58057a18451ec4f2b995df6b226b1d619f9109423b091769d39d68999b639c22/README.md
[Q250B-060]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/69719284fe2764e2c7a85d223ba4bf7b4e5067ae6efcab544ba547412233a947/README.md
[Q250B-061]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/84d819256b564b4acc8def4602d6882cebfd15417f44e8f9c3b5005d459f8875/analysis_core.py
[Q250B-062]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0e17bc10f0e52c199fece92cd649c6006e7e7b5b9c94dce834b6410d288ab8d0/batch_sensitivity.py
[Q250B-063]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/f9b3153dcad9a21842796a09df7966b26c1348f0785f3863e09177b28f6a3aa3/estimate_contrasts.py
[Q250B-064]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a67a96c885051d5639869b7fe01d5f07a00a8269f50ee9f48f9ec06e8b55a288/manipulation_checks.py
[Q250B-065]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/562d0dd4f09cbd8a3bdba354cdb6b9430f8ca7bfc1e24ca8c5dda37371f25fe6/replay.py
[Q250B-066]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/65b97f7db87e4cdcb0f4157240cfece5b48363b3e6a18fdccf72d6528ebcbf85/requirements.txt
[Q250B-067]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/86bc29fab24a54e5a09efce1a7696b9491f28b95cd23ed4ecee89e076e524baf/run_reanalysis.py
[Q250B-068]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a1be6c6b5a84eeb7d3417fdc8713fcd0d7982d7358ddf0cc78079b2f0ba60a6a/test_analysis_core.py
[Q250B-069]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/fc6def72d222220c4a9da5b443c3e528eede27a4e4bb14bc6a10c74eb7bad151/test_replay_cli.py

### 10.5 Incomplete records of a fixed outcome

A recorded correct answer, a completed finite run and a successful whole inquiry can be different outcomes. The reassessment linking collective diagnosis with committed continuation makes this distinction precise at an original deadline. Fix the task, required components, evidential conditions and deadline before classifying the cases. If success requires their conjunction, an observed failure of one required component makes the whole outcome a failure even when another component is unrecorded. If no required component is known to have failed but the record cannot establish the conjunction, the case remains unresolved. A later repair can be a real success at its later task without changing what occurred by the original deadline. [12, §5][r12]

This distinction is between an outcome and the evidence for it. Missing recording alone establishes neither incompetence nor action without permission. Conversely, an unknown component cannot cancel a known failure of another required component. Calling every recorded favorable output a whole-task success changes the target; calling every unresolved case a demonstrated failure changes what the evidence establishes.

For a nonempty fixed cohort of N cases, let S be the number with established whole-task success, F those with an established failure of the conjunction, and U the unresolved cases. Thus

```math
N=S+F+U,\qquad N>0.
```

Assume the established classifications are sound for that fixed factual outcome. Each unresolved case has a binary actual outcome, even though the available record does not determine it. If z is the number of unresolved cases that actually succeeded, then $`0\le z\le U`$ and the cohort's actual success fraction is $`p=(S+z)/N`$. Therefore

```math
\frac{S}{N}\le p\le\frac{S+U}{N}.
```

The proof uses only the number of unclassified outcomes. With unrestricted binary completions, setting all unresolved outcomes to failure or all to success attains the two endpoints. The possible fractions between them are discrete for a fixed finite cohort; the displayed interval is their exact lower and upper envelope, not a claim that every real point in it is attained. Extra constraints on the missing cases can tighten the bounds. When U is zero, the recorded cohort fraction is determined. Sampling uncertainty about a different population is a separate question, so these bounds are not a confidence interval. [12, §5][r12]

For two cohorts a and b, write their corresponding bounds as $`p_a\in[L_a,H_a]`$ and $`p_b\in[L_b,H_b]`$. Subtracting gives the sound outer bounds

```math
L_a-H_b\le p_a-p_b\le H_a-L_b.
```

Attaining an endpoint requires a **jointly feasible** completion: a completion attaining $`L_a`$ must be compatible with one attaining $`H_b`$ for the lower endpoint, and conversely for the upper endpoint. Separate marginal attainability does not suffice. For example, suppose each cohort consists of one unresolved case and a justified constraint makes their outcomes equal to the same unknown bit. Each marginal permits both zero and one, but their difference is always zero. Combining opposite marginal endpoints would invent an impossible completion. If the two cohorts' admitted completion sets instead form the full product, the endpoint combinations are available. This simple control makes the source's joint-feasibility qualification explicit; it is an expository construction, not a reported dataset. [12, §5][r12]

These calculations concern incomplete records of an already fixed factual outcome. They do not establish a causal treatment effect between the cohorts. [Recognition, Warrant, Defeat and Restoration, §9.6](../epistemology/recognition-warrant-and-restoration.md#96-what-a-comparative-study-can-identify) addresses the further question of beneficial within-unit change when two potential-outcome marginals are identified under the required comparative assumptions. Its joint-outcome bounds should not be substituted for missing-record bounds, or used to certify a wider restoration conjunction from a proxy alone.

Outcome adjudication must also keep decision time and task type fixed. A known failure of any required component makes the whole endpoint fail; an incomplete evidential record without such a failure leaves it unknown. A missing recording is not itself a certificate of non-delivery, and later reconstruction cannot supply warrant retrospectively. Conversely, a genuinely supported reevaluation delivered before the original deadline is assessed at its own decision time: an earlier unsupported statement is not an irreversible failure if the task permits correction. Warranted deferral can be positively justified, but it does not complete a task that required resolving a resolvable question; warranted uncertainty can complete a task whose correct outcome remains unresolved. Whole-cell compensation does not transfer another member's designated role. These rules determine which observations enter the already defined success/failure/unknown counts. [Q250A-007]

For the proposed four-arm access-by-integration design, keep every assigned case in its original arm. The primary contrast is $`A^+I^+`$ against $`A^-I^-`$; simple access effects are evaluated at each fixed integration level and simple integration effects at each fixed access level. An interaction is secondary. Conditioning on achieved receipt, comprehension or successful integration would change the estimand after assignment and does not identify a mediation effect. The finite missing-outcome bounds above describe feasible arm endpoints and jointly feasible risk differences, not confidence intervals, population estimates, power calculations or a sample-size justification. [Q250A-007]

The source's empirical comparisons show why the outcome has to remain fixed. Its inherited same-data comparison of 15 dyads reports mean sensitivities of 4.15 for immediate discussion and 3.44 for private-vote-first, with $`t(14)=2.704`$, $`p=.0171`$ and a reported 95% interval of 0.147–1.278 for the contrast. This is positive, source-reported evidence of a procedure-relative difference at that study's scope. Missing private responses in the immediate-discussion condition leave individual contribution unidentified. The Gaussian mechanism pair in §8 is an explanatory nonidentification control, not a fitted assertion about those participants. No new cohort or empirical reanalysis is supplied here. [12, §5][r12]

The same reassessment credits Pan's reported finite onward construction and RepliBench's finite construction-role renewal while preserving the non-chain baseline log, incomplete final startup observation, discrepant figure rates, untested further generation and shared inference support in the respective reports. These limits leave the positive finite capabilities intact. Duplicate author-hosted and arXiv PDF witnesses do not become independent corroboration, and different studies cannot be combined into one demonstrated lineage possessing every desired property. The archived group-score reanalysis in §10.4 likewise has its own cohort, outcome and reading scope. None of these observations is made into a new execution or a proof of indefinite supported continuation. [12, §5][r12]

The mathematical continuation result provides a separate exact boundary. [Measure, Computability and Finite Warrant, §§9.1–9.3 and 9.7](measure-computability-and-finite-warrant.md#91-finite-success-and-an-indefinitely-continuing-policy) gives a finite planner at every requested horizon whose corrected plans converge coordinatewise, yet no computable irrevocable infinite lineage exists. Recomputing a provisional plan does not revise an already enacted causal past. The positive repair supplies an effectively accessible pruned region, with the required common support and permission premises preserved. Observed finite success, sound retrospective correction and supported indefinite continuation therefore each retain their own positive content and their own further conditions. [12, §4][r12]


#### What the retained fifteen-dyad reanalysis actually checks

The separately retained reanalysis package is a reproducibility contract for the same fifteen paired dyads, not an additional empirical cohort or a replacement for the distinct 232-participant study in §10.4. It requires separately obtained archive and workbook inputs with mandatory expected hashes, verifies the selected MAT member's identity, and checks the declared 128-row layouts, eight contrast levels with sixteen trials each, response/correctness coding and paired-condition alignment. Missing announcement timing is checked to occur exactly on agreement trials and is not a filter on the choices. Announcer-specific subsets can have unequal level counts; the declared equal-bin fit therefore averages the eight level contributions rather than silently substituting trial-count weights. The weak/strong ordering is reconstructed from private slopes, retaining a negative slope instead of forcing sensitivity nonnegative. [Q250A-043] [Q250A-046]

The two numerical paths implement a common probit target through different optimization checks. The BFGS path uses stable log-CDF calculations, an analytic gradient, three starts and a stationarity tolerance; its rescaled slope is converted by division by $`\sqrt{2\pi}`$. The checked path uses a different predictor scale, an analytic Hessian, trust-region fitting, score-root polishing and a separate Fisher-scoring line search. It requires a small score, positive observed curvature and agreement among starts and the alternate solver. The wrapper requires the two implementations' derived values to agree within $`10^{-6}`$ and both to reconcile the supplied workbook at four decimals before computing the paired immediate-discussion minus private-vote-first contrast with fourteen degrees of freedom. Agreement of algorithms is a valuable numerical check, not independent participants or independent evidence for the mechanism. [Q250A-044] [Q250A-045] [Q250A-046]

The pinned numerical dependencies are NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3 and openpyxl 3.1.5. The synthetic tests exercise signed slopes, derivative differences, unequal-bin weighting, the paired contrast direction, timing missingness without choice filtering, malformed inputs, hash mismatches and output-overwrite protection, including hard links. They are invented fixtures, not new source trials. The validation wrapper reruns the aggregate calculation and compares exact output keys, Boolean values and numeric values with absolute tolerance $`10^{-7}`$ and zero relative tolerance against its separately retained aggregate reference. It emits aggregate JSON, not participant rows, and grants no permission to redistribute the private inputs. All scripts, pinned dependencies, locked data and reference output remain dependencies of a replay; the present static reconciliation neither ran that replay nor newly verified the inherited numerical estimates. [Q250A-047] [Q250A-048] [Q250A-049]

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

The ordinary Markov and retained-rotor reviews [54–55] qualify their own exact predecessor sources, including the completed-event stopping argument, rational allowance and all-counter-vector closure proof. The hidden-priority and posterior-deterministic reviews [56–57] supply distinct ordinary scope: full-pair recurrence, min-even pruning, the actual joint kernel, observable-history equivalence, unshifted cost and priority streams, and almost-sure attainment. These contributions are integrated into §7.14 beside the existing stateful theorem; they are not new kernel executions or qualifications of a production solver. The later literal signed-service results in §§7.15–7.18 keep their own source and implementation identity.

The recovery's integrated-report review [58] expressly separates fresh mathematical arguments and bounded finite controls from missing older formal closures and from historical-priority claims. Its control-and-memory, hidden-objective, clock and attainment distinctions remain operative here. Source-relative finite-check counts remain historical evidence for their exact freezes, not fresh execution of this exposition. Neither ordinary source review nor successful control proves the separate philosophical premises summarized by that report, and the report's bounded application comparison is not empirical validation or external endorsement. This edition's explanatory construction and composition require their own independent scientific review.

### Staged restoration reviews and the scope of their conclusions

The complete public *Independent read of controlled-information
restoration draft* [53] records six successive mathematical and
specification readings on 30 September 2026. The first reviewer is
identified as the source/intentionality bridge contributor, distinct
from the controlled-restoration author. Those readings are not
reported as fresh independent kernel compilations. Their conclusions
belong to the versions and interfaces actually read.

The initial finite positive-law reading supports the ordinary
necessity and sufficiency arguments now in §7.11: recurrent good
actions must sustain the needed discrimination; full-prefix transfer
uses deterministic cuts; and the common seed has the behavioral
reduction proved above. It retains full support, fresh controlled
observations, common licensing, finite model/action/observation sets
and unrestricted memory. The asymmetric good-action example, the
singular-revelation counterexample and the absence of a finite
last-error declaration preserve the source's limits. Its
continuous-space discussion requires the explicit measurable,
standard Borel and common-continuation hypotheses stated in the
broader obstruction. The geometry-to-control composition requires
the same issued output, target and sample contract as the
[binary-repair treatment](information-and-inquiry.md#97-unknown-standards-the-information-needed-for-persistent-repair).

The second reading identifies the greatest-kernel lemma needed by
the support-elimination argument. The contracting monotone deletion
proof and survival of every self-verifying subset are explicit in
§7.11. The recursive support construction in §7.12 separately
accounts for all positive exits, uses unnormalized continuing
likelihoods and preserves the support-dependent menu. Hardcoding an
acquired prefix into a continuation remains justified only because
the model is fixed, future acquisitions are fresh, and the relevant
state and permissions are represented. Omitted plant state,
exhausted resources, changing versions and unrestricted
history-dependent permissions remain outside that argument.

The third reading inspects a canonical support-block selector whose
inputs are the supplied finite family, support family, fixed initial
candidate and already-used stack prefixes. Its theorem concludes
eventual nonempty good **blocks** under declared joint independence,
correct marginal laws and full support. The ordinary block-to-action
argument and the later explicit queue construction have their own
premises. That historical read does not certify the full ordinary
iff, zero-support recursion, finite memory or an actual sensor and
permission model.

The fourth reading exposes two genuine missing implications:
decreasing rank does not imply permanent exclusion without support
inclusion, and positive charged cost implying badness does not
establish domination of executed bad actions. Both distinctions are
proved explicitly in §7.12. The guarded successor preserves true-model membership along
positive-probability exits from live phases; it need not place the true
model in irrelevant analysis phases. The same reading leaves open the binding
between a finite-tree reset calculation and an actual infinite path
law. The fifth reading checks the later six-module seal
`generated-qualification-20260930T214115Z`, containing
`ResetTrajectory`, `ResetFutureCost`, `MarkovCharge`,
`ResetExpectation`, `TrajectoryBudget` and
`GeneratedLiveController`. It reports the generated Markov law,
the history-mass-times-normalized-cost identity, the zero-mass
case and exact current-state charge indexing. The reset calculation
above makes that identity readable without asserting a fresh formal
replay. `RecursivePhaseExtraction` and `StoppedSupportUpdate`
were inspected outside that earlier seal and are not silently added
to its six-source population.

The sixth reading checks eight principal extraction, recorded-prefix
and decoder sources against the separate seal
`action-decoder-qualification-20260930T221510Z`. It retains
the old execution record on reset, the empty initial placeholder,
nonempty later prefixes, the initial-record cost adjustment and the
total decoder's irrelevant fallback on the proved event. It supports
measurable physical eventual goodness and executed-charge transfer.
It expressly distinguishes that endpoint from physical-action
nonanticipation, as explained above. Later policy-law endpoints in
references 38–43 and their existing chapter proofs retain their
separate qualification; this historical sequence is not a new
combined source closure.

Finite expected error count and almost-sure eventual goodness never
become a claim of integrable final-error time; the explicit late
single-error example in §7.12 separates them. Analysis potentials,
costs and probability laws may be indexed by the true model, while
the selector and public state update must remain common. None of
these readings supplies source authenticity, normative authority,
original representation, consciousness or an ultimate bearer. The
report's dates, named seals and source-hash lists remain historical
provenance; the author's builds and another reviewer's kernel replays
are different evidence. The present additions preserve and explain
those distinctions without executing the historical controls.

## References and source editions

The numbered project sources below identify public research editions. They establish attribution and allow comparison of the inherited statements and corrections. The arguments required for this chapter are given above; ordinary reading does not require reconstructing those historical files. Source extraction is distinguished from the unretrieved original PDF, and a section citation does not claim incorporation of an entire larger work.

1. Orthemology project. *Multi-Actor / Zero-Sum Orthemic Note: stress test, corrections, and formal residue*. Public revised analytic note, 20 July 2026. [Exact public edition][r1].
2. Orthemology project. *Orthemic Core Formalization: Orthing, Episodes, Metaorthemes, Pathway Adequacy*, §§5.2–5.3. Public revised formal core, 20 July 2026. [Exact public edition][r2].
3. Orthemology project. *Five state evidence control*. Ordinary mathematical construction. [Exact public edition][r3].
4. *Epistemic Tuples and Intra-Agential Equilibrium: A formal thesis on evidentiary profiles, cognitive faculties, mixed epistemic policies, and equilibrium*. Public text extraction of the manuscript. The original PDF is a distinct edition and is not newly authenticated or reproduced here. [Exact public extraction][r4].
5. Orthemology public research. *Epistemic tuples and equilibrium as a typed restoration test domain*, especially the corrected scalarization, local-information, finite-game, vector-equilibrium, team-concavity and temporal arguments. [Exact public edition][r5].
6. Orthemology public research. *Relative normative-gap disclosure with an exact continuous-weight checker*. Relative admissibility, exact sign-cell comparison, canonicity and philosophical limits, and finite ascent are treated in §§2.1, 2.4 and 7.2. Original prototype, execution and primary-reading claims retain their separate scopes. [Exact public edition][r6].
7. Orthemology public research. *Graded Representations, Witnessed Revision, and Inquiry Landscapes: A conditional mathematical extension of Orthemology*, §8 and reference appendix. Research draft, 8 September 2026. [Exact public edition][r7].
8. Orthemology public research. *Continuation-Complete Orthings: Sharp information loss, minimal predictive memory, and safe strategic composition*, the pairwise-parity and strategic-composition sections. Research supplement, 8 September 2026. [Exact public edition][r8].
9. Orthemology public research. *A bounded information consequence for coordination explanations*. Ordinary-mathematics result, 4 October 2026. [Exact public edition][r9].
10. Orthemology public research. *A sharp error budget for finite coordination modes*. Ordinary-mathematics corollary. [Exact public edition][r10].
11. Orthemology public research. *What final answers can identify about collective evidence use*. Complete constituent of the public mathematical compendium, 5 October 2026, including its finite and sequential discrimination results. The other constituent works are separate. [Exact public edition][r11].
12. Orthemology public research. *Collective diagnosis and committed continuation*, 11 October 2026. Adaptive inquiry, linked information, recalibration and incomplete outcome records are treated in §§8.3 and 9–10.5; the committed-continuation arguments are developed in [Measure, Computability and Finite Warrant, §§9.1–9.3 and 9.7](measure-computability-and-finite-warrant.md#91-finite-success-and-an-indefinitely-continuing-policy). Original empirical and execution claims retain their stated evidence scopes. [Exact public edition][r12].
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

36. Orthemology public research. Recursive support certificates, live-model self-verification and the finite stage interface. Exact Git objects: `e7701448d95bdc8c60e539df3531f16b19ff9c4b`, `f6c5c5e49e7d2443d61310f84c522551d14cb155`, `aa0685e6ab327d463442ad81816e780e35e3fcac` and `1b5c1ce9787d0e4bd33f9b2b8d526caea4fcd127`.
37. Orthemology public research. Guarded live-controller budgets, recursive phase extraction and physical-action decoding. Exact source objects: `182b9cb7df5dd153e0689fa875fe66bccbb9131d`, `7775998d720b8975bc6f44c12eb0bc0a2a5b4ffa`, `fa314059dcd26e131cb6f62be9434ba726fa593e` and `401cd2d590030834a5c30969dcf0ed2543acd0dd`. The earlier independent constructive review is the exact public object `38e462ee8c12a50cce8fd6bccf5ca3dde2597458`. Original execution and dependency evidence retain their own scope.
38. Orthemology public research. Zero-support canonical causal sufficiency. Exact theorem object `5df005790b352fbef1025edf47f64777d8acdd7d`; exact public review object `f320596f12ed2fcaa197dd26ba3490704e56e1c8`. Its feasible action-consistent history contract, finite physical-cost conclusion and historical source qualification are distinct from a fresh kernel replay.
39. Orthemology public research. Recursive same-policy-law equivalence. Exact theorem object `c96dd7ee08b6b4a69e64b215f4e90d051f0510a2`; exact public review object `ec10faa1fd2a0248945de137db28f9b1c8bcc8b4`. The necessity proof and its original dependency closure remain separate from the constructive treatment here.

40. Orthemology public research. Recursive necessity, invariant safety and stable-support necessity. Exact Git objects: `669d9f1931717f0e9b15044cee87b4d456a632f7`, `2854f3900577895a322428c030f8361ab91745fd` and `c79c6bcf2fab2258a78c7d97f707d351c547583c`.
41. Orthemology public research. Common-seed derandomization, deterministic acquired-history continuation and the independent head/tail law. Exact Git objects: `827b7258ca49c904a3a08fd344dbff8c0b00d02f`, `a7b647d2e962beca46b4256dd776bff9c555e9fa` and `b448bd272b30aff8ba694ac9e2e85f08be6fda81`. The exact canonical stack-law bridge is object `fd0f87524f95c5f807615a0bf89ed99cd3c173cb`.
42. Orthemology public research. Relative finite-prefix transfer and transfer guarded by the actually visited action set. Exact Git objects: `293a90207a83252c9132ea7695403efbf554484c` and `dc99af6ec60084a53f318f5d8f1dac9e707d1b29`. The broader finite-query implementation and original source closure retain their own scope.
43. Orthemology public research. Common winning continuations after positive acquired histories. Exact Git object: `937ae4e2933820e6036f042a9cefade4c9d34e1c`. The literal seeded-policy equivalence endpoints and their historical independent review are cited in reference 39.

44. Orthemology public research. *Markov acceptance with revealing support changes*. Complete public prose projection, exact Git object `4e69862256f3014f8e94d528b13ff0f63dd7f3eb`. Its randomized construction, completed-event navigation proof, quantitative bounds and original source qualifications remain distinct from the deterministic successor.
45. Orthemology public research. *A computable deterministic scheduler for the recovered Markov theorem*. Complete public prose projection, exact Git object `80e45c60c8f4e71a8191f906d04afd4ab0384b06`. The retained counter vector, augmented-state proof, target-pruning argument and common-support reduction establish the stated ordinary refinement; no lost historical review is reconstructed.
46. Orthemology public research. *Concrete allowance for the deterministic construction*. Complete public clarification, exact Git object `6bcd9f7c0faea3fe3037c1f188288555312517b1`. The rational choice ε=1/2 supplies the effective threshold parameter without changing the abstract existence statement.
47. Iadine Chadès, Josie Carwardine, Tara G. Martin, Samuel Nicol, Régis Sabbadin and Olivier Buffet. “MOMDPs: A Solution for Modelling Adaptive Management Problems.” *Proceedings of the AAAI Conference on Artificial Intelligence* (2012), printed p. 269, hidden-model definition and Proposition 1. [Primary paper](https://ojs.aaai.org/index.php/AAAI/article/download/8171/8029).
48. Marnix Suilen, Marck van der Vegt and Sebastian Junges. *A PSPACE Algorithm for Almost-Sure Rabin Objectives in Multi-Environment MDPs*. arXiv:2407.07006v1 (2024), §§3–6. [Primary preprint](https://arxiv.org/html/2407.07006v1).
49. Min Chen, Emilio Frazzoli, David Hsu and Wee Sun Lee. *POMDP-lite for Robust Robot Planning under Uncertainty*. arXiv:1602.04875v3 (2016), §§III–IV. [Primary preprint](https://arxiv.org/html/1602.04875v3).
50. Xiaoming Duan, Yagiz Savas, Rui Yan, Zhe Xu and Ufuk Topcu. *On the Detection of Markov Decision Processes*. arXiv:2112.12338v1 (2021), §§I–IV. [Primary preprint](https://arxiv.org/html/2112.12338v1). This identifies the inspected preprint edition; the source's journal-version comparison and any later correction retain their own evidence boundaries.

51. Orthemology public research. *Synchronisation deficit and provenance-innovation rank balance*, revised public proposal. [Public source edition][synchronisation-source]. Exact Git object: `360478ec98f93ca4d0281023fb86ed42287fbc32`. The finite-dimensional argument, old-recovery correction, counterexamples and application limits are incorporated in §1.4; the zero-row qualification is made explicit there.
52. Orthemology public research. *Provenance-root nonmultiplicity under copying and synchronisation*. [Public source edition][lineage-source]. Exact Git object: `37cdc615db920ea2eb559b338a9b68acacdc4fac`. The lineage invariant and controls are incorporated in §1.4. Its historical checker counts remain source-reported execution evidence, not a fresh run or a new general theorem.

53. Orthemology public research. *Independent read of controlled-information restoration draft*. [Complete public projected review][restoration-staged-review], 30 September 2026. Six sequential mathematical/specification readings distinguish the ordinary finite criterion, support elimination, canonical blocks, reset budgets, generated expected charges and physical decoding; they are not fresh kernel replays.

54. Orthemology public research. *Fresh independent ordinary review of the support-changing Markov theorem*. Complete public projected review of the exact support-changing source, retaining necessity, row-test stopping and inherited-qualification boundaries. [Exact public edition][t4-markov-review].
55. Orthemology public research. *Fresh independent review: deterministic round-robin successor*. Complete public projected review of the scheduler and rational-allowance clarification, including the augmented-state and reset-starvation controls. [Exact public edition][t4-rotor-review].
56. Orthemology public research. *Fresh independent review: hidden parity extension*. Complete public projected ordinary review, including the recurrent-set criterion, odd-minimum pruning, posterior-deterministic consequence, finite-monitor limitation and exact co-Büchi encoding. [Exact public edition][t4-parity-review].
57. Orthemology public research. *Fresh independent review: posterior-deterministic hidden coBüchi crosswalk*. Complete public projected ordinary review of the finite rational joint-kernel construction, policy and path-law transport, descriptor complexity and value-one counterexample. [Exact public edition][t4-pd-review].
58. Orthemology public research. *Final integrated fourth-tranche claim review*. Public projected source-bound report review. Its mathematical, implementation, philosophical and application limits retain their separate scopes. [Exact public edition][t4-integrated-review].

[synchronisation-source]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6
[lineage-source]: https://github.com/theislampill/orthemology/commit/a7ff0e33d1a299db640041c46b1af81ca70851f6

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

[signed-companion]: https://github.com/theislampill/orthemology/blob/7b385e4116b052a0132dd740d07b918d3103f648/experiments/orthemology-v5-successors/source-store/10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e/FULL_READER_TEXT_v5.md
[signed-report]: https://github.com/theislampill/orthemology/blob/7b385e4116b052a0132dd740d07b918d3103f648/experiments/orthemology-v5-successors/source-store/a59f7555e3f32f6869c55c28013a7dc94ee14a744494cf9e4a34eccf9770de78/SIXTEENTH_REPORT.md
[empirical-pescetelli]: https://journals.sagepub.com/doi/10.1177/26339137251372605

[restoration-staged-review]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/docs/provenance/v5-research-continuations/notes/deb77eb74e9172f964247172725074e94633de9a76fe30d62e4788ef06bb399d.md


[t4-markov-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/e9d10938606929f7f64512e650c2a428388844ddfcad1ba6f5c58d97444d95d2.md
[t4-rotor-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/2d04cd0598a7933cd502289ab8b89fb02023902257d4514ec748f0a29922b257.md
[t4-parity-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/4698db33ea1d4e8670d0496e52de19f92dbc8665087d6ffbf88f54c3da56f2cc.md
[t4-pd-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/efb018e75afe764c7acee58f0ca391df5b3ed0c77b59aaeb50027f1e8f00956d.md
[t4-integrated-review]: https://github.com/theislampill/orthemology/blob/0e92ccbd8c16190ad6b18e6e61cd86db07d47202/docs/provenance/v5-research-continuations/notes/9412522bec33bc12a790e1610d328b160a00cf25eea03126ec219f01abc5e5ac.md

[receipt-au-01]: https://api.github.com/repos/theislampill/orthemology/git/blobs/7fa57eb705afaf25c29a8b456e82c90087bda2c4
[receipt-au-02]: https://api.github.com/repos/theislampill/orthemology/git/blobs/19d46308364406bb113e41cd16ea35c0a149ffd7
[receipt-au-03]: https://api.github.com/repos/theislampill/orthemology/git/blobs/5e0b7da712a47faf4587e227412d82188bf64ed9
[receipt-au-04]: https://api.github.com/repos/theislampill/orthemology/git/blobs/e4d29b87361df7ec26d69bf1f998d0202b6c2db8
[receipt-au-05]: https://api.github.com/repos/theislampill/orthemology/git/blobs/9e5ee0ff8395babb51c6c0865f9989072a35f986
[receipt-au-06]: https://api.github.com/repos/theislampill/orthemology/git/blobs/b3c087138f108241406cb6e8c7092607fd8247eb

## Source records for one-step agreement

The following exact source editions supply the arguments, recorded failures, repairs and finite checking history cited above. A result or disposition is attributed to its historical record; the incorporation performs no new execution of the source programs. Mathematical ancestry and interpretation limits remain those stated in the corresponding sections.

- [R68-S020] — **One-step agreement with varying correct participants: audit** (cold audit).
- [R68-S021] — **One-step agreement with varying correct participants: review** (distinct review).
- [R68-S022] — **One-step agreement with varying correct participants: results** (result file).

[R68-S020]: https://api.github.com/repos/theislampill/orthemology/git/blobs/332fa5722e23ca135a90799ad6b97e3b9ea8be67
[R68-S021]: https://api.github.com/repos/theislampill/orthemology/git/blobs/5010c98adf35b5876d31b66f2afb3813dd15743b
[R68-S022]: https://api.github.com/repos/theislampill/orthemology/git/blobs/42fea34a366d8e4a8b1ce3afdfbb1bfa696282ed


## Source guides for the additional arguments and qualifications

These exact public guides identify the reported results, historical review scopes and dependencies used in the additional discussion. A guide citation does not claim receipt or renewed verification of every linked proof, primary source or execution record.

- [GUIDE105-G064] Rational actual-source bridge: additive preservation.
- [GUIDE105-G092] Independent hidden-parity target-pruning review.

[GUIDE105-G064]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/a288f1990b9320e0f4d0447d366ebaae7cd43344af8c16a1a6b421fb507396c5/README.md
[GUIDE105-G092]: https://github.com/theislampill/orthemology/blob/561b6bffea7af95a5eed767ba2e37d9dcc34f31e/research/t20-v6-20261012/sources/e1db9b4ba20122bfd5052fa802a5408493c8cde398d5155c657a8d4e4e9a0d25/README.md


## Source editions for the common exponential cost range

The following exact public editions are the theorem and proof texts used in §7.19. They are bound by the common-range suite descriptor, not selected from similarly named later modules. The comparison reconstructs their ordinary argument without asserting a new kernel replay or an unavailable historical independent acceptance. The bound uses the original generated policy; the separately compiled signed-body policy retains its distinct cost boundary.

- [EXP-common] **FiniteModelExponentialUniformity**, exact Git object `863a0388927949d9c75a604e8025dce7e2237cf3`; complete body read.
- [EXP-actual] **ActualExponentialMoments**, exact Git object `14235fc2e06c5adf2465818a6b0b7e64590b9f6b`; complete body read.
- [EXP-exp-tail] **GeneratedExponentialTail**, exact Git object `b520b9f22c7a775b473238c11f60e421539d239d`; complete body read.
- [EXP-affine] **AffineTailOptimization**, exact Git object `c7797aeb50ecb60ed4af47fcc64602f3eb0f78a0`; complete body read.
- [EXP-tail-moments] **TailMoments**, exact Git object `b32f686d61f9f3e91fd52410a2100884bc688263`; complete body read.
- [EXP-moments] **ActualCostMoments**, exact Git object `1bada0a94ab7fa45ef0346719ea8cd377e747107`; complete body read.
- [EXP-product] **GeneratedPrefixProduct**, exact Git object `c060aa26ebe3a0dca5ce6222d9d359d5229de010`; complete body read.
- [EXP-cost-law] **GeneratedCostLaw**, exact Git object `08e270e893aa959b5fe952d5d04a1e475e82289b`; complete body read.
- [EXP-cutoff] **ActualTotalCostTail**, exact Git object `d6740f8d1efc93196343e9f43cc7d4c622123121`; complete body read.
- [EXP-slot] **GeneratedSlotMoment**, exact Git object `e41d3edf34f8c0ca2c59b2666e9710a39609c082`; complete body read.
- [EXP-charge] **GeneratedChargeBudget**, exact Git object `2a2056483fe25dfc6186877f31235384e948be19`; complete body read.
- [EXP-tower] **PrefixWeightedProduct**, exact Git object `3c35db59850de00ce3cc89525b5548258e50cd20`; complete body read.
- [EXP-margin] **QuantitativeEmpiricalGate**, exact Git object `f4a7b6ec010df44f02458c57712f013e58bf55e7`; finite positive-margin theorem read.
- [EXP-test] **ObservedRowTest**, exact Git object `d4b346d7f1179bc27f8c8408a710eca96f2851ef`; finite common separation and literal empirical-test definitions read.
- [EXP-rotor] **FrozenRotorProgress**, exact Git object `50f6e54557c1fecf6e81dc53f108240c972ce50e`; rotor dimension definition read.

[EXP-common]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/d0b174d6c0dd1e96df91497883e297ef41fe1ddb3e08d14c050dab15a3d180cc.lean
[EXP-actual]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/20cd0fcfa5f1218776fd9377a32bb40c2324efc8cc85f08c490b8d16f3b2d595.lean
[EXP-exp-tail]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/4904e5827d4b972c32fb182f40707c96b46b7d309f0cd75d63c54c42615df22c.lean
[EXP-affine]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/ebc2d3831afafd6d1bda98da2213bdbb1dfe1fc164655f05945d9d7bf669c0d6.lean
[EXP-tail-moments]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/7f58b3c0270925b452c97ebeaaaa9383f7958f2c0c0b4fc6b578a7cde01ef4f7.lean
[EXP-moments]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/8b4014de8d7ae893631060dbe780cce434bccbce16524e6303e2c692f3fce46b.lean
[EXP-product]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/6ab22024412f84e0295bb162ea1cd84432c2610dc87c917fd71281a5507caa94.lean
[EXP-cost-law]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/9e5c38fdd7f3c7c3fe19dc9849cdba3ae3cb6abb1639d3ce7d4c8edfca0d7736.lean
[EXP-cutoff]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/a55e4106c813ee266475198cadd3b93a90b2256b9d486468b5405d993b27bb4b.lean
[EXP-slot]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/3c4ed79c762cc1e81f5b0ff4797c10fb0e45ab17b5c79a24495f8c8af775116b.lean
[EXP-charge]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/4e315dcb799ddd5cd1c8b9a3392b0e159c38f271ca1826cb3e9625f1e44693ff.lean
[EXP-tower]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/b8010ed64321d19eebe4a8b08b5b9066717bf701e40d64b254eef6a7caa55d32.lean
[EXP-margin]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/00743077f4ad01f106967f1200f4d8a0d2b04cd48c568ad0a82ab4ae38b9b5c3.lean
[EXP-test]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/e38e3a972bbdf859b854b42c44a7cbf4d83c0f5b2fb7566d2f726f155572bfee.lean
[EXP-rotor]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/experiments/orthemology-v5-continuations/source-store/3804ba91149f9672a3c6e8c878c53a6661c74cb11f15069fbb7c9b5afb555703.lean

[specialist-a-radius]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R5_COMMON_KNOWLEDGE_RADIUS.md

[specialist-a-uniform]: https://github.com/theislampill/orthemology/blob/c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce/docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R4_OBSERVATION_COBUCHI.md


## Exact formal source interfaces for the consolidated qualification

[fc250-0]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0009ee9c664a710663a7c5b32418610d87bc92d62cdbd4840aa2ffadb1e48f97/SignedService.lean
[fc250-9]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/029cc4ad8bd297767b4365ca1aa4e2731be8e1c279d838ec9dfe2ea327e0eb0f/CompiledServiceDependencies.lean
[fc250-50]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0d7903e07dec34ff6706a0579b4b59cc911f98240ddc9585be4eb23710542bbf/DirectRun.lean
[fc250-61]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/106c15b37e7b54d132d367687d7a8f3b9b881fdc5f2336059527ab612fdcb7b0/DirectStability.lean
[fc250-62]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/1073426563bc23a80db142b34efce42143df772823fd330390e0046c4c5996bc/FiniteListsControls.lean
[fc250-109]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/20af8b9ff9911bcfb4839e8456363cd707d13c19df4269ffd21335dab817cd1f/DirectEndpoint.lean
[fc250-114]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/21ce74039d33a3d5573422374a857d3ac3a5945403982efbf68aee66e0698b33/IndexedCoverage.lean
[fc250-115]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/222b6d8cb68432c716845e31e842fe49ad7d273ab8237d4b5e195ebc828356f4/Refutation.lean
[fc250-142]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2a763523bd55662c8bc93aa71cd614a5c193739d15c15fb51bbd6add40e1460d/DirectSafety.lean
[fc250-175]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/35302cfdb1f172b18fd479d55c84905639f643a56b809f7a7e8f43407764c44a/FormulaBranchControls.lean
[fc250-176]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/35633954b024de762d61783ba20b80c238b71a1a764e15bf2411ea5ab9ae3aa0/EmpiricalHistoryTruncated.lean
[fc250-180]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/35a5d6255b3fb2076f1a7440051f05249a1c467c436e5fcd5fd008b2c07d8b35/SignedControls.lean
[fc250-209]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3daa65d1823676e1e861834eaa4b975c439d1890f1146790f5023379e829c02c/CertificateSoundnessRequired.lean
[fc250-218]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/403d3369cafa7d7285d68bd2b7559d83c20c85e152ce9ef99e63b77ecc8d8d0f/DirectParity.lean

## Source records for the exact first-cohort integration

[T07F029] NegativeControls.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0742ea0af9455417b94789b05a037538e766082d27f36d652664ae2be01fc807/NegativeControls.lean.

[T07F034] CriterionTransport.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/08d5efa5dc92642e6aec422389928314a0cd39c5a64f6f63032a369825905edc/CriterionTransport.lean.

[T07F035] AxiomAudit.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/092ab2114fc8caface95afac9a2d0379ac968a04f974779196e0ec75bfacb1c5/AxiomAudit.lean.

[T07F071] ReplayRuleInstallation.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/13bd258591c255005e0661291643b34364c98607c388b2a09961936beee39adc/ReplayRuleInstallation.lean.

[T07F075] B_replies_are_enough.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/14dc43264be5cd0eaddb9ef6362da0392e1e8627627bee8cefd7b3cb8fd1c165/B_replies_are_enough.lean.

[T07F106] THEOREM_MAP.md. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2061a7daab39d0b47fcf0740e348508510b9b7dfc6c02ac48c1fc8378f170908/THEOREM_MAP.md.

[T07F116] Artifacts.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/22c721beac4a8788436ce8fab017c4ccff4f832dc8ab0a95f8016c37fa91b560/Artifacts.lean.

[T07F143] approved_label_binds_substituted_bytes.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2bbb55544f4b60721ca9409d7306bd86cd96deefb6cc8d7246029d096f7496cd/approved_label_binds_substituted_bytes.lean.

[T07F145] ExactCap.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2cf94c485255f644b3d369b0e247d1c1d6d3bd228753e9fb12f40750b47d220a/ExactCap.lean.

[T07F147] OpaqueSearch.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2db9c51cecebf0f4d680c1b4fe82d9c3bbc8cfcf63920aa7f01ed1cc4e6ce3bf/OpaqueSearch.lean.

[T07F189] MultiEpoch.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/384f3f137bc52157f80d8bbab4281bd569cf0bf76de407be7b837ef93c9f2337/MultiEpoch.lean.

[T07F199] TargetB.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3a6a425d50a2fa2e94c3ecc0bcfbcd78cc9490f64167c3a09f3c5f41c79b2239/TargetB.lean.

[T07F212] TargetA.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3f02c883711d7b06151808d2246985e16cc62986db7ebc3da1a298d05d10af89/TargetA.lean.

[T07F238] FullCommandInterface.lean. Exact original: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4404a9dde8c580e01e1b752769e2a5a04a3af71e9b42b21a0d42b77b1fd2c746/FullCommandInterface.lean.


## Exact sources for formal and operational interfaces

[F250-10]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/02b4744e9d8bc25d6ea3bb58c6cc6e8d79e9345e0144f47a7c824e8adc25e714/AllNewAxioms.lean
[F250-11]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/02fa71e29d711f92d4f77c087609bd270eaae726ced36fb2cd748b695d1d37ab/CertificateFixtures.lean
[F250-15]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0466a5edff0defc5a4982ebf5b4f310b1ae2831a27b956fc4cc227c30f7c1ed4/ReviewAllAxioms.lean
[F250-25]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/063ae7ddf4123a414d29f3cf12a08691dcbb20967209010ebaf435a17c46d8bc/ReviewerControls.lean
[F250-64]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/11975a5518aa70a8b3cb264a07b155611dfc84992a75fc4fe2a417e46813bb0e/CertificateOrder.lean
[F250-107]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/206f1197ac41521668bfbb2939d6c817bfe1d114e7f32066e679ce038e999a82/CertificateBinding.lean
[F250-126]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/2628c64ef41e82c87c0c35890b12767b04a2075d8b25f98eb1137c2db3aaed57/PathEdgesMutationControl.lean
[F250-170]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/3452763b86cabba5a453c1d0c693f2bf2b8a55e525750ba9908c283f23bbb2ce/InputControls.lean
[F250-195]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/399829e271d3b6db65cfd077a68c15ad9a2e2f4d59d3957a2f30b6f2cd37a4ba/CertificateSoundness.lean

[HC250]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/464055b56abd1d1191fce18c116cb9c4c01227ceb056ba7e8d0f956d208dd5e3/HiddenChangeParityBridge.lean
[HC262]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/48d86b1dff40143d124a5074083059d321c0e22a532f480dc708a169e3b0ffb3/ControllerAxioms.lean
[HC265]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/49d8fdd5a54d8bb31c82801bb855a50d36ebc1d23bc56d7d8d222a45d6a0f5e4/ReviewerControls.lean
[HC280]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4cd70ef0b70a85f16dfa0fa7bc68eee0542af6416aea621741f314668e820eda/BindingControls.lean
[HC284]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4dd6f350a034531fad9d2753cc405503e152aed574c0e590febdf593b62b3fc4/FixedIndexControls.lean
[HC287]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4e2893243c488b572ff15d9dbf4c7053536110acac1e6cf2088e2e66bd8414dc/MutationRejectBeforeReveal.lean
[HC313]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/531276ea83eec88186836c473074c54fb96527e45889b9a7c39f288fa9fe8029/HiddenChangeUncertainProgress.lean
[HC331]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/578f6f4bc699f0658d77e0eff4dc39b995410b35f7380ddf02f68ed15550e70a/Orthemology_Eighteenth_Mathematical_Companion_Final_v1_20261006.md
[HC358]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5f1f208bdb9f837f69368e783e4fb5b6122927b113df8daba02392ba9474e26f/EndpointAxioms.lean
[HC365]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5ff601a4d001fb9db5fa49a5cb9fdae2d8a5caa76fadeb987d37b6c0f9f84563/EndpointControls.lean
[HC378]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/622117a8996db7a4de715666764643cce316519aa8de7137c06089088109ede9/MutationStrictDiscrepancy.lean
[HC387]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/646eab76f1f39827772ed08587824d7c945ba3b2ca6504f34841b6aa73ed4540/HiddenChangeSemanticEndpoint.lean
[HC396]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6767af52fc1cb0462631f66bd760960094643521336503dc844a12dc1e655e1a/ReviewAllAxioms.lean
[HC400]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/67c260c32c7d6db10fec65451d9efe09574bd1a0027c99fdb7f34965548d85b3/HiddenChangeActualRecurrence.lean
[HC403]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/68e3fa0145d194dc4d8532eb99237af170cb8736ba964ea8ea752bc0c04736bd/HiddenChangePrefix.lean
[HC409]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6b523d00092658c68f7fb6ebb0285ce83d9bde6e6855b7b7c6c450b9da6206ef/EndpointSeparator.lean
[HC412]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6c0b651c0910d309529007929d34e619617b3a2af51e64007033f265ffa1f20f/HiddenChangePolicyRegions.lean
[HC430]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/73b7076ec67e3a60bea1627928088c0edf8decaa53f41b96f4c782639f4c884b/HiddenChangeControllerDynamics.lean
[HC443]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7693bde5a031bd8b61970e495dd51d7fbd55dcf135e88064925ec57577b1ff3e/MutationClearsKnownFlag.lean
[HC461]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7c0f8725f69ceb644b4f18fd991d47a153f429657781920c2ec4cc7a16c08d9a/ControllerTimingRed.lean
[HC462]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7c11c21b07e296136e93287e8017d90b8f8dc8485ed04d3286e3d8c5dbd12f92/SupplementaryControls.lean
[HC476]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7ef35cb6890a6b3f721188d3fe569ea2b49faf06001403fbe89b3d4790aa333c/HiddenChangeTailTransport.lean
[HC497]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/850b3c60a6c6f7e44807a4e50bdae1f3789962a52b6716622fc06a08db5a14b5/HiddenChangePrefixSafety.lean



## Exact sources for source-warrant and interlock qualifications

These exact-public bodies were read as scientific prose or source code. Review replay statements are attributed historical evidence; no new execution or inspection of their referenced originals is claimed. Batch indices identify the present250-file cohort; manifest indices preserve its admission-source identities.

- **N250A-000**, cohort row0, manifest28395: [REVIEW.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md). Exact repository path `experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md`; SHA-256 `ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69`; 12,511 bytes. Role: authored_argument.

[N250A-000]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ff64060c0e14ba67437f92f5b714aa7018941c26b9afdf2aa86aba9cbe8bad69/REVIEW.md

- **N250A-001**, cohort row1, manifest25383: [SPEC.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md). Exact repository path `experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md`; SHA-256 `e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1`; 2,340 bytes. Role: authored_argument.

[N250A-001]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e39f418d04d5bb4e5e7a8866150a0aca063a79da707d450f48afbf43623785b1/SPEC.md

- **N250A-005**, cohort row5, manifest27900: [REVIEW_V2.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/faebf1a57d91ef459e12cedbb7cac455ff1d2e2476f1b2fc6347d2f20ae96180/REVIEW_V2.md). Exact repository path `experiments/orthemology-v5-successors/source-store/faebf1a57d91ef459e12cedbb7cac455ff1d2e2476f1b2fc6347d2f20ae96180/REVIEW_V2.md`; SHA-256 `faebf1a57d91ef459e12cedbb7cac455ff1d2e2476f1b2fc6347d2f20ae96180`; 17,392 bytes. Role: authored_argument.

[N250A-005]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/faebf1a57d91ef459e12cedbb7cac455ff1d2e2476f1b2fc6347d2f20ae96180/REVIEW_V2.md

- **N250A-006**, cohort row6, manifest14399: [check_primary_mutants.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/812dd6c8f15770791b87e2e94ac2c49858a2a58a17817aba50f4d78d8eddd6ae/check_primary_mutants.py). Exact repository path `experiments/orthemology-v5-successors/source-store/812dd6c8f15770791b87e2e94ac2c49858a2a58a17817aba50f4d78d8eddd6ae/check_primary_mutants.py`; SHA-256 `812dd6c8f15770791b87e2e94ac2c49858a2a58a17817aba50f4d78d8eddd6ae`; 2,169 bytes. Role: authored_code.

[N250A-006]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/812dd6c8f15770791b87e2e94ac2c49858a2a58a17817aba50f4d78d8eddd6ae/check_primary_mutants.py

- **N250A-007**, cohort row7, manifest25903: [independent_semantics.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e849927a94d6290db9ae5d34eea6ba0155fd266451c2261864c7daf97811fdc3/independent_semantics.py). Exact repository path `experiments/orthemology-v5-successors/source-store/e849927a94d6290db9ae5d34eea6ba0155fd266451c2261864c7daf97811fdc3/independent_semantics.py`; SHA-256 `e849927a94d6290db9ae5d34eea6ba0155fd266451c2261864c7daf97811fdc3`; 5,072 bytes. Role: authored_code.

[N250A-007]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/e849927a94d6290db9ae5d34eea6ba0155fd266451c2261864c7daf97811fdc3/independent_semantics.py

- **N250A-008**, cohort row8, manifest2511: [SPEC.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/177e21118d8a6c7e1df00c591729671122a534235dc76fe915d40e77e7423362/SPEC.md). Exact repository path `experiments/orthemology-v5-successors/source-store/177e21118d8a6c7e1df00c591729671122a534235dc76fe915d40e77e7423362/SPEC.md`; SHA-256 `177e21118d8a6c7e1df00c591729671122a534235dc76fe915d40e77e7423362`; 8,399 bytes. Role: authored_argument.

[N250A-008]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/177e21118d8a6c7e1df00c591729671122a534235dc76fe915d40e77e7423362/SPEC.md

- **N250A-009**, cohort row9, manifest14817: [mutation_controls.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/84cc407e25b40c3886f12d117669c9dd28254eaf47cd233de441a556c6244d4f/mutation_controls.py). Exact repository path `experiments/orthemology-v5-successors/source-store/84cc407e25b40c3886f12d117669c9dd28254eaf47cd233de441a556c6244d4f/mutation_controls.py`; SHA-256 `84cc407e25b40c3886f12d117669c9dd28254eaf47cd233de441a556c6244d4f`; 2,000 bytes. Role: authored_code.

[N250A-009]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/84cc407e25b40c3886f12d117669c9dd28254eaf47cd233de441a556c6244d4f/mutation_controls.py

- **N250A-010**, cohort row10, manifest5960: [semantic_controls.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/36b9b9141d3fec557bc5f95467861ae1eea980ce56f6821f1c3fa6019de3a5be/semantic_controls.py). Exact repository path `experiments/orthemology-v5-successors/source-store/36b9b9141d3fec557bc5f95467861ae1eea980ce56f6821f1c3fa6019de3a5be/semantic_controls.py`; SHA-256 `36b9b9141d3fec557bc5f95467861ae1eea980ce56f6821f1c3fa6019de3a5be`; 7,183 bytes. Role: authored_code.

[N250A-010]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/36b9b9141d3fec557bc5f95467861ae1eea980ce56f6821f1c3fa6019de3a5be/semantic_controls.py

- **N250A-011**, cohort row11, manifest9875: [CANDIDATE_E_COLD_ASSESSMENT.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md). Exact repository path `experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md`; SHA-256 `59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e`; 11,404 bytes. Role: authored_argument.

[N250A-011]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/59ac68fa9278932de6f35d30ef219bc7af9eca63e84f843e4b256103c2afb16e/CANDIDATE_E_COLD_ASSESSMENT.md

- **N250A-015**, cohort row15, manifest457: [SPECIFICATION.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md). Exact repository path `experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md`; SHA-256 `0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603`; 6,894 bytes. Role: authored_argument.

[N250A-015]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/0455329eb125848dbdb0601e5e75221804355094382cdf20cd004e59dded8603/SPECIFICATION.md

- **N250A-016**, cohort row16, manifest14893: [TRANSPORT_ARGUMENT.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md). Exact repository path `experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md`; SHA-256 `855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1`; 21,081 bytes. Role: authored_argument.

[N250A-016]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/855b8f438e5d5f05b53e2d6ee151375a1601d3e568f53b31316b336f07f3def1/TRANSPORT_ARGUMENT.md

- **N250A-024**, cohort row24, manifest8404: [COVERING_TRADEOFF.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4d5425b42dad562700a7572a84a077dbcf9330de54b10dd6c755df0d10d8fde4/COVERING_TRADEOFF.md). Exact repository path `experiments/orthemology-v5-successors/source-store/4d5425b42dad562700a7572a84a077dbcf9330de54b10dd6c755df0d10d8fde4/COVERING_TRADEOFF.md`; SHA-256 `4d5425b42dad562700a7572a84a077dbcf9330de54b10dd6c755df0d10d8fde4`; 9,259 bytes. Role: authored_argument.

[N250A-024]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/4d5425b42dad562700a7572a84a077dbcf9330de54b10dd6c755df0d10d8fde4/COVERING_TRADEOFF.md

- **N250A-027**, cohort row27, manifest11844: [verify_covering.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6b256ec341909c8848aa48bfe79cd4e0061c0d601db1f5bff87035447f7b6262/verify_covering.py). Exact repository path `experiments/orthemology-v5-successors/source-store/6b256ec341909c8848aa48bfe79cd4e0061c0d601db1f5bff87035447f7b6262/verify_covering.py`; SHA-256 `6b256ec341909c8848aa48bfe79cd4e0061c0d601db1f5bff87035447f7b6262`; 4,295 bytes. Role: authored_code.

[N250A-027]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6b256ec341909c8848aa48bfe79cd4e0061c0d601db1f5bff87035447f7b6262/verify_covering.py

- **N250A-029**, cohort row29, manifest11077: [independent_root_image_checks.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/648e72d299627c267578358b64bbaa9c227fd44fcb13bf9756a6296bdb58a851/independent_root_image_checks.py). Exact repository path `experiments/orthemology-v5-successors/source-store/648e72d299627c267578358b64bbaa9c227fd44fcb13bf9756a6296bdb58a851/independent_root_image_checks.py`; SHA-256 `648e72d299627c267578358b64bbaa9c227fd44fcb13bf9756a6296bdb58a851`; 3,260 bytes. Role: authored_code.

[N250A-029]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/648e72d299627c267578358b64bbaa9c227fd44fcb13bf9756a6296bdb58a851/independent_root_image_checks.py

- **N250A-030**, cohort row30, manifest22315: [verify_attribution.py](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c85728a3e6274ab1f2e37421191baa80d7ada449f4e3c3f6f68d9982c222d93b/verify_attribution.py). Exact repository path `experiments/orthemology-v5-successors/source-store/c85728a3e6274ab1f2e37421191baa80d7ada449f4e3c3f6f68d9982c222d93b/verify_attribution.py`; SHA-256 `c85728a3e6274ab1f2e37421191baa80d7ada449f4e3c3f6f68d9982c222d93b`; 10,325 bytes. Role: authored_code.

[N250A-030]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c85728a3e6274ab1f2e37421191baa80d7ada449f4e3c3f6f68d9982c222d93b/verify_attribution.py



### Exact public bridges for bounded access and source warrant

- **N250A-246**, cohort row 246, manifest 1061: [FRESH_HISTORIES_BOUNDED_OBSERVATION_AND_ORIGINAL_SUPPORT_v4.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09e145f0f1420b81f7852416f4849673126ea60faf249e575d33d4377ecbcbab/FRESH_HISTORIES_BOUNDED_OBSERVATION_AND_ORIGINAL_SUPPORT_v4.md); exact repository path `experiments/orthemology-v5-successors/source-store/09e145f0f1420b81f7852416f4849673126ea60faf249e575d33d4377ecbcbab/FRESH_HISTORIES_BOUNDED_OBSERVATION_AND_ORIGINAL_SUPPORT_v4.md`; SHA-256 `09e145f0f1420b81f7852416f4849673126ea60faf249e575d33d4377ecbcbab`; 27,006 bytes.

[N250A-246]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/09e145f0f1420b81f7852416f4849673126ea60faf249e575d33d4377ecbcbab/FRESH_HISTORIES_BOUNDED_OBSERVATION_AND_ORIGINAL_SUPPORT_v4.md

- **N250A-247**, cohort row 247, manifest 21613: [BOUNDED_ACCESS_AND_DIACHRONIC_COHERENCE_v3.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c24a896b6aa4119bdbbbee92efbbe55c0765745c9b901221f716a06f6e230942/BOUNDED_ACCESS_AND_DIACHRONIC_COHERENCE_v3.md); exact repository path `experiments/orthemology-v5-successors/source-store/c24a896b6aa4119bdbbbee92efbbe55c0765745c9b901221f716a06f6e230942/BOUNDED_ACCESS_AND_DIACHRONIC_COHERENCE_v3.md`; SHA-256 `c24a896b6aa4119bdbbbee92efbbe55c0765745c9b901221f716a06f6e230942`; 31,721 bytes.

[N250A-247]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c24a896b6aa4119bdbbbee92efbbe55c0765745c9b901221f716a06f6e230942/BOUNDED_ACCESS_AND_DIACHRONIC_COHERENCE_v3.md

- **N250A-249**, cohort row 249, manifest 10710: [QUANTITATIVE_AND_CAPTURE_PUBLIC_v1.md](https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6130a832114b87dcdefbdf60841fe8785f62549ee175adf7dbf25670f880430d/QUANTITATIVE_AND_CAPTURE_PUBLIC_v1.md); exact repository path `experiments/orthemology-v5-successors/source-store/6130a832114b87dcdefbdf60841fe8785f62549ee175adf7dbf25670f880430d/QUANTITATIVE_AND_CAPTURE_PUBLIC_v1.md`; SHA-256 `6130a832114b87dcdefbdf60841fe8785f62549ee175adf7dbf25670f880430d`; 9,511 bytes.

[N250A-249]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6130a832114b87dcdefbdf60841fe8785f62549ee175adf7dbf25670f880430d/QUANTITATIVE_AND_CAPTURE_PUBLIC_v1.md

## Exact public sources for the Ninth argument and evidence reconciliation

[N250C-127]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/cdad7bcf0ae847fa3319f164eb7a755a25a51a053982372664b68b92e8beb8a7/INDEPENDENT_REVIEW.md "Next-250 cohort index 127; SHA-256 cdad7bcf0ae847fa3319f164eb7a755a25a51a053982372664b68b92e8beb8a7"
[N250C-128]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/3e2a5c75831131a63a130104c673e49cdb9bb0410a43de4de22b9a73910dbb68/README.md "Next-250 cohort index 128; SHA-256 3e2a5c75831131a63a130104c673e49cdb9bb0410a43de4de22b9a73910dbb68"
[N250C-129]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/b4a5ad9929b7617104eae93884fee9cbfd071b82b090bf30d3b5052e524f4fba/V3_V4_REPLAY_METADATA_DIFF.txt "Next-250 cohort index 129; SHA-256 b4a5ad9929b7617104eae93884fee9cbfd071b82b090bf30d3b5052e524f4fba"
[N250C-130]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/d8b1bc636da5cb56b05801ca3961188a9b3cf04e406f3beb26bea82d5da3ba64/replay_review.py "Next-250 cohort index 130; SHA-256 d8b1bc636da5cb56b05801ca3961188a9b3cf04e406f3beb26bea82d5da3ba64"
[N250C-131]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/144df48b2fdf2371f8a70fe0e6d4363f88ad61af58a516f9ad6101eb6820f969/DEPENDENCY_TRUST.md "Next-250 cohort index 131; SHA-256 144df48b2fdf2371f8a70fe0e6d4363f88ad61af58a516f9ad6101eb6820f969"
[N250C-132]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/d436f50c8e1335b48d694d22636e554fa2388783645e4e5cbf604417ce6a8f34/README.md "Next-250 cohort index 132; SHA-256 d436f50c8e1335b48d694d22636e554fa2388783645e4e5cbf604417ce6a8f34"
[N250C-133]: https://github.com/theislampill/orthemology/blob/542170635a2b01c57d02d1e01eb195c588509dc5/experiments/orthemology-v5-successors/source-store/119fee26d6e3b3a642d03e8fe6af25e7671ac9d06fb0c8954a0bf2f0234e806a/replay.py "Next-250 cohort index 133; SHA-256 119fee26d6e3b3a642d03e8fe6af25e7671ac9d06fb0c8954a0bf2f0234e806a"

[Q250A-000]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/6d83bd91e8b85803150c18da26068d4cd56c6da0fadc453ce268ef0008670b48/INTEGER_TOTAL_REPORT_PROTOCOL_v3.md
[Q250A-001]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md
[Q250A-002]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/438b0f2f0ce979da7293c22f87e16782cfb24a65cc6bbe55222454b3ccaa8b3a/FINITE_FORWARD_INTERVENTIONS_v1.md
[Q250A-003]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/73bdb7a528a145fc409cf7cc6925b6210eda17808ba8e6c918ffd892f61953b8/INDEPENDENT_REVIEW_PUBLIC_v1.md
[Q250A-004]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/32bb7071666b4582b5547d484cafe9d5973dc0aaca7f099380fe6eda613f3c68/OBSERVATION_ROUTE_CLARIFICATION_v1.md
[Q250A-005]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a73f2cac6cb027d65c46ce6923e80bfed72a3591789779b57cc5578cdb359f84/FIVE_STATE_MODEL.md
[Q250A-007]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/8bb522943f659e2f50a97fe8987f48d851a7fc1577f020995ac43dc31ebfe115/MISSING_OUTCOME_ANALYSIS_v1.md
[Q250A-009]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/804583a332db2f52e53c6d112efeda6ee456c94b73ca5131fc7694f09a1e65f6/SPECIALIST_REVIEW_QUESTIONS.md
[Q250A-012]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/15e4d26373bded96f77aeafd0b92f1a7435d46d8811deafc1f4b5d92a57e420b/README.md
[Q250A-013]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/a61800a28a1a7be9415072a949407dfe91085620ddf10d01df0c77219b7a9615/verify_occurrence.py
[Q250A-014]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/5727a43f5207ec7e93aed9b9d6c4a26f83ce3af61bc4041122621bc101d2216d/verify_sense_sources.py
[Q250A-043]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/55f26bac8864c6e3279debaf821d1c714abbcff6f22f5364a654823ae6a61b70/README.md
[Q250A-044]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/cd6f203e2e79f6113de3cef2e4d98926c3f75fe374ca04b3ea73aeee02301a02/fit_bfgs.py
[Q250A-045]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/ebefc609d09bf68296e5a1c5392064effaf4c4d462b82cbb451b1e93340ec376/fit_checked.py
[Q250A-046]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/20110e73fd822e21651064578946cdf910edc493c973953b2c7d1bb74481dd94/reanalyse.py
[Q250A-047]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/41b4c6a14166306b9f593728df115892a3f0a64aa4c153741b9579c14b74270d/requirements.txt
[Q250A-048]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/afb1ba14ecbbf193f07ac81f985be30535abf9771387813e9dbd0bbbfc72fb50/test_package.py
[Q250A-049]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-successors/source-store/7d9a4c8d071e2591c8d4568c88c277ab61834e52df21500a1367efb2ac7e060a/validate.py

[Q250C-084]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7040e104fbb268ae6dea93fbd21f1db8bccc56bd5f04910b9d43c64597d0da74.lean
[Q250C-085]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/24cf86efc439d077f7860aabf90f455d75269130094d94c46bc6734bacc2aaf9.lean
[Q250C-086]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/d1751ecda2c7730b2580575391486f38a40a9ea0e585d90ad12774da9fb33ff8.lean
[Q250C-087]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/06d403f36ee3cb95094a53b4a53eea72810565fc66ac1fb0607fef9b01922a9b.lean
[Q250C-088]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/1547d34d2a53302e070e7a02131f242f9cb1d80f6aa0f96fc478844f630703a3.lean
[Q250C-089]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/48f69898de357b1cce90acfa6d575cf0688fae41821c8376a4a395bea1ba04c8.lean
[Q250C-090]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/987df7f2262b0b2a5e74bd4aee521b3315d61ca97d1e308ef6b10223f20d48f2.lean
[Q250C-091]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/cfcafcc7e1ebcda71370644b4b89c84a9948353e9115ed2e3a7807b78079a97e.lean
[Q250C-092]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/76d70084a57a2beb4b41784b3c93fd248d732b7422055aba2fdafdaf7957f993.lean
[Q250C-093]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/81f3343152589ab4d36d10ccc487f2bbf8c251bd6a2e95cf50826d59fff88da6.lean
[Q250C-094]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f4298061653adc768b292363885e1a7b2213ccb56d17d52376762529d35b2531.lean
[Q250C-095]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/eb29e22c35c3a366d440669da516663f9fe56601794f98ba8dbc81958ab7d5b7.lean
[Q250C-096]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3098f76a8065b9a327a4e9763de88428cd4711c79232b87201b7c079ee7789db.lean
[Q250C-097]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/566f01a571617215b71386917896044a7dc150e84130dcd0f92f36e45038f414.lean
[Q250C-098]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/c497220e36e59578dc8d1efa53bfac17014446fcc84826f3af37f270d9f6e8f3.lean
[Q250C-101]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f7af0f36a68359e8b20b5c85ca527e07191c43686ec345b7d08f582bb4741e24.lean
[Q250C-102]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/71acea2c2028a111c1e15ddc85f76f0dd59efb639f9a0372bc35a320c7f4e3ef.lean
[Q250C-103]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/ad50af371e175b27b62f9fe545267dd434ed256ab84b950afdc92b932dc5fd74.lean
[Q250C-104]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/db9ec6cae92ba47810fd360afa3eda2b4447327378a032b17d87afef743a67c4.lean
[Q250C-105]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3c52bf3ff7d270ef0343f1d41223b3aacc8a748df216d130a580ff338dd94174.lean
[Q250C-106]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/df0a80d810a176bb32b8a5574039115e823bfbeaa588a3ed23a52a7d7aa10a91.lean
[Q250C-107]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/6a52c99c8bfe581ed13dcec6a396dcb7227656e6eba937a4cf73c7e36a8f4100.lean
[Q250C-108]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/bdd551d8c61ae4c78332b957eba7ecab5718747747a51a91902ea55e2306aca9.lean
[Q250C-112]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7b54bfb8cd869bbe72f7ebeb42504a616c216a1912d09a6fc0d2ab35ca9d39c3.lean
[Q250C-113]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/4a93ef96999718cc4fc6ac566da899c6f9938d5a8cbce269d8ee20a3f459d9a3.lean
[Q250C-114]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3c5dc0288543e481971f9ccdbf811102b191fa4067ff65ed1e0e3cd8e0da06b2.lean
[Q250C-115]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2fc036ffd94d213ad5215c447308132dd08edaad19d5f893dd130780382cc146.lean
[Q250C-116]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/2870a3c2d0dd125a59b49600e0fa0853e8d5c46a98153f27846a9f43f860bea5.lean
[Q250C-118]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/1792831c1af1628fae2c31b821f40d6d3a67be22303595f66ca14d273223228a.lean
[Q250C-119]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/ff7c13f5212d6b5f9cfdf64979e664e51934422189528d6169b8a72c57cfff56.lean
[Q250C-120]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/17793ba9787eb9c3fc1618d4acfc368804be8309197156f22d440508f8ad22a0.lean
[Q250C-121]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/5de3075faa5e7041d31cb7c18868c0a91db7ef8d47a0630d26cb63dfcd6dd60b.lean
[Q250C-122]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/feef9755524c9f08ad782339f0c60cbbd5c82391d992b48d59d30e191b1da17e.lean
[Q250C-123]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/f163f76a1fdab9b12bd96122780339901fcb76b5a3c75cdec56b8d3d505e32dd.lean
[Q250C-124]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/97e0f881af3140b625d45642c06cecc20dbb49773528f8345dd4c948b1ddfc68.lean
[Q250C-125]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/7d828069e42926c9e7acb36bfb683a6b3bd8c6f46907d00ccd8c643e27555c04.lean
[Q250C-126]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/adc48e40e89c35782be3f30eafb0a62bb6100de48bf853a84e081631da8092e0.lean
[Q250C-127]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/6c281b2bc6036789a0d342a14df80b1d9c68bcbdf49a1720855d3cd03a46e499.lean
[Q250C-128]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/3fd4a3d8e4a7a2c74343087c8f3a31714b569ff209b3d63b9764f70c2462fe25.lean
[Q250C-129]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/90ba0fd6a17d86323b83185acd96a639fe584407d2496dad678aed08bc74717e.lean
[Q250C-130]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/9814025d9195fe98c7df8a8839fd37b8696f0b61d3970cb3dd61cb257a0009f1.lean
[Q250C-131]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/e38e3a972bbdf859b854b42c44a7cbf4d83c0f5b2fb7566d2f726f155572bfee.lean
[Q250C-132]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/1dc8c0e40a86a205498af32bd7c4a0d96afca6020f2fbd321e21fae2beee0077.lean
[Q250C-133]: https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/experiments/orthemology-v5-continuations/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183.lean
