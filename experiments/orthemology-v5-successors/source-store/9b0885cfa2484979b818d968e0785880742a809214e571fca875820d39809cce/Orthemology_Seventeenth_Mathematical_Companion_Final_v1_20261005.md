> **DERIVED public reading projection.** Original DOCX `Orthemology_Seventeenth_Mathematical_Companion_Final_v1_20261005.docx`; original SHA-256 `764c038e4cd2febb74c23e19c15cc86f6377c65f376964b3a33512a7ac83cf89`. This projection was prepared on 7 October 2026. Original authored text order, link destinations, native mathematics, AI attribution, dates, and scope limitations are retained. Research, reading, review, and verification claims below remain the source’s dated claims, not fresh acceptance or replication. Internal page references name the original DOCX pagination; Markdown has no matching page numbers. Where present, native equations are rendered as TeX with an exact source-to-projection map and declared spacing and prime-glyph normalization. Word typography, pagination, and dynamic page-number fields are not reproduced.

# Orthemology Seventeenth Mathematical Companion

Prepared by dot, an AI assistant powered by OpenAI

5 October 2026

# 1 Finite inference under assignment uncertainty

This companion develops a finite probability contract for a weighted binary-assignment statistic. It answers three questions: which assignment information makes an observed extreme value meaningful, how to bound its probability when assignments may depend on earlier assignments, and how to keep numerical approximations conservative. It contains ordinary written proofs and synthetic counterexamples. It does not establish any real experiment’s assignment mechanism, and it makes no claim of new historical ownership for classical randomisation, dynamic programming or concentration arguments.

The central distinction is simple. Knowing that each coin is individually fair does not say how all the coins move together. If they can move as one coordinated pattern or its opposite, an absolute weighted total can be constant. Bounds on the next coin’s probability after every preceding pattern provide stronger information. They allow an exact finite recursion and scalable conservative bounds, while still allowing dependence.

The second distinction concerns the response. A no-effect hypothesis can make the response schedule fixed while assignments are varied. It cannot turn a merely marginal assignment distribution into random assignment relative to that schedule. The assignment relation and the sharp no-effect hypothesis are separate premises.

The mathematics below retains these premises throughout. The quantitative outputs are upper probability bounds under specified model families. A large bound is not evidence that the no-effect hypothesis is true; a small bound challenges it only together with the maintained assignment and measurement assumptions.

# 2 The finite experiment and conditioning contract

There are $N$ binary placement coordinates in a specified total order. Write $Z_{i}\text{=}1$ for the positive assignment and $Z_{i}\text{=}0$ for the negative assignment, and $A_{i}\text{=}2Z_{i}\text{−}1\text{.}$ The full assignment is $z$ in a specified set $\Omega\text{⊆}\text{\{}0\text{,}1\text{\}}^{N}\text{.}$ Unless additional restrictions are stated, $\Omega$ is the full cube. The order is part of the model: a probability conditional on previous rounds for one participant is not automatically a probability conditional on every earlier coordinate in a participant-by-round ordering.

Let $X$ denote inputs legitimately fixed by the experiment/conditioning contract. Possible components include task items, complete cue content and polarity schedules, source identities, treatment assignments, group membership, and exogenous baseline data. Their inclusion is a requirement to be justified, not an automatic consequence of their being present in a dataset. In particular, a cue presented before its own response need not have been fixed before earlier placements. A future adaptive cue, feedback value, or knowledge report cannot be silently treated as a baseline covariate.

Let $u$ describe a fixed experimental world: the units, exogenous states and potential response process relevant to this finite experiment. The randomisation draws generating placement are excluded from $u\text{;}$ they remain random under the assignment law. For each admissible full array $z\text{,}$ let $W_{u}\text{(}z\text{)}$ be the complete recorded response trajectory, including availability $R_{i}\text{(}z\text{)}\text{,}$ every recorded response $F_{i}\text{(}z\text{)}\text{,}$ and any additional outcome-derived variables used by the statistic or its analysis rule. Potential responses may depend on earlier assignments, other participants’ assignments, feedback, common cues and treatment. No no-carryover or no-interference assumption is imposed.

The sharp full-trajectory null is

$$H_{0}\text{:}\quad W_{u}\text{(}z\text{)}\text{=}w_{u}\quad \text{for every }z\text{∈}\Omega\text{.}\quad\quad \text{(2.1)}$$

This is a statement about the whole trajectory, not merely $\text{𝔼}\text{[}F_{i}\text{(}1\text{)}\text{−}F_{i}\text{(}0\text{)}\text{]}\text{=}0\text{,}$ a zero regression coefficient, or absence of a same-round direct effect. It must cover availability whenever unavailable responses are encoded or observations are selected by availability. It must cover every outcome-dependent ingredient held fixed during reference assignment calculations. It does not require feedback itself to be invariant if feedback is not fixed or used in an unjustified conditioning step; rather, it says the resulting recorded response trajectory is invariant even allowing the intervention’s downstream feedback consequences.

An assignment contract supplies a law $Q_{X\text{,}u}$ for $Z\text{,}$ or a set of possible such laws, conditional on the legitimate fixed inputs and fixed experimental world. Usual randomised-design reasoning provides a law not depending on $u$ beyond allowed design inputs. A weaker sufficient condition for the robust results is that, for every relevant $u$ under $H_{0}\text{,}$ $Q_{X\text{,}u}$ belongs to the declared family. A claim only about the marginal law $Q\text{(}Z\text{∣}X\text{)}\text{,}$ averaged over a possibly assignment-associated $u\text{,}$ is not sufficient for freezing $w_{u}\text{.}$

For a sequential physical experiment, the same point can be expressed using exogenous randomisation and a specified history: the required probability bounds must hold conditional on the fixed potential-response schedule and every assignment prefix relevant to the model. Bounds conditional on a larger legitimate history imply bounds conditional on a smaller one by averaging when the endpoints are deterministic functions of the retained information. Conditioning additionally on a future observed variable does not follow from this averaging argument.

## 2.1 Why both parts of the contract are indispensable

Here is a finite counterexample with no placement effect. Let $U_{i}$ be independent fair signs. Set the response under every intervention to $W_{i}\text{(}z\text{)}\text{=}U_{i}\text{,}$ so the sharp null is true. Now let the observational assignment be $A_{i}\text{=}U_{i}\text{.}$ Marginally, the assignment array is a product of fair signs. Nevertheless, with fixed observed weights $a_{i}\text{=}W_{i}\text{,}$ the observed sum is always $N\text{.}$ A reference calculation that freezes those weights and substitutes independent fair $A_{i}$ gives two-sided probability $2^{1\text{−}N}\text{,}$ for $N$ at least one. For $N\text{=}6$ it rejects at level $.05$ on every experimental world. The error is not the sharp null; it is treating the marginal assignment law as a randomised law conditional on the potential responses.

A related conditioning error begins with genuine independent randomisation $A_{i}$ independent of $U_{i}\text{,}$ and the same invariant response $W_{i}\text{(}z\text{)}\text{=}U_{i}\text{.}$ Define a post-assignment variable $C_{i}\text{=}\text{𝟏}\text{\{}A_{i}\text{=}U_{i}\text{\}}\text{.}$ Conditional on $C_{i}\text{=}1\text{,}$ $A_{i}$ and the response agree deterministically. Keeping the fair unconditional reference law after selecting or conditioning on $C_{i}$ produces the wrong test. A correct conditional design calculation would have to account for the selection event and the experimental world; the unconditional coin law is no longer the claimed conditional law.

These are synthetic examples. They distinguish a marginal distribution from the conditional assignment relation required by a fixed-response reference calculation; they are not evidence about any actual experiment.

# 3 A fully specified candidate weighted statistic

The following defines a generic finite-response statistic. A scientific application must select its population, response validation and weighting before inspecting the assignment-response relation. No actual observations are used here.

Let $E_{i}$ be a binary eligibility indicator supplied by legitimate fixed inputs. Let $B_{i}$ be a signed recorded response in $\text{[}\text{−}1\text{,}1\text{]}$ when a response is available. Let $R_{i}$ indicate availability under a predeclared validation rule. Define $Y_{i}\text{=}R_{i}B_{i}$ by cases: $Y_{i}\text{=}B_{i}$ when $R_{i}\text{=}1$ and $Y_{i}\text{=}0$ otherwise. No unobserved $B_{i}$ is imputed. The zero contribution of an unavailable response means no recorded directional contribution; it does not mean that a neutral response was observed.

Eligibility must be invariant under the assignment intervention, or covered by an adequate conditional model. A rule measured before its own response is not automatically fixed with respect to earlier assignments. These conditions are requirements of the mathematical application, not conclusions from the notation.

For each group $g\text{,}$ let $n_{g}\text{=}\sum_{i\text{:}g\text{(}i\text{)}\text{=}g}^{}E_{i}$ over its prespecified member-round coordinates. Let $G_{\text{+}}$ be the number of groups with $n_{g}\text{>}0\text{.}$ If $G_{\text{+}}\text{=}0\text{,}$ the selected statistic has no eligible population and no test is defined. Otherwise put

$$\begin{matrix}
c_{i} & \text{=}\frac{E_{i}}{G_{\text{+}}n_{g\text{(}i\text{)}}}\quad \text{if }n_{g\text{(}i\text{)}}\text{>}0\text{,} \\
c_{i} & \text{=}0\quad \text{if }n_{g\text{(}i\text{)}}\text{=}0\text{,} \\
a_{i} & \text{=}c_{i}Y_{i}\text{,} \\
S\text{(}z\text{;}w\text{,}X\text{)} & \text{=}\sum_{i\text{=}1}^{N}a_{i}\text{(}2z_{i}\text{−}1\text{)}\text{,} \\
T\text{(}z\text{;}w\text{,}X\text{)} & \text{=}\text{|}S\text{(}z\text{;}w\text{,}X\text{)}\text{|}\text{.}
\end{matrix}\quad\quad \text{(3.1)}$$

Groups are equally weighted; eligible member-rounds within a group are equally weighted. The denominator never depends on whether a response is available. Thus $\sum_{i}^{}c_{i}\text{=}1$ and $\text{|}S\text{|}\text{≤}\sum_{i}^{}{\text{|}a_{i}\text{|}}\text{≤}1\text{.}$ Other participant/group weightings are possible, but their denominators and target population must be stated rather than changed after looking at results.

The product $A_{i}B_{i}$ is a signed assignment-response alignment. Its sign does not identify a hidden generating mechanism. Negative $a_{i}$ are allowed; the probability results below do not require response weights to be positive.

Under $H_{0}$ and the assignment contract, $a_{i}\text{=}a_{i}\text{(}w_{u}\text{,}X\text{)}$ are fixed numbers when assignments are varied. The weights need not have arisen from independent outcomes. Observed response-derived weights could, mathematically, be chosen by an assignment-invariant rule under $H_{0}\text{;}$ prospective declaration is still required here to avoid an undisclosed search over questions, transformations or subgroups. A rule that depends directly on the observed placements must instead be rerun for every reference array and incorporated into the statistic. Holding its chosen output fixed would not implement the same test.

Availability deserves its own predeclared diagnostic, for example $S_{R}\text{(}z\text{)}\text{=}\sum_{i}^{}c_{i}R_{i}\text{(}2z_{i}\text{−}1\text{)}\text{.}$ A zero-aligned-evidence statistic can miss placement effects consisting only of availability changes or cancellations. If both statistics can trigger an inferential rejection, predeclare a joint randomisation statistic or an error allocation such as a Bonferroni split. Calling a second test a diagnostic does not remove multiplicity. Purely descriptive reporting can be identified as such.

Treatment is held fixed only under a valid conditional placement law given treatment. Subgroups, selected time windows, transformations and interactions require their own predeclared inferential treatment. A rejection concerning placement does not identify an effect of another intervention.

## 3.1 Fixed opportunity weighting

An alternative target retains every scheduled opportunity in its denominator. Suppose there are $K$ groups, group $g$ has a fixed roster of $m_{g}$ members, and every member has $J$ scheduled questions. With the same eligibility indicator $E_{i}$ and recorded evidence $Y_{i}$ as above, define

$$c_{i}\text{=}\frac{E_{i}}{Km_{g\text{(}i\text{)}}J}\text{,}\quad\quad a_{i}\text{=}c_{i}Y_{i}\text{.}\quad\quad \text{(3.2)}$$

The scheduled question count $J$ is distinct from the availability indicator $R_{i}\text{.}$ All groups remain in the population, including groups with no eligible opportunities or no recorded directional evidence. The total opportunity weight per group is $1\text{/}K\text{,}$ while its total eligible weight can be smaller. Thus, with $H_{E}\text{=}\sum_{i}^{}c_{i}\text{,}$

$$\text{|}S\text{(}z\text{)}\text{|}\text{≤}\sum_{i\text{=}1}^{N}{\text{|}a_{i}\text{|}}\text{≤}H_{E}\text{≤}1\text{.}\quad\quad \text{(3.3)}$$

This target differs from the equally weighted mean of group-specific means among eligible opportunities. It must not inherit that target’s normalisation silently. Both constructions yield fixed real coefficients under the specified sharp null and assignment contract, so every probability result below applies to either. Fixed exported or observed membership is not automatically intervention-invariant: that fact, or an adequate conditional law for it, remains an application premise.

# 4 Declared assignment models and their different warrants

The following are different hypotheses about the design, not interchangeable approximations.

- Known joint law. $Q\text{(}z\text{∣}X\text{,}u\text{)}$ is specified on $\Omega$ and applicable to the retained experimental units. Direct summation, exact state computation or a valid Monte Carlo rank procedure can produce a reference test.
- Fair marginal law. Each $Q\text{(}Z_{i}\text{=}1\text{∣}X\text{,}u\text{)}\text{=}1\text{/}2\text{,}$ with arbitrary dependence. This does not specify conditional probabilities after previous assignments and gives the two-sided impossibility in Section 6 when the support allows complements.
- Rectangular sequential interval law. For every positive-probability prefix $h$ in a specified order, $\text{ℓ}_{i}\text{(}h\text{)}\text{≤}Q\text{(}Z_{i}\text{=}1\text{∣}Z_{\text{<}i}\text{=}h\text{,}X\text{,}u\text{)}\text{≤}u_{i}\text{(}h\text{)}\text{,}$ with known $0\text{≤}\text{ℓ}_{i}\text{(}h\text{)}\text{≤}u_{i}\text{(}h\text{)}\text{≤}1\text{.}$ All kernels satisfying these restrictions are allowed. This is the sharp recursion model in Section 7.
- Independently assigned coordinates with unknown biases. $Q$ is a product law, with $p_{i}$ in specified intervals. This is a smaller family than the sequential interval family. A general event probability is multiaffine in the separate $p_{i}\text{,}$ so a maximum over a rectangular box occurs at some vertex, but there may be $2^{N}$ vertices. A common unknown $p$ across coordinates is another restriction and does not follow this separate-coordinate endpoint argument.
- Known blocking, balancing, permutation or shared-coin law. Such a design can be analysed on its actual support and joint law, sometimes very efficiently. It must be documented. It does not follow from observed totals, repeated vectors or a general statement that placement was random.
- Unspecified randomised placement. No numerical bounds, probabilities or support symmetries are known. This description alone does not specify a numerical reference distribution.

A stipulated model can support a conditional sensitivity statement, explicitly beginning “if the assignment mechanism satisfies …”. It is not retrospectively upgraded into a recovered design fact. A single observed complete array cannot warrant arbitrary-prefix probability bounds merely through its frequencies. Statistical estimation under a separately justified repeated-draw model is a different task; assuming that model to estimate its own independence premise would be circular.

# 5 Finite reference probabilities and validity

Fix $X\text{,}$$u$ satisfying $H_{0}\text{,}$ suppress these arguments, and let $T$ be the fixed statistic on $\Omega\text{.}$ For a known law $Q$ define the inclusive tail function and $p$-value

$$\begin{matrix}
r_{Q}\text{(}t\text{)} & \text{=}Q\text{\{}T\text{(}Z\text{)}\text{≥}t\text{\}}\text{,} \\
p_{Q}\text{(}z\text{)} & \text{=}r_{Q}\text{(}T\text{(}z\text{)}\text{)}\text{.}
\end{matrix}\quad\quad \text{(5.1)}$$

Inclusive ties are essential to this simple nonrandomised validity statement. A strict tail or a mid-$p$ adjustment is not automatically a level-valid $p$-value. For any $\alpha\text{∈}\text{[}0\text{,}1\text{]}\text{,}$

$$Q\text{\{}p_{Q}\text{(}Z\text{)}\text{≤}\alpha\text{\}}\text{≤}\alpha\text{.}\quad\quad \text{(5.2)}$$

Proof. There are finitely many distinct statistic values. If none has upper-tail mass at most $\alpha\text{,}$ the rejection event is empty. Otherwise let $t_{\text{*}}$ be the smallest such value. Since the upper-tail function is nonincreasing, the rejection event is exactly $\text{\{}T\text{≥}t_{\text{*}}\text{\}}\text{,}$ whose $Q$ probability is at most $\alpha\text{.}$ This also covers zero-probability statistic values by restricting to the support. End proof.

For a declared nonempty family $\text{𝒬}$ containing the actual conditional law, define

$$\begin{matrix}
r_{\text{*}}\text{(}t\text{)} & \text{=}\underset{Q\text{∈}\text{𝒬}}{\text{sup}}Q\text{\{}T\text{(}Z\text{)}\text{≥}t\text{\}}\text{,} \\
p_{\text{*}}\text{(}z\text{)} & \text{=}r_{\text{*}}\text{(}T\text{(}z\text{)}\text{)}\text{.}
\end{matrix}\quad\quad \text{(5.3)}$$

Then $p_{\text{*}}\text{(}z\text{)}\text{≥}p_{Q_{0}}\text{(}z\text{)}$ for the actual $Q_{0}\text{.}$ Consequently

$$Q_{0}\text{\{}p_{\text{*}}\text{(}Z\text{)}\text{≤}\alpha\text{\}}\text{≤}Q_{0}\text{\{}p_{Q_{0}}\text{(}Z\text{)}\text{≤}\alpha\text{\}}\text{≤}\alpha\text{.}\quad\quad \text{(5.4)}$$

This is finite-sample validity, uniform over the declared family, conditional on the fixed experimental world. Averaging over such worlds preserves the inequality when the contract holds in every world under the null. Taking the supremum separately at each observed threshold does not invalidate the test; pointwise domination is the reason. The maximising law need not be the actual law and may differ between thresholds.

Any certified upper bound $U\text{(}t\text{)}\text{≥}r_{\text{*}}\text{(}t\text{)}$ gives an equally valid, possibly more conservative $p$-value $\text{min}\text{\{}1\text{,}U\text{(}T\text{(}z\text{)}\text{)}\text{\}}\text{.}$ An algorithm that merely finds one admissible law supplies a lower bound on $r_{\text{*}}\text{,}$ which has the wrong direction for this purpose. A large approximate search is not a certificate of a global upper bound.

Attribution of a rejection to placement noninvariance is conditional on the maintained assignment, linkage and measurement contract. Formally the test controls rejection of the sharp null under that contract. If the contract is only a speculative model, the result challenges the conjunction, not the null in isolation. Nonrejection proves neither invariance nor absence of source use.

# 6 Fair marginals alone make this two sided test vacuous

Proposition. Suppose $\Omega$ contains $z$ and its bitwise complement $z^{\text{c}}$ for every possible observation $z\text{,}$ and $\text{𝒬}$ includes every fair-marginal law on $\Omega\text{.}$ Let $S\text{(}z\text{)}\text{=}\sum_{i}^{}a_{i}\text{(}2z_{i}\text{−}1\text{)}$ with fixed real weights, and $T\text{(}z\text{)}\text{=}\text{|}S\text{(}z\text{)}\text{|}\text{.}$ Then $p_{\text{*}}\text{(}z\text{)}\text{=}1$ for every $z\text{.}$

Proof. For the particular observed $z\text{,}$ define $Q_{z}$ to assign mass $1\text{/}2$ to $z$ and mass $1\text{/}2$ to $z^{\text{c}}\text{.}$ Each coordinate is one in exactly one of these arrays, so $Q_{z}$ has fair marginals. Also $S\text{(}z^{\text{c}}\text{)}\text{=}\text{−}S\text{(}z\text{)}\text{,}$ hence $T\text{(}z^{\text{c}}\text{)}\text{=}T\text{(}z\text{)}\text{.}$ Both support points satisfy the inclusive tail event at the observed threshold. Therefore $r_{Q_{z}}\text{(}T\text{(}z\text{)}\text{)}\text{=}1\text{,}$ and no probability can exceed one. End proof.

The same construction works for any complement-invariant extremeness statistic. It does not require equal weights, positive weights, independent participants, or a particular observed array. A conventional doubled smaller one-sided $p$-value is also one for this pair law, with the usual cap at one.

$Q_{z}$ is chosen after fixing $z$ only as a member witnessing the pointwise supremum over the previously declared family. It is not an assertion about the actual generator, a fitted estimate of its law, or a claim that every admissible law is equally plausible. Section 5 explains why this pointwise worst-case calculation still gives a valid robust $p$-value.

Qualitative strict positivity without numerical bounds does not rescue the test on the full cube. Let $U$ be the uniform law on the cube and take $Q_{\varepsilon}\text{=}\text{(}1\text{−}\varepsilon\text{)}Q_{z}\text{+}\varepsilon U$ for $0\text{<}\varepsilon\text{<}1\text{.}$ It has fair marginals, full support, and strictly interior conditional branch probabilities at every prefix. Its tail probability is at least $1\text{−}\varepsilon$ and tends to one. Thus the supremum is still one even if the exact two-point law is excluded. If the tail event is proper, full support prevents attainment of one; the conclusion is then a supremum, not a maximising law. This extension uses the full-cube support and must not be transferred to an arbitrary restricted support without a corresponding construction.

This is not a theorem that every possible test under every fair-marginal model is useless. A prespecified one-sided event is not complement-invariant, and additional support or independence restrictions can rule out the construction. The one-sided distinction does not offer a conventional-level rescue under the present family: for an inclusive signed upper tail at the observed $S\text{(}z\text{)}\text{,}$ the pair law gives probability $1\text{/}2$ when $S\text{(}z\text{)}\text{>}0$ and probability one when $S\text{(}z\text{)}\text{≤}0\text{.}$ Its robust one-sided $p$-value therefore cannot reject at a level below $1\text{/}2\text{.}$ The exact probability-one proposition above concerns the ordinary two-sided linear-alignment statistic under the stated family. If a documented support is not closed under complements, the proposition must not be applied without checking it.

With no marginal restrictions at all, the point mass at the observed array gives the same upper-tail conclusion even more directly. Saying only that some randomness was used, without quantitative constraints, does not repair the numerical inference gate.

# 7 Sharp recursion for sequential interval bounds

## 7.1 The family and the finite recursion

At each prefix $h$ of length $i\text{−}1\text{,}$ let $\text{[}\text{ℓ}_{i}\text{(}h\text{)}\text{,}u_{i}\text{(}h\text{)}\text{]}$ be a specified nonempty closed interval. A kernel policy $q$ chooses $q_{i}\text{(}h\text{)}$ in that interval. It induces the full-array law

$$\begin{matrix}
b_{i}\text{(}z\text{)} & \text{=}q_{i}\text{(}z_{\text{<}i}\text{)}\quad \text{if }z_{i}\text{=}1\text{,} \\
b_{i}\text{(}z\text{)} & \text{=}1\text{−}q_{i}\text{(}z_{\text{<}i}\text{)}\quad \text{if }z_{i}\text{=}0\text{,} \\
Q_{q}\text{(}z\text{)} & \text{=}\prod_{i\text{=}1}^{N}b_{i}\text{(}z\text{)}\text{.}
\end{matrix}\quad\quad \text{(7.1)}$$

The piecewise factor selects the realised branch probability and avoids an ambiguous $0^{0}$ convention. Conditional restrictions are substantive only at reached histories; assigning an arbitrary admissible kernel at an unreachable history has no effect on the law. Let $\text{𝒬}_{\text{rect}}$ be the laws generated by all such policies. Choices at distinct histories are otherwise unconstrained. This last “rectangularity” condition is important to sharpness.

For a threshold $t\text{,}$ set

$$V_{N}\text{(}z\text{)}\text{=}\text{𝟏}\text{\{}\text{|}\sum_{i\text{=}1}^{N}a_{i}\text{(}2z_{i}\text{−}1\text{)}\text{|}\text{≥}t\text{\}}\text{.}\quad\quad \text{(7.2)}$$

Working backwards, at a prefix $h$ of length $i\text{−}1$ put

$$\begin{array}{r}
v_{0}\text{=}V_{i}\text{(}h\text{,}0\text{)}\text{,}\quad\quad v_{1}\text{=}V_{i}\text{(}h\text{,}1\text{)}\text{,} \\
V_{i\text{−}1}\text{(}h\text{)}\text{=}\underset{q\text{∈}\text{[}\text{ℓ}_{i}\text{(}h\text{)}\text{,}u_{i}\text{(}h\text{)}\text{]}}{\text{max}}\text{\{}\text{(}1\text{−}q\text{)}v_{0}\text{+}qv_{1}\text{\}} \\
\text{=}v_{0}\text{+}\text{max}\text{\{}\text{ℓ}_{i}\text{(}h\text{)}\text{(}v_{1}\text{−}v_{0}\text{)}\text{,}u_{i}\text{(}h\text{)}\text{(}v_{1}\text{−}v_{0}\text{)}\text{\}}\text{.}
\end{array}\quad\quad \text{(7.3)}$$

Then

$$V_{0}\text{(}\text{⌀}\text{)}\text{=}\underset{Q\text{∈}\text{𝒬}_{\text{rect}}}{\text{max}}Q\text{\{}\text{|}S\text{|}\text{≥}t\text{\}}\text{.}\quad\quad \text{(7.4)}$$

Proof by backward induction. At a final prefix the terminal value is the exact event indicator. At an earlier prefix, any admissible continuation first chooses a feasible branch probability $q\text{;}$ conditional success on each branch is at most that branch’s induction value. This proves the displayed maximum is an upper bound. The objective is linear in $q\text{,}$ so choose $u_{i}\text{(}h\text{)}$ when $v_{1}\text{>}v_{0}\text{,}$ $\text{ℓ}_{i}\text{(}h\text{)}$ when $v_{1}\text{<}v_{0}\text{,}$ and either endpoint when equal. By induction there are optimal continuation policies in both subtrees. Rectangularity allows their simultaneous use under the chosen $q\text{.}$ Combining them attains the bound. Repeating to the root proves equality and existence of an optimising endpoint policy. End proof.

Thus the exact maximiser is allowed to favour different sides after different histories. Such conditional kernels are also a chain-rule representation of a precomputed correlated array. Their mathematical dependence on history does not establish that the historical generator ran online, consulted feedback, or adaptively reacted to participants. This is ordinary finite-horizon dynamic programming; the proof does not invoke iid assignments or outcomes.

## 7.2 Equivalent finite linear program

Assign a nonnegative mass $x\text{(}h\text{)}$ to every prefix, with $x\text{(}\text{⌀}\text{)}\text{=}1$ and $x\text{(}h\text{)}\text{=}x\text{(}h\text{,}0\text{)}\text{+}x\text{(}h\text{,}1\text{)}\text{.}$ Impose

$$\text{ℓ}_{i}\text{(}h\text{)}x\text{(}h\text{)}\text{≤}x\text{(}h\text{,}1\text{)}\text{≤}u_{i}\text{(}h\text{)}x\text{(}h\text{)}\text{.}\quad\quad \text{(7.5)}$$

Maximise sum of $x\text{(}z\text{)}$ over terminal arrays in the tail event. These constraints are linear, including when $x\text{(}h\text{)}\text{=}0\text{.}$ Positive prefix masses recover $q_{i}\text{(}h\text{)}\text{=}x\text{(}h\text{,}1\text{)}\text{/}x\text{(}h\text{)}\text{;}$ zero-mass prefixes can be completed arbitrarily. The feasible leaf masses are exactly $\text{𝒬}_{\text{rect}}\text{,}$ so the linear program has the same optimum as the recursion.

Additional restrictions linking different histories, such as fair marginals, common bias parameters, exchangeability, or an exact global balance requirement, can change the feasible family. Some can be added as linear constraints on leaf masses; independence or a common product parameter is not automatically a linear constraint. The unaugmented Bellman recursion remains an upper bound for any smaller family but need not be sharp for it. Rectangularising a family is a conservative enlargement, not proof that all resulting policies are actual possible designs.

The bounds must cover every relevant prefix, or a specified conservative envelope of all of them. Knowing the numerical propensity only on the single observed path does not supply a full reference distribution. Filling unobserved branches with $\text{[}0\text{,}1\text{]}$ is a valid enlargement only if that is explicitly the intended family; its result may be uninformative.

## 7.3 State compression and its limits

If the bounds depend only on the coordinate $i\text{,}$ and the statistic is a fixed weighted sum, the partial sum $s$ is a sufficient state for optimisation. With $J_{N\text{+}1}\text{(}s\text{)}\text{=}\text{𝟏}\text{\{}\text{|}s\text{|}\text{≥}t\text{\}}\text{,}$

$$J_{i}\text{(}s\text{)}\text{=}\underset{q\text{∈}\text{[}\text{ℓ}_{i}\text{,}u_{i}\text{]}}{\text{max}}\text{\{}\text{(}1\text{−}q\text{)}J_{i\text{+}1}\text{(}s\text{−}a_{i}\text{)}\text{+}qJ_{i\text{+}1}\text{(}s\text{+}a_{i}\text{)}\text{\}}\text{.}\quad\quad \text{(7.6)}$$

Evaluate $J_{1}\text{(}0\text{)}\text{.}$ The maximising $q$ still depends on $s\text{.}$ If bounds or future allowed actions depend on additional state, that state must be retained. If they depend on the whole prefix, merging histories merely because they have the same partial sum can give the wrong answer. A finite sufficient state may include remaining balance counts, block state or other documented generator state.

Dropping zero-weight or ineligible coordinates is harmless for this deterministic-coordinate-bound model after averaging over omitted history: the retained conditional probabilities remain within the same deterministic bounds. It is not automatically harmless for history-dependent bounds, support constraints, or a known coupled design. In those cases the omitted coordinates can carry relevant assignment state even though they contribute zero to $S\text{.}$

# 8 A smallest counterexample to a fixed product worst case

Take $N\text{=}2\text{,}$ $a_{1}\text{=}a_{2}\text{=}1$ and $t\text{=}2\text{.}$ At every history, require the probability of a plus sign to lie in $\text{[}1\text{/}4\text{,}3\text{/}4\text{]}\text{.}$ The event $\text{|}A_{1}\text{+}A_{2}\text{|}\text{≥}2$ is exactly the event that the signs match.

Use $\text{Pr}\text{(}A_{1}\text{=}\text{+}1\text{)}\text{=}1\text{/}2\text{,}$ then

$$\begin{matrix}
\text{Pr}\text{(}A_{2}\text{=}\text{+}1\text{∣}A_{1}\text{=}\text{+}1\text{)} & \text{=}\frac{3}{4}\text{,} \\
\text{Pr}\text{(}A_{2}\text{=}\text{+}1\text{∣}A_{1}\text{=}\text{−}1\text{)} & \text{=}\frac{1}{4}\text{.}
\end{matrix}\quad\quad \text{(8.1)}$$

The four probabilities for $\text{(}\text{+}\text{+}\text{,}\text{+}\text{−}\text{,}\text{−}\text{+}\text{,}\text{−}\text{−}\text{)}$ are $\text{(}3\text{/}8\text{,}1\text{/}8\text{,}1\text{/}8\text{,}3\text{/}8\text{)}\text{.}$ Both signs have fair marginals, and the tail probability is $3\text{/}4\text{.}$ Bellman optimality is immediate: after either first sign, the matching probability is at most $3\text{/}4\text{,}$ and the chosen kernel reaches it.

For an independent product law with $p_{1}\text{,}p_{2}$ in $\text{[}1\text{/}4\text{,}3\text{/}4\text{]}\text{,}$ the matching probability is

$$p_{1}p_{2}\text{+}\text{(}1\text{−}p_{1}\text{)}\text{(}1\text{−}p_{2}\text{)}\text{.}\quad\quad \text{(8.2)}$$

It is affine in each coordinate separately, so its maximum is at a box corner. The four corner values are $5\text{/}8\text{,}3\text{/}8\text{,}3\text{/}8\text{,}5\text{/}8\text{.}$ Hence even the best independent coordinate-specific product law has probability only $5\text{/}8\text{.}$ The adaptive optimum is strictly larger, $3\text{/}4\text{.}$

The same example shows why centring at the unconditional expectation cannot replace a martingale or conditional-drift argument. Here $\text{𝔼}\text{[}S\text{]}\text{=}0$ and each increment has magnitude one. Nevertheless

$$\text{Pr}\text{(}\text{|}S\text{−}\text{𝔼}\text{[}S\text{]}\text{|}\text{≥}2\text{)}\text{=}\frac{3}{4}\text{>}2\text{exp}\text{(}\text{−}1\text{)}\text{,}\quad\quad \text{(8.3)}$$

so the familiar unadjusted independent-sign two-sided exponential bound is false for this dependent array. The corrected bound in Section 10 includes the allowed conditional drift.

Even within a common-bias independent model, one cannot mechanically maximise a nonmonotone event at the common parameter’s interval endpoints. For $a_{1}\text{=}1\text{,}$ $a_{2}\text{=}\text{−}1$ and $t\text{=}2\text{,}$ the event is disagreement of the underlying plus signs. Under iid $\text{Bernoulli}\text{(}p\text{)}\text{,}$ its probability is $2p\text{(}1\text{−}p\text{)}\text{,}$ maximised at $p\text{=}1\text{/}2\text{,}$ not at either endpoint of $\text{[}1\text{/}4\text{,}3\text{/}4\text{]}\text{.}$ This is a different counterexample concerning a shared parameter; it does not contradict multiaffinity in separately free coordinate parameters.

# 9 Directed tails have exact endpoint product optimisers

Assume now deterministic coordinatewise bounds $\text{[}\text{ℓ}_{i}\text{,}u_{i}\text{]}\text{,}$ without cross-history restrictions. Write $w_{i}\text{=}\text{|}a_{i}\text{|}\text{.}$ For $a_{i}$ nonnegative put $X_{i}\text{=}A_{i}\text{,}$ $\alpha_{i}\text{=}\text{ℓ}_{i}$ and $\beta_{i}\text{=}u_{i}\text{.}$ For $a_{i}$ negative put $X_{i}\text{=}\text{−}A_{i}\text{,}$ $\alpha_{i}\text{=}1\text{−}u_{i}$ and $\beta_{i}\text{=}1\text{−}\text{ℓ}_{i}\text{.}$ Then $S\text{=}\sum_{i}^{}w_{i}X_{i}$ and

$$\alpha_{i}\text{≤}\text{Pr}\text{(}X_{i}\text{=}\text{+}1\text{∣}Z_{\text{<}i}\text{)}\text{≤}\beta_{i}\text{.}\quad\quad \text{(9.1)}$$

For zero weights the sign convention is immaterial. Here $Y_{i}$ denotes an auxiliary comparison sign, distinct from the recorded evidence in Section 3. Let these $Y_{i}$ be independent signs with $\text{Pr}\text{(}Y_{i}\text{=}\text{+}1\text{)}\text{=}\beta_{i}\text{.}$ Then for every $t\text{,}$

$$\underset{Q\text{∈}\text{𝒬}_{\text{rect}}}{\text{max}}Q\text{(}S\text{≥}t\text{)}\text{=}\text{Pr}\left( \sum_{i\text{=}1}^{N}w_{i}Y_{i}\text{≥}t \right)\text{.}\quad\quad \text{(9.2)}$$

Proof. Any binary sequential law can be generated using independent uniforms $U_{i}$ and its conditional probabilities $q_{i}\text{(}X_{\text{<}i}\text{)}\text{,}$ with $X_{i}\text{=}\text{+}1$ when $U_{i}\text{≤}q_{i}\text{.}$ On the same uniforms put $Y_{i}\text{=}\text{+}1$ when $U_{i}\text{≤}\beta_{i}\text{.}$ Since $q_{i}\text{≤}\beta_{i}\text{,}$ $X_{i}\text{≤}Y_{i}$ coordinatewise on every realised path. Nonnegative $w_{i}$ imply $S\text{≤}\sum_{i}^{}w_{i}Y_{i}\text{.}$ This proves the tail inequality. The independent endpoint law $q_{i}\text{=}\beta_{i}$ is in $\text{𝒬}_{\text{rect}}$ and attains equality. End proof.

Similarly the exact minimum-direction optimiser has independent signs with plus probabilities $\alpha_{i}\text{:}$

$$\underset{Q\text{∈}\text{𝒬}_{\text{rect}}}{\text{max}}Q\text{(}S\text{≤}\text{−}t\text{)}\text{=}\text{Pr}\left( \sum_{i\text{=}1}^{N}w_{i}Y_{i}^{\text{low}}\text{≤}\text{−}t \right)\text{.}\quad\quad \text{(9.3)}$$

For $t\text{>}0$ the upper and lower events are disjoint under any one law, but their maximisers can be different laws. Therefore

$$r_{\text{*}}\text{(}t\text{)}\text{≤}\text{min}\text{\{}1\text{,}\underset{\beta}{\text{Pr}}\text{(}S\text{≥}t\text{)}\text{+}\underset{\alpha}{\text{Pr}}\text{(}S\text{≤}\text{−}t\text{)}\text{\}}\text{.}\quad\quad \text{(9.4)}$$

This is an upper bound, not generally an equality. In the two-coordinate example its uncapped sum is $9\text{/}16\text{+}9\text{/}16\text{=}9\text{/}8\text{,}$ while the sharp two-sided value is $3\text{/}4\text{.}$ At $t\text{=}0$ the absolute-tail probability is one and should be handled directly.

If original bounds depend on history, deterministic envelopes $\alpha_{i}$ and $\beta_{i}$ containing all admissible favourable-sign probabilities still give the same conservative domination. They do not in general give a sharp endpoint law for the original smaller family. No stochastic-order claim here applies to an arbitrary nonmonotone event.

# 10 Scalable conservative exponential bounds

Continue with the deterministic favourable-sign bounds $\alpha_{i}\text{,}\beta_{i}$ from Section 9, or valid deterministic envelopes. These formulas can be evaluated without enumerating arrays. They are upper bounds rather than exact two-sided probabilities.

For $\lambda\text{≥}0\text{,}$ define

$$\begin{matrix}
C_{\text{+}}\text{(}\lambda\text{)} & \text{=}\prod_{i\text{=}1}^{N}\text{\{}\text{(}1\text{−}\beta_{i}\text{)}e^{\text{−}\lambda w_{i}}\text{+}\beta_{i}e^{\lambda w_{i}}\text{\}}\text{,} \\
C_{\text{−}}\text{(}\lambda\text{)} & \text{=}\prod_{i\text{=}1}^{N}\text{\{}\text{(}1\text{−}\alpha_{i}\text{)}e^{\lambda w_{i}}\text{+}\alpha_{i}e^{\text{−}\lambda w_{i}}\text{\}}\text{.}
\end{matrix}\quad\quad \text{(10.1)}$$

The conditional exponential factor for $w_{i}X_{i}$ is at most the corresponding factor in $C_{\text{+}}\text{,}$ because $\text{exp}\text{(}\lambda w_{i}\text{)}\text{≥}\text{exp}\text{(}\text{−}\lambda w_{i}\text{)}\text{.}$ Iterated conditional expectation therefore gives $\text{𝔼}_{Q}\text{exp}\text{(}\lambda S\text{)}\text{≤}C_{\text{+}}\text{(}\lambda\text{)}$ under every admissible dependent law. Applying the same reasoning to $\text{−}S$ gives $C_{\text{−}}\text{.}$ The elementary pointwise inequality $\text{𝟏}\text{\{}S\text{≥}t\text{\}}\text{≤}\text{exp}\text{(}\lambda\text{(}S\text{−}t\text{)}\text{)}$ gives, for $t\text{>}0\text{,}$

$$\begin{matrix}
B_{\text{+}}\text{(}t\text{)} & \text{=}\underset{\lambda\text{≥}0}{\text{inf}}e^{\text{−}\lambda t}C_{\text{+}}\text{(}\lambda\text{)}\text{,} \\
B_{\text{−}}\text{(}t\text{)} & \text{=}\underset{\lambda\text{≥}0}{\text{inf}}e^{\text{−}\lambda t}C_{\text{−}}\text{(}\lambda\text{)}\text{,} \\
r_{\text{*}}\text{(}t\text{)} & \text{≤}\text{min}\text{\{}1\text{,}B_{\text{+}}\text{(}t\text{)}\text{+}B_{\text{−}}\text{(}t\text{)}\text{\}}\text{.}
\end{matrix}\quad\quad \text{(10.2)}$$

Any fixed nonnegative choices of $\lambda$ give valid upper bounds; numerical optimisation only improves tightness. A numerical minimum must not be rounded down and called a certificate. Logarithms avoid overflow, and certified outward arithmetic can preserve the required upper-bound direction. These are the usual exponential-moment arguments, with the assignment restrictions made explicit.

There is a simpler closed-form bound. Put

$$V\text{=}\sum_{i\text{=}1}^{N}w_{i}^{2}\text{,}\quad\quad M_{\text{+}}\text{=}\sum_{i\text{=}1}^{N}w_{i}\text{(}2\beta_{i}\text{−}1\text{)}\text{,}\quad\quad M_{\text{−}}\text{=}\sum_{i\text{=}1}^{N}w_{i}\text{(}1\text{−}2\alpha_{i}\text{)}\text{.}\quad\quad \text{(10.3)}$$

For $V\text{>}0\text{,}$

$$r_{\text{*}}\text{(}t\text{)}\text{≤}\text{min}\left( 1\text{,}\text{exp}\left( \text{−}\frac{{\text{[}{\text{(}t\text{−}M_{\text{+}}\text{)}}_{\text{+}}\text{]}}^{2}}{2V} \right)\text{+}\text{exp}\left( \text{−}\frac{{\text{[}{\text{(}t\text{−}M_{\text{−}}\text{)}}_{\text{+}}\text{]}}^{2}}{2V} \right) \right)\text{,}\quad\quad \text{(10.4)}$$

where $x_{\text{+}}\text{=}\text{max}\text{(}x\text{,}0\text{)}\text{.}$ To prove this without importing an independence premise, consider a sign taking values $\text{±}w$ with plus probability $p\text{.}$ Let $K\text{(}\lambda\text{)}$ be its log moment generating function. $K\text{(}0\text{)}\text{=}0\text{,}$ $K^{\text{′}}\text{(}0\text{)}\text{=}w\text{(}2p\text{−}1\text{)}\text{,}$ and $K^{\text{′}\text{′}}\text{(}\lambda\text{)}$ is the variance under exponential tilting. The tilted variable still lies at $\text{±}w\text{,}$ so $K^{\text{′}\text{′}}\text{(}\lambda\text{)}\text{≤}w^{2}\text{.}$ Integrating twice for $\lambda\text{≥}0$ gives $K\text{(}\lambda\text{)}\text{≤}\lambda w\text{(}2p\text{−}1\text{)}\text{+}\lambda^{2}w^{2}\text{/}2\text{.}$ Apply this to each deterministic endpoint factor in $C_{\text{+}}$ and $C_{\text{−}}\text{,}$ then minimise the resulting quadratic exponent over $\lambda\text{≥}0\text{.}$ This establishes the displayed bound.

The step “variance at most $w^{2}$” follows directly: a variable at $\text{±}w$ with tilted mean $m$ has variance $w^{2}\text{−}m^{2}\text{≤}w^{2}\text{.}$ Thus the proof is complete in this finite setting. This is the familiar bounded-increment exponential argument, not a new inequality.

For symmetric bounds $\text{ℓ}_{i}\text{=}1\text{/}2\text{−}\varepsilon_{i}$ and $u_{i}\text{=}1\text{/}2\text{+}\varepsilon_{i}\text{,}$ with $0\text{≤}\varepsilon_{i}\text{≤}1\text{/}2\text{,}$ define $D\text{=}\sum_{i}^{}2\varepsilon_{i}\text{|}a_{i}\text{|}\text{.}$ Then $M_{\text{+}}\text{=}M_{\text{−}}\text{=}D$ and

$$r_{\text{*}}\text{(}t\text{)}\text{≤}\text{min}\left( 1\text{,}2\text{exp}\left( \text{−}\frac{{\text{[}{\text{(}t\text{−}D\text{)}}_{\text{+}}\text{]}}^{2}}{2V} \right) \right)\text{.}\quad\quad \text{(10.5)}$$

This keeps the permitted predictable drift explicit. If $t\text{≤}D\text{,}$ this particular bound is trivial; that does not prove the exact recursion is trivial. If every conditional probability is exactly $1\text{/}2$ in the specified order, the chain rule gives a product of fair assignment signs conditional on the fixed experimental world. The familiar $D\text{=}0$ expression is then valid, while response dependence and feedback remain allowed under the sharp null. Fair unconditional marginals do not imply that case.

More generally $S$ minus its actual predictable conditional-mean sum is a martingale, but the compensator requires the actual conditional law. Subtracting only the unconditional $\text{𝔼}\text{[}S\text{]}\text{,}$ or estimating a propensity and ignoring estimation/model uncertainty, does not supply that martingale. The bounds above avoid this step by using an externally justified deterministic drift envelope.

If $V\text{=}0\text{,}$ $S$ is identically zero. Its observed absolute threshold is zero and its $p$-value is one. There is no division by zero case to regularise.

# 11 Exact cases and computational certification

## 11.1 Exact finite state calculations

For deterministic coordinate bounds and weights $a_{i}\text{=}m_{i}\Delta$ with integer $m_{i}\text{,}$ the partial sum lies on a finite lattice. Let $L\text{=}\sum_{i}^{}{\text{|}m_{i}\text{|}}\text{.}$ A dynamic program over at most $2L\text{+}1$ sum states per layer uses $O\text{(}NL\text{)}$ arithmetic operations and $O\text{(}L\text{)}$ memory for the value alone. Backtracking an optimal policy or saving all layers takes more memory. Sparse reachable sums, parity and symmetry can reduce this count. This is pseudopolynomial in the integer weight magnitudes, not polynomial in their binary encoding length.

For equal-magnitude weights, count states give a particularly small exact recursion. For known independent but nonidentical probabilities, standard convolution of the weighted two-point distributions gives the known-law distribution. For a documented fixed-count uniform assignment, the state includes the remaining count; the next plus probability is the remaining number of plus placements divided by the remaining coordinates. At some states it is zero or one. Known independent blocks with known within-block laws can instead convolve block contribution distributions. None of these shortcuts may be borrowed solely because it is convenient for a particular dataset.

Conditioning on an assignment total can be legitimate when the model establishes the corresponding conditional law. For example, under independent common-probability Bernoulli assignments, conditional on the total number of ones every array with that total has equal probability, regardless of the unknown common probability. This follows because each such array has the same product probability $p^{k}{\text{(}1\text{−}p\text{)}}^{N\text{−}k}\text{.}$ Fair marginals alone do not imply this conditional uniformity. Observing a total does not certify a permutation design.

## 11.2 Why finite does not mean feasible at large sample sizes

The full binary assignment tree has exponentially many leaves. A general history-dependent contract may require exponentially many histories even to specify its input. With arbitrary unequal rational weights, distinct partial sums can also grow exponentially. Clearing denominators can create enormous integer weights, so the $O\text{(}NL\text{)}$ statement is not a promise of practicality.

Arithmetic-operation counts omit bit complexity. Exact rational probabilities can acquire large numerators and denominators through multiplication and addition. Real weights must have a specified exact finite representation or a certified numerical enclosure. Ordinary floating-point equality at the inclusive tail threshold can otherwise change the event. A mathematically exact recurrence is not, by itself, a verified numerical implementation or a scalable product interface.

## 11.3 Safe weight coarsening

Choose computational weights ${\widetilde{a}}_{i}$ and certify

$$\eta\text{=}\sum_{i\text{=}1}^{N}{\text{|}a_{i}\text{−}{\widetilde{a}}_{i}\text{|}}\text{.}\quad\quad \text{(11.1)}$$

For every full array, $\text{|}S\text{(}z\text{)}\text{−}\widetilde{S}\text{(}z\text{)}\text{|}\text{≤}\eta$ by the triangle inequality. Hence

$$\text{\{}\text{|}S\text{(}z\text{)}\text{|}\text{≥}t\text{\}}\text{⊆}\text{\{}\text{|}\widetilde{S}\text{(}z\text{)}\text{|}\text{≥}\text{max}\text{(}0\text{,}t\text{−}\eta\text{)}\text{\}}\text{.}\quad\quad \text{(11.2)}$$

For an unchanged assignment family, an exact or upper-bounded coarse-lattice tail at the lowered threshold is a conservative bound for the original tail. A data-dependent computational choice of coarse weights also remains conservative if the certificate holds pointwise for the same fixed original statistic and assignment family; it must not redefine the inferential target. Use the original observed threshold $t\text{=}\text{|}S\text{(}z_{\text{obs}}\text{)}\text{|}\text{;}$ merely rounding the weights and testing at their newly observed threshold has no such automatic guarantee. If $t\text{≤}\eta$ the displayed outer event is the full space.

This compression is directly usable with deterministic-coordinate bounds. If bounds depend on the unrounded partial sum or other original state, the computational state must retain enough information or use a conservative envelope over all original histories represented by a coarse state. The coarsening error bound does not by itself justify merging assignment states.

## 11.4 Branch pruning and finite resource limits

At partial sum $s\text{,}$ let $R_{\text{rem}}$ be the sum of the absolute remaining weights. All terminal sums lie between $s\text{−}R_{\text{rem}}$ and $s\text{+}R_{\text{rem}}\text{.}$ If $\text{|}s\text{|}\text{+}R_{\text{rem}}\text{<}t\text{,}$ the continuation tail value is exactly zero. If $\text{|}s\text{|}\text{−}R_{\text{rem}}\text{≥}t\text{,}$ it is exactly one. These are safe sufficient pruning rules; gaps in the attainable weighted sums may allow additional pruning.

An unfinished subtree can be bounded by $\text{[}0\text{,}1\text{]}\text{.}$ Propagating lower and upper continuation bounds through the monotone Bellman update gives a certified bracket at the root. A resource-limited run may report its upper endpoint as a conservative $p$-value or report that the bracket is too wide for the requested decision. It must not return the best policy found as though it were an upper bound. This permits a declared finite computation budget without silently dropping possible assignments.

## 11.5 Monte Carlo statements and their limits

For a known exact assignment law $Q\text{,}$ generate $B$ independent reference arrays from $Q$ and include the observed assignment in the rank comparison. Conditional on the fixed null trajectory, the $B\text{+}1$ statistics are exchangeable. Therefore

$$p_{\text{MC}}\text{=}\frac{1\text{+}\sum_{b\text{=}1}^{B}\text{𝟏}\text{\{}T\text{(}Z^{\text{(}b\text{)}}\text{)}\text{≥}T\text{(}z_{\text{obs}}\text{)}\text{\}}}{B\text{+}1}\quad\quad \text{(11.3)}$$

is a valid conservative Monte Carlo $p$-value. To see this, among any fixed $B\text{+}1$ statistic values, at most $\text{⌊}\alpha\text{(}B\text{+}1\text{)}\text{⌋}$ indices can have their inclusive upper rank divided by $B\text{+}1$ at most $\alpha\text{;}$ ties can only reduce this number. Exchangeability assigns the observed index no privileged position, so its rejection probability is at most $\alpha\text{.}$ The leading one and tie rule are part of the procedure, not cosmetic small-sample corrections. A simulator for a guessed law has only that guessed-law interpretation.

Simulating a selected candidate adversarial policy does not upper-bound the robust optimum. Nor does taking the maximum over a finite, unverified collection of policies prove a maximum over every admissible policy. When a valid deterministic domination reduces the problem to one or two known product tails, simulation can approximate those tails, but an approximate number should not be passed off as a certified upper probability.

A general way to retain conservative validity is to produce, conditional on each observed dataset, a randomised nonnegative upper bound $U$ for $p_{\text{*}}\text{(}z_{\text{obs}}\text{)}$ that fails with probability at most $\delta\text{,}$ using independent computational randomness and a justified confidence procedure. Replace $U$ by $\text{max}\text{(}0\text{,}U\text{)}$ first if necessary. Then $\text{min}\text{(}1\text{,}U\text{+}\delta\text{)}$ is valid. For $\delta\text{≤}\alpha\text{<}1\text{,}$ the rejection event equals $\text{\{}U\text{+}\delta\text{≤}\alpha\text{\}}\text{;}$ it lies inside $\text{\{}p_{\text{*}}\text{≤}\alpha\text{−}\delta\text{\}}$ except on the failure event, so its probability is at most $\text{(}\alpha\text{−}\delta\text{)}\text{+}\delta\text{.}$ For $\alpha\text{<}\delta$ the event is empty because $U\text{≥}0\text{.}$ For $\alpha\text{=}1$ validity is the trivial probability bound by one. This is only useful when the computational procedure genuinely bounds the full robust quantity, not a lower-bound candidate. Simultaneous error across two simulated tails or several bounds must be included in $\delta\text{.}$

# 12 Conditional inference from block complement symmetry

A test can sometimes be calibrated without identifying the entire assignment law. A sufficiently supported symmetry can determine the reference distribution within the observed assignment orbit, while leaving the probabilities of different orbits unknown. This section gives one finite example. It specifies an additional model; it does not assert that any particular experiment satisfies it.

## 12.1 The conditional symmetry contract

Fix legitimate inputs $X$ and a potential-response world $u\text{,}$ excluding the assignment randomisation draws. Partition the finite coordinate set into $M$ prespecified nonempty blocks $I_{1}\text{,}\text{…}\text{,}I_{M}\text{.}$ The group

$$\text{𝒢}\text{=}\text{\{}\text{−}1\text{,}\text{+}1\text{\}}^{M}\quad\quad \text{(12.1)}$$

acts on a sign array $x$ by multiplying every coordinate in block $I_{b}$ by $e_{b}\text{,}$ for $e\text{∈}\text{𝒢}\text{.}$ Write this transformed array as $ex\text{.}$ Require the legitimate assignment set $\Omega$ to be closed under these transformations.

Let $Q$ be the conditional assignment law given $\text{(}X\text{,}u\text{)}\text{.}$ For each block, let $f_{b}$ flip that block alone. The required symmetry is invariance of the full joint law under every such generator:

$$Q\text{\{}A\text{=}x\text{\}}\text{=}Q\text{\{}A\text{=}f_{b}x\text{\}}\quad \text{for every }x\text{∈}\Omega\quad \text{and every }b\text{.}\quad\quad \text{(12.2)}$$

Composition then gives the same equality for every $e\text{∈}\text{𝒢}\text{.}$ Symmetry of each block’s marginal distribution is a different, insufficient premise.

Assume the sharp recorded-trajectory null on the relevant assignments, including availability and every ingredient held fixed by the statistic. Thus the real coefficients $a_{i}\text{=}a_{i}\text{(}X\text{,}u\text{)}$ remain fixed under all these transformations. The block partition and conditioning scheme must also be fixed appropriately. Response independence, no interference and no carryover are not required.

## 12.2 Theorem and proof

Define the block contributions and the inclusive orbit probability by

$$C_{b}\text{(}A\text{)}\text{=}\sum_{i\text{∈}I_{b}}^{}a_{i}A_{i}\text{,}\quad\quad \text{(12.3)}$$

$$p_{\text{block}}\text{(}A\text{)}\text{=}2^{\text{−}M}\sum_{e\text{∈}\text{𝒢}}^{}\text{𝟏}\text{\{}\text{|}\sum_{b\text{=}1}^{M}e_{b}C_{b}\text{(}A\text{)}\text{|}\text{≥}\text{|}\sum_{b\text{=}1}^{M}C_{b}\text{(}A\text{)}\text{|}\text{\}}\text{.}\quad\quad \text{(12.4)}$$

For every $\alpha\text{∈}\text{[}0\text{,}1\text{]}$ and every positive-probability orbit $O\text{,}$

$$Q\text{\{}p_{\text{block}}\text{(}A\text{)}\text{≤}\alpha\text{∣}O\text{(}A\text{)}\text{=}O\text{\}}\text{≤}\alpha\text{,}\quad\quad \text{(12.5)}$$

where $O\text{(}A\text{)}\text{=}\text{\{}eA\text{:}e\text{∈}\text{𝒢}\text{\}}\text{.}$ Consequently the unconditional rejection probability under $Q$ is also at most $\alpha\text{.}$

Proof. Because every block is nonempty and every coordinate is a sign, a nonidentity block flip changes at least one coordinate. The action is therefore free, so each orbit has exactly $2^{M}$ distinct arrays. Joint-law invariance gives every array in a particular orbit the same mass. Conditional on a positive-probability orbit, the assignment is uniform, regardless of that orbit’s total probability.

Put $T\text{(}x\text{)}\text{=}\text{|}\sum_{i}^{}a_{i}x_{i}\text{|}\text{.}$ Fixed coefficients give $T\text{(}eA\text{)}\text{=}\text{|}\sum_{b}^{}e_{b}C_{b}\text{(}A\text{)}\text{|}\text{,}$ so the displayed probability is the inclusive upper rank of $T\text{(}A\text{)}$ divided by the orbit size. Among $m$ fixed statistic values, at most $\text{⌊}\alpha m\text{⌋}$ positions have inclusive upper rank at most $\alpha m\text{;}$ ties cannot increase this number. Uniformity within the orbit proves the conditional inequality. Averaging over the orbits proves the unconditional inequality. Averaging over fixed worlds preserves it if the contract holds in every world under the sharp null. End proof.

Here exactness means finite-sample level control, allowing conservativeness from ties and discrete attainable levels. Orientations producing identical statistic values retain their multiplicities. Uniform weighting of distinct statistic values would be a different procedure.

## 12.3 Independent orientations and dependent block patterns

Let $V$ be any jointly distributed collection of block sign patterns, conditional on $\text{(}X\text{,}u\text{)}\text{.}$ Its blocks may be dependent. Given $\text{(}V\text{,}X\text{,}u\text{)}\text{,}$ let $E$ be uniform on $\text{𝒢}\text{,}$ equivalently a collection of mutually independent fair block signs, and set $A\text{=}EV\text{.}$ For any fixed $g\text{∈}\text{𝒢}\text{,}$ the sign vector $gE$ is again uniform and independent of $V$ under the same conditioning. Hence $gA$ and $A$ have the same conditional law. This proves the required joint invariance without independent coordinate assignments or independent block patterns.

The representation does not require literal block-orientation coins in a physical implementation. Under an invariant law, orient each block canonically so that its first coordinate is positive. Conditional on the entire canonical pattern collection, the original anchor signs are uniform on $\text{𝒢}\text{.}$ The assignment symmetry, rather than a particular implementation of it, is the premise needing support.

This family can admit deterministic dependence within a block. For example, give each of several two-coordinate blocks the fixed pattern $\text{(}\text{+}1\text{,}\text{+}1\text{)}\text{,}$ then orient the blocks independently and fairly. Within a block its second sign is determined by its first. A reached full-prefix conditional probability is therefore zero or one. It violates every finite interval

$$\text{[}\frac{1}{1\text{+}\Gamma}\text{,}\frac{\Gamma}{1\text{+}\Gamma}\text{]}\text{,}\quad\quad 1\text{≤}\Gamma\text{<}\text{∞}\text{,}\quad\quad \text{(12.6)}$$

although the block test remains valid. Conversely, for $\Gamma\text{>}1\text{,}$ a product law with nonfair coordinate biases inside this interval need not be block-complement invariant. The block-symmetry and finite conditional-bound families are therefore not nested in general.

## 12.4 Synthetic separation from marginal block symmetry

Consider six nonzero block contributions that are equal and aligned. Only the two unanimous orientations attain the largest absolute sum, so the inclusive orbit probability is

$$\frac{2}{2^{6}}\text{=}\frac{1}{32}\text{.}\quad\quad \text{(12.7)}$$

Now orient all six fixed block patterns using one common fair sign $H\text{.}$ Each block separately has a symmetric marginal distribution, and the whole array has global-complement symmetry. Yet its joint law contains only two of the independently flipped orientations. The unsupported six-block reference probability is $1\text{/}32$ at both possible observations, so it rejects at level $0.05$ with probability one. The valid two-element global-complement reference gives probability one. This is a synthetic failure of an omitted premise, not a reconstruction of an actual assignment process.

With $k\text{>}0$ nonzero block contributions, the smallest possible inclusive two-sided orbit probability is $2\text{/}2^{k}\text{,}$ attained when those contributions are aligned in sign. Zero-contribution flips duplicate values equally. If every contribution is zero, the probability is one. A single global-complement block is always uninformative for the absolute statistic. Choosing more, finer blocks requires stronger joint invariance; the improved resolution is not available merely by changing the partition.

## 12.5 Classical attribution and the weaker statistic condition

This is a specialisation of classical finite-group testing. Hemerik and Goeman’s section 2 gives group-based level control under a transformed-statistic-vector invariance condition weaker than full-data invariance. That weaker condition can justify a rank test without making the actual assignment orbit uniform. The proof here deliberately retains the stronger joint assignment-law premise.

Jesse Hemerik and Jelle Goeman, *Exact testing with random permutations*, TEST 27, 811–825 (2018), section 2, Definition 1 and Theorem 1. DOI: [10.1007/s11749-017-0571-1](https://doi.org/10.1007/s11749-017-0571-1). [Open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6405018/).

# 13 Proof status and use

The arguments in this companion are ordinary finite mathematical proofs, independently challenged with exact synthetic controls. They are not a newly kernel-checked Lean package. Finite checks supplement rather than replace the proofs. Existing programme results on constructed row laws, observed-policy laws, asymptotic tests and subprobability budgets retain their previous ownership; none is assumed to authenticate an actual assignment mechanism.

A scientific application must bind the intended assignment coordinate, legitimate conditioning inputs, population and schedule, full response and availability null, law family, statistic and numerical procedure. The model can be useful even when its empirical premises remain provisional, provided that conditional status accompanies the result.
